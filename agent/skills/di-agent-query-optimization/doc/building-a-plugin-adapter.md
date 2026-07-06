# Building a New Pushdown Plug-in Adapter

This is the practical guide. If you have a customer-specific input format
(shell-wrapped SQL, DBT models, Informatica exports, an existing
DataStage flow, etc.) that should feed the DataStage pushdown pipeline,
ship a plug-in adapter and the rest of the framework picks it up
automatically.

Before reading this, you should already understand the v1 contracts the
framework freezes — see [`../references/adapter-contract.md`](../references/adapter-contract.md).
That is the spec; the current doc is the how-to.

If a customer-specific adapter is already in the skills tree (under
`agent/skills/di-adapter-*/`), reading its `SKILL.md` alongside this
guide is the fastest way to internalize the conventions.

## When to build a plug-in

| Your input | Build a plug-in? |
|---|---|
| One natural-language query | No. The optimizer's path 1 invokes `di-agent-query-substrait`. |
| SQL text pasted in the prompt | No. The optimizer's path 2 handles it directly. |
| A path to a `.sql` file | No. The optimizer's path 3 reads it directly. |
| A folder of `.sql` files | Usually no. `di-agent-pushdown-batch` iterates and uses path 3 per file. |
| A custom file format (e.g. shell-wrapped SnowSQL, DBT model, Informatica export) | **Yes — build a `di-adapter-<source>` plug-in.** |

All adapters produce the same output: a `pushdown-workload-v1` JSON
object. They differ only in how they parse the customer-specific input
format on the way in.

## Step 1 — Copy the template

```bash
# from your plugin development root
cp -r agent/skills/di-agent-query-optimization/examples/reference-adapter \
      agent/skills/di-adapter-<source>
```

The template gives you a working `SKILL.md`, an example input file, and
an example workload JSON.

For production, your plug-in lives in its own Claude Code plugin package,
not under `agent/skills/`. The in-tree location is fine during
development.

## Step 2 — Write the frontmatter

Open `SKILL.md` and edit the frontmatter. The required fields:

```yaml
---
name: di-adapter-<source>                   # MUST start with di-adapter-
description: >                              # the LLM uses this to decide
  Parses <custom format> into a             # when to invoke your skill.
  pushdown-workload-v1 JSON object          # Be specific about what
  for di-agent-query-optimization.          # files / formats you accept.
  Trigger on: "<distinctive phrases>".
capability: pushdown-adapter                # constant — do not change
produces: pushdown-workload-v1              # constant for any adapter
accepts: [".<ext>", "<content-tag>"]        # file extensions or content tags the batch driver uses for dispatch
---
```

Guidance on each field:

- `name` — `di-adapter-<source>` where `<source>` is short and
  customer-or-format-specific (`acme-dbt`, `nightly-cron-bash`, `vendor-export`).
- `description` — the LLM-routing layer reads this. Be concrete about
  what the input looks like and include the most likely trigger phrases
  the user will type.
- `accepts` — used by `di-agent-pushdown-batch` for per-file dispatch.
  Include file extensions (`.ctl`, `.dbt`, `.sql.j2`) and any content
  tags you want the driver to recognize. Lowercase. Include the dot for
  extensions.

## Step 3 — Write the workflow

Your skill's body documents the deterministic steps to turn one input
into one workload JSON. Five things you almost always need to do:

### 3a. Read and bound the workload

If the input is a wrapper around SQL (shell script, Jinja template, DBT
model), define how to find the start and end of the SQL block. Document
the bounding pattern explicitly. Example pattern for a shell heredoc
wrapping SQL:

> Identify the heredoc delimiter by scanning for `<<\s*\$?\{?(\w+)\}?`
> after the `snowsql` invocation. Use that token to find the closing
> line.

### 3b. Strip non-SQL noise

Things to typically remove:

- shell comments (`#`);
- CLI directives (`!set`, `!option`);
- session-noise statements that introspect state without doing work
  (`SELECT 'SESSION ID' ...`, `set var = ...`);
- empty lines and whitespace-only blocks.

Add a `hints.notes` entry for any non-trivial transform you applied so
the user can see what was dropped.

### 3c. Split into statements

Split on top-level `;`. Quoted strings (`'...'`, `"..."`, `$$...$$`)
shield embedded `;`. Comments are not splits but stay in the SQL text.

If your dialect has unusual statement terminators (e.g. `GO` for
T-SQL, `/` for PL/SQL), document and handle them.

### 3d. Detect statement kinds and tables

For each statement, match the leading keyword (case-insensitive) to the
canonical kinds listed in `../references/adapter-contract.md`:

`SELECT`, `INSERT`, `INSERT_SELECT`, `UPDATE`, `DELETE`, `MERGE`,
`COPY_INTO`, `CREATE`, `CREATE_AS_SELECT`, `TRUNCATE`, `USE`, `SET`,
`COMMIT`, `ROLLBACK`, `OTHER`.

Extract `reads` and `writes` heuristically:

- `INSERT INTO <X>` → `writes: [<X>]`; `FROM <Y>` clauses → `reads: [<Y>]`.
- `UPDATE <X>` → `writes: [<X>]`; `FROM <Y>` → `reads`.
- `COPY INTO <X> FROM <Y>` → `writes: [<X>]`; `Y` (usually a stage) →
  `reads`.
- `MERGE INTO <X> USING <Y>` → `writes: [<X>]`, `reads: [<Y>]`.

Preserve `${VAR}` placeholders verbatim — do not resolve them. Better
metadata here means the optimizer can classify more sharply without
re-parsing.

### 3e. Collect parameters

Scan the workload text for `${WORD}` placeholders. Deduplicate. Ignore
obvious internals (heredoc tokens, shell-private vars).

### 3f. (target-pushdown) Derive the observability SELECT

This is the highest-value optional step. If the workload classifies as
target pushdown (INSERT/UPDATE/COPY/etc. with no trailing SELECT), the
flow's only output is whatever the connector's select-statement
property returns. By default
the optimizer picks something via its own LLM step at run time, which is
non-deterministic across re-runs.

If your adapter can pick a useful SELECT up front, set
`hints.observability_select` and `hints.observability_schema`. The
optimizer validates and uses them, skipping its own LLM step.

Run an LLM analysis over the parsed statements and ask it to emit:

```json
{
  "observability_select": "<single SELECT statement>",
  "observability_schema": {
    "names": ["<col1>", "..."],
    "types": [<Substrait type objects>]
  }
}
```

Good observability picks per workload pattern:

| Workload pattern | Useful SELECT |
|---|---|
| Pure INSERT into one target | `SELECT COUNT(*) AS <target>_rows FROM <target>` |
| INSERT into N targets | row counts across the primary targets, one row each |
| UPDATE with a `WHERE` filter | `SELECT COUNT(*) FROM <target> WHERE updt_dt_tm >= <recent>` |
| COPY INTO | `SELECT LAST_QUERY_ID() AS last_query_id` |
| MERGE | `SELECT $1.METADATA$ACTION, COUNT(*) ... FROM TABLE(RESULT_SCAN(LAST_QUERY_ID())) GROUP BY 1` (Snowflake) |
| Mixed / unsure | `SELECT 'OK' AS status, CURRENT_TIMESTAMP() AS run_dt` |

Substrait types for common cases:

```json
{"i64":       {"nullability": "NULLABILITY_NULLABLE"}}   // counts
{"string":    {"nullability": "NULLABILITY_NULLABLE"}}   // statuses, IDs
{"timestamp": {"nullability": "NULLABILITY_NULLABLE"}}   // run times
```

If the LLM cannot derive anything useful, leave both hint fields `null`
and let the optimizer fall back.

## Step 4 — Emit the workload JSON

Use the template in `../references/adapter-contract.md` § workload JSON. Three rules:

1. `extensionUris[0].uri` is **exactly** `urn:datastage:substrait:extensions:pushdown-workload`.
2. `enhancement.nodeKind` is **exactly** `"pushdown-workload-v1"`.
3. `root.names`, `baseSchema.names`, `baseSchema.struct.types` are
   **empty arrays**. The optimizer fills them when building optimized pushdown plan.

`connection_id` should be an empty string unless your input format
genuinely carries one (rare). The user or batch driver resolves it.

## Step 5 — Validate against the conformance checklist

Before returning, run the checklist from `../references/adapter-contract.md` § Adapter
conformance checklist. The non-obvious ones:

- If you set `hints.observability_select`, you **must** set
  `hints.observability_schema` with matching `names`/`types` lengths.
- `rawSqlStatement` must be a non-empty string — even degenerate cases
  like a single `COMMIT;` count.
- `dialect` is lowercase.

## Step 6 — Document the workflow in your `SKILL.md`

Use the template's structure:

- short prose intro explaining what the adapter does;
- "Input shape" section showing what a typical input looks like;
- "Workflow" section with numbered steps from §3 above, adapted to your
  format;
- "Output template" section showing the workload JSON you produce;
- "Conformance checklist" section restating the checks from
  `../references/adapter-contract.md`;
- "What this skill does NOT do" — explicit non-goals (don't resolve
  `connection_id`, don't classify, don't generate Python).

A clear "What this skill does NOT do" section is the single best
prevention against scope creep. Plug-ins that drift into doing the
optimizer's or flow skill's job become hard to debug.

## Step 7 — Test against `di-agent-query-optimization`

Hand-write a tiny input that exercises both classification paths. For
each, confirm:

1. Your adapter produces a valid workload JSON (all conformance
   checks pass).
2. `di-agent-query-optimization` reads your workload JSON, runs the SQL-text
   probe, and emits a optimized pushdown plan.
3. The optimized pushdown plan `nodeKind` matches your expectation
   (`source_full_pushdown_read` for trailing-SELECT workloads,
   `target_full_pushdown_read` for write-only workloads).
4. If you supplied `hints.observability_select`, the optimizer's
   "Observability SELECT source" output says `adapter`, not `llm` or
   `fallback`.

The fastest way is to ask the agent: *"Run this <format> file through
di-adapter-<source> then di-agent-query-optimization in classify_only
mode."*

## Step 8 — Test with the batch driver

If your adapter is going to be used for bulk runs, smoke-test with two
or three inputs through `di-agent-pushdown-batch`:

> Process all files matching `<glob>` for target pushdown. Output flows
> under project `<test-project>`, connection `<test-connection>`. Write
> a manifest to `./test_manifest.csv`. Mode: classify_only.

Confirm the manifest:

- has one row per input;
- the `adapter` column names your skill;
- `observability_select` is populated when you supplied it;
- `confidence` is `high` when the input is clean.

Then retry once with the same manifest path. Confirm that previously
classified rows are not reprocessed (idempotence).

## Step 9 — Package and distribute

For production, ship as a standalone Claude Code plugin package
containing just your `di-adapter-<source>/` folder. Customers install
the plugin; the framework discovers the adapter automatically through
Claude's skill scan.

The framework discovers installed adapters by listing
`agent/skills/di-adapter-*/`; no registry file needs updating.

## Common pitfalls

- **Adapter tries to expose per-statement metadata in workload JSON.** It can't
  — workload JSON's `rawSqlStatement` is a single string. The optimizer
  re-derives kinds, reads, and writes from the joined text. Adapter
  authors may still extract per-statement info internally to inform
  their observability-SELECT choice, but only the joined SQL string
  goes into the workload JSON.
- **Adapter resolves `${VAR}` placeholders.** Don't. The user or a later
  parameterization pass owns this. Resolving in the adapter bakes
  values into the flow at generation time and defeats reuse.
- **Adapter tries to be helpful and resolves `connection_id` via
  environment lookups.** Don't. The batch driver and optimizer want to
  see an empty string they can resolve uniformly.
- **Adapter classifies source vs. target.** Don't. That's the
  optimizer's job. If you want to nudge classification (e.g. you know
  this script is always target), set `hints.force_mode`.
- **Adapter emits optimized pushdown plan.** Don't. That's the optimizer's job. Stop
  at workload JSON.
- **Adapter triggers on overly broad description.** "Parses script
  files" matches too much. Be specific: "Parses customer-X SnowSQL
  `.ctl` scripts (Bourne shell wrapper around Snowflake SQL)".
- **Observability SELECT references columns that don't exist.** Pin
  your LLM step to use only the table names that appear in the parsed
  `writes` arrays — never invent column names. When unsure, prefer
  `SELECT COUNT(*)` over column-specific queries.

## Pointers

- Reference adapter template — [`../examples/reference-adapter/`](../examples/reference-adapter/)
- v1 contract spec — [`../references/adapter-contract.md`](../references/adapter-contract.md)
- Testing scenarios — [`testing-the-framework.md`](testing-the-framework.md)
