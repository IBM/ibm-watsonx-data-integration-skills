# DataStage Survive Stage

## Purpose
Select the best or most appropriate record from a group of matched records based on survivorship rules and data quality criteria.

## When to Use
- Selecting the best record from duplicate or matched records
- Implementing survivorship rules for master data management
- Consolidating multiple records into a single golden record
- Data quality-driven record selection

## When NOT to Use
- For simple duplicate removal (use Remove Duplicates stage)
- When all records should be kept (use other stages)
- For basic filtering (use Filter or Transformer stage)

## Requirements
- **Link Cardinality**: Option 1: exactly 1 primary input; Option 2: exactly 1 primary output

## Best Practices


## Property Configuration
