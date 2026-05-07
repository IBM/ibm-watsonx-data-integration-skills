---
name: di-sdk-batch-flows
description: Build and run DataStage batch flows via the Python SDK — workflow, stage configuration, schema definitions, available stage types, and column types.
---

# Batch flows

---

## Key differences from streaming

- Batch flows do **not** need an environment at all
- Always fetch batch flows by `flow_id` — fetching by name returns incomplete stage data

```python
# ALWAYS fetch batch flows by flow_id — fetching by name returns incomplete stage data
flow = project.flows.get(flow_id='abc-123')     # ✅ stages populated
flow = project.flows.get(name='My Batch Flow')  # ❌ stages missing

# Creating a batch flow
flow = project.create_flow(name='My Batch Flow', flow_type='batch')

# Compile the flow
flow.compile()

# Batch job runtime config
batch_job.edit_configuration(
    environment='default_datastage_px',
    retention_amount=100,
    warn_limit=50,
)
```

---

## Creating Batch Flows

When creating batch flows, follow this work flow:
```
1.  authenticate         → Detect auth type (IAMAuthenticator, ICP4DAuthenticator, or ZenApiKeyAuthenticator) + Platform
2.  get project          → platform.projects.get(project_id=...)
3.  create flow  → project.flows.get(name=...) or project.create_flow(name=..., environment=env)
4.  add stages           → flow.add_stage(label=..., type=...)
5.  configure stages     → print(stage.configuration), then set fields using accepted_values
6. connect stages       → schema = origin.connect_output_to(destination)
7. define schema fields      -> schema.add_field(...)

8. update flow          → project.update_flow(flow)
9. compile flow        → flow.compile()
10. create job           → project.create_job(name=..., flow=flow)
11. start job            → job_run = job.start()
```

Important notes for creating batch flows:
- For more information on adding stages, refer to `watsonx://docs/chapters:05_preparing_data:batch:stages`
- For more information on adding and configuring schemas, refer to `watsonx://docs/chapters:05_preparing_data:batch:batch_schemas`
- Every link between stages must have a defined schema for the flow to compile properly.
- NEVER guess on what configuration values are accepted. Always check the stage models for each stage.
- If you need more clarification on stage configuration, prompt the user more to better understand their needs. For example, if a user would like to use a postgresql stage to pull from their postgres database, ask the user to provide the table name, schema name, and column names.

---

## Stage models and enums

All batch stage models are under:
```
ibm_watsonx_data_integration/services/datastage/models/stage_models
```

When using configurations for batch stages, check the accepted values in the enums file:
```
ibm_watsonx_data_integration/services/datastage/models/enums
```

When adding a new stage, make sure the `type` parameter is properly defined. The `type` parameter is used to determine which stage you are adding, and the list of available options are defined here: ibm_watsonx_data_integration/services/datastage/models/stage_type_str.py. The list is also defined later in this document under "Available batch stages".

To clarify the `label` parameter in flow.add_stage() is what the UI will display for the stage, and the `type` parameter is the type of stage you are adding to the flow. So for example, if I wanted to add a row generator stage with the label "myrowgenerator" I would call `flow.add_stage(type="Row Generator", label="myrowgenerator")` since the appropriate stage type found in the list is "Row Generator".

Additionally, when using a connection stage, make sure to use the stage.use_connection() function to properly define what connection that the stage uses. The stage.use_connection() function takes the Connection object as a parameter.

---

## Schema models and enums

When adding columns to link schemas, you can find the accepted types here:
```
ibm_watsonx_data_integration/services/datastage/models/schema/schema.py
```

---

## Available batch stages

**Full alphabetical list of stage types:**
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

## Available batch stage column types:

Below is a list of column types that can be used when adding fields to a schema via the schema.add_field() function.

**Full alphabetical list of stage column types:**
```
[
    "BIGINT",
    "BINARY",
    "BIT",
    "CHAR",
    "DATE",
    "DECIMAL",
    "DOUBLE",
    "FLOAT",
    "INTEGER",
    "LONGNVARCHAR",
    "LONGVARBINARY",
    "LONGVARCHAR",
    "NCHAR",
    "NUMERIC",
    "NVARCHAR",
    "REAL",
    "SMALLINT",
    "TIME",
    "TIMESTAMP",
    "TINYINT",
    "UNKNOWN",
    "VARBINARY",
    "VARCHAR"
]
```
