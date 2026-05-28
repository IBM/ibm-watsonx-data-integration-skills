# DataStage Transformer Utility Functions

Reference of builtin transfomer utility functions

### ForceError

- **Description**: Force error
- **Usage**: `none ForceError(anystring:string)`
- **Example**: If mylink.errorMsg contains the string "Error! Aborting", then the following function stops orchestrate processing with an "Error! Aborting" message: ForceError(mylink.errorMsg)

### GetEnvironment

- **Description**: Return the vaue of the given environment variable
- **Usage**: `anystring GetEnvironment(anystring, anystring)`
- **Example**: If you queried the value of the environment variable name APT_RDBMS_COMMIT_ROWS then the following derivation might return the value "2048". GetEnvironment("APT_RDBMS_COMMIT_ROWS")

### GetNumOfPartitions

- **Description**: get number of partitions
- **Usage**: `int16 GetNumOfPartitions()`
- **Example**: If the current total number of partitions is 2, then the following function returns 1: GetNumOfPartitions()

### GetPartitionNum

- **Description**: get partition number
- **Usage**: `int16 GetPartitionNum()`
- **Example**: If the current partition number is 1, then the following function returns 1: GetPartitionNum()

### GetSavedInputRecord

- **Description**: Make the next saved input record current and return the number of this saved input record
- **Usage**: `int32 GetSavedInputRecord()`
- **Example**: The following example is the derivation of a loop variable named SavedRecordIndex in a Transformer stage: SavedRecordIndex: GetSavedInputRecord()

### LastRow

- **Description**: Returns true when the current input row is the last input row
- **Usage**: `int8 LastRow()`
- **Example**: You can use the following function to detect end of data or end of wave, and then process data accordingly: LastRow() You can call this function when processing an input row, and the function returns TRUE if the current row is the last row in the data, or the end of wave.

### LastRowInGroup

- **Description**: Return whether the value of the given column will change in the next row
- **Usage**: `int8 LastRowInGroup(any:inputcol)`
- **Example**: You can use the following function to detect key breaks, and then process data accordingly: LastRowInGroup(InputColumn) You can call this function when processing an input row, and the function returns TRUE if the value in the named column changes after this row (that is, this row is the last row in a group). The function also returns TRUE if this row is the last row in the input data. If the input data is sorted by more than one column, then LastRowInGroup() can be called with any of those columns as its argument. If the argument specified is the primary sorted key, then the behavior is as described for a single column. If the argument specified is the secondary or other sorted key, then LastRowInGroup() returns TRUE if the value of the specified column is about to change, or if any of its higher level of key columns are about to change. For example, if the primary sorted column is Col1 and the secondary sorted column is Col2, then LastRowInGroup(Col2) returns true when either the value in Col2 is about to change, or the value in Col1 is about to change. Therefore it can return true when Col2 is not about to change but Col1 is, because Col1 is a higher level sorted key than Col2.

### NextSKChain

- **Description**: Returns the next surrogate key chain integer value
- **Usage**: `int32 NextSKChain(int32:end_of_chain_value)`
- **Example**: If you specify the following function in the derivation field for a SKChain column in an SCD stage, the output column contains the value of the surrogate key of the next record in the chain, or the value 180858 if this is the last row in the chain. NextSKChain(180858)

### NextSurrogateKey

- **Description**: Returns the next surrogate key integer value from the surrogate key state
- **Usage**: `int32 NextSurrogateKey()`
- **Example**: The derivation field of your surrogate key column contains the following function: NextSurrogateKey()

### PrevSKChain

- **Description**: Returns the previous surrogate key chain integer value
- **Usage**: `int32 PrevSKChain(int32:end_of_chain_value)`
- **Example**: If you specify the following function in the derivation field for a SKChain column in an SCD stage, the output column contains the value of the surrogate key of the previous record in the chain, or the value 121060 if this is the last row in the chain. PrevSKChain(121060)

### PrintMessage

- **Description**: Prints out the given message string.
- **Usage**: `none PrintMessage(anystring)`
- **Example**: The following example will cause an Info log with the string "My custom log" to be output to the job run log: PrintMessage("My custom log")

### PrintWarning

- **Description**: Prints out the given string as a warning.
- **Usage**: `none PrintWarning(anystring)`
- **Example**: The following example will cause a Warning log with the string "My custom warning" to be output to the job run log: PrintWarning("My custom warning")

### SaveInputRecord

- **Description**: Saves the current input record and returns the count of saved input records
- **Usage**: `int32 SaveInputRecord()`
- **Example**: The following example is the derivation of a stage variable named NumSavedRecords in a Transformer stage: NumSavedRecords: SaveInputRecord()

### SendCustomInstanceReport

- **Description**: Send a custom instance report message to the job monitoring framework
- **Usage**: `anystring SendCustomInstanceReport(anystring, anystring, anystring)`

### SendCustomReport

- **Description**: Send a custom report message to the job monitoring framework
- **Usage**: `anystring SendCustomReport(anystring, anystring, anystring)`

### SetCustomMetadataInfo

- **Description**: Set custom metadata info
- **Usage**: `string SetCustomMetadataInfo(string, string, string)`

### SetCustomSummaryInfo

- **Description**: Set custom summary info
- **Usage**: `anystring SetCustomSummaryInfo(anystring, anystring, anystring)`

### SetUserStatus

- **Description**: Set an internal value for user status
- **Usage**: `int8 SetUserStatus(anystring:string)`
- **Example**: The following command sets a termination code of "sales job done": SetUserStatus("sales job done")

### StatusCode

- **Description**: Returns the internal status code for the previous function call. Non zero values indicate a call failure.
- **Usage**: `int32 StatusCode()`
- **Example**: If a previous call to Iconv() was successful StatusCode() returns 0. If a previous call to Iconv() failed due to invalid data StatusCode() returns 3.
