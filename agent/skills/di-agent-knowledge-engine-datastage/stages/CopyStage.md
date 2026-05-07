# DataStage Copy Stage

## Purpose
Copy data with optional type conversion for simple data flow operations.

## When to Use
- Design placeholder during development
- Simple type conversions without business logic
- Data flow splitting to multiple targets

## When NOT to Use
- For complex transformations and business logic (use Transformer Stage)

## Alternative Stage Options
- [Transformer Stage](TransformerStage.md) - Use for complex transformations, business logic, conditional operations, or calculations

## Requirements
- **Link Cardinality**: exactly 1 primary input, any number of primary outputs

## Best Practices
- Remove unnecessary Copy stages in production
- Use Transformer Stage for complex transformations and business logic

## Performance
- Lightweight operation with minimal CPU and memory overhead
- Preserves partitioning for downstream stages
