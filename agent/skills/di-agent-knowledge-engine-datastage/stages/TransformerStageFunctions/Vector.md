# DataStage Transformer Vector Functions

Reference of builtin transfomer functions for manipulating vector fields

### ElementAt

- **Description**: Return a specific element of a vector column
- **Usage**: `any ElementAt(any:vectorfield, int64:index)`
- **Example**: The following example outputs the third element of the vector in the column mylink.myvector. : ElementAt(mylink.myvector, 2)

### GetVectorLength

- **Description**: get vector length
- **Usage**: `uint32 GetVectorLength(none)`
- **Example**: The following example is the derivation of a function named GetVectorLength in a Transformer stage: GetVectorLength(mylink.vector)

### SetVectorLength

- **Description**: set vector length
- **Usage**: `none SetVectorLength(none, uint32)`
- **Example**: The following example is the derivation of a function named SetVectorLength in a Transformer stage: SetVectorLength(mylink.vector, 4)
