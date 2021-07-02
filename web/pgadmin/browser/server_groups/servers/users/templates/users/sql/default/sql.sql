{% if is_user %}
SHOW CREATE USER {{ rid }};
{% else %}
SHOW CREATE ROLE {{ rid }};
{% endif %}
