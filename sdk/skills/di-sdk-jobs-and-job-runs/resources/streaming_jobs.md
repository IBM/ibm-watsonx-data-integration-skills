# Streaming Job Specifics

This resource covers streaming-specific job operations and configurations.

## Streaming Job Characteristics

Streaming jobs are designed for continuous data processing and have fundamentally different execution patterns compared to batch jobs:

- **Continuous execution**: Streaming jobs run indefinitely, processing data as it arrives. They do not have a natural completion state and typically end only when explicitly cancelled by the user.
- **No pause/resume**: Streaming jobs cannot be paused. Once started, they run continuously until cancelled.
- **Terminal state**: The most common terminal state for streaming jobs is `Canceled` rather than `Completed`, as they are designed to run until manually stopped.
- **Limited `edit_configuration()` support**: Most runtime settings are not available for streaming jobs.
- **Offset tracking**: Streaming jobs track offsets to remember the last processed data position, enabling recovery and reprocessing from specific points.
- **Limited metrics**: Detailed performance metrics are not available like in batch jobs.
- **Log availability**: May vary compared to batch jobs.

## Resetting Job Offset

**⚠️ This method only works for streaming jobs, NOT batch jobs.**

Streaming jobs track offsets to remember the last processed data position. Resetting allows reprocessing:

```python
import os
from ibm_watsonx_data_integration.common.auth import IAMAuthenticator
from ibm_watsonx_data_integration import Platform

# Authenticate and get project
api_key = os.environ.get('WATSONX_API_KEY')
auth = IAMAuthenticator(api_key=api_key)
platform = Platform(auth=auth, base_api_url='https://api.ca-tor.dai.cloud.ibm.com')  # pragma: allowlist secret
project = platform.projects.get(project_id='your-project-id')

# Get streaming job
streaming_job = project.jobs.get(name='My Streaming Job')

# Reset offset for streaming job
streaming_job.reset_offset()  # Returns <Response [200]>
```

### Use Cases

- Reprocess data from the beginning after fixing a bug
- Recover from processing errors that corrupted state
- Reset after job completion or cancellation to start fresh

### Why Offsets Matter

Offsets enable streaming jobs to maintain state across runs. When a streaming job processes data from a database source, it tracks which records have been processed. For example, when new records are appended to a table, the streaming flow processes them incrementally. Resetting the offset allows you to reprocess all records from the beginning, which is useful for:

1. **Bug fixes**: After fixing a processing bug, reprocess all data with the corrected logic
2. **State corruption**: If the job's internal state becomes corrupted, reset and rebuild from scratch
3. **Testing**: Replay the same data stream for testing or validation purposes
4. **Full reprocessing**: When you need to reprocess the entire dataset after schema or logic changes

## Streaming Job Logs

Streaming job logs may have different availability or format compared to batch jobs. To access logs, first start a streaming job run, then retrieve the logs from the job_run object:

```python
import os
from ibm_watsonx_data_integration.common.auth import IAMAuthenticator
from ibm_watsonx_data_integration import Platform

# Authenticate and get project
api_key = os.environ.get('WATSONX_API_KEY')
auth = IAMAuthenticator(api_key=api_key)
platform = Platform(auth=auth, base_api_url='https://api.ca-tor.dai.cloud.ibm.com')  # pragma: allowlist secret
project = platform.projects.get(project_id='your-project-id')

# Get streaming job and start run
streaming_job = project.jobs.get(name='My Streaming Job')
job_run = streaming_job.start(name='Log Test Run')

# Get logs (list of strings)
logs = job_run.logs

for log_line in logs:
    print(log_line)
```

**Note**: Log availability and format may vary for streaming jobs. Check the actual log output to understand the structure.

## Streaming Job Configuration Limitations

Unlike batch jobs, streaming jobs have limited support for runtime configuration:

- No `edit_configuration()` support for most settings
- No detailed metrics like batch jobs
- No environment selection
- No retention policies
- No scheduling (streaming jobs typically run continuously)

Focus on:
- Creating the job with correct initial parameters
- Starting and monitoring job runs
- Managing offsets for reprocessing
- Cancelling runs when needed
