# DataStage Generation Reference

Use this file after `SKILL.md` validates that the input is a compact full-pushdown
optimized Substrait plan.

## Extract Plan Fields

Verify again before generating code:

- exactly one top-level relation;
- the relation contains `relations[0].root.input.read`;
- `nodeKind` is `"source_full_pushdown_read"` or `"target_full_pushdown_read"`;
- `sqlStatement` is present and non-empty;
- `read.advanced_extension.optimization[0].connection_id` is present.

Use only the optimized plan's `connection_id` for this workload. If
runtime metadata lookup fails, stop and ask for that connection's
metadata; do not switch to another connector.

Extract:

- `nodeKind` from `read.common.advancedExtension.enhancement.nodeKind`;
- `sqlStatement` from `read.common.advancedExtension.enhancement.sqlStatement`;
- `beforeSqlStatement` from
  `read.common.advancedExtension.enhancement.beforeSqlStatement` when
  `nodeKind == "target_full_pushdown_read"`;
- `connection_id` from `read.advanced_extension.optimization[0].connection_id`;
- output column names from `relations[0].root.names`;
- output column types from `read.baseSchema.struct.types`;
- suggested flow name, parameter defaults, and parameter bindings from
  `read.common.advancedExtension.enhancement.flow_metadata`.

If `flow_metadata` carries resolved table metadata such as catalog,
schema, table, or data asset id, preserve it in the generated summary.

For `source_full_pushdown_read`, `sqlStatement` is the workload SELECT. For
`target_full_pushdown_read`, `beforeSqlStatement` is the workload block
(`INSERT`, `UPDATE`, `COPY`, `MERGE`, etc.) and `sqlStatement` is the
optimizer-chosen observability SELECT whose rows flow into the sink.

After extraction, load the topology reference for the selected mode:

- `source-pushdown-topology.md` for `source_full_pushdown_read`;
- `target-pushdown-topology.md` for `target_full_pushdown_read`.

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

1. One database connector source stage configured in SQL-read mode.
2. One `Sequential file` sink stage.
3. One link from source to sink.
4. Link schema copied from the optimized plan's read `baseSchema`.

Both supported pushdown modes use this same graph. They differ only in
which connector SQL properties are populated:

| `nodeKind` | Connector workload | Connector row source |
|---|---|---|
| `source_full_pushdown_read` | none | `sqlStatement` in the select-statement property |
| `target_full_pushdown_read` | `beforeSqlStatement` in before-SQL | `sqlStatement` in the select-statement property as an observability SELECT |

Read the topology reference for the selected mode before generating code.
The topology files own connector SQL property values. This file owns the
shared two-stage graph, schema, sink, type mapping, template, and MCP
subset rules.

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

Both supported pushdown modes drive the database connector in SQL mode,
not table-name mode. The mode-specific topology file decides which SQL
properties are populated:

- `source-pushdown-topology.md` sets only the connector select-statement
  to the workload SELECT.
- `target-pushdown-topology.md` sets connector before-SQL to the workload
  block and the select-statement to the observability SELECT.

Resolve connector labels, map names, enum names, and SQL-read support from
`references/datastage-connector-sdk-reference.md`. Do not guess enum
spelling. Do not emit `generate_sql_at_runtime = True` with
`select_statement`; that mode is for table-name reads with runtime SQL
generation.

## Parameter Rendering

The optimized plan may preserve source/dialect parameter syntax in SQL.
Render parameters to DataStage syntax only when generating the flow.

Inputs:

- `enhancement.parameters`: normalized parameter names.
- `flow_metadata.parameter_defaults`: optional defaults keyed by
  normalized parameter name. For local bindings, use as the local
  parameter default; for parameter-set bindings, use as a member-level
  runtime value unless `runtime_value` is supplied.
- `flow_metadata.parameter_bindings`: optional binding metadata keyed by
  normalized name.

For every name in `enhancement.parameters`, resolve a binding:

```json
{
  "source_syntax": "${TARGET_DB}",
  "binding": "local | parameter_set",
  "type": "string",
  "usage": "identifier | literal | unknown",
  "description": "Target database",
  "parameter_set_name": "ENV_PARAMS",
  "parameter_name": "TARGET_DB",
  "value_set": "prod",
  "runtime_value": "DW"
}
```

Defaults when a binding is absent:

- `binding = "local"`
- `type = "string"`
- `usage = "unknown"`
- `parameter_name = <NAME>`
- `runtime_value = null`

Local binding is the default. Use a parameter-set binding only when the
optimized plan already says so; the flow skill must not promote local
parameters into parameter sets based on name patterns.

When `source_syntax` is absent, including when the entire binding is
absent, apply the known fallback registry in this order for the
normalized name:

1. `${NAME}` — SnowSQL/shell-template style placeholders. Safe
   backward-compatible default.
2. `&&NAME`, then `&NAME` — SQL*Plus/Oracle-script style placeholders.
   Use only when the token appears for that exact normalized name and
   the source/dialect indicates SQL*Plus-style scripting, or when no
   other fallback matches and the token is outside strings/comments.
3. `:NAME` — named-bind style placeholders. Use only when the token is
   outside strings/comments and is not part of a dialect operator or
   cast syntax.

Do not fallback-render positional `?`; it has no stable parameter name.
Require explicit metadata for positional parameters.

**Already-rendered guard** — before searching for source-syntax tokens,
scan the SQL for existing `#…#` spans. If `#<PS>.<PARAM>#` or `#<NAME>#`
already appears for a parameter, count it as present and skip the
source-token search and rewrite for that parameter. Do not render it
again.

Rewrite SQL text before assigning connector properties:

- local parameter target: `#<NAME>#`
- parameter-set target: `#<parameter_set_name>.<parameter_name>#`

Apply the rewrite to `sqlStatement` and, for target pushdown,
`beforeSqlStatement`. If the declared source token is absent from all
SQL strings **and** the already-rendered form is also absent, stop and
report the missing parameter reference. Do not scan for unrelated
dialect syntaxes beyond the fallback registry. Never rewrite inside SQL
string literals or comments unless the adapter explicitly marks those
spans as template placeholders.

Declare parameters before stage definitions:

```python
flow.add_local_parameter("string", "$APT_OSL_PARAM_ESC_SQUOTE", value="True")
flow.add_local_parameter("<type>", "<NAME>", value="<default>", prompt="<description>")
```

Use `flow.add_local_parameter`, not `flow.add_parameter`. The installed
SDK signature is:

```python
flow.add_local_parameter(parameter_type, name, description="", prompt="", value="", valid_values=[])
```

For parameter-set bindings:

```python
paramset_env_params = project.parameter_sets.get(name="ENV_PARAMS")
flow.use_parameter_set(paramset_env_params)
flow.set_runtime_value_set(parameter_set_name="ENV_PARAMS", value_set_name="prod")  # only when value_set is supplied
flow.set_runtime_parameter_value(parameter_set_name="ENV_PARAMS", parameter_name="TARGET_DB", value="DW")  # only when an explicit value override is supplied
```

Retrieve a parameter set at most once even if multiple parameters use
it. Validate that every referenced `parameter_name` exists in the
retrieved set and that `value_set` exists when supplied. If validation
fails, stop before creating/updating a flow.

Runtime parameter values use three distinct SDK calls:

- `flow.set_runtime_value_set(parameter_set_name="<PS_NAME>", value_set_name="<VALUE_SET>")`
  selects a named value set for the whole parameter set. Use only when
  `parameter_bindings[NAME].value_set` is supplied.
- `flow.set_runtime_parameter_value(parameter_set_name="<PS_NAME>", parameter_name="<PARAM>", value="<VALUE>")`
  overrides one member of an attached parameter set. Use when an
  explicit `runtime_value` is supplied for a `parameter_set` binding. If
  `flow_metadata.parameter_defaults[NAME]` is present for a
  `parameter_set` binding, treat it as this member-level runtime value.
- `flow.set_runtime_local_parameter(local_parameter_name="<NAME>", value="<VALUE>")`
  overrides a local parameter at runtime. Use when `runtime_value` is
  supplied for a local binding; still declare the local
  parameter with `flow.add_local_parameter(...)` first.

Parameter types should use SDK parameter types such as `string`,
`int64`, `sfloat`, `date`, `timestamp`, `encrypted`, `path`, `time`,
or `multilinestring`. Use `string` when unspecified.

For parameters with `usage = "identifier"` and a default value, validate
the default conservatively before writing it into the flow, e.g.
`^[A-Za-z_][A-Za-z0-9_$]*$` for common SQL identifiers. Do not quote or
escape identifier parameters automatically.

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
- include local parameter declarations and parameter-set attachments
  before stage definitions when the optimized plan contains parameters;
  the MCP validator accepts all of:
  - `flow.add_local_parameter(type, name, value=..., prompt=...)`
  - `ps_var = project.parameter_sets.get(name="<PS_NAME>")`
  - `flow.use_parameter_set(ps_var)`
  - `flow.set_runtime_value_set(parameter_set_name="<PS_NAME>", value_set_name="<VALUE_SET>")` (only when value_set is set)
  - `flow.set_runtime_parameter_value(parameter_set_name="<PS_NAME>", parameter_name="<PARAM>", value="<VALUE>")` (only when a parameter-set value override is set)
  - `flow.set_runtime_local_parameter(local_parameter_name="<NAME>", value="<VALUE>")` (only when a local runtime override is set)
- include stage definitions, flow graph, and schema definition;
- omit imports, `cast(...)`, `Connection`, auth/platform setup, project retrieval,
  `project.update_flow(...)`, job creation, job run, monitoring, CLI parsing, and
  environment loading;
- use `project.connections.get(name="<CONN_NAME>")` directly, then attach it with
  `<stage_var>.use_connection(<conn_var>)`;
- do not assign connections through `<stage_var>.configuration.connection = ...`;
  the MCP SDK-code validator rejects that statement even though `connection` is
  listed as a stage property;
- call `create_datastage_flow(flow_name=<FLOW_NAME>, project_id=<PROJECT_ID>, sdk_code=<subset>)`
  to create a new flow, or `update_datastage_flow` with the same arguments to
  overwrite an existing flow in place;
- on clear SDK-code errors, fix and retry with corrected non-empty `sdk_code`;
- if `create_datastage_flow` errors because the name already exists, do NOT retry
  automatically — ask the user whether to overwrite with `update_datastage_flow` or
  pick a new flow name. Conversely, `update_datastage_flow` errors when no flow with
  that name exists, so use `create_datastage_flow` for the first publish.

Use the selected topology file's connector-property model when writing the
stage definition. The resulting MCP subset must still contain exactly one
connector, one Sequential file sink, one link, and one schema.

The link must be a separate statement assigned to a variable, then named via
`link.name = "Link_1"`, then `link.create_schema()`. The chained form
`...connect_output_to(...).set_name("Link_1").create_schema()` is rejected by the
SDK validator ("Link variable 'None' does not exist").

Expected-code conventions:

- Stage variables are lowercase with numbered suffixes, e.g. `read_000`.
- Connection variables use `conn_<stage_var>`.
- `flow.add_stage` uses named arguments: `type = "...", label = "..."`.
- Schema variables are named `schema_<source_stage_var>`.
- Schema fields use `add_field("<DATASTAGE_TYPE>", "<column_name>", ...)` — the
  **DataStage type is the first positional argument, the column name the second**
  (e.g. `add_field("BIGINT", "LOADED_ROW_COUNT", nullable=True)`). Passing the name
  first fails validation (`'<name>' is not a valid schema field type`). Keyword
  arguments accepted by the installed SDK: `nullable=True`, `length=...`,
  `precision=...`, `scale=...`.
