select
       t.database AS {{ conn|qtIdent(_('Database name')) }},
       t.name AS {{ conn|qtIdent(_('Table name')) }},
       t.total_rows AS {{ conn|qtIdent(_('Total rows')) }},
       t.total_bytes AS {{ conn|qtIdent(_('Total bytes')) }}
from system.tables t
WHERE
    database = '{{ did }}'
    AND name NOT LIKE '.%'
    AND engine NOT LIKE '%View'
ORDER BY name
