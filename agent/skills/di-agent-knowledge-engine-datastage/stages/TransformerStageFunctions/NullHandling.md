# DataStage Transformer Null Handling Functions

Reference of builtin transfomer functions for processing nullable fields

### HandleNull

- **Description**: If the passed input column value is null sets the current target column to the passed string value
- **Usage**: `none HandleNull(any:inputcol, string)`
- **Example**: If the current column is a non-nullable column, but Link_1.score is nullable, then the following code avoids the current column from being dropped: HandleNull(Link_1.score, \"-100\")

### IsDfloatInbandNull

- **Description**: Check if the dfloat inband is null or not
- **Usage**: `int8 IsDfloatInbandNull(dfloat)`
- **Example**: If mylink.inbandNull contains an inband null, then the following function returns 1: IsDfloatInbandNull(mylink.inbandNull)

### IsInt16InbandNull

- **Description**: Check if the int16 inband is null or not
- **Usage**: `int8 IsInt16InbandNull(int16)`
- **Example**: If mylink.inbandNull contains an inband null, then the following function returns 1: IsInt16InbandNull(mylink.inbandNull)

### IsInt32InbandNull

- **Description**: Check if the int32 inband is null or not
- **Usage**: `int8 IsInt32InbandNull(int32)`
- **Example**: If mylink.inbandNull contains an inband null, then the following function returns 1: IsInt32InbandNull(mylink.inbandNull)

### IsInt64InbandNull

- **Description**: Check if the int64 inband is null or not
- **Usage**: `int8 IsInt64InbandNull(int64)`
- **Example**: If mylink.inbandNull contains an inband null, then the following function returns 1: IsInt64InbandNull(mylink.inbandNull)

### IsNotNull

- **Description**: Returns true when an expression does not evaluate to the null value
- **Usage**: `int8 IsNotNull(any:value)`
- **Example**: If the Derivation field for an output column contained the following code, then the Transformer stage checks if the input column named mylink.mycolumn contains a null value. If the input column does not contain a null, the output column contains the value of the input column. If the input column does contain a null, then the output column contains the string NULL. If IsNotNull(mylink.mycolumn) Then mylink.mycolumn Else "NULL"

### IsNull

- **Description**: Returns true when an expression evaluates to the null value
- **Usage**: `int8 IsNull(any:value)`
- **Example**: If the Derivation field for an output column contained the following code, then the Transformer stage checks if the input column named mylink.mycolumn contains a null value. If the input column contains a null, the output column contains the string NULL. If the input column does not contain a null, then the output column contains the value of the input column. If IsNull(mylink.mycolumn) Then "NULL" Else mylink.mycolumn

### IsSfloatInbandNull

- **Description**: Check if the sfloat inband is null or not
- **Usage**: `int8 IsSfloatInbandNull(sfloat)`
- **Example**: If mylink.inbandNull contains an inband null, then the following function returns 1: IsSfloatInbandNull(mylink.inbandNull)

### IsStringInbandNull

- **Description**: Check if the string inband is null or not
- **Usage**: `int8 IsStringInbandNull(anystring:string)`
- **Example**: If mylink.inbandNull contains an inband null, then the following function returns 1: IsStringInbandNull(mylink.inbandNull)

### MakeNull

- **Description**: Converts an inband null field to out of band null based on the passed string value
- **Usage**: `none MakeNull(any:outputcol, string)`
- **Example**: If mylink.mycolumn matches the passed string the target output derivation column will be set to out of band null, otherwise the target column gets the value of mylink.mycolumn: MakeNull(mylink.mycolumn, "-128")

### NullToEmpty

- **Description**: Return either the given field, if not null, or an empty string if it is
- **Usage**: `any NullToEmpty(any:inputcol)`
- **Example**: If the Derivation field for an output column contained the following code, then the Transformer stage checks if the input column named mylink.mycolumn contains a null value. If the input column contains a null, the output column contains an empty string. If the input column does not contain a null, then the output column contains the value from the input column. NullToEmpty(mylink.mycolumn)

### NullToValue

- **Description**: Return either the given field, if not null, or the given value if it is
- **Usage**: `any NullToValue(any:inputcol, any:value)`
- **Example**: If the Derivation field for an output column contained the following code, then the Transformer stage checks if the input column named mylink.mycolumn contains a null value. If the input column contains a null, the output column contains 42. If the input column does not contain a null, then the output column contains the value from the input column. NullToValue(mylink.mycolumn, 42)

### NullToZero

- **Description**: Return either the given field, if not null, or zero if it is
- **Usage**: `any NullToZero(any:inputcol)`
- **Example**: If the Derivation field for an output column contained the following code, then the Transformer stage checks if the input column named mylink.mycolumn contains a null value. If the input column contains a null, the output column contains zero. If the input column does not contain a null, then the output column contains the value from the input column. NullToZero(mylink.mycolumn)

### SetNull

- **Description**: Assign a null value to the target field
- **Usage**: `any SetNull()`
- **Example**: If the Derivation field for an output column contained the following code, then the Transformer stage sets the output column to null: setnull()
