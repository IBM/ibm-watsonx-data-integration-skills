---
name: di-sdk-platform
description: Entry point for the IBM watsonx Data Integration SDK — authentication patterns, collection methods, job lifecycle, persisting changes, and error handling. Read before any SDK task, then load the skill that matches your work.
---

# data-intg-mcp Skill: IBM watsonx.data Integration

Read this in full before taking any action on a watsonx.data Integration task. This is the entry point for all data-intg-mcp skills — after reading this, load the skill that matches your task:

- **`project`** — creating, listing, and retrieving projects
- **`streaming-flows`** — building, configuring, and running a streaming flow
- **`batch-flows`** — building, configuring, and running a batch flow

---

## Mandatory startup sequence

Before doing anything else, call these two tools in order:

1. `best_practices` — loads the full SDK mental model and pattern guide
2. `list_docs` — shows all available documentation URIs; read relevant ones with `read_doc` before writing any code

**Do not skip this.** Reading docs before generating code prevents the most common failures.

---

## Correct collection methods

The SDK uses collection objects — **never guess method names, use exactly these**:

```python
# Projects
platform.projects.get_all()                        # list all projects
platform.projects.get(name='My Project')           # get one by name
platform.projects.get(project_id='abc-123')        # get one by ID — use project_id=, NOT id=

# Flows
project.flows.get_all()                            # all flows (streaming + batch)
project.flows.get_all(flow_type='streaming')       # only streaming flows
project.flows.get_all(flow_type='batch')           # only batch flows
project.flows.get(name='My Flow')                  # get by name (streaming OK)
project.flows.get(flow_id='abc-123')               # get by ID (REQUIRED for batch — see below)

# Jobs
project.jobs.get_all()
project.jobs.get(name='My Job')

# Engines
project.engines.get_all()                          # returns list of Engine objects
project.engines.get(engine_id='abc-123')            # get single engine by ID

# Environments
project.environments.get_all()
project.environments.get(environment_id='abc-123')
```

> ❌ `.list()` does not exist on any collection — always use `.get_all()`

---

## Authentication patterns

**IMPORTANT: Always detect the authentication type based on available environment variables.**

The SDK supports both SaaS and On-Premises deployments. Use this pattern to automatically detect and use the correct authenticator:

```python
import os
from ibm_watsonx_data_integration.common.auth import (
    IAMAuthenticator,
    ICP4DAuthenticator,
    ZenApiKeyAuthenticator,
)
from ibm_watsonx_data_integration.platform import Platform

# Detect authentication type based on available credentials
api_key = os.getenv('WATSONX_API_KEY')
cp4d_username = os.getenv('CP4D_USERNAME')
cp4d_password = os.getenv('CP4D_PASSWORD')
zen_api_key = os.getenv('ZEN_API_KEY')
cp4d_url = os.getenv('CP4D_URL', 'https://your-cp4d-cluster.com')
disable_ssl = os.getenv('CP4D_DISABLE_SSL_VERIFICATION', 'false').lower() in ('true', '1', 'yes')

if api_key:
    # SaaS authentication
    auth = IAMAuthenticator(api_key=api_key)
    base_api_url = 'https://api.ca-tor.dai.cloud.ibm.com'
    base_url = 'https://cloud.ibm.com'
elif cp4d_username and cp4d_password:
    # On-Premises with password
    auth = ICP4DAuthenticator(
        username=cp4d_username,
        password=cp4d_password,
        url=cp4d_url,
        disable_ssl_verification=disable_ssl
    )
    base_api_url = cp4d_url
    base_url = cp4d_url
elif cp4d_username and zen_api_key:
    # On-Premises with Zen API key
    auth = ZenApiKeyAuthenticator(
        username=cp4d_username,
        zen_api_key=zen_api_key,
        disable_ssl_verification=disable_ssl
    )
    base_api_url = cp4d_url
    base_url = cp4d_url
else:
    raise RuntimeError(
        "No valid authentication credentials found. Please set one of:\n"
        "  - WATSONX_API_KEY (for SaaS)\n"
        "  - CP4D_USERNAME + CP4D_PASSWORD (for On-Premises)\n"
        "  - CP4D_USERNAME + ZEN_API_KEY (for On-Premises)"
    )

platform = Platform(auth=auth, base_api_url=base_api_url, base_url=base_url)
```

### Individual Authentication Examples

**SaaS (IAMAuthenticator):**
```python
from ibm_watsonx_data_integration.common.auth import IAMAuthenticator
auth = IAMAuthenticator(api_key=os.getenv('WATSONX_API_KEY'))
platform = Platform(auth=auth, base_api_url='https://api.ca-tor.dai.cloud.ibm.com')
```

**On-Premises (ICP4DAuthenticator with password):**
```python
from ibm_watsonx_data_integration.common.auth import ICP4DAuthenticator
cp4d_url = os.getenv('CP4D_URL', 'https://your-cp4d-cluster.com')
disable_ssl = os.getenv('CP4D_DISABLE_SSL_VERIFICATION', 'false').lower() in ('true', '1', 'yes')
auth = ICP4DAuthenticator(
    username=os.getenv('CP4D_USERNAME'),
    password=os.getenv('CP4D_PASSWORD'),
    url=cp4d_url,
    disable_ssl_verification=disable_ssl
)
platform = Platform(auth=auth, base_api_url=cp4d_url, base_url=cp4d_url)
```

**On-Premises (ZenApiKeyAuthenticator with API key):**
```python
from ibm_watsonx_data_integration.common.auth import ZenApiKeyAuthenticator
cp4d_url = os.getenv('CP4D_URL', 'https://your-cp4d-cluster.com')
disable_ssl = os.getenv('CP4D_DISABLE_SSL_VERIFICATION', 'false').lower() in ('true', '1', 'yes')
auth = ZenApiKeyAuthenticator(
    username=os.getenv('CP4D_USERNAME'),
    zen_api_key=os.getenv('ZEN_API_KEY'),
    disable_ssl_verification=disable_ssl
)
platform = Platform(auth=auth, base_api_url=cp4d_url, base_url=cp4d_url)
```

**Environment Variables:**
- `CP4D_DISABLE_SSL_VERIFICATION`: Set to `"true"`, `"1"`, or `"yes"` to disable SSL verification (for self-signed certificates in dev/test only)

---

## Job lifecycle

```python
# Create and run
job = project.create_job(name='My Job', flow=flow)
job_run = job.start(name='Run 1')

# Monitor
job_run.refresh_status()
print(job_run.state)

# Logs
for line in job_run.logs:
    print(line)

# Cancel
job_run.cancel()

# Reset offset (streaming only)
job.reset_offset()
```

---

## Persisting changes: the golden rule

Call `project.update_flow(flow)` after **every** change before moving on. Changes are in-memory only until you call update.

```python
stage = flow.add_stage('Field Remover')         # in-memory
stage.configuration['action'] = 'REMOVE'        # in-memory
project.update_flow(flow)                        # ✅ now persisted — do this after EACH change
```

---

## Error handling / flow error stage

```python
# Set error stage
write_to_file = flow.set_error_stage('Write to File')
write_to_file.configuration['directory'] = '/tmp/errors'

# Set error record policy
flow.configuration['error_record_policy'] = 'STAGE_RECORD'  # or 'ORIGINAL_RECORD'

# View current error stage
print(flow.error_stage)
```

---

## Private attributes

The `execute_script` sandbox **blocks all `_` prefixed access**. Do not attempt to use private attributes in scripts. The only way to discover streaming stages is via the MCP tools (`list_available_streaming_stages`, `list_all_available_stage_configurations_streaming`).
