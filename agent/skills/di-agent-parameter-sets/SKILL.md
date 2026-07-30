---
name: di-agent-parameter-sets
description: "Guide for creating, editing, and using parameter sets (paramsets) in IBM watsonx Data Integration. Covers parameter types, value sets, PROJDEF, local parameters, runtime parameters, flow parameters, #param# and ${param} reference syntax for both DataStage (batch) and StreamSets (streaming) flows. Use when the user wants to create, list, update, or delete parameter sets; manage value sets; attach parameter sets to flows; or reference parameters inside a flow."
---

# Parameter Sets

Parameter sets are named collections of typed parameters stored as project-level assets. They let you define values once and reuse them across multiple flows — switching between environments (dev, test, prod) at job runtime without modifying the flow.

## Always Determine Flow Type First

Before discussing parameter types, value sets, PROJDEF, local parameters, or reference syntax — determine whether the target flow is:

- **DataStage** (batch) — supports all 11 parameter types, value sets, PROJDEF, local parameters
- **StreamSets** (streaming) — supports `string` parameters only; no value sets, no PROJDEF

Most parameter-set features are engine-specific. Getting this wrong leads to silent failures.
→ See [resources/streaming_limitations.md](resources/streaming_limitations.md) for the full constraints and validation checklist.

## What Feature Do You Need?

| User need | Feature to use |
|---|---|
| Reuse values across multiple flows | Parameter set |
| Switch between dev / test / prod environments | Value set on a parameter set |
| One-off parameter for a single flow run | Local parameter (DataStage only) — defined inside the flow, no agent tool available yet |
| Project-level DataStage environment variables | PROJDEF |
| Parameterise a StreamSets pipeline | String-only parameter set |

## Common Tasks

### List or find parameter sets

```
list_parameter_sets(project_id=..., name_filter=...)  # use name_filter to narrow
get_parameter_set(parameter_set_id=..., project_id=...)  # full details incl. value sets
```

### Create a reusable parameter set

```
create_parameter_set(project_id=..., name=..., parameters=[...])
```

Always confirm the target engine first — StreamSets only supports `string` type.
→ [resources/parameter_types.md](resources/parameter_types.md) for the full type table.

### Add or modify parameters on an existing set

Never guess the current state. Always fetch first:

```
get_parameter_set(...)         # 1. fetch current parameters
update_parameter_set(          # 2. submit full replacement list
    parameters=[...merged...],
    ...
)
```

`parameters` is a **full replacement list** — any parameter omitted is deleted.

### Create dev / test / prod environments

Value sets let a single parameter set carry multiple environment snapshots:

```
manage_value_set(action="add",     value_set_name="prod", values={...})
manage_value_set(action="replace", value_set_name="prod", values={...})  # overwrite
manage_value_set(action="remove",  value_set_name="dev")
```

→ [resources/value_sets.md](resources/value_sets.md) for full workflow and runtime selection.

### Attach a parameter set to a flow

```
attach_parameter_set_to_flow(project_id=..., flow_id=..., engine=..., parameter_set_name=...)
```

The registration is saved immediately. Then add parameter references (`#setName.paramName#` for DataStage, `${setName__paramName}` for StreamSets) to stage properties via `update_datastage_flow` or the StreamSets editing tools.
→ [resources/flow_integration.md](resources/flow_integration.md) for reference syntax and workflow.

### Audit what parameters a flow uses

> **Planned tool — not yet available.**
> `get_flow_parameter_references` will be added in a future milestone.
> In the meantime, inspect stage property strings in the flow JSON for `#setName.param#` references manually.

### Rename or re-describe a set

```
update_parameter_set(parameter_set_id=..., project_id=..., name="NewName", description="...")
```

### Delete a parameter set

```
delete_parameter_set(parameter_set_id=..., project_id=...)
```

Permanent and unrecoverable. Deleting a parameter set that is still referenced by flows can leave those flows in an invalid state. Depending on the platform and workflow, validation may fail, runtime execution may fail, or the flow may become difficult to open or edit until the reference is corrected.

## Tool Reference

| Tool | Purpose |
|---|---|
| `list_parameter_sets` | List all sets in a project (excludes PROJDEF) |
| `get_parameter_set` | Full details: parameters + value sets |
| `create_parameter_set` | Create a new set |
| `update_parameter_set` | Rename, re-describe, or replace the parameters list |
| `delete_parameter_set` | Permanently delete a set |
| `manage_value_set` | Add / replace / remove a named value set |
| `attach_parameter_set_to_flow` | Associate a set with a DataStage or StreamSets flow |
| `get_flow_parameter_references` | *(planned)* Audit parameter references in a DataStage flow |

## Guardrails

- `PROJDEF` is a reserved system name — never create a set with that name.
- `update_parameter_set` replaces the entire `parameters` list. Fetch first, merge, then submit.
- `delete_parameter_set` is permanent. Referencing flows can become invalid, fail validation or runtime execution, or become difficult to open in the UI until the reference is removed.
- StreamSets: parameter set names must not contain `__`. Only `string` parameters are injected.
- After `attach_parameter_set_to_flow`, add `#setName.paramName#` (or `${setName__paramName}`) references to stage properties via `update_datastage_flow` to activate them.
- When something isn't working as expected → [resources/troubleshooting.md](resources/troubleshooting.md).
- For the most common agent mistakes → [resources/common_mistakes.md](resources/common_mistakes.md).
