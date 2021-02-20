SELECT DISTINCT
    cluster AS did,
    cluster AS name,
    '' AS spcname,
    1 AS datallowconn,
    1 AS cancreate,
    user AS owner
FROM
    system.clusters
WHERE
    1
ORDER BY
    name;
