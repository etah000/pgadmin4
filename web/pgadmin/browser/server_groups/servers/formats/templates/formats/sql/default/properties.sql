{### SQL to fetch tablespace object properties ###}
SELECT
    name AS oid,
    name,
    '' AS spclocation,
    '' AS spcoptions,
    is_input AS is_input,
    is_output AS  is_output,
    '' as acl
FROM system.formats
{% if fsid %} WHERE name = '{{ fsid }}' {% endif %}
order by name;

