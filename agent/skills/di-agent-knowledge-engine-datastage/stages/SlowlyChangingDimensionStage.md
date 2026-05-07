# DataStage Slowly Changing Dimension Stage

## Purpose
Manage slowly changing dimensions in data warehouses.

## When to Use
- Data warehouse dimension management
- Implementing SCD Type 1, Type 2, or Type 3 logic

## When NOT to Use
- For simple dimension loads without history tracking

## Requirements
- **Link Cardinality**: Option 1: exactly 1 primary input, exactly 1 reference input; Option 2: exactly 1 reference input, exactly 2 primary outputs

## Best Practices
- Choose appropriate SCD type based on business requirements
- Ensure proper key management for dimension records

## Property Configuration
Configure SCD type, key columns, change detection columns, and historical tracking according to data warehouse requirements.