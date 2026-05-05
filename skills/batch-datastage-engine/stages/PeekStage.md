# DataStage Peek Stage

## Purpose
View data during job execution for debugging, data inspection, and monitoring.

## When to Use
- Debugging data flow issues
- Inspecting data at specific points in the flow
- Example: `flow.add_stage('Peek', 'peek')`

## When NOT to Use
- In production jobs (remove after debugging)

## Requirements
- **Link Cardinality**: exactly 1 primary input, any number of primary outputs

## Best Practices
- Remove Peek stages in production
- Configure appropriate number of records to display

## Property Configuration

### Key Properties
- Number of records to display is configurable, default is 10
- Field names can optionally be displayed
- Output logs to job output
