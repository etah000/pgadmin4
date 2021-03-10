SELECT d.name AS {{ conn|qtIdent(_('Database')) }},
       toString(sum(bytes_on_disk))  AS {{ conn|qtIdent(_('Size')) }}
FROM system.databases d all left join system.parts p
on (p.database=d.name)
    {% if did %} WHERE d.name = '{{ did }}' {% endif %}
GROUP BY d.name
ORDER BY d.name
