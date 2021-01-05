SELECT 
    replica_num AS oid,
    replica_num as name,
    0 AS triggercount,
    0 AS has_enable_triggers,
    0 AS is_inherits,
    0 AS is_inherited,
    cluster,
    shard_num,
    shard_weight,
    replica_num,
    host_name,
    host_address,
    port,
    is_local,
    user,
    default_database,
    errors_count,
    estimated_recovery_time
FROM system.clusters
WHERE 
    cluster = '{{ did }}' 
    {% if scid %} AND shard_num = {{ scid }} {% endif %}
    {% if tid %} AND replica_num = {{ tid }} {% endif %}
