# DataStage Change Apply Stage

## Purpose
Apply changes to a target dataset based on change records, enabling incremental updates rather than full reloads.

## When to Use
- Incremental updates to target datasets
- Applying CDC (Change Data Capture) records

## When NOT to Use
- When full dataset reloads are more appropriate

## Requirements
- **Link Cardinality**: exactly 2 primary inputs, exactly 1 primary output
- Hash partitioning on key columns
- Sorted inputs on key columns

## Best Practices
- Ensure both inputs are sorted on key columns
- Validate change records before applying to target

## Property Configuration

### selection

It is best to specify the selection mode. 

This mode determines how keys and values are specified. Explicit Keys & Values means that key & value columns must be explicitly defined. All Keys, Explicit Values means that value columns must be defined, but all other columns are key columns unless they are excluded. Explicit Keys & Values means that key & value columns must be explicitly defined. Explicit Keys, All Values means that key columns must be defined, but all other columns are value columns unless they are excluded.

```python
change_apply.configuration.selection = CHANGE_APPLY.Selection.allvalues
```

### code_field

Name of the column containing the change codes. This MUST match the name of the TINYINT column coming from the input stage. The default if unspecified is "change_code," meaning an TINYINT column called "change_code" must exist from the input.

### key_properties

A flat list of dicts containing names of column to be used as keys. 

Required if selection == CHANGE_APPLY.Selection.allvalues or selection == CHANGE_APPLY.Selection.custom. Do NOT set this property if selection == CHANGE_APPLY.Selection.allkeys. 

- `key` (required): Key column name
- `key-ci-cs` (optional): Whether the column name is case sensitive
- `key-nulls` (optional): Whether to put nulls first or last
- `key-asc-desc` (optional): Ascending or descending

```python
change_apply.configuration.value_properties = [
    {"key": "KEY_1", "key-asc-desc": "desc", "key-nulls": "last", "key-ci-cs": "ci"},
    {"key": "KEY_2", "key-asc-desc": "asc", "key-nulls": "first"},
]
```

### value_properties

A flat list of dicts, each identifying a value column (modified by edit rows, used to disambiguate deletes when keys are not unique). 

Required if selection == CHANGE_APPLY.Selection.allkeys or selection == CHANGE_APPLY.Selection.custom. Do NOT set this property if selection == CHANGE_APPLY.Selection.allvalues. 

- `value` (required): Column name
- `value-ci-cs` (optional): Whether the column name is case sensitive

```python
change_apply.configuration.value_properties = [
    {"value": "amount", "value-ci-cs": "ci"},
    {"value": "status"}
]
