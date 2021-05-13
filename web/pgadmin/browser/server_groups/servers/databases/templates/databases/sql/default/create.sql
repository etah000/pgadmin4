{% if data %}
CREATE DATABASE {{ conn|qtIdent(data.name) }} {% if data.cluster %}ON CLUSTER {{ data.cluster }}{% endif %}
{% endif %}
