{% if fetch_database %}
SELECT '' datname,
    '' datallowconn,
    '' datdictionary
{% endif %}

{% if fetch_dependents %}
SELECT '' as relkind, '' as nspname,
    '' as relname, '' as indname
{% endif %}

