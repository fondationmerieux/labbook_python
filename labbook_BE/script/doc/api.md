# API used by labbook_BE for backup and restore

## Introduction

labbook_BE uses a script `backup.sh` to execute the various actions needed to perform backups and restores.
This documents describes the API between labbook_BE and `backup.sh`.

Shared definitions between labbook_BE and `backup.sh` are in environment variables:

- LABBOOK_KEY_DIR=/storage/key
- LABBOOK_DB_HOST=10.88.0.1
- LABBOOK_DB_NAME=SIGL
- LABBOOK_DB_USER=root
- LABBOOK_USER=user_labbook
- LABBOOK_STATUS_DIR=/storage/io
- LABBOOK_LOG_DIR=/storage/log

It can be useful during development to fake `backup.sh` commands.
Place command names into these variables to fake execution with status OK or ERROR:

- LABBOOK_TEST_OK=command[,...]
- LABBOOK_TEST_KO=command[,...]

`labbook.sh` input is taken from parameters except for:

- GPG private key passphrase in LABBOOK_KEY_PWD
- DB user password in LABBOOK_DB_PWD

Output: depends on status

- if status = 0 output is empty or consists of one or more lines of semicolon (;) separated fields
- if status > 0 output is an error message

backup.sh writes a logfile into LABBOOK_LOG_DIR/backup.out (or to stderr if LABBOOK_LOG_DIR is not defined)

Scripts are in DIR_SCRIPTS=/usr/local/bin (not shared with Labbook_BE)

## Check GPG key exist

~~~
$ backup.sh [-d DIR] keyexist && echo "key exists"

    -d DIR    : directory containing GPG keys [DEFAULT=LABBOOK_KEY_DIR]
~~~

## Generate GPG keypair

~~~
$ LABBOOK_KEY_PWD=passphrase backup.sh [-d DIR] [-s FILE] genkey && echo "key generated successfully"

    -d DIR    : directory containing GPG keys [DEFAULT=LABBOOK_KEY_DIR]
    -s FILE   : status file [DEFAULT=LABBOOK_STATUS_DIR/genkey]
~~~

## Init media structure

Useful to avoid writing to a media that is not intended for backup

~~~
$ backup.sh [-u USER] [-o FILE] -m MEDIA initmedia || echo "error searching for medias"

    -u USER     : connected user with mounted USB device [DEFAULT=LABBOOK_USER]
    -o FILE     : output file [DEFAULT=stdout]
~~~

## List

~~~
$ backup.sh [-u USER] [-o FILE] [-U] listmedia || echo "error searching for medias"

    -u USER     : connected user with mounted USB device [DEFAULT=LABBOOK_USER]
    -o FILE     : output file [DEFAULT=stdout]
    -U          : list uninitialized media

Output: media names

Ex:
USB
~~~

~~~
$ backup.sh [-u USER] [-o FILE] -m MEDIA listarchive || echo "error searching for archives"

    -u USER     : connected user with mounted USB device [DEFAULT=LABBOOK_USER]
    -o FILE     : output file [DEFAULT=stdout]
    -m MEDIA    : media to search for backups

Output: archive names

Ex:
backup_SIGL_2018-04-13_15h58m51s.tar.gz
backup_SIGL_2018-04-13_15h58m52s.tar.gz
backup_SIGL_2018-04-13_15h58m53s.tar.gz
backup_SIGL_2018-04-13_16h01m19s.tar.gz
backup_SIGL_2018-04-13_16h03m12s.tar.gz
backup_SIGL_2018-04-13_16h06m42s.tar.gz
backup_SIGL_2018-04-13_16h08m21s.tar.gz
backup_SIGL_2018-04-13_16h10m02s.tar.gz
backup_SIGL_2018-04-13_18h38m32s.tar.gz
backup_SIGL_2018-04-13_18h46m16s.tar.gz
backup_SIGL_2018-04-15_16h54m15s.tar.gz
backup_SIGL_2018-04-24_15h55m54s.tar.gz
backup_SIGL_2018-04-25_09h11m57s.tar.gz
backup_SIGL_2018-04-26_13h46m54s.tar.gz
backup_SIGL_2018-05-03_13h51m04s.tar.gz
~~~

## Backup

UX:

- choose media
- refresh last backup status

Script steps:

- dump DB
- create archive from DB dump file and other files
- encrypts archive to keys present in directory
- result in last_backup file

~~~
$ backup.sh [-u USER] [-o FILE] [-m MEDIA] [-s FILE] [-d DIR] [-b DATABASE] [-p PATTERN ...] backup && echo "backup was successful"

    -u USER     : connected user with mounted USB device [DEFAULT=LABBOOK_USER]
    -o FILE     : output file [DEFAULT=stdout]
    -m MEDIA    : media to store backup to. If absent, there should be only one initialized media.
    -s FILE     : status file
    -d DIR      : directory containing GPG keys [DEFAULT=LABBOOK_KEY_DIR]
    -b DATABASE : database [DEFAULT=LABBOOK_DB_NAME]
    -p PATTERN  : file patterns to backup (can be repeated). If absent use predefined list.

The backup is a gpg encrypted archive in the form `backup_v30_database_timestamp.tar.gz.gpg` containing
  - db/dump.sql : database dump
  - files/...   : files

Output:
OK;YYYY-MM-DD HH:MM:SS
or
ERROR;YYYY-MM-DD HH:MM:SS;message
~~~

## Restore

UX:

- message quit all other LabBook instances
- choose media
- choose archive
- enter private key passphrase
- (if restore successful) message prepare for application restart, enter user password

Script steps:

- decrypt backup
- restore DB
- restore files
- exit value is status
- exit message in file
- container restart

~~~
$ LABBOOK_KEY_PWD=passphrase backup.sh -m MEDIA -a ARCHIVE \
                                       [-u USER] [-o FILE]  [-s FILE] [-d DIR] [-b DATABASE] [-p PATTERN ...] \
                                       restore && echo "restored successfully"

    -u USER     : connected user with mounted USB device [DEFAULT=LABBOOK_USER]
    -o FILE     : output file [DEFAULT=stdout]
    -m MEDIA    : media to restore backup from. If absent, there should be only one initialized media.
    -a ARCHIVE  : encrypted archive to restore from
    -s FILE     : status file
    -d DIR      : directory containing GPG keys [DEFAULT=LABBOOK_KEY_DIR]
    -b DATABASE : database [DEFAULT=LABBOOK_DB_NAME]

$ LABBOOK_USER_PWD=password backup.sh [-u USER] restart || echo "Failed to restart container"

    -u USER     : user authorized to restart LabBook container without providing sudo password [DEFAULT=LABBOOK_USER]
~~~

## NOTES

### Distinguishing 2.5, 2.9 and 3.0 backups

2.5 and 2.9 database backups have identical names in the form `backup_SIGL_timestamp.tar.gz` like :

backup_SIGL_2018-05-30_01h40m57s.tar.gz

Apart from backup .tar.gz files, content differs with LabBook version.

LabBook 2.5 backups contain:

- clef_sauvegarde.privee.crypt
- clef_sauvegarde.public.crypt

LabBook 2.9 backups contain:

- clef_sauvegarde.privee.gpg
- .asc public and private gpg keys
- files.tar.gz.gpg

LabBook 3.0 backups contain:

- gpg encrypted archive in the form `backup_v30_SIGL_timestamp.tar.gz.gpg` containing
  - db/dump.sql
  - storage/...
- .asc public and private gpg keys

### Restart from container

#### Requirements

- User user_labbook has to be created as before because it must login to mount the USB device.
- /etc/sudoers.d/labbook-config must mention the restart command as in:
  Cmnd_Alias LABBOOK_RESTART = /usr/sbin/service labbook restart
  user_labbook ALL = NOPASSWD: LABBOOK_RESTART
- ssh client and sshpass must be available in container

#### Execution

~~~
sigl@labbook-test:~$ sudo podman exec -it f533b07f1db2 bash

# option StrictHostKeyChecking=no to avoid question
[root@labbook /]# ssh -o "StrictHostKeyChecking no" user_labbook@10.88.0.1 sudo service labbook restart
Warning: Permanently added '10.88.0.1' (ECDSA) to the list of known hosts.
user_labbook@10.88.0.1's password: 
sigl@labbook-test:~$ 

# not yet...
sigl@labbook-test:~$ sudo podman ps
CONTAINER ID  IMAGE   COMMAND  CREATED  STATUS  PORTS   NAMES

# OK
sigl@labbook-test:~$ sudo podman ps
CONTAINER ID  IMAGE                            COMMAND               CREATED         STATUS             PORTS               NAMES
2950376294f3  localhost/labbook-python:v3.0.0  supervisord -c /h...  9 seconds ago   Up 9 seconds ago   0.0.0.0:80->80/tcp  labbook_python
f533b07f1db2  localhost/labbook-php:v3.0.0     /usr/bin/python /...  10 seconds ago  Up 10 seconds ago  0.0.0.0:80->80/tcp  labbook_php
a5fb35eeeeb2  localhost/labbook-pod:3.2                              11 seconds ago  Up 10 seconds ago  0.0.0.0:80->80/tcp  cd840df46780-infra
~~~

### Run script in another container

#### From the host

~~~
sigl@labbook3-test:~$ sudo podman run --rm -v "/media:/media" localhost/labbook-python:v3.0.1 ls -R /media/user_labbook > /tmp/out
~~~

#### From a container

~~~
sigl@labbook3-test:~$ sudo podman exec -it labbook_php bash
[root@labbook /]# 

[root@labbook /]# ssh -o "StrictHostKeyChecking no" user_labbook@10.88.0.1 \
   sudo podman run --rm -v "/media:/media" localhost/labbook-python:v3.0.1 ls -R /media/user_labbook > /tmp/out
~~~

### QUESTIONS


### TODO

- try final commands above when container with ssh and sshpass is available,
  which (with password in SSHPASS env variable) should by like :
  # sshpass -e sh -o "StrictHostKeyChecking no" user_labbook@10.88.0.1 sudo service labbook restart
- use environment to share definitions (paths, DB name, DB credentials, ...) between Labbook_BE and backup
- pass environment when running script in another container
