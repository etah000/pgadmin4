{### SQL to fetch datatype object properties ###}
SELECT
    name AS oid,
    name,
    '' AS spclocation,
    '' AS spcoptions,
    case_insensitive AS case_insensitive,
    alias_to AS  alias_to,
    '' as acl
FROM system.data_type_families
{% if dtid %} WHERE name = '{{ dtid }}' {% endif %}
order by name;

