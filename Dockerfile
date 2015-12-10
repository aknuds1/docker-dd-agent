FROM datadog/docker-dd-agent
ENV API_KEY=$DD_API_KEY
COPY conf.d/haproxy.yaml /etc/dd-agent/conf.d/haproxy.yaml
