# DataStage Column Export Stage

## Purpose
Export column definitions to external targets by mapping multiple input columns of any type to one output column of string or binary type.

## When to Use
- Converting multiple columns into a single string or binary column
- Preparing data for export to systems requiring specific column formats
- Serializing structured data into a single field

## When NOT to Use
- When columns don't need to be combined or exported
- For simple column selection (use Copy stage instead)

## Requirements
- **Link Cardinality**: exactly 1 primary input, exactly 1 primary output, optionally 1 reject output
- Ensure the format settings are correct for the downstream processing of the field
- Use the Column Import Stage for the reverse operation

## Best Practices
- Utilize the reject dataset output for identifying export issues
- Verify format settings match downstream system requirements
- Test with sample data before processing large volumes

## Property Configuration

### selection

Whether to specify columns to export explicitly or use a Schema File. Default: COLUMN_EXPORT.Selection.explicit. Not required but recommended for clarity.

### field

Required. Name of the varchar or binary column to which the input column or columns are exported.

### schema_

Input column names to export. Required if selection == COLUMN_EXPORT.Selection.explicit selection. Example: ["col_1"]

### schema_file

The name of the schema file. Required if selection == COLUMN_EXPORT.Selection.file. 

### type

The type of the exported field. Example: COLUMN_EXPORT.Type.string