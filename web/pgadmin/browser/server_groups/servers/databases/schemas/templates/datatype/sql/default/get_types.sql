SELECT 
    name AS typname,
    name AS elemoid,
    -1 AS typlen,
    'b' AS typtype,
    name AS oid,
    'pg_catalog' AS nspname,
    alias_to AS isdup,
    0 AS is_collatable
FROM
    system.data_type_families
WHERE 
    alias_to = '' 
    AND name not in ('AggregateFunction','Array','LowCardinality','MultiPolygon','Nested','Nothing','Nullable','Point','Polygon','Ring','SimpleAggregateFunction','Tuple')
    AND name not like 'Interval%'