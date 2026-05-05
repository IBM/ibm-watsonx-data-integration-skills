# DataStage Decode Stage

## Purpose
Decode previously encoded data from Base64, Hexadecimal, or URL encoding formats.

## When to Use
- Processing encoded data from external sources
- Decoding data previously encoded by the Encode Stage
- Converting Base64, Hexadecimal, or URL encoded data to original format
- Processing data received from web services or APIs

## When NOT to Use
- When data is not encoded
- For encryption/decryption (use appropriate security stages instead)

## Requirements
- **Link Cardinality**: exactly 1 primary input, exactly 1 primary output
- Use appropriate validation and error handling to ensure data integrity
- If data validation is required include a checksum field with encoded data

## Best Practices
- Validate encoded data format before decoding
- Implement error handling for malformed encoded data
- Use checksums to verify data integrity after decoding
- Test with sample data to ensure correct decoding

## Performance
- Consider memory usage when decoding large fields
- Decoding operations are generally CPU-intensive
