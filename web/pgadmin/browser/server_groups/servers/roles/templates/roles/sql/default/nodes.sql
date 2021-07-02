SELECT
	name AS oid,
	name AS rolname,
	0 AS rolcanlogin,
	0 AS rolsuper
FROM system.roles
{% if rid %} WHERE name = '{{ rid }}' {% endif %}
