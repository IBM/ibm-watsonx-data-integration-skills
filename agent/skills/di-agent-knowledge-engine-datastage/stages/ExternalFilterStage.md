# DataStage External Filter Stage

## Purpose
Filter data using external programs or scripts for custom filtering logic integration.

## When to Use
- Custom filtering logic that cannot be implemented in Transformer stage
- Integration with existing external filtering programs
- Leveraging specialized filtering tools or scripts
- When filtering logic is maintained outside DataStage

## When NOT to Use
- When filtering can be done with Transformer Stage (preferred for performance)
- When Buildop Stage can implement the logic (better performance)
- For simple filtering operations

## Alternative Stage Options
- [Transformer Stage](TransformerStage.md) - Preferred for most filtering operations
- [Buildop Stage](BuildopStage.md) - Better performance for custom logic

## Requirements
- **Link Cardinality**: Optionally 1 primary input, optionally 1 primary output
- External program or script must be accessible and executable
- Proper error handling for external program failures

## Best Practices
- If performance is important prefer Transformer Stage or Buildop Stage if possible
- Test external programs thoroughly before production use
- Implement proper error handling and logging
- Document external program dependencies

## Performance
- Requires launching an external program and converting records to/from external format so may impact performance
- External program execution adds overhead
- Consider performance impact for high-volume data processing
