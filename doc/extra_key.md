# Extra key for restoring LabBook GPG backups

## Context

Starting with version 2.9.0, LabBook backups are encrypted using GPG, which allows multiple recipients when encrypting.
LabBook backups are therefore encrypted to the local public key as well as another public key.
LabBook is distributed with a special `fondation-merieux` key which allows [Fondation Mérieux](https://www.fondation-merieux.org)
to be able to decrypt a backup should the passphrase to the local private key be lost.

This document describe how to generate such an extra keys pair, change the private key passphrase
and decrypt a backup encrypted on a LabBook system with the corresponding public key installed.

You will need a linux system with access to the command line.
If it is a LabBook system, you must be logged in as `sigl`.
On ubuntu, you can [open a terminal](https://askubuntu.com/questions/183775/how-do-i-open-a-terminal) by hitting `Ctrl Alt T`

## Generating keys

Any gpg key pair will do, but if you wish you can generate a GPG key pair on a spare LabBook 3 machine:

- generate a key pair from the application,
- perform a backup,
- the keys will be available on the media with the names `kpri.[fingerprint].asc` and `kpub.[fingerprint].asc`.

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

A similar key pair was generated for LabBook 3 and the public key is included in the `labbook_python` project as `labbook_python/labbook_BE/script/kpub.fondation-merieux.asc`.
It is copied on every LabBook 3 backup media.
The corresponding private key is stored safely by [Fondation Mérieux](https://www.fondation-merieux.org).

## Modifying the private key passphrase

To modify the passphrase associated with a private key, you have to import it into your keyring first:
(depending on your gpg version, you may have to provide the corresponding passphrase to import the private key)

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

## Decrypting a LabBook v3 backup with an extra key

The backup you are restoring must have been encrypted with the public key corresponding to your private extra key.
You should first import the private key into your keyring :
(depending on your gpg version, you may have to provide the corresponding passphrase to import the private key)

~~~
$ gpg --import kpri.my-extra-key.asc
~~~


Then you can decrypt the backup:

~~~
$ gpg --output /tmp/backup_v30_SIGL_2021-03-31_18h03m10s.tar.gz \
      --decrypt /tmp/backup_v30_SIGL_2021-03-31_18h03m10s.tar.gz.gpg
~~~

You will have to provide the corresponding passphrase to unlock the private key.
The resulting file is a standard tar archive containing the SQL dump of the database and the files:

~~~
$ tar tf /tmp/backup_v30_SIGL_2021-03-31_18h03m10s.tar.gz
dump/dump.sql
report/
report/.gitignore
upload/
upload/8c/
upload/8c/42/
upload/8c/42/8c42586eb5e771edd6f94ce1be236c05
...
~~~

## Re encrypting a LabBook v3 backup to a different key

If you want to restore a backup you have decrypted on a LabBook v3 machine,
you must first re encrypt the archive to the public key of the corresponding machine.

For information about obtaining a copy of the public key file `kpub.[fingerprint].asc`
please see `Command line access to the LabBook container` in [backup_testing.md](backup_testting.md).

~~~
$ gpg --output /tmp/backup_v30_SIGL_2021-03-31_18h03m10s.tar.gz.gpg \
      --recipient-file /tmp/kpub.[fingerprint].asc \
      --encrypt /tmp/backup_v30_SIGL_2021-03-31_18h03m10s.tar.gz
~~~

Notes:

- gpg may add the public key in you keyring,
- you may have to confirm that the key belongs to the person named in the user ID,
- for older gpg versions, you may have to import the public key in your keyring and use the `--recipient` option.
