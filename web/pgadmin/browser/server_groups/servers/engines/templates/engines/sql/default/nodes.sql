SELECT
	name AS oid, 
	name AS rolname, 
	1 AS rolcanlogin, 
	1 AS rolsuper
FROM system.table_engines
{% if rid %} WHERE name = '{{ rid }}' {% endif %}
