---
name: di-agent-query-optimization
description: >
  Optimize a workload for DataStage SQL pushdown. Activate when the
  user's request contains "pushdown", "optimize", "convert to flow", or
  similar.
  Accepts four input forms — natural language, SQL statements (text), a
  SQL file, or a custom-format file handled by a di-adapter-* plug-in —
  routes each to its pre-processing path, probes pushdown capability,
  then emits the optimized Substrait plan that
  di-agent-flow-substrait-datastage renders into a DataStage flow.
  Supports both source full pushdown and target full pushdown. Partial
  pushdown is recognized but not generated.
  Trigger on: "use pushdown", "pushdown this", "push down to database",
  "optimize for pushdown", "full pushdown", "source pushdown",
  "target pushdown", "pushdown plan", "convert script to flow",
  "pushdown sql", "pushdown ctl", "convert query to pushdown flow".
---

# Optimize a Workload for DataStage SQL Pushdown

The entry point for any "use pushdown" request. Routes the user's
workload through one of four paths, probes whether it can run as full
pushdown (source or target), and emits the optimized Substrait plan that
`di-agent-flow-substrait-datastage` renders into a DataStage flow.

```
              user input
                  │
                  ▼
      ┌────────────────────────┐
      │ this skill — dispatch  │
      │   by input type        │
      └───────────┬────────────┘
                  │
      ┌───────────┼────────────┬──────────────┬──────────────────┐
      ▼           ▼            ▼              ▼                  ▼
   Natural    SQL text     SQL file      Custom-format       (re-entry:
   language   in prompt    path           file (e.g. .ctl)    raw Substrait
                                                              or workload JSON)
      │           │            │              │                  │
      ▼           │            │              ▼                  │
  di-agent-       │            │         di-adapter-<source>     │
  query-          │            │              │                  │
  substrait       │            │       workload JSON             │
      │           │            │       (pushdown-workload-v1)    │
      ▼           │            │              │                  │
  raw Substrait   │            │              │                  │
      │           ▼            ▼              ▼                  ▼
      │       SQL-text probe ◄──────────────  │     (relation-tree probe for Substrait;
      ▼                                       │      SQL-text probe for workload JSON)
  relation-tree probe                         │
      │                                       │
      └─────────────────┬─────────────────────┘
                        │
                        ▼
        classify (source / target / partial / not)
                        │
                        ▼
           emit optimized Substrait plan
                        │
                        ▼
          di-agent-flow-substrait-datastage
                        │
                        ▼
                  DataStage flow
```

## Inputs and dispatch paths

| # | Input | Detection | Path |
|---|---|---|---|
| 1 | **Natural language** | a natural-language description of the workload; no embedded SQL or file path | Invoke `di-agent-query-substrait` to produce a raw Substrait plan, then run the **relation-tree probe** on that plan. |
| 2 | **SQL statements (text)** | not JSON, looks like SQL; may be a multi-statement script pasted into the prompt | Run the **SQL-text probe** directly on the pasted text. |
| 3 | **SQL file path** | the user gives a path to a `.sql` file (or any file they explicitly say to treat as SQL) | Read the file's contents, run the **SQL-text probe** directly on them. |
| 4 | **Custom-format file** | the user gives a path whose extension matches an installed `di-adapter-*` plug-in's `accepts` field (e.g. `.ctl`) | Invoke the matching adapter to produce a **workload JSON** (`pushdown-workload-v1`), then run the **SQL-text probe** on the workload's `rawSqlStatement`. The adapter's `hints` and `flow_metadata` are honored downstream. |

Two re-entry inputs (not user-facing — produced by paths above or by
prior skill steps):

- **Raw Substrait plan** — produced by path 1 (`di-agent-query-substrait`).
  Continue with the relation-tree probe.
- **Workload JSON** — produced by path 4 (a `di-adapter-*` plug-in).
  Continue with the SQL-text probe on `rawSqlStatement`.

Recommended metadata (any path):

- `target_dialect` (e.g. `snowflake`, `db2`, `databricks`, `postgresql`);
- `connection_id` or `connection_name` proving all reads/writes resolve
  to one DB;
- optional flow defaults: flow name, parameter defaults, parameter
  bindings, tags, output file.

## Workflow

1. **Identify the input type** per the dispatch table above.
2. **Run the matching pre-processing**:
   - Path 1 → invoke `di-agent-query-substrait`, receive raw Substrait plan.
   - Path 2 → use the pasted text as the workload SQL string.
   - Path 3 → read the file, use its contents as the workload SQL string.
   - Path 4 → invoke the adapter, receive workload JSON.
3. **Resolve placeholders, tables, and connection.** Run the section
   below (skipped for path 1, which already carries `connection_id`).
   Asset lookup uses bare table names so it works even when the SQL
   has unresolved `${VAR}` placeholders in the qualifier; resolution
   of those placeholders falls out as a byproduct of unique-candidate
   matching. Same-database pushdown must be explicit by the end of
   this step; if neither the input, the user, nor asset/connection
   discovery resolves all reads/writes to one connection, stop and ask.
4. **Run the probe**:
   - Relation-tree probe for raw Substrait (path 1).
   - SQL-text probe for SQL text / SQL file / workload JSON (paths 2/3/4).
5. **Classify** with the rules below. Stop with a specific reason for
   partial pushdown, mixed connections, non-SQL operations, or missing
   metadata.
6. **For target pushdown**, choose the observability `sqlStatement` and
   its schema using the precedence below.
7. **Build the optimized Substrait plan** using the emission rules in
   this skill and the byte-level schema in
   [`references/adapter-contract.md`](references/adapter-contract.md),
   then **run the pre-return validation** below.
8. **Hand off** to `di-agent-flow-substrait-datastage`. Do not generate
   DataStage Python here.

## Probes

**Relation-tree probe** (path 1 — NL via `di-agent-query-substrait`):

Step A — **Parse and inspect the raw plan.** Validate that the input is
JSON containing a top-level `relations` array. Collect:

- root relation kind: `root`, `write`, `fetch`, or a direct relation;
- read table paths from `read.namedTable.names`;
- write table paths from `write.namedTable.names`;
- connection IDs from `advancedExtension` / `advancedExtensions` /
  DataStage extension metadata when present;
- output schema from root `names` and the read/write `baseSchema`.

Step B — **Convert to SQL** by calling
`di-agent-query-sql` / `substrait_to_sql`:

```python
substrait_to_sql(
    substrait_json="<original_substrait_json_string>",
    target_dialect="<target_dialect>",
    preprocessed=false
)
```

Pass the raw plan, not a rewritten one. If conversion fails, stop and
return the conversion error with the original plan.

Step C — **Decide full-pushdown eligibility.** Treat the plan as full
pushdown only when **all three** are true:

1. `substrait_to_sql` succeeds and returns non-empty SQL (single
   statement or block) that preserves every relation rel from the
   original plan. **No relation, operation, or boundary may be dropped,
   skipped, approximated, or left for DataStage.**
2. Every read rel reads from the same connector / database connection.
   If the plan has a write target, it must also be in that same
   connection.
3. Every operation in the source plan can execute inside that connector
   as SQL — no DataStage-only stages, external files, datasets, engine
   operations, or partial-flow boundaries.

Step D — **Classify source vs. target:**

- Root is a `Write` relation → `target_full_pushdown`. The materialized
  SQL becomes `beforeSqlStatement`; the observability `sqlStatement` is
  chosen by the precedence below.
- Trailing statement of the materialized SQL is a `SELECT` returning
  output rows → `source_full_pushdown`. That `SELECT` becomes
  `sqlStatement`.
- Multi-statement blocks where writes are side-effects and the trailing
  `SELECT` returns output rows → `source_full_pushdown` (writes execute
  before the trailing SELECT supplies the sink rows).
- Only a subgraph converts, relation rels are lost, or reads span
  different connectors → `partial_pushdown_unsupported` (stop).

Source full pushdown is the path the original optimizer supported.
Target full pushdown is the new extension: NL queries describing a
write/update/copy intent now produce a target-pushdown flow instead of
being rejected as write-only.

**SQL-text probe** (paths 2/3/4 — SQL text, SQL file, or adapter
workload JSON):

Split the workload SQL on top-level `;` (preserving `;` inside string
literals and `$$...$$` blocks), detect each statement's kind by leading
keyword, and collect best-effort read/write tables.

Verify all statements can run in one connector context: one dialect,
one resolved connection, and any session/transaction statements (`USE`,
`SET`, `COMMIT`, `ROLLBACK`) valid within that session. If not, stop as
`partial_pushdown_unsupported`.

The probe produces the same downstream artifacts as the relation-tree
probe (workload statements, trailing-statement signal, reads/writes for
the same-connection check).

## Resolving placeholders, tables, and connection

Paths 2/3/4 supply a workload SQL but no guaranteed `connection_id`.
When the user or input supplies the connection, resolve that connection
directly and skip data-asset discovery. Otherwise, the optimizer
discovers each referenced table's connection (and infers parameter
values for placeholders that appear inside table references) by
querying the project's asset and connection APIs.

For SQL text / SQL files, project asset discovery is mandatory unless
the user or workload JSON supplied an explicit connection. Do not infer
connection, dialect, schema, catalog, or column types from local files,
examples, prior flows, naming conventions, or previous conversation
context.

For **path 1** (NL → raw Substrait), the input plan already carries
`connection_id` on its read nodes. Carry it forward; no asset lookup
is needed.

### Skip data-asset discovery when…

- The input is **workload JSON** with a UUID in `connection_id`.
- The user **explicitly supplied** `connection_id` (or
  `connection_name`, in which case look it up once with
  `list_connections(entity_name=…)` and inspect the connection asset)
  in the prompt.
- The input is **raw Substrait** (path 1).

Otherwise, run the sequence below.

### Inputs from the SQL-text probe

The probe returns `reads` and `writes` as raw, possibly qualified
table references — e.g. `${SCHEMA}_DB.target_table_1`. For each
reference, extract:

- **Bare name** — the trailing identifier (`target_table_1`). This is
  what gets passed to `list_data_assets`; it works even when the
  qualifier contains unresolved `${VAR}` placeholders.
- **Qualifier pattern** — the leading identifier(s) with placeholders
  intact (`${SCHEMA}_DB`, or `${CATALOG}.${SCHEMA}`). This is matched
  later against candidate assets to infer placeholder values.
- **Placeholders in qualifier** — the `${VAR}` names that need
  resolution to identify the candidate (`{SCHEMA}`). For dialects or
  adapters that use non-`${VAR}` syntax, use the detected parameter's
  normalized name from the input `parameters` array (or
  `flow_metadata.parameter_bindings[NAME].source_syntax` when present).

**DataStage `#…#` syntax in table references** — when a table
reference contains DataStage runtime placeholders (`#<PS>.<PARAM>#` or
`#<NAME>#`), treat each `#…#` span as a single token:

- Parse by scanning for `#…#` boundaries first; split on `.` only at
  separators that lie **outside** any `#…#` span.
- Example: `#PARAM_SET.CATALOG#.#PARAM_SET.SCHEMA#.payments` →
  bare name `payments`, qualifier `#PARAM_SET.CATALOG#.#PARAM_SET.SCHEMA#`,
  placeholders `PARAM_SET.CATALOG` and `PARAM_SET.SCHEMA` (both
  parameter-set `PARAM_SET`). Do **not** yield catalog `#PARAM_SET`,
  schema `CATALOG#`.
- A `#…#` placeholder in a qualifier means the physical catalog or
  schema is unknown at parse time. Skip schema pattern-matching for
  that part and apply connection-only candidate selection (see
  *Same-connection short-circuit* below).

Placeholders that appear only in column references, value literals, or
`WHERE` predicates (e.g. `WHERE load_dt = '${DATA_DT}'`) do not need
resolution for asset discovery and are left untouched.

### Per-table discovery

1. **Find candidates.** Call
   `list_data_assets(project_id=<project>, entity_name="<bare name>")`.
   Multiple matches are common (same table name in different schemas).
2. **Batch-inspect candidates.** Across all tables, collect candidate
   asset IDs and call
   `inspect_project_asset(project_id=<project>, asset_type="data_asset", asset_ids=[<all candidate ids>])`
   **once** rather than per-table. Each returned record provides
   `schema_name`, `table_name`, columns, and (when present)
   `connection_name` + `datasource_type`.
3. **Match candidates to the SQL qualifier.** For each table:
   - If the SQL uses an **unqualified** name and exactly one candidate
     has connection metadata, that candidate wins.
   - If the SQL uses a qualifier with **no placeholders**, pick the
     candidate whose `schema_name` matches the qualifier (and whose
     connection's `database`/`catalog` property matches when the SQL
     used a 3-part name).
     If the candidate asset reports a `catalog_name` and the workload
     SQL omitted it, preserve that catalog in the emitted plan metadata
     for downstream flow generation.
   - If the SQL uses a qualifier with **`${VAR}`-style placeholders**,
     match the pattern against each candidate's `schema_name`. Example:
     pattern `${SCHEMA}_DB`, candidate `schema_name = "PROD_DB"` →
     infer `SCHEMA = "PROD"` and accept. If exactly one candidate fits,
     add the inferred value to `flow_metadata.parameter_defaults` with
     a `hints.notes` entry. If multiple candidates fit with conflicting
     values, ask the user.
   - If the SQL uses a qualifier with **`#…#` placeholders**, the
     physical catalog/schema is unresolvable from text; skip pattern
     matching and apply connection-only selection per the
     *Same-connection short-circuit* rule.

### Same-connection short-circuit

After the first table resolves to a `connection_id`, **constrain all
subsequent candidate filtering to that same connection** —
short-circuit by preferring candidates whose `connection_name` matches
the already-resolved one. This avoids expensive cross-connection
discovery work for a workload that the same-connection invariant will
ultimately reject anyway.

### Connection resolution

Per table, the matched candidate provides either:

- A `connection_name` directly → call
  `list_connections(project_id=<project>, entity_name="<connection_name>")`
  to get `connection_id`. Inspect with
  `inspect_project_asset(asset_type="connection")` to confirm
  `datasource_type` and harvest connection properties.
- No connection metadata → call
  `get_asset_relationships(project_id=<project>, assets=[{asset_type:"data_asset", asset_id:<id>}])`
  to find the related connection asset, then inspect it.

Batch the connection inspections too: collect all distinct
`connection_id`s discovered across tables and pass them as one
`inspect_project_asset` call.

### Connection-only fallback (no candidate asset)

If a table reference returns zero matches from `list_data_assets`:

1. If the user supplied `connection_name`, look it up
   (`list_connections(entity_name=…)`) and inspect it. Use this as the
   table's connection. Optionally verify reachability with
   `read_connection_data_preview(connection_id=<id>, resource_path="<schema>/<table>")`.
2. If the user supplied no connection hint, ask:

   > Table `<name>` is not registered as a project data asset.
   > Available project connections: `<list with datasource_type>`.
   > Which connection holds this table?

### Same-connection invariant

After all tables have a resolved `connection_id`:

- All same `connection_id` → proceed; this is the canonical
  `connection_id` for the optimized plan.
- Mixed → stop with `partial_pushdown_unsupported`.
- Any still unresolved → ask the user, listing unresolved tables and
  the resolved ones with their connections:

  > I could not resolve the connection for table(s) `<list>`. Please
  > supply a `connection_name` (or `connection_id`) that contains
  > these tables. Resolved so far: `<list with connection>`.

### Dialect resolution

The `dialect` (`snowflake`, `db2`, `databricks`, `postgresql`, …)
comes from the resolved connection's `datasource_type`, mapped through
the runtime's dialect-mapping reference (the same one
`di-agent-query-sql` uses). An explicit `target_dialect` from the
user always wins.

### What lands in the optimized plan

- `read.advanced_extension.optimization[0].connection_id` — the
  resolved UUID.
- `dialect` — resolved from `datasource_type`.
- `flow_metadata.parameter_defaults[NAME]` — any placeholder values
  the user supplied, the adapter supplied, or the optimizer inferred
  from unique candidate assets. Placeholders that did not need
  resolution (column refs, WHERE values) are left out unless the user
  supplied a default for them separately. These defaults are intended
  for local flow parameters; parameter-set-backed values should use
  `parameter_bindings[NAME].value_set` or runtime overrides.
- `flow_metadata.parameter_bindings[NAME]` — optional normalized
  parameter metadata. Include this whenever the input uses a
  dialect-specific parameter syntax, the user describes local
  parameters or parameter sets in natural language, or a parameter is
  used as an identifier and needs stricter rendering/validation.
- `sqlStatement` and `beforeSqlStatement` — **unchanged**. Customer
  placeholders stay literal in their source syntax; the flow skill
  renders them to DataStage syntax (`#VAR#` or `#PARAMSET.VAR#`) when
  assigning SQL to connector properties. The optimizer never rewrites
  table names to DataStage syntax.

## Classification

Strip terminal `COMMIT` and `ROLLBACK` before finding the trailing
meaningful statement.

DML/write statements: `INSERT`, `INSERT_SELECT`, `UPDATE`, `DELETE`,
`MERGE`, `COPY_INTO`, `CREATE_AS_SELECT`, `TRUNCATE`.

Supported session/transaction statements: `USE`, `SET`, `COMMIT`,
`ROLLBACK`.

| Signal | Decision |
|---|---|
| Zero DML, trailing meaningful statement is `SELECT`, same connection | `source_full_pushdown` |
| One or more DML, trailing meaningful statement is `SELECT`, same connection | `target_full_pushdown`; lift the trailing SELECT as the observability candidate and remove it from `beforeSqlStatement` |
| One or more DML, no trailing SELECT, same connection | `target_full_pushdown`; choose observability SELECT per the precedence below |
| Relation-tree probe: root is a Write relation | `target_full_pushdown` |
| Multiple connector sessions, mixed connections, or only a subgraph fits SQL | `partial_pushdown_unsupported` (stop) |
| Not a SQL pushdown candidate at all | `not_full_pushdown` (stop) |

`hints.force_mode` (from a workload-JSON adapter input) resolves
source/target ambiguity but cannot upgrade a non-pushdown workload to a
pushdown workload.

Same-database eligibility must be **explicit**: a `connection_id` is
set, all reads/writes resolve to one connection, or the user supplies
it. If connection metadata is absent, stop and report:

> Full pushdown is not confirmed because source and target connection metadata is missing.

When classification stops with `partial_pushdown_unsupported` or
`not_full_pushdown`, return:

```json
{
  "optimized": false,
  "mode": "<partial_pushdown_unsupported|not_full_pushdown>",
  "reason": "<specific reason>",
  "message": "Partial pushdown is not supported yet by this skill.",
  "input": "<original input>"
}
```

Use `partial_pushdown_unsupported` when a subgraph could be converted to
SQL but the complete plan cannot, or when reads span different
connectors. Use `not_full_pushdown` only when the plan is not a SQL
pushdown candidate at all.

## Target observability SELECT

For `target_full_pushdown`, choose `sqlStatement` in this order:

1. **Adapter-supplied** — `hints.observability_select` and
   `hints.observability_schema` both set on a workload JSON input.
2. **Script-trailing** — a SELECT lifted from the workload by the
   classifier.
3. **LLM-derived** — the optimizer asks the LLM to inspect
   `beforeSqlStatement` and emit one read-only `SELECT` plus `{names,
   types}`.
4. **Fallback** — `SELECT 1 AS DUMMY_COL` with one nullable `i32`
   column.

Validate the chosen SELECT before accepting it:

- exactly one read-only statement;
- references only objects in the same connection;
- output aliases match `root.names` after sanitization;
- schema `names` / `types` are positional and equal length.

If a higher-precedence source fails validation, drop to the next source
and record the reason in `hints.notes`.

## Optimized pushdown plan — emission rules

The byte-level schema and invariants live in
[`references/adapter-contract.md`](references/adapter-contract.md). The
rules below cover only optimizer-side behaviors not in the contract.

### Pass-through and parameter rules

- pass `parameters` through — the list of normalized parameter names
  found in the workload SQL;
- pass `flow_metadata.parameter_defaults` and `runtime_hints` through
  from the input; drop any `parameter_defaults` entry whose key does
  not appear in `parameters`, and record the dropped key in
  `hints.notes`;
- pass `flow_metadata.parameter_bindings` through when present, after
  validating that every key appears in `parameters`;
- when the user describes parameters in natural language (for example
  "use local parameter SCHEMA for schema name" or "use parameter set
  ENV_PARAMS for TARGET_DB"), convert that intent into
  `flow_metadata.parameter_bindings`; this skill is the control layer
  that merges user intent, adapter metadata, and inferred defaults;
- preserve customer placeholders literally in their source syntax
  (`${VAR}`, `&VAR`, `:VAR`, etc.). The flow skill renders them to
  DataStage runtime syntax. Do not rewrite placeholders to `#VAR#`
  or `#PS.VAR#` here — **except** when the input SQL already contains
  `#…#` syntax (e.g. from an adapter that pre-rendered DataStage
  placeholders): preserve those tokens as-is and set
  `source_syntax = "#<PS>.<PARAM>#"` (or `"#<NAME>#"`) in the binding;
- resolve `flow_metadata.suggested_flow_name` per the 5-step chain
  documented in the contract.

`flow_metadata.parameter_bindings` is keyed by normalized parameter
name. Each value may contain:

```json
{
  "source_syntax": "${TARGET_DB}",
  "binding": "local | parameter_set",
  "type": "string | int64 | sfloat | date | timestamp | encrypted | ...",
  "usage": "identifier | literal | unknown",
  "description": "Target database qualifier",
  "parameter_set_name": "ENV_PARAMS",
  "parameter_name": "TARGET_DB",
  "value_set": "prod"
}
```

Use `binding="local"` by default. Use `binding="parameter_set"` only
when the adapter supplied it or the user explicitly requested a
parameter set. `source_syntax` is optional for `${NAME}` placeholders
and recommended for other dialect-specific forms. The flow skill has a
bounded fallback registry for known forms (`${NAME}`, SQL*Plus-style
`&NAME`/`&&NAME`, and named-bind `:NAME`), but explicit
`source_syntax` is preferred whenever an adapter or this skill can
identify it. For positional parameters such as `?`, require the adapter
or user to provide stable names and source spans/rewrite metadata; do
not invent names from position alone.

Local parameters are the default for generated one-off flows and for
natural-language requests such as "make schema/date/customer_id a
parameter." Parameter sets are used only when the user names a
parameter set, the adapter supplies a parameter-set binding, or a
known customer convention maps the parameter to an existing managed set.
Do not auto-promote enterprise-looking names such as `SRC_DBE`,
`TARGET_DB`, `RUN_DATE`, or `LOAD_DATE` to parameter sets without that
explicit signal.

### Output schema derivation (path 1 — from raw Substrait)

When emitting from a raw Substrait input:

- prefer root `names` for output column names, then apply the
  DataStage-safe alias check below;
- prefer the final relation's `baseSchema.struct.types` for output
  types — carry compatible Substrait type objects across as-is;
- ensure canonical output names are used consistently in the SQL `AS`
  aliases, `relations[0].root.names`, and `read.baseSchema.names`;
- if the final output schema cannot be found, fall back to a
  conservative **single-column row-count schema** (`names: ["row_count"]`,
  `types: [{i64: {nullability: NULLABILITY_NULLABLE}}]`) only when the
  trailing SELECT is a row-count expression (e.g. `SELECT COUNT(*) ...`).
  Otherwise stop and ask the user for the expected output schema. Do
  not invent a schema in other cases.

### Output schema derivation (paths 2/3/4 — from SQL text / workload JSON)

- for `source_full_pushdown`, derive `root.names` and types from the
  trailing `SELECT`'s output columns;
- for `target_full_pushdown`, derive from the chosen observability
  `sqlStatement` and (when supplied) `hints.observability_schema`.

### DataStage-safe alias sanitization

Before embedding SQL in the optimized plan, check the trailing `SELECT`
aliases. If an alias is already DataStage-safe and unique, keep it
unchanged. If an alias is missing, unsafe, or collides after
sanitization, repair only the final output alias and the corresponding
output schema name:

1. Start from the original root names / trailing SELECT aliases in
   output order.
2. Replace every character outside `[a-zA-Z0-9_]` with `_`.
3. If the result does not start with a letter, prepend `col_`.
4. If the result is empty or null, use `col`.
5. Deduplicate within the output list using `_1`, `_2`, ... suffixes.

The checked/repaired names are the canonical output names for the
optimized plan. The SQL trailing `SELECT` must alias every output
expression with exactly the matching canonical name (`AS <name>`), and
both `root.names` and `read.baseSchema.names` must use those same names
in the same order. Do not modify the SQL converter output if the
aliases already satisfy the rule. If repair is needed, repair only
final SELECT aliases; do not rename physical source table or source
column identifiers.

### Connection ID

Carry `connection_id` over from the input (raw Substrait read nodes, or
the workload JSON's `connection_id`). This is the canonical DataStage
convention; do not invent a UUID and do not omit the field.

## Pre-return validation

Before returning the optimized plan, verify every item below. These are
the load-bearing invariants downstream consumers
(`di-agent-flow-substrait-datastage` and any other tooling reading the
plan) depend on:

- exactly one top-level relation, containing `root.input.read`;
- `read.common.advancedExtension.enhancement.nodeKind` is exactly
  `source_full_pushdown_read` or `target_full_pushdown_read`;
- `enhancement.sqlStatement` is non-empty;
- for `target_full_pushdown_read`: `enhancement.beforeSqlStatement` is
  non-empty;
- `read.advanced_extension.optimization[0].connection_id` is present
  (UUID carried over from the input);
- `root.names` length equals `baseSchema.names` length equals
  `baseSchema.struct.types` length, matched by position;
- every trailing SELECT output expression has an `AS` alias matching
  the canonical name at the same position in `root.names`, after the
  DataStage-safe sanitization in the emission rules;
- `flow_metadata.suggested_flow_name` is set and matches
  `^[a-zA-Z][a-zA-Z0-9_]{0,59}$`;
- every key in `flow_metadata.parameter_defaults` corresponds to a
  normalized name in `enhancement.parameters`;
- every key in `flow_metadata.parameter_bindings` corresponds to a
  normalized name in `enhancement.parameters`; every
  `parameter_set` binding has `parameter_set_name` and
  `parameter_name`.

If any item fails, do not return the plan; report which invariant
failed and stop.

## Classify-only mode

Triggered by `classify_only=true`, "classify only", "dry run", or "do
not generate flow yet". Run dispatch, probing, classification, and
target observability selection, then stop before emitting the optimized
plan. Return a JSON report containing:

- `mode`, `confidence`, `dialect`, resolved connection;
- input/output tables;
- `parameters`;
- `observability_select`, `observability_schema`, `observability_source`
  ∈ `{adapter, script_trailing, llm, fallback, n_a}`,
  `observability_lifted_from_workload` boolean;
- resolved `flow_metadata` (`suggested_flow_name`,
  `suggested_flow_name_source`, `parameter_defaults`,
  `parameter_bindings`, `runtime_hints`);
- `issues`, `notes`.

The bulk driver (`di-agent-pushdown-batch`) uses classify-only to fill
its manifest before flow generation.

## Output

For the normal workflow, return:

````markdown
### Optimization Result

- Mode: source_full_pushdown | target_full_pushdown
- Dialect: <dialect>
- Connection ID: <uuid>
- Observability SELECT source: adapter | script_trailing | llm | fallback (target only)

### Workload SQL (target only)

```sql
<beforeSqlStatement>
```

### Result SELECT

```sql
<sqlStatement>
```

### Optimized pushdown Substrait plan

```json
<plan>
```
````

## Scope and limits

This skill is purely a plan rewriter. It does not:

- generate DataStage Python — that is
  `di-agent-flow-substrait-datastage`'s job;
- split partial-pushdown plans into database + DataStage fragments —
  that is future work;
- invent connection metadata, table schemas, or UUIDs.

Keeping the skill rewriter-pure means the same optimized plan can feed
other downstream consumers (flow generation, visualization, replay,
validation tooling) without any of them having to re-do classification
or repair work.

Other known limits:

- Partial pushdown is recognized but not generated.
- LLM-derived target observability SELECTs may vary across runs; the
  batch driver caches the chosen SELECT for re-run determinism.
