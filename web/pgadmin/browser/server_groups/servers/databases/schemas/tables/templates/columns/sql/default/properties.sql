SELECT 
    NULL AS attacl,
    0 AS attlen,
    0 AS attndims,
    0 AS attnotnull,
    rowNumberInAllBlocks() AS attnum,
    NULL AS attoptions,
    -1 AS attstattarget
    'p' AS attstorage,
    0 AS atttypid,
    -1 AS atttypmod,
    name AS cltype,
    '' AS collspcname,
    'p' AS defaultstorage,
    NULL AS defval,
    NULL AS description,
    name AS displaytypname,
    23 AS elemoid,
    is_in_sorting_key AS indkey,
    is_fk: false
    0 AS is_sys_column,
    0 AS isdup,
    name,
    seclabels: null
    name AS typname,
    'public' AS typnspname
FROM system.columns
WHERE database = '{{ did }}' AND table = '{{ tid }}'