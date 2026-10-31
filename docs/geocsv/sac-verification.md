# SAC export verification

The consumer owns association and station projection. The publisher verifies
the final waveform and scratch SAC export using consumer >= 0.27.0, schema
1.0.0 and ObsPy writing. `Time` is already corrected; Elevation is explicit
source zero, and known blank Location retains its two source spaces.

## Consumer contract

`associate(..., create_sac_header=True)` creates a fresh `stats.sac` through ObsPy's public
`SACTrace.from_obspy_trace(..., keep_sac_header=False)` conversion and adds
only stla/stlo/stel/stdp. The destination must be absent. All requested
projections validate before any trace changes. `False` leaves existing SAC
headers alone. Native Stats and samples remain authoritative and unchanged.
Only a complete finite coordinate pair and valid declared units are accepted.
Depth uses the documented WaterPressure[mbar]/100 approximation; missing REQ
pressure remains undefined and missing DET pressure raises. Other GeoCSV
fields remain in the source attachment, not additional SAC mappings.

User writing is `Trace.write` or `Stream.write` with ObsPy's default
`keep_sac_header=True`; False discards the projection. File naming, overwriting,
byte order and storage conversion belong to ObsPy. Later waveform processing
does not refresh association. The consumer does not offer export-time checks.
See the consumer [SAC tutorial](../../../mermaid-geocsv/tutorials/04_write-sac.md).

## Publisher checks

Internal `_verify_sac.py` checks: one Trace,
a valid association label/report/waveform snapshot and dataset provenance;
exact native/source/snapshot SNCL and storage-safe identity; loaded, nonempty,
unmasked association-time count; finite real float32-representable samples;
unchanged start and rate; source rate agreement within the existing endpoint
rule; storage-safe delta, calibration metadata, depth and final e; coordinate
bounds, declared units and missing-pressure rules. Calibration values that
collide with SAC undefined after float32 conversion still raise. Counts have
no tolerance. Anchor source count may differ from the loaded waveform count.

Verify the already-created four geographic fields
against attached source evidence and verify the ObsPy scale/calib mapping.
These comparisons never repair a header or perform association. Scratch
exports use ObsPy on a copy, with float64 accumulation over the float32-stored
sample values to retain finite summaries for large finite float32 inputs.
Exclusive creation protects existing files and failed preflight creates none.
Source files are never reopened and supplied traces remain unchanged. An I/O
failure can still leave a partial scratch file. Equal-length filtering or
sample replacement cannot be inferred from association headers.

`compare_pair` verifies: strict label, identity,
count, exact native/reference float32 samples, exact native interval, at most
one reference interval ULP, native/reference first-sample time, geographic
coordinates, depth and zero elevation. See [validation limits](validation.md).
`software.publisher_code_sha256` binds `_verify_sac.py`. Altered
software or evidence requires a distinct fresh report; old reports and hosted
objects are not rewritten.
