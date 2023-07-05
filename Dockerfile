FROM almalinux:8

# permanent files (manuals, reports, logo ...)
COPY storage /storage

# copy some resource
COPY labbook_BE/alembic/resource /storage/resource

COPY vendor/*.rpm /tmp

# EPEL repository is needed for sshpass
RUN yum install -y epel-release

# may have to add openssl libssl.so.10 before compat-openssl10
RUN yum update -y && yum install -y \
    compat-openssl10 \
    binutils \
    glibc-devel \
    mysql \
    python39 \
    which \
    openssh-clients \
    httpd \
    /tmp/*.rpm

RUN rm -f /tmp/*.rpm

RUN yum clean all

RUN yum install -y sshpass

RUN yum install -y mod_ssl

RUN yum install -y unoconv

RUN yum install -y logrotate

RUN yum clean all

# install supervisor
RUN pip3 install supervisor

RUN mkdir -p /home/supervisor/log \
             /home/supervisor/tmp \
             /home/apps/labbook_FE/labbook_FE \
             /home/apps/labbook_BE/labbook_BE

COPY supervisor/etc /home/supervisor/etc

RUN ln -s /storage/resource /var/www/html/

RUN echo  "alias ls='ls --color=auto'" >> /root/.bashrc
RUN echo  "alias l.='ls -d .* --color=auto'" >> /root/.bashrc
RUN echo  "alias l='ls -CF'" >> /root/.bashrc
RUN echo  "alias la='ls -A'" >> /root/.bashrc
RUN echo  "alias ll='ls -alF'" >> /root/.bashrc

COPY etc/httpd/build/conf/httpd.conf /etc/httpd/conf/
COPY etc/httpd/build/conf.d/ssl.conf /etc/httpd/conf.d/

RUN mkdir -p /home/apps/apache

COPY apache/apache.sh /home/apps/apache/

# venv labbook_FE
COPY labbook_FE/Pipfile /home/apps/labbook_FE/labbook_FE

WORKDIR /home/apps/labbook_FE/labbook_FE

RUN python3 -m venv venv

RUN source venv/bin/activate && pip install --upgrade pip && pip install pipenv && pipenv install

# venv labbook_BE
COPY labbook_BE/Pipfile /home/apps/labbook_BE/labbook_BE

WORKDIR /home/apps/labbook_BE/labbook_BE

RUN python3 -m venv venv

RUN source venv/bin/activate && pip install --upgrade pip && pip install pipenv && pipenv install

# install labbook_FE
COPY labbook_FE /home/apps/labbook_FE/labbook_FE

# install labbook_BE
COPY labbook_BE /home/apps/labbook_BE/labbook_BE

CMD ["supervisord", \
     "-c", "/home/supervisor/etc/supervisor.conf", \
     "--pidfile", "/home/supervisor/tmp/supervisor.pid", \
     "--user", "root"]
