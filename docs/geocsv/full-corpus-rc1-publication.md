> **AI-written documentation — non-authoritative.** Verify against the frozen manifest, scientific report and publication receipt.

# Full-corpus rc1 testing snapshot

The canonical automaid v4.10.0 corpus uses payload schema `1.0.0-rc1` and
literal creation identity `2026-11-05T23:41:47.235000Z`. This is a full-corpus
release-candidate test, not a production data or software release. Final
schema 1.0.0 is reserved for paper publication.

## Inputs and scientific acceptance

The source was read directly from `$MERMAID/processed`, clean at full Git commit
`a387bbb3b4436cb9b36a6fb4eccff74b64d0d4de` (`automaid v4.10.0`). No alternate
source copy or non-Git bypass was used. Original waveform archives remain outside
the publication archive and were not regenerated or modified.

| Accounting | Count |
| --- | ---: |
| Source instruments accounted for | 112 |
| Published-candidate instruments | 103 |
| Explicit recordless exclusions | 9 |
| GeoCSV data rows | 4,104,855 |
| Recording rows with waveform coverage | 43,316 |
| Original miniSEED/SAC pairs passed | 43,333 |
| Failed, missing, unsupported or unexamined pairs | 0 |

Recordless instruments: R0060, S0081, S0082, S0085, S0086, S0087, S0090,
S0092 and S0094. Their source headers and exclusions were checked. Validation
excludes Init/IcCycle waveform namespaces under the existing scope. It checks
every other original pair for all included instruments, complete Recording
coverage, GPS bracketing and byte-bound producer clash reports. Scientific
rules and tolerances are unchanged. Source files were fingerprinted before and
after validation, and source Git revision and cleanliness were rechecked.

Publisher 0.8.0 and consumer 0.29.0 produced report schema 5. Validation ran
from `2026-11-06T02:27:51.092244Z` to `2026-11-06T02:33:10.787885Z`.
The largest association start offset was 1 microsecond; sample/count, depth
and elevation comparison errors were zero. All measured limits passed.
Older reports remain unchanged and do not accept these regenerated inputs.

P0006 and P0045 retain all 20,345 and 124,016 predecessor rows respectively,
exactly and in order after excluding only automaid revision labels. The
header/schema change needs explicit `--allow-schema-change`; no scientific
metadata-change override is needed. The other 101 payloads expand the testing
inventory. Data citation remains MH network DOI `10.7914/SN/MH`; testing
approval does not establish production scope or a general data license.

## Fresh verification

- Consumer suite: 425 passed, including 27 tutorial execution/parity checks
- Publisher suite: 115 passed
- Read-only Worker suite: 23 passed using an existing standalone Node 24.22.2 runtime
- Live pinned EarthScope tutorial: all three DET downloads, full-history
  association and independent miniSEED/SAC comparisons passed
- Markdown/notebook companions have identical prose and Python source;
  notebook outputs are empty and execution counts unset

No dependency, public API, scientific rule, tolerance or hosting configuration
changed. Automaid edits are restricted to GeoCSV documentation; unrelated
producer documentation and algorithms are untouched. Environments were unchanged.

## Publication status

The snapshot was published and selected by testing latest at
`2026-11-06T02:56:09.852640Z`. All 313 immutable objects passed publisher SDK
and public HTTPS byte checks; pinned fetch returned all 103 instruments. The
scientific gate was rechecked before conditional latest activation. The scoped
archive commit completed and preserved unrelated archive work. Production
remains inactive. No predecessor snapshot was retired.

Independent postpublication checks passed:

- Latest and pinned fetch, all 103 instruments, memory/disk access and identical
  disk-file reuse; the fetch tutorial ran unchanged against the public service
- All 4,104,855 data rows parsed; every downloaded payload matched its local
  manifested bytes and retained schema `1.0.0-rc1`
- Exact public manifest, accepted report, bundle and all 207 auxiliary reports;
  every bundle member matched its instrument manifest hash
- Testing flags, uncached latest and GET/HEAD redirects, immutable/no-transform
  objects, unencoded gzip bytes and release-directory GET/HEAD
- Production latest returned 404; the predecessor manifest stayed byte-identical
- The pinned EarthScope tutorial ran unchanged against the full P0006 history;
  all three live waveform/SAC comparisons passed

The bound client-verification record is retained locally with this snapshot.
No Worker or static-site deployment, push, tag, software release or retirement
occurred. The four software repositories' documentation changes are local commits;
updated static landing-page text is not yet deployed.

- [Release directory](https://bathymetrix.com/geocsv/testing/releases/2026-11-05T23-41-47.235000Z/)
- [Manifest](https://bathymetrix.com/geocsv/testing/releases/2026-11-05T23-41-47.235000Z/manifest.json)
- [Scientific validation](https://bathymetrix.com/geocsv/testing/releases/2026-11-05T23-41-47.235000Z/validation.json)
- [Bundle](https://bathymetrix.com/geocsv/testing/releases/2026-11-05T23-41-47.235000Z/MERMAID.geocsv.tar.gz)
- [Comparison](https://bathymetrix.com/geocsv/testing/releases/2026-11-05T23-41-47.235000Z/comparison.json)

## Bound local artifacts

Paths are relative to `$MERMAID/publisher/geocsv/testing/`.

| Artifact | Path or SHA-256 |
| --- | --- |
| Candidate | `snapshots/2026-11-05T23-41-47.235000Z/` |
| Accepted report | `validation/2026-11-05T23-41-47.235000Z/validation-full-rc1.json` |
| Staging inventory | `staging/2026-11-05T23-41-47.235000Z/inventory.json` |
| Manifest SHA-256 | `7d75dbc537bfc39769b7feff496ca7f2d1834f67ff5b9e42502095161c9d5e16` |
| Report SHA-256 | `e310db4253c336233f95ebf8fd023b1091afc53ef16ac73d9cb5d74640367074` |
| Source provenance SHA-256 | `4ea3f7d26933209da7ddb20aaa57bf4ba93e90162d0ac35b54c7ea0b8141975f` |
| Inventory SHA-256 | `1cb8cda9e6b7502d1beb044c18a82a6acc468c7e25179ebaf778595055508ad4` |
| Independent client verification | `validation/2026-11-05T23-41-47.235000Z/client-verification-20261106.json` |
| Receipt | `publications/20261106T025609.852640Z.json` |
| Client verification SHA-256 | `faf7ac70731b91e9a855089bc7ecc062919bb6f7d3f701b39b80f5797dbd4e27` |
| Client evidence commit | `429e788bbf9276aabbafe88df3ddb20bacd902d8` |
| Scoped archive commit | `2a9a906eec3326bab7669a62ec3cf6a3cb2f95f6` |
| Auxiliary reports | `reports/2026-11-05T23-41-47.235000Z/` |
| Bundle | `bundles/2026-11-05T23-41-47.235000Z/MERMAID.geocsv.tar.gz` |
| Comparison SHA-256 | `2bab6e58a96f33ce59139e1953632f3af31932f979fd91fe9465c7955e33ffb3` |
| Bundle SHA-256 | `8dba20dd5b3b34c1cea5c8e6e2723bbc6344bb96e72fbe4a1d982e56fac01627` |

The persistent archive retains exact manifested GeoCSV, source provenance,
producer clash reports, staging exclusions and the exhaustive report. Reports,
receipts and source mappings are artifact-bound evidence and remain immutable.
