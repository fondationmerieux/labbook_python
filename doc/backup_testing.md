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

If you don't have access to a physical USB port, you can simulate a connected USB drive.
Being logged in as `sigl`:

~~~
# you can replace USB with whatever media name you want to use
$ sudo install --owner=user_labbook --group=user_labbook --mode=755 \
               --directory /media/user_labbook /media/user_labbook/USB
~~~


### Basic tests

- program automatic backup. Verify `user_labbook` crontab.
- initialize media. Verify presence of `SIGL_sauvegardes` directory.
- generate backup key. Verify presence in `/storage/key`, backup button becomes active.
- backup. Verify presence in `SIGL_sauvegardes` and last backup information update.
- restore a LabBook 3 backup.
- automatic backup. Verify presence in `SIGL_sauvegardes` and last backup information update.

### Restore a LabBook 2.9 backup

Prepare a media containing only:

- the archive
- clef_sauvegarde.privee.gpg
- files.tar.gz.gpg
- kpri.fingerprint.asc

Verify:

- files have been restored in /storage/report and /storage/upload
- database has been upgraded in /storage/log/alembic.out

### Restore a LabBook 2.5 backup

Prepare a media containing only:
- the archive
- clef_sauvegarde.privee.crypt

Verify:

- database has been upgraded in /storage/log/alembic.out

### Verify trusted tier decrypt

If you have access to the `fondation-merieux` private key you can verify that you can decrypt a backup
as described in [extra_key.md](extra_key.md).

### Additional tests

- automatic backup with no media.
- automatic backup with uninitialized media.

Verify last backup ERR information on screen.

## <a name="exec_bash"></a>Command line access to the LabBook container

For testing or debugging purposes you may want to access a running LabBook application.
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

## Reload database dump

You may want to restore your LabBook database from a SQL dump file.
This file may be the result of a previous dump or backup.

Steps:

- you must be logged in as `user_labbook`.
- open a bash session into the running LabBook container [as explained here](#exec_bash),
- invoke the internal command `loaddb` from `backup.sh` with the path of the SQL dump file.
- restart the container

ATTENTION: this command drops and recreates the database. All data will be lost.

~~~
# open a bash session
user_labbook@labbook3-test:~$ sudo podman exec -it labbook_python bash

# setup the environment needed to access the database
export LABBOOK_DB_NAME=SIGL
export LABBOOK_DB_HOST=10.88.0.1
export LABBOOK_DB_USER=xxxxx
export LABBOOK_DB_PWD=xxxxx

# drop/create the database and load from SQL dump
[root@labbook labbook_BE]# script/backup.sh -i /storage/dump/dump.sql loaddb

# setup the environment needed to restart the container
export LABBOOK_USER=user_labbook
export LABBOOK_USER_PWD=xxxxx

# restart the container
[root@labbook labbook_BE]# script/backup.sh restart

# if the previous command is successful, the container having been stopped
# you should return to your user_labbook session
user_labbook@labbook3-test:~$
~~~
