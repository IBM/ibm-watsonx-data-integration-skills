# DataStage Transformer String Comparison Functions

Reference of builtin transfomer functions for comparing string fields

### AlNum

- **Description**: Return whether the given string consists of alphanumeric characters
- **Usage**: `int8 AlNum(anystring:string)`
- **Example**: If mylink.mystring1 contains the string "OED_75_9*E", then the following function would return the value 0 (false): AlNum(mylink.mystring1). If mylink.mystring2 contains the string "12redroses", then the following function would return the value 1 (true): AlNum(mylink.mystring2)

### Alpha

- **Description**: Returns 1 if string is purely alphabetic
- **Usage**: `int8 Alpha(anystring:string)`
- **Example**: If mylink.mystring1 contains the string "12redroses", then the following function would return the value 0 (false): Alpha(mylink.mystring1). If mylink.mystring2 contains the string "twelveredroses", then the following function would return the value 1 (true): Alpha(mylink.mystring2)

### Compare

- **Description**: Compares two strings for sorting
- **Usage**: `int32 Compare(anystring:string1, anystring:string2, string:justification, [,justification])`
- **Example**: If mylink.mystring1 contains the string "AB99" and mylink.mystring2 contains the string "AB100", then the following function returns the result 1: Compare(mylink.mystring1, mylink.mystring2, L). If mylink.mystring1 contains the string "AB99" and mylink.mystring2 contains the string "AB100", then the following function returns the result -1: Compare(mylink.mystring1, mylink.mystring2, R)

### CompareNoCase

- **Description**: Case insensitive comparison of two strings
- **Usage**: `int8 CompareNoCase(anystring:string1, anystring:string2)`
- **Example**: If mylink.mystring1 contains the string "Chocolate Cake" and mylink.mystring2 contains the string "chocolate cake", then the following function returns the result 0. CompareNoCase(mylink.mystring1, mylink.mystring2)

### CompareNum

- **Description**: Compare the first n characters of the two strings
- **Usage**: `int8 CompareNum(anystring, anystring, int16)`
- **Example**: If mylink.mystring1 contains the string "Chocolate" and mylink.mystring2 contains the string "Choccy Treat", then the following function returns the result 0. CompareNum(mylink.mystring1, mylink.mystring2, 4)

### CompareNum

- **Description**: Compare the first n characters of the two strings
- **Usage**: `int8 CompareNum(anystring:string1, anystring:string2, int16:length)`
- **Example**: If mylink.mystring1 contains the string "Chocolate" and mylink.mystring2 contains the string "Choccy Treat", then the following function returns the result 0. CompareNum(mylink.mystring1, mylink.mystring2, 4)

### CompareNumNoCase

- **Description**: Caseless comparison of the first n characters of the two strings
- **Usage**: `int8 CompareNumNoCase(anystring:string1, anystring:string2, int16:length)`
- **Example**: If mylink.mystring1 contains the string "chocolate" and mylink.mystring2 contains the string "Choccy Treat", then the following function returns the result 0. CompareNumNoCase(mylink.mystring1, mylink.mystring2, 4)

### contains

- **Description**: Check if string contains the substring
- **Usage**: `int8 contains(anystring:string, anystring:substring)`
- **Example**: If mylink.mystring contains the expression "otter", then the following function returns 0: contains(Link_1.COLUMN_1, 'a') If mylink.mystring contains the expression "caterpillar", then the following function returns 1: contains(Link_1.COLUMN_1, "cat")

### Count

- **Description**: Count number of times a substring occurs in a string
- **Usage**: `int32 Count(anystring:string, anystring:substring, int8)`
- **Example**: If mylink.mystring1 contains the string "chocolate drops, chocolate ice cream, chocolate bars", then the following function returns 3. Count(mylink.mystring1, "choc") By default, the Count function continues the search with the next character, even if it has already been used as part of a matched substring. If mylink.mystring1 contains the string 'TTTT', then the following function returns 3. Count(mylink.mystring1, "TT") If a third optional argument is passed with any value other than 0, then each character in string is matched to substring only once. In this case, when substring is longer than one character and a match is found, the search continues with the character following the matched substring. No part of the matched string is recounted toward another match. For example, the following statement counts two occurrences of substring TT and returns 2. Count(mylink.mystring1, "TT", 1)

### Dcount

- **Description**: Count number of delimited fields in a string
- **Usage**: `int32 Dcount(anystring:string, anystring:delimiter)`
- **Example**: If mylink.mystring1 contains the string "chocolate drops, chocolate ice cream, chocolate bars", then the following function returns 3. Dcount(mylink.mystring1, ", ")

### endsWith

- **Description**: Check if string ends with the substring
- **Usage**: `int8 endsWith(anystring:string, anystring:substring)`
- **Example**: If mylink.mystring contains the expression "frog", then the following function returns 0: endsWith(mylink.mystring, "toad") If mylink.mystring contains the expression "caterpillar", then the following function returns 1: endsWith(mylink.mystring, "pillar")

### Index

- **Description**: Find starting character position of substring. Starting from 1.
- **Usage**: `int32 Index(anystring:string, anystring:substring, int32:occurrence)`
- **Example**: If mylink.mystring1 contains the string "chocolate drops, chocolate ice cream, chocolate bars, chocolate dippers", then the following function returns the value 18. Index(mylink.mystring1, "chocolate", 2)

### IndexOfSubstring

- **Description**: Find starting character position of substring. Starting from 0.
- **Usage**: `int32 IndexOfSubstring(anystring:string, anystring:substring, int32:occurrence)`
- **Example**: If mylink.mystring1 contains the string "chocolate drops, chocolate ice cream, chocolate bars, chocolate dippers", then the following function returns the value 17. IndexOfSubstring(mylink.mystring1, "chocolate", 2)'

### IndexOfSubstring1

- **Description**: Find starting character position of substring plus 1
- **Usage**: `int32 IndexOfSubstring1(anystring:string, anystring:substring, int32:occurrence)`
- **Example**: If mylink.mystring1 contains the string "chocolate drops, chocolate ice cream, chocolate bars, chocolate dippers", then the following function returns the value 18. IndexOfSubstring1(mylink.mystring1, "chocolate", 2)'

### IsBase64

- **Description**: Return true if the input is in Base64 format
- **Usage**: `int8 IsBase64(anystring:string)`
- **Example**: If mylink.mystring1 contains a base 64 encoded string, then the following function returns the value 1. IsBase64(mylink.mystring1)

### Num

- **Description**: Return 1 if string can be converted to a number
- **Usage**: `int8 Num(anystring:string)`
- **Example**: If mylink.mystring1 contains the string "22", then the following function returns the value 1: Num(mylink.mystring1) If mylink.mystring1 contains the string "twenty two", then the following function returns the value 0: Num(mylink.mystring1)

### OffsetOfSubstring

- **Description**: offset of substring
- **Usage**: `int32 OffsetOfSubstring(anystring, anystring, int32)`
- **Example**: If mylink.mystring1 contains the string "chocolate drops, chocolate ice cream, chocolate bars, chocolate dippers", then the following function returns the value 17. OffsetOfSubstring(mylink.mystring1, "chocolate", 2)

### OffsetOfSubstring1

- **Description**: offset of substring plus 1
- **Usage**: `int32 OffsetOfSubstring1(anystring, anystring, int32)`
- **Example**: If mylink.mystring1 contains the string "chocolate drops, chocolate ice cream, chocolate bars, chocolate dippers", then the following function returns the value 18. OffsetOfSubstring1(mylink.mystring1, "chocolate", 2)

### RegexMatch

- **Description**: Regex match
- **Usage**: `uint8 RegexMatch(string, string)`
- **Example**: If the input string is "He!!0 w@rld", and pattern is "[A-Za-z0-9@! ]+", then the following function returns 1 (true). RegexMatch("He!!0 w@rld", "[A-Za-z0-9@! ]+")

### RegexSearch

- **Description**: Regex search
- **Usage**: `int32 RegexSearch(string, string)`
- **Example**: If the input string is "TEST PATTERN", and pattern is "P.T+E", then the following function returns 5. RegexSearch("TEST PATTERN", "P.T+E")

### startsWith

- **Description**: Check if string starts with the substring
- **Usage**: `int8 startsWith(anystring:string, anystring:substring)`
- **Example**: If mylink.mystring contains the expression "cat", then the following function returns 0: startsWith(mylink.mystring, "caterpillar") If mylink.mystring contains the expression "racecar", then the following function returns 1: startsWith(mylink.mystring, "race")

### StrCmp

- **Description**: Compares two strings by lexicographical order. Returns 1 if string_1 is greater than string_2. Returns -1 if string_1 is less than string_2. Returns zero if string_1 and string_2 are equal.
- **Usage**: `int32 StrCmp(anystring, anystring)`
- **Example**: If mylink.string1 is "world", and mylink.string2 is "hello", then the following function returns 1: StrCmp(mylink.string1, mylink.string2)

### StringCompare

- **Description**: Compare two strings
- **Usage**: `int8 StringCompare(anystring, anystring)`
- **Example**: If mylink.string1 is "world", and mylink.string2 is "hello", then the following function returns 1: StringCompare(mylink.string1, mylink.string2)
