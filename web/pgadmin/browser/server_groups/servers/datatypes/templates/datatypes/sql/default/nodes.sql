SELECT
    name as oid,
    name,
    case_insensitive as owner
FROM system.data_type_families
ORDER BY name ASC;

