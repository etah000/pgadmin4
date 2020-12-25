SELECT
    name as oid,
    name,
    alias_to as owner
FROM system.functions
ORDER BY name ASC;
