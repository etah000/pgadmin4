select
       name as nspname
FROM system.databases
{% if did %} WHERE name = '{{ did }}' {% endif %}
