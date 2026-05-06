# DataStage External Source Stage

## Purpose
Read data from external programs or scripts for custom data source integration.

## When to Use
- Custom data source integration that cannot be handled by built-in stages
- Integration with existing external data extraction programs
- Leveraging specialized data retrieval tools or scripts
- When data source logic is maintained outside DataStage

## When NOT to Use
- When built-in connector stages can handle the data source
- For standard file or database sources (use appropriate connector stages)
- When performance is critical and alternatives exist

## Requirements
- **Link Cardinality**: Optionally 1 primary output, optionally 1 reject output
- External program or script must be accessible and executable
- Proper error handling for external program failures

## Best Practices
- Test external programs thoroughly before production use
- Implement proper error handling and logging
- Use reject link to capture errors from external program
- Document external program dependencies and requirements
- Validate data format and schema from external source

## Performance
- External program execution adds overhead
- Consider performance impact for high-volume data processing
- Monitor external program resource usage