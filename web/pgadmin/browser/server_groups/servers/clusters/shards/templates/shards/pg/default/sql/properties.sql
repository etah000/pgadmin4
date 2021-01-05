{% import 'catalog/pg/macros/catalogs.sql' as CATALOGS %}
SELECT DISTINCT
    3 AS nsptyp,
    shard_num AS name,
    shard_num AS oid,
    '' AS acl,
    'default' AS namespaceowner, 
    '' AS description,
    1 AS can_create,
    '' AS tblacl,
    '' AS seqacl,
    '' AS funcacl,
    '' AS seclabels,
    shard_weight,
    user
FROM
    system.clusters
WHERE 1
{% if did %}
    AND cluster = '{{did}}'
{% endif %} 

