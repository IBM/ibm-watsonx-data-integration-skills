# DataStage Transformer System Variables

System variables are built-in read-only values provided by the DataStage runtime. They are referenced with an `@` prefix and require no link name or function call — use them directly in any derivation expression.

### @TRUE

- **Description**: Represents the boolean true value (evaluates to 1)
- **Usage**: `int8 @TRUE`
- **Example**: Return true when Revenue exceeds Cost: `IF mylink.Revenue > mylink.Cost THEN @TRUE ELSE @FALSE`

### @FALSE

- **Description**: Represents the boolean false value (evaluates to 0)
- **Usage**: `int8 @FALSE`
- **Example**: Return false when a condition is not met: `IF mylink.score > 0 THEN @TRUE ELSE @FALSE`

### @INROWNUM

- **Description**: The sequential number of the current row as it enters the Transformer stage (resets to 1 for each partition)
- **Usage**: `int32 @INROWNUM`
- **Example**: Tag each input row with its arrival sequence: `@INROWNUM`

### @ITERATION

- **Description**: The iteration number of the current loop inside a looping Transformer stage
- **Usage**: `int32 @ITERATION`
- **Example**: Use inside a loop to track which iteration is executing: `@ITERATION`

### @NUMPARTITIONS

- **Description**: The total number of partitions for this Transformer stage instance
- **Usage**: `int32 @NUMPARTITIONS`
- **Example**: Compute each row's share of the total partitions: `@PARTITIONNUM : "/" : StringOf(@NUMPARTITIONS)`

### @OUTROWNUM

- **Description**: The sequential number of the current row as it exits the Transformer stage (resets to 1 for each partition)
- **Usage**: `int32 @OUTROWNUM`
- **Example**: Tag each output row with its exit sequence: `@OUTROWNUM`

### @PARTITIONNUM

- **Description**: The partition number on which the current row is being processed (zero-based)
- **Usage**: `int32 @PARTITIONNUM`
- **Example**: Label each row with its processing partition: `@PARTITIONNUM`
