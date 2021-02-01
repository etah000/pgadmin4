SELECT
    query_id as pid,
    memory_usage,
    address,
    read_rows,
    elapsed,
    read_bytes,
    query,
    user as usename
FROM system.processes
ORDER BY query_id ASC;
