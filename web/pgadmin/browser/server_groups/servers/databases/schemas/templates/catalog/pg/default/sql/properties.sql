{% import 'catalog/pg/macros/catalogs.sql' as CATALOGS %}
SELECT
    2 AS nsptyp,
    '' AS name,
    0 AS oid,
    '' as acl,
    '' AS namespaceowner, 
    '' AS description,
    0 AS can_create,
    '' AS tblacl,
    '' AS seqacl,
    '' AS funcacl,
    '' AS typeacl
FROM
    (SELECT 1 LIMIT 0) AS T