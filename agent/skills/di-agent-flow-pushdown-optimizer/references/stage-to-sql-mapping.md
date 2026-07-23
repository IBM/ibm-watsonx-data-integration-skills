# Stage-to-SQL Mapping Reference

## Supported stage translations

| DataStage stage | SQL equivalent |
|---|---|
| **Connector with custom SQL** | CTE: `WITH alias AS (…custom SQL…)` |
| **Connector reading a table** | CTE: `WITH alias AS (SELECT * FROM schema.table)` |
| **Join** | `LEFT JOIN` / `INNER JOIN` on the declared key columns |
| **Lookup** | `LEFT JOIN` (hash enrichment; treat same as Join) |
| **Transformer expressions** | Scalar SQL expressions (`COALESCE`, `CASE WHEN`, `ABS`, arithmetic, etc.) |
| **Transformer `stage_variables`** | Inline as SQL expressions or materialize as CTE columns |
| **Transformer proprietary functions** (e.g. `BitExpand`, `DateFromDaysSince`, `BitCompress`) | Look up exact semantics in `di-agent-knowledge-engine-datastage` (TransformerStageFunctions), then derive the target-dialect equivalent; flag any function with no safe equivalent |
| **Aggregator `selection=sum/mean/min/max`** | `GROUP BY keys` + the corresponding aggregate function |
| **Aggregator `selection=countField`** | `GROUP BY keys` + `COUNT(*) AS <countField>`; NULL groups included when `nul_res=true` |
| **Funnel** | `UNION ALL` (preserves duplicates); use `UNION` only if configured for distinct rows |
| **Remove Duplicates** | `SELECT DISTINCT` or `ROW_NUMBER() OVER (PARTITION BY … ORDER BY …) = 1` |
| **Modify** | Column rename/drop via `SELECT col AS new_name` |
| **Head** | `LIMIT n` |
| **Copy** | No-op — omit |
| **Sort** | `ORDER BY` |
| **Filter** | `WHERE` |

## Target connector write-mode prepend

Prepend the following statements before the `INSERT` in the workload SQL to match the
original write behaviour exactly. Always preserve this behaviour; do not silently omit
the truncate/delete.

| `table_action` | `write_mode` | Prepend before the INSERT |
|---|---|---|
| `replace` | any | `TRUNCATE TABLE <target>;` |
| `append` | `delete_insert` with key filter | `DELETE FROM <target> WHERE <key> IN (SELECT <key> FROM source_cte);` |
| `append` | `insert` | nothing — pure append |
| `create` | any | `CREATE TABLE IF NOT EXISTS <target> (…);` — flag for manual review |

## Stages that block full pushdown

If **any** of these appear as an intermediate stage, the flow cannot be fully converted to
SQL — classify as Partial Pushdown (not supported) or Not eligible and stop:

`Dataset`, `FileSet`, `Sequential File` (as source), `Switch`,
`SCD (Slowly Changing Dimension)`, `Change Capture`, `Change Apply`,
`External Filter`, `External Source`, `Hierarchical`, `XML Input/Output`,
`Buildop`, `Java Integration`, `Web Service`, `REST`, `HTTP`, `IBM MQ`,
`Apache Kafka`

## Mixed-mode stages (ELT with partial ETL fallback)

The following stages run in **Mixed mode** — flag these for manual review and note the
known limitations:

| Stage | Key limitations |
|---|---|
| **Aggregator** | Re-calculation and Summary aggregation types not supported |
| **Filter** | Predicates and job parameters in WHERE clause not supported |
| **Lookup** | Range lookup not supported; Fail mode not supported; function support varies by dialect (PostgreSQL/Snowflake have a reduced function set) |
| **Remove Duplicates** | Always case-sensitive; first/last duplicate retention not supported |
| **Sort** | Case-insensitive sorting not supported; stable sort ignored |
| **Transformer** | Loop variables, surrogate keys, and triggers not supported; several functions unsupported: `ForceError`, `GetEnvironment`, `GetNumOfPartitions`, `GetPartitionNum`, `GetSavedInputRecord`, `NextSKChain`, `NextSurrogateKey`, `PrevSKChain`, `PrintMessage`, `PrintWarning`, `SaveInputRecord`, `SendCustomInstanceReport`, `SetCustomMetadataInfo`, `SendCustomReport`, `SetCustomSummaryInfo`, `SetUserStatus` |

## Runtime parameters

Preserve DataStage runtime parameters (`#PARAM#`, `#PARAMSET.PARAM#`) verbatim in the
SQL — do not resolve them.
