# DataStage Transformer String Utility Functions

Reference of builtin transfomer string field utility functions

### DQuote

- **Description**: Enclose a string in double quotation marks
- **Usage**: `anystring DQuote(anystring:string)`

### DQuoteEscape

- **Description**: Escape double quote
- **Usage**: `anystring DQuoteEscape(anystring:string)`

### Fmt

- **Description**: Format data for output
- **Usage**: `anystring Fmt(anystring:string, anystring:string)`

### FmtDP

- **Description**: Format a string in display positions
- **Usage**: `anystring FmtDP(anystring:string, anystring:string, anystring:string)`

### Len

- **Description**: Length of string in characters
- **Usage**: `int32 Len(anystring:string)`

### LenDP

- **Description**: Length of string in display positions
- **Usage**: `int32 LenDP(anystring:string, anystring:string)`

### NextValidDate

- **Description**: Get next valid date
- **Usage**: `anystring NextValidDate(anystring:string)`

### PadString

- **Description**: Return the string padded with the specified pad character and specified length
- **Usage**: `anystring PadString(anystring:string, anystring:padstring, int32:padlength)`

### RawLength

- **Description**: Returns the length of a raw string
- **Usage**: `int32 RawLength(raw)`

### Reverse

- **Description**: Reverse a string
- **Usage**: `anystring Reverse(anystring:string)`

### SizeOf

- **Description**: size of the string
- **Usage**: `uint32 SizeOf(string)`

### Squote

- **Description**: Enclose a string in single quotation marks
- **Usage**: `anystring Squote(anystring:string)`

### SQuoteEscape

- **Description**: Escape single quote
- **Usage**: `anystring SQuoteEscape(anystring:string)`

### Str

- **Description**: Repeat a string
- **Usage**: `anystring Str(anystring:string, int32:repeats)`

### StringNumConcatenate

- **Description**: Concatenate string and number
- **Usage**: `anystring StringNumConcatenate(anystring, anystring, int16)`

### StringNumCopy

- **Description**: String number copy
- **Usage**: `anystring StringNumCopy(anystring, int16)`
