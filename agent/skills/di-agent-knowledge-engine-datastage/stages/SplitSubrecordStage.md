# DataStage Split Subrecord Stage

## Purpose
Separate subrecord into top-level vector fields for parallel processing.

## When to Use
- Converting nested structures to vector format for parallel processing
- Preparing subrecord data for vector operations
- Flattening subrecords into vectors

## When NOT to Use
- When subrecord structure should be maintained
- For simple field operations without vectorization

## Requirements
- **Link Cardinality**: exactly 1 primary input, exactly 1 primary output

## Best Practices
- Consider memory requirements for large vectors
- Plan vector structure based on downstream processing needs
- Test with representative data volumes

## Performance
- Vector operations can be more efficient than iterative processing
- Monitor memory usage for large vectors
- Consider data volume when designing vector structures

## Property Configuration

The input must contain a subrecord field matching the subrecname property. Example: 

```python
rg1 = flow.add_stage("Row Generator", "RG1")
make_subrecord_1 = flow.add_stage("Make Subrecord", "Make_Subrecord_1")
make_subrecord_1.configuration.name = ["subrec0", "subrec1"]
make_subrecord_1.configuration.subrecname = "subrec"
split_subrecord = flow.add_stage("Split Subrecord", "Split_Subrecord")
split_subrecord.configuration.subrecname = "subrec"
peek1 = flow.add_stage("Peek", "Peek1")

link_1 = rg1.connect_output_to(make_subrecord_1)
link_1.name = "Link_1"
rg1_schema = link_1.create_schema()
rg1_schema.add_field("VARCHAR", "subrec0")
rg1_schema.add_field("VARCHAR", "subrec1")

link_2 = make_subrecord_1.connect_output_to(split_subrecord)
link_2.name = "Link_2"
make_subrecord_1_schema = link_2.create_schema()
make_subrecord_1_schema.add_field("CHAR", "subrec", source="subrec")
```