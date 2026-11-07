# Publisher release audit — 2026-11-06

The published full corpus passes the existing acceptance rules. This audit
identifies **two high-priority release conditions and two moderate fixes** in
those rules. It found no demonstrated corruption of the published payloads in
the checks described below. The [consumer checklist](../../../mermaid-geocsv/docs/audit/release-audit-2026-11-06.md)
records the same findings and their effects on fetch, read and initial association.

Publisher 0.8.0, consumer 0.29.0, schema `1.0.0-rc1` and `testing_only: true`
describe the inspected baseline. Their prerelease/testing status is **not a
blocker in this audit**. Production enablement, licensing and authorization
remain separate decisions in the [production checklist](pre-release-checklist.md).
This document changes no contract or acceptance result by itself.

## Checklist, highest severity first

P1 means resolve the workflow policy or validation gap before scientific
release sign-off. P2 means a bounded evidence defect to fix before claiming
the affected evidence is fully checked. RA-05 is an accepted limitation of an
external input, not a blocker for original-waveform association.

| ID | Severity | Status | Publisher responsibility | Consumer linkage |
| --- | --- | --- | --- | --- |
| RA-01 | P1 | Open | Keep schema approval separate from scientific row-change approval | Preserve changed source values; acknowledge comparison coverage |
| RA-02 | P1 | Open | Check serialized clock-correction provenance independently of loaded start time | Preserve correction metadata and never apply it again |
| RA-03 | P2 | Open | Validate the documented shape of producer clash evidence | Retain many-originals-to-one-row association |
| RA-04 | P2 | Open | Reject out-of-limit rate diagnostics at the acceptance gate | Retain existing rate-matching semantics |
| RA-05 | P2 | Accepted limitation | Keep original-corpus acceptance distinct from external waveform responses | Reject the demonstrated unmatched/ambiguous response |

### RA-01: schema approval can hide scientific row changes

**Observed policy gap; the implementation follows the current contract.**
[`data_diff`](../../scripts/geocsv/_reports.py) returns immediately on a schema
mismatch, with `metadata_changed=False`. Consequently, `--allow-schema-change`
can approve a candidate without `--allow-metadata-changes`, even when scientific
rows also changed. Neither the placeholder diff nor the comparison flag says
what those changes were. GPS bracketing checks timestamps, not measured positions.

**Numerical example.** A temporary copy of current P0006 changes schema
`1.0.0-rc1` to supported `1.0.0-rc2` and changes the first Position latitude
from **−14.453383° to −13.453383°**, approximately **111 km**. `data_diff`
returns `(placeholder, True, False)`. Both revisions retain the same 16-column
layout; the measurement change is absent from the diff. The existing publication
test confirms that the schema override alone permits the mismatch path.

The real latest publication used `allow_schema_change=true` and
`allow_metadata_changes=false`; its P0006/P0045 diffs contain the placeholder.
Fresh independent comparison confirmed their **20,345 / 124,016 rows** are
unchanged and in order after excluding only producer revision labels. Thus
this is a future-review blind spot, not evidence of a 111 km error in the archive.

- [ ] Revise the comparison policy so a schema override does not implicitly
  approve unknown scientific edits. Compare rows for supported revisions with
  the same layout; require separately reviewed change evidence when comparison
  is unavailable. No generic schema migration framework or legacy reader is needed.
- [ ] Add one focused supported-family schema-plus-latitude-change test; require
  a visible row change and its separate approval before transfer.
- [ ] Update [publication reports](publication-reports.md), the
  [contract](contract.md) and the consumer counterpart when the policy changes.

### RA-02: loaded waveform agreement does not check correction provenance

**Confirmed missing check; proposed release criterion.** The current
[`compare_pair`](../../scripts/geocsv/validate_snapshot.py) verifies loaded
starts but does not compare `TimeCorrectionApplied` with MiniSEED's serialized
correction and applied bit. The documented comparison list does not currently
promise this check. A patched producer can write a correct start and an incorrect
correction-history value without failing any of the 12 scientific checks.

**Numerical example.** In a fresh synthetic four-sample, **20 Hz** fixture,
changing GeoCSV's correction from **0 to +2 seconds**, while leaving the original
MiniSEED/SAC unchanged, passes validation and `require_acceptance` with **12/12
checks true**. The original MiniSEED correction is **0 ticks**. The claimed
correction error is **2 seconds**, or **40 sample intervals**. The consumer
correctly preserves that incorrect source claim without changing waveform time.

Fresh read-only inspection of the actual corpus examined **240,242 MiniSEED
records in 43,333 files**. Every applied bit is set, and all corrections agree
with GeoCSV within the independent serialization allowance. A naive exact
re-rounding test would nevertheless flag **1,158 records in 214 files**:
each discrepancy is exactly **50 µs**. For N0001 source index **1050**, physical
line **1064**, GeoCSV reports **−0.466050 s** while
`20190331T071319.01_5CAD1886.MER.REQ.WLT5.mseed` stores **−4661 ticks = −0.4661 s**.
Re-rounding the printed value with ties to even gives −4660 ticks. This is
consistent with independently quantizing the original value to six decimal
places and 100 µs ticks; it is not a demonstrated timing defect.

- [ ] Add a focused publisher check of each original MiniSEED record's applied
  bit and correction against the matched GeoCSV value. Keep it separate from
  the loaded-start comparison and record the measured discrepancy.
- [ ] Specify the precision rule first: independent nearest-1-µs and
  nearest-100-µs serialization permits up to **50.5 µs** difference. Do not
  require equality after re-rounding the six-decimal cell, widen association
  tolerances, or apply the correction to the start a second time.
- [ ] Cover the +2 s rejection and the real −0.466050 s boundary example.
  Update the validation contract and consumer acknowledgement. Automaid may be
  patched if a real inconsistency is found; no producer test-suite overhaul is required.

### RA-03: incomplete producer clash reports can be labelled verified

**Confirmed evidence-validation defect.**
[`recording_evidence`](../../scripts/geocsv/_evidence.py) checks the report's
binding, row references and filenames, but not required `variant_count`,
`header_differences` or `payload_bytes_identical` fields. The existing
`test_clash_filenames_verified_without_mer_header_interpretation` even accepts
an entry missing two of these fields. Structural validation can remain small
and need not interpret raw MER headers or reproduce producer algorithms.

**Numerical example.** Current P0006 source index **100**, line **114**, maps
**3 MiniSEED files to 2 raw variants**. Reported `FORMAT.SAMPLING_RATE` values
are **20.007053 / 20.007053 / 20.007048 Hz**, a **0.000005 Hz** spread; raw
payload bytes are reported identical. Removing all three required fields from
each of P0006's **3 clash entries** in a temporary sidecar still returns
`status="verified"`. The actual archived sidecar contains the fields and was
not changed. Binding proves which report was supplied, not that it is complete.

- [ ] Require the documented fields and their basic types; verify per-file
  references in difference entries without judging the scientific differences.
- [ ] Add one malformed-report rejection test and retain acceptance of the
  complete real shape. Describe verification as binding/reference/structure
  verification; raw header and payload findings remain producer assertions.
- [ ] Preserve repeated-original semantics. **43,333 pairs / 43,316 Recording
  rows** is valid accounting, not 17 excess rows to remove. Repetition alone
  does not establish a clash: identical raw events may also repeat.

### RA-04: the independent gate omits the rate-diagnostic limit

**Confirmed gate-consistency defect.**
[`check_measurements`](../../scripts/geocsv/gate_snapshot.py) checks that
`association_rate_error_hz` is finite and nonnegative, but never bounds it by
the declared matching rule. Recomputing maxima therefore does not detect an
otherwise internally consistent out-of-limit diagnostic.

**Numerical example.** Editing only a temporary synthetic report's rate error
to **0.1 Hz** and recomputing its maxima still passes `require_acceptance`.
That is **10,000 times** the declared **0.00001 Hz** allowance. The real full
corpus maximum is **0.0000034332129956737845 Hz**, about **34.3%** of the
allowance; no out-of-limit actual association was found. The normal consumer
already rejects large rate differences, so this demonstrates an incomplete
gate rather than a normal validator-produced bad match.

- [ ] Check rate diagnostics consistently with the consumer's documented
  floating-point endpoint rule; retain enough rate evidence if needed to
  reproduce that rule. Do not change the scientific tolerance.
- [ ] Add a focused copied-report rejection test and retain endpoint coverage.
  Update the report reference and linked consumer acknowledgement.

### RA-05: external responses are not covered by original-corpus acceptance

**Accepted input limitation, rechecked with current hosted metadata.** The
saved EarthScope response `P0006_record_100.mseed` has **4,800 samples** at
**2018-07-06T01:49:28.613021Z**. Current P0006 REQ index **100** starts at
**01:49:28.590640Z**, **22.381 ms** earlier; DET index **101** starts exactly
with the response but has **4,736 samples**, **64 fewer**. Strict association
rejects; opt-in containment rejects **2 containing anchors**. These are the
correct outcomes. The [consumer checklist](../../../mermaid-geocsv/docs/audit/release-audit-2026-11-06.md)
records the response hash and evidence boundary.

- [x] Keep this limitation explicit. Passing **43,333 original pairs** does not
  certify every external service response. No tolerance widening, automatic
  anchor selection, reconstruction project or additional release blocker is implied.

## Evidence and verification

The live [testing pointer](https://bathymetrix.com/geocsv/testing/latest.json)
was read on 2026-11-06 and selects
`2026-11-05T23:41:47.235000Z`. The public
[manifest](https://bathymetrix.com/geocsv/testing/releases/2026-11-05T23-41-47.235000Z/manifest.json)
is byte-identical to the archived **28,636-byte** manifest. Local archive root:
`$MERMAID/publisher/geocsv/testing/`.

| Binding | Value |
| --- | --- |
| Manifest SHA-256 | `7d75dbc537bfc39769b7feff496ca7f2d1834f67ff5b9e42502095161c9d5e16` |
| Accepted report | `validation/2026-11-05T23-41-47.235000Z/validation-full-rc1.json` |
| Report SHA-256 | `e310db4253c336233f95ebf8fd023b1091afc53ef16ac73d9cb5d74640367074` |
| Source processed commit | `a387bbb3b4436cb9b36a6fb4eccff74b64d0d4de` |
| Publisher inspected commit | `26862f0d30c6f42a5eb470ec8a5da9d88e2baf09` |
| Consumer inspected commit | `2ca333de4fd53c770eda25c6ef4c4645150f34c3` |
| Automaid inspected commit | `39519e0e3f1de5c4c6d015089b3b4f1392713236` |
| ObsPy read-only source commit | `50033e1daf95233cd4f30e95a49c37fd50be2ccd` |

- [x] Fresh archive check: all **103 payloads**, **479,216,050 bytes**, match
  manifest sizes/hashes; all **103 bundle members** match, without extraction.
  Row accounting is **4,104,855 total / 43,316 Recording**. The **9 recordless
  exclusions** account for the remainder of the **112 source instruments**.
- [x] Fresh local publisher suite: **115 passed**, Python **3.12.4**, consumer
  **0.29.0**, ObsPy **1.5.1**, pandas **3.0.6**, NumPy **2.5.3**; `pip check`
  passed. Publisher and installed consumer code hashes match the accepted report.
- [x] Fresh `require_acceptance` on the complete archived candidate/report
  passed against the canonical source: **86,872 source inputs**, **43,333
  passing pairs**, **0 failed/missing/unsupported/unexamined**. This rechecked
  fingerprints, software, parsed payloads and coverage rather than rerunning
  the waveform comparisons.
- [x] Fresh consumer suite: **425 passed, 9 expected warnings**, including
  **27 tutorial checks**; installed-wheel smoke and `pip check` passed. See
  the counterpart for its separate environment.
- [x] Fresh isolated probes reproduced RA-01–RA-04. Source products and frozen
  reports were never edited. RA-02's header inspection covers every original
  MiniSEED record, not just one record per file.

The [publication record](full-corpus-rc1-publication.md) and immutable client
verification retain the earlier exhaustive **43,333-pair** comparisons and
public checks of **313 release objects**. This audit freshly read public latest
and the manifest; it did not redownload all public payloads or rerun every SAC
comparison. Local suites initially failed on sandbox-blocked localhost sockets;
the reruns with localhost access passed. No new environment, upload, deployment,
software/archive commit, tag, archive mutation or source regeneration was performed.

## Ownership, accepted boundaries and checklist maintenance

The publisher owns RA-01–RA-04 fixes. The consumer owns faithful parsing and
initial association; it must not repair producer values or duplicate publisher
gating. A matching producer-generated SAC is an independently read file, not
an independent scientific estimate. For example, a common producer error that
writes **151,800 mbar as 1,518 mbar** and agrees in SAC would give **15.18 m
instead of 1,518 m** under the approved projection. Existing agreement checks
do not independently validate that producer estimate. This is an acknowledged
scientific provenance boundary, not a demand to reimplement automaid here.

Keep this document and the linked consumer checklist synchronized by **RA ID**.
Any change to severity, status, numerical evidence or resolution must update or
explicitly acknowledge the counterpart in the same change. Checkboxes are
manual; there is no automatic synchronization. Changed validation code or
inputs require new acceptance evidence; never edit the frozen report to close
an item. A software-only gate fix can use a distinct report for unchanged
candidate bytes; an already published `validation.json` remains immutable.

Automaid and the site's ownership/hosting documents were inspected; this
documentation-only audit changes neither producer behavior nor serving rules.
If a later resolution changes their contracts, update the relevant documents
at the same time. Post-association processing, persistence and transformed
waveforms are outside this audit.
