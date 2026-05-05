# SDK conventions

Self-contained SDK reference — method signatures, call patterns, conventions. Use alongside `get_datastage_sdk_spec` when available, but this file is sufficient on its own.

---

## Authentication

```python
# SaaS
from ibm_watsonx_data_integration.common.auth import IAMAuthenticator
from ibm_watsonx_data_integration.platform import Platform

auth = IAMAuthenticator(api_key=os.getenv('WATSONX_API_KEY', 'YourAPIKey'))
platform = Platform(auth=auth, base_api_url='https://api.ca-tor.dai.cloud.ibm.com')

# On-prem
from ibm_watsonx_data_integration.common.auth import ZenApiKeyAuthenticator
auth = ZenApiKeyAuthenticator(username='user', zen_api_key=os.getenv('ZEN_API_KEY'))
```

---

## Script boilerplate

Standard entry for direct-SDK scripts:

```python
from ibm_watsonx_data_integration.common.auth import IAMAuthenticator
from ibm_watsonx_data_integration.platform import Platform
import os

auth = IAMAuthenticator(
    api_key=os.environ.get('WATSONX_API_KEY', 'YourAPIKey'),
    base_auth_url=os.environ.get('WATSONX_AUTH_URL', 'https://cloud.ibm.com'),
)
platform = Platform(
    auth=auth,
    base_api_url=os.environ.get('WATSONX_API_URL', 'https://api.dataplatform.cloud.ibm.com'),
)

project = platform.projects.get(project_id=os.environ.get('WATSONX_PROJECT_ID'))
# OR: project = platform.projects.get(name=os.environ.get('WATSONX_PROJECT_NAME'))

flow = project.create_flow(name="MyFlow", environment=None, flow_type="batch")
# ... build flow ...
project.update_flow(flow)
```

---

## Asset discovery

Discover project assets via MCP tools:

- `get_projects()` — list projects
- `list_project_assets(project_id=..., query=..., types=[...])` — search by type/keyword
- `inspect_project_asset(asset_ids=[...], ...)` — schema + metadata

**Skip discovery when the user already named the info.** If they said "use connection X, table Y", use it directly — don't search for it.

### `data_asset` vs connector tables

`list_project_assets(types=["data_asset"])` returns **0** for database tables — they are not project assets.

- **`data_asset`** = files/datasets stored in the watsonx project (uploaded CSVs, Parquet, etc.)
- **Database tables** (Db2, BigQuery, Snowflake, Oracle, etc.) are referenced by path on the stage, not discovered. Example: Db2 `/SALES/ORDERS` → set `schema_name="/SALES"` + `table_name="ORDERS"` on the stage.
- The **connection** (credentials pointing at the database) IS a project asset of type `connection`. Use `list_project_assets(types=["connection"])` to look up a connection ID — never to find individual tables inside it.

Asset types: `data_asset`, `connection`, `flow`, `job`. `asset_ids` is always a list, even for one asset.

---

## Collection methods

Every collection exposes the same shape. `.list()` does NOT exist — always `.get_all()`.

```python
# Projects
platform.projects.get_all()                        # list all projects
platform.projects.get(name='My Project')           # by name
platform.projects.get(project_id='abc-123')        # by ID — parameter is project_id=, NOT id=

# Flows (batch + streaming)
project.flows.get_all()                            # all flows
project.flows.get_all(flow_type='streaming')       # filter streaming
project.flows.get_all(flow_type='batch')           # filter batch
project.flows.get(name='My Flow')                  # OK for streaming
project.flows.get(flow_id='abc-123')               # REQUIRED for batch — name returns incomplete data

# Jobs
project.jobs.get_all()
project.jobs.get(name='My Job')

# Engines (streaming)
project.engines.get_all()                          # list of Engine objects
project.get_engine(engine_id='abc-123')            # single engine by ID

# Environments (streaming)
project.environments.get_all()
project.environments.get(environment_id='abc-123')

# Connections (for connection-backed stages)
project.connections.get(name='my-connection')
```

---

## Flow creation and persistence

```python
# Batch
flow = project.create_flow(name='My Flow', environment=None, flow_type='batch')

# Streaming (with environment)
env = project.environments.get_all()[0]
flow = project.create_flow(name='My Flow', environment=env)   # flow_type defaults to 'streaming'

# Streaming (engineless)
flow = project.create_flow(name='My Flow', environment=None)

# Persist every change
project.update_flow(flow)
```

**Golden rule:** changes are in-memory until `project.update_flow(flow)`. Call it after every change.

---

## Adding and configuring stages

```python
stage = flow.add_stage(type='Row Generator', label='my_row_gen')
# type = stage type string (e.g., "Row Generator", "Transformer")
# label = UI display name

# Inspect before setting — configuration object varies per stage
print(stage.configuration)

# Both access styles work
stage.configuration['key_capture_mode'] = 'RECORD_HEADER'
stage.configuration.key_capture_mode = 'RECORD_HEADER'
```

When `accepted_values` on a field is non-empty, use one of those values exactly. Never invent or guess enum values.

---

## Connecting stages

```python
# Basic
origin.connect_output_to(destination)
destination.connect_input_to(origin)                 # equivalent

# Chaining (returns the destination stage)
origin.connect_output_to(processor).connect_output_to(destination)

# Fan-out (one stage to many)
origin.connect_output_to(proc1, proc2, proc3)

# Event output (e.g., to a Pipeline Finisher)
origin.connect_event_to(pipeline_finisher)
```

`connect_output_to` returns a link object you can name and attach schemas to (see [Link schemas](#link-schemas)). Streaming-only Stream Selector pattern: [streaming-streamsets.md](streaming-streamsets.md).

---

## Validation

```python
# Batch
flow.compile()

# Streaming
result = flow.validate()             # NOT project.validate_flow(flow) — that doesn't exist
for issue in result.issues:
    print(issue.instance_name, issue.human_readable_message)
```

Always `project.update_flow(flow)` before validating.

---

## Job lifecycle

```python
job = project.create_job(name='My Job', flow=flow)
job_run = job.start(name='Run 1')

job_run.refresh_status()
print(job_run.state)

for line in job_run.logs:
    print(line)

job_run.cancel()

# Streaming-only
job.reset_offset()

# Batch job runtime config
job.edit_configuration(
    environment='default_datastage_px',
    retention_amount=100,
    warn_limit=50,
)
```

---

## Link schemas

Every link needs a schema or the flow won't compile.

```python
link = origin.connect_output_to(dest)
link.name = "Link_1"
schema = link.create_schema()
schema.add_field("VARCHAR", "my_col", length=100)
schema.add_field("DECIMAL", "my_num", length=10, precision=2)
schema.add_field("INTEGER", "my_int", source="OtherLink.other_int")      # propagate
schema.add_field("DECIMAL", "derived", length=10, precision=2,
                 derivation="Link_1.my_num * 2")                         # computed
```

---

## Column types

```
BIGINT, BINARY, BIT, CHAR, DATE, DECIMAL, DOUBLE, FLOAT, INTEGER,
LONGNVARCHAR, LONGVARBINARY, LONGVARCHAR, NCHAR, NUMERIC, NVARCHAR,
REAL, SMALLINT, TIME, TIMESTAMP, TINYINT, UNKNOWN, VARBINARY, VARCHAR
```

**No BOOLEAN.** Use `BIT` with value 0 or 1.

---

## Execmode and common stage properties

Stage execmode requires the stage-specific enum class:

```python
from ibm_watsonx_data_integration.services.datastage import PEEK, ROW_GENERATOR

row_gen.configuration.execmode = ROW_GENERATOR.Execmode.par   # parallel
peek.configuration.execmode = PEEK.Execmode.seq               # sequential
peek.configuration.dataset = PEEK.Dataset.false
```

Other common stage properties: `auto_column_propagation`, `combinability`.

---

## Error stage

```python
write_to_file = flow.set_error_stage('Write to File')
write_to_file.configuration['directory'] = '/tmp/errors'
flow.configuration['error_record_policy'] = 'STAGE_RECORD'   # or 'ORIGINAL_RECORD'

print(flow.error_stage)
```

Write to File error stage properties: `directory`, `max_file_size_in_mb`, `file_wait_time_in_secs`, `files_prefix`.

---

## Connection binding

For connection-backed stages (database connectors, cloud storage, etc.):

```python
conn = project.connections.get(name='my-db-connection')
stage = flow.add_stage(type='IBM Db2', label='db2_source')
stage.use_connection(conn)
stage.configuration.schema_name = 'MYSCHEMA'
stage.configuration.table_name = 'MYTABLE'
```

---

## Foot-guns

- **`.list()` does not exist** on any collection — always `.get_all()`.
- **Parameter is `project_id=`, not `id=`** — `platform.projects.get(project_id='abc-123')`.
- **Fetch batch flows by `flow_id`, not by name** — name returns incomplete stage data.
- **Private attrs (`_x`) are blocked in `execute_script`** sandbox. Use MCP tools for streaming stage discovery — not private SDK attributes.
- **No BOOLEAN column type.** Use `BIT` with 0/1.
- **Never guess enum values.** Inspect `accepted_values` and use one exactly.
- **`project.validate_flow(flow)` does not exist** — use `flow.validate()`.
- **`project.update_flow(flow)` after every change.** In-memory until persisted.

---

## Source tree (for grepping enums / models)

```
ibm_watsonx_data_integration/services/datastage/models/stage_models       # stage models
ibm_watsonx_data_integration/services/datastage/models/enums              # accepted values
ibm_watsonx_data_integration/services/datastage/models/stage_type_str.py  # type= strings
ibm_watsonx_data_integration/services/datastage/models/schema/schema.py   # column types
```

`label` = UI display name. `type` = stage type string. Example: `flow.add_stage(type="Row Generator", label="myrowgenerator")`.
