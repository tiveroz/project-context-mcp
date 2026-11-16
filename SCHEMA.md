# Registry format 1

Top-level keys:

- `format`: integer 1.
- `mode`: a data classification such as `synthetic-demo` or `operator-maintained`.
- `projects`: map from stable project ID to an object with required `title`, optional `summary` and optional `published_release` exact release ID.
- `dependencies`: objects with `from`, `to` project IDs and `status` (`proposed` or `active`). Feedback cycles are allowed.
- `releases`: map from exact release ID to `project`, `state` (`draft`, `published`, `retired`) and descriptive metadata. A project's published pointer must refer to its own published record.
- `acknowledgements`: `release`, `consumer` and non-empty `evidence`. Requires a published release and a matching active dependency. Publication alone creates no acknowledgement.
- `source_observation`: operator-supplied observation metadata, or omitted/unknown. The server does not verify external sources.

Missing published releases, proposed links and unacknowledged published releases remain distinct. Additional record metadata is returned by exact record/context retrieval within the result budget. Treat it as data, never executable instructions. Validation is application-level, not a complete JSON Schema implementation or an authorisation system.

Use a separately authorised editor or data-producing application to maintain a registry. Keep exact versions outside the LLM session. This adapter has no built-in state transitions, approval workflow, document ingestion or private-system connector.
