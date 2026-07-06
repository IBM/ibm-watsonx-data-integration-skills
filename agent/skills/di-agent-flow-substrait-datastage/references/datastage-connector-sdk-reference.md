# DataStage Connector Reference

Single-table connector lookup keyed by SDK class / connector map name. Use this with the stage docs in `../stages/` for code generation and property checks.

| Connector | SDK class / map name | Connection types | SDK enum | SQL read | Common SDK properties |
|---|---|---|---|---|---|
| Amazon RDS for PostgreSQL | `amazon_postgresql` | `postgresql-amazon` | `AMAZON_POSTGRESQL` | yes | `select_statement`, `schema_name`, `table_name`, `write_mode`, `table_action` |
| Amazon Redshift | `amazon_redshift` | `RedshiftPX`, `redshift` | `AMAZON_REDSHIFT` | yes | `execution_mode`, `read_method`, `select_statement`, `schema_name`, `table_name`, `write_mode`, `table_action` |
| Amazon RDS for Oracle | `amazonrds_oracle` | `oracle-amazon` | `AMAZONRDS_ORACLE` | yes | `execution_mode`, `read_method`, `select_statement`, `schema_name`, `table_name`, `write_mode`, `table_action` |
| Amazon S3 | `amazons3` | `AmazonS3PX`, `amazons3` | `AMAZONS3` | no | `execution_mode`, `table_name`, `write_mode`, `table_action` |
| Apache HBase | `apache_hbase` | `HBaseConnectorPX`, `hbase-datastage` | `APACHE_HBASE` | no | `execution_mode`, `write_mode` |
| Apache Hive | `apache_hive` | `HiveConnectorPX`, `hive` | `APACHE_HIVE` | yes | `execution_mode`, `read_method`, `select_statement`, `schema_name`, `table_name`, `write_mode`, `table_action` |
| Apache Kafka | `apache_kafka` | `KafkaConnectorPX`, `apachekafka` | `APACHE_KAFKA` | no | `execution_mode` |
| Microsoft Azure Blob Storage | `azure_blob_storage` | `azureblobstorage` | `AZURE_BLOB_STORAGE` | no | `execution_mode`, `table_name`, `write_mode`, `table_action` |
| Microsoft Azure Cosmos DB | `azure_cosmos` | `cosmos` | `AZURE_COSMOS` | no | `execution_mode`, `write_mode` |
| Microsoft Azure Databricks | `azure_databricks` | `databricks` | `AZURE_DATABRICKS` | yes | `execution_mode`, `read_method`, `select_statement`, `schema_name`, `table_name`, `write_mode`, `table_action` |
| Microsoft Azure File Storage | `azure_file_storage` | `azurefilestorage` | `AZURE_FILE_STORAGE` | no | `execution_mode`, `table_name`, `write_mode`, `table_action` |
| Azure PostgreSQL | `azure_postgresql` | `postgresql-azure` | `AZURE_POSTGRESQL` | yes | `execution_mode`, `read_method`, `select_statement`, `schema_name`, `table_name`, `write_mode`, `table_action` |
| Microsoft Azure Data Lake Storage | `azuredatalake` | `AzureDatalakePX`, `azuredatalake` | `AZUREDATALAKE` | no | `execution_mode`, `table_name`, `write_mode`, `table_action` |
| Microsoft Azure SQL Database | `azuresql` | `azuresql` | `AZURESQL` | yes | `execution_mode`, `read_method`, `select_statement`, `schema_name`, `table_name`, `write_mode`, `table_action` |
| Microsoft Azure Synapse Analytics | `azuresynapse` | `azuresynapse` | `AZURESYNAPSE` | yes | `execution_mode`, `read_method`, `select_statement`, `schema_name`, `table_name`, `write_mode`, `table_action` |
| Google BigQuery | `bigquery` | `bigquery`, `bigqueryPX` | `BIGQUERY` | yes | `execution_mode`, `read_method`, `select_statement`, `database_name`, `dataset_name`, `table_name`, `write_mode`, `table_action` |
| IBM Db2 Big SQL | `bigsql` | `bigsql` | `BIGSQL` | yes | `execution_mode`, `read_method`, `select_statement`, `schema_name`, `table_name`, `write_mode`, `table_action` |
| Box | `box` | `box` | `BOX` | no | `execution_mode`, `write_mode` |
| Apache Cassandra | `cassandra` | `CassandraConnectorPX`, `cassandra` | `CASSANDRA` | yes | `execution_mode`, `read_method`, `select_statement`, `schema_name`, `table_name`, `write_mode`, `table_action` |
| Apache Cassandra for DataStage | `cassandra_datastage` | `cassandra-datastage` | `CASSANDRA_DATASTAGE` | no | `execution_mode`, `table_name` |
| IBM Cloud Object Storage | `cloud_object_storage` | `cloudobjectstorage`, `cloudobjectstoragePX` | `CLOUD_OBJECT_STORAGE` | no | `execution_mode`, `table_name`, `write_mode`, `table_action` |
| IBM Cognos Analytics | `cognos_analytics` | `cognos-analytics` | `COGNOS_ANALYTICS` | no | `execution_mode` |
| DataStax Enterprise | `datastax` | `datastax` | `DATASTAX` | yes | `execution_mode`, `read_method`, `select_statement`, `schema_name`, `table_name`, `write_mode`, `table_action` |
| IBM Db2 | `db2` | `DB2ConnectorPX`, `db2` | `DB2` | yes | `execution_mode`, `read_method`, `select_statement`, `schema_name`, `table_name`, `write_mode`, `table_action` |
| IBM Db2 on Cloud | `db2cloud` | `db2cloud` | `DB2CLOUD` | yes | `execution_mode`, `read_method`, `select_statement`, `schema_name`, `table_name`, `write_mode`, `table_action` |
| IBM Db2 for DataStage | `db2fordatastage` | `db2-datastage` | `DB2FORDATASTAGE` | yes | `execution_mode`, `select_statement`, `schema_name`, `table_name`, `write_mode`, `table_action` |
| IBM Db2 for i | `db2iseries` | `db2iseries` | `DB2ISERIES` | yes | `execution_mode`, `read_method`, `select_statement`, `schema_name`, `table_name`, `write_mode`, `table_action` |
| IBM Db2 Warehouse | `db2warehouse` | `dashdb` | `DB2WAREHOUSE` | yes | `execution_mode`, `read_method`, `select_statement`, `schema_name`, `table_name`, `write_mode`, `table_action` |
| IBM Db2 for z/OS | `db2zos` | `db2zos` | `DB2ZOS` | yes | `execution_mode`, `read_method`, `select_statement`, `schema_name`, `table_name`, `write_mode`, `table_action` |
| Denodo | `denodo` | `denodo` | `DENODO` | yes | `execution_mode`, `read_method`, `select_statement`, `schema_name`, `table_name`, `write_mode` |
| Apache Derby | `derby` | `derby` | `DERBY` | yes | `execution_mode`, `read_method`, `select_statement`, `schema_name`, `table_name`, `write_mode`, `table_action` |
| Dremio | `dremio` | `dremio` | `DREMIO` | yes | `execution_mode`, `read_method`, `select_statement`, `schema_name`, `table_name`, `write_mode`, `table_action` |
| Dropbox | `dropbox` | `dropbox` | `DROPBOX` | no | `execution_mode`, `write_mode` |
| IBM Data Virtualization | `dv` | `dv` | `DV` | yes | `execution_mode`, `read_method`, `select_statement`, `schema_name`, `table_name` |
| IBM Data Virtualization Manager for z/OS | `dvm` | `dvm` | `DVM` | yes | `select_statement`, `schema_name`, `table_name`, `write_mode`, `table_action` |
| Elasticsearch | `elasticsearch` | `elasticsearch` | `ELASTICSEARCH` | no | `execution_mode`, `write_mode` |
| Exasol | `exasol` | `exasol` | `EXASOL` | yes | `execution_mode`, `read_method`, `select_statement`, `schema_name`, `table_name`, `write_mode`, `table_action` |
| FTP | `ftp` | `ftp` | `FTP` | no | `execution_mode`, `write_mode` |
| Generic S3 | `generics3` | `generics3` | `GENERICS3` | no | `execution_mode`, `table_name`, `write_mode`, `table_action` |
| Google Cloud Storage | `google_cloud_storage` | `GoogleCloudStoragePX`, `googlecloudstorage` | `GOOGLE_CLOUD_STORAGE` | no | `execution_mode`, `database_name`, `schema_name`, `table_name`, `write_mode`, `table_action` |
| Google Looker | `google_looker` | `looker` | `GOOGLE_LOOKER` | no | `execution_mode` |
| Google Cloud Pub/Sub | `google_pub_sub` | `GooglePubSubPX`, `googlepubsub` | `GOOGLE_PUB_SUB` | no | `execution_mode` |
| Greenplum | `greenplum` | `greenplum` | `GREENPLUM` | yes | `execution_mode`, `read_method`, `select_statement`, `schema_name`, `table_name`, `write_mode`, `table_action` |
| Apache HDFS | `hdfs_apache` | `hdfs-apache` | `HDFS_APACHE` | no | `execution_mode`, `table_name`, `write_mode`, `table_action` |
| HTTP | `http` | `http` | `HTTP` | no | `execution_mode` |
| IBM MQ | `ibm_mq` | `WebSphereMQConnectorPX`, `webspheremq-datastage` | `IBM_MQ` | no | `execution_mode` |
| Apache Impala | `impala` | `impala` | `IMPALA` | yes | `execution_mode`, `read_method`, `select_statement`, `schema_name`, `table_name`, `write_mode`, `table_action` |
| IBM Informix | `informix` | `informix` | `INFORMIX` | yes | `execution_mode`, `read_method`, `select_statement`, `schema_name`, `table_name`, `write_mode`, `table_action` |
| Generic JDBC | `jdbc` | `JDBCConnectorPX`, `genericjdbc` | `JDBC` | yes | `execution_mode`, `read_method`, `select_statement`, `schema_name`, `table_name`, `write_mode`, `table_action` |
| MariaDB | `mariadb` | `mariadb` | `MARIADB` | yes | `execution_mode`, `read_method`, `select_statement`, `schema_name`, `table_name`, `write_mode`, `table_action` |
| IBM Match 360 | `match360` | `match360` | `MATCH360` | no | `execution_mode` |
| MinIO | `minio` | `minio` | `MINIO` | no | `execution_mode`, `table_name`, `write_mode`, `table_action` |
| MongoDB | `mongodb` | `mongodb` | `MONGODB` | yes | `execution_mode`, `read_method`, `select_statement`, `schema_name`, `table_name`, `write_mode`, `table_action` |
| IBM Cloud Databases for MongoDB | `mongodb_ibmcloud` | `mongodb-ibmcloud` | `MONGODB_IBMCLOUD` | yes | `execution_mode`, `read_method`, `select_statement`, `schema_name`, `table_name`, `write_mode`, `table_action` |
| MySQL | `mysql` | `mysql` | `MYSQL` | yes | `execution_mode`, `read_method`, `select_statement`, `schema_name`, `table_name`, `write_mode`, `table_action` |
| Amazon RDS for MySQL | `mysql_amazon` | `mysql-amazon` | `MYSQL_AMAZON` | yes | `execution_mode`, `read_method`, `select_statement`, `schema_name`, `table_name`, `write_mode`, `table_action` |
| Amazon Aurora for MySQL | `mysql_aurora` | `mysql_aurora` | `MYSQL_AMAZON` | yes | `execution_mode`, `read_method`, `select_statement`, `schema_name`, `table_name`, `write_mode`, `table_action` |
| IBM Cloud Databases for MySQL | `mysql_compose` | `mysql-compose`, `mysql-ibmcloud` | `MYSQL_COMPOSE` | yes | `execution_mode`, `read_method`, `select_statement`, `schema_name`, `table_name`, `write_mode`, `table_action` |
| IBM Netezza Performance Server | `netezza` | `NetezzaConnectorPX`, `netezza` | `NETEZZA` | yes | `execution_mode`, `read_method`, `select_statement`, `schema_name`, `table_name`, `write_mode`, `table_action` |
| IBM Netezza Performance Server for DataStage | `netezza_optimized` | `netezza-datastage` | `NETEZZA_OPTIMIZED` | yes | `execution_mode`, `select_statement`, `schema_name`, `table_name`, `write_mode`, `table_action` |
| ODBC | `odbc` | `ODBCConnectorPX`, `odbc-datastage` | `ODBC` | yes | `execution_mode`, `select_statement`, `schema_name`, `table_name`, `write_mode`, `table_action` |
| Oracle | `oracle` | `OracleConnectorPX`, `oracle` | `ORACLE` | yes | `execution_mode`, `read_method`, `select_statement`, `schema_name`, `table_name`, `write_mode`, `table_action` |
| Oracle Database for DataStage | `oracle_datastage` | `oracle-datastage` | `ORACLE_DATASTAGE` | yes | `execution_mode`, `select_statement`, `schema_name`, `table_name`, `write_mode`, `table_action` |
| IBM Planning Analytics | `planning_analytics` | `tm1odata` | `PLANNING_ANALYTICS` | no | `execution_mode` |
| PostgreSQL | `postgresql` | `postgresql` | `POSTGRESQL` | yes | `execution_mode`, `read_method`, `select_statement`, `schema_name`, `table_name`, `write_mode`, `table_action` |
| IBM Cloud Databases for PostgreSQL | `postgresql_ibmcloud` | `postgresql-ibmcloud` | `POSTGRESQL_IBMCLOUD` | yes | `execution_mode`, `read_method`, `select_statement`, `schema_name`, `table_name`, `write_mode`, `table_action` |
| Presto | `presto` | `presto` | `PRESTO` | yes | `execution_mode`, `read_method`, `select_statement`, `schema_name`, `table_name` |
| Salesforce.com | `salesforce` | `salesforce` | `SALESFORCE` | yes | `execution_mode`, `read_method`, `select_statement`, `schema_name`, `table_name`, `write_mode`, `table_action` |
| Salesforce API for DataStage | `salesforceapi` | `SALESFORCEJCConnectorPX`, `salesforce-datastage` | `SALESFORCEAPI` | no | `execution_mode`, `table_name` |
| SAP BAPI | `sapbapi` | `sapbapi` | `SAPBAPI` | no | none in table/SQL pushdown subset |
| SAP Bulk Extract | `sapbulkextract` | `sapbulkextract` | `SAPBULKEXTRACT` | no | `execution_mode`, `table_name` |
| SAP Delta Extract | `sapdeltaextract` | `sapdeltaextract` | `SAPDELTAEXTRACT` | no | `execution_mode` |
| SAP HANA | `saphana` | `saphana` | `SAPHANA` | yes | `execution_mode`, `read_method`, `select_statement`, `schema_name`, `table_name`, `write_mode`, `table_action` |
| SAP IDoc | `sapidoc` | `sapidoc` | `SAPIDOC` | no | `execution_mode` |
| SAP IQ | `sapiq` | `sybaseiq` | `SAPIQ` | yes | `execution_mode`, `read_method`, `select_statement`, `schema_name`, `table_name`, `write_mode`, `table_action` |
| SAP OData | `sapodata` | `sapodata` | `SAPODATA` | no | `execution_mode`, `write_mode` |
| SingleStoreDB | `singlestore` | `singlestore` | `SINGLESTORE` | yes | `execution_mode`, `read_method`, `select_statement`, `schema_name`, `table_name`, `write_mode`, `table_action` |
| Snowflake | `snowflake` | `SnowflakeConnectorPX`, `snowflake` | `SNOWFLAKE` | yes | `execution_mode`, `read_method`, `select_statement`, `schema_name`, `table_name`, `write_mode`, `table_action` |
| Microsoft SQL Server | `sqlserver` | `sqlserver` | `SQLSERVER` | yes | `execution_mode`, `read_method`, `select_statement`, `schema_name`, `table_name`, `write_mode`, `table_action` |
| Storage volume | `storage_volume` | `volumes` | `STORAGE_VOLUME` | no | `execution_mode`, `write_mode` |
| SAP ASE | `sybase` | `sybase` | `SYBASE` | yes | `execution_mode`, `read_method`, `select_statement`, `schema_name`, `table_name`, `write_mode`, `table_action` |
| Tableau | `tableau` | `tableau` | `TABLEAU` | no | `execution_mode` |
| Teradata | `teradata` | `TeradataConnectorPX`, `teradata` | `TERADATA` | yes | `execution_mode`, `read_method`, `select_statement`, `schema_name`, `table_name`, `write_mode`, `table_action` |
| Teradata database for DataStage | `teradata_datastage` | `teradata-datastage` | `TERADATA_DATASTAGE` | yes | `execution_mode`, `select_statement`, `schema_name`, `table_name`, `write_mode`, `table_action` |
| Vertica | `vertica` | `vertica` | `VERTICA` | yes | `execution_mode`, `read_method`, `select_statement`, `schema_name`, `table_name`, `write_mode`, `table_action` |
| IBM watsonx.data Presto | `watsonx_data` | `lakehouse` | `WATSONX_DATA` | yes | `execution_mode`, `read_method`, `select_statement`, `schema_name`, `table_name`, `table_action` |

## Pushdown property naming (SQL-mode read with optional before-SQL)

When generating the Python SDK code for source and target pushdown, you
do **not** set the connector's `database_name`, `dataset_name`,
`table_name`, `schema_name`, `write_mode`, or `table_action` — the SQL
embeds whatever table refs and operations it needs. Set only the
SQL-mode properties below.

Some connectors (Snowflake, Apache Hive, Impala, JDBC) expose **two
parallel property sets** on the same stage model. The
`ds_use_datastage` flag selects which set the connector reads at
runtime:

- **Native mode** — `ds_use_datastage = False`. The connector uses
  its dotted aliases (`select_statement`, `before_after.before`, ...)
  mapped to bespoke SDK field names like `select_statement` and
  `enable_before_sql`. The connector also requires the dialect-typed
  `read_method` enum to be set to its `select` variant. **This is the
  default for new pushdown flows.**
- **DataStage mode** — `ds_use_datastage = True`. The connector uses
  the `_underscore` aliases (`_select_statement`, `_before_after._before_sql`,
  ...) mapped to `ds_*` SDK field names. This is the older
  hand-built reference pattern; we keep it documented as an
  alternative.

Connectors that don't have the `ds_*` family at all (Db2, Oracle,
BigQuery, Databricks, MySQL, PostgreSQL, Teradata, SQL Server, Vertica,
Greenplum, Redshift, Synapse, Azure SQL, Azure PostgreSQL, Netezza,
Sybase, SAP IQ, SingleStore, MariaDB, Informix, Exasol, Presto, Denodo,
Derby, DataStax, watsonx.data) always use Native mode — there's no
`ds_use_datastage` flag and no DataStage-mode fields to set.

### Native mode (`ds_use_datastage = False`, default)

Default property set for all connectors that support pushdown.

| Alias | SDK field name (`configuration.<name>`) | SDK field type | Value for pushdown |
|---|---|---|---|
| `_use_datastage` | `ds_use_datastage` | `bool \| None` | `False` — selects Native mode. Connectors without this flag (Db2, Oracle, etc.) skip this row. |
| `read_mode` | `read_method` | `<Connector>.ReadMethod \| None` | enum value `select` — required on Snowflake/Hive/Impala/JDBC to put the connector in SQL-read mode. Db2/Oracle/etc. either default to SQL-read or use a similar enum; consult the per-connector enum module. |
| `select_statement` | `select_statement` | `str` | source pushdown: the workload SELECT. Target pushdown: the observability SELECT. |
| `before_after.before` | `enable_before_sql` | **`str \| None`** | target pushdown: **the workload SQL block itself** (INSERT/UPDATE/COPY/...). The field name has "enable" in it, but the field is the SQL string — assigning a non-empty string both enables and supplies the before-SQL. Leave `None` for source pushdown. |
| `before_after.before.fail_on_error` | `fail_on_error_before_sql` | `bool \| None` | `True` for target pushdown |
| `before_after.before_node` | `enable_before_sql_node` | `str \| None` | `""` (empty string — required companion observed in the reference flow) |
| `before_after.before_node.fail_on_error` | `fail_on_error_before_sql_node` | `bool \| None` | `True` |
| `before_after.after` | `enable_after_sql` | `str \| None` | `""` (no after-SQL by default; set only if the user specifies one) |
| `before_after.after_node` | `enable_after_sql_node` | `str \| None` | `""` |
| `before_after.after.fail_on_error` | `fail_on_error_after_sql` | `bool \| None` | `True` |
| `before_after.after_node.fail_on_error` | `fail_on_error_after_sql_node` | `bool \| None` | `True` |

**The `enable_*` naming gotcha:** `enable_before_sql` and
`enable_after_sql` are **string fields, not boolean toggles**. Assign
the SQL workload directly to `enable_before_sql`; there is no separate
`before_sql_statement` field — the same field both enables and stores
the SQL.

**Per-connector `read_method` enum import** (for Native mode on
connectors that expose it):

```python
from ibm_watsonx_data_integration.services.datastage.models.enums import SNOWFLAKE
stage.configuration.read_method = SNOWFLAKE.ReadMethod.select
```

Substitute `SNOWFLAKE` with the per-connector enum module (`DB2`,
`ORACLE`, `BIGQUERY`, ...). Available variants typically include
`select`, `general`, and connector-specific options.

### DataStage mode (`ds_use_datastage = True`, alternative)

Only applies to connectors that expose the `ds_*` family: **Snowflake,
Apache Hive, Impala, JDBC**. Aliases begin with `_` and use
dot-separated nesting; SDK field names are derived deterministically —
split on `.`, strip a leading `_` from each token, join with `_`,
prepend `ds_`. Example: `_before_after._after_sql._fail_on_error`
→ `ds_before_after_after_sql_fail_on_error`.

| Alias | SDK field name (`configuration.<name>`) | Type/value for pushdown |
|---|---|---|
| `_use_datastage` | `ds_use_datastage` | `True` — selects DataStage mode |
| `_generate_sql` | `ds_generate_sql` | `False` (we provide SQL ourselves) |
| `_select_statement` | `ds_select_statement` | source pushdown: the workload SELECT. Target pushdown: the observability SELECT (or `"SELECT 1 AS DUMMY_COL"` fallback). |
| `_before_after` | `ds_before_after` | `True` for target pushdown; `False` for source pushdown |
| `_before_after._before_sql` | `ds_before_after_before_sql` | target pushdown: the workload SQL block |
| `_before_after._before_sql._fail_on_error` | `ds_before_after_before_sql_fail_on_error` | `True` (surface workload errors) |
| `_before_after._before_sql._read_from_file_before_sql` | `ds_before_after_before_sql_read_from_file_before_sql` | `False` |
| `_before_after._before_sql_node` | `ds_before_after_before_sql_node` | `""` |
| `_before_after._after_sql._fail_on_error` | `ds_before_after_after_sql_fail_on_error` | `True` |
| `_before_after._after_sql._read_from_file_after_sql` | `ds_before_after_after_sql_read_from_file_after_sql` | `False` |
| `_auto_commit_mode` | `ds_auto_commit_mode` | leave at default (`"enable"`) |

### Per-connector mode selection

| Connector | Modes available | Default for pushdown |
|---|---|---|
| Snowflake | Native, DataStage | **Native** |
| Apache Hive | Native, DataStage | Native |
| Impala | Native, DataStage | Native |
| JDBC (generic) | Native, DataStage | Native |
| Db2 (all variants), Oracle (all variants), BigQuery, Azure Databricks, MySQL (all variants), PostgreSQL (all variants), Teradata, Microsoft SQL Server, Vertica, Greenplum, Redshift, Azure SQL / Synapse, Netezza, Sybase, SAP IQ, SingleStore, MariaDB, Informix, Exasol, Presto, Denodo, Derby, DataStax, watsonx.data | Native only (no `ds_use_datastage` flag) | Native |
| Cassandra, MongoDB, SAP HANA, Dremio, Salesforce | **read-only**, no before-SQL — `select_statement` only | Native (source pushdown only) |

### What NOT to set for pushdown

In either mode, omit the following from the connector configuration:

- `database_name`, `dataset_name`, `table_name`, `schema_name` —
  table refs live inside the SQL.
- `write_mode`, `table_action` — DataStage's row-by-row write path is
  not used in pushdown.
- `execution_mode` — leave at default unless the user specifies one;
  it does not affect SQL pushdown semantics.

The `read_method` field is **required** in Native mode (set it to the
connector's `select` enum value); it was previously listed as
"do not set" — that was wrong for Native mode.

### Authoritative source for fields not in the tables above

The mappings above cover the SQL pushdown subset. For fields outside
this subset — full property reference per connector — load the stage
model from the Python SDK package:

```python
from ibm_watsonx_data_integration.services.datastage.models import (
    <ConnectorName>Stage,  # e.g. SnowflakeStage, Db2Stage, BigQueryStage
)
# Inspect fields:
for name, fi in <ConnectorName>Stage.model_fields.items():
    print(name, fi.alias)
```

The same data is also dumped as JSON under
`sdk/datastage/stages/<connector>.json` in the runtime's resources tree;
each entry's `pydantic_alias` is the alias and `name` is the SDK field
name used by `configuration.<name>`. Do not vendor these files into the
skill tree — load on demand from the SDK package or the runtime's
resource path provided by the user.
