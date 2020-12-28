{### SQL to fetch tablespace object properties ###}
SELECT
    name AS oid,
    name,
    path AS location,
    '' AS spcoptions,
    'default' AS spcuser,
    type AS  type,
    '' as acl
FROM system.disks
{% if tsid %} WHERE name = '{{ tsid }}' {% endif %}
;

