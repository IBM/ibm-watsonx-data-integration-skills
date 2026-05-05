# DataStage Transformer Utility Functions

Reference of builtin transfomer utility functions

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

### MaskData

- **Description**: Mask data
- **Usage**: `string MaskData(string, uint8)`

### MaskDataFormat

- **Description**: Mask data format
- **Usage**: `string MaskDataFormat(string, uint8)`

### MaskDataFormatKeepFirst

- **Description**: Mask data format keep first
- **Usage**: `string MaskDataFormatKeepFirst(string, int32, uint8)`

### MaskDataFormatKeepLast

- **Description**: Mask data format keep last
- **Usage**: `string MaskDataFormatKeepLast(string, int32, uint8)`

### MaskDataFormatWithChar

- **Description**: Mask data format with char
- **Usage**: `string MaskDataFormatWithChar(string, string)`

### MaskDataFormatWithCharKeepFirst

- **Description**: Mask data format with char keep first
- **Usage**: `string MaskDataFormatWithCharKeepFirst(string, int32, string)`

### MaskDataFormatWithCharKeepLast

- **Description**: Mask data format with char keep last
- **Usage**: `string MaskDataFormatWithCharKeepLast(string, int32, string)`

### MaskDataKeepFirst

- **Description**: Mask data keep first
- **Usage**: `string MaskDataKeepFirst(string, int32, uint8)`

### MaskDataKeepLast

- **Description**: Mask data keep last
- **Usage**: `string MaskDataKeepLast(string, int32, uint8)`

### MaskDataWithChar

- **Description**: Mask data with char
- **Usage**: `string MaskDataWithChar(string, string)`

### MaskDataWithCharKeepFirst

- **Description**: Mask data with char keep first
- **Usage**: `string MaskDataWithCharKeepFirst(string, int32, string)`

### MaskDataWithCharKeepLast

- **Description**: Mask data with char keep last
- **Usage**: `string MaskDataWithCharKeepLast(string, int32, string)`

### NextSKChain

- **Description**: Returns the next surrogate key chain integer value
- **Usage**: `int32 NextSKChain(int32:end_of_chain_value)`

### NextSurrogateKey

- **Description**: Returns the next surrogate key integer value from the surrogate key state
- **Usage**: `int32 NextSurrogateKey()`

### PrevSKChain

- **Description**: Returns the previous surrogate key chain integer value
- **Usage**: `int32 PrevSKChain(int32:end_of_chain_value)`

### SaveInputRecord

- **Description**: Saves the current input record and returns the count of saved input records
- **Usage**: `int32 SaveInputRecord()`

### StatusCode

- **Description**: Returns the current internal status code
- **Usage**: `int32 StatusCode()`
