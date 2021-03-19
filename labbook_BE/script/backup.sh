#!/bin/bash
#
# Utilities for LabBook 3 backup
#
# 2021-03-18
#
ENV_PASS="LABBOOK_KEY_PWD"
ENV_KEY_DIR="LABBOOK_KEY_DIR"
ENV_STATUS_DIR="LABBOOK_STATUS_DIR"
ENV_LOG_DIR="LABBOOK_LOG_DIR"
ENV_TEST_OK="LABBOOK_TEST_OK"
ENV_TEST_KO="LABBOOK_TEST_KO"
ENV_USER="LABBOOK_USER"
KEY_REAL_NAME="LabBook Backup Key"
WORK_DIRECTORY="/tmp"

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
    echo "Passphrase for gpg operations is read from $ENV_PASS environment variable"
    echo
    echo "Commands as described in api.md:"
    echo "  genkey            Create key pair in DIR"
    echo "  keyexist          Check key pair exist in DIR"
    echo "  initmedia         Initialize media"
    echo "  listmedia         List medias"
    echo
    echo "Internal commands used for testing:"
    echo "  encrypt           Encrypt INPUT_FILE to DIR/INPUT_FILE.gpg and copy keys to DIR"
    echo "  decrypt           Decrypt INPUT_FILE to OUTPUT_FILE using key in DIR"
    echo "                    If DIR is omitted key should be in the current keyring"
    echo "  savefiles         Archive FILE_PATH(s) to ARCHIVE_PATH then encrypt archive to OUTPUT_FILE using keys in DIR"
    echo "                    If specified, FILE_PATHs are relative to ROOT_PATH or VOLUME moutpoint"
    echo "                    ARCHIVE_PATH can be omitted"
    echo "  restorefiles      Decrypt INPUT_FILE to ARCHIVE_PATH then restore to ROOT_PATH or VOLUME moutpoint"
    echo "  mountpoint        Display mountpoint directory for VOLUME. Used for testing"
    echo "  testfake          Display faking mode. Used for testing"
    echo
    echo "Options:"
    echo "  -h                Display this help and exit"
    echo "  -v                Verbose mode"
    echo "  -i INPUT_FILE     Input file"
    echo "  -o OUTPUT_FILE    Output file"
    echo "  -d DIR            Directory for input or output"
    echo "  -a ARCHIVE_PATH   Archive path"
    echo "  -V VOLUME         Container volume"
    echo "  -R ROOT_PATH      Root path"
    echo "  -p FILE_PATH      File path, may be repeated"
    echo "  -s STATUS_FILE    Status file [default=$ENV_STATUS_DIR/command]"
    echo "  -u USER           Linux user [default=$ENV_USER]"
    echo "  -U                Include uninitialized medias in list"
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

    passwd=$(printenv $ENV_PASS)

    [[ $verbose -eq 1 ]] && echo_message "Generating keys with file=$gen_key_cmd_file"

    echo "$passwd" | gpg --pinentry-mode loopback --batch --passphrase-fd 0 --generate-key "$gen_key_cmd_file"
    status=$?

    [[ $status -eq 0 ]] || {
        echo_message "error generating keys"
        return 1
    }

    fpr=$(gpg --list-keys --with-colon "$KEY_REAL_NAME" | grep "^fpr" | cut -d: -f10)
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
# Decrypt a file
#
# Params:
# - input file to decrypt
# - output file
# - directory containing private key (if empty use current keyring)
#
fn_decrypt() {
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

        passwd=$(printenv $ENV_PASS)

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
# Save files to an encrypted archive
#
# Params:
# - final encrypted archive
# - intermediate clear archive (may be empty)
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

        passwd=$(printenv $ENV_PASS)

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

    if type podman > /dev/null 2>&1; then
        docker_cmd="podman"
    elif type docker > /dev/null 2>&1; then
        docker_cmd="docker"
    else
        echo_message "cannot find podman or docker to query volume"
        return 1
    fi

    mountpoint=$($docker_cmd volume inspect "$volume_name" | grep -i mountpoint | sed -e 's/.*point": *"//' | sed -e 's/".*$//' 2> /dev/null)
    cmd_status=$?

    if [[ $cmd_status -eq 0 ]]; then
        echo "$mountpoint"
        return 0
    else
        echo_message "error in $docker_cmd volume inspect $volume_name"
        return 1
    fi
}

#
# Display error message on stderr and exit
#
error_exit() {
    log_message "$*"

    case "$status_format" in
        backup)
            if [[ -n "$*" ]]; then
                backup_message "$*"
            else
                backup_message "UNKNOWN ERROR"
            fi
            ;;

        *)
            if [[ -n "$*" ]]; then
                status_message ""
                status_message "$*"
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
    if [[ -n "$status_file" ]]; then
        if [[ -n "$*" ]]; then
            echo "$*" >> "$status_file"
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
# Fake mode is active if 'cmd' appears in ENV_TEST_OK or ENV_TEST_KO (of the form cmd,cmd,cmd)
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
status_format=""
log_file=""
arg_dir=""
cmd=""
root_dir="."
volume=""
archive=""
file_paths=()
user=""
with_uninitialized=0
media=""

while getopts "hvi:o:d:V:R:a:p:s:u:Um:" option; do
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

        *)
            usage
            ;;
    esac
done

shift $((OPTIND -1))

cmd="$1"

# Initialize log file
def_log_dir=$(printenv $ENV_LOG_DIR)

[[ -n "$def_log_dir" ]] && log_file=$(realpath "$def_log_dir/$cmd")

init_fake_mode "$cmd"

[[ $verbose -eq 1 ]] && log_message "cmd=$cmd fake_mode=$fake_mode fake_status=$fake_status"

# Initialize default status file if -s argument was not used.
# It can stay empty if ENV_STATUS_DIR is not defined, will be verified by each command that needs it.
if [[ -z "$status_file" ]]; then
def_status_dir=$(printenv $ENV_STATUS_DIR)

    [[ -n "$def_status_dir" ]] && status_file=$(realpath "$def_status_dir/$cmd")
fi

case "$cmd" in
    genkey)
        [[ -n "$arg_dir" ]] || arg_dir=$(printenv $ENV_KEY_DIR)

        [[ -n "$arg_dir" ]] || error_exit "$cmd: missing directory, use -d argument or $ENV_KEY_DIR env variable"

        if [[ -n $(printenv $ENV_PASS) ]]; then
            if [[ $fake_mode -eq 0 ]]; then
                fn_genkey "$arg_dir" || exit_status=1
            elif [[ $fake_status -eq 1 ]]; then
                error_exit "$cmd: faking failure"
            fi
        else
            error_exit "$cmd: cannot find passphrase in $ENV_PASS"
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
            error_exit "$cmd $media: not implemented"
        elif [[ $fake_status -eq 1 ]]; then
            error_exit "$cmd: faking failure"
        fi

        [[ $exit_status -eq 0 ]] && status_message ""
        ;;

    listmedia)
        [[ -n "$user" ]] || user=$(printenv $ENV_USER)

        [[ -n "$user" ]] || error_exit "$cmd: missing user, use -u argument or $ENV_USER env variable"

        [[ -n "$status_file" ]] || error_exit "$cmd: missing status file, use -s argument or $ENV_STATUS_DIR env variable"

        if [[ $fake_mode -eq 0 ]]; then
            error_exit "$cmd $with_uninitialized: not implemented"
        else
            if [[ $fake_status -eq 0 ]]; then
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
            error_exit "$cmd $media: not implemented"
        else
            if [[ $fake_status -eq 0 ]]; then
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

        if [[ -z "$media" ]]; then
            error_exit "$cmd with unique media: not implemented"
        fi

        if [[ $fake_mode -eq 0 ]]; then
            error_exit "$cmd $media: not implemented"
        else
            if [[ $fake_status -eq 0 ]]; then
                backup_message ""
            else
                error_exit "$cmd $media: faking failure"
            fi
        fi
        ;;

    restore)
        [[ -n "$user" ]] || user=$(printenv $ENV_USER)

        [[ -n "$user" ]] || error_exit "$cmd: missing user, use -u argument or $ENV_USER env variable"

        [[ -n "$media" ]] || error_exit "$cmd: missing media, use -m argument"

        [[ -n "$archive" ]] || error_exit "$cmd: missing archive, use -a argument"

        if [[ $fake_mode -eq 0 ]]; then
            error_exit "$cmd $media $archive: not implemented"
        elif [[ $fake_status -eq 1 ]]; then
            error_exit "$cmd $media $archive: faking failure"
        fi

        [[ $exit_status -eq 0 ]] && status_message ""
        ;;

    encrypt)
        [[ -n "$input_file" ]] ||  error_exit "$cmd: missing input file, use -i argument"

        [[ -n "$arg_dir" ]] ||  error_exit "$cmd: missing directory, use -d argument"

        fn_encrypt "$input_file" "$arg_dir" || exit_status=1
        ;;

    decrypt)
        [[ -n "$input_file" ]] ||  error_exit "$cmd: missing input file, use -i argument"

        [[ -n "$output_file" ]] ||  error_exit "missing output file, use -o argument"

        if [[ -n "$arg_dir" ]]; then
            if [[ -n $(printenv $ENV_PASS) ]]; then
                fn_decrypt "$input_file" "$output_file" "$arg_dir" || exit_status=1
            else
                error_exit "cannot find passphrase in $ENV_PASS"
            fi
        else
            fn_decrypt "$input_file" "$output_file" "" || exit_status=1
        fi
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
        [[ -n "$volume" ]] ||  error_exit "missing volume, use -V argument"

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
            if [[ -n $(printenv $ENV_PASS) ]]; then
                fn_restorefiles "$input_file" "$archive" "$arg_dir" "$root_dir" || exit_status=1
            else
                error_exit "cannot find passphrase in $ENV_PASS"
            fi
        else
            fn_restorefiles "$input_file" "$archive" "" "$root_dir" || exit_status=1
        fi
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
