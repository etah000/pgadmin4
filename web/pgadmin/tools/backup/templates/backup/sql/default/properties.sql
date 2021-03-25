SELECT
    backup_name,
    backup_type,
    backup_ctime
FROM 
    ir.backup
ORDER BY 
    backup_ctime ASC