---
name: di-agent-flow-pushdown-optimizer
description: >
  Analyze an existing DataStage flow and rewrite it as a full SQL
  pushdown flow. Use when the user says "optimize flow", "convert to
  pushdown", "rewrite as pushdown", or provides a DataStage flow ID and
  asks for SQL optimization or pushdown conversion.
  Use this skill — not di-agent-query-optimization — when the input is
  an existing DataStage flow (flow_id or flow_name), not raw SQL.
  Trigger on: "optimize flow", "rewrite as pushdown", "convert to
  pushdown", "flow to pushdown", "optimize this flow", "pushdown
  optimization", "convert flow to pushdown".
---

# DataStage Flow Pushdown Optimizer

Analyze a DataStage flow and rewrite it as a **Full Pushdown flow** —
all computation moves inside the database engine as a single SQL
statement, leaving exactly 2 stages: one connector + one sink.

**Scope:** Both **Target Full Pushdown (ELT)** and **Source Full
Pushdown (TEL)** are supported, subject to the following constraints:

| Mode | Condition |
|---|---|
| **Target Full Pushdown (ELT)** | All connectors (source + target) share the same connection; flow has a write target |
| **Source Full Pushdown (TEL)** | All source connectors share the same connection; sink is Sequential File, PxCopy, or PxPeek (no write target DB connector) |

**Not supported:**
- Partial pushdown (any intermediate stage not convertible to SQL)
- TEL with a different-connection DB as sink (sink config cannot be
  preserved through the pipeline) — future work

If the flow does not meet either mode's conditions, stop and report the
reason clearly; do not attempt any partial conversion.

## Inputs

Ask for these if not already provided:
- `flow_id` or `flow_name` — the DataStage flow to analyze
- `project_id` or `project_name` — the watsonx project

If names are given instead of IDs, resolve them first:
- `project_name` → `get_projects(name=<name>)` to get `project_id`
- `flow_name` → `list_datastage_flows(entity_name=<name>, project_id=...)` to get `flow_id`

## Workflow

### 1. Retrieve the flow
Call `retrieve_datastage_flow_code`. Read the full `sdk_code` and extract:

- **All connector stages** — identify every `flow.add_stage(...)` call whose type is a
  database connector (not Sequential File, Filter, Sort, Aggregator, etc.). For each:
  - **Connection name** — the string passed to `project.create_connection(name=...)` or
    `project.connections.get(name=...)` used by that stage.
  - **Connection ID** — call `list_connections(project_id=<project_id>, entity_name=<connection_name>)`
    and record the returned `id` UUID. Resolve every connector's connection separately;
    do not assume all connectors share the same connection until Step 2 verifies it.
- **Local parameters** — any `flow.add_local_parameter(...)` calls; record name and default value.

The resolved connection UUIDs per connector are the inputs to the same-connection check
in Step 2. The single canonical `connection_id` used in Step 5 is only determined after
Step 2 confirms all connectors share the same UUID.

### 2. Classify pushdown eligibility

First verify the connector type is in the ELT-supported list. Only the following connectors
support full pushdown (ELT run mode):
Amazon RDS for PostgreSQL, Amazon Redshift, Google BigQuery, IBM Cloud Databases for PostgreSQL,
IBM Db2, IBM Db2 for DataStage, IBM Db2 on Cloud, IBM Db2 Warehouse, Oracle, PostgreSQL,
Snowflake, Teradata, Teradata database for DataStage, watsonx.data.

Cross-database and cross-schema operations are not supported in either source or target full
pushdown — all tables referenced in the flow must belong to the same database and schema.

Classify the flow into one of the supported modes. Apply in order
(first match wins):

| Priority | Mode | Condition |
|---|---|---|
| 1 | **Target Full Pushdown (ELT)** | All connectors (source + target) from the supported list, same connection, same database/schema, all intermediate stages convertible to SQL, flow has a write target connector |
| 2 | **Source Full Pushdown (TEL)** | All source connectors from the supported list, same connection, same database/schema, all intermediate stages convertible to SQL, sink is Sequential File / PxCopy / PxPeek (no write target DB connector) |
| 3 | **Not supported** | Any other case — stop and report |

Common preconditions for both modes (check first):

| Condition | Check |
|---|---|
| All connectors are from the supported list | See connector list above |
| All connectors share the **same connection** | Same connection UUID |
| All tables are in the same database/schema | No cross-database or cross-schema reads/writes |
| All intermediate stages have a SQL equivalent | See stage mapping in Step 3 |

If **any** condition fails, stop immediately and report:

| Failure | Report |
|---|---|
| Connector not in supported list | "Connector `<type>` does not support ELT run mode." |
| Connectors on different connections | "Connectors use different connections — Full Pushdown requires the same connection." |
| Cross-database or cross-schema | "Cross-database/schema operations are not supported in pushdown mode." |
| Any intermediate stage not convertible to SQL | "Stage `<name>` (`<type>`) cannot be translated to SQL — Partial Pushdown is not supported. Blocking stage(s): `<list>`." |
| TEL with a different-connection DB sink | "Sink is a DB connector on a different connection — TEL with a different-connection DB sink is not supported yet." |

### 3. Translate stages to SQL

Use the stage-to-SQL mapping in
[`references/stage-to-sql-mapping.md`](references/stage-to-sql-mapping.md)
to translate each DataStage stage. That file covers: supported stage translations,
target connector write-mode prepend (`table_action` / `write_mode`), stages that
block full pushdown, Mixed-mode stage limitations, and the runtime parameter
preservation rule.

### 4. Present SQL and confirm

Show the user:
1. Pushdown classification and reasoning
2. Each stage → SQL mapping
3. Any items requiring manual verification (case sensitivity, dialect-specific functions)
4. The complete optimized SQL

The "complete optimized SQL" for **Target Full Pushdown** is the full
workload block — i.e. the TRUNCATE/DELETE/CREATE prepend (from the
`table_action` table above) followed by the `INSERT … SELECT`. Do not
add a trailing SELECT here; the observability SELECT is appended
temporarily in Step 5 only when passing the SQL to `di-agent-query-optimization`.

For **Source Full Pushdown**, the complete SQL is just the single
workload `SELECT`.

**Wait for explicit user confirmation before creating the flow.**

### 5. Create the optimized flow

#### Observability SELECT rule (applies to BOTH paths below)

For **Target Full Pushdown**, the observability SELECT **must** be:

```sql
SELECT <col1>, <col2>, … FROM <target_table>
```

Where `<col1>, <col2>, …` are exactly the output columns of the target connector
(taken from the output link schema in Step 3), and `<target_table>` is the
fully-qualified target table name.

**Hard constraints — never violate:**
- **No aggregation functions** (`COUNT`, `SUM`, `AVG`, `MIN`, `MAX`, etc.) —
  the target table already holds aggregated data; re-aggregating produces wrong results
  (e.g. `COUNT(*) AS int2` over a pre-aggregated table returns `1` per row, not the
  original counts)
- **No `GROUP BY`**
- **No subqueries, CTEs, or JOINs**
- **No reuse of any expression from the workload `INSERT … SELECT`** — derive the
  observability SELECT only from the target table's column list, never by copying or
  adapting the workload SELECT
- The observability SELECT is read-only; it must not modify any data

#### Primary path: delegate to `di-agent-query-optimization` + `di-agent-flow-substrait-datastage`

**This is the mandatory first attempt. Do not skip it. Do not use any other tool
(e.g. `substrait_to_flow_code`, `compile_substrait_dsl`, or direct SDK generation)
as a shortcut before trying this path.**

Execute in strict order:

**Step 5a — Invoke `di-agent-query-optimization`** (Path 2 — SQL text).
`di-agent-query-optimization` is a **skill**, not an MCP tool. If no MCP tool with
that name exists, that is expected — do not treat it as unavailability and do not use
it as a reason to enter the fallback path. Activate the skill and execute its workflow
inline to produce an optimized pushdown Substrait plan. The primary path is considered
attempted only after a Substrait plan has been produced and handed to Step 5b, or after
the skill workflow returns an explicit failure (`optimized: false` or an error).
Proceeding directly to SDK code generation without producing a plan does **not** count
as attempting the primary path.

Pass to the skill:
- the canonical `connection_id` confirmed in Step 2
- the SQL constructed as follows:
  - **Target Full Pushdown** — append the observability SELECT (per the rule above)
    as a trailing statement after the workload block from Step 4:
    ```
    TRUNCATE/DELETE ...;
    INSERT INTO target ...;
    SELECT <output_cols> FROM <target_table>;   ← appended trailing SELECT
    ```
    The optimizer's script-trailing classifier lifts this SELECT as the observability
    SELECT automatically — no `hints` needed.
  - **Source Full Pushdown** — pass the workload SELECT from Step 4 as-is.
- the suggested optimized flow name derived from the original flow name per the rule below,
  and local parameter defaults from Step 1 (when available)

**Optimized flow naming rule:**
1. Always create a new flow — never overwrite the original flow or ask the user.
2. The new flow name is `<original_flow_name>_optimized`.
3. If `<original_flow_name>_optimized` already exists, try `<original_flow_name>_optimized_1`,
   then `<original_flow_name>_optimized_2`, and so on until a free name is found.
4. Pass the resolved name as `flow_metadata.suggested_flow_name` to `di-agent-flow-substrait-datastage`.

**Step 5b — Pass the resulting Substrait plan to `di-agent-flow-substrait-datastage`**
to generate and call `create_datastage_flow`.
`di-agent-flow-substrait-datastage` is also a **skill**, not an MCP tool. If no MCP
tool with that name exists, that is expected — activate the skill and execute its
workflow inline.

The primary path has **failed** — and only then may you proceed to the fallback — when
any of the following occurs:
- `di-agent-query-optimization` returns `optimized: false` or an explicit error
- `di-agent-flow-substrait-datastage` returns an error that cannot be fixed by correcting
  the SDK code (e.g. a skill or tool is unavailable)
- `create_datastage_flow` returns an SDK-code error that persists after one corrective retry

A tool call returning a retryable error (e.g. a fixable SDK-code validation error) is
**not** a primary-path failure — fix the error and retry within the same path.

#### Fallback path: generate SDK code directly

Only enter this path after the primary path has failed per the definition above.
Do not enter it preemptively, speculatively, or because an intermediate tool
(e.g. `substrait_to_flow_code`) that is not part of the primary path returned an error.
In the fallback path, do not invoke `substrait_to_flow_code` or `compile_substrait_dsl`.

Generate the `sdk_code` and call `create_datastage_flow` directly. Apply the same
**Optimized flow naming rule** as the primary path (always create new, `_optimized` suffix,
then `_optimized_1`, `_optimized_2`, … if needed). When generating SDK code, apply these rules:

- `enable_before_sql` = the workload block only (TRUNCATE/DELETE + INSERT) — no SELECT
- `select_statement` = the observability SELECT per the rule above — a plain
  `SELECT <output_cols> FROM <target_table>` reading the target table post-write
- For Source Full Pushdown: `select_statement` = the workload SELECT; no `enable_before_sql`

### 6. Summarize

Report: flow link, optimized flow name, pushdown mode (Target Full Pushdown or Source Full
Pushdown), stage count (original → 2), parameters preserved, and (for target pushdown) the
observability SELECT used. Do not report the original flow's execution mode. Note any items
the user should verify before running.

## Scope and limits

- **Target Full Pushdown (ELT)** — all connectors share the same
  connection; flow has a write target; entire logic becomes
  `INSERT … SELECT` inside the target database.
- **Source Full Pushdown (TEL)** — all source connectors share the
  same connection; sink is Sequential File, PxCopy, or PxPeek;
  entire logic becomes a single `SELECT`; sink is automatically
  rebuilt by `di-agent-flow-substrait-datastage` (original sink
  configuration is not preserved).
- **TEL with a different-connection DB sink is not supported** —
  the sink connector configuration cannot be preserved through the
  current pipeline. Future work.
- **Partial Pushdown is not supported** — if any intermediate stage
  cannot be translated to SQL, the skill stops and reports the
  blocking stage(s). Future work.
- `di-agent-query-optimization` is only invoked after Step 3 confirms
  that **all** stages have been successfully translated into a single
  complete SQL statement. It is never called for partial conversions.
