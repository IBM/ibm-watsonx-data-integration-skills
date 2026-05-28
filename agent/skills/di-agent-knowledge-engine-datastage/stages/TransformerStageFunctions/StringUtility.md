# DataStage Transformer String Utility Functions

Reference of builtin transfomer string field utility functions

### DQuote

- **Description**: Enclose a string in double quotation marks
- **Usage**: `anystring DQuote(anystring:string)`
- **Example**: If mylink.mystring1 contains the string needs quotes, then the following function returns the string "needs quotes". DQuote(mylink.mystring1)

### DQuoteEscape

- **Description**: Escape double quote characters in the passed string
- **Usage**: `anystring DQuoteEscape(anystring:string)`
- **Example**: If mylink.mystring1 contains the string 'needs "" escape', then the following function returns the string 'needs \"\" escape'. DQuoteEscape(mylink.mystring1)

### Fmt

- **Description**: Format data for output
- **Usage**: `anystring Fmt(anystring:string, anystring:string)`
- **Example**: Using the following example, we will get the output of '1234-5678-9000-0000'. Fmt(1234567890, "%%%%-%%%%-%%%%-%%%%")

### FmtDP

- **Description**: Format a string in display positions
- **Usage**: `anystring FmtDP(anystring:string, anystring:string, anystring:string)`
- **Example**: The following example is the derivation of a function named FmtDP in a Transformer stage: FmtDP(mylink.expression, mylink.format, mylink.mapname)

### Len

- **Description**: Length of string in characters
- **Usage**: `int32 Len(anystring:string)`
- **Example**: If mylink.mystring1 contains the string "chocolate", then the following function returns the value 9. Len(mylink.mystring1)

### LenDP

- **Description**: Length of string in display positions
- **Usage**: `int32 LenDP(anystring:string, anystring:string)`
- **Example**: The following example is the derivation of a function named LenDP in a Transformer stage: LenDP(mylink.string, mylink.mapname)

### NextValidDate

- **Description**: Get next valid date
- **Usage**: `anystring NextValidDate(anystring:string)`
- **Example**: If mylink.date contains the string "2021-12-32", then the following function returns the date string "2022-01-01": NextValidDate(mylink.date)

### PadString

- **Description**: Return the string padded with the specified pad character and specified length
- **Usage**: `anystring PadString(anystring:string, anystring:padstring, int32:padlength)`
- **Example**: If mylink.mystring1 contains the string "AB175", then the following function returns the string "AB17500000". PadString(mylink.mystring1, "0", 5)

### RawLength

- **Description**: Returns the length of a raw string
- **Usage**: `int32 RawLength(raw)`
- **Example**: If mylink.rawdata contains the raw data from a bitmap, then the following function returns the size of the bitmap in bytes: RawLength(mylink.rawdata)

### Reverse

- **Description**: Reverse a string
- **Usage**: `anystring Reverse(anystring:string)`
- **Example**: If mylink.mystring1 contains the string "Hello world", then the following function returns the string "dlrow olleH". Reverse(mylink.mystring1)

### SizeOf

- **Description**: size of the string
- **Usage**: `uint32 SizeOf(string)`
- **Example**: If the current string is "John", then the following function returns 4: SIZEOF(b.%column%) SIZEOF(c.%column%)

### Squote

- **Description**: Enclose a string in single quotation marks
- **Usage**: `anystring Squote(anystring:string)`
- **Example**: If mylink.mystring1 contains the string needs quotes, then the following function returns the string 'needs quotes'. SQuote(mylink.mystring1)

### SQuoteEscape

- **Description**: Escape single quote characters in the passed string
- **Usage**: `anystring SQuoteEscape(anystring:string)`
- **Example**: If mylink.mystring1 contains the string "needs '' escape", then the following function returns the string "needs \'\' escape". SQuoteEscape(mylink.mystring1)

### Str

- **Description**: Repeat a string
- **Usage**: `anystring Str(anystring:string, int32:repeats)`
- **Example**: If mylink.mystring1 contains the string needs "choc", then the following function returns the string "chocchocchocchocchoc". Str(mylink.mystring1, 5)

### StringNumConcatenate

- **Description**: Concatenate string and number
- **Usage**: `anystring StringNumConcatenate(anystring, anystring, int16)`
- **Example**: If mylink.string1 is "hello", and mylink.string2 is "racecar", and num is 4, then the following function returns "hellorace": StringNumConcatenate(mylink.string1, mylink.string2, num)

### StringNumCopy

- **Description**: String number copy
- **Usage**: `anystring StringNumCopy(anystring, int16)`
- **Example**: If mylink.string1 is "racecar", and num is 4, then the following function returns "race": StringNumCopy(mylink.string1, num)
