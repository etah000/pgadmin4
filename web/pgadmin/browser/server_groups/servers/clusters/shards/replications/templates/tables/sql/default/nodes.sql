SELECT 
    name AS oid,
    name,
    0 AS triggercount,
    0 AS has_enable_triggers,
    0 AS is_inherits,
    0 AS is_inherited
FROM system.tables
WHERE 
    database = '{{ did }}' 
    AND name NOT LIKE '.%'
    AND engine NOT LIKE '%View'
{% if tid %}    AND name = '{{ tid }}' {% endif %}
ORDER BY name;
