{### SQL to fetch dictionary object properties ###}
SELECT
    name,
    status,
    origin,
    type,
    key,
    source
FROM system.dictionaries
{% if dcid %} WHERE name = '{{ dcid }}' {% endif %}
ORDER BY name ASC;
