# Recorded infrastructure verification

The dated observations below identify their original scope and deployment
state. They are retained evidence, not instructions or claims about current
availability. Use the [hosting runbook](../../../bathymetrix-site/docs/geocsv-hosting.md)
for current service behavior and operational requirements.

## Initial testing publication — 2026-10-26

The authorized P0006/P0045 snapshot `2026-10-21T22:48:33.277Z` is published
under the isolated testing collection. Its four immutable objects and testing
latest pointer are present; the production pointer remains absent. Complete
transport, cache, fetch and scientific verification passed, including a fresh
3,292-pair rerun using hosted downloads. The local archive contains the initial
candidate commit and a scoped publication receipt commit. See
[publication findings](schema3-findings.md#initial-hosted-testing-publication--2026-10-26).
No source or DNS changes were made during publication. The separately
authorized DNSSEC restoration was completed afterward as recorded below.

## DNSSEC restoration — 2026-10-26

After hosting verification, Cloudflare DNSSEC signing was enabled and its
matching DS record was saved through Squarespace. Cloudflare confirmed active
protection. Independent Google and Cloudflare validating resolvers returned
successful authenticated answers for DS, DNSKEY, website-address and mail-routing
queries, establishing the chain of trust.

Post-activation checks passed for apex/www HTTPS, canonical redirects, the
GeoCSV landing page and testing pointer/manifest. Both P0006 and P0045 payloads
were downloaded with identity encoding and matched the published manifest's
sizes and SHA-256 values. These HTTP checks used the standard library and were
independent of the consumer environment. Email sending and receiving both
passed. Detailed verification results remain in the approved private operational
location; no DNS record values or private configuration are copied here.

## Preparation and Worker deployment — 2026-10-23

Fresh schema-3 validation and acceptance completed on 2026-10-23. The full
temporary snapshot passed all 43,365 original waveform pairs across 103
payloads; nine recordless sources were explicitly excluded. The separate
archived P0006/P0045 candidate passed all 3,292 original pairs. Both reports
have zero failed, missing, unsupported or unexamined pairs, and both passed
the current read-only publication gate. Their manifests and reports are
distinct. No original waveform archives, full-corpus payloads or full-corpus
reports were copied into the publication archive. No uploads or archive
commits were performed. See [fresh schema-3 findings](schema3-findings.md).

The local layout now derives a `testing/` collection from the manifest flag.
Existing testing artifacts were explicitly moved without byte changes. Reports
were refreshed as `validation-v3-testing-layout.json` because publisher code
fingerprints changed. The full 43,365-pair and selected 3,292-pair runs and their
read-only acceptance gates passed again. The selected snapshot and its evidence
are under `$MERMAID/publisher/geocsv/testing/`; the full check remains temporary.

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
