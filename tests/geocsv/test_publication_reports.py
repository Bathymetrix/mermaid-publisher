"""Insertion-aware exact CSV diffs and immutable comparison evidence."""
import io
import json
import tempfile
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'scripts/geocsv'))
from _reports import data_diff, source_rows, publication_reports
from inspect_snapshot import json_bytes
from geocsv.schema_helpers import HEADER


class Diffs(unittest.TestCase):
    def test_producer_revision_only_keeps_exact_diff_without_metadata_flag(self):
        for method in ('Derivation:Recording', 'Interpolation:Crossing-Ascent',
                       'Interpolation:Crossing-Descent'):
            for quote in ('', '"'):
                old = f'{quote}{method}:automaid-v4.6.2{quote},unchanged\n'
                new = old.replace('v4.6.2', 'v4.9.2')
                with self.subTest(method=method, quote=quote):
                    diff, schema, changed = data_diff((HEADER+old).encode(), (HEADER+new).encode())
                    self.assertEqual(diff, f'-0,{old}+0,{new}'.encode())
                    self.assertFalse(schema or changed)

    def test_producer_revision_does_not_hide_other_changes_or_deletions(self):
        old = 'Derivation:Recording:automaid-v4.6.2,unchanged\n'
        new = old.replace('v4.6.2', 'v4.9.2')
        for content in (new.replace('unchanged', 'changed'), '', new.replace('\n', '\r\n')):
            with self.subTest(content=content):
                self.assertTrue(data_diff((HEADER+old).encode(), (HEADER+content).encode())[2])
        # Producer-like strings elsewhere in a row and sensor revisions remain metadata.
        for row in ('Measurement:Position:sensor-v1,value\n', 'a,automaid-v1\n'):
            self.assertTrue(data_diff((HEADER+row).encode(), (HEADER+row.replace('v1','v2')).encode())[2])
        before = HEADER + old + 'other,row\n'
        after = HEADER + 'other,row\n' + new
        self.assertTrue(data_diff(before.encode(), after.encode())[2])

    def test_insert_does_not_report_shifted_rows(self):
        before = (HEADER + 'a,b\nc,d\n').encode()
        after = (HEADER + 'a,b\nx,y\nc,d\n').encode()
        diff, schema, changed = data_diff(before, after)
        self.assertEqual(diff, b'+1,x,y\n')
        self.assertFalse(schema or changed)

    def test_change_delete_and_comments(self):
        before = (HEADER + 'a,b\nc,d\n').encode()
        diff, _, changed = data_diff(before, (HEADER + 'a,z\n').encode())
        self.assertEqual(diff, b'-0,a,b\n-1,c,d\n+0,a,z\n')
        self.assertTrue(changed)
        self.assertEqual(data_diff(before, before.replace(b'#dataset:', b'#note: ignored\n#dataset:'))[0], b'')

    def test_multiline_row_and_schema_mismatch(self):
        before = (HEADER + 'a,"b\nc"\n').encode()
        self.assertEqual(len(source_rows(before)[1]), 1)
        diff, schema, changed = data_diff(before, before.replace(b'schema: MERMAID GeoCSV v1.0.0-rc1', b'schema: 2.0.0'))
        self.assertTrue(schema)
        self.assertIn(b'simple diff cannot be made', diff)
        self.assertFalse(changed)

    def test_reports_enforce_overrides_and_bind_previous_snapshot(self):
        import hashlib
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            candidate = root / 'testing/snapshots/2026-01-01T00-00-00.000000Z'
            candidate.mkdir(parents=True)
            previous_id = '2025-01-01T00:00:00.000000Z'
            previous = (HEADER + 'a,b\n').encode()
            current = (HEADER + 'a,c\n').encode()
            def manifest(release, content):
                return {'release_id': release, 'testing_only': True, 'files': [{
                    'instrument_id': 'P0006', 'filename': 'P0006.geocsv',
                    'size_bytes': len(content), 'sha256': hashlib.sha256(content).hexdigest(),
                    'provenance': {'source_path': 'serial/geo_DET_REQ.csv'}}]}
            (candidate / 'manifest.json').write_bytes(json_bytes(manifest('2026-01-01T00:00:00.000000Z', current)))
            (candidate / 'P0006.geocsv').write_bytes(current)
            report = root / 'report.json'
            report.write_bytes(json_bytes({'instruments': [{'instrument_id': 'P0006', 'coverage': [
                {'source_line': 11, 'mseed_filenames': ['a.mseed', 'b.mseed']}]}]}))
            objects = {'manifest.json': json_bytes(manifest(previous_id, previous)), 'P0006.geocsv': previous}
            class Store:
                def get(self, key):
                    return {'Body': io.BytesIO(objects[key.rsplit('/', 1)[1]])}
            with self.assertRaisesRegex(ValueError, 'allow-metadata-changes'):
                publication_reports(candidate, report, Store(), 'geocsv/testing', previous_id)
            paths = publication_reports(candidate, report, Store(), 'geocsv/testing', previous_id,
                                        allow_metadata_changes=True)
            files = {name: path.read_bytes() for name, path in paths}
            self.assertIn(b'geocsv_line_number,mseed_filename(s)\n11,a.mseed,b.mseed\n', files['P0006.mapping.csv'])
            self.assertEqual(json.loads(files['comparison.json'])['previous_release_id'], previous_id)
            # Schema mismatch is separately opt-in.
            objects['P0006.geocsv'] = previous.replace(b'schema: MERMAID GeoCSV v1.0.0-rc1', b'schema: 2.0.0')
            objects['manifest.json'] = json_bytes(manifest(previous_id, objects['P0006.geocsv']))
            with self.assertRaisesRegex(FileExistsError, 'conflicting immutable'):
                publication_reports(candidate, report, Store(), 'geocsv/testing', previous_id,
                                    allow_metadata_changes=True)
            import shutil
            other = root / 'other/testing/snapshots' / candidate.name
            shutil.copytree(candidate, other)
            with self.assertRaisesRegex(ValueError, 'allow-schema-change'):
                publication_reports(other, report, Store(), 'geocsv/testing', previous_id)
            paths = publication_reports(other, report, Store(), 'geocsv/testing', previous_id,
                                        allow_schema_change=True)
            self.assertIn(b'simple diff cannot be made', dict(paths)['P0006.diff'].read_bytes())
