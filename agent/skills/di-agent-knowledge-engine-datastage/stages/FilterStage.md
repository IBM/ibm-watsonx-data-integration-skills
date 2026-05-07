# DataStage Filter Stage

## Purpose
Filter records based on conditions for simple record filtering operations.

## When to Use
- Simple record filtering based on conditions

## When NOT to Use
- When transformation or more flexibility is also needed (use Transformer stage)
- For complex filtering logic (use Transformer stage)

## Alternative Stage Options
- [Transformer Stage](TransformerStage.md) - Preferred for most filtering scenarios with more flexibility

## Requirements
- **Link Cardinality**: exactly 1 primary input, 1 or more primary outputs, optionally 1 reject output

## Best Practices
- Prefer Transformer Stage for better flexibility
- Use a single Transformer rather than chained Filter Stages

## Property Configuration

### where_properties

Required. An array of dictionaries that specifies the conditions which determines the filter. Each dictionary contains 2 keys: 'where' whose value is the where condition and 'target' whose value is the index number of the link to output to.

```python
filter.configuration.where_properties = [
    {"where": "ord_db_id > ord_id", "target": 0},
    {"where": "ord_id <= ord_db_id", "target": 1},
]
```