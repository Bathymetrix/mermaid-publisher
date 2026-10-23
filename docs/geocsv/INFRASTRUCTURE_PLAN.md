# GeoCSV testing infrastructure plan

This checklist tracks preparation and verification of the isolated GeoCSV
testing service. The production collection remains inactive. Deployment and
uploads require separate explicit authorization. Credentials and private
operational configuration stay outside both repositories.

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
- [ ] Recheck authoritative DNS, Cloudflare route/binding state, R2 bucket
  state, and DNSSEC/DS state through current account or resolver evidence.
  Shell DNS lookup is unavailable in the current execution environment; public
  page responses do not establish DNSSEC state.
- [ ] Record current Cloudflare state in the approved private operational
  location, not in either repository.

## 2. Resolve data licensing and citation

- [x] Review the public MERMAID/EarthScope-Oceans data-policy and FDSN
  citation pages. The policy says release rules can vary by contributing
  organization and instrument; the FDSN network page identifies the MH DOI
  `10.7914/SN/MH` for citation.
- [ ] Confirm the selected candidate's instrument-by-instrument reuse and
  redistribution rights, including any embargo or owner permission. A network
  DOI is citation guidance, not a data license or proof of redistribution
  rights.
- [ ] Decide the license and citation text for the hosted dataset and its
  landing-page description.
- [ ] Record the decision before preparing any upload. Do not infer licensing
  from software repository licenses or prior hosting.

## 3. Prepare isolated private testing hosting

- [ ] Choose and create the private R2 bucket through the approved account
  workflow; keep public bucket access disabled.
- [ ] Establish least-privilege operator access for the publisher's R2/S3
  operations. Keep credentials in the SDK provider or approved secret store.
- [ ] Prepare external Worker deployment configuration using the existing
  `workers/geocsv/wrangler.example.jsonc` template and the approved private
  bucket binding.
- [ ] Confirm the Worker remains read-only and serves only the existing route
  design. Keep testing objects under `geocsv/testing` and future production
  objects under the separate `geocsv/` collection namespace.
- [ ] Review the concrete deployment change and recovery procedure before
  deployment. Deployment remains unauthorized until explicitly approved.

## 4. Prepare and accept the exact candidate

- [ ] Resolve instrument licensing and citation requirements for the selected
  candidate.
- [ ] Create and freeze a candidate from the read-only canonical
  `$MERMAID/processed` source into `$MERMAID/publisher/geocsv/snapshots/`.
- [ ] Produce a fresh schema-3 full-archive report for that exact candidate
  using the pinned `mermaid-geocsv` 0.24.0 consumer baseline.
- [ ] Require the publication gate to accept the candidate, source provenance,
  complete inventory, pair coverage and report. Historical schema-2 acceptance
  for 43,365 pairs cannot satisfy this step.

## 5. Deploy and verify testing service

Deployment and data upload are separate externally visible actions and require
explicit authorization before execution.

- [ ] Deploy the private R2 binding and read-only Worker on the approved route.
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

The public browser checks on 2026-10-23 reached GitHub Pages and returned 404
for both pointer paths. This confirms those URLs were not being served by the
GeoCSV Worker during the check. It does not establish current R2 bucket,
Cloudflare account, DNSSEC or DS configuration. The local archive was empty
apart from its untracked `.gitattributes` and `.gitignore`; no candidate or
schema-3 report was available to inspect. No deployment, upload, DNS change,
candidate creation or credential access was performed.

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
browser access change is needed for read-only public endpoint checks. Shell DNS
queries are blocked in this execution environment. Cloudflare account state
requires authorized access to the relevant account view or current operator
evidence.
