# Common Mistakes with Parameter Sets

## Using Non-String Parameters in a StreamSets Flow

**Mistake:** Creating a parameter set with `int64`, `date`, `encrypted`, or other typed parameters, then attaching it to a StreamSets flow.

**What happens:** The non-string parameters are silently skipped — no constant is injected for them, no error is raised.

**Fix:** Use only `string` type for parameter sets attached to StreamSets flows. For DataStage flows, all 11 types are supported.

---

## Creating Value Sets for a StreamSets Parameter Set

**Mistake:** Adding value sets to a parameter set and expecting environment switching to work in a StreamSets job run.

**What happens:** Value sets are silently ignored by StreamSets. There is no runtime mechanism to select a named snapshot.

**Fix:** Value sets are a DataStage-only feature. For StreamSets environment switching, maintain separate parameter sets per environment or update constants directly before each run.

---

## Parameter Set Name Contains `__`

**Mistake:** Naming a parameter set `My__Config` or `Prod__DB` and trying to attach it to a StreamSets flow.

**What happens:** `attach_parameter_set_to_flow` returns an error immediately — no change is made to the flow.

**Fix:** Rename the set to remove `__` before attaching to a StreamSets flow. For DataStage flows, `__` in the name is allowed.

---

## Forgetting to Republish After Attaching

**Mistake:** Calling `attach_parameter_set_to_flow` and then running the job immediately without republishing the flow.

**What happens:** The job uses the last published version of the flow, which does not contain the parameter set reference. Parameters resolve to empty or cause compilation errors.

**Fix:** Always republish the flow (`update_datastage_flow`) after attaching a parameter set. Check the tool result — it includes a `note` reminding you to republish.

---

## Overwriting Parameters with `update_parameter_set`

**Mistake:** Calling `update_parameter_set(parameters=[new_param])` without including existing parameters.

**What happens:** The existing parameters are deleted. The `parameters` argument is a full replacement list, not a merge.

**Fix:** The tool checks for you — it returns an error listing the parameters that would be removed and asks you to either include them or pass `confirm_replacement=True`. But to be safe, always fetch first and merge your changes into the full list before submitting.

---

## Deleting a Parameter Set Still Referenced by a Flow

**Mistake:** Calling `delete_parameter_set` while a published flow still has `#setName.param#` references.

**What happens:** The API deletes the asset. At runtime, the DataStage compiler cannot resolve the references — the job fails silently or raises a compilation error on the next publish.

**Fix:** `delete_parameter_set` already lists attached flows in its confirmation prompt — read that list rather than deleting blind. To check a specific flow yourself, before deleting:
1. Call `get_flow_parameter_references(flow_id=..., project_id=...)` on each suspected flow to check whether the set is registered in `external_paramsets`.
2. That covers registration only. If the answer has to be exhaustive, also retrieve each flow via `retrieve_datastage_flow_code` and search stage property strings for `#SetName.ParamName#` — expression references can outlive the registration.
3. Remove the references from those flows (`update_datastage_flow`).
4. Then delete the set.

---

## Referencing a Parameter Set That Is Not Attached

**Mistake:** Writing `#DBConfig.DB_HOST#` in a stage expression for a flow that has not had `DBConfig` attached via `attach_parameter_set_to_flow`.

**What happens:** The DataStage compiler raises an "unknown parameter set" error when the flow is compiled or published.

**Fix:** Always call `attach_parameter_set_to_flow` before adding `#setName.param#` expressions to the flow.

---

## Using the Wrong Reference Syntax for the Engine

**Mistake:** Using `#setName.param#` (DataStage syntax) in a StreamSets stage expression, or using `${setName__param}` in a DataStage stage expression.

**What happens:** The expression is treated as a literal string — the parameter value is never substituted.

**Fix:** Use the correct syntax for the engine:
- DataStage: `#ParamSetName.ParameterName#`
- StreamSets: `${ParamSetName__ParameterName}`

---

## Using Wrong Property Names in `attach_parameter_set_to_connection`

**Mistake:** Passing property names that don't match the connection's actual entity properties (e.g. `"hostname"` instead of `"host"`, or `"db"` instead of `"database"`).

**What happens:** The tool validates both halves of `property_mappings` before patching and returns an error listing the unknown names — nothing is written. Property names are datasource-specific, so a name that is correct for one connection type is often wrong for another (`host` for PostgreSQL vs `server` for Db2).

**Fix:** Call `inspect_project_asset(asset_type="connection")` first to see the exact property names for that datasource type. If the tool rejects a name, read the `Known properties` list in the error and re-call with a name from it — do not guess a second time.

---

## Browsing a Connection After Parameterizing It

**Mistake:** Calling `attach_parameter_set_to_connection` and then trying to explore the connection — `discover_connection_data`, or a data-asset schema lookup — to build or fix a flow against it.

**What happens:** The call fails. Only the DataStage job runtime resolves `#setName.paramName#`; the connections API uses the stored string literally and rejects it:

```
CDICO2034E: The property [host] value [#DBConfig.DB_HOST#] is not valid.
Cause: invalid characters in hostname.
```

This holds even when the parameter's default is the correct value — nothing is substituted at browse time.

**Fix:** Finish all discovery first, then parameterize. If you already parameterized and still need the schema, read it from a data asset that was registered beforehand, or restore the plain values in the UI connection editor. Parameterize connections that flows already point at, not ones still being explored.

---

## Expecting Environment Switching on StreamSets Connections

**Mistake:** Attaching a parameter set to a connection that is used by a StreamSets flow and expecting value set selection to work at runtime.

**What happens:** Value sets on a connection parameter set are a DataStage feature. StreamSets does not support runtime value set selection; the parameters resolve to their default values only.

**Fix:** For StreamSets connections, maintain separate parameter sets per environment, or update the connection properties directly before each run.

---

## Deleting a Parameter Set Attached to a Connection

**Mistake:** Deleting a parameter set that is still referenced by a connection (i.e. a connection property contains `#setName.paramName#`).

**What happens:** The connection will fail to resolve the property at runtime. The `delete_parameter_set` confirmation prompt lists attached **flows and connections** — read both lists before confirming.

**Fix:** Before deleting a parameter set, review the attached connections listed in the confirmation message. If any are shown, use `inspect_project_asset(asset_type="connection")` to verify which properties still hold `#setName.*#` references, then update those properties (via the UI connection editor) before confirming the deletion.

---

## Renaming a Parameter Set While Flows or Connections Reference It

**Mistake:** Calling `update_parameter_set(name="NewName", ...)` while attached flows contain `#OldName.paramName#` stage expressions or attached connections contain `#OldName.paramName#` property values.

**What happens:** The rename succeeds instantly. All existing `#OldName.paramName#` references in flows and connections are **not updated automatically** — they become unresolvable. The next job run or connection test will fail with a parameter resolution error.

**Fix:** Before renaming, find every occurrence of `#OldName.` across all attached flows (use `retrieve_datastage_flow_code` and search stage property strings) and across all parameterized connections (use `inspect_project_asset(asset_type="connection")` on each). Update those references to `#NewName.` **after** the rename, then republish the affected flows.

---

## Calling `manage_value_set` Concurrently on the Same Parameter Set

**Mistake:** Issuing two `manage_value_set` calls against the same parameter set at almost the same time (e.g. two agents, two browser sessions, or two rapid tool calls).

**What happens:** `manage_value_set` is implemented as a read-modify-write — it reads all existing value sets, applies the change in memory, then writes the full list back. Two concurrent writers each read the same state, apply their own change, and whichever write lands second silently overwrites the first. One of the two changes is lost.

**Fix:** Treat `manage_value_set` as a serialised operation. Do not issue two calls against the same parameter set in parallel. If you need to add multiple value sets, issue the calls sequentially and wait for each to complete before issuing the next.
