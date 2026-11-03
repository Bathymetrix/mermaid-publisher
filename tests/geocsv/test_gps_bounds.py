"""Publication policy: GPS observations bracket all normal GeoCSV rows."""

import sys
from pathlib import Path
import unittest

from geocsv.schema_helpers import HEADER
from mermaid import geocsv

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'scripts/geocsv'))
from _evidence import check_gps_bounds


class GPSBounds(unittest.TestCase):
    first = 'Measurement:Position:test,2020-01-01T00:00:00.000000Z,MH,PTEST,,,,12,-150,,,MERMAID_test,,,,\n'
    last = first.replace('00:00:00.000000Z', '01:00:00.000000Z')
    pressure = 'Measurement:Pressure-Absolute:test,TIME,MH,PTEST,,,,,,,1000,MERMAID_test,,,,\n'
    recording = 'Derivation:Recording:automaid-v0,TIME,MH,PTEST,00,BDH,Q,12,-150,0,1000,MERMAID_test,20,4,,0\n'
    crossing = 'Interpolation:Crossing-Ascent:automaid-v0,TIME,MH,PTEST,,,,12,-150,,5000,MERMAID_test,,,,\n'

    def check(self, rows):
        check_gps_bounds(geocsv.read((HEADER + rows).encode()))

    def test_inclusive_gps_bounds(self):
        for row in (self.pressure, self.recording, self.crossing):
            for time in ('00:00:00.000000Z', '00:30:00.000000Z', '01:00:00.000000Z'):
                with self.subTest(row=row, time=time):
                    self.check(self.first + row.replace('TIME', '2020-01-01T' + time) + self.last)

    def test_all_row_types_outside_gps_bounds_fail(self):
        for row in (self.pressure, self.recording, self.crossing):
            for time in ('2019-12-31T23:59:59.999999Z', '2020-01-01T01:00:00.000001Z'):
                with self.subTest(row=row, time=time), self.assertRaisesRegex(ValueError, 'outside GPS time bounds'):
                    self.check(self.first + row.replace('TIME', time) + self.last)

    def test_missing_gps_fails_but_empty_dataset_is_allowed(self):
        with self.assertRaisesRegex(ValueError, 'requires GPS measurements'):
            self.check(self.recording.replace('TIME', '2020-01-01T00:30:00.000000Z'))
        self.check('')
