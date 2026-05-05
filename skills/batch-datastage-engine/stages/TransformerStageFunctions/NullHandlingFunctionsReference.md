# DataStage Transformer Null Handling Functions

Reference of builtin transfomer functions for processing nullable fields

### HandleNull

- **Description**: handle null
- **Usage**: `none HandleNull(none, string)`

### IsDfloatInbandNull

- **Description**: Check if the dfloat inband is null or not
- **Usage**: `int8 IsDfloatInbandNull(dfloat)`

### IsInt16InbandNull

- **Description**: Check if the int16 inband is null or not
- **Usage**: `int8 IsInt16InbandNull(int16)`

### IsInt32InbandNull

- **Description**: Check if the int32 inband is null or not
- **Usage**: `int8 IsInt32InbandNull(int32)`

### IsInt64InbandNull

- **Description**: Check if the int64 inband is null or not
- **Usage**: `int8 IsInt64InbandNull(int64)`

### IsNotNull

- **Description**: Returns true when an expression does not evaluate to the null value
- **Usage**: `int8 IsNotNull(any:value)`

### IsNull

- **Description**: Returns true when an expression evaluates to the null value
- **Usage**: `int8 IsNull(any:value)`

### IsSfloatInbandNull

- **Description**: Check if the sfloat inband is null or not
- **Usage**: `int8 IsSfloatInbandNull(sfloat)`

### IsStringInbandNull

- **Description**: Check if the string inband is null or not
- **Usage**: `int8 IsStringInbandNull(anystring:string)`

### MakeNull

- **Description**: make null
- **Usage**: `none MakeNull(none, string)`

### NullToEmpty

- **Description**: Return either the given field, if not null, or an empty string if it is
- **Usage**: `any NullToEmpty(any:inputcol)`

### NullToValue

- **Description**: Return either the given field, if not null, or the given value if it is
- **Usage**: `any NullToValue(any:inputcol, any:value)`

### NullToZero

- **Description**: Return either the given field, if not null, or zero if it is
- **Usage**: `any NullToZero(any:inputcol)`

### SetNull

- **Description**: Assign a null value to the target field
- **Usage**: `any SetNull()`
