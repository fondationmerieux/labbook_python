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

If you are interested in the production setup you may find some useful information in [this document](doc/architecture.md).

## Clone the repository

~~~
git clone https://github.com/fondationmerieux/labbook_python.git
~~~

## Configuration file

Labbook reads its configuration from a file named `labbook.conf` which can be located at:

- `$HOME/.config/labbook.conf`
- `$HOME/labbook.conf`

Contents:

- `LABBOOK_DB_USER`: database user name
- `LABBOOK_DB_PWD`: database user password
- `LABBOOK_DB_NAME`: database name
- `LABBOOK_DB_HOST`: database host as seen from the container
- `LABBOOK_DEBUG`: if 1 runs gunicorn with reload option
- `LABBOOK_TEST_OK`: backup.sh commands (com1,com2,...) to fake with OK status
- `LABBOOK_TEST_KO`: backup.sh commands (com1,com2,...) to fake with ERROR status
- `LABBOOK_URL_PREFIX`: set it to replace `sigl` in LabBook URLs in development mode

Example:

~~~
$ cat ~/.config/labbook.conf
LABBOOK_DB_USER=labbook
LABBOOK_DB_PWD=iTpRPQfIxZWQGg
LABBOOK_DB_NAME=SIGL
LABBOOK_DB_HOST=10.88.0.1
LABBOOK_DEBUG=1
LABBOOK_TEST_OK=
LABBOOK_TEST_KO=
~~~

A sample file is provided in `doc/labbook.conf.sample`.

### Testing backup and restore functions in your current environment

In order to test backup/restore functions directly in your current environment you may have to modify some defaults.
A few additional configuration variables are available in `labbook.conf`:

- `LABBOOK_USER`: to replace `user_labbook`
- `LABBOOK_MEDIA_DIR`: to replace `/media` for mounted removable media
- `LABBOOK_ROOTLESS`: set it to 1 if you run podman in rootless mode
- `LABBOOK_DUMP_COL_STATS`: set it to 0 to add `--column-statistics=0` to mysqldump arguments. This may be necessary for mysqldump >= 8.

Notes:

- LabBook will replace the `LABBOOK_USER` crontab when you use the "MODIFY SAVE TIME" button
- LabBook will keep asking you for the "user_labbook" password even if you provide a different user in the `LABBOOK_USER` configuration variable.
Just enter the password for the user specified in the `LABBOOK_USER` configuration variable.
- Because backup.sh spawns commands in new containers for which there is no mapping of the working tree, you must rebuild the image with `make devbuild` every time you modify backup.sh.
- After a restore, the automatic restart will not work in the development environment, you have to manually restart the application with `make devstop` and `make devrun`.
- Depending on the rootful or rootless podman configuration on your system the database host as seen from the container varies. The examples above are from a rooful configuration. In a rootless configuration the database host as seen from the container is probably the host network address.

## Database setup

### Database users

LabBook, running from the container, connects as `LABBOOK_DB_USER` value to the database on the host.
We must grant access to this user from the container.

You also need to access the database from the host, to load a demo database for example.
We must grant access to this user from the host either.

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

MariaDB [(none)]> CREATE USER myuser@localhost IDENTIFIED BY 'mypass';
Query OK, 0 rows affected (0.008 sec)

MariaDB [(none)]> GRANT ALL PRIVILEGES ON *.* TO myuser@localhost;
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
  make build [VERSION=version]       build image localhost/labbook-python:version from v3.3.7 tag
  make save [VERSION=version]        save image localhost/labbook-python:version to /tmp/labbook-python-version.tar,
                                     compress tar to tar.xz and compute md5sums for them
  make clean [VERSION=version]       remove image localhost/labbook-python:version
Default version value in VERSION file=3.3.7 TAG_NAME=v3.3.7

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

### Notes

#### LabBook uses a storage volume to hold various files.

The initial content of the volume is stored in the `./storage` directory of the source tree.
In order to prevent modification of this directory it is replicated to a `DEVRUN_STORAGE` directory before mounting it into the container.
`DEVRUN_STORAGE=./devrun_storage` by default, you can modify it by setting the `DEVRUN_STORAGE` environment variable.

#### Missing configuration file

If the configuration file cannot be found or if a parameter is missing an error is displayed when you invoke make:

~~~
$ make help
Makefile:23: *** LABBOOK_DB_USER undefined.  Stop.
~~~

#### Log directories

`make devrun` creates the log directories `./logs` if necessary
and mounts them into the container to facilitate access and to preserve logs across restarts.
The `logs` directories are ignored by git.

#### Connecting to the database

`make dbinit` connects to the database from the host, whereas the application connects from the container.

`make dbtest` can be used to test the connection to the database from the host.

In order to test the connection to the database from the container,
you can open an interactive bash session into the container and invoke mysql manually like:

~~~
# subsitute LABBOOK_DB_... with their respective values
$ podman exec -it labbook_python bash
[root@labbook labbook_BE]# mysql -u LABBOOK_DB_USER -p LABBOOK_DB_HOST
Enter password:
...
mysql>
~~~

# Documentation

Documentation provided here is exclusively technical, and in a very partial and early state.

Extensive [Manuals](https://www.lab-book.org/en/resources/?type=user_manual) and [Tutorials](https://www.lab-book.org/en/resources/?type=tutorial)
for the LabBook application can be found at the [LabBook website](https://www.lab-book.org/en/).

Interactive API documentation for the LabBook backend is available at the following url: YOUR_LABBOOK_URL/sigl/api

## Changes

You can have a look at [CHANGELOG.md](CHANGELOG.md) for changes to the program.

Changes to the analyses repository are documented in [analyzes.md](doc/analyzes.md)

## Production architecture

The architecture of the standard LabBook installation is described in [architecture.md](doc/architecture.md).

## Manual update

Manually updating a LabBook container with an archive obtained from a `make save` command is described in [manual_update.md](doc/manual_update.md).

## Backups

The API between labbook_BE and the script performing backup and restore actions is decribed in [backup_api.md](doc/backup_api.md).

Information about GPG keys used for encrypting backups can be found in [extra_key.md](doc/extra_key.md)

A few elements about testing backup and restore functions and accessing the LabBook python container are available in [backup_testing.md](doc/backup_testing.md)

## Exports

Elements for configuring:

- the epidemiological report [epidemio.md](doc/epidemio.md)
- the DHIS2 export [dhis2.md](doc/dhis2.md)
- the indicator report [indicator.md](doc/indicator.md)

## Database

Significant tables are documented in [tables.md](doc/tables.md) (partly in French)

## Imports

List of detailed import schemes are documented in [import.md](doc/import.md)

## Running LabBook behind your own web server

In the production environment, when LabBook is installed on a dedicated Ubuntu system from the provided ISO,
the application container is started with a mapping of the 80 port,
so that all requests on http://<labbook_host> are handled by the apache server that runs inside the container.

You can run LabBook behind your own web server by proxying requests from `<your_web_server>/sigl` to `http://<labbook_host>/sigl`.
A sample configuration for Apache is available, see [this file](doc/apache_proxy.conf.sample).

Notes:

- even though by proxying it behind an https enabled web server, you may provide access to your LabBook server over the internet,
THIS IS NOT SUPPORTED for security reasons.
You should also consider your local legal constraints for hosting personal health care data and providing access to it over the internet.
- you can change the default `/sigl` prefix for LabBook URLs with the `LABBOOK_URL_PREFIX` configuration variable.
This works only for images built with `make devbuild`.

# Contributing

We happily accept contributions but we opened this repository only very recently so we have a long way to go to make contributing easy.

Feel free to open issues when things are confused.

# Licence

[GNU General Public License v2.0](LICENSE.md)
