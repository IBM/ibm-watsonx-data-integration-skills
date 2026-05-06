# DataStage Surrogate Key Generator Stage

## Purpose
Generate surrogate keys for dimension tables in data warehouse key management.

## When to Use
- Data warehouse key management
- Generating unique surrogate keys for dimension tables

## When NOT to Use
- When natural keys are sufficient

## Requirements
- **Link Cardinality**: Optionally 1 primary input, optionally 1 primary output

## Best Practices
- Ensure key generation is consistent across job runs
- Plan key ranges to avoid conflicts

## Property Configuration
Specify either input_key or output_key. Specify either admin or output_key.