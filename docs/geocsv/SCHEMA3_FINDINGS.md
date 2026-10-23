# Fresh schema-3 validation findings — 2026-10-23

Release ID: `2026-10-21T22:48:33.277Z`.

Two separate frozen snapshots were created and validated with publisher 0.1.0.
Both fresh schema-3 reports passed the current scientific acceptance gate.
The full-corpus check uses an ordinary temporary workspace. The publication
archive contains only the independently accepted P0006/P0045 candidate.
No data were uploaded and no latest pointer or publication receipt was created.

## Inputs and software

The read-only canonical source was `$MERMAID/processed`, at clean Git commit
`ac10d037f824084693813d62851728a7691374d7`. Source provenance was checked
during creation, validation and acceptance. Complete waveform-input fingerprints
were checked during validation and acceptance.

The previous temporary inventory was absent. The 112-entry inventory was
reconstructed using the earlier run’s recorded procedure: explicit Station
values for nonempty sources and the nine previously documented recordless IDs.
Every Station record, serial coverage and ID uniqueness was checked. No ID was
inferred from a serial suffix. The mapping remains outside the repositories;
its SHA-256 is `054cc4174bc08dd5b311343aa069d110a13f8f0e16912ed04ec6dd9dc67caece`.

The installed consumer matched every fixed-baseline Python-source fingerprint:
`mermaid-geocsv` 0.24.0 at `c1eb805e420f7f8d4bfb8c6f737316c9f5766534`.
The environment used Python 3.12.4, NumPy 2.5.3, pandas 3.0.6 and ObsPy 1.5.1.
No scientific limits, consumer behavior or download formats changed.

## Complete accounting

| Accounting | Full corpus | P0006/P0045 |
| --- | ---: | ---: |
| Source instruments accounted for | 112 | 2 |
| Frozen GeoCSV payloads | 103 | 2 |
| Recordless sources excluded | 9 | 0 |
| Original MiniSEED/SAC pairs | 43,365 | 3,292 |
| Pairs passing all scientific checks | 43,365 | 3,292 |
| Failed pairs | 0 | 0 |
| Missing pairs | 0 | 0 |
| Unsupported pairs | 0 | 0 |
| Unexamined pairs | 0 | 0 |

P0006 contributed 833 pairs and P0045 contributed 2,459 pairs. The full-corpus
recordless exclusions remain R0060, S0081, S0082, S0085, S0086, S0087, S0090,
S0092 and S0094. Their unchanged GeoCSV files were not staged; local staging
evidence accounts for each exclusion. Spectra remain outside scope and were
neither read nor counted. Original waveform archives were not copied.

Native samples and SAC float32 intervals were preserved exactly. Independent
reference intervals differed by zero ULP for 32,400 full-corpus pairs and one
ULP for 10,965; selected-candidate counts were 2,415 and 877. The maximum
interval difference was 7.450580596923828e-9 seconds. Native first-sample times
matched exactly; independent-reference differences were at most 1,000 ns.
These are the unchanged [versioned comparison rules](VALIDATION.md).

## Separate immutable evidence

| Scope | Manifest SHA-256 | Report SHA-256 |
| --- | --- | --- |
| Full corpus | `16350b6b996de621fe0c07cdb4c44fb1de5744d5f0866c9687e042a670518500` | `bd0bb5f32a8c376fbf9fecba38cbd3f6077b9908ee691100b4d630487bb6f7cf` |
| P0006/P0045 | `dd1eb6c41196c46458d0fc259a1d8fb1bd091ece29ba94253888784f0c27736b` | `4efa2caf0ec0210db79cc71a63c24c82caa1bd247260e95c0a3b1cbfe7c616d9` |

The full report completed at `2026-10-23T22:57:36.276296Z`; the selected report
completed at `2026-10-23T22:55:00.712181Z`. Both use `validation-v3.json` under
`validation/2026-10-21T22%3A48%3A33.277Z/`, outside their frozen candidate
directories.
Each report binds its own exact manifest, source provenance, staging inventory,
input fingerprints, pair coverage, scientific results and software fingerprints.
Neither report accepts the other snapshot. Both manifests retain
`testing_only: true`.

The full snapshot, report and run log remain in their temporary workspace,
with no archival obligation or publication intent. The P0006/P0045 snapshot,
staging inventory, report, run log and read-only acceptance plan remain under
`$MERMAID/publisher/geocsv/`. Its frozen staging schema 2 explicitly contains
only P0006 and P0045. There are no publication receipts or archive commits yet.

The read-only `publish_snapshot.py --plan` gate passed for each snapshot and
reported `gate passed; no publication performed`. These checks performed no
network transfer or Git recording. Acceptance must be rechecked against the
current source and code before a separately authorized upload.
