# Batch Job Specifics

This resource covers batch-specific job operations and configurations.

## Batch Job Runtime Settings

Batch jobs have additional runtime settings that **cannot** be modified via `update_job()`. Use `job.edit_configuration()` instead.

### Why the Separation?

Batch jobs distinguish between what the job *is* (metadata) and how it *runs* (runtime settings). This allows you to modify execution behavior (environment, retention, schedules) without changing the job's definition, maintaining a clean separation of concerns.

### Configuration Example

```python
import os
import datetime
from ibm_watsonx_data_integration.common.auth import IAMAuthenticator
from ibm_watsonx_data_integration import Platform
from ibm_watsonx_data_integration.cpd_models.job_model import Schedule

# Authenticate
api_key = os.environ.get('WATSONX_API_KEY')
auth = IAMAuthenticator(api_key=api_key)
platform = Platform(auth=auth, base_api_url='https://api.ca-tor.dai.cloud.ibm.com')  # pragma: allowlist secret

# Get project
project = platform.projects.get(project_id='your-project-id')

# Get batch job (assumes job already created)
batch_job = project.jobs.get(name='My Batch Job')

# Get available batch environments (returns internal names)
project.list_batch_environments()
# ['default_datastage_px', 'default_datastage_px_large', 'default_datastage_px_medium']

# Convert display name to internal name
env_name = project.get_batch_environment('Default DataStage PX S')
# Returns: 'default_datastage_px'

# Configure batch job runtime settings
schedule = Schedule(
    start_date=datetime.datetime(2030, 12, 11, 22, 17),
    repeat_mode='daily',
    repeat_value=datetime.time(23, 17)
)

batch_job.edit_configuration(
    environment='default_datastage_px',
    warn_limit=100,                    # int > 0 or None for no limit
    retention_days=30,                 # int > 0 or None (cannot set with retention_amount)
    retention_amount=None,             # int > 0 or None (cannot set with retention_days)
    parameter_value_sets=[
        ('myparamset', 'value_set_1'),
        ('paramset2', 'valset_2')
    ],
    job_parameters=[
        ('myparamset.param1', 'myvalue'),
        ('localparam1', 'myvalue2')
    ],
    schedule=schedule,                 # Schedule object or None
    notify_success=True,
    notify_warning=False,
    notify_failure=True
)
```

### Batch-Only Settings

- **`environment`**: Internal name of batch environment (use `list_batch_environments()` to discover)
- **`warn_limit`**: Number of warnings before stopping stages (int > 0 or None)
- **`retention_days`** / **`retention_amount`**: Mutually exclusive - choose one or None
- **`parameter_value_sets`**: List of tuples `(param_set_name, value_set_name)`
- **`job_parameters`**: List of tuples `(param_name, value)` with format `'paramset.param'` for external
- **`schedule`**: Schedule object or None for manual execution
- **`notify_*`**: Boolean notification flags for different outcomes

### Environment Names

- **Always use internal names** in `edit_configuration(environment=...)`
- Use `project.list_batch_environments()` to get internal names
- Use `project.get_batch_environment('Display Name')` to convert display name to internal name
- Display names are user-friendly but not accepted by the API

## Batch Job Run Metrics

Batch jobs provide detailed performance metrics for analyzing execution:

```python
import os
from ibm_watsonx_data_integration.common.auth import IAMAuthenticator
from ibm_watsonx_data_integration import Platform

# Authenticate and get project
api_key = os.environ.get('WATSONX_API_KEY')
auth = IAMAuthenticator(api_key=api_key)
platform = Platform(auth=auth, base_api_url='https://api.ca-tor.dai.cloud.ibm.com')  # pragma: allowlist secret
project = platform.projects.get(project_id='your-project-id')

# Get job and start run
batch_job = project.jobs.get(name='My Batch Job')
job_run = batch_job.start(name='Metrics Test Run')

# Wait for completion (simplified - see main SKILL.md for full monitoring)
job_run.refresh_status()

# Get metrics (BatchJobRunMetrics object)
metrics = job_run.metrics

# Refresh metrics to get latest data
job_run.refresh_metrics()  # Returns <Response [200]>

# Link metrics (data flow between stages)
for link in metrics.link_metrics:
    print(f"{link.source} -> {link.dest}: {link.rows_read} rows")
    print(f"  State: {link.state}, Link: {link.link_name}")

# Stage metrics (performance per stage)
for stage in metrics.stage_metrics:
    print(f"{stage.stage_name} ({stage.stage_type})")
    print(f"  Rows: {stage.rows_read} read, {stage.rows_written} written")
    print(f"  Partitions: {stage.num_partitions}")
    print(f"  CPU: {stage.stage_seconds_cpu}s")
    print(f"  Memory: {stage.total_memory}")

# Filter metrics using get() and get_all()
link = metrics.link_metrics.get(source='Row_Generator')
stage = metrics.stage_metrics.get(stage_type='PxRowGenerator')
finished = metrics.stage_metrics.get_all(state='finished')
```

### Metrics Structure

- **Link Metrics**: `start_time`, `stop_time`, `rows_read`, `rows_written`, `source`, `dest`, `link_name`, `state`
- **Stage Metrics**: `stage_name`, `stage_type`, `rows_read`, `rows_written`, `num_partitions`, `partition_row_counts`, `stage_seconds_cpu`, `total_memory`, `start_time`, `stop_time`, `state`

### When to Use Metrics

After job completion for performance analysis, capacity planning, or identifying bottlenecks. Metrics may be incomplete during execution.

## Batch Job Logs

Runtime logs are fully available for IBM watsonx.data integration batch job runs. Access logs through the job_run.logs property after starting a batch job run:

```python
import os
from ibm_watsonx_data_integration.common.auth import IAMAuthenticator
from ibm_watsonx_data_integration import Platform

# Authenticate and get project
api_key = os.environ.get('WATSONX_API_KEY')
auth = IAMAuthenticator(api_key=api_key)
platform = Platform(auth=auth, base_api_url='https://api.ca-tor.dai.cloud.ibm.com')  # pragma: allowlist secret
project = platform.projects.get(project_id='your-project-id')

# Get batch job and start run
batch_job = project.jobs.get(name='My Batch Job')
job_run = batch_job.start(name='Log Test Run')

# Get logs (list of strings)
logs = job_run.logs

for log_line in logs:
    print(log_line)

# Example output:
# '##I IIS-DSEE-TOSH-00397 2025-05-27 14:27:27(000) Starting job...'
# '##I IIS-DSEE-TOSH-00408 2025-05-27 14:27:27(000) Job Parameters:'
