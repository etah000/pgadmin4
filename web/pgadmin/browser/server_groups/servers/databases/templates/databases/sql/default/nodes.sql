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
ORDER BY
    name;
