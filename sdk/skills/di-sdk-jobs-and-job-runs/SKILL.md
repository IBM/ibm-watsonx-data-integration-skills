---
name: di-sdk-jobs-and-job-runs
description: Creating, managing, and monitoring jobs and job runs in IBM watsonx.data integration. Use this skill whenever the user mentions jobs, job runs, executing assets, scheduling workflows, monitoring execution status, checking job logs, viewing job metrics, setting retention policies, managing job parameters, runtime parameters or asks about running, starting, stopping, cancelling, tracking, or troubleshooting data integration workflows. Also trigger when users want to create scheduled tasks, monitor pipeline execution, view execution history, configure job schedules, set up notifications, or work with job state management.
---

# Jobs and Job Runs

## Overview

A **job** is an executable unit of work defined for a specific asset. A job acts as a reusable template that includes basic configuration and parameters, allowing you to execute the same asset multiple times with different settings.

A **job run** is the actual execution instance of a specific job template, capturing runtime details and allowing parameter overrides without modifying the job template itself.

**Always import required enums:**
```python
from ibm_watsonx_data_integration.cpd_models.job_model import JobRunState
```

---

## Part I: Understanding Jobs

### Core Concepts

- **Job**: Reusable execution template for an asset (created once, run many times)
- **Job Run**: Actual execution instance with runtime state, logs, and metrics
- **Asset**: The underlying resource being executed (typically a Flow object)
- **Runtime Parameters**: Override parameter set values at job or job run level

### Why Use Jobs?

Jobs separate the **what** (the asset definition) from the **how** (execution configuration). This separation enables:

- **Repeatability**: Run the same asset with different parameters (e.g., daily ETL with different dates)
- **Scheduling**: Automate execution on a schedule rather than manual triggering
- **History Tracking**: Maintain execution history across multiple runs with consistent configuration
- **Team Collaboration**: Share execution templates with team members who need the same settings
- **Configuration Management**: Modify execution settings without changing the underlying asset

### Prerequisites

Before working with jobs, ensure you have:
- An authenticated `Platform` instance (see `platform` skill)
- A `Project` object retrieved via `platform.projects.get(...)`
- An asset to create jobs from

**Prerequisites Setup Example:**

```python
import os
from ibm_watsonx_data_integration.common.auth import IAMAuthenticator
from ibm_watsonx_data_integration import Platform

# 1. Authenticated Platform instance
api_key = os.environ.get('WATSONX_API_KEY')
auth = IAMAuthenticator(api_key=api_key)
platform = Platform(auth=auth, base_api_url='https://api.ca-tor.dai.cloud.ibm.com')

# 2. Project object
project = platform.projects.get(project_id='your-project-id')

# 3. Asset to create jobs from
my_flow = project.flows.get(name='My Flow')

# Now ready to create jobs
job = project.create_job(flow=my_flow, name='My Job')
```

---

## Part II: Working with Jobs

### Creating a Job

Jobs are created for a specific asset within a project. The asset reference is required, while configuration is optional.

```python
import os
from ibm_watsonx_data_integration.common.auth import IAMAuthenticator
from ibm_watsonx_data_integration import Platform

# Authenticate
api_key = os.environ.get('WATSONX_API_KEY')
auth = IAMAuthenticator(api_key=api_key)
platform = Platform(auth=auth, base_api_url='https://api.ca-tor.dai.cloud.ibm.com')

# Get project and asset
project = platform.projects.get(project_id='your-project-id')
my_flow = project.flows.get(name='My Flow')

# Basic job creation for an asset
job = project.create_job(
    flow=my_flow,
    name='My Job',
    description='Job description'
)

# Job with runtime parameters (override parameter set values)
job = project.create_job(
    flow=my_flow,
    name='Job with Parameters',
    description='Job with custom parameter values',
    runtime_parameters={
        'myparamset.param1': 'production_db',  # external parameter
        'localparam1': 'custom_value'          # local parameter
    }
)
```

**Parameter Format Rules:**
- **External parameters**: `'parameter_set_name.parameter_name'` (dot notation required)
- **Local parameters**: `'parameter_name'` (no prefix)
- Accepts `dict` or `ParameterSet` object
- Mixing formats will cause errors

**Why Runtime Parameters?** They enable the same job template to work across different environments (dev/staging/prod) or with different input data without creating multiple job definitions.

### Retrieving Jobs

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `project.jobs.get_all()` | None | `List[Job]` | Get all jobs in the project |
| `project.jobs.get(name='...')` | `name: str` | `Job` | Get first job matching the name |
| `project.jobs.get_all(name='...')` | `name: str` | `List[Job]` | Get all jobs matching the name |

```python
import os
from ibm_watsonx_data_integration.common.auth import IAMAuthenticator
from ibm_watsonx_data_integration import Platform

# Authenticate and get project
api_key = os.environ.get('WATSONX_API_KEY')
auth = IAMAuthenticator(api_key=api_key)
platform = Platform(auth=auth, base_api_url='https://api.ca-tor.dai.cloud.ibm.com')
project = platform.projects.get(project_id='your-project-id')

# Get all jobs in project
all_jobs = project.jobs.get_all()

# Get specific job by name (returns first match)
job = project.jobs.get(name='My Job')

# Get all jobs matching criteria (returns list)
matching_jobs = project.jobs.get_all(name='My Job')
```

### Updating Job Attributes

Metadata includes the job's identity and description. These can be modified at any time:

```python
# Modify job properties
job.name = 'New Job Name'
job.description = 'Updated description'

# Persist changes
project.update_job(job)  # Returns <Response [200]>

# View job configuration
job.print_json()  # Shows metadata, configuration, etc.
```

### Job-Type Specific Configuration

Jobs behave differently based on their type. For detailed configuration:

- **Batch jobs**: See [`resources/batch_jobs.md`](resources/batch_jobs.md) for runtime settings, environments, schedules, and metrics
- **Streaming jobs**: See [`resources/streaming_jobs.md`](resources/streaming_jobs.md) for offset management and limitations

**Quick comparison:**

| Feature | Batch Jobs | Streaming Jobs |
|---------|-----------|----------------|
| Runtime configuration | ✅ Full support | ❌ Limited/none |
| Offset management | ❌ Not supported | ✅ Supported |
| Detailed metrics | ✅ Available | ❌ Limited |
| Scheduling | ✅ Supported | ⚠️ Typically continuous |

---

## Part III: Executing and Monitoring

### Starting a Job Run

A job serves as a reusable template. To execute the underlying asset (typically a Flow), you must start a job run from an existing Job object. First retrieve or create a job, then call the start() method:

```python
# Basic job run
job_run = job.start(
    name='Test Job Run',
    description='Run description'
)

# Job run with runtime parameter overrides
job_run = job.start(
    name='Custom Run',
    description='Run with overridden parameters',
    runtime_parameters={
        'myparamset.param1': 'override_value',
        'localparam1': 'another_override'
    }
)
```

**Default Values:** If the `name` or `description` parameters are not provided to the job.start() method, the defaults are `name='job run'`, `description=''`.

**Parameter Override Hierarchy:**
Parameters can be overridden at three levels (later overrides take precedence):
1. Asset parameter sets (default values)
2. Job creation (`create_job(runtime_parameters=...)`)
3. Job run start (`job.start(runtime_parameters=...)`)

### Retrieving Job Runs

```python
from ibm_watsonx_data_integration.cpd_models.job_model import JobRunState

# Get all job runs for a job
job_runs = job.job_runs.get_all()

# Filter by state (use JobRunState enum)
running_runs = job.job_runs.get_all(states=[JobRunState.Running])

# Filter by multiple states
active_runs = job.job_runs.get_all(states=[JobRunState.Running, JobRunState.Queued])
```

**Available JobRunState Values:**
- `JobRunState.Queued` - Waiting to start
- `JobRunState.Starting` - Initialization phase
- `JobRunState.Running` - Currently executing
- `JobRunState.Paused` - Temporarily paused
- `JobRunState.Resuming` - Resuming from pause
- `JobRunState.Canceling` - Cancellation in progress
- `JobRunState.Canceled` - Successfully cancelled
- `JobRunState.Failed` - Execution failed
- `JobRunState.Completed` - Successfully completed
- `JobRunState.CompletedWithErrors` - Completed but with errors
- `JobRunState.CompletedWithWarnings` - Completed but with warnings

### Monitoring Job Run State

Job run state is **not** automatically updated. You must explicitly refresh it:

```python
import time
from ibm_watsonx_data_integration.cpd_models.job_model import JobRunState

# Refresh job run status
job_run.refresh_status()  # Returns <Response [200]>

# Check current state (returns JobRunState enum)
print(job_run.state)  # JobRunState.Running

# Job run state lifecycle:
# Queued → Starting → Running → Completed (success path)
#                             → Failed (error path)
#                             → Canceling → Canceled (user intervention)

# Monitor until completion using enum comparison
terminal_states = {
    JobRunState.Completed,
    JobRunState.CompletedWithErrors,
    JobRunState.CompletedWithWarnings,
    JobRunState.Failed,
    JobRunState.Canceled
}

while True:
    job_run.refresh_status()
    if job_run.state in terminal_states:
        break
    time.sleep(5)
```

**Why manual refresh?** Automatic polling would be inefficient. The SDK gives you control over when to check status, allowing you to implement your own polling strategy based on your needs.

### Retrieving Job Run Logs

Runtime logs capture execution details and are essential for troubleshooting:

```python
# Get logs (list of strings)
logs = job_run.logs

for log_line in logs:
    print(log_line)
```

**Note:** Log availability and format may vary by job type. See type-specific resources for details.

### Cancelling a Job Run

```python
# Cancel a running job run
job_run.cancel()  # Returns <Response [204]>

# Always refresh status after cancelling to confirm state change
job_run.refresh_status()
```

---

## Part IV: Cleanup and Management

### Deleting a Job

```python
# Delete job from project
project.delete_job(job)  # Returns <Response [204]>
```

**Warning:** Deleting a job will also delete all associated job runs. This operation cannot be undone.

---

## Complete Workflow Example

```python
import os
import time
from ibm_watsonx_data_integration.common.auth import IAMAuthenticator
from ibm_watsonx_data_integration import Platform
from ibm_watsonx_data_integration.cpd_models.job_model import JobRunState

# 1. Authenticate
api_key = os.environ.get('WATSONX_API_KEY')
auth = IAMAuthenticator(api_key=api_key)
platform = Platform(auth=auth, base_api_url='https://api.ca-tor.dai.cloud.ibm.com')

# 2. Get project and asset
project = platform.projects.get(project_id='your-project-id')
my_flow = project.flows.get(name='Production Flow')

# 3. Create job for the asset
job = project.create_job(
    flow=my_flow,
    name='Production Job',
    runtime_parameters={'myparamset.db': 'prod_db'}
)

# 4. Start job run with overrides
job_run = job.start(
    name='Daily Run',
    runtime_parameters={'myparamset.date': '2026-05-04'}
)

# 5. Monitor execution using enum comparison
terminal_states = {
    JobRunState.Completed,
    JobRunState.CompletedWithErrors,
    JobRunState.CompletedWithWarnings,
    JobRunState.Failed,
    JobRunState.Canceled
}

while True:
    job_run.refresh_status()
    if job_run.state in terminal_states:
        break
    time.sleep(5)

# 6. Check results using enum comparison
if job_run.state in {JobRunState.Completed, JobRunState.CompletedWithWarnings}:
    print("Job completed successfully")
    if job_run.state == JobRunState.CompletedWithWarnings:
        print("Job completed with warnings - check logs")
elif job_run.state == JobRunState.Failed:
    print("Job failed - check logs:")
    for log in job_run.logs:
        print(log)
elif job_run.state == JobRunState.Canceled:
    print("Job was cancelled")
```

---

## Edge Cases and Best Practices

### Parameter Naming Convention
- **External parameters** MUST use format: `'parameter_set_name.parameter_name'`
- **Local parameters** use just: `'parameter_name'`
- Mixing formats will cause errors
- Parameter names are case-sensitive

### Retention Policies
- `retention_days` and `retention_amount` are **mutually exclusive**
- Setting both will cause an error
- Use `None` to disable retention limits
- Retention applies to job runs, not the job itself

### State Management
- `job_run.state` returns a `JobRunState` enum, not a string
- State is not automatically updated - call `refresh_status()` explicitly
- Use enum comparison: `job_run.state == JobRunState.Running`

---

## Common Mistakes to Avoid

1. ❌ Using `update_job()` for runtime settings → Use type-specific configuration methods
2. ❌ Wrong parameter format: `'param1'` for external → Use `'paramset.param1'`
3. ❌ Setting both `retention_days` and `retention_amount` → Choose one or None
4. ❌ Forgetting to call `refresh_status()` → State is not auto-updated
5. ❌ Comparing `job_run.state` to strings → Use `JobRunState` enum (e.g., `JobRunState.Running`)
6. ❌ Not handling None values in metrics → Use `or 0` for safe aggregation
7. ❌ Using `space_id` to filter job runs → Use `project_id` parameter
9. ❌ Passing state as string → Use `states=[JobRunState.Running]` with enum list
10. ❌ Forgetting to import `JobRunState` → Always import required enums

---

## Additional Resources

For job-type specific operations, consult:
- [`resources/batch_jobs.md`](resources/batch_jobs.md) - Batch job runtime settings, environments, schedules, and metrics
- [`resources/streaming_jobs.md`](resources/streaming_jobs.md) - Streaming job offset management and limitations
