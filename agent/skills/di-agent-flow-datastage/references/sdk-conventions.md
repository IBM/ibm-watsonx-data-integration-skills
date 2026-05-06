# SDK conventions

DataStage batch SDK reference — method signatures, call patterns, conventions. Auth and project context are handled by the platform MCP tool; the patterns below apply to flow code you write and submit.

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
- The **connection** IS a project asset of type `connection`. Use `list_project_assets(types=["connection"])` to look up a connection ID — never to find individual tables inside it.

Asset types: `data_asset`, `connection`, `flow`, `job`. `asset_ids` is always a list, even for one asset.

---

## Flow creation (batch)

```python
flow = project.create_flow(name='My Flow', environment=None, flow_type='batch')
project.update_flow(flow)   # persist every change
```

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

`connect_output_to` returns a link object you can name and attach schemas to (see [Link schemas](#link-schemas)).

---

## Validation

```python
flow.compile()
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
- **No BOOLEAN column type.** Use `BIT` with 0/1.
- **Never guess enum values.** Inspect `accepted_values` and use one exactly.
- **`project.validate_flow(flow)` does not exist** — use `flow.compile()` for batch.
