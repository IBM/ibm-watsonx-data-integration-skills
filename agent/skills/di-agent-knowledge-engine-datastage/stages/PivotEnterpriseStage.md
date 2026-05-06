# DataStage Pivot Enterprise Stage

## Purpose
Pivot data from rows to columns or columns to rows for report generation and data reshaping.

## When to Use
- Report generation requiring pivoted data
- Data reshaping operations
- Converting row-based data to column-based or vice versa

## When NOT to Use
- When data structure doesn't need pivoting
- For simple transformations (use Transformer stage)

## Requirements
- **Link Cardinality**: exactly 1 primary input, exactly 1 primary output

## Best Practices
- Plan pivot structure carefully based on output requirements
- Consider performance impact of pivoting large datasets
- Validate pivot results with sample data

## Property Configuration

### pivot_properties Format

**`pivot_properties`**: Flat list of dicts, one per pivot output column. Each dict:
- `name` (required): Source column name to pivot
- `derivation` (required): Source column expression (usually same as `name`)
- `sqlType` (optional): ODBC type string for the output column (e.g. `"VARCHAR"`, `"INTEGER"`)
- `length` (optional): Integer column length
- `scale` (optional): Integer decimal scale
- `isPivotIndex` (optional): Bool, whether this column is the pivot index

```python
pivot.configuration.pivot_properties = [
    {"name": "col1", "derivation": "col1", "sqlType": "VARCHAR", "length": 100, "scale": 0, "isPivotIndex": False},
    {"name": "col2", "derivation": "col2", "sqlType": "INTEGER", "length": 10, "scale": 0, "isPivotIndex": False}
]
