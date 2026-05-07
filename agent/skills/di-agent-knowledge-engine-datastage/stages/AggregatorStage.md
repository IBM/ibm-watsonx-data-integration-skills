# DataStage Aggregator Stage

## Purpose
Group and aggregate data to produce summaries, totals, counts, averages, and other statistical calculations.

## When to Use
- Calculate totals, counts, averages, and other statistical calculations
- Generate aggregated reports from detailed transaction data

## When NOT to Use
- When data doesn't need grouping or aggregation
- For simple filtering or transformation (use Filter or Transformer stages)

## Requirements
- **Link Cardinality**: exactly 1 primary input, exactly 1 primary output
- Hash or Modulus partitioning on grouping keys
- Input sorted on grouping keys (optional but improves performance)

## Best Practices
- Use Hash method when distinct key values are small
- Use Sort method when distinct key values are large or unknown
- Pre-sort input data on grouping keys to improve performance

## Property Configuration

### Aggregation Functions
Available aggregation functions:
- COUNT, SUM, AVG, MIN, MAX, FIRST, LAST
- Standard deviation, variance
- Valid functions: `sum`, `min`, `max`, `mean`, `css`, `missing`, `count`, `cv`, `range`, `std`, `ste`, `sumw`, `uss`, `var`, `summary`

### Key Properties Format

**`reduce_properties`** and **`rereduce_properties`**: List of lists of single-key dicts. Each inner list defines one aggregation group.
- First dict: `{"reduce": "source_col"}` (or `{"rereduce": "source_col"}` for rereduce)
- Subsequent dicts: one per operation, key is the function name, value is the output column

```python
agg.configuration.reduce_properties = [
    [{"reduce": "price"}, {"sum": "total_price"}, {"mean": "avg_price"}],
    [{"reduce": "qty"}, {"sum": "total_qty"}]
]
```

**`count_field_properties`**: Same double-nested format. Each inner list has `{"countField": "output_col"}` and optionally `{"weightField": "weight_col"}`.

```python
agg.configuration.count_field_properties = [
    [{"countField": "record_count"}],
    [{"countField": "weighted_count"}, {"weightField": "order_qty"}]
]
```

**`key_properties`**: Flat list of dicts. Each dict must have key `"key"` with the column name. Optional: `"key-keep"` (`"keep"` or `" "`), `"key-ci-cs"` (`"ci"` for case-insensitive).

```python
agg.configuration.key_properties = [{"key": "customer_id"}]
```