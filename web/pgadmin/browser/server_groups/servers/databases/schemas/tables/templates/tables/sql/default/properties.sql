SELECT
    NULL AS autovacuum_analyze_scale_factor,
    NULL AS autovacuum_analyze_threshold,
    NULL AS autovacuum_enabled,
    NULL AS autovacuum_freeze_max_age,
    NULL AS autovacuum_freeze_min_age,
    NULL AS autovacuum_freeze_table_age,
    NULL AS autovacuum_vacuum_cost_delay,
    NULL AS autovacuum_vacuum_cost_limit,
    NULL AS autovacuum_vacuum_scale_factor,
    NULL AS autovacuum_vacuum_threshold,
    dependencies_table AS coll_inherits,
    NULL AS conkey,
    NULL AS conname,
    NULL AS description,
    NULL AS fillfactor,
    0 AS hastoasttable,
    '0' AS inherited_tables_cnt,
    if (database='system',1,0) AS is_sys_table,
    0 AS isrepl,
    name,
    name AS oid,
    NULL AS relacl_str,
    0 AS relhasoids,
    0 AS relhassubclass,
    0 AS reloftype,
    NULL AS reloptions,
    'default' AS relowner,
    0 AS relpersistence,
    '0' AS reltuples,
    'public' AS schema,
    NULL AS seclabels,
    'public' AS spcname,
    0 AS spcoid,
    NULL AS toast_autovacuum_analyze_scale_factor,
    NULL AS toast_autovacuum_analyze_threshold,
    NULL AS toast_autovacuum_enabled,
    NULL AS toast_autovacuum_freeze_max_age,
    NULL AS toast_autovacuum_freeze_min_age,
    NULL AS toast_autovacuum_freeze_table_age,
    NULL AS toast_autovacuum_vacuum_cost_delay,
    NULL AS toast_autovacuum_vacuum_cost_limit,
    NULL AS toast_autovacuum_vacuum_scale_factor,
    NULL AS toast_autovacuum_vacuum_threshold,
    NULL AS toast_reloptions,
    '0' AS triggercount,
    NULL AS typname,
    NULL AS typoid,
    database,
    uuid,
    engine,
    engine as p_engine,
    is_temporary,
    data_paths,
    metadata_path,
    metadata_modification_time,
    dependencies_database,
    dependencies_table,
    create_table_query,
    engine_full,
    partition_key,
    sorting_key,
    primary_key as primarykey,
    sampling_key,
    storage_policy,
    total_rows,
    total_bytes,
    lifetime_rows,
    lifetime_bytes
FROM
   system.tables
WHERE
    database = '{{ did }}'
    AND name NOT LIKE '.%'
    AND engine NOT LIKE '%View'
    {% if tid %} AND name = '{{ tid }}' {% endif %}
ORDER BY name
