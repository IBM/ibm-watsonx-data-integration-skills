# DataStage Transformer Math Functions

Reference of builtin transfomer mathmatical functions

### Abs

- **Description**: Absolute value of any numeric expression
- **Usage**: `int32 Abs(int32:number)`
- **Example**: If mylink.number1 contains the number 12 and mylink.number2 contains the number 34, then the following two functions are equivalent, and return the number 22: Abs(12-34) Abs(mylink.mynumber1-mylink.mynumber2) If mylink.number1 contains the number 34 and mylink.number2 contains the number 12, then the following two functions are equivalent, and return the number 22: Abs(34-12) Abs(mylink.mynumber1-mylink.mynumber2)

### Acos

- **Description**: Calculates the trigonometric arc-cosine of an expression
- **Usage**: `dfloat Acos(dfloat:number)`
- **Example**: If mylink.number contains the number 0.707106781, then the following two functions are equivalent, and return the value 0.785398: Acos(0.707106781) Acos(mylink.mynumber)

### Asin

- **Description**: Calculates the trigonometric arc-sine of an expression
- **Usage**: `dfloat Asin(dfloat:number)`
- **Example**: If mylink.number contains the number 0.707106781, then the following two functions are equivalent, and return the value 0.785398: Asin(0.707106781) Asin(mylink.mynumber)

### Atan

- **Description**: Calculates the trigonometric arc-tangent of an expression
- **Usage**: `dfloat Atan(dfloat:number)`
- **Example**: If mylink.number contains the number 135, then the following two functions are equivalent, and return the value 1.56339, which is the angle that has an arc tangent of 135: Atan(135) Atan(mylink.mynumber)

### Atan2

- **Description**: Calculates the trigonometric arc-tangent of arg1/arg2
- **Usage**: `dfloat Atan2(dfloat:number, dfloat:number)`
- **Example**: If mylink.number1 contains the number 10.0 and mylink.number2 contains the number -10.0, then the following two functions are equivalent, and return the value 2.35619: Atan2(10.0. -10.0) Atan2(mylink.mynumber1, mylink.mynumber2)

### Ceil

- **Description**: Calculates the smallest integer value greater than or equal to the given decimal value
- **Usage**: `int32 Ceil(dfloat:number)`
- **Example**: If mylink.number contains the number 2355.66, then the following two functions are equivalent, and return the value 2356: Ceil(2355.66) Ceil(mylink.mynumber)

### Cos

- **Description**: Calculates the trigonometric cosine of an expression
- **Usage**: `dfloat Cos(dfloat:number)`
- **Example**: If mylink.number contains the number 0.785398, then the following two functions are equivalent, and return the value 0.7071: Cos(0.785398) Cos(mylink.mynumber)

### Cosh

- **Description**: Calculates the hyperbolic cosine of an expression
- **Usage**: `dfloat Cosh(dfloat:number)`
- **Example**: If mylink.number contains the number 2, then the following two functions are equivalent, and return the value 3.7622: Cosh(2) Cosh(mylink.mynumber)

### Div

- **Description**: Outputs the whole part of the real division of two real numbers
- **Usage**: `dfloat Div(dfloat:dividend, dfloat:divisor)`
- **Example**: If mylink.dividend contains the number 100, and mylink.divisor contains the number 25, then the following two functions are equivalent, and return the value 4: Div(100, 25) Div(mylink.dividend, mylink.divisor)

### Exp

- **Description**: Calculates the result of base 'e' raised to the power designated by the value of the expression
- **Usage**: `dfloat Exp(dfloat:number)`
- **Example**: If mylink.number contains the number 5, then the following two functions are equivalent, and return the value 54.5982: Exp(5-1) Exp(mylink.number-1)

### Fabs

- **Description**: Calculates the absolute value of the given value
- **Usage**: `dfloat Fabs(dfloat:number)`
- **Example**: If mylink.number contains the number -26.53, then the following two functions are equivalent, and return the value 26.53: Fabs(-26.53) Fabs(mylink.number)

### Floor

- **Description**: Calculates the largest integer value less than or equal to the given decimal value
- **Usage**: `int32 Floor(dfloat:number)`
- **Example**: If mylink.number contains the number 203.25, then the following two functions are equivalent, and return the value 203: Floor(203.25) Floor(mylink.number)

### Ldexp

- **Description**: Calculates a number from an exponent and mantissa
- **Usage**: `dfloat Ldexp(dfloat:mantissa, int32:exponent)`
- **Example**: If mylink.mantissa contains the number 2, and mylink.exponent contains the number 3, then the following two functions are equivalent, and return the value 16: Floor(2, 3) Floor(mylink.mantissa, mylink.exponent)

### Llabs

- **Description**: Returns the absolute value of the given integer
- **Usage**: `uint64 Llabs(int64:number)`
- **Example**: If mylink.number contains the number -26, then the following two functions are equivalent, and return the value 26: Llabs(-26) Llabs(mylink.number)

### Ln

- **Description**: Calculates the natural logarithm of an expression in base 'e'
- **Usage**: `dfloat Ln(dfloat:number)`
- **Example**: If mylink.number contains the number 6, then the following two functions are equivalent, and return the value 1.79176: Ln(6) Ln(mylink.number)

### Log10

- **Description**: Returns the log to the base 10 of the given value
- **Usage**: `dfloat Log10(dfloat:number)`
- **Example**: If mylink.number contains the number 6, then the following two functions are equivalent, and return the value 0.778151: Log10(6) Log10(mylink.number)

### Max

- **Description**: Returns the greater of the two argument values
- **Usage**: `int32 Max(int32:number1, int32:number2)`
- **Example**: If mylink.number1 contains the number 6, and mylink.number1 contains the number 101, then the following two functions are equivalent, and return the value 101: Max(6, 101) Max(mylink.number1, mylink.number2)

### Min

- **Description**: Returns the lower of the two argument values
- **Usage**: `int32 Min(int32:number1, int32:number2)`
- **Example**: If mylink.number1 contains the number 6, and mylink.number1 contains the number 101, then the following two functions are equivalent, and return the value 6: Min(6, 101) Min(mylink.number1, mylink.number2)

### Mod

- **Description**: Calculates the modulo (the remainder) of two expressions
- **Usage**: `int32 Mod(int32:dividend, int32:divisor)`
- **Example**: If mylink.dividend contains the number 115, and mylink.divisor contains the number 25, then the following two functions are equivalent, and return the value 15: Mod(115, 25) Mod(mylink.dividend, mylink.divisor)

### Neg

- **Description**: Negate a number
- **Usage**: `dfloat Neg(dfloat:number)`
- **Example**: If mylink.number contains the number 123, then the following two functions are equivalent, and return the value -123: Neg(123) Neg(mylink.number)

### Pwr

- **Description**: Calculates the value of an expression when raised to a specified power
- **Usage**: `dfloat Pwr(dfloat:expression, dfloat:power)`
- **Example**: If mylink.expression contains the number 2, and mylink.power contains the number 3, then the following two functions are equivalent, and return the value 8: Pwr(2, 3) Pwr(mylink.expression, mylink.power)

### Rand

- **Description**: Return a psuedo random integer between 0 and 2^32-1
- **Usage**: `uint32 Rand()`
- **Example**: Use this function to add a column to your output that contains a pseudorandom number: Rand()

### Random

- **Description**: Returns a random number between 0 2^32-1
- **Usage**: `uint32 Random()`
- **Example**: Use this function to add a column to your output that contains a random number: Random()

### Rnd

- **Description**: Return a psuedo random integer between 0 and arg-1
- **Usage**: `none Rnd(uint32)`
- **Example**: Rnd('10') Will return a random integer between 0 and 10.

### Sin

- **Description**: Calculates the trigonometric sine of an angle
- **Usage**: `dfloat Sin(dfloat:number)`
- **Example**: If mylink.number contains the number 0.785398, then the following two functions are equivalent, and return the value 0.7071: Sin(0.785398) Sin(mylink.mynumber)

### Sinh

- **Description**: Calculates the hyperbolic sine of an expression
- **Usage**: `dfloat Sinh(dfloat:number)`
- **Example**: If mylink.number contains the number 2, then the following two functions are equivalent, and return the value 3.62686: Sinh(2) Sinh(mylink.mynumber)

### Sqrt

- **Description**: Calculates the square root of a number
- **Usage**: `dfloat Sqrt(dfloat:number)`
- **Example**: If mylink.number contains the number 450, then the following two functions are equivalent, and return the value 21.2132: Sqrt(450) Sqrt(mylink.mynumber)

### Srandom

- **Description**: Returns a random number between 0 and arg-1
- **Usage**: `none Srandom(uint32)`
- **Example**: If mylink.givenNum is 1, then this will cause random() to reproduce default set of random numbers: Srandom(mylink.givenNum)

### Tan

- **Description**: Calculates the trigonometric tangent of an angle
- **Usage**: `dfloat Tan(dfloat:number)`
- **Example**: If mylink.number contains the number 0.7853981, then the following two functions are equivalent, and return the value 0.7071: Tan(0.7853981) Tan(mylink.mynumber)

### Tanh

- **Description**: Calculates the hyperbolic tangent of an expression
- **Usage**: `dfloat Tanh(dfloat:number)`
- **Example**: If mylink.number contains the number 2, then the following two functions are equivalent, and return the value 0.964028: Tanh(2) Tanh(mylink.mynumber)
