SELECT DISTINCT
    cluster AS did, 
    cluster AS oid, 
    cluster AS name, 
    0 AS spcoid,
    'public' AS spcname, 
    1 AS datallowconn, 
    'utf-8' AS encoding,
    user AS datowner,
    '' AS datcollate,
    '' AS datctype,
    0 AS datconnlimit,
    1 AS cancreate,
    'public' AS default_tablespace,
    '' AS comments,
    0 AS is_template,
    '' AS tblacl,
    '' AS seqacl,
    '' AS funcacl,
    '' AS acl
FROM 
    (SELECT DISTINCT cluster,user  FROM system.clusters)
{% if did %} WHERE cluster = '{{ did }}' {% endif %}
ORDER BY cluster;