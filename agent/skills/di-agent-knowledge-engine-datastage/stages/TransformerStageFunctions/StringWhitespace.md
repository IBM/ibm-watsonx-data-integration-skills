# DataStage Transformer String Whitespace Functions

Reference of builtin transfomer functions for dealing with whitespace in string fields

### CompactWhiteSpace

- **Description**: Return the string after reducing all consective whitespace to a single space
- **Usage**: `anystring CompactWhiteSpace(anystring:string)`
- **Example**: If mylink.mystring contains the string "too &nbsp;&nbsp;many&nbsp;&nbsp;&nbsp;&nbsp;spaces", then the following function returns the string "too many spaces": CompactWhiteSpace(mylink.mystring)

### Space

- **Description**: Return a string of N space characters
- **Usage**: `anystring Space(int32:length)`
- **Example**: If mylink.mylength contains the number 100, then the following function returns a string that contains 100 space characters. Space(mylink.mylength)

### StripWhiteSpace

- **Description**: Return the string after stripping all whitespace from a string
- **Usage**: `anystring StripWhiteSpace(anystring:string)`
- **Example**: If mylink.mystring contains the string "too \u00A0\u00A0many\u00A0\u00A0\u00A0\u00A0spaces", then the following function returns the string "toomanyspaces": StripWhiteSpace(mylink.mystring)

### Trim

- **Description**: Remove all leading and trailing spaces and tabs plus reduce internal occurrences to one
- **Usage**: `anystring Trim(anystring:string, anystring:stripchar, string:option)`
- **Example**: If mylink.mystring contains the string " String with whitespace ", then the following function returns the string "String with whitespace": Trim(mylink.mystring). If mylink.mystring contains the string "..Remove..redundant..dots....", then the following function returns the string "Remove.redundant.dots": Trim(mylink.mystring, ".") If mylink.mystring contains the string "Remove..all..dots....", then the following function returns the string "Removealldots": Trim(mylink.mystring, ".", "A") If mylink.mystring contains the string "Remove..trailing..dots....", then the following function returns the string "Remove..trailing..dots": Trim(mylink.mystring, ".", "T")

### TrimB

- **Description**: Remove all trailing spaces and tabs
- **Usage**: `anystring TrimB(anystring:string)`
- **Example**: If mylink.mystring contains the string "too many trailing spaces &nbsp;&nbsp;&nbsp;", then the following function returns the string "too many trailing spaces": TrimB(mylink.mystring)

### TrimF

- **Description**: Remove all leading spaces and tabs
- **Usage**: `anystring TrimF(anystring:string)`
- **Example**: If mylink.mystring contains the string " &nbsp;&nbsp;&nbsp;too many leading spaces", then the following function returns the string "too many leading spaces": TrimF(mylink.mystring)

### TrimLeadingTrailing

- **Description**: Returns a string with leading and trailing whitespace removed
- **Usage**: `anystring TrimLeadingTrailing(anystring:string)`
- **Example**: If mylink.mystring contains the string " too many spaces ", then the following function returns the string "too many spaces": TrimLeadingTrailing(mylink.mystring)
