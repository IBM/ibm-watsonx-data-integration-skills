from ibm_watsonx_data_integration.common.auth import IAMAuthenticator
from ibm_watsonx_data_integration.platform import Platform
from ibm_watsonx_data_integration.services.datastage import DB2
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
flow_name = "copy_to_many"
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
db2_conn = project.connections.get(name="db2-conn")

# Stages
ibm_db2_1 = flow.add_stage("IBM Db2", "IBM_Db2_1")
ibm_db2_1.use_connection(db2_conn)
ibm_db2_1.configuration.runtime_column_propagation = False
ibm_db2_1.configuration.schema_name = "my_db2_schema"
ibm_db2_1.configuration.table_name = "my_db2_table"

copy_1 = flow.add_stage("Copy", "Copy_1")

copy_1.configuration.runtime_column_propagation = False

ibm_db2_2 = flow.add_stage("IBM Db2", "IBM_Db2_2")
ibm_db2_2.use_connection(db2_conn)
ibm_db2_2.configuration.column_metadata_change_propagation = False
ibm_db2_2.configuration.output_acp_should_hide = False
ibm_db2_2.configuration.schema_name = "my_db2_schema"
ibm_db2_2.configuration.show_coll_type = False
ibm_db2_2.configuration.show_part_type = True
ibm_db2_2.configuration.show_sort_options = False
ibm_db2_2.configuration.table_action = DB2.TableAction.replace
ibm_db2_2.configuration.table_name = "backup_table"

peek_1 = flow.add_stage("Peek", "Peek_1")

# Graph
link_1 = ibm_db2_1.connect_output_to(copy_1)
link_1.name = "Link_1"
ibm_db2_1_schema = link_1.create_schema()
ibm_db2_1_schema.add_field("BIGINT", "my_bigint")

link_2 = copy_1.connect_output_to(ibm_db2_2)
link_2.name = "Link_2"
copy_1_schema = link_2.create_schema()
copy_1_schema.add_field("BIGINT", "my_bigint", source="Link_1.my_bigint")

link_3 = copy_1.connect_output_to(peek_1)
link_3.name = "Link_3"
copy_1_schema_2 = link_3.create_schema()
copy_1_schema_2.add_field("BIGINT", "my_bigint", source="Link_1.my_bigint")

project.update_flow(flow)

print(f"Flow '{flow.name}' created successfully!")
print(f"Flow ID: {flow.flow_id}")
