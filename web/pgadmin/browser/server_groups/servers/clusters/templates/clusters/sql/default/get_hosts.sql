SELECT DISTINCT host_name,port
FROM system.clusters
{% if did %}WHERE cluster = '{{ did }}' {% endif %}
ORDER BY host_name
