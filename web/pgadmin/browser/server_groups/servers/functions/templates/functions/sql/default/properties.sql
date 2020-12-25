{### SQL to fetch function object properties ###}
SELECT
    name,
    is_aggregate,
    case_insensitive,
    alias_to
FROM system.functions
{% if fcid %} WHERE name = '{{ fcid }}' {% endif %}
ORDER BY name ASC;
