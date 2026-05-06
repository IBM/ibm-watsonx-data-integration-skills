# DataStage File Set Stage

## Purpose
Read and write data to file sets for large-scale parallel data processing when human readable format is required.

## When to Use
- Large-scale parallel data processing requiring human-readable format
- Processing large datasets that need to be accessible outside DataStage

## When NOT to Use
- For inter-job communication within DataStage (use Data Set Stage)
- For small datasets (use Sequential File Stage)

## Requirements
- **Link Cardinality**: Optionally 1 primary input, optionally 1 primary output, optionally 1 reject output

## Best Practices
- Consider partitioning strategy for optimal parallel processing
- Use reject link to capture processing errors

## Performance
- Provides parallel processing capabilities
- Better performance than Sequential File Stage for large volumes
