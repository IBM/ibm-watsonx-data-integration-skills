# DataStage IBM MQ Stage

## Purpose
Read from and write to IBM MQ queues for enterprise messaging integration.

## When to Use
- Enterprise messaging integration with IBM MQ
- Asynchronous message processing
- Integration with MQ-based systems

## When NOT to Use
- For file-based data transfer
- When MQ infrastructure is not available

## Requirements
- **Link Cardinality**: Option 1: any number allowed primary inputs, any number allowed reject outputs; Option 2: optionally 1 primary output
- IBM MQ infrastructure and connectivity
- Appropriate queue permissions

## Best Practices
- Configure appropriate message handling and error recovery
- Monitor queue depths and message processing rates
- Implement proper transaction handling

## Property Configuration
Configure MQ connection details, queue names, message formats, and transaction settings according to MQ infrastructure requirements.
