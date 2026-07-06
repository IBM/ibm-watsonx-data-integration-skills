# Source-Pushdown Topology Reference

Load this file when generating a flow from an optimized Substrait plan whose
`nodeKind == "source_full_pushdown_read"`. For `target_full_pushdown_read`, use
`target-pushdown-topology.md` instead.

Source mode has no before/after SQL workload. The connector's
select-statement is the workload SELECT and directly produces the link
rows. Shared graph, sink, schema, template, and MCP subset rules live in
`datastage-generation.md`.

## Required input fields (already validated by `di-agent-query-optimization`)

For `source_full_pushdown_read` the optimized pushdown plan carries:

| Field | Source for the generated flow |
|---|---|
| `enhancement.sqlStatement` | the connector's select-statement property (Native mode: `select_statement`; DataStage mode: `ds_select_statement`) |
| `root.names`, `baseSchema.names`, `baseSchema.struct.types` | link output schema (column names + types) |
| `advanced_extension.optimization[0].connection_id` | resolves to the DataStage connection name |

`enhancement.beforeSqlStatement` must be absent or null in source mode.

## Connector property values for source mode

Full source pushdown drives the read connector in SQL mode, not table-name
mode:

```python
conn_read_000 = cast(Connection, project.connections.get(name="<connection-name>"))
read_000 = flow.add_stage(type = "<connector_stage_label>", label = "<map_name>_0")
read_000.use_connection(conn_read_000)
read_000.configuration.execution_mode = <CONNECTOR_ENUM>.ExecutionMode.seq
read_000.configuration.read_method = <CONNECTOR_ENUM>.ReadMethod.select
read_000.configuration.select_statement = """<sqlStatement from optimized pushdown plan>"""
```

Render any source/dialect placeholders in `enhancement.sqlStatement` to
DataStage job-parameter syntax before assigning `select_statement`. Parameter
binding, fallback source-token detection, local parameter declarations, and
parameter-set attachment are shared rules in `datastage-generation.md`.

Resolve `<connector_stage_label>`, `<map_name>`, and `<CONNECTOR_ENUM>` from
`datastage-connector-sdk-reference.md`. Do not guess enum spelling.

Set `execution_mode` to `ExecutionMode.seq` when the connector exposes that
enum. If a connector has no `execution_mode` field, omit it.

Do not emit `generate_sql_at_runtime = True` with `select_statement`; that
mode is for table-name reads with runtime SQL generation.

Do not enable before/after SQL in source mode unless the user supplied an
explicit non-pushdown customization request outside this skill's supported
topology.

Do not set `database_name`, `dataset_name`, `table_name`, `schema_name`,
`write_mode`, or `table_action` for the source connector. The SQL embeds
the database objects.

## Schema wiring

`root.names`, `baseSchema.names`, and `baseSchema.struct.types` describe the
workload SELECT output. Wire them as the link schema between connector and
Sequential file:

- Each `baseSchema.struct.types[i]` maps to a DataStage column type per
  `datastage-generation.md`'s type mapping table.
- Each `baseSchema.names[i]` becomes the column name.
- The SELECT aliases must match `root.names` after DataStage-safe
  sanitization. If they do not, repair aliases, `root.names`,
  `baseSchema.names`, and SDK schema names together per
  `datastage-generation.md`.

When using PxPeek by explicit request, the connector configuration is
unchanged; only the sink stage changes per `connector-type-label-map.json`.
