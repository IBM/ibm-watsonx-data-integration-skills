---
name: di-adapter-reference
description: >
  Reference pushdown input adapter. Demonstrates the minimal behavior
  required to satisfy the pushdown-workload-v1 contract. Copy this skill
  when starting a new di-adapter-<source> plug-in. Not intended for
  production use. Trigger on: "reference adapter", "adapter template",
  "pushdown adapter example".
capability: pushdown-adapter
produces: pushdown-workload-v1
accepts: [".sql", "plain-sql-script"]
---

# Reference Pushdown Adapter

This is a copy-paste template for new `di-adapter-*` plug-ins. It
accepts a plain `.sql` file containing one or more statements separated
by `;` and emits a `pushdown-workload-v1` JSON object.

See `../../references/adapter-contract.md` for the v1 input contract
this skill satisfies.

## Workflow

1. Read the input file. If the user did not specify a dialect, ask.
2. Detect `${PARAM}` placeholders and collect parameter names.
3. (Optional, recommended for target_full_pushdown workloads) Run an
   LLM pass over the workload SQL to choose a useful observability
   SELECT and its output schema. Populate `hints.observability_select`
   and `hints.observability_schema`. Skip this if the workload ends in
   a real output SELECT — the optimizer will treat that as
   source_full_pushdown.
4. (Optional) Lift parameter defaults the source format makes available
   into `flow_metadata.parameter_defaults`. Leave
   `flow_metadata.suggested_flow_name` unset so the framework derives
   it from `source.ref` (only override when the customer's naming
   convention differs from the basename rule).
5. Emit the workload JSON. Statement splitting and kind detection are
   the optimizer's job — emit the SQL as one string.

## Output template

```json
{
  "schema_version": "pushdown-workload-v1",
  "dialect": "<DIALECT>",
  "source": {"kind": "script", "ref": "<FILENAME>"},
  "connection_id": "",
  "rawSqlStatement": "<workload SQL block; statements separated by ;\\n>",
  "parameters": ["<PARAM_NAMES>"],
  "hints": {
    "force_mode": null,
    "observability_select": null,
    "observability_schema": null,
    "notes": []
  },
  "flow_metadata": {
    "suggested_flow_name": null,
    "parameter_defaults": {},
    "runtime_hints": {
      "schedule": null,
      "tags": [],
      "concurrency_group": null
    }
  }
}
```

## Conformance checklist

Before returning, verify:

- `schema_version` is exactly `"pushdown-workload-v1"`.
- `dialect` is set (lowercase).
- `rawSqlStatement` is a non-empty string.
- `parameters` lists every `${VAR}` placeholder that appears in
  `rawSqlStatement`.
- If `hints.observability_select` is set, `hints.observability_schema`
  is also set with matching array lengths.
- Every key in `flow_metadata.parameter_defaults` (when set) appears in
  the `parameters` array.
- If `flow_metadata.suggested_flow_name` is set, it matches
  `^[a-zA-Z][a-zA-Z0-9_]{0,59}$`.

## What this adapter does NOT do

- Resolve `connection_id` — leave as empty string; the optimizer or user
  resolves it.
- Classify source vs. target pushdown — that's the optimizer's job.
- Build the optimized pushdown plan — that's the optimizer's job.
- Generate DataStage flow — that's `di-agent-flow-substrait-datastage`'s
  job.
