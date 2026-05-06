# DataStage Bloom Filter Stage

## Purpose
Create and use Bloom filters for efficient set membership testing with minimal memory footprint.

## When to Use
- Efficient filtering against large sets when 100% accuracy is not required
- First-pass filter before expensive lookups or joins

## When NOT to Use
- When 100% accuracy is required
- When the reference set is small enough for exact matching (use Lookup stage)

## Requirements
- **Link Cardinality**: Option 1 (in process mode): exactly 1 primary input, exactly 2 primary outputs; Option 2 (in create mode): exactly 1 primary input, no outputs

## Best Practices
- Use as first-pass filter before expensive lookups
- Configure appropriate filter size based on expected data volume

## Performance
- Fast and memory efficient for testing set membership
- False positives are possible but false negatives are not
