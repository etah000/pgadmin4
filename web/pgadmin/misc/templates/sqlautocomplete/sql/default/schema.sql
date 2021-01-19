{# SQL query for getting current_schemas #}
{% if search_path %}
SELECT name as schema FROM system.databases ORDER BY 1
{% else %}
SELECT name as schema FROM system.databases ORDER BY 1
{% endif %}
