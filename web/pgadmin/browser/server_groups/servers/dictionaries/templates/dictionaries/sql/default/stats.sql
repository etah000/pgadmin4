{### SQL to fetch dictionary object stats ###}
select
       name,
       query_count,
       loading_duration,
       last_exception
from system.dictionaries;
