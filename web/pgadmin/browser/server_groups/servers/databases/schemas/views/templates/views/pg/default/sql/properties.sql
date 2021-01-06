{# ========================== Fetch View Properties ========================= #}
SELECT
    name AS oid,
    '0' AS xmin,
    0 AS relkind,
    '' AS comment,
    'public' AS spcname,
    name AS name,
    0 AS spcoid,
    'public' AS schema,
    0 AS ispopulated,
    'default' AS owner,
    '' AS acl,
    create_table_query AS definition,
    0 AS system_view,
    array() AS seclabels,
    '' AS check_option,
    '' AS security_barrier,
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
FROM system.tables
WHERE engine in ('View','LiveView')
{% if did %}
    AND database = '{{did}}'
{% endif %}
{% if (vid and datlastsysoid) %}
    AND name = '{{vid}}'
{% endif %}
ORDER BY
    name