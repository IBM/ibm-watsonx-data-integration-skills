# DataStage Transformer Type Conversion Functions

Reference of builtin transfomer functions for converting between builtin types

### Char

- **Description**: ASCII character from numeric value
- **Usage**: `anystring Char(int32:number, uint8:allow8bits)`
- **Example**: The following example outputs the ASCII code 65 as the character A. Char(65)

### DateToDecimal

- **Description**: Returns the given date as a packed decimal, with optional format string
- **Usage**: `decimal DateToDecimal(date:date, string:"%yyyy%mm%dd")`
- **Example**: If the column mylink.basedate contains the date 2012-08-18, then the following function stores the date as the decimal number 18082012: DateToDecimal(mylink.basedate, "%dd%mm%yyyy") If the column mylink.basedate contains the date 2012-08-18, and the target column has a length of 10 and a scale of 2, then the following function stores the date as the decimal number 201208.18: DateToDecimal(mylink.basedate)

### DateToString

- **Description**: Return the string representation of the given date
- **Usage**: `anystring DateToString(date, string:"%yyyy-%mm-%dd")`
- **Example**: The following example outputs the date contained in the column mylink.mydate to a string. If mylink.mydate contains the date 18th August, 2009, then the output string is "2009-08-18": DateToString(mylink.mydate) The following example outputs the date contained in the column mylink.mydate to a string with the format dd:mm:yyyy. If mylink.mydate contained the date 18th August, 2009, then the output string would be "18:08:2009": DateToString(mylink.mydate, "%dd:%mm:%yyyy")

### DecimalToDate

- **Description**: Returns the given packed decimal as a date, with optional format string
- **Usage**: `date DecimalToDate(decimal:decimal, string:"%yyyy%mm%dd")`
- **Example**: If the column mylink.mydecdata contains the value 18082012, then the following function returns the date 2012-08-18: DecimalToDate(mylink.basedate, "%dd%mm%yyyy") If the column mylink.mydecdata contains the value -201208.18, then the following function returns the date 2012-08-18: DecimalToDate(mylink.basedate)

### DecimalToDecimal

- **Description**: Returns the given decimal in decimal representation with specified precision and scale
- **Usage**: `decimal DecimalToDecimal(decimal:decimal, string:rounding)`
- **Example**: If the column mylink.mydec contains the decimal number 2.5345, the following function returns the decimal number 00000002.54: DecimalToDecimal(mylink.mydec, "ceil") The following function returns the decimal number 00000002.53: DecimalToDecimal(mylink.mydec, "floor") The following function returns the decimal number 00000002.53: DecimalToDecimal(mylink.mydec, "trunc_zero") The following function returns the decimal number 00000002.53: DecimalToDecimal(mylink.mydec, "round_inf") In all these examples, the target decimal has a length of 10 and a scale of 2.

### DecimalToDFloat

- **Description**: Returns the given decimal in dfloat representation
- **Usage**: `dfloat DecimalToDFloat(decimal:number, string:"fix_zero")`
- **Example**: If the column mylink.mydec contains the decimal number 00000004.00 the following function returns the dfloat number 4.00000000000000000E+00: DecimalToDFloat(mylink.mydec, "fix_zero") If the column mylink.mydec contains the decimal number 00012344.00 the following function returns the dfloat number 1.23440000000000000E+04: DecimalToDFloat(mylink.mydec, "fix_zero") If the column mylink.mydec contains the decimal number 00012344.120 the following function returns the dfloat number 1.23441200000000010E+04: DecimalToDFloat(mylink.mydec, "fix_zero") If the column mylink.mydec contains the decimal number 00012344.120 the following function returns the dfloat number 1.23441200000000010E+04: DecimalToDFloat(mylink.mydec) If the column mylink.mydec contains the decimal number 00012344.000 the following function returns the dfloat number 1.23440000000000000E+04: DecimalToDFloat(mylink.mydec)

### DecimalToString

- **Description**: Return the string representation of the given decimal
- **Usage**: `anystring DecimalToString(decimal:number, string:"[fix_zero][#Csuppress_zero]")`
- **Example**: If the column mylink.mydec contains the decimal number 00000004.00, the following function returns the string "4": DecimalToString(mylink.mydec, "suppress_zero") If the column mylink.mydec contains the decimal number 00000004.00, the following function returns the string "0000000000000000000000000004.0000000000": DecimalToString(mylink.mydec, "fix_zero") If the column mylink.mydec contains the decimal number 00012344.00, the following function returns the string "12344": DecimalToString(mylink.mydec, "suppress_zero") If the column mylink.mydec contains the decimal number 00012344.00, the following function returns the string "0000000000000000000000012344.0000000000": DecimalToString(mylink.mydec, "fix_zero") If the column mylink.mydec contains the decimal number 00012344.120, the following function returns the string "0000000000000000000000012344.1200000000": DecimalToString(mylink.mydec, "fix_zero") If the column mylink.mydec contains the decimal number 00012344.120, the following function returns the string "12344.12": DecimalToString(mylink.mydec, "suppress_zero") If the column mylink.mydec contains the decimal number 00012344.120, the following function returns the string "00012344.120": DecimalToString(mylink.mydec) If the column mylink.mydec contains the decimal number 00012344.000, the following function returns the string "00012344.000": DecimalToString(mylink.mydec)

### DecimalToTime

- **Description**: Returns the given packed decimal as a time, with optional format string
- **Usage**: `time DecimalToTime(decimal:decimal, string:"%hh%nn%ss")`
- **Example**: If the column mylink.mytimedec contains the decimal value 200658, then the following function returns the time 20:06:58: DecimalToTime(mylink.mytimedec) If the column mylink.mytimedec contains the decimal value 580620, then the following function returns the time 20:06:58: DecimalToTime(mylink.mytimedec, "%ss%nn%hh")

### DecimalToTimestamp

- **Description**: Returns the given packed decimal as a timestamp, with optional format string
- **Usage**: `timestamp DecimalToTimestamp(decimal:decimal, string:"%yyyy%mm%dd%hh%nn%ss")`
- **Example**: If the column mylink.mytimestampdec contains the value 19580818200658, then the following function returns the timestamp 1958-08-18 20:06:58: DecimalToTimestamp(mylink.mytimestampdec) If the column mylink.mytimestampdec contains the decimal value 200658580818, then the following function returns the timestamp 1958-08-18 20:06:58: DecimalToTimestamp(mylink.mytimestampdec, "%hh%nn%ss%yy%mm%dd")

### DFloatToDecimal

- **Description**: Returns the given dfloat in decimal representation
- **Usage**: `decimal DFloatToDecimal(dfloat:number, string:rtype)`
- **Example**: If the column mylink.myfloat contains the dfloat number 2.534, the following function returns the decimal number 00000002.54. DFloatToDecimal(mylink.mydec, "ceil") If the column mylink.myfloat contains the dfloat number 2.534, the following function returns the decimal number 00000002.53. DFloatToDecimal(mylink.mydec, "floor") If the column mylink.myfloat contains the dfloat number 2.534, the following function returns the decimal number 00000002.53. DFloatToDecimal(mylink.mydec, "trunc_zero") If the column mylink.myfloat contains the dfloat number 2.534, the following function returns the decimal number 00000002.53. DFloatToDecimal(mylink.mydec, "round_inf")

### DFloatToStringNoExp

- **Description**: Convert the given float to a string with no exponent
- **Usage**: `anystring DFloatToStringNoExp(dfloat:number, string:scale)`
- **Example**: If the column mylink.myfloat contains the dfloat number 2.534, then the following function returns the string 00000002.50: DfloatToStringNoExp(mylink.myfloat, 2)

### IsValid

- **Description**: Return whether the given string is valid for the given type
- **Usage**: `int8 IsValid(string:typestring, anystring:valuestring, anystring:format)`
- **Example**: If the column mylink.mystring contains the string "1", then the following function returns the value 1: IsValid("int8", mylink.mystring) If the column mylink.mystring contains the string "380096.06", then the following function returns the value 0: IsValid("int8", mylink.mystring) If the column mylink.teststring contains the string "12:01:28", then the following function returns the value 1: IsValid("time", mylink.teststring, "%hh:%nn:%ss")

### IsValidDate

- **Description**: Return whether the given date is valid
- **Usage**: `int8 IsValidDate(date)`
- **Example**: If the column mylink.mydate contains the date 2011-09-13, then the following function returns the value 1: IsValidDate(mylink.mydate) If the column mylink.mydate contains the string "380096.06", then the following function returns the value 0, because the converted string is not a valid date: IsValidDate(StringToDate (mylink.mydate))

### IsValidDecimal

- **Description**: Return whether the given decimal is valid
- **Usage**: `int8 IsValidDecimal(decimal, uint8:allzerosisvalid)`
- **Example**: If the column mylink.mynum contains the value 310007.65, then the following function returns the value 1: IsValidDecimal(mylink.mynum) If the column mylink.mynum contains the string "wake-robin", then the following function returns the value 0, because the converted string is not a valid decimal: IsValidDecimal(StringToDecimal (mylink.mynum))

### IsValidTime

- **Description**: Return whether the given time is valid
- **Usage**: `int8 IsValidTime(time)`
- **Example**: If the column mylink.mytime contains the time 23:09:22, then the following function returns the value 1: IsValidTime(mylink.mytime). If the column mylink.mydate contains the string "IbnKayeed", then the following function returns the value 0, because the converted string is not a valid time: IsValidTime(StringToTime (mylink.mytime))

### IsValidTimestamp

- **Description**: Return whether the given timestamp is valid
- **Usage**: `int8 IsValidTimestamp(timestamp)`
- **Example**: If the column mylink.mytimestamp contains the time 2011-09-13 23:09:22, then the following function returns the value 1: IsValidTimestamp(mylink.mytimestamp) If the column mylink.mytimestamp contains the string "one of two", then the following function returns the value 0, because the converted string is not a valid timestamp: IsValidTimestamp(StringToTimestamp (mylink.mytimestamp))

### NumToStr

- **Description**: Convert number to string
- **Usage**: `anystring NumToStr(dfloat:number, int32:precision)`
- **Example**: If mylink.number has a value of 2.244, then the following function returns "2.244": NumToStr(mylink.number, 3)

### NumToStrFixed

- **Description**: Convert number to fixed string
- **Usage**: `anystring NumToStrFixed(dfloat, int32)`
- **Example**: If mylink.number has a value of 2.244, then the following function returns "2.24": NumToStrFixed(mylink.number, 2)

### NumToVar

- **Description**: Convert number to variant
- **Usage**: `string NumToVar(dfloat:number)`
- **Example**: Using the following example, we will get the result of '�e)OY%{izXL'. NumToVar(3.1415926)

### RawNumAt

- **Description**: Returns the integer value at the position of the given raw value
- **Usage**: `int32 RawNumAt(raw, int32:position)`
- **Example**: If the column mylink.myraw contains a raw value derived from the string "hello", then the following function returns the integer 0x68 (the ASCII code for the character h): RawNumAt(mylink.myraw, 0) If the column mylink.myraw contains a raw value derived from the string "hello", then the following function returns 0 because the specified index is out of range: RawNumAt(mylink.myraw, 12)

### RawToString

- **Description**: Returns a string from the given raw value
- **Usage**: `string RawToString(raw)`
- **Example**: If the column mylink.myraw contains a certain sequence of values, then the following function returns the string "11052209". RawNumAt(mylink.myraw)

### Seq

- **Description**: ASCII numeric value of character
- **Usage**: `int32 Seq(anystring:character)`
- **Example**: The following example outputs the character A as the ASCII code 65. Seq("A")

### SeqAt

- **Description**: ASCII numeric value of the character at the given position in the given string
- **Usage**: `int32 SeqAt(anystring:string, int32:index)`
- **Example**: If the column mylink.mystring contains the string "horse", then the following function returns the value 0x6F (that is, the ASCII value of the character o). SeqAt(mylink.mystring, 1)

### StringToDate

- **Description**: Returns a date from the given string in the given format
- **Usage**: `date StringToDate(anystring:datestring, string:"%yyyy-%mm-%dd")`
- **Example**: If the column mylink.mystring contains the string ?1958-08-18?, then the following function returns the date 1958-08-18: StringToDate(mylink.mystring) If the column mylink.mystring contains the string ?18:08:1958?, then the following function returns the date 1958-08-18: StringToDate(mylink.mystring, "%dd:%mm:%yyyy")

### StringToDecimal

- **Description**: Returns the given string in decimal representation
- **Usage**: `decimal StringToDecimal(anystring:string, string:rtype)`
- **Example**: If the column mylink.mystring contains the string "19982.22", and the target is defined as having a precision of 7 and a scale of 2, then the following function returns the decimal 19983.22. StringToDecimal(mylink.mystring) If the column mylink.mystring contains the string "19982.2276", and the target is defined as having a precision of 7 and a scale of 2, then the following function returns the decimal 19983.23. StringToDecimal(mylink.mystring,"ceil")

### StringToRaw

- **Description**: Returns a string in raw representation
- **Usage**: `raw StringToRaw(anystring:string)`
- **Example**: If the column mylink.mystring contains the string "hello", and the target column is defined as being of type Binary then the following function returns a certain value. StringToRaw(mylink.mystring)

### StringToTime

- **Description**: Returns a time representation of the given string
- **Usage**: `time StringToTime(anystring:string, string:"%hh:%nn:%ss")`
- **Example**: If the column mylink.mystring contains the string "20:06:58", then the function returns a time of 20:06:58: StringToTime(mylink.mystring) If the column mylink.mystring contains the string "20: 6:58", then the function returns a time of 20:06:58: StringToTime(mylink.mystring, "%(h, s):$(n, s):$(s, s)")

### StringToTimestamp

- **Description**: Returns a timestamp representation of the given string
- **Usage**: `timestamp StringToTimestamp(anystring:string, string:"%yyyy-%mm-%dd %hh:%nn:%ss")`
- **Example**: If the column mylink.mystring contains the string "1958-08-08 20:06:58", then the function returns the timestamp 1958-08-08 20:06:58: StringToTimestamp(mylink.mystring) If the column mylink.mystring contains the string "8/ 8/1958 20: 6:58", then the function returns the timestamp 1958-08-08 20:06:58: StringToTimestamp(mylink.mystring, "%(d, s)/%(m, s)/%yyyy%(h, s):$(n, s):$(s, s)")

### StringToUString

- **Description**: Return the ustring representation of the given string, with optional map
- **Usage**: `ustring StringToUString(string, string:mapname)`
- **Example**: If the column mylink.mystring contains the string "11052009", then the following function returns the ustring "11052009" StringToUstring(mylink.mystring)

### StrToDecimalOrNull

- **Description**: Convert string to decimal, default to Null when conversion fails
- **Usage**: `decimal StrToDecimalOrNull(anystring:inputcol, anystring:fmtstr1, anystring:fmtstr2)`
- **Example**: If the column mylink.mystring contains the string "19982.22", then the function returns the decimal 19982.22: StrToDecimalOrNull(mylink.mystring, "6", "2") If the conversion fails, null is returned.

### StrToNum

- **Description**: Convert string to number
- **Usage**: `dfloat StrToNum(anystring)`
- **Example**: If mylink.string has a value of "1", then the following function returns 1: StrToNum(mylink.string)

### StrToNumOrNull

- **Description**: Convert string to number, default to null when conversion fails
- **Usage**: `dfloat StrToNumOrNull(anystring:inputcol)`
- **Example**: If mylink.string has a value of "1", then the following function returns 1: StrToNumOrNull(mylink.string) If mylink.string has a value of "abc", then the following function returns null: StrToNumOrNull(mylink.string)

### StrToNumOrZero

- **Description**: Convert string to number, default to 0 when conversion fails
- **Usage**: `dfloat StrToNumOrZero(anystring)`
- **Example**: If mylink.string has a value of "1", then the following function returns 1: StrToNumOrZero(mylink.string) If mylink.string has a value of "abc", then the following function returns 0: StrToNumOrZero(mylink.string)

### StrToTimestampOrInvalid

- **Description**: Convert string to timestamp, default to Invalid when conversion fails
- **Usage**: `timestamp StrToTimestampOrInvalid(anystring:inputcol)`
- **Example**: If the column mylink.mystring contains the string "1958-08-08 20:06:58", then the function returns the timestamp 1958-08-08 20:06:58: StrToTimestampOrInvalid(mylink.mystring) If the conversion fails, an invalid timestamp is returned.

### StrToTimestampOrNull

- **Description**: Convert string to timestamp, default to Null when conversion fails
- **Usage**: `timestamp StrToTimestampOrNull(anystring:inputcol)`
- **Example**: If the column mylink.mystring contains the string "1958-08-08 20:06:58", then the function returns the timestamp 1958-08-08 20:06:58: StrToTimestampOrNull(mylink.mystring) If the conversion fails, null is returned.

### StrToVar

- **Description**: Convert string to variant
- **Usage**: `string StrToVar(anystring)`
- **Example**: Using the following example, we will get the result of '\u0012!@#$%'. StrToVar("!@#$%")

### TimestampToDate

- **Description**: Returns a date from the given timestamp
- **Usage**: `date TimestampToDate(timestamp)`
- **Example**: If the column mylink.mytimestamp contains the timestamp 1958-08-18 20:06:58, then the following function returns the date 1958-08-18: TimestampToDate(mylink.mytimestamp)

### TimestampToDecimal

- **Description**: Returns the given timestamp as a packed decimal, with optional format string
- **Usage**: `decimal TimestampToDecimal(timestamp:timestamp, string:"%yyyy%mm%dd%hh%nn%ss")`
- **Example**: If the column mylink.mytimestamp contains the timestamp 1958-08-18 20:06:58, then the following function returns the decimal value 19580818200658: TimestampToDecimal(mylink.mytimestamp) If the column mylink.mytimestamp contains the timestamp 1958-08-18 20:06:58, then the following function returns the decimal value 200658580818: TimestampToDecimal(mylink.mytimestamp, "%hh%nn%ss%yy%mm%dd")

### TimestampToString

- **Description**: Return the string representation of the given timestamp
- **Usage**: `anystring TimestampToString(timestamp, string:"%yyyy-%mm-%dd %hh:%nn:%ss")`
- **Example**: If the column mylink.mytimestamp contains the timestamp 1958-08-1820:06:58, then the function returns the string "1958-08-1820:06:58": TimestampToString(mylink.mytimestamp) If the column mylink.mytimestamp contains the timestamp 1958-08-1820:06:58, then the function returns the string "18/08/1958 20:06:58": TimestampToString(mylink.mytimestamp, "%dd/%mm/%yyyy %hh:$nn:$ss")

### TimestampToTime

- **Description**: Returns the time from a given timestamp
- **Usage**: `time TimestampToTime(timestamp)`
- **Example**: If the column mylink.mytimestamp contains the timestamp 1958-08-1820:06:58, then the function returns the time 20:06:58: TimestampToTime(mylink.mytimestamp)

### TimeToDecimal

- **Description**: Returns the given time as a packed decimal, with optional format string
- **Usage**: `decimal TimeToDecimal(time:time, string:"%hh%nn%ss")`
- **Example**: If the column mylink.mytime contains the time 20:06:58, then the following function returns the decimal value 200658: TimeToDecimal(mylink.mytime) If the column mylink.mytime contains the time 20:06:58, then the following function returns the decimal value 580620: TimeToDecimal(mylink.mytime, "%ss%nn%hh")

### TimeToString

- **Description**: Return the string representation of the given time
- **Usage**: `anystring TimeToString(time, string:"%hh:%nn:%ss")`
- **Example**: If the column mylink.mytime contains the time 20:06:58, then the following function returns the string "20:06:58": TimeToString(mylink.mytime) If the column mylink.mytime contains the time 20:06:58, then the following function returns the string "58:06:20": TimeToString(mylink.mytime, "%ss:$nn:$hh")

### UniChar

- **Description**: Convert to a single character from a Unicode value
- **Usage**: `ustring UniChar(int32:number)`
- **Example**: If the column mylink.unicode contains the integer 241, then the following function returns the string "\u00F1"\: UniChar(mylink.unicode)

### UniSeq

- **Description**: Convert to a Unicode value from expression
- **Usage**: `int32 UniSeq(ustring)`
- **Example**: If the column mylink.expression contains the string "\u00FB"\, then the following function returns the unicode integer 251: UniSeq(mylink.expression)

### UStringToString

- **Description**: Return the string representation of the given ustring, with optional map
- **Usage**: `string UStringToString(ustring, string:mapname)`
- **Example**: If the column mylink.myustring contains the ustring "11052009", then the following function returns the string "11052009": UstringToString(mylink.myustring)

### VarToBool

- **Description**: Convert variant to boolean
- **Usage**: `int32 VarToBool(string:variant)`
- **Example**: Using the following example, we will get the result of '1'. VarToBool("Test")

### VarToNum

- **Description**: Convert variant to number
- **Usage**: `dfloat VarToNum(string:variant)`
- **Example**: Using the following example, we will get the result of '3.14159'. VarToNum(NumToVar(3.1415926))

### VarToNumOrNull

- **Description**: Convert variant to number, default to Null when conversion fails
- **Usage**: `dfloat VarToNumOrNull(string:inputcol)`
- **Example**: Using the following example, we will get the result of '3.14159'. VarToNumOrNull(NumToVar(3.1415926))

### VarToStr

- **Description**: Convert variant to string
- **Usage**: `anystring VarToStr(string:variant, int32:precision)`
- **Example**: Using the following example, we will get the result of '!@#$%'. VarToStr(StrToVar("!@#$%"), 6)

### VarToStrFixed

- **Description**: Convert variant to fixed string
- **Usage**: `anystring VarToStrFixed(string:variant, int32:precision)`
- **Example**: Using the following example, we will get the result of 'Hello'. VarToStrFixed("Hello", 1)
