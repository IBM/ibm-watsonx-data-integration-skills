# Pushdown Contracts — v1

Two byte-level contracts that the optimizer
(`di-agent-query-optimization`) freezes. If you are writing a
`di-adapter-*` plug-in, emit a **workload** (input contract). If you are
building or validating the optimizer's downstream artifact, use the
**optimized pushdown plan** (output contract).

```
        NL ──► di-agent-query-substrait ──► raw Substrait ──┐
                                                            │
        SQL text or SQL file ─────────────────────────────► │
                                                            ├──► optimizer ──► optimized pushdown plan (Substrait) ──► flow skill
        custom-format file ──► di-adapter-* ──► workload JSON
```

The optimizer accepts **three input forms** that produce two byte-level
shapes at its boundary:

- **Raw Substrait plan** (from `di-agent-query-substrait` on the NL path)
- **SQL text or SQL file** (handled directly inside the optimizer; no
  envelope is constructed)
- **Workload JSON** (from a `di-adapter-*` plug-in handling a
  custom-format file)

It emits **one output format**: the optimized pushdown Substrait plan.

## Output contract — Optimized pushdown Substrait plan v1

What the optimizer emits and the flow skill consumes. The load-bearing
boundary; downstream consumers depend on these invariants.

### Schema

```json
{
  "version": {"minorNumber": 55, "producer": "di-agent-query-optimization"},
  "extensionUris": [{
    "extensionUriAnchor": 1,
    "uri": "urn:datastage:substrait:extensions:full-pushdown-sql"
  }],
  "relations": [{
    "root": {
      "names": ["<output_col_1>", "..."],
      "input": {
        "read": {
          "common": {
            "direct": {},
            "advancedExtension": {
              "enhancement": {
                "nodeKind": "source_full_pushdown_read | target_full_pushdown_read",
                "sqlStatement": "<see per-mode rules below>",
                "beforeSqlStatement": "<target only; null for source>",
                "parameters": ["<NORMALIZED_PARAM_NAME>", "..."],
                "flow_metadata": {
                  "suggested_flow_name": "<always set per the resolution chain>",
                  "parameter_defaults": {"<NAME>": "<default>"},
                  "parameter_bindings": {
                    "<NAME>": {
                      "source_syntax": "<original placeholder, optional for ${NAME}>",
                      "binding": "local | parameter_set",
                      "type": "string",
                      "usage": "identifier | literal | unknown",
                      "description": null,
                      "parameter_set_name": null,
                      "parameter_name": null,
                      "value_set": null,
                      "runtime_value": null
                    }
                  },
                  "runtime_hints": {
                    "schedule": null,
                    "tags": [],
                    "concurrency_group": null
                  }
                }
              }
            }
          },
          "baseSchema": {
            "names": ["<output_col_1>", "..."],
            "struct": {"types": [/* Substrait type objects */]}
          },
          "advanced_extension": {
            "optimization": [{
              "@type": "type.di.ibm.com/com.ibm.di.substrait.Optimization",
              "connection_id": "<UUID>"
            }]
          }
        }
      }
    }
  }]
}
```

### Per-mode rules

**`source_full_pushdown_read`** (source full pushdown):

- `sqlStatement` non-empty. May be a block ending in `SELECT`. The trailing `SELECT` supplies the flow's output rows.
- `beforeSqlStatement` is `null` or omitted.
- `root.names` / `baseSchema.names` / `baseSchema.struct.types` describe the trailing SELECT's output, by position.

**`target_full_pushdown_read`** (target full pushdown):

- `beforeSqlStatement` non-empty. Carries the workload (INSERT, UPDATE, COPY, etc.). Executed via the connector's before-SQL property.
- `sqlStatement` non-empty, read-only `SELECT`. Chosen by the precedence in the optimizer SKILL.md "Target observability SELECT" section (adapter → script-trailing → LLM → dummy).
- `root.names` / `baseSchema.names` / `baseSchema.struct.types` describe the `sqlStatement`'s output, by position.

### Invariants the flow skill validates

- exactly one top-level relation; relation contains `root.input.read`;
- `nodeKind` ∈ `{source_full_pushdown_read, target_full_pushdown_read}`;
- `connection_id` present and a non-empty UUID;
- `root.names.length == baseSchema.names.length == baseSchema.struct.types.length`;
- per-mode `sqlStatement` / `beforeSqlStatement` rules above;
- `sqlStatement` trailing SELECT aliases match `root.names` exactly after sanitization;
- `flow_metadata.suggested_flow_name` set and matches `^[a-zA-Z][a-zA-Z0-9_]{0,59}$`;
- every key in `flow_metadata.parameter_defaults` corresponds to a
  normalized name in `enhancement.parameters`;
- every key in `flow_metadata.parameter_bindings` corresponds to a
  normalized name in `enhancement.parameters`; every
  `parameter_set` binding has `parameter_set_name` and
  `parameter_name`; when `value_set` is non-null the flow skill must
  verify the named value set exists in the retrieved `ParameterSet`
  before calling `flow.set_runtime_value_set()`. When `runtime_value`
  is non-null the flow skill must set it with
  `flow.set_runtime_parameter_value()` for `parameter_set` bindings or
  `flow.set_runtime_local_parameter()` for `local` bindings.

### Flow-name resolution chain

The optimizer fills `flow_metadata.suggested_flow_name` using this
precedence:

1. User-supplied (explicit prompt or batch driver arg).
2. Adapter-supplied via the input workload's `flow_metadata.suggested_flow_name`.
3. Derived from `source.ref` — strip path, strip recognized extensions, sanitize.
4. Derived from the input filename when the optimizer was given a file path with no adapter match.
5. Last resort — `pushdown_<short_hash_of_sql>`.

Extension strip list (applied in order, repeatedly):
`.snowsql.ctl`, `.ctl`, `.snowsql`, `.sql.j2`, `.sql`, `.j2`.

After stripping, sanitize: replace any character outside `[a-zA-Z0-9_]`
with `_`, collapse repeats, prepend `flow_` if the result does not start
with a letter, truncate to 60 chars.

## Input contract — Workload JSON v1

What `di-adapter-*` plug-ins produce when handling custom-format files.
Plain JSON, **not Substrait**. The optimizer is the only consumer.

SQL text and SQL file inputs do **not** become workload JSON — the
optimizer feeds them directly to its SQL-text probe. This contract
exists for adapter outputs only.

### Schema

```json
{
  "schema_version": "pushdown-workload-v1",
  "dialect": "snowflake | db2 | databricks | postgresql | ...",
  "source": {"kind": "script|nl|flow|other", "ref": "<filename or id>"},
  "connection_id": "<UUID or empty string>",
  "rawSqlStatement": "<one SQL string; multiple statements may be ;-separated>",
  "parameters": ["PARAM_NAME", "..."],
  "hints": {
    "force_mode": null,
    "observability_select": null,
    "observability_schema": null,
    "row_count_select": null,
    "notes": []
  },
  "flow_metadata": {
    "suggested_flow_name": null,
    "parameter_defaults": {},
    "parameter_bindings": {},
    "runtime_hints": {
      "schedule": null,
      "tags": [],
      "concurrency_group": null
    }
  }
}
```

### Field rules

- `schema_version` must be exactly `"pushdown-workload-v1"`. This is how
  the optimizer distinguishes a workload from a raw Substrait plan.
- `dialect` required, lowercase.
- `source` — `kind` ∈ `{script, nl, flow, other}`; `ref` is a filename,
  opaque ID, or short identifier.
- `connection_id` — UUID if known, empty string otherwise. The optimizer
  or user resolves it before emitting the optimized plan.
- `rawSqlStatement` required. Single string. Multiple statements joined
  with `;`. The optimizer's SQL-text probe splits and parses.
- `parameters` — normalized parameter names present in
  `rawSqlStatement`. Adapters should preserve placeholders literally in
  their source syntax and describe non-`${NAME}` forms in
  `flow_metadata.parameter_bindings`.
- `hints` (all optional):
  - `force_mode` ∈ `{"source_full", "target_full", null}` — resolves
    source/target ambiguity. Cannot upgrade a non-pushdown workload.
  - `observability_select` — read-only SELECT for target pushdown.
    When set, `observability_schema` **MUST** also be set.
  - `observability_schema` — `{"names": [...], "types": [<Substrait
    type objects>]}`. Positions match the SELECT's output columns.
  - `row_count_select` — deprecated alias for `observability_select`.
    `observability_select` wins on collision.
  - `notes` — array of human-readable strings.
- `flow_metadata`:
  - `suggested_flow_name` — string identifier matching
    `^[a-zA-Z][a-zA-Z0-9_]{0,59}$`, or `null` to let the framework
    derive from `source.ref`.
  - `parameter_defaults` — object keyed by names that appear in
    `parameters`; values populate DataStage local flow parameter
    defaults. For `parameter_set` bindings, these values are treated as
    member-level runtime overrides unless `runtime_value` is supplied.
  - `parameter_bindings` — optional object keyed by names that appear
    in `parameters`. Each binding can specify `source_syntax`,
    `binding` (`local` or `parameter_set`), `type`, `usage`
    (`identifier`, `literal`, or `unknown`), `description`,
    `parameter_set_name`, `parameter_name`, `value_set`, and
    `runtime_value`. Use this field when an adapter detects
    source-specific parameter syntax or when the user requested a local
    parameter or parameter set.
  - `runtime_hints` — advisory only. `schedule` (string), `tags`
    (string array), `concurrency_group` (string).

### Adapter conformance checklist

Before returning the workload, verify:

- [ ] `schema_version` is exactly `"pushdown-workload-v1"`.
- [ ] `dialect` is set (lowercase).
- [ ] `rawSqlStatement` is a non-empty string.
- [ ] `parameters` lists every normalized parameter that appears in
      `rawSqlStatement`.
- [ ] For every parameter whose source syntax is not exactly
      `${NAME}`, `flow_metadata.parameter_bindings[NAME].source_syntax`
      identifies the original placeholder form or the adapter provides
      equivalent rewrite metadata.
- [ ] If `hints.observability_select` is set, `hints.observability_schema`
      is also set with matching `names` / `types` array lengths.
- [ ] Every key in `flow_metadata.parameter_defaults` (when set) appears
      in the `parameters` array.
- [ ] Every key in `flow_metadata.parameter_bindings` (when set)
      appears in the `parameters` array; every `parameter_set` binding
      includes `parameter_set_name` and `parameter_name`.
- [ ] If `flow_metadata.suggested_flow_name` is set, it matches
      `^[a-zA-Z][a-zA-Z0-9_]{0,59}$`.

## Raw Substrait input (NL path)

When the input is a raw Substrait plan (produced by
`di-agent-query-substrait` from a natural-language query), the
optimizer uses it as-is and runs the relation-tree probe. There is no
workload-JSON translation step on this path. The classification rules
and per-mode emission are the same regardless of which probe ran.

## Versioning

- Workload JSON: `pushdown-workload-v1`.
- Optimized pushdown plan: `compact-pushdown-substrait-v1` —
  `full-pushdown-sql` extension URI plus `nodeKind` ∈ the v1 set.

Additive changes (new optional fields, new `kind` enum values) do not
bump the version. Breaking changes (renamed fields, removed invariants,
new required fields) bump to v2 with a deprecation window on the
optimizer's input.
