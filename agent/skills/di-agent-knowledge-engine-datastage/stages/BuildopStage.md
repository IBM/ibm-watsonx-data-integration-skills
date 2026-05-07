# DataStage Buildop Stage

## Purpose
Write custom C/C++ operators that plug directly into the DataStage parallel engine for advanced transformation logic unavailable in built-in stages.

## When to Use
- Transformation logic cannot be expressed in a Transformer stage
- Performance is critical and Java Integration is too slow

## When NOT to Use
- Logic can be handled by a built-in stage
- User is more comfortable with Java and performance isn't critical (use Java Integration Stage)
- Team lacks C/C++ expertise

## Alternative Stage Options
- [Transformer Stage](TransformerStage.md) - Preferred first choice for custom logic
- [Java Integration Stage](JavaIntegrationStage.md) - Java-based alternative when C++ expertise is unavailable

## Requirements
- **Link Cardinality**: Can have any number of input links and output links
- Compatibility: requires gcc 8.5+
- C/C++ development expertise
- Thorough testing with representative data volumes

## Best Practices
- Exhaust Transformer capabilities first
- Prefer Buildop over Java Integration for performance-critical operations
- Implement comprehensive error handling - unhandled exceptions can crash the engine process
- Document the build environment (compiler version, flags, dependencies)

## Performance
- Highest performance option for custom logic
- Engine calls C++ code for each data partition in parallel

## Property Configuration

### How It Works
Compiles into a native shared library the DataStage engine loads at runtime. Can have any number of input links, output links, and configuration options. The engine calls your C++ code for each data partition in parallel.

### Considerations
- **Maintenance burden** - Custom code requires ongoing support as DataStage versions change
- **Complexity** - Significantly harder to write and debug than Transformer logic
- **Testing** - Thorough unit + integration testing required
- **Portability** - Compiled artifacts may have platform dependencies; document the build environment
- **Documentation** - Must document all custom logic for future maintainers
