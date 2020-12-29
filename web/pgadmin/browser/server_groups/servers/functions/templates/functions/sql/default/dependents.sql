{% if fetch_database %}
SELECT '' datname,
    '' datallowconn,
    '' datfunction
{% endif %}

{% if fetch_dependents %}
SELECT '' as relkind, '' as nspname,
    '' as relname, '' as indname
{% endif %}

