{# ============================ Get ACLs ========================= #}
{% if vid %}
SELECT
    'datacl' AS deftype,
    'PUBLIC' AS grantee,
    'default' AS grantor,
    array() as privileges,
    array() as grantable
{% endif %}
