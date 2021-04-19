{#============================Create new view=========================#}
{% if display_comments %}
-- View: {{ data.schema }}.{{ data.name }}

-- DROP VIEW {{ conn|qtIdent(data.schema, data.name) }};

{% endif %}
{% if data.name and data.definition %}
CREATE OR REPLACE VIEW {% if data.database %}{{ data.database }}.{% endif %}{{ data.name }}{% if data.on_cluster %} ON CLUSTER {{ data.on_cluster }}{% endif %}
 AS
{{ data.definition.rstrip(';') }};
{% endif %}
