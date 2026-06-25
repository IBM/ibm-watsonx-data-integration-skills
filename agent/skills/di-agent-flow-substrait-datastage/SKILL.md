---
name: di-agent-flow-substrait-datastage
description: >
  Use when the user asks to generate a DataStage flow or Python SDK script from an
  optimized Substrait plan. Use for Substrait-to-DataStage Python generation after
  di-agent-query-optimization. Current implementation supports the full-pushdown
  mode: one SQL-bearing database read node connected directly to a Sequential file
  sink. Partial-pushdown plans are in scope for this skill's future expansion, but
  must be rejected with an unsupported message for now. Trigger on: "substrait to
  datastage", "generate datastage flow", "substrait to flow", "optimized substrait
  to datastage", "full pushdown datastage", "build pushdown datastage flow",
  "build pushdown datastage flow and run".
---

# Substrait Plan to DataStage Python SDK

Generate a DataStage Python SDK script from an optimized Substrait plan. This skill is
the DataStage flow-generation handoff after `di-agent-query-optimization`.

Current support is limited to **full pushdown**: one database connector executes a SQL
statement and writes the returned rows to one **Sequential file** stage. If a plan is
partial pushdown, raw Substrait, lowered Substrait, or otherwise not the compact
full-pushdown shape, stop instead of generating a partial DataStage graph.

## Reference Files

Load only the files needed for the current step:

- `references/datastage-generation.md` — required for Python generation. Contains the
  compact full-pushdown shape checks, SQL-mode connector pattern, type mapping, output
  alias rules, `template-skeleton.py` contract, and MCP `sdk_code` subset contract.
- `references/flow-execution.md` — required only when the user asks to create, run,
  monitor, or fetch results from the generated flow.
- `references/minimal-full-pushdown-example.md` — optional worked example for
  `examples/minimal_full_pushdown.substrait.json`.
- `references/template-skeleton.py` — authoritative complete SDK script skeleton.
  Substitute `<FLOW_NAME>` and `<PROJECT_ID>`, then replace only the
  `# <<< BEGIN_FILL >>>` / `# <<< END_FILL >>>` region.
- `references/datastage-connector-sdk-reference.md` — connector labels, SDK map names,
  connection type aliases, enum names, SQL-read support, and common SDK properties.
- `references/connector-type-label-map.json` — utility-stage labels and variable
  prefixes, especially `PxSequentialFile` -> `type = "Sequential file"` and
  `sequentialfile_0`.
- `references/connector-property-values.md` — connector property value sources and
  SQL-mode read rules.
- `../di-agent-knowledge-engine-datastage/stages/SequentialFileStage.md` — Sequential
  file stage behavior, when deeper stage semantics are needed.

## Input Preconditions

The input must be an optimized plan produced by `di-agent-query-optimization`.
Specifically, it must use the compact full-pushdown contract:

- Exactly one top-level relation.
- The relation contains `relations[0].root.input.read`.
- `read.common.advancedExtension.enhancement.nodeKind == "full_pushdown_read"`.
- `read.common.advancedExtension.enhancement.sqlStatement` is present and non-empty.
- The read node carries exactly one source database connection id at
  `read.advanced_extension.optimization[0].connection_id`.

If the user hands you a raw plan or a lowered plan, ask them to run it through
`di-agent-query-optimization` first.

If the plan is marked `partial_pushdown_unsupported`, stop and say:

> Partial pushdown is not supported yet by this skill. This flow skill only accepts
> the currently supported full-pushdown optimized Substrait shape where the complete
> plan is represented by one SQL-bearing read from a single connector.

For any other missing full-pushdown field, do not generate Python. Report the exact
missing field and ask for the required metadata only when it cannot be derived.

## Required Runtime Metadata

The optimized plan contains SQL, but SDK generation also needs runtime DataStage
metadata:

```json
{
  "project_id": "<watsonx project ID used as the script fallback>",
  "connection_name": "<DataStage connection name matching the plan connection_id>",
  "connector_stage": "<DataStage connector stage label, e.g. IBM Db2>",
  "output_file": "<flow_name>.csv"
}
```

Rules:

- `connection_id` must come from the optimized plan. Never invent it.
- `connection_name` is required because the SDK calls
  `project.connections.get(name="...")`. If it is missing, ask the user for the
  matching connection name and include the `connection_id` in the question.
- Resolve `connector_stage`, SDK map name, and enum from
  `references/datastage-connector-sdk-reference.md`. If the source uses a
  three-level `catalog.schema.table` namespace (e.g. Azure Databricks), fully
  qualify every table as `catalog.schema.table` inside the `select_statement`.
- `output_file` defaults to a flat `<flow_name>.csv` (no directory prefix) when the
  user does not specify it. The Sequential file writer does not create parent
  directories, so a path like `di/<flow_name>.csv` fails at runtime with
  `Unable to open <path>: No such file or directory` unless that directory already
  exists on the engine storage. Use a bare filename, or a directory you have
  confirmed exists.

## Workflow

1. Verify the input satisfies the full-pushdown preconditions above.
2. Read `references/datastage-generation.md`.
3. Extract `sqlStatement`, `connection_id`, output names, output types, and a flow
   name. Sanitize output names only when needed by the rules in the generation
   reference.
4. Resolve the connector label, map name, enum, and SQL-mode read support from
   `references/datastage-connector-sdk-reference.md`; consult
   `references/connector-property-values.md` for property values.
5. Generate exactly two stages and one link:
   - one SQL-mode database connector source;
   - one `Sequential file` sink;
   - one source-to-sink link with the optimized output schema.
6. Keep two artifacts:
   - a complete SDK script produced from `references/template-skeleton.py`;
   - a no-boilerplate MCP `sdk_code` subset for `create_datastage_flow`.
7. Create the flow with `create_datastage_flow` when it is available. If it fails
   with a clear SDK-code error, fix and retry with non-empty `sdk_code`. If it fails
   because a flow with that name already exists, do NOT retry automatically: ask the
   user whether to overwrite the existing flow with `update_datastage_flow` (same
   `flow_name`, `project_id`, `sdk_code`) or create it under a new name.
8. If the user asked to run the flow or fetch results, read `references/flow-execution.md`
   and use MCP job/result tools first; use the saved script only as the local fallback.

Do not insert additional stages, transformers, joins, or alternate sinks. This skill
emits exactly the currently supported full-pushdown topology.

## Output Format

Return:

````markdown
### DataStage Flow Generation

- Mode: full_pushdown
- Source stage: <connector_stage>
- Sink stage: Sequential file
- Output file: <output_file>

### Python SDK Script

```python
<complete script or requested fill block>
```
````

When the flow is created or run through MCP tools, include the resulting flow, job,
job-run, and output links or IDs that were returned by the tools.

## Current Support

- Generates DataStage Python only for the compact full-pushdown optimized shape.
- Partial-pushdown plans are a planned extension point. Until supported, stop and say
  partial pushdown is not supported in this case.
- Does not infer or create database connections.
- The generated sink is always a Sequential file stage.
