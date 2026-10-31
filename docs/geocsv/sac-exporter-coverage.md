# SAC exporter coverage evidence

This source-bound record preserves the original exporter/test fingerprints and
coverage mapping. It is not a supported consumer API or installation guide.
Current checks are defined in [SAC verification](sac-verification.md).

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
