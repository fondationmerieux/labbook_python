FROM centos

# may have to add openssl libssl.so.10 before compat-openssl10
RUN yum update && yum install -y \
    compat-openssl10 \
    binutils \
    glibc-devel \
    mysql \
    python36

# install supervisor
RUN pip3 install supervisor

RUN mkdir -p /home/supervisor/log \
             /home/supervisor/tmp

COPY supervisor/etc /home/supervisor/etc

# install venv labbook_FE
COPY labbook_FE/requirements.txt /home/apps/labbook_FE/labbook_FE

WORKDIR /home/apps/labbook_FE/labbook_FE

RUN python3 -m venv venv

RUN source venv/bin/activate

RUN pip install -r requirements.txt

RUN deactivate

# install venv labbook_BE
COPY labbook_BE/requirements.txt /home/apps/labbook_BE/labbook_BE

WORKDIR /home/apps/labbook_BE/labbook_BE

RUN python3 -m venv venv

RUN source venv/bin/activate

RUN pip install -r requirements.txt

RUN deactivate

# install labbook_FE
COPY labbook_FE /home/apps/labbook_FE/labbook_FE

# install labbook_BE
COPY labbook_BE /home/apps/labbook_BE/labbook_BE

CMD ["supervisord", \
     "-c", "/home/supervisor/etc/supervisor.conf", \
     "--logfile", "/home/supervisor/log", \
     "--pidfile", "/home/supervisor/tmp", \
     "--user", "root"]
