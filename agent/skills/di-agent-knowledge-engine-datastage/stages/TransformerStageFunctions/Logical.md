# DataStage Logical Transformer Functions

Reference of builtin transfomer logic functions

### BitAnd

- **Description**: Bitwise AND of two integers
- **Usage**: `uint64 BitAnd(uint64:integer, uint64:integer)`

### BitCompress

- **Description**: Convert the given string bit representation (1 and 0s) into an integer
- **Usage**: `uint64 BitCompress(anystring:binarystring)`

### BitExpand

- **Description**: Convert the given integer into a string representation
- **Usage**: `anystring BitExpand(uint64:bitfield)`

### BitOr

- **Description**: Bitwise OR of two integers
- **Usage**: `uint64 BitOr(uint64:integer, uint64:integer)`

### BitXOr

- **Description**: Bitwise exclusive OR of two integers
- **Usage**: `uint64 BitXOr(uint64:integer, uint64:integer)`

### Not

- **Description**: Returns the complement of the logical value of an expression
- **Usage**: `int8 Not(int32:expression)`

### SetBit

- **Description**: Sets bits on or off in a specified field
- **Usage**: `uint64 SetBit(uint64:bitfield, anystring:bitliststring, uint8:bitstate)`
