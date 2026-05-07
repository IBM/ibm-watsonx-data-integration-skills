# DSL Syntax Reference

## Primary Entity

- The DSL operates on immutable **VirtualTable** (vtable) objects
- Vtables are transformed through **Construct** expressions
- A complete DSL program consists of multiple lines of constructs transforming vtables and assigning them to new variables
- The final result must be a single vtable, which is returned on the last line

## Types

- SubstraitType = Literal['i64', 'i16', 'fp32', 'fp64', 'string', 'date', 'timestamp', 'boolean']

def NamedStruct(struct: dict[str, SubstraitType]) -> NamedStruct

## Core Rules

- Each line should contain a construct and assign the resulting vtable to a new variable name
- Expressions **must** be inlined in the construct they are used; they cannot be assigned to variables or shared
- Variables must be legal, snake_case Python identifiers
- Return final vtable object with a single `return` statement
- You can use Python `#` comments for notes and explanations

## Constructs

A construct takes in one or more vtables and parameters and outputs a new vtable.

### ReadTable(table_name: str, type: NamedStruct) -> VirtualTable

Loads a table from the catalog with a known schema.

- `table_name` : the name of the table.
- `type` : the table schema.

### Select(plan: VirtualTable, exprs: list[Expression]) -> VirtualTable

Selects and reshapes columns. Output schema contains ONLY the columns (with their new names) defined in `exprs`.

This uses SELECT semantics: the output schema is exactly what you project.

Scoping rule: expressions in `exprs` can only reference columns from the input `plan`. Aliases defined within the same
`exprs` list are NOT available to other expressions in that list; they only become referenceable after the Select
completes. If you need to reference a derived column, chain a second Select.

- `plan` : the input vtable.
- `exprs` : list of columns or computed expressions. E.g., `[col("time", "t"), add(col("a"), col("b"), alias="sum")]`

### Project(plan: VirtualTable, exprs: list[Expression]) -> VirtualTable

Projects columns while preserving all parent columns. Output schema contains ALL parent columns plus the projected columns.

This uses withColumn semantics: all original columns are preserved, and projected expressions are added/appended.

Scoping rule: same as Select - expressions in `exprs` can only reference columns from the input `plan`. Aliases defined
within the same `exprs` list are NOT available to other expressions in that list.

- `plan` : the input vtable.
- `exprs` : list of columns or computed expressions to add/append. E.g., `[col("time", "t"), add(col("a"), col("b"), alias="sum")]`

**Key Difference**: Use `Select` when you want to keep ONLY specific columns. Use `Project` when you want to keep ALL columns and ADD new derived columns.

### Filter(plan: VirtualTable, expr: Expression) -> VirtualTable

Keeps only rows matching a boolean predicate. Preserves schema.

- `plan` : the input vtable.
- `expr` : a boolean expression. E.g., `gt(col("age"), literal(18, "i32"))`

### Cross(left_plan: VirtualTable, right_plan: VirtualTable) -> VirtualTable

Creates Cartesian product (cross join) of two vtables. Output schema is union of two input schemas.

- `left_plan` : left input vtable.
- `right_plan` : right input vtable.

### Join(left_plan: VirtualTable, right_plan: VirtualTable, expr: Expression, join_type: Literal['inner', 'outer', 'left', 'right']) -> VirtualTable

Joins two vtables. Output schema is union of two input schemas.
Possible join types: inner, outer, left, right. For cross join use `Cross` construct.

- `left_plan` : left input vtable.
- `right_plan` : right input vtable.
- `expr` : join condition. E.g., `equal(col("left.p_driverId"), col("right.l_driverId"))`
- `join_type` : join type.

### Aggregate(plan: VirtualTable, grouping_exprs: list[Column], measures: list[Expression]) -> VirtualTable

Computes aggregates over groups. Output schema contains `grouping_exprs` and `measures` columns only.

- `plan` : the input vtable.
- `grouping_exprs` : list of columns to group by.
- `measures` : non-empty list of aggregation functions (e.g., `sum`, `min`). The aggregation function must not be wrapped in a cast.

Type reference:
- str_var = string/varchar
- numeric = i8/i16/i32/i64/fp32/fp64

Aggregate functions:
- `avg(x: numeric|decimal<P,S>)` -> same type (nullable, decimal promoted to decimal<38,S>)
- `sum(x: numeric)` -> same type (nullable)
- `count(x: any)` -> i64
- `min(x: any comparable)` -> same type (nullable)
- `max(x: any comparable)` -> same type (nullable)
- `any_value(x: any)` -> same type (nullable) - returns an arbitrary value from the group

Example:

```query
aggr = Aggregate(plan=flt,
                grouping_exprs=[col("raceId", alias="race_id")],
                measures=[min(col("milliseconds"))])
```

Always use alias for the grouping expressions column.

### Sort(plan: VirtualTable, exprs_order: list[tuple[Column, Literal['asc', 'desc']]]) -> VirtualTable

Sorts rows in the input vtable, using `exprs_order` as sorting keys. Preserves schema.

- `plan` : the input vtable.
- `exprs_order` : list of `(column, direction)`

### Fetch(plan: VirtualTable, offset: int, count: int) -> VirtualTable

Returns a limited number of rows. Preserves schema.

- `plan` : the input vtable.
- `offset` : rows to skip.
- `count` : rows to return.

Example:

```query
ft = Fetch(plan=sg, offset=0, count=10)
```

## Expressions

An expression returns an `Expression` object for use in constructs.

### col(name: str, alias: str = None) -> Column

`Column` is a type of `Expression`

References a column in one of the construct's input vtables.
- `name` must exactly match one of the columns in the vtable(s) passed to the construct.
- Optional alias renames it for subsequent constructs.

Examples:

```query
col("name")
col("name", "alias")
```

### literal(value: Any, type: LiteralType) -> Expression

```
type LiteralType = Literal['boolean', 'date', 'fp32', 'fp64', 'i16', 'i32', 'i64', 'interval_compound', 'interval_day', 'interval_year', 'list', 'map', 'precision_time', 'precision_timestamp', 'precision_timestamp_tz', 'string', 'struct', 'time', 'timestamp', 'timestamp_tz', 'uuid', 'varchar']
```

Creates a literal value.

Examples:

```query
literal(10, "i32")
literal("hello", "string")
literal("2020-12-20", "date")
```

### Scalar Functions

All scalar functions accept an optional `alias` arg to project the result to a new column name.

Type reference:
- str_type = string/varchar/fixedchar
- str_var = string/varchar
- integer = i8/i16/i32/i64
- float = fp32/fp64
- numeric = i8/i16/i32/i64/fp32/fp64
- temporal = timestamp/date/time

Functions:

- `trim(input: str_var, characters: str_var)` -> str_var
- `rtrim(input: str_var, characters: str_var)` -> str_var
- `starts_with(input: str_type, substring: str_type)` -> boolean
- `ends_with(input: str_type, substring: str_type)` -> boolean
- `contains(input: str_type, substring: str_type)` -> boolean
- `like(input: str_var, match: str_var)` -> boolean
- `replace(input: str_var, substring: str_var, replacement: str_var)` -> str_var
- `concat(...input: str_var)` -> str_var
- `substring(input: str_type, start: i32, length?: i32)` -> str_var
- `upper(input: str_type)` -> str_type
- `strptime_time(time_string: string, format: string)` -> time
- `strftime(x: temporal, format: string, timezone?: string)` -> string
- `add(x: numeric, y: numeric)` -> same type as x
- `add(x: timestamp|date, y: interval)` -> same type as x
- `subtract(x: numeric, y: numeric)` -> same type as x
- `subtract(x: timestamp|date, y: interval)` -> same type as x
- `multiply(x: integer, y: interval_day<P>|interval_year)` -> interval
- `divide(x: numeric, y: numeric)` -> numeric
- `abs(x: numeric)` -> numeric
- `ceil(x: decimal<P,S>)` -> decimal
- `negate(x: numeric)` -> numeric
- `equal(x: any, y: any)` -> boolean
- `not_equal(x: any, y: any)` -> boolean
- `lt(x: any, y: any)` -> boolean
- `lte(x: any, y: any)` -> boolean
- `gt(x: any, y: any)` -> boolean
- `gte(x: any, y: any)` -> boolean
- `is_not_null(x: any)` -> boolean
- `is_nan(x: float)` -> boolean
- `and(x: boolean, y: boolean)` -> boolean
- `or(x: boolean, y: boolean)` -> boolean
- `not(x: boolean)` -> boolean

Examples:

```query
add(col("a"), col("b"), alias='sum_columns_a_b')
gt(col("external_sell"), col("outside_sell"), alias="external_sell_greater")
```

### cast(expr: Expression, type: LiteralType, alias: str) -> Expression

Cast the expression to a type.

```query
cast(literal('777', 'string'), 'i32', 'triple seven')
cast(col('year'), 'i32', 'year')
```

## Guidance

- In Join expressions, use `left.` and `right.` prefix for column references.
- The `alias` parameter changes the column name for subsequent constructs; expressions in the same construct are not in scope of the new name.

## Schema Enforcement

Track the output schema after each construct. Reference only columns present in the current vtable schema.
When referencing columns from input vtables, ONLY use names from the available set.

## Notes

- Scalar and aggregation functions never rename columns automatically — you must use `alias` explicitly. Example:
  ```query
  min(col("milliseconds"), alias="min_ms")
  ```
- Use `strftime` to extract specific time measures from temporal columns.
