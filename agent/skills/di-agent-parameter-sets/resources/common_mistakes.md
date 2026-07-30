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

**Fix:** Always call `get_parameter_set` first, copy the existing `parameters` list, append or modify your changes, then submit the full list.

---

## Deleting a Parameter Set Still Referenced by a Flow

**Mistake:** Calling `delete_parameter_set` while a published flow still has `#setName.param#` references.

**What happens:** The API deletes the asset. At runtime, the DataStage compiler cannot resolve the references — the job fails silently or raises a compilation error on the next publish.

**Fix:** Before deleting:
1. Retrieve each suspected flow definition and search stage property strings for `#setName.param#` patterns to confirm which flows use the set. *(A dedicated `get_flow_parameter_references` tool is planned for a future milestone.)*
2. Remove the references from those flows (`update_datastage_flow`).
3. Then delete the set.

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
