# mermaid-publisher

Create, validate and publish immutable MERMAID GeoCSV snapshots using the
public `mermaid-geocsv` APIs and ObsPy. Automaid owns scientific source
generation; `bathymetrix-site` owns read-only hosting.

## Installation

From this repository root, create a fresh Python 3.12 environment and install
the adjacent consumer with the scientific and transport requirements. The
consumer is installed as a regular package, not in editable mode:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements/geocsv.txt ../mermaid-geocsv
python -m pip check
python -B -m unittest discover -s tests -v
```

Activate `.venv` in each new shell session before running publisher commands.
Python >= 3.11 and mermaid-geocsv >= 0.29.0 are required. Python 3.12 is
the documented full-suite setup. Only dataset-first payloads in the MERMAID
1.0.0 schema family are supported. Repository version authority is `version`;
validation reports use schema 5. Reports bind the exact installed software
and code hashes, not just version numbers.

## Workflow

With `.venv` active, the three commands run as `python scripts/geocsv/<file>`:

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
`geocsv/testing/{snapshots,staging,validation,bundles,reports,publications}`. Sources remain
read-only; original waveform archives are not copied. Selection is frozen at
creation; validation and transfer cover that exact inventory.

### External inputs

- `--source-root` reads canonical source data from `$MERMAID/processed`.
- `--workspace` names the base publication archive workspace,
  `$MERMAID/publisher/geocsv`. `--inventory` explicitly selects the reviewed
  instrument-mapping CSV and overrides the configured default.
- `MERMAID_PUBLISHER_GEOCSV_CONFIG` optionally names a private directory
  containing `instruments.csv` and `r2.json`. Creation uses `instruments.csv`
  when `--inventory` is omitted; publication reads destination settings and an
  optional SDK profile from `r2.json`. Explicit destination command options
  override file settings. The former `MERMAID_PUBLISHER_CONFIG` name is not read.
- For remote publication, boto3 resolves credentials through its SDK provider,
  commonly from `~/.aws/credentials` and `~/.aws/config` or AWS environment
  variables. The publisher does not read credential values from the JSON
  settings file. Keep credentials outside the software and publication archive.

Publication also builds `MERMAID.geocsv.tar.gz` from the manifested instrument
files. The bundle is served beside them, outside `manifest.files`; individual
hashes and the scientific report are unchanged. Archive pages use a plain
clickable directory tree, with a page for each release directory.

All hosted data are **testing only**. The current full-corpus rc1 snapshot is approved for testing;
production scope and licensing remain unresolved. Scientific acceptance does not
authorize uploads, deployment, retirement or production activation. Publication
requires an isolated HTTPS testing destination, licensing/citation approval and
explicit upload authorization. Private settings and credentials remain outside
checkouts; the SDK resolves credentials.

## Documentation

- [Publisher release audit and linked consumer checklist](docs/geocsv/release-audit-2026-11-06.md)
- [Full-corpus rc1 testing publication](docs/geocsv/full-corpus-rc1-publication.md)
- [Create, validate, publish and recover](docs/geocsv/workflow.md)
- [Publication/download contract](docs/geocsv/contract.md)
- [Scientific comparisons and report schema](docs/geocsv/validation.md)
- [Final waveform and SAC export checks](docs/geocsv/sac-verification.md)
- [Artifact-bound evidence](docs/geocsv/evidence.md)
- [Production pre-release checklist](docs/geocsv/pre-release-checklist.md)
- [Hosting runbook](../bathymetrix-site/docs/geocsv-hosting.md)

## Verification

```bash
python -B -m unittest discover -s tests -v
```

Tests use synthetic temporary inputs, mocked storage and disposable fixture
Git repositories. They do not publish real data or modify the publication
archive. Changed candidate/source bytes or validation software require fresh
acceptance; existing manifests, reports and receipts remain immutable.

Every nonempty published dataset requires GPS Position measurements that bracket
all row timestamps, inclusively and without tolerance. Producer exclusions are
retained locally in `outside_filterDate_gps.geocsv`; this audit file is not uploaded.

See [publication reports](docs/geocsv/publication-reports.md) for mandatory Recording
coverage, producer clash verification, schema-5 names and published mapping/diff
reports.

IcCycle and Init waveform paths are excluded from publisher validation and accounting.
Directory or filename components containing `IcCycle` or `Init` (case-insensitive) are
skipped before opening or fingerprinting files, including for recordless-source
checks. GeoCSV is copied verbatim: Recording rows supported only by excluded
waveforms still fail mandatory coverage. The clean-source Git requirement is
unchanged. Publisher 0.6.1 requires fresh validation evidence for this scope;
existing reports and snapshots remain immutable.
