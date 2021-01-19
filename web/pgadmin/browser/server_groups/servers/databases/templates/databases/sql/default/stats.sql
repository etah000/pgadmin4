SELECT database AS {{ conn|qtIdent(_('Database')) }},
       sum(bytes_on_disk)  AS {{ conn|qtIdent(_('Size')) }}
FROM system.parts
    {% if did %} WHERE database = '{{ did }}' {% endif %}
GROUP BY database
ORDER BY database
