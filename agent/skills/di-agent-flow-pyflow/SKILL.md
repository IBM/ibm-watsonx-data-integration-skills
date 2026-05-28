---
name: di-agent-flow-pyflow
description: "Complete API spec for pyflow, IBM's LLM-only Python DSL for authoring new batch or streaming flows on DataStage or StreamSets. The compact surface is built for high LLM authoring reliability — bootstrap here first, and fall back to the verbose engine-specific SDK only when pyflow cannot express a needed feature."
---

# Pyflow API Spec

The runtime provides `q`; do not import or instantiate. Every flow:

1. Declares sources with `q.source()` -- list only referenced columns, using exact names and types from asset metadata.
2. Calls `q.name("<snake_case_name>")` exactly once.
3. Ends with exactly one sink: `q.output(frame)`, or `q.write(frame, "symbol", operation="insert" | "overwrite" | "update")` when writing to a destination asset.

Code must contain no imports or `print()`.

## Engine Targets

The caller passes the target engine to `create_pyflow(engine=...)`; do not declare it in the code. The engine determines which Frame operations are allowed.

| Op | DataStage | StreamSets |
|---|---|---|
| `q.source()` | any count | exactly one |
| `q.output()` / `q.write()` | yes | yes |
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
q.source() -> [.filter() | .lookup()]* -> [.tumble()/.slide().agg()]? -> q.output() | q.write()
```

StreamSets windowed-agg measures support only `.sum()`.

## Symbols And Bindings

Strings passed to `q.source()`, `.lookup()`, and `q.write()` are local **symbols**. The caller binds each symbol to a catalog asset via `create_pyflow(bindings=...)`; symbols need not match catalog names. Every used symbol must be bound.

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
q.source(symbol, {"col": "type", ...}) -> Frame   # dict form; supports names with spaces/punctuation
q.source(symbol, col="type", ...) -> Frame         # kwargs form; identifier-safe names
q.name(name)                              # flow name; snake_case; exactly once
q.output(frame)                           # register final output
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

### Write Operations

`q.write()` supports row-level destination operations:

```python
q.write(frame, "target")                         # same as operation="insert"
q.write(frame, "target", operation="insert")     # append rows
q.write(frame, "target", operation="overwrite")  # replace the table's contents
q.write(frame, "target", operation="update")     # update existing rows
```

- `operation`: `"insert"` | `"overwrite"` | `"update"`.
- `"overwrite"` truncates the table before writing, so re-running a flow is idempotent. Use it when the destination should hold exactly this run's output (datastage only).
- Unsupported operations such as `"upsert"` are rejected; do not approximate them with insert or update.

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
```

**Aggregates** may appear only in `.select()` or `.group_by().agg()`. To filter on an aggregated value, aggregate first, then `.filter(...)`.

**No analytic window-over functions.** Use `.tumble()` / `.slide()` for time-windowed aggregates on StreamSets.

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
    .head(10)
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
    .select("custkey", "name", "nation", q.col("name_right").alias("region"))
)
```

StreamSets lookup; reference schema is declared inline, not via a separate `q.source()`:

```python
orders = q.source("orders", {"cust_id": "i64", "amount": "f64"})
q.name("orders_with_customer")
q.output(
    orders
    .filter(q.col("amount") > 0)
    .lookup("customer", {"cust_id": "i64", "name": "string"}, on="cust_id")
)
```

StreamSets windowed aggregate on an event-time column:

```python
events = q.source("events", {"region": "string", "amount": "f64", "ts": "timestamp"})
q.name("revenue_15m")
q.output(
    events
    .tumble("15m", group_by="region", on="ts")
    .agg(q.col("amount").sum().alias("revenue"))
)
```

