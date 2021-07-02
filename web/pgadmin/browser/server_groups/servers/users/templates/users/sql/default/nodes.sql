SELECT
	name AS oid,
	name AS rolname,
	1 AS rolcanlogin,
	(CASE name WHEN 'default' THEN 1 ELSE 0 END) AS rolsuper
FROM system.users
{% if rid %} WHERE name = '{{ rid }}' {% endif %}
