# DataStage Switch Stage

## Purpose
Route records based on selector value for multi-way routing operations.

## When to Use
- Multi-way routing based on single selector field

## When NOT to Use
- For complex routing logic (use Transformer with constraints - preferred)

## Alternative Stage Options
- [Transformer Stage](TransformerStage.md) - Preferred for routing with constraints, offers more flexibility

## Requirements
- **Link Cardinality**: exactly 1 primary input, 1 to 128 primary outputs, optionally 1 reject output

## Best Practices
- Transformer with constraints is generally preferred over Switch stage
- Use reject link to capture unmatched records

## Property Configuration

### Characteristics
- Routes to different outputs based on single selector field
- Selector field value determines output link
- Supports up to 128 output links
