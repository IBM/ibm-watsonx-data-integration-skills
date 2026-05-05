# DataStage Checksum Stage

## Purpose
Calculate checksums for data validation and integrity verification.

## When to Use
- Data integrity verification across systems
- Generating hash values for record comparison

## When NOT to Use
- When data integrity verification is not required
- For encryption purposes (use appropriate encryption stages)

## Requirements
- **Link Cardinality**: exactly 1 primary input, optionally 1 primary output

## Best Practices
- Choose appropriate checksum algorithm based on security and performance requirements
- Store checksums for later comparison and validation

## Property Configuration
Configure checksum algorithm and target columns for checksum calculation according to data validation requirements.
