# Changelog

## 0.4.1 — unreleased

- Require the exact schema 1.0.0 declaration and six-digit UTC `#created`
  during creation and candidate inspection, including recordless sources.
- Reject duplicate schema declarations and comments after the column header;
  preserve quoted multiline fields and exact source bytes.
- Keep report schema 4, scientific limits and manifest/download semantics unchanged.

## 0.4.0 — unreleased

- Require the migrated consumer >= 0.27.0 for schema 1.0.0 scientific validation.
- Select Recording rows and Time, and verify explicit source Elevation.
- Introduce report revision 4 with `recording_records`; retain scientific limits.
- Remove active historical-consumer, encoded-candidate and receipt aliases.
- Retain immutable historical fixtures, baseline fingerprints and reports.

## 0.1.0 — unreleased

- Migrate the GeoCSV workflow from bathymetrix-site commit 698bc38.
- Rename snapshot helpers to inspect_snapshot and acceptance rules to gate_snapshot.
- Require testing-only manifests and isolated explicit destinations.
- Archive clean-source Git provenance while supporting ordinary source directories.
- Introduce report schema 3 with source-provenance binding and publisher identity;
  retain schema identifiers and unchanged scientific comparison rules.
- Record successful publications in a dedicated local Git archive, with scoped
  commits and network-free receipt recovery. Never push automatically.
- Freeze the 0.24.0 consumer baseline at commit c1eb805e420f7f8d4bfb8c6f737316c9f5766534.
