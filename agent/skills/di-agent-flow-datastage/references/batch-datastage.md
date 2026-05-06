# Batch flows (DataStage)

Batch-specific nuances. Read alongside [editing-flows.md](editing-flows.md).

## Batch job runtime config

```python
batch_job.edit_configuration(
    environment='default_datastage_px',
    retention_amount=100,
    warn_limit=50,
)
```

## Stage discovery — static catalog

All DataStage batch stages have static catalogs — no runtime discovery needed.

- Usage overview and when-to-use: [stages/](stages/) (one file per stage)
- Property lookup at runtime: `datastage_property_lookup(requests=[{"stage": "Aggregator", "properties": ["grouping_keys"]}])` — batched, one or more stages per call

`flow.add_stage(type=<stage-type-string>, label=<ui-label>)`. The stage type string must match the catalog exactly — e.g. `type="Row Generator"` for a Row Generator, `type="Transformer"` for a Transformer.

### Available batch stage types

```
Address Verification, Aggregator, Amazon RDS for MySQL, Amazon RDS for Oracle,
Amazon RDS for PostgreSQL, Amazon Redshift, Amazon S3, Apache Cassandra,
Apache Cassandra for DataStage, Apache Derby, Apache HBase, Apache HDFS,
Apache Hive, Apache Impala, Apache Kafka, Azure PostgreSQL, Bloom Filter,
Box, Change Apply, Change Capture, Checksum, Column Export, Column Generator,
Column Import, Combine Records, Compare, Complex Flat File, Compress, Copy,
Data Rules, Data set, DataStax Enterprise, Decode, Denodo, Difference,
Dremio, Dropbox, Elasticsearch, Encode, Exasol, Expand, External Filter,
External Source, External Target, FTP, File set, Filter, Funnel, Generic,
Generic JDBC, Generic S3, Google BigQuery, Google Cloud Pub/Sub,
Google Cloud Storage, Google Looker, Greenplum, HTTP, Head, Hierarchical Data,
IBM Cloud Databases for MongoDB, IBM Cloud Databases for MySQL,
IBM Cloud Databases for PostgreSQL, IBM Cloud Object Storage,
IBM Cognos Analytics, IBM Data Virtualization,
IBM Data Virtualization Manager for z/OS, IBM Db2, IBM Db2 Big SQL,
IBM Db2 Warehouse, IBM Db2 for DataStage, IBM Db2 for i, IBM Db2 for z/OS,
IBM Db2 on Cloud, IBM Informix, IBM MQ, IBM Match 360,
IBM Netezza Performance Server, IBM Netezza Performance Server for DataStage,
IBM Planning Analytics, IBM watsonx.data Presto, Investigate, Java Integration,
Join, Lookup, Lookup file set, Make Subrecord, Make Vector, MariaDB,
Match Frequency, Merge, Microsoft Azure Blob Storage,
Microsoft Azure Cosmos DB, Microsoft Azure Data Lake Storage,
Microsoft Azure Databricks, Microsoft Azure File Storage,
Microsoft Azure SQL Database, Microsoft Azure Synapse Analytics,
Microsoft SQL Server, MinIO, Modify, MongoDB, MySQL, ODBC,
One-source Match, Oracle, Oracle Database for DataStage, Peek,
Pivot Enterprise, PostgreSQL, Presto, Promote Subrecord, Remove Duplicates,
Rest, Row Generator, SAP ASE, SAP BAPI, SAP Bulk Extract, SAP Delta Extract,
SAP HANA, SAP IDoc, SAP IQ, SAP OData, Salesforce API for DataStage,
Salesforce.com, Sample, Sequential file, SingleStoreDB,
Slowly Changing Dimension, Snowflake, Sort, Split Subrecord, Split Vector,
Standardize, Storage volume, Surrogate Key Generator, Survive, Switch,
Tableau, Tail, Teradata, Teradata database for DataStage, Transformer,
Two-source Match, Vertica, Wave Generator, Web Service, Write Range Map,
XML Input, XML Output
```

## Link schemas

Every link between batch stages must have a defined schema or the flow won't compile. Schema field syntax and column types are in [sdk-conventions.md](sdk-conventions.md).
