# DataStage Sample Stage

## Purpose
Extract statistical samples of records for testing and analysis.

## When to Use
- Statistical sampling of large datasets
- Creating test datasets with representative samples
- Random or systematic sampling requirements
- Example: Extract 10% random sample for testing

## When NOT to Use
- For extracting first N records only (use Head stage instead)
- When all records need to be processed

## Requirements
- **Link Cardinality**: exactly 1 primary input, 1 or more primary outputs

## Best Practices
- Choose appropriate sampling method based on requirements
- Ensure percentages sum to 100% or less when using percent sampling

## Property Configuration

### Sampling Methods
- First N records
- Every Nth record
- Random percentage

### percent_properties

Use when `selection` is `percent` mode. A flat list of dicts, one per output link. The sum of all percentages cannot exceed 100%.

Each dict:
- `output` (required): Output link index
- `percent` (required): Integer percentage (0-100)

```python
sample.configuration.selection = SAMPLE.Selection.percent
sample.configuration.percent_properties = [
    {"output": 0, "percent": 30},
    {"output": 1, "percent": 70}
]
```

### sample

Use when `selection` is `period` mode. Sample every N'th row per partition. Ex: 10.
