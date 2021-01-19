SELECT
    c.name AS {{ conn|qtIdent(_('Column Name')) }},
    c.data_compressed_bytes AS {{ conn|qtIdent(_('Data Compressed Bytes')) }},
    c.data_uncompressed_bytes AS {{ conn|qtIdent(_('Data Uncompressed Bytes')) }},
    c.marks_bytes AS {{ conn|qtIdent(_('Marks Bytes')) }}
FROM
    system.columns c
WHERE database = '{{ did }}' AND table = '{{ tid }}'
{% if clid %}
 AND name = '{{ clid }}'
{% endif %}
