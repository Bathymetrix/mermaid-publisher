"""GPS time bounds, Recording coverage and producer-supplied clash evidence."""

from pathlib import Path

from inspect_snapshot import fingerprint, read_json


def check_gps_bounds(tables):
    """Require GPS measurements to bracket every row, with inclusive bounds."""
    for table in tables:
        if table.empty:
            continue
        gps = table.loc[table.MethodIdentifier.str.startswith('Measurement:Position:')]
        if gps.empty:
            raise ValueError('nonempty GeoCSV requires GPS measurements for time bounds')
        first, last = gps.Time.min(), gps.Time.max()
        outside = table.loc[(table.Time < first) | (table.Time > last)]
        if not outside.empty:
            lines = table.attrs['geocsv'].line_numbers
            indices = list(outside.index)
            raise ValueError(f'{len(indices)} GeoCSV rows outside GPS time bounds; '
                             f'source indices {indices[:10]}, '
                             f'lines {[lines[index] for index in indices[:10]]}')


def recording_evidence(candidate, entry, tables, pairs):
    """Describe every Recording row and verify the bound producer report.

    No producer algorithms or MER inputs are used here.
    """
    check_gps_bounds(tables)
    rows = {}
    for dataset_index, table in enumerate(tables):
        metadata = table.attrs['geocsv']
        recordings = table.loc[table.MethodIdentifier.str.startswith('Derivation:Recording:')]
        for index in recordings.index:
            rows[(dataset_index, int(index))] = {
                'source_index': int(index), 'source_line': metadata.line_numbers[index],
                'mseed_filenames': []}
    seen = set()
    for pair in pairs:
        if pair['status'] != 'passed':
            continue
        name = pair['mseed_filename']
        if name in seen:
            raise ValueError(f'ambiguous MiniSEED basename: {name}')
        seen.add(name)
        association = pair['association']
        key = (association['dataset_index'], association['source_index'])
        if key not in rows or association.get('source_line') != rows[key]['source_line']:
            raise ValueError('association does not identify a Recording row')
        rows[key]['mseed_filenames'].append(name)
    coverage = list(rows.values())
    for row in coverage:
        row['mseed_filenames'].sort()
    missing = [row['source_index'] for row in coverage if not row['mseed_filenames']]
    if missing:
        raise ValueError(f'unmatched Recording source indices: {missing}')
    path = Path(candidate) / f"{entry['instrument_id']}.clash.json"
    producer = read_json(path)
    if (not isinstance(producer, dict) or type(producer.get('schema_version')) is not int
            or producer['schema_version'] != 1 or producer.get('geocsv_sha256') != entry['sha256']
            or not isinstance(producer.get('clashes'), list)):
        raise ValueError('missing, unsupported or stale producer clash report')
    by_index = {row['source_index']: row for row in coverage}
    indices = set()
    for clash in producer['clashes']:
        if not isinstance(clash, dict) or type(clash.get('source_index')) is not int:
            raise ValueError('invalid clash source index')
        index = clash['source_index']
        row = by_index.get(index)
        if index in indices or row is None or type(clash.get('source_line')) is not int:
            raise ValueError('duplicate or invalid clash row reference')
        indices.add(index)
        if (clash['source_line'] != row['source_line']
                or clash.get('mseed_filenames') != row['mseed_filenames']):
            raise ValueError('producer clash line/filenames differ from waveform associations')
        # Header differences, variant counts and raw payload equality are producer
        # evidence only. Do not interpret or recalculate them here.
    return {'recording_rows': len(coverage), 'coverage': coverage,
            'clash_report': {'filename': path.name, 'sha256': fingerprint(path)[1],
                             'content': producer, 'status': 'verified'}}
