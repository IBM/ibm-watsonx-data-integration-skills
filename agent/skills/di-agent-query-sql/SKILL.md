---
name: di-agent-query-sql
description: >
  Use when the user asks to generate SQL from natural language, convert a query to
  SQL, or translate a natural-language request into SQL. This skill first tries
  to generate and compile a Substrait plan, then converts it to SQL using the
  substrait_to_sql tool. If DSL compilation fails, except for obvious low-risk
  generation mistakes that can be corrected immediately, or if
  substrait_to_sql/runtime `/sql` returns an error, fall back to direct
  model-generated SQL. In fallback responses, show a concise warning that the
  deterministic Substrait-to-SQL path could not be used; do not show debug fields
  or raw compile/runtime errors unless the user explicitly asks for debug output.
  Trigger on: "generate sql", "convert to sql", "create sql query", "write sql",
  "translate to sql".
disable-model-invocation: false
---

# Generate SQL from Natural Language

Convert natural language data requests into SQL. Prefer the Substrait
intermediate representation when it can express the request; use direct
model-generated SQL only as an explicit fallback when DSL compilation fails,
required functionality is not supported by the Substrait path, or runtime
`/sql` conversion fails.

## Overview

This skill provides end-to-end conversion from natural language to executable SQL:

```
Natural Language
  → try Substrait DSL
  → compile DSL
  → if compile succeeds: Substrait Plan → SQL via substrait_to_sql
  → if compile fails with unsupported function/construct: direct NL → SQL fallback
  → if runtime /sql conversion fails: direct NL → SQL fallback
```

The conversion process:
1. **Substrait Generation**: Convert natural language to Substrait intermediate representation
2. **SQL Generation**: Convert Substrait to SQL syntax
3. **Fallback SQL Generation**: If Substrait cannot express the required
   semantics, or runtime `/sql` cannot convert the compiled Substrait plan,
   generate SQL directly for the target database implied by the user request or
   source metadata, and report the failure that triggered the fallback

## Workflow

### Phase 1: Generate Substrait Plan (Steps 1-6)

Follow `di-agent-query-substrait` for semantic DSL generation rules, examples,
schema verification, and `NamedStruct` construction. For SQL generation,
the compile step is overridden by this skill: call `compile_substrait_dsl`
with `project_id` and `asset_ids`, not `read_tables`, so the compiler preserves
full table paths in `namedTable.names`.

1. **Fetch Few-Shot Examples** - Call `get_substrait_dsl_examples`
2. **Verify Schema from Assets** - Use `list_data_assets` and `inspect_project_asset` to get asset metadata and connection information
3. **Resolve Runtime SQL Dialect** - Resolve the `target_dialect` value used only for runtime `/sql` conversion from the inspected data asset's connection metadata, with fallback to runtime default dialect behavior when it cannot be identified
4. **Generate DSL** - Call `get_substrait_dsl_spec` and write DSL code following
   `di-agent-query-substrait` rules for type mapping and `NamedStruct` construction.
   Use `table_name` equal to the logical asset name (e.g. `'orders'`), not a
   schema-prefixed string, so that `asset_ids` binding can resolve the full path.
5. **Compile DSL** - Call `compile_substrait_dsl` with **both** `asset_ids` and
   `project_id` so the compiler resolves the full table path from asset metadata
   into `namedTable.names` (e.g. `["schema", "table"]` or
   `["catalog", "schema", "table"]` depending on the asset). This is required so
   that Phase 2 `/sql` can emit a schema-qualified `FROM` clause. The
   `NamedStruct` must still contain the correct column names and types — when
   `asset_ids` is provided the compiler validates the declared types against the
   asset and will error on any mismatch. Phase 1 succeeds only when
   `compile_substrait_dsl` returns a compiled Substrait JSON plan.
6. **Correct Obvious Low-Risk Errors Only** - If compilation fails because of an immediately correctable generation mistake, fix it and retry; otherwise proceed to fallback

**Important:** You must attempt Phase 1 first. The Substrait JSON from a
successful `compile_substrait_dsl` call is required for Phase 2. If DSL
compilation fails, proceed to Phase 3 fallback SQL generation unless the error
is an obvious low-risk generation mistake that can be corrected immediately,
such as a misspelled column name, wrong table alias, simple DSL syntax typo, or
missing asset binding.

Do not require exhausting a fixed retry count before fallback. Phase 1 failures
that should fall back include, but are not limited to:

- `function '<name>' is not defined in Substrait`
- Unsupported DSL functions, expressions, relational constructs, or type
  signatures required by the request
- Missing Substrait support for dialect-specific constructs such as array
  expansion, ordered string aggregation, regex extraction, procedural binary
  conversion, or correlated scalar subqueries

Only retry for obvious low-risk generation mistakes that can be corrected
immediately. Otherwise use Phase 3 fallback after the compile failure.

### Resolve Runtime SQL Dialect

During Phase 1, resolve one `runtime_target_dialect` value for the
`substrait_to_sql` call. This value exists only for runtime `/sql` conversion.
Pass it as `target_dialect` to `substrait_to_sql` so `/sql` can return
database-specific SQL when the source database type is known. If it cannot be
identified, pass an empty value and clearly tell the user runtime default
dialect behavior was used.

Do not use the runtime dialect mapping to limit direct model-generated SQL
in Phase 3. Once generation falls back to the active model, generate for the
database named or implied by the user's request and source metadata, even when
that database is not in the runtime `/sql` dialect list.

Resolve it from the source assets and their connections:

1. Inspect every source data asset with
   `inspect_project_asset(..., asset_type="data_asset")` and resolve its
   `datasource_type`:
   - Use the data asset's `datasource_type` when present.
   - If a connection asset ID is present, call
     `inspect_project_asset(asset_ids=[...], asset_type="connection")`.
   - If only `connection_name` is present, call
     `list_connections(entity_name="<exact connection name>")`, then inspect the
     matching connection ID with `inspect_project_asset`.
   - If the data asset has no connection metadata, call
     `get_asset_relationships` for that data asset, find the related connection
     ID, and inspect that connection.
2. Normalize each resolved `datasource_type` using the [dialect mapping reference](references/dialect-mapping.md) for runtime `/sql` conversion.
3. For multiple source assets, use a runtime `/sql` dialect only when all
   resolved source dialects agree. If they differ and Phase 2 runtime `/sql`
   conversion is still needed, ask the user for the runtime target dialect. If
   some sources are unresolved but every resolved source agrees, use the agreed
   dialect and report which sources could not be identified.

**See [Dialect Mapping Reference](references/dialect-mapping.md)** for the complete mapping table of connection datasource types to runtime target dialects.

If no source connection can be mapped, state that the database type could not
be identified. In that case, call `substrait_to_sql` with an empty
`target_dialect` value so runtime `/sql` can apply its default dialect
behavior, and clearly tell the user that a fallback/default dialect was used.

### Phase 2: Convert Substrait to SQL

Once you have a successfully compiled Substrait plan, convert it to SQL:

Before calling the tool, verify both conversion inputs are present:

- `substrait_json` is the successful output from `compile_substrait_dsl`
- `runtime_target_dialect` is either one of the values accepted by runtime
  `/sql` per the [dialect mapping reference](references/dialect-mapping.md), or
  an empty value when the source database type could not be identified

Then pass `runtime_target_dialect` as `target_dialect`. Never drop it from the
tool call; use an empty value when dialect resolution failed.

#### Call substrait_to_sql

```python
substrait_to_sql(
    substrait_json="<substrait_json_string>",
    target_dialect="<runtime_target_dialect>",
    preprocessed=false
)
```

**Parameters:**

- **`substrait_json`** (required): The Substrait plan in JSON string format from `compile_substrait_dsl`
- **`target_dialect`**: Required by this workflow. Pass the lowercase
  `runtime_target_dialect` resolved from inspected source connection metadata.
  If the source database type could not be identified, pass an empty value and
  tell the user runtime default dialect behavior was used.
- **`preprocessed`** (optional, default: false): Whether to return preprocessed SQL. If not specified, defaults to false.

**Response:**

```json
{
  "success": true,
  "sql": "SELECT ...",
  "dialect": "<dialect>",
  "errors": null
}
```

Or on failure:

```json
{
  "success": false,
  "sql": null,
  "dialect": "<dialect>",
  "errors": "Error message"
}
```

**Error Handling:**
- Check the `success` field in the response
- If `success` is false, examine the `errors` field
- If `runtime_target_dialect` is empty, tell the user runtime default dialect
  behavior was used and report the returned `dialect` value
- Summarize conversion limitations in the fallback warning, then proceed to
  Phase 3 fallback direct NL-to-SQL generation. Include sanitized error details
  only when the user explicitly asks for debug or verbose output.

### Phase 3: Fallback Direct NL to SQL

Enter this phase when either:

- Phase 1 DSL compilation fails, except when the error is an obvious low-risk
  generation mistake that can be corrected immediately, such as a misspelled
  column name, wrong table alias, simple DSL syntax typo, or missing asset
  binding.
- Phase 2 calls `substrait_to_sql` / runtime `/sql` with a compiled Substrait
  plan, but the tool returns `success: false`, an HTTP error, a timeout, or any
  other conversion error.

When falling back:

1. Preserve the user's original natural-language semantics exactly.
2. Choose the fallback SQL target database from the user's request first, then
   from source metadata. This choice is not limited by the runtime `/sql`
   dialect table. If the database cannot be identified, state that explicitly
   and generate conservative ANSI SQL only when the semantics can be preserved.
3. Generate SQL directly with the active model. Do not call `substrait_to_sql`
   without a compiled Substrait plan.
4. Use dialect-native functions when needed to preserve semantics.
5. Include a concise warning before the SQL. The warning must state that the
   deterministic Substrait-to-SQL path could not be used, summarize the
   Substrait or runtime `/sql` limitation, and state that SQL was generated
   directly by the model for the target database.
6. Do not show `fallback_nl_to_sql`, Substrait status, failed phase, or raw
   compile/runtime error text in the default response. Show sanitized error
   details only when the user explicitly asks for debug or verbose output.

If the SQL uses dialect-specific syntax, list those features briefly.

## Output Format

When the Substrait path succeeds, present the complete workflow results:

````markdown
### Natural Language Query
<user's original query>

### Target Database
<database_type>

### Generated Substrait Plan
```json
<substrait_json>
```

### Generated SQL
```sql
<database_specific_sql>
```

### Database-Specific Features
- <list of dialect-specific syntax used>
````

When the fallback path is used, present:

````markdown
### Natural Language Query
<user's original query>

### Target Database
<database named/implied for direct SQL generation>

### Warning
The deterministic Substrait-to-SQL path could not be used because <brief
Substrait DSL, Substrait compiler, or runtime /sql limitation>. SQL was generated
directly by the model for <target database>.

### Generated SQL
```sql
<database_specific_sql>
```

### Database-Specific Features
- <list of dialect-specific syntax used>
````


### Example 1: Basic Query

**Input:**
```
Query: "How many orders are there for each shipping mode in the lineitem table?"
Table: lineitem (orderkey: int, shipmode: string)
```

**Workflow:**
1. Generate Substrait plan using `di-agent-query-substrait` workflow
2. Call `substrait_to_sql`:
   ```python
   substrait_to_sql(
       substrait_json='{"relations": [...]}',
       target_dialect="<runtime_target_dialect>",
       preprocessed=false
   )
   ```

**Output:**
````markdown
### Natural Language Query
How many orders are there for each shipping mode in the lineitem table?

### Target Database
<runtime_target_dialect>

### Generated Substrait Plan
```json
{
  "relations": [...],
  "extensions": [...]
}
```

### Generated SQL
```sql
SELECT "shipmode", COUNT("orderkey") AS "order_count"
FROM "tiny.lineitem"
GROUP BY "shipmode";
```
````


## Supported Databases

The `substrait_to_sql` tool supports SQL generation.

## Important Notes

### Conversion Process

This skill performs a three-phase workflow with a fallback path:

1. **Substrait Generation** (Phase 1):
   - Parse natural language query
   - Generate Substrait DSL code
   - Compile to Substrait intermediate representation
   - Validate query semantics

2. **SQL Generation** (Phase 2 via `substrait_to_sql`):
   - Convert Substrait to SQL
   - Apply database-specific syntax rules
   - Use native database functions
   - Handle database type system

3. **Fallback SQL Generation** (Phase 3 via active model):
   - Generate SQL directly from natural language for the database named or
     implied by the user request and source metadata when Phase 1 cannot compile
     the required Substrait plan or Phase 2 cannot convert the compiled plan
     through runtime `/sql`
   - Summarize the Substrait or runtime `/sql` limitation in the fallback warning

### Tool Implementation Details

The `substrait_to_sql` tool:
- Calls di-runtime REST API endpoint: `/data_intg_ai/v1/runtime/sql`
- Forwards the resolved runtime dialect through its `target_dialect` argument
- Uses Engine Adapter for deterministic and accurate SQL generation
- Converts Substrait to SQL syntax
- Returns structured response with success/error handling
- Timeout: 60 seconds

### Schema Verification

**Critical:** Always verify schemas and connection metadata from project assets
using `list_data_assets` and `inspect_project_asset` during Phase 1. Never rely on:
- Few-shot examples for schema information
- User-provided schemas without verification
- Prior knowledge or assumptions

The schema and datasource type from asset tools are authoritative for Substrait
generation and runtime `/sql` dialect resolution. They should also inform the
Phase 3 fallback target database, but the Phase 3 model-generated SQL path is
not restricted to the runtime `/sql` dialect list.

## Error Handling

### Error Redaction Requirements
- Before showing any compile/runtime error text to users, sanitize sensitive details.
- Mask credentials, tokens, keys, passwords, and authorization headers.
- Mask internal hostnames/IPs, full URLs, filesystem paths, and request IDs that are not needed for debugging.
- Preserve only the minimum error context required to explain fallback decisions.
- If sanitization would remove all useful context, provide a short normalized error summary instead of raw text.

### Phase 1 Errors (Substrait Generation)
If DSL compilation fails, fall back to Phase 3 direct NL-to-SQL generation and
summarize the Substrait limitation in the fallback warning.
Retry only for obvious low-risk generation mistakes that can be corrected
immediately, such as a misspelled column name, wrong table alias, simple DSL
syntax typo, or missing asset binding. Do not require exhausting a fixed retry
count before fallback.

### Phase 2 Errors (SQL Conversion)
- Check the `success` field in the response
- If `runtime_target_dialect` is empty, tell the user runtime default dialect behavior was used and report the returned `dialect` value
- If `success` is false, examine the `errors` field
- Common issues:
  - Invalid Substrait JSON format
  - Unsupported operations
  - Missing or mismatched target dialect
  - Network/timeout errors
- Do not stop at reporting the error. Proceed to Phase 3 fallback direct
  NL-to-SQL generation and summarize the runtime `/sql` limitation in the
  fallback warning.

### Phase 3 Errors (Fallback SQL Generation)
- If the target database cannot be identified and cannot be inferred from the
  user's request or source metadata, generate conservative ANSI SQL when
  possible and state the assumption. Ask the user only when the unknown target
  database makes faithful SQL generation impossible.
- If required semantics are ambiguous, state the ambiguity and generate the
  closest SQL only when the assumption is explicit.
- If no faithful SQL can be generated, report both the Substrait failure and the
  direct SQL limitation.

## MCP Tools Used

1. **Phase 1 (Substrait Generation):**
   - `get_substrait_dsl_examples` - Fetch few-shot examples
   - `get_substrait_dsl_spec` - Get DSL specification
   - `list_data_assets` - Find assets by name
   - `inspect_project_asset` - Get asset schemas and connection metadata
   - `list_connections` - Resolve a connection ID from a data asset's connection name
   - `get_asset_relationships` - Resolve related connection when the data asset does not include datasource metadata
   - `compile_substrait_dsl` - Compile DSL to Substrait

2. **Phase 2 (SQL Generation):**
   - `substrait_to_sql` - Convert Substrait to SQL (calls di-runtime REST API)

3. **Phase 3 (Fallback SQL Generation):**
   - Active model only - Generate SQL directly from natural language for the
     database named or implied by the user request and source metadata when
     Substrait cannot express the request or runtime `/sql` cannot convert the
     compiled Substrait plan. This path is not limited by the runtime `/sql`
     dialect table.

## Success Criteria

A successful execution produces:
1. Either a valid Substrait plan compiled without errors, or an explicit
   fallback warning that summarizes the Substrait or runtime `/sql` limitation
2. On the Substrait path, a resolved runtime target dialect, or an explicit
   fallback to runtime default dialect behavior when resolution fails
3. For the Substrait path, a `substrait_to_sql` call that explicitly passes the
   dialect as `target_dialect`
4. A database-specific SQL query, either from `substrait_to_sql` or from the
   direct NL-to-SQL fallback
5. Clear documentation of database-specific features used and, when applicable,
   why fallback was used

## Related Skills

- **di-agent-query-substrait**: Generates Substrait plans (Phase 1 of this skill)

## Runtime Considerations

- **Nullability**: Columns marked `nullable: true` must use nullable type suffix (e.g., `string?`)
- **Case-insensitive filtering**: Use `lower()` for case-insensitive text comparisons
- **Column disambiguation**: Pre-rename overlapping columns before joins
- **Database features**: Generated SQL may reference database-specific features (indexes, hints, etc.) that should be created for optimal performance
