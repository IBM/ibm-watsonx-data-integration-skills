# DataStage Promote Subrecord Stage

## Purpose
Promote subrecord fields to top-level fields for flattening hierarchical data structures.

## When to Use
- Flattening hierarchical data structures from JSON, XML, COBOL Copybooks
- Converting nested data to flat relational format
- Preparing hierarchical data for relational processing

## When NOT to Use
- When hierarchical structure should be maintained
- For simple field operations without nested structures

## Requirements
- **Link Cardinality**: exactly 1 primary input, exactly 1 primary output
- Handle cases where subrecords may be null or missing
- Ensure promoted field names do not conflict with existing fields

## Best Practices
- Plan field naming to avoid conflicts
- Handle null or missing subrecords appropriately
- Document flattened schema for downstream stages

## Performance
- Promoting subrecords is generally a lightweight operation
- Consider the impact on downstream stages that may need to process more fields
- Monitor memory usage when promoting large subrecords

The input must contain a subrecord field matching the subrecname property. Example: 

```python
rg1 = flow.add_stage("Row Generator", "RG1")
make_subrecord_1 = flow.add_stage("Make Subrecord", "Make_Subrecord_1")
make_subrecord_1.configuration.name = ["subrec0", "subrec1"]
make_subrecord_1.configuration.subrecname = "subrec"
promote_subrecord = flow.add_stage("Promote Subrecord", "Promote_Subrecord")
promote_subrecord.configuration.subrecname = "subrec"
peek1 = flow.add_stage("Peek", "Peek1")

link_1 = rg1.connect_output_to(make_subrecord_1)
link_1.name = "Link_1"
rg1_schema = link_1.create_schema()
rg1_schema.add_field("VARCHAR", "subrec0")
rg1_schema.add_field("VARCHAR", "subrec1")

link_2 = make_subrecord_1.connect_output_to(promote_subrecord)
link_2.name = "Link_2"
make_subrecord_1_schema = link_2.create_schema()
make_subrecord_1_schema.add_field("CHAR", "subrec", source="subrec")
```