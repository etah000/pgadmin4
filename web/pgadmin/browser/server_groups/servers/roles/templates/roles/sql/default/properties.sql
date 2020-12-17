SELECT
    name AS oid,
	name AS `oid-2`,
    name AS rolname,
    0 AS rolinherit,
    0 AS rolcreaterole,
    0 AS rolcreatedb,
    1 AS rolcanlogin,
    0 AS rolreplication,
    -1 AS rolconnlimit,
    '' AS rolpassword,
    0 AS rolvaliduntil,
    0 AS rolbypassrls,
    array() AS rolconfig,
    1 AS rolsuper,
    1 AS rolcatupdate,
    '' AS description,
    array() AS rolmembership,
    array() AS seclabels
FROM system.users
{% if rid %} WHERE name = '{{ rid }}' {% endif %}
UNION ALL
SELECT
    name AS oid,
	name AS `oid-2`,
    name AS rolname,
    0 AS rolinherit,
    0 AS rolcreaterole,
    0 AS rolcreatedb,
    0 AS rolcanlogin,
    0 AS rolreplication,
    -1 AS rolconnlimit,
    '' AS rolpassword,
    0 AS rolvaliduntil,
    0 AS rolbypassrls,
    array() AS rolconfig,
    0 AS rolsuper,
    1 AS rolcatupdate,
    '' AS description,
    array() AS rolmembership,
    array() AS seclabels
FROM system.roles
{% if rid %} WHERE name = '{{ rid }}' {% endif %}
