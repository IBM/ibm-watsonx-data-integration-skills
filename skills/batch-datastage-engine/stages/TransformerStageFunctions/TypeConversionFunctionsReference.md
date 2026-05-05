# DataStage Transformer Type Conversion Functions

Reference of builtin transfomer functions for converting between builtin types

### Char

- **Description**: ASCII character from numeric value
- **Usage**: `anystring Char(int32:number, uint8:allow8bits)`

### DateToDecimal

- **Description**: Returns the given date as a packed decimal, with optional format string
- **Usage**: `decimal DateToDecimal(date:date, string:"%yyyy%mm%dd")`

### DateToString

- **Description**: Return the string representation of the given date
- **Usage**: `anystring DateToString(date, string:"%yyyy-%mm-%dd")`

### DecimalToDate

- **Description**: Returns the given packed decimal as a date, with optional format string
- **Usage**: `date DecimalToDate(decimal:decimal, string:"%yyyy%mm%dd")`

### DecimalToDecimal

- **Description**: Returns the given decimal in decimal representation with specified precision and scale
- **Usage**: `decimal DecimalToDecimal(decimal:decimal, string:rounding)`

### DecimalToDFloat

- **Description**: Returns the given decimal in dfloat representation
- **Usage**: `dfloat DecimalToDFloat(decimal:number, string:"fix_zero")`

### DecimalToString

- **Description**: Return the string representation of the given decimal
- **Usage**: `anystring DecimalToString(decimal:number, string:"[fix_zero][#Csuppress_zero]")`

### DecimalToTime

- **Description**: Returns the given packed decimal as a time, with optional format string
- **Usage**: `time DecimalToTime(decimal:decimal, string:"%hh%nn%ss")`

### DecimalToTimestamp

- **Description**: Returns the given packed decimal as a timestamp, with optional format string
- **Usage**: `timestamp DecimalToTimestamp(decimal:decimal, string:"%yyyy%mm%dd%hh%nn%ss")`

### DFloatToDecimal

- **Description**: Returns the given dfloat in decimal representation
- **Usage**: `decimal DFloatToDecimal(dfloat:number, string:rtype)`

### DFloatToStringNoExp

- **Description**: Convert the given float to a string with no exponent
- **Usage**: `anystring DFloatToStringNoExp(dfloat:number, string:scale)`

### IsValid

- **Description**: Return whether the given string is valid for the given type
- **Usage**: `int8 IsValid(string:typestring, anystring:valuestring, anystring:format)`

### IsValidDate

- **Description**: Return whether the given date is valid
- **Usage**: `int8 IsValidDate(date)`

### IsValidDecimal

- **Description**: Return whether the given decimal is valid
- **Usage**: `int8 IsValidDecimal(decimal, uint8:allzerosisvalid)`

### IsValidTime

- **Description**: Return whether the given time is valid
- **Usage**: `int8 IsValidTime(time)`

### IsValidTimestamp

- **Description**: Return whether the given timestamp is valid
- **Usage**: `int8 IsValidTimestamp(timestamp)`

### NumToStr

- **Description**: Convert number to string
- **Usage**: `anystring NumToStr(dfloat:number, int32:precision)`

### NumToStrFixed

- **Description**: Convert number to fixed string
- **Usage**: `anystring NumToStrFixed(dfloat, int32)`

### NumToVar

- **Description**: Convert number to variant
- **Usage**: `string NumToVar(dfloat:number)`

### RawNumAt

- **Description**: Returns the integer value at the position of the given raw value
- **Usage**: `int32 RawNumAt(raw, int32:position)`

### RawToString

- **Description**: Returns a string from the given raw value
- **Usage**: `string RawToString(raw)`

### Seq

- **Description**: ASCII numeric value of character
- **Usage**: `int32 Seq(anystring:character)`

### SeqAt

- **Description**: ASCII numeric value of the character at the given position in the given string
- **Usage**: `int32 SeqAt(anystring:string, int32:index)`

### StringToDate

- **Description**: Returns a date from the given string in the given format
- **Usage**: `date StringToDate(anystring:datestring, string:"%yyyy-%mm-%dd")`

### StringToDecimal

- **Description**: Returns the given string in decimal representation
- **Usage**: `decimal StringToDecimal(anystring:string, string:rtype)`

### StringToRaw

- **Description**: Returns a string in raw representation
- **Usage**: `raw StringToRaw(anystring:string)`

### StringToTime

- **Description**: Returns a time representation of the given string
- **Usage**: `time StringToTime(anystring:string, string:"%hh:%nn:%ss")`

### StringToTimestamp

- **Description**: Returns a timestamp representation of the given string
- **Usage**: `timestamp StringToTimestamp(anystring:string, string:"%yyyy-%mm-%dd %hh:%nn:%ss")`

### StringToUString

- **Description**: Return the ustring representation of the given string, with optional map
- **Usage**: `ustring StringToUString(string, string:mapname)`

### StrToDecimalOrNull

- **Description**: Convert string to decimal, default to Null when conversion fails
- **Usage**: `decimal StrToDecimalOrNull(anystring:inputcol, anystring:fmtstr1, anystring:fmtstr2)`

### StrToNum

- **Description**: Convert string to number
- **Usage**: `dfloat StrToNum(anystring)`

### StrToNumOrNull

- **Description**: Convert string to number, default to null when conversion fails
- **Usage**: `dfloat StrToNumOrNull(anystring:inputcol)`

### StrToNumOrZero

- **Description**: Convert string to number Or Zero
- **Usage**: `dfloat StrToNumOrZero(anystring)`

### StrToTimestampOrInvalid

- **Description**: Convert string to timestamp, default to Invalid when conversion fails
- **Usage**: `timestamp StrToTimestampOrInvalid(anystring:inputcol)`

### StrToTimestampOrNull

- **Description**: Convert string to timestamp, default to Null when conversion fails
- **Usage**: `timestamp StrToTimestampOrNull(anystring:inputcol)`

### StrToVar

- **Description**: Convert string to variant
- **Usage**: `string StrToVar(anystring)`

### TimestampToDate

- **Description**: Returns a date from the given timestamp
- **Usage**: `date TimestampToDate(timestamp)`

### TimestampToDecimal

- **Description**: Returns the given timestamp as a packed decimal, with optional format string
- **Usage**: `decimal TimestampToDecimal(timestamp:timestamp, string:"%yyyy%mm%dd%hh%nn%ss")`

### TimestampToString

- **Description**: Return the string representation of the given timestamp
- **Usage**: `anystring TimestampToString(timestamp, string:"%yyyy-%mm-%dd %hh:%nn:%ss")`

### TimestampToTime

- **Description**: Returns the time from a given timestamp
- **Usage**: `time TimestampToTime(timestamp)`

### TimeToDecimal

- **Description**: Returns the given time as a packed decimal, with optional format string
- **Usage**: `decimal TimeToDecimal(time:time, string:"%hh%nn%ss")`

### TimeToString

- **Description**: Return the string representation of the given time
- **Usage**: `anystring TimeToString(time, string:"%hh:%nn:%ss")`

### UniChar

- **Description**: Convert to a single character from a Unicode value
- **Usage**: `ustring UniChar(int32:number)`

### UniSeq

- **Description**: Convert to a Unicode value from expression
- **Usage**: `int32 UniSeq(ustring)`

### UStringToString

- **Description**: Return the string representation of the given ustring, with optional map
- **Usage**: `string UStringToString(ustring, string:mapname)`

### VarToBool

- **Description**: Convert variant to boolean
- **Usage**: `int32 VarToBool(string:variant)`

### VarToNum

- **Description**: Convert variant to number
- **Usage**: `dfloat VarToNum(string:variant)`

### VarToNumOrNull

- **Description**: Convert variant to number, default to Null when conversion fails
- **Usage**: `dfloat VarToNumOrNull(string:inputcol)`

### VarToStr

- **Description**: Convert variant to string
- **Usage**: `anystring VarToStr(string:variant, int32:precision)`

### VarToStrFixed

- **Description**: Convert variant to fixed string
- **Usage**: `anystring VarToStrFixed(string:variant, int32:precision)`
