# DataStage Modify Stage

## Purpose
Perform data type conversions, column manipulations, and metadata modifications on records passing through the stage.

## When to Use
- Converting data types between formats
- Modifying column metadata (length, precision, scale)
- Performing column-level transformations
- Adjusting data formats and representations

## When NOT to Use
- For complex business logic transformations (use Transformer stage)
- For simple filtering (use Filter stage)
- When no data modification is needed (use Copy stage)

## Requirements
- **Link Cardinality**: exactly 1 primary input, exactly 1 primary output

## Best Practices


## Property Configuration

### modifyspec_properties

Required. An array of dictionaries where each dictionary defines a property that will contain a specification (modifyspec) and a suffix to add after the specification (specsuffix). Specify how the Modify stage operates. Each line is a new specification string that specifies a column to drop,keep,convert and more. DROP and KEEP are mutually exclusive.

```python
modify_stage.configuration.modifyspec_properties = [
    {"modifyspec": "DROP COL2", "specsuffix": ";"},
    {"modifyspec": "DROP COL3", "specsuffix": ";"},
]
```
