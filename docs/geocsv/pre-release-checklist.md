# GeoCSV production pre-release checklist

This is a planning checklist. Production publication is not implemented or
authorized. The current publisher creates and accepts only `testing_only: true`
snapshots and testing destinations; the production latest pointer is absent.
Do not use a testing snapshot or edit a frozen manifest to activate production.

## Decisions and implementation

- [ ] Approve the production instrument scope, data license, citation, and
  formal release policy. The approved testing scope does not establish a
  production scope.
- [ ] Review and implement production collection support in the publisher and
  the publication/download contract, including matching `testing_only: false`
  flags, separate local/archive paths, production URLs and object prefixes,
  retention, and publication recording. Test both collection isolation and
  immutable bytes without uploading real data.
- [ ] Verify the site Worker and consumer against the approved production
  contract. Deploy and verify any required Worker changes through a separately
  authorized operation.

## Private settings and credentials

- [ ] Preserve the current testing settings. Prepare a separate production
  `r2.json` settings file outside both checkouts and the publication archive;
  review its `base_url`, `object_prefix`, `endpoint_url`, `bucket`, and optional
  `profile` for the approved production destination. The current testing
  settings must not be reused unchanged. Do not store credentials in this JSON
  file. Select the approved file with `MERMAID_PUBLISHER_GEOCSV_CONFIG` for the
  production operation. The name `r2.json` is an operator choice, not a path
  discovered by the publisher.
- [ ] Confirm the SDK credential provider uses the intended scoped account and
  permissions without displaying or copying credential values. Keep Worker
  deployment configuration separate from publisher destination settings.

## Candidate and acceptance

- [ ] Freeze a new candidate from the canonical read-only source and the
  reviewed instrument inventory. Require clean Git source state when the
  source is Git, complete source fingerprints, and a distinct immutable
  release identity.
- [ ] Run fresh exhaustive validation for that exact candidate with the
  supported consumer and current publisher. Review the complete report,
  scientific limits, exclusions, mapping/diff evidence, and acceptance gate.
- [ ] Run a read-only publication plan against the approved production
  destination. Resolve any local or hosted contract conflict before upload.

## Publication and verification

- [ ] Obtain explicit authorization for the specific production upload and
  latest activation after licensing, citation, scientific, and infrastructure
  review. A passing test or plan is not authorization.
- [ ] Upload immutable objects, verify their exact public bytes and pinned
  consumer downloads, then activate production latest last using conditional
  writes. Verify testing and production remain isolated.
- [ ] Retain the production payloads, manifests, inventories, reports, bundles,
  and receipts indefinitely. Confirm the scoped local archive commit and
  preserve any receipt needed for network-free recording recovery. Do not push
  the archive automatically.

See the [publication contract](contract.md), [workflow](workflow.md), and the
site [hosting runbook](../../../bathymetrix-site/docs/geocsv-hosting.md) for
current requirements and deployment status.
