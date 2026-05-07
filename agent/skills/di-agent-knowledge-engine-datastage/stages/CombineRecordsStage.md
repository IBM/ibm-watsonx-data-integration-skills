# DataStage Combine Records Stage

## Purpose
Combine multiple input records into a single output record based on specified key, creating variable length vector subrecords for data consolidation.

## When to Use
- Data consolidation and aggregation scenarios
- Creating hierarchical data structures from flat records
- Grouping related records into a single composite record

## When NOT to Use
- For simple aggregation operations (use Aggregator stage instead)
- When records don't need to be combined into vector structures

## Requirements
- **Link Cardinality**: exactly 1 primary input, exactly 1 primary output
- Input must be sorted on key columns
- Hash partitioning on key columns required
- Output record schema will be a variable length vector subrecord of the input record schema

## Best Practices
- Ensure input data is properly sorted on key columns
- Use appropriate partitioning strategy for optimal performance
- Consider memory implications of combining large numbers of records

## Property Configuration
Configure key columns for grouping records and specify how records should be combined into vector subrecords.
