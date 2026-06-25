# Connector property values — where each value comes from

Connector label, map-name, connection type alias, enum, and common-property lookups
live in this skill's `references/datastage-connector-sdk-reference.md` table.

Generation needs four pieces of connector information:

1. The connector **label** (`flow.add_stage(type="<label>", label="<node_id>")`) —
   resolve from `references/datastage-connector-sdk-reference.md`.
2. The connection **object** (`<stage>.use_connection(<connection_obj>)`) — built from
   the substrait rel's `connectionId` and the matching project connection name.
3. The connector property **names** (`<stage>.configuration.<sdk_attr>`) — use the
   SDK attribute names listed in `references/datastage-connector-sdk-reference.md` and
   verify with `datastage_property_lookup` when available.
4. The connector property **values** — documented in this file.

This doc owns the value piece: **where does the actual value on the right-hand side
come from?** E.g. `read_000.configuration.database_name = 'wkc-project-280420'` — that
string literal is not in the substrait plan as such; it's pulled from the connection's
metadata. This file documents the exact source for every per-connector configuration
property.

Connector behavior is summarized in this file and in
`references/datastage-connector-sdk-reference.md`.
When a connector-specific rule is missing here, use platform connection metadata or
ask the user instead of guessing.

The resolution rules in this doc cover everything generation needs. Each connector's behavior is already projected into the tables and worked examples below.

---

## Source expressions

Connector property mappings use these source expressions:

| Template expression | Resolves to | Example output |
|-------------------------------|------------------------------------------------------------|---------------------------|
| `namedTable.0` | `readRel.namedTable.names[0]` (or write) | `'TM_DS_USER_1'` |
| `namedTable.1` | `readRel.namedTable.names[1]` (or write) | `'AgenticTargetTable1'` |
| `namedTable.2` | `readRel.namedTable.names[2]` (3-part-name connectors) | `'EMPLOYEES'` |
| `connection.<property>` | `connection.properties.<property>` (from user-supplied connection metadata) | `'wkc-project-280420'` |
| `nodeInfo.sqlStatement` | the SQL string built for SQL-mode reads | `'SELECT * FROM ...'` |
| literal string (no `.`) | used verbatim | `'general'`, `'replace'` |

`connection.<property>` reads from the same connection metadata the label resolution
already used (`{ connections: { "<id>": { type, name, properties } } }`). After looking
up the `type` (hop 1), keep the connection object — its `properties` map (the
per-connection blob) is where these values live. If the property is absent (the user's
metadata was incomplete), ask the user or call `get_connection_info(connection_id)`.

---

## Read stages

Every read connector has connector-specific general/table mode behavior and may have
SQL mode behavior. The resolved properties depend on which mode generation selected.

### Mode selection

Read mode is `"select"` (SQL mode) when:
- The connector supports SQL mode, AND
- The read rel carries a SQL statement in `nodeInfo.sqlStatement` (set by upstream rules
 when the read is fed by a non-trivial projection / filter chain).

Otherwise it's `"general"` (default for nearly every read in a lowered plan that
matches a `bigquery_inner_join*` shape).

### Properties emitted — general mode

For the **general** (table-name) mode, every connector emits a subset of:

| DataStage key | Value source | When |
|-----------------|-------------------------------------------|-------------------------------|
| `read_mode` | literal `"general"` | always |
| `schema_name` | `namedTable.0` | always |
| `table_name` | `namedTable.1` | always |
| `database_name` | `connection.<the connector's db property>`| only when the connector needs a 3rd-part identifier |

The connector's "db property" name varies by connector:

| Connector type | `connection.<key>` for `database_name` |
|------------------|---------------------------------------|
| `bigquery` | `project_id` |
| `db2cloud` | (3-part-name not used — no entry) |
| `snowflake` | `database` |
| (most JDBC ones) | (none — no entry; only schema+table) |

Check the connector reference and connection metadata for the connector-specific
database property. If a `database_name` entry is required, that's where it comes from.

After the **pydantic_alias rename**, these become SDK attributes. For BigQuery:
- `schema_name` → SDK `dataset_name`
- `table_name` → SDK `table_name`
- `database_name` → SDK `database_name`

So a BigQuery read emits:

```python
read_000 = flow.add_stage("Google BigQuery", "read_000")
read_000.use_connection(connection_read_000)
read_000.configuration.database_name = 'wkc-project-280420' # connection.project_id
read_000.configuration.dataset_name = 'ConnectionTest' # namedTable.0 (renamed from schema_name)
read_000.configuration.table_name = 'EMPLOYEES' # namedTable.1
```

### Properties emitted — SQL mode

| DataStage key | Value source |
|--------------------|---------------------------|
| `read_mode` | literal `"select"` |
| `select_statement` | `nodeInfo.sqlStatement` with connector-appropriate quoting |

In the lowered-plan workflow you'll rarely emit SQL mode — it is used
when it folds a Project/Filter chain back into the connector. If you're translating
from a lowered plan that already split out a `CTransformerStage`, the read should be
in general mode.

---

## Write stages

The write side is similar but adds two more properties: `write_mode` and
`table_action`. Both come from substrait and connector-specific write behavior.

### Properties emitted

| DataStage key | Value source |
|-----------------|-------------------------------------------------------------------------|
| `schema_name` | `namedTable.0` |
| `table_name` | `namedTable.1` |
| `database_name` | `connection.<db key>` — same rule as read; only when connector needs it |
| `write_mode` | derived from `writeRel.op` (the `WRITE_OP_*` enum) — **per-connector mapping**, see below |
| `table_action` | literal `"replace"` (every connector hard-codes this) |

### `write_mode` mapping — per connector

Each Write **handler** has its own switch over `WriteRel.WriteOp`, embedded in
the per-connector handler. The mapping is **not uniform** across
connectors — BigQuery, for example, maps `WRITE_OP_UNSPECIFIED` to `"delete_insert"`
where most JDBC connectors map it to `"insert"`.

| Substrait `WriteOp` | Db2 / most JDBC | BigQuery |
|---------------------------|---------------------------------|-----------------------------------|
| `WRITE_OP_UNSPECIFIED` | `"insert"` | `"delete_insert"` |
| `UNRECOGNIZED` | `"insert"` | `"delete_insert"` |
| `WRITE_OP_INSERT` | `"insert"` | `"insert"` |
| `WRITE_OP_DELETE` | `"update"` | `"delete"` |
| `WRITE_OP_UPDATE` | `"update"` | `"update"` |
| `WRITE_OP_CTAS` | `"merge"` | `"merge"` |

Use the per-connector behavior for the write-mode mapping. When in doubt, ask the
user if the substrait write op is not covered by the known mapping.

### Worked example — Db2 write

Two ways to arrive at the same Python:

**Path 1 — from a substrait plan.** Generation walks the relation tree and populates the
DataStage write properties. Substrait input fragment:

```json
"write": {
 "namedTable": { "names": ["TM_DS_USER_1", "AgenticTargetTable1"] },
 "op": "WRITE_OP_INSERT",
 "advancedExtension": {
 "optimization": [{
 "@type": "type.googleapis.com/com.ibm.di.substrait.Optimization",
 "connectionId": "aa3abc5f-15b8-4867-a506-ae5f0cbba3a5"
 }]
 }
}
```

User-supplied connection metadata:
```json
{
 "connections": {
 "aa3abc5f-15b8-4867-a506-ae5f0cbba3a5": {
 "type": "db2",
 "name": "db2conn",
 "properties": {}
 }
 }
}
```

**Path 2 — from a graph plan.** The user hands you a graph plan JSON. The
relevant node is already resolved:

```json
{
 "id": "write_000",
 "stage_type": "db2",
 "node_class": "connector",
 "properties": {
 "connection_id": "aa3abc5f-15b8-4867-a506-ae5f0cbba3a5",
 "write_mode": "insert",
 "schema_name": "TM_DS_USER_1",
 "table_name": "AgenticTargetTable1",
 "table_action": "replace"
 }
}
```

Both paths converge on the same resolved values:

| Source | Value |
|------------------------------------------|--------------------------------|
| connector reference row where SDK class / map name is `db2` | label: `"IBM Db2"` |
| `namedTable.0` | `"TM_DS_USER_1"` |
| `namedTable.1` | `"AgenticTargetTable1"` |
| Db2 write_mode switch[WRITE_OP_INSERT] | `"insert"` |
| Db2 write default | `table_action = "replace"` |
| connector reference common SDK properties | `schema_name`/`table_name`/`write_mode`/`table_action` all keep their names |

Emit:

```python
connection_write_000 = cast(Connection, project.connections.get(
 connection_id='aa3abc5f-15b8-4867-a506-ae5f0cbba3a5'))
write_000 = flow.add_stage("IBM Db2", "write_000")
write_000.use_connection(connection_write_000)
write_000.configuration.write_mode = 'insert'
write_000.configuration.schema_name = 'TM_DS_USER_1'
write_000.configuration.table_name = 'AgenticTargetTable1'
write_000.configuration.table_action = 'replace'
```

---

## Resolution algorithm (read or write)

```
1. From the substrait rel:
 - connectionId ← advancedExtension.optimization[].connectionId
 - namedTable.names[*] ← rel.namedTable.names
 - (write only) writeOp ← rel.op (the WriteOp enum)

2. From user-supplied connection metadata (or get_connection_info(connectionId)):
 - type ← .type
 - name ← .name (used for the connection object label)
 - props ← .properties (a dict; values like project_id, database, ...)

3. From connector lookup:
 - map_name ← `references/datastage-connector-sdk-reference.md`
 - label ← the matching connector row's "Connector" value

4. From connector-specific behavior:
 - general or SQL read property mapping → for a read
 - write property mapping and write-mode mapping → for a write

5. For each DataStage key in step 4's properties map:
 a. If value template is "namedTable.N" → namedTable.names[N]
 b. If value template is "connection.X" → props[X] (from step 2)
 c. If value template is "nodeInfo.X" → only if upstream supplied it
 d. If value template is a literal → take verbatim
 e. (write only) override "write_mode" → connector-specific write-mode mapping[writeOp]

6. For each DataStage key, look up the SDK attribute name in the matching connector
 reference's "Common SDK Properties" table. If no alias entry is documented, the SDK
 attribute name = the DataStage key. Do not rename the key unless the SDK reference
 or `datastage_property_lookup` explicitly gives a different SDK attribute name.

7. Emit:
 <stage_var>.configuration.<sdk_attr> = <resolved_value>
```

---

## Failure modes specific to value resolution

1. **`connection.X` template references a property the connection doesn't have.** The
 `metadata.json` entry's `properties` map is empty (`{}`) for many test connections.
 The connector value resolver emits an empty string in that case. **Don't fabricate values** —
 if `connection.project_id` resolves to `""`, emit `''` (and surface to the user that
 the connection metadata is incomplete).

2. **`namedTable.N` out of range.** The substrait `namedTable.names` array is shorter
 than the template expects (e.g. `namedTable.2` referenced for a 2-part name).
 Surface to the user — don't guess.

3. **`nodeInfo.sqlStatement` not present.** Only set when a SQL-fold rule fired
 upstream. If the connector's `defaultMode` is `null` and there's no SQL statement,
 fall through to general mode. If `defaultMode` is `"general"`, you're fine.

4. **Unknown `WriteOp`** (a value not in the enum's switch). Per most connectors, this
 maps to `"insert"`. BigQuery maps `WRITE_OP_UNSPECIFIED` to `"delete_insert"` instead.
 When in doubt check the connector-specific write-mode mapping.

5. **`table_action` differs from `"replace"`.** The default is always `"replace"` regardless of `WriteOp`. If you're matching a bundled example whose Python has a different value (e.g. `"append"`), defer to the bundled example when diff-checking — the fixture exercised a specific code path.

---

## Quick reference — connector-specific surprises

| Connector | Surprise |
|------------|-------------------------------------------------------------------------|
| BigQuery | `schema_name` aliases to SDK `dataset_name`. `WRITE_OP_INSERT` → `"insert_only"`, not `"insert"`. `WRITE_OP_UNSPECIFIED` → `"delete_insert"`. Needs `connection.project_id` for `database_name`. |
| Snowflake | Often needs `connection.database` for `database_name`. Quotes table names with `"` (per `quoting` block). |
| Db2 | No `database_name` (only `schema_name` + `table_name`). All write modes default to `"insert"` except DELETE/UPDATE → `"update"` and CTAS → `"merge"`. |
| ODBC / JDBC| `schema_name` is often empty when the connection's metadata is generic — emit `''`, don't guess. |
| Redshift | Connection type `"redshift"` maps to connector map name `amazon_redshift`; see the matching row in `references/datastage-connector-sdk-reference.md`. |
| Dashdb | Connection type `"dashdb"` maps to connector map name `db2warehouse`; see the Db2 Warehouse connector reference. |

When in doubt: resolve the connector in `references/datastage-connector-sdk-reference.md` and ask for missing connection metadata instead of inventing properties. After the alias rename, each DataStage key becomes one `<stage>.configuration.<sdk_attr> = <value>` line in Python.
