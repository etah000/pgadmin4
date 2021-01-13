{% import 'macros/schemas/security.macros' as SECLABEL %}
{% import 'macros/schemas/privilege.macros' as PRIVILEGE %}
{% import 'macros/variable.macros' as VARIABLE %}
{% import 'columns/macros/security.macros' as COLUMN_SECLABEL %}
{% import 'columns/macros/privilege.macros' as COLUMN_PRIVILEGE %}
{% import 'tables/sql/macros/constraints.macro' as CONSTRAINTS %}
{#===========================================#}
{#====== MAIN TABLE TEMPLATE STARTS HERE ======#}
{#===========================================#}
{#
 If user has not provided any details but only name then
 add empty bracket with table name
#}
{% set empty_bracket = ""%}
{% if data.coll_inherits|length == 0 and  data.columns|length == 0 and not data.typname and not data.like_relation and data.primary_key|length == 0 and data.unique_constraint|length == 0 and data.foreign_key|length == 0 and data.check_constraint|length == 0 and data.exclude_constraint|length == 0 %}
{% set empty_bracket = "\n(\n)"%}
{% endif %}
{{data.create_table_query}}

{#===========================================#}
{#====== MAIN TABLE TEMPLATE ENDS HERE ======#}
{#===========================================#}
