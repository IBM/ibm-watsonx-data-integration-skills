# Example: Join with Filter

## User Query

> List all the clients' IDs whose junior credit cards were issued after 1996.

## Table Schemas

```json
[
  {"name": "card", "columns": {"card_id": "i64", "disp_id": "i64", "type": "string", "issued": "date"}},
  {"name": "disp", "columns": {"disp_id": "i64", "client_id": "i64", "account_id": "i64", "type": "string"}}
]
```

## Generated DSL

```query
# Filter cards to only junior type and issued after 1996-12-31
junior_cards = Filter(
    plan=card,
    expr=and(
        equal(col("type"), literal("junior", "string")),
        gt(col("issued"), literal("1996-12-31", "date"))
    )
)

# Join filtered cards with disp to get the associated client_id
cards_with_clients = Join(
    left_plan=junior_cards,
    right_plan=disp,
    expr=equal(col("left.disp_id"), col("right.disp_id")),
    join_type='inner'
)

# Select only the client IDs
output = Select(
    plan=cards_with_clients,
    exprs=[col("client_id")]
)

return output
```

## Notes

- Filter before Join to reduce the number of rows processed
- Join conditions use `left.` and `right.` prefixes to disambiguate columns
- `and()` combines multiple boolean predicates
- Date literals use `"date"` type with `"YYYY-MM-DD"` format
