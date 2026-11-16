# Project Context MCP

A standalone read-only MCP server for small, explicitly configured project registries. It helps an assistant retrieve bounded project context, follow declared dependencies and distinguish published outputs from consumer acknowledgement.

It does not provide a memory service, infer project ownership, scan conversations, watch repositories, approve releases or modify downstream systems. Catalogue submission is a proposal: this package is not Nous-approved, affiliated with Nous or currently listed.

## Install and run

Python 3.10+ and Git for a Git-based catalogue installation.

```sh
python bootstrap.py install
python bootstrap.py run
```

Installation creates a package-local virtual environment and installs the official MCP SDK in the supported v1 range. It accesses the package index during this explicit step. Starting the server never installs or updates anything.

The default registry is a clearly labelled synthetic example. Set the non-secret `PROJECT_CONTEXT_REGISTRY` environment variable to an absolute path, or pass `--registry /absolute/path/to/registry.json` to `bootstrap.py run`, to use your own registry. The value `demo` selects the bundled example. Data stays outside the public source repository.

Direct development invocation with an existing SDK environment:

```sh
python server.py --registry examples/registry.json
python -m unittest discover -s tests -v
```

MCP transport is stdio, not HTTP. No listening port, API key, external service account or hosted backend is required. Configure this server only through the methods permitted by the MCP client's administrator; catalogue inclusion would not override local policy.

## Tools

| Tool | Purpose |
|---|---|
| `list_projects` | Paginated IDs and titles |
| `resolve_project` | Exact ID or name candidates; no silent ambiguous selection |
| `get_project_context` | Project metadata, dependency edges and pending acknowledgements |
| `get_record` | One exact project or release record |
| `list_impacts` | Paginated downstream review scope; feedback cycles terminate |
| `list_pending` | Proposed links, missing releases and missing consumer acknowledgements |

All tools advertise the MCP read-only hint. Actual code exposes no write APIs, shell tools or caller-selected file paths. Hints alone are not a security boundary: a subprocess has the OS permissions of its launcher. Restrict its account/filesystem access where required.

## Registry contract

Format 1 uses `projects` and `releases` maps, a dependency list and explicit consumer acknowledgements; see `examples/registry.json` and `SCHEMA.md`. Files are limited to 2 MiB, projects to 500, dependencies/releases/acknowledgements to 2,000 each, and each result to 12,000 UTF-8 bytes. Pagination limits are 1–20. Oversized context fails explicitly; it is not silently truncated. Byte limits are not token guarantees.

The registry is read once per query. Atomic file replacement by the separately authorised writer avoids partial JSON reads. This server neither writes nor synchronises it. A recorded source-observation time is a claim supplied by that registry; it is not evidence that this server checked the source.

## Data access and privacy disclosure

- Reads the bundled demo or the single operator-configured local registry file, which may be outside the package directory. It does not follow source URLs or scan directories.
- Reads only one documented non-secret environment variable, `PROJECT_CONTEXT_REGISTRY`. It does not open credential stores or application profiles.
- Returns configured registry metadata to the connected MCP client. That client's model/provider may receive the returned content; choose data and access permissions accordingly. Local transport does not guarantee that a client's AI processing is local.
- No runtime network calls, telemetry, analytics, background jobs, self-update mechanism, subprocess tool calls or writes to registry records.
- Explicit installation uses Python's venv/pip and the package index. The launcher replaces itself with the dedicated Python interpreter; it does not spawn an agent or alter client guards.
- Dataset examples are invented and contain no customer, employer or operational records. Production datasets, credentials and personal information do not belong in this public repository.

## Contribution status

The `submission/` directory holds a catalogue manifest template, a renderer that requires a public repository and full immutable commit SHA, and a draft PR body. It contains no fake pin and cannot be submitted unchanged.

This is a separately authored generic implementation with synthetic fixtures; it is not an export of any private project repository or its history. Public source: https://github.com/tiveroz/project-context-mcp. Catalogue acceptance and package-registry publication are separate; neither is claimed.

Linux/Python 3.12 and official SDK 1.29.0 were exercised locally, including a real stdio client session. Windows/macOS interpreter path handling is implemented but has not been tested on those hosts. No installed Hermes version or upstream catalogue acceptance is claimed.
