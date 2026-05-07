# DataStage Compare Stage

## Purpose
Compare two datasets and identify differences for data validation and reconciliation purposes.

## When to Use
- Data validation and reconciliation between systems
- Quality assurance testing to verify data accuracy

## When NOT to Use
- For change data capture (use Change Capture stage)

## Requirements
- **Link Cardinality**: exactly 2 primary inputs, optionally 1 primary output
- Input must be sorted on key columns
- Hash partitioning on key columns required

## Best Practices
- Ensure both inputs are sorted on key columns
- Configure case sensitivity settings appropriately for text comparisons

## Property Configuration

### field_properties Format

**`field_properties`**: Flat list of dicts. Each dict defines a key column with optional case sensitivity:
- `key` (required): Column name to sort/compare on
- `ci-cs` (optional): `"ci"` for case-insensitive, `"cs"` for case-sensitive (default)

```python
compare.configuration.field_properties = [
    {"key": "customer_id"},
    {"key": "name", "ci-cs": "ci"}
]
```