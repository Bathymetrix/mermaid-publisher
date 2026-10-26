"""Retain former exporter checks as publisher-only verification.

All examples are synthetic. No canonical waveform source or archive is opened.
The same checks run with the exact frozen consumer and the current consumer.
"""

from dataclasses import replace
import inspect
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd
from obspy import Trace, Stream, UTCDateTime
from obspy.io.sac import SACTrace
from mermaid import geocsv

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts/geocsv"))
from _verify_sac import write_verified_sac


class SACVerification(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.output = self.root / "checked.sac"
        self.current = "create_sac_header" in inspect.signature(geocsv.associate).parameters
        self.trace = self.associated()

    def associated(self, *, clipped=False, empty_location=False, submicrosecond=False):
        start = "2025-01-01T00:00:00.123456789Z" if submicrosecond else "2025-01-01T00:00:00Z"
        location = "" if empty_location else "00"
        content = (
            "#dataset: GeoCSV\n"
            "#field_type: string,datetime,string,string,string,string,string,float,float,float,float,integer\n"
            "#field_unit: unitless,iso8601,unitless,unitless,unitless,unitless,unitless,degrees_north,degrees_east,mbar,hertz,unitless\n"
            "MethodIdentifier,StartTime,Network,Station,Location,Channel,DataQuality,Latitude,Longitude,WaterPressure,SampleRate,SampleCount\n"
            f"Algorithm(event):synthetic:v0,{start},MH,SYN01,{location},BDH,Q,12,-150,10000,20,4\n"
        ).encode()
        trace = Trace(np.array([0, 1, -10, 16777217], dtype=np.int32), header={
            "network": "MH", "station": "SYN01", "location": location, "channel": "BDH",
            "starttime": UTCDateTime(ns=pd.Timestamp(start).value), "sampling_rate": 20,
            "calib": 2.5,
        })
        if clipped:
            trace.stats.starttime += trace.stats.delta
            trace.data = trace.data[1:].copy()
        options = {"create_sac_header": True} if self.current else {}
        geocsv.associate(trace, geocsv.read(content), allow_first_segment=clipped, **options)
        return trace

    def rejected(self, trace, expression=None):
        before = trace.copy()
        with self.assertRaisesRegex(ValueError, expression or ".*"):
            write_verified_sac(trace, self.output)
        self.assertFalse(self.output.exists())
        self.assertEqual(trace.stats, before.stats)
        np.testing.assert_array_equal(trace.data, before.data)

    def test_roundtrip_precision_identity_calibration_and_no_mutation(self):
        for clipped in (False, True):
            with self.subTest(clipped=clipped):
                trace = self.associated(clipped=clipped, empty_location=True, submicrosecond=True)
                before = trace.copy()
                write_verified_sac(trace, self.output)
                actual = SACTrace.read(str(self.output))
                restored = actual.to_obspy_trace(round_sampling_interval=False)
                self.assertEqual(restored.id, "MH.SYN01..BDH")
                self.assertLessEqual(abs(restored.stats.starttime.ns - trace.stats.starttime.ns), 1000)
                self.assertEqual(actual.delta, np.float32(trace.stats.delta))
                self.assertEqual(actual.scale, 2.5)
                self.assertEqual(actual.stla, 12)
                self.assertEqual(actual.stlo, -150)
                self.assertEqual(actual.stdp, 100)
                self.assertEqual(actual.stel, 0)
                np.testing.assert_array_equal(actual.data, trace.data.astype(np.float32))
                self.assertEqual(actual.data[-1], 16777216)
                self.assertEqual(trace.stats, before.stats)
                np.testing.assert_array_equal(trace.data, before.data)
                self.output.unlink()

    def test_requires_one_trace(self):
        for value in (None, [], "waveform", Stream()):
            with self.subTest(value=repr(value)), self.assertRaises(TypeError):
                write_verified_sac(value, self.output)
        self.assertFalse(self.output.exists())

    def test_requires_association_snapshot_and_dataset_metadata(self):
        for value in (None, {}, {"association": "anchor_segment"}):
            trace = self.trace.copy()
            trace.stats.geocsv = value
            self.rejected(trace, "requires")
        for key in ("type", "waveform", "waveform_start_offset_seconds"):
            trace = self.trace.copy()
            del trace.stats.geocsv.association[key]
            self.rejected(trace)
        trace = self.trace.copy()
        del trace.stats.geocsv.metadata
        self.rejected(trace, "dataset metadata")

    def test_changed_waveform_identity_start_count_rate_rejected(self):
        for field, value in (("network", "OTHER"), ("station", "OTHER"),
                             ("location", "OTHER"), ("channel", "OTHER"),
                             ("starttime", UTCDateTime(0)), ("npts", 1),
                             ("sampling_rate", 1), ("sampling_rate", 20.000001)):
            with self.subTest(field=field, value=value):
                trace = self.trace.copy()
                trace.stats[field] = value
                self.rejected(trace)
        trace = self.associated(clipped=True)
        trace.data = np.append(trace.data, 0)
        self.rejected(trace, "association-time loaded sample count")

    def test_incomplete_source_identity_count_start_and_quality_rejected(self):
        for key in ("Station", "SampleCount", "StartTime", "DataQuality"):
            trace = self.trace.copy()
            trace.stats.geocsv[key] = pd.NA
            if key == "DataQuality":
                trace.stats.geocsv.WaterPressure = pd.NA
            self.rejected(trace)

    def test_invalid_geographic_values_rejected(self):
        for field, value in (("Latitude", pd.NA), ("Longitude", None), ("Latitude", 91),
                             ("Longitude", -181), ("Latitude", np.inf),
                             ("WaterPressure", pd.NA), ("WaterPressure", -1),
                             ("WaterPressure", np.inf)):
            with self.subTest(field=field, value=value):
                trace = self.trace.copy()
                trace.stats.geocsv[field] = value
                self.rejected(trace)

    def test_declared_units_rejected(self):
        for field, unit in (("Latitude", "radians"), ("Longitude", None),
                            ("WaterPressure", "dbar"), ("SampleRate", "kilohertz")):
            trace = self.trace.copy()
            metadata = trace.stats.geocsv.metadata
            trace.stats.geocsv.metadata = replace(metadata, field_units={**metadata.field_units, field: unit})
            self.rejected(trace)

    def test_missing_request_pressure_stays_undefined_and_is_not_borrowed(self):
        trace = self.trace.copy()
        trace.stats.geocsv.WaterPressure = pd.NA
        trace.stats.geocsv.DataQuality = "D"
        if self.current:
            # Synthetic projected REQ case, independently checked against source D.
            trace.stats.sac.stdp = -12345.0
        write_verified_sac(trace, self.output)
        self.assertIsNone(SACTrace.read(str(self.output)).stdp)

    def test_masked_and_empty_samples_rejected(self):
        for samples in (np.ma.array(self.trace.data, mask=[True, False, False, False]),
                        np.array([], dtype=np.float32)):
            trace = self.trace.copy()
            trace.data = samples
            self.rejected(trace, "loaded sample count")

    def test_nonfinite_complex_overflow_and_underflow_samples_rejected(self):
        for value in (1e100, 1e-100, np.nan, np.inf, 1 + 2j):
            trace = self.trace.copy()
            trace.data = np.full(trace.stats.npts, value)
            self.rejected(trace, "samples")

    def test_finite_float32_summary_headers_do_not_overflow(self):
        self.trace.data = np.full(self.trace.stats.npts, np.finfo(np.float32).max, dtype=np.float32)
        write_verified_sac(self.trace, self.output)
        actual = SACTrace.read(str(self.output), headonly=True)
        self.assertEqual(actual.depmin, np.finfo(np.float32).max)
        self.assertEqual(actual.depmax, actual.depmin)
        self.assertEqual(actual.depmen, actual.depmin)

    def test_identity_storage_rejects_truncation_unicode_padding_and_null(self):
        for code in ("ABCDEFGHI", "SYNé", " PAD ", "-12345"):
            trace = self.trace.copy()
            trace.stats.station = trace.stats.geocsv.Station = code
            trace.stats.geocsv.association.waveform.station = code
            self.rejected(trace, "ASCII SAC identity")

    def test_numeric_header_overflow_underflow_and_null_collision_rejected(self):
        for field, value in (("WaterPressure", 1e100), ("WaterPressure", 1e-100),
                             ("WaterPressure", 5e-324), ("calib", 1e100),
                             ("calib", 1e-100), ("calib", -12345),
                             ("calib", -12344.99999), ("SampleRate", 1e100)):
            trace = self.trace.copy()
            if field == "calib":
                trace.stats.calib = value
            else:
                trace.stats.geocsv[field] = value
                if field == "SampleRate":
                    trace.stats.sampling_rate = value
                    trace.stats.geocsv.association.waveform.sampling_rate_hz = value
            self.rejected(trace, "float32|undefined")

    def test_source_rate_exact_endpoint_and_next_float(self):
        boundary = self.trace.stats.sampling_rate + 0.00001
        self.trace.stats.geocsv.SampleRate = boundary
        write_verified_sac(self.trace, self.output)
        self.assertEqual(SACTrace.read(str(self.output)).delta, np.float32(self.trace.stats.delta))
        self.output.unlink()
        self.trace.stats.geocsv.SampleRate = np.nextafter(boundary, np.inf)
        self.rejected(self.trace, "rate disagrees")

    def test_existing_output_is_preserved(self):
        self.output.write_bytes(b"keep me")
        with self.assertRaises(FileExistsError):
            write_verified_sac(self.trace, self.output)
        self.assertEqual(self.output.read_bytes(), b"keep me")

    def test_no_source_reread_or_coordinate_fallback(self):
        trace = self.trace
        trace.stats.coordinates = {"latitude": -80, "longitude": -90, "elevation": 99}
        trace.stats.geocsv.metadata = replace(trace.stats.geocsv.metadata, source_path=self.root / "gone.csv")
        before = trace.copy()
        with patch.object(geocsv, "read", side_effect=AssertionError("must not reopen source")):
            write_verified_sac(trace, self.output)
        actual = SACTrace.read(str(self.output))
        self.assertEqual(actual.stla, 12)
        self.assertEqual(actual.stlo, -150)
        self.assertEqual(trace.stats, before.stats)

    def test_projected_headers_are_verified_without_repair(self):
        if not self.current:
            self.skipTest("the fixed baseline constructs its header inside write_sac")
        for key in ("stla", "stlo", "stel", "stdp", "scale"):
            trace = self.trace.copy()
            trace.stats.sac[key] = 999
            self.rejected(trace, "differs")
        trace = self.trace.copy()
        del trace.stats.sac
        self.rejected(trace, "create_sac_header")


if __name__ == "__main__":
    unittest.main()
