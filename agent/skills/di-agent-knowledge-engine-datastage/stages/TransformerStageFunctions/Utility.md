# DataStage Transformer Utility Functions

Reference of builtin transfomer utility functions

### ForceError

- **Description**: Force error
- **Usage**: `none ForceError(anystring:string)`

### GetEnvironment

- **Description**: Return the vaue of the given environment variable
- **Usage**: `anystring GetEnvironment(anystring, anystring)`

### GetNumOfPartitions

- **Description**: get number of partitions
- **Usage**: `int16 GetNumOfPartitions()`

### GetPartitionNum

- **Description**: get partition number
- **Usage**: `int16 GetPartitionNum()`

### GetSavedInputRecord

- **Description**: Make the next saved input record current and return the number of this saved input record
- **Usage**: `int32 GetSavedInputRecord()`

### LastRow

- **Description**: Returns true when the current input row is the last input row
- **Usage**: `int8 LastRow()`

### LastRowInGroup

- **Description**: Return whether the value of the given column will change in the next row
- **Usage**: `int8 LastRowInGroup(any:inputcol)`

### NextSKChain

- **Description**: Returns the next surrogate key chain integer value
- **Usage**: `int32 NextSKChain(int32:end_of_chain_value)`

### NextSurrogateKey

- **Description**: Returns the next surrogate key integer value from the surrogate key state
- **Usage**: `int32 NextSurrogateKey()`

### PrevSKChain

- **Description**: Returns the previous surrogate key chain integer value
- **Usage**: `int32 PrevSKChain(int32:end_of_chain_value)`

### PrintMessage

- **Description**: print message
- **Usage**: `none PrintMessage(anystring)`

### PrintWarning

- **Description**: print warning
- **Usage**: `none PrintWarning(anystring)`

### SaveInputRecord

- **Description**: Saves the current input record and returns the count of saved input records
- **Usage**: `int32 SaveInputRecord()`

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

### StatusCode

- **Description**: Returns the current internal status code
- **Usage**: `int32 StatusCode()`
