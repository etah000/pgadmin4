{### SQL to fetch tablespace object stats ###}
SELECT name as {{ conn|qtIdent(_('Name')) }},
        concat(toString(round(total_space/(1024*1024*1024))),'G') as {{ conn|qtIdent(_('Total Size')) }},
        concat(toString(round(free_space/(1024*1024*1024))),'G') as {{ conn|qtIdent(_('Free Size')) }},
        concat(toString(round(keep_free_space/(1024*1024*1024))),'G') as {{ conn|qtIdent(_('Keep Free Size')) }}
FROM system.disks;


