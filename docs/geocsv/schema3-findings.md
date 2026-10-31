# Fresh schema-3 validation findings — 2026-10-23

The dated findings below retain their original paths and software provenance.
The 2026-10-28 [hyphenated-path replacement](release-path-review.md) supersedes
the original hosted testing paths; their encoded URLs have been retired.
Historical local evidence is retained.

Release ID: `2026-10-21T22:48:33.277Z`.

Two separate frozen snapshots were created and validated with publisher 0.1.0.
Independent schema-3 reports passed the scientific acceptance gate. Current
acceptance is refreshed after local layout changes as recorded below.
The full-corpus check uses an ordinary temporary workspace. The publication
archive contains only the independently accepted P0006/P0045 candidate.
At the 2026-10-23 validation stage, no data were uploaded and no latest pointer
or publication receipt was created. The separately authorized initial testing
publication on 2026-10-26 is recorded below.

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
These are the unchanged [versioned comparison rules](validation.md).

## Initial immutable evidence before the local layout change

| Scope | Manifest SHA-256 | Report SHA-256 |
| --- | --- | --- |
| Full corpus | `16350b6b996de621fe0c07cdb4c44fb1de5744d5f0866c9687e042a670518500` | `bd0bb5f32a8c376fbf9fecba38cbd3f6077b9908ee691100b4d630487bb6f7cf` |
| P0006/P0045 | `dd1eb6c41196c46458d0fc259a1d8fb1bd091ece29ba94253888784f0c27736b` | `4efa2caf0ec0210db79cc71a63c24c82caa1bd247260e95c0a3b1cbfe7c616d9` |

The full report completed at `2026-10-23T22:57:36.276296Z`; the selected report
completed at `2026-10-23T22:55:00.712181Z`. Both use `validation-v3.json`, now
retained under `testing/validation/2026-10-21T22%3A48%3A33.277Z/`, outside
their frozen candidate directories.
Each report binds its own exact manifest, source provenance, staging inventory,
input fingerprints, pair coverage, scientific results and software fingerprints.
Neither report accepts the other snapshot. Both manifests retain
`testing_only: true`.

The full snapshot, report and run log remain in their temporary workspace,
with no archival obligation or publication intent. The P0006/P0045 snapshot,
staging inventory, report, run log and read-only acceptance plan remain under
`$MERMAID/publisher/geocsv/testing/`. Its frozen staging schema 2 explicitly contains
only P0006 and P0045. At that stage there were no publication receipts or
archive commits.

The read-only `publish_snapshot.py --plan` gate passed for each snapshot and
reported `gate passed; no publication performed`. These checks performed no
network transfer or Git recording. Acceptance must be rechecked against the
current source and code before a separately authorized upload.

## Acceptance after the local testing layout change

The local testing snapshots, staging inventories and validation directories were
explicitly moved into each base workspace's `testing/` collection. Every moved
file's SHA-256 was checked before and after the move. Frozen manifests, payloads,
source provenance, staging inventories and earlier reports are byte-identical.
The previous flat snapshot/staging/validation directories are absent. No source
or remote data changed, and no archive Git history was changed.

The updated creator selects this collection from `testing_only: true`, while
`--workspace` continues to name the base workspace. An identical creator retry
resolved the archived candidate under `geocsv/testing/snapshots/` without
changing its frozen files. Read-only archive preflight accepted the new
collection location and existing exact-byte Git attributes.

Publisher code fingerprints changed, so earlier reports remain historical
evidence rather than current acceptance. Fresh exhaustive reports use
`validation-v3-testing-layout.json`; both passed the current publication gate
through `--plan`. The source inventories, candidate bindings, staging hashes,
pair counts, scientific limits and measured maxima match the earlier reports.
Consumer source fingerprints are unchanged.

| Scope | Pairs passed | Completed UTC | Current report SHA-256 |
| --- | ---: | --- | --- |
| Full corpus | 43,365 | `2026-10-23T23:22:09.604518Z` | `489fac9069a5e88eee124c5c00ffbd09a959a776dabdd6457dacb6b894683166` |
| P0006/P0045 | 3,292 | `2026-10-23T23:20:12.586929Z` | `b55b28bfd6a040be486f3cd4baa658eae8d1cf38b01e17ed40534e548ed549e8` |

Both current reports have zero failed, missing, unsupported or unexamined pairs.
Their read-only gate outputs are retained as `acceptance-plan-testing-layout.json`
beside the reports. The full corpus remains in an ordinary temporary workspace;
only P0006/P0045 is in `$MERMAID/publisher/geocsv/testing/`. Production manifests
remain rejected. No data were uploaded, no pointer or receipt was written, and
no archive commit was created. Verification used the real-source
create/validate/gate workflow, Python syntax checks and documentation checks.
Subsequent focused verification passed all 55 publisher tests with the exact
consumer baseline, 11 Worker serving tests and 70 package fetch/tutorial tests.
The publisher tests exercise fixture-only local Git recording and recovery in
the new testing namespace; no live storage writes were performed.

## Initial hosted testing publication — 2026-10-26

The exact P0006/P0045 candidate was explicitly authorized for testing upload.
Its current gate passed before transfer and again before activation. The
publisher uploaded only the two GeoCSV payloads, manifest and accepted
`validation-v3-testing-layout.json` report (served as `validation.json`), then
verified exact SDK/HTTPS bytes and pinned public fetch before selecting testing
latest. The collection contains exactly those four immutable objects and its
one latest pointer. Production latest remains absent.

The public manifest is available at
[the pinned testing URL](https://bathymetrix.com/geocsv/testing/releases/2026-10-21T22%3A48%3A33.277Z/manifest.json).
GET/HEAD checks passed with testing labels and identity encoding. Repeated
immutable requests returned cache hits with the one-year immutable/no-transform
policy; latest and convenience redirects remained no-store. Missing objects,
missing instruments and double-encoded release paths returned uncached 404s.
Conditional create against the existing manifest and a stale-ETag latest write
both returned 412 using identical published bytes; bytes, ETags and modification
times were unchanged.

The unmodified consumer passed latest/pinned, one/all instruments, memory/disk,
explicit ordering, identical local-file reuse and download-provenance checks.
The downloaded payloads were then placed in a temporary validation workspace
with byte-identical local staging/provenance evidence. The existing schema-3
validator reran read, strict association, SAC export and independent reference
comparison for every selected original waveform pair. All 833 P0006 pairs and
2,459 P0045 pairs passed: 3,292 passed and zero failed, missing, unsupported or
unexamined. The new report passed the current acceptance gate. Original sources
remained clean and unchanged. The published acceptance report was not replaced.

The separate local archive has initial commit `f3eb04b` and scoped publication
commit `f5b81ea`. Its receipt is
`geocsv/testing/publications/20261026T140711.532138Z.json`. Detailed hosted HTTP,
SDK and scientific verification evidence is retained in the approved private
operational location, outside the software checkouts. Initial testing artifacts
remain retireable only through separately authorized cleanup. This publication
does not authorize production promotion, further uploads or DNS changes;
DNSSEC restoration was separately completed and verified later on 2026-10-26;
see the [restoration findings](infrastructure-verification.md#dnssec-restoration--2026-10-26).

## Local consumer-baseline revalidation — 2026-10-26

The frozen consumer is `mermaid-geocsv` 0.24.0 at
`33ed5ff477b6c44447d472fc8e828b5ae930e0db`, containing the completed private
reader-module rename. Current consumer HEAD
`5815832e9c5877e010a7295b2949cf4e45042795` has identical package source and
packaging configuration; its later changes affect hosting documentation only.
Both revisions passed all 55 publisher compatibility tests in their respective
CI modes. The publisher `.venv` was restored to the separate, noneditable frozen
installation before scientific validation. See the
[baseline review](consumer-baseline-review.md#completed-local-acceptance-refresh).

The original published acceptance report still records consumer `c1eb805`.
The current gate correctly rejected it for a new acceptance decision because
the package-code fingerprints differ. It remains unchanged historical evidence
for the completed publication, with SHA-256
`b55b28bfd6a040be486f3cd4baa658eae8d1cf38b01e17ed40534e548ed549e8`.

The existing candidate was not recreated or expanded. Its manifest remains
`dd1eb6c41196c46458d0fc259a1d8fb1bd091ece29ba94253888784f0c27736b` and its
scope remains exactly P0006/P0045 with `testing_only: true`. The original source
remained read-only at clean commit `ac10d037f824084693813d62851728a7691374d7`.
Publisher 0.1.0/report schema 3, Python 3.12.4, NumPy 2.5.3, pandas 3.0.6 and
ObsPy 1.5.1 were unchanged.

The validator exclusively created this new local report under
`$MERMAID/publisher/geocsv/testing/validation/2026-10-21T22%3A48%3A33.277Z/`:

`validation-v3-consumer-33ed5ff-20261026T182615Z.json`

- SHA-256: `225c2ad8a35405257629930fc7a54eb264ca7ff382a6738d2d115abcb35a9134`.
- Report size: 7,092,188 bytes.
- Run: `2026-10-26T18:27:34.753921Z` to `2026-10-26T18:27:46.458128Z`.

| Instrument | Original pairs | Passed |
| --- | ---: | ---: |
| P0006 | 833 | 833 |
| P0045 | 2,459 | 2,459 |
| Total | 3,292 | 3,292 |

The run fingerprinted 3,292 MiniSEED files, 3,292 independent SAC references
and two source GeoCSV files. Failed, missing, unsupported and unexamined counts
were all zero, with no reported failures. Pair results, measurements, maxima,
scientific limits, source inventory, staging and provenance bindings match the
original published report exactly. No full-corpus validation was rerun.

The current `publish_snapshot.py --plan` gate accepted the new report with the
explicit testing destination and returned `gate passed; no publication
performed`. All 14 pre-existing archive files were compared with their hashes
captured before this run and remained byte-identical. Only the new local report
was added to the archive working tree; no commit or publication receipt was
created. No storage credentials or private deployment configuration were needed.
Hosted payloads, manifest, immutable `validation.json` and pointers were not
changed. This local acceptance does not replace the original publication report
or authorize uploads, redeployment or DNS changes.
