{# ============= Fetch the list of tables/view based on given schema_names ============= #}
SELECT  database schema_name,
    name object_name
FROM system.tables
    WHERE database IN ({{schema_names}})
    ORDER BY 1,2
