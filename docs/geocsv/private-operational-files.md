# Files needed for GeoCSV publishing

This inventory covers the names supplied for
`~/.config/mermaid-publisher/geocsv-testing/`. The private directory and its
contents were not inspected. The classification is based on the publisher and
`bathymetrix-site` Worker source and documentation. It assumes no other
workflow uses this directory.

## Retain for the publisher

| Name | Why |
| --- | --- |
| `instruments.csv` | Required when creating a snapshot, passed explicitly as `create_snapshot.py --inventory`. It supplies the reviewed `instrument_serial,instrument_id` mapping. Validation and publication use the frozen candidate and do not reread this CSV. |
| `r2.json` | Retain provisionally because it may be the only copy of operator-entered R2 values. The publisher has no filename-based dependency on it; see below. |

Remote publication also needs R2 destination settings and SDK credentials,
but the publisher does not require either to live in this directory. The
optional `MERMAID_PUBLISHER_GEOCSV_CONFIG` environment variable selects a JSON file
with `profile`, `endpoint_url`, `bucket`, `base_url`, and `object_prefix` settings.
The same destination values can be supplied as command options. The publisher
uses `boto3.Session` for credentials; it does not load credentials from
`r2.json` by filename or accept credential keys in the optional settings file.
If `r2.json` is the sole retained copy of credentials or destination values,
keep it until those values are available through the SDK provider and command
options or a valid private settings file. Its contents were not checked.

The snapshot, staging inventory, scientific reports, bundle, and publication
receipts belong in the separate `$MERMAID/publisher/geocsv/testing/` archive.
They are not replaced by files in this private configuration directory.

## Optional Worker deployment file

`wrangler.jsonc` is not read, generated, or sourced by checked-in code in either
repository. The site contains only a `wrangler.example.jsonc` template and no
deploy command. The hosting runbook requires actual deployment configuration
outside the site checkout. The listed private file might be that configuration,
but repository evidence cannot establish whether it was used. Keep it if
preserving the existing operator deployment setup matters; it is not needed to
run the publisher or the already deployed Worker. A future deployment can use a
new external configuration based on the site template.

## Not required by the publisher or site Worker source

Under the stated assumption, the following names are not dependencies of the
current publisher commands or checked-in Worker source:

| Names | Code-based reason |
| --- | --- |
| `build`, `build-hyphenated-paths-20261028`, `build.log`, `path-replacement-20261028` | No publisher command reads these build or path-change products. |
| `deployment-preflight.json`, `deployment-result.json`, `deployment.log`, `hosted-verification-20261026T141136Z` | No publisher command reads these deployment records. |
| `dns-status.txt`, `dnssec-restoration-20261026T154321Z.json` | No publisher command reads DNS records or checks. |
| `https-after-worker.json`, `https-before-worker.json`, `https-browser-agent-check.json`, `r2-read-check.json` | No publisher command reads these historical HTTP or storage checks. |
| `scientific-run-context.json`, `testing-layout-migration.json` | No publisher command reads these run or migration records. Scientific acceptance uses the candidate, source, staging inventory, and validation report in the archive. |
| `tooling`, `wrangler`, `wrangler-whoami.log`, `wrangler.log` | No publisher command invokes or reads these names. |

The site has no deployment script or package command that references the
private directory. Its Worker reads the configured `GEOCSV` R2 binding at
runtime. An external Wrangler configuration is an operator-supplied deployment
input, not a runtime file dependency. `tooling` or `wrangler` might contain locally installed
tools, but neither checkout calls those names; such tools can be supplied
separately when a deployment is authorized. The site's template points its
Worker entry point at the site source. Because the actual private configuration
was not inspected, a different `main` path in `wrangler.jsonc` cannot be ruled
out before removing `build` or another apparent deployment product.

This is a code-dependency decision, not an instruction to delete historical
evidence that is wanted for other reasons. No files in the private directory
were deleted for this review.

## Production transition

Renaming `geocsv-testing` does not enable production. The creator currently
writes `testing_only: true`; candidate inspection requires it; publication
requires the local `testing/` collection and testing URL/object prefix. The
Worker has distinct testing and production routes and checks that pointer and
manifest flags match the collection. Production latest is currently absent.

Production needs a separately reviewed publisher and contract change, fresh
scientific acceptance for the exact production candidate, resolved data license
and citation, distinct production destination settings, deployment verification,
and explicit upload and activation authorization. Preserve the existing testing
archive and immutable artifacts; do not relabel them as production. Production
artifacts and evidence have indefinite retention under the current contract.
