# mermaid-publisher

Read and follow `~/.codex/AGENTS.md`, `~/programs/AGENTS.md`, and
`$MERMAID/AGENTS.md` before working in this repository. These instructions
supplement the guidance in those files.

This repository owns maintainer publication workflows. GeoCSV is the only
implemented data type. Keep its code, tests and documentation under their
`geocsv/` directories. Add shared infrastructure only after another implemented
workflow demonstrates the need.

Use public `mermaid-geocsv` APIs. Scientific API behavior and package defects
belong in that package. Publication-specific comparisons and the versioned
archive report belong here. Consult current package scientific contracts and
tests before changing comparisons; do not widen tolerances to pass a corpus.

`docs/geocsv/CONTRACT.md` is the canonical producer/consumer agreement. A
publisher change does not implicitly change fetch behavior. Retain fixed
historical download fixtures and the exact supported consumer baseline. Updating
either requires an explicit compatibility review. Repository version authority
is `VERSION`; report schema versions are independent. No release tags or remote
publication are implied by a version change.

There are three commands: create, validate and publish. `inspect_snapshot.py`
and `gate_snapshot.py` are internal modules. Preserve scientific comparison
rules and exact-byte immutability. Keep manifest/download changes distinct from
local report and provenance changes.

All hosted data remain testing only. Require matching `testing_only: true`,
isolated testing URLs/object prefixes, scientific acceptance, licensing/citation
and explicit upload authorization. Production promotion is unauthorized.

The canonical source is `$MERMAID/processed`; never modify it. Ordinary source
directories are valid. Git sources require a clean entire worktree and a full
commit hash in immutable snapshot provenance. Recheck source state during
staging, validation and publication gating. Fingerprints remain authoritative
for ignored inputs. Never copy original waveform archives into the publication
archive; retain reports and fingerprints instead.

The external archive is `$MERMAID/publisher`, a separate local Git repository;
GeoCSV uses its `geocsv/` subdirectory. Retain production payloads, manifests,
inventories, reports and receipts indefinitely. Initial workflow-testing
snapshots are disposable and may be retired after verification through an
explicitly authorized cleanup. Keep their bytes immutable until retirement;
never reuse a retired testing identity for different bytes. Cleanup of hosted
objects, caches, local artifacts or Git history is not automatically authorized.
Credentials and private operational configuration stay outside both checkouts.
Resolve credentials through the SDK provider; do not inspect or print them.

A user-authorized successful publication includes a scoped local archive commit.
Commit only that publication's artifacts and preserve unrelated staged work.
Never push automatically. Remote publication and local recording are separate
outcomes; preserve a receipt for network-free recording recovery. Do not commit
this software repository unless explicitly asked.

Use this repository's `.venv` when present. Run the focused unittest suite and
consumer compatibility checks. Tests must not access real sources, upload data,
or modify non-fixture Git history. Update relevant docs with behavior changes.

After completing and verifying a coherent repository change, suggest a Git
commit message in the final handoff using `<subsystem>: <imperative summary>`.
Do not commit unless explicitly asked.
