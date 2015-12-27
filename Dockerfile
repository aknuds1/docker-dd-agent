FROM datadog/docker-dd-agent

RUN /opt/datadog-agent/embedded/bin/pip install rethinkdb

COPY conf.d/haproxy.yaml /etc/dd-agent/conf.d/haproxy.yaml
COPY checks.d/rethinkdb.py /etc/dd-agent/checks.d/rethinkdb.py
COPY conf.d/rethinkdb.yaml /etc/dd-agent/conf.d/rethinkdb.yaml
