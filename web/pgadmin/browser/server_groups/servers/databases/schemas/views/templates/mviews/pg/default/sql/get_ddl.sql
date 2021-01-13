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
    AND engine in ('MaterializedView')
{% if vid %}    AND name = '{{ vid }}' {% endif %}
ORDER BY name;
