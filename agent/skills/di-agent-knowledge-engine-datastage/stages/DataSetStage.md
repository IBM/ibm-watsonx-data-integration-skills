# DataStage Data Set Stage

## Purpose
Read and write DataStage native binary format files for efficient inter-job communication and checkpoint/restart capabilities.

## When to Use
- Inter-job communication within DataStage
- Checkpoint/restart scenarios

## When NOT to Use
- For data shared with other applications (use Sequential File Stage or Database Tables)
- When human-readable format is required

## Requirements
- **Link Cardinality**: Optionally 1 primary input, optionally 1 primary output

## Best Practices
- Use for intermediate storage between jobs unless data needs to be shared with other applications
- Parameterize the Data Set path and file name

## Performance
- Fastest option for inter-job data transfer within DataStage
- Maintains complete schema metadata and partitioning information
- No data conversion overhead

## Property Configuration

### file

- This setting is required and provides a path where the dataset header file is written

```python
dataset_valid_ssn.configuration.file = "/example/path/valid.ds"
```

### update_policy

- This setting should be set to overwrite by default unless other values discard_records, append, discard_schema, or create is required

```python
from ibm_watsonx_data_integration.services.datastage.models.enums import DATASET

dataset_valid_ssn.configuration.update_policy = DATASET.UpdatePolicy.overwrite
```
