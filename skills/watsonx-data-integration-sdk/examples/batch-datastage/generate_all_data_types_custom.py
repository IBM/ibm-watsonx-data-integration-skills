from ibm_watsonx_data_integration.common.auth import IAMAuthenticator
from ibm_watsonx_data_integration.platform import Platform
from ibm_watsonx_data_integration.services.datastage import ROW_GENERATOR, PEEK, FIELD
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
flow_name = "All_Data_Types_Custom_Generation"
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

# Add Row Generator stage - generates 100 records
row_generator = flow.add_stage("Row Generator", "Row_Generator_All_Types")
row_generator.configuration.records = 100
row_generator.configuration.runtime_column_propagation = False
row_generator.configuration.execmode = ROW_GENERATOR.Execmode.par

# Add Peek stage to view the generated data
peek = flow.add_stage("Peek", "Peek_All_Types")
peek.configuration.dataset = PEEK.Dataset.false
peek.configuration.all = PEEK.All.false
peek.configuration.nrecs = 50
peek.configuration.runtime_column_propagation = False
peek.configuration.execmode = PEEK.Execmode.seq

# Create link between stages
link = row_generator.connect_output_to(peek)
link.name = "Link_Generator_To_Peek"

# Create schema with all data types using different generation patterns
schema = link.create_schema()

# ============================================================================
# INTEGER TYPES - Demonstrating cycle, random patterns
# ============================================================================

# BIGINT with cycle generation
schema.add_field(
    "BIGINT",
    "BIGINT_CYCLE",
    generate_type=FIELD.GenerateType.cycle,
    cycle_initial_value=1000000,
    cycle_increment=100000,
    cycle_limit=5000000
)

# BIGINT with random generation
schema.add_field(
    "BIGINT",
    "BIGINT_RANDOM",
    generate_type=FIELD.GenerateType.random,
    random_seed=1,
    random_limit=9999999999
)

# INTEGER with cycle generation
schema.add_field(
    "INTEGER",
    "INTEGER_CYCLE",
    generate_type=FIELD.GenerateType.cycle,
    cycle_initial_value=1,
    cycle_increment=1,
    cycle_limit=10
)

# INTEGER with random generation
schema.add_field(
    "INTEGER",
    "INTEGER_RANDOM",
    generate_type=FIELD.GenerateType.random,
    random_seed=1,
    random_limit=1000
)

# SMALLINT with cycle
schema.add_field(
    "SMALLINT",
    "SMALLINT_CYCLE",
    generate_type=FIELD.GenerateType.cycle,
    cycle_initial_value=1,
    cycle_increment=10,
    cycle_limit=100
)

# SMALLINT with random
schema.add_field(
    "SMALLINT",
    "SMALLINT_RANDOM",
    generate_type=FIELD.GenerateType.random,
    random_seed=1,
    random_limit=100
)

# TINYINT with cycle
schema.add_field(
    "TINYINT",
    "TINYINT_CYCLE",
    generate_type=FIELD.GenerateType.cycle,
    cycle_initial_value=0,
    cycle_increment=5,
    cycle_limit=50
)

# TINYINT with random
schema.add_field(
    "TINYINT",
    "TINYINT_RANDOM",
    generate_type=FIELD.GenerateType.random,
    random_seed=0,
    random_limit=255
)

# ============================================================================
# DECIMAL/NUMERIC TYPES - Demonstrating cycle and random with precision
# ============================================================================

# DECIMAL with cycle
schema.add_field(
    "DECIMAL",
    "DECIMAL_CYCLE",
    length=10,
    precision=10,
    scale=2,
    generate_type=FIELD.GenerateType.cycle,
    cycle_initial_value=100.50,
    cycle_increment=25.25,
    cycle_limit=500.00
)

# DECIMAL with random
schema.add_field(
    "DECIMAL",
    "DECIMAL_RANDOM",
    length=8,
    precision=8,
    scale=2,
    generate_type=FIELD.GenerateType.random,
    random_seed=0.01,
    random_limit=999.99
)

# NUMERIC with cycle
schema.add_field(
    "NUMERIC",
    "NUMERIC_CYCLE",
    length=6,
    scale=1,
    generate_type=FIELD.GenerateType.cycle,
    cycle_initial_value=10.0,
    cycle_increment=5.5,
    cycle_limit=100.0
)

# NUMERIC with random
schema.add_field(
    "NUMERIC",
    "NUMERIC_RANDOM",
    length=8,
    scale=3,
    generate_type=FIELD.GenerateType.random,
    random_seed=1.0,
    random_limit=9999.999
)

# ============================================================================
# FLOATING POINT TYPES - Random generation
# ============================================================================

# DOUBLE with random
schema.add_field(
    "DOUBLE",
    "DOUBLE_RANDOM",
    generate_type=FIELD.GenerateType.random,
    random_seed=0.0,
    random_limit=10000.0
)

# FLOAT with random
schema.add_field(
    "FLOAT",
    "FLOAT_RANDOM",
    generate_type=FIELD.GenerateType.random,
    random_seed=0.0,
    random_limit=1000.0
)

# REAL with random
schema.add_field(
    "REAL",
    "REAL_RANDOM",
    generate_type=FIELD.GenerateType.random,
    random_seed=0.0,
    random_limit=100.0
)

# ============================================================================
# STRING TYPES - Demonstrating cycle with string values and alphabet
# ============================================================================

# VARCHAR with cycle through predefined values
schema.add_field(
    "VARCHAR",
    "VARCHAR_CYCLE_VALUES",
    length=50,
    generate_algorithm=FIELD.GenerateAlgorithm.cycle,
    cycle_values=["Alpha", "Beta", "Gamma", "Delta", "Epsilon"]
)

# VARCHAR with alphabet generation
schema.add_field(
    "VARCHAR",
    "VARCHAR_ALPHABET",
    length=20,
    generate_algorithm=FIELD.GenerateAlgorithm.alphabet
)

# VARCHAR with random (default generation)
schema.add_field(
    "VARCHAR",
    "VARCHAR_DEFAULT",
    length=100
)

# CHAR with cycle through department names
schema.add_field(
    "CHAR",
    "CHAR_DEPT_CYCLE",
    length=30,
    generate_algorithm=FIELD.GenerateAlgorithm.cycle,
    cycle_values=["Sales", "Marketing", "Engineering", "HR", "Finance"]
)

# CHAR with alphabet
schema.add_field(
    "CHAR",
    "CHAR_ALPHABET",
    length=15,
    generate_algorithm=FIELD.GenerateAlgorithm.alphabet
)

# CHAR with default generation
schema.add_field(
    "CHAR",
    "CHAR_DEFAULT",
    length=50
)

# NVARCHAR with cycle
schema.add_field(
    "NVARCHAR",
    "NVARCHAR_CYCLE",
    length=40,
    generate_algorithm=FIELD.GenerateAlgorithm.cycle,
    cycle_values=["Product_A", "Product_B", "Product_C", "Product_D"]
)

# NVARCHAR with alphabet
schema.add_field(
    "NVARCHAR",
    "NVARCHAR_ALPHABET",
    length=30,
    generate_algorithm=FIELD.GenerateAlgorithm.alphabet
)

# NVARCHAR with default generation
schema.add_field(
    "NVARCHAR",
    "NVARCHAR_DEFAULT",
    length=100
)

# NCHAR with cycle
schema.add_field(
    "NCHAR",
    "NCHAR_STATUS_CYCLE",
    length=20,
    generate_algorithm=FIELD.GenerateAlgorithm.cycle,
    cycle_values=["Active", "Inactive", "Pending", "Archived"]
)

# NCHAR with alphabet
schema.add_field(
    "NCHAR",
    "NCHAR_ALPHABET",
    length=25,
    generate_algorithm=FIELD.GenerateAlgorithm.alphabet
)

# NCHAR with default generation
schema.add_field(
    "NCHAR",
    "NCHAR_DEFAULT",
    length=50
)

# LONGVARCHAR with alphabet
schema.add_field(
    "LONGVARCHAR",
    "LONGVARCHAR_ALPHABET",
    length=500,
    generate_algorithm=FIELD.GenerateAlgorithm.alphabet
)

# LONGVARCHAR with cycle
schema.add_field(
    "LONGVARCHAR",
    "LONGVARCHAR_CYCLE",
    length=500,
    generate_algorithm=FIELD.GenerateAlgorithm.cycle,
    cycle_values=["Description_One", "Description_Two", "Description_Three"]
)

# LONGVARCHAR with default generation
schema.add_field(
    "LONGVARCHAR",
    "LONGVARCHAR_DEFAULT",
    length=500
)

# LONGNVARCHAR with cycle
schema.add_field(
    "LONGNVARCHAR",
    "LONGNVARCHAR_CYCLE",
    length=500,
    generate_algorithm=FIELD.GenerateAlgorithm.cycle,
    cycle_values=["LongText_A", "LongText_B", "LongText_C"]
)

# LONGNVARCHAR with alphabet
schema.add_field(
    "LONGNVARCHAR",
    "LONGNVARCHAR_ALPHABET",
    length=500,
    generate_algorithm=FIELD.GenerateAlgorithm.alphabet,
    alphabet="wxyz"
)

# LONGNVARCHAR with default generation
schema.add_field(
    "LONGNVARCHAR",
    "LONGNVARCHAR_DEFAULT",
    length=500
)

# ============================================================================
# DATE/TIME TYPES - Basic generation (no custom patterns)
# ============================================================================

# DATE field
schema.add_field("DATE", "DATE_COL")

# TIME field
schema.add_field("TIME", "TIME_COL", length=8)

# TIMESTAMP field
schema.add_field("TIMESTAMP", "TIMESTAMP_COL", length=19)

# ============================================================================
# BINARY TYPES - Basic generation
# ============================================================================

# BINARY field
schema.add_field("BINARY", "BINARY_COL", length=100)

# VARBINARY field
schema.add_field("VARBINARY", "VARBINARY_COL", length=255)

# LONGVARBINARY field
schema.add_field("LONGVARBINARY", "LONGVARBINARY_COL", length=1000)

# ============================================================================
# OTHER TYPES
# ============================================================================

# BIT field
schema.add_field("BIT", "BIT_COL")

# UNKNOWN type field
schema.add_field("UNKNOWN", "UNKNOWN_COL", length=100)

# Update the flow in the project
project.update_flow(flow)

print(f"Flow '{flow.name}' created successfully!")
print(f"Flow ID: {flow.flow_id}")
