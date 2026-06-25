# Runtime SQL Dialect Mapping Reference

This document provides the mapping between data source connection types and runtime SQL dialect values used by the `substrait_to_sql` tool.

## Supported Runtime Dialects

The following dialect values are accepted by the runtime `/sql` endpoint:
- `postgresql`
- `mysql`
- `oracle`
- `teradata`
- `bigquery`
- `snowflake`
- `db2`
- `presto`
- `mariadb`
- `dremio`
- `hive`
- `spark`
- `sqlite`
- `flink`
- `redshift`
- `databricks`

## Connection Type to Dialect Mapping

Map inspected `datasource_type` values to `runtime_target_dialect` before calling `substrait_to_sql`. Match case-insensitively and prefer the most specific match.

| Connection datasource type contains | `target_dialect` |
|---|---|
| `PostgreSQL`, `Postgres`, `Amazon RDS for PostgreSQL`, `Azure PostgreSQL`, `IBM Cloud Databases for PostgreSQL` | `postgresql` |
| `Amazon Redshift`, `Redshift` | `redshift` |
| `Google BigQuery`, `BigQuery` | `bigquery` |
| `MySQL`, `Amazon RDS for MySQL`, `IBM Cloud Databases for MySQL` | `mysql` |
| `MariaDB` | `mariadb` |
| `Db2`, `DB2`, `IBM Db2`, `IBM Db2 Warehouse`, `IBM Db2 on Cloud`, `IBM Db2 Big SQL`, `IBM Db2 for z/OS`, `IBM Db2 for i` | `db2` |
| `Oracle` | `oracle` |
| `Snowflake` | `snowflake` |
| `Teradata` | `teradata` |
| `Presto` | `presto` |
| `Apache Hive`, `Hive` | `hive` |
| `Apache Spark`, `Spark SQL`, `Spark` | `spark` |
| `SQLite`, `Sqlite` | `sqlite` |
| `Dremio` | `dremio` |
| `Apache Flink`, `Flink` | `flink` |
| `Databricks`, `Databricks SQL`, `Databricks Lakehouse` | `databricks` |

## Usage Notes

1. **For runtime `/sql` conversion only**: This mapping is used exclusively when calling `substrait_to_sql` in Phase 2 of the SQL generation workflow.

2. **Not for Phase 3 fallback**: When falling back to direct model-generated SQL (Phase 3), generate SQL for any database named or implied by the user's request and source metadata, even if it's not in this list.

3. **Case-insensitive matching**: Match connection types case-insensitively.

4. **Most specific match**: When multiple patterns could match, prefer the most specific one.

5. **Unknown sources**: If no source connection can be mapped, call `substrait_to_sql` with an empty `target_dialect` value to use runtime default dialect behavior.