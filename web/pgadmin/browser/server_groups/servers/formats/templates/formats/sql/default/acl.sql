{### SQL to fetch privileges for formats ###}
SELECT 'spcacl' as deftype, 
       'PUBLIC' as  grantee, 
       'default' as grantor,
       array() as privileges, 
       array() as grantable

