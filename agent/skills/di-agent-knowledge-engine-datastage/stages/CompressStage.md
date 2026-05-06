# DataStage Compress Stage

## Purpose
Compress data to reduce size for storage and data transfer optimization.

## When to Use
- Storage optimization for large data volumes
- Reducing data transfer time over networks
- Archiving data with reduced storage footprint
- Preparing data for compressed file formats

## When NOT to Use
- When downstream systems cannot handle compressed data
- For small datasets where compression overhead exceeds benefits
- When CPU resources are constrained

## Requirements
- **Link Cardinality**: exactly 1 primary input, exactly 1 primary output

## Best Practices
- Choose compression algorithm based on speed vs. compression ratio requirements
- Use LZ4 for speed-critical applications
- Use BZIP2 for maximum compression ratio
- Consider CPU impact on overall job performance

## Performance
- Compression is CPU-intensive
- LZ4 provides fast compression with moderate compression ratio
- BZIP2 provides high compression ratio but slower processing
- Balance compression benefits against CPU overhead
