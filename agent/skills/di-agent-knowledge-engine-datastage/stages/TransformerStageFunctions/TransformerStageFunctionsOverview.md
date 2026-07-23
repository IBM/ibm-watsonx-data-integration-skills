# Transformer Stage Functions

Built-in functions available in DataStage Transformer stage derivation expressions.
Load the specific resource file for the category relevant to your expression.

# Create Transformer Expressions

Always call `validate_transformer_expressions` or `validate_transformer_expressions_from_sdk_code` to validate expressions before finalizing.

## References

| File                                                         | Contents                                                                                                                                                            |
| ------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `stages/TransformerStageFunctions/ConditionalExpressions.md` | If...Then...Else conditional expressions for evaluating boolean conditions in derivations.                                                                          |
| `stages/TransformerStageFunctions/Macros.md`                 | Built-in job-start substitution tokens: DSFlowId, DSFlowName, DSHostName, DSJobController, DSJobId, DSJobInvocationId, DSJobName, DSJobRunId, DSJobStartDate, DSJobStartTime, DSJobStartTimestamp, DSJobWaveNo, DSProjectId, DSProjectName, DSStageName, and GetEnvironment() for runtime environment variables. |
| `stages/TransformerStageFunctions/DateTime.md`               | Date and time manipulation functions: ConvertDatum, ConvertTimeZone, CurrentDate, CurrentTime, CurrentTimeMS, and more.                                             |
| `stages/TransformerStageFunctions/Logical.md`                | Logical and bitwise functions: BitAnd, BitCompress, BitExpand, BitOr, BitXOr.                                                                                       |
| `stages/TransformerStageFunctions/Lookup.md`                 | Lookup functions that convert between string and numeric types using lookup tables: LookupInt16FromString, LookupStringFromInt16, LookupUint32FromString, and more. |
| `stages/TransformerStageFunctions/Math.md`                   | Mathematical functions including trigonometric (Abs, Acos, Asin, Atan, Atan2) and general arithmetic operations.                                                    |
| `stages/TransformerStageFunctions/NullHandling.md`           | Null handling functions for nullable fields: HandleNull and inband null checking for various numeric types.                                                         |
| `stages/TransformerStageFunctions/NumericConversion.md`      | Numeric type conversion functions: AsDouble, AsFloat, AsInteger, Fix, Int32FromDecimal, and more.                                                                   |
| `stages/TransformerStageFunctions/SpecialConversion.md`      | Specialised conversion functions: ASCII/EBCDIC conversion, checksum/CRC, and hexadecimal conversion.                                                                |
| `stages/TransformerStageFunctions/StringCompare.md`          | String comparison and classification functions: AlNum, Alpha, Compare, CompareNoCase, CompareNum.                                                                   |
| `stages/TransformerStageFunctions/StringEncode.md`           | String encoding and encryption functions: Base64ToString, DecryptString, EncryptString, DownCase.                                                                   |
| `stages/TransformerStageFunctions/StringMasking.md`          | String masking functions for obscuring sensitive data, with options to preserve format or keep portions visible.                                                    |
| `stages/TransformerStageFunctions/StringUtility.md`          | String formatting and utility functions: DQuote, DQuoteEscape, Fmt, FmtDP, Len.                                                                                     |
| `stages/TransformerStageFunctions/StringWhitespace.md`       | Whitespace handling functions: CompactWhiteSpace, Space, StripWhiteSpace, Trim.                                                                                     |
| `stages/TransformerStageFunctions/Substring.md`              | Substring manipulation functions: Change, Convert, Ereplace, EEReplace, EEEReplace.                                                                                 |
| `stages/TransformerStageFunctions/SystemVariables.md`        | Built-in read-only runtime variables: @TRUE, @FALSE, @INROWNUM, @ITERATION, @NUMPARTITIONS.                                                                         |
| `stages/TransformerStageFunctions/TypeConversion.md`         | Type conversion functions: Char, DateToDecimal, DateToString, DecimalToDate, DecimalToDecimal.                                                                      |
| `stages/TransformerStageFunctions/Utility.md`                | Utility functions: ForceError, GetEnvironment, GetNumOfPartitions, GetPartitionNum, GetSavedInputRecord.                                                            |
| `stages/TransformerStageFunctions/Vector.md`                 | Vector manipulation functions: ElementAt, GetVectorLength, SetVectorLength.                                                                                         |
