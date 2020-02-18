FROM debian:stretch

# Install the Jenkins agent
ARG user=jenkins
ARG group=jenkins
ARG uid=10000
ARG gid=10000

ENV AGENT_VERSION=3.23 \
    AGENT_WORKDIR=/home/${user}/agent

RUN apt-get update && \
    apt-get install -y --no-install-recommends ca-certificates default-jre wget && \
    groupadd -g ${gid} ${group} && \
    useradd -c "Jenkins user" -d /home/${user} -u ${uid} -g ${gid} -m ${user} -s /bin/bash && \
    mkdir -p /usr/share/jenkins && \
    wget -q -O /usr/share/jenkins/slave.jar https://repo.jenkins-ci.org/public/org/jenkins-ci/main/remoting/${AGENT_VERSION}/remoting-${AGENT_VERSION}.jar && \
    chmod 755 /usr/share/jenkins && \
    chmod 644 /usr/share/jenkins/slave.jar && \
    wget -q -O /usr/local/bin/jenkins-slave https://artifactory.srv.orionprod.net/artifactory/jenkins/jenkins-slave && \
    chmod 755 /usr/local/bin/jenkins-slave

# Install golang, its dependencies, and other tooling
ENV GOLANG_VERSION=1.11.5 \
    GOROOT=/usr/src/go \
    GOPATH=/go

RUN apt-get install -y --no-install-recommends apt-transport-https gnupg && \
    echo 'deb http://apt.postgresql.org/pub/repos/apt/ stretch-pgdg main' > /etc/apt/sources.list.d/stretch-pgdg.list && \
    wget -q -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - && \
    apt-get update && \
    apt-get install -y --no-install-recommends build-essential curl dh-make fakeroot genisoimage git jq libpam0g-dev lintian maven m4 net-tools openjdk-8-jdk openssh-client postgresql-9.5 postgresql-contrib-9.5 python-jinja2 python-pip python-setuptools python-yaml qemu-kvm qemu-utils shellcheck sudo unzip vim zip && \
    pip install awscli && \
    mkdir ${GOROOT} && \
    wget -q -O - https://dl.google.com/go/go${GOLANG_VERSION}.linux-amd64.tar.gz | tar -C ${GOROOT} --strip-components=1 -xvz && \
    (wget -q -O - https://raw.githubusercontent.com/creationix/nvm/v0.33.8/install.sh | PROFILE=/etc/profile.d/nvm.sh NVM_DIR=/usr/local/nvm bash) && \
    echo 'export NVM_DIR=/usr/local/nvm && . "$NVM_DIR/nvm.sh"' > /etc/profile.d/nvm.sh && \
    chmod +x /etc/profile.d/nvm.sh && . /etc/profile.d/nvm.sh && \
    nvm install 8.11.1 && nvm install 6.9.1 && nvm use 6.9.1 && \
    npm install -g npm@3.10.8 && \
    chmod -R o+w /usr/local/nvm && \
    mkdir /opt/flyway && wget -q -O - https://repo1.maven.org/maven2/org/flywaydb/flyway-commandline/4.0/flyway-commandline-4.0-linux-x64.tar.gz | tar -xz -C /opt/flyway --strip-components=1 && \
    chmod +x /opt/flyway/flyway && \
    ln -sf /usr/lib/postgresql/9.5/bin/pg_ctl /usr/bin && \
    usermod -a -G postgres ${user} && \
    ln -sf /opt/flyway/flyway /usr/local/bin && \
    echo "dash dash/sh boolean false" | debconf-set-selections && \
    DEBIAN_FRONTEND=noninteractive dpkg-reconfigure dash && \
    echo "${user} ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers && \
    cd /tmp && wget -q https://releases.hashicorp.com/packer/1.3.3/packer_1.3.3_linux_amd64.zip && \
    unzip packer_1.3.3_linux_amd64.zip -d /usr/local/bin && \
    rm -f packer_1.3.3_linux_amd64.zip && \
    usermod -a -G kvm ${user}

which pip 

# Install python3 and related tools.  Python2 above should be removed when no
# build depends on it.
RUN apt-get install -y --no-install-recommends python3 python3-jinja2 python3-pip python3-setuptools python3-yaml python3-wheel python3-six python3-bitarray python3-certifi python3-chardet python3-idna python3-regex python3-lxml python3-setuptools

# remove python2, 
RUN rm /usr/bin/python && ln -s /usr/bin/python3 /usr/bin/python && which pip && pip install certifi && pip install chardet && pip install idna && pip install lxml && pip install urllib3==1.23 && pip install requests==2.22.0 

# Install various Go-based tools
RUN $GOROOT/bin/go get golang.org/x/tools/cmd/goimports && \
    $GOROOT/bin/go get github.com/kardianos/govendor && \
    $GOROOT/bin/go get github.com/golang/mock/gomock && \
    $GOROOT/bin/go get github.com/jteeuwen/go-bindata/... && \
    $GOROOT/bin/go get github.com/golang/mock/mockgen && \
    $GOROOT/bin/go get github.com/ugorji/go/codec/codecgen && \
    $GOROOT/bin/go get github.com/onsi/ginkgo/ginkgo && \
    $GOROOT/bin/go get github.com/onsi/gomega && \
    $GOROOT/bin/go get github.com/SpirentOrion/gocovmerge && \
    $GOROOT/bin/go get github.com/axw/gocov/... && \
    $GOROOT/bin/go get github.com/AlekSi/gocov-xml && \
    wget -q -O ${GOPATH}/bin/jfrog http://artifactory.srv.orionprod.net/artifactory/jenkins/jfrog && \
    chmod +x ${GOPATH}/bin/jfrog && \
    chown -R ${user}:${group} ${GOPATH}

# Install Orion CLI tools
ENV ARTIFACTORY_URL=https://artifactory.srv.orionprod.net/artifactory \
    ARTIFACTORY_USER=builder \
    ARTIFACTORY_APIKEY=eyJ2ZXIiOiIyIiwidHlwIjoiSldUIiwiYWxnIjoiUlMyNTYiLCJraWQiOiJnQmxsZzRiMkM3T1VGWmNXZnNiUXFBOUE0NzhWZUR1am9nSGxhM2RUSWRFIn0.eyJzdWIiOiJqZnJ0QDAxYzgxdzhoeHFnYnQ2MW15NTY1bTQwNGRlXC91c2Vyc1wvYnVpbGRlciIsInNjcCI6Im1lbWJlci1vZi1ncm91cHM6cmVhZGVycyBhcGk6KiIsImF1ZCI6ImpmcnRAMDFjODF3OGh4cWdidDYxbXk1NjVtNDA0ZGUiLCJpc3MiOiJqZnJ0QDAxYzgxdzhoeHFnYnQ2MW15NTY1bTQwNGRlIiwiaWF0IjoxNTIyNjc5MDI0LCJqdGkiOiI0ZTRiMzViZC0xYTA1LTRjMWItYTg5ZS0wZWYyNDk3MTNiODAifQ.vYyvVXn-FZU434z9PSVsA4m5_03-7zBfDiBPFpfB9mwuqtjfq7bKHXXtnPsnnwLY4x8GSZlPs1rv6k7OPsSoXE_wzOuBWYhB7CcxFqqXRxPexGATgoALlSL04rzd8nB-MxRFEGEcrmdpqE5jD6Z_KRIu61PbdTQ-pARC3AZ548ob5VMy6YvbV9LQxny5xz1wT_Hh9xWSd2w4eTn_E9U4yZTHM_Q2JUZtEf960p0XDD5ezyytCrI6x3ycX2Cf1tN2Rk3JSPOmfyyHcDby9C8_PFMecjy8k_aFE3tTe6JLBaSYFw6Q_YkiYcFjd4ODjkMzbJVFIuGaznwYquHsXKafHQ \
    JFROG_CLI_LOG_LEVEL=INFO \
    JFROG_CLI_OFFER_CONFIG=false

RUN mkdir /opt/orion && \
    $GOPATH/bin/jfrog rt dl --url ${ARTIFACTORY_URL} --user ${ARTIFACTORY_USER} --apikey ${ARTIFACTORY_APIKEY} --explode --flat temeva/aat/orion-cli.linux-amd64.tgz /opt/orion/ && \
    chown -R ${user}:${group} /opt/orion && \
    echo 20180814

# Run the Jenkins slave as the Jenkins user
USER ${user}

ENV USER=${user} \
HOME=/home/${user}

RUN mkdir /home/${user}/.jenkins && \
    mkdir -p ${AGENT_WORKDIR}

VOLUME /home/${user}/.jenkins
VOLUME ${AGENT_WORKDIR}

ENTRYPOINT ["jenkins-slave"]
