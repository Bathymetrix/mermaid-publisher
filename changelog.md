# Changelog

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
