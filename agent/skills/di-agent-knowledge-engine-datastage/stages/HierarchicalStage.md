# DataStage Hierarchical Stage

## Purpose
Process hierarchical data structures like XML and JSON.

## When to Use
- Parsing XML or JSON responses from API calls or external sources
- Processing nested data structures
- Transforming hierarchical data to relational format

## When NOT to Use
- For simple flat file processing (use Sequential File stage)
- When data is already in relational format

## Requirements
- **Link Cardinality**: Varies based on configuration

## Best Practices
- Monitor memory usage for deeply nested structures
- Consider performance impact of complex hierarchical parsing
- Test with representative data structures

## Performance
- Hierarchical parsing can be CPU-intensive
- Parsing deeply nested structures can consume significant memory
- Consider data structure complexity when designing flows
