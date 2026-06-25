---
name: di-agent-query-optimization
description: >
  Use when the user asks to optimize a Substrait plan, perform SQL pushdown,
  simplify a Substrait plan for pushdown, classify full versus partial pushdown,
  or rewrite a Substrait plan so DataStage executes a single SQL statement.
  Route here whenever the user's request contains both a pushdown-related term
  ("pushdown", "push down", "full pushdown", "SQL pushdown") and an
  optimization-related term ("optimize", "optimized", "optimization",
  "optimise", "optimised", "optimisation"), even when Substrait is not mentioned.
  If no raw Substrait plan is available, first use `di-agent-query-substrait`;
  then convert the raw plan to SQL, classify full versus partial pushdown, and emit
  the compact full-pushdown plan. Partial pushdown is recognized but not supported.
  Trigger on: "optimize substrait", "full pushdown", "partial pushdown",
  "pushdown plan", "optimize plan", "simplify substrait", "engine optimization",
  "pushdown optimization".
---

# Optimize Substrait Plan for SQL Pushdown

Rewrite a normal Substrait plan JSON into the compact full-pushdown shape used by the
Natural Language to DataStage flow workflow:

```
Natural language -> Substrait plan -> Optimization -> optimized Substrait plan -> DataStage flow
```

This skill classifies **full SQL pushdown** versus **partial SQL pushdown**, but it
only generates optimized output for full pushdown.
If full pushdown is not provably safe, stop and return the original plan plus the
reason. Do not attempt to split the plan into partial database and DataStage
fragments yet.

## Inputs

Required:
- A valid Substrait plan JSON object or JSON string.

Optional but recommended:
- `target_dialect`, for example `postgresql`, `db2`, `snowflake`, or `generic`.
- Source and target connection metadata. At minimum, identify whether every source and
  target table is in the same database connection.
- Desired root mode:
  - `fetch`: SQL returns a final result set.
  - `write`: SQL performs database-side writes and returns a final result set for the
    downstream sink.

## End-to-End Pushdown Workflow

When the user says "use pushdown to optimize", "optimize with pushdown", or asks for
pushdown optimization without providing a raw Substrait plan:

0. Treat this skill as the required entry point; DataStage flow generation comes
   only after this skill produces an optimized full-pushdown plan.
1. Use `di-agent-query-substrait` to generate the raw Substrait plan from the user's
   natural language or query request.
2. Use `di-agent-query-sql` / `substrait_to_sql` with the **raw** Substrait plan to
   test SQL conversion. Pass the raw plan, not a rewritten or optimized plan.
3. If SQL conversion preserves every relation rel and all reads use the same connector
   / database connection, classify the plan as full pushdown and emit the optimized
   full-pushdown Substrait plan described below.
4. If only a subgraph can be converted, if relation rels are lost, or if reads span
   different connectors, stop and say partial pushdown is not supported yet by this
   skill.
5. Hand the optimized full-pushdown plan to `di-agent-flow-substrait-datastage` to
   generate the Python SDK script and DataStage flow.

## Pushdown Classification

Treat a plan as **full pushdown** only when all of these are true:

1. `substrait_to_sql` succeeds and returns non-empty SQL — a single statement or a
   statement block — that preserves every relation rel from the original plan. No
   relation, operation, or boundary may be dropped, skipped, approximated, or left
   for DataStage.
2. Every read rel reads from the same connector / database connection. If the plan
   has a write target, it must also be in that same connection or be represented by
   the SQL block without requiring an external DataStage write.
3. Every operation in the source plan can execute inside that connector as SQL —
   no DataStage-only stages, external files, datasets, engine operations, or
   partial-flow boundaries.

Treat the plan as **partial pushdown** when some subgraph can be converted to SQL,
but the complete plan cannot, or when reads span different connectors. Partial
pushdown is a future enhancement; this skill must stop and report that partial
pushdown is not supported yet.

Same-database eligibility must be **explicit**: the plan's metadata must show one
connection ID across all reads/writes, or the user must supply it. If connection
metadata is absent, stop and report:

> Full pushdown is not confirmed because source and target connection metadata is missing.

Do not silently assume same-database pushdown.

## Workflow

### 1. Parse and Inspect the Plan

Validate that the input is JSON and contains a top-level `relations` array.

Collect:
- Root relation kinds: `root`, `write`, `fetch`, or direct relation.
- Read table paths from `read.namedTable.names`.
- Write table paths from `write.namedTable.names`.
- Connection IDs from `advancedExtension`, `advancedExtensions`, or DataStage extension
  metadata when present.
- Output schema from the root names and the read/write `baseSchema`.

### 2. Decide Full-Pushdown Eligibility

Apply the **Pushdown Classification** rules above. If the plan appears SQL-pushdown
eligible only for a subgraph, or if it converts to SQL only by leaving some rels or
connectors outside the SQL result, stop and return:

```json
{
  "optimized": false,
  "mode": "partial_pushdown_unsupported",
  "reason": "<specific reason>",
  "message": "Partial pushdown is not supported yet by this skill.",
  "substrait_json": <original_plan>
}
```

Use `mode: "not_full_pushdown"` only when the plan is not a SQL pushdown candidate at
all. Use `mode: "partial_pushdown_unsupported"` when some SQL conversion may be
possible but the complete plan cannot be fully pushed down.

### 3. Convert the Original Plan to SQL

Use the existing `di-agent-query-sql` skill's Substrait-to-SQL phase.

Call:

```python
substrait_to_sql(
    substrait_json="<original_substrait_json_string>",
    target_dialect="<target_dialect>",
    preprocessed=false
)
```

If conversion fails, stop and return the conversion error with the original plan.
If conversion succeeds but inspection shows relation rel loss, omitted reads,
different connectors, or remaining non-SQL work, treat the result as partial
pushdown and stop with `mode: "partial_pushdown_unsupported"`.

### 4. Build the Full-Pushdown Plan

Create a new Substrait JSON object with:

- `version.producer = "di-agent-query-optimization-full-pushdown"`
- `extensionUris` containing `urn:datastage:substrait:extensions:full-pushdown-sql`
- One relation.
- A SQL-bearing `read` node at `relations[0].root.input.read`.

The SQL's final statement must be a `SELECT` whose rows are the flow's output —
the downstream Sequential file sink consumes those rows. Multi-statement blocks that
contain writes AND end in a `SELECT` (e.g. `TRUNCATE...; INSERT...; SELECT
COUNT(*)...`) are allowed: the writes are side-effects performed inside the
source database and the trailing SELECT supplies the sink rows. Write-only
blocks (no trailing SELECT) are not supported — stop and ask the
user to add a row-count or affected-row SELECT.

The output column names and types must come from the trailing SELECT. Do not
invent a schema — stop and ask if it cannot be derived.

Before embedding SQL in the optimized plan, check the SQL trailing `SELECT`
aliases against the column-name sanitization contract from
`substrait-to-datastage-python`. If an alias is already DataStage-safe and unique,
keep it unchanged. If an alias is missing, unsafe, or collides after sanitization,
repair only the final output alias and the corresponding output schema name:

1. Start from the original root names / trailing SELECT aliases in output order.
2. Replace every character outside `[a-zA-Z0-9_]` with `_`.
3. If the result does not start with a letter, prepend `col_`.
4. If the result is empty or null, use `col`.
5. Deduplicate within the output list using `_1`, `_2`, ... suffixes.

The checked/repaired names are the canonical output names for the full-pushdown
plan. The SQL trailing `SELECT` must alias every output expression with exactly the
matching canonical name (`AS <name>`), and both `root.names` and
`read.baseSchema.names` must use those same names in the same order. Do not modify
the SQL converter output if the aliases already satisfy the rule. If repair is
needed, repair only final SELECT aliases; do not rename physical source table or
source column identifiers.

Use this compact shape:

```json
{
  "version": {
    "minorNumber": 55,
    "producer": "di-agent-query-optimization-full-pushdown"
  },
  "extensionUris": [
    {
      "extensionUriAnchor": 1,
      "uri": "urn:datastage:substrait:extensions:full-pushdown-sql"
    }
  ],
  "relations": [
    {
      "root": {
        "names": ["<output_column_1>", "<output_column_2>"],
        "input": {
          "read": {
            "common": {
              "direct": {},
              "advancedExtension": {
                "enhancement": {
                  "nodeKind": "full_pushdown_read",
                  "sqlStatement": "<sql from substrait_to_sql>"
                }
              }
            },
            "baseSchema": {
              "names": ["<output_column_1>", "<output_column_2>"],
              "struct": {
                "types": ["<copy compatible Substrait type objects from original root>"]
              }
            },
            "advanced_extension": {
              "optimization": [
                {
                  "@type": "type.di.ibm.com/com.ibm.di.substrait.Optimization",
                  "connection_id": "<UUID of the source database connection from the original plan>"
                }
              ]
            }
          }
        }
      }
    }
  ]
}
```

Carry `connection_id` over from the original plan's read nodes (they share the same
connection — that's a full-pushdown prerequisite). This is the canonical DataStage
convention; do not invent a UUID and do not omit the field.

Preserve schema carefully:
- Prefer root `names` for output column names, then check them with the
  DataStage-safe alias rules above. Keep already-safe names unchanged; sanitize and
  deduplicate only unsafe/missing/colliding names.
- Prefer the final relation's `baseSchema.struct.types` for output types.
- Ensure the canonical output names are used consistently in the SQL `AS` aliases,
  `relations[0].root.names`, and `read.baseSchema.names`.
- If the final output schema cannot be found, use a conservative two-column row-count
  schema only when the SQL is a statement block that ends with a row-count `SELECT`.
  Otherwise stop and ask for the expected output schema.

### 5. Validate the Optimized Plan

Before returning, verify:
- There is exactly one top-level relation.
- The relation contains `root.input.read`.
- The read node has `common.advancedExtension.enhancement.sqlStatement` and its
  `nodeKind` is `"full_pushdown_read"`.
- The read node has
  `advanced_extension.optimization[0].connection_id` (typed) carried over from
  the original plan.
- Root names match read `baseSchema.names`.
- Every trailing SELECT output expression has an `AS` alias matching the canonical
  name at the same position in `root.names`.

## Output Format

Return:

````markdown
### Optimization Result

- Mode: full_pushdown
- SQL dialect: <target_dialect>
- Connection ID: <connection_id>

### Generated SQL

```sql
<sql>
```

### Optimized Substrait JSON

```json
<full-pushdown plan>
```
````

## Handoff

The optimized JSON is the input contract for `di-agent-flow-substrait-datastage`.
After emitting the plan, the next step in the workflow is to invoke that skill (or
prompt the user to). Do not emit Python yourself — keep this skill purely a plan
rewriter so the same optimized JSON can feed other downstream consumers
(visualization, replay, validation, etc.). Partial-pushdown splitting is future work
and must not be attempted by this skill.

Downstream consumers rely on these invariants. Validate before returning:
- `relations[0].root.input.read.common.advancedExtension.enhancement.nodeKind == "full_pushdown_read"`
- `sqlStatement` is non-empty and its trailing statement is a `SELECT`.
- `relations[0].root.input.read.advanced_extension.optimization[0].connection_id`
  is present (UUID carried over from the original plan).
- Root `names` length equals `baseSchema.names` length and entries match by position.
- `baseSchema.struct.types` length matches `baseSchema.names` length.
- SQL trailing SELECT aliases match `root.names` exactly and are DataStage-safe
  canonical names after the check/repair step.

## Current Limitations

- Partial pushdown is not supported yet.
- The skill does not split a plan into database and DataStage fragments.
- If a plan can only be partially pushed down, stop and say partial
  pushdown is not supported in this case.
- The skill does not invent connection metadata. Same-database eligibility must be
  explicit or supplied by the user.
- SQL correctness depends on the `substrait_to_sql` tool used by `di-agent-query-sql`.
