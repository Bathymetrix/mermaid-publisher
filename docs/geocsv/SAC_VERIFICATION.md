# SAC header refactor and retained verification

Consumer 0.25.0 replaces `geocsv.write_sac(trace, path)` with optional
`geocsv.associate(..., create_sac_header=True)` and ordinary ObsPy writing.
The consumer owns matching and the scientific station location projection;
this publisher owns verification of final waveforms and scratch SAC exports.
Publisher repository version: 0.2.0. Report schema 3, scientific limits and
the manifest/download protocol are unchanged.

## Consumer contract

True creates a fresh `stats.sac` through ObsPy's public
`SACTrace.from_obspy_trace(..., keep_sac_header=False)` conversion and adds
only stla/stlo/stel/stdp. The destination must be absent. All requested
projections validate before any trace changes. False leaves existing SAC
headers alone. Native Stats and samples remain authoritative and unchanged.
Only a complete finite coordinate pair and valid declared units are accepted.
Depth uses the documented WaterPressure[mbar]/100 approximation; missing REQ
pressure remains undefined and missing DET pressure raises. Other GeoCSV
fields remain in the source attachment, not additional SAC mappings.

User writing is `Trace.write` or `Stream.write` with ObsPy's default
`keep_sac_header=True`; False discards the projection. File naming, overwriting,
byte order and storage conversion belong to ObsPy. Later waveform processing
does not refresh association. The consumer does not offer export-time checks.
The synchronized consumer WRITE_SAC tutorial now exercises both ObsPy writers.

## Publisher checks

Internal `_verify_sac.py` retains the former exporter preflight: one Trace,
a valid association label/report/waveform snapshot and dataset provenance;
exact native/source/snapshot SNCL and storage-safe identity; loaded, nonempty,
unmasked association-time count; finite real float32-representable samples;
unchanged start and rate; source rate agreement within the existing endpoint
rule; storage-safe delta, calibration metadata, depth and final e; coordinate
bounds, declared units and missing-pressure rules. Calibration values that
collide with SAC undefined after float32 conversion still raise. Counts have
no tolerance. Anchor source count may differ from the loaded waveform count.

For current consumers, verify the already-created four geographic fields
against attached source evidence and verify the ObsPy scale/calib mapping.
These comparisons never repair a header or perform association. Scratch
exports use ObsPy on a copy, with float64 accumulation over the float32-stored
sample values to retain finite summaries for large finite float32 inputs.
Exclusive creation protects existing files and failed preflight creates none.
Source files are never reopened and supplied traces remain unchanged. An I/O
failure can still leave a partial scratch file. Equal-length filtering or
sample replacement cannot be inferred from association headers.

`compare_pair` retains every existing report comparison: strict label, identity,
count, exact native/reference float32 samples, exact native interval, at most
one reference interval ULP, native/reference first-sample time, geographic
coordinates, depth and zero elevation. No tolerance has been widened.
`software.publisher_code_sha256` now also binds `_verify_sac.py`. Altered
software or evidence requires a distinct fresh report; old reports and hosted
objects are not rewritten.

## Compatibility

The frozen consumer remains 0.24.0 at
`33ed5ff477b6c44447d472fc8e828b5ae930e0db`, with unchanged requirements and
fingerprint fixtures. The publisher explicitly detects the public association
keyword: current consumers create headers during association and use local
verification plus ObsPy writing; the frozen consumer continues through its
existing public writer. No consumer private implementation is imported.
Historical manifest/payload fixtures and archived reports remain unchanged.
The publisher's pinned environment is retained; current source is selected
explicitly through PYTHONPATH for local compatibility tests.

## Verification migration inventory

The removed 0.24.0 writer SHA-256 is `c6398145e4f767bf5b680954223b928f4b9a15f4702554ff00ddf5015592bf9f`.
Its original test module SHA-256 is `0f5dac6b9ca129091c6c9d7b0828edd2edbea9cd221c2d4c38160e2c9caec5ab`.
Every one of its 21 test functions has an explicit destination below.
Consumer tests live in `tests/test_sac_headers.py`; publisher tests live in
`tests/geocsv/test_sac_verification.py` and existing archive-validation tests.

| Former test | Retained verification |
| --- | --- |
| `test_real_roundtrip_and_independent_sac_reference` | consumer `test_real_roundtrip_and_independent_sac_reference`; publisher archive comparisons |
| `test_attached_source_only_no_reread_or_existing_sac_defaults` | consumer destination rejection and `test_fresh_headers_source_quality_and_no_reread`; publisher `test_no_source_reread_or_coordinate_fallback` |
| `test_existing_file_is_preserved` | publisher `test_existing_output_is_preserved` |
| `test_requires_one_trace` | publisher `test_requires_one_trace` |
| `test_requires_standard_association` | publisher `test_requires_association_snapshot_and_dataset_metadata` |
| `test_changed_waveform_is_rejected` | publisher `test_changed_waveform_identity_start_count_rate_rejected` |
| `test_invalid_geographic_source_fails_before_creating_file` | consumer `test_invalid_geographic_source_fails_without_mutation`; publisher `test_invalid_geographic_values_rejected` |
| `test_declared_units_are_required` | consumer `test_declared_units_are_required`; publisher `test_declared_units_rejected` |
| `test_missing_request_pressure_uses_source_quality_and_never_previous_depth` | consumer `test_fresh_headers_source_quality_and_no_reread`; publisher `test_missing_request_pressure_stays_undefined_and_is_not_borrowed` |
| `test_masked_and_empty_data_are_rejected` | publisher `test_masked_and_empty_samples_rejected`; unchanged consumer association tests |
| `test_submicrosecond_start_empty_location_and_float32_samples` | consumer `test_native_nanoseconds_and_calibration_survive_header_initialization`; publisher `test_roundtrip_precision_identity_calibration_and_no_mutation` |
| `test_incomplete_attachment_is_rejected` | publisher `test_incomplete_source_identity_count_start_and_quality_rejected` |
| `test_missing_dataset_provenance_is_rejected` | publisher `test_requires_association_snapshot_and_dataset_metadata` |
| `test_clipped_real_det_uses_containing_anchor_geography` | consumer `test_clipped_real_det_uses_containing_anchor_geography`; publisher round-trip and changed-count tests |
| `test_unrepresentable_samples_fail_before_file_creation` | publisher `test_nonfinite_complex_overflow_and_underflow_samples_rejected` |
| `test_large_finite_float32_samples_have_finite_summary_headers` | publisher `test_finite_float32_summary_headers_do_not_overflow` |
| `test_identity_must_survive_sac_serialization` | publisher `test_identity_storage_rejects_truncation_unicode_padding_and_null` |
| `test_unrepresentable_numeric_headers_fail_before_file_creation` | publisher `test_numeric_header_overflow_underflow_and_null_collision_rejected` |
| `test_incomplete_association_report_is_rejected` | publisher `test_requires_association_snapshot_and_dataset_metadata` |
| `test_changed_rate_within_source_tolerance_is_rejected` | publisher `test_changed_waveform_identity_start_count_rate_rejected` |
| `test_source_rate_agreement_uses_ten_microhertz_limit` | publisher `test_source_rate_exact_endpoint_and_next_float` |

The prior ability to ignore an existing input `stats.sac` is intentionally
replaced by the consumer's absent-destination requirement. The corresponding
coverage now tests rejection (including empty destinations and later batch
conflicts), unchanged input on failure, per-trace allocation and native
metadata preservation. Geographic checks run during projection as well as
publisher preflight; export-only checks do not expand the consumer API.

## Local verification status

Local checks on 2026-10-26:

- Consumer: all 446 tests passed, including Markdown/notebook parity and every
  tutorial's Python examples from all three documented working directories.
  Nine expected noninteractive Matplotlib warnings remain.
- Consumer wheel: 0.25.0 built and passed the isolated installed-wheel smoke
  check in a disposable environment, including lazy ObsPy loading, absence of
  the removed writer/module and all four geographic output fields.
- Publisher: all 72 tests passed with the explicit current source. The frozen
  baseline run passed with one expected skip for the current-only projected
  header tampering check. Its exact source fingerprints still match the
  historical fixture. Both runs retain the existing one-ULP and timing limits.
- Website: all 11 existing Worker tests passed; serving code is unchanged.
- The 21-function migration table above was checked against the complete
  original exporter test module. Requirements, baseline fingerprints and
  historical download fixtures are unchanged.

These synthetic/fixture checks are not a new canonical-corpus acceptance run
or live hosting verification. No deployment, publication, pointer change,
archive mutation or software commit was performed. Existing reports and
already hosted artifacts remain bound to their original software.
