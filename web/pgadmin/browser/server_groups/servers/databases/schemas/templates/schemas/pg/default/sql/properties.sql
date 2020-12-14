{% import 'catalog/pg/macros/catalogs.sql' as CATALOGS %}
SELECT
    3 AS nsptyp,
    'public' AS name,
    0 AS oid,
    '' AS acl,
    'default' AS namespaceowner, 
    '' AS description,
    1 AS can_create,
    {### Default ACL for Tables ###}
    '' AS tblacl,
    {### Default ACL for Sequnces ###}
    '' AS seqacl,
    {### Default ACL for Functions ###}
    '' AS funcacl,
    '' AS seclabels

