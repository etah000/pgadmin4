SELECT
    name,
    name AS oid,
    type AS datatype,
    default_expression AS not_null,
    default_expression AS has_default_val
FROM system.columns
WHERE database = '{{ did }}' AND table = '{{ tid }}'