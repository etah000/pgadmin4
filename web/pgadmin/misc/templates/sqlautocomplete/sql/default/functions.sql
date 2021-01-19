{# ============= Fetch the list of functions based on given schema_names ============= #}
SELECT d.name schema_name,
    f.name func_name,
    '' arg_names,
    '' arg_types,
    '' arg_modes,
    '' return_type,
    f.is_aggregate is_aggregate,
    0 is_window,
    '' is_set_returning,
    '' AS arg_defaults
FROM system.functions f, (SELECT name FROM system.databases) d
ORDER BY 1, 2
