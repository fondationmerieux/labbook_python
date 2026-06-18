FROM almalinux:9.7

# permanent files (manuals, reports, logo ...)
COPY storage /storage

# copy some resource
COPY labbook_BE/alembic/resource /storage/resource

RUN mkdir -p /storage/resource/connect/analyzer/mapping
RUN mkdir -p /storage/resource/connect/analyzer/plugin
RUN mkdir -p /storage/resource/connect/analyzer/setting

# EPEL (sshpass, wkhtmltopdf) + plugins
RUN yum install -y epel-release dnf-plugins-core

# Python 3.11
RUN yum update -y && yum install -y python3.11 python3.11-pip python3.11-devel

# MySQL 8.4 community client (mysql/mysqldump)
RUN yum install -y https://dev.mysql.com/get/mysql84-community-release-el9-1.noarch.rpm && dnf -y --refresh makecache \
    && echo "exclude=mysql84-community-release*" >> /etc/dnf/dnf.conf

# system packages (EL9: no compat-openssl10, no 'mysql' client package)
RUN yum update -y && yum install -y \
    binutils \
    glibc-devel \
    which \
    openssh-clients \
    httpd \
    mod_ssl \
    sshpass \
    unoconv \
    libreoffice-headless \
    logrotate \
    mysql-community-client

# specific for wkhtmltopdf used by pdfkit
COPY vendor/*.rpm /tmp

RUN set -eux \
    && yum install -y /tmp/*.rpm \
    && rm -f /tmp/*.rpm \
    && yum clean all \
    && python3.11 -m pip install --upgrade pip \
    && python3.11 -m pip install --no-cache-dir --ignore-installed setuptools \
    && python3.11 -m pip install --no-cache-dir supervisor pipenv \
    && mkdir -p /home/supervisor/log /home/supervisor/tmp \
               /home/apps/labbook_FE/labbook_FE \
               /home/apps/labbook_BE/labbook_BE

COPY supervisor/etc /home/supervisor/etc

# symlink resources to Apache docroot
RUN ln -s /storage/resource /var/www/html/

# bash aliases
RUN echo  "alias ls='ls --color=auto'" >> /root/.bashrc && \
    echo  "alias l.='ls -d .* --color=auto'" >> /root/.bashrc && \
    echo  "alias l='ls -CF'" >> /root/.bashrc && \
    echo  "alias la='ls -A'" >> /root/.bashrc && \
    echo  "alias ll='ls -alF'" >> /root/.bashrc

# Apache config
COPY etc/httpd/build/conf/httpd.conf /etc/httpd/conf/
COPY etc/httpd/build/conf.d/ssl.conf /etc/httpd/conf.d/

# ===== FE =====
WORKDIR /home/apps/labbook_FE/labbook_FE
COPY labbook_FE/Pipfile ./
RUN /bin/bash -lc "\
    python3.11 -m venv venv && \
    source venv/bin/activate && \
    pip install --upgrade pip && \
    pip install pipenv && \
    pipenv install --deploy"
COPY labbook_FE /home/apps/labbook_FE/labbook_FE

# ===== BE =====
WORKDIR /home/apps/labbook_BE/labbook_BE
COPY labbook_BE/Pipfile ./
RUN /bin/bash -lc "\
    python3.11 -m venv venv && \
    source venv/bin/activate && \
    pip install --upgrade pip && \pip install pipenv && \
    pipenv install --deploy"
COPY labbook_BE /home/apps/labbook_BE/labbook_BE

# optional helper
RUN mkdir -p /home/apps/apache
COPY apache/apache.sh /home/apps/apache/

# Logrotate config for LabBook
COPY logrotate.d/labbook /etc/logrotate.d/labbook

CMD ["supervisord", "-c", "/home/supervisor/etc/supervisor.conf", "--pidfile", "/home/supervisor/tmp/supervisor.pid", "--user", "root"]
