{% if data.is_import %}
insert into {{ conn|qtIdent(data.database, data.table)}}  {% if columns %} ({{ columns }}) {% endif %} FORMAT {{ data.format }}
{% else %}
SELECT{% if columns %} {{ columns }} {% else %} * {% endif %}from {{ conn|qtIdent(data.database, data.table)}} INTO OUTFILE '{{ data.filename }}' FORMAT {{ data.format }}
{% endif %}
