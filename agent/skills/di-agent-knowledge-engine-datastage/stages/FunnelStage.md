# DataStage Funnel Stage

## Purpose
Combine multiple inputs into single output for merging data streams.

## When to Use
- Merging data streams from multiple sources
- Union operations on multiple datasets

## When NOT to Use
- When data needs to be joined based on keys (use Join stage)

## Requirements
- **Link Cardinality**: 2 or more primary inputs, exactly 1 primary output

## Best Practices
- Choose appropriate funnel type based on requirements
- Monitor for potential data deadlock scenarios

## Performance
- Buffer operators inserted into flow to avoid data deadlock which use memory and may spill data to disk
- Continuous funnel has lower overhead than sort funnel

## Property Configuration

### Funnel Types
- **Continuous funnel**: Combines data as it arrives without ordering
- **Sort funnel**: Combines sorted inputs maintaining sort order