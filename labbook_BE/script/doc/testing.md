# Elements for testing backup and restore functions

## Unit tests

Unit tests for `backup.sh` can be run from the project with:

~~~
$ make test
~~~

## Application tests

See below how you can access the LabBook container and volume.

Prepare the environment:

- connect a USB media,
- remove or rename the `SIGL_sauvegardes` directory at the root of the media,
- remove keys in /storage/key

Steps:

- program automatic backup. Verify `user_labbook` crontab.
- initialize media. Verify presence of `SIGL_sauvegardes` directory.
- generate backup key. Verify presence in `/storage/key`.
- backup. Verify presence in `SIGL_sauvegardes`
- restore a LabBook 3 backup.

### Restore a LabBook 2.9 backup

Prepare a media containing only:
- the archive
- clef_sauvegarde.privee.gpg
- files.tar.gz.gpg
- kpri.fingerprint.asc

### Restore a LabBook 2.5 backup

Prepare a media containing only:
- the archive
- clef_sauvegarde.privee.crypt

## Command line access to the LabBook container

For testing purposes you may want to access a running LabBook application.
This is not as easy as connecting to the LabBook system because the application runs inside a container.
The purpose of using containers is to isolate as much as possible the application from the underlying Ubuntu system.

LabBook uses [Podman](https://podman.io/) containers.
You can access the application container from the command line when logged in as `user_labbook`.
This user has special permissions to issue podman commands with sudo without providing its password.

There are 2 containers on a running LabBook 3 system:

~~~
user_labbook@labbook3-test:~$ sudo podman ps
CONTAINER ID  IMAGE                           COMMAND               CREATED         STATUS             PORTS               NAMES
7c52711c247f  localhost/labbook-pod:3.2                             47 minutes ago  Up 47 minutes ago  0.0.0.0:80->80/tcp  ae89404ab911-infra
b07f35f73c26  localhost/labbook-python:3.0.2  supervisord -c /h...  47 minutes ago  Up 47 minutes ago  0.0.0.0:80->80/tcp  labbook_python
~~~

Persistent data are stored in a volume:

~~~
user_labbook@labbook3-test:~$ sudo podman volume ls
DRIVER      VOLUME NAME
local       labbook_storage
~~~

You can connect to the running `labbook_python` container:

~~~
user_labbook@labbook3-test:~$ sudo podman exec -it labbook_python bash
[root@labbook labbook_BE]# 
~~~

You can access the persistent data from the volume which is mounted at `/storage`:

~~~
[root@labbook labbook_BE]# ls /storage
dump  io  key  log  report  resource  upload
~~~ 

Directories of interest in /storage for backup/restore:

- /storage/key contains the GPG keys,
- /storage/io contains exchange files between the backend application and `backup.sh`,
- /storage/log contains logs.

It can be useful to access the volume content from the host.
You can display its mountpoint with:

~~~
user_labbook@labbook3-test:~$ sudo podman volume ls --format '{{.Mountpoint}}'
/var/lib/containers/storage/volumes/labbook_storage/_data
~~~

Dynamic access to removable media is not reliable from the application container,
and therefore other temporary containers are started to perform various backup/restore tasks.
You can see an example in the `user_labbook` crontab when an automatic backup is scheduled:

~~~
user_labbook@labbook3-test:~$ crontab -l
0 12 * * * sudo podman run --rm --tz=local -v /media:/media -v labbook_storage:/storage localhost/labbook-python:3.0.2 /home/apps/labbook_BE/labbook_BE/script/backup.sh -e /storage/io//backup_settings.sh backupauto
~~~

You can also start such a container in interactive mode:

~~~
user_labbook@labbook3-test:~$ sudo podman run -it --rm --tz=local -v /media:/media -v labbook_storage:/storage localhost/labbook-python:3.0.2 bash
[root@76cbb7b9e87f labbook_BE]# ls /media/user_labbook
USB
~~~

The container is removed when you exit the `bash` session.

## Update the labbook-python image

You must be logged in as `sigl`.

Steps:

- stop the application,
- remove the labbook-python image,
- replace the labbook-python image archive in `/home/LabBook_images`,
- start the application.

~~~
sigl@labbook3-test:~$ sudo /usr/bin/systemctl stop labbook

# look for the image id and remove it
sigl@labbook3-test:~$ sudo podman image ls localhost/labbook-python
sigl@labbook3-test:~$ sudo podman rmi image_id_from_above

# or in one step
sigl@labbook3-test:~$ sudo podman rmi $(sudo podman image ls --format '{{.ID}}' localhost/labbook-python)

sigl@labbook3-test:~$ sudo mv /tmp/labbook-python-3.0.2.tar /home/LabBook_images
sigl@labbook3-test:~$ sudo /usr/bin/systemctl start labbook
~~~