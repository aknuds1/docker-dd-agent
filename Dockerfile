FROM datadog/docker-dd-agent

RUN apt-get update && apt-get install -y --no-install-recommends \
build-essential \
ca-certificates \
g++ \
git \
flex \
bison \
gperf \
perl \
python \
ruby \
libsqlite3-dev \
libfontconfig1-dev \
libicu-dev \
libfreetype6 \
libssl-dev \
libpng-dev \
libjpeg-dev \
&& git clone --recurse-submodules https://github.com/ariya/phantomjs /tmp/phantomjs \
&& cd /tmp/phantomjs \
&& ./build.py --confirm --silent --jobs 2 \
&& mv bin/phantomjs /usr/local/bin \
&& cd \
&& apt-get purge --auto-remove -y \
build-essential \
g++ \
git \
flex \
bison \
gperf \
ruby \
perl \
python \
&& apt-get clean \
&& rm -rf /tmp/* /var/lib/apt/lists/*

RUN /opt/datadog-agent/embedded/bin/pip install rethinkdb selenium

COPY conf.d/haproxy.yaml /etc/dd-agent/conf.d/haproxy.yaml
COPY checks.d/rethinkdb.py /etc/dd-agent/checks.d/rethinkdb.py
COPY conf.d/rethinkdb.yaml /etc/dd-agent/conf.d/rethinkdb.yaml
COPY checks.d/browsertest.py /etc/dd-agent/checks.d/browsertest.py
COPY conf.d/browsertest.yaml /etc/dd-agent/conf.d/browsertest.yaml
