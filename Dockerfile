FROM datadog/docker-dd-agent
COPY conf.d/haproxy.yaml /etc/dd-agent/conf.d/haproxy.yaml
