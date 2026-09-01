# Flow Lifecycle with Parameter Sets

This guide covers how parameter set registrations are preserved (or can be lost) across the full lifecycle of a DataStage flow — create, edit, copy, delete, and runtime.

---

## Lifecycle Overview

```
create_pyflow / create_parameter_set
        │
        ▼
attach_parameter_set_to_flow          ← registration saved to flow
        │
        ▼
update_datastage_flow (edit)          ← registration preserved automatically
        │
        ▼
create_job_run (runtime)              ← value set selected here
        │
        ▼
delete_parameter_set                  ← warns about attached flows and connections
```

---

## Creating a Flow with Parameters

### Option A — Pyflow (auto-attaches)

`create_pyflow` detects `#setName.paramName#` tokens in connection-path binding strings and automatically:

1. Validates that the set and each referenced parameter exist in the project.
2. Attaches the set to the compiled flow's `external_paramsets`.

No separate `attach_parameter_set_to_flow` call is needed.

```python
bindings = {
    "orders": "conn-id:/#EnvParams.SCHEMA#/#EnvParams.SRC_TABLE#",
    "target": "conn-id:/#EnvParams.SCHEMA#/ORDERS_ARCHIVE",
}
# EnvParams must already exist before calling create_pyflow.
```

See [flow_integration.md — Using Parameters in Pyflow Flows](flow_integration.md#using-parameters-in-pyflow-flows).

### Option B — Explicit attach after create

For flows created via `create_datastage_flow` or `update_datastage_flow`, register the set explicitly:

```
attach_parameter_set_to_flow(
    project_id=..., flow_id=...,
    engine="datastage",
    parameter_set_name="DBConfig",
)
```

Then add `#DBConfig.paramName#` expressions to the relevant stage properties via `update_datastage_flow`.

---

## Editing a Flow

### Registrations survive an edit on their own

`update_datastage_flow` takes the flow *name* and SDK code — not a full flow definition:

```
retrieve_datastage_flow_code(flow_id=..., project_id=...)   # returns SDK code for the stages
# ... modify stage properties only ...
update_datastage_flow(flow_name=..., project_id=..., sdk_code=<edited code>)
```

The SDK code describes stages and links; it does not carry `external_paramsets`. Registrations are preserved because the tool loads the existing flow before applying your code, so `external_paramsets` and `local_parameters` carry over without anything extra on your part. You do **not** need to re-attach after a routine edit.

### Verify rather than assume

Preservation depends on the tool loading the stored flow, so confirm it rather than trusting it after any edit that matters:

```
get_flow_parameter_references(flow_id=..., project_id=...)
```

**If a registration did go missing:** call `attach_parameter_set_to_flow` again, then re-check with `get_flow_parameter_references`.

### After a pyflow edit

`create_pyflow` is only used for initial creation. Subsequent structural changes via the SDK must use `retrieve_datastage_flow_code` → edit → `update_datastage_flow`. Any parameter set tokens in connection paths must also be present in the existing flow body for the registration to remain; if you remove the stage that used them, manually remove the stale entry from `external_paramsets` too.

---

## Verifying Registration at Any Point

```
get_flow_parameter_references(flow_id=..., project_id=...)
```

Returns `external_paramsets` (registered sets) and `local_parameters` (flow-scoped parameters).

Use this:
- After `attach_parameter_set_to_flow` — confirm the registration was saved.
- After any `update_datastage_flow` call that replaced the flow body — confirm registrations survived.
- Before a job run — confirm all sets the flow references are still attached.

> **Important:** This reports *registration* state only. A set appearing in `external_paramsets` does not prove any stage expression currently uses it. To audit actual `#setName.paramName#` usage, retrieve the flow code and search the stage property strings.

---

## Runtime: Selecting an Environment

At job run time, pass the value set to activate:

```json
{
  "parameter_sets": [
    { "name": "DBConfig", "value_set": "prod" }
  ]
}
```

- **No `value_set` key** → parameter default values apply.
- **Multiple sets** → list each set in the array.
- **Value sets are DataStage-only.** StreamSets connections use separate parameter sets per environment.

If the flow also uses a parameterized connection (via `attach_parameter_set_to_connection`), the same value set selection applies to the connection — no additional configuration is needed at run time.

See [value_sets.md](value_sets.md) for the full value set management workflow.

---

## Deleting a Parameter Set

`delete_parameter_set` proactively scans for DataStage flows and connections that reference the set and includes their names in the confirmation message.

Before confirming deletion:

1. Review the listed attached flows and connections.
2. Decide whether to:
   - Remove the `#setName.paramName#` references from affected flow stage properties and remove the `external_paramsets` entry.
   - Detach parameterized connection properties via the UI or a new `attach_parameter_set_to_connection` call pointing to a replacement set.
3. Confirm deletion only when the references have been cleared or you accept the impact.

**Impact of deleting a referenced set:**
- Attached flows that still carry `#setName.paramName#` references will fail validation and may fail to run.
- Connections whose properties hold `#setName.paramName#` values will resolve to literal `#...#` strings at runtime — effectively broken.

---

## Copying or Importing a Flow

When a DataStage flow is duplicated (via the UI copy action or a project export/import):

- The `external_paramsets` registrations are copied as part of the flow definition.
- The underlying parameter sets they reference **are not automatically copied** — they remain in the source project.
- If the flow uses a **parameterized connection** (`#setName.paramName#` values in connection properties), the connection asset is also not copied. The flow copy will reference a connection that may not exist or will not be parameterized in the destination project.

If you copy a flow to a different project:
1. Create the same parameter sets in the destination project.
2. Re-create or re-configure the parameterized connection in the destination project (the source connection is not duplicated).
3. Attach the parameter set to the destination connection with the same `property_mappings`.
4. Verify with `get_flow_parameter_references` that the flow's `external_paramsets` registrations survived the copy.
5. If the set names differ, update the stage expressions and re-attach.

---

## Local Parameters and Flow Lifecycle

Local parameters (added via `add_local_parameter`) are stored inside the flow definition. Unlike parameter sets they have no separate asset — they travel with the flow through edits, copies, and exports.

However:
- A `update_datastage_flow` that reconstructs the flow body from scratch will drop them, just as it drops `external_paramsets`.
- The safe pattern is the same: retrieve → merge → resubmit.
- Use `get_flow_parameter_references` to audit after any structural edit.

See [flow_integration.md — Local Parameters](flow_integration.md#local-parameters-datastage-only).

---

## Quick Reference: Lifecycle Risks

| Operation | Risk | Mitigation |
|---|---|---|
| `update_datastage_flow` on a parameterized flow | Registrations are preserved by the tool, but the flow is fully replaced | No re-attach needed; confirm with `get_flow_parameter_references` after edits that matter |
| `create_pyflow` re-run on an existing flow | Overwrites the whole flow definition | Use `retrieve_datastage_flow_code` + SDK edits for changes to existing flows |
| `delete_parameter_set` | Breaks attached flows and connections | Review the confirmation message listing; clean up references first |
| Copy/import to another project | Parameter sets **and** parameterized connections are not copied | Re-create sets in destination; re-attach set to the destination connection; verify registration with `get_flow_parameter_references` |
| Rename a parameter set (`update_parameter_set(name=...)`) | All `#OldName.paramName#` references in flows and connection properties become unresolvable | Find and update every reference before or immediately after the rename; republish affected flows |
| Rename a parameter set parameter | Value set entries referencing the old name become orphaned | Update value sets manually after any parameter rename |
