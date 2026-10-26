# Consumer baseline review — 2026-10-26

## Decision and source comparison

The active consumer baseline remains `mermaid-geocsv` 0.24.0 and advances from
`c1eb805e420f7f8d4bfb8c6f737316c9f5766534` to
`33ed5ff477b6c44447d472fc8e828b5ae930e0db`.

Comparison of the complete package source and `pyproject.toml` establishes:

- `read.py` becomes `_read.py` with identical bytes and SHA-256
  `cc6be8b0a73376fd23581c1ca564f6d15a02edc039b3661e44d7697acf678afb`.
- `__init__.py`, `_associate.py` and `_write_sac.py` each update one import.
- `_fetch.py`, scientific implementation logic, package version, dependencies
  and packaging configuration are unchanged.
- Other changes between these revisions concern documentation, tutorial text,
  audit links and repository instructions.

The supported public operations remain `geocsv.read`, `associate`, `write_sac`
and `fetch`. Private reader-module imports are not supported public interfaces.
No manifest format, path, checksum, testing flag, scientific tolerance or report
schema changes are introduced.

## Installation and retained evidence

`requirements/geocsv.txt` pins the new full commit. The publisher's `.venv`
contains a separate, noneditable installation built from that exact local Git
revision with no dependency changes. Installed Python-source filenames and
hashes must match `tests/geocsv/fixtures/consumer_baseline.json`.

The former baseline fixture is retained byte-for-byte as
`tests/geocsv/fixtures/consumer_baseline_c1eb805.json`. Historical download
`manifest.json` and `P0006.geocsv` fixtures remain unchanged. Historical findings,
archived reports, publication receipts and already hosted bytes remain unchanged.

Reports bind filenames and code hashes as well as package versions. Version
0.24.0 alone therefore does not make old evidence current under the new
installation. Before another publication, generate a distinct exhaustive report
for the exact candidate with the active consumer and pass the publication gate.
Preserve previous evidence. The already published testing snapshot keeps its
original immutable validation report; do not overwrite it to refresh evidence.

## Initial compatibility verification

The following checks passed on 2026-10-26:

- Before installation, both focused publisher fetch-compatibility tests passed
  against the original installed baseline, including the historical manifest.
- After installation, all 55 publisher tests passed with
  `MERMAID_CONSUMER_BASELINE=1`. These cover historical download bytes,
  latest/pinned memory/disk fetch, scientific comparisons, publication gating,
  testing isolation and local Git recording/recovery using temporary fixtures.
- The consumer checkout passed 463 tests across `test_read.py`,
  `test_associate_synthetic.py`, `test_associate.py`, `test_write_sac.py`,
  `test_fetch.py` and `test_tutorials.py`, using its existing `.venv` and pytest
  source configuration. Nine expected noninteractive Matplotlib warnings remain.
- Installed source hashes and installation commit provenance match the new
  baseline; the installation is noneditable and contains `_read.py` instead of
  `read.py`. `pip check` found no broken requirements. NumPy 2.5.3, pandas 3.0.6,
  ObsPy 1.5.1 and boto3 1.43.118 remain unchanged.
- The historical baseline fixture and both historical download fixture files
  were compared byte-for-byte with their previous committed versions.

These are local compatibility checks, not fresh canonical-corpus acceptance or
live hosting verification. No real source data, archive evidence, hosted objects
or pointers were modified, and no new publication was attempted.

The related consumer hosting guide records the new pin. Website serving behavior
and its deployment configuration do not depend on the private reader-module
name; no Worker change or deployment is required.

## Completed local acceptance refresh

The follow-up on 2026-10-26 rechecked consumer history and public imports. Commit
`33ed5ff477b6c44447d472fc8e828b5ae930e0db` remains the exact completed-rename
baseline. Current consumer HEAD `5815832e9c5877e010a7295b2949cf4e45042795`
differs only in `docs/HOSTING.md`; its package sources and packaging configuration
match the baseline. No additional pin or fingerprint change is required.

Both consumer revisions were installed separately in the existing publisher
`.venv`, without dependency changes, and checked using the CI test modes:

```bash
# With current consumer 5815832 installed:
MERMAID_CONSUMER_BASELINE=0 .venv/bin/python -B -m unittest discover -s tests -v
# After restoring frozen consumer 33ed5ff:
MERMAID_CONSUMER_BASELINE=1 .venv/bin/python -B -m unittest discover -s tests -v
```

Both runs passed all 55 tests. The final installation is noneditable at the
frozen full commit, with source hashes matching the active baseline fixture;
`pip check` passed. Public imports remain `from mermaid import geocsv` and
`geocsv.read`, `associate`, `write_sac` and `fetch`.

The published `validation-v3-testing-layout.json` report was rejected for a new
acceptance decision with `validation code or dependency versions differ; rerun
validation`, as expected. Its bytes remain unchanged. A distinct, exclusively
created local report then passed every original pair for the existing
P0006/P0045 candidate and passed `publish_snapshot.py --plan`. No creation or
full-corpus run was performed. The new report, hashes and pair accounting are
recorded in the [local revalidation findings](SCHEMA3_FINDINGS.md#local-consumer-baseline-revalidation--2026-10-26).

This refresh adds local evidence only. It does not replace the original published
report or alter hosted objects, pointers, archive history, hosting or DNS.
