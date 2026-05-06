# DataStage Lookup File Set Stage

## Purpose
Create lookup file sets for large static reference data lookups.

## When to Use
- Large static reference data lookups
- When lookups are performed against the same static table data repeatedly
- To avoid overhead of creating lookup table for every run

## When NOT to Use
- For small reference tables (use Lookup stage directly)
- When reference data changes frequently

## Requirements
- **Link Cardinality**: Optionally 1 primary input, optionally 1 primary output

## Best Practices
- Use for static reference data that doesn't change frequently
- Create lookup file set once and reuse across multiple jobs
- Monitor file set size and update when reference data changes

## Performance
- More efficient than creating lookup table for every run
- Avoids overhead of loading reference data repeatedly
- Best for large static reference datasets
