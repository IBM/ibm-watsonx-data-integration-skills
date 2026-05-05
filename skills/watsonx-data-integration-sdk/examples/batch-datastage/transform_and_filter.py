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
flow_name = "azure_sql_transform_filter_example"
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
azure_sql_conn = project.connections.get(name="azure-sql-conn")

# Stages
microsoft_azure_sql_database_1 = flow.add_stage("Microsoft Azure SQL Database", "Microsoft_Azure_SQL_Database_1")
microsoft_azure_sql_database_1.use_connection(azure_sql_conn)
microsoft_azure_sql_database_1.configuration.runtime_column_propagation = False
microsoft_azure_sql_database_1.configuration.schema_name = "my_schema"
microsoft_azure_sql_database_1.configuration.table_name = "my_table"

transformer_1 = flow.add_stage("Transformer", "Transformer_1")
transformer_1.configuration.runtime_column_propagation = False

filter_1 = flow.add_stage("Filter", "Filter_1")

filter_1.configuration.show_coll_type = False
filter_1.configuration.show_part_type = True
filter_1.configuration.show_sort_options = False
filter_1.configuration.where_properties = [{"where": "my_decimal_2 > 10", "target": "0"}]

microsoft_azure_sql_database_2 = flow.add_stage("Microsoft Azure SQL Database", "Microsoft_Azure_SQL_Database_2")
microsoft_azure_sql_database_2.use_connection(azure_sql_conn)
microsoft_azure_sql_database_2.configuration.column_metadata_change_propagation = False
microsoft_azure_sql_database_2.configuration.output_acp_should_hide = False
microsoft_azure_sql_database_2.configuration.schema_name = "my_schema"
microsoft_azure_sql_database_2.configuration.show_coll_type = False
microsoft_azure_sql_database_2.configuration.show_part_type = True
microsoft_azure_sql_database_2.configuration.show_sort_options = False
microsoft_azure_sql_database_2.configuration.table_name = "target_table"

# Graph
link_1 = microsoft_azure_sql_database_1.connect_output_to(transformer_1)
link_1.name = "Link_1"
microsoft_azure_sql_database_1_schema = link_1.create_schema()
microsoft_azure_sql_database_1_schema.add_field("DECIMAL", "my_decimal", length=10, precision=10)
microsoft_azure_sql_database_1_schema.add_field("VARCHAR", "my_varchar", length=100)
microsoft_azure_sql_database_1_schema.add_field("INTEGER", "my_int")
microsoft_azure_sql_database_1_schema.add_field("CHAR", "my_char", length=5)

link_2 = transformer_1.connect_output_to(filter_1)
link_2.name = "Link_2"
transformer_1_schema = link_2.create_schema()
transformer_1_schema.add_field("DECIMAL", "my_decimal", source="Link_1.my_decimal", length=10, precision=10)
transformer_1_schema.add_field("VARCHAR", "my_varchar", source="Link_1.my_varchar", length=100)
transformer_1_schema.add_field("INTEGER", "my_int", source="Link_1.my_int")
transformer_1_schema.add_field("CHAR", "my_char", source="Link_1.my_char", length=5)
transformer_1_schema.add_field("DECIMAL", "my_decimal_2", length=10, precision=10, derivation="Link_1.my_decimal * 2")
transformer_1_schema.add_field("CHAR", "substring", length=100, derivation="Substrings1(Link_1.my_varchar, 0,5)")

link_3 = filter_1.connect_output_to(microsoft_azure_sql_database_2)
link_3.name = "Link_3"
filter_1_schema = link_3.create_schema()
filter_1_schema.add_field("DECIMAL", "my_decimal", source="Link_2.my_decimal", length=10, precision=10)
filter_1_schema.add_field("VARCHAR", "my_varchar", source="Link_2.my_varchar", length=100)
filter_1_schema.add_field("INTEGER", "my_int", source="Link_2.my_int")
filter_1_schema.add_field("CHAR", "my_char", source="Link_2.my_char", length=5)
filter_1_schema.add_field("DECIMAL", "my_decimal_2", source="Link_2.my_decimal_2", length=10, precision=10)
filter_1_schema.add_field("CHAR", "substring", source="Link_2.substring", length=100)

project.update_flow(flow)

print(f"Flow '{flow.name}' created successfully!")
print(f"Flow ID: {flow.flow_id}")

azure_sql_transform_filter_example_job = project.create_job(name="azure_sql_transform_filter_example_job", flow=flow)

azure_sql_transform_filter_example_job_run = azure_sql_transform_filter_example_job.start(
    name="azure_sql_transform_filter_example_job_run", description=""
)
