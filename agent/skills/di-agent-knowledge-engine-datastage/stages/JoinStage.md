# DataStage Join Stage

## Purpose
Combine records from multiple inputs using relational join operations on large datasets.

## When to Use
- Relational joins on large datasets
- Inner, left outer, right outer, or full outer join operations

## When NOT to Use
- For small reference table lookups (use Lookup stage)

## Requirements
- **Link Cardinality**: 2 or more primary inputs, exactly 1 primary output. 
    - Join infers the reference link as the second primary link. Do not use reference links when writing code.
- Hash partitioning on join keys (all inputs)
- Inputs sorted on join keys
- Non-key columns must be nullable for outer joins
- Both input links need schemas with matching key column names
- Output schema should list all columns from both inputs; join key column appears once

## Best Practices
- For Inner Join and Full Outer Join, chose the smaller dataset for the second link

## Performance
- Requires sorting all data on join keys
- Second link (reference) data for each key value must fit in memory

## Property Configuration

### key_properties

Required. An array of Dictionaries. where each dictionary must contain a key name 'key'. May also include whether the key name is case sensitive 'ci-cs' which has values 'ci' for case insensitive and 'cs' for case sensitive.

```python
join_stage.configuration.key_properties = [{"key": "ID"}]
```

### inputlink_ordering_list

Required. Identifies which two named input links contain the data for the left and right of the join.

```python
join_stage.configuration.inputlink_ordering_list = [
    {"link_label": "Left", "link_name": "Link_Left"},
    {"link_label": "Right", "link_name": "Link_Right"},
]
```

### Join Types
- **Inner Join**: Only matching records from both inputs
- **Left Outer Join**: All left + matching right records
- **Right Outer Join**: All right + matching left records
- **Full Outer Join**: All records from both sides

### Output Schemas

The output schema of the join stage must map each field to its source.

```python
output_schema = link.create_schema()
output_schema.add_field("INTEGER", "ID", source="Link_1_Join.ID")
output_schema.add_field("VARCHAR", "COL1", source="Link_1_Join.COL1")
output_schema.add_field("VARCHAR", "COL2", source="Link_2_Join.COL2")
```