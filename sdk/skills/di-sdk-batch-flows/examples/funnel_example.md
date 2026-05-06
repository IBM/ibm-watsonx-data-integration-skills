User request:
Please create a batch flow in my project "my-test-project" in the Dallas Region. This flow should leverage the following connections in my project:

- "PostgresSQL-AmazonRDS-conn": Amazon RDS for PostgreSQL
- "db2BigSql": IBM Db2 Big SQL
- "oracle-conn": Oracle
- "mysql-conn": MySQL
- "db2cloud-conn": IBM Db2 on Cloud
- "hive-conn": Apache Hive

In my connections for PostgresSQL-AmazonRDS-conn, db2BigSql, oracle-conn, mysql-conn, and db2cloud-conn, I have tables under the "duplicate_schema.duplicate_table" that I would like to combine into a single table which will be uploaded to hive-conn. I would like the table in hive-conn to be called "combined_duplicate". I would only like to take the first 50 records from each of the tables and upload it to apache hive. The schema for "duplicate_schema.duplicate_table" is very simple, it has one column called "mychar" and is a CHAR(100).

Output:
```
from ibm_watsonx_data_integration.common.auth import IAMAuthenticator
from ibm_watsonx_data_integration.platform import Platform
from ibm_watsonx_data_integration.services.datastage import *
import os

auth = IAMAuthenticator(api_key=os.getenv('WATSONX_API_KEY'))
platform = Platform(auth=auth, base_api_url='https://api.dataplatform.cloud.ibm.com')

project = platform.projects.get(name="my-test-project")

flow = project.create_flow(name="funnel_example", environment=None, flow_type="batch")

# Project-Level Connections
postgres_sql_amazon_rds_conn = project.connections.get(name="PostgresSQL-AmazonRDS-conn")
db2_big_sql = project.connections.get(name="db2BigSql")
hive_conn = project.connections.get(name="hive-conn")
oracle_conn = project.connections.get(name="oracle-conn")
mysql_conn = project.connections.get(name="mysql-conn")
db2cloud_conn = project.connections.get(name="db2cloud-conn")

# Stages
amazon_rds_for_postgre_sql_1 = flow.add_stage("Amazon RDS for PostgreSQL", "Amazon_RDS_for_PostgreSQL_1")
amazon_rds_for_postgre_sql_1.use_connection(postgres_sql_amazon_rds_conn)
amazon_rds_for_postgre_sql_1.configuration.row_limit = 50
amazon_rds_for_postgre_sql_1.configuration.schema_name = "duplicate_schema"
amazon_rds_for_postgre_sql_1.configuration.table_name = "duplicate_Table"

ibm_db2_big_sql_1 = flow.add_stage("IBM Db2 Big SQL", "IBM_Db2_Big_SQL_1")
ibm_db2_big_sql_1.use_connection(db2_big_sql)
ibm_db2_big_sql_1.configuration.runtime_column_propagation = False
ibm_db2_big_sql_1.configuration.row_limit = 50
ibm_db2_big_sql_1.configuration.schema_name = "duplicate_schema"
ibm_db2_big_sql_1.configuration.table_name = "duplicate_table"

oracle_1 = flow.add_stage("Oracle", "Oracle_1")
oracle_1.use_connection(oracle_conn)
oracle_1.configuration.runtime_column_propagation = False
oracle_1.configuration.row_limit = 50
oracle_1.configuration.schema_name = "duplicate_schema"
oracle_1.configuration.table_name = "duplicate_table"

my_sql_1 = flow.add_stage("MySQL", "MySQL_1")
my_sql_1.use_connection(mysql_conn)
my_sql_1.configuration.runtime_column_propagation = False
my_sql_1.configuration.row_limit = 50
my_sql_1.configuration.schema_name = "duplicate_schema"
my_sql_1.configuration.table_name = "duplicate_table"

ibm_db2_on_cloud_1 = flow.add_stage("IBM Db2 on Cloud", "IBM_Db2_on_Cloud_1")
ibm_db2_on_cloud_1.use_connection(db2cloud_conn)
ibm_db2_on_cloud_1.configuration.runtime_column_propagation = False
ibm_db2_on_cloud_1.configuration.row_limit = 50
ibm_db2_on_cloud_1.configuration.schema_name = "duplicate_schema"
ibm_db2_on_cloud_1.configuration.table_name = "duplicate_table"

funnel_1 = flow.add_stage("Funnel", "Funnel_1")

funnel_1.configuration.runtime_column_propagation = False
funnel_1.configuration.inputlink_ordering_list = [
    {"link_label": "0", "link_name": "Link_1"},
    {"link_label": "1", "link_name": "Link_2"},
    {"link_label": "2", "link_name": "Link_3"},
    {"link_label": "3", "link_name": "Link_4"},
    {"link_label": "4", "link_name": "Link_5"},
]
funnel_1.configuration.key_properties = [{"asc-desc": "asc", "key": "mychar"}]
funnel_1.configuration.operator = FUNNEL.Operator.sortfunnel
funnel_1.configuration.show_coll_type = False
funnel_1.configuration.show_part_type = True
funnel_1.configuration.show_sort_options = False

apache_hive_1 = flow.add_stage("Apache Hive", "Apache_Hive_1")
apache_hive_1.use_connection(hive_conn)
apache_hive_1.configuration.ds_table_name = "combined_duplicate"
apache_hive_1.configuration.output_acp_should_hide = False
apache_hive_1.configuration.show_coll_type = False
apache_hive_1.configuration.show_part_type = True
apache_hive_1.configuration.show_sort_options = False

# Graph
link_1 = amazon_rds_for_postgre_sql_1.connect_output_to(funnel_1)
link_1.name = "Link_1"
amazon_rds_for_postgre_sql_1_schema = link_1.create_schema()
amazon_rds_for_postgre_sql_1_schema.add_field("CHAR", "mychar", length=100)


link_6 = funnel_1.connect_output_to(apache_hive_1)
link_6.name = "Link_6"
funnel_1_schema = link_6.create_schema()
funnel_1_schema.add_field("CHAR", "mychar", length=100)


link_2 = ibm_db2_big_sql_1.connect_output_to(funnel_1)
link_2.name = "Link_2"
ibm_db2_big_sql_1_schema = link_2.create_schema()
ibm_db2_big_sql_1_schema.add_field("CHAR", "mychar", length=100)


link_3 = oracle_1.connect_output_to(funnel_1)
link_3.name = "Link_3"
oracle_1_schema = link_3.create_schema()
oracle_1_schema.add_field("CHAR", "mychar", length=100)


link_4 = my_sql_1.connect_output_to(funnel_1)
link_4.name = "Link_4"
my_sql_1_schema = link_4.create_schema()
my_sql_1_schema.add_field("CHAR", "mychar", length=100)


link_5 = ibm_db2_on_cloud_1.connect_output_to(funnel_1)
link_5.name = "Link_5"
ibm_db2_on_cloud_1_schema = link_5.create_schema()
ibm_db2_on_cloud_1_schema.add_field("CHAR", "mychar", length=100)


project.update_flow(flow)


funnel_example_job = project.create_job(name="funnel_example_job", flow=flow)


funnel_example_job_run = funnel_example_job.start(name="funnel_example_job_run", description="")
