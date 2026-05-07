# DataStage Transformer Math Functions

Reference of builtin transfomer mathmatical functions

### Abs

- **Description**: Absolute value of any numeric expression
- **Usage**: `int32 Abs(int32:number)`

### Acos

- **Description**: Calculates the trigonometric arc-cosine of an expression
- **Usage**: `dfloat Acos(dfloat:number)`

### Asin

- **Description**: Calculates the trigonometric arc-sine of an expression
- **Usage**: `dfloat Asin(dfloat:number)`

### Atan

- **Description**: Calculates the trigonometric arc-tangent of an expression
- **Usage**: `dfloat Atan(dfloat:number)`

### Atan2

- **Description**: Calculates the trigonometric arc-tangent of arg1/arg2
- **Usage**: `dfloat Atan2(dfloat:number, dfloat:number)`

### Ceil

- **Description**: Calculates the smallest integer value greater than or equal to the given decimal value
- **Usage**: `int32 Ceil(dfloat:number)`

### Cos

- **Description**: Calculates the trigonometric cosine of an expression
- **Usage**: `dfloat Cos(dfloat:number)`

### Cosh

- **Description**: Calculates the hyperbolic cosine of an expression
- **Usage**: `dfloat Cosh(dfloat:number)`

### Div

- **Description**: Outputs the whole part of the real division of two real numbers
- **Usage**: `dfloat Div(dfloat:dividend, dfloat:divisor)`

### Exp

- **Description**: Calculates the result of base 'e' raised to the power designated by the value of the expression
- **Usage**: `dfloat Exp(dfloat:number)`

### Fabs

- **Description**: Calculates the absolute value of the given value
- **Usage**: `dfloat Fabs(dfloat:number)`

### Floor

- **Description**: Calculates the largest integer value less than or equal to the given decimal value
- **Usage**: `int32 Floor(dfloat:number)`

### Ldexp

- **Description**: Calculates a number from an exponent and mantissa
- **Usage**: `dfloat Ldexp(dfloat:mantissa, int32:exponent)`

### Llabs

- **Description**: Returns the absolute value of the given integer
- **Usage**: `uint64 Llabs(int64:number)`

### Ln

- **Description**: Calculates the natural logarithm of an expression in base 'e'
- **Usage**: `dfloat Ln(dfloat:number)`

### Log10

- **Description**: Returns the log to the base 10 of the given value
- **Usage**: `dfloat Log10(dfloat:number)`

### Max

- **Description**: Returns the greater of the two argument values
- **Usage**: `int32 Max(int32:number1, int32:number2)`

### Min

- **Description**: Returns the lower of the two argument values
- **Usage**: `int32 Min(int32:number1, int32:number2)`

### Mod

- **Description**: Calculates the modulo (the remainder) of two expressions
- **Usage**: `int32 Mod(int32:dividend, int32:divisor)`

### Neg

- **Description**: Negate a number
- **Usage**: `dfloat Neg(dfloat:number)`

### Pwr

- **Description**: Calculates the value of an expression when raised to a specified power
- **Usage**: `dfloat Pwr(dfloat:expression, dfloat:power)`

### Rand

- **Description**: Return a psuedo random integer between 0 and 2^32-1
- **Usage**: `uint32 Rand()`

### Random

- **Description**: Returns a random number between 0 2^32-1
- **Usage**: `uint32 Random()`

### Rnd

- **Description**: Return a psuedo random integer between 0 and arg-1
- **Usage**: `none Rnd(uint32)`

### Sin

- **Description**: Calculates the trigonometric sine of an angle
- **Usage**: `dfloat Sin(dfloat:number)`

### Sinh

- **Description**: Calculates the hyperbolic sine of an expression
- **Usage**: `dfloat Sinh(dfloat:number)`

### Sqrt

- **Description**: Calculates the square root of a number
- **Usage**: `dfloat Sqrt(dfloat:number)`

### Srandom

- **Description**: Returns a random number between 0 and arg-1
- **Usage**: `none Srandom(uint32)`

### Tan

- **Description**: Calculates the trigonometric tangent of an angle
- **Usage**: `dfloat Tan(dfloat:number)`

### Tanh

- **Description**: Calculates the hyperbolic tangent of an expression
- **Usage**: `dfloat Tanh(dfloat:number)`
