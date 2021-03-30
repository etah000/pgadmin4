{# ===== Grant Permissions on Database Objects Selected ====
SET(conn, type, role, param, privs, with_grant_privs, schema, cluster)
#}
{% import 'macros/schemas/privilege.macros' as PRIVILEGE %}
{% for obj in data.objects -%}
{% for priv in data.priv -%}
{% if obj.object_type == 'Table' or obj.object_type == 'View' or obj.object_type == 'Materialized View'%}
{{ PRIVILEGE.SET(conn, 'TABLE', priv['grantee'], obj.name, priv['without_grant'], priv['with_grant'], obj.nspname, priv['cluster'] ) }}
{% endif %}
{% endfor -%}
{% endfor -%}
