FROM almalinux

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
    /tmp/wkhtmltox-0.12.5-1.centos8.x86_64.rpm

RUN yum clean all

RUN yum install -y sshpass

RUN yum install -y mod_ssl

RUN yum install -y unoconv

RUN yum clean all

# install supervisor
RUN pip3 install supervisor

RUN mkdir -p /home/supervisor/log \
             /home/supervisor/tmp \
             /home/apps/labbook_FE/labbook_FE \
             /home/apps/labbook_BE/labbook_BE

COPY supervisor/etc /home/supervisor/etc

RUN ln -s /storage /var/www/html/

RUN echo  "alias ls='ls --color=auto'" >> /root/.bashrc
RUN echo  "alias l.='ls -d .* --color=auto'" >> /root/.bashrc
RUN echo  "alias l='ls -CF'" >> /root/.bashrc
RUN echo  "alias la='ls -A'" >> /root/.bashrc
RUN echo  "alias ll='ls -alF'" >> /root/.bashrc

COPY etc/httpd/conf/httpd.conf /etc/httpd/conf/
COPY etc/httpd/conf.d/ssl.conf /etc/httpd/conf.d/

RUN mkdir -p /home/apps/apache

COPY apache/apache.sh /home/apps/apache/

# venv labbook_FE
COPY labbook_FE/Pipfile.lock /home/apps/labbook_FE/labbook_FE

WORKDIR /home/apps/labbook_FE/labbook_FE

RUN python3 -m venv venv

RUN source venv/bin/activate && pip install pipenv && pipenv install --ignore-pipfile

# venv labbook_BE
COPY labbook_BE/Pipfile.lock /home/apps/labbook_BE/labbook_BE

WORKDIR /home/apps/labbook_BE/labbook_BE

RUN python3 -m venv venv

RUN source venv/bin/activate && pip install pipenv && pipenv install --ignore-pipfile

# install labbook_FE
COPY labbook_FE /home/apps/labbook_FE/labbook_FE

# install labbook_BE
COPY labbook_BE /home/apps/labbook_BE/labbook_BE

CMD ["supervisord", \
     "-c", "/home/supervisor/etc/supervisor.conf", \
     "--logfile", "/home/supervisor/log/supervisor.log", \
     "--pidfile", "/home/supervisor/tmp/supervisor.pid", \
     "--user", "root"]
