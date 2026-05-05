# DataStage Transformer Stage

## Purpose
Perform complex data transformations when built-in stages cannot handle the required logic.

## When to Use
- Complex transformation logic with multiple conditions
- Constraint-based filtering and routing
- When multiple transformations are required on fields
- Example: Calculate total sales by customer with conditional logic

## When NOT to Use
- For simple type conversions and keep/drop fields (use Copy stage instead)
- When custom C/C++ logic is needed and performance is critical (use Buildop Stage)
- When Java-based logic is required (use Java Integration Stage)

## Alternative Stage Options
- [BuildOp Stage](BuildopStage.md) - For custom C/C++ logic when Transformer capabilities are insufficient
- [Java Integration Stage](JavaIntegrationStage.md) - For Java-based logic

## Requirements
- **Link Cardinality**: Multiple input/output links supported
- Fields cannot be added to reject links

## Best Practices
- Preferred over Filter and Switch stages
- Preferred over Buildop Stage, Java Integration Stage when builtin functions and conversions are supported
- Add "Otherwise" link to catch unmatched records
- Use stage variables for reusable calculations
- Implement error handling with reject links
- Use a single transformer stage when possible for multiple transformations

### Capabilities
- Multiple input/output links
- Constraint-based filtering
- Built-in functions (string, date, numeric)
- Stage variables
- Loop processing
- Can be extended with custom C functions

## Property Configuration

### transformer_constraint

- Used for filtering records based on a condition
- Use empty constraint with otherwise_log set to True to catch unmatched records if needed.

```python
from ibm_watsonx_data_integration.services.datastage.models.stage_models.complex_stages.transformer import Constraint

transformer_1.configuration.transformer_constraint = [
    Constraint(
        output_name="Link_Valid",
        constraint="RegexMatch(Link_Input.ssn, '^[0-9]{3}-[0-9]{2}-[0-9]{4}$')",
        otherwise_log=False,
        abort_after_rows=0
    ),
    Constraint(
        output_name="Link_Invalid",
        constraint="",
        otherwise_log=True,
        abort_after_rows=0
    )
]
```

- Constraints cannot be used for output links defined as reject links as shown below
- Transformer output links defined as reject must match the input link schema, columns cannot be added to a reject link

```python
from ibm_watsonx_data_integration.services.datastage.models.stage_models.complex_stages.transformer import Constraint

link_reject = transformer.connect_output_to(seq_file_reject)
link_reject.name = "Link_Invalid_SSN"
link_reject.reject()

transformer_1.configuration.transformer_constraint = [
    Constraint(
        output_name="Link_Valid",
        constraint="RegexMatch(Link_Input.ssn, '^[0-9]{3}-[0-9]{2}-[0-9]{4}$')",
        otherwise_log=False,
        abort_after_rows=0
    )
]
```

### Builtin Functions
- For a complete list of available functions refer to the following references grouped by category
- [String handling functions](TransformerStageFunctions/StringFunctionsReference.md)
- [Date and Time functions](TransformerStageFunctions/DateAndTimeFunctionsReference.md)
- [Type Conversion functions](TransformerStageFunctions/TypeConversionFunctionsReference.md)
- [Null handling functions](TransformerStageFunctions/NullHandlingFunctionsReference.md)
- [Numeric functions](TransformerStageFunctions/NumericFunctionsReference.md)
- [Mathematical functions](TransformerStageFunctions/MathematicalFunctionsReference.md)
- [Logical functions](TransformerStageFunctions/LogicalFunctionsReference.md)
- [Utility functions](TransformerStageFunctions/UtilityFunctionsReference.md)
- [Special Conversion functions](TransformerStageFunctions/SpecialConversionFunctionsReference.md)
- [Lookup functions](TransformerStageFunctions/LookupFunctionsReference.md)
- [Vector functions](TransformerStageFunctions/VectorFunctionsReference.md)
