> **AI-written documentation — non-authoritative.** Verify findings against the frozen candidate, generation provenance and validation report.

# Local PPHC rc1 snapshot validation — 2026-11-05

A testing-only P0006/P0045 snapshot was generated with automaid v4.10.0,
created and validated with publisher 0.8.0 and consumer 0.29.0, and accepted by
the local report-schema-5 gate. Payload schema is `1.0.0-rc1`. No upload,
latest activation, archive commit, deployment, tag or release occurred.

Literal snapshot identity: `2026-11-05T17:40:39.379513Z`.

| Instrument | Recording rows | Original waveform pairs passed |
| --- | ---: | ---: |
| P0006 | 828 | 833 |
| P0045 | 2,455 | 2,455 |
| Total | 3,283 | 3,288 |

Failures, missing pairs, unsupported inputs and unexamined pairs are all zero.
Complete Recording coverage and the producer's exact-byte-bound clash reports
passed. Validation excludes Init/IcCycle waveform namespaces under the current
publisher scope; all copied waveforms, including excluded products, match the
canonical originals byte-for-byte. Scientific comparison limits are unchanged.
This selected candidate does not establish full-corpus acceptance.

Only the saved-cycle GeoCSV writer ran, under conda `pymaid3.10`, with explicit
temporary outputs and deployment bounds. GPS/cycle/clock processing, waveform
production and mirror refresh did not run. Canonical GeoCSV and pickle hashes
were rechecked unchanged. Generated scientific data-record bytes match canonical
rows after excluding only the actual producer revision from comparison. Headers,
creation identity, producer labels and hashes change. The source directory is
an ordinary isolated directory with truthful `git: null` provenance, not a
claimed clean commit of regenerated products.

## Verification

- Installed consumer suite: 425 passed, 9 expected warnings
- Publisher suite: 115 passed
- Worker suite: 23 passed; serving code unchanged
- Final standalone tutorial execution/parity: 27 passed, 9 expected warnings
- Installed-wheel smoke: read, associate, fresh SAC headers and ObsPy export passed
- Local real-candidate HTTP: 8 latest/pinned × one/all × memory/disk fetch/read modes,
  4 disk-reuse checks, and 2 native-waveform/SAC pipelines passed

The raw rc1 schema declaration, normalized comment metadata and exact creation
identity survive read/fetch/association provenance. Header syntax padding is
normalized; literal data cells and raw comments retain their source characters.
Published old-header snapshots remain downloadable as bytes but are rejected
by the new dataset-first reader. No public rc1 snapshot has been published.

## Evidence bindings

Local evidence root: `/private/tmp/mermaid-pphc-rc1-f05iq5l9/`.
The candidate is under `candidate/testing/snapshots/2026-11-05T17-40-39.379513Z/`;
the scientific report is
`candidate/testing/validation/2026-11-05T17-40-39.379513Z/validation.json`.

Manifest SHA-256: `8fb7116977992cb961c6e52131b60bed35f84ce86ba1e90a301a75127e9df58d`.

Report SHA-256: `46fd70141add8a52c3707abec56a95b9f6f7fec6ba8c6ac47f83cb19cfcace61`.

`generation.json` records source pickle/original-output hashes and value-preservation
checks; `protected-source-check.json` records original waveform equality.
`gate-summary.json`, `client-verification.json`, the run logs and scripts retain
local verification evidence. Temporary evidence is not a persistent publication
archive. Reports remain bound to the exact input bytes, software and selected
scope; changes require fresh acceptance. Staging software edits does not commit,
publish or authorize a later upload. Final schema 1.0.0 is reserved for paper
publication, independent of software package versions.
