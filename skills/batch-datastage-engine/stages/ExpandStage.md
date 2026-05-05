# DataStage Expand Stage

## Purpose
Decompress compressed data to restore it to its original format.

## When to Use
- Accessing compressed archived data produced by the Compress Stage
- Processing compressed data from external sources
- Decompressing data for downstream processing
- Restoring archived data to usable format

## When NOT to Use
- When data is not compressed
- When downstream stages can process compressed data directly

## Requirements
- **Link Cardinality**: exactly 1 primary input, exactly 1 primary output
- If data validation is required include a checksum field with compressed data
- Compression algorithm must match the one used during compression

## Best Practices
- Validate compressed data integrity before decompression
- Use checksums to verify data integrity after decompression
- Ensure sufficient memory and disk space for decompression
- Match decompression algorithm with original compression method

## Performance
- Decompression is CPU-intensive
- Consider CPU impact on overall job performance
- Balance decompression overhead against data transfer benefits
