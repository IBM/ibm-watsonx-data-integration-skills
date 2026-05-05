# DataStage Column Import Stage

## Purpose
Import column definitions from external sources by mapping a single string or binary column to one or more output columns.

## When to Use
- Parsing a single string or binary column into multiple structured columns
- Importing data from systems that provide data in serialized format
- Deserializing structured data from a single field

## When NOT to Use
- When data is already in structured column format
- For simple column transformations (use Transformer stage instead)

## Requirements
- **Link Cardinality**: exactly 1 primary input, exactly 1 primary output, optionally 1 reject output
- Ensure the format settings for the input column exactly match the format of the data
- Use the Column Export Stage for the reverse operation

## Best Practices
- Utilize the reject dataset output for identifying formatting issues
- Verify format settings match the source data format exactly
- Test with sample data to validate parsing rules before processing large volumes

## Property Configuration

### selection

Whether to specify columns to export explicitly or use a Schema File. Default: COLUMN_EXPORT.Selection.explicit. Not required but recommended for clarity.

### field

Required. Name of the varchar or binary column containing the string or raw data to import.

### schema_

Input column names to import. Required if selection == COLUMN_EXPORT.Selection.explicit selection. 

```python
column_import.configuration.schema_ = [
    {"ColumnName": "Age"}, 
    {"ColumnName": "Department"}, 
    {"ColumnName": "ID"}
]
```

### schema_file

The name of the schema file. Required if selection == COLUMN_EXPORT.Selection.file. 
