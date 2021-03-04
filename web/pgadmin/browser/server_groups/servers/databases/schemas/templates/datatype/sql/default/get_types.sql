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
    AND name not in ('Enum8','Enum16','Enum','UInt256','Int256','Decimal256','Int128')
ORDER BY name