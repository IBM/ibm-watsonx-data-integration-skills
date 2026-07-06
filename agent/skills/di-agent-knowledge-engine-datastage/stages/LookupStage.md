# DataStage Lookup Stage

## Purpose
Enrich data with reference information from small reference tables loaded into memory.

## When to Use
- Small reference table lookups
- When reference data fits in memory

## When NOT to Use
- For large reference tables (use Join stage)

## Requirements
- **Link Cardinality**: exactly 1 primary input, 1 or more reference inputs, exactly 1 primary output, optionally 1 reject output
- Reference data loaded into memory
- No partitioning requirement

## Best Practices
- Use reject link to capture lookup failures
- Configure appropriate failure handling (continue, drop, or fail)
- Monitor memory usage for reference tables

## Performance
- Fast for small lookup tables
- No sorting required

## Property Configuration

### Lookup Types
- **Normal lookup**: Single match per key
- **Sparse lookup**: Optimized for large reference tables
- **Range lookup**: Value within range matching

### has_primary_link

**Required.** Must be set to `True` when a primary link is connected to this lookup stage.

```python
lookup_stage.configuration.has_primary_link = True
```

### inputlink_ordering_list

**Required.** Identifies which input links are the primary and reference links.

```python
lookup_stage.configuration.inputlink_ordering_list = [
    {"link_label": "Primary Link", "link_name": "Link_1"},
    {"link_label": "Reference Link", "link_name": "Link_2"},
]
```

### lookup_derivation

**`lookup_derivation`**: A list of `lookup.LookupDerivation(...)` objects, one per reference input link. Each object takes these keyword arguments (snake_case):

- `reference_link` (required, str): Name of the reference input link
- `derivations` (required, list of dicts): Each dict has exactly these keys:
  - `key_expression`: Expression to match — a column name or literal expression from the primary link (e.g. `"depot_id"` or `'"HELLO"'`)
  - `key_type`: The match type for this key — **not** a column data type. One of the string codes `"0"` (equality, UI "="), `"1"` (equality caseless, UI "a=A(Caseless)"), or `"2"` (range, UI "a..z(Range)"). **Not** type names like `"VARCHAR"` or `"INTEGER"` — only these three codes are accepted.
  - `key_column`: Output column name
- `lookup_failure` (optional, `LOOKUP.LookupFail` enum): What to do when the lookup fails. Use `LOOKUP.LookupFail.fail`, `.cont`, `.drop`, or `.reject`.
- `condition_not_met` (optional, `LOOKUP.ConditionNotMet` enum): What to do when a row doesn't meet the condition. Use `LOOKUP.ConditionNotMet.fail`, `.cont`, `.drop`, or `.reject`.
- `condition` (optional, str or None): A filter expression string

```python
lookup_stage.configuration.lookup_derivation = [
    lookup.LookupDerivation(
        lookup_failure=LOOKUP.LookupFail.cont,
        reference_link="Link_Ref",
        condition=None,
        condition_not_met=LOOKUP.ConditionNotMet.fail,
        derivations=[{"key_column": "depot_id", "key_type": "0", "key_expression": "depot_id"}],
    )
]
```

### Complete Lookup example

```python
flow = project.create_flow(name="My Flow", environment=None, flow_type="batch")
conn = project.connections.get(name="my_conn")

# Primary source
src = flow.add_stage("IBM Cloud Databases for PostgreSQL", "src")
src.use_connection(conn)
src.configuration.schema_name = "my_schema"
src.configuration.table_name = "orders"

# Reference source (lookup table)
ref = flow.add_stage("IBM Cloud Databases for PostgreSQL", "ref")
ref.use_connection(conn)
ref.configuration.schema_name = "my_schema"
ref.configuration.table_name = "customers"

# Lookup stage
lkp = flow.add_stage("Lookup", "lkp")
lkp.configuration.has_primary_link = True
lkp.configuration.inputlink_ordering_list = [
    {"link_label": "Primary Link", "link_name": "link_primary"},
    {"link_label": "Reference Link", "link_name": "link_ref"},
]
lkp.configuration.lookup_derivation = [
    lookup.LookupDerivation(
        lookup_failure=LOOKUP.LookupFail.cont,
        reference_link="link_ref",
        condition=None,
        condition_not_met=LOOKUP.ConditionNotMet.cont,
        derivations=[{"key_column": "customer_name", "key_type": "0", "key_expression": "customer_id"}],
    )
]

# Primary link: src -> lkp
link_primary = src.connect_output_to(lkp)
link_primary.name = "link_primary"
schema_primary = link_primary.create_schema()
schema_primary.add_field("INTEGER", "order_id")
schema_primary.add_field("INTEGER", "customer_id")

# Reference link: ref -> lkp (must call .reference() to set as reference)
link_ref = ref.connect_output_to(lkp)
link_ref.name = "link_ref"
link_ref.reference()
schema_ref = link_ref.create_schema()
schema_ref.add_field("INTEGER", "customer_id")
schema_ref.add_field("VARCHAR", "customer_name", length=100)

# Output link: lkp -> output
link_out = lkp.connect_output_to(flow.add_stage("Peek", "peek"))
link_out.name = "link_out"
```
