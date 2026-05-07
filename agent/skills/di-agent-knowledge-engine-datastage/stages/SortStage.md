# DataStage Sort Stage

## Purpose
Sort records by key columns to prepare data for downstream stages.

## When to Use
- Preparing data for stages requiring sorted input (Join, Merge, Remove Duplicates)
- Verifying sort order

## Requirements
- **Link Cardinality**: exactly 1 primary input, exactly 1 primary output
- Hash partitioning on sort keys

## Best Practices
- Combine multiple sort requirements into single sort operation
- Monitor disk space usage in container environments

## Performance
- Expensive operation
- Large data sets require disk space for temporary files
- Disk space uses ephemeral storage which can be limited in container environments

## Property Configuration

### Sort Options
- Ascending/Descending order
- Multiple key columns
- Stable sort option
