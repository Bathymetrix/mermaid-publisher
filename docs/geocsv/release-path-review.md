# Hyphenated release paths and testing replacement — 2026-10-28

Publisher 0.3.0, consumer 0.26.0 and the read-only hosting Worker adopt the same
release component: replace the two time-separator colons in the validated
creation-timestamp release ID with hyphens. For example:

| Context | Value |
| --- | --- |
| GeoCSV `#created`, JSON `release_id`, fetch argument and provenance | `2026-10-21T22:48:33.277Z` |
| URL component, R2 key and new local release directory | `2026-10-21T22-48-33.277Z` |

All fractional digits, scientific timestamps, instrument filenames, payload
bytes and manifest fields are preserved. There is no timestamp reformatting,
rounding, global colon replacement, change to scientific comparison limits,
or report-schema change. Report schema remains 3.

## Compatibility decision

The initial P0006/P0045 hosted testing collection is authorized for replacement,
including retirement of its old percent-encoded URLs and corresponding literal
timestamp storage keys. Testing availability was explicitly temporary; this
decision does not change production retention or authorize production activation.
No legacy serving aliases or download fallbacks are provided. The updated
Worker rejects encoded and literal-colon release paths before cache lookup,
including requests for previously cached test objects.

Consumer 0.25.x and frozen 0.24.0 require the old encoded manifest path and
cannot fetch the replacement timestamped collection. Consumer >= 0.26.0 is
required for new publication/download. Publication rejects older consumers
before object writes. The unchanged frozen source pin
`33ed5ff477b6c44447d472fc8e828b5ae930e0db`, its fingerprints and all historical
download fixtures remain retained for historical/scientific checks. This
explicitly revises their download-compatibility scope; the old client remains
incompatible with the new protocol. An exact new source pin can be adopted
only after the consumer changes are committed through a separately authorized
task. Local operations select the adjacent source through `PYTHONPATH`.

Existing local downloads are not moved. New fetch calls use hyphenated output
directories, retaining exact manifests and literal release provenance. Historical
archive directories remain readable for integrity checks and receipt recovery.
Creation checks both historical and current layouts for immutable identity
conflicts. Historical local reports, receipts and Git history are retained.

## Ownership and replacement sequence

- `mermaid-publisher` owns path creation, immutable transfer, current scientific
  evidence, latest activation and scoped local archive recording.
- `mermaid-geocsv` owns fetch URLs, pointer checks, output directories and
  unchanged scientific metadata/provenance.
- `bathymetrix-site` owns direct Worker key lookup, pointer/redirect paths,
  cache rejection and deployment.

The replacement uses the same unchanged P0006/P0045 data and manifest, with
fresh complete scientific validation under the updated software. Verify new
objects and pinned fetch before selecting testing latest. Confirm latest and
download behavior, then delete only the four retired testing release objects.
Production keys/pointers and canonical source files are outside this operation.
The successful replacement includes a publication receipt and scoped local
archive commit. Software repositories are not committed or pushed automatically.

Public destination and service identifiers are recorded in
[the operator workflow](workflow.md#recorded-public-testing-destination).
Credentials and private account-specific deployment configuration are excluded.

## Verification and deployment evidence

Completed on 2026-10-28:

- Consumer: 81 fetch, tutorial/parity/execution and public-API checks passed.
- Publisher: all 75 checks passed against the current consumer. The exact frozen
  historical source run passed 74 checks with one existing skip. A subsequent
  historical receipt-recovery check passed in the 18-test archive suite against
  both current and historical consumers.
- Host: all 13 Worker checks passed, including old cached URL rejection and
  obsolete-pointer rejection. The deployed Worker version is
  `5c856ea5-34f0-43de-a414-f8faddc6a866`.
- Fresh scientific acceptance passed all 3,292 pairs: P0006 833; P0045 2,459.
  Failed, missing, unsupported and unexamined pairs: zero.
- Live SDK/HTTPS checks verified the exact unchanged data and manifest, all four
  new immutable objects, GET/HEAD bytes, identity encoding, testing labels,
  no-store latest and convenience redirects. Latest/pinned, one/all instruments,
  memory/disk/reuse, parsing and literal release provenance passed.
- Exactly four old testing release objects were deleted after verification.
  All corresponding encoded URLs return uncached 404, including through the
  updated Worker's pre-cache path rejection. Production latest remains absent;
  canonical source inputs, local historical artifacts and Git history remain
  unchanged.

Current [testing manifest](https://bathymetrix.com/geocsv/testing/releases/2026-10-21T22-48-33.277Z/manifest.json).

| Evidence | Value |
| --- | --- |
| Manifest SHA-256 (unchanged) | `dd1eb6c41196c46458d0fc259a1d8fb1bd091ece29ba94253888784f0c27736b` |
| Fresh report | `geocsv/testing/validation/2026-10-21T22-48-33.277Z/validation-v3-hyphenated-paths-20261028.json` |
| Report SHA-256 | `e5f76c3973898221662cf97363963209986e97eaf5080a6e9bcae23db1393f7e` |
| Publication receipt | `geocsv/testing/publications/20261028T222326.290227Z.json` |
| Scoped local archive commit | `2b0f134` |

The report records imported consumer 0.26.0 and exact source hashes separately
from installed distribution metadata 0.25.1. The adjacent source was selected
with `PYTHONPATH`; neither virtual environment was modified. Exact frozen
baseline source was extracted to temporary storage for verification without
changing the pin or fixtures.

Worker/data replacement is deployed. The coordinated source changes are
recorded in these commits:

- `mermaid-publisher`: `4ed7086972260a837f6635b50bf334fa4bce23c9`.
- `mermaid-geocsv`: `6f899ff898ec0aef3ee9e9d88986f83594ba9153`.
- `bathymetrix-site`: `8012fdcbaae0226b38a57814fe49a2d61daa0a0c`.

These commits do not establish published packages or deployment of the updated
landing-page wording. Source version bumps do not authorize tags, production
publication or additional uploads.
