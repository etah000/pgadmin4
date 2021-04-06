{% from 'mviews/macros/engine.macro' import ENGINE %}
{% from 'mviews/macros/column.macro' import COLUMNS %}
{% from 'mviews/macros/index.macro' import INDEXES %}
{% from 'mviews/macros/constraint.macro' import CONSTRAINTS %}

{#===========================================#}
{#====== MAIN MVIEW TEMPLATE STARTS HERE ======#}
{#===========================================#}

{# ===================== Create new view ===================== #}
{% if display_comments %}
-- View: {{ data.schema }}.{{ data.name }}

-- DROP MATERIALIZED VIEW {{ conn|qtIdent(data.schema, data.name) }};

{% endif %}
{% if data.name and data.definition %}
CREATE MATERIALIZED VIEW IF NOT EXISTS {% if data.database %}{{ data.database }}.{% endif %}{{ data.name }}
{%- if data.columns|length > 0 %}({%- endif %}

{{ COLUMNS(data.columns) }}

{%- if data.columns|length > 0 and data.indexes and data.indexes|length > 0 %}
{{ INDEXES(data) }}
{%- endif %}

{%- if data.columns|length > 0 and data.constraints and data.constraints|length > 0 %}
{{ CONSTRAINTS(data) }}
{%- endif %}

{%- if data.columns|length > 0 %}){%- endif %}

{%- if data.on_cluster and data.columns|length <= 0 %}ON CLUSTER {{ data.on_cluster }}{%- endif %}

{%- if data.to_database or data.to_table %} TO {% if data.to_database %}{{ data.to_database }}.{% endif %}{% if data.to_table %}{{ data.to_table }}{% endif %}{%- endif %}

{% if not (data.to_database or data.to_table) %}{{ ENGINE(data) }}{% endif %}

{% if data.populate and not (data.to_database or data.to_table) %}POPULATE{% endif %}
 AS
{{ data.definition.rstrip(';') }}
{% endif %}