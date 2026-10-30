> **AI-written documentation — non-authoritative.** Verify findings against the frozen manifest, validation report and publication receipt.

# Schema 1.0.0 testing publication — 2026-10-30

The explicitly authorized P0006/P0045 testing snapshot was created, freshly
validated with publisher 0.4.2 and consumer 0.27.0, published and selected by
testing latest on 2026-10-30. Payload schema is MERMAID GeoCSV 1.0.0; the
scientific report uses schema 4. Production latest remains absent. No Worker
deployment, software commit, remote Git push, release tag or deletion occurred.

Literal snapshot identity: `2026-10-30T18:08:32.316000Z`.

- [Pinned manifest](https://bathymetrix.com/geocsv/testing/releases/2026-10-30T18-08-32.316000Z/manifest.json)
- [P0006](https://bathymetrix.com/geocsv/testing/releases/2026-10-30T18-08-32.316000Z/P0006.geocsv)
- [P0045](https://bathymetrix.com/geocsv/testing/releases/2026-10-30T18-08-32.316000Z/P0045.geocsv)
- [Published scientific report](https://bathymetrix.com/geocsv/testing/releases/2026-10-30T18-08-32.316000Z/validation.json)

## Scientific acceptance

The read-only canonical source was clean at full commit
`6a11918d2f740f083f5b922e5da507ba36934a18`. Creation reused identical frozen
bytes from the earlier local candidate. A new report was generated for the
current publisher; the earlier report was neither reused nor changed.

| Instrument | GeoCSV rows | Recording rows | Original waveform pairs passed |
| --- | ---: | ---: | ---: |
| P0006 | 20,345 | 828 | 833 |
| P0045 | 124,022 | 2,459 | 2,459 |
| Total | 144,367 | 3,287 | 3,292 |

Every original MiniSEED and independently read paired SAC in this selected
scope was examined. Failed, missing, unsupported and unexamined pair counts
were all zero. Repeated original traces can associate with one Recording row;
row and pair counts need not agree. Scientific comparisons and limits were
unchanged. The separate full-corpus report does not accept this selected manifest.

## Transfer and independent verification

The current-evidence gate passed before publication and again before latest
activation. The publisher uploaded two payloads, the manifest and the accepted
report, verified exact SDK/public HTTPS bytes and pinned public fetch, and
conditionally selected testing latest last. The scoped local archive commit
completed after activation.

Independent public checks passed latest/all memory fetch, pinned/all disk
fetch, identical disk reuse without file rewrites, explicit selection order,
single-instrument latest/disk and pinned/memory fetch, exact payload/manifest
bytes and literal-release provenance. Both downloaded histories parsed as
schema 1.0.0. One original waveform per instrument passed strict association,
scratch SAC export and independent-reference scientific comparisons using
the downloaded metadata.

Public HEAD responses carried testing labels and identity encoding. Latest
was no-store; immutable payloads and manifest retained immutable/no-transform
caching. Production latest returned 404. The previous hyphenated testing
manifest remained available with its original SHA-256; no historical objects
or local artifacts were retired.

## Persistent archive evidence

All paths below are relative to `$MERMAID/publisher/geocsv/testing/`.

| Artifact | Path or value |
| --- | --- |
| Candidate | `snapshots/2026-10-30T18-08-32.316000Z/` |
| Accepted report | `validation/2026-10-30T18-08-32.316000Z/validation-v4-publisher042-20261030.json` |
| Receipt | `publications/20261030T231603.251374Z.json` |
| Scoped local archive commit | `b2f7040b8249a1b1b0f138b60a86fd7533eb9e4e` |
| Manifest SHA-256 | `9c938e29eb5045b518b2ed60a5454aadfecebfc828f43baf35c78e0aad87a627` |
| Report SHA-256 | `b3ebed4d4fa10838ae88db240d621e4df6ea0ae6d56ab70cd36facc69c49057b` |
| Staging inventory SHA-256 | `f4a8a32b2401cc7c8df43c7f287c48e4f1abe1cbd194e97f35f5630723be3fbe` |

Original waveform archives were not copied. The pre-pause validation report
remains untracked and unchanged in the archive; it was excluded from the scoped
publication commit. Future publication requires its own authorization and
current scientific evidence. Production promotion remains unauthorized.
