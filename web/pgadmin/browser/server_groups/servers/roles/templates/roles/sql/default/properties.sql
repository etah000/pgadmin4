SELECT
    name AS oid,
	name AS `oid-2`,
    name AS rolname,
    1 AS rolinherit,
    0 AS rolcreaterole,
    0 AS rolcreatedb,
    1 AS rolcanlogin,
    (CASE name WHEN 'default' THEN 1 ELSE 0 END) AS rolreplication,
    -1 AS rolconnlimit,
    '' AS rolpassword,
    0 AS rolvaliduntil,
    0 AS rolbypassrls,
    array() AS rolconfig,
    (CASE name WHEN 'default' THEN 1 ELSE 0 END) AS rolsuper,
    (CASE name WHEN 'default' THEN 1 ELSE 0 END) AS rolcatupdate,
    '' AS description,
    array() AS rolmembership,
    array() AS seclabels,
    storage,
    auth_type,
    auth_params,
    host_ip,
    host_names,
    host_names_regexp,
    host_names_like,
    default_roles_all,
    default_roles_list,
    default_roles_except
FROM system.users
{% if rid %} WHERE name = '{{ rid }}' {% endif %}
UNION ALL
SELECT
    name AS oid,
	name AS `oid-2`,
    name AS rolname,
    1 AS rolinherit,
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
    0 AS rolcatupdate,
    '' AS description,
    array() AS rolmembership,
    array() AS seclabels,
    '' AS storage,
    NULL AS auth_type,
    NULL AS auth_params,
    array() AS host_ip,
    array() AS host_names,
    array() AS host_names_regexp,
    array() AS host_names_like,
    0 AS default_roles_all,
    array() AS default_roles_list,
    array() AS default_roles_except
FROM system.roles
{% if rid %} WHERE name = '{{ rid }}' {% endif %}
