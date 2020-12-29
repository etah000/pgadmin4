{# Fetch privileges for schema #}
SELECT
    'nspacl' AS deftype, 
    'PUBLIC' AS grantee,
    'default' AS grantor, 
    array() AS privileges,
    array() AS grantable
