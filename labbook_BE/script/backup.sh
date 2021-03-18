#!/bin/bash
#
# Utilities for LabBook 3 backup
#
# 2021-03-18
#
ENV_PASS="LABBOOK_KEY_PWD"
ENV_KEY_DIR="LABBOOK_KEY_DIR"
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
            [[ $verbose -eq 1 ]] && echo_message "Cannot found $pubkey_file matching $privkey_file"
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
    echo "[$(date +'%Y-%m-%dT%H:%M:%S')] $*" >&2
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

#######################
# Program starts here #
#######################
debug=0
verbose=0
exit_status=0
saved_dir="$(pwd)"
tmp_workdir=""
input_file=""
output_file=""
arg_dir=""
cmd=""
root_dir="."
volume=""
archive=""
file_paths=()

while getopts "hvi:o:d:V:R:a:p:" option; do
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

        *)
            usage
            ;;
    esac
done

shift $((OPTIND -1))

cmd="$1"

[[ $verbose -eq 1 ]] && echo_message "cmd=$cmd"

case "$cmd" in
    genkey)
        [[ -n "$arg_dir" ]] || arg_dir=$(printenv $ENV_KEY_DIR)

        [[ -n "$arg_dir" ]] || error_exit "missing directory, use -d argument or $ENV_KEY_DIR env variable"

        if [[ -n $(printenv $ENV_PASS) ]]; then
            fn_genkey "$arg_dir" || exit_status=1
        else
            error_exit "cannot find passphrase in $ENV_PASS"
        fi
        ;;

    keyexist)
        [[ -n "$arg_dir" ]] || arg_dir=$(printenv $ENV_KEY_DIR)

        [[ -n "$arg_dir" ]] || error_exit "missing directory, use -d argument or $ENV_KEY_DIR env variable"

        fn_keyexist "$arg_dir" || exit_status=1
        ;;

    encrypt)
        [[ -n "$input_file" ]] ||  error_exit "missing input file, use -i argument"

        [[ -n "$arg_dir" ]] ||  error_exit "missing directory, use -d argument"

        fn_encrypt "$input_file" "$arg_dir" || exit_status=1
        ;;

    decrypt)
        [[ -n "$input_file" ]] ||  error_exit "missing input file, use -i argument"

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

    *)
        usage "Unknown command=$cmd"
        ;;
esac

cleanup
exit $exit_status
