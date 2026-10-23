# GeoCSV testing infrastructure plan

This checklist tracks preparation and verification of the isolated GeoCSV
testing service. The production collection remains inactive. Deployment and
uploads require separate explicit authorization. Credentials and private
operational configuration stay outside both repositories.

Hosted testing is limited to P0006 and P0045. Full-corpus validation remains a
separate local check in a temporary workspace. Instrument scope is frozen at
creation and remains identical through validation and publication; there is no
selection at publishing. Validation alone creates no archival obligation.

Initial workflow-testing snapshots are disposable and may be retired after
verification through separately authorized cleanup. They are not permanent
scientific releases. Retain immutable bytes until retirement; never reuse their
testing identities for different bytes. No cleanup has been performed or
authorized. Production retention remains indefinite.

## 1. Re-establish live deployment status

- [x] Confirm the publisher, website and consumer checkouts are at the expected
  migration commits and have no working-tree changes.
- [x] Inspect the local Worker deployment template and hosting implementation.
- [x] Request the public testing pointer in the desktop browser. On
  2026-10-23, `https://bathymetrix.com/geocsv/testing/latest.json` showed the
  GitHub Pages 404 page, not a Worker response.
- [x] Request the public production pointer in the desktop browser. On
  2026-10-23, `https://bathymetrix.com/geocsv/latest.json` showed the GitHub
  Pages 404 page. No production pointer was exposed at this URL.
- [x] Read the public GeoCSV landing page. It identifies hosted data as testing
  only and states that production downloads are not available.
- [x] Recheck authoritative DNS and DNSSEC/DS through two independent public
  resolvers. Both confirm Cloudflare authority and no DS record on 2026-10-23.
- [x] Confirm the private testing bucket is empty through the S3 API and its
  testing latest pointer is absent.
- [x] Confirm the intended Worker does not yet exist in the dashboard.
- [x] Confirm the planned route does not replace another Worker's assignment.
  Wrangler's route-conflict check passed during the approved deployment.
- [x] Retain raw DNS and R2 check evidence in the approved private operational
  location outside both repositories.

## 2. Resolve data licensing and citation

- [x] Review the public MERMAID/EarthScope-Oceans data-policy and FDSN
  citation pages. The policy says release rules can vary by contributing
  organization and instrument; the FDSN network page identifies the MH DOI
  `10.7914/SN/MH` for citation.
- [x] Establish the approved testing scope: P0006 and P0045 only. Broader
  distribution and full-corpus licensing remain deferred.
- [x] Prepare the testing-only scope and MH network DOI in the landing-page
  source. No general data license is inferred from the software license or the
  limited testing authorization.
- [ ] Ship and verify that landing-page description before data uploads.

## 3. Prepare isolated private testing hosting

- [x] Activate R2 through the account dashboard.
- [x] Create the dedicated testing bucket with public access disabled and no
  custom domain.
- [x] Establish a bucket-scoped Object Read & Write operator token and save it
  in the SDK credential provider. Read-only ListObjectsV2/HeadObject checks
  passed without credential output; live conditional writes remain untested.
- [x] Prepare external Worker deployment configuration using the existing
  `workers/geocsv/wrangler.example.jsonc` template and the approved private
  bucket binding. Pin Wrangler 4.152.0 privately and verify its local dry-run
  build. Resolve the entry point relative to the external config location.
- [x] Confirm the Worker remains read-only and serves only the existing route
  design. Keep testing objects under `geocsv/testing` and future production
  objects under the separate `geocsv/` collection namespace. All 11 serving tests
  pass, including the testing header on convenience redirects.
- [x] Verify the separate scoped Wrangler login and intended account, then pin
  private deployment configuration to the account used by the tested R2 endpoint.
- [x] Review the concrete deployment change and recovery procedure, and obtain
  explicit authorization for Worker deployment and read-only verification.
  A Worker fault can be isolated by removing its route, restoring the existing
  GitHub Pages origin path. No recovery change was needed.

## 4. Prepare and accept the exact candidate

- [x] Support immutable selection at creation with `--instruments P0006 P0045`.
  Default creation retains complete-source accounting. Selected creation uses
  local staging schema 2; report schema 3 and the download format are unchanged.
- [x] Verify create and validate in an ordinary temporary workspace without
  Git, archival, uploads or publication intent.
- [x] Reconstruct and review the complete 112-entry serial-to-ID mapping using
  explicit Station records and the nine documented recordless IDs; retain it
  outside both repositories.
- [x] Run fresh full-corpus validation in a temporary workspace with the
  reviewed complete source mapping. Retain the result locally for inspection;
  this check does not populate the publication archive.
- [x] Create the separate P0006/P0045 candidate from the read-only canonical
  `$MERMAID/processed` source in `$MERMAID/publisher/geocsv/snapshots/`.
- [x] Produce a fresh schema-3 exhaustive report for that exact two-instrument
  candidate using the pinned `mermaid-geocsv` 0.24.0 consumer baseline.
- [x] Require the publication gate to accept the candidate, source provenance,
  complete inventory, pair coverage and report. Historical schema-2 acceptance
  for 43,365 pairs cannot satisfy this step.

## 5. Deploy and verify testing service

Deployment and data upload are separate externally visible actions and require
explicit authorization before execution.

- [x] Deploy the private R2 binding and read-only Worker on the approved route.
- [x] Verify landing-page pass-through, GET/HEAD pointer misses, immutable-path
  misses, no-store error responses and the www-to-apex redirect. Confirm the
  bucket remains empty and both testing and production pointers are absent.
- [ ] Verify conditional immutable writes and conflict handling with isolated
  testing objects.
- [ ] Verify exact HTTPS bytes, identity encoding, cache behavior, uncached
  latest responses and misses, and correct `testing_only: true` labels.
- [ ] Verify testing and production pointers and object prefixes remain
  isolated; confirm no production pointer changes.
- [ ] Upload only after the candidate gate passes and upload is explicitly
  authorized. Verify every object against local byte count and SHA-256.
- [ ] Verify pinned and latest `mermaid-geocsv.fetch`, one-instrument and
  complete-inventory downloads, disk and memory modes, and scientific use.
- [ ] Confirm successful publication is recorded in the separate local archive
  with a scoped commit and receipt. Never push automatically.

## 6. Restore DNSSEC

- [ ] After hosting verification, enable DNSSEC at the active authoritative
  provider and install the matching DS at the registrar.
- [ ] Verify the complete DNSSEC chain from independent validating resolvers.
- [ ] Recheck site TLS, redirects, email and the testing endpoint after
  validation is enabled.

## Current execution notes

Fresh schema-3 validation and acceptance completed on 2026-10-23. The full
temporary snapshot passed all 43,365 original waveform pairs across 103
payloads; nine recordless sources were explicitly excluded. The separate
archived P0006/P0045 candidate passed all 3,292 original pairs. Both reports
have zero failed, missing, unsupported or unexamined pairs, and both passed
the current read-only publication gate. Their manifests and reports are
distinct. No original waveform archives, full-corpus payloads or full-corpus
reports were copied into the publication archive. No uploads or archive
commits were performed. See [fresh schema-3 findings](SCHEMA3_FINDINGS.md).

The approved Worker deployment completed on 2026-10-23. The private bucket
binding and `bathymetrix.com/geocsv/*` route are active. Live GET/HEAD checks
returned the expected uncached 404 responses for absent testing and production
pointers and absent immutable objects, with no content encoding. Landing-page
bytes on apex/www match the pre-deployment baseline; `/geocsv/index.html` also
returns the same page. The bucket remains empty and both pointers are absent.
No objects were uploaded, no latest pointer was written, and no DNS settings
were changed. Successful-object labels, exact payload bytes, immutable caching,
conditional writes and complete client downloads remain unverified.

Wrangler skipped automatic R2 resource provisioning because the scoped login
cannot inspect bucket management state. Deployment succeeded against the
existing bucket; live pointer/object misses and separate SDK reads confirmed
storage access without widening permissions. An additional homepage probe with
Python's default user agent received the existing Cloudflare bot-filter 403;
the homepage returned 200 with a browser user agent. Normal Python requests
under `/geocsv/` passed. Raw deployment and verification evidence remains in the
approved private operational directory outside the repositories.

### Earlier preparation

The public browser checks on 2026-10-23 reached GitHub Pages and returned 404
for both pointer paths. This confirms those URLs were not being served by the
GeoCSV Worker during the check. It does not establish current R2 bucket,
Cloudflare account, DNSSEC or DS configuration. The local archive was empty
apart from its untracked `.gitattributes` and `.gitignore`; no candidate or
schema-3 report was available to inspect. During this initial inspection, no
deployment, upload, DNS change, candidate creation or credential access was
performed.

Subsequent dashboard setup confirmed R2 activation, creation of a private
testing bucket and a bucket-scoped publisher token. The SDK provider resolved
the named profile and read-only API access passed; the bucket is empty and its
testing pointer is absent. Two independent DNS resolvers confirmed Cloudflare
authority and no DS. Private deployment configuration and a pinned local Worker
build were prepared before deployment. Wrangler login and account
access are verified. Anonymous GET/HEAD rechecks returned 200 for the landing
page on apex/www and 404 for both unpublished pointers, through Cloudflare.
The selection/workspace implementation passed 55 offline publisher
tests with the fixed consumer baseline, including memory/disk downloads,
independent full/selected acceptance and scoped fixture-archive recording. Real
source inspection confirmed a clean Git source with 112 GeoCSV source
directories. At that preparation stage, no new corpus validation or publication
candidate had been created.

The public GeoCSV landing page returned the expected page and states that
hosted data are testing only and production downloads are unavailable.

Public licensing/citation reconnaissance found no dataset license in the
publisher or hosting documentation. The EarthScope-Oceans data policy describes
organization-specific release policies; the FDSN MH network record identifies
DOI `10.7914/SN/MH`. These facts do not establish that every instrument in a
future candidate can be redistributed through this service. See the [EarthScope-Oceans
data policy](https://earthscopeoceans.princeton.edu/data/metadata.html) and
[FDSN MH network record](https://www.fdsn.org/networks/detail/MH/).

The public endpoints were reachable using the Codex desktop in-app browser; no
browser access change is needed for read-only public endpoint checks. Authorized
network checks subsequently re-established DNS and SDK access. Raw operational
evidence, account details, actual configuration and tool output remain in the
approved private directory outside the repositories.
