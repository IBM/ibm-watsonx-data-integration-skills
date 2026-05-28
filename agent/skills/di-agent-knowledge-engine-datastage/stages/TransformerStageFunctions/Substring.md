# DataStage Transformer Substring Functions

Reference of builtin transfomer functions for substring manipulation of string fields

### Change

- **Description**: Substitutes an element of a string with a replacement element
- **Usage**: `anystring Change(anystring:string, anystring:substring, anystring:replacement, int32:occurrence, int32:begin, [,occurrence[,begin])`
- **Example**: If mylink.mystring contains the expression "aaabbbcccbbb", then the following function returns the string "aaaZZZcccZZZ": Change(mylink.mystring, "bbb", "ZZZ") If mylink.mystring contains the expression "ABC" and the substring is empty, then the following function returns the string "ABC": Change(mylink.mystring, "", "ZZZ") If mylink.mystring contains the expression "aaabbbcccbbb" and the replacement is empty, then the following function returns the string "aaaccc": Change(mylink.mystring, "bbb", "")

### Convert

- **Description**: Converts specified characters in a string to designated replacement characters
- **Usage**: `anystring Convert(anystring:fromlist, anystring:tolist, anystring:expression)`
- **Example**: If mylink.mystring1 contains the string "NOW IS THE TIME", then the following function returns the string "NOW YS XHE XYME". Convert("TI", "XY", mylink.mystring1)

### EEEReplace

- **Description**: Replace substring of string
- **Usage**: `anystring EEEReplace(anystring:string, anystring:substring, anystring:replacement, int32:occurrence, int32:begin, [, occurrence[, begin])`

### EEReplace

- **Description**: Replace substring of string
- **Usage**: `anystring EEReplace(anystring:string, anystring:substring, anystring:replacement, int32:occurrence, int32:begin, [, occurrence[, begin])`

### Ereplace

- **Description**: Replace substring of string
- **Usage**: `anystring Ereplace(anystring:string, anystring:substring, anystring:replacement, int32:occurrence, int32:begin, [, occurrence[, begin])`
- **Example**: If mylink.mystring contains the expression "ABC" and the substring is empty, the following function returns the value "ZZZABC": Ereplace(mylink.mystring, "", "ZZZ") If mylink.mystring contains the expression "aaabbbcccbbb" and the replacement is empty, the following function returns the value "aaaccc": Ereplace(mylink.mystring, "bbb", "")

### Field

- **Description**: Return 1 or more delimited substrings
- **Usage**: `anystring Field(anystring:string, anystring:delimiter, int32:occurrence, int32:number, [number])`
- **Example**: If mylink.mystring1 contains the string "chocolate drops, chocolate ice cream, chocolate bars, chocolate dippers", then the following function returns the string " chocolate ice cream": Field(mylink.mystring1, ", ", 2). If mylink.mystring1 contains the string "chocolate drops, chocolate ice cream, chocolate bars, chocolate dippers", then the following function returns the string " chocolate ice cream, chocolate bars": Field(mylink.mystring1, ", ", 2, 2)

### FieldStore

- **Description**: Modify string fields separated by specified delimiters
- **Usage**: `anystring FieldStore(anystring:string, anystring:string, int32:number, int32:number, anystring:string)`
- **Example**: If mylink.mystring1 contains the string "racecar|level", the delimiter is "|", start integer is 2, n is 2, and the new string is "noon", then the following function returns the string "racecar|noon|": FieldStore(mylink.mystring1, "|", 2, 2, "noon")

### FindReplace

- **Description**: Search the given source string, find and replace specified substring with the replacement
- **Usage**: `anystring FindReplace(anystring:string, anystring:string, anystring:string)`
- **Example**: If mylink.mystring1 contains the string "A-B-C" and the find substring is "-" and the replacement string is ", " then the following function returns the string "A, B, C". FindReplace(mylink.mystring1, "-", ", ")

### Fold

- **Description**: Divide a string into a number of substrings separated by field marks
- **Usage**: `anystring Fold(anystring:string, int32:number)`
- **Example**: If mylink.mystring1 contains the string "THIS IS A FOLDED STRING.", then the following function returns the result "THISFIS AFFOLDEFDFSTRINFG.": FOLD("THIS IS A FOLDED STRING.", 5)

### FoldDP

- **Description**: Divides a string into a number of substrings in display positions rather than character lengths
- **Usage**: `anystring FoldDP(anystring:string, int32:number, anystring:string)`
- **Example**: Using the following example, we will get the output of 'abcde�fghij�klmno�p'. FoldDP("abcdefghijklmnop", 5, ' ')

### Left

- **Description**: Leftmost n characters of string
- **Usage**: `anystring Left(anystring:string, int32:length)`
- **Example**: If mylink.mystring1 contains the string "chocolate drops, chocolate ice cream, chocolate bars, chocolate dippers", then the following function returns the string "chocolate". Left(mylink.mystring1, 9)

### MatchField

- **Description**: Check a string against a match pattern
- **Usage**: `anystring MatchField(anystring:string, anystring:string, int32:number)`
- **Example**: "pattern" must contain specifiers to cover all characters contained in string. For example, the following statement returns an empty string because not all parts of string are specified in the pattern: MatchField("XYZ123AB", "3X3N", 1) To achieve a positive pattern match on the string in the example, the following statement can be used: MatchField("XYZ123AB", "3X3N0X", 1) This statement returns a value of "XYZ".

### RegexReplace

- **Description**: Regex replace
- **Usage**: `string RegexReplace(string, string, string)`
- **Example**: If the input string is "TEST PATTERN PATTERN TEXT", pattern is "P.T+E", and new pattern is "REPLACE" then the following function returns "TEST REPLACERN REPLACERN TEXT". RegexReplace("TEST PATTERN PATTERN TEXT", "P.T+E", "REPLACE")

### Remove

- **Description**: Successively extract and return dynamic array elements that are separated by system delimiters.
- **Usage**: `string Remove(string, int32)`

### Right

- **Description**: Rightmost n characters of string
- **Usage**: `anystring Right(anystring:string, int32:length)`
- **Example**: If mylink.mystring1 contains the string "chocolate drops, chocolate ice cream, chocolate bars, chocolate dippers", then the following function returns the string "dippers". Right(mylink.mystring1, 7)

### RmUnprint

- **Description**: Remove unprintable string
- **Usage**: `anystring RmUnprint(anystring:string)`
- **Example**: Using the following example, we will get the result of "Test". RmUnprint("����Test����")

### SubstituteString

- **Description**: Substitute string
- **Usage**: `anystring SubstituteString(anystring, anystring, anystring, int8, int8, int8)`
- **Example**: If the column mylink.mystring contains the string "123451234512345", then the following function returns the value "aa2345aa2345aa2345": SubstituteString(mylink.mystring, "1", "aa", 0, 1, 1) If the column mylink.mystring contains the string "123451234512345", then the following function returns the value "1234512345aa2345": SubstituteString(mylink.mystring, "1", "aa", 1, 1, 1) If the column mylink.mystring contains the string "123451234512345", then the following function returns the value "aa23451234512345": SubstituteString(mylink.mystring, "1", "aa", 1, 0, 1) If the column mylink.mystring contains the string "123451234512345", then the following function returns the value "12345aa234512345": SubstituteString(mylink.mystring, "1", "aa", 2, 1, 1)

### Substrings

- **Description**: Return a substring of a string. Indexing is 0 based.
- **Usage**: `anystring Substrings(anystring:string, int32:start, int32:length)`
- **Example**: If mylink.string is "racecar", then the following function returns the value "car": Substrings1("racecar", 4, 6)

### Substrings1

- **Description**: Return a substring of a string. Indexing is 1 based.
- **Usage**: `anystring Substrings1(anystring:string, int32:start, int32:length)`
- **Example**: If mylink.string is "racecar", then the following function returns the value "car": Substrings1("racecar", 5, 7)
