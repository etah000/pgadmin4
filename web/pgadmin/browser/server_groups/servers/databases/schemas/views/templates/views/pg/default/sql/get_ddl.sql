SELECT
    database,
    name,
    engine_full,
    partition_key,
    primary_key,
    create_table_query
FROM system.tables
WHERE
    database = '{{ did }}'
    AND name NOT LIKE '.%'
    AND engine in ('View','LiveView')
{% if vid %}    AND name = '{{ vid }}' {% endif %}
ORDER BY name;
