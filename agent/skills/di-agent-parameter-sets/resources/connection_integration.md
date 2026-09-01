# Connection Integration for Parameter Sets

Parameter sets can be attached directly to a connection so that its property values (host, port, database name, credentials, etc.) are managed externally rather than stored as plain text. This mirrors the "Use external Parameter Sets" toggle visible in the UI next to each connection property.

When attached, the selected property values become `#paramSetName.paramName#` references. When a DataStage job runs, the engine resolves these references from the parameter set, optionally selecting a named value set (e.g. `prod`, `dev`) to switch environments.

> **Parameterizing a connection makes it unbrowsable.** Only the DataStage job runtime resolves these references. The connections API does not — it uses the stored string literally, so `discover_connection_data` and data-asset schema lookups against the connection fail:
>
> ```
> CDICO2034E: The property [host] value [#DBConfig.DB_HOST#] is not valid.
> Cause: invalid characters in hostname.
> ```
>
> Do all schema and table discovery **before** parameterizing, and prefer parameterizing a connection that flows already point at rather than one you are still exploring. There is no tool to reverse it — see [Removing Parameterization](#removing-parameterization).

---

## When to Use This

| Scenario | Approach |
|---|---|
| Same connection used in dev / test / prod with different hostnames or credentials | Attach a parameter set to the connection and create one value set per environment |
| Credentials must not be stored as plain text in the connection | Use a parameter set with `encrypted` parameters; reference them in the connection |
| Multiple flows share a connection whose endpoint changes per environment | Parameterize the connection once — all flows that use it benefit automatically |

---

## Full Workflow

Do steps 1 and 2 in this order for a reason: once step 4 runs, the connection can no longer be browsed, so anything you still need from it must be read first.

### 1. Discover what properties the connection exposes

```
inspect_project_asset(
    project_id=...,
    asset_id=<connection_id>,
    asset_type="connection",
)
```

The response lists the connection's current property names and values (passwords are redacted). Use these exact property names in `property_mappings`.

### 2. Confirm or create the parameter set

```
list_parameter_sets(project_id=..., name_filter=...)   # find an existing set
get_parameter_set(parameter_set_id=..., project_id=...) # verify parameter names
```

If the set does not exist, create it:

```
create_parameter_set(
    project_id=...,
    name="DBConfig",
    parameters=[
        {"name": "DB_HOST",   "type": "string"},
        {"name": "DB_PORT",   "type": "string"},
        {"name": "DB_NAME",   "type": "string"},
        {"name": "DB_PASS",   "type": "encrypted"},
    ],
)
```

Note: DataStage supports all 11 parameter types for connection properties; `encrypted` is recommended for passwords.

### 3. Optionally add value sets for environment switching

```
manage_value_set(
    parameter_set_id=...,
    project_id=...,
    action="add",
    value_set_name="prod",
    values={
        "DB_HOST": "prod-db.example.com",
        "DB_PORT": "5432",
        "DB_NAME": "my_database",
        "DB_PASS": "<password>",
    },
)
manage_value_set(..., action="add", value_set_name="dev", values={...})
```

### 4. Attach the parameter set to the connection

```
attach_parameter_set_to_connection(
    project_id=...,
    connection_id=...,
    parameter_set_name="DBConfig",
    property_mappings={
        "host":     "DB_HOST",
        "port":     "DB_PORT",
        "database": "DB_NAME",
        "password": "DB_PASS",
    },
)
```

The tool:
- Validates that every property name is one the connection actually has, and that every parameter name exists on the named set. Nothing is patched unless both check out.
- Sends a single PATCH that adds `"parameterized"` to `entity.flags` and sets each mapped property to `#DBConfig.DB_HOST#`, `#DBConfig.DB_PORT#`, etc.
- Patches each property at its own path, so properties you did not map are never rewritten.

A partial mapping is valid — only the listed properties are parameterized; others keep their current plain values. This matters for secrets: the connection API does not return passwords for personal-credential or vault-backed connections, so an unmapped password is left exactly as it was rather than being written back from a value the tool cannot see.

### 5. Select an environment at job runtime

When running a DataStage job that uses this connection, pass the value set in `runtime_parameters`:

```json
{
  "parameter_sets": [
    { "name": "DBConfig", "value_set": "prod" }
  ]
}
```

If no value set is specified, the parameter default values on the set are used.

---

## Reference Syntax

Connection property values are stored using the same `#setName.paramName#` syntax used in DataStage stage expressions:

```
#DBConfig.DB_HOST#
```

The UI renders parameterized property fields with a small parameter icon and displays the reference rather than the resolved value.

---

## Removing Parameterization

There is no MCP tool for removing connection parameterization. To restore a plain value, use the UI connection editor to overwrite each parameterized property with its plain value directly. When all parameterized properties have been restored, the "Use external Parameter Sets" toggle will be disabled automatically.

If a programmatic update is required (direct API call, not available via agent tools):

1. Call `inspect_project_asset(asset_type="connection")` to see the current property values and identify which ones still hold `#setName.paramName#` references.
2. Use the UI connection editor to replace each reference with the intended plain value, then save.
3. Verify the change by calling `inspect_project_asset` again and confirming no `#...#` references remain in the properties.

---

## Guardrails

- `property_mappings` keys must be properties the connection already has, and its values must be exact parameter names on the named set. The tool returns an error listing the unknown names — and the connection is left untouched — before any write.
- Use `inspect_project_asset(asset_type="connection")` to discover available property names. Property names are datasource-specific (e.g. `host`, `port`, `database` for PostgreSQL; `server`, `port`, `databasename` for Db2).
- Partial parameterization is intentional — only map the properties that should vary per environment. Leaving a property plain also keeps it readable by the connections API.
- Discovery must happen before parameterizing. A parameterized connection cannot be browsed, so `discover_connection_data` and schema lookups stop working on it.
- Value sets are DataStage only. For environment switching with StreamSets, parameterize the connection once and rely on separate parameter sets per environment.
