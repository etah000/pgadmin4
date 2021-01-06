{# ========================== Fetch Materialized View Properties ========================= #}
SELECT
    name AS oid,
    '0' AS xmin,
    name AS name,
    0 AS spcoid,
    0 AS with_data,
    'public' AS spcname,
    '' AS acl,
    'public' as schema,
    'default' AS owner,
    '' AS comment,
    create_table_query AS definition,
    0 AS system_view,
    '' AS acl,
    '' AS seclabels,
    '' AS fillfactor,
    0 AS autovacuum_enabled,
    '' AS autovacuum_vacuum_threshold,
    '' AS autovacuum_vacuum_scale_factor,
    '' AS autovacuum_analyze_threshold,
    '' AS autovacuum_analyze_scale_factor,
    '' AS autovacuum_vacuum_cost_delay,
    '' AS autovacuum_vacuum_cost_limit,
    '' AS autovacuum_freeze_min_age,
    '' AS autovacuum_freeze_max_age,
    '' AS autovacuum_freeze_table_age,
    0 AS toast_autovacuum_enabled,
    '' AS toast_autovacuum_vacuum_threshold,
    '' AS toast_autovacuum_vacuum_scale_factor,
    '' AS toast_autovacuum_analyze_threshold,
    '' AS toast_autovacuum_analyze_scale_factor,
    '' AS toast_autovacuum_vacuum_cost_delay,
    '' AS toast_autovacuum_vacuum_cost_limit,
    '' AS toast_autovacuum_freeze_min_age,
    '' AS toast_autovacuum_freeze_max_age,
    '' AS toast_autovacuum_freeze_table_age,
    '' AS reloptions,
    array() AS toast_reloptions,
    0 AS hastoasttable,
    database,
    uuid,
    engine,
    is_temporary,
    data_paths,
    metadata_path,
    metadata_modification_time,
    dependencies_database,
    dependencies_table,
    engine_full,
    partition_key,
    sorting_key,
    primary_key,
    sampling_key,
    storage_policy,
    total_rows,
    total_bytes,
    lifetime_rows,
    lifetime_bytes
FROM
    system.tables
WHERE
    engine in ('MaterializedView')
{% if did %}
    AND database = '{{did}}'
{% endif %}
{% if (vid and datlastsysoid) %}
    AND name = '{{vid}}'
{% endif %}
ORDER BY
    name
