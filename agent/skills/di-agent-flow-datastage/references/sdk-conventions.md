# SDK conventions

DataStage batch SDK reference — method signatures, call patterns, conventions. Auth and project context are handled by the platform MCP tool; the patterns below apply to flow code you write and submit.

---

## CRITICAL REQUIREMENT — Read stage-specific files first

Before writing ANY code that includes a stage, you MUST read its corresponding stage skill file.

Stage skill files are located at: `subprojects/app/python/src/de_agent/de_agent/skills/di-agent-knowledge-engine-datastage/stages/<UserFriendlyStageName>Stage.md`. For example, if the flow contains a change apply stage, you must read `subprojects/app/python/src/de_agent/de_agent/skills/di-agent-knowledge-engine-datastage/stages/ChangeApplyStage.md`

Do not write any code without first reading the corresponding stage skill files. The link cardinality rules in those files must be followed.

---

## Asset discovery

Discover project assets via MCP tools:

- `get_projects()` — list projects
- `list_data_assets(project_id=...)` — list data assets (uploaded CSVs, Parquet, etc.)
- `list_connections(project_id=...)` — list connections
- `list_datastage_flows(project_id=...)` — list DataStage flows
- `list_streamsets_flows(project_id=...)` — list StreamSets flows
- `inspect_project_asset(asset_ids=[...], ...)` — schema + metadata

**Skip discovery when the user already named the info.** If they said "use connection X, table Y", use it directly — don't search for it.

### `data_asset` vs connector tables

`list_data_assets(project_id=...)` returns **0** for database tables — they are not data assets.

- **`data_asset`** = files/datasets stored in the watsonx project (uploaded CSVs, Parquet, etc.)
- **Database tables** (Db2, BigQuery, Snowflake, Oracle, etc.) are referenced by path on the stage, not discovered. Example: Db2 `/SALES/ORDERS` → set `schema_name="/SALES"` + `table_name="ORDERS"` on the stage.
- The **connection** IS a project asset. Use `list_connections(project_id=...)` to look up a connection ID — never to find individual tables inside it.

Asset types: `data_asset`, `connection`, `datastage_flow`, `streamsets_flow`, `job`. `asset_ids` is always a list, even for one asset.

---

## Flow creation

```python
flow = project.create_flow(name='My Flow', environment=None, flow_type='batch')
project.update_flow(flow)   # persist every change
```

You must include these exact named parameters. `environment` must be `None` and `flow_type` must be `batch`.

---

## Adding and configuring stages

```python
stage = flow.add_stage(type='Row Generator', label='my_row_gen')
# type = exact stage type string, label = UI display name
```

### Available Stages
```
[
    "Address Verification",
    "Aggregator",
    "Amazon RDS for MySQL",
    "Amazon RDS for Oracle",
    "Amazon RDS for PostgreSQL",
    "Amazon Redshift",
    "Amazon S3",
    "Apache Cassandra",
    "Apache Cassandra for DataStage",
    "Apache Derby",
    "Apache HBase",
    "Apache HDFS",
    "Apache Hive",
    "Apache Impala",
    "Apache Kafka",
    "Azure PostgreSQL",
    "Bloom Filter",
    "Box",
    "Change Apply",
    "Change Capture",
    "Checksum",
    "Column Export",
    "Column Generator",
    "Column Import",
    "Combine Records",
    "Compare",
    "Complex Flat File",
    "Compress",
    "Copy",
    "Data Rules",
    "Data set",
    "DataStax Enterprise",
    "Decode",
    "Denodo",
    "Difference",
    "Dremio",
    "Dropbox",
    "Elasticsearch",
    "Encode",
    "Exasol",
    "Expand",
    "External Filter",
    "External Source",
    "External Target",
    "FTP",
    "File set",
    "Filter",
    "Funnel",
    "Generic",
    "Generic JDBC",
    "Generic S3",
    "Google BigQuery",
    "Google Cloud Pub/Sub",
    "Google Cloud Storage",
    "Google Looker",
    "Greenplum",
    "HTTP",
    "Head",
    "Hierarchical Data",
    "IBM Cloud Databases for MongoDB",
    "IBM Cloud Databases for MySQL",
    "IBM Cloud Databases for PostgreSQL",
    "IBM Cloud Object Storage",
    "IBM Cognos Analytics",
    "IBM Data Virtualization",
    "IBM Data Virtualization Manager for z/OS",
    "IBM Db2",
    "IBM Db2 Big SQL",
    "IBM Db2 Warehouse",
    "IBM Db2 for DataStage",
    "IBM Db2 for i",
    "IBM Db2 for z/OS",
    "IBM Db2 on Cloud",
    "IBM Informix",
    "IBM MQ",
    "IBM Match 360",
    "IBM Netezza Performance Server",
    "IBM Netezza Performance Server for DataStage",
    "IBM Planning Analytics",
    "IBM watsonx.data Presto",
    "Investigate",
    "Java Integration",
    "Join",
    "Lookup",
    "Lookup file set",
    "Make Subrecord",
    "Make Vector",
    "MariaDB",
    "Match Frequency",
    "Merge",
    "Microsoft Azure Blob Storage",
    "Microsoft Azure Cosmos DB",
    "Microsoft Azure Data Lake Storage",
    "Microsoft Azure Databricks",
    "Microsoft Azure File Storage",
    "Microsoft Azure SQL Database",
    "Microsoft Azure Synapse Analytics",
    "Microsoft SQL Server",
    "MinIO",
    "Modify",
    "MongoDB",
    "MySQL",
    "ODBC",
    "One-source Match",
    "Oracle",
    "Oracle Database for DataStage",
    "Peek",
    "Pivot Enterprise",
    "PostgreSQL",
    "Presto",
    "Promote Subrecord",
    "Remove Duplicates",
    "Rest",
    "Row Generator",
    "SAP ASE",
    "SAP BAPI",
    "SAP Bulk Extract",
    "SAP Delta Extract",
    "SAP HANA",
    "SAP IDoc",
    "SAP IQ",
    "SAP OData",
    "Salesforce API for DataStage",
    "Salesforce.com",
    "Sample",
    "Sequential file",
    "SingleStoreDB",
    "Slowly Changing Dimension",
    "Snowflake",
    "Sort",
    "Split Subrecord",
    "Split Vector",
    "Standardize",
    "Storage volume",
    "Surrogate Key Generator",
    "Survive",
    "Switch",
    "Tableau",
    "Tail",
    "Teradata",
    "Teradata database for DataStage",
    "Transformer",
    "Two-source Match",
    "Vertica",
    "Wave Generator",
    "Web Service",
    "Write Range Map",
    "XML Input",
    "XML Output",
]
```

### Setting stage properties

Always set `stage.configuration.runtime_column_propagation = True` on stages that have it. Otherwise, schemas will not be propagated and will cause downstream compilation failures.

When adding new properties, call `datastage_property_lookup` first to verify property names and accepted values — never guess.

Both access styles work:
```python
stage.configuration['key_capture_mode'] = 'RECORD_HEADER'
stage.configuration.key_capture_mode = 'RECORD_HEADER'
```

When `accepted_values` on a field is non-empty, use one of those values exactly.

**Property value types:**
- **Primitives**: `int`, `str`, `bool`
- **Enums**: Use `STAGENAME.PropertyName.enum_value` format, e.g. `PEEK.Dataset.true`
- **Lists or Dicts**: For complex properties like `key_properties`

### Stage-specific enum classes

Enum-valued properties require the **stage-specific** enum class — the class name is the stage's own (e.g. `ROW_GENERATOR.Execmode`, `POSTGRESQL_IBMCLOUD.TableAction`), not a shared/global one. The same property name (`execmode`, `table_action`, …) maps to a different enum class per stage, so you cannot reuse one stage's class for another.

```python
from ibm_watsonx_data_integration.services.datastage import PEEK, ROW_GENERATOR

row_gen.configuration.execmode = ROW_GENERATOR.Execmode.par   # parallel
peek.configuration.execmode = PEEK.Execmode.seq               # sequential
peek.configuration.dataset = PEEK.Dataset.false
```

`table_action` follows the exact same rule — the truncate/replace enum class depends on the connector stage type: `POSTGRESQL_IBMCLOUD.TableAction.replace` for "IBM Cloud Databases for PostgreSQL", `POSTGRESQL.TableAction.replace` for generic PostgreSQL, `ODBC.TableAction.replace` for ODBC stages. There is no `overwrite` property — use `table_action`.

When unsure which enum class a stage uses, call `datastage_property_lookup` with the stage name and read the property's enum class name from the result.

Other common stage properties: `auto_column_propagation`, `combinability`.

---

## Connecting stages

```python
# Basic
origin.connect_output_to(destination)
destination.connect_input_to(origin)                 # equivalent

# Chaining (returns the destination stage)
origin.connect_output_to(processor).connect_output_to(destination)

# Fan-out (one stage to many) — call separately for each destination
link_a = origin.connect_output_to(proc1)
link_b = origin.connect_output_to(proc2)
link_c = origin.connect_output_to(proc3)
```

`connect_output_to` returns a link object you can name and attach schemas to (see [Link schemas](#link-schemas)).

### Link type methods

Every link defaults to `PRIMARY`. Only call when changing type:

```python
link.primary()    # Set as PRIMARY link (default — rarely needed)
link.reference()  # Set as REFERENCE link
link.reject()     # Set as REJECT link
```

**Wrong — chained assignment is NOT supported:**
```python
link = transformer.connect_output_to(join_stage).primary()
```

**Correct — separate statements:**
```python
link = transformer.connect_output_to(join_stage)
link.name = "Link_Transformer_Join"

link = rg2.connect_output_to(join_stage)
link.name = "Link_RG2_Join"
link.reference()
```

---

## Link schemas

Every link needs a schema or the flow won't compile. Always create schemas for every input stage. Output stages do not typically need explicit schemas — `runtime_column_propagation` handles downstream schemas automatically.

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

### Field sources

If a field maps to a column from an upstream link, the source MUST be specified or compilation will fail:

```python
schema.add_field("INTEGER", "value2", source="Link_1.value2")
schema.add_field("VARCHAR", "value1", source="Link_1.value1")
```

### Field properties

Every schema must have at least one field. Use mock fields with plausible types if the user hasn't specified columns explicitly.

Configure schema field properties by setting attributes on the field or passing them to `add_field` upfront:

```python
field = schema.add_field("VARCHAR", "column_name", source="Link_Before.Column_Name")
field.description = "Field description"
field.nullable = True
field.key = True
field.length = 255
field.scale = 2

# derivation must be passed as a kwarg to add_field — not set post-hoc
schema.add_field("DATE", "computed_col", derivation="CurrentDate()")
schema.add_field("DECIMAL", "derived", length=10, precision=2, derivation="Link_1.my_num * 2")
```

Some field-level properties use the `FIELD` enum class — it is available in scope automatically, no import needed:

```python
schema.add_field("VARCHAR", "col", delimiter=FIELD.Delim.comma)
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

## Writing the flow's output to a file

A flow whose result the user will want to *read* — sample rows, a count, a transformed extract — writes to a **Sequential file** sink. The output is only retrievable afterwards if the stage registers a project data asset, so set these four together:

```python
sink = flow.add_stage("Sequential file", "Output_1")
sink.configuration.file = ["orders_summary.csv"]          # a LIST, and the property is `file`
sink.configuration.create_data_asset = True               # default False — without it nothing is published
sink.configuration.data_asset_name = "orders_summary.csv" # the name the asset appears under
sink.configuration.first_line_is_column_names = SEQUENTIALFILE.FirstLineColumnNames.true
```

- **The property is `file`, and it takes a list.** `file_name` and `file_type` do not exist on this stage and are the most common compile error on the SDK path.
- **`create_data_asset` defaults to `False`.** A flow that omits it runs green and publishes nothing — there is then no asset to preview and no way to recover the rows. Never conclude from a missing asset that the run failed; check this property first.
- **Keep `data_asset_name` identical to the file name**, as the pyflow compiler does. They are separate properties, so they can disagree — and then the asset exists under a name you are not searching for.
- `file_update_mode`, `delimiter`, `quote`, and `final_delimiter` already default to overwrite / comma / double-quote / end-of-row. Leave them alone unless the user asked for something else.

After the run completes, find the asset with `list_data_assets(entity_name=<data_asset_name>)` and read it with `read_data_preview` (binding = the asset's id). The name you set above is the name to search for.

---

## Connection binding

### Local connections

Set properties on the stage's connection property — accessible only within the scope of the stage and current flow:

```python
stage.configuration.connection.property_name_1 = value_1
stage.configuration.connection.property_name_2 = value_2
```

### Project-level connections

Retrieve an existing project-level connection:

```python
conn = project.connections.get(name='my-db-connection')
```

Create a new project-level connection — retrieve the `DatasourceType` first:

```python
datasource_type = platform.datasources.get(name='IBM Db2')
connection = project.create_connection(
    name="...",
    datasource_type=datasource_type,
    description="...",
    properties={
        "database": "...",
        "port": 1234,
        "username_password_security": DB2_CONNECTION.UsernamePasswordSecurity.default,
    },
)
```

Only `name` and `datasource_type` are required.

Attach to a stage:

```python
stage = flow.add_stage(type='IBM Db2', label='db2_source')
stage.use_connection(conn)
stage.configuration.schema_name = 'MYSCHEMA'
stage.configuration.table_name = 'MYTABLE'
```

**WARNING — connection must be a variable, never a string literal:**
```python
# WRONG — passing string directly causes a runtime error
db2_stage.use_connection("db2-conn")

# WRONG — inline call not supported
db2_stage.use_connection(project.connections.get(name="db2-conn"))

# CORRECT — always assign to a variable first, then pass the variable
db2_conn = project.connections.get(name="db2-conn")
db2_stage.use_connection(db2_conn)
```

---



## Validation and running — not part of the submission

The submission is the flow *definition* and nothing else. Saving, compiling, and running are the MCP tools' job, and the grammar rejects the library calls that do them:

| To do this | Do NOT write | Call this instead |
|---|---|---|
| save the flow | `project.update_flow(flow)` | nothing — `create_datastage_flow` / `update_datastage_flow` saves |
| compile / validate | `flow.compile()`, `project.validate_flow(flow)` | nothing — the same call compiles as part of the save |
| create a job | `project.create_job(...)` | the `create_job` tool |
| run it | `job.start(...)` | the `create_job_run` tool |
| check on it | `job_run.refresh_status()`, `job_run.logs` | the `poll_datastage_job` / `get_job_run_logs` tools |
| cancel it | `job_run.cancel()` | the `cancel_job_run` tool |

Any of these inside `sdk_code` fails the whole submission with *"Unsupported statement type"* and nothing is saved.

---

## Complete example

```python
# Create flow
flow = project.create_flow(name="DataMergeFlow", environment=None, flow_type="batch")

# Retrieve existing project-level connection
db2_conn = project.connections.get(name="My Db2 Connection")

# Add stages and configure their properties
row_gen_1 = flow.add_stage("Row Generator", "Row_Generator_1")
row_gen_1.configuration.records = 100

db2_stage = flow.add_stage("IBM Db2", "Db2_1")
db2_stage.use_connection(db2_conn)
db2_stage.configuration.row_limit = 100

merge = flow.add_stage("Merge", "Merge_1")
merge.configuration.key_properties = [{"key": "ID", "asc-desc": "asc"}]

peek = flow.add_stage("Peek", "Peek_1")
peek.configuration.dataset = PEEK.Dataset.false
peek.configuration.all = PEEK.All.false
peek.configuration.nrecs = 20

# Create links, create schemas, and configure schema fields
link1 = row_gen_1.connect_output_to(merge)
link1.name = "Link_1"
schema1 = link1.create_schema()
schema1.add_field("INTEGER", "ID")
field = schema1.add_field("VARCHAR", "NAME", nullable=True)
field.length = 200
schema1.add_field("DECIMAL", "AMOUNT")

link2 = db2_stage.connect_output_to(merge)
link2.name = "Link_2"
schema2 = link2.create_schema()
schema2.add_field("INTEGER", "ID")
schema2.add_field("VARCHAR", "NAME")
schema2.add_field("DECIMAL", "AMOUNT")

link3 = merge.connect_output_to(peek)
link3.name = "Link_3"

# Write the result somewhere the user can actually read it
sink = flow.add_stage("Sequential file", "Output_1")
sink.configuration.file = ["merged_data.csv"]
sink.configuration.create_data_asset = True
sink.configuration.data_asset_name = "merged_data.csv"
sink.configuration.first_line_is_column_names = SEQUENTIALFILE.FirstLineColumnNames.true

link4 = peek.connect_output_to(sink)
link4.name = "Link_4"
```

Note there is no `flow.compile()` or `project.update_flow(flow)` at the end — including either one fails the submission.

---

## Key rules

1. **The code will NOT be executed in a full Python environment.** Only generate simple, flat syntax as described above.
2. **Do not hallucinate methods** that are not listed here.
3. **Do not add `update_flow` or `compile` calls at the end** of a submission — those are handled by the MCP tool. Avoid imports beyond built-ins and `ibm_watsonx_data_integration` paths.
4. **No complex Python constructs:** loops (`for`, `while`), conditionals (`if`, `elif`, `else`, `match`), functions (`def`, `async def`, `lambda`), exception handling (`try`, `except`, `finally`, `raise`), context managers (`with`, `async with`), classes (`class`), decorators (`@`), assertions (`assert`), `del`, augmented assignments (`+=`, `-=`, etc.), the walrus / named-expression operator (`:=` — never inline-assign inside another expression; assign to a variable on its own line first), `return`, `yield`, `break`, `continue`, `pass`, `global`, `nonlocal`.
5. **Stage types and datasource types must match exactly** and are case sensitive.
6. **Avoid modifying user-inputted code unless absolutely necessary.**
7. **Always include every required property.** Guess mock values when a required property is not explicitly specified. Never skip conditionally required properties when the condition is met.
8. **Adhere to the cardinality rules** in stage-specific files.
9. **If a field maps to a column from an upstream link, the source MUST be specified** or compilation will fail.

---

## Foot-guns

- **`.list()` does not exist** on any collection — always `.get_all()`.
- **Parameter is `project_id=`, not `id=`** — `platform.projects.get(project_id='abc-123')`.
- **Fetch batch flows by `flow_id`, not by name** — `retrieve_datastage_flow_code`'s name path takes the first name-search match without checking it is unique.
- **No BOOLEAN column type.** Use `BIT` with 0/1.
- **Never guess enum values.** Inspect `accepted_values` and use one exactly.
- **No save, compile, job, or run calls in a submission** — see [Validation and running](#validation-and-running--not-part-of-the-submission).
- **The Sequential file sink property is `file` (a list), never `file_name`** — and without `create_data_asset = True` the run publishes no asset to read back.
- **Connection must be a variable, not a string literal** — always assign to a variable first.
- **Table action enums are stage-specific** (e.g. `POSTGRESQL_IBMCLOUD.TableAction.replace`, not `POSTGRESQL.TableAction` or `overwrite`). This is the same per-stage enum-class rule as `execmode` — see [Stage-specific enum classes](#stage-specific-enum-classes).
