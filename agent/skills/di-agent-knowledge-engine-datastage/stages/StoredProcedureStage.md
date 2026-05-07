# DataStage Stored Procedure Stage

## Purpose
Execute database stored procedures for database business logic integration.

## When to Use
- Database business logic integration
- Executing database-side operations
- Leveraging existing stored procedures

## When NOT to Use
- When logic can be implemented in DataStage stages
- For simple data operations that don't require database procedures

## Requirements
- **Link Cardinality**: Varies based on configuration
- Database connectivity and stored procedure access
- Appropriate database permissions

## Best Practices
- Minimize stored procedure calls for performance
- Use batch operations when possible
- Implement proper error handling
- Document stored procedure dependencies

## Performance
- Consider network and database latency when using
- Stored procedure execution adds overhead
- Monitor database performance impact
