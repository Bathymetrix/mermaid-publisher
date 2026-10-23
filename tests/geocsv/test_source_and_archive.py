"""Git provenance, archive recording and testing isolation with local synthetic inputs."""

import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts/geocsv"))
from inspect_snapshot import check_source_provenance, fingerprint, json_bytes, source_provenance
import publish_snapshot as publisher
from geocsv import test_snapshot_workflow as workflow
from geocsv import test_scientific_validation as science


def git(root, *args):
    return subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True, text=True).stdout.strip()


def initialize(root):
    root.mkdir(parents=True, exist_ok=True)
    git(root, "init", "-b", "main")
    git(root, "config", "user.name", "Publication Test")
    git(root, "config", "user.email", "publication-test@example.invalid")
    (root / ".gitattributes").write_text("* -text -filter -ident\n")


class SourceProvenance(unittest.TestCase):
    setUp = workflow.Snapshots.setUp
    create = workflow.Snapshots.create

    def track_source(self):
        initialize(self.source)
        git(self.source, "add", ".")
        git(self.source, "commit", "-m", "fixture: record source")

    def test_ordinary_directory_records_absent_git_provenance(self):
        candidate = self.create()
        self.assertEqual(json.loads((candidate / "source_provenance.json").read_bytes()), {"schema_version": 1, "git": None})

    def test_clean_source_records_full_commit_and_relative_subdirectory(self):
        self.track_source()
        expected = git(self.source, "rev-parse", "HEAD")
        candidate = self.create()
        value = json.loads((candidate / "source_provenance.json").read_bytes())
        self.assertEqual(value["git"], {"commit": expected, "source_subdirectory": "."})
        check_source_provenance(candidate, self.source)
        self.file.write_bytes(self.file.read_bytes() + b"#new comment\n")
        with self.assertRaisesRegex(ValueError, "clean"):
            check_source_provenance(candidate, self.source)

    def test_dirty_staged_and_untracked_source_stop_creation(self):
        self.track_source()
        self.file.write_bytes(self.file.read_bytes() + b"#changed\n")
        with self.assertRaisesRegex(ValueError, "clean"):
            self.create()
        git(self.source, "add", ".")
        with self.assertRaisesRegex(ValueError, "clean"):
            self.create()
        git(self.source, "commit", "-m", "fixture: change comment")
        (self.source / "untracked.txt").write_text("uncommitted")
        with self.assertRaisesRegex(ValueError, "clean"):
            self.create()
        self.assertFalse((self.workspace / "snapshots").exists())

    def test_source_revision_change_during_staging_stops_freeze(self):
        self.track_source()
        import create_snapshot as creator
        first = source_provenance(self.source)
        changed = json.loads(json.dumps(first))
        changed["git"]["commit"] = "f" * 40
        with patch.object(creator, "source_provenance", side_effect=[first, changed]), self.assertRaisesRegex(ValueError, "changed during staging"):
            self.create()
        self.assertFalse(list((self.workspace / "snapshots").glob("20*")))

    def test_linked_git_worktree_and_nested_source_are_supported(self):
        self.track_source()
        linked = self.root / "linked-source"
        git(self.source, "worktree", "add", "--detach", str(linked), "HEAD")
        self.assertEqual(source_provenance(linked)["git"]["commit"], git(self.source, "rev-parse", "HEAD"))
        self.assertEqual(source_provenance(linked / "452.020-P-06")["git"]["source_subdirectory"], "452.020-P-06")

    def test_dedicated_git_archive_allows_staging(self):
        initialize(self.workspace.parent / "archive")
        self.workspace = self.workspace.parent / "archive/geocsv"
        self.assertTrue(self.create().is_dir())


class PublicationRecording(unittest.TestCase):
    def setUp(self):
        workflow.Snapshots.setUp(self)
        self.archive = self.root / "archive"
        initialize(self.archive)
        self.workspace = self.archive / "geocsv"
        self.candidate = workflow.Snapshots.create(self)
        self.report = self.workspace / "validation" / self.candidate.name / "validation.json"
        self.report.parent.mkdir(parents=True)
        self.report.write_bytes(b'{"synthetic_transport_test": true}\n')
        self.url = "https://example.test/geocsv/testing/"
        self.prefix = "geocsv/testing"

    def record(self, **kwargs):
        return publisher.record_publication(self.candidate, self.report, self.url, self.prefix, **kwargs)

    def test_successful_publication_commits_only_selected_artifacts_and_retries_reuse(self):
        unrelated = self.archive / "unrelated.txt"
        unrelated.write_text("unrelated staged work")
        git(self.archive, "add", "unrelated.txt")
        receipt = self.record()
        committed = git(self.archive, "ls-tree", "-r", "--name-only", "HEAD").splitlines()
        self.assertNotIn("unrelated.txt", committed)
        self.assertIn(receipt.relative_to(self.archive.resolve()).as_posix(), committed)
        self.assertIn("unrelated.txt", git(self.archive, "diff", "--cached", "--name-only"))
        head = git(self.archive, "rev-parse", "HEAD")
        self.assertEqual(self.record(already_selected=True), receipt)
        self.assertEqual(git(self.archive, "rev-parse", "HEAD"), head)
        self.record(already_selected=False)
        self.assertNotEqual(git(self.archive, "rev-parse", "HEAD"), head)

    def test_commit_failure_keeps_receipt_for_network_free_recovery(self):
        with patch.object(publisher, "commit_publication", side_effect=OSError("commit failed")):
            with self.assertRaisesRegex(publisher.PublicationRecordingError, "published; local recording incomplete"):
                self.record()
        receipt, = (self.workspace / "publications").glob("*.json")
        publisher.commit_publication(receipt)
        self.assertTrue(git(self.archive, "rev-parse", "HEAD"))
        command = [sys.executable, "-B", str(Path(publisher.__file__)), "--record-only", str(receipt)]
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_tampered_provenance_is_rejected_before_local_recording(self):
        receipt = self.record()
        (self.candidate / "source_provenance.json").write_bytes(json_bytes({"schema_version": 1, "git": {"commit": "f" * 40, "source_subdirectory": "."}}))
        with self.assertRaisesRegex(ValueError, "provenance differs"):
            publisher.commit_publication(receipt)

    def test_testing_destinations_are_required(self):
        for url, prefix in (("https://example.test/geocsv/", self.prefix), (self.url, "geocsv"), (self.url, "../testing")):
            with self.subTest(url=url, prefix=prefix), self.assertRaises(ValueError):
                publisher.check_destination(url, prefix)
        self.assertEqual(publisher.check_destination(self.url, self.prefix), (self.url, self.prefix))

    def test_git_archive_preserves_exact_crlf_bytes(self):
        git(self.archive, "config", "core.autocrlf", "true")
        self.file.write_bytes(workflow.geocsv(created="2026-10-22T22:48:33.277Z").replace(b"\n", b"\r\n"))
        from create_snapshot import create_snapshot
        self.candidate = create_snapshot(self.source, self.workspace, self.inventory)
        self.report = self.workspace / "validation" / self.candidate.name / "validation.json"
        self.report.parent.mkdir(parents=True)
        self.report.write_bytes(b'{"synthetic_transport_test": true}\r\n')
        self.record()
        for path in (self.candidate / "P0006.geocsv", self.report):
            relative = path.resolve().relative_to(self.archive.resolve()).as_posix()
            content = subprocess.run(["git", "-C", str(self.archive), "show", f"HEAD:{relative}"], check=True, capture_output=True).stdout
            self.assertEqual(content, path.read_bytes())


class ProvenanceGate(unittest.TestCase):
    setUp = science.ArchiveValidation.setUp
    validate = science.ArchiveValidation.validate

    def test_report_binds_provenance_and_rejects_source_tracking_changes(self):
        from gate_snapshot import require_acceptance
        report = self.validate()
        self.assertEqual(report["schema_version"], 3)
        self.assertEqual(report["source_provenance_sha256"], fingerprint(self.candidate / "source_provenance.json")[1])
        initialize(self.source)
        git(self.source, "add", ".")
        git(self.source, "commit", "-m", "fixture: establish source history")
        with self.assertRaisesRegex(ValueError, "tracking state differs"):
            require_acceptance(self.candidate, self.report_path, self.source)

class PublicationCommand(unittest.TestCase):
    def setUp(self):
        science.ArchiveValidation.setUp(self)
        self.archive = self.root / "archive"
        initialize(self.archive)
        self.work = self.archive / "geocsv"
        from create_snapshot import create_snapshot
        self.candidate = create_snapshot(self.source, self.work, self.inventory)
        self.report_path = self.work / "validation" / self.candidate.name / "validation.json"
        science.ArchiveValidation.validate(self)
        self.store = workflow.MemoryStore()
        self.command = ["publish_snapshot.py", "--candidate", str(self.candidate), "--report", str(self.report_path),
                        "--source-root", str(self.source), "--base-url", "https://example.test/geocsv/testing/",
                        "--object-prefix", "geocsv/testing", "--endpoint-url", "https://storage.example.invalid", "--bucket", "fixture"]

    def invoke(self):
        from types import SimpleNamespace
        from mermaid import geocsv
        manifest = (self.candidate / "manifest.json").read_bytes()
        result = SimpleNamespace(provenance=SimpleNamespace(instrument_id="P0006", manifest=manifest))
        with patch.object(sys, "argv", self.command), patch.object(publisher, "R2Store", return_value=self.store), patch.object(publisher, "verify_https"), patch.object(geocsv, "fetch", return_value=[result]):
            publisher.main()

    def test_real_gate_publication_and_git_record_are_connected(self):
        self.invoke()
        self.assertTrue(git(self.archive, "rev-parse", "HEAD"))
        self.assertEqual(self.store.writes[-1], "geocsv/testing/latest.json")
        self.assertFalse(any("source_provenance.json" in key for key in self.store.data))
        self.assertEqual(len(list((self.work / "publications").glob("*.json"))), 1)
        head = git(self.archive, "rev-parse", "HEAD")
        self.invoke()
        self.assertEqual(git(self.archive, "rev-parse", "HEAD"), head)

    def test_source_change_prevents_remote_writes(self):
        self.geo.write_bytes(self.geo.read_bytes() + b"#changed\n")
        with self.assertRaises(SystemExit) as caught:
            self.invoke()
        self.assertEqual(caught.exception.code, 1)
        self.assertEqual(self.store.writes, [])

    def test_commit_failure_is_a_distinct_exit_after_success(self):
        with patch.object(publisher, "commit_publication", side_effect=OSError("failed")):
            with self.assertRaises(SystemExit) as caught:
                self.invoke()
        self.assertEqual(caught.exception.code, 2)
        self.assertIn("geocsv/testing/latest.json", self.store.data)
        receipt, = (self.work / "publications").glob("*.json")
        publisher.commit_publication(receipt)

    def test_final_public_http_failure_reports_unknown_outcome(self):
        from types import SimpleNamespace
        from mermaid import geocsv
        manifest = (self.candidate / "manifest.json").read_bytes()
        result = SimpleNamespace(provenance=SimpleNamespace(instrument_id="P0006", manifest=manifest))
        def verify(url, expected):
            if url.endswith("latest.json"):
                raise OSError("final confirmation failed")
        with patch.object(sys, "argv", self.command), patch.object(publisher, "R2Store", return_value=self.store), patch.object(publisher, "verify_https", side_effect=verify), patch.object(geocsv, "fetch", return_value=[result]):
            with self.assertRaises(SystemExit) as caught:
                publisher.main()
        self.assertEqual(caught.exception.code, 2)
        self.assertIn("geocsv/testing/latest.json", self.store.data)
        self.assertFalse((self.work / "publications").exists())
