# Flow Integration for Parameter Sets

## Reference Syntax Quick Lookup

| Scenario | Syntax |
|---|---|
| DataStage — parameter set parameter | `#ParamSetName.ParameterName#` |
| DataStage — local parameter | `#ParameterName#` |
| DataStage — PROJDEF parameter | `#PROJDEF.ParameterName#` |
| StreamSets — parameter set constant | `${ParamSetName__ParameterName}` |

Use the exact parameter set name and parameter name — both are case-sensitive.

---

## Attaching a Parameter Set to a Flow

```
list_parameter_sets(project_id=...)                    # confirm set name
attach_parameter_set_to_flow(
    project_id=..., flow_id=...,
    engine="datastage" | "streamsets",
    parameter_set_name=...
)
```

The tool saves the registration immediately via a flow update — no further step is required for the attachment itself. Add `#setName.paramName#` (DataStage) or `${setName__paramName}` (StreamSets) expressions to stage properties via `update_datastage_flow` or the StreamSets editing tools to activate the references.

One flow can reference multiple parameter sets — call `attach_parameter_set_to_flow` once per set.

---

## DataStage: Full Linking Workflow

1. `list_parameter_sets` — confirm the set exists and note its name.
2. `attach_parameter_set_to_flow(engine="datastage", ...)` — registers the set in `external_paramsets`.
3. Edit the flow via `update_datastage_flow` (or pyflow bootstrap then SDK edit) to place `#setName.paramName#` in the relevant stage property strings. The PUT takes effect immediately.
4. At job run time, optionally select a value set:
   ```json
   { "parameter_sets": [{ "name": "DBConfig", "value_set": "prod" }] }
   ```

### PROJDEF

`PROJDEF` is a built-in **batch-only** project-level parameter set for DataStage engine settings. It is excluded from `list_parameter_sets` results but can be referenced directly in any DataStage stage expression with `#PROJDEF.ParameterName#`. It does not need to be attached to flows explicitly.

**Scope of `attach_parameter_set_to_flow`**

For DataStage flows, `attach_parameter_set_to_flow(engine="datastage", ...)` only registers a user-defined parameter set in the flow's `external_paramsets` list by adding a reference like:

```json
{ "ref": "DBConfig" }
```

It does **not** configure any additional DataStage parameter-binding modes. If a flow should read from `PROJDEF`, reference `#PROJDEF.ParameterName#` directly in the relevant stage property string.

**Environment variable bridge**

A PROJDEF parameter can be bound to a DataStage environment variable by using the `envvar` subtype. This lets a stage property read its value from a DataStage env var at run time rather than from a stored parameter value:

```json
{ "name": "DS_HOME", "type": "string", "subtype": "envvar" }
```

When the flow runs, `#PROJDEF.DS_HOME#` resolves to the runtime value of the `DS_HOME` environment variable. See [parameter_types.md](parameter_types.md) for the full `envvar` subtype spec.

---

## StreamSets: Full Linking Workflow

1. Verify the set has only `string` parameters and the name contains no `__`.
   → [streaming_limitations.md](streaming_limitations.md) for the full checklist.
2. `attach_parameter_set_to_flow(engine="streamsets", ...)` — injects constants into `pipelineConfig` and saves the attachment immediately.
3. Edit stage field expressions to use `${setName__paramName}` syntax.
4. Save or publish subsequent flow edits according to the normal StreamSets workflow.

---

## Using Parameters in Pyflow Flows

Pyflow does not have native parameter set syntax. Add parameter references after flow structure is generated:

1. Create the flow structure via `create_pyflow`.
2. Retrieve the generated SDK via `retrieve_datastage_flow_code`.
3. Attach the parameter set via `attach_parameter_set_to_flow`.
4. Edit the retrieved SDK — replace hard-coded values with `#setName.paramName#` in stage property strings.
5. Resubmit via `update_datastage_flow`.

Pyflow builds the structure; the SDK handles expression-level customisation.

---

## Auditing Parameter References in a Flow

> **Planned tool — not yet available.**
> `get_flow_parameter_references` will be added in a future milestone.

Until then, audit references manually:

1. Retrieve the flow definition (e.g. via `retrieve_datastage_flow_code`).
2. Search stage property strings for `#setName.paramName#` patterns.
3. Check `external_paramsets` in the pipeline JSON to see which sets are attached.

---

## Removing a Parameter Set from a Flow

There is no dedicated detach tool. To remove a DataStage parameter set reference:

1. `retrieve_datastage_flow_code` — get the current SDK.
2. Remove all `#setName.param#` expressions from stage properties.
3. Remove the set's entry from `external_paramsets` in the pipeline JSON.
4. Resubmit via `update_datastage_flow`.

For StreamSets: remove the `${setName__paramName}` constant entries from `pipelineConfig.constants` and redeploy.
