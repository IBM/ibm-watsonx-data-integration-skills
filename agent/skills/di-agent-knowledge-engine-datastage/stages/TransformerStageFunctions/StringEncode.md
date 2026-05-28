# DataStage Transformer String Encoding Functions

Reference of builtin transfomer functions for encoding and encrypting string fields

### Base64ToString

- **Description**: Decode from Base64 format
- **Usage**: `anystring Base64ToString(anystring:string)`
- **Example**: If mylink.mystring1 contains a base 64 encoded string, then the following function returns the base 64 decoded string. Base64ToString(mylink.mystring1)

### Conversion

- **Description**: Perform string conversions in the style of Iconv or Oconv
- **Usage**: `anystring Conversion(anystring:sourcestring, anystring:convchars, anystring:convmode, ["I" or "E"])`
- **Example**: If mylink.mystring contains the string "1111", then the following function returns the value 15: Conversion(mylink.mystring, "MB", "I") If mylink.mystring contains the string "CDE", then the following function returns the value 434445: Conversion(mylink.mystring, "MX0C", "O")

### DecryptString

- **Description**: Decrypts (AES-256) input cipher text with 32-byte key
- **Usage**: `string DecryptString(string, string)`
- **Example**: If Link_1.Phone contains the string "+1 123-456-7890", we encrypt it using a key and then decrypt it using the same key. This function will output the decrypted string "+1 123-456-7890". DecryptString(EncryptString(Link_1.Phone, "12345678912345678912345678912345"), "12345678912345678912345678912345")

### DownCase

- **Description**: Change all uppercase letters in a string to lowercase
- **Usage**: `anystring DownCase(anystring:string)`
- **Example**: If mylink.mystring1 contains the string "CaMel cAsE", then the following function returns the string "camel case". DownCase(mylink.mystring1)

### EncryptString

- **Description**: Encrypts (AES-256) input string with 32-byte key.
- **Usage**: `string EncryptString(string, string)`
- **Example**: If Link_1.Phone contains the string "+1 123-456-7890", this function will output an encrypted string. EncryptString(Link_1.Phone, "12345678912345678912345678912345")

### Iconv

- **Description**: Convert a string to internal form
- **Usage**: `string Iconv(string, string)`
- **Example**: Iconv('9AM','MT') Output will be: 32400

### Soundex

- **Description**: Return the soundex code for a string
- **Usage**: `string Soundex(string, uint8)`
- **Example**: If mylink.mystring1 contains the string "Griffin", then the following function returns the code "G615". Soundex(mylink.mystring1) If mylink.mystring1 contains the string "Griphin" then the following function also returns the code "G615". Soundex(mylink.mystring1)

### StringToBase64

- **Description**: Encode to Base64 format
- **Usage**: `anystring StringToBase64(anystring:string)`
- **Example**: If mylink.mystring1 contains the string "Hello world", then the following function returns the base 64 encoded string. StringToBase64(mylink.mystring1)

### UpCase

- **Description**: Change all lowercase letters in a string to uppercase
- **Usage**: `anystring UpCase(anystring:string)`
- **Example**: If mylink.mystring1 contains the string "CaMel cAsE", then the following function returns the string "CAMEL CASE". UpCase(mylink.mystring1)

### UrlDecode

- **Description**: Decode URL
- **Usage**: `anystring UrlDecode(anystring:string)`
- **Example**: If mylink.urlFragment contains the string "Address%3DHampshire,United%20Kingdom", then the following function returns the string "Address=Hampshire,United Kingdom": UrlDecode(mylink.urlFragment)

### UrlEncode

- **Description**: Encode URL
- **Usage**: `anystring UrlEncode(anystring:string)`
- **Example**: If mylink.string contains a string, then the following function returns the URL encoded string. UrlEncode(myLink.string)
