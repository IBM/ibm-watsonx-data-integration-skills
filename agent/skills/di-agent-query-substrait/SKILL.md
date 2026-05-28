---
name: di-agent-query-substrait
description: >
  Use when the user asks to generate a Substrait query plan, create a Substrait plan
  from natural language, convert a data query to Substrait JSON, write a Substrait DSL
  pipeline, translate a data request into a query plan, process a test entry from a
  JSONL dataset. Covers writing DSL code, calling MCP tools (compile_substrait_dsl,
  get_substrait_dsl_examples, load_test_entry), and self-correcting on compile errors.
  Trigger on: "generate substrait", "generate substrait dsl", "generate functional plan",
  "generate fp", "process entry", "run entry", "generate dsl".
disable-model-invocation: true
---

# Generate Substrait DSL

Translate natural language data requests into executable Substrait JSON via the Substrait DSL.

## Inputs Required

We need the flow description and the input schema.  It is important to get the input schema correct and it should be consistent with the names and types in the asset browser.  Use `list_project_assets` to find the relevant asset(s) by names and `inspect_project_asset` with the asset ID(s) to retrieve the authoritative column names, types, and nullability.  Do not use any other information like fewshot examples or prior knowledge to guess the schema — it must be derived from the project assets to ensure the generated Substrait plan is valid against the actual data.

If the user provides the table schemas (one or more source tables with column names and substrait types), verify them against the actual asset in the project using `list_project_assets` and `inspect_project_asset`. If there are inconsistencies, flag them to the user. **The schema from the asset tools takes precedence** unless the user explicitly overrides it.

If the user does not supply table schemas, derive them directly from the project assets by calling `list_project_assets` and `inspect_project_asset`.

Once you have the assets build a `NamedStruct` by mapping them assets to DSL types using the following mapping:

### Asset Type Mapping

When constructing a `NamedStruct` from an inspected asset, map asset column types to DSL types as follows:

| Asset type | DSL type |
|---|---|
| `longvarchar`, `varchar`, `char`, `text` | `string` |
| `bigint`, `int8` | `i64` |
| `integer`, `int`, `int4` | `i64` |
| `smallint`, `int2` | `i16` |
| `real`, `float4` | `fp32` |
| `numeric`, `decimal` | `fp64` |
| `double precision`, `float8` | `fp64` |
| `boolean`, `bool` | `boolean` |
| `date` | `date` |
| `timestamp`, `timestamp without time zone` | `timestamp` |

Append `?` to the DSL type for any column where `nullable: true` in the asset metadata (e.g., `string?`).

## Workflow

Follow these steps to generate a Substrait plan from a natural language request.

### 1. Fetch Few-Shot Examples

Call `get_substrait_dsl_examples` with the user's query to get relevant DSL examples:
```
get_substrait_dsl_examples(query="<user_query>", collection="draft_generation", n=5)
```

Study the returned examples to understand the syntax of the DSL.  Never use the few-shot examples to derive any input schema even if seemingly more appropriate — that must come from the project assets as described in the next step.

### 2. Verify Schema from Assets

It is mandatory to verify the schema using the asset tools. Otherwise, the result will be an invalid plan that fails to execute!
1. Call `list_project_assets` to locate the asset(s) by name in the project
2. Call `inspect_project_asset` with the asset ID(s) and `asset_type="data_asset"` to retrieve column metadata
3. For each column, map the asset type to a DSL type using the **Asset Type Mapping** table above
4. It is imperative to append `?` to nullable column types (e.g., `string?`)
5. Use the resulting schema as the `NamedStruct` for `ReadTable`

The schema found in the asset browser takes precedence over any schema mentioned in the few-shot examples.  If there are inconsistencies to user provided schemas, flag them and ask the user to confirm which one to use.

### 3. Generate DSL

Call `get_substrait_dsl_spec` to retrieve the language specification. Study it carefully before writing any DSL code. Write a DSL query that matches the user's request using the verified table schemas by following the rules in the spec for how to construct the query, how to name and reference columns, and how to use aliases.

- Work with immutable **VirtualTable** objects transformed through **Constructs**
- Each line: `variable = Construct(...)`
- End with `return <vtable>`
- Expressions must be inlined — no expression variables
- Use `left.` and `right.` prefixes in Join conditions and only in Join conditions
- Use `alias` on aggregation functions and grouping expressions

### 4. Compile via compile_substrait_dsl

Call the `compile_substrait_dsl` MCP tool with the generated DSL:
```
compile_substrait_dsl(substrait_dsl_code="<your_dsl>", read_tables=[...])
```

You may only proceed if `compile_substrait_dsl` succeeds. If it succeeds, the Substrait JSON is in the response — proceed to step 6. If it does not succeed, continue with step 5.

### 5. Self-Correct (up to 3 attempts)

When errors occur:

1. Read the error message carefully
2. Optionally call `get_substrait_dsl_examples` with `collection="generation_with_error_correction"` for correction examples
3. Fix the DSL based on the error feedback
4. Call `compile_substrait_dsl` again

Common errors and fixes:
- **Column not found**: check the vtable schema after each construct — use only columns that exist
- **Type mismatch**: use `cast()` to convert types, or check literal types
- **Scope errors**: aliases in the same construct's `exprs` list are not visible to each other — chain a second Select/Project
- **Join column errors**: use `left.` and `right.` prefixes

**If all 3 attempts fail**: report the final error to the user, show the last DSL attempt, and suggest they refine their query or check the table schemas.

### 6. Execute or Convert

Depending on the user's request, execute or convert the DSL. Only execute the request if the user explicitly asks for it.

- **Execute the Substrait DSL** (if the user asks to run it):

  Two execution tools are available. Both compile the DSL and run the resulting
  flow. Only call either after a successful `compile_substrait_dsl` validation.

  ```
  run_substrait_dsl(substrait_dsl_code="<dsl>", project_id="<project_id>", source_asset_ids=["<id1>", ...])
  ```
  ```
  run_substrait_dsl_static(substrait_dsl_code="<dsl>", project_id="<project_id>")
  ```

  If one fails, retry with the other as a fallback — either can fail in cases
  where the other succeeds.

- **Convert to Elyra pipeline JSON** (if the user requests it):
  ```
  convert_substrait_dsl_to_elyra(substrait_dsl_code="<dsl>", read_tables=[...])
  ```
  Returns `{"success": bool, "elyra_json": dict|null, "errors": str|null}`.

### 7. Return Results

Present the user with:
- The **Substrait JSON** from the successful compilation
- The **DSL code** generated (for transparency)

## Output Format

```
### Generated DSL

\`\`\`query
<DSL code, excluding ReadTable lines>
\`\`\`

### Substrait JSON

\`\`\`json
<substrait_json from compile_substrait_dsl>
\`\`\`
```

## Important Notes

- **You must call `get_substrait_dsl_spec` and study the spec before generating any DSL code.** It is the authoritative reference for all constructs, expressions, types, and scoping rules — do not only rely on few-shot examples or prior knowledge for syntax details
- `Select` keeps ONLY listed columns; `Project` keeps ALL columns plus new ones
- Aggregation measures must NOT be wrapped in `cast()`
- Final output column names must not contain dots — use `Select` with aliases to rename

## Runtime Considerations

- **Nullability**: Any column marked `nullable: true` in the asset metadata MUST use the nullable type suffix (e.g., `string?`, `i64?`). DataStage will crash at runtime if NULL values are read into non-nullable fields.
- **Case-insensitive filtering**: When filtering on text/enum columns, use `lower()` for case-insensitive comparison (e.g., `equal(lower(col("status")), literal("pending", "string"))`) rather than assuming a specific casing in the data.
- **Column disambiguation**: When joining multiple tables, pre-rename overlapping columns via `Select` before joining (e.g., rename `customer_id` to `orders_customer_id` using a table-derived prefix). Do not rely on `left.`/`right.` prefixes outside of Join conditions.
