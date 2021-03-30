{# ===== Fetch list of Database object types(Tables) ===== #}
{% if node_id %}
select name,database as nspname,
case
when engine='MaterializedView' then 'Materialized View'
when engine='View' then 'View'
else 'Table'
end as object_type,
case
when engine='MaterializedView' then 'icon-mview'
when engine='View' then 'icon-view'
else 'icon-table'
end as icon
from system.tables
WHERE database = '{{ did }}'
AND name NOT LIKE '.%';
{% endif %}
