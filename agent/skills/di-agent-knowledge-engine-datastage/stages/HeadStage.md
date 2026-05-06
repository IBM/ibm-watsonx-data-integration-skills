# DataStage Head Stage

## Purpose
Pass along only the first N records from the input for sampling and testing purposes.

## When to Use
- Sampling data for testing
- Creating test datasets with subset of records
- Quick data validation with limited records
- Development and debugging with small data volumes

## When NOT to Use
- For production data filtering (use Filter or Transformer stage)
- When all records need to be processed
- For random sampling (use Sample stage instead)

## Requirements
- **Link Cardinality**: exactly 1 primary input, exactly 1 primary output

## Best Practices
- Use primarily for development and testing
- Remove or disable in production unless specifically needed
- Consider using Sample stage for statistical sampling

## Property Configuration

Specify number of records to pass through from the beginning of the input stream.
