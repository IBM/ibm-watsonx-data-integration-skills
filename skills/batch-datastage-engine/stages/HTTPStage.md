# DataStage HTTP Stage

## Purpose
Make HTTP requests to web services and APIs for REST API integration.

## When to Use
- REST API integration
- Making HTTP/HTTPS requests to external services
- Consuming web services

## When NOT to Use
- For file-based data transfer (use appropriate file stages)
- When API doesn't support HTTP/REST protocols

## Requirements
- **Link Cardinality**: Option 1: no links required; Option 2: exactly 1 primary output

## Best Practices
- Implement proper error handling for HTTP failures
- Configure appropriate timeouts
- Handle authentication securely
- Monitor API rate limits

## Property Configuration
Configure HTTP method, URL, headers, authentication, and request/response handling according to API requirements.
