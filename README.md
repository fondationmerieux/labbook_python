This repository contains the material needed to build the docker labbook Python image.

To see the available commands :

    make help

You can have a look at [CHANGELOG.md](CHANGELOG.md) for changes.

There is some documentation about backups:

- the API between labbook_BE and the script performing backup and restore actions in [api.md](labbook_BE/script/doc/api.md)
- information about GPG keys used for encrypting backups in [extra_key.md](labbook_BE/script/doc/extra_key.md)
- a few elements about testing backup and restore functions in [testing.md](labbook_BE/script/doc/testing.md)


There is some documentation about analyzes repository:

- list of analyzes that could conflict with existing in a backup during a restore [ANALYZES.md](ANALYZES.md)


There is some documentation about epidemiological settings:

- describes how to configure the epidemiological report [EPIDEMIO.md](EPIDEMIO.md)


There is some documentation about DHIS2 settings:

- describes how to configure a spreadsheet for DHIS2 export [DHIS2.md](DHIS2.md)


There is some documentation about tables used in database of this application:

- describes tables [TABLES.md](labbook_BE/TABLES.md)
