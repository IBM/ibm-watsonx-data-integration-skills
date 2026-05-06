# DataStage Transformer String Comparison Functions

Reference of builtin transfomer functions for comparing string fields

### AlNum

- **Description**: Return whether the given string consists of alphanumeric characters
- **Usage**: `int8 AlNum(anystring:string)`

### Alpha

- **Description**: Returns 1 if string is purely alphabetic
- **Usage**: `int8 Alpha(anystring:string)`

### Compare

- **Description**: Compares two strings for sorting
- **Usage**: `int32 Compare(anystring:string1, anystring:string2, string:justification, [,justification])`

### CompareNoCase

- **Description**: Case insensitive comparison of two strings
- **Usage**: `int8 CompareNoCase(anystring:string1, anystring:string2)`

### CompareNum

- **Description**: Compare the first n characters of the two strings
- **Usage**: `int8 CompareNum(anystring, anystring, int16)`

### CompareNum

- **Description**: Compare the first n characters of the two strings
- **Usage**: `int8 CompareNum(anystring:string1, anystring:string2, int16:length)`

### CompareNumNoCase

- **Description**: Caseless comparison of the first n characters of the two strings
- **Usage**: `int8 CompareNumNoCase(anystring:string1, anystring:string2, int16:length)`

### contains

- **Description**: Check if string contains the substring
- **Usage**: `int8 contains(anystring:string, anystring:substring)`

### Count

- **Description**: Count number of times a substring occurs in a string
- **Usage**: `int32 Count(anystring:string, anystring:substring, int8)`

### Dcount

- **Description**: Count number of delimited fields in a string
- **Usage**: `int32 Dcount(anystring:string, anystring:delimiter)`

### endsWith

- **Description**: Check if string ends with the substring
- **Usage**: `int8 endsWith(anystring:string, anystring:substring)`

### Index

- **Description**: Find starting character position of substring
- **Usage**: `int32 Index(anystring:string, anystring:substring, int32:occurrence)`

### IndexOfSubstring

- **Description**: Find starting character position of substring
- **Usage**: `int32 IndexOfSubstring(anystring:string, anystring:substring, int32)`

### IndexOfSubstring1

- **Description**: Find starting character position of substring plus 1
- **Usage**: `int32 IndexOfSubstring1(anystring:string, anystring:substring, int32)`

### IsBase64

- **Description**: Return true if the input is in Base64 format
- **Usage**: `int8 IsBase64(anystring:string)`

### Num

- **Description**: Return 1 if string can be converted to a number
- **Usage**: `int8 Num(anystring:string)`

### OffsetOfSubstring

- **Description**: offset of substring
- **Usage**: `int32 OffsetOfSubstring(anystring, anystring, int32)`

### OffsetOfSubstring1

- **Description**: offset of substring plus 1
- **Usage**: `int32 OffsetOfSubstring1(anystring, anystring, int32)`

### RegexMatch

- **Description**: Regex match
- **Usage**: `uint8 RegexMatch(string, string)`

### RegexSearch

- **Description**: Regex search
- **Usage**: `int32 RegexSearch(string, string)`

### startsWith

- **Description**: Check if string starts with the substring
- **Usage**: `int8 startsWith(anystring:string, anystring:substring)`

### StrCmp

- **Description**: Compare two strings
- **Usage**: `int32 StrCmp(anystring, anystring)`

### StringCompare

- **Description**: Compare two strings
- **Usage**: `int8 StringCompare(anystring, anystring)`
