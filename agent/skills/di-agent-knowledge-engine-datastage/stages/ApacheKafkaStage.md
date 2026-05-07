# DataStage Apache Kafka Stage

## Purpose
Read from and write to Apache Kafka topics for real-time data streaming integration.

## When to Use
- Real-time data streaming applications
- Integration with Kafka-based messaging systems

## When NOT to Use
- Batch processing of static files (use Sequential File or Data Set stages)

## Requirements
- **Link Cardinality**: Varies based on usage (source or target)
- Valid Kafka broker connection configuration
- Appropriate Kafka topic access permissions

## Best Practices
- Configure appropriate batch sizes for optimal throughput
- Monitor Kafka consumer lag for source operations

## Property Configuration
Configuration details for Kafka broker connections, topics, serialization, and other Kafka-specific settings should be specified according to your Kafka environment requirements.
