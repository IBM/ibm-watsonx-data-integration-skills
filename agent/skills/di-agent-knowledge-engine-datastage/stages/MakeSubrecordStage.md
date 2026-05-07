# DataStage Make Subrecord Stage

## Purpose
Create subrecord structures from top-level fields to build hierarchical data structures.

## When to Use
- Building hierarchical data structures
- Reverting flattening of schema by Promote Subrecord Stage
- Creating nested data structures

## When NOT to Use
- When flat structure is required
- For simple field grouping without hierarchy

## Requirements
- **Link Cardinality**: exactly 1 primary input, exactly 1 primary output

## Best Practices
- Plan subrecord structure carefully
- Ensure field names are appropriate for nested structure
- Document subrecord schema for maintenance

## Property Configuration

### name

Required. The name of a vector column to combine into the subrecord column.

### subrecname

Required. The name of the subrecord column on the output into which you want to combine one or more vector columns on the input.