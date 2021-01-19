{# SQL query for getting columns #}
SELECT database as schema_name,
      table as table_name,
	  name as column_name,
	  type as type_name,
	  default_kind as has_default,
	  default_expression as default
FROM system.columns
where database in ({{schema_names}})
ORDER BY 1,2
