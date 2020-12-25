{### SQL to fetch privileges for datatype ###}
SELECT 'spcacl' as deftype,
       'PUBLIC' as  grantee,
       'default' as grantor,
       array() as privileges,
       array() as grantable

