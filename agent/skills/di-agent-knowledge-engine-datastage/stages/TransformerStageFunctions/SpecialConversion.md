# DataStage Transformer Special Conversion Functions

Reference of builtin transfomer functions for providing specialized conversions

### Ascii

- **Description**: EBCDIC to ASCII string conversion
- **Usage**: `string Ascii(string)`
- **Example**: Using the following example, we will get the output of 'A'. Ascii(Ebcdic("A"))

### ChecksumCRC32

- **Description**: Returns a cyclical redundancy code
- **Usage**: `uint32 ChecksumCRC32(string)`
- **Example**: ChecksumCRC32("A quick fox")

### CRC32

- **Description**: Returns a cyclical redundancy code
- **Usage**: `uint32 CRC32(string)`
- **Example**: CRC32("A quick fox")

### Dtx

- **Description**: Converts a decimal integer into its hexadecimal equivalent
- **Usage**: `string Dtx(string, [,minsize])`
- **Example**: Dtx(12) The output is 'C'.

### Ebcdic

- **Description**: ASCII to EBCDIC string Conversion
- **Usage**: `string Ebcdic(string)`

### md5

- **Description**: Calculates the checksum of the input value
- **Usage**: `anystring md5(anystring:string)`
- **Example**: If mylink.mystring1 contains the string "Hello world", then the following function returns the MD5 128-bit hash value. MD5(mylink.mystring1)

### Oconv

- **Description**: Convert a string to external form
- **Usage**: `string Oconv(string, string)`
- **Example**: Oconv('9166','D2') Output will be: 03 FEB 93

### StringToMD5

- **Description**: Calculates the checksum of the input value
- **Usage**: `anystring StringToMD5(anystring:string)`
- **Example**: If mylink.mystring1 contains the string "Hello world", then the following function returns the MD5 128-bit hash value. StringToMD5(mylink.mystring1)

### Xtd

- **Description**: Converts a hexadecimal string into its decimal equivalent
- **Usage**: `string Xtd(string)`
- **Example**: Xtd('C') The output is '12'.
