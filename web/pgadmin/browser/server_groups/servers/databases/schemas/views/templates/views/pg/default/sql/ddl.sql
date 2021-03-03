{#===========================================#}
{#====== MAIN VIEW TEMPLATE STARTS HERE ======#}
{#===========================================#}
{#
 If user has not provided any details but only name then
 add empty bracket with table name
#}
{% set empty_bracket = ""%}

{% if not data.format %}
{{data.create_table_query}}
{% endif %}

{% if data.format %}
CREATE VIEW {{ data.view_str }}
{### Add columns ###}
{% if data.column_str and data.column_str|length > 0 %}
(
{% for c in data.column_str %}
    {{c}}{% if not loop.last %},
{% endif %}
{% endfor %}
{% endif %})
AS SELECT {{data.table_str}}
;
{% endif %}

{#===========================================#}
{#====== MAIN VIEW TEMPLATE ENDS HERE ======#}
{#===========================================#}
