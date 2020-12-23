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
    '' AS security_barrier
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