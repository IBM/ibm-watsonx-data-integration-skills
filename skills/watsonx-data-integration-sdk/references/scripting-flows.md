# Direct SDK scripting (power-user path)

Write Python locally against the `ibm_watsonx_data_integration` SDK. Use this when the user is running scripts themselves (Claude Code workflow, CI job, notebook) rather than submitting code through MCP.

For creating flows from scratch in a conversational flow-authoring workflow, prefer `pyflow`.
For editing existing flows via MCP, see [editing-flows.md](editing-flows.md).

---

## Authoring workflow

```
1.  authenticate              → IAMAuthenticator + Platform
2.  get project               → platform.projects.get(project_id=...)
3.  (streaming only) engine   → project.engines.get_all() — verify health.status == 'online'
3b. (streaming only) env      → project.environments.get_all()
4.  create flow               → project.create_flow(name=..., flow_type=...)
5.  discover stages
        batch      →  stages/ reference or datastage_property_lookup
        streaming  →  list_available_streaming_stages (MCP)
                      list_all_available_stage_configurations_streaming (MCP, batch 5–8 at a time)
6.  add stages                → flow.add_stage(label=..., type=...)
7.  configure stages          → inspect stage.configuration, set fields using accepted_values
8.  connect stages            → origin.connect_output_to(destination)
9.  define link schemas       → link.create_schema().add_field(...)
10. update flow               → project.update_flow(flow)
11. validate
        batch      →  flow.compile()
        streaming  →  flow.validate() — inspect ValidationResult.issues
12. create job                → project.create_job(name=..., flow=flow)
13. start job                 → job_run = job.start()
```

Auth boilerplate, collection methods, connection binding, schema field syntax, column types: [sdk-conventions.md](sdk-conventions.md).

Batch-only nuances: [batch-ds.md](batch-ds.md).
Streaming-only nuances (engine pre-flight, engineless mode, Stream Selector, MCP stage discovery parsing): [streaming-streamsets.md](streaming-streamsets.md).

---

## Worked examples

See [examples/](../examples/) for end-to-end flows covering transforms, filters, funnels, fan-out, and every column type.

---

## Clarify before building

When configuration details aren't provided, ask the user — don't guess. Typical gaps:
- Database stages: table name, schema name, column names/types
- File stages: file path, format, delimiter, header
- Target stages: load mode (append/overwrite/upsert), key columns

Good SDK code requires complete metadata. Prompt for it.
