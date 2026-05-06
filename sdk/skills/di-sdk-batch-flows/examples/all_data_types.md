User request:
Please create a batch flow in my project "my-test-project" in the Dallas Region. I would like to create a flow that demonstrates how to use all of the data types using a simple rowgen -> peek.

Output:
```
from ibm_watsonx_data_integration.common.auth import IAMAuthenticator
from ibm_watsonx_data_integration.platform import Platform
from ibm_watsonx_data_integration.services.datastage import *
import os

auth = IAMAuthenticator(api_key=os.getenv('WATSONX_API_KEY'))
platform = Platform(auth=auth, base_api_url='https://api.dataplatform.cloud.ibm.com')

project = platform.projects.get(name="my-test-project")

flow = project.create_flow(name="all_data_types_example", environment=None, flow_type="batch")

# Stages
row_generator_1 = flow.add_stage("Row Generator", "Row_Generator_1")

row_generator_1.configuration.runtime_column_propagation = False

peek_1 = flow.add_stage("Peek", "Peek_1")

peek_1.configuration.runtime_column_propagation = False

# Graph
link_1 = row_generator_1.connect_output_to(peek_1)
link_1.name = "Link_1"
row_generator_1_schema = link_1.create_schema()
row_generator_1_schema.add_field("BIGINT", "COLUMN_1")
row_generator_1_schema.add_field("BINARY", "COLUMN_2", length=100)
row_generator_1_schema.add_field("BIT", "COLUMN_3")
row_generator_1_schema.add_field("CHAR", "COLUMN_4", length=100)
row_generator_1_schema.add_field("DATE", "COLUMN_5")
row_generator_1_schema.add_field("DECIMAL", "COLUMN_6", length=100)
row_generator_1_schema.add_field("DOUBLE", "COLUMN_7")
row_generator_1_schema.add_field("FLOAT", "COLUMN_8")
row_generator_1_schema.add_field("INTEGER", "COLUMN_9")
row_generator_1_schema.add_field("LONGNVARCHAR", "COLUMN_10", length=100)
row_generator_1_schema.add_field("LONGVARBINARY", "COLUMN_11", length=100)
row_generator_1_schema.add_field("LONGVARCHAR", "COLUMN_12", length=100)
row_generator_1_schema.add_field("NCHAR", "COLUMN_13", length=100)
row_generator_1_schema.add_field("NUMERIC", "COLUMN_14", length=100)
row_generator_1_schema.add_field("NVARCHAR", "COLUMN_15", length=100)
row_generator_1_schema.add_field("REAL", "COLUMN_16", length=100)
row_generator_1_schema.add_field("SMALLINT", "COLUMN_17")
row_generator_1_schema.add_field("TIME", "COLUMN_18", length=8)
row_generator_1_schema.add_field("TIMESTAMP", "COLUMN_19", length=19)
row_generator_1_schema.add_field("TINYINT", "COLUMN_20")
row_generator_1_schema.add_field("UNKNOWN", "COLUMN_21", length=100)
row_generator_1_schema.add_field("VARBINARY", "COLUMN_22", length=100)
row_generator_1_schema.add_field("VARCHAR", "COLUMN_23", length=100)


project.update_flow(flow)


all_data_types_job = project.create_job(name="all_data_types_job", flow=flow)


all_data_types_job_run = all_data_types_job.start(name="all_data_types_job_run", description="")
