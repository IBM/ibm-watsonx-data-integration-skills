# DataStage Java Integration Stage

## Purpose
Execute custom Java code for transformation logic when built-in stages are insufficient.

## When to Use
- User is most comfortable with Java for custom transformation logic
- When Java libraries are required for implementation

## When NOT to Use
- Transformation logic can be handled by built-in stage or Transformer
- Performance is critical (prefer Buildop Stage)

## Alternative Stage Options
- [Transformer Stage](TransformerStage.md) - Preferred alternative for most transformations
- [Buildop Stage](BuildopStage.md) - C/C++ alternative for performance-critical operations

## Requirements
- **Link Cardinality**: Varies based on implementation
- Compatibility: requires JDK 17+
- Java development expertise

## Best Practices
- Prefer built-in stages or Transformer capabilities before custom Java
- Prefer Buildop for performance-critical transformations
- Implement comprehensive error handling
- Use standard Java libraries when possible

## Property Configuration

### Considerations
- **Performance** - Generally slower than Buildop (C/C++)
- **Maintenance** - Requires Java expertise
- **Testing** - Thorough unit + integration testing required
- **Documentation** - Must document custom logic
- **Dependencies** - Manage Java library dependencies carefully
