# DataStage Transformer Numeric Conversion Functions

Reference of builtin transfomer functions for converting numeric types

### AsDouble

- **Description**: Return the given argument as a double
- **Usage**: `dfloat AsDouble(any:number)`

### AsFloat

- **Description**: Return the given argument as a float
- **Usage**: `sfloat AsFloat(any:number)`

### AsInteger

- **Description**: Return the given argument as an integer
- **Usage**: `int64 AsInteger(any:number)`

### Fix

- **Description**: Convert a numeric value to a floating-point number with a specified precision
- **Usage**: `decimal Fix(decimal:number, int32:precision, int32:mode, [,mode])`

### Int32FromDecimal

- **Description**: get integer part of the decimal number
- **Usage**: `int32 Int32FromDecimal(decimal, string)`

### IsStrNum

- **Description**: Check whether number is valid
- **Usage**: `int32 IsStrNum(anystring)`

### IsVarNum

- **Description**: Check whether variant is number
- **Usage**: `int32 IsVarNum(string:variant)`

### MantissaFromDecimal

- **Description**: Returns the mantissa from the given decimal
- **Usage**: `dfloat MantissaFromDecimal(decimal:number)`

### MantissaFromDFloat

- **Description**: Returns the mantissa from the given dfloat
- **Usage**: `dfloat MantissaFromDFloat(dfloat:number)`

### VarCmp

- **Description**: Compare two variants
- **Usage**: `int32 VarCmp(string, string, int32)`
