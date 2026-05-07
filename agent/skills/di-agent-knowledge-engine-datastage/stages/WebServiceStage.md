# DataStage Web Service Stage

## Purpose
Invoke SOAP-based web services for SOAP web service integration.

## When to Use
- SOAP web service integration
- Invoking SOAP-based APIs
- Legacy web service integration

## When NOT to Use
- For REST APIs (use REST or HTTP stage instead)
- When SOAP protocol is not required

## Requirements
- **Link Cardinality**: Option 1: optionally 1 primary input, optionally 1 reject output; Option 2: up to 2 primary outputs
- SOAP web service endpoint and WSDL
- Appropriate authentication credentials

## Best Practices
- Implement proper error handling for web service failures
- Configure appropriate timeouts
- Handle SOAP faults appropriately
- Document web service dependencies

## Property Configuration
Configure SOAP endpoint, WSDL location, operations, and message handling according to web service requirements.