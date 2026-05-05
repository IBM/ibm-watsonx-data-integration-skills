# DataStage Transformer String Functions

Reference of builtin transfomer functions for manipulating string fields

### AlNum

- **Description**: Return whether the given string consists of alphanumeric characters
- **Usage**: `int8 AlNum(anystring:string)`

### Alpha

- **Description**: Returns 1 if string is purely alphabetic
- **Usage**: `int8 Alpha(anystring:string)`

### Base64ToString

- **Description**: Decode from Base64 format
- **Usage**: `anystring Base64ToString(anystring:string)`

### Change

- **Description**: Substitutes an element of a string with a replacement element
- **Usage**: `anystring Change(anystring:string, anystring:substring, anystring:replacement, int32:occurrence, int32:begin, [,occurrence[,begin])`

### CompactWhiteSpace

- **Description**: Return the string after reducing all consective whitespace to a single space
- **Usage**: `anystring CompactWhiteSpace(anystring:string)`

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

### Conversion

- **Description**: Perform string conversions in the style of Iconv or Oconv
- **Usage**: `anystring Conversion(anystring:sourcestring, anystring:convchars, anystring:convmode, ["I" or "E"])`

### Convert

- **Description**: Converts specified characters in a string to designated replacement characters
- **Usage**: `anystring Convert(anystring:fromlist, anystring:tolist, anystring:expression)`

### Count

- **Description**: Count number of times a substring occurs in a string
- **Usage**: `int32 Count(anystring:string, anystring:substring, int8)`

### Dcount

- **Description**: Count number of delimited fields in a string
- **Usage**: `int32 Dcount(anystring:string, anystring:delimiter)`

### DecryptString

- **Description**: Decrypt string
- **Usage**: `string DecryptString(string, string)`

### DownCase

- **Description**: Change all uppercase letters in a string to lowercase
- **Usage**: `anystring DownCase(anystring:string)`

### DQuote

- **Description**: Enclose a string in double quotation marks
- **Usage**: `anystring DQuote(anystring:string)`

### DQuoteEscape

- **Description**: Escape double quote
- **Usage**: `anystring DQuoteEscape(anystring:string)`

### EEEReplace

- **Description**: Replace substring of string
- **Usage**: `anystring EEEReplace(anystring:string, anystring:substring, anystring:replacement, int32:occurrence, int32:begin, [, occurrence[, begin])`

### EEReplace

- **Description**: Replace substring of string
- **Usage**: `anystring EEReplace(anystring:string, anystring:substring, anystring:replacement, int32:occurrence, int32:begin, [, occurrence[, begin])`

### EncryptString

- **Description**: Encrypt string
- **Usage**: `string EncryptString(string, string)`

### endsWith

- **Description**: Check if string ends with the substring
- **Usage**: `int8 endsWith(anystring:string, anystring:substring)`

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

### Fmt

- **Description**: Format data for output
- **Usage**: `anystring Fmt(anystring:string, anystring:string)`

### FmtDP

- **Description**: Format a string in display positions
- **Usage**: `anystring FmtDP(anystring:string, anystring:string, anystring:string)`

### Fold

- **Description**: Divide a string into a number of substrings separated by field marks
- **Usage**: `anystring Fold(anystring:string, int32:number)`

### FoldDP

- **Description**: Divides a string into a number of substrings in display positions rather than character lengths
- **Usage**: `anystring FoldDP(anystring:string, int32:number, anystring:string)`

### ForceError

- **Description**: Force error
- **Usage**: `none ForceError(anystring:string)`

### Iconv

- **Description**: Convert a string to internal form
- **Usage**: `string Iconv(string, string)`

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

### Left

- **Description**: Leftmost n characters of string
- **Usage**: `anystring Left(anystring:string, int32:length)`

### Len

- **Description**: Length of string in characters
- **Usage**: `int32 Len(anystring:string)`

### LenDP

- **Description**: Length of string in display positions
- **Usage**: `int32 LenDP(anystring:string, anystring:string)`

### MatchField

- **Description**: Check a string against a match pattern
- **Usage**: `anystring MatchField(anystring:string, anystring:string, int32:number)`

### NextValidDate

- **Description**: Get next valid date
- **Usage**: `anystring NextValidDate(anystring:string)`

### Num

- **Description**: Return 1 if string can be converted to a number
- **Usage**: `int8 Num(anystring:string)`

### OffsetOfSubstring

- **Description**: offset of substring
- **Usage**: `int32 OffsetOfSubstring(anystring, anystring, int32)`

### OffsetOfSubstring1

- **Description**: offset of substring plus 1
- **Usage**: `int32 OffsetOfSubstring1(anystring, anystring, int32)`

### PadString

- **Description**: Return the string padded with the specified pad character and specified length
- **Usage**: `anystring PadString(anystring:string, anystring:padstring, int32:padlength)`

### PrintMessage

- **Description**: print message
- **Usage**: `none PrintMessage(anystring)`

### PrintWarning

- **Description**: print warning
- **Usage**: `none PrintWarning(anystring)`

### RawLength

- **Description**: Returns the length of a raw string
- **Usage**: `int32 RawLength(raw)`

### RegexMatch

- **Description**: Regex match
- **Usage**: `uint8 RegexMatch(string, string)`

### RegexReplace

- **Description**: Regex replace
- **Usage**: `string RegexReplace(string, string, string)`

### RegexSearch

- **Description**: Regex search
- **Usage**: `int32 RegexSearch(string, string)`

### Remove

- **Description**: remove substring
- **Usage**: `string Remove(string, int32)`

### Reverse

- **Description**: Reverse a string
- **Usage**: `anystring Reverse(anystring:string)`

### Right

- **Description**: Rightmost n characters of string
- **Usage**: `anystring Right(anystring:string, int32:length)`

### RmUnprint

- **Description**: Remove unprintable string
- **Usage**: `anystring RmUnprint(anystring:string)`

### SendCustomInstanceReport

- **Description**: Send custom instance report
- **Usage**: `anystring SendCustomInstanceReport(anystring, anystring, anystring)`

### SendCustomReport

- **Description**: Send custom report
- **Usage**: `anystring SendCustomReport(anystring, anystring, anystring)`

### SetCustomMetadataInfo

- **Description**: set custom metadata info
- **Usage**: `string SetCustomMetadataInfo(string, string, string)`

### SetCustomSummaryInfo

- **Description**: Set custom summary info
- **Usage**: `anystring SetCustomSummaryInfo(anystring, anystring, anystring)`

### SetUserStatus

- **Description**: Set an internal value for user status
- **Usage**: `int8 SetUserStatus(anystring:string)`

### SizeOf

- **Description**: size of the string
- **Usage**: `uint32 SizeOf(string)`

### Soundex

- **Description**: Return the soundex code for a string
- **Usage**: `string Soundex(string, uint8)`

### Space

- **Description**: Return a string of N space characters
- **Usage**: `anystring Space(int32:length)`

### Squote

- **Description**: Enclose a string in single quotation marks
- **Usage**: `anystring Squote(anystring:string)`

### SQuoteEscape

- **Description**: Escape single quote
- **Usage**: `anystring SQuoteEscape(anystring:string)`

### startsWith

- **Description**: Check if string starts with the substring
- **Usage**: `int8 startsWith(anystring:string, anystring:substring)`

### Str

- **Description**: Repeat a string
- **Usage**: `anystring Str(anystring:string, int32:repeats)`

### StrCmp

- **Description**: Compare two strings
- **Usage**: `int32 StrCmp(anystring, anystring)`

### StringCompare

- **Description**: Compare two strings
- **Usage**: `int8 StringCompare(anystring, anystring)`

### StringNumConcatenate

- **Description**: Concatenate string and number
- **Usage**: `anystring StringNumConcatenate(anystring, anystring, int16)`

### StringNumCopy

- **Description**: String number copy
- **Usage**: `anystring StringNumCopy(anystring, int16)`

### StringToBase64

- **Description**: Encode to Base64 format
- **Usage**: `anystring StringToBase64(anystring:string)`

### StripWhiteSpace

- **Description**: Return the string after stripping all whitespace from a string
- **Usage**: `anystring StripWhiteSpace(anystring:string)`

### SubstituteString

- **Description**: Substitute string
- **Usage**: `anystring SubstituteString(anystring, anystring, anystring, int8, int8, int8)`

### Substrings

- **Description**: Substring a string
- **Usage**: `anystring Substrings(anystring, int32, int32)`

### Substrings1

- **Description**: Substring a string
- **Usage**: `anystring Substrings1(anystring, int32, int32)`

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

### UpCase

- **Description**: Change all lowercase letters in a string to uppercase
- **Usage**: `anystring UpCase(anystring:string)`

### UrlDecode

- **Description**: Decode URL
- **Usage**: `anystring UrlDecode(anystring:string)`

### UrlEncode

- **Description**: Encode URL
- **Usage**: `anystring UrlEncode(anystring:string)`
