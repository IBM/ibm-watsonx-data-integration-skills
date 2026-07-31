# Troubleshooting Parameterized Flows

## Flow Cannot Resolve a Parameter at Compile / Publish Time

**Symptoms:** "Unknown parameter set", "unresolved parameter reference", or compile error on publish.

**Check:**
1. Is the parameter set attached to the flow? → `list_parameter_sets` to confirm the set exists; inspect `external_paramsets` in the flow JSON to confirm it is registered.
2. Does the parameter exist on the set? → `get_parameter_set`
3. Is the reference syntax correct for the engine?
   - DataStage: `#SetName.ParamName#`
   - StreamSets: `${SetName__ParamName}`
4. Was the flow republished after attaching the set?

---

## StreamSets Parameter Not Substituted at Runtime

**Symptoms:** The stage expression evaluates to the literal `${SetName__ParamName}` string instead of the actual value.

**Check:**
1. Is the parameter type `string`? Non-string parameters are skipped when injecting constants.
2. Does the parameter set name contain `__`? Attaching would have failed — verify the set was attached successfully.
3. Was the pipeline redeployed after calling `attach_parameter_set_to_flow`?
4. Is the constant key present? Derive the expected constant key from the parameter set: `SetName__ParamName`. Call `get_parameter_set` to see the parameter names, then confirm the stage expression uses exactly that key.
5. Is the reference syntax exactly `${SetName__ParamName}` (double underscore, dollar-brace)?

---

## Job Run Uses Wrong Parameter Value

**Symptoms:** The job runs with an unexpected value — not the default, not the value set you intended.

**Check:**
1. Was a value set specified in `runtime_parameters`? If not, the parameter default applies.
   ```json
   { "parameter_sets": [{ "name": "DBConfig", "value_set": "prod" }] }
   ```
2. Is the value set name correct? Run `get_parameter_set` to list all value sets and their entries.
3. Is there a runtime override taking precedence? Check the `local_parameters` key in `runtime_parameters`.
4. Was the default value on the parameter updated recently but the flow not republished?

---

## Value Set Has No Effect on StreamSets Job

**Symptoms:** Selecting `value_set: "prod"` in `runtime_parameters` does nothing for a StreamSets job.

**Root cause:** StreamSets does not support value sets. Runtime parameter set selection only works for DataStage (batch) flows.

**Fix:** For StreamSets environment switching, use separate parameter sets per environment, or update the constant values directly before each run.

---

## Parameter Set Delete Caused Runtime Failures

**Symptoms:** A previously working flow now fails with parameter resolution errors after a parameter set was deleted.

**Diagnosis:**
1. Identify flows that may have been using the deleted set. Retrieve each suspected flow definition and search stage property strings for `#SetName.ParamName#` patterns.
2. Look for unresolved `#SetName.ParamName#` expressions in stage properties.

**Fix:**
1. Recreate the parameter set with the same name and parameters using `create_parameter_set`.
2. Re-attach it to each affected flow with `attach_parameter_set_to_flow`.
3. Republish the affected flows.

For a permanent fix, remove the parameter references from the flows instead.

---

## `attach_parameter_set_to_flow` Returns `already_attached`

**Symptoms:** Tool returns `status: "already_attached"` — no change was made.

**This is not an error.** The parameter set is already registered with the flow. If you expected the constants or `external_paramsets` to be updated, they are already correct from the previous attach. You may still need to republish if you recently modified the parameter set's parameters.

---

## `update_parameter_set` Removed Existing Parameters

**Symptoms:** Parameters that existed before are missing after an `update_parameter_set` call.

**Root cause:** `parameters` is a full replacement list. If you passed only the new parameters, the existing ones were dropped.

**Fix:** The tool guards against this automatically — if your submitted list would remove existing parameters it returns an error naming the affected parameters and requires you to either include them or pass `confirm_replacement=True`. To avoid hitting the guard, fetch the current state first and merge your additions before submitting:
```
get_parameter_set(parameter_set_id=..., project_id=...)
```
Then merge your additions into the existing `parameters` list and resubmit the full list.
