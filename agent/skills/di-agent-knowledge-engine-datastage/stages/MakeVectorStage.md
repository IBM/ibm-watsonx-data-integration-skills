# DataStage Make Vector Stage

## Purpose
Create vector fields from scalar input fields for array-based data operations.

## When to Use
- Array-based data operations
- Creating vector structures from scalar fields
- Preparing data for vector processing

## When NOT to Use
- When scalar fields are sufficient
- For simple field operations without arrays

## Requirements
- **Link Cardinality**: exactly 1 primary input, exactly 1 primary output

## Best Practices
- Plan vector structure based on downstream requirements
- Ensure appropriate vector size and data types
- Document vector schema for maintenance

## Property Configuration

### name

Required. The beginning part of the name of the series of consecutively numbered columns (named like xxxyyy0 to xxxyyyn) to be combined into a vector called xxxyyy. These columns must exist on the input link to this stage. 

```python
rowgen = flow.add_stage("Row Generator", "Row_Generator_1")
makevector = flow.add_stage("Make Vector", "Make_Vector_1")
makevector.configuration.name = "VEC"

link = rowgen.connect_output_to(makevector)
schema = link.create_schema()
schema.add_field("INTEGER", "VEC0")
schema.add_field("INTEGER", "VEC1")
schema.add_field("INTEGER", "VEC2")
```