> **AI-written documentation — non-authoritative.** Verify findings against the frozen manifest, validation report and publication receipt.

# GeoCSV testing publication — 2026-11-03

The explicitly authorized P0006/P0045 snapshot from the automaid v4.9.2 rebuild
was published and selected by testing latest at `2026-11-03T23:49:18.833351Z`.
Its literal release identity is `2026-11-03T22:29:17.981000Z`. Payload schema is
1.0.0, validation report schema is 5, publisher version is 0.7.0 and the consumer
is 0.28.0. All objects remain testing only; production latest remains absent.

- [Release directory](https://bathymetrix.com/geocsv/testing/releases/2026-11-03T22-29-17.981000Z/)
- [Manifest](https://bathymetrix.com/geocsv/testing/releases/2026-11-03T22-29-17.981000Z/manifest.json)
- [Download bundle](https://bathymetrix.com/geocsv/testing/releases/2026-11-03T22-29-17.981000Z/MERMAID.geocsv.tar.gz)
- [Scientific validation](https://bathymetrix.com/geocsv/testing/releases/2026-11-03T22-29-17.981000Z/validation.json)
- [Comparison evidence](https://bathymetrix.com/geocsv/testing/releases/2026-11-03T22-29-17.981000Z/comparison.json)

## Source and scientific acceptance

The canonical read-only source was clean at full commit
`bd992f61eb524771c57df236f5034a11c704eef8` (`automaid v4.9.2`). Creation froze
a new candidate; the abandoned v4.9.1 candidate was retained unchanged.

| Instrument | GeoCSV rows | Recording rows | Original waveform pairs passed |
| --- | ---: | ---: | ---: |
| P0006 | 20,345 | 828 | 833 |
| P0045 | 124,016 | 2,455 | 2,455 |
| Total | 144,361 | 3,283 | 3,288 |

Every selected original MiniSEED/SAC pair passed. Failed, missing, unsupported
and unexamined pair counts were zero. GPS measurements bracketed every normal
row. Both source `outside_filterDate_gps.geocsv` files were recordless. Fresh
validation was generated after the producer-revision metadata policy changed
the workflow fingerprints; earlier reports were preserved unchanged.

The report binds exact installed source fingerprints as well as package
versions: Python 3.12.4, mermaid-geocsv 0.28.0, NumPy 2.5.3, pandas 3.0.6 and
ObsPy 1.5.1. Scientific tolerances were unchanged.

## Reviewed predecessor changes

The predecessor was `2026-10-30T18:08:32.316000Z`; its public manifest and
payload hashes were verified before comparison. All measurement rows in both
instruments match that snapshot byte-for-byte and in the same order. This
restores the 6 GPS and 57 pressure rows lost by the abandoned P0006 generation,
and the 8 GPS and 2,752 pressure rows lost by the abandoned P0045 generation.

The exact diffs include 1,612 P0006 and 3,451 P0045 automaid revision-only row
updates. These changes alone require no metadata override. Six actual P0045
deletions were explicitly approved: four Recording rows and two crossings from
the excluded IcCycle. No other fields changed in retained rows after accounting
for the producer revision. `comparison.json` binds this predecessor and the
selected `allow_metadata_changes: true`, `allow_schema_change: false` policy.

## Transfer and public verification

The Worker update for bundle, mapping/diff, comparison and release-directory
serving was separately authorized and deployed before publication. Its 22
tests and deployment dry run passed; the publisher suite passed 114 tests.

The publisher uploaded the two payloads, bundle, manifest, accepted validation
and auxiliary reports; verified SDK/public HTTPS bytes and a pinned fetch;
rechecked acceptance; then conditionally activated testing latest last.
It wrote the receipt and completed the scoped local archive commit.

Independent postpublication checks passed latest and pinned consumer fetches,
exact manifest/validation/auxiliary-report receipt hashes, exact bundle bytes
and member hashes, directory GET/HEAD and links, testing labels, identity
encoding and cache policy. Both payloads parsed with the row counts above.
The previous public manifest retained its exact bytes. Production latest
returned 404. No prior snapshot or local testing artifact was retired.

## Persistent archive evidence

Paths below are relative to `$MERMAID/publisher/geocsv/testing/`.

| Artifact | Path or value |
| --- | --- |
| Candidate | `snapshots/2026-11-03T22-29-17.981000Z/` |
| Accepted report | `validation/2026-11-03T22-29-17.981000Z/validation-v5-revision-policy-20261103.json` |
| Auxiliary reports | `reports/2026-11-03T22-29-17.981000Z/` |
| Bundle | `bundles/2026-11-03T22-29-17.981000Z/MERMAID.geocsv.tar.gz` |
| Receipt | `publications/20261103T234918.833351Z.json` |
| Scoped local archive commit | `1958edd9f20607544658876c132bf73071b14737` |
| Manifest SHA-256 | `16daa04ed8acc364aabaf7759841bc32a7f50c4dcd75990d183c0e481c6b8e66` |
| Report SHA-256 | `15fdea7fa5cc080ff54cda841469caf8017f01ea97a65517535cee15ba73da2d` |
| Source provenance SHA-256 | `25d814d8c75502656c89cc081432074a68935b64fbb8173425c001edc9c69538` |
| Staging inventory SHA-256 | `c4c556117e3cf9969caaf779115f43630aefb20bc5bcd3350ea892b6d179fc6c` |
| Bundle SHA-256 | `77b5f6af4353aec5418c73a730393b30325c7e4e47cba38e2eba99c682f145a3` |

The archive commit contains exactly this publication's 15 artifacts. It excludes
the abandoned candidate, preliminary reports, local review summaries and
unrelated untracked files. Original waveform archives were not copied. No
software repository was committed, no Git repository was pushed, and no tag
was created by this publication workflow. Cite MH network DOI `10.7914/SN/MH`.
