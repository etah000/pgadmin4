SELECT database,
       table,
       is_leader,
       total_replicas,
       active_replicas,
       is_readonly,
       is_session_expired,
       future_parts,
       parts_to_check,
       queue_size,
       inserts_in_queue
  FROM system.replicas
 WHERE is_readonly
    OR is_session_expired
    OR future_parts > 30
    OR parts_to_check > 20
    OR queue_size > 30
    OR inserts_in_queue > 20
    OR log_max_index - log_pointer > 20
    OR total_replicas < 2
    OR active_replicas < total_replicas;
