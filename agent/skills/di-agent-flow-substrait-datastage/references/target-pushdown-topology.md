# Target-Pushdown Topology Reference

Load this file when generating a flow from an optimized Substrait plan whose
`nodeKind == "target_full_pushdown_read"`. For `source_full_pushdown_read` (source),
use `source-pushdown-topology.md` instead.

Target mode runs the workload through connector before-SQL, then uses the
connector select-statement for the optimizer-chosen observability SELECT.
Shared graph, sink, schema, template, and MCP subset rules live in
`datastage-generation.md`.

## Required input fields (already validated by `di-agent-query-optimization`)

For `target_full_pushdown_read` the optimized pushdown plan carries:

| Field | Source for the generated flow |
|---|---|
| `enhancement.beforeSqlStatement` | the connector's before-SQL property (Native mode: `enable_before_sql` — string field despite the name; DataStage mode: `ds_before_after_before_sql`) |
| `enhancement.sqlStatement` (observability SELECT) | the connector's select-statement property (Native mode: `select_statement`; DataStage mode: `ds_select_statement`) |
| `root.names`, `baseSchema.names`, `baseSchema.struct.types` | link output schema (column names + types) |
| `advanced_extension.optimization[0].connection_id` | resolves to the DataStage connection name |

## Connector property values for target mode

The default for all pushdown flows is **Native mode**
(`ds_use_datastage = False`). DataStage mode (`ds_use_datastage = True`)
is documented as an alternative for connectors that expose both
(Snowflake, Hive, Impala, JDBC). See
`datastage-connector-sdk-reference.md` section "Pushdown property
naming" for the full per-mode field reference.

**Native mode (default) — Snowflake example:**

```python
from ibm_watsonx_data_integration.services.datastage.models.enums import SNOWFLAKE

conn = project.connections.get(name="<connection-name>")
stage = flow.add_stage(type = "Snowflake", label = "snowflake_0")
stage.use_connection(conn)

stage.configuration.ds_use_datastage = False                         # select Native mode
stage.configuration.read_method = SNOWFLAKE.ReadMethod.select        # SQL-read mode

stage.configuration.select_statement = "<sqlStatement from optimized pushdown plan>" # observability SELECT
# enable_before_sql is a str | None field, NOT a boolean.
# Assigning the workload SQL both enables before-SQL and supplies its value.
stage.configuration.enable_before_sql = "<beforeSqlStatement from optimized pushdown plan>"
stage.configuration.enable_before_sql_node = ""                      # required companion
stage.configuration.fail_on_error_before_sql = True
stage.configuration.fail_on_error_before_sql_node = True
# After-SQL left empty unless the user supplied content
stage.configuration.enable_after_sql = ""
stage.configuration.enable_after_sql_node = ""
stage.configuration.fail_on_error_after_sql = True
stage.configuration.fail_on_error_after_sql_node = True
```

Attach the connection with `stage.use_connection(conn)`. Do not use
`stage.configuration.connection = conn`; the MCP `create_datastage_flow` /
`update_datastage_flow` validator rejects direct assignment to the connection
configuration field.

Other Native-mode connectors (Db2, Oracle, BigQuery, Databricks, MySQL,
PostgreSQL, Teradata, ...) use the same property set minus
`ds_use_datastage` (they don't expose it). The `read_method` field is
also exposed per-connector with its own enum — substitute `SNOWFLAKE`
with the appropriate module (`DB2`, `BIGQUERY`, etc.) and pick the
connector's `select` variant.

**DataStage mode (alternative) — Snowflake example:**

```python
stage.configuration.ds_use_datastage = True                          # select DataStage mode
stage.configuration.ds_generate_sql = False
stage.configuration.ds_select_statement = "<sqlStatement from optimized pushdown plan>"
stage.configuration.ds_before_after = True
stage.configuration.ds_before_after_before_sql = "<beforeSqlStatement from optimized pushdown plan>"
stage.configuration.ds_before_after_before_sql_fail_on_error = True
stage.configuration.ds_before_after_before_sql_read_from_file_before_sql = False
stage.configuration.ds_before_after_before_sql_node = ""
stage.configuration.ds_before_after_after_sql_fail_on_error = True
stage.configuration.ds_before_after_after_sql_read_from_file_after_sql = False
stage.configuration.ds_auto_commit_mode = "enable"
```

**Do not set `database_name`, `dataset_name`, `table_name`, `schema_name`,
`write_mode`, or `table_action`** in either mode — the SQL embeds those.

Notes:

- Fail-on-error for the before-SQL property is intentionally `True` — the
  workload is the whole point of the flow; silent failure would generate a
  successful flow run with no rows changed. Users will misdiagnose this as
  success.
- Do not move the workload into after-SQL. The connector executes
  before-SQL → select-statement → after-SQL; the observability SELECT
  must see the post-workload state.
- Auto-commit is enabled by default (or implicit in Native mode). The
  trailing `COMMIT;` in the workload is therefore optional but harmless —
  keep it as the adapter or user supplied it.

## Schema wiring

`root.names`, `baseSchema.names`, and `baseSchema.struct.types` describe the
*observability SELECT* output, not any of the workload's writes. Wire them
as the link schema between connector and Sequential file:

- Each `baseSchema.struct.types[i]` maps to a DataStage column type per
  `datastage-generation.md`'s type mapping table.
- Each `baseSchema.names[i]` becomes the column name. The optimizer has
  already sanitized these; do not re-sanitize.
- The observability SELECT's trailing aliases must already match
  `root.names`. If they do not, the optimizer's validation failed and the
  plan should not have reached this skill — stop and report.

## Sink choice for target pushdown

Default is **Sequential file** (`PxSequentialFile`) so target-pushdown
flows behave like source-pushdown flows for any downstream tooling
that reads the observability output as CSV.

Two alternatives are available on explicit user request:

- **`PxCopy`** — pure pass-through. Generates no file, writes nothing
  to the job log. The lightest option when the user does not care
  about the observability rows at all: the connector's before-SQL has
  already done the real work inside the database, and the sink stage
  exists only to satisfy DataStage's requirement that every output
  link end in a stage. Choose this when the user says "no need to
  write output", "skip the file", "I don't need the rows", or similar.
- **`PxPeek`** — writes rows to the job log. Useful for debugging the
  observability SELECT during development.

When switching sinks, the connector configuration is unchanged; only
the sink stage and its `op` change per `connector-type-label-map.json`
(`PxSequentialFile` / `PxCopy` / `PxPeek`).

## Worked example

Input optimized plan (excerpt):

Note the optimized plan preserves source placeholders. The flow skill
renders them to DataStage job-parameter syntax before assigning to
connector properties.

```json
{
  "relations": [{"root": {
    "names": ["target_table_1_rows"],
    "input": {"read": {
      "common": {"direct": {}, "advancedExtension": {"enhancement": {
        "nodeKind": "target_full_pushdown_read",
        "beforeSqlStatement": "INSERT INTO ${SCHEMA}_DB.target_table_1 (...) SELECT ... FROM ${SCHEMA}_STAGE.staging WHERE load_dt = '${DATA_DT}';\nINSERT INTO ${SCHEMA}_DB.target_table_2 (...) SELECT ... FROM ${SCHEMA}_STAGE.staging;\nCOMMIT;",
        "sqlStatement": "SELECT COUNT(*) AS target_table_1_rows FROM ${SCHEMA}_DB.target_table_1",
        "parameters": ["SCHEMA", "DATA_DT"],
        "flow_metadata": {
          "suggested_flow_name": "load_target_table",
          "parameter_defaults": {"SCHEMA": "PROD"},
          "parameter_bindings": {
            "SCHEMA": {
              "source_syntax": "${SCHEMA}",
              "binding": "local",
              "type": "string",
              "usage": "identifier",
              "description": "Snowflake schema prefix"
            },
            "DATA_DT": {
              "source_syntax": "${DATA_DT}",
              "binding": "parameter_set",
              "parameter_set_name": "BATCH_PARAMS",
              "parameter_name": "DATA_DT",
              "value_set": "prod",
              "runtime_value": "20260101",
              "type": "string",
              "usage": "literal",
              "description": "Run date (YYYYMMDD)"
            }
          },
          "runtime_hints": {"schedule": null, "tags": [], "concurrency_group": null}
        }
      }}},
      "baseSchema": {
        "names": ["target_table_1_rows"],
        "struct": {"types": [{"i64": {"nullability": "NULLABILITY_NULLABLE"}}]}
      },
      "advanced_extension": {"optimization": [{
        "@type": "type.di.ibm.com/com.ibm.di.substrait.Optimization",
        "connection_id": "33a89e3f-3fa2-415d-bbbc-e0569c1ebbd3"
      }]}
    }}
  }}]
}
```

Connector stage properties (Snowflake — Native mode, default). After
the placeholder rewrite, `${SCHEMA}` becomes `#SCHEMA#` and `${DATA_DT}`
becomes `#BATCH_PARAMS.DATA_DT#`:

```python
from ibm_watsonx_data_integration.services.datastage.models.enums import SNOWFLAKE

stage.configuration.ds_use_datastage = False
stage.configuration.read_method = SNOWFLAKE.ReadMethod.select

stage.configuration.select_statement = "SELECT COUNT(*) AS target_table_1_rows FROM #SCHEMA#_DB.target_table_1"
stage.configuration.enable_before_sql = (
    "INSERT INTO #SCHEMA#_DB.target_table_1 (...) SELECT ... FROM #SCHEMA#_STAGE.staging WHERE load_dt = '#BATCH_PARAMS.DATA_DT#';\n"
    "INSERT INTO #SCHEMA#_DB.target_table_2 (...) SELECT ... FROM #SCHEMA#_STAGE.staging;\n"
    "COMMIT;"
)
stage.configuration.enable_before_sql_node = ""
stage.configuration.fail_on_error_before_sql = True
stage.configuration.fail_on_error_before_sql_node = True
stage.configuration.enable_after_sql = ""
stage.configuration.enable_after_sql_node = ""
stage.configuration.fail_on_error_after_sql = True
stage.configuration.fail_on_error_after_sql_node = True
```

At the flow level, declare local parameters, attach parameter sets, and
set the escape environment parameter:

```python
flow.add_local_parameter("string", "SCHEMA", value="PROD", prompt="Snowflake schema prefix")

paramset_batch_params = project.parameter_sets.get(name="BATCH_PARAMS")
flow.use_parameter_set(paramset_batch_params)
flow.set_runtime_value_set(parameter_set_name="BATCH_PARAMS", value_set_name="prod")
flow.set_runtime_parameter_value(parameter_set_name="BATCH_PARAMS", parameter_name="DATA_DT", value="20260101")

# Required environment parameter — escapes single-quotes in parameter
# values substituted into SQL strings. Without this, any parameter value
# containing an apostrophe causes a runtime SQL syntax error.
flow.add_local_parameter("string", "$APT_OSL_PARAM_ESC_SQUOTE", value="True")
```

The multi-line value for `ds_before_after_before_sql` uses Python's
implicit string concatenation: adjacent string literals with only
whitespace between them are joined at compile time, so the three
`"..."` lines produce one string with literal `\n` characters
separating the statements. The wrapping `()` is line continuation; it
does not call a function or build a tuple.

Link schema (one column, one row):

| Name | Type |
|---|---|
| `target_table_1_rows` | `int64` (nullable) |

Sink: Sequential file by default, `<flow_name>.csv`. On explicit user
request, swap the sink to `PxCopy` (no persistence) or `PxPeek`
(write to job log); the connector configuration above does not change.
