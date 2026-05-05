# DataStage REST Stage

## Purpose
Make REST API calls to web services for REST API integration.

## When to Use
- REST API integration with external services
- Consuming RESTful web services
- Making HTTP-based API calls

## When NOT to Use
- For file-based data transfer
- When API doesn't support REST protocols

## Requirements
- **Link Cardinality**: Any number allowed primary inputs, any number allowed primary outputs

## Best Practices
- Use batch APIs when available to reduce latency
- Implement proper error handling for API failures
- Configure appropriate timeouts and retry logic
- Monitor API rate limits and quotas

## Performance
- REST calls add latency to processing
- Consider batching requests when possible
- Monitor network and API response times
