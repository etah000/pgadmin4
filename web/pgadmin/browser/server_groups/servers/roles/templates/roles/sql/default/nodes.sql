SELECT
	name AS oid, 
	name AS rolname, 
	1 AS rolcanlogin, 
	1 AS rolsuper
FROM system.users
{% if rid %} WHERE name = '{{ rid }}' {% endif %}
UNION ALL
SELECT
	name AS oid, 
	name AS rolname, 
	0 AS rolcanlogin, 
	0 AS rolsuper
FROM system.roles
{% if rid %} WHERE name = '{{ rid }}' {% endif %}