{### SQL to fetch tablespace object properties ###}
SELECT
    name AS oid, 
    name, 
    path AS spclocation, 
    '' AS spcoptions,
    'default' AS spcuser,
    '' AS  description,
    '' as acl
FROM system.disks;

