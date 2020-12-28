{### SQL to fetch tablespace object stats ###}
SELECT name as Name,
        concat(toString(round(total_space/(1024*1024*1024))),'G') as Total_Size
        ,concat(toString(round(free_space/(1024*1024*1024))),'G') as Free_Size
        ,concat(toString(round(keep_free_space/(1024*1024*1024))),'G') as Keep_Free_Size
FROM system.disks;


