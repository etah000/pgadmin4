SELECT
    name AS oid,
    name AS name
FROM system.tables
WHERE
  engine in ('MaterializedView')
{% if did %}
    AND database = '{{did}}'
{% endif %}
{% if (vid and datlastsysoid) %}
    AND name = '{{vid}}'
{% endif %}
ORDER BY
    name