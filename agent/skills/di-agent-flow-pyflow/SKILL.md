---
name: di-agent-flow-pyflow
description: "API spec for pyflow, IBM's LLM-optimized Python DSL for authoring DataStage and StreamSets flows. Its compact surface and compile-time validation offer context efficiency, fast feedback, and correctness guarantees. Load this only after the di-agent-flow-lifecycle router has selected the pyflow authoring backend — this is a language reference, not a decision about whether to use it. If you have not routed yet, load di-agent-flow-lifecycle instead."
---

# Pyflow API Spec

> **Routing lives elsewhere.** Whether a request should be authored in pyflow or the DataStage SDK, and whether it is a create or an edit, is decided by the `di-agent-flow-lifecycle` skill (AUTHOR state). This file is the pyflow language reference and the mechanics of using it. Before working with flows, you must load the `di-agent-flow-lifecycle` skill. Do not write any Pyflow code before loading the lifecycle skills.


## Usage Guidance

Pyflow is *declarative* intent; the pyflow compiler lowers the DSL to an engine-specific *imperative* flow, producing an accurate functional plan for what you declare. You express the user's **goal**; the compiler picks the stages and the wiring. That is why pyflow needs no stage-level DataStage expertise to use.

The compiler validates your flow and gives detailed compile-time feedback *before* any asset is published, guarantees correctness, and sets up connection metadata for you — all at a fraction of the tokens of the SDK. The result is a pyflow-native flow that round-trips cleanly for later edits.

**Pyflow's value is building structure** — sources, joins, filters, and the wiring between them — the expensive, error-prone part to hand-author in the SDK. Expressions and stage properties are cheap to add in the SDK *once the structure exists*.

**Do not abandon pyflow because one function or stage isn't supported.** A flow that needs, say, a regex extraction pyflow lacks still starts in pyflow: bootstrap the sources, filter, and join, then splice the missing piece into the generated SDK. Hand-authoring a new join or source from scratch is the SDK's least reliable path — never do it when pyflow can scaffold it.

### Creating vs. overwriting a flow

`create_pyflow` has two modes, selected by `replace_flow_id`:

- **`replace_flow_id` omitted** — creates a NEW flow. Use this only when no target flow exists.
- **`replace_flow_id=<flow_id>`** — recompiles the DSL and overwrites that flow **in place**, keeping its id and name. This is how you redo, fix, or regenerate a flow that already exists. Because the id survives, jobs pointing at the flow keep working, and no duplicate asset is created.

Re-calling `create_pyflow` without `replace_flow_id` to "redo" an existing flow mints a second asset. Never delete a flow in order to recreate it.

Because an overwrite preserves the existing name, the rename step below applies to fresh creates only.

### Bootstrap-then-splice mechanics

When pyflow can build the backbone but not the last detail:

1. Bootstrap the structure in pyflow — sources, filters, joins, wiring — with `create_pyflow`.
2. `retrieve_datastage_flow_code` to read the generated SDK.
3. Precision-edit that SDK to add what pyflow couldn't express (an expression, a property, an extra custom / Buildop / Java stage) and resubmit the whole body via `update_datastage_flow`.

**SDK code is verbose** — manual node linking, schema propagation, and both visible and hidden properties. Writing structure from scratch without a working reference is highly error-prone; pyflow generates it correctly wired, leaving only small, local edits.

### Where pyflow stops

The known gaps live in one place: `di-agent-flow-lifecycle/references/registry.md`, under this backend's "Known gaps" headings, split into **blocking** (pyflow cannot lay a usable backbone — go to the SDK for the create) and **spliceable** (pyflow builds the flow, one local stage or property is added afterwards). That split is a routing decision and belongs to the router, not here.

There is deliberately no list of what pyflow *supports*. pyflow is declarative — you express the goal and the compiler chooses the stages — so a supported-stage table cannot be kept true, differs per engine, and invites the wrong question. The question is whether pyflow can express the request, and the engine op tables below answer it directly.

### Editing an existing flow

- **Adds or alters structure** (a new source, a join, a different shape) -> bootstrap that structure in pyflow, then precision-edit anything pyflow can't express — an expression, a property, even an extra custom / Buildop / Java stage — onto the generated SDK. Pyflow wires the backbone reliably; you splice the rest in after.
- **Only expressions or properties on existing structure**, no new wiring -> edit the retrieved SDK in place.
- **The core shape has no faithful pyflow form**, so a bootstrap would yield a scaffold you'd have to *rewire* rather than add to -> bootstrap the closest shape pyflow can produce, then reshape the generated SDK via `update_datastage_flow`. A missing stage alone never qualifies as "no pyflow form", since stages splice in after (above).

## Code Anatomy

The runtime provides `q`; do not import or instantiate. Every flow:

1. Declares sources with `q.source()` -- list only referenced columns, using exact names and types from asset metadata. **At least one column must be provided** — `q.source("sym")` with no columns is a compile error.
2. Calls `q.name("<snake_case_name>")` exactly once.
3. Ends with exactly one sink: `q.output(frame)`, or `q.write(frame, "symbol", operation="insert" | "overwrite" | "update" | "create")` when writing to a destination asset. `operation="create"` is DataStage-only.

Code must contain no imports or `print()`.

### The `q` variable — do not reassign it

`q` is the global DSL handle. **Never assign a source result back to `q`.**

```python
# ✗ WRONG — q is now a Frame; q.col(), q.name(), q.output() all break
q = q.source("orders", id="i64", amount="f64")

# ✓ CORRECT — source result goes to a new variable
orders = q.source("orders", id="i64", amount="f64")
q.name("my_flow")
q.output(orders, name="out")
```

`q` has exactly the methods listed in the `q` Namespace section. It has no `.lit()`, `.sum()`, `.avg()`, `.max()`, `.round()`, `.row_number()`, `.select()`, or any other method not shown there. Aggregates, window functions, and scalar ops live on `Expr` objects returned by `q.col(...)`, not on `q` itself.

## Engine Targets

The caller passes the target engine to `create_pyflow(engine=...)`; do not declare it in the code. The engine determines which Frame operations are allowed.

| Op | DataStage | StreamSets |
|---|---|---|
| `q.source()` / `q.debug_source()` | any count | exactly one |
| `q.output()` / `q.sink()` / `q.write()` | yes | yes |
| `.filter()`, `.sort()` | yes | yes |
| `.lookup()` | no | yes |
| `.tumble()` / `.slide().agg()` | no | at most one |
| `.select()` / `.with_columns()` | yes | yes |
| `.head()` / `.fetch()`, `.unique()` | yes | no |
| `.union()`, `.intersect()` | yes | no |
| `.group_by().agg()` | yes | no |
| `.join()`, `.cross()` | yes | no |

StreamSets flows must be a single linear chain:

```
q.source() | q.debug_source() -> [.filter() | .lookup()]* -> [.tumble()/.slide().agg()]? -> q.output() | q.write() | q.sink()
```

StreamSets windowed-agg measures support only `.sum()`.

## Symbols And Bindings

Strings passed to `q.source()`, `.lookup()`, and `q.write()` are local **symbols**. The caller binds each symbol to a data source via `create_pyflow(bindings=...)`; symbols need not match catalog names. Every used symbol must be bound.

**Name each symbol after the asset it binds to** — `q.write(frame, "orders_augmented")`, not `q.write(frame, "target")`. `"target"` and `"source"` are placeholders in the examples below, not names to copy: they compile fine but leave the code and the bindings map unreadable, since nothing but the asset id then says where the rows land. Reuse the destination asset's own name whenever you have it.

Each binding value is one of:

- **Registered data asset** — a data asset UUID, e.g. `{"<symbol>": "<data_asset_id>"}`. Resolved to its connection and schema automatically.
- **Direct connection use** — bind straight to a table or file you found with `discover_connection_data`, even when it is *not* a registered data asset. Write it as `"<connection_id>:<path>"`, using the `path` exactly as `discover_connection_data` returned it:

  ```
  {"<symbol>": "<connection_id>:/<SCHEMA>/<TABLE>"}
  ```

Do **not** put column lists in the binding. For database tables the schema comes from your typed `q.source()` declarations; for files it is fetched automatically. As always, declare in `q.source()` only the columns the flow actually uses.

### Resolving a binding — prefer data assets

When you need to bind a symbol to a data source, **always try `list_data_assets` first** before walking any connection:

1. Call `list_data_assets(project_id=<project>, entity_name="<table or file name>")`.
2. If a matching asset is returned, use its UUID as the binding — `{"<symbol>": "<data_asset_id>"}`. The compiler resolves the connection and schema automatically; skip `discover_connection_data` entirely.
3. **Only if `list_data_assets` returns no match** (the table is not a registered project asset) should you fall back to `discover_connection_data`: walk the relevant connection (connection → schema → table) and bind `"<connection_id>:/<SCHEMA>/<TABLE>"`.

This order matters: data asset bindings carry richer metadata, are faster to resolve at compile time, and avoid unnecessary connection traversal. Use `discover_connection_data` only as a last resort when no data asset exists for the source.

### Local Parameters `[datastage]`

A direct connection binding path may contain DataStage local-parameter tokens in the form `#name#`. At job runtime DataStage substitutes each token with the parameter's current value, so the same compiled flow can read from or write to different tables without being recompiled.

Pass `parameters` to `create_pyflow` to declare each token and its default value:

```python
# DSL code — symbols are unchanged
orders = q.source("orders", id="i64", amount="f64")
q.name("parameterized_table_flow")
q.write(orders, "target", operation="insert")
```

```python
# create_pyflow call
bindings = {
    "orders": "conn-id:/MYSCHEMA/#src_table#",
    "target": "conn-id:/MYSCHEMA/#tgt_table#",
}
parameters = {
    "src_table": "ORDERS_2024",    # default value
    "tgt_table": "ORDERS_ARCHIVE", # default value
}
```

Rules:
- `parameters` is **DataStage-only**; passing it with `engine="streamsets"` raises an error.
- Every `#token#` that appears in any binding path **must** have a matching key in `parameters`, **unless it is a DataStage macro** (see next section). Missing non-macro entries are rejected at compile time.
- The default value may be an empty string if no sensible default exists.
- `parameters` keys that do not appear in any binding path are still registered on the flow and can be used in stage expressions via the SDK.
- Do **not** use `#token#` in data-asset UUID bindings — tokens are only meaningful inside direct connection paths.

**Overriding at runtime** — pass `runtime_parameters` to `create_job_run` without recompiling:

```python
create_job_run(
    job_ids=["<job_id>"],
    project_id="<project_id>",
    runtime_parameters={
        "local_parameters": {
            "src_table": "ORDERS_2025",
            "tgt_table": "ORDERS_ARCHIVE_2025",
        }
    }
)
```

### Parameter Sets `[datastage]`

A **parameter set** is a project-level asset that groups named parameters together. In binding paths, parameter-set parameters are referenced using a **dotted token**: `#setname.paramname#`. The dot between the set name and the parameter name is what distinguishes a parameter-set reference from a local parameter (`#name#`, no dot).

Unlike local parameters, parameter sets are **not declared in `parameters`** — `create_pyflow` detects every `#setname.paramname#` token in the bindings automatically, validates that the set and each referenced parameter exist in the project, and attaches the set to the compiled flow.

**The parameter set must already exist before calling `create_pyflow`.** Use `create_parameter_set` to create it first, then `list_parameter_sets` to confirm the name.

> **Do NOT call `attach_parameter_set_to_flow` after `create_pyflow` when the flow was created with `#setname.paramname#` binding tokens.** The compiler attaches the set as part of compilation. Calling `attach_parameter_set_to_flow` afterwards is always redundant — the tool will return `status: already_attached` and do nothing. Only call `attach_parameter_set_to_flow` when adding a parameter set to a flow that was created without any binding tokens referencing that set.

```python
# DSL code — unchanged from any other flow
orders = q.source("orders", id="i64", amount="f64")
q.name("env_paramset_flow")
q.write(orders, "target", operation="insert")
```

```python
# create_pyflow call — no 'parameters' argument needed for the set
bindings = {
    "orders": "conn-id:/#EnvParams.SCHEMA#/#EnvParams.SRC_TABLE#",
    "target": "conn-id:/#EnvParams.SCHEMA#/ORDERS_ARCHIVE",
}
# EnvParams is a project parameter set with at least SCHEMA and SRC_TABLE parameters.
# No entry in 'parameters' is needed — the tool handles everything automatically.
```

Mixing parameter sets with local parameters in the same flow is supported:

```python
bindings = {
    "orders": "conn-id:/#EnvParams.SCHEMA#/#src_table#",
    "target": "conn-id:/#EnvParams.SCHEMA#/ORDERS_OUT",
}
parameters = {
    "src_table": "ORDERS_2024",   # local parameter — must be declared here
    # EnvParams is a parameter set — do NOT add its params here
}
```

**Overriding at runtime** — select a named value set or override individual parameters via `create_job_run` without recompiling:

```python
create_job_run(
    job_ids=["<job_id>"],
    project_id="<project_id>",
    runtime_parameters={
        "parameter_sets": [
            {
                "name": "EnvParams",
                "value_set": "prod",   # switch to the 'prod' value set
            }
        ]
    }
)
```

Rules:
- Parameter-set tokens (`#setname.paramname#`) are **DataStage-only** — using them with `engine="streamsets"` raises an error.
- Both the set name and the parameter name must be valid identifiers (`[A-Za-z_]\w*`). Invalid names are rejected at compile time.
- The parameter set **must exist** in the project before calling `create_pyflow`. Missing sets or misspelled parameter names are rejected at compile time with a descriptive error listing what is available.
- **Do not** add parameter-set parameter names to `parameters`. The dotted syntax (`#set.param#`) is how the tool tells them apart from local parameters (`#name#`).
- Multiple parameter sets may be referenced in a single flow — all are validated and attached.
- Parameter-set tokens can be freely combined with local parameters (`#name#`) in the same binding path.

### DataStage Macros `[datastage]`

DataStage **macros** are built-in global parameters whose values are resolved automatically by the parallel engine at job start — they do not require any entry in `parameters`. Use them in direct connection binding paths the same way as local parameters (with `#…#` delimiters), but **never** add them to the `parameters` map.

```python
# DSL code — unchanged
orders = q.source("orders", id="i64", amount="f64")
q.name("macro_demo_flow")
q.write(orders, "target", operation="insert")
```

```python
# create_pyflow call — no entry in parameters for the macro
bindings = {
    "orders": "conn-id:/MYSCHEMA/#DSProjectName#_ORDERS",
    "target": "conn-id:/MYSCHEMA/#tgt_table#",
}
parameters = {
    "tgt_table": "ORDERS_ARCHIVE",  # local parameter — must be declared
    # Do NOT add DSProjectName here — it is a macro, not a local parameter
}
```

**Available macros:**

| Macro | Value injected at runtime |
|---|---|
| `#DSFlowName#` | Name of the DataStage flow |
| `#DSHostName#` | Hostname of the engine tier |
| `#DSJobName#` | Name of the job |
| `#DSJobStartDate#` | Job start date (`YYYY-MM-DD`) |
| `#DSJobStartTime#` | Job start time (`HH:MM:SS`) |
| `#DSJobStartTimestamp#` | Job start date and time combined |
| `#DSJobWaveNo#` | Wave (invocation) number of the current job run |
| `#DSProjectName#` | Name of the DataStage project |
| `#DSProjectDirectory#` | Filesystem path of the project directory on the engine |
| `#DSProjectId#` | Unique ID of the DataStage project |
| `#DSJobRunId#` | Unique ID of the current job run |
| `#DSJobId#` | Unique ID of the job |
| `#DSJobController#` | Hostname of the job controller process |

Rules:
- Macros are **DataStage-only** — they have no meaning on StreamSets.
- Do **not** declare macro names in `parameters`. The validator will accept them without a declaration and will raise an error if you try to declare one (it would be ignored at runtime anyway).
- Macros can be combined with local-parameter tokens in the same path, e.g. `"conn-id:/#DSProjectName#/#src_table#"`.
- Macro names are **case-sensitive** — use the exact capitalisation shown in the table above.

## Types

```
i8  i16  i32  i64       signed integers
f32  f64                floating point
string  boolean         text, true/false
date  time  timestamp   temporal
```

Python literals auto-convert: `int -> i64`, `float -> f64`, `str -> string`, `bool -> boolean`. Never write nullable suffixes (`?`) in DSL code; suffixes appear only in catalog metadata.

## `q` Namespace

`q` exposes only the methods listed here. **Do not call any other method on `q`** — there is no `q.lit()`, `q.sum()`, `q.avg()`, `q.max()`, `q.round()`, `q.row_number()`, `q.select()`, `q.datediff()`, or any free aggregate/scalar function. All of those live on `Expr`, accessed via `q.col(name).method()`.

```python
q.source(symbol, {"col": "type", ...}) -> Frame   # dict form; supports names with spaces/punctuation; at least one column must be provided
q.source(symbol, col="type", ...) -> Frame         # kwargs form; identifier-safe names; at least one column must be provided
q.source(symbol, col="type", ..., schema_metadata={...}) -> Frame  # with schema metadata (Kafka/StreamSets)
q.debug_source()                          # debug source stage for development: Dev Raw Data Source
q.name(name)                              # flow name; snake_case; exactly once — see Flow Naming below
q.output(frame, name)                     # register final output; required name; no other kwargs accepted
q.sink()                                  # register destination stage to discard incoming records
q.write(frame, symbol, operation="insert"|"overwrite"|"update"|"create")  # write final output to destination
q.col(name) -> Expr                       # column reference — use this, not frame['col'] or frame.col(name)
q.count_star() -> Expr                    # count-all `[datastage]`; use in .select() or .group_by().agg()
q.cast(value, type) -> Expr               # typed literal or expr cast; null: q.cast(None, "f64")
q.when(cond).then(val)...                 # see Conditional
q.concat(*exprs) -> Expr                  # string concat; 2+ args
q.date_diff(d1, d2) -> Expr               # day difference as i64 — note: date_diff, not datediff
q.strptime_time(expr, fmt) -> Expr        # string -> temporal; fmt is a strftime-style format
q.strftime(expr, fmt, tz?) -> Expr        # temporal -> string; tz is an IANA name
```

### Sink Operations / Trash Destination Stage Handling Instructions

The Trash destination is a sink that discards all incoming records. Thus, no schema is required and no data asset needs to be referenced.

Pyflow Code - for example:

```python
source_data = q.source("pg_table", {"id":"i32", "name": "string"})

# Name the flow
q.name("pg_discard")

# Sink to Trash
q.sink(source_data)
```

### Source Schema Metadata `[streamsets]`

For Kafka sources on StreamSets, optionally specify schema registry metadata:

```python
q.source(symbol, col="type", ..., schema_metadata={"subject": "...", "format": "..."})
```

**Parameters:**
- `schema_metadata`: Optional dict with schema registry information:
  - `"subject"`: Schema registry subject name (only used when format is AVRO; defaults to `{symbol}-value`)
  - `"format"`: Data serialization format - `"AVRO"`, `"JSON"`, or `"PROTOBUF"` (defaults to `"AVRO"`)

**Behavior:**
- **No schema registry lookups are performed.** All values are either explicitly provided or use defaults.
- **`schema_subject` is only used when format is AVRO.** For JSON/PROTOBUF, the subject is ignored.
- If `schema_metadata` is not provided: format defaults to `"AVRO"`, subject defaults to `{topic}-value`
- If only `"subject"` is provided: format defaults to `"AVRO"`, subject is used
- If only `"format"` is provided: format is used; if AVRO, subject defaults to `{topic}-value`

**Examples:**

```python
# AVRO with custom subject (subject is used)
orders = q.source("orders",
                  order_id="i64",
                  amount="f64",
                  schema_metadata={
                      "subject": "orders-value-v2",
                      "format": "AVRO"
                  })

# JSON format (subject is ignored even if provided)
orders = q.source("orders",
                  order_id="i64",
                  amount="f64",
                  schema_metadata={"format": "JSON"})

# Subject only (format defaults to AVRO, subject is used)
orders = q.source("orders",
                  order_id="i64",
                  amount="f64",
                  schema_metadata={"subject": "orders-value-v2"})

# No metadata (format defaults to AVRO, subject defaults to "orders-value")
orders = q.source("orders", order_id="i64", amount="f64")
```

**Use Cases:**
- Network policies prevent schema registry access during compilation
- Custom AVRO schema subject naming that doesn't follow `{topic}-value` convention
- Explicit control over data formats (AVRO, JSON, PROTOBUF)

### Output Operations

`q.output()` registers a frame as the flow's final output and creates a file data asset in the project that contains the frame's full data:

```python
q.output(frame, name="my_output")
```

`name` is required. The output file is named `{name}.csv` and is overwritten on each run. Use `q.sink(frame, name)` for the same effect; omitting `name` from `q.sink()` produces an unpredictable filename — use `target_info[].target_path` from the `create_pyflow` response to find it.

To find the output asset after a run, call `list_data_assets` with `entity_name={name}.csv`. If nothing is returned, the run has not completed yet.

`read_data_preview` returns **at most 100 rows**. The asset holds the frame's full data; the tool shows a sample of it and reports `row_count` and `truncated`. When `truncated` is true, do not present those rows as the complete result and do not count them to answer "how many rows" — the real count is `rows_written` from `poll_datastage_job`, the engine's own count of what it wrote.

Preview the asset named in `create_pyflow`'s `target_info[].target_path`, not a source table. If reading the output asset fails, say so rather than describing an input table as the result.

### Write Operations

`q.write()` writes to a catalog asset (connection-backed table) using a binding symbol:

```python
q.write(frame, "target")                         # same as operation="insert"
q.write(frame, "target", operation="insert")     # append rows
q.write(frame, "target", operation="overwrite")  # replace the table's contents
q.write(frame, "target", operation="update")     # update existing rows
q.write(frame, "target", operation="create")     # create a new (non-existent) table from the frame's schema
```

- `operation`: `"insert"` | `"overwrite"` | `"update"` | `"create"`.
- `"create"` is supported only on DataStage targets.
- `"overwrite"` truncates the table before writing, so re-running a flow is idempotent. Use it when the destination should hold exactly this run's output (datastage only).
- Unsupported operations such as `"upsert"` are rejected; do not approximate them with insert or update.
- The `"target"` symbol is bound like any other (see Symbols And Bindings): a registered data asset UUID, or direct connection use `"<connection_id>:/<SCHEMA>/<TABLE>"` to write straight to a connection-backed table without registering a data asset.
- **Reading written data**: After running the flow, use the `read_data_preview` tool to read data from the destination connection. It returns at most 100 rows; the number written is `rows_written` from `poll_datastage_job`, not the length of the preview.

#### Create Operation Behavior

When using `operation="create"` on DataStage:

1. **Table doesn't exist**: The table will be created with the schema inferred from the frame's columns
2. **Table already exists**: Do not use `operation=create` with an existing table.
3. **Binding requirement**: Must use a direct connection binding (`"connection_id:/SCHEMA/TABLE"`) rather than a data asset ID, since the table doesn't exist in the catalog yet

**Example**:
```python
# Create a new table from source data
source = q.source("input_table", id="i64", name="string", amount="f64")
q.name("create_new_table_flow")

# Use direct connection binding for non-existent table
q.write(source, "new_table", operation="create")

# In bindings:
bindings = {
    "input_table": "existing-asset-id-123",
    "new_table": "connection-id-456:/MYSCHEMA/NEW_TABLE"  # Direct connection binding
}
```

**Schema Inference**:
- Column names and types come from the frame's schema
- Primary keys, indexes, and constraints are NOT automatically created
- For advanced table creation options, create the table manually first, then use `operation="insert"`

## Expression Methods

Operators return `Expr`, not Python bools. Use `&`/`|`/`~`, never `and`/`or`/`not`. Parenthesize each comparison: `(q.col("a") > 1) & (q.col("b") < 2)`.

```
==  !=  >  <  >=  <=    comparison -> boolean
+  -  *  /              arithmetic
&  |  ~                 and / or / not
```

```python
.alias(name)                              # snake_case
.cast(type)                               # q.col("x").cast("i32") — use for rounding/type coercion; no .round() method
.precision(n)                             # numeric precision hint for output columns; int only
.scale(n)                                 # numeric scale hint for output columns; int only
.sum()                                    # aggregate; both engines
.mean()/.avg() .count() .min() .max()     # aggregates; `[datastage]` only
.rank() .dense_rank() .row_number()       # window functions; `[datastage]` only; see Partitioning section
.is_in(v1, v2, ...)                       # or .is_in([v1, v2])
.is_null() .is_not_null()                 # null checks -> boolean;
.asc() .desc()                            # sort direction only
.nulls_first() .nulls_last()              # nulls position in sort
```

**There is no `.round()` method.** To reduce decimal places, cast to a lower-precision type: `q.col("x").cast("f32")`, or use `.precision(n).scale(n)` on the output column.

**There is no `.fillna()` or `.coalesce()` method on `Expr`.** For null replacement, use a conditional: `q.when(q.col("x").is_null()).then(0).otherwise(q.col("x"))`. For a two-argument coalesce pattern, chain `.when().then().otherwise()` the same way.

**There is no `.contains()` method directly on a column reference.** String predicates live under the `.str` accessor: `q.col("x").str.contains("pattern")`.

**Aggregates and window functions must be called on `Expr` objects** (`q.col(...).sum()`, `q.col(...).row_number()`), never on `q` directly or on a Frame. They are only valid inside `.select()`, `.group_by().agg()`, or `.partition_by().select()`.

`.precision(n)` and `.scale(n)` are chainable in any order and apply only to `f64`/`numeric`/`decimal`/`double` columns.

**They must be placed on the last `.with_columns()` or `.select()` that feeds directly into `q.output()` or `q.write()`.** Annotations placed on any earlier (intermediate) node are ignored — a warning is returned in the `create_pyflow` response when this happens.

```python
# ✓ CORRECT — annotations on the node fed directly into q.output()
q.output(
    frame.with_columns(
        q.col("amount").precision(18).scale(4),
        q.col("rate").precision(10).scale(6),
    ),
    name="result",
)

# ✓ CORRECT — annotations on the node fed directly into q.write()
q.write(
    frame.with_columns(
        q.col("amount").precision(18).scale(4),
    ),
    "target_table",
    operation="insert",
)

# ✗ WRONG — annotations set mid-pipeline; the downstream .select() strips them
intermediate = frame.with_columns(
    q.col("amount").precision(18).scale(4),  # ignored — not the last node
)
q.output(
    intermediate.select("amount", "rate"),   # annotations lost here
    name="result",
)
```

### Conditional

```python
q.when(cond).then(val)                                      # else is NULL
q.when(cond).then(val).otherwise(else_val)
q.when(c1).then(v1).when(c2).then(v2).otherwise(else_val)   # multi-branch
```

### `.str` Accessor

String methods are accessed via `.str.<method>()`, **not directly on the column reference**. `q.col("x").contains(...)` is wrong; use `q.col("x").str.contains(...)`.

```python
.str.upper()
.str.contains(s)       .str.starts_with(p)   .str.ends_with(s)
.str.like(pattern)     .str.replace(old, new)
.str.trim(chars?)      .str.rtrim(chars?)
.str.substring(start_1based, length?)
```

**Best practice:** Apply `.str.trim()` to string columns in final output results to remove leading and trailing whitespace, unless there is a clear requirement to preserve spacing or the user explicitly requests otherwise. Clean, trimmed final output is preferred by default.

## Frame Methods

```python
.filter(expr) -> Frame                    # boolean expr; no aggregates inside
.select(*exprs) -> Frame                  # bare strings become col(name); mixing plain refs with aggregates triggers implicit group-by
.with_columns(*exprs) -> Frame            # keep all input cols + add/replace; no aggregates inside; all expressions must use .alias(); no keyword-argument form
.sort(*col_refs) -> Frame                 # column refs only; bare strings sort asc; use .asc()/.desc()/.nulls_first()/.nulls_last()
                                          # nulls position defaults to nulls_first when not specified
.head(count) -> Frame                     # use .fetch(count, offset) when offset needed; not .limit()
.unique(*subset) -> Frame                 # empty subset dedupes on all columns; not .distinct() or .drop_duplicates()
.union(other) -> Frame                    # set-semantics dedup
.intersect(other) -> Frame
.partition_by(*col_refs, order_by=?) -> _PartitionBuilder  # `[datastage]` only; see Partitioning section
```

**Frame method names — do not substitute synonyms.** The following are all compile errors: `.order_by()` (use `.sort()`), `.limit()` (use `.head()`), `.distinct()` / `.drop_duplicates()` (use `.unique()`), `.left_join()` / `.right_join()` (use `.join(..., how="left")`), `.groupby()` (use `.group_by()` with underscore), `.with_column()` singular (use `.with_columns()` plural), `.agg()` directly on Frame (use `.group_by(...).agg(...)`).

**Columns are referenced via `q.col('name')`, not via subscript.** `frame['col']` is not supported — use `q.col('col')` in expressions.

**`with_columns()` takes positional `Expr` arguments, each with `.alias()` — not keyword arguments.** `frame.with_columns(new_col=q.col("x") + 1)` is wrong. Write `frame.with_columns((q.col("x") + 1).alias("new_col"))`.

**Aggregates** may appear only in `.select()` or `.group_by().agg()`. To filter on an aggregated value, aggregate first, then `.filter(...)`.

**No analytic window-over functions.** Use `.tumble()` / `.slide()` for time-windowed aggregates on StreamSets. For DataStage window functions, see Partitioning section below.

**Rolling / range-window aggregates on DataStage** (e.g. "sum of contributions within the last 27 days of each anchor row") are not a built-in operation. Express them as `.cross()` → `.filter(q.date_diff(...) <= N)` → `.group_by().agg()`. See the recipe in the Examples section.

### Join `[datastage]`

```python
a.join(b, on=, how="inner", suffix="_right") -> Frame
a.join(b, left_on=, right_on=, how="inner", suffix="_right") -> Frame
a.cross(b, suffix="_right") -> Frame
```

- `how`: `inner` | `left` | `right` | `outer` | `cross`.
- `on=` (same-name keys): right key columns are dropped. The key must be a **string** (column name), not an expression. When key names differ use `left_on=` / `right_on=`.
- `left_on` / `right_on` (different-name keys): both key columns are kept.
- Duplicate non-key right columns get `suffix` (collisions stack: `_right_right`). Rename via `q.col("x_right").alias(...)`.
- **`join()` takes exactly one positional argument (the right frame) plus keyword arguments.** `a.join(b, q.col("id") == q.col("id2"))` is wrong. Pass the join condition via `on=`, `left_on=`, or `right_on=`. If the key columns have different names, use `left_on="id", right_on="id2"`.
- **Columns passed to `left_on=` / `right_on=` must exist in the respective side** — `left_on` must name a column in the left frame; `right_on` must name a column in the right frame. If you get a "column not found" error, verify the column name against the source schema.
- **Non-equi and range joins** (inequality predicates such as `a.date <= b.date`, date-distance thresholds, or `id != id`) cannot use `.join()`, which is equi-only. Use `.cross()` to produce the Cartesian product, then `.filter()` with the inequality condition.

### Lookup `[streamsets]`

```python
m.lookup(symbol, {col: type, ...}, on=, suffix="_right") -> Frame
m.lookup(symbol, {col: type, ...}, left_on=, right_on=, suffix="_right") -> Frame
m.lookup(symbol, col=type, ..., on=) -> Frame                  # kwargs form
```

- Enriches `m` with columns read inline from the reference symbol. Do **not** declare the reference via a separate `q.source()`.
- Reference columns are the reference stage's full schema: include `on=` / `right_on=` key columns plus columns to pull through.
- Semantics: left-join-like. Unmatched rows are kept with reference columns as NULL. First match only. No `how=`.
- Key and suffix rules match `.join()` above.

### Windowed Aggregates `[streamsets]`

```python
m.tumble(length, group_by=?, tz=?, on=?).agg(*measures) -> Frame
m.slide(length, group_by=?, tz=?, on=?).agg(*measures) -> Frame
```

- `length`: `<number><unit>` where unit is `s` | `m` | `h` | `d` (e.g. `"30s"`, `"15m"`, `"1h"`).
- `group_by`: str or list of column names; omit for one global row per window.
- `tz`: IANA timezone. `on`: event-time column; omit to use processing time.
- Output columns: `[*group_by, window_start, window_end, *measure_aliases]`; `window_start` / `window_end` are `timestamp`.
- Measures: the initial StreamSets windowing compiler supports only `.sum()`. Each measure must be `.alias()`'d; no nesting.

### Partitioning `[datastage]`

```python
.partition_by(*col_refs, order_by=?) -> _PartitionBuilder
```

Partitioning configures how data is distributed and ordered for window functions like `rank()`, `dense_rank()`, and `row_number()`. Chain **only `.select()`** after `.partition_by()` — `.with_columns()` is not available on a `_PartitionBuilder`. Window functions (`.rank()`, `.dense_rank()`, `.row_number()`) are `Expr` methods called inside that `.select()`, not standalone functions on `q`. At least one partition key must be provided; for a global window with no partitioning, use a constant column (e.g., add a literal column with `q.cast(1, "i32").alias("_part")`).

```python
# Rank products by sales within each category
result = (
    sales
    .partition_by("category", order_by="amount")
    .select(
        q.col("category"),
        q.col("product"),
        q.col("amount"),
        q.col("amount").rank().alias("sales_rank")
    )
)

# Multiple partition keys and order columns
result = (
    sales
    .partition_by("region", "category", order_by=[("amount", "desc"), "date"])
    .select(
        q.col("region"),
        q.col("category"),
        q.col("product"),
        q.col("amount").row_number().alias("row_num")
    )
)
```

- **Partition keys**: Column names to partition by (distribute data into groups)
- **order_by**: Optional. Column(s) to sort within each partition. Can be:
  - Single column: `order_by="amount"`
  - List of columns: `order_by=["amount", "date"]`
  - List with direction tuples: `order_by=[("amount", "desc"), ("date", "asc")]`
- **Window functions**: `.rank()`, `.dense_rank()`, `.row_number()` evaluate within partition boundaries
- **Regular functions**: Scalar functions like `.str.upper()`, `q.strftime()`, arithmetic, etc. work normally in the same `.select()` - partitioning only affects window functions
- **Partitioning is optional**: Window functions can be used without `.partition_by()` (operates on entire dataset as one partition), though partitioning is recommended for performance and correctness

### Group-By And Aggregates-In-Select `[datastage]`

```python
.group_by(*col_refs).agg(*measures) -> Frame     # .alias() every measure
```

- `.group_by()` requires at least one column argument. For a global aggregate with no grouping key, use `.select()` with an aggregate expression instead: `t.select(q.col("x").sum().alias("total"))`.
- `.agg()` takes positional `Expr` arguments — **not keyword arguments**. `agg(total=q.col("x").sum())` is wrong. Write `agg(q.col("x").sum().alias("total"))`.
- Grouping columns must be simple column references (a bare name string or `q.col("name")`), not computed expressions. To group by a derived value, materialize it with `.with_columns()` first, then pass that column name to `.group_by()`.

Inside `.select()`, mixing plain column refs with aggregates turns the plain refs into implicit grouping keys:

```python
t.select(q.col("x").sum().alias("total"))               # global aggregate
t.select("status", q.col("x").count().alias("n"))       # grouped by status
```

For a computed grouping key, materialize it with `.with_columns()` first, then group by that column name.

## Flow Naming

The name passed to `q.name()` is used as the base flow name. To avoid collisions across repeated compilations, `create_pyflow` appends a short random suffix when it creates the flow (e.g. `my_flow` becomes `my_flow_a4bc9z1q`).

This applies to **creates only**. When `replace_flow_id` is set, the target flow keeps its existing name and `q.name()` is ignored for naming purposes — no rename is needed afterwards.

**After a fresh create, always call `rename_asset` to set the intended name** — immediately, before any job or run, and even if the flow failed to compile or a later run fails. The suffix makes the create collision-proof; it is not the flow's name, and the suffixed flow is what stays behind in the project either way. Pass the `flow_id` returned by `create_pyflow` and the name you put in `q.name()`:

```
rename_asset(
    asset_id   = "<flow_id from create_pyflow>",
    asset_type = "datastage_flow",   # "streamsets_flow" on StreamSets
    new_name   = "<the name passed to q.name()>",
    project_id = "<project_id>",
)
```

On a retry, reuse the existing flow via `replace_flow_id` rather than creating a second one to rename.

## Examples

DataStage aggregate: typed-literal filter, aggregate-in-select, then filter on the aggregated column:

```python
orders = q.source("orders", {"region": "string", "amount": "f64", "orderdate": "date"})
q.name("top_regions_2024")
q.output(
    orders
    .filter(q.col("orderdate") >= q.cast("2024-01-01", "date"))
    .select("region", q.col("amount").sum().alias("revenue"), q.count_star().alias("n_orders"))
    .filter(q.col("n_orders") > 100)
    .sort(q.col("revenue").desc())
    .head(10),
    name="top_regions_output"
)
```

DataStage chained joins; duplicate right-side names get `"_right"` and are renamed via `.alias()`:

```python
customer = q.source("customer", {"custkey": "i64", "name": "string", "nationkey": "i64"})
nation = q.source("nation", {"nationkey": "i64", "name": "string", "regionkey": "i64"})
region = q.source("region", {"regionkey": "i64", "name": "string"})
q.name("customer_geography")
q.output(
    customer.join(nation, on="nationkey")
    .select("custkey", "name", "regionkey", q.col("name_right").alias("nation"))
    .join(region, on="regionkey")
    .select("custkey", "name", "nation", q.col("name_right").alias("region")),
    name="customer_geography_output"
)
```

StreamSets lookup; reference schema is declared inline, not via a separate `q.source()`:

```python
orders = q.source("orders", {"cust_id": "i64", "amount": "f64"})
q.name("orders_with_customer")
q.output(
    orders
    .filter(q.col("amount") > 0)
    .lookup("customer", {"cust_id": "i64", "name": "string"}, on="cust_id"),
    name="orders_with_customer_output"
)
```

StreamSets windowed aggregate on an event-time column:

```python
events = q.source("events", {"region": "string", "amount": "f64", "ts": "timestamp"})
q.name("revenue_15m")
q.output(
    events
    .tumble("15m", group_by="region", on="ts")
    .agg(q.col("amount").sum().alias("revenue")),
    name="revenue_output"
)
```

DataStage window functions with partitioning:

```python
sales = q.source("sales", {"category": "string", "product": "string", "amount": "f64", "date": "date"})
q.name("ranked_products")
q.output(
    sales
    .partition_by("category", order_by=[("amount", "desc")])
    .select(
        q.col("category"),
        q.col("product"),
        q.col("amount"),
        q.col("date").strftime("%Y-%m").alias("month"),  # regular function works fine
        q.col("amount").rank().alias("sales_rank"),
        q.col("amount").row_number().alias("row_num")
    )
    .filter(q.col("sales_rank") <= 10),  # top 10 per category
    name="top_products_output"
)
```

DataStage rolling / range-window aggregate — cross-join pattern `[datastage]`:

```python
# For each anchor row, sum all contributions that fall within 27 days before it.
# The Join stage is equi-only, so a range predicate goes through .cross() + .filter().
anchors = q.source("anchors", {"id": "i64", "anchor_date": "date", "region": "string"})
contribs = q.source("contribs", {"anchor_id": "i64", "contrib_date": "date", "amount": "f64"})
q.name("rolling_27d_sum")
q.output(
    anchors
    .cross(contribs, suffix="_c")                               # full cartesian product
    .filter(
        (q.col("id") == q.col("anchor_id_c")) &                # equi predicate first (cheap filter)
        (q.date_diff(q.col("anchor_date"), q.col("contrib_date_c")) >= 0) &
        (q.date_diff(q.col("anchor_date"), q.col("contrib_date_c")) <= 27)
    )
    .group_by("id", "anchor_date", "region")
    .agg(q.col("amount_c").sum().alias("rolling_sum")),
    name="rolling_output"
)
```

Key points:
- `.cross()` is the only way to join on an inequality or date-distance predicate; `.join()` is equi-only.
- Put the equi-predicate (`id == anchor_id`) first inside `.filter()` so the engine discards non-matching pairs before evaluating the range condition.
- `q.date_diff(later, earlier)` returns a positive i64 when `later >= earlier`. Swap arguments if the sign is reversed.
- After `.filter()`, treat the result as a normal frame: `.group_by().agg()`, `.select()`, further `.join()`, etc.

## Stage Configuration `[streamsets]`

Operations support an optional `configs` parameter to pass engine-specific configuration to the underlying stage. Configs are only applied for StreamSets flows; DataStage ignores them.

```python
q.source(symbol, col="type", ..., configs={"key": "value"})
q.debug_source(configs={"key": "value"})
q.write(frame, symbol, operation="insert", configs={"key": "value"})
frame.filter(expr, configs={"key": "value"})
frame.select(..., configs={"key": "value"})
frame.with_columns(..., configs={"key": "value"})
frame.sort(..., configs={"key": "value"})
frame.lookup(symbol, {...}, on=, configs={"key": "value"})
frame.tumble(length, configs={"key": "value"}).agg(...)
frame.slide(length, configs={"key": "value"}).agg(...)
```

**Rules:**
- `configs` must be a dict with string keys and JSON-serializable values (str, int, float, bool, None, list, dict)
- Reserved keys cannot be used: `stageType`, `instanceName`, `stageName`, `uiInfo`, `inputLanes`, `outputLanes`, `eventLanes`, `services`, `configuration`
- Configs are merged into the StreamSets stage configuration after standard properties are set
- Invalid configs raise `ConfigValidationError` during compilation

**Examples:**

```python
# Source with batch size config
orders = q.source("orders_kafka",
                  order_id="i64",
                  amount="f64",
                  configs={"batchSize": 1000, "maxWaitTime": 5000})

# Debug source with rawData and dataFormat config
orders = q.debug_source(configs={"rawData":"id,total\n1,1.1\n2,2.2", "dataFormat":"CSV"})

# Write with custom buffer settings
q.write(result, "target_db",
        operation="insert",
        configs={"batchSize": 500, "connectionTimeout": 30})

# Filter with processing hints
filtered = orders.filter(
    q.col("amount") > 100,
    configs={"enableMetrics": True}
)

# Lookup with cache configuration
enriched = orders.lookup(
    "customers",
    {"cust_id": "i64", "name": "string"},
    on="cust_id",
    configs={"cacheSize": 10000, "cacheTTL": 3600}
)

# Window with custom watermark
windowed = events.tumble(
    "15m",
    group_by="region",
    on="ts",
    configs={"allowedLateness": "5m"}
).agg(q.col("amount").sum().alias("revenue"))
```