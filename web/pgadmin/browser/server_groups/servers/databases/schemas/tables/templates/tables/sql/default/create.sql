{% import 'macros/schemas/security.macros' as SECLABEL %}
{% import 'macros/schemas/privilege.macros' as PRIVILEGE %}
{% import 'macros/variable.macros' as VARIABLE %}
{% import 'columns/macros/security.macros' as COLUMN_SECLABEL %}
{% import 'columns/macros/privilege.macros' as COLUMN_PRIVILEGE %}
{% import 'tables/sql/macros/constraints.macro' as CONSTRAINTS %}
{#% import 'types/macros/get_full_type_sql_format.macros' as GET_TYPE %#}
{#===========================================#}
{#====== MAIN TABLE TEMPLATE STARTS HERE ======#}
{#===========================================#}

CREATE TABLE {{did}}.{{conn|qtIdent(data.name)}}

{% if data.like_relation or data.coll_inherits or data.columns|length > 0 or data.primary_key|length > 0 or data.unique_constraint|length > 0 or data.foreign_key|length > 0 or data.check_constraint|length > 0 or data.exclude_constraint|length > 0 %}
(
{% endif %}

{# {% if data.like_relation %}  #}
{#     LIKE {{ data.like_relation }}{% if data.like_default_value %}  #}

{#         INCLUDING DEFAULTS{% endif %}{% if data.like_constraints %}  #}

{#         INCLUDING CONSTRAINTS{% endif %}{% if data.like_indexes %}  #}

{#         INCLUDING INDEXES{% endif %}{% if data.like_storage %}  #}

{#         INCLUDING STORAGE{% endif %}{% if data.like_comments %}  #}

{#         INCLUDING COMMENTS{% endif %}{% if data.columns|length > 0 %},  #}
{# {% endif %}  #}
{# {% endif %}  #}

{### Add columns ###}
{% if data.columns and data.columns|length > 0 %}
{% for c in data.columns %}
{% if c.name and c.cltype %}
    {{conn|qtIdent(c.name)}} {{c.displaytypname}}{{c.cltype}}{% if c.attnotnull %} NOT NULL{% endif %}{% if c.defval is defined and c.defval is not none and c.defval != '' %} DEFAULT {{c.defval}}{% endif %}
{% if not loop.last %},
{% endif %}
{% endif %}
{% endfor %}
{% endif %}
{# Macro to render for constraints #}
{# {% if data.primary_key|length > 0 %}{% if data.columns|length > 0 %},{% endif %} #}
{# {{CONSTRAINTS.PRIMARY_KEY(conn, data.primary_key[0])}}{% endif %} #}

{% if data.like_relation or data.coll_inherits or data.columns|length > 0 or data.primary_key|length > 0 or data.unique_constraint|length > 0 or data.foreign_key|length > 0 or data.check_constraint|length > 0 or data.exclude_constraint|length > 0 %}

){% endif %}{% if data.relkind is defined and data.relkind == 'p' %} PARTITION BY {{ data.partition_scheme }} {% endif %}

{###  ENGINE ###}

ENGINE = Memory()

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
