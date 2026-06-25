# DataStage Generation Reference

Use this file after `SKILL.md` validates that the input is a compact full-pushdown
optimized Substrait plan.

## Extract Plan Fields

Verify again before generating code:

- exactly one top-level relation;
- the relation contains `relations[0].root.input.read`;
- `nodeKind` is `"full_pushdown_read"`;
- `sqlStatement` is present and non-empty;
- `read.advanced_extension.optimization[0].connection_id` is present.

Extract:

- `sqlStatement` from `read.common.advancedExtension.enhancement.sqlStatement`;
- `connection_id` from `read.advanced_extension.optimization[0].connection_id`;
- output column names from `relations[0].root.names`;
- output column types from `read.baseSchema.struct.types`;
- suggested flow name from source metadata, or use `full_pushdown_to_file`.

If `connection_id` is missing, stop and ask:

> The optimized plan does not carry a `connection_id` on the read node
> (expected at `read.advanced_extension.optimization[0].connection_id`).
> Please provide the source database connection ID (UUID), and the matching
> DataStage connection name so the script can call `project.connections.get(name=...)`.

## Type Mapping

| Substrait type | DataStage type |
|---|---|
| `bool` / `boolean` | `BIT` |
| `i8`, `i16`, `i32` | `INTEGER` |
| `i64` | `BIGINT` |
| `fp32` | `FLOAT` |
| `fp64` | `DOUBLE` |
| `decimal` | `DECIMAL` |
| `string`, `varchar`, `char` | `VARCHAR` |
| `date` | `DATE` |
| `timestamp`, `timestampTz` | `TIMESTAMP` |

Nullability:

- `NULLABILITY_NULLABLE` -> pass `nullable=True` to `add_field(...)`.
- `NULLABILITY_REQUIRED` -> omit `nullable`.
- Missing nullability -> pass `nullable=True`.

For strings, pass `length=<length>`; use the plan length when present, otherwise
`1024`. For decimals, pass `precision=<precision>` and `scale=<scale>` when present.

## Two-Stage Topology

The generated flow contains exactly:

1. One database connector source stage that executes the SQL statement.
2. One `Sequential file` sink stage.
3. One link from source to sink.
4. Link schema copied from the optimized plan's read `baseSchema`.

The sink is always `flow.add_stage(type = "Sequential file", label = "sequentialfile_0")`.
`sequentialfile_0.configuration.file` is a one-element list, not a string.

Use a **flat filename** (e.g. `["<flow_name>.csv"]`), not a directory-prefixed path
like `["di/<flow_name>.csv"]`. The Sequential file writer does not create parent
directories: a non-existent prefix aborts the run with
`<APT_RealFileExportOperator ...> Unable to open <path>: No such file or directory`
(0 records exported). Only prefix the path with a directory you have confirmed exists
on the engine storage.

Use these sink defaults:

```python
sequentialfile_0.configuration.file_update_mode = SEQUENTIALFILE.AppendOverwrite.overwrite
sequentialfile_0.configuration.final_delimiter = SEQUENTIALFILE.FinalDelimiter.end
sequentialfile_0.configuration.file = ["<flow_name>.csv"]
sequentialfile_0.configuration.first_line_is_column_names = SEQUENTIALFILE.FirstLineColumnNames.true
sequentialfile_0.configuration.delimiter = SEQUENTIALFILE.Delimiter.comma
sequentialfile_0.configuration.null_field_value = "NULL"
sequentialfile_0.configuration.create_data_asset = True
sequentialfile_0.configuration.data_asset_name = "<flow_name>"
```

`delimiter` and `final_delimiter` are enum-typed (`SEQUENTIALFILE.Delimiter.*`,
`SEQUENTIALFILE.FinalDelimiter.*`) in the installed SDK — pass the enum members
shown above, not quoted strings like `"'|'"` or `"'end'"`, which the validator
rejects. `null_field_value` is a plain string. Verify any enum value with
`datastage_property_lookup(requests=[{"stage": "sequentialfile"}])`.

Always set `create_data_asset = True` on the Sequential file sink, with a
`data_asset_name` (`data_asset_name` is required whenever `create_data_asset` is
True). This registers the written file as a project data asset so the output rows
can be read back via `read_file_data_asset` after the run — without it, the file
lands in object storage uncatalogued and is not directly readable. The asset is
created once and is not refreshed on rerun; if the named asset already exists from a
prior run, delete it (or use a new `data_asset_name`) before re-running to get fresh
contents.

If a live SDK or MCP validator rejects an optional formatting property, remove or
adjust only that property. Do not change the full-pushdown topology. Do not drop
`create_data_asset` / `data_asset_name`.

## SQL-Mode Connector Pattern

Full pushdown drives the read connector in SQL mode, not table-name mode:

```python
conn_read_000 = cast(Connection, project.connections.get(name="<connection-name>"))
read_000 = flow.add_stage(type = "<connector_stage_label>", label = "<map_name>_0")
read_000.use_connection(conn_read_000)
read_000.configuration.execution_mode = <CONNECTOR_ENUM>.ExecutionMode.seq
read_000.configuration.read_method = <CONNECTOR_ENUM>.ReadMethod.select
read_000.configuration.select_statement = """<sqlStatement>"""
```

Resolve `<connector_stage_label>`, `<map_name>`, and `<CONNECTOR_ENUM>` from
`references/datastage-connector-sdk-reference.md`. Do not guess enum spelling.

Set `execution_mode` to `ExecutionMode.seq` when the connector exposes that enum. If
a connector has no `execution_mode` field, omit it.

Do not emit `generate_sql_at_runtime = True` with `select_statement`; that mode is for
table-name reads with runtime SQL generation.

## SQL Identifier Case

Do not rewrite source table or source column identifiers from the SQL generated by the
optimization/SQL skill unless database metadata or a runtime error proves a repair is
needed. SQL mode runs inside the source database, where identifier case rules are
dialect-specific.

Only final output aliases may be repaired for DataStage-safe names. If repaired, keep
the SQL aliases, `root.names`, `read.baseSchema.names`, and SDK schema field names in
the same order.

## Output Column Names

Check each output name:

1. Replace every character outside `[a-zA-Z0-9_]` with `_`.
2. If the result does not start with a letter, prepend `col_`.
3. If empty or null, use `col`.
4. Deduplicate with `_1`, `_2`, and so on.

If the checked name is unchanged and unique, keep it. If it changes or collides, use
the repaired name in all three places:

- trailing SQL `SELECT` alias: `AS <canonical_name>`;
- `relations[0].root.names` / `read.baseSchema.names`;
- SDK schema: `schema_<source>.add_field(..., "<canonical_name>")`.

## SDK Script Skeleton Contract

The authoritative complete script is `references/template-skeleton.py`.

1. Do not rewrite anything outside the `# <<< BEGIN_FILL >>>` /
   `# <<< END_FILL >>>` block inside `create_flow()`.
2. Substitute `<FLOW_NAME>` and `<PROJECT_ID>` everywhere in the boilerplate.
3. Generate the fill region with exactly three labeled sections:
   - `# Stage definition` — one SQL-mode database source and one Sequential file sink.
   - `# Flow graph` — exactly one source-to-sink link.
   - `# Schema definition` — one `add_field(...)` per output column.
4. Keep `flow_type="batch"` and `description=""`.
5. Keep `platform = Platform(auth, base_api_url=base_api_url, base_url=base_auth_url)`
   in the complete skeleton.

Do not use older complex-skill skeletons with `.env`, `PROJECT_GUID`, `--apply-only`,
`--delete`, resilience caching, or `project.update_flow(flow=cast(...))`.

## MCP Create/Update Subset

When `create_datastage_flow` is available (or `update_datastage_flow`, for revising
an existing flow), send only the subset:

- include `flow = project.create_flow(name="<FLOW_NAME>", description="", environment=None, flow_type="batch")`;
- include stage definitions, flow graph, and schema definition;
- omit imports, `cast(...)`, `Connection`, auth/platform setup, project retrieval,
  `project.update_flow(...)`, job creation, job run, monitoring, CLI parsing, and
  environment loading;
- use `project.connections.get(name="<CONN_NAME>")` directly;
- call `create_datastage_flow(flow_name=<FLOW_NAME>, project_id=<PROJECT_ID>, sdk_code=<subset>)`
  to create a new flow, or `update_datastage_flow` with the same arguments to
  overwrite an existing flow in place;
- on clear SDK-code errors, fix and retry with corrected non-empty `sdk_code`;
- if `create_datastage_flow` errors because the name already exists, do NOT retry
  automatically — ask the user whether to overwrite with `update_datastage_flow` or
  pick a new flow name. Conversely, `update_datastage_flow` errors when no flow with
  that name exists, so use `create_datastage_flow` for the first publish.

Minimal subset pattern:

```python
flow = project.create_flow(name="<FLOW_NAME>", description="", environment=None, flow_type="batch")

# Stage definition
conn_postgresql_ibmcloud_0 = project.connections.get(name="<connection-name>")
postgresql_ibmcloud_0 = flow.add_stage(type = "IBM Cloud Databases for PostgreSQL", label = "postgresql_ibmcloud_0")
postgresql_ibmcloud_0.use_connection(conn_postgresql_ibmcloud_0)
postgresql_ibmcloud_0.configuration.execution_mode = POSTGRESQL_IBMCLOUD.ExecutionMode.seq
postgresql_ibmcloud_0.configuration.read_method = POSTGRESQL_IBMCLOUD.ReadMethod.select
postgresql_ibmcloud_0.configuration.select_statement = """<sqlStatement>"""

sequentialfile_0 = flow.add_stage(type = "Sequential file", label = "sequentialfile_0")
sequentialfile_0.configuration.file_update_mode = SEQUENTIALFILE.AppendOverwrite.overwrite
sequentialfile_0.configuration.final_delimiter = SEQUENTIALFILE.FinalDelimiter.end
sequentialfile_0.configuration.file = ["<flow_name>.csv"]
sequentialfile_0.configuration.first_line_is_column_names = SEQUENTIALFILE.FirstLineColumnNames.true
sequentialfile_0.configuration.delimiter = SEQUENTIALFILE.Delimiter.comma
sequentialfile_0.configuration.null_field_value = "NULL"
sequentialfile_0.configuration.create_data_asset = True
sequentialfile_0.configuration.data_asset_name = "<flow_name>"

# Flow graph
link_1 = postgresql_ibmcloud_0.connect_output_to(sequentialfile_0)
link_1.name = "Link_1"
schema_postgresql_ibmcloud_0 = link_1.create_schema()

# Schema definition
schema_postgresql_ibmcloud_0.add_field("<DATASTAGE_TYPE>", "<column_name>", nullable=True)
```

The link must be a separate statement assigned to a variable, then named via
`link.name = "Link_1"`, then `link.create_schema()`. The chained form
`...connect_output_to(...).set_name("Link_1").create_schema()` is rejected by the
SDK validator ("Link variable 'None' does not exist").

Expected-code conventions:

- Stage variables are lowercase with numbered suffixes, e.g. `read_000`.
- Connection variables use `conn_<stage_var>`.
- `flow.add_stage` uses named arguments: `type = "...", label = "..."`.
- Schema variables are named `schema_<source_stage_var>`.
- Schema fields use `add_field(...)` keyword arguments accepted by the installed SDK,
  such as `nullable=True`, `length=...`, `precision=...`, and `scale=...`.
