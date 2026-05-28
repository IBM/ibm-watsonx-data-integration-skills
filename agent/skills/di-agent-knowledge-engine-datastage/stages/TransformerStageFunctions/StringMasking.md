# DataStage Transformer String Masking Functions

Reference of builtin transfomer string masking functions

### MaskData

- **Description**: Mask all input characters with the optional mask-byte character, or the '*' character if no mask-byte is supplied.
- **Usage**: `string MaskData(string, uint8)`
- **Example**: If Link_1.Phone contains the string "+1 123-456-7890", the following function returns the masked string "###############". MaskData("+1 123-456-7890", 35)

### MaskDataFormat

- **Description**: Mask all alphanumeric input characters in the specified format with the optional mask-byte character, or the '*' character if no mask-byte is supplied, while preserving the format.
- **Usage**: `string MaskDataFormat(string, uint8)`
- **Example**: If Link_1.Phone contains the string "+1 123-456-7890", the following function returns the masked string "+# ###-###-####". MaskDataFormat("+1 123-456-7890", 35)

### MaskDataFormatKeepFirst

- **Description**: Mask all alphanumeric input except the first number of characters unmodified from the beginning of the string in the specified format with the optional mask-byte character, or the '*' character if no mask-byte is supplied, while preserving the format.
- **Usage**: `string MaskDataFormatKeepFirst(string, int32, uint8)`
- **Example**: If Link_1.Phone contains the string "+1 123-456-7890", the following function returns the masked string "+1 1##-###-####". MaskDataFormatKeepFirst("+1 123-456-7890", 4, 35)

### MaskDataFormatKeepLast

- **Description**: Mask all alphanumeric input except the last number of characters unmodified from the end of the string in the specified format with the optional mask-byte character, or the '*' character if no mask-byte is supplied, while preserving the format.
- **Usage**: `string MaskDataFormatKeepLast(string, int32, uint8)`
- **Example**: If Link_1.Phone contains the string "+1 123-456-7890", the following function returns the masked string "+# ###-###-7890". MaskDataFormatKeepLast("+1 123-456-7890", 4, 35)

### MaskDataFormatWithChar

- **Description**: Mask all alphanumeric input characters in the specified format with the specified character, or the '*' character if no character is supplied, while preserving the format.
- **Usage**: `string MaskDataFormatWithChar(string, string)`
- **Example**: If Link_1.Phone contains the string "+1 123-456-7890", the following function returns the masked string "+# ###-###-####". MaskDataFormatWithChar("+1 123-456-7890", "#")

### MaskDataFormatWithCharKeepFirst

- **Description**: Mask all alphanumeric input except the first number of characters unmodified from the beginning of the string in the specified format with the specified character, or the '*' character if no character is supplied, while preserving the format.
- **Usage**: `string MaskDataFormatWithCharKeepFirst(string, int32, string)`
- **Example**: If Link_1.Phone contains the string "+1 123-456-7890", the following function returns the masked string "+1 1XX-XXX-XXXX". MaskDataFormatWithCharKeepFirst("+1 123-456-7890", 4, "X")

### MaskDataFormatWithCharKeepLast

- **Description**: Mask all alphanumeric input except the last number of characters unmodified from the end of the string in the specified format with the the specified character, or the '*' character if no character is supplied, while preserving the format.
- **Usage**: `string MaskDataFormatWithCharKeepLast(string, int32, string)`
- **Example**: If Link_1.Phone contains the string "+1 123-456-7890", the following function returns the masked string "+# ###-###-7890". MaskDataFormatWithCharKeepLast("+1 123-456-7890", 4, "#")

### MaskDataKeepFirst

- **Description**: Mask all input except the first number of characters unmodified from the beginning of the string with the optional mask-byte character, or the '*' character if no mask-byte is supplied.
- **Usage**: `string MaskDataKeepFirst(string, int32, uint8)`
- **Example**: If Link_1.Phone contains the string "+1 123-456-7890", the following function returns the masked string "+1 12##########". MaskDataKeepFirst("+1 123-456-7890", 5, 35)

### MaskDataKeepLast

- **Description**: Mask all input except the last number of characters unmodified from the end of the string with the optional mask-byte character, or the '*' character if no mask-byte is supplied.
- **Usage**: `string MaskDataKeepLast(string, int32, uint8)`
- **Example**: If Link_1.Phone contains the string "+1 123-456-7890", the following function returns the masked string "#########6-7890". MaskDataKeepLast("+1 123-456-7890", 6, 35)

### MaskDataWithChar

- **Description**: Mask all input characters with the specified character, or the '*' character if no character is supplied.
- **Usage**: `string MaskDataWithChar(string, string)`
- **Example**: If Link_1.Phone contains the string "+1 123-456-7890", the following function returns the masked string "###############". MaskDataWithChar("+1 123-456-7890", "#")

### MaskDataWithCharKeepFirst

- **Description**: Mask all input except the first number of characters unmodified from the beginning of the string with the specified character, or the '*' character if no character is supplied.
- **Usage**: `string MaskDataWithCharKeepFirst(string, int32, string)`
- **Example**: If Link_1.Phone contains the string "+1 123-456-7890", the following function returns the masked string "+1 12##########". MaskDataWithCharKeepFirst("+1 123-456-7890", 5, "#")

### MaskDataWithCharKeepLast

- **Description**: Mask all input except the last number of characters unmodified from the end of the string with the specified character, or the '*' character if no character is supplied.
- **Usage**: `string MaskDataWithCharKeepLast(string, int32, string)`
- **Example**: If Link_1.Phone contains the string "+1 123-456-7890", the following function returns the masked string "#########6-7890". MaskDataWithCharKeepLast("+1 123-456-7890", 6, "#")
