{% import 'macros/schemas/security.macros' as SECLABEL %}
{% import 'macros/schemas/privilege.macros' as PRIVILEGE %}
{% import 'macros/variable.macros' as VARIABLE %}
{% import 'columns/macros/security.macros' as COLUMN_SECLABEL %}
{% import 'columns/macros/privilege.macros' as COLUMN_PRIVILEGE %}
{# import 'tables/sql/macros/constraints.macro' as CONSTRAINTS #}
{#===========================================#}
{#====== MAIN TABLE TEMPLATE STARTS HERE ======#}
{#===========================================#}

{% from 'tables/sql/macros/column.macro' import COLUMNS %}
{% from 'tables/sql/macros/index.macro' import INDEXES %}
{% from 'tables/sql/macros/constraint.macro' import CONSTRAINTS %}
{% from 'tables/sql/macros/engine.macro' import ENGINE %}


{#===========================================#}
{#====== MAIN TABLE TEMPLATE STARTS HERE ======#}
{#===========================================#}



CREATE TABLE {{did}}.{{conn|qtIdent(data.name)}}{% if data.cluster %} ON CLUSTER {{ data.cluster }}{% endif %}

{% if data.columns|length > 0 %}({% endif %}

{### Add columns ###}
{% if data.columns and data.columns|length > 0 %}
{{ COLUMNS(data.columns) }}
{% endif %}

{### Add indexes ###}
{%- if data.indexes and data.indexes|length > 0 %}
{{ INDEXES(data) }}
{% endif %}

{### Add constraints ###}
{%- if data.constraints and data.constraints|length > 0 %}
{{ CONSTRAINTS(data) }}
{% endif %}

{% if data.columns|length > 0 %}){% endif %}

{###  ENGINE ###}
{{ ENGINE(data) }}


{###  ACL on Table ###}
{% if data.relacl %}

{% for priv in data.relacl %}
{{ PRIVILEGE.SET(conn, 'TABLE', priv.grantee, data.name, priv.without_grant, priv.with_grant, data.schema) }}
{% endfor %}
{% endif %}
{### SQL for COMMENT ###}
{#===========================================#}
{#====== MAIN TABLE TEMPLATE ENDS HERE ======#}
{#===========================================#}
{#===========================================#}
{#  COLUMN SPECIFIC TEMPLATES STARTS HERE    #}
{#===========================================#}
{% if data.columns and data.columns|length > 0 %}
{% for c in data.columns %}
{% if c.description %}

COMMENT ON COLUMN {{conn|qtIdent(data.schema, data.name, c.name)}}
    IS {{c.description|qtLiteral}};
{% endif %}

{###  ACL ###}
{% if c.attacl and c.attacl|length > 0 %}

{% for priv in c.attacl %}
    {{ COLUMN_PRIVILEGE.APPLY(conn, data.schema, data.name, c.name, priv.grantee, priv.without_grant, priv.with_grant) }}
{% endfor %}
{% endif %}
{###  ACL END ###}

{% endfor %}
{% endif %}
