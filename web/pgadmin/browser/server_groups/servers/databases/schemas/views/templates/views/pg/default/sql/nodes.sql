SELECT
    name AS oid,
    name AS name
FROM system.tables
WHERE
  engine in ('View','LiveView')
{% if did %}
    AND database = '{{did}}'
{% endif %}
{% if vid %}
    AND name = '{{vid}}'
{% endif %}
ORDER BY
    name