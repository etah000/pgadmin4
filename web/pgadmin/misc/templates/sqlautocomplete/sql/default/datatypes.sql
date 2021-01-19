{# SQL query for getting datatypes #}
SELECT d.name schema_name,
    t.name object_name
FROM system.data_type_families t, (SELECT name FROM system.databases) d
ORDER BY 1, 2;
