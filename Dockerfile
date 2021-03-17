FROM centos

# permanent files (manuals, reports, logo ...)
COPY storage /storage

COPY vendor/*.rpm /tmp

# may have to add openssl libssl.so.10 before compat-openssl10
RUN yum update -y && yum install -y \
    compat-openssl10 \
    binutils \
    glibc-devel \
    mysql \
    python36 \
    which \
    openssh-clients \
    httpd \
    /tmp/wkhtmltox-0.12.5-1.centos8.x86_64.rpm

# EPEL repository is needed for sshpass
RUN yum install -y epel-release

RUN yum install -y sshpass

# install supervisor
RUN pip3 install supervisor

RUN mkdir -p /home/supervisor/log \
             /home/supervisor/tmp \
             /home/apps/labbook_FE/labbook_FE \
             /home/apps/labbook_BE/labbook_BE

COPY supervisor/etc /home/supervisor/etc

# install venv labbook_FE
COPY labbook_FE/requirements.txt /home/apps/labbook_FE/labbook_FE

WORKDIR /home/apps/labbook_FE/labbook_FE

RUN python3 -m venv venv

RUN source venv/bin/activate && pip install -r requirements.txt

# install venv labbook_BE
COPY labbook_BE/requirements.txt /home/apps/labbook_BE/labbook_BE

WORKDIR /home/apps/labbook_BE/labbook_BE

RUN python3 -m venv venv

RUN source venv/bin/activate && pip install -r requirements.txt

# install labbook_FE
COPY labbook_FE /home/apps/labbook_FE/labbook_FE

# install labbook_BE
COPY labbook_BE /home/apps/labbook_BE/labbook_BE

CMD ["supervisord", \
     "-c", "/home/supervisor/etc/supervisor.conf", \
     "--logfile", "/home/supervisor/log/supervisor.log", \
     "--pidfile", "/home/supervisor/tmp/supervisor.pid", \
     "--user", "root"]
