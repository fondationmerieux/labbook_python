h Extra key for restoring LabBook GPG backups

## Context

Starting with version 2.9.0, LabBook backups are encrypted using GPG, which allows multiple recipients when encrypting.
LabBook backups are therefore encrypted to the local public key as well as any other public key available.
LabBook is distributed with a special `fondation-merieux` key which allows [Fondation Mérieux](www.fondation-merieux.org)
to be able to decrypt a backup should the passphrase to the local private key be lost.

This document describe how to generate such an extra keys pair, change the private key passphrase
and decrypt a backup encrypted on a LabBook system with the corresponding public key installed.

You will need a running LabBook system and access to the command line.
You must be logged in as `sigl`.
You can [open a terminal](https://askubuntu.com/questions/183775/how-do-i-open-a-terminal) by hitting `Ctrl Alt T`

## Generating keys

Any gpg key pair will do, but if you wish you can generate a gpg key pair on a spare LabBook 3 machine:

- generate a key pair from the application,
- perform a backup,
- the keys will be available on the media with the names `kpri.[fingerprint].asc` and `kpub.[fingerprint].asc`.

To start encrypting the backups of a given site with the extra public key you have to place the corresponding file
into the `/opt/ec/systeme` folder of the LabBook machine.
You can rename it and change the [fingerprint] part of the filename but you should keep the kpub. prefix and .asc suffix.

You must keep the corresponding private key and its passphrase in a safe place.
DO NOT COPY the private key to a production LabBook system.

You can obtain information about the key stored in an `*.asc` file with :

~~~
$ gpg kpub.fondation-merieux.asc 
pub  2048R/8E57A7A1 2021-03-25 LabBook Backup Key
$ gpg kpri.fondation-merieux.asc 
sec  2048R/8E57A7A1 2021-03-25 LabBook Backup Key
~~~

A special key pair was generated for LabBook 3 and the public key is included in the `labbook_python` project as `labbook_python/labbook_BE/script/kpub.fondation-merieux.asc`. It is copied on every LabBook 3 backup media. The corresponding private key is sotred safely by [Fondation Mérieux](www.fondation-merieux.org).

## Modifying the private key passphrase

To modify the passphrase associated with a private key, you have to import it into your keyring first :

~~~
$ gpg --import kpri.my-extra-key.asc

$ gpg --list-secret-keys
...
sec   2048R/336D32CB 2020-03-31
uid                  LabBook Backup Key
...
~~~

Then edit it :

~~~
$ gpg --edit-key 336D32CB
...
gpg> passwd
...
you are asked to type the current passphrase then the new passphrase
...
gpg> save
$
~~~

You can export it back :

~~~
$ gpg --export-secret-keys --armor --yes --output kpri.my-extra-key.asc 336D32CB
~~~

## Decrypting a backup with an extra key

The backup you are restoring must have been encrypted with the public key corresponding to your private extra key.
You should first import the private key into your keyring :

~~~
$ gpg --import kpri.my-extra-key.asc
~~~

Then use the `extract_backup.sh` script from the `labbook_python`
You can first list the backup contents :

~~~
$ extract_backup.sh -n -a backup_SIGL_2018-12-14_09h30m31s.tar.gz
~~~

Then extract it into a folder of your choice :

~~~
$ extract_backup.sh -a backup_SIGL_2018-12-14_09h30m31s.tar.gz -o /tmp
~~~

You will have to provide the corresponding passphrase to unlock the private extra key.
