# Value Sets

> **DataStage only.** StreamSets does not support value sets — they are silently ignored if present.

Value sets are named snapshots of parameter values within a DataStage parameter set. They let you switch between environments (dev, test, prod) at job-run time without editing the flow or the parameter set definition.

## Anatomy of a Value Set

```
ParameterSet "DBConfig"
  Parameters:  DB_HOST (string), DB_PORT (string), TIMEOUT (int64)

  Value Sets:
    "dev":   DB_HOST=dev-db,  DB_PORT=5432, TIMEOUT=10
    "prod":  DB_HOST=prod-db, DB_PORT=5432, TIMEOUT=60
```

When a job runs:
- No value set selected → parameter default values apply.
- `value_set: "prod"` in `runtime_parameters` → the `prod` snapshot overrides defaults for that run.

## Managing Value Sets

All value set operations use `manage_value_set`.

### Add a new value set

```python
manage_value_set(
    parameter_set_id="<id>",
    project_id="<project_id>",
    action="add",
    value_set_name="prod",
    values={
        "DB_HOST": "prod-db.example.com",
        "DB_PORT": "5432",
        "TIMEOUT": 60,
    }
)
```

Rules:
- Fails if a value set with that name already exists — use `action="replace"` to overwrite.
- All keys in `values` must match existing parameter names on the set.
- You do not need to include every parameter — omitted parameters use their defaults when this value set is selected.

### Replace (overwrite) a value set

```python
manage_value_set(
    parameter_set_id="<id>",
    project_id="<project_id>",
    action="replace",
    value_set_name="prod",
    values={"DB_HOST": "new-prod-db.example.com", "DB_PORT": "5433", "TIMEOUT": 60},
)
```

- If `prod` exists, its values are replaced entirely.
- If `prod` does not exist yet, it is created (upsert behaviour).

### Remove a value set

```python
manage_value_set(
    parameter_set_id="<id>",
    project_id="<project_id>",
    action="remove",
    value_set_name="dev",
)
```

- `values` is ignored for `remove`.
- Returns an error if the named value set does not exist.

## Selecting a Value Set at Job Run Time

Pass the value set name in `runtime_parameters` when calling `create_job_run`:

```json
{
  "parameter_sets": [
    { "name": "DBConfig", "value_set": "prod" }
  ]
}
```

To run without a value set (using parameter defaults), omit the `value_set` key entirely.

## Guardrails

- **Never echo secret values in responses.** When a value set contains `encrypted` parameters, confirm by parameter name only ("DB_PASS was stored") — never repeat the plaintext value in a confirmation, summary, or plan preview.
- **Parameter rename hazard:** if you rename a parameter after creating value sets, the old name remains in the value set entries and becomes orphaned — update each value set manually after renaming.
- **Parameter set rename hazard:** renaming the parameter set itself orphans all `#OldName.paramName#` references in attached flows and connection properties — those are not updated automatically.
- **Values are fully replaced per call:** a `replace` call with three keys drops any other entries that were in the set previously; always include all intended key-value pairs.
- **Concurrent modification risk:** `manage_value_set` uses a read-modify-write pattern with no locking. Do not issue two calls against the same parameter set in parallel — the second write silently overwrites the first.
- **Do not create value sets on StreamSets parameter sets** — the API does not reject them, but they have no effect at runtime.
