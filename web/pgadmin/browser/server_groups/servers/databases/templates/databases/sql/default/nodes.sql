SELECT
    name AS did,
    *
FROM ( SELECT DISTINCT
        db.database AS name,
        '' AS spcname,
        1 AS datallowconn,
        1 AS cancreate,
        currentUser () AS owner
    FROM
        system.tables AS db
    WHERE 1
{% if db_restrictions %}
AND
db.database IN ({{db_restrictions}})
{% endif %}

    ORDER BY
        database);
