# Example: Aggregate with Sort and Fetch

## User Query

> What is the most common bond type?

## Table Schemas

```json
[{"name": "bond", "columns": {"bond_id": "string", "molecule_id": "string", "bond_type": "string"}}]
```

## Generated DSL

```query
# Count occurrences of each bond type
bond_counts = Aggregate(
    plan=bond,
    grouping_exprs=[col("bond_type", alias="bond_type")],
    measures=[count(col("bond_type"), alias="cnt")]
)

# Sort by count descending to get the most common first
sorted_counts = Sort(
    plan=bond_counts,
    exprs_order=[(col("cnt"), "desc")]
)

# Take the top row (most common bond type)
top_bond = Fetch(
    plan=sorted_counts,
    offset=0,
    count=1
)

# Return bond type and its count
result = Select(
    plan=top_bond,
    exprs=[col("bond_type"), col("cnt")]
)

return result
```

## Notes

- ReadTable statements are omitted — `parse_dsl_tool` prepends them automatically when `clean=true`
- `alias` is required on both grouping expressions and measures in `Aggregate`
- `Sort` + `Fetch` pattern is used for "top N" queries
