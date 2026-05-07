# DataStage Change Capture Stage

## Purpose
Identify changes between two datasets by comparing before and after snapshots, generating change records for CDC (Change Data Capture) and incremental load scenarios.

## When to Use
- CDC (Change Data Capture) implementations
- Incremental loads requiring change identification

## When NOT to Use
- When source system provides native CDC capabilities

## Requirements
- **Link Cardinality**: exactly 2 primary inputs, exactly 1 primary output
- Both inputs sorted on key columns
- Hash partitioning on key columns

## Best Practices
- Ensure both inputs are sorted on key columns
- Define value columns to track for change detection

## Property Configuration

### Ouput Schema Requirements
The output schema must contain the source property for every field and a TINYINT change_code field where the changes are captured. The change_code property on the change_code field must be True.

python```
change_capture_1_schema.add_field("DECIMAL", "colname", source="Link_Before.colname")
change_capture_1_schema.add_field("TINYINT", "change_code", nullable=True, change_code=True)
```

### inputlink_ordering_list

Required. Identifies which two named input links contain the data Before and After the change to capture. 

```python
change_capture_stage.configuration.inputlink_ordering_list = [
    {"link_label": "Before", "link_name": "..."},
    {"link_label": "After", "link_name": "..."}
]
```

### value_properties Format

**`value_properties`**: Flat list of dicts. Each dict identifies a value column to track for changes between before and after records:
- `value` (required): Column name

```python
change_capture.configuration.value_properties = [
    {"value": "amount"},
    {"value": "status"}
]
```

### Output Records
The stage generates records with change indicators:
- Insert: Records present in after but not in before
- Update: Records present in both with different values
- Delete: Records present in before but not in after
- Copy: Records present in both with identical values
