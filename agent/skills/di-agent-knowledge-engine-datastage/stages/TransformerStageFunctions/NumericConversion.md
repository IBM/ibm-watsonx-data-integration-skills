# DataStage Transformer Numeric Conversion Functions

Reference of builtin transfomer functions for converting numeric types

### AsDouble

- **Description**: Return the given argument as a double
- **Usage**: `dfloat AsDouble(any:number)`
- **Example**: In the following expression, the input column mynumber contains an integer, but the function outputs a double. If mylink.mynumber contains the value 56, then the following two functions are equivalent, and return the value 1.29629629629629619E+01: AsDouble(56/4.32) AsDouble(mylink.mynumber/4.32)

### AsFloat

- **Description**: Return the given argument as a float
- **Usage**: `sfloat AsFloat(any:number)`
- **Example**: In the following expression, the input column mynumber contains an integer, but the function outputs a float. If mylink.mynumber contains the value 56, then the following two functions are equivalent, and return the value 1.29629629629629619E+01: AsFloat(56/4.32) AsFloat(mylink.mynumber/4.32)

### AsInteger

- **Description**: Return the given argument as an integer
- **Usage**: `int64 AsInteger(any:number)`
- **Example**: In the following expression, the input column mynumber contains a double, but the function outputs an integer. If mylink.mynumber contains the value 56, then the following two functions are equivalent, and return the value 13: AsInteger(56/4.32) AsInteger(mylink.mynumber/4.32)

### Fix

- **Description**: Convert a numeric value to a floating-point number with a specified precision
- **Usage**: `decimal Fix(decimal:number, int32:precision, int32:mode, [,mode])`

### Int32FromDecimal

- **Description**: get integer part of the decimal number
- **Usage**: `int32 Int32FromDecimal(decimal, string)`
- **Example**: If mylink.decimal contains the number 1.00, then the following function returns 1: Int32FromDecimal(mylink.decimal, "ceil")

### IsStrNum

- **Description**: Check whether number is valid
- **Usage**: `int32 IsStrNum(anystring)`
- **Example**: If mylink.string has a value of "1", then the following function returns 1: IsStrNum(mylink.string)

### IsVarNum

- **Description**: Check whether variant is number
- **Usage**: `int32 IsVarNum(string:variant)`
- **Example**: Using the following example, we will get the result of 1. IsVarNum("2") \ Using the following example, we will get the result of 0. IsVarNum("A")

### MantissaFromDecimal

- **Description**: Returns the mantissa from the given decimal
- **Usage**: `dfloat MantissaFromDecimal(decimal:number)`
- **Example**: If mylink.number contains the number 243.7675, then the following two functions are equivalent, and return the value 7675: MantissaFromDecimal(243.7675) MantissaFromDecimal(mylink.mynumber)

### MantissaFromDFloat

- **Description**: Returns the mantissa from the given dfloat
- **Usage**: `dfloat MantissaFromDFloat(dfloat:number)`
- **Example**: If mylink.number contains the number 1.234412000000000010E +4, then the following function returns the value 1: MantissaFromDFloat(mylink.mynumber)

### VarCmp

- **Description**: Compare two variants
- **Usage**: `int32 VarCmp(string, string, int32)`
- **Example**: Using the following example, we will get the result of 0. VarCmp('11.123456', '11.123456', 3) \ Using the following example, we will get the result of 1. VarCmp('11.123456890', '11.123456', 3)
