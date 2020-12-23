SELECT
    name AS name, 
    type AS cltype,
    '' AS inheritedfrom,
    name as inheritedid
FROM
    system.columns
WHERE
    1
{% if did %}
    AND database = '{{did}}'
{% endif %}
{% if tid %}
    AND table = '{{tid}}'
{% endif %}