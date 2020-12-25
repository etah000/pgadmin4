SELECT
    name AS did,
    *
FROM ( SELECT DISTINCT
        db.cluster AS name,
        '' AS spcname,
        1 AS datallowconn,
        1 AS cancreate,
        currentUser () AS owner
    FROM
        system.clusters AS db
    WHERE 1
    ORDER BY
        name);
