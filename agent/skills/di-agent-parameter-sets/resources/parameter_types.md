# Parameter Types

The `type` field of a parameter definition determines how the value is stored and validated.

## Type Table

| API value | Aliases accepted by tools | Description | Notes |
|---|---|---|---|
| `string` | — | Plain text | Default; works in both DataStage and StreamSets |
| `int64` | `integer` | 64-bit integer | DataStage only |
| `sfloat` | `float` | Single-precision float | DataStage only |
| `date` | — | Date (YYYY-MM-DD) | DataStage only |
| `time` | — | Time (HH:MM:SS) | DataStage only |
| `timestamp` | — | Date + time | DataStage only |
| `encrypted` | `multiline_encrypted_string` | Stored encrypted; masked in UI | DataStage only |
| `email` | — | E-mail address | DataStage only |
| `multilinestring` | `multiline_string` | Multi-line text | DataStage only |
| `enum` | `list` | Drop-down list | Requires `valid_values`; DataStage only |
| `path` | — | File or directory path | DataStage only |

## Rules

- **`enum` / `list`** — `valid_values` is required. The UI renders this as a drop-down. Example:
  ```json
  { "name": "ENV", "type": "enum", "valid_values": ["dev", "test", "prod"], "value": "dev" }
  ```
- **`encrypted`** — values are masked after creation; never returned in plain text.
- **StreamSets** accepts **only `string`**. All other types are silently ignored when the set is linked to a StreamSets flow.

## Parameter Dict Shape

```json
{
  "name":         "DB_HOST",       // required — parameter name, no spaces
  "type":         "string",        // required — see table above
  "value":        "localhost",     // optional default value
  "description":  "DB hostname",   // optional free-text description
  "prompt":       "Database host", // optional UI label
  "valid_values": []               // required only for enum/list
}
```

## Environment Variable Subtype

DataStage supports a special `envvar` subtype that binds a parameter to a DataStage environment variable. Specify `"subtype": "envvar"` alongside the base type. Environment variables are configured in the DataStage runtime settings — ask the user which variable to bind before using this subtype.
