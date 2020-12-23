SELECT
    name as oid,
    name,
    source as owner
FROM system.dictionaries
ORDER BY name ASC;
