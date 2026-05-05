from ibm_watsonx_data_integration.common.auth import IAMAuthenticator
from ibm_watsonx_data_integration.platform import Platform
import os

# Setup authentication and platform
api_key = os.environ.get('WATSONX_API_KEY', 'YourApiKey')
base_auth_url = os.environ.get('WATSONX_AUTH_URL', 'https://cloud.ibm.com')
base_api_url = os.environ.get('WATSONX_API_URL', 'https://api.dataplatform.cloud.ibm.com')

auth = IAMAuthenticator(api_key=api_key, base_auth_url=base_auth_url)
platform = Platform(auth=auth, base_api_url=base_api_url)

# Get project by name
project_name = os.environ.get('WATSONX_PROJECT_NAME', 'ProjectName')
project = platform.projects.get(name=project_name)

# Check if flow exists, if so get it, otherwise create it
flow_name = "funnel_example"
flow = None
try:
    # Try to get existing flow by name
    flow = project.flows.get(name=flow_name)
    print(f"Found existing flow '{flow_name}'")
    print("Deleting the existing flow so it can be recreated")
    project.delete_flow(flow)
except Exception as e:
    print(f"Flow '{flow_name}' not found, will create new one")

# Create the flow
flow = project.create_flow(name=flow_name, environment=None, flow_type="batch")
print(f"Created new flow '{flow_name}'")

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

print(f"Flow '{flow.name}' created successfully!")
print(f"Flow ID: {flow.flow_id}")
