# DataStage Wave Generator Stage

## Purpose
Generate wave patterns for testing, simulation, and artificial mini-batching of records.

## When to Use
- Test data generation with wave patterns
- Artificial mini-batching of records
- Simulation scenarios requiring periodic patterns

## When NOT to Use
- For production data processing
- When wave patterns are not needed

## Requirements
- **Link Cardinality**: exactly 1 primary input, exactly 1 primary output

## Best Practices
- Use primarily for testing and development
- Configure wave parameters based on test requirements
- Document wave pattern configuration

## Property Configuration

### mode

The mode of operation by which end-of-wave markers are inserted. `WAVE_GENERATOR.Mode.count` by default. When in count mode, the property `record_count` must be set. `record_count` specifies the maximum number of records that comprise a wave. Other options are `WAVE_GENERATOR.Mode.column` and `WAVE_GENERATOR.Mode.dupkey`.