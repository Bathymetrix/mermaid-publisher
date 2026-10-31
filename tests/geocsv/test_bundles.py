"""Manifest-derived snapshot bundles."""

import io
import json
import os
from pathlib import Path
import sys
import tarfile
import unittest
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts/geocsv"))
import publish_snapshot as publisher
from geocsv import test_snapshot_workflow as workflow


class Bundles(unittest.TestCase):
    setUp = workflow.Snapshots.setUp

    def test_all_manifested_files_exact_bytes_and_deterministic_metadata(self):
        workflow.Snapshots.add_instrument(self)
        candidate = workflow.Snapshots.create(self)
        before = {path.name: path.read_bytes() for path in candidate.iterdir()}
        bundle = publisher.create_bundle(candidate)
        expected = bundle.read_bytes()
        with tarfile.open(bundle, "r:gz") as archive:
            self.assertEqual(archive.getnames(), ["N0001.geocsv", "P0006.geocsv"])
            for member in archive:
                self.assertEqual(archive.extractfile(member).read(), before[member.name])
                self.assertEqual((member.uid, member.gid, member.mtime, member.mode), (0, 0, 0, 0o644))
                self.assertEqual((member.uname, member.gname), ("", ""))
        for path in candidate.glob("*.geocsv"):
            os.utime(path, (100, 100))
            path.chmod(0o600)
        self.assertEqual(publisher.create_bundle(candidate).read_bytes(), expected)
        bundle.unlink()
        self.assertEqual(publisher.create_bundle(candidate).read_bytes(), expected)
        self.assertEqual({path.name: path.read_bytes() for path in candidate.iterdir()}, before)
        self.assertEqual(bundle.parent, candidate.parent.parent / "bundles" / candidate.name)

    def test_selection_contains_only_selected_files(self):
        workflow.Snapshots.add_instrument(self)
        candidate = workflow.Snapshots.create(self, instruments=["P0006"])
        with tarfile.open(publisher.create_bundle(candidate), "r:gz") as archive:
            self.assertEqual(archive.getnames(), ["P0006.geocsv"])

    def test_changed_existing_bundle_is_not_replaced(self):
        candidate = workflow.Snapshots.create(self)
        bundle = publisher.create_bundle(candidate)
        bundle.write_bytes(b"changed")
        with self.assertRaisesRegex(FileExistsError, "immutable bundle"):
            publisher.create_bundle(candidate)
        self.assertEqual(bundle.read_bytes(), b"changed")

    def test_member_inventory_and_bytes_checked_against_manifest(self):
        candidate = workflow.Snapshots.create(self)
        manifest = json.loads((candidate / "manifest.json").read_bytes())
        for name, content in (("P0006.geocsv", b"x" * manifest["files"][0]["size_bytes"]),
                              ("../P0006.geocsv", b"wrong inventory")):
            path = self.root / "invalid.tar.gz"
            with tarfile.open(path, "w:gz") as archive:
                member = tarfile.TarInfo(name)
                member.size = len(content)
                archive.addfile(member, io.BytesIO(content))
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, "bundle"):
                publisher.verify_bundle(path, manifest)

    def test_storage_content_type(self):
        client = Mock()
        session = Mock(client=Mock(return_value=client))
        with patch("boto3.Session", return_value=session):
            store = publisher.R2Store("https://storage.example.invalid", "fixture")
        path = self.root / publisher.BUNDLE_FILENAME
        path.write_bytes(b"fixture")
        store.put(publisher.BUNDLE_FILENAME, path)
        self.assertEqual(client.put_object.call_args.kwargs["ContentType"], "application/gzip")


if __name__ == "__main__":
    unittest.main()
