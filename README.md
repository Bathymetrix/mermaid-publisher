# mermaid-publisher

Create, validate and publish immutable MERMAID GeoCSV snapshots using the
public `mermaid-geocsv` APIs and ObsPy. Automaid owns scientific source
generation; `bathymetrix-site` owns read-only hosting.

## Installation

Use this repository's existing `.venv`. Install the adjacent consumer and the
scientific/transport requirements together:

```bash
.venv/bin/python -m pip install ../mermaid-geocsv -r requirements/geocsv.txt
.venv/bin/python -m pip check
```

Python >= 3.11 and mermaid-geocsv >= 0.27.0 are required. Only MERMAID payload
schema 1.0.0 is supported. Repository version authority is `version`;
validation reports use schema 4. Reports bind the exact installed software
and code hashes, not just version numbers.

## Workflow

The three commands run as `.venv/bin/python scripts/geocsv/<file>`:

| Command | Responsibility |
| --- | --- |
| `create_snapshot.py` | Copy verbatim GeoCSV and freeze instrument scope, manifest and source provenance |
| `validate_snapshot.py` | Examine every original MiniSEED/SAC pair in that scope |
| `publish_snapshot.py` | Gate evidence, transfer, verify public bytes, activate latest last and record the publication |

`inspect_snapshot.py`, `gate_snapshot.py` and `_verify_sac.py` are internal
integrity, acceptance and export-verification modules.

Create and validate accept ordinary temporary workspaces without Git or
publication intent. Actual publication requires the dedicated Git archive
`$MERMAID/publisher`, with artifacts under
`geocsv/testing/{snapshots,staging,validation,bundles,publications}`. Sources remain
read-only; original waveform archives are not copied. Selection is frozen at
creation; validation and transfer cover that exact inventory.

Publication also builds `MERMAID.geocsv.tar.gz` from the manifested instrument
files. The bundle is served beside them, outside `manifest.files`; individual
hashes and the scientific report are unchanged. Archive pages use a plain
clickable directory tree, with a page for each release directory.

All hosted data are **testing only**. The approved hosted scope is P0006/P0045;
full-corpus licensing remains unresolved. Scientific acceptance does not
authorize uploads, deployment, retirement or production activation. Publication
requires an isolated HTTPS testing destination, licensing/citation approval and
explicit upload authorization. Private settings and credentials remain outside
checkouts; the SDK resolves credentials.

## Documentation

- [Create, validate, publish and recover](docs/geocsv/workflow.md)
- [Publication/download contract](docs/geocsv/contract.md)
- [Scientific comparisons and report schema](docs/geocsv/validation.md)
- [Final waveform and SAC export checks](docs/geocsv/sac-verification.md)
- [Artifact-bound evidence](docs/geocsv/evidence.md)
- [Hosting runbook](../bathymetrix-site/docs/geocsv-hosting.md)

## Verification

```bash
.venv/bin/python -B -m unittest discover -s tests -v
```

Tests use synthetic temporary inputs, mocked storage and disposable fixture
Git repositories. They do not publish real data or modify the publication
archive. Changed candidate/source bytes or validation software require fresh
acceptance; existing manifests, reports and receipts remain immutable.
