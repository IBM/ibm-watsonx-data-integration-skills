# DataStage Transformer String Whitespace Functions

Reference of builtin transfomer functions for dealing with whitespace in string fields

### CompactWhiteSpace

- **Description**: Return the string after reducing all consective whitespace to a single space
- **Usage**: `anystring CompactWhiteSpace(anystring:string)`

### Space

- **Description**: Return a string of N space characters
- **Usage**: `anystring Space(int32:length)`

### StripWhiteSpace

- **Description**: Return the string after stripping all whitespace from a string
- **Usage**: `anystring StripWhiteSpace(anystring:string)`

### Trim

- **Description**: Remove all leading and trailing spaces and tabs plus reduce internal occurrences to one
- **Usage**: `anystring Trim(anystring:string, anystring:stripchar, string:option)`

### TrimB

- **Description**: Remove all trailing spaces and tabs
- **Usage**: `anystring TrimB(anystring:string)`

### TrimF

- **Description**: Remove all leading spaces and tabs
- **Usage**: `anystring TrimF(anystring:string)`

### TrimLeadingTrailing

- **Description**: Returns a string with leading and trailing whitespace removed
- **Usage**: `anystring TrimLeadingTrailing(anystring:string)`
