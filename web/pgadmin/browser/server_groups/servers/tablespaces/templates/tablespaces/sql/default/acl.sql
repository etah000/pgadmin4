{### SQL to fetch privileges for tablespace ###}
SELECT 'spcacl' as deftype, 
       'PUBLIC' as  grantee, 
       'default' as grantor,
       array() as privileges, 
       array() as grantable

