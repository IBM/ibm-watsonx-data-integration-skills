# DataStage Logical Transformer Functions

Reference of builtin transfomer logic functions

### BitAnd

- **Description**: Bitwise AND of two integers
- **Usage**: `uint64 BitAnd(uint64:integer, uint64:integer)`
- **Example**: If mylink.mynumber1 contains the number 352 and mylink.mynumber2 contains the number 400, then the following two functions are equivalent, and return the value 256: BitAnd(352, 400) BitAnd(mylink.mynumber1, mylink.mynumber2)

### BitCompress

- **Description**: Convert the given string bit representation (1 and 0s) into an integer
- **Usage**: `uint64 BitCompress(anystring:binarystring)`
- **Example**: If mylink.mynumber1 contains the string "0101100000", then the following two functions are equivalent, and return the number 352. BitCompress("0101100000") BitCompress(mylink.mynumber)

### BitExpand

- **Description**: Convert the given integer into a string representation
- **Usage**: `anystring BitExpand(uint64:bitfield)`
- **Example**: If mylink.mynumber1 contains the number 352, then the following two functions are equivalent, and return the string "0101100000". BitExpand(352) BitExpand(mylink.mynumber)

### BitOr

- **Description**: Bitwise OR of two integers
- **Usage**: `uint64 BitOr(uint64:integer, uint64:integer)`
- **Example**: If mylink.mynumber1 contains the number 352 and mylink.mynumber2 contains the number 400, then the following two functions are equivalent, and return the value 496: BitOr(352, 400) BitOr(mylink.mynumber1, mylink.mynumber2)

### BitXOr

- **Description**: Bitwise exclusive OR of two integers
- **Usage**: `uint64 BitXOr(uint64:integer, uint64:integer)`
- **Example**: If mylink.mynumber1 contains the number 352 and mylink.mynumber2 contains the number 400, then the following two functions are equivalent, and return the value 240: BitXOr(352, 400) BitXOr(mylink.mynumber1, mylink.mynumber2)

### Not

- **Description**: Returns the complement of the logical value of an expression
- **Usage**: `int8 Not(int32:expression)`
- **Example**: If mylink.myexpression contains the expression 5-5, then the following two functions are equivalent, and return the value 1: Not(5-5) Not(mylink.myexpression) If mylink.myexpression contains the expression 5+5, then the following two functions are equivalent, and return the value 0: Not(5+5) Not(mylink.myexpression)

### SetBit

- **Description**: Sets bits on or off in a specified field
- **Usage**: `uint64 SetBit(uint64:bitfield, anystring:bitliststring, uint8:bitstate)`
- **Example**: If mylink.origfield contains the number 352, mylink.bitlist contains the list "2, 4, 8", and mylink.bitstate contains the value 1, then the following two functions are equivalent, and return the value 494: SetBit(356, "2, 4, 8", 1) SetBit(mylink.origfield, mylink.bitlist, mylink.bitstate)
