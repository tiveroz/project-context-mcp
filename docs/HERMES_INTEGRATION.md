# Hermes catalogue integration verification

Verified 16 November 2026 on Linux x86-64 using Python 3.14.10 and official MCP SDK 1.30.0.

- Server source pin: `599d987a08aaab720c66f07edb1a6dc431e8af43`.
- Hermes checkout: `f8acc26834bf1275c34d09ccc3e51250bcd1e26b` with the proposed manifest added.
- A disposable Hermes home and independent minimal test interpreter were used. No existing user installation was changed. This was not a PM-built full application environment.

## Results

1. The actual `hermes_cli.mcp_catalog.install_entry` parsed the manifest, cloned its exact public commit, ran `python bootstrap.py install`, accepted preloaded `PROJECT_CONTEXT_REGISTRY=demo`, saved enabled server configuration and discovered the six declared tools.
2. An additional actual `hermes_cli.mcp_config._probe_single_server` discovered exactly the six declared tools.
3. A fresh Python process loaded that persisted Hermes configuration and used Hermes's actual `_connect_server` transport. Calls to all six tools succeeded; an attempted `files` record lookup was rejected. Registry bytes were unchanged after the calls.
4. Canonical upstream command:

   `HERMES_PYTHON=/path/to/test-interpreter scripts/run_tests.sh tests/hermes_cli/test_mcp_catalog.py tests/hermes_cli/test_mcp_catalog_env_boundary.py -q`

   Result: **54 passed, 0 failed**, including shipped manifest parsing/version-lock checks with this entry present.
5. Standalone source: **16 tests passed** from the public clone with MCP SDK 1.30.0/Python 3.12; earlier preparation also passed with SDK 1.29.0.

Initial attempts with an incomplete sparse checkout and Python 3.12 for current Hermes hit missing modules and a Python-version incompatibility. Those were corrected by completing required source directories/dependencies and using Python 3.14; no server-code workaround or upstream patch was made.

## Limits

This verifies the Linux catalogue install/configuration/probe and fresh transport calls, not a model conversation, desktop UI, Windows/macOS installation, organisational permission or Nous approval. The complete Hermes test suite and PM-locked application distribution were not exercised. Only synthetic records were used.
