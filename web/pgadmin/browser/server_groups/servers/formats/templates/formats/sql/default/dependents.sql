{% if fetch_database %}
SELECT '' datname,
    '' datallowconn,
    '' datformat
{% endif %}

{% if fetch_dependents %}
SELECT '' as relkind, '' as nspname,
    '' as relname, '' as indname
{% endif %}

