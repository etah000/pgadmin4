 SELECT DISTINCT
    name AS did,
    '' AS spcname,
    1 AS datallowconn,
    1 AS cancreate,
    currentUser () AS owner,
    name,
    engine,
    data_path,
    metadata_path
FROM
    system.databases
WHERE 1
    {% if db_restrictions %}
    AND db.database IN ({{db_restrictions}})
    {% endif %}
    AND name <>'_temporary_and_external_tables'
    {% if did %}
    AND name IN ('{{ did }}')
    {% endif %}    
ORDER BY
    name;
