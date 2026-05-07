# DataStage Excel Stage

## Purpose
Read and write Microsoft Excel files for integration with Excel-based data sources and targets.

## When to Use
- Reading data from Excel spreadsheets
- Writing data to Excel format for business users

## When NOT to Use
- For simple delimited files (use Sequential File Stage)
- For large-scale data processing where performance is critical

## Requirements
- **Link Cardinality**: Varies based on usage (source or target)

## Best Practices
- Use Sequential File Stage for simple delimited files
- Consider file size limitations of Excel format

## Performance
- Excel processing has overhead compared to plain text formats
