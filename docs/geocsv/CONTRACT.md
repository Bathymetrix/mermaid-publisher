# GeoCSV publication and download agreement

This document is the canonical GeoCSV producer/consumer agreement. The fixed
historical scientific/download consumer baseline is mermaid-geocsv 0.24.0 at commit
`33ed5ff477b6c44447d472fc8e828b5ae930e0db`. Owning this document does not permit
silent producer/consumer changes: retain historical fixtures and review
protocol changes explicitly across repositories. The authorized
[2026-10-28 path review](RELEASE_PATH_REVIEW.md) requires consumer >= 0.26.0
for the replacement timestamped testing collection. The frozen baseline is
retained for historical downloads and scientific compatibility, not the new
path protocol.

The [2026-10-26 compatibility review](CONSUMER_BASELINE_REVIEW.md) adopts this
revision after an identical reader-module rename and import updates. The
original baseline fingerprints and historical download fixtures remain retained.
Existing archived reports describe their original software; future publication
requires fresh evidence matching the active installed consumer.

## Ownership

`mermaid-publisher` owns creation, archive validation, its report schema,
publication gate, transfer and local recording. `mermaid-geocsv` owns public
fetch/read/associate APIs and optional SAC station location projection.
The publisher owns export verification and uses ObsPy for current-consumer
writing; the frozen 0.24.0 consumer keeps its public exporter compatibility
path. Automaid owns scientific source generation. `bathymetrix-site` owns its read-only download
service, landing page and hosting runbook. Hosting can change independently.

Repository version, validation-report schema and download compatibility are
separate concerns. Report schema 3 is a local evidence revision independent of download-path
changes. Publisher 0.3.0 and consumer 0.26.0 implement the explicitly reviewed
hyphenated path protocol; manifest fields and scientific release IDs are unchanged.

Consumer 0.25.0 removes its public writer and adds `create_sac_header`. This
scientific API migration does not change the fixed fetch baseline, historical
fixtures, manifests, URLs or byte semantics. The publisher supports both
consumer paths; [SAC verification](SAC_VERIFICATION.md) records every retained
check. Evidence remains bound to the exact installed software.

## Current publication phase: testing only

All hosted data are testing only, including complete-corpus tests. Require
matching `testing_only: true` in manifest and latest. Current publisher commands
reject production activation and require explicit collection URLs ending in
`/testing/` and object prefixes ending in `/testing`. For Bathymetrix, the local
serving implementation uses `/geocsv/testing/` and keys `geocsv/testing/`.
Production `/geocsv/latest.json` and `geocsv/latest.json` remain separate.
The read-only Worker was deployed on 2026-10-23. The explicitly authorized
P0006/P0045 testing snapshot `2026-10-21T22:48:33.277Z` was published on
2026-10-26. On 2026-10-28 the same unchanged data/manifest were republished
under hyphenated paths and selected by testing latest, with fresh scientific
evidence. The four old testing objects and encoded URLs were retired. See the
[path review and replacement evidence](RELEASE_PATH_REVIEW.md). Production
remains inactive.
The public landing page identifies that scope, provides the MH network DOI
(10.7914/SN/MH), and states that initial workflow tests may be retired after
verification. Infrastructure deployment, landing-page publication and test
acceptance do not authorize further uploads, production publication or a first
release tag. Required licensing/citation decisions and explicit authorization
remain prerequisites for any further publication.

Initial workflow-testing snapshots are disposable qualification artifacts, not
permanent scientific releases. After workflow verification, an explicitly
authorized cleanup may retire their hosted objects and local archive evidence.
Indefinite availability is not promised for these initial testing URLs. Payloads
and manifests remain immutable until retirement; a retired testing identity must
never be reused for different bytes. Retirement intentionally ends pinned-link
availability, with cache cleanup considered separately. Production artifacts
retain their indefinite-retention policy. No cleanup is authorized by this rule.

## Relative collection paths

The same relative download agreement applies within a chosen collection:

```text
latest.json
latest/<instrument_id>.geocsv
releases/<release-component>/manifest.json
releases/<release-component>/<instrument_id>.geocsv
releases/<release-component>/validation.json
```

Convenience latest file paths return temporary 302 redirects. Fetch resolves
latest.json once and pins immutable paths. Testing and future production have
separate base URLs, object namespaces and activation pointers. Their relative
manifest paths retain the same format. Exact delivered bytes and conditional
immutable writes/latest activation are destination requirements.

## Literal release identity and hyphenated paths

Scientific `release_id` is the exact GeoCSV `#created` value, with grammar
`YYYY-MM-DDTHH:MM:SS[.digits]Z`, a valid calendar date, hours 00–23 and seconds
00–59. There must be exactly one declaration per file and exact spelling agreement
across the complete snapshot. Missing, repeated or mixed declarations raise.
Preserve all fractional digits; do not round or reformat the identity.

Compute `release_component = release_id.replace(":", "-")` only for the
validated creation-timestamp release ID. This is a path representation, not a
replacement timestamp format. Do not rewrite GeoCSV contents, `#created`,
JSON release IDs, provenance or any other dates/times:

| Context | Example |
| --- | --- |
| JSON and fetch argument | `2026-10-21T22:48:33.277Z` |
| URL, R2 key and new local snapshot/staging/validation/download directory | `2026-10-21T22-48-33.277Z` |

Worker lookup uses the plain path component directly as its storage-key
component. Literal colons and percent-encoded components are rejected before
cache lookup. No URL decoding or legacy aliases are required. Equivalent
instants with different fractional spellings remain distinct release IDs.
Token IDs remain supported unchanged for illustrative client/Worker tests only.
Historical local encoded directories remain readable for archive verification
and receipt recovery; new snapshots use hyphens, and creation checks both
layouts for same-identity byte conflicts. Existing local downloads are not moved.

## Exact manifest protocol

Testing-only latest-pointer format (relative to its isolated collection):

```json
{
  "release_id": "2026-10-21T22:48:33.277Z",
  "testing_only": true,
  "manifest": "releases/2026-10-21T22-48-33.277Z/manifest.json"
}
```

The relative manifest path must exactly match its hyphenated release component. Its
`testing_only` flag must match the manifest and remain true throughout the current
testing phase. No `release_component` JSON field is needed.

The immutable manifest requires `release_id`, boolean `testing_only`, and a
`files` array. Each entry requires:

| Field | Meaning |
| --- | --- |
| `instrument_id` | Unique nonempty ID, with exact spelling and case |
| `filename` | Unique filename, resolved relative to the manifest URL |
| `size_bytes` | Nonnegative integer count of complete uncompressed file bytes |
| `sha256` | Lowercase 64-hex SHA-256 of those exact bytes, including comments |
| `provenance` | Descriptive object; never interpreted as filesystem instructions |

Scientific filenames are `{instrument_id}.geocsv`. Publisher staging accepts IDs
starting with an ASCII letter/digit and otherwise containing only ASCII letters,
digits, `.`, `_`, `-`. Filenames have the same character rule; `manifest.json` is
reserved by the client. The creator uses a reviewed serial-to-ID mapping and
requires all Station values to agree; it does not infer an ID from a serial.

Instrument scope is frozen at creation. Without `--instruments`, every mapped
source instrument is in scope. With `--instruments ID ...`, only those explicit
IDs are in scope. The reviewed mapping must still account for every source
serial. Unknown or duplicate selected IDs raise. Validation covers every
original waveform pair for included instruments; publishing transfers the
complete frozen candidate and cannot filter or expand it. A different selection
requires a separate candidate and its own acceptance report.

Recordless GeoCSV sources are never staged or published. The local-only staging
inventory records all in-scope inputs and explicit recordless exclusions.
Validator and publisher recheck those exclusions and reject any original
waveforms in an in-scope recordless directory. Instruments outside an explicit
selection are not validation inputs and are not copied or fingerprinted.
The sidecar is not an R2 release object. The report binds its hash separately.
Staging schema 1 retains complete-source accounting for default creation.
Staging schema 2 adds a sorted, nonempty, unique `instrument_ids` array for
explicit selections; its instrument entries must cover exactly that selection,
including recordless exclusions. Both versions remain supported. The public
manifest/download format and validation-report schema 3 are unchanged.

The creator emits entries sorted by ID. Source provenance uses a
processed-root-relative `source_path` (`<serial>/geo_DET_REQ.csv`) and
`manual_edits: false`. Payloads are copied verbatim. Manifests are deterministic;
publication/report times must not cause same-ID manifest regeneration. Optional
descriptive fields are retained by clients, without becoming instructions.
`created_utc`, when supplied, is descriptive rather than a release ID.

## Fetch and immutable releases

An explicit literal release ID bypasses latest. Latest is read once per fetch
operation; manifest identity and test flags must agree. A missing release or
instrument raises without fallback. Files are discovered from the manifest,
not HTML scraping or guessed sequential IDs. Downloads are streamed and accepted
only after size/SHA-256 checks. Pin/cache directories by hyphenated release component, and
retain the exact manifest and literal release provenance.

Under an existing release ID, payloads and manifests are immutable. Identical
retries reuse them; differing bytes (including comments) or inventories raise.
Unchanged historical records with updated comments and a new shared timestamp
are valid. Retain prior releases. Published snapshots, inventories, reports and
publication receipts live in the separate local Git archive
`$MERMAID/publisher/geocsv/testing`, outside the protected processed tree and
software checkout. Creation and validation alone may use ordinary temporary
workspaces without Git or archival obligations. Validation does not imply publication
intent. Original waveform archives are not copied.

Latest responses and redirects bypass caches. Successful immutable objects are
cached deliberately; misses/errors are not. Downloads honor
`Accept-Encoding: identity` with exact bytes and no transformation. Compression
is outside this protocol; coordinate any change before implementation.

## Scientific publication gate

Freeze the candidate, obtain its exhaustive scientific acceptance report,
recheck the complete manifest/inventory/hashes, upload payloads before the
manifest, verify public HTTPS bytes and explicitly pinned `geocsv.fetch`, then
update latest last. Failures before activation leave the previous latest selected.
An unconfirmed activation requires inspecting remote state before retrying. Serialize
publication and use conditional object writes to prevent conflicting updates.

The publisher owns `scripts/geocsv/validate_snapshot.py`, the version 3 report
format and `scripts/geocsv/gate_snapshot.py`. Validation covers every original
MiniSEED and independently read paired SAC for included instruments; `.mhpsd`
spectra are outside scope and are not counted. Missing pairs, unsupported
waveforms and unexamined comparisons block acceptance.

Reports bind the exact frozen manifest and staged file inventory, full source
waveform fingerprints and pair accounting, scientific checks/limits/results,
failures/maxima, and package/code/dependency versions. Acceptance rechecks inputs
and complete coverage rather than trusting a success flag. See
[the concrete report protocol](VALIDATION.md). Scientific
acceptance requires a passing complete run over each candidate's frozen
instrument scope. A full-corpus report cannot accept a different selected
candidate. The historical
2026-10-22 version-2 run passed all 43,365 original waveform pairs and its report
passed the publisher's acceptance gate; see
[archive findings](ARCHIVE_FINDINGS.md).

An accepted report may be stored as `validation.json` outside the manifest's
GeoCSV files list. It binds the manifest; the manifest never depends on its hash.
Public report provenance is source-relative. Data license and citation remain
owner decisions before publication. No DNS activation, production publication,
software commit, or release is authorized by this document. An authorized
successful publication includes its scoped local archive commit.

## Local provenance and recording

For `testing_only: true`, the base workspace contains a `testing/` collection
with `snapshots/`, `staging/`, `validation/` and `publications/` subdirectories.
The creator selects this namespace from the manifest flag; callers continue to
supply the base workspace. Testing snapshots in the former flat layout must be
explicitly relocated with their evidence. Candidate inspection rejects testing
manifests outside `testing/snapshots/`. Publication recording and network-free
receipt recovery use the same collection. No remote paths or schemas change.

Each snapshot also retains local `source_provenance.json`: schema_version 1 and
`git: null` for ordinary sources, or a Git object with the full commit hash and
source_subdirectory relative to its working-tree root. A Git source must be
clean before/after staging and at validation/gating. Ignore status does not
replace input fingerprints. The report binds this file's SHA-256. It is not a
GeoCSV manifest entry and is not uploaded. No credentials, remote URLs or
machine-specific source roots are recorded.

A successful remote publication creates an immutable local receipt and a
scoped archive Git commit. Receipts and inventories are not public release
objects. Publication success and local recording failure are separate outcomes;
`--record-only` finishes recording without network writes. No automatic pushes
are performed. See [the workflow](WORKFLOW.md).
