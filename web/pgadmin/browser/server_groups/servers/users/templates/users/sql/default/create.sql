{% import 'macros/security.macros' as SECLABEL %}
{% import 'macros/variable.macros' as VARIABLE %}

{# CREATE USER [IF NOT EXISTS | OR REPLACE] name1 [ON CLUSTER cluster_name1]
        [, name2 [ON CLUSTER cluster_name2] ...]
    [IDENTIFIED [WITH {NO_PASSWORD|PLAINTEXT_PASSWORD|SHA256_PASSWORD|SHA256_HASH|DOUBLE_SHA1_PASSWORD|DOUBLE_SHA1_HASH|LDAP_SERVER}] BY {'password'|'hash'}]
    [HOST {LOCAL | NAME 'name' | REGEXP 'name_regexp' | IP 'address' | LIKE 'pattern'} [,...] | ANY | NONE]
    [DEFAULT ROLE role [,...]]
    [SETTINGS variable [= value] [MIN [=] min_value] [MAX [=] max_value] [READONLY|WRITABLE] | PROFILE 'profile_name'] [,...]
#}
{#
CREATE ROLE [IF NOT EXISTS | OR REPLACE] name1 [, name2 ...]
    [SETTINGS variable [= value] [MIN [=] min_value] [MAX [=] max_value] [READONLY|WRITABLE] | PROFILE 'profile_name'] [,...]
#}

{% if data.is_user %}
CREATE USER {{ conn|qtIdent(data.rolname) }}{% if data.cluster %} ON CLUSTER {{ data.cluster }}{% endif %}{% if data.rolpassword %}

   IDENTIFIED WITH PLAINTEXT_PASSWORD BY {% if dummy %}'xxxxxx'{% else %} {{ data.rolpassword | qtLiteral(True) }}{% endif %}{% endif %}{% if data.host_type and data.host_express %}

   HOST {{ data.host_type}} {{ data.host_express | qtLiteral(True) }}{% endif %} {% if data.members and data.members|length > 0 %}

   DEFAULT ROLE {{ conn|qtIdent(data.members)|join(', ') }}{% endif %}{% if data.variables or data.profile %}

   SETTINGS {% for var in data.variables %}{{ var.name }}={{ var.value }}{% if not loop.last %},{% endif %}{% endfor %}{% endif %}{% if data.profile %}

   PROFILE {{ data.profile| qtLiteral(True) }}{% endif %}

;
{#
   % if data.read_write_mode=='WRITABLE' %}

   WRITABLE {% else %} {% if data.read_write_mode=='READONLY' %}

   READONLY {% endif %} {% endif %}
   #}
{% endif %}

{% if not data.is_user %}
CREATE ROLE {{ conn|qtIdent(data.rolname) }}{% if data.variables or data.profile %}

   SETTINGS {% for var in data.variables %}{{ var.name }}={{ var.value }}{% if not loop.last %},{% endif %}{% endfor %}{% endif %} {% if data.profile %}

   PROFILE {{ data.profile| qtLiteral(True) }}{% endif %}
;

    {#
    {% if data.read_write_mode=='WRITABLE' %}

   WRITABLE {% else %} {% if data.read_write_mode=='READONLY' %}

   READONLY {% endif %} {% endif %}
    #}

{% endif %}

