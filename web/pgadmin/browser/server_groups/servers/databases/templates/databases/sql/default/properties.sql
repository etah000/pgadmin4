SELECT
    name AS did, 
    name AS oid, 
    name, 
    0 AS spcoid,
    'public' AS spcname, 
    1 AS datallowconn, 
    'utf-8' AS encoding,
    'default' AS datowner,
    '' AS datcollate,
    '' AS datctype,
    0 AS datconnlimit,
    1 AS cancreate,
    'public' AS default_tablespace,
    '' AS comments,
    0 AS is_template,
    {### Default ACL for Tables ###}
    '' AS tblacl,
    {### Default ACL for Sequnces ###}
    '' AS seqacl,
    {### Default ACL for Functions ###}
    '' AS funcacl,
    '' AS acl
FROM system.tables
WHERE {% if did %} database = '{{ did }}' {% endif %}
ORDER BY name;