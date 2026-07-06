INSERT INTO ${SCHEMA}.target_table (id, name, loaded_at)
SELECT id, name, current_timestamp()
FROM ${SCHEMA}.staging_table
WHERE load_dt = '${DATA_DT}';

COMMIT;
