> **AI-written documentation — non-authoritative.** Verify findings against the frozen manifest, source fingerprints and validation report before reuse.

# Regenerated schema 1.0.0 corpus validation — 2026-10-30

The regenerated canonical `$MERMAID/processed` corpus passed fresh exhaustive
local validation and the independent acceptance gate with publisher 0.4.0,
consumer 0.27.0 and report schema 4. This is testing-only evidence. No upload,
real publication-archive commit, pointer change, deployment or release occurred.
Existing hosted payloads remain old-format and incompatible with the new-only
reader. Production remains inactive. Earlier reports were not reused.

## Frozen inputs and identity

The canonical source was clean at Git commit
`6a11918d2f740f083f5b922e5da507ba36934a18` (source subdirectory `.`).
Automaid source was v4.6.2 at `4332daf5d3eb0f86e7828b5765ba6c80ebdd15a7`.
All 112 histories declare payload schema 1.0.0 and the same literal creation
identity, `2026-10-30T18:08:32.316000Z`. The path component is
`2026-10-30T18-08-32.316000Z`; no source timestamp or payload byte was rewritten.

| Accounting | Fresh result |
| --- | ---: |
| Source GeoCSV histories | 112 |
| Populated payloads frozen in candidate | 103 |
| Recordless histories explicitly excluded | 9 |
| GeoCSV data rows | 4,100,941 |
| Recording rows | 43,348 |
| Original MiniSEED files | 43,365 |
| Independently read paired SAC files | 43,365 |
| Pairs passing every scientific check | 43,365 |
| Failed / missing / unsupported / unexamined pairs | 0 / 0 / 0 / 0 |

Counts were obtained from the regenerated source, not copied from historical
acceptance. The examined scope includes 78 pairs under IcCycle directories. Every derivation/crossing source label is `automaid-v4.6.2`.
Six existing clash reports remain beside the canonical outputs; no deduplication
or sampling-frequency policy changed. Recording-row and waveform-file counts
need not agree: repeated original traces can associate independently with one row.
The nine recordless IDs are R0060, S0081, S0082, S0085, S0086, S0087, S0090,
S0092 and S0094. Their exclusions and hashes are retained in the staging
inventory; original waveform files in an excluded directory would block acceptance.

The prior reviewed serial-to-ID mapping was reused for the 103 populated
histories, with the nine explicit recordless identities from historical
[archive findings](archive-findings.md). The creator verified every populated
Station cell against this mapping; no identity was inferred from a serial.

## Scientific checks and environments

The validator used strict public read/associate APIs, fresh SAC station headers,
ObsPy scratch exports and independently read SAC references. All original pairs
in the complete frozen instrument scope were examined. Scientific comparisons
and limits in [validation.md](validation.md) were unchanged.

Maximum source/native start difference was 1 microsecond; exported/native starts
agreed exactly; exported/reference starts differed by at most 1,000 ns.
Maximum rate difference was 3.4332129956737845e-6 Hz. Independent-reference
intervals differed by at most one float32 ULP, while native float32 intervals
were preserved exactly. Sample/count, depth and elevation errors were zero;
coordinates satisfied the existing per-pair limits.

Validation used publisher Python 3.12.4, consumer 0.27.0, ObsPy 1.5.1,
pandas 3.0.6 and NumPy 2.5.3. Installed consumer Python files matched the
consumer source checkout. The report binds exact publisher/package code hashes
and dependencies. Source fingerprints and clean Git provenance were rechecked
at completion and by the acceptance gate.

Automaid remains a checkout executed with conda `pymaid3.10` (Python 3.10.15,
ObsPy 1.4.1); it was not run for this task. Its source version authority reports
v4.6.2. Local egg-info reporting 4.5.3 is stale metadata, not an isolated conda
installation. No environment was installed or modified. The separate rounding,
read-back behavior and remaining byte-order/record-length limitations are in
[the clock matrix](../../../automaid/docs/clock-timing-matrix.md).

Fresh verification also passed 411 consumer tests (9 warnings), 76 publisher
tests and 13 Worker tests (Node 24.22.1). Initial sandbox runs could not bind
localhost; reruns with localhost access passed. Publisher test publication
messages concern disposable mocked fixtures only.

## Local fetch and association

A temporary localhost HTTP server served the exact frozen candidate. Latest
and pinned all-instrument disk fetches each verified all 103 payloads against
the manifest. Four single-instrument combinations covered latest/pinned and
memory/disk; four disk-reuse checks requested no payload again. Literal release
identity, exact manifest bytes, identity encoding and source-schema provenance
were retained. P0006 and P0045 fetched metadata each passed a native-waveform
association, scratch SAC export and independent-reference comparison.
These checks establish local HTTP behavior, not live HTTPS or deployed Worker
verification. No new bytes were hosted remotely.

## Evidence and reuse boundary

Evidence workspace: `/private/tmp/mermaid-regenerated-v462-oiyvfx_e/`.
Temporary evidence is local and must be retained if needed for later review;
its presence does not establish persistent publication archival.

| Artifact | Workspace-relative path |
| --- | --- |
| Frozen candidate | `candidate/testing/snapshots/2026-10-30T18-08-32.316000Z/` |
| Full scientific report and input fingerprints | `validation.json` |
| Acceptance result | `gate-summary.json` |
| Complete source/exclusion staging inventory | `candidate/testing/staging/2026-10-30T18-08-32.316000Z/inventory.json` |
| 112-history hashes, row counts and producer labels | `geocsv-audit.json` |
| Initial counts and mapping basis | `initial-inventory.json`, `inventory.csv` |
| Software/source identities | `software-baseline.json` |
| Local fetch evidence | `local-fetch-verification.json`, `verify-local-fetch.py` |
| Execution logs | `create.log`, `validation.log`, `local-fetch.log`, `consumer-tests-with-localhost.log`, `publisher-tests-with-localhost.log`, `worker-tests.log` |

Manifest SHA-256: `2984282101f9b339872a6c623a3321f4815637a7b9fe912589c3f006828b0ed8`.

Report SHA-256: `207ad69bcad1eb2a8385e9e393e540712e745df21f74d89157ac715664b5e66b`.

Staging inventory SHA-256: `e7396cf6a72b4aea49bbd4849a7a41628f4d4fc755edb2bf09da7fd48736ce00`.

Source provenance SHA-256: `850168c34fe23ed7cdf6ec5fcaddafeca2b5305dbfa481407410ebfdde2e4c3b`.

Acceptance applies only to this candidate, complete source inventory and exact
software evidence. Changed bytes or validation code require fresh acceptance.
Licensing, publication scope and explicit upload authorization remain separate
prerequisites; local acceptance grants none of them.
