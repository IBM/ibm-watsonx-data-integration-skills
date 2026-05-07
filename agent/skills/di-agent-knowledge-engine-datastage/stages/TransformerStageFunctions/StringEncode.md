# DataStage Transformer String Encoding Functions

Reference of builtin transfomer functions for encoding and encrypting string fields

### Base64ToString

- **Description**: Decode from Base64 format
- **Usage**: `anystring Base64ToString(anystring:string)`

### Conversion

- **Description**: Perform string conversions in the style of Iconv or Oconv
- **Usage**: `anystring Conversion(anystring:sourcestring, anystring:convchars, anystring:convmode, ["I" or "E"])`

### DecryptString

- **Description**: Decrypt string
- **Usage**: `string DecryptString(string, string)`

### DownCase

- **Description**: Change all uppercase letters in a string to lowercase
- **Usage**: `anystring DownCase(anystring:string)`

### EncryptString

- **Description**: Encrypt string
- **Usage**: `string EncryptString(string, string)`

### Iconv

- **Description**: Convert a string to internal form
- **Usage**: `string Iconv(string, string)`

### Soundex

- **Description**: Return the soundex code for a string
- **Usage**: `string Soundex(string, uint8)`

### StringToBase64

- **Description**: Encode to Base64 format
- **Usage**: `anystring StringToBase64(anystring:string)`

### UpCase

- **Description**: Change all lowercase letters in a string to uppercase
- **Usage**: `anystring UpCase(anystring:string)`

### UrlDecode

- **Description**: Decode URL
- **Usage**: `anystring UrlDecode(anystring:string)`

### UrlEncode

- **Description**: Encode URL
- **Usage**: `anystring UrlEncode(anystring:string)`
