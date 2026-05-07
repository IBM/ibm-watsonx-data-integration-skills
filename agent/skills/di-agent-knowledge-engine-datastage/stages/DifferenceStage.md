# DataStage Difference Stage

## Purpose
Output records that differ between two datasets for incremental loading and change detection.

## When to Use
- Incremental loading scenarios
- Change detection between datasets

## When NOT to Use
- For complete change tracking with insert/update/delete indicators (use Change Capture stage)

## Requirements
- **Link Cardinality**: exactly 2 primary inputs, optionally 1 primary output
- Input must be sorted on key columns
- Hash partitioning on key columns required

## Best Practices
- Ensure both inputs are sorted on key columns
- Define value columns to compare for detecting differences

## Property Configuration

### key_properties

Required. "The difference key columns that the sort will be carried out on and their properties. Keys have the property 'key' which contains the name of the key, and the property 'ci-cs' which indicates whether the key is case sensitive.

```python
difference.configuration.key_properties = [
    {"key": "Name", "ci-cs": "ci"}, 
    {"key": "ID", "ci-cs": "cs"}
]
```

### value_properties

Flat list of dicts. Each dict identifies a non-key column to compare for changes:
- `value` (required): Column name

```python
difference.configuration.value_properties = [
    {"value": "amount"},
    {"value": "status"}
]
