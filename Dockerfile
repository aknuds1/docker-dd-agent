FROM datadog/docker-dd-agent

RUN apt-get update && apt-get install -y wget libicu52 libfontconfig1 libfreetype6 \
libsqlite3-0 libssl1.0.0 libpng12-0
RUN wget https://s3.eu-central-1.amazonaws.com/muzhack.com/phantomjs.tar.gz && \
tar xzf phantomjs.tar.gz && mv phantomjs /usr/local/bin \
&& apt-get purge --auto-remove -y wget \
&& apt-get clean \
&& rm -rf /tmp/* /var/lib/apt/lists/*

RUN /opt/datadog-agent/embedded/bin/pip install rethinkdb selenium

COPY conf.d/haproxy.yaml /etc/dd-agent/conf.d/haproxy.yaml
COPY checks.d/rethinkdb.py /etc/dd-agent/checks.d/rethinkdb.py
COPY conf.d/rethinkdb.yaml /etc/dd-agent/conf.d/rethinkdb.yaml
COPY checks.d/browsertest.py /etc/dd-agent/checks.d/browsertest.py
COPY conf.d/browsertest.yaml /etc/dd-agent/conf.d/browsertest.yaml
