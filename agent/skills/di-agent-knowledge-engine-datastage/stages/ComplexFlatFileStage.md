# DataStage Complex Flat File Stage

## Purpose
Process complex flat files with hierarchical structures including Cobol Copybooks and MVS files for legacy system integration.

## When to Use
- Legacy system integration requiring Cobol Copybook processing
- Processing MVS (mainframe) files with complex structures

## When NOT to Use
- For simple flat files (use Sequential File stage)

## Requirements
- **Link Cardinality**: Optionally 1 primary input, any number of primary outputs, optionally 1 reject output
- Proper Cobol Copybook or file format definition
- Understanding of the hierarchical structure

## Best Practices
- Validate Copybook definitions before processing
- Use reject link to capture parsing errors

## Property Configuration
Configure Cobol Copybook definitions, record structures, and hierarchical relationships for processing complex flat files.
