User request:
Please create a batch flow in my project "my-test-project" in the Dallas Region. This flow should pull from my azure sql database defined in my connection "azure-sql-conn" from my table "my_schema.my_table" which has the following columns:

- my_decimal: DECIMAL(10, 10)
- my_varchar: VARCHAR(100)
- my_int: INTEGER
- my_char: CHAR(5)

I would like to transform this data which will result in the following dataset:

- my_decimal: DECIMAL(10, 10)
- my_varchar: VARCHAR(100)
- my_int: INTEGER
- my_char: CHAR(5)
- my_decimal_2: my_decimal * 2
- substring: Substrings1(my_varchar, 0,5)

After this I would like to filter the data and remove all data where my_decimal_2 <= 10. After filtering I would like to load the resulting data back into my azure sql database, this time into table "my_schema.target_table".

Output:
```
from ibm_watsonx_data_integration.common.auth import IAMAuthenticator
from ibm_watsonx_data_integration.platform import Platform
from ibm_watsonx_data_integration.services.datastage import *

auth = IAMAuthenticator(api_key=os.getenv('WATSONX_API_KEY'))
platform = Platform(auth=auth, base_api_url='https://api.dataplatform.cloud.ibm.com')


project = platform.projects.get(name="my-test-project")

flow = project.create_flow(name="azure_sql_transform_filter_example", environment=None, flow_type="batch")

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

azure_sql_transform_filter_example_job = project.create_job(name="azure_sql_transform_filter_example_job", flow=flow)

azure_sql_transform_filter_example_job_run = azure_sql_transform_filter_example_job.start(
    name="azure_sql_transform_filter_example_job_run", description=""
)
```
