# mermaid-publisher

Create, validate, gate and publish immutable MERMAID data snapshots.

This repository contains maintainer tools. GeoCSV is the only implemented
workflow, under `scripts/geocsv/`. Future data types can use sibling directories.
Scientific GeoCSV APIs remain in `mermaid-geocsv`; Bathymetrix hosting remains in
`bathymetrix-site`. Repository version: **0.4.1**, independently maintained in
`version`. No formal software or production data release has been published.

## Local installation

Use the existing environment and install the adjacent migrated consumer with
its declared scientific/transport dependencies. Before consumer 0.27.0 is
released, use the local checkout in the same pip invocation:

```bash
.venv/bin/python -m pip install --force-reinstall ../mermaid-geocsv -r requirements/geocsv.txt
.venv/bin/python -m pip check
```

Publisher 0.4.1 requires mermaid-geocsv >= 0.27.0 and supports only payload
schema 1.0.0. Creation and candidate inspection require its exact first-line
declaration and six-digit UTC `#created`; full parsing and scientific validation
use the consumer. Historical consumer pins and fixture
bytes remain evidence, without an active legacy reader/exporter path. Installed
versions and loaded source hashes are bound into every fresh report.

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
Use [the workflow guide](docs/geocsv/workflow.md) for complete commands.

Creation freezes all instruments by default; `--instruments P0006 P0045`
freezes only those IDs. Validation covers every original pair for the frozen
instruments, and publishing transfers that exact snapshot without selection.
Create and validate can use an ordinary temporary workspace without Git or any
publication intent. Only publishing requires the dedicated persistent archive.

The canonical external archive is `$MERMAID/publisher`, a separate local Git
repository. Testing GeoCSV artifacts reside under
`geocsv/testing/{snapshots,staging,validation,publications}`.
New release components replace only creation-timestamp colons with hyphens;
GeoCSV bytes and literal release IDs remain unchanged. The authorized
replacement testing set requires updated fetch/hosting code. Its old URLs may
be retired; see the [compatibility review](docs/geocsv/release-path-review.md).
Original MiniSEED/SAC archives remain at their source; only their evidence is archived.

All hosted data are **testing only**. Current commands require explicit HTTPS
collection URLs ending in `/testing/` and storage prefixes ending in `/testing`.
Production promotion, remote uploads and deployment require explicit authorization.
The initial P0006/P0045 testing snapshot was published on 2026-10-26. Live
conditional-write rejection, exact-byte downloads, caching, fetch modes and all
3,292 scientific waveform-pair comparisons passed. See the
[publication findings](docs/geocsv/schema3-findings.md#initial-hosted-testing-publication--2026-10-26).
The authorized 2026-10-28 replacement now serves the same data and manifest
under hyphenated paths. Its fresh scientific report passed all 3,292 pairs;
latest/pinned and disk/memory fetch passed, and the four old testing objects
were retired. [Replacement evidence](docs/geocsv/release-path-review.md) records
the deployed Worker, receipt and local archive commit. Further uploads and
production promotion still require explicit authorization.
No credentials or private deployment configuration belong in either Git repository.

## Documentation

- [Create, validate, gate, publish and recover](docs/geocsv/workflow.md)
- [Publication/download contract](docs/geocsv/contract.md)
- [Hyphenated path review and testing replacement](docs/geocsv/release-path-review.md)
- [Scientific checks and report schema 4](docs/geocsv/validation.md)
- [Historical version-2 archive findings](docs/geocsv/archive-findings.md)
- [Fresh schema-3 full-corpus and testing-batch findings](docs/geocsv/schema3-findings.md)

## SAC header compatibility

Current consumers use `associate(..., create_sac_header=True)` and ObsPy writing.
The publisher retains the former exporter checks in `_verify_sac.py` and keeps
historical 0.24.0 evidence unchanged. The active path requires consumer >= 0.27.0
with fresh SAC header creation; no legacy exporter branch remains. See the
[complete verification migration inventory](docs/geocsv/sac-verification.md).

## Verification

```bash
.venv/bin/python -B -m unittest discover -s tests -v
```

Tests use synthetic temporary inputs, mocked remote storage and disposable
fixture Git repositories. They do not publish real data or modify the real
publication archive. Scientific validation uses only public consumer APIs,
`associate(..., create_sac_header=True)`, ObsPy writing and publisher-owned
export comparisons. Schema-4 reports use `recording_records`; comparison limits
are unchanged. The historical 0.24.0 evidence and schema-3 reports remain intact.

Local schema migration and candidate acceptance do not establish a software
release, compatible hosted payloads, deployment or publication authorization.
