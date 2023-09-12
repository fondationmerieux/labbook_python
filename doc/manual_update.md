# Update the labbook-python image

You must be logged in as `sigl`.

Steps:

- stop the application,
- remove the labbook-python image,
- replace the labbook-python image archive in `/home/LabBook_images`,
- start the application.

ATTENTION: When the application starts, it upgrades the database if necessary.
But downgrading the database is not supported, you should not install an image from a previous version.

~~~
# verify initial state
sigl@labbook3-test:~$ sudo podman ps
CONTAINER ID  IMAGE                           COMMAND               CREATED        STATUS            PORTS               NAMES
b5db8a0daff3  localhost/labbook-pod:3.2                             3 minutes ago  Up 3 minutes ago  0.0.0.0:80->80/tcp  18b0b7e4e7cf-infra
913b6b12cf9d  localhost/labbook-python:3.0.1  supervisord -c /h...  3 minutes ago  Up 3 minutes ago  0.0.0.0:80->80/tcp  labbook_python

# stop labbook
sigl@labbook3-test:~$ sudo /usr/bin/systemctl stop labbook

# all running containers should have been stopped
sigl@labbook3-test:~$ sudo podman ps
CONTAINER ID  IMAGE   COMMAND  CREATED  STATUS  PORTS   NAMES
sigl@labbook3-test:~$ 

# look for the image id and remove it
sigl@labbook3-test:~$ sudo podman image ls localhost/labbook-python
sigl@labbook3-test:~$ sudo podman rmi image_id_from_above

# or in one step
sigl@labbook3-test:~$ sudo podman rmi $(sudo podman image ls --format '{{.ID}}' localhost/labbook-python)

# install the new image
sigl@labbook3-test:~$ sudo mv /tmp/labbook-python-3.0.2.tar /home/LabBook_images

# start labbook
sigl@labbook3-test:~$ sudo /usr/bin/systemctl start labbook
~~~
