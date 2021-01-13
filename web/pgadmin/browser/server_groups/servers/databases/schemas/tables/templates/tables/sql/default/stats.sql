select
       t.database,
       t.name,
       t.total_rows,
       t.total_bytes
from system.tables t
WHERE
    database = '{{ did }}'
    AND name NOT LIKE '.%'
    AND engine NOT LIKE '%View'
{% if tid %}  AND name = '{{ tid }}' {% endif %}
ORDER BY name
