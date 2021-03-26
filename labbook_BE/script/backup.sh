#!/bin/bash
#
# Utilities for LabBook 3 backup
#
# 2021-03-18
#
ENV_KEY_PASS="LABBOOK_KEY_PWD"
ENV_KEY_DIR="LABBOOK_KEY_DIR"
ENV_STATUS_DIR="LABBOOK_STATUS_DIR"
ENV_LOG_DIR="LABBOOK_LOG_DIR"
ENV_TEST_OK="LABBOOK_TEST_OK"
ENV_TEST_KO="LABBOOK_TEST_KO"
ENV_HOST="LABBOOK_DB_HOST"  # DB is on the host for now, no need to have a LABBOOK_HOST env variable
ENV_USER="LABBOOK_USER"
ENV_USER_PASS="LABBOOK_USER_PWD"
ENV_DB_NAME="LABBOOK_DB_NAME"
ENV_DB_HOST="LABBOOK_DB_HOST"
ENV_DB_USER="LABBOOK_DB_USER"
ENV_DB_PASS="LABBOOK_DB_PWD"
KEY_REAL_NAME="LabBook Backup Key"
WORK_DIRECTORY="/tmp"
MEDIA_DIRECTORY="/media"
BACKUPS_DIRECTORY="SIGL_sauvegardes"
DEF_VOLUME_NAME="labbook_storage"
MOUNTDIR_STORAGE="/storage"
LB25_KPRI_CLEAR_FILENAME="clef_sauvegarde.privee"
LB25_KPRI_FILENAME="$LB25_KPRI_CLEAR_FILENAME.crypt"
LB25_KPRI_PASSWORD="eiKie7di"
LB25_DUMP_FILENAME="SIGL.sql"
LB29_KPRI_FILENAME="clef_sauvegarde.privee.gpg"
LB30_DUMP_DIR="dump"
LB30_DUMP_FILENAME="dump.sql"
LB30_REPORT_DIR="report"
LB30_UPLOAD_DIR="upload"
LB30_RESOURCE_DIR="resource"
CONTAINER="labbook-python"
SCRIPT_ABSOLUTE_DIR="/home/apps/labbook_BE/labbook_BE/script"
MAP_MEDIA="/media:/media"
MAP_STORAGE="$DEF_VOLUME_NAME:$MOUNTDIR_STORAGE"
LAST_BACKUP_OK="last_backup_ok"
FMX_KPUB_FILENAME="kpub.fondation-merieux.asc"
BACKUPAUTO_SETTINGS="backupauto_settings.sh"

#############
# Functions #
#############
#
# Display usage and exit
#
usage()
{
    local message="$1"

    [[ "$message" ]] && {
        echo
        echo "$message"
    }

    echo
    echo "Utilities for LabBook backup"
    echo
    echo "Usage:"
    echo
    echo "  $(basename "$0") [options] command"
    echo
    echo "Passphrase for gpg operations is read from $ENV_KEY_PASS environment variable"
    echo "Password for user operations is read from $ENV_USER_PASS environment variable"
    echo
    echo "Commands as described in api.md:"
    echo "  genkey            Create key pair in DIR"
    echo "  keyexist          Check key pair exist in DIR"
    echo "  initmedia         Initialize media"
    echo "  listmedia         List initialized medias in /media/USER"
    echo "  listarchive       List archives in MEDIA"
    echo "  backup            Backup"
    echo "  restore           Restore ARCHIVE from MEDIA"
    echo "  restart           Restart LabBook container"
    echo "  progbackup        Program daily backup at HH:MM by cron"
    echo "  backupauto        Backup started by cron"
    echo
    echo "Internal commands:"
    echo "  encrypt           Encrypt INPUT_FILE to DIR/INPUT_FILE.gpg and copy keys to DIR"
    echo "  decrypt29         Decrypt a LabBook 2.9 INPUT_FILE to OUTPUT_FILE using key in DIR"
    echo "                    If DIR is omitted key should be in the current keyring"
    echo "  decrypt25         Decrypt a LabBook 2.5 INPUT_FILE to OUTPUT_FILE"
    echo "  savefiles         Archive FILE_PATH(s) to ARCHIVE_PATH then encrypt archive to OUTPUT_FILE using keys in DIR"
    echo "                    If specified, FILE_PATHs are relative to ROOT_PATH or VOLUME moutpoint"
    echo "                    ARCHIVE_PATH can be omitted"
    echo "  restorefiles      Decrypt INPUT_FILE to ARCHIVE_PATH then restore to ROOT_PATH or VOLUME moutpoint"
    echo "  mountpoint        Display mountpoint directory for VOLUME. Internal use"
    echo "  testfake          Display faking mode. Used for testing"
    echo "  dumpdb            Dump database to OUTPUT_FILE"
    echo "  loaddb            Load database from INPUT_FILE"
    echo "  islb30            Is INPUT_FILE a LabBook 3 archive ?"
    echo "  islb25            Is INPUT_FILE a LabBook 2.5 archive ?"
    echo
    echo "Options:"
    echo "  -h                Display this help and exit"
    echo "  -v                Verbose mode"
    echo "  -i INPUT_FILE     Input file"
    echo "  -o OUTPUT_FILE    Output file"
    echo "  -d DIR            Directory for input or output"
    echo "  -a ARCHIVE        Archive"
    echo "  -V VOLUME         Container volume"
    echo "  -R ROOT_PATH      Root path"
    echo "  -P TEST_PATH      Test path"
    echo "  -p FILE_PATH      File path, may be repeated"
    echo "  -s STATUS_FILE    Status file [default=$ENV_STATUS_DIR/command]"
    echo "  -u USER           Linux user [default=$ENV_USER]"
    echo "  -m MEDIA          Media"
    echo "  -U                Include uninitialized medias in list"
    echo "  -w HH:MM          moment in the form HH:MM"
    echo "  -T                Test mode"
    echo

    exit 2
}

#
# Look for one key pair
#
# Param: directory to look into
#
fn_keyexist() {
    local keys_dir="$1"
    declare -a kpris
    local privkey_file=""
    local pubkey_file=""
    local ret_status=1

    [[ -d "$keys_dir" ]] || {
        echo_message "cannot find directory $keys_dir"
        return 1
    }

    kpris=("$keys_dir"/kpri.*.asc)

    for privkey_file in "${kpris[@]}"; do
        pubkey_file=${privkey_file/kpri/kpub}

        if [[ -f "$pubkey_file" ]]; then
            [[ $verbose -eq 1 ]] && echo_message "Found keypair $privkey_file and $pubkey_file"
            ret_status=0
            break
        else
            [[ $verbose -eq 1 ]] && echo_message "Cannot find $pubkey_file matching $privkey_file"
        fi
    done

    return $ret_status
}

#
# Remove private keys and associated public keys
#
# Param: directory to look into
#
fn_delkeys() {
    local keys_dir="$1"
    declare -a kpris
    local privkey_file=""
    local pubkey_file=""

    [[ -d "$keys_dir" ]] || {
        echo_message "cannot find directory $keys_dir"
        return 1
    }

    kpris=("$keys_dir"/kpri.*.asc)

    for privkey_file in "${kpris[@]}"; do
        pubkey_file=${privkey_file/kpri/kpub}

        [[ -f "$pubkey_file" ]] && rm -f "$pubkey_file"

        rm -f "$privkey_file"
    done

    return 0
}

#
# Generate a keypair
#
# Param: directory to export keys to
#
fn_genkey() {
    local export_dir="$1"
    local gen_key_cmd_file=""
    local passwd=""
    local fpr=""
    local privkey_file=""
    local pubkey_file=""

    [[ -d "$export_dir" ]] || {
        echo_message "cannot find directory $export_dir"
        return 1
    }

    GNUPGHOME="$(mktemp -d -p $WORK_DIRECTORY)"
    export GNUPGHOME

    cat > "$GNUPGHOME/gpg-agent.conf" <<EOF
allow-loopback-pinentry
EOF

    gen_key_cmd_file="$GNUPGHOME/gen_key_cmd_file"

    cat > "$gen_key_cmd_file" <<EOF
Key-Type: RSA
Key-Length: 2048
Name-Real: $KEY_REAL_NAME
Expire-Date: 0
EOF

    passwd=$(printenv $ENV_KEY_PASS)

    if [[ $verbose -eq 1 ]]; then
        echo_message "Generating keys with file=$gen_key_cmd_file"

        echo "$passwd" | gpg --pinentry-mode loopback --batch --passphrase-fd 0 --generate-key "$gen_key_cmd_file"
        status=$?
    else
        # even with --quiet option there is an output
        echo "$passwd" | gpg --pinentry-mode loopback --batch --quiet --passphrase-fd 0 --generate-key "$gen_key_cmd_file" > /dev/null 2>&1
        status=$?
    fi

    [[ $status -eq 0 ]] || {
        echo_message "error generating keys"
        return 1
    }

    [[ $verbose -eq 1 ]] && echo_message "Evaluating fingerprint"

    fpr=$(gpg --list-keys --with-colon "$KEY_REAL_NAME" 2> /dev/null | grep "^fpr" | cut -d: -f10)
    privkey_file="$export_dir/kpri.$fpr.asc"
    pubkey_file="$export_dir/kpub.$fpr.asc"

    [[ $verbose -eq 1 ]] && echo_message "Exporting private key to $privkey_file"

    echo "$passwd" | gpg --pinentry-mode loopback --batch --passphrase-fd 0 --export-secret-keys --armor --yes --output "$privkey_file" "$fpr"
    status=$?

    [[ $status -eq 0 ]] || {
        echo_message "error exporting private key to $privkey_file"
        return 1
    }

    [[ $verbose -eq 1 ]] && echo_message "Exporting public key to $pubkey_file"

    echo "$passwd" | gpg --pinentry-mode loopback --batch --passphrase-fd 0 --export --armor --yes --output "$pubkey_file" "$fpr"
    status=$?

    [[ $status -eq 0 ]] || {
        echo_message "error exporting public key to $pubkey_file"
        return 1
    }

    rm -rf "$GNUPGHOME"

    return 0
}

#
# Encrypt a file
#
# Params:
# - input file to encrypt
# - directory for encrypted file and public keys to use
#
fn_encrypt() {
    local input_file="$1"
    local keys_dir="$2"
    local output_dir="$2"
    local recipients_option=""
    local basename_file=""
    local output_file=""

    [[ -f "$input_file" && -r "$input_file" ]] || {
        echo_message "cannot read file $input_file"
        return 1
    }

    [[ -d "$keys_dir" ]] || {
        echo_message "cannot find directory $keys_dir"
        return 1
    }

    for pubkey_file in "$keys_dir"/kpub.*.asc; do
        recipients_option="$recipients_option --recipient-file $pubkey_file"
    done

    [[ -n "$recipients_option" ]] || {
        echo_message "cannot find recipients public keys in $keys_dir"
        return 1
    }

    # to prevent gpg from adding the recipients keys to the current user keyring
    GNUPGHOME="$(mktemp -d -p $WORK_DIRECTORY)"
    export GNUPGHOME

    basename_file=$(basename "$input_file")
    output_file="$output_dir/${basename_file}.gpg"

    [[ $verbose -eq 1 ]] && echo_message "encrypting $input_file to $output_file recipients_option=$recipients_option"

    # shellcheck disable=SC2086
    gpg --yes --output "$output_file" $recipients_option --encrypt "$input_file" || {
        echo_message "error encrypting $input_file to $output_file recipients_option=$recipients_option"
        return 1
    }

    rm -rf "$GNUPGHOME"

    return 0
}

#
# Create a temporary keyring
#
# Params:
# - directory containing private key
# - temporary GNUPGHOME
#
fn_tmpkeyring() {
    local keys_dir="$1"
    local tmp_gnupghome="$2"
    local privkey_file=""

    [[ -n "$keys_dir" && -d "$keys_dir" ]] || {
        echo_message "cannot find key directory $keys_dir"
        return 1
    }

    [[ -n "$tmp_gnupghome" && -d "$tmp_gnupghome" ]] || {
        echo_message "cannot find temporary GNUPGHOME $tmp_gnupghome"
        return 1
    }

    GNUPGHOME="$tmp_gnupghome"
    export GNUPGHOME

    cat > "$GNUPGHOME/gpg-agent.conf" <<EOF
allow-loopback-pinentry
EOF

    # shellcheck disable=SC2012
    privkey_file=$(ls "$keys_dir"/kpri.*.asc | head -1)

    [[ -n "$privkey_file" ]] || {
        echo_message "cannot find private key in $keys_dir"
        return 1
    }

    [[ -r "$privkey_file" ]] || {
        echo_message "cannot read private key in $privkey_file"
        return 1
    }

    [[ $verbose -eq 1 ]] && echo_message "importing private key from $privkey_file"

    gpg --batch --import "$privkey_file"
    status=$?

    [[ $status -eq 0 ]] || {
        echo_message "error importing private key from $privkey_file"
        return 1
    }

    return 0
}

#
# Decrypt a LabBook 2.9 backup
#
# Params:
# - input file to decrypt
# - output file
# - directory containing private key (if empty use current keyring)
#
fn_decrypt29() {
    local input_file="$1"
    local output_file="$2"
    local keys_dir="$3"
    local tmp_gnupghome=""

    [[ -f "$input_file" && -r "$input_file" ]] || {
        echo_message "cannot read file $input_file"
        return 1
    }

    if [[ -n "$keys_dir" ]]; then
        tmp_gnupghome="$(mktemp -d -p $WORK_DIRECTORY)"

        fn_tmpkeyring "$keys_dir" "$tmp_gnupghome" || {
            echo_message "error creating temporary keyring with private key in $keys_dir"
            return 1
        }

        passwd=$(printenv $ENV_KEY_PASS)

        # shellcheck disable=SC2086
        echo "$passwd" | gpg --pinentry-mode loopback --batch --passphrase-fd 0 \
                             --yes --output "$output_file" --decrypt "$input_file" || {
            echo_message "error decrypting $input_file with private key in $keys_dir"
            return 1
            }

        rm -rf "$tmp_gnupghome"

    else
        gpg --yes --output "$output_file" --decrypt "$input_file" || {
            echo_message "error decrypting $input_file"
            return 1
            }
    fi

    return 0
}

#
# Decrypt a LabBook 2.5 backup
#
# Main steps:
# - extract archive content yields archive data and archive key
# - decrypt private key with fixed password
# - decrypt archive key with decrypted private key
# - decrypt archive data with decrypted archive key
#
# Params:
# - input file to decrypt
# - output file
# - directory containing private key
#
fn_decrypt25() {
    local input_file="$1"
    local output_file="$2"
    local keys_dir="$3"
    local absolute_input_file=""
    local absolute_output_file=""
    local encrypted_privkey_file=""
    local absolute_encrypted_privkey_file=""
    local saved_workdir=""
    local encrypted_archive_key=""
    local clear_archive_key=""

    [[ -f "$input_file" && -r "$input_file" ]] || {
        echo_message "cannot read file $input_file"
        return 1
    }

    [[ -d "$keys_dir" ]] || {
        echo_message "cannot find directory $keys_dir"
        return 1
    }

    encrypted_privkey_file="$keys_dir/$LB25_KPRI_FILENAME"

    [[ -f "$encrypted_privkey_file" && -r "$encrypted_privkey_file" ]] || {
        echo_message "cannot find private key file $encrypted_privkey_file"
        return 1
    }

    tmp_workdir=$(mktemp -d) || {
        echo_message "cannot create temporary working directory"
        return 1
    }

    # since we change directory, we need the absolute paths to the input, output and key files
    case "$input_file" in
        /*) absolute_input_file="$input_file" ;;
        *)  absolute_input_file=$(realpath "$(pwd)/$input_file") ;;
    esac

    [[ $verbose -eq 1 ]] && echo_message "Absolute encrypted archive path is $absolute_input_file"

    case "$output_file" in
        /*) absolute_output_file="$output_file" ;;
        *)  absolute_output_file=$(realpath "$(pwd)/$output_file") ;;
    esac

    [[ $verbose -eq 1 ]] && echo_message "Absolute decrypted archive path is $absolute_output_file"

    case "$encrypted_privkey_file" in
        /*) absolute_encrypted_privkey_file="$encrypted_privkey_file" ;;
        *)  absolute_encrypted_privkey_file=$(realpath "$(pwd)/$encrypted_privkey_file") ;;
    esac

    [[ $verbose -eq 1 ]] && echo_message "Absolute encrypted private key path is $absolute_encrypted_privkey_file"

    saved_workdir=$(pwd)

    cd "$tmp_workdir" || {
        echo_message "cannot cd to $tmp_workdir"
        return 1
    }

    [[ $verbose -eq 1 ]] && echo_message "Extracting $absolute_input_file content into $(pwd)"

    tar xf "$absolute_input_file" || {
        echo_message "cannot extract $absolute_input_file content"
        return 1
    }

    # verify expected result of untar : encrypted archive key and encrypted archive data
    encrypted_archive_key=$(basename "$input_file").tar.key
    encrypted_archive_data=$(basename "$input_file").tar.crypt

    [[ -r "$encrypted_archive_key" ]] || {
        echo_message "cannot read encrypted archive key file $encrypted_archive_key"
        return 1
    }

    [[ -r "$encrypted_archive_data" ]] || {
        echo_message "cannot read encrypted archive data file $encrypted_archive_data"
        return 1
    }

    [[ $verbose -eq 1 ]] && echo_message "Decrypting $absolute_encrypted_privkey_file to $LB25_KPRI_CLEAR_FILENAME"

    # With openssl versions >= 1.1.0 we have to force md5 to decrypt LabBook 2.5 backups.
    # There is no option to suppress the warning message about md5 being deprecated, redirecting STDERR in non verbose mode.
    if [[ $verbose -eq 1 ]]; then
        openssl enc -d -des3 -md md5 -salt \
            -k "$LB25_KPRI_PASSWORD" \
            -in "$absolute_encrypted_privkey_file" \
            -out "$LB25_KPRI_CLEAR_FILENAME" || {
            echo_message "cannot decrypt private key $absolute_encrypted_privkey_file with openssl"
            return 1
        }
    else
        openssl enc -d -des3 -md md5 -salt \
            -k "$LB25_KPRI_PASSWORD" \
            -in "$absolute_encrypted_privkey_file" \
            -out "$LB25_KPRI_CLEAR_FILENAME" 2> /dev/null || {
            echo_message "cannot decrypt private key $absolute_encrypted_privkey_file with openssl"
            return 1
        }
    fi

    clear_archive_key=$(basename "$input_file").key

    [[ $verbose -eq 1 ]] && echo_message "Decrypting archive key file $encrypted_archive_key to $clear_archive_key"

    openssl rsautl \
        -decrypt \
        -inkey "$LB25_KPRI_CLEAR_FILENAME" \
        -in "$encrypted_archive_key" \
        -out "$clear_archive_key" || {
        echo_message "cannot decrypt archive key $encrypted_archive_key"
        return 1
    }

    [[ -r "$clear_archive_key" ]] || {
        echo_message "cannot read archive key $clear_archive_key"
        return 1
    }

    # archive key file contains K and iv data encryption parameters in the form K=iv
    K=$(cut -d= -f1 "$clear_archive_key")
    iv=$(cut -d= -f2 "$clear_archive_key")

    [[ $verbose -eq 1 ]] && echo_message "Decrypting archive data file $encrypted_archive_data to $absolute_output_file"

    openssl enc \
        -d -aes-256-cbc -nosalt \
        -in "$encrypted_archive_data" \
        -out "$absolute_output_file" \
        -K "$K" -iv "$iv" || {
        echo_message "cannot decrypt archive data $encrypted_archive_data"
        return 1
    }

    cd "$saved_workdir" || {
        echo_message "cannot cd to $saved_workdir"
        return 1
    }

    return 0
}

#
# Save files to an encrypted archive
#
# Params:
# - final encrypted archive
# - intermediate clear archive (if empty no clear archive is created)
# - directory containing public keys
# - root path
# - files and directories relative to root path
#
fn_savefiles() {
    local output_file="$1"
    local clear_archive="$2"
    local keys_dir="$3"
    local root_dir="$4"
    local initial_dir=""

    shift 4  # remaining arguments are files and directories to save

    initial_dir="$(pwd)"

    [[ $# -gt 0 ]] || {
        echo_message "nothing to save"
        return 1
    }

    [[ -d "$keys_dir" ]] || {
        echo_message "cannot find directory $keys_dir"
        return 1
    }

    for pubkey_file in "$keys_dir"/kpub.*.asc; do
        recipients_option="$recipients_option --recipient-file $pubkey_file"
    done

    [[ -n "$recipients_option" ]] || {
        echo_message "cannot find recipients public keys in $keys_dir"
        return 1
    }

    # to prevent gpg from adding the recipients keys to the current user keyring
    GNUPGHOME="$(mktemp -d -p $WORK_DIRECTORY)"
    export GNUPGHOME

    cd "$root_dir" || {
        echo_message "cannot cd to $root_dir"
        return 1
    }

    if [[ -n "$clear_archive" ]]; then
        [[ $verbose -eq 1 ]] && echo_message "creating $clear_archive from $*"

        tar czf "$clear_archive" "$@" || {
            echo_message "error creating archive $clear_archive"
            return 1
        }

        [[ $verbose -eq 1 ]] && echo_message "encrypting $clear_archive to $output_file recipients_option=$recipients_option"

        # shellcheck disable=SC2086
        gpg --yes --output "$output_file" $recipients_option --encrypt "$clear_archive" || {
            echo_message "error encrypting $clear_archive to $output_file recipients_option=$recipients_option"
            return 1
        }
    else
        [[ $verbose -eq 1 ]] && echo_message "archiving $* and encrypting to $output_file recipients_option=$recipients_option"
        # shellcheck disable=SC2086
        tar czf - "$@" | gpg --yes --output "$output_file" $recipients_option --encrypt || {
            echo_message "error archiving and encrypting to $output_file recipients_option=$recipients_option"
            return 1
        }
    fi

    cd "$initial_dir" || {
        echo_message "cannot cd back to $initial_dir"
        return 1
    }

    rm -rf "$GNUPGHOME"

    return 0
}

#
# Restore files from an encrypted archive
#
# Params:
# - input encrypted archive
# - intermediate clear archive (may be empty)
# - directory containing private key (if empty use current keyring)
# - root path to restore to
#
fn_restorefiles() {
    local input_archive="$1"
    local clear_archive="$2"
    local keys_dir="$3"
    local root_dir="$4"
    local tmp_gnupghome=""
    local initial_dir=""

    #local input_file="$1"
    #local output_file="$2"
    #local keys_dir="$3"
    #local privkey_file=""

    [[ -f "$input_archive" && -r "$input_archive" ]] || {
        echo_message "cannot read encrypted archive $input_archive"
        return 1
    }

    initial_dir="$(pwd)"

    cd "$root_dir" || {
        echo_message "cannot cd to $root_dir"
        return 1
    }

    if [[ -n "$keys_dir" ]]; then
        tmp_gnupghome="$(mktemp -d -p $WORK_DIRECTORY)"

        fn_tmpkeyring "$keys_dir" "$tmp_gnupghome" || {
            echo_message "error creating temporary keyring with private key in $keys_dir"
            return 1
        }

        passwd=$(printenv $ENV_KEY_PASS)

        if [[ -n "$clear_archive" ]]; then
            # shellcheck disable=SC2086
            echo "$passwd" | gpg --pinentry-mode loopback --batch --passphrase-fd 0 \
                                 --yes --output "$clear_archive" --decrypt "$input_archive" || {
                echo_message "error decrypting archive $input_archive with private key in $keys_dir"
                return 1
                }

            tar xf "$clear_archive" || {
                echo_message "error extracting archive $clear_archive"
                return 1
            }
        else
            # tar reads from stdin, no filename, z option must be present
            # shellcheck disable=SC2086
            echo "$passwd" | \
            gpg --pinentry-mode loopback --batch --passphrase-fd 0 --yes --decrypt "$input_archive" | \
            tar xzf - || {
                echo_message "error decrypting and extracting archive $input_archive with private key in $keys_dir"
                return 1
            }
        fi

        rm -rf "$tmp_gnupghome"

    else
        if [[ -n "$clear_archive" ]]; then
            gpg --yes --output "$clear_archive" --decrypt "$input_archive" || {
                echo_message "error decrypting archive $input_archive"
                return 1
                }

            tar xf "$clear_archive" || {
                echo_message "error extracting archive $clear_archive"
                return 1
            }
        else
            # tar reads from stdin, no filename, z option must be present
            gpg --yes --decrypt "$input_archive" | tar xzf - || {
                echo_message "error decrypting and extracting archive $input_archive"
                return 1
            }
        fi
    fi

    cd "$initial_dir" || {
        echo_message "cannot cd back to $initial_dir"
        return 1
    }

    return 0
}

#
# Get mountpoint of container volume
#
# Param:
# - volume name
#
fn_get_mountpoint() {
    local volume_name="$1"
    local docker_cmd=""
    local mountpoint=""
    local cmd_status=0
    local local_user=""
    local local_host=""

    if in_app_container; then
        docker_cmd="podman"
        local_user="$user"

        [[ -n "$local_user" ]] || local_user=$(printenv $ENV_USER)

        [[ -n "$local_user" ]] || {
            echo_message "cannot evaluate user"
            return 1
        }

        local_host="$host"

        [[ -n "$local_host" ]] || local_host=$(printenv $ENV_HOST)

        [[ -n "$local_host" ]] || {
            echo_message "cannot evaluate host"
            return 1
        }

        [[ $verbose -eq 1 ]] && echo_message "user=$local_user host=$local_host"

        mountpoint=$(SSHPASS=$(printenv $ENV_USER_PASS) \
                     sshpass -e \
                     ssh -o "StrictHostKeyChecking no" "$local_user@$local_host" \
                     sudo $docker_cmd volume inspect --format '{{.Mountpoint}}' "$volume_name" 2> /dev/null)
        cmd_status=$?
    else
        if type podman > /dev/null 2>&1; then
            docker_cmd="podman"
        elif type docker > /dev/null 2>&1; then
            docker_cmd="docker"
        else
            echo_message "cannot find podman or docker to query volume"
            return 1
        fi

        mountpoint=$($docker_cmd volume inspect --format '{{.Mountpoint}}' "$volume_name" 2> /dev/null)
        cmd_status=$?
    fi

    if [[ $cmd_status -eq 0 ]]; then
        echo "$mountpoint"
        return 0
    else
        echo_message "error in $docker_cmd volume inspect $volume_name"
        return 1
    fi
}

#
# Init media
#
# Param:
# - user
# - media
# - path to search for medias (for test only, if empty use MEDIA_DIRECTORY)
#
fn_initmedia() {
    local user="$1"
    local media="$2"
    local media_dir="$3"
    local media_path=""
    local backup_path=""

    [[ -z "$media_dir" ]] && media_dir="$MEDIA_DIRECTORY"

    [[ -d "$media_dir" ]] || {
        log_message "cannot find directory $media_dir"
        return 1
    }

    media_path="$media_dir/$user/$media"

    [[ $verbose -eq 1 ]] && log_message "Initializing $media_path"

    [[ -d "$media_path" ]] || {
        log_message "cannot find media $media_path"
        return 1
    }

    backup_path="$media_path/$BACKUPS_DIRECTORY"

    mkdir -p "$backup_path" || {
        log_message "cannot create directory $backup_path"
        return 1
    }

    return 0
}

#
# List medias
#
# Param:
# - user
# - status file
# - list only initialized medias (0) or all medias (1)
# - path to search for medias (for test only, if empty use MEDIA_DIRECTORY)
#
# Output in status_file: media names, one per line
#
fn_listmedia() {
    local user="$1"
    local status_file="$2"
    local with_uninitialized="$3"
    local media_dir="$4"

    [[ -z "$media_dir" ]] && media_dir="$MEDIA_DIRECTORY"

    [[ -d "$media_dir" ]] || {
        log_message "cannot find directory $media_dir"
        return 1
    }

    status_message ""

    [[ $verbose -eq 1 ]] && log_message "Listing content of $media_dir/$user"

    for media in "$media_dir"/"$user"/*; do
        [[ -e "$media" ]] || break

        [[ $with_uninitialized -eq 1 ]] || {
            is_initialized "$media" || continue
        }

        status_message "$(basename "$media")"
    done

    return 0
}

#
# List archives
#
# Param:
# - user
# - status file
# - media
# - path to search for medias (for test only, if empty use MEDIA_DIRECTORY)
#
# Output in status_file: archive names, one per line
#
fn_listarchive() {
    local user="$1"
    local status_file="$2"
    local media="$3"
    local media_dir="$4"
    local media_path=""

    [[ -z "$media_dir" ]] && media_dir="$MEDIA_DIRECTORY"

    [[ -d "$media_dir" ]] || {
        log_message "cannot find directory $media_dir"
        return 1
    }

    status_message ""

    media_path="$media_dir/$user/$media"

    [[ -d "$media_path" ]] || {
        log_message "cannot find media $media in $media_path"
        return 1
    }

    is_initialized "$media_path" || {
        log_message "media $media not initialized in $media_path"
        return 1
    }

    [[ $verbose -eq 1 ]] && log_message "Listing backups in $media_path/$BACKUPS_DIRECTORY"

    for backup in "$media_path"/"$BACKUPS_DIRECTORY"/backup_*; do
        [[ -e "$backup" ]] || break

        status_message "$(basename "$backup")"
    done

    return 0
}

#
# Check if a media is initialized
#
# Param:
# - path to media
#
is_initialized() {
    local media_path="$1"

    [[ -d "$media_path/$BACKUPS_DIRECTORY" ]] || return 1

    return 0
}

#
# Restart LabBook container
#
# Param:
# - user
# - host
#
fn_restart() {
    local user="$1"
    local host="$2"

    [[ $verbose -eq 1 ]] && log_message "Restarting container as $user on $host"

    [[ $test_mode -eq 0 ]] && {
        SSHPASS=$(printenv $ENV_USER_PASS) \
            sshpass -e \
            ssh -o "StrictHostKeyChecking no" "$user@$host" \
            sudo service labbook restart
    }

    return 0
}

#
# Program daily backup
#
# Param:
# - when in the form HH:MM
# - user
# - host
#
fn_progbackup() {
    local when="$1"
    local user="$2"
    local host="$3"
    local cron_file="$WORK_DIRECTORY/cron_file"
    local hour_c=""
    local hour_i=0
    local minute_c=""
    local minute_i=0
    local status=0
    local image=""
    local my_absolute_path=""
    local settings_file=""

    [[ $verbose -eq 1 ]] && echo_message "Programming daily backup at $when as $user on $host"

    hour_c=$(echo "$when" | cut -d: -f1)
    minute_c=$(echo "$when" | cut -d: -f2)

    # without 10# (base 10), 09 will be interpreted as an invalid octal number
    hour_i=$((10#$hour_c + 0))
    minute_i=$((10#$minute_c + 0))

    [[ $hour_i -ge 0 && $hour_i -le 23 ]] || {
        log_message "$when incorrect HH should be between 00 and 23"
        return 1
    }

    [[ $minute_i -ge 0 && $minute_i -le 59 ]] || {
        log_message "$when incorrect MM should be between 00 and 59"
        return 1
    }

    [[ $verbose -eq 1 ]] && echo_message "Time is h=$hour_i m=$minute_i"

    [[ $verbose -eq 1 ]] && echo_message "Creating cron file in $cron_file"

    image=$(fn_get_my_image "$user" "$host")

    [[ -n "$image" ]] || {
        echo_message "cannot get my image name with $user@$host"
        return 1
    }

    my_absolute_path="$test_path"

    [[ -n "$my_absolute_path" ]] || my_absolute_path="$SCRIPT_ABSOLUTE_DIR/backup.sh"

    settings_file="$(printenv $ENV_STATUS_DIR)/$BACKUPAUTO_SETTINGS"

    cat > "$cron_file" <<%
$minute_i $hour_i * * * sudo podman run --rm -v $MAP_MEDIA -v $MAP_STORAGE $image $my_absolute_path -i $settings_file backupauto
%

    [[ $test_mode -eq 0 ]] && {
        [[ $verbose -eq 1 ]] && echo_message "Installing cron file for $user@$host"

        SSHPASS=$(printenv $ENV_USER_PASS) \
            sshpass -e \
            ssh -o "StrictHostKeyChecking no" "$user@$host" \
            crontab - \
        < "$cron_file" || status=1
    }

    rm -f "$cron_file"

    [[ $status -eq 0 ]] || return $status

    [[ $verbose -eq 1 ]] && echo_message "Creating settings file in $settings_file"

    cat > "$settings_file" <<%
# Settings for automatic LabBook backups
# This file is generated when automatic backups are scheduled. DO NOT EDIT !!
export $ENV_USER=$(printenv $ENV_USER)
export $ENV_STATUS_DIR=$(printenv $ENV_STATUS_DIR)
export $ENV_KEY_DIR=$(printenv $ENV_KEY_DIR)
export $ENV_LOG_DIR=$(printenv $ENV_LOG_DIR)
export $ENV_DB_HOST=$(printenv $ENV_DB_HOST)
export $ENV_DB_USER=$(printenv $ENV_DB_USER)
export $ENV_DB_PASS=$(printenv $ENV_DB_PASS)
export $ENV_DB_NAME=$(printenv $ENV_DB_NAME)
%
    status=$?

    [[ $status -eq 0 ]] || {
        echo_message "cannot create settings file in $settings_file"
        return 1
    }

    return 0
}

#
# Dump SQL database
#
# Param:
# - output file
#
fn_dumpdb() {
    local output="$1"
    local db_name=""
    local db_host=""
    local db_user=""

    db_name=$(printenv $ENV_DB_NAME)
    db_host=$(printenv $ENV_DB_HOST)
    db_user=$(printenv $ENV_DB_USER)

    [[ $verbose -eq 1 ]] && echo_message "Dumping $db_name from $db_user@$db_host to $output"

    MYSQL_PWD=$(printenv $ENV_DB_PASS)
    export MYSQL_PWD

    mysqldump \
        --force \
        --add-drop-table \
        --complete-insert \
        --default-character-set=UTF8 \
        --host="$db_host" \
        --user="$db_user" \
        --result-file="$output" \
        "$db_name" || {
        log_message "mysqldump to $output failed"
        return 1
    }

    return 0
}

#
# Load SQL database
#
# Param:
# - input file
#
fn_loaddb() {
    local input="$1"
    local db_name=""
    local db_host=""
    local db_user=""
    local db_pass=""
    local mysql_cmd=""

    db_name=$(printenv $ENV_DB_NAME)
    db_host=$(printenv $ENV_DB_HOST)
    db_user=$(printenv $ENV_DB_USER)
    db_pass=$(printenv $ENV_DB_PASS)

    [[ -f "$input" && -r "$input" ]] || {
        echo_message "cannot read input file $input"
        return 1
    }

    [[ $verbose -eq 1 ]] && log_message "Loading $db_name on $db_user@$db_host from $input"

    [[ -n "$db_pass" ]] && {
        MYSQL_PWD="$db_pass"
        export MYSQL_PWD
    }

    mysql_cmd="mysql --max_allowed_packet=512M --default-character-set=UTF8"

    [[ -n "$db_host" ]] && mysql_cmd="$mysql_cmd --host=$db_host"

    [[ -n "$db_user" ]] && mysql_cmd="$mysql_cmd --user=$db_user"

    [[ $verbose -eq 1 ]] && log_message "mysql_cmd=$mysql_cmd"

    echo "drop database if exists $db_name;" | $mysql_cmd || {
        echo_message "cannot drop database $db_name"
        return 1
    }

    echo "create database $db_name;" | $mysql_cmd || {
        echo_message "cannot create database $db_name"
        return 1
    }

    echo "source $input;" | $mysql_cmd -D "$db_name" || {
        echo_message "cannot load database $db_name"
        return 1
    }

    return 0
}

#
# Backup
#
# Param:
# - media
# - user
# - path to search for medias (for test only, if empty use MEDIA_DIRECTORY)
#
fn_backup() {
    local media="$1"
    local user="$2"
    local media_dir="$3"
    local media_path=""
    local dump_dir=""
    local dump_file=""
    local archive_path=""
    local backups_dir=""
    local db_name=""
    local timestamp=""
    local files=()
    local keys_dir=""
    local privkey_file=""
    local pubkey_file=""
    local fmx_pubkey_file=""

    [[ -z "$media_dir" ]] && media_dir="$MEDIA_DIRECTORY"

    [[ -d "$media_dir" ]] || {
        log_message "cannot find directory $media_dir"
        return 1
    }

    status_message ""

    media_path="$media_dir/$user/$media"

    [[ -d "$media_path" ]] || {
        log_message "cannot find media $media in $media_path"
        return 1
    }

    is_initialized "$media_path" || {
        log_message "media $media not initialized in $media_path"
        return 1
    }

    dump_dir="$MOUNTDIR_STORAGE/$LB30_DUMP_DIR"
    dump_file="$dump_dir/$LB30_DUMP_FILENAME"

    mkdir -p "$dump_dir"

    # dump database
    fn_dumpdb "$dump_file" || {
        log_message "error dumping database"
        return 1
    }

    # archive dump and files
    backups_dir="$media_path/$BACKUPS_DIRECTORY"
    db_name=$(printenv $ENV_DB_NAME)
    timestamp=$(date '+%F_%Hh%Mm%Ss')
    archive_path="$backups_dir/backup_v30_${db_name}_${timestamp}.tar.gz.gpg"
    files=("$LB30_DUMP_DIR/$LB30_DUMP_FILENAME" "$LB30_REPORT_DIR/" "$LB30_UPLOAD_DIR/" "$LB30_RESOURCE_DIR/")
    keys_dir="$(printenv $ENV_KEY_DIR)"

    fn_savefiles "$archive_path" "" "$keys_dir" "$MOUNTDIR_STORAGE" "${files[@]}" || {
        log_message "error saving files"
        return 1
    }

    rm -f "$dump_file"

    # copy keys
    # shellcheck disable=SC2012
    privkey_file=$(ls "$keys_dir"/kpri.*.asc | head -1)
    pubkey_file=${privkey_file/kpri/kpub}
    fmx_pubkey_file="$keys_dir/$FMX_KPUB_FILENAME"

    cp -p "$privkey_file" "$backups_dir" || {
        log_message "error copying $privkey_file"
        return 1
    }

    cp -p "$pubkey_file" "$backups_dir" || {
        log_message "error copying $pubkey_file"
        return 1
    }

    cp -p "$fmx_pubkey_file" "$backups_dir" || {
        log_message "error copying $fmx_pubkey_file"
        return 1
    }

    return 0
}

#
# Restore backup
#
# Param:
# - media
# - archive
# - user
# - path to search for medias (for test only, if empty use MEDIA_DIRECTORY)
#
fn_restore() {
    local media="$1"
    local archive="$2"
    local user="$3"
    local media_dir="$4"
    local media_path=""
    local archive_path=""

    [[ -z "$media_dir" ]] && media_dir="$MEDIA_DIRECTORY"

    [[ -d "$media_dir" ]] || {
        log_message "cannot find directory $media_dir"
        return 1
    }

    status_message ""

    media_path="$media_dir/$user/$media"

    [[ -d "$media_path" ]] || {
        log_message "cannot find media $media in $media_path"
        return 1
    }

    is_initialized "$media_path" || {
        log_message "media $media not initialized in $media_path"
        return 1
    }

    archive_path="$media_path/$BACKUPS_DIRECTORY/$archive"

    [[ -f "$archive_path" && -r "$archive_path" ]] || {
        echo_message "cannot read archive file $archive_path"
        return 1
    }

    # LabBook 3 archives have a distinctive name, identification is safe
    is_lb30_archive "$archive_path" && {
        [[ $verbose -eq 1 ]] && log_message "Restoring LabBook 3 archive $archive_path"

        fn_restore_lb30 "$archive_path" "$user" || {
            log_message "error restoring LabBook 3 archive $archive_path"
            return 1
        }

        return 0
    }

    is_lb25_archive "$archive_path" && {
        [[ $verbose -eq 1 ]] && log_message "Restoring LabBook 2.5 archive $archive_path"

        fn_restore_lb25 "$archive_path" "$user" || {
            log_message "error restoring LabBook 2.5 archive $archive_path"
            return 1
        }

        return 0
    }

    is_lb29_archive "$archive_path" && {
        [[ $verbose -eq 1 ]] && log_message "Restoring LabBook 2.9 archive $archive_path"

        fn_restore_lb29 "$archive_path" "$user" || {
            log_message "error restoring LabBook 2.9 archive $archive_path"
            return 1
        }

        return 0
    }

    log_message "cannot identify archive type of $archive_path"
    return 1
}

#
# Restore LabBook 2.5 backup
#
# Param:
# - archive
# - user
#
fn_restore_lb25() {
    local encrypted_archive="$1"
    local user="$2"
    local archive_name=""
    local archive_dir=""
    local clear_archive=""
    local dump_file=""

    archive_name="$(basename "$encrypted_archive")"
    archive_dir="$(dirname "$encrypted_archive")"
    clear_archive="$WORK_DIRECTORY/$archive_name"

    fn_decrypt25 "$encrypted_archive" "$clear_archive" "$archive_dir" || {
        log_message "error decrypting LabBook 2.5 archive $encrypted_archive"
        return 1
    }

    # archive structure: tar tf ARCHIVE --no-anchored SIGL.sql would give:
    # backup_SIGL_2019-10-07_23h16m55s/db/SIGL.sql
    tar xf "$clear_archive" --directory="$WORK_DIRECTORY" --strip-components=2 --no-anchored "$LB25_DUMP_FILENAME" || {
        log_message "error extracting SQL dump file $LB25_DUMP_FILENAME from LabBook 2.5 archive $encrypted_archive"
        return 1
    }

    dump_file="$WORK_DIRECTORY/$LB25_DUMP_FILENAME"

    [[ -f "$dump_file" && -r "$dump_file" ]] || {
        log_message "cannot read SQL dump file $dump_file"
        return 1
    }

    fn_loaddb "$dump_file" || {
        log_message "error loading database from SQL dump file $dump_file"
        return 1
    }

    return 0
}

#
# Restore LabBook 3 backup
#
# Param:
# - archive
# - user
#
fn_restore_lb30() {
    local encrypted_archive="$1"
    local user="$2"
    local archive_name=""
    local archive_dir=""
    local clear_archive=""
    local dump_file=""

    archive_name="$(basename "$encrypted_archive")"
    archive_dir="$(dirname "$encrypted_archive")"
    clear_archive="$WORK_DIRECTORY/$archive_name"

    # decrypt archive with key in archive directory
    fn_decrypt29 "$encrypted_archive" "$clear_archive" "$archive_dir" || {
        log_message "error decrypting LabBook 3 archive $encrypted_archive"
        return 1
    }

    # extract and reload sql dump
    tar xf "$clear_archive" --directory="$MOUNTDIR_STORAGE" "$LB30_DUMP_DIR/$LB30_DUMP_FILENAME" || {
        log_message "error extracting SQL dump file $LB30_DUMP_FILENAME from LabBook 3 archive $encrypted_archive"
        return 1
    }

    dump_file="$MOUNTDIR_STORAGE/$LB30_DUMP_DIR/$LB30_DUMP_FILENAME"

    [[ -f "$dump_file" && -r "$dump_file" ]] || {
        log_message "cannot read SQL dump file $dump_file"
        return 1
    }

    fn_loaddb "$dump_file" || {
        log_message "error loading database from SQL dump file $dump_file"
        return 1
    }

    rm -f "$dump_file"

    # restore files
    tar xf "$clear_archive" --directory="$MOUNTDIR_STORAGE" --exclude="$LB30_DUMP_DIR/$LB30_DUMP_FILENAME" || {
        log_message "error extracting files from LabBook 3 archive $encrypted_archive"
        return 1
    }

    return 0
}

#
# Check if an archive is a LabBook 3 backup
#
# True if filename in the form backup_v30_DATABASE_TIMESTAMP.tar.gz.gpg
#
# Param:
# - path to archive
#
is_lb30_archive() {
    local archive_path="$1"

    [[ $(basename "$archive_path") == backup_v30_*_*.tar.gz.gpg ]] || return 1

    return 0
}

#
# Check if an archive is a LabBook 2.5 backup
#
# True if:
# - filename in the form backup_DATABASE_TIMESTAMP.tar.gz
# - a file named LB25_KPRI_FILENAME is present in the same directory
#
# Param:
# - path to archive
#
is_lb25_archive() {
    local archive_path="$1"
    local kpri_path=""

    [[ $(basename "$archive_path") == backup_*_*.tar.gz ]] || return 1

    kpri_path="$(dirname "$archive_path")/$LB25_KPRI_FILENAME"

    [[ -f "$kpri_path" ]] || return 1

    return 0
}

#
# Check if an archive is a LabBook 2.9 backup
#
# True if:
# - filename in the form backup_DATABASE_TIMESTAMP.tar.gz
# - a file named LB29_KPRI_FILENAME is present in the same directory
#
# Param:
# - path to archive
#
is_lb29_archive() {
    local archive_path="$1"
    local kpri_path=""

    [[ $(basename "$archive_path") == backup_*_*.tar.gz ]] || return 1

    kpri_path="$(dirname "$archive_path")/$LB29_KPRI_FILENAME"

    [[ -f "$kpri_path" ]] || return 1

    return 0
}

#
# Are we running in application labbook-python container ?
#
in_app_container() {
    head -1 /proc/1/sched | head -1 | grep supervisord > /dev/null 2>&1 && return 0

    return 1
}

#
# Run backup.sh in another container
#
# Param:
# - user
# - host
# - backup.sh parameters
#
# Return: backup.sh status
#
run_in_container() {
    local user="$1"
    local host="$2"
    local image=""
    local my_absolute_path=""
    local status=0

    shift 2

    [[ $verbose -eq 1 ]] && echo_message "user=$user host=$host cmd=$*"

    image=$(fn_get_my_image "$user" "$host")

    [[ -n "$image" ]] || {
        echo_message "cannot get my image name with $user@$host"
        return 1
    }

    my_absolute_path="$test_path"

    [[ -n "$my_absolute_path" ]] || my_absolute_path="$SCRIPT_ABSOLUTE_DIR/backup.sh"

    SSHPASS=$(printenv $ENV_USER_PASS) \
        sshpass -e \
        ssh -o "StrictHostKeyChecking no" "$user@$host" \
        sudo podman run --rm -v "$MAP_MEDIA" -v "$MAP_STORAGE" "$image" "$my_absolute_path" \
        "$@"
    status=$?

    return $status
}

#
# Get image name of labbook-python running container
#
# Param:
# - user
# - host
#
fn_get_my_image() {
    local user="$1"
    local host="$2"

    SSHPASS=$(printenv $ENV_USER_PASS) \
        sshpass -e \
        ssh -o "StrictHostKeyChecking no" "$user@$host" \
        sudo podman ps --format '{{.Image}}' | grep "$CONTAINER" | head -1 || return 1

    return 0
}

#
# Install FMX public key
#
fn_install_pubkey() {
    local dest_file=""

    dest_file=$(printenv $ENV_KEY_DIR)/"$FMX_KPUB_FILENAME"

    [[ -f "$dest_file" && -r "$dest_file" ]] || {
        install --mode=644 "$SCRIPT_ABSOLUTE_DIR/$FMX_KPUB_FILENAME" "$dest_file" || return 1
    }

    return 0
}

#
# Display error message on stderr and exit
#
error_exit() {
    local message="$*"

    log_message "$message"

    case "$status_format" in
        backup)
            if [[ -n "$message" ]]; then
                backup_message "$message"
            else
                backup_message "UNKNOWN ERROR"
            fi
            ;;

        *)
            if [[ -n "$message" ]]; then
                status_message ""
                status_message "$message"
            else
                status_message ""
                status_message "UNKNOWN ERROR"
            fi
            ;;
    esac


    cleanup
    exit 1
}

#
# Cleanup before exiting
#
cleanup() {
    if [[ $debug -eq 0 ]]; then
        [[ -n "$tmp_workdir" && -d "$tmp_workdir" ]] && rm -rf "$tmp_workdir"
    else
        echo "[DEBUG] keeping workdir $tmp_workdir" >&2
    fi

    cd "$saved_dir" || exit 1
}

#
# Display message on stderr
#
echo_message() {
    echo "[$(date +'%Y-%m-%dT%H:%M:%S')] $*" >&2
}

#
# Log message to file or stderr
#
log_message() {
    if [[ -n "$log_file" ]]; then
        echo "[$(date +'%Y-%m-%dT%H:%M:%S')] $*" >> "$log_file"
    else
        echo "[$(date +'%Y-%m-%dT%H:%M:%S')] $*" >&2
    fi
}

#
# Write message to status file
# If message is empty clears status file
#
status_message() {
    local message="$*"

    if [[ -n "$status_file" ]]; then
        if [[ -n "$message" ]]; then
            echo "$message" >> "$status_file"
        else
            true > "$status_file"
        fi
    fi
}

#
# Write backup message to status file
#
# Empty message 
# OK;YYYY-MM-DD HH:MM:SS
#
# Non-empty message
# ERROR;YYYY-MM-DD HH:MM:SS;message
#
backup_message() {
    if [[ -n "$status_file" ]]; then
        if [[ -z "$*" ]]; then
            echo "OK;$(date +'%Y-%m-%d %H:%M:%S')" > "$status_file"
        else
            echo "ERROR;$(date +'%Y-%m-%d %H:%M:%S');$*" > "$status_file"
        fi
    fi
}

#
# Initialize fake mode and fake status
# Fake mode is active if 'cmd' appears in ENV_TEST_OK or ENV_TEST_KO
# Both variables are in the form cmd,cmd,....
#
# Param:
# - command name
#
init_fake_mode() {
    local cmd_name="$1"

    [[ ",$(printenv $ENV_TEST_OK)," == *,$cmd_name,* ]] && {
        fake_mode=1
        fake_status=0
    }

    [[ ",$(printenv $ENV_TEST_KO)," == *,$cmd_name,* ]] && {
        fake_mode=1
        fake_status=1
    }
}

#######################
# Program starts here #
#######################
debug=0
verbose=0
fake_mode=0
fake_status=0
exit_status=0
saved_dir="$(pwd)"
tmp_workdir=""
input_file=""
output_file=""
status_file=""
status_filename=""
status_format=""
log_file=""
arg_dir=""
cmd=""
root_dir=""
test_path=""
volume=""
archive=""
file_paths=()
user=""
with_uninitialized=0
media=""
when=""
host=""
params_from_file=""
last_backup_ok_file=""
test_mode=0

while getopts "hvi:o:d:V:R:a:p:s:u:Um:w:F:P:T" option; do
    case "$option" in
        h)
            usage
            ;;

        v)
            verbose=1
            ;;

        i)
            input_file="$OPTARG"
            ;;

        o)
            output_file="$OPTARG"
            ;;

        s)
            status_file="$OPTARG"
            ;;

        d)
            arg_dir="$OPTARG"
            ;;

        V)
            volume="$OPTARG"
            ;;

        R)
            root_dir="$OPTARG"
            ;;

        a)
            archive="$OPTARG"
            ;;

        p)
            file_paths=("${file_paths[@]}" "$OPTARG")
            ;;

        u)
            user="$OPTARG"
            ;;

        U)
            with_uninitialized=1
            ;;

        m)
            media="$OPTARG"
            ;;

        w)
            when="$OPTARG"
            ;;

        F)
            params_from_file="$OPTARG"
            ;;

        P)
            test_path="$OPTARG"
            ;;

        T)
            test_mode=1
            ;;

        *)
            usage
            ;;
    esac
done

shift $((OPTIND -1))

cmd="$1"

# for this command we must initialize environment
[[ "$cmd" == "backupauto" ]] && {
    [[ -n "$input_file" ]] || error_exit "$cmd: missing settings file, use -i argument"

    # shellcheck disable=SC1090
    source "$input_file"
}

[[ -n "$params_from_file" ]] && {
    # shellcheck disable=SC1090
    source "$params_from_file"
}

# Initialize log file
def_log_dir=$(printenv $ENV_LOG_DIR)

[[ -n "$def_log_dir" ]] && log_file=$(realpath "$def_log_dir/$cmd")

init_fake_mode "$cmd"

[[ $verbose -eq 1 ]] && log_message "cmd=$cmd fake_mode=$fake_mode fake_status=$fake_status"

# Initialize default status file if -s argument was not used.
# It can stay empty if ENV_STATUS_DIR is not defined, will be verified by each command that needs it.
# Special case for backupauto command, status is expected with backup filename
if [[ -z "$status_file" ]]; then
def_status_dir=$(printenv $ENV_STATUS_DIR)
status_filename="$cmd"

    [[ -n "$def_status_dir" ]] && {
        [[ "$cmd" == "backupauto" ]] && status_filename="backup"

        status_file=$(realpath "$def_status_dir/$status_filename")
    }
fi

case "$cmd" in
    genkey)
        [[ -n "$arg_dir" ]] || arg_dir=$(printenv $ENV_KEY_DIR)

        [[ -n "$arg_dir" ]] || error_exit "$cmd: missing directory, use -d argument or $ENV_KEY_DIR env variable"

        if [[ -n $(printenv $ENV_KEY_PASS) ]]; then
            if [[ $fake_mode -eq 0 ]]; then
                if fn_keyexist "$arg_dir"; then
                    fn_delkeys "$arg_dir" || error_exit "$cmd: cannot remove existing keys in $arg_dir"
                fi

                fn_genkey "$arg_dir" || exit_status=1
            elif [[ $fake_status -eq 1 ]]; then
                error_exit "$cmd: faking failure"
            fi
        else
            error_exit "$cmd: cannot find passphrase in $ENV_KEY_PASS"
        fi

        [[ $exit_status -eq 0 ]] && status_message ""
        ;;

    keyexist)
        [[ -n "$arg_dir" ]] || arg_dir=$(printenv $ENV_KEY_DIR)

        [[ -n "$arg_dir" ]] || error_exit "$cmd: missing directory, use -d argument or $ENV_KEY_DIR env variable"

        if [[ $fake_mode -eq 0 ]]; then
            fn_keyexist "$arg_dir" || exit_status=1
        elif [[ $fake_status -eq 1 ]]; then
            error_exit "$cmd: faking failure"
        fi

        [[ $exit_status -eq 0 ]] && status_message ""
        ;;

    initmedia)
        [[ -n "$user" ]] || user=$(printenv $ENV_USER)

        [[ -n "$user" ]] || error_exit "$cmd: missing user, use -u argument or $ENV_USER env variable"

        [[ -n "$media" ]] || error_exit "$cmd: missing media, use -m argument"

        if [[ $fake_mode -eq 0 ]]; then
            fn_initmedia "$user" "$media" "$test_path" || exit_status=1
        elif [[ $fake_status -eq 1 ]]; then
            error_exit "$cmd: faking failure"
        fi

        [[ $exit_status -eq 0 ]] && status_message ""
        ;;

    listmedia)
        [[ -n "$user" ]] || user=$(printenv $ENV_USER)

        [[ -n "$user" ]] || error_exit "$cmd: missing user, use -u argument or $ENV_USER env variable"

        [[ -n "$status_file" ]] || error_exit "$cmd: missing status file, use -s argument or $ENV_STATUS_DIR env variable"

        [[ -n $(printenv $ENV_HOST) ]] || error_exit "$cmd: cannot find host in $ENV_HOST"

    host=$(printenv $ENV_HOST)

        if [[ $fake_mode -eq 0 ]]; then
            if in_app_container; then
                run_in_container "$user" "$host" -u "$user" -s "$status_file" "$cmd"
            else
                fn_listmedia "$user" "$status_file" "$with_uninitialized" "$test_path" || exit_status=1
            fi
        else
            if [[ $fake_status -eq 0 ]]; then
                status_message ""
                status_message "USB"
            else
                error_exit "$cmd: faking failure"
            fi
        fi
        ;;

    listarchive)
        [[ -n "$user" ]] || user=$(printenv $ENV_USER)

        [[ -n "$user" ]] || error_exit "$cmd: missing user, use -u argument or $ENV_USER env variable"

        [[ -n "$status_file" ]] || error_exit "$cmd: missing status file, use -s argument or $ENV_STATUS_DIR env variable"

        [[ -n "$media" ]] || error_exit "$cmd: missing media, use -m argument"

        if [[ $fake_mode -eq 0 ]]; then
            if in_app_container; then
                run_in_container "$user" "$host" -u "$user" -s "$status_file" -m "$media" "$cmd"
            else
                fn_listarchive "$user" "$status_file" "$media" "$test_path" || exit_status=1
            fi
        else
            if [[ $fake_status -eq 0 ]]; then
                status_message ""
                status_message "backup_SIGL_2018-04-13_15h58m51s.tar.gz"
                status_message "backup_SIGL_2018-04-13_15h58m52s.tar.gz"
                status_message "backup_SIGL_2018-04-13_15h58m53s.tar.gz"
                status_message "backup_SIGL_2018-04-13_16h01m19s.tar.gz"
                status_message "backup_SIGL_2018-04-13_16h03m12s.tar.gz"
                status_message "backup_SIGL_2018-04-13_16h06m42s.tar.gz"
                status_message "backup_SIGL_2018-04-13_16h08m21s.tar.gz"
                status_message "backup_SIGL_2018-04-13_16h10m02s.tar.gz"
                status_message "backup_SIGL_2018-04-13_18h38m32s.tar.gz"
                status_message "backup_SIGL_2018-04-13_18h46m16s.tar.gz"
                status_message "backup_SIGL_2018-04-15_16h54m15s.tar.gz"
                status_message "backup_SIGL_2018-04-24_15h55m54s.tar.gz"
                status_message "backup_SIGL_2018-04-25_09h11m57s.tar.gz"
                status_message "backup_SIGL_2018-04-26_13h46m54s.tar.gz"
                status_message "backup_SIGL_2018-05-03_13h51m04s.tar.gz"
            else
                error_exit "$cmd: faking failure"
            fi
        fi
        ;;

    backup)
        status_format="$cmd"  # backup style error format

        [[ -n "$user" ]] || user=$(printenv $ENV_USER)

        [[ -n "$user" ]] || error_exit "$cmd: missing user, use -u argument or $ENV_USER env variable"

        [[ -n "$status_file" ]] || error_exit "$cmd: missing status file, use -s argument or $ENV_STATUS_DIR env variable"

        [[ -n $(printenv $ENV_KEY_DIR) ]] || error_exit "$cmd: cannot find key directory in $ENV_KEY_DIR"

        [[ -n $(printenv $ENV_DB_HOST) ]] || error_exit "$cmd: cannot find DB host in $ENV_DB_HOST"

        [[ -n $(printenv $ENV_DB_NAME) ]] || error_exit "$cmd: cannot find DB name in $ENV_DB_NAME"

        [[ -n $(printenv $ENV_DB_USER) ]] || error_exit "$cmd: cannot find DB user in $ENV_DB_USER"

        [[ -n $(printenv $ENV_DB_PASS) ]] || error_exit "$cmd: cannot find DB password in $ENV_DB_PASS"

        [[ -n $(printenv $ENV_USER_PASS) ]] || error_exit "$cmd: cannot find user password in $ENV_USER_PASS"

        [[ -n "$media" ]] || error_exit "$cmd: missing media, use -m option"

        fn_install_pubkey || error_exit "$cmd: cannot install FMX public key"

        last_backup_ok_file="$(dirname "$status_file")/$LAST_BACKUP_OK"

        if [[ $fake_mode -eq 0 ]]; then
            if in_app_container; then
                run_in_container "$user" "$(printenv $ENV_HOST)" -u "$user" -s "$status_file" -m "$media" "$cmd"
            else
                fn_backup "$media" "$user" "$test_path"
            fi
        else
            if [[ $fake_status -eq 0 ]]; then
                backup_message ""
                touch "$last_backup_ok_file"
            else
                error_exit "$cmd $media: faking failure"
            fi
        fi
        ;;

    backupauto)
        status_format="backup"  # backup style error format

        [[ -n $(printenv $ENV_STATUS_DIR) ]] || error_exit "$cmd: cannot find status directory in $ENV_STATUS_DIR"

        [[ -n $(printenv $ENV_KEY_DIR) ]] || error_exit "$cmd: cannot find key directory in $ENV_KEY_DIR"

        [[ -n $(printenv $ENV_DB_HOST) ]] || error_exit "$cmd: cannot find DB host in $ENV_DB_HOST"

        [[ -n $(printenv $ENV_DB_NAME) ]] || error_exit "$cmd: cannot find DB name in $ENV_DB_NAME"

        [[ -n $(printenv $ENV_DB_USER) ]] || error_exit "$cmd: cannot find DB user in $ENV_DB_USER"

        [[ -n $(printenv $ENV_DB_PASS) ]] || error_exit "$cmd: cannot find DB password in $ENV_DB_PASS"

        user="$(printenv $ENV_USER)"
        media=""

        # we are running in a container that just started, connected medias are visible
        tmp_status_file="$WORK_DIRECTORY/listmedia"

        fn_listmedia "$user" "$tmp_status_file" 0 "" || error_exit "$cmd: error in listmedia"

        # we want exactly one initialized media
        nb_media=$(wc -l "$tmp_status_file" | awk '{ print $1 }')

        [[ $nb_media -eq 1 ]] && media=$(cat "$tmp_status_file")

        log_message "user=$user nb_media=$nb_media media=$media)"

        rm -f "$tmp_status_file"

        if [[ $nb_media -eq 0 ]]; then
            error_exit "$cmd: cannot find an initialized media"
        elif [[ $nb_media -gt 1 ]]; then
            error_exit "$cmd: more than one initialized media"
        fi

        fn_install_pubkey || error_exit "$cmd: cannot install FMX public key"

        last_backup_ok_file="$(dirname "$status_file")/$LAST_BACKUP_OK"

        fn_backup "$media" "$user" "" || exit_status=1
        ;;

    restore)
        [[ -n "$user" ]] || user=$(printenv $ENV_USER)

        [[ -n "$user" ]] || error_exit "$cmd: missing user, use -u argument or $ENV_USER env variable"

        [[ -n "$media" ]] || error_exit "$cmd: missing media, use -m argument"

        [[ -n "$archive" ]] || error_exit "$cmd: missing archive, use -a argument"

        [[ -n "$status_file" ]] || error_exit "$cmd: missing status file, use -s argument or $ENV_STATUS_DIR env variable"

        [[ -n $(printenv $ENV_KEY_PASS) ]] || error_exit "$cmd: cannot find key passphrase in $ENV_KEY_PASS"

        [[ -n $(printenv $ENV_USER_PASS) ]] || error_exit "$cmd: cannot find user password in $ENV_USER_PASS"

        [[ -n $(printenv $ENV_KEY_DIR) ]] || error_exit "$cmd: cannot find key directory in $ENV_KEY_DIR"

        [[ -n $(printenv $ENV_DB_HOST) ]] || error_exit "$cmd: cannot find DB host in $ENV_DB_HOST"

        [[ -n $(printenv $ENV_DB_NAME) ]] || error_exit "$cmd: cannot find DB name in $ENV_DB_NAME"

        [[ -n $(printenv $ENV_DB_USER) ]] || error_exit "$cmd: cannot find DB user in $ENV_DB_USER"

        [[ -n $(printenv $ENV_DB_PASS) ]] || error_exit "$cmd: cannot find DB password in $ENV_DB_PASS"

        if [[ $fake_mode -eq 0 ]]; then
            fn_restore "$media" "$archive" "$user" "$test_path" || exit_status=1
        elif [[ $fake_status -eq 1 ]]; then
            error_exit "$cmd $media $archive: faking failure"
        fi

        [[ $exit_status -eq 0 ]] && status_message ""
        ;;

    restart)
        [[ -n "$user" ]] || user=$(printenv $ENV_USER)

        [[ -n "$user" ]] || error_exit "$cmd: missing user, use -u argument or $ENV_USER env variable"

        [[ -n $(printenv $ENV_HOST) ]] || error_exit "$cmd: cannot find host in $ENV_HOST"

    host=$(printenv $ENV_HOST)

        [[ -n $(printenv $ENV_USER_PASS) ]] || error_exit "$cmd: cannot find user password in $ENV_USER_PASS"

        if [[ $fake_mode -eq 0 ]]; then
            fn_restart "$user" "$host" || exit_status=1
        elif [[ $fake_status -eq 1 ]]; then
            error_exit "$cmd $user $host: faking failure"
        fi

        [[ $exit_status -eq 0 ]] && status_message ""
        ;;

    progbackup)
        [[ -n "$when" ]] || error_exit "$cmd: missing moment, use -w argument"

        [[ -n "$user" ]] || user=$(printenv $ENV_USER)

        [[ -n "$user" ]] || error_exit "$cmd: missing user, use -u argument or $ENV_USER env variable"

        [[ -n $(printenv $ENV_HOST) ]] || error_exit "$cmd: cannot find host in $ENV_HOST"

    host=$(printenv $ENV_HOST)

        [[ -n $(printenv $ENV_USER_PASS) ]] || error_exit "$cmd: cannot find user password in $ENV_USER_PASS"

        if [[ $fake_mode -eq 0 ]]; then
            fn_progbackup "$when" "$user" "$host" || exit_status=1
        elif [[ $fake_status -eq 1 ]]; then
            error_exit "$cmd $when $user $host: faking failure"
        fi

        [[ $exit_status -eq 0 ]] && status_message ""
        ;;

    encrypt)
        [[ -n "$input_file" ]] ||  error_exit "$cmd: missing input file, use -i argument"

        [[ -n "$arg_dir" ]] ||  error_exit "$cmd: missing directory, use -d argument"

        fn_encrypt "$input_file" "$arg_dir" || exit_status=1
        ;;

    decrypt29)
        [[ -n "$input_file" ]] ||  error_exit "$cmd: missing input file, use -i argument"

        [[ -n "$output_file" ]] ||  error_exit "missing output file, use -o argument"

        if [[ -n "$arg_dir" ]]; then
            if [[ -n $(printenv $ENV_KEY_PASS) ]]; then
                fn_decrypt29 "$input_file" "$output_file" "$arg_dir" || exit_status=1
            else
                error_exit "cannot find passphrase in $ENV_KEY_PASS"
            fi
        else
            fn_decrypt29 "$input_file" "$output_file" "" || exit_status=1
        fi
        ;;

    decrypt25)
        [[ -n "$input_file" ]] ||  error_exit "$cmd: missing input file, use -i argument"

        [[ -n "$output_file" ]] ||  error_exit "missing output file, use -o argument"

        [[ -n "$arg_dir" ]] || arg_dir=$(dirname "$input_file")

        fn_decrypt25 "$input_file" "$output_file" "$arg_dir" || exit_status=1
        ;;

    savefiles)
        [[ "${#file_paths[@]}" -gt 0 ]] ||  error_exit "missing file paths, use -p argument"

        [[ -n "$output_file" ]] ||  error_exit "missing output file, use -o argument"

        [[ -n "$arg_dir" ]] ||  error_exit "missing directory, use -d argument"

        if [[ -n "$volume" ]]; then
            root_dir=$(fn_get_mountpoint "$volume")

            [[ -n "$root_dir" ]] ||  error_exit "cannot get mountpoint of $volume"
        fi

        [[ -n "$root_dir" ]] ||  error_exit "missing root dir, use -R or -V argument"

        fn_savefiles "$output_file" "$archive" "$arg_dir" "$root_dir" "${file_paths[@]}" || exit_status=1
        ;;

    mountpoint)
        [[ -n "$volume" ]] || error_exit "missing volume, use -V argument"

        root_dir=$(fn_get_mountpoint "$volume")
        exit_status=$?

        [[ $exit_status -eq 0 ]] ||  error_exit "error in getting mountpoint of $volume"

        [[ -n "$root_dir" ]] || error_exit "empty root dir"

        echo "$root_dir"
        ;;

    restorefiles)
        [[ -n "$input_file" ]] ||  error_exit "missing input file, use -i argument"

        if [[ -n "$volume" ]]; then
            root_dir=$(fn_get_mountpoint "$volume")

            [[ -n "$root_dir" ]] ||  error_exit "cannot get mountpoint of $volume"
        fi

        [[ -n "$root_dir" ]] ||  error_exit "missing root dir, use -R or -V argument"

        if [[ -n "$arg_dir" ]]; then
            if [[ -n $(printenv $ENV_KEY_PASS) ]]; then
                fn_restorefiles "$input_file" "$archive" "$arg_dir" "$root_dir" || exit_status=1
            else
                error_exit "cannot find passphrase in $ENV_KEY_PASS"
            fi
        else
            fn_restorefiles "$input_file" "$archive" "" "$root_dir" || exit_status=1
        fi
        ;;

    dumpdb)
        [[ -n "$output_file" ]] ||  error_exit "missing output file, use -o argument"

        [[ -n $(printenv $ENV_DB_NAME) ]] || error_exit "$cmd: cannot find DB name in $ENV_DB_NAME"

        if [[ $test_mode -eq 0 ]]; then
            [[ -n $(printenv $ENV_DB_HOST) ]] || error_exit "$cmd: cannot find DB host in $ENV_DB_HOST"

            [[ -n $(printenv $ENV_DB_USER) ]] || error_exit "$cmd: cannot find DB user in $ENV_DB_USER"

            [[ -n $(printenv $ENV_DB_PASS) ]] || error_exit "$cmd: cannot find DB password in $ENV_DB_PASS"
        fi

        fn_dumpdb "$output_file" || exit_status=1
        ;;

    loaddb)
        [[ -n "$input_file" ]] ||  error_exit "missing input file, use -i argument"

        [[ -n $(printenv $ENV_DB_NAME) ]] || error_exit "$cmd: cannot find DB name in $ENV_DB_NAME"

        if [[ $test_mode -eq 0 ]]; then
            [[ -n $(printenv $ENV_DB_HOST) ]] || error_exit "$cmd: cannot find DB host in $ENV_DB_HOST"

            [[ -n $(printenv $ENV_DB_USER) ]] || error_exit "$cmd: cannot find DB user in $ENV_DB_USER"

            [[ -n $(printenv $ENV_DB_PASS) ]] || error_exit "$cmd: cannot find DB password in $ENV_DB_PASS"
        fi

        fn_loaddb "$input_file" || exit_status=1
        ;;

    islb30)
        [[ -n "$input_file" ]] ||  error_exit "missing input file, use -i argument"

        is_lb30_archive "$input_file" || exit_status=1
        ;;

    islb25)
        [[ -n "$input_file" ]] ||  error_exit "missing input file, use -i argument"

        is_lb25_archive "$input_file" || exit_status=1
        ;;

    testfake)
        log_message "fake_mode=$fake_mode fake_status=$fake_status"
        ;;

    *)
        usage "Unknown command=$cmd"
        ;;
esac

cleanup

exit $exit_status
