select
       t.database AS {{ conn|qtIdent(_('Database Name')) }},
       t.name AS {{ conn|qtIdent(_('Table Name')) }} ,
       p.partion_num AS {{ conn|qtIdent(_('Partition Number')) }},
       t.total_rows AS {{ conn|qtIdent(_('Total Rows')) }},
       t.total_bytes AS {{ conn|qtIdent(_('Size')) }}
from system.tables t all left join
              (
                  select table, database, count(partition) partion_num from system.parts group by table, database
                  ) p
on (t.database=p.database and t.name=p.table)
WHERE
    t.database = '{{ did }}'
    AND t.name NOT LIKE '.%'
    AND t.engine NOT LIKE '%View'
{% if tid %}  AND t.name = '{{ tid }}' {% endif %}
{% if did %}  AND t.database = '{{ did }}' {% endif %}
ORDER BY name
