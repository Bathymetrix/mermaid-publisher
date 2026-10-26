# mermaid-publisher

Create, validate, gate and publish immutable MERMAID data snapshots.

This repository contains maintainer tools. GeoCSV is the only implemented
workflow, under `scripts/geocsv/`. Future data types can use sibling directories.
Scientific GeoCSV APIs remain in `mermaid-geocsv`; Bathymetrix hosting remains in
`bathymetrix-site`. Repository version: **0.2.0**, independently maintained in
`VERSION`. No formal software or production data release has been published.

## Setup

Python 3.12 is the tested operator runtime. Create the repository's environment
once, then install the fixed consumer baseline and scientific/transport dependencies:

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements/geocsv.txt
```

The requirement pins `mermaid-geocsv` to an exact source commit. CI runs both
that frozen consumer and an explicitly selected current consumer. Updating the
baseline is a compatibility decision, not a routine dependency refresh.
The [2026-10-26 baseline review](docs/geocsv/CONSUMER_BASELINE_REVIEW.md)
records the reader-module rename, preserved historical fingerprints and the
requirement for fresh validation before another publication.
`boto3` is used only for publication transport; snapshot creation uses the
standard library. Dependency versions and code hashes are recorded in reports.

## GeoCSV workflow

| File | Responsibility |
| --- | --- |
| `create_snapshot.py` | Stage verbatim GeoCSV and freeze inventory, manifest and source provenance |
| `inspect_snapshot.py` | Internal snapshot integrity and source/workspace checks |
| `validate_snapshot.py` | Scientific comparisons and complete archive report |
| `_verify_sac.py` | Internal final-waveform, projection and scratch-export verification |
| `gate_snapshot.py` | Internal current-evidence publication gate |
| `publish_snapshot.py` | Transfer, exact-byte checks, latest activation and local archive recording |

The three commands run directly with `.venv/bin/python scripts/geocsv/<file>`.
Use [the workflow guide](docs/geocsv/WORKFLOW.md) for complete commands.

Creation freezes all instruments by default; `--instruments P0006 P0045`
freezes only those IDs. Validation covers every original pair for the frozen
instruments, and publishing transfers that exact snapshot without selection.
Create and validate can use an ordinary temporary workspace without Git or any
publication intent. Only publishing requires the dedicated persistent archive.

The canonical external archive is `$MERMAID/publisher`, a separate local Git
repository. Testing GeoCSV artifacts reside under
`geocsv/testing/{snapshots,staging,validation,publications}`.
Original MiniSEED/SAC archives remain at their source; only their evidence is archived.

All hosted data are **testing only**. Current commands require explicit HTTPS
collection URLs ending in `/testing/` and storage prefixes ending in `/testing`.
Production promotion, remote uploads and deployment require explicit authorization.
The initial P0006/P0045 testing snapshot was published on 2026-10-26. Live
conditional-write rejection, exact-byte downloads, caching, fetch modes and all
3,292 scientific waveform-pair comparisons passed. See the
[publication findings](docs/geocsv/SCHEMA3_FINDINGS.md#initial-hosted-testing-publication--2026-10-26).
Further uploads and production promotion still require explicit authorization.
No credentials or private deployment configuration belong in either Git repository.

## Documentation

- [Create, validate, gate, publish and recover](docs/geocsv/WORKFLOW.md)
- [Publication/download contract](docs/geocsv/CONTRACT.md)
- [Scientific checks and report schema 3](docs/geocsv/VALIDATION.md)
- [Historical version-2 archive findings](docs/geocsv/ARCHIVE_FINDINGS.md)
- [Fresh schema-3 full-corpus and testing-batch findings](docs/geocsv/SCHEMA3_FINDINGS.md)

## SAC header compatibility

Current consumers use `associate(..., create_sac_header=True)` and ObsPy writing.
The publisher retains the former exporter checks in `_verify_sac.py` and keeps
the fixed 0.24.0 consumer supported through its original public writer. The
baseline pin and historical download fixtures are unchanged. See the
[complete verification migration inventory](docs/geocsv/SAC_VERIFICATION.md).

## Verification

```bash
MERMAID_CONSUMER_BASELINE=1 .venv/bin/python -B -m unittest discover -s tests -v
```

To test the adjacent refactored consumer without changing the pinned install:

```bash
PYTHONPATH=../mermaid-geocsv/src MERMAID_CONSUMER_BASELINE=0 \
  .venv/bin/python -B -m unittest discover -s tests -v
```

Tests use synthetic sources, temporary Git repositories and localhost HTTP.
They do not access canonical data or publish remotely. The historical 43,365-pair
pass predates this migration and does not accept a new candidate or schema-3 report.

Developed and maintained by [Bathymetrix®](https://bathymetrix.com).
