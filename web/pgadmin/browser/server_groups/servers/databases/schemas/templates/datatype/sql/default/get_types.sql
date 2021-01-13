SELECT 
    name AS typname,
    rowNumberInAllBlocks() AS elemoid,
    -1 AS typlen,
    'b' AS typtype,
    name AS oid,
    'pg_catalog' AS nspname,
    alias_to AS isdup,
    0 AS is_collatable
FROM
    system.data_type_families
WHERE alias_to = ''