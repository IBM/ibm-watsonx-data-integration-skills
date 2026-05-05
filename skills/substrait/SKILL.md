---
name: generate-substrait
description: >
  Use when the user asks to generate a Substrait query plan, create a Substrait plan
  from natural language, convert a data query to Substrait JSON, write a Substrait DSL
  pipeline, translate a data request into a query plan, process a test entry from a
  JSONL dataset, or run an entry by index. Covers writing DSL code, calling MCP
  validation tools (validate_inputs, parse_dsl_tool, query_few_shot, load_test_entry),
  and self-correcting on parse errors.
  Trigger on: "generate substrait", "generate functional plan", "generate fp",
  "process entry", "run entry", "generate dsl".
disable-model-invocation: true
---

# Generate Substrait Plan

Translate natural language data requests into Substrait query plans using a Python-like DSL.

## Inputs Required

**Two ways to provide input:**

### Option A — Inline

The user provides the query and table schemas directly:
1. **User query**: a natural language description of the desired data pipeline
2. **Table schemas**: one or more source tables with column names and Substrait types

Table schema format for MCP tools:
```json
{"name": "drivers", "columns": {"driverId": "i64", "name": "string", "nationality": "string"}}
```

### Option B — JSONL test entry

The user provides a dataset path and entry index (e.g., `<path> entry 5` or `<path> idx 5`).

Call the `load_test_entry` MCP tool:
```
load_test_entry(dataset_path="<path>", entry_idx=<index>)
```

This returns `nl_query`, `read_tables` (already parsed from SQL DDL), `output_schema`, `difficulty`, and `domain`. Use these as inputs for the rest of the workflow.

Display the parsed inputs for confirmation: the query, tables with columns/types, output schema (if any), and difficulty.

## Workflow

### 1. Validate Inputs

Call the `validate_inputs` MCP tool to check the user query and table schemas are well-formed.

### 2. Fetch Few-Shot Examples

Call `query_few_shot` with the user's query to get relevant DSL examples:
```
query_few_shot(query="<user_query>", collection="draft_generation", n=5)
```

Study the returned examples to understand DSL patterns for similar queries.

### 3. Generate DSL

Write DSL code following the grammar in `references/dsl-syntax.md`. Key rules:

- Work with immutable **VirtualTable** objects transformed through **Constructs**
- Each line: `variable = Construct(...)`
- End with `return <vtable>`
- Expressions must be inlined — no expression variables
- Use `left.` and `right.` prefixes in Join conditions
- Use `alias` on aggregation functions and grouping expressions

**Do NOT include ReadTable statements** — they are prepended automatically by the `parse_dsl_tool`.

Core constructs: `ReadTable`, `Select`, `Project`, `Filter`, `Cross`, `Join`, `Aggregate`, `Sort`, `Fetch`

### 4. Validate via parse_dsl_tool

Call the `parse_dsl_tool` MCP tool with the generated DSL and table schemas:
```
parse_dsl_tool(dsl="<your_dsl>", read_tables=[...], clean=true)
```

- If `success: true` — the Substrait JSON is in the response. Proceed to step 6.
- If `success: false` — read the `errors` field and proceed to step 5.

### 5. Self-Correct (up to 3 attempts)

When errors occur:

1. Read the error message carefully
2. Optionally call `query_few_shot` with `collection="generation_with_error_correction"` for correction examples
3. Fix the DSL based on the error feedback
4. Call `parse_dsl_tool` again

Common errors and fixes:
- **Column not found**: check the vtable schema after each construct — use only columns that exist
- **Type mismatch**: use `cast()` to convert types, or check literal types
- **Scope errors**: aliases in the same construct's `exprs` list are not visible to each other — chain a second Select/Project
- **Join column errors**: use `left.` and `right.` prefixes

**If all 3 attempts fail**: report the final error to the user, show the last DSL attempt, and suggest they refine their query or check the table schemas.

### 6. Optional: Compile or Convert

- **Recompile Substrait JSON** (if needed separately from parsing):
  ```
  compile_substrait(dsl="<dsl>", read_tables=[...])
  ```
  Returns `{"success": bool, "substrait_json": str|null, "errors": str|null}`.

- **Convert to Elyra pipeline JSON** (if the user requests it):
  ```
  convert_elyra(dsl="<dsl>", read_tables=[...])
  ```
  Returns `{"success": bool, "elyra_json": dict|null, "errors": str|null}`.

### 7. Return Results

Present the user with:
- The **Substrait JSON** from the successful parse
- The **DSL code** generated (for transparency)

## Output Format

```
### Generated DSL

\`\`\`query
<DSL code, excluding ReadTable lines>
\`\`\`

### Substrait JSON

\`\`\`json
<substrait_json from parse_dsl_tool>
\`\`\`
```

## Important Notes

- The DSL grammar is fully specified in `references/dsl-syntax.md` — consult it for any construct or expression details
- `Select` keeps ONLY listed columns; `Project` keeps ALL columns plus new ones
- Aggregation measures must NOT be wrapped in `cast()`
- Final output column names must not contain dots — use `Select` with aliases to rename
