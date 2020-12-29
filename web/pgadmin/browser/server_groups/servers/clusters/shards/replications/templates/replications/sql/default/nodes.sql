SELECT 
    replica_num AS oid,
    replica_num as name,
    0 AS triggercount,
    0 AS has_enable_triggers,
    0 AS is_inherits,
    0 AS is_inherited
FROM system.clusters
WHERE 
    cluster = '{{ did }}' 
    {% if scid %} AND shard_num = {{ scid }} {% endif %}
    {% if tid %} AND replica_num = {{ tid }} {% endif %}
