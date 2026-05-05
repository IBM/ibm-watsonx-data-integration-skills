# DataStage Row Generator Stage

## Purpose
Generate test data with specified number of records for testing and prototyping.

## When to Use
- Testing and prototyping data flows
- Generating test datasets
- Creating sample data for development
- Example: `flow.add_stage('Row Generator', 'row_gen')`

## When NOT to Use
- For production data generation
- When real data sources are available

## Requirements
- **Link Cardinality**: exactly 1 primary output, optionally 1 input link
- Output schema definition required

## Best Practices
- Use for development and testing only
- Configure appropriate number of records for test scenarios
- Define realistic data ranges and patterns

## Property Configuration

### Key Properties
- Number of records to generate (default is 10)
- Mode: sequential (default) or parallel
- If an input link is provided, new fields will be added to the front of existing records
- Can generate a percentage of null records for nullable fields
- Field values can cycle through ranges, random values, or static lists