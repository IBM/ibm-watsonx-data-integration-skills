# DataStage Tail Stage

## Purpose
Pass only the last N records from the input for recent data processing.

## When to Use
- Processing most recent records
- Extracting latest data entries
- Testing with end-of-file records
- Analyzing final records in a dataset

## When NOT to Use
- For production data filtering (use Filter or Transformer stage)
- When all records need to be processed
- When order of records is not guaranteed

## Requirements
- **Link Cardinality**: exactly 1 primary input, exactly 1 primary output

## Best Practices
- Ensure input data has meaningful ordering
- Use primarily for development and testing
- Consider memory implications for large N values

## Property Configuration

Specify number of records to pass through from the end of the input stream.
