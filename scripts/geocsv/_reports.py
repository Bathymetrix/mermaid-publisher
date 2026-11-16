"""Deterministic publication mapping and exact source-row diffs."""

import csv
from difflib import SequenceMatcher
import hashlib
import io
import json
from pathlib import Path
import re

from inspect_snapshot import PAYLOAD_SCHEMA, check_manifest, fingerprint, json_bytes, read_json, release_component


def _schema_declaration(content):
    """Read the explicit application schema, without interpreting source rows."""
    lines = content.decode('utf-8').splitlines()
    if not lines or not re.fullmatch(r'#\s*dataset\s*:\s*GeoCSV 2\.0\s*', lines[0]):
        return None
    schemas = []
    for line in lines[1:]:
        if not line.startswith('#'):
            break
        key, separator, value = line[1:].partition(':')
        if separator and key.strip() == 'schema':
            schemas.append(value.strip())
    return schemas[0] if len(schemas) == 1 else None


def source_rows(content):
    """Return complete CSV row strings, preserving bytes."""
    text = content.decode('utf-8')
    lines = io.StringIO(text, newline='').readlines()
    if _schema_declaration(content) != PAYLOAD_SCHEMA:
        raise ValueError(f'comparison source requires {PAYLOAD_SCHEMA}')
    start = 0
    while start < len(lines) and lines[start].startswith('#'):
        start += 1
    reader = csv.reader(iter(lines[start:]), strict=True)
    next(reader)  # Column header, not a data row.
    previous = reader.line_num
    rows = []
    for _ in reader:
        rows.append(''.join(lines[start + previous:start + reader.line_num]))
        previous = reader.line_num
    return rows


def data_diff(previous, current):
    """Return exact -/+ source-index rows and whether previous rows changed."""
    previous_rows = source_rows(previous) if previous is not None else []
    current_rows = source_rows(current) if current is not None else []
    output = []
    changed = False
    for tag, first, stop, new_first, new_stop in SequenceMatcher(
            None, previous_rows, current_rows, autojunk=False).get_opcodes():
        if tag in ('replace', 'delete'):
            changed = True
            output.extend(f'-{index},{previous_rows[index]}' for index in range(first, stop))
        if tag in ('replace', 'insert'):
            output.extend(f'+{index},{current_rows[index]}' for index in range(new_first, new_stop))
    return ''.join(output).encode('utf-8'), changed


def publication_reports(candidate, report, store, object_prefix, previous_id, *,
                        already_selected=False, allow_metadata_changes=False):
    """Freeze reports against the previous pointer observed before activation."""
    candidate = Path(candidate)
    manifest = read_json(candidate / 'manifest.json')
    component = release_component(manifest['release_id'])
    directory = candidate.parent.parent / 'reports' / component
    comparison_path = directory / 'comparison.json'
    if already_selected:
        # An identical retry compares against its original predecessor, not itself.
        if not comparison_path.exists():
            raise ValueError('selected snapshot lacks local comparison evidence; inspect publication state')
        previous_id = read_json(comparison_path)['previous_release_id']
    baseline = {}
    previous_manifest_hash = None
    if previous_id is not None:
        prefix = f'{object_prefix}/releases/{release_component(previous_id)}/'
        response = store.get(prefix + 'manifest.json')
        if response is None:
            raise ValueError('previous latest manifest is unavailable')
        with response['Body'] as stream:
            manifest_bytes = stream.read()
        previous_manifest = json.loads(manifest_bytes)
        entries = check_manifest(previous_manifest)
        if previous_manifest['release_id'] != previous_id:
            raise ValueError('previous manifest identity differs')
        previous_manifest_hash = hashlib.sha256(manifest_bytes).hexdigest()
        for entry in entries:
            response = store.get(prefix + entry['filename'])
            if response is None:
                raise ValueError('previous snapshot payload is unavailable')
            with response['Body'] as stream:
                content = stream.read()
            if (len(content), hashlib.sha256(content).hexdigest()) != (entry['size_bytes'], entry['sha256']):
                raise ValueError('previous snapshot payload differs from its manifest')
            baseline[entry['instrument_id']] = content
    payloads = {entry['instrument_id']: (candidate / entry['filename']).read_bytes()
                for entry in manifest['files']}
    outputs = {}
    removed = False
    for instrument in sorted(baseline.keys() | payloads.keys()):
        content, changed_rows = data_diff(baseline.get(instrument), payloads.get(instrument))
        outputs[f'{instrument}.diff'] = content
        removed |= changed_rows
    evidence = read_json(report)
    for instrument in evidence.get('instruments', []):
        stream = io.StringIO(newline='')
        writer = csv.writer(stream, lineterminator='\n')
        writer.writerow(['geocsv_line_number', 'mseed_filename(s)'])
        for row in instrument['coverage']:
            writer.writerow([row['source_line'], *row['mseed_filenames']])
        outputs[f"{instrument['instrument_id']}.mapping.csv"] = stream.getvalue().encode()
    # Make the exact diff available for review even when its policy blocks upload.
    directory.mkdir(parents=True, exist_ok=True)
    for name, content in outputs.items():
        path = directory / name
        if path.exists():
            if path.is_symlink() or path.read_bytes() != content:
                raise FileExistsError(f'conflicting immutable publication report: {path}')
        else:
            with path.open('xb') as stream:
                stream.write(content)
    if removed and not allow_metadata_changes:
        raise ValueError(f'previous data rows changed or were deleted; use --allow-metadata-changes explicitly; review {directory}')
    comparison = {'schema_version': 1, 'release_id': manifest['release_id'],
                  'manifest_sha256': fingerprint(candidate / 'manifest.json')[1],
                  'validation_sha256': fingerprint(report)[1],
                  'previous_release_id': previous_id,
                  'previous_manifest_sha256': previous_manifest_hash,
                  'allow_metadata_changes': allow_metadata_changes,
                  'files': {name: hashlib.sha256(content).hexdigest() for name, content in outputs.items()}}
    comparison_bytes = json_bytes(comparison)
    if {path.name for path in directory.iterdir()} - (outputs.keys() | {'comparison.json'}):
        raise FileExistsError('unexpected files in immutable publication reports')
    if comparison_path.exists():
        if comparison_path.is_symlink() or comparison_path.read_bytes() != comparison_bytes:
            raise FileExistsError('conflicting immutable comparison evidence')
    else:
        with comparison_path.open('xb') as stream:
            stream.write(comparison_bytes)
    outputs['comparison.json'] = comparison_bytes
    return [(name, directory / name) for name in sorted(outputs)]
