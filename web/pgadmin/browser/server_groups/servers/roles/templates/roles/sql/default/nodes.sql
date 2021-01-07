SELECT
	name AS oid, 
	name AS rolname, 
	1 AS rolcanlogin, 
	(CASE name WHEN 'default' THEN 1 ELSE 0 END) AS rolsuper
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