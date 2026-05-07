# DataStage Transformer Substring Functions

Reference of builtin transfomer functions for substring manipulation of string fields

### Change

- **Description**: Substitutes an element of a string with a replacement element
- **Usage**: `anystring Change(anystring:string, anystring:substring, anystring:replacement, int32:occurrence, int32:begin, [,occurrence[,begin])`

### Convert

- **Description**: Converts specified characters in a string to designated replacement characters
- **Usage**: `anystring Convert(anystring:fromlist, anystring:tolist, anystring:expression)`

### EEEReplace

- **Description**: Replace substring of string
- **Usage**: `anystring EEEReplace(anystring:string, anystring:substring, anystring:replacement, int32:occurrence, int32:begin, [, occurrence[, begin])`

### EEReplace

- **Description**: Replace substring of string
- **Usage**: `anystring EEReplace(anystring:string, anystring:substring, anystring:replacement, int32:occurrence, int32:begin, [, occurrence[, begin])`

### Ereplace

- **Description**: Replace substring of string
- **Usage**: `anystring Ereplace(anystring:string, anystring:substring, anystring:replacement, int32:occurrence, int32:begin, [, occurrence[, begin])`

### Field

- **Description**: Return 1 or more delimited substrings
- **Usage**: `anystring Field(anystring:string, anystring:delimiter, int32:occurrence, int32:number, [number])`

### FieldStore

- **Description**: Modify string fields separated by specified delimiters
- **Usage**: `anystring FieldStore(anystring:string, anystring:string, int32:number, int32:number, anystring:string)`

### FindReplace

- **Description**: Search the given source string, find and replace specified substring with the replacement
- **Usage**: `anystring FindReplace(anystring:string, anystring:string, anystring:string)`

### Fold

- **Description**: Divide a string into a number of substrings separated by field marks
- **Usage**: `anystring Fold(anystring:string, int32:number)`

### FoldDP

- **Description**: Divides a string into a number of substrings in display positions rather than character lengths
- **Usage**: `anystring FoldDP(anystring:string, int32:number, anystring:string)`

### Left

- **Description**: Leftmost n characters of string
- **Usage**: `anystring Left(anystring:string, int32:length)`

### MatchField

- **Description**: Check a string against a match pattern
- **Usage**: `anystring MatchField(anystring:string, anystring:string, int32:number)`

### RegexReplace

- **Description**: Regex replace
- **Usage**: `string RegexReplace(string, string, string)`

### Remove

- **Description**: remove substring
- **Usage**: `string Remove(string, int32)`

### Right

- **Description**: Rightmost n characters of string
- **Usage**: `anystring Right(anystring:string, int32:length)`

### RmUnprint

- **Description**: Remove unprintable string
- **Usage**: `anystring RmUnprint(anystring:string)`

### SubstituteString

- **Description**: Substitute string
- **Usage**: `anystring SubstituteString(anystring, anystring, anystring, int8, int8, int8)`

### Substrings

- **Description**: Substring a string
- **Usage**: `anystring Substrings(anystring, int32, int32)`

### Substrings1

- **Description**: Substring a string
- **Usage**: `anystring Substrings1(anystring, int32, int32)`
