# DataStage Merge Stage

## Purpose
Merge sorted datasets while maintaining sort order.

## When to Use
- Combining pre-sorted data from multiple sources

## When NOT to Use
- When data is not already sorted (use Sort stage first)
- For joining data based on keys (use Join stage)

## Requirements
- **Link Cardinality**: 2 or more primary inputs, exactly 1 primary output, any number of reject outputs
- All inputs sorted on merge keys
- Hash partitioning on merge keys

## Best Practices
- Ensure all inputs are sorted before merging
- Leverage multiple reject output links for error handling

## Property Configuration

### Characteristics
- Efficient for sorted data
- Maintains sort order in output
- Unlike Join or Lookup allows for multiple reject output links
