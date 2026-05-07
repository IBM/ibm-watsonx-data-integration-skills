# DataStage Sequential File Stage

## Purpose
Process data from flat files as a source or target for file-based data import or export.

## When to Use
- File-based data import or export
- Processing CSV, delimited, fixed-width, parquet, or binary files

## When NOT to Use
- For inter-job communication within DataStage (use Data Set Stage)
- For large-scale parallel processing (use File Set Stage)

## Requirements
- **Link Cardinality**: Optionally 1 primary input, optionally 1 primary output, optionally 1 reject output

## Best Practices
- Parameterize the file path and file name
- Use Data Set Stage when data will be ingested by another DataStage flow

## Property Configuration

### Supported Formats
- CSV, delimited, fixed-width, parquet, binary

### Supported File Systems
- Posix, IBM Cloud Object Storage, HDFS, S3, GCS, Azure Blob Storage

### Characteristics
- Runs in sequential mode by default
- Collect to single partition (default) when exporting data
- Can read single or multiple files in parallel
- Supports reading and writing file patterns
