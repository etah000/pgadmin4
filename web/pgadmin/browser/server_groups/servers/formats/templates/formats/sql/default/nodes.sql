SELECT
    name as oid,
    name,
    is_input as owner
FROM system.formats
ORDER BY name ASC;
