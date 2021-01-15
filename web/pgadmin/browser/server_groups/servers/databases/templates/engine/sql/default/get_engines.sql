SELECT DISTINCT
    name AS label,
    name AS value,
    supports_settings,
    supports_skipping_indices,
    supports_sort_order,
    supports_ttl,
    supports_replication,
    supports_deduplication
FROM
    system.table_engines
