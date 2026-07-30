# StreamSets Limitations for Parameter Sets

StreamSets (streaming engine) has a significantly smaller parameter set feature surface than DataStage. Some violations are blocked by the tool, while others cause parameters to be skipped or ignored by the engine.

## Feature Comparison

| Feature | DataStage | StreamSets |
|---|---|---|
| Parameter types | All 11 types | `string` only |
| Value sets | ✓ | ✗ — silently ignored |
| PROJDEF | ✓ | ✗ — unsupported |
| Local parameters | ✓ | ✗ — unsupported |
| `__` in set name | Allowed | **Forbidden** — blocks attaching |
| Linking mechanism | `external_paramsets` in pipeline JSON | Constants injected into `pipelineConfig` |
| Reference syntax | `#setName.paramName#` | `${setName__paramName}` |

## Validation Checklist

Before attaching a parameter set to a StreamSets flow, verify **all** of the following:

- ✓ Parameter set name does **not** contain `__`
- ✓ Every parameter on the set has type `string`
- ✓ No value sets are needed (they have no effect)
- ✓ No dependence on PROJDEF
- ✓ No dependence on local parameters

If any item fails, resolve it before proceeding.

## What Happens When Rules Are Violated

| Violation | Outcome |
|---|---|
| Parameter type is `int64`, `date`, etc. | Parameter is skipped — constant is **not** injected |
| Parameter type is `encrypted` | Parameter is skipped |
| Value set defined on the parameter set | Value set is silently ignored at runtime |
| PROJDEF referenced in stage expression | Runtime error or unresolved reference |
| `__` in parameter set name | `attach_parameter_set_to_flow` returns an error before making any change |

## Name Restriction Explained

StreamSets uses double-underscore (`__`) as the separator in the constant key format:

```
${<paramset_name>__<param_name>}
```

A name like `My__Set` would produce ambiguous keys like `${My__Set__DB_HOST}`, making it impossible to parse which part is the set name and which is the parameter name. This is why `__` is forbidden in the set name. The `attach_parameter_set_to_flow` tool enforces this at call time.

## How Attaching Works for StreamSets

`attach_parameter_set_to_flow(engine="streamsets")` injects one pipeline constant per `string` parameter into `pipelineConfig.constants` using the key format `<paramset_name>__<param_name>`. The default value of the parameter becomes the constant's initial value.

Attaching a parameter set updates the flow immediately. No additional publish or redeploy step is required solely for the attachment. Subsequent flow edits may still require the normal StreamSets save or publish workflow.

## Workflow for StreamSets

1. Create the parameter set with only `string` parameters — no non-string types.
2. Confirm the set name contains no `__`.
3. Call `attach_parameter_set_to_flow(engine="streamsets", ...)`.
4. Edit stage field expressions to use `${setName__paramName}` syntax.
5. Save or publish those later flow edits according to the normal StreamSets workflow.

> If environment switching (dev/prod) is needed for a StreamSets flow, maintain separate parameter sets or update the constant values before each run. There is no value set equivalent for StreamSets.
