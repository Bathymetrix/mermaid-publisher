"""Offline publication checks. Synthetic data/reports never authorize publication."""

import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile
import subprocess
import unittest
from unittest.mock import patch
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts/geocsv"))
from create_snapshot import create_snapshot
from inspect_snapshot import fingerprint, json_bytes, release_component, verify_candidate
import publish_snapshot as publisher

RELEASE = "2026-10-21T22:48:33.277000001Z"
COMPONENT = "2026-10-21T22-48-33.277000001Z"


def geocsv(instrument="P0006", created=RELEASE, note=""):
    return (f"#dataset: GeoCSV\n#created: {created}\n{note}"
            f"MethodIdentifier,Station\nMeasurement:GPS,{instrument}\n").encode()


class Snapshots(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.source = self.root / "processed"
        (self.source / "452.020-P-06").mkdir(parents=True)
        self.file = self.source / "452.020-P-06/geo_DET_REQ.csv"
        self.file.write_bytes(geocsv())
        self.inventory = self.root / "inventory.csv"
        self.inventory.write_text("instrument_serial,instrument_id\n452.020-P-06,P0006\n")
        self.workspace = self.root / "publication"

    def create(self, previous=None, *, instruments=None):
        return create_snapshot(self.source, self.workspace, self.inventory, previous, instruments=instruments)

    def test_exact_copy_deterministic_idempotent_inventory(self):
        source = self.file.read_bytes()
        result = self.create()
        self.assertEqual(result.relative_to(self.workspace.resolve()), Path("testing/snapshots/2026-10-21T22-48-33.277000001Z"))
        self.assertEqual((result / "P0006.geocsv").read_bytes(), source)
        self.assertEqual(self.file.read_bytes(), source)
        manifest = (result / "manifest.json").read_bytes()
        self.assertEqual(self.create(), result)
        self.assertEqual((result / "manifest.json").read_bytes(), manifest)
        entry = verify_candidate(result)["files"][0]
        self.assertEqual(entry["provenance"]["source_path"], "452.020-P-06/geo_DET_REQ.csv")
        self.assertEqual(entry["sha256"], hashlib.sha256(source).hexdigest())

    def test_invalid_missing_repeated_and_mixed_created(self):
        for value in ("2026-02-30T00:00:00Z", "2026-10-21T24:00:00Z", "2026-10-21T22:48:60Z", "test-001", "2026-10-21T22:48:33+00:00"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                release_component(value)
        for content in (geocsv().replace(f"#created: {RELEASE}\n".encode(), b""),
                        geocsv(note=f"#created: {RELEASE}\n")):
            self.file.write_bytes(content)
            with self.assertRaisesRegex(ValueError, "exactly one"):
                self.create()
        self.file.write_bytes(geocsv())
        self.add_instrument(created=RELEASE.replace(".277000001", ".277"))
        with self.assertRaisesRegex(ValueError, "mixed"):
            self.create()

    def add_instrument(self, created=RELEASE):
        (self.source / "second").mkdir()
        (self.source / "second/geo_DET_REQ.csv").write_bytes(geocsv("N0001", created))
        self.inventory.write_text(self.inventory.read_text() + "second,N0001\n")

    def test_unchanged_rows_new_comments_new_timestamp_allowed(self):
        first = self.create()
        self.file.write_bytes(geocsv(created=RELEASE.replace("21T", "22T"), note="#new: comment\n"))
        second = self.create(first / "manifest.json")
        self.assertNotEqual(first, second)
        self.assertEqual((first / "P0006.geocsv").read_bytes().splitlines()[-1],
                         (second / "P0006.geocsv").read_bytes().splitlines()[-1])

    def test_same_release_changed_comment_conflicts(self):
        first = self.create()
        frozen = (first / "manifest.json").read_bytes()
        self.file.write_bytes(geocsv(note="#new: comment\n"))
        with self.assertRaises(FileExistsError):
            self.create()
        self.assertEqual((first / "manifest.json").read_bytes(), frozen)

    def test_historical_layout_remains_readable_and_cannot_hide_identity_conflicts(self):
        from urllib.parse import quote
        first = self.create()
        historical = first.with_name(quote(RELEASE, safe=""))
        first.rename(historical)
        self.assertEqual(verify_candidate(historical)["release_id"], RELEASE)
        current = self.create()
        self.assertEqual((current / "manifest.json").read_bytes(), (historical / "manifest.json").read_bytes())
        self.file.write_bytes(geocsv(note="#new: comment\n"))
        with self.assertRaisesRegex(FileExistsError, "historical snapshot"):
            self.create()

    def test_station_mismatch_and_multiple_ids_raise(self):
        for content in (geocsv("P0007"), geocsv() + b"Measurement:GPS,P0007\n"):
            self.file.write_bytes(content)
            with self.assertRaisesRegex(ValueError, "Station"):
                self.create()

    def test_duplicates_missing_and_unlisted_sources(self):
        self.inventory.write_text(self.inventory.read_text() + "452.020-P-06,P0007\n")
        with self.assertRaisesRegex(ValueError, "duplicate"):
            self.create()
        self.inventory.write_text("instrument_serial,instrument_id\nmissing,P0006\n")
        with self.assertRaisesRegex(ValueError, "incomplete inventory"):
            self.create()

    def test_previously_published_instruments_cannot_disappear(self):
        self.add_instrument()
        first = self.create()
        (self.source / "second/geo_DET_REQ.csv").unlink()
        self.inventory.write_text("instrument_serial,instrument_id\n452.020-P-06,P0006\n")
        with self.assertRaisesRegex(ValueError, "previously published"):
            self.create(first / "manifest.json")

    def test_workspace_cannot_be_source_or_invalid_git_checkout(self):
        self.workspace = self.source / "publication"
        with self.assertRaises(ValueError):
            self.create()
        self.workspace = self.root / "checkout/publication"
        (self.root / "checkout/.git").mkdir(parents=True)
        with self.assertRaisesRegex(ValueError, "Git"):
            self.create()

    def test_frozen_candidate_detects_hash_and_inventory_changes(self):
        candidate = self.create()
        (candidate / "unexpected").touch()
        with self.assertRaisesRegex(ValueError, "inventory"):
            verify_candidate(candidate)
        (candidate / "unexpected").unlink()
        (candidate / "P0006.geocsv").write_bytes(b"changed")
        with self.assertRaisesRegex(ValueError, "bytes changed"):
            verify_candidate(candidate)

    def test_selected_snapshot_freezes_only_selected_payloads_and_scope(self):
        self.add_instrument()
        third = self.source / "third"
        third.mkdir()
        (third / "geo_DET_REQ.csv").write_bytes(geocsv("P0045"))
        self.inventory.write_text(self.inventory.read_text() + "third,P0045\n")
        # An unselected source is outside this validation batch, even if malformed.
        (self.source / "second/geo_DET_REQ.csv").write_bytes(b"not GeoCSV\n")
        candidate = self.create(instruments=["P0045", "P0006"])
        manifest = verify_candidate(candidate)
        self.assertEqual([entry["instrument_id"] for entry in manifest["files"]], ["P0006", "P0045"])
        self.assertEqual({path.name for path in candidate.iterdir()},
                         {"P0006.geocsv", "P0045.geocsv", "manifest.json", "source_provenance.json"})
        staging = self.workspace / "testing/staging" / candidate.name / "inventory.json"
        value = json.loads(staging.read_bytes())
        self.assertEqual(value["schema_version"], 2)
        self.assertEqual(value["instrument_ids"], ["P0006", "P0045"])
        frozen = staging.read_bytes()
        self.assertEqual(self.create(instruments=["P0006", "P0045"]), candidate)
        with self.assertRaisesRegex(FileExistsError, "immutable snapshot"):
            self.create(instruments=["P0006"])
        self.assertEqual(staging.read_bytes(), frozen)
        self.assertEqual(len(verify_candidate(candidate)["files"]), 2)

    def test_selection_requires_known_unique_ids_and_complete_source_mapping(self):
        for selection in ([], ["P0006", "P0006"], ["P9999"], ["../P0006"]):
            with self.subTest(selection=selection), self.assertRaises(ValueError):
                self.create(instruments=selection)
        self.add_instrument()
        self.inventory.write_text("instrument_serial,instrument_id\n452.020-P-06,P0006\n")
        with self.assertRaisesRegex(ValueError, "incomplete inventory"):
            self.create(instruments=["P0006"])
        self.assertFalse((self.workspace / "testing/snapshots").exists())

    def test_selection_cannot_drop_a_previously_published_instrument(self):
        self.add_instrument()
        previous = self.create()
        self.workspace = self.root / "selected"
        with self.assertRaisesRegex(ValueError, "previously published"):
            self.create(previous / "manifest.json", instruments=["P0006"])


class MemoryStore:
    def __init__(self):
        self.data, self.writes = {}, []
        self.fail_on = None

    def get(self, key):
        if key not in self.data:
            return None
        content = self.data[key]
        return {"Body": io.BytesIO(content), "ETag": hashlib.md5(content).hexdigest()}

    def keys(self, prefix):
        return {key for key in self.data if key.startswith(prefix)}

    def put(self, key, path, *, etag=None, immutable=True):
        if key == self.fail_on:
            raise OSError("interrupted upload")
        existing = self.get(key)
        if immutable and existing is not None:
            raise FileExistsError(key)
        if not immutable and ((existing is None) != (etag is None)
                              or existing is not None and existing["ETag"] != etag):
            raise FileExistsError("latest changed concurrently")
        self.data[key] = Path(path).read_bytes()
        self.writes.append(key)


class Publication(unittest.TestCase):
    create = Snapshots.create

    def setUp(self):
        Snapshots.setUp(self)
        self.candidate = self.create()
        self.report = self.root / "synthetic-validation.json"
        # This is transport test data, NOT a proposed validation report schema.
        self.report.write_text('{"synthetic_transport_test": true}\n')
        self.store = MemoryStore()
        manifest_bytes = (self.candidate / "manifest.json").read_bytes()
        result = SimpleNamespace(provenance=SimpleNamespace(instrument_id="P0006", manifest=manifest_bytes))
        self.client = SimpleNamespace(geocsv=SimpleNamespace(__version__="0.26.0", fetch=lambda **kwargs: [result]))
        self.patches = [patch.object(publisher, "verify_https"),
                        patch.dict(sys.modules, {"mermaid": self.client})]
        self.https = self.patches[0].start()
        self.patches[1].start()
        for item in self.patches:
            self.addCleanup(item.stop)

    def transfer(self):
        publisher._transfer_and_verify(self.candidate, self.report, self.store, "https://example.test/geocsv/testing/", object_prefix="geocsv/testing")

    def test_gate_never_accepts_synthetic_pass_or_missing_report(self):
        for report in (None, self.report):
            with self.assertRaises(publisher.AcceptanceUnavailable):
                publisher.require_scientific_acceptance(self.candidate, report)
        self.assertEqual(self.store.writes, [])

    def test_old_fetch_consumer_stops_before_remote_writes(self):
        self.client.geocsv.__version__ = "0.24.0"
        with self.assertRaisesRegex(ValueError, ">= 0.26.0"):
            self.transfer()
        self.assertEqual(self.store.writes, [])

    def test_historical_latest_can_be_replaced_without_rewriting_its_objects(self):
        from urllib.parse import quote
        old_prefix = f"geocsv/testing/releases/{RELEASE}/"
        old_manifest = (self.candidate / "manifest.json").read_bytes()
        self.store.data[old_prefix + "manifest.json"] = old_manifest
        self.store.data["geocsv/testing/latest.json"] = json_bytes({
            "release_id": RELEASE, "testing_only": True,
            "manifest": f"releases/{quote(RELEASE, safe='')}/manifest.json"})
        self.transfer()
        self.assertEqual(self.store.data[old_prefix + "manifest.json"], old_manifest)
        self.assertFalse(any(key.startswith(old_prefix) for key in self.store.writes))

    def test_cli_plan_is_read_only_and_publication_requires_full_evidence(self):
        script = Path(publisher.__file__)
        command = [sys.executable, "-B", str(script), "--candidate", str(self.candidate), "--base-url", "https://example.test/geocsv/testing/", "--object-prefix", "geocsv/testing"]
        plan = subprocess.run([*command, "--plan"], capture_output=True, text=True)
        self.assertEqual(plan.returncode, 0, plan.stderr)
        self.assertIn("BLOCKED", plan.stdout)
        blocked = subprocess.run([*command, "--report", str(self.report)], capture_output=True, text=True)
        self.assertNotEqual(blocked.returncode, 0)
        self.assertIn("dedicated Git archive", blocked.stderr)

    def test_https_identity_and_checksum_enforced(self):
        # Use a real context-managed bytes stream with response metadata.
        class Response(io.BytesIO):
            headers = {"Content-Encoding": "identity"}
            def geturl(self):
                return "https://example.test/file"
        body = b"unchanged payload"
        with patch.object(publisher, "urlopen", return_value=Response(body)) as opened:
            # verify_https is patched for transfer tests; exercise its original here.
            self.patches[0].stop()
            publisher.verify_https("https://example.test/file", (len(body), hashlib.sha256(body).hexdigest()))
            self.assertEqual(opened.call_args.args[0].get_header("Accept-encoding"), "identity")
        response = Response(body)
        response.headers = {"Content-Encoding": "gzip"}
        with patch.object(publisher, "urlopen", return_value=response):
            with self.assertRaisesRegex(ValueError, "transformed"):
                publisher.verify_https("https://example.test/file", (len(body), hashlib.sha256(body).hexdigest()))
        with patch.object(publisher, "urlopen", return_value=Response(b"corrupted payload")):
            with self.assertRaisesRegex(ValueError, "checksum mismatch"):
                publisher.verify_https("https://example.test/file", (len(body), hashlib.sha256(body).hexdigest()))

    def test_upload_order_exact_retry_and_latest_last(self):
        self.transfer()
        self.assertTrue(self.store.writes[0].endswith("P0006.geocsv"))
        self.assertTrue(self.store.writes[1].endswith("manifest.json"))
        self.assertEqual(self.store.writes[-1], "geocsv/testing/latest.json")
        self.assertIn(COMPONENT, self.store.writes[0])
        self.assertIn(COMPONENT, self.https.call_args_list[0].args[0])
        self.assertNotIn("%", self.https.call_args_list[0].args[0])
        latest = json.loads(self.store.data["geocsv/testing/latest.json"])
        self.assertEqual(latest["release_id"], RELEASE)
        self.assertEqual(latest["manifest"], f"releases/{COMPONENT}/manifest.json")
        self.store.writes.clear()
        self.transfer()
        self.assertEqual(self.store.writes, ["geocsv/testing/latest.json"])

    def test_upload_failure_leaves_latest_absent_and_retry_resumes(self):
        self.store.fail_on = f"geocsv/testing/releases/{COMPONENT}/manifest.json"
        with self.assertRaises(OSError):
            self.transfer()
        self.assertNotIn("geocsv/testing/latest.json", self.store.data)
        self.store.fail_on = None
        self.transfer()
        self.assertIn("geocsv/testing/latest.json", self.store.data)

    def test_conflict_preflight_writes_nothing(self):
        self.store.data[f"geocsv/testing/releases/{COMPONENT}/manifest.json"] = b"different manifest"
        with self.assertRaises(FileExistsError):
            self.transfer()
        self.assertEqual(self.store.writes, [])

    def test_unexpected_remote_inventory_rejected(self):
        self.store.data[f"geocsv/testing/releases/{COMPONENT}/other.geocsv"] = b"different inventory"
        with self.assertRaises(FileExistsError):
            self.transfer()
        self.assertEqual(self.store.writes, [])

    def test_public_verification_failure_keeps_existing_latest(self):
        self.transfer()
        old_latest = self.store.data["geocsv/testing/latest.json"]
        self.https.side_effect = ValueError("bad public checksum")
        with self.assertRaises(ValueError):
            self.transfer()
        self.assertEqual(self.store.data["geocsv/testing/latest.json"], old_latest)

    def test_changed_candidate_or_report_blocks_latest(self):
        self.https.side_effect = lambda *args: self.report.write_text("changed report")
        with self.assertRaisesRegex(ValueError, "report changed"):
            self.transfer()
        self.assertNotIn("geocsv/testing/latest.json", self.store.data)

    def test_concurrent_latest_update_not_overwritten(self):
        original = self.store.put
        def race(key, path, **kwargs):
            if key == "geocsv/testing/latest.json":
                self.store.data[key] = b'"competing latest"'
            return original(key, path, **kwargs)
        self.store.put = race
        with self.assertRaises(FileExistsError):
            self.transfer()
        self.assertEqual(self.store.data["geocsv/testing/latest.json"], b'"competing latest"')

    def test_lock_serializes_publishers(self):
        with publisher.publication_lock(self.workspace):
            with self.assertRaises(FileExistsError):
                with publisher.publication_lock(self.workspace):
                    self.fail("second publisher entered")


if __name__ == "__main__":
    unittest.main()
