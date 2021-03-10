{# ===================== Create new view ===================== #}
{% if display_comments %}
-- View: {{ data.schema }}.{{ data.name }}

-- DROP MATERIALIZED VIEW {{ conn|qtIdent(data.schema, data.name) }};

{% endif %}
{% if data.name and data.definition %}
CREATE MATERIALIZED VIEW IF NOT EXISTS {% if data.database %}{{ data.database }}.{% endif %}{{ data.name }}{% if data.on_cluster %} ON CLUSTER {{ data.on_cluster }}{% endif %}{% if data.to_database or data.to_table %} TO {% if data.to_database %}{{ data.to_database }}.{% endif %}{% if data.to_table %}{{ data.to_table }}{% endif %}{% endif %}{% if not (data.to_database or data.to_table) %} ENGINE = {{ data.engine }}{% endif %}{% if data.populate and not (data.to_database or data.to_table) %} POPULATE{% endif %}
 AS
{{ data.definition.rstrip(';') }}
{% endif %}
