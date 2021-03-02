{# SELECT DISTINCT #}
{#     cluster AS did,  #}
{#     cluster AS oid,  #}
{#     cluster AS name,  #}
{#     0 AS spcoid, #}
{#     'public' AS spcname,  #}
{#     1 AS datallowconn,  #}
{#     'utf-8' AS encoding, #}
{#     user AS datowner, #}
{#     '' AS datcollate, #}
{#     '' AS datctype, #}
{#     0 AS datconnlimit, #}
{#     1 AS cancreate, #}
{#     'public' AS default_tablespace, #}
{#     '' AS comments, #}
{#     0 AS is_template, #}
{#     '' AS tblacl, #}
{#     '' AS seqacl, #}
{#     '' AS funcacl, #}
{#     '' AS acl #}
{# FROM  #}
{#     (SELECT DISTINCT cluster,user  FROM system.clusters) #}
{# {% if did %} WHERE cluster = '{{ did }}' {% endif %} #}
{# ORDER BY cluster; #}

SELECT
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
    '' AS acl,
    toString(groupArray(host_name)) host_name,
    toString(groupArray(host_address)) host_address,
    toString(groupArray(port)) port,
    toString(groupArray(shard_num)) shard_num,
    toString(groupArray(shard_weight)) shard_weight
FROM
(SELECT DISTINCT cluster,user,host_name,host_address,port,shard_num,shard_weight FROM system.clusters)
{% if did %} WHERE cluster = '{{ did }}' {% endif %}
 group  by cluster,user

