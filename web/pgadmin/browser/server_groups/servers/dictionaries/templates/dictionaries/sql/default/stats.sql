{### SQL to fetch dictionary object stats ###}
select
       name as {{ conn|qtIdent(_('Name')) }},
       query_count as {{ conn|qtIdent(_('Query Count')) }},
       loading_duration as {{ conn|qtIdent(_('Loading Duration')) }},
       last_exception  as {{ conn|qtIdent(_('Last Exception')) }}
from system.dictionaries;
