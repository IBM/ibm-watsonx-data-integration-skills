# DataStage Lookup Transformer Functions

Reference of builtin transfomer lookup functions

### LookupInt16FromString

- **Description**: lookup int16 from the string
- **Usage**: `int16 LookupInt16FromString(anystring, string)`
- **Example**: If mylink.tableDef has a value of "('off' = 0; 'on' = 1; 'running' = 2; 'processing' = 3;)" then the following function returns the value 3: LookupInt16FromString("processing", mylink.tableDef)

### LookupStringFromInt16

- **Description**: lookup int16 from the ustring
- **Usage**: `anystring LookupStringFromInt16(int16, string)`
- **Example**: If mylink.tableDef has a value of "('off' = 0; 'on' = 1; 'running' = 2; 'processing' = 3;)" then the following function returns the string value "off": LookupStringFromInt16(0, mylink.tableDef)

### LookupStringFromUint32

- **Description**: lookup string from uint32
- **Usage**: `anystring LookupStringFromUint32(uint32, string)`
- **Example**: If mylink.tableDef has a value of "('off' = 0; 'on' = 1; 'running' = 2; 'processing' = 3;)" then the following function returns the string value "off": LookupStringFromUint32(0, mylink.tableDef)

### LookupUint32FromString

- **Description**: lookup uint32 from the string
- **Usage**: `uint32 LookupUint32FromString(anystring, string)`
- **Example**: If mylink.tableDef has a value of "('off' = 0; 'on' = 1; 'running' = 2; 'processing' = 3;)" then the following function returns the value 3: LookupUint32FromString("processing", mylink.tableDef)
