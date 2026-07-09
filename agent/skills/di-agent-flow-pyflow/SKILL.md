---
name: di-agent-flow-pyflow
description: "API spec for pyflow, IBM's LLM-optimized Python DSL for authoring DataStage and StreamSets flows. Its compact surface and compile-time validation offer context efficiency, fast feedback, and correctness guarantees, making it the ideal choice for writing flows from scratch and for editing — bootstrap any structural change (a new source, a join) here before precision-editing the SDK."
---

# Pyflow API Spec

## Usage Guidance

Pyflow is *declarative* intent; the pyflow compiler lowers the DSL to an engine-specific *imperative* flow, producing an optimized physical plan for what you declare.

**For new flows, always author with pyflow — it is the only way to create one.** The SDK surface can only update flows that already exist; there is no tool for creating a flow from SDK code. Beyond that, the compiler validates your flow and gives detailed compile-time feedback, guarantees correctness, and sets up connection metadata for you — all at a fraction of the tokens of the SDK. The result is a pyflow-native flow that round-trips cleanly for later edits.

**Pyflow's value is building structure** — sources, joins, filters, and the wiring between them — the expensive, error-prone part to hand-author in the SDK. Expressions and stage properties are cheap to add in the SDK *once the structure exists*. So the editing question is never "can pyflow express the whole flow?" but "does this change touch structure?"

### Editing an existing flow

- **Adds or alters structure** (a new source, a join, a different shape) -> bootstrap that structure in pyflow, then precision-edit anything pyflow can't express — an expression, a property, even an extra custom / Buildop / Java stage — onto the generated SDK. Pyflow wires the backbone reliably; you splice the rest in after.
- **Only expressions or properties on existing structure**, no new wiring -> edit the retrieved SDK in place.
- **The core shape has no faithful pyflow form**, so a bootstrap would yield a scaffold you'd have to *rewire* rather than add to -> bootstrap the closest shape pyflow can produce, then reshape the generated SDK via `update_datastage_flow`. A missing stage alone never qualifies as "no pyflow form", since stages splice in after (above).

**Do not abandon pyflow because one function or stage isn't supported.** A flow that needs, say, a regex extraction pyflow lacks still starts in pyflow: bootstrap the sources, filter, and join, then splice the missing piece into the generated SDK. Hand-authoring a new join or source from scratch is the SDK's least reliable path — never do it when pyflow can scaffold it.

### Recommended Workflow

1. Read the existing SDK — capture anything you must preserve (an exact expression, a stage's settings).
2. Bootstrap the structure in pyflow — sources, filters, joins, wiring.
3. Read the generated SDK.
4. Precision-edit it to add what pyflow couldn't express.

**SDK code is verbose** — manual node linking, schema propagation, and both visible and hidden properties. Writing structure from scratch without a working reference is highly error-prone; pyflow generates it correctly wired, leaving only small, local edits.

## Code Anatomy

The runtime provides `q`; do not import or instantiate. Every flow:

1. Declares sources with `q.source()` -- list only referenced columns, using exact names and types from asset metadata. At least one column must be provided.
2. Calls `q.name("<snake_case_name>")` exactly once.
3. Ends with exactly one sink: `q.output(frame)`, or `q.write(frame, "symbol", operation="insert" | "overwrite" | "update")` when writing to a destination asset.

Code must contain no imports or `print()`.

## Engine Targets

The caller passes the target engine to `create_pyflow(engine=...)`; do not declare it in the code. The engine determines which Frame operations are allowed.

| Op | DataStage | StreamSets |
|---|---|---|
| `q.source()` | any count | exactly one |
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
q.source() -> [.filter() | .lookup()]* -> [.tumble()/.slide().agg()]? -> q.output() | q.write() | q.sink()
```

StreamSets windowed-agg measures support only `.sum()`.

## Symbols And Bindings

Strings passed to `q.source()`, `.lookup()`, and `q.write()` are local **symbols**. The caller binds each symbol to a data source via `create_pyflow(bindings=...)`; symbols need not match catalog names. Every used symbol must be bound except for the symbol `dev_raw_data` since it is used for stage Dev Raw Data Source which writes raw data directly without any data asset.

Each binding value is one of:

- **Registered data asset** — a data asset UUID, e.g. `{"<symbol>": "<data_asset_id>"}`. Resolved to its connection and schema automatically.
- **Direct connection use** — bind straight to a table or file you found with `discover_connection_data`, even when it is *not* a registered data asset. Write it as `"<connection_id>:<path>"`, using the `path` exactly as `discover_connection_data` returned it:

  ```
  {"<symbol>": "<connection_id>:/<SCHEMA>/<TABLE>"}
  ```

  The object form `{"<symbol>": {"connection_id": "<connection_id>", "path": "/<SCHEMA>/<TABLE>"}}` is also accepted.

Do **not** put column lists in the binding. For database tables the schema comes from your typed `q.source()` declarations; for files it is fetched automatically. As always, declare in `q.source()` only the columns the flow actually uses.

To bind a source the user describes by connection + table (e.g. "the `<TABLE>` table in my `<database>` database"), use `discover_connection_data` to walk connection → schema → table, then bind `"<connection_id>:<path>"` — no need to register a data asset first.

## Types

```
i8  i16  i32  i64       signed integers
f32  f64                floating point
string  boolean         text, true/false
date  time  timestamp   temporal
```

Python literals auto-convert: `int -> i64`, `float -> f64`, `str -> string`, `bool -> boolean`. Never write nullable suffixes (`?`) in DSL code; suffixes appear only in catalog metadata.

## `q` Namespace

```python
q.source(symbol, {"col": "type", ...}) -> Frame   # dict form; supports names with spaces/punctuation; at least one column must be provided
q.source(symbol, col="type", ...) -> Frame         # kwargs form; identifier-safe names; at least one column must be provided
q.source(symbol, col="type", ..., schema_metadata={...}) -> Frame  # with schema metadata (Kafka/StreamSets)
q.name(name)                              # flow name; snake_case; exactly once — see Flow Naming below
q.output(frame, name)                     # register final output; required name for flat-file output
q.sink()                                  # register destination stage to discard incoming records
q.write(frame, symbol, operation="insert")  # write final output to destination
q.col(name) -> Expr                       # column reference
q.count_star() -> Expr                    # count-all `[datastage]`; use in .select() or .group_by().agg()
q.cast(value, type) -> Expr               # typed literal or expr cast; null: q.cast(None, "f64")
q.when(cond).then(val)...                 # see Conditional
q.concat(*exprs) -> Expr                  # string concat; 2+ args
q.date_diff(d1, d2) -> Expr               # day difference as i64
q.strptime_time(expr, fmt) -> Expr        # string -> temporal; fmt is a strftime-style format
q.strftime(expr, fmt, tz?) -> Expr        # temporal -> string; tz is an IANA name
```

### Dev Raw Data Source Handling Instructions

1.  If the user specifies that the source is "Dev Raw Data Source":
    *   The table_name passed to q.source() must be "dev_raw_data".
    *   The user request must include the following fields:
        a.  raw_data
        b.  data_format
2.  If either raw_data or data_format is missing:
    *   Prompt the user explicitly to provide these fields.
    *   These are required to derive the schema using the get_dev_raw_data_schema MCP tool.
3.  Schema derivation rules:
    *   Use up to the first 10 records from raw_data to infer the schema. If fewer than 10 records are available, use all of them.
4.  Supported values for data_format:
    *   "JSON"
    *   "Delimited"
    *   "Avro JSON"
5.  If the user provides any unsupported data_format:
    *   Immediately ask the user to choose one of the supported formats listed above.

Pyflow Code - for example:

```python
# Source: Dev Raw Data Source (schema to be derived from the raw_data in the request using get_dev_raw_data_schema tool)
# Note: get_dev_raw_data_schema only gets you schema for Source, for schema of target, you need to use inspect_project_asset tool
source_data = q.source("dev_raw_data", {"id":"i32", "name": "string"})

# Name the flow
q.name("dev_raw_to_pg_backup")

# Write to target table
q.write(source_data, "target_table", operation="insert")
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

`q.output()` registers a frame as the pipeline's final output and creates a file data asset in the project that contains
the frame's full data:

```python
q.output(frame, name="my_output")
```

The `name` parameter is required, but the file asset is **not** simply named `{name}.csv` — the
compiler prefixes it (`de_agent_...`) and adds a random suffix to avoid collisions. The actual
filename is returned by `create_pyflow` in `target_info[].target_path`; use that exact string,
not the `name` you passed in.

Agent-generated assets (anything matching the `de_agent_` prefix) are hidden from `list_data_assets`
by default. To discover the asset ID for this output, call `list_data_assets` with
`entity_name` set to the `target_path` from `create_pyflow` (or `starts:de_agent_<name>`) **and**
`exclude_agent_generated=False` — otherwise the search returns zero results even with the
correct name. Then use `read_file_data_asset` to retrieve the data.

### Write Operations

`q.write()` writes to a catalog asset (connection-backed table) using a binding symbol:

```python
q.write(frame, "target")                         # same as operation="insert"
q.write(frame, "target", operation="insert")     # append rows
q.write(frame, "target", operation="overwrite")  # replace the table's contents
q.write(frame, "target", operation="update")     # update existing rows
```

- `operation`: `"insert"` | `"overwrite"` | `"update"`.
- `"overwrite"` truncates the table before writing, so re-running a flow is idempotent. Use it when the destination should hold exactly this run's output (datastage only).
- Unsupported operations such as `"upsert"` are rejected; do not approximate them with insert or update.
- The `"target"` symbol is bound like any other (see Symbols And Bindings): a registered data asset UUID, or direct connection use `"<connection_id>:/<SCHEMA>/<TABLE>"` to write straight to a connection-backed table without registering a data asset.
- **Reading written data**: After running the flow, use the `read_connection_data_preview` tool to read data from the destination connection.

## Expression Methods

Operators return `Expr`, not Python bools. Use `&`/`|`/`~`, never `and`/`or`/`not`. Parenthesize each comparison: `(q.col("a") > 1) & (q.col("b") < 2)`.

```
==  !=  >  <  >=  <=    comparison -> boolean
+  -  *  /              arithmetic
&  |  ~                 and / or / not
```

```python
.alias(name)                              # snake_case
.cast(type)                               # q.col("x").cast("i32")
.sum()                                    # aggregate; both engines
.mean()/.avg() .count() .min() .max()     # aggregates; `[datastage]` only
.rank() .dense_rank() .row_number()       # window functions; `[datastage]` only; see Partitioning section
.is_in(v1, v2, ...)                       # or .is_in([v1, v2])
.is_null() .is_not_null()                 # null checks -> boolean;
.asc() .desc()                            # sort direction only
.nulls_first() .nulls_last()              # nulls position in sort
```

### Conditional

```python
q.when(cond).then(val)                                      # else is NULL
q.when(cond).then(val).otherwise(else_val)
q.when(c1).then(v1).when(c2).then(v2).otherwise(else_val)   # multi-branch
```

### `.str` Accessor

```python
.str.upper()
.str.contains(s)       .str.starts_with(p)   .str.ends_with(s)
.str.like(pattern)     .str.replace(old, new)
.str.trim(chars?)      .str.rtrim(chars?)
.str.substring(start_1based, length?)
```

**Best Practice:** Apply `.str.trim()` to string columns in final output results to remove leading and trailing whitespace, unless there is a clear requirement to preserve spacing or the user explicitly requests otherwise. Clean, trimmed final output is preferred by default.

## Frame Methods

```python
.filter(expr) -> Frame                    # boolean expr; no aggregates inside
.select(*exprs) -> Frame                  # bare strings become col(name); mixing plain refs with aggregates triggers implicit group-by
.with_columns(*exprs) -> Frame            # keep all input cols + add/replace; no aggregates inside
.sort(*col_refs) -> Frame                 # column refs only; bare strings sort asc; use .asc()/.desc()/.nulls_first()/.nulls_last()
                                          # nulls position defaults to nulls_first when not specified
.head(count) -> Frame                     # use .fetch(count, offset) when offset needed
.unique(*subset) -> Frame                 # empty subset dedupes on all columns; output keeps every column
.union(other) -> Frame                    # set-semantics dedup
.intersect(other) -> Frame
.partition_by(*col_refs, order_by=?) -> _PartitionBuilder  # `[datastage]` only; see Partitioning section
```

**Aggregates** may appear only in `.select()` or `.group_by().agg()`. To filter on an aggregated value, aggregate first, then `.filter(...)`.

**No analytic window-over functions.** Use `.tumble()` / `.slide()` for time-windowed aggregates on StreamSets. For DataStage window functions, see Partitioning section below.

### Join `[datastage]`

```python
a.join(b, on=, how="inner", suffix="_right") -> Frame
a.join(b, left_on=, right_on=, how="inner", suffix="_right") -> Frame
a.cross(b, suffix="_right") -> Frame
```

- `how`: `inner` | `left` | `right` | `outer` | `cross`.
- `on=` (same-name keys): right key columns are dropped.
- `left_on` / `right_on` (different-name keys): both key columns are kept.
- Duplicate non-key right columns get `suffix` (collisions stack: `_right_right`). Rename via `q.col("x_right").alias(...)`.

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

Partitioning configures how data is distributed and ordered for window functions like `rank()`, `dense_rank()`, and `row_number()`. Chain `.select()` after `.partition_by()` to project columns with window functions:

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

Inside `.select()`, mixing plain column refs with aggregates turns the plain refs into implicit grouping keys:

```python
t.select(q.col("x").sum().alias("total"))               # global aggregate
t.select("status", q.col("x").count().alias("n"))       # grouped by status
```

For a computed grouping key, materialize it with `.with_columns()` first, then group by that column name.

## Flow Naming

The name passed to `q.name()` is used as the base flow name. To avoid collisions across repeated
compilations, `create_pyflow` appends a short random suffix when it creates the flow
(e.g. `my_flow` becomes `my_flow_a4bc9z1q`).

If the user requested a specific name, use `rename_datastage_flow` after creation to strip the
suffix and apply it. Pass the `flow_id` returned by `create_pyflow` and the intended name:

```
rename_datastage_flow(
    flow_id    = "<flow_id from create_pyflow>",
    new_name   = "<the name passed to q.name()>",
    project_id = "<project_id>",
)
```

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
