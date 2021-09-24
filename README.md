# Project

[LabBook](https://www.lab-book.org/en/) Software helps you computerize your biology laboratory data ensuring better patient care.

This repository contains the material needed to build the LabBook python container image.
It contains two separate python applications that constitute the LabBook application:

- labbook_FE manages the front end,
- labbook_BE exposes backend data through a REST API.

# Requirements

- linux
- podman
- MySQL

# Installation

For the time being, LabBook is developped with several virtual machines.

We are working on a more lightweight setup.

# Usage

To see the available commands :

    make help

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
