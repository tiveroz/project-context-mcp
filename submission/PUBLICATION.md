# Publication and catalogue proposal

Public source is maintained at https://github.com/tiveroz/project-context-mcp. Do not make an existing private repository public or reuse its Git history.

1. Create a new public repository named `project-context-mcp` under the chosen public identity, with this source and synthetic data only. Review the MIT licence and public attribution before publishing. Repository/identity details and the contribution itself will be public.
2. Obtain its actual full source commit SHA. Render the manifest:

   `python submission/render_manifest.py --repo OWNER/project-context-mcp --commit FULL_SHA --output /path/to/hermes-fork/optional-mcps/project-context/manifest.yaml`

3. Against a disposable current Hermes fork, read CONTRIBUTING.md and current catalogue validation instructions, search existing proposals, and run the relevant validation. A manifest parser accepts fields but cannot grant approval. Resolve any install/probe or compatibility issues before submission.
4. Open a focused upstream PR containing the rendered catalogue entry, public source link, exact pin, disclosures and actual validation evidence. Keep the server source in its standalone repo. Nous maintainers decide acceptance and destination; do not self-label it official.
5. A catalogue merge, if accepted, is distinct from installation in an organisation's managed Hermes environment. Follow that environment's applicable approval route.