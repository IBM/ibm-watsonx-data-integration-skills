# Minimal Full-Pushdown Example

Input plan: `examples/minimal_full_pushdown.substrait.json`.

Extracted fields:

- `connection_id = "00000000-0000-0000-0000-000000000000"` in the example. This is a
  placeholder; the user must supply the matching `connection_name`.
- `relations[0].root.names = ["customer_id", "customer_name", "total_orders"]`.
- `baseSchema.struct.types = [i32 REQUIRED, varchar(100) NULLABLE, i64 REQUIRED]`.
- `sqlStatement` is a single `SELECT ... LEFT JOIN ... GROUP BY`; its rows feed the
  Sequential file sink directly.

Expected fill block, assuming `connection_name = "pg_demo"` and
`output_file = "customer_orders.csv"` (a flat filename — the Sequential file writer
does not create parent directories):

```python
# Stage definition
conn_postgresql_ibmcloud_0 = cast(Connection, project.connections.get(name="pg_demo"))
postgresql_ibmcloud_0 = flow.add_stage(type = "IBM Cloud Databases for PostgreSQL", label = "postgresql_ibmcloud_0")
postgresql_ibmcloud_0.use_connection(conn_postgresql_ibmcloud_0)
postgresql_ibmcloud_0.configuration.execution_mode = POSTGRESQL_IBMCLOUD.ExecutionMode.seq
postgresql_ibmcloud_0.configuration.read_method = POSTGRESQL_IBMCLOUD.ReadMethod.select
postgresql_ibmcloud_0.configuration.select_statement = "SELECT c.customer_id, c.customer_name, COUNT(o.order_id) AS total_orders FROM public.customer c LEFT JOIN public.orders o ON c.customer_id = o.customer_id GROUP BY c.customer_id, c.customer_name"

sequentialfile_0 = flow.add_stage(type = "Sequential file", label = "sequentialfile_0")
sequentialfile_0.configuration.file_update_mode = SEQUENTIALFILE.AppendOverwrite.overwrite
sequentialfile_0.configuration.final_delimiter = SEQUENTIALFILE.FinalDelimiter.end
sequentialfile_0.configuration.file = ["customer_orders.csv"]
sequentialfile_0.configuration.first_line_is_column_names = SEQUENTIALFILE.FirstLineColumnNames.true
sequentialfile_0.configuration.delimiter = SEQUENTIALFILE.Delimiter.comma
sequentialfile_0.configuration.null_field_value = "NULL"
sequentialfile_0.configuration.create_data_asset = True
sequentialfile_0.configuration.data_asset_name = "customer_orders"

# Flow graph
link_1 = postgresql_ibmcloud_0.connect_output_to(sequentialfile_0)
link_1.name = "Link_1"
schema_postgresql_ibmcloud_0 = link_1.create_schema()

# Schema definition
schema_postgresql_ibmcloud_0.add_field("INTEGER", "customer_id")
schema_postgresql_ibmcloud_0.add_field("VARCHAR", "customer_name", nullable=True, length=100)
schema_postgresql_ibmcloud_0.add_field("BIGINT", "total_orders")
```

Notes:

- `i32 REQUIRED` maps to `INTEGER` with no `nullable` argument.
- `varchar(100) NULLABLE` maps to `VARCHAR` with `nullable=True, length=100`.
- `i64 REQUIRED` maps to `BIGINT` with no `nullable` argument.
- Single-statement SELECT can use a normal quoted string. Multi-statement SQL blocks
  must use triple quotes to preserve embedded newlines.
- Verify the user's PostgreSQL connector variant. Other PostgreSQL connectors have
  different labels/enums, such as `PostgreSQL` / `POSTGRESQL` versus
  `IBM Cloud Databases for PostgreSQL` / `POSTGRESQL_IBMCLOUD`.
