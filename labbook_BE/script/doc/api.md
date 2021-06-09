# API used by labbook_BE for backup and restore

## Introduction

labbook_BE uses a script `backup.sh` to execute the various actions needed to perform backups and restores.
This documents describes the API between labbook_BE and `backup.sh`.

Shared definitions between labbook_BE and `backup.sh` are in environment variables.

List of variables with default values:

- LABBOOK_KEY_DIR=/storage/key
- LABBOOK_DB_HOST=10.88.0.1
- LABBOOK_DB_NAME=SIGL
- LABBOOK_DB_USER=root
- LABBOOK_USER=user_labbook
- LABBOOK_STATUS_DIR=/storage/io
- LABBOOK_LOG_DIR=/storage/log

It can be useful during development to fake `backup.sh` commands.
Place command names into these variables to fake execution with status OK or ERROR:

- LABBOOK_TEST_OK=cmd1,cmd2,...
- LABBOOK_TEST_KO=cmd1,cmd2,...

`backup.sh` input is taken from parameters except for keys and passwords to avoid exposing them as parameters:

- GPG private key passphrase in LABBOOK_KEY_PWD
- DB user password in LABBOOK_DB_PWD
- user password in LABBOOK_USER_PWD

Output is written to LABBOOK_STATUS_DIR/name_of_command

- if status = 0 when command produce a simple status output is empty, otherwise it consists of one or more lines of semicolon (;) separated fields
- if status > 0 output is an error message

`backup.sh` writes logfiles into LABBOOK_LOG_DIR/name_of_command (or to stderr if LABBOOK_LOG_DIR is not defined)

`backup.sh` is either started by labbook_BE or by cron for automatic backups:

- when started by labbook_BE, if it needs an access to the media, it has to start in turn another container because media visibility is not dynamic.
- the command in `user_labbook` crontab is also a `podman run` command.

Backup and restore are lengthy operations that are started asynchronously.
They write messages in their status file indicating the operation they are running.
These messages are displayed by the application.

The absolute path to the script is `/home/apps/labbook_BE/labbook_BE/script/backup.sh`.

WARNING : character set of media names is not checked by backup.sh but labbook_BE expects UTF8 encoding.

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
$ LABBOOK_USER_PWD=password \
  backup.sh [-u USER] [-o FILE] -m MEDIA initmedia || echo "error searching for medias"

    -u USER     : connected user with mounted USB device [DEFAULT=LABBOOK_USER]
    -o FILE     : output file [DEFAULT=stdout]
~~~

## List

~~~
$ LABBOOK_USER_PWD=password \
  backup.sh [-u USER] [-o FILE] [-U] listmedia || echo "error searching for medias"

    -u USER     : connected user with mounted USB device [DEFAULT=LABBOOK_USER]
    -o FILE     : output file [DEFAULT=stdout]
    -U          : list uninitialized media

Output: media names

Ex:
USB
~~~

WARNING : character set of media names is not checked by backup.sh but labbook_BE expects UTF8 encoding

~~~
$ LABBOOK_USER_PWD=password \
  backup.sh [-u USER] [-o FILE] -m MEDIA listarchive || echo "error searching for archives"

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
- start backup script in the background
- poll status file, read last line and display backup progress information based on status keyword
- refresh last backup status

Script steps:

- dump DB into LABBOOK_STATUS_DIR
- create archive of DB dump and other files
- encrypts archive to keys present in LABBOOK_KEY_DIR
- result in status file
- touch last_backup_ok if successful

~~~
$ LABBOOK_USER_PWD=password \
  backup.sh [-u USER] [-o FILE] [-m MEDIA] [-s FILE] [-d DIR] [-b DATABASE] [-p PATTERN ...] backup && echo "backup was successful"

    -u USER     : connected user with mounted USB device [DEFAULT=LABBOOK_USER]
    -o FILE     : output file [DEFAULT=stdout]
    -m MEDIA    : media to store backup to. If absent, there should be only one initialized media.
    -s FILE     : status file
    -d DIR      : directory containing GPG keys [DEFAULT=LABBOOK_KEY_DIR]
    -b DATABASE : database [DEFAULT=LABBOOK_DB_NAME]
    -p PATTERN  : file patterns to backup (can be repeated). If absent use predefined list.

The backup is a gpg encrypted archive in the form `backup_v30_database_timestamp.tar.gz.gpg` containing
  - dump/dump.sql
  - report/
  - upload/
  - resource/

Output backup steps in status file:

START;YYYY-MM-DD HH:MM:SS;PID
DUMPDB;YYYY-MM-DD HH:MM:SS
MAKEARCHIVE;YYYY-MM-DD HH:MM:SS
COPYKEYS;YYYY-MM-DD HH:MM:SS
OK;YYYY-MM-DD HH:MM:SS
or
ERR;YYYY-MM-DD HH:MM:SS;message
~~~

## Restore

UX:

- message quit all other LabBook instances
- choose media
- choose archive
- enter private key passphrase
- start restore script in the background
- poll status file, read last line and display restore progress information based on status keyword
- (if restore successful) message prepare for application restart

Restore steps:

- decrypt backup
- restore DB
- restore files
- exit value is status
- exit message in file

~~~
$ LABBOOK_KEY_PWD=passphrase \
  LABBOOK_USER_PWD=password \
  LABBOOK_KEY_DIR=dir \
  LABBOOK_DB_NAME=name \
  backup.sh -m MEDIA -a ARCHIVE [-u USER] [-s FILE] restore && echo "restored successfully"

    -u USER     : connected user with mounted USB device [DEFAULT=LABBOOK_USER]
    -m MEDIA    : media to restore backup from. If absent, there should be only one initialized media.
    -a ARCHIVE  : encrypted archive to restore from
    -s FILE     : status file

Output restore steps in status file:

START;YYYY-MM-DD HH:MM:SS;PID
DECRYPT;YYYY-MM-DD HH:MM:SS
EXTRACTDB;YYYY-MM-DD HH:MM:SS
LOADDB;YYYY-MM-DD HH:MM:SS
RESTOREFILES;YYYY-MM-DD HH:MM:SS
OK;YYYY-MM-DD HH:MM:SS
or
ERR;YYYY-MM-DD HH:MM:SS;message

$ LABBOOK_USER_PWD=password backup.sh [-u USER] restart || echo "Failed to restart container"

    -u USER     : user authorized to restart LabBook container without providing sudo password [DEFAULT=LABBOOK_USER]
~~~

## Program daily backup

UX:

- choose a time
- ask for LABBOOK_USER password

~~~
$ LABBOOK_USER_PWD=password backup.sh -w WHEN [-u USER] [-V VOLUME] progbackup || echo "Failed to program daily backup"

    -w WHEN     : time in the form HH:MM
    -u USER     : user [DEFAULT=LABBOOK_USER]
    -V VOLUME   : volume name [DEFAULT=Labbook_space]
~~~
