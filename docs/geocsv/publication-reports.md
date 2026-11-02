# Publication evidence and snapshot changes

Publisher 0.6.0 requires consumer >= 0.28.0 and validation report schema 5.
Payload schema remains 1.0.0. Historical evidence is immutable; these changes
require a fresh candidate/report and do not authorize uploads or production.

## Recording coverage and names

Every Recording source_index must have at least one passing original
MiniSEED/SAC pair. There is no exception or waiver. One original MiniSEED must
match exactly one row; repeated originals may match the same row. Basenames
must be unique per instrument. Reports use mseed_filename and sac_filename;
source inventories keep filename basenames and source-relative directory values
separately to locate the exact files. No MiniSEED filename value includes a directory.

source_index is a zero-based data-row position, excluding comments and the
column header. source_line is its one-based physical starting line, as in a
text editor. A quoted multiline row has one index and may occupy several lines.
These are file-local positions, not stable identifiers across snapshots.

## Producer clash evidence

Automaid writes geocsv-clash.json beside geo_DET_REQ.csv on every generation,
including an empty clashes list when clean. Schema 1 contains schema_version,
geocsv_sha256 and clashes. Each clash has source_index, source_line,
variant_count, mseed_filenames (basenames), header_differences and
payload_bytes_identical. Header differences identify qualified field names
such as FORMAT.SAMPLING_RATE and INFO.TRUE_FS and exact source strings per
mseed_filename. Missing fields are represented by present=false without value.
Raw differences outside parsed fields use raw_header. Payload equality concerns
raw DATA bytes, not decoded waveform equivalence.

Creation freezes each supplied report as {instrument}.clash.json alongside the
candidate. Missing reports can be staged but fail validation. Reports bind the
exact GeoCSV SHA-256. Validation/gating compare source and frozen report hashes,
verify source index/line references and compare all listed filenames with the
independent waveform associations. Header differences and payload findings are
producer evidence: publisher never calls automaid, reads MER inputs, or judges
whether clashes are acceptable. Nonempty clash reports are permitted. The
validation report retains each producer report's full content and checksum;
local archive recording retains its exact bytes. Missing or stale evidence fails.

Scientific estimation and its validation belong to the automaid version in the
GeoCSV attribution header and scientific publication. Measurement rows supply
observations; derived times/locations are best estimates supplied in the hope
that they are useful. Researchers may reinterpolate measurements. Consumer SAC
station-depth projection remains WaterPressure/100 metres, with source mbar.

## Published reports

Each snapshot publication includes {instrument}.mapping.csv, {instrument}.diff,
and comparison.json alongside payloads, manifest.json and validation.json.
These auxiliary reports are outside manifest.files. The mapping CSV header is:

```csv
geocsv_line_number,mseed_filename(s)
```

Each Recording row has one mapping entry: its source_line followed by every
matching MiniSEED basename in sorted trailing columns. Use ordinary CSV quoting.

Diffs compare complete original CSV data rows (comments and the column header
excluded). Removed old rows begin -<source_index>, and added current rows begin
+<source_index>, followed by the complete original row, preserving quoting and
terminators. A changed row prints both sides. Interior insertions do not report
unchanged shifted rows. Quoted multiline fields remain multiline in the diff.
Initial publication has a null predecessor and reports all rows as additions.

Publication reads the current testing latest once, verifies its manifest and
payload hashes, and binds the comparison to that exact predecessor. Edits and
deletions fail by default; --allow-metadata-changes explicitly allows them.
A payload-schema mismatch writes 'simple diff cannot be made' and requires
--allow-schema-change. These options cannot waive scientific comparisons,
unique associations, Recording coverage or valid producer-report binding.
A failed comparison leaves the generated diff/mapping files available for
local review and blocks before uploads. comparison.json is frozen only after
the selected policy passes. First-publication additions need
neither override. The --plan command checks local evidence only, without storage
access; remote predecessor comparison occurs during actual authorized publication.

Reports freeze under testing/reports/{component}/. comparison.json records both
snapshot identities, manifest hashes, validation hash, report hashes and selected
overrides. An identical retry retains its original predecessor. Existing report
bytes cannot be overwritten. Public HTTPS verification covers every auxiliary
report before conditional latest activation. Receipts bind their checksums;
archive commit and network-free receipt recovery include them. Old receipts
without auxiliary reports retain their original recovery behavior.

The host serves these objects read-only and lists reports when present. Source
support is local until separately authorized deployment and publication. The
future Metadata Changes website page is outside this implementation scope.
