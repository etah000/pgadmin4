{### SQL to fetch dictionary object properties ###}
SELECT
    name,
    status,
    origin,
    type,
    key,
    source,
    attribute.names as attribute_names,
    attribute.types as attribute_types,
    bytes_allocated,
    element_count
FROM system.dictionaries
{% if dcid %} WHERE name = '{{ dcid }}' {% endif %}
ORDER BY name ASC;
