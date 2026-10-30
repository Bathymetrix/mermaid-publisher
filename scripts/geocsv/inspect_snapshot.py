"""Private, standard-library publication helpers; no scientific transformations."""

import csv
import hashlib
import itertools
import json
import re
import subprocess
from datetime import datetime
from pathlib import Path, PurePosixPath


def release_component(value):
    if not isinstance(value, str) or not re.fullmatch(
        r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]+)?Z", value
    ):
        raise ValueError(f"invalid UTC release timestamp: {value!r}")
    datetime.fromisoformat(value[:19])  # Validate calendar/time, never round fractional identity.
    return value.replace(":", "-")


def check_instrument(value):
    if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", value):
        raise ValueError(f"invalid instrument ID: {value!r}")
    return value


def read_json(path):
    def unique_pairs(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key: {key}")
            result[key] = value
        return result
    return json.loads(Path(path).read_text(encoding="utf-8"), object_pairs_hook=unique_pairs)


def json_bytes(value):
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n").encode()


def fingerprint(path):
    checksum = hashlib.sha256()
    size = 0
    with Path(path).open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            checksum.update(chunk)
            size += len(chunk)
    return size, checksum.hexdigest()


def inspect_source_geocsv(path, instrument_id):
    """Require schema 1.0.0 identity; leave full parsing to the consumer validator."""
    created = []
    station_index = None
    count = 0
    with Path(path).open(encoding="utf-8", newline="") as stream:
        lines = iter(stream)
        if next(lines, "").rstrip("\r\n") != "# MERMAID GeoCSV schema: 1.0.0":
            raise ValueError(f"{path}: requires first-line MERMAID GeoCSV schema: 1.0.0 declaration")
        for line in lines:
            if line.startswith("#"):
                if station_index is not None:
                    raise ValueError(f"{path}: comments after the column header are invalid")
                if line.startswith("# MERMAID GeoCSV schema:"):
                    raise ValueError(f"{path}: duplicate MERMAID GeoCSV schema declaration")
                match = re.match(r"#\s*created\s*:\s*(.*?)\s*$", line)
                if match:
                    declaration = line.rstrip("\r\n")
                    if not re.fullmatch(r"#created: [0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{6}Z", declaration):
                        raise ValueError(f"{path}: schema 1.0.0 requires literal #created: and six-digit UTC timestamp")
                    value = declaration.removeprefix("#created: ")
                    release_component(value)
                    created.append(value)
                continue
            if not line.strip():
                raise ValueError(f"{path}: empty record")
            # csv.reader consumes any continuation lines in a quoted record.
            row = next(csv.reader(itertools.chain([line], lines), strict=True))
            if station_index is None:
                if row.count("Station") != 1:
                    raise ValueError(f"{path}: requires one Station column")
                width = len(row)
                station_index = row.index("Station")
            else:
                if len(row) != width or row[station_index] != instrument_id:
                    raise ValueError(f"{path}: ambiguous/mismatched Station; expected {instrument_id}")
                count += 1
    if len(created) != 1:
        raise ValueError(f"{path}: requires exactly one valid UTC #created, found {len(created)}")
    if station_index is None:
        raise ValueError(f"{path}: missing header")
    return created[0], count


def inspect_geocsv(path, instrument_id):
    created, count = inspect_source_geocsv(path, instrument_id)
    if not count:
        raise ValueError(f"{path}: no instrument records")
    return created


def check_manifest(manifest):
    if not isinstance(manifest, dict):
        raise ValueError("manifest must be an object")
    release_component(manifest.get("release_id"))
    if manifest.get("testing_only") is not True:
        raise ValueError("current publication phase requires testing_only=true")
    entries = manifest.get("files")
    if not isinstance(entries, list) or not entries:
        raise ValueError("snapshot requires a nonempty complete files inventory")
    instruments, filenames = set(), set()
    for entry in entries:
        instrument = check_instrument(entry.get("instrument_id"))
        filename = entry.get("filename")
        if filename != f"{instrument}.geocsv":
            raise ValueError(f"invalid snapshot filename: {filename}")
        if instrument in instruments or filename in filenames:
            raise ValueError(f"duplicate instrument or filename: {instrument}")
        instruments.add(instrument)
        filenames.add(filename)
        if type(entry.get("size_bytes")) is not int or entry["size_bytes"] < 0:
            raise ValueError("invalid size_bytes")
        if not isinstance(entry.get("sha256"), str) or not re.fullmatch(r"[0-9a-f]{64}", entry["sha256"]):
            raise ValueError("invalid SHA-256")
        if not isinstance(entry.get("provenance"), dict):
            raise ValueError("missing provenance object")
    return entries


def verify_candidate(directory):
    directory = Path(directory).resolve()
    manifest_path = directory / "manifest.json"
    if manifest_path.is_symlink():
        raise ValueError("candidate manifest cannot be a symlink")
    manifest = read_json(manifest_path)
    entries = check_manifest(manifest)
    if manifest["testing_only"] and (directory.parent.name != "snapshots" or directory.parent.parent.name != "testing"):
        raise ValueError("testing snapshot must be under <workspace>/testing/snapshots/<snapshot ID>/")
    if directory.name != release_component(manifest["release_id"]):
        raise ValueError("candidate directory must use the hyphenated release component")
    expected = {"manifest.json", "source_provenance.json", *(entry["filename"] for entry in entries)}
    if {path.name for path in directory.iterdir()} != expected:
        raise ValueError("candidate inventory differs from frozen manifest")
    provenance_path = directory / "source_provenance.json"
    if provenance_path.is_symlink() or not provenance_path.is_file():
        raise ValueError("source provenance must be a regular file")
    provenance = read_json(provenance_path)
    if not isinstance(provenance, dict) or set(provenance) != {"schema_version", "git"} or type(provenance["schema_version"]) is not int or provenance["schema_version"] != 1:
        raise ValueError("invalid source provenance")
    revision = provenance["git"]
    if revision is not None:
        if (not isinstance(revision, dict) or set(revision) != {"commit", "source_subdirectory"}
                or not isinstance(revision["commit"], str) or not re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", revision["commit"])
                or not isinstance(revision["source_subdirectory"], str)
                or PurePosixPath(revision["source_subdirectory"]).is_absolute()
                or ".." in PurePosixPath(revision["source_subdirectory"]).parts):
            raise ValueError("invalid Git source provenance")
    for entry in entries:
        path = directory / entry["filename"]
        if path.is_symlink() or not path.is_file():
            raise ValueError(f"not a regular candidate file: {path}")
        if fingerprint(path) != (entry["size_bytes"], entry["sha256"]):
            raise ValueError(f"candidate bytes changed: {path}")
        if inspect_geocsv(path, entry["instrument_id"]) != manifest["release_id"]:
            raise ValueError(f"candidate #created differs from manifest: {path}")
    return manifest


def require_external_workspace(workspace, source_root):
    workspace, source_root = Path(workspace).resolve(), Path(source_root).resolve()
    if workspace == source_root or source_root in workspace.parents:
        raise ValueError("publication workspace must be outside the protected source tree")
    if workspace == source_root.parent or workspace in source_root.parents:
        raise ValueError("publication workspace must not contain the protected source tree")
    software_root = Path(__file__).resolve().parents[2]
    if workspace == software_root or software_root in workspace.parents:
        raise ValueError("publication workspace must be outside the software checkout")
    repository = git_repository(workspace)
    if repository is not None:
        if repository == git_repository(source_root):
            raise ValueError("use a dedicated Git publication archive")
        if (repository / "pyproject.toml").exists() or (repository / "scripts").is_dir() or (repository / "workers").is_dir():
            raise ValueError("publication workspace must not be a software checkout")
    return workspace


def git_command(directory, *arguments):
    """Run a Git operation without exposing configuration or credentials."""
    result = subprocess.run(["git", "-C", str(directory), *arguments], capture_output=True, text=True)
    if result.returncode:
        raise ValueError(f"Git operation failed: {arguments[0]}")
    return result.stdout.strip()


def git_repository(directory):
    """Find a working tree, including .git files used by linked worktrees."""
    directory = Path(directory).resolve()
    while not directory.exists():
        directory = directory.parent
    if not any((parent / ".git").exists() for parent in (directory, *directory.parents)):
        return None
    return Path(git_command(directory, "rev-parse", "--show-toplevel")).resolve()


def source_provenance(source_root):
    """Require a clean Git source when present; ordinary directories are valid."""
    source_root = Path(source_root).resolve(strict=True)
    repository = git_repository(source_root)
    revision = None
    if repository is not None:
        if git_command(repository, "status", "--porcelain=v1", "--untracked-files=all", "--ignore-submodules=none"):
            raise ValueError("source Git working tree must be clean")
        revision = {"commit": git_command(repository, "rev-parse", "--verify", "HEAD"),
                    "source_subdirectory": source_root.relative_to(repository).as_posix()}
    return {"schema_version": 1, "git": revision}


def check_source_provenance(candidate, source_root):
    path = Path(candidate) / "source_provenance.json"
    if read_json(path) != source_provenance(source_root):
        raise ValueError("source Git revision or tracking state differs from snapshot")
    return fingerprint(path)[1]
