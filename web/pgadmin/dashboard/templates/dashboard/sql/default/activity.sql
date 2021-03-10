SELECT
    --snowAdmin process
    query_id as pid,
    memory_usage,
    address,
    read_rows,
    elapsed,
    read_bytes,
    query,
    user as usename
FROM system.processes
where query not like '%--snowAdmin process%'
ORDER BY query_id ASC;
