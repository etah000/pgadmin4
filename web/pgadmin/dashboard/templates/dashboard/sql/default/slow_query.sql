SELECT
    user,
    client_hostname AS host,
    client_name AS client,
    query_start_time AS started,
    query_duration_ms / 1000 AS sec,
    round(memory_usage / 1048576) AS MEM_MB,
    result_rows,
    result_bytes / 1048576 AS RES_MB,
    read_rows,
    round(read_bytes / 1048576) AS R_MB,
    written_rows,
    round(written_bytes / 1048576) AS W_MB,
    query
FROM system.query_log
WHERE type = 2
AND query_start_time > subtractDays(now(),7)
ORDER BY query_duration_ms DESC, query_start_time DESC
LIMIT 50
