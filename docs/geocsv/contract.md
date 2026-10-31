# GeoCSV publication and download agreement

This is the canonical snapshot, manifest and download contract. The consumer's
[MERMAID schema 1.0.0](../../../mermaid-geocsv/docs/format-spec.md) defines
payload semantics. Automaid writes scientific products; `mermaid-geocsv` owns
fetch/read/associate and optional SAC station headers; this publisher owns
snapshot creation, validation, gating, transfer and recording; the site owns
read-only hosting. See [workflow](workflow.md) and [SAC verification](sac-verification.md).

## Payload and software requirements

Require Python >= 3.11 and consumer >= 0.27.0. Creation and inspection require
the exact first-line schema declaration and literal six-digit UTC `#created`,
including recordless sources. Repeated schema declarations and comments after
the column header raise; quoted multiline continuations remain CSV data.
Full parsing and scientific association belong to the consumer. Validation
selects `Derivation:Recording:` rows and uses `Time`; it projects explicit
Recording Elevation and never supplies missing source defaults.

Package version, payload schema, report schema and literal snapshot identity
are independent. Reports use schema 4 and `recording_records`; they bind exact
inputs, validation code and dependencies. A report for another inventory or
software revision cannot accept this candidate.

## Testing-only boundary

Require `testing_only: true` in both manifest and latest, collection URLs ending
in `/testing/` and object prefixes ending in `/testing`. Production activation
is rejected by publisher commands. Testing and production pointers remain
separate. The approved hosted scope is P0006/P0045; broader distribution needs
licensing and scope decisions. See [hosting status](../../../bathymetrix-site/docs/geocsv-hosting.md)
and the [artifact evidence index](evidence.md).

Scientific acceptance, infrastructure availability and testing publication do
not authorize further uploads, retirement, production promotion or a formal
release. Explicit upload authorization and licensing/citation approval are
required. Cite the MH network DOI `10.7914/SN/MH`; the software license does not
establish a data license.

Initial testing snapshots can be retired only through separately authorized
cleanup. Keep their bytes immutable until retirement and never reuse an
identity for different bytes. Pinned testing URLs do not promise indefinite
availability. Production artifacts have indefinite retention. Cleanup of
objects, caches, local artifacts or Git history is not implicit.

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

## Literal release identity and paths

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
| JSON and fetch argument | `2026-10-30T18:08:32.316000Z` |
| URL, R2 key and new local snapshot/staging/validation/download directory | `2026-10-30T18-08-32.316000Z` |

Worker lookup uses the plain path component directly as its storage-key
component. Literal colons and percent-encoded components are rejected before
cache lookup. No URL decoding or legacy aliases are required. Equivalent
instants with different fractional spellings remain distinct release IDs.
Token IDs remain supported unchanged for illustrative client/Worker tests only.
Candidate directories use the hyphenated release component. Encoded-directory
aliases are unsupported; creation rejects an encoded directory for the same
identity. No operation automatically renames retained artifacts.

## Exact manifest protocol

Testing-only latest-pointer format (relative to its isolated collection):

```json
{
  "release_id": "2026-10-30T18:08:32.316000Z",
  "testing_only": true,
  "manifest": "releases/2026-10-30T18-08-32.316000Z/manifest.json"
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
Staging schema 1 records complete-source accounting for default creation.
Staging schema 2 records a sorted, nonempty, unique `instrument_ids` array for
explicit selections; its instrument entries must cover exactly that selection,
including recordless exclusions. Both versions remain supported. Validation
reports use schema 4.

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

The publisher owns `scripts/geocsv/validate_snapshot.py`, the version 4 report
format and `scripts/geocsv/gate_snapshot.py`. Validation covers every original
MiniSEED and independently read paired SAC for included instruments; `.mhpsd`
spectra are outside scope and are not counted. Missing pairs, unsupported
waveforms and unexamined comparisons block acceptance.

Reports bind the exact frozen manifest and staged file inventory, full source
waveform fingerprints and pair accounting, scientific checks/limits/results,
failures/maxima, and package/code/dependency versions. Acceptance rechecks inputs
and complete coverage rather than trusting a success flag. See
[the concrete report protocol](validation.md). Scientific
acceptance requires a passing complete run over each candidate's frozen
instrument scope. A full-corpus report cannot accept a different selected
candidate.
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
supply the base workspace. Candidate inspection rejects testing
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
are performed. See [the workflow](workflow.md).
