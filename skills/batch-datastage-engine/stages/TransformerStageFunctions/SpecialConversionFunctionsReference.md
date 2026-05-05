# DataStage Transformer Special Conversion Functions

Reference of builtin transfomer functions for providing specialized conversions

### Ascii

- **Description**: EBCDIC to ASCII string conversion
- **Usage**: `string Ascii(string)`

### ChecksumCRC32

- **Description**: Returns a cyclical redundancy code
- **Usage**: `uint32 ChecksumCRC32(string)`

### CRC32

- **Description**: Returns a cyclical redundancy code
- **Usage**: `uint32 CRC32(string)`

### Dtx

- **Description**: Converts a decimal integer into its hexadecimal equivalent
- **Usage**: `string Dtx(string, int32:minsize, [,minsize])`

### Ebcdic

- **Description**: ASCII to EBCDIC string Conversion
- **Usage**: `string Ebcdic(string)`

### md5

- **Description**: Calculates the checksum of the input value
- **Usage**: `anystring md5(anystring:string)`

### Oconv

- **Description**: Convert a string to external form
- **Usage**: `string Oconv(string, string)`

### StringToMD5

- **Description**: Calculates the checksum of the input value
- **Usage**: `anystring StringToMD5(anystring:string)`

### Xtd

- **Description**: Converts a hexadecimal string into its decimal equivalent
- **Usage**: `string Xtd(string)`
