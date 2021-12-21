# Project

<!---
Keep the sentence synchronised with the sentence in the linked page
-->
[LabBook](https://www.lab-book.org/en/) Software helps you computerize your biology laboratory data ensuring better patient care.

This repository contains the material needed to build the LabBook python container image.
It contains two separate python applications that constitute the LabBook application:

- labbook_FE manages the front end,
- labbook_BE exposes backend data through a REST API.

# Requirements

- linux
- podman
- MySQL or MariaDB
- make
- git

# Installation and usage

The development setup mirrors the production setup with the application running in a container that connects to the database on the host.

## Clone the repository

~~~
git clone https://github.com/fondationmerieux/labbook_python.git
~~~

## Configuration file

Labbook reads its configuration from a file named `labbook.conf` which can be located at:

- `$HOME/.config/labbook.conf`
- `$HOME/labbook.conf`

Contents:

- `LABBOOK_DB_USER` : database user name
- `LABBOOK_DB_PWD` : database user password
- `LABBOOK_DB_NAME` : database name
- `LABBOOK_DB_HOST` : database host as seen from the container

Example:

~~~
$ cat ~/.config/labbook.conf 
LABBOOK_DB_USER=labbook
LABBOOK_DB_PWD=iTpRPQfIxZWQGg
LABBOOK_DB_NAME=SIGL
LABBOOK_DB_HOST=10.88.0.1
~~~

## Database setup

### Database user

LabBook, running from the container, connects as `LABBOOK_DB_USER` value to the database on the host.
We must grant access to this user from the container.

~~~
# for this example
LABBOOK_DB_USER=myuser
LABBOOK_DB_PWD=mypass

$ mysql -u root -p -h localhost
Enter password:
[...]
MariaDB [(none)]> CREATE USER myuser@'10.88.%.%' IDENTIFIED BY 'mypass';
Query OK, 0 rows affected (0.008 sec)

MariaDB [(none)]> GRANT ALL PRIVILEGES ON *.* TO myuser@'10.88.%.%';
Query OK, 0 rows affected (0.008 sec)

MariaDB [(none)]> FLUSH PRIVILEGES;
Query OK, 0 rows affected (0.008 sec)
~~~

### sql_mode

Clear the sql_mode parameter in your `.cnf` configuration file.

For example for MariaDB version 10.3.17

~~~
# in /etc/my.cnf.d/mariadb-server.cnf 
...
[mariadb]
sql_mode=''
...
~~~

## Commands available

~~~
$ make help
Usage:

When shipping an image:
  make build [VERSION=version]       build image localhost/labbook-python:version from v3.1.1 tag
  make save [VERSION=version]        save image localhost/labbook-python:version to /tmp/labbook-python-version.tar,
                                     compress tar to tar.xz and compute md5sums for them
  make clean [VERSION=version]       remove image localhost/labbook-python:version
Default version value in VERSION file=3.1.1 TAG_NAME=v3.1.1

For developers:
  make dbtest        test connection to MySQL with username=myuser password=mypass
  make dbinit        initialize SIGL database from etc/sql/demo_dump.sql
  make devbuild      build image localhost/labbook-python:latest from working directory
  make devclean      remove image localhost/labbook-python:latest
  make devrun        run the application access from http://localhost:5000/sigl
  make devstop       stop the application
~~~

The commands in the first group are used to build an image in order to release a LabBook version.

The second group of commands provides a few shortcuts when working on LabBook development.
The more useful are:

- `make dbinit` creates and loads the database used at [the LabBook demo](http://demo.lab-book.org/).
- `make devbuild` builds an image from the files in the working directory with the same `Dockerfile` used for building production images.
- `make devrun` runs a container from the image built by `make devbuild` but it substitutes some directories in the container
 with the current ones. This way if you reload the page you're currently on, you get the current version of it.
 Please note that you should take a look at the actual list of directories mapped into the container from the `Makefile`
 or the `make devrun` output. To reflect changes from any other file into the application you need to rebuild the image.

Note1: LabBook uses a storage volume to hold various files.
The initial content of the volume is stored in the `./storage` directory of the source tree.
In order to prevent modification of this directory it is replicated to a `DEVRUN_STORAGE` directory before mounting it into the container.
`DEVRUN_STORAGE=./devrun_storage` by default, you can modify it by setting the `DEVRUN_STORAGE` environment variable.

Note2: if the configuration file cannot be found an error is displayed when you invoke make:
~~~
$ make help
Makefile:23: *** LABBOOK_DB_USER undefined.  Stop.
~~~


# Documentation

Documentation provided here is exclusively technical, and in a very partial and early state.

Extensive [Manuals](https://www.lab-book.org/en/resources/?type=user_manual) and [Tutorials](https://www.lab-book.org/en/resources/?type=tutorial)
for the LabBook application can be found at the [LabBook website](https://www.lab-book.org/en/).

## Changes

You can have a look at [CHANGELOG.md](CHANGELOG.md) for changes to the program.

Changes to the analyses repository are documented in [analyzes.md](doc/analyzes.md)

## Backups

The API between labbook_BE and the script performing backup and restore actions is decribed in [backup_api.md](doc/backup_api.md).

Information about GPG keys used for encrypting backups can be found in [extra_key.md](doc/extra_key.md)

A few elements about testing backup and restore functions and accessing the LabBook python container are available in [backup_testing.md](doc/backup_testing.md)

## Exports

Elements for configuring:

- the epidemiological report [epidemio.md](doc/epidemio.md)
- the DHIS2 export [dhis2.md](doc/dhis2.md)

## Database

Significant tables [tables.md](doc/tables.md) (partly in French)

# Contributing

We happily accept contributions but we opened this repository only very recently so we have a long way to go to make contributing easy.

Feel free to open issues when things are confused.

# Licence

[GNU General Public License v2.0](LICENSE.md)
