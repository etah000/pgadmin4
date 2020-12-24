{% import 'tables/sql/macros/db_catalogs.macro' as CATALOG %}
SELECT 
    name AS oid, 
    '' AS relname,
    'public' AS nspname,
    '' AS inherits
FROM system.tables
LIMIT 0