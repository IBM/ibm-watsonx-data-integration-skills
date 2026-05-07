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

### lookup_derivation

**`lookup_derivation`**: Flat list of dicts, one per reference input link. Each dict:
- `reference_link` (required): Name of the reference input link
- `derivations` (required): List of dicts, each with:
  - `key_expression`: Expression to match (column name from primary link)
  - `key_type`: ODBC type string (e.g. `"INTEGER"`, `"VARCHAR"`)
  - `key_column`: Output column name
- `conditionNotMet` (optional): `"continue"`, `"drop"`, or `"fail"`
- `Condition` (optional): Filter expression string
- `lookupFail` (optional): `"continue"`, `"drop"`, or `"fail"`

```python
lookup_stage.configuration.lookup_derivation = [
    lookup.LookupDerivation(
        lookup_failure="continue",
        reference_link="Link_Ref",
        condition=None,
        condition_not_met="fail",
        derivations=[{"key_column": "ID", "key_type": "0", "key_expression": "ID"}],
    )
]
```