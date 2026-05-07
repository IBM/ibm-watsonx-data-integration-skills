# DataStage Column Generator Stage

## Purpose
Generate new columns with calculated or derived values such as sequence numbers, timestamps, or other computed fields.

## When to Use
- Adding sequence numbers to records
- Generating timestamps for record processing
- Creating unique identifiers
- Adding computed columns based on system values

## When NOT to Use
- For complex transformations (use Transformer stage instead)
- When values should come from source data rather than being generated

## Requirements
- **Link Cardinality**: exactly 1 primary input, exactly 1 primary output

## Best Practices
- Use for simple column generation tasks
- Consider partitioning impact on sequence number generation
- Ensure generated values meet downstream requirements

## Property Configuration
Configure column generation rules including sequence numbers, timestamps, and other derived values.
