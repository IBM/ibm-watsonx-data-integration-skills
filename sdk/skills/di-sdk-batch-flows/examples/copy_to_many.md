User request:
Please create a batch flow in my project "my-test-project" in the Dallas Region. This flow should pull from my db2 database defined in my connection "db2-conn" from my table "my_db2_schema.my_table" which has the following columns:

- my_bigint: BIGINT

I would like to create a backup of this data in "my_db2_schema.my_table_backup" and at the same time copy this data over to a peek so when I run the flow I can see what data is being backed up.

Output:
```
from ibm_watsonx_data_integration.common.auth import IAMAuthenticator
from ibm_watsonx_data_integration.platform import Platform
from ibm_watsonx_data_integration.services.datastage import *
import os

auth = IAMAuthenticator(api_key=os.getenv('WATSONX_API_KEY'))
platform = Platform(auth=auth, base_api_url='https://api.dataplatform.cloud.ibm.com')

project = platform.projects.get(name="my-test-project")

flow = project.create_flow(name="copy_to_many", environment=None, flow_type="batch")

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

copy_to_many_job = project.create_job(name="copy_to_many_job", flow=flow)

copy_to_many_job_run = copy_to_many_job.start(name="copy_to_many_job_run", description="")

```
