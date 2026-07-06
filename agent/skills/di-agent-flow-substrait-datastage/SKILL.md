---
name: di-agent-flow-substrait-datastage
description: >
  Generate a DataStage flow and Python SDK script from the optimized
  pushdown Substrait plan emitted by di-agent-query-optimization.
  Switches on enhancement.nodeKind to pick the topology:
  source_full_pushdown_read (source full pushdown — workload SELECT in
  the connector's select-statement property) or
  target_full_pushdown_read (target full pushdown — workload in the
  connector's before-SQL property plus an observability SELECT in
  select-statement). Default sink is Sequential file for both modes;
  for target pushdown, PxCopy (pure pass-through, no persistence) and
  PxPeek (debug — write to job log) are available on explicit user
  request. Defaults connectors that
  support both modes (Snowflake, Hive, Impala, JDBC) to Native mode
  (ds_use_datastage = False); DataStage mode available on request.
  Renders source/dialect parameter placeholders to DataStage
  `#PARAM#` or `#PARAM_SET.PARAM#` syntax before assigning SQL to
  connector properties. Partial-pushdown plans are rejected with an unsupported
  message. Trigger on: "substrait to datastage", "generate datastage
  flow", "substrait to flow", "optimized substrait to datastage", "full
  pushdown datastage", "target pushdown datastage", "build pushdown
  datastage flow", "build pushdown datastage flow and run".
---

# Generate a DataStage Flow from an Optimized Pushdown Plan

Generate a DataStage Python SDK script from the optimized pushdown
Substrait plan emitted by `di-agent-query-optimization`.

This skill is a flow generator. It does not classify SQL, lower arbitrary
Substrait, or invent database connection metadata.

## Supported Topologies

| `nodeKind` | Connector SQL behavior | Default sink | Alternative sinks |
|---|---|---|---|
| `source_full_pushdown_read` | Put `sqlStatement` in the connector select-statement property; disable generate-SQL and before-after SQL | Sequential file | PxPeek (debugging) |
| `target_full_pushdown_read` | Enable before-after SQL, put `beforeSqlStatement` in before-SQL, and put the optimizer-chosen observability `sqlStatement` in the connector select-statement property | Sequential file | PxCopy, PxPeek |

Sink choice (target pushdown):

- **Sequential file** (default) — persists the observability SELECT
  output to a CSV. Matches source pushdown so downstream post-processing
  tooling works uniformly. Choose this unless the user explicitly opts
  out.
- **PxCopy** (opt-in) — pure pass-through, no persistence, no log
  emission. The lightest option when the user doesn't care about the
  observability rows: the connector's before-SQL has already done all
  the real work inside the database, and Copy just satisfies the
  DataStage requirement that every link end in a sink stage. Use when
  the user says "no need to write the output anywhere", "skip the file
  sink", or similar.
- **PxPeek** (opt-in) — writes rows to the job log. Useful for
  debugging the observability SELECT during development.

For source pushdown, Sequential file is the default; PxPeek is the only
alternative on explicit request (PxCopy is not useful — source pushdown
actually returns the workload's rows, and the user normally wants them
persisted).

Connector property names above are intent-level names. Resolve actual SDK
fields, enum values, and Native/DataStage mode differences from the
reference files.

## References

Load only what the current request needs:

- `references/datastage-generation.md` - required for Python generation,
  compact-shape checks, output alias rules, type mapping, and skeleton use.
- `references/source-pushdown-topology.md` - required for
  `source_full_pushdown_read`.
- `references/target-pushdown-topology.md` - required for
  `target_full_pushdown_read`.
- `references/template-skeleton.py` - authoritative complete SDK script
  skeleton; replace only the fill block.
- `references/datastage-connector-sdk-reference.md` - connector labels,
  SDK map names, enum names, SQL read support, and pushdown property names.
- `references/connector-property-values.md` - connector property value
  sources and SQL-mode read rules.
- `references/connector-type-label-map.json` - utility-stage labels,
  especially Sequential file.
- `references/flow-execution.md` - only when the user asks to create, run,
  monitor, or fetch flow results.

## Input Preconditions

The input must be optimized pushdown plan from `di-agent-query-optimization`. The
byte-level schema and all invariants are in
`../di-agent-query-optimization/references/adapter-contract.md`. This
skill validates the plan against that spec on entry; if any invariant
fails, stop and report the specific missing field rather than
attempting to generate.

Fields this skill extracts from the plan:

- `enhancement.nodeKind` to select source or target topology;
- `enhancement.sqlStatement` and (for target) `enhancement.beforeSqlStatement`;
- `enhancement.parameters` for normalized parameter names;
- `enhancement.flow_metadata` for flow name, parameter defaults,
  parameter bindings, parameter sets, and runtime hints;
- `root.names` / `baseSchema` for link schema wiring;
- `advanced_extension.optimization[0].connection_id` for the connector.

The plan's `connection_id` is authoritative. If it is missing or cannot
be inspected, stop with the specific missing/invalid field; do not
choose another connection from local files, prior flows, job history, or
conversation context.

If the user gives raw SQL, a SQL file, a `pushdown-workload-v1` JSON
object, a lowered Substrait plan, or a partial-pushdown result, stop
and ask them to run `di-agent-query-optimization` first. That control
skill handles all those input forms and emits the optimized pushdown
plan this skill consumes.

For partial pushdown, say:

> Partial pushdown is not supported yet by this skill. This flow skill only accepts the optimized pushdown Substrait plan where the complete workload is represented by one SQL-bearing read from a single connector.

## Runtime Metadata

The optimized plan supplies SQL and `connection_id`; SDK generation still
needs DataStage runtime metadata:

```json
{
  "project_id": "<watsonx project ID used as the script fallback>",
  "connection_name": "<DataStage connection name matching the plan connection_id>",
  "connector_stage": "<DataStage connector stage label, e.g. IBM Db2>",
  "output_file": "<flow_name>.csv"
}
```

Rules:

- never invent `connection_id`;
- **resolve `connection_name` automatically when possible.** The
  optimized plan always carries `connection_id`. Call
  `inspect_project_asset(asset_ids=[<connection_id>], asset_type="connection", project_id=<project>)`
  to retrieve the connection's `name` and `datasource_type`. Only ask
  the user when this lookup fails (e.g. the connection has been
  deleted) and the user did not supply a name in the prompt. When you
  do ask, include the known `connection_id` in the question.
- **resolve `connector_stage` automatically from the connection's
  `datasource_type`.** The same `inspect_project_asset` call returns
  `datasource_type`; map it to the SDK connector label, map name, and
  enum using `references/datastage-connector-sdk-reference.md`. Ask the
  user only when the type is unknown or ambiguous;
- default `output_file` to a flat `<flow_name>.csv`; avoid directory
  prefixes unless the engine storage path is known to exist;
- use `flow_metadata.suggested_flow_name` unless the user explicitly
  supplies a different flow name;
- pass `flow_metadata.runtime_hints` through in the summary, but do not
  schedule or tag flows unless the SDK/API surface supports it directly.

## Parameter Handling

The optimized pushdown plan preserves customer placeholders in their
source syntax (`${NAME}`, `&NAME`, `:NAME`, etc.). DataStage connector
SQL needs runtime job-parameter syntax, so this skill performs the
boundary rewrite before assigning SQL to connector properties.

Use `enhancement.parameters` as the normalized list of parameter names.
Use `flow_metadata.parameter_bindings` when present. When bindings are
absent, use the known fallback patterns below so existing SQL can still
be rendered without forcing adapters to describe every common syntax.

For each parameter:

1. Validate that the parameter name appears in `enhancement.parameters`.
2. Determine the source token to replace:
   - `flow_metadata.parameter_bindings[NAME].source_syntax` when set;
   - otherwise, choose from the known fallback patterns:
     - `${NAME}` for SnowSQL/shell-template style placeholders;
     - `&&NAME`, then `&NAME`, only for SQL*Plus/Oracle-script style
       sources or when those exact tokens appear for the normalized
       parameter name;
     - `:NAME` only for named-bind SQL sources where the token appears
       outside strings/comments and is not part of a dialect operator;
     - never use positional `?` without explicit rewrite metadata.
3. Determine the DataStage target token:
   - local parameter: `#NAME#`;
   - parameter set: `#PARAMETER_SET.PARAMETER#`, using
     `parameter_set_name` and `parameter_name`.
4. Replace the source token in `sqlStatement` and, for target pushdown,
   `beforeSqlStatement`. If no known fallback token is found, stop and
   report the missing rewrite rather than guessing. Never rewrite
   inside SQL string literals or comments unless the adapter explicitly
   marks those spans as template placeholders.
5. For local parameters, call:

   ```python
   flow.add_local_parameter("<type>", "NAME", value="<default>", prompt="<description>")
   ```

   Use `flow_metadata.parameter_defaults[NAME]` when present;
   otherwise pass an empty value. If the binding supplies
   `runtime_value` for a local parameter, also call:

   ```python
   flow.set_runtime_local_parameter(local_parameter_name="NAME", value="<runtime-value>")
   ```
6. For parameter-set parameters, retrieve and validate the parameter
   set, then attach it:

   ```python
   paramset = project.parameter_sets.get(name="<PARAMETER_SET>")
   flow.use_parameter_set(paramset)
   ```

   Verify that `parameter_name` exists in the retrieved set. If
   `value_set` is supplied, verify it exists and call
   `flow.set_runtime_value_set(parameter_set_name="<PARAMETER_SET>", value_set_name="<VALUE_SET>")`.
   If a parameter-set binding supplies `runtime_value`, or
   `flow_metadata.parameter_defaults[NAME]` is present for that binding,
   call:

   ```python
   flow.set_runtime_parameter_value(parameter_set_name="<PARAMETER_SET>", parameter_name="<PARAMETER>", value="<runtime-value>")
   ```

Always add the local environment parameter:

```python
flow.add_local_parameter("string", "$APT_OSL_PARAM_ESC_SQUOTE", value="True")
```

This makes string-valued substitutions safer when placed inside quoted
SQL literals. Parameters used as identifiers (`usage="identifier"`) are
not SQL-escaped by the database; if a default is supplied for an
identifier parameter, validate it with a conservative identifier
pattern before using it.

Do not resolve database parameter values during generation. DataStage
performs substitution at job-run time.

## Workflow

1. Validate the optimized pushdown plan preconditions and note the `nodeKind`.
2. Read `references/datastage-generation.md` and the required topology
   reference for the selected `nodeKind`.
3. Extract SQL, schema names/types, connection metadata, `flow_metadata`,
   and target `beforeSqlStatement` when present.
4. Render SQL placeholders to DataStage parameter syntax, declare
   matching local parameters, and attach requested parameter sets.
5. Generate exactly two stages and one link:
   - one SQL-mode database connector source configured per topology;
   - one sink stage: Sequential file by default; for target pushdown,
     PxCopy or PxPeek on explicit request (source pushdown supports
     only Sequential file or PxPeek);
   - one source-to-sink link with the optimized output schema.
6. Produce both a complete SDK script from `template-skeleton.py` and the
   no-boilerplate `sdk_code` subset for `create_datastage_flow`.
7. If MCP flow tools are available and the user asked to create the flow,
   call `create_datastage_flow`. On a clear SDK-code error, fix and retry
   with non-empty `sdk_code`.
8. If a flow with the same name already exists, ask whether to overwrite
   with `update_datastage_flow` or create a new name.
9. If the user asked to run or fetch results, read
   `references/flow-execution.md` and use MCP job/result tools first;
   keep the saved script as fallback. **Fetch outputs only when the
   sink writes a data asset.** Sequential file → fetch the file; PxCopy
   → skip result fetch (no persistence); PxPeek → return the relevant
   job-log portion instead of calling a result tool.

Do not add transformers, joins, alternate sinks, or extra stages.

## Output

Return:

````markdown
### DataStage Flow Generation

- Mode: source_full_pushdown | target_full_pushdown
- Flow name: <flow_name> (source: user | adapter | source_ref | filename | hash)
- Source stage: <connector_stage>
- Sink stage: Sequential file (default) | PxCopy (target, on request) | PxPeek (on request)
- Output file: <output_file>
- Flow parameters: <list of local parameters and parameter-set
  references, or "none">
- Runtime hints: <tags, schedule, concurrency_group, or "none">
- Notes from optimizer: <any hints.notes entries>

### Python SDK Script

```python
<complete script or requested fill block>
```
````

When MCP tools create or run a flow, include the returned flow, job,
job-run, and output IDs or links.

## Limits

- Only `source_full_pushdown_read` and `target_full_pushdown_read` are supported.
- Partial pushdown is rejected for now.
- Database connections are required inputs, not generated by this skill.
