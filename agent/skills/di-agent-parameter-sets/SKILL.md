---
name: di-agent-parameter-sets
description: "Guide for creating, editing, and using parameter sets (paramsets) in IBM watsonx.data integration. Covers parameter types, value sets, PROJDEF, local parameters, runtime parameters, flow parameters, #param# and ${param} reference syntax for both DataStage (batch) and StreamSets (streaming) flows, and parameterizing connection properties with external parameter sets. Use when the user wants to create, list, update, or delete parameter sets; manage value sets; attach parameter sets to flows or connections; parameterize connection properties; or reference parameters inside a flow or connection."
---

# Parameter Sets

> **Never include any UUID in a reply.** Project IDs, asset IDs, flow IDs, connection IDs, parameter set IDs — none of these may appear in your response, regardless of whether they came from a tool result or from your own session context. In particular, never open a reply with a phrase like "in your project `<uuid>`" or "in project `4c2d…`". Always identify assets by name only. The only exception is a `flow_link` field returned ready-made by a tool.

> **StreamSets only supports `string` parameters.** If the user's request involves a StreamSets flow and any requested parameter is not `string` type, stop immediately — before calling any tool. Explain the constraint, propose a corrected string-only plan, and wait for confirmation before proceeding. This check must happen before `list_streamsets_flows`, before `create_parameter_set`, and before any other tool call.

Parameter sets are named collections of typed parameters stored as project-level assets. They let you define values once and reuse them across multiple flows — switching between environments (dev, test, prod) at job runtime without modifying the flow.

## Always Determine Flow Type First

Before calling any tool, determine whether the target flow is:

- **DataStage** (batch) — supports all 11 parameter types, value sets, PROJDEF, local parameters
- **StreamSets** (streaming) — supports `string` parameters only; no value sets, no PROJDEF

Most parameter-set features are engine-specific. Getting this wrong leads to silent failures.
→ See [resources/streaming_limitations.md](resources/streaming_limitations.md) for the full constraints and validation checklist.

## What Feature Do You Need?

| User need | Feature to use |
|---|---|
| Reuse values across multiple flows | Parameter set |
| Switch between dev / test / prod environments | Value set on a parameter set |
| One-off parameter for a single flow run | Local parameter (DataStage only) — use `add_local_parameter` |
| Project-level DataStage environment variables | PROJDEF |
| Parameterise a StreamSets flow | String-only parameter set |
| Manage connection values across environments | Attach parameter set to connection |

## Common Tasks

### List or find parameter sets

```
list_parameter_sets(project_id=..., name_filter=...)  # use name_filter to narrow
get_parameter_set(parameter_set_id=..., project_id=...)  # full details incl. value sets
```

Report by parameter set **name only**.

### Create a reusable parameter set

**If the target is a StreamSets flow, verify every parameter type is `string` before calling any tool** — see "Always Determine Flow Type First" above.

```
create_parameter_set(project_id=..., name=..., parameters=[...])
```

Confirm by parameter set name and parameters only.

For DataStage flows, all 11 types are supported.
→ [resources/parameter_types.md](resources/parameter_types.md) for the full type table.

### Add or modify parameters on an existing set

`parameters` is a **full replacement list** — any parameter omitted is deleted.
The tool enforces this automatically: if your submitted list would remove existing
parameters it returns an error naming the parameters that would be lost and asks
you to either include them or pass `confirm_replacement=True`.

Confirm changes by parameter set name and the updated parameter list.

The safest workflow is still to fetch first and merge:

```
get_parameter_set(...)               # 1. fetch current parameters
update_parameter_set(                # 2. submit full replacement list
    parameter_set_id=...,
    project_id=...,
    parameters=[...merged...],
)
```

To intentionally drop parameters, pass `confirm_replacement=True`:

```
update_parameter_set(
    parameter_set_id=...,
    project_id=...,
    parameters=[...reduced list...],
    confirm_replacement=True,
)
```

### Create dev / test / prod environments

Value sets let a single parameter set carry multiple environment snapshots:

```
manage_value_set(action="add",     value_set_name="prod", values={...})
manage_value_set(action="replace", value_set_name="prod", values={...})  # overwrite
manage_value_set(action="remove",  value_set_name="dev")
```

Confirm by parameter set name and value set name.

**Never echo secret values back to the user.** When a parameter set contains `encrypted` parameters, confirm the operation by naming the parameters that were set (e.g. "DB_PASS was stored") — never repeat the actual values in your response. This applies to confirmations, summaries, and plan previews.

→ [resources/value_sets.md](resources/value_sets.md) for full workflow and runtime selection.

### Attach a parameter set to a flow

```
attach_parameter_set_to_flow(project_id=..., flow_id=..., engine=..., parameter_set_name=...)
```

The registration is saved immediately. **After confirming success, always tell the user the next step:** to activate the parameters, add references to stage expressions using the correct syntax for the engine:
- DataStage: `#setName.paramName#`
- StreamSets: `${setName__paramName}`

Do this in every attach confirmation reply — do not omit the next-step guidance even when the user only asked to attach. Confirm by flow name and parameter set name.
→ [resources/flow_integration.md](resources/flow_integration.md) for reference syntax and workflow.

### Attach a parameter set to a connection

```
attach_parameter_set_to_connection(
    project_id=...,
    connection_id=...,
    parameter_set_name=...,
    property_mappings={"host": "DB_HOST", "port": "DB_PORT", "database": "DB_NAME"},
)
```

Confirm by connection name and parameter set name. If the tool result includes a runtime value-set selection example, relay it in prose (e.g. "To switch environments at runtime, pass the value set name in the job's runtime parameters") — do not reproduce it as a code block.

Replaces the listed connection property values with `#paramSetName.paramName#` references and enables the "Use external Parameter Sets" toggle on the connection. Use `list_connections` to find the `connection_id`, `inspect_project_asset` with `asset_type="connection"` to see the available property names, and `list_parameter_sets` / `get_parameter_set` to confirm parameter names.
→ [resources/connection_integration.md](resources/connection_integration.md) for the full workflow.

### Audit what parameters a flow uses

`get_flow_parameter_references` requires a `flow_id` — never call it with an empty string. When the user gives a flow name, always call `list_datastage_flows` first to resolve the ID, then call `get_flow_parameter_references` with it. Do not attempt `get_flow_parameter_references` before the list call completes.

```
list_datastage_flows(entity_name=..., project_id=...)   # 1. always do this first
get_flow_parameter_references(flow_id=..., project_id=...)  # 2. then call with the id
```

Returns `external_paramsets` (parameter sets registered on the flow) and `local_parameters` (flow-scoped parameters). Report by flow name, parameter set names, and local parameter names. Use this before deleting a parameter set to confirm the flow still references it, or after `attach_parameter_set_to_flow` to verify the registration was saved.

**DataStage only** — `engine` is optional and defaults to `"datastage"`; pass `engine="streamsets"` only if you want the explicit not-supported error. This reports what is *registered* on the flow, not which stage expressions actually use those parameters; to find `#setName.paramName#` usage, retrieve the flow with `retrieve_datastage_flow_code` and search the stage property strings.

### Add a local parameter to a DataStage flow

Local parameters are flow-scoped variables defined directly on the flow — not shared with other flows and not part of any parameter set. Reference them in stage expressions as `#paramName#` (no set name prefix).

```
add_local_parameter(
    flow_id=..., project_id=...,
    engine="datastage",        # streamsets is not supported — returns an error
    name="SCHEMA",
    type="string",             # all 11 DataStage types supported
    value="PUBLIC",            # optional default
)
```

Confirm by flow name and parameter name.

- If a local parameter with the same name already exists it is overwritten (case-sensitive match).
- `type` accepts the same aliases as `create_parameter_set`: `integer` → `int64`, `float` → `sfloat`, `list` → `enum`.
- `enum` type requires `valid_values=[...]`.
- `subtype="envvar"` is accepted as pass-through but has not been validated against the backend — treat as experimental until confirmed.

### Remove a local parameter from a DataStage flow

```
remove_local_parameter(flow_id=..., project_id=..., engine="datastage", name=...)
```

Confirm by flow name and parameter name.

Removes the named parameter. Match is case-sensitive. Returns `status="removed"` on success or `status="not_found"` if the name does not exist — safe to call without a prior existence check.

### Rename or re-describe a set

```
update_parameter_set(parameter_set_id=..., project_id=..., name="NewName", description="...")
```

Confirm by old and new names only.

### Delete a parameter set

**REQUIRED sequence — do not skip any step:**

1. Call `list_parameter_sets` to resolve the name to an asset ID.
2. Call `get_asset_relationships` (asset_type `"parameter_set"`) with that ID **before calling `delete_parameter_set`**, regardless of whether you expect references.
3. If `used_by` is non-empty, warn the user of every referencing flow or connection and ask for confirmation before proceeding.
4. If `used_by` is empty, proceed to delete immediately — no confirmation turn is needed.
5. Call `delete_parameter_set` only after step 3 is confirmed (or step 4 applies).

```python
# Step 1
list_parameter_sets(project_id=..., name_filter="MySet")

# Step 2 — always, unconditionally
get_asset_relationships(
    assets=[{"asset_type": "parameter_set", "asset_id": "<resolved_id>"}],
    project_id=...
)

# Step 5 — only after steps 3–4
delete_parameter_set(parameter_set_id=..., project_id=...)
```

Confirm deletion by parameter set name only.

Permanent and unrecoverable. The tool returns only `{'deleted': True, 'parameter_set_id': ...}` — it does **not** check for referencing flows. Deleting a set that is still referenced can leave those flows unable to validate or run until the broken references are removed.

## Tool Reference

| Tool | Purpose |
|---|---|
| `list_parameter_sets` | List all sets in a project (excludes PROJDEF) |
| `get_parameter_set` | Full details: parameters + value sets; includes `streaming_warnings` if the set has StreamSets incompatibilities |
| `create_parameter_set` | Create a new set |
| `update_parameter_set` | Rename, re-describe, or replace the parameters list; guards against accidental removal — use `confirm_replacement=True` to allow drops |
| `delete_parameter_set` | Permanently delete a set; call `get_asset_relationships` first to find referencing flows, warn the user, then delete |
| `manage_value_set` | Add / replace / remove a named value set |
| `attach_parameter_set_to_flow` | Associate a set with a DataStage or StreamSets flow |
| `attach_parameter_set_to_connection` | Parameterize connection properties with a parameter set; enables "Use external Parameter Sets" on the connection |
| `get_flow_parameter_references` | Return `external_paramsets` and `local_parameters` registered on a DataStage flow (DataStage only) |
| `add_local_parameter` | Add or overwrite a local parameter on a DataStage flow (DataStage only) |
| `remove_local_parameter` | Remove a local parameter from a DataStage flow (DataStage only) |

## Guardrails

- See the UUID rule at the top of this skill — never echo any UUID in a reply.
- `PROJDEF` is a reserved system name — never create a set with that name.
- `update_parameter_set` replaces the entire `parameters` list. Fetch first, merge, then submit.
- `delete_parameter_set` is permanent. Follow the 5-step sequence under "Delete a parameter set" above — `get_asset_relationships` before `delete_parameter_set`, unconditionally. Skip the confirmation turn only when `used_by` is empty; otherwise warn and confirm first.
- StreamSets: parameter set names must not contain `__`. Only `string` parameters are injected.
- `add_local_parameter` and `remove_local_parameter` are DataStage only — passing `engine="streamsets"` returns an error immediately. On `get_flow_parameter_references` the `engine` argument is optional and defaults to `"datastage"`.
- Call `get_flow_parameter_references` before `add_local_parameter` to avoid creating a duplicate under a different case.
- `get_flow_parameter_references` reports registration only. A set appearing in `external_paramsets` does not prove any stage expression uses it, and absence does not prove no `#setName.paramName#` text remains in the flow.
- `attach_parameter_set_to_connection`: both halves of `property_mappings` are validated before anything is patched — the keys must be properties the connection already has, and the values must be parameters on the named set. Use `inspect_project_asset(asset_type="connection")` to see available property names. Properties you don't map are left untouched, including secrets.
- `update_datastage_flow` replaces the entire flow definition, but it loads the stored flow first, so `external_paramsets` and `local_parameters` survive an edit — no re-attach is needed. Confirm with `get_flow_parameter_references` after edits that matter. → [resources/flow_lifecycle_with_parameters.md](resources/flow_lifecycle_with_parameters.md) for the full risk table.
- When something isn't working as expected → [resources/troubleshooting.md](resources/troubleshooting.md).
- For the most common agent mistakes → [resources/common_mistakes.md](resources/common_mistakes.md).
