# DataStage Operational Decision Manager Stage

## Purpose
Integrate with IBM ODM for business rules execution.

## When to Use
- Business rules integration with IBM ODM
- Executing business rules on data flows
- Decision management integration

## When NOT to Use
- When business rules can be implemented in Transformer stage
- When ODM infrastructure is not available

## Requirements
- **Link Cardinality**: Varies based on configuration
- IBM ODM infrastructure and connectivity
- Appropriate ODM rule sets configured

## Best Practices
- Ensure ODM rules are properly tested before integration
- Monitor ODM performance and rule execution times
- Document rule dependencies and versions

## Property Configuration
Configure ODM connection details, rule sets, and decision service parameters according to ODM infrastructure requirements.
