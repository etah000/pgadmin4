SELECT
    name AS oid,
	name AS `oid-2`,
    name AS rolname,
    1 AS rolinherit,
    0 AS rolcreaterole,
    0 AS rolcreatedb,
    1 AS rolcanlogin,
    1 AS rolreplication,
    -1 AS rolconnlimit,
    '' AS rolpassword,
    0 AS rolvaliduntil,
    0 AS rolbypassrls,
    array() AS rolconfig,
    1 AS rolsuper,
    1 AS rolcatupdate,
    '' AS description,
    array() AS rolmembership,
    array() AS seclabels,
    supports_settings,
    supports_skipping_indices,
    supports_sort_order,
    supports_ttl,
    supports_replication,
    supports_deduplication
FROM system.table_engines
{% if rid %} WHERE name = '{{ rid }}' {% endif %}

