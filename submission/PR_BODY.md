Adds a proposed read-only Project Context MCP catalogue entry for maintainer review.

The separately maintained server retrieves bounded metadata from one explicitly configured local JSON file: project identity, declared dependencies, release references and consumer acknowledgements. It exposes six read-only tools with no registry writes, source-URL fetching, telemetry or background monitoring. The default is synthetic demo data.

Disclosures: installation clones the public source at the manifest's exact commit and creates a dedicated virtual environment using the package index. Runtime reads the chosen registry, potentially outside its install directory, and returns its contents to the connected client/model provider. This is not a local-data privacy guarantee for a remote AI client. No credentials are required or read. No self-updater, Hermes core patch, protected-file edit or approval bypass is included.

Validation evidence: Linux/Python 3.12, official MCP SDK 1.29.0, unit tests and real stdio tool discovery/query tests. Windows/macOS are not claimed tested. Full installed-Hermes catalogue validation and any requested current-version compatibility checks must be recorded before this PR is submitted as ready for review.

Before opening this PR:
- Replace the manifest template with its renderer output, using the actual public repository commit.
- Link the public source and immutable pin here.
- Search existing issues/PRs for overlapping standalone project-registry MCP entries.
- Run the relevant upstream catalogue validation using a disposable supported Hermes checkout and record the commands/results here. Do not validate by modifying a managed installation.
- Confirm whether maintainers prefer optional-mcps or a community plugin listing for this external server. Do not add native core tools or a new in-tree memory provider.

This is a submission request, not a claim of Nous approval. Local administrators retain control over installation and filesystem/model access.
