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
