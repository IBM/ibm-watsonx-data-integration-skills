# DataStage Remove Duplicates Stage

## Purpose
Identify and remove duplicate records based on key columns.

## When to Use
- Data deduplication operations

## When NOT to Use
- When duplicates are valid and should be retained
- For aggregation operations (use Aggregator stage)

## Requirements
- **Link Cardinality**: exactly 1 primary input, exactly 1 primary output
- Input must be sorted on key columns
- Hash partitioning on key columns required

## Best Practices
- Ensure input is sorted on key columns
- Choose appropriate keep option (first/last/unique)

## Property Configuration

- Define key columns for duplicate detection
- Choose keep first/last/unique option
