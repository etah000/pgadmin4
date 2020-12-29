{% import 'catalog/pg/macros/catalogs.sql' as CATALOGS %}
SELECT DISTINCT
    shard_num AS oid,
    shard_num as name,
    1 as can_create,
    1 as has_usage
FROM
    system.clusters
WHERE 1
{% if did %}
    AND cluster = '{{did}}'
{% endif %}    
{% if scid %}
    AND shard_num = {{scid}}
{% endif %}    

