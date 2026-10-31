#!/usr/bin/env python3
"""Require full-archive acceptance, then upload, verify and select latest last."""

import argparse
from contextlib import contextmanager
import gzip
import hashlib
import json
import os
from pathlib import Path
import tempfile
import tarfile
from datetime import datetime, timezone
from urllib.parse import quote, urlsplit
from urllib.request import Request, urlopen

from inspect_snapshot import fingerprint, git_command, git_repository, json_bytes, read_json, release_component, require_external_workspace, verify_candidate
from gate_snapshot import AcceptanceError, require_acceptance


AcceptanceUnavailable = AcceptanceError  # Retain the private preflight exception name.
BUNDLE_FILENAME = "MERMAID.geocsv.tar.gz"


def verify_bundle(path, manifest):
    """Check archive members against the instrument manifest."""
    entries = sorted(manifest["files"], key=lambda entry: entry["filename"])
    try:
        with tarfile.open(path, "r:gz") as archive:
            members = archive.getmembers()
            if [member.name for member in members] != [entry["filename"] for entry in entries]:
                raise ValueError("bundle inventory differs from manifest")
            for member, entry in zip(members, entries):
                if not member.isfile() or member.size != entry["size_bytes"]:
                    raise ValueError("bundle member differs from manifest")
                checksum = hashlib.sha256()
                with archive.extractfile(member) as stream:
                    while chunk := stream.read(1024 * 1024):
                        checksum.update(chunk)
                if checksum.hexdigest() != entry["sha256"]:
                    raise ValueError("bundle member differs from manifest")
    except (tarfile.TarError, EOFError, OSError) as exc:
        raise ValueError("cannot read instrument bundle") from exc


def create_bundle(candidate):
    """Build an immutable, deterministic instrument bundle."""
    candidate = Path(candidate)
    manifest = verify_candidate(candidate)
    directory = candidate.parent.parent / "bundles" / candidate.name
    directory.mkdir(parents=True, exist_ok=True)
    destination = directory / BUNDLE_FILENAME
    if destination.exists():
        if destination.is_symlink():
            raise FileExistsError("conflicting immutable bundle")
        try:
            verify_bundle(destination, manifest)
        except ValueError:
            raise FileExistsError("conflicting immutable bundle") from None
        return destination
    with tempfile.TemporaryDirectory(prefix=".bundle-", dir=directory) as temporary:
        path = Path(temporary) / BUNDLE_FILENAME
        with path.open("xb") as raw, gzip.GzipFile(filename="", fileobj=raw, mode="wb", mtime=0) as compressed:
            with tarfile.open(fileobj=compressed, mode="w|", format=tarfile.USTAR_FORMAT) as archive:
                for entry in sorted(manifest["files"], key=lambda entry: entry["filename"]):
                    member = tarfile.TarInfo(entry["filename"])
                    member.size = entry["size_bytes"]
                    member.mode = 0o644
                    with (candidate / member.name).open("rb") as stream:
                        archive.addfile(member, stream)
        verify_bundle(path, manifest)
        if verify_candidate(candidate) != manifest:
            raise ValueError("candidate changed during bundle creation")
        path.rename(destination)
    return destination


class PublicationOutcomeUnknown(RuntimeError):
    """A latest write was attempted but its resulting public state is unconfirmed."""


def require_scientific_acceptance(candidate, report, source_root=None):
    """Apply the publication gate and recheck exact input coverage."""
    return require_acceptance(candidate, report, source_root)


class R2Store:
    """Small S3 transport; credentials are resolved by the SDK, never inspected here."""

    def __init__(self, endpoint_url, bucket, *, profile=None):
        import boto3  # Optional deployment dependency; offline staging needs no SDK.
        session = boto3.Session(profile_name=profile)
        self.client = session.client("s3", endpoint_url=endpoint_url, region_name="auto")
        self.bucket = bucket

    def get(self, key):
        try:
            return self.client.get_object(Bucket=self.bucket, Key=key)
        except self.client.exceptions.ClientError as exc:
            if exc.response["Error"]["Code"] in {"NoSuchKey", "404"}:
                return None
            raise

    def keys(self, prefix):
        paginator = self.client.get_paginator("list_objects_v2")
        return {obj["Key"] for page in paginator.paginate(Bucket=self.bucket, Prefix=prefix)
                for obj in page.get("Contents", [])}

    def put(self, key, path, *, etag=None, immutable=True):
        condition = {"IfNoneMatch": "*"} if immutable or etag is None else {"IfMatch": etag}
        with Path(path).open("rb") as stream:
            self.client.put_object(
                Bucket=self.bucket, Key=key, Body=stream, **condition,
                ContentType=("application/gzip" if key.endswith(".tar.gz") else
                             "application/json" if key.endswith(".json") else "text/csv; charset=utf-8"),
                CacheControl="public, max-age=31536000, immutable, no-transform" if immutable else "no-store",
            )


def remote_fingerprint(response):
    checksum, size = hashlib.sha256(), 0
    with response["Body"] as stream:
        while chunk := stream.read(1024 * 1024):
            checksum.update(chunk)
            size += len(chunk)
    return size, checksum.hexdigest()


def upload_identical_or_new(store, key, path):
    expected = fingerprint(path)
    existing = store.get(key)
    if existing is not None:
        if remote_fingerprint(existing) != expected:
            raise FileExistsError(f"immutable remote object conflicts: {key}")
        return
    # Conditional create prevents overwriting a concurrent upload.
    store.put(key, path)
    if remote_fingerprint(store.get(key)) != expected:
        raise ValueError(f"uploaded bytes differ: {key}")


def verify_https(url, expected):
    request = Request(url, headers={"Accept-Encoding": "identity", "Cache-Control": "no-cache"})
    checksum, size = hashlib.sha256(), 0
    with urlopen(request, timeout=60) as response:
        if response.geturl() != url:
            raise ValueError(f"immutable URL unexpectedly redirected: {url}")
        if response.headers.get("Content-Encoding", "identity").lower() != "identity":
            raise ValueError(f"server transformed exact bytes: {url}")
        while chunk := response.read(1024 * 1024):
            checksum.update(chunk)
            size += len(chunk)
    if (size, checksum.hexdigest()) != expected:
        raise ValueError(f"public HTTPS checksum mismatch: {url}")


def require_fetch_consumer():
    """Reject the historical download protocol before any object writes."""
    from mermaid import geocsv
    if tuple(int(part) for part in geocsv.__version__.split(".")) < (0, 27, 0):
        raise ValueError("schema 1.0.0 publication requires mermaid-geocsv >= 0.27.0")


def _transfer_and_verify(candidate, report, store, base_url, *, object_prefix, accepted=None, report_fingerprint=None, before_activation=None):
    """Publication sequence, reachable from the CLI only after scientific acceptance.

    Kept separate to test ordering and failures with an in-memory transport;
    it is not an alternate publication interface or acceptance override.
    """
    from mermaid import geocsv  # Public API, not private scientific logic.
    require_fetch_consumer()
    manifest = verify_candidate(candidate)
    candidate = Path(candidate)
    frozen_manifest = (candidate / "manifest.json").read_bytes()
    frozen_report = fingerprint(report)
    if accepted is not None and (
            accepted["candidate"] != {"manifest_sha256": hashlib.sha256(frozen_manifest).hexdigest(), "files": manifest["files"]}
            or frozen_report != report_fingerprint):
        raise ValueError("candidate/report changed after scientific acceptance")
    release = manifest["release_id"]
    component = release_component(release)
    prefix = f"{object_prefix}/releases/{component}/"
    latest_key = f"{object_prefix}/latest.json"
    latest_before = store.get(latest_key)
    already_selected = False
    etag = None
    if latest_before is not None:
        etag = latest_before["ETag"]
        with latest_before["Body"] as stream:
            old = json.load(stream)
        old_id = old.get("release_id")
        old_component = release_component(old_id)
        if (old.get("testing_only") is not True
                or old.get("manifest") != f"releases/{old_component}/manifest.json"):
            raise ValueError("current testing pointer is inconsistent")
        already_selected = old_id == release
        previous_component = old_component
        previous = store.get(f"{object_prefix}/releases/{previous_component}/manifest.json")
        if previous is None:
            raise ValueError("current latest manifest is missing")
        with previous["Body"] as stream:
            old_manifest = json.load(stream)
        missing = {entry["instrument_id"] for entry in old_manifest["files"]} - {
            entry["instrument_id"] for entry in manifest["files"]}
        if missing:
            raise ValueError(f"previously published instruments missing: {sorted(missing)}")
    paths = [(entry["filename"], candidate / entry["filename"]) for entry in manifest["files"]]
    bundle = create_bundle(candidate)
    frozen_bundle = fingerprint(bundle)
    paths.append((BUNDLE_FILENAME, bundle))
    paths += [("manifest.json", candidate / "manifest.json"), ("validation.json", Path(report))]
    expected_keys = {prefix + name for name, _ in paths}
    unexpected = store.keys(prefix) - expected_keys
    if unexpected:
        raise FileExistsError(f"conflicting remote inventory: {sorted(unexpected)}")
    # Preflight ALL existing objects before uploading anything.
    for name, path in paths:
        existing = store.get(prefix + name)
        if existing is not None and remote_fingerprint(existing) != fingerprint(path):
            raise FileExistsError(f"immutable remote object conflicts: {prefix + name}")
    for name, path in paths:  # Payloads before manifest, then independent evidence.
        upload_identical_or_new(store, prefix + name, path)
    for name, path in paths:
        verify_https(f"{base_url}releases/{component}/{name}", fingerprint(path))
    with tempfile.TemporaryDirectory(prefix="fetch-check-") as output:
        results = geocsv.fetch(base_url=base_url, release=release, output_dir=output)
        if {item.provenance.instrument_id for item in results} != {entry["instrument_id"] for entry in manifest["files"]}:
            raise ValueError("pinned fetch returned a different inventory")
        if any(item.provenance.manifest != (candidate / "manifest.json").read_bytes() for item in results):
            raise ValueError("pinned fetch returned a different manifest")
    # Detect candidate changes during upload/verification before touching latest.
    verify_candidate(candidate)
    if (candidate / "manifest.json").read_bytes() != frozen_manifest or fingerprint(report) != frozen_report:
        raise ValueError("candidate manifest or validation report changed during publication")
    if fingerprint(bundle) != frozen_bundle:
        raise ValueError("bundle changed during publication")
    if before_activation is not None:
        before_activation()
    with tempfile.TemporaryDirectory(prefix="latest-") as directory:
        path = Path(directory) / "latest.json"
        path.write_bytes(json_bytes({"release_id": release, "testing_only": True,
                                    "manifest": f"releases/{component}/manifest.json"}))
        # Compare-and-swap: a competing publisher must not be silently overwritten.
        try:
            store.put(latest_key, path, etag=etag, immutable=False)
            if remote_fingerprint(store.get(latest_key)) != fingerprint(path):
                raise RuntimeError("latest differs after activation")
            verify_https(f"{base_url}latest.json", fingerprint(path))
        except FileExistsError:
            raise  # A rejected conditional write did not replace latest.
        except Exception as exc:
            raise PublicationOutcomeUnknown("publication outcome unconfirmed; inspect remote latest before retrying") from exc
    return already_selected


@contextmanager
def publication_lock(workspace):
    lock = Path(workspace) / ".geocsv-publication-lock"
    lock.mkdir()  # All operators use one external workspace. Crash leaves a visible lock.
    try:
        yield
    finally:
        lock.rmdir()


class PublicationRecordingError(RuntimeError):
    """Remote publication succeeded, but its local Git record is incomplete."""


def check_destination(base_url, object_prefix):
    """Require explicit, isolated testing collections until production is authorized."""
    import re
    parsed = urlsplit(base_url)
    if (parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password
            or parsed.query or parsed.fragment or not parsed.path.rstrip("/").endswith("/testing")):
        raise ValueError("use an explicit HTTPS collection URL ending in /testing/")
    parts = object_prefix.split("/")
    if (parts[-1] != "testing" or any(part in ("", ".", "..") or not re.fullmatch(r"[A-Za-z0-9._-]+", part) for part in parts)):
        raise ValueError("use an isolated object prefix ending in /testing")
    return base_url.rstrip("/") + "/", object_prefix


def archive_repository(workspace):
    workspace = Path(workspace).resolve()
    repository = git_repository(workspace)
    if repository is None or workspace != repository / "geocsv" / "testing":
        raise ValueError("publication requires <dedicated Git archive>/geocsv/testing as collection workspace")
    if (repository / "scripts").exists() or (repository / "pyproject.toml").exists():
        raise ValueError("publication archive must be separate from software")
    attributes = repository / ".gitattributes"
    if not attributes.is_file() or attributes.read_text() != "* -text -filter -ident\n":
        raise ValueError("archive .gitattributes must preserve exact bytes: * -text -filter -ident")
    # Read-only preflight: fail before remote writes if local author identity is absent.
    git_command(repository, "var", "GIT_AUTHOR_IDENT")
    git_command(repository, "var", "GIT_COMMITTER_IDENT")
    return repository


def commit_publication(receipt_path):
    """Commit only this receipt's artifacts, preserving unrelated staged changes."""
    receipt_path = Path(receipt_path).resolve(strict=True)
    workspace = receipt_path.parent.parent
    repository = archive_repository(workspace)
    if receipt_path.parent.name != "publications":
        raise ValueError("receipt must be in <archive>/geocsv/testing/publications")
    receipt = read_json(receipt_path)
    if receipt.get("schema_version") != 1 or receipt.get("testing_only") is not True:
        raise ValueError("unsupported publication receipt")
    base_url, prefix = check_destination(receipt["base_url"], receipt["object_prefix"])
    component = release_component(receipt["release_id"])
    candidate = workspace / "snapshots" / component
    manifest = verify_candidate(candidate)
    if manifest["release_id"] != receipt["release_id"]:
        raise ValueError("receipt release differs from snapshot")
    report = workspace / "validation" / component / receipt["report_filename"]
    if report.parent != (workspace / "validation" / component) or report.name != receipt["report_filename"]:
        raise ValueError("receipt report must be a plain filename")
    if fingerprint(candidate / "manifest.json")[1] != receipt["manifest_sha256"] or fingerprint(report)[1] != receipt["report_sha256"]:
        raise ValueError("publication artifacts differ from receipt")
    if fingerprint(candidate / "source_provenance.json")[1] != receipt["source_provenance_sha256"]:
        raise ValueError("source provenance differs from receipt")
    sidecar = workspace / "staging" / component / "inventory.json"
    if fingerprint(sidecar)[1] != receipt["staging_inventory_sha256"]:
        raise ValueError("staging inventory differs from receipt")
    paths = [repository / ".gitattributes", *sorted(candidate.iterdir()), report, sidecar, receipt_path]
    if "bundle_filename" in receipt:
        if receipt["bundle_filename"] != BUNDLE_FILENAME:
            raise ValueError("unsupported receipt bundle filename")
        bundle = workspace / "bundles" / component / BUNDLE_FILENAME
        if bundle.is_symlink():
            raise ValueError("bundle must be a regular file")
        verify_bundle(bundle, manifest)
        paths.append(bundle)
    relative = [path.relative_to(repository).as_posix() for path in paths]
    # A repeat after a completed commit is a no-op, including when HEAD has moved.
    if not git_command(repository, "status", "--porcelain=v1", "--", *relative):
        return
    git_command(repository, "add", "--", *relative)
    git_command(repository, "commit", "--only", "-m", f"geocsv: record publication of {receipt['release_id']} to {base_url}", "--", *relative)


def record_publication(candidate, report, base_url, object_prefix, *, already_selected=False):
    """Create durable local evidence before attempting its Git commit."""
    candidate, report = Path(candidate).resolve(), Path(report).resolve()
    workspace = candidate.parent.parent
    archive_repository(workspace)
    manifest = verify_candidate(candidate)
    if report.parent != workspace / "validation" / candidate.name or report.is_symlink():
        raise ValueError("report must be under <workspace>/validation/<snapshot ID>/")
    value = {"schema_version": 1, "release_id": manifest["release_id"], "testing_only": True,
             "base_url": base_url, "object_prefix": object_prefix,
             "manifest_sha256": fingerprint(candidate / "manifest.json")[1],
             "source_provenance_sha256": fingerprint(candidate / "source_provenance.json")[1],
             "report_filename": report.name, "report_sha256": fingerprint(report)[1],
             "staging_inventory_sha256": fingerprint(workspace / "staging" / candidate.name / "inventory.json")[1]}
    bundle = workspace / "bundles" / candidate.name / BUNDLE_FILENAME
    if bundle.exists():
        verify_bundle(bundle, manifest)
        value["bundle_filename"] = BUNDLE_FILENAME
    directory = workspace / "publications"
    directory.mkdir(exist_ok=True)
    receipt = None
    if already_selected:
        for previous in sorted(directory.glob("*.json"), reverse=True):
            old = read_json(previous)
            if {key: old.get(key) for key in value} == value:
                receipt = previous
                break
    if receipt is None:
        now = datetime.now(timezone.utc)
        value["completed_utc"] = now.isoformat().replace("+00:00", "Z")
        receipt = directory / (now.strftime("%Y%m%dT%H%M%S.%fZ") + ".json")
        with receipt.open("xb") as stream:
            stream.write(json_bytes(value))
    try:
        commit_publication(receipt)
    except (ValueError, OSError) as exc:
        raise PublicationRecordingError(f"published; local recording incomplete. Retry --record-only {receipt}") from exc
    return receipt


def read_publication_config():
    """Load optional environment-selected settings without disclosing private values."""
    path = os.environ.get("MERMAID_PUBLISHER_CONFIG")
    if not path:
        return {}
    try:
        config = read_json(Path(path).expanduser())
    except (OSError, ValueError, UnicodeError):
        raise ValueError("cannot read MERMAID_PUBLISHER_CONFIG as a JSON settings file") from None
    keys = {"profile", "bucket", "endpoint_url", "base_url", "object_prefix"}
    if (not isinstance(config, dict) or config.keys() - keys
            or any(not isinstance(value, str) or not value.strip() for value in config.values())):
        raise ValueError("MERMAID_PUBLISHER_CONFIG accepts only profile, bucket, endpoint_url, "
                         "base_url and object_prefix with nonempty string values")
    return config


def main():
    parser = argparse.ArgumentParser(description=__doc__, epilog=(
        "MERMAID_PUBLISHER_CONFIG may name a private JSON settings file; "
        "explicit destination options override file settings. Credentials use the SDK provider."))
    parser.add_argument("--candidate", type=Path)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--source-root", type=Path, help="read-only processed root")
    parser.add_argument("--plan", action="store_true", help="read-only local inspection and gate; no uploads or commits")
    parser.add_argument("--record-only", type=Path, metavar="RECEIPT", help="finish local Git recording after successful publication; no network")
    parser.add_argument("--base-url", help="explicit HTTPS testing collection URL")
    parser.add_argument("--object-prefix", help="explicit isolated storage prefix, e.g. geocsv/testing")
    parser.add_argument("--endpoint-url", help="S3-compatible endpoint; credentials resolved by SDK")
    parser.add_argument("--bucket")
    args = parser.parse_args()
    try:
        if args.record_only:
            if any((args.candidate, args.report, args.source_root, args.plan, args.base_url, args.object_prefix, args.endpoint_url, args.bucket)):
                raise ValueError("--record-only must be used alone")
            try:
                commit_publication(args.record_only)
            except (ValueError, OSError) as exc:
                raise PublicationRecordingError("published; local recording remains incomplete") from exc
            print("Local publication recording complete")
            return
        config = read_publication_config()
        for key in ("base_url", "object_prefix", "endpoint_url", "bucket"):
            if getattr(args, key) is None:
                setattr(args, key, config.get(key))
        if not args.candidate or not args.base_url or not args.object_prefix:
            raise ValueError("--candidate, --base-url and --object-prefix are required")
        base_url, object_prefix = check_destination(args.base_url, args.object_prefix)
        candidate = args.candidate.resolve()
        manifest = verify_candidate(candidate)
        workspace = candidate.parent.parent
        require_external_workspace(workspace, args.source_root or Path(__file__).resolve().parents[2])
        if candidate.parent.name != "snapshots":
            raise ValueError("candidate must be under <workspace>/testing/snapshots/")
        if args.plan:
            if bool(args.report) != bool(args.source_root):
                raise ValueError("supply both --report and --source-root for the scientific gate")
            if args.report:
                require_scientific_acceptance(candidate, args.report, args.source_root)
            print(json.dumps({"release_id": manifest["release_id"], "files": len(manifest["files"]),
                              "base_url": base_url, "object_prefix": object_prefix, "testing_only": True,
                              "publication": "gate passed; no publication performed" if args.report else "BLOCKED: report and source root required"}, indent=2))
            return
        archive_repository(workspace)
        if not args.report or args.report.resolve().parent != workspace / "validation" / candidate.name:
            raise ValueError("--report must be under <workspace>/validation/<snapshot ID>/")
        if not args.endpoint_url or not args.bucket:
            raise ValueError("--endpoint-url and --bucket are required")
        with publication_lock(workspace):
            accepted_fingerprint = fingerprint(args.report)
            accepted = require_scientific_acceptance(candidate, args.report, args.source_root)
            store = R2Store(args.endpoint_url, args.bucket, profile=config.get("profile"))
            already_selected = _transfer_and_verify(
                candidate, args.report, store, base_url, object_prefix=object_prefix,
                accepted=accepted, report_fingerprint=accepted_fingerprint,
                before_activation=lambda: require_scientific_acceptance(candidate, args.report, args.source_root))
            try:
                receipt = record_publication(candidate, args.report, base_url, object_prefix, already_selected=already_selected)
            except PublicationRecordingError:
                raise
            except (ValueError, OSError) as exc:
                raise PublicationRecordingError("published; local recording incomplete; inspect archive and remote state") from exc
            print(f"Published and recorded: {receipt}")
    except (PublicationRecordingError, PublicationOutcomeUnknown) as exc:
        parser.exit(2, f"{exc}\n")
    except (ValueError, OSError, RuntimeError) as exc:
        parser.exit(1, f"Not published: {exc}\n")


if __name__ == "__main__":
    main()
