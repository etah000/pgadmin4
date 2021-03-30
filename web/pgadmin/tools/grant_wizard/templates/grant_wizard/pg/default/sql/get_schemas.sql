{# ===== Fetch list of all schemas ===== #}
select name as oid,
       name
from system.databases
{% if did %} WHERE name = '{{ did }}'; {% endif %}

