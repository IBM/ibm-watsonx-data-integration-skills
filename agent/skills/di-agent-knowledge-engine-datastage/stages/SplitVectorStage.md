# DataStage Split Vector Stage

## Purpose
Split vector fields into separate scalar fields for data flattening and element-wise processing.

## When to Use
- Data flattening from vector to scalar format
- Element-wise processing of vector data
- Converting vectors to individual fields

## When NOT to Use
- When vector structure should be maintained
- For operations that work directly on vectors

## Requirements
- **Link Cardinality**: exactly 1 primary input, exactly 1 primary output

## Best Practices
- Plan output schema based on vector size
- Ensure field names are appropriate for split elements
- Consider downstream processing requirements

## Property Configuration

The input stage to a split vector stage must contain a vector matching the `name` property. Example: 

```python
rg1 = flow.add_stage("Row Generator", "RG1")
make_vector = flow.add_stage("Make Vector", "make_vector")
make_vector.configuration.name = ["vec0", "vec1"]
make_vector.configuration.name = "vec"

split_vector = flow.add_stage("Split Vector", "split_vector")
split_vector.configuration.name = "vec"
peek1 = flow.add_stage("Peek", "Peek1")

link_1 = rg1.connect_output_to(make_vector)
link_1.name = "Link_1"
rg1_schema = link_1.create_schema()
rg1_schema.add_field("VARCHAR", "vec0")
rg1_schema.add_field("VARCHAR", "vec1")

link_2 = make_vector.connect_output_to(split_vector)
link_2.name = "Link_2"
make_vector_schema = link_2.create_schema()
make_vector_schema.add_field("CHAR", "vec", source="vec")
```