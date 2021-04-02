#!/bin/bash
# special syntax from ${_XXX_} macros
# shellcheck disable=SC2016,SC2034
#
# Tests for backup.sh
#
# To run a single test use:
# test_backup.sh -- test
#
# 2020-03-26
#
BACKUP_CMD="backup.sh"
BACKUP_SH_PATH="../$BACKUP_CMD"
BASE_OS="ubuntu"
BASE_IMAGE_UBUNTU="docker.io/library/ubuntu:18.04"
PACKAGES_UBUNTU="gnupg2"
BASE_OS="centos"
BASE_IMAGE_CENTOS="docker.io/library/centos:8"
PACKAGES_CENTOS=""  # gnupg2 package is already included in centos8 base image
TEST_IMAGE="localhost/labbook-config-test-gpg-backup"
VOLUME_NAME="labbook-config-test-volume"
WORK_DIRECTORY="/tmp/test_backup"
ENV_PASS="LABBOOK_KEY_PWD"
PASS_TEST="abcdef"
ENV_TEST_OK="LABBOOK_TEST_OK"
ENV_TEST_KO="LABBOOK_TEST_KO"
KPRI_TEST1="kpri.test1.asc"
KPUB_TEST1="kpub.test1.asc"
KPRI_TEST2="kpri.test2.asc"
KPUB_TEST2="kpub.test2.asc"
BACKUPS_DIRECTORY="SIGL_sauvegardes"
ENV_DB_HOST="LABBOOK_DB_HOST"
ENV_DB_NAME="LABBOOK_DB_NAME"
ENV_DB_USER="LABBOOK_DB_USER"
ENV_DB_PASS="LABBOOK_DB_PWD"
TEST_DB_NAME="TEST_SIGL"
TEST_DB_USER="root"
TEST_DB_PASS="root"
DUMP_TEST1="TEST_SIGL.sql"

oneTimeSetUp() {
    local dockerfile=""
    local stdin_option=""
    local my_user_id=0
    local my_group_id=0

    rm -rf "$WORK_DIRECTORY"
    mkdir -p "$WORK_DIRECTORY"

    install -m 755 "$BACKUP_SH_PATH" "$WORK_DIRECTORY" || return 1

    if type podman > /dev/null 2>&1; then
        docker_cmd="podman"
    elif type docker > /dev/null 2>&1; then
        docker_cmd="docker"
    else
        echo "cannot find podman or docker command"
        return 1
    fi

    dockerfile="$WORK_DIRECTORY/Dockerfile"

    echo "Creating $dockerfile for $BASE_OS"

    case "$BASE_OS" in
        ubuntu)
            cat > "$dockerfile" <<%
FROM $BASE_IMAGE_UBUNTU

RUN apt-get update && apt-get install -y $PACKAGES_UBUNTU

RUN mkdir -p $WORK_DIRECTORY
%
            ;;

        centos)
            cat > "$dockerfile" <<%
FROM $BASE_IMAGE_CENTOS

RUN mkdir -p $WORK_DIRECTORY
%
            ;;

        *)
            echo "unknown BASE_OS=$BASE_OS"
            return 1
            ;;
    esac

    case "$docker_cmd" in
        docker)
            # we must own files generated in the container
            my_user_id=$(id -u)
            my_group_id=$(id -g)

            cat >> "$dockerfile" <<%
USER $my_user_id:$my_group_id
%

            # docker build -f - gives the error :
            # "docker build" requires exactly 1 argument(s).
            stdin_option="-"
            ;;

        podman)
            # podman needs a -f option
            # keep it 1 word (no -f -) because of quoting in shell command
            stdin_option="-f-"
            ;;

        *)
            echo "unknown docker_cmd=$docker_cmd"
            return 1
            ;;
    esac

    echo "Building $TEST_IMAGE from $dockerfile"

    # shellcheck disable=SC2002
    cat "$dockerfile" | $docker_cmd build -t "$TEST_IMAGE" "$stdin_option" || {
        echo "cannot build $TEST_IMAGE from $dockerfile"
        return 1
    }

    # In this testing context, we dont care about /dev/urandom insecurity,
    # we map /dev/urandom from the host as /dev/random into the container to speedup gpg operations.
    run_cmd_noenv="$docker_cmd run \
--rm \
-v /dev/urandom:/dev/random \
-v $WORK_DIRECTORY:$WORK_DIRECTORY \
$TEST_IMAGE \
$WORK_DIRECTORY/$BACKUP_CMD"

    run_cmd="$docker_cmd run \
--rm \
-v /dev/urandom:/dev/random \
-v $WORK_DIRECTORY:$WORK_DIRECTORY \
-e $ENV_PASS \
-e $ENV_TEST_OK \
-e $ENV_TEST_KO \
-e $ENV_DB_HOST \
$TEST_IMAGE \
$WORK_DIRECTORY/$BACKUP_CMD"

    echo
    echo "Tests will be run with:"
    echo "$run_cmd"
    echo

    $docker_cmd volume inspect "$VOLUME_NAME" > /dev/null 2>&1 || {
        echo
        echo "Creating container volume $VOLUME_NAME"
        echo
        $docker_cmd volume create "$VOLUME_NAME" > /dev/null || {
            echo "cannot create volume $VOLUME_NAME"
            return 1
        }
    }

    return 0
}

test_minus_h() {
    local first_line=""

    first_line=$($run_cmd -h | grep LabBook | head -1)

    ${_ASSERT_NOT_NULL_} '"$first_line"'
    ${_ASSERT_CONTAINS_} '"$first_line"' '"Utilities for LabBook backup"'
}

test_unknown_cmd() {
    local first_line=""

    first_line=$($run_cmd abc | grep Unknown | head -1)

    ${_ASSERT_EQUALS_} '"$first_line"' '"Unknown command=abc"'
}

test_genkey_nopass() {
    local cmd_stderr=""
    local first_line=""
    local status=0

    cmd_stderr=$($run_cmd_noenv -d "$WORK_DIRECTORY" genkey 2>&1)
    status=$?

    ${_ASSERT_FALSE_} '$status'

    first_line=$(echo "$cmd_stderr" | grep "cannot find" | head -1)

    ${_ASSERT_NOT_NULL_} '"$first_line"'
    ${_ASSERT_CONTAINS_} '"$first_line"' '"cannot find passphrase"'
}

test_genkey_nodir() {
    local genkey_dir=""
    local cmd_stderr=""
    local first_line=""
    local status=0

    export $ENV_PASS="$PASS_TEST"

    genkey_dir="$WORK_DIRECTORY/genkey"
    rm -rf "$genkey_dir"

    cmd_stderr=$($run_cmd -d "$genkey_dir" genkey 2>&1)
    status=$?

    ${_ASSERT_FALSE_} '$status'

    first_line=$(echo "$cmd_stderr" | grep "cannot find" | head -1)

    ${_ASSERT_NOT_NULL_} '"$first_line"'
    ${_ASSERT_CONTAINS_} '"[first_line=$first_line]"' '"$first_line"' '"cannot find directory $genkey_dir"'
}

test_genkey() {
    local genkey_dir=""
    local cmd_stderr=""
    local first_line=""
    local status=0
    local nbkpri=0
    local nbkpub=0
    local kpri=""
    local kpub=""

    export $ENV_PASS="$PASS_TEST"

    genkey_dir="$WORK_DIRECTORY/genkey"
    rm -rf "$genkey_dir"
    mkdir -p "$genkey_dir"

    # generate in empty directory
    cmd_stderr=$($run_cmd -d "$genkey_dir" genkey 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_TRUE_} '$status'

    [[ $verbose -eq 1 ]] && ls -l "$genkey_dir"

    kpri=("$genkey_dir"/kpri.*.asc)

    ${_ASSERT_EQUALS_} '"[kpri=$kpri]"' '1' '${#kpri[@]}'
    ${_ASSERT_TRUE_} '"[kpri=$kpri]"' '"[ -f $kpri ]"'

    kpub=("$genkey_dir"/kpub.*.asc)

    ${_ASSERT_EQUALS_} '"[kpub=$kpub]"' '1' '${#kpub[@]}'
    ${_ASSERT_TRUE_} '"[kpub=$kpub]"' '"[ -f $kpub ]"'

    # (re)generate in non empty directory, should remove previous keys
    cmd_stderr=$($run_cmd -d "$genkey_dir" genkey 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_TRUE_} '$status'

    [[ $verbose -eq 1 ]] && ls -l "$genkey_dir"

    kpri=("$genkey_dir"/kpri.*.asc)

    ${_ASSERT_EQUALS_} '"[kpri=$kpri]"' '1' '${#kpri[@]}'
    ${_ASSERT_TRUE_} '"[kpri=$kpri]"' '"[ -f $kpri ]"'

    kpub=("$genkey_dir"/kpub.*.asc)

    ${_ASSERT_EQUALS_} '"[kpub=$kpub]"' '1' '${#kpub[@]}'
    ${_ASSERT_TRUE_} '"[kpub=$kpub]"' '"[ -f $kpub ]"'

    # fake fail if asked to
    export $ENV_TEST_KO="genkey"

    cmd_stderr=$($run_cmd -d "$genkey_dir" genkey 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "status=$status cmd_stderr=$cmd_stderr"

    ${_ASSERT_FALSE_} '$status'

    first_line=$(echo "$cmd_stderr" | grep "faking" | head -1)

    ${_ASSERT_NOT_NULL_} '"$first_line"'

    return 0
}

test_encrypt_nodir() {
    local cmd_stderr=""
    local first_line=""
    local status=0

    cmd_stderr=$($run_cmd -i somefile encrypt 2>&1)
    status=$?

    ${_ASSERT_FALSE_} '$status'

    first_line=$(echo "$cmd_stderr" | grep "missing" | head -1)

    ${_ASSERT_NOT_NULL_} '"$first_line"'
    ${_ASSERT_CONTAINS_} '"[first_line=$first_line]"' '"$first_line"' '"missing directory"'
}

test_encrypt_nofile() {
    local cmd_stderr=""
    local first_line=""
    local status=0

    cmd_stderr=$($run_cmd_noenv -d somedir encrypt 2>&1)
    status=$?

    ${_ASSERT_FALSE_} '$status'

    first_line=$(echo "$cmd_stderr" | grep "missing" | head -1)

    ${_ASSERT_NOT_NULL_} '"$first_line"'
    ${_ASSERT_CONTAINS_} '"[first_line=$first_line]"' '"$first_line"' '"missing input file"'
}

test_encrypt_dir_not_found() {
    local output_dir=""
    local cmd_stderr=""
    local first_line=""
    local status=0

    output_dir="$WORK_DIRECTORY/encrypt"
    rm -rf "$output_dir"

    cp "$this_script" "$WORK_DIRECTORY" || return 1

    cmd_stderr=$($run_cmd_noenv -i "$WORK_DIRECTORY/$this_script"  -d "$output_dir" encrypt 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_FALSE_} '$status'

    first_line=$(echo "$cmd_stderr" | grep "cannot find" | head -1)

    ${_ASSERT_NOT_NULL_} '"$first_line"'
    ${_ASSERT_CONTAINS_} '"[first_line=$first_line]"' '"$first_line"' '"cannot find directory $output_dir"'
}

test_encrypt_file_not_found() {
    local input_file=""
    local output_dir=""
    local cmd_stderr=""
    local first_line=""
    local status=0

    output_dir="$WORK_DIRECTORY/encrypt"
    rm -rf "$output_dir"
    mkdir -p "$output_dir" || return 1

    input_file="not_a_file"

    cmd_stderr=$($run_cmd_noenv -i "$input_file" -d "$output_dir" encrypt 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_FALSE_} '$status'

    first_line=$(echo "$cmd_stderr" | grep "cannot read" | head -1)

    ${_ASSERT_NOT_NULL_} '"$first_line"'
    ${_ASSERT_CONTAINS_} '"[first_line=$first_line]"' '"$first_line"' '"cannot read file $input_file"'
}

test_encrypt_to_one() {
    local input_file=""
    local output_dir=""
    local output_one_array=""
    local output_file=""
    local cmd_stderr=""
    local first_line=""
    local status=0

    output_dir="$WORK_DIRECTORY/encrypt"
    rm -rf "$output_dir"
    mkdir -p "$output_dir" || return 1

    cp "$this_script" "$WORK_DIRECTORY" || return 1
    cp "$KPUB_TEST1" "$output_dir" || return 1

    [[ $verbose -eq 1 ]] && echo "cmd=$run_cmd_noenv -i $WORK_DIRECTORY/$this_script  -d $output_dir encrypt"

    cmd_stderr=$($run_cmd_noenv -i "$WORK_DIRECTORY/$this_script"  -d "$output_dir" encrypt 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_TRUE_} '$status'

    output_one_array=("$output_dir"/*.gpg)

    [[ $verbose -eq 1 ]] && echo "output_one_array=${output_one_array[*]}"

    ${_ASSERT_EQUALS_} '"[output_one_array=$output_one_array]"' '1' '${#output_one_array[@]}'
    ${_ASSERT_TRUE_} '"[output_one_array=$output_one_array]"' '"[ -f $output_one_array ]"'

    export $ENV_PASS="$PASS_TEST"

    input_file="${output_one_array[0]}"
    output_file="$WORK_DIRECTORY/$this_script.clear"

    cp "$KPRI_TEST1" "$output_dir" || return 1

    cmd_stderr=$($run_cmd -i "$input_file" -o "$output_file"  -d "$output_dir" decryptgpg 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_TRUE_} '$status'
    ${_ASSERT_TRUE_} '"[output_file=$output_file]"' '"[ -f $output_file ]"'

    cmd_stderr=$(diff "$WORK_DIRECTORY/$this_script" "$output_file" 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_TRUE_} '$status'
}

test_encrypt_to_two() {
    local input_file=""
    local output_dir=""
    local output_two_array=""
    local output_file=""
    local cmd_stderr=""
    local first_line=""
    local status=0

    output_dir="$WORK_DIRECTORY/encrypt"
    rm -rf "$output_dir"
    mkdir -p "$output_dir" || return 1

    cp "$this_script" "$WORK_DIRECTORY" || return 1
    cp "$KPUB_TEST1" "$output_dir" || return 1
    cp "$KPUB_TEST2" "$output_dir" || return 1

    [[ $verbose -eq 1 ]] && echo "cmd=$run_cmd_noenv -i $WORK_DIRECTORY/$this_script  -d $output_dir encrypt"

    cmd_stderr=$($run_cmd_noenv -i "$WORK_DIRECTORY/$this_script"  -d "$output_dir" encrypt 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_TRUE_} '$status'

    output_two_array=("$output_dir"/*.gpg)

    [[ $verbose -eq 1 ]] && echo "output_two_array=${output_two_array[*]}"

    ${_ASSERT_EQUALS_} '"[output_two_array=$output_two_array]"' '1' '${#output_two_array[@]}'
    ${_ASSERT_TRUE_} '"[output_two_array=$output_two_array]"' '"[ -f $output_two_array ]"'

    export $ENV_PASS="$PASS_TEST"

    input_file="${output_two_array[0]}"
    output_file="$WORK_DIRECTORY/$this_script.clear"

    # decrypt with key test1
    rm -f "$output_file" || return 1
    cp "$KPRI_TEST1" "$output_dir" || return 1

    cmd_stderr=$($run_cmd -i "$input_file" -o "$output_file"  -d "$output_dir" decryptgpg 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_TRUE_} '$status'
    ${_ASSERT_TRUE_} '"[output_file=$output_file]"' '"[ -f $output_file ]"'

    cmd_stderr=$(diff "$WORK_DIRECTORY/$this_script" "$output_file" 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_TRUE_} '$status'

    # decrypt with key test2
    rm -f "$output_file" || return 1
    rm -f "$output_dir/$KPRI_TEST1" || return 1
    cp "$KPRI_TEST2" "$output_dir" || return 1

    cmd_stderr=$($run_cmd -i "$input_file" -o "$output_file"  -d "$output_dir" decryptgpg 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_TRUE_} '$status'
    ${_ASSERT_TRUE_} '"[output_file=$output_file]"' '"[ -f $output_file ]"'

    cmd_stderr=$(diff "$WORK_DIRECTORY/$this_script" "$output_file" 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_TRUE_} '$status'
}

test_decrypt_noinput() {
    local cmd_stderr=""
    local first_line=""
    local input_file=""
    local status=0

    cmd_stderr=$($run_cmd_noenv decryptgpg 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_FALSE_} '$status'

    first_line=$(echo "$cmd_stderr" | grep "missing" | head -1)

    ${_ASSERT_NOT_NULL_} '"$first_line"'
    ${_ASSERT_CONTAINS_} '"[first_line=$first_line]"' '"$first_line"' '"missing input file"'

    input_file="not_a_file"

    cmd_stderr=$($run_cmd_noenv -i "$input_file" -o /dev/null decryptgpg 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_FALSE_} '$status'

    first_line=$(echo "$cmd_stderr" | grep "cannot read" | head -1)

    ${_ASSERT_NOT_NULL_} '"$first_line"'
    ${_ASSERT_CONTAINS_} '"[first_line=$first_line]"' '"$first_line"' '"cannot read file $input_file"'
}

test_decrypt_nooutput() {
    local cmd_stderr=""
    local first_line=""
    local status=0

    cmd_stderr=$($run_cmd_noenv -i nofile decryptgpg 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_FALSE_} '$status'

    first_line=$(echo "$cmd_stderr" | grep "missing" | head -1)

    ${_ASSERT_NOT_NULL_} '"$first_line"'
    ${_ASSERT_CONTAINS_} '"[first_line=$first_line]"' '"$first_line"' '"missing output file"'
}

test_decrypt_dir_not_found() {
    local output_dir=""
    local cmd_stderr=""
    local first_line=""
    local status=0

    output_dir="$WORK_DIRECTORY/decrypt"
    rm -rf "$output_dir"

    cp "$this_script" "$WORK_DIRECTORY" || return 1

    export $ENV_PASS="$PASS_TEST"

    cmd_stderr=$($run_cmd -i "$WORK_DIRECTORY/$this_script" -o /dev/null -d "$output_dir" decryptgpg 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_FALSE_} '$status'

    first_line=$(echo "$cmd_stderr" | grep "cannot find" | head -1)

    ${_ASSERT_NOT_NULL_} '"$first_line"'
    ${_ASSERT_CONTAINS_} '"[first_line=$first_line]"' '"$first_line"' '"cannot find key directory $output_dir"'
}

test_decrypt_nopass() {
    local output_dir=""
    local cmd_stderr=""
    local first_line=""
    local status=0

    output_dir="$WORK_DIRECTORY/decrypt"
    rm -rf "$output_dir"

    cp "$this_script" "$WORK_DIRECTORY" || return 1

    cmd_stderr=$($run_cmd_noenv -i "$WORK_DIRECTORY/$this_script" -o /dev/null -d "$output_dir" decryptgpg 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_FALSE_} '$status'

    first_line=$(echo "$cmd_stderr" | grep "cannot find" | head -1)

    ${_ASSERT_NOT_NULL_} '"$first_line"'
    ${_ASSERT_CONTAINS_} '"[first_line=$first_line]"' '"$first_line"' '"cannot find passphrase"'
}

test_keyexist_nodir() {
    local cmd_stderr=""
    local first_line=""
    local status=0

    cmd_stderr=$($run_cmd keyexist 2>&1)
    status=$?

    ${_ASSERT_FALSE_} '$status'

    first_line=$(echo "$cmd_stderr" | grep "missing" | head -1)

    ${_ASSERT_NOT_NULL_} '"$first_line"'
    ${_ASSERT_CONTAINS_} '"[first_line=$first_line]"' '"$first_line"' '"missing directory"'
}

test_keyexist_dir_not_found() {
    local keys_dir=""
    local cmd_stderr=""
    local first_line=""
    local status=0

    keys_dir="$WORK_DIRECTORY/keyexist"
    rm -rf "$keys_dir"

    cmd_stderr=$($run_cmd -d "$keys_dir" keyexist 2>&1)
    status=$?

    ${_ASSERT_FALSE_} '$status'

    first_line=$(echo "$cmd_stderr" | grep "cannot find" | head -1)

    ${_ASSERT_NOT_NULL_} '"$first_line"'
    ${_ASSERT_CONTAINS_} '"[first_line=$first_line]"' '"$first_line"' '"cannot find directory $keys_dir"'
}

test_keyexist() {
    local keys_dir=""
    local cmd_stderr=""
    local first_line=""
    local status=0

    keys_dir="$WORK_DIRECTORY/keyexist"
    rm -rf "$keys_dir"
    mkdir -p "$keys_dir" || return 1

    # no key at all
    cmd_stderr=$($run_cmd -d "$keys_dir" keyexist 2>&1)
    status=$?

    ${_ASSERT_FALSE_} '$status'

    # private key only
    cp "$KPRI_TEST1" "$keys_dir" || return 1

    cmd_stderr=$($run_cmd -d "$keys_dir" keyexist 2>&1)
    status=$?

    ${_ASSERT_FALSE_} '$status'

    # now adding public key
    cp "$KPUB_TEST1" "$keys_dir" || return 1

    cmd_stderr=$($run_cmd -d "$keys_dir" keyexist 2>&1)
    status=$?

    ${_ASSERT_TRUE_} '$status'

    # fake fail if asked to
    export $ENV_TEST_KO="keyexist"

    cmd_stderr=$($run_cmd -v -d "$keys_dir" keyexist 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "status=$status cmd_stderr=$cmd_stderr"

    ${_ASSERT_FALSE_} '$status'

    first_line=$(echo "$cmd_stderr" | grep "faking" | head -1)

    ${_ASSERT_NOT_NULL_} '"$first_line"'
}

test_savefiles_nofilepaths() {
    local cmd_stderr=""
    local first_line=""
    local status=0

    cmd_stderr=$($run_cmd_noenv savefiles 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_FALSE_} '$status'

    first_line=$(echo "$cmd_stderr" | grep "missing" | head -1)

    ${_ASSERT_NOT_NULL_} '"$first_line"'
    ${_ASSERT_CONTAINS_} '"[first_line=$first_line]"' '"$first_line"' '"missing file paths"'
}

test_savefiles_nooutput() {
    local cmd_stderr=""
    local first_line=""
    local status=0

    cmd_stderr=$($run_cmd_noenv -p somefile savefiles 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_FALSE_} '$status'

    first_line=$(echo "$cmd_stderr" | grep "missing" | head -1)

    ${_ASSERT_NOT_NULL_} '"$first_line"'
    ${_ASSERT_CONTAINS_} '"[first_line=$first_line]"' '"$first_line"' '"missing output file"'
}

test_savefiles_nodir() {
    local cmd_stderr=""
    local first_line=""
    local status=0

    cmd_stderr=$($run_cmd_noenv -p somefile -o somefile savefiles 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_FALSE_} '$status'

    first_line=$(echo "$cmd_stderr" | grep "missing" | head -1)

    ${_ASSERT_NOT_NULL_} '"$first_line"'
    ${_ASSERT_CONTAINS_} '"[first_line=$first_line]"' '"$first_line"' '"missing directory"'
}

test_savefiles_noroot() {
    local cmd_stderr=""
    local first_line=""
    local status=0

    cmd_stderr=$($run_cmd_noenv -p somefile -o somefile -d somedir -R "" savefiles 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_FALSE_} '$status'

    first_line=$(echo "$cmd_stderr" | grep "missing" | head -1)

    ${_ASSERT_NOT_NULL_} '"$first_line"'
    ${_ASSERT_CONTAINS_} '"[first_line=$first_line]"' '"$first_line"' '"missing root dir"'
}

test_savefiles_mountpoint() {
    local cmd_stderr=""
    local first_line=""
    local status=0

    # this command must run on the host, not in the container
    [[ $verbose -eq 1 ]] && echo "cmd=$WORK_DIRECTORY/$BACKUP_CMD -V $VOLUME_NAME mountpoint"

    cmd_stderr=$($WORK_DIRECTORY/$BACKUP_CMD -V "$VOLUME_NAME" mountpoint 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_TRUE_} '$status'

    first_line=$(echo "$cmd_stderr" | head -1)

    ${_ASSERT_NOT_NULL_} '"$first_line"'
    ${_ASSERT_CONTAINS_} '"[first_line=$first_line]"' '"$first_line"' '"$VOLUME_NAME"'
}

test_savefiles() {
    local input_file=""
    local output_dir=""
    local reference_archive=""
    local root1_dir=""
    local output_archive=""
    local output_file=""
    local cmd_stderr=""
    local first_line=""
    local status=0

    output_dir="$WORK_DIRECTORY/savefiles"
    rm -rf "$output_dir"
    mkdir -p "$output_dir" || return 1

    cp "$this_script" "$WORK_DIRECTORY" || return 1
    cp "$KPUB_TEST1" "$output_dir" || return 1
    cp "$KPUB_TEST2" "$output_dir" || return 1

    # reference archive to work with
    export reference_archive="$WORK_DIRECTORY/repo.tar.gz"

    # It seems there is no way to archive the whole repo from a subdirectory with the <path> argument
    # see https://stackoverflow.com/questions/27451658/git-archive-inside-subdirectory
    # Now we are in labbook_python this is a big archive
    #(cd "$(git rev-parse --show-toplevel)" && git archive --format=tar.gz HEAD) > "$reference_archive" || return 1
    (cd .. && tar czf - --exclude='.*.sw?' .) > "$reference_archive" || return 1

    # extract reference archive in root1/rep1
    export root1_dir="$WORK_DIRECTORY/root1"

    mkdir -p "$root1_dir" || return 1

    (cd "$root1_dir" && mkdir rep1 && cd rep1 && tar xf "$reference_archive") || return 1

    # save rep1 and create an intermediate output archive
    output_archive="$output_dir/repo1.tar.gz"
    output_file1="${output_archive}.gpg"

    [[ $verbose -eq 1 ]] && echo "cmd=$run_cmd_noenv -R $root1_dir/rep1 -d $output_dir -p . -a $output_archive -o $output_file1 savefiles"

    cmd_stderr=$($run_cmd_noenv -R "$root1_dir/rep1" -d "$output_dir" -p . -a "$output_archive" -o $output_file1 savefiles 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_TRUE_} '$status'

    # save rep1 without intermediate output archive
    output_file2="$output_dir/repo2.tar.gz.gpg"

    [[ $verbose -eq 1 ]] && echo "cmd=$run_cmd_noenv -R $root1_dir/rep1 -d $output_dir -p . -o $output_file2 savefiles"

    cmd_stderr=$($run_cmd_noenv -R "$root1_dir/rep1" -d "$output_dir" -p . -o $output_file2 savefiles 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_TRUE_} '$status'

    # extract output_archive in root1/rep2 and compare to rep1
    export output_archive

    (cd "$root1_dir" && mkdir rep2 && cd rep2 && tar xf "$output_archive") || return 1

    cmd_stderr=$(diff "$root1_dir/rep1" "$root1_dir/rep2" 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_TRUE_} '$status'

    # decrypt output_file1 and verify it's identical to output_archive
    export $ENV_PASS="$PASS_TEST"

    output_file="$output_dir/check_repo1.tar.gz"

    cp "$KPRI_TEST1" "$output_dir" || return 1

    cmd_stderr=$($run_cmd -i "$output_file1" -o "$output_file"  -d "$output_dir" decryptgpg 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_TRUE_} '$status'
    ${_ASSERT_TRUE_} '"[output_file=$output_file]"' '"[ -f $output_file ]"'

    cmd_stderr=$(diff "$output_archive" "$output_file" 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_TRUE_} '$status'

    # restore output_file1 in root1/rep3 (with clear archive) and compare to rep1
    # compare clear archive to output_archive
    mkdir -p "$root1_dir/rep3" || return 1

    export $ENV_PASS="$PASS_TEST"

    clear_archive="$output_dir/clear_repo1.tar.gz"

    cp "$KPRI_TEST1" "$output_dir" || return 1

    [[ $verbose -eq 1 ]] && echo "cmd=$run_cmd -i $output_file1 -a $clear_archive -R $root1_dir/rep3 -d $output_dir restorefiles"

    cmd_stderr=$($run_cmd -i "$output_file1" -a "$clear_archive" -R "$root1_dir/rep3" -d "$output_dir" restorefiles 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_TRUE_} '$status'

    # compare rep3 to rep1
    cmd_stderr=$(diff "$root1_dir/rep1" "$root1_dir/rep3" 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_TRUE_} '$status'

    # compare clear_archive to output_archive
    cmd_stderr=$(diff "$output_archive" "$clear_archive" 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_TRUE_} '$status'

    # restore output_file2 in root1/rep4 and compare to rep1
    mkdir -p "$root1_dir/rep4" || return 1

    export $ENV_PASS="$PASS_TEST"

    cp "$KPRI_TEST1" "$output_dir" || return 1

    [[ $verbose -eq 1 ]] && echo "cmd=$run_cmd -i $output_file2 -R $root1_dir/rep4 -d $output_dir restorefiles"

    cmd_stderr=$($run_cmd -i "$output_file2" -R "$root1_dir/rep4" -d "$output_dir" restorefiles 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_TRUE_} '$status'

    # compare rep4 to rep1
    cmd_stderr=$(diff "$root1_dir/rep1" "$root1_dir/rep4" 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_TRUE_} '$status'

    # save rep1 and rep2
    output_archive="$output_dir/repo1_2.tar.gz"
    output_file="${output_archive}.gpg"

    [[ $verbose -eq 1 ]] && echo "cmd=$run_cmd_noenv -R $root1_dir -d $output_dir -p rep1 -p rep2 -a $output_archive -o $output_file savefiles"

    cmd_stderr=$($run_cmd_noenv -R "$root1_dir" -d "$output_dir" -p rep1 -p rep2 -a "$output_archive" -o $output_file savefiles 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_TRUE_} '$status'

    # restore in a different root and compare to original
    root2_dir="$WORK_DIRECTORY/root2"

    mkdir -p "$root2_dir" || return 1

    export $ENV_PASS="$PASS_TEST"

    cp "$KPRI_TEST1" "$output_dir" || return 1

    [[ $verbose -eq 1 ]] && echo "cmd=$run_cmd -i $output_file -R $root2_dir -d $output_dir restorefiles"

    cmd_stderr=$($run_cmd -i "$output_file" -R "$root2_dir" -d "$output_dir" restorefiles 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_TRUE_} '$status'

    # compare the 2 rep1
    cmd_stderr=$(diff "$root1_dir/rep1" "$root2_dir/rep1" 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_TRUE_} '$status'

    # compare the 2 rep2
    cmd_stderr=$(diff "$root1_dir/rep2" "$root2_dir/rep2" 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_TRUE_} '$status'
}

test_copydir() {
    local work_dir=""
    local source_dir=""
    local destination_dir=""
    local cmd_stderr=""
    local first_line=""
    local status=0

    # missing input param
    cmd_stderr=$($run_cmd_noenv copydir 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_FALSE_} '$status'

    first_line=$(echo "$cmd_stderr" | grep "missing" | head -1)

    ${_ASSERT_NOT_NULL_} '"$first_line"'
    ${_ASSERT_CONTAINS_} '"[first_line=$first_line]"' '"$first_line"' '"missing input directory"'

    # missing output param
    cmd_stderr=$($run_cmd_noenv -i input copydir 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_FALSE_} '$status'

    first_line=$(echo "$cmd_stderr" | grep "missing" | head -1)

    ${_ASSERT_NOT_NULL_} '"$first_line"'
    ${_ASSERT_CONTAINS_} '"[first_line=$first_line]"' '"$first_line"' '"missing output directory"'

    # missing source dir
    cmd_stderr=$($run_cmd_noenv -i donotexist -o donotexit copydir 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_FALSE_} '$status'

    first_line=$(echo "$cmd_stderr" | grep "cannot" | head -1)

    ${_ASSERT_NOT_NULL_} '"$first_line"'
    ${_ASSERT_CONTAINS_} '"[first_line=$first_line]"' '"$first_line"' '"cannot find source directory"'

    # copy
    work_dir="$WORK_DIRECTORY/copydir"
    rm -rf "$work_dir"
    mkdir -p "$work_dir" || return 1

    cp "$this_script" "$WORK_DIRECTORY" || return 1

    # reference archive to work with
    export reference_archive="$WORK_DIRECTORY/repo.tar.gz"

    # It seems there is no way to archive the whole repo from a subdirectory with the <path> argument
    # see https://stackoverflow.com/questions/27451658/git-archive-inside-subdirectory
    # Now we are in labbook_python this is a big archive
    #(cd "$(git rev-parse --show-toplevel)" && git archive --format=tar.gz HEAD) > "$reference_archive" || return 1
    (cd .. && tar czf - --exclude='.*.sw?' .) > "$reference_archive" || return 1

    # extract reference archive in source dir
    export source_dir="$work_dir/source"

    mkdir -p "$source_dir" || return 1

    (cd "$source_dir" && tar xf "$reference_archive") || return 1

    # missing destination dir
    cmd_stderr=$($run_cmd_noenv -i "$source_dir" -o donotexit copydir 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_FALSE_} '$status'

    first_line=$(echo "$cmd_stderr" | grep "cannot" | head -1)

    ${_ASSERT_NOT_NULL_} '"$first_line"'
    ${_ASSERT_CONTAINS_} '"[first_line=$first_line]"' '"$first_line"' '"cannot find destination directory"'

    # copy source to destination
    destination_dir="$work_dir/destination"

    mkdir -p "$destination_dir" || return 1

    cmd_stderr=$($run_cmd_noenv -i "$source_dir" -o "$destination_dir" copydir 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_TRUE_} '$status'

    # compare source and destination
    cmd_stderr=$(diff "$source_dir" "$destination_dir" 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_TRUE_} '$status'
}

test_restorefiles_noinput() {
    local cmd_stderr=""
    local first_line=""
    local status=0

    cmd_stderr=$($run_cmd_noenv restorefiles 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_FALSE_} '$status'

    first_line=$(echo "$cmd_stderr" | grep "missing" | head -1)

    ${_ASSERT_NOT_NULL_} '"$first_line"'
    ${_ASSERT_CONTAINS_} '"[first_line=$first_line]"' '"$first_line"' '"missing input file"'
}

test_restorefiles_noroot() {
    local cmd_stderr=""
    local first_line=""
    local status=0

    cmd_stderr=$($run_cmd_noenv -i somefile -R "" restorefiles 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_FALSE_} '$status'

    first_line=$(echo "$cmd_stderr" | grep "missing" | head -1)

    ${_ASSERT_NOT_NULL_} '"$first_line"'
    ${_ASSERT_CONTAINS_} '"[first_line=$first_line]"' '"$first_line"' '"missing root dir"'
}

test_fake_mode() {
    local cmd_stderr=""
    local status=0

    # failing command should fail even if asked to fake OK
    export $ENV_TEST_OK="genkey"

    cmd_stderr=$($run_cmd genkey 2>&1)
    status=$?

    ${_ASSERT_FALSE_} '$status'

    # detect command name at the beginning
    export $ENV_TEST_OK="genkey,other"

    cmd_stderr=$($run_cmd genkey 2>&1)
    status=$?

    ${_ASSERT_FALSE_} '$status'

    # detect command name in the middle
    export $ENV_TEST_OK="other,genkey,other"

    cmd_stderr=$($run_cmd genkey 2>&1)
    status=$?

    ${_ASSERT_FALSE_} '$status'

    # detect command name at the end
    export $ENV_TEST_OK="other,genkey"

    cmd_stderr=$($run_cmd genkey 2>&1)
    status=$?

    ${_ASSERT_FALSE_} '$status'
}

test_initmedia() {
    local cmd_stderr=""
    local first_line=""
    local status=0

    # missing user
    cmd_stderr=$($run_cmd_noenv initmedia 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_FALSE_} '$status'

    first_line=$(echo "$cmd_stderr" | grep "missing" | head -1)

    ${_ASSERT_NOT_NULL_} '"$first_line"'
    ${_ASSERT_CONTAINS_} '"[first_line=$first_line]"' '"$first_line"' '"missing user"'

    # missing media
    cmd_stderr=$($run_cmd_noenv -u user initmedia 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_FALSE_} '$status'

    first_line=$(echo "$cmd_stderr" | grep "missing" | head -1)

    ${_ASSERT_NOT_NULL_} '"$first_line"'
    ${_ASSERT_CONTAINS_} '"[first_line=$first_line]"' '"$first_line"' '"missing media"'

    export $ENV_DB_HOST="localhost"

    media_dir="$WORK_DIRECTORY/media"
    user="someuser"
    media="USB"
    expected_dir="$media_dir/$user/$media/$BACKUPS_DIRECTORY"

    # start clean
    rm -rf "$media_dir"

    mkdir -p "$media_dir/$user"

    # wrong media
    cmd_stderr=$($run_cmd -u "$user" -m "wrongmedia" -P "$media_dir" initmedia 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_FALSE_} '$status'

    first_line=$(echo "$cmd_stderr" | grep "media" | head -1)

    ${_ASSERT_NOT_NULL_} '"$first_line"'
    ${_ASSERT_CONTAINS_} '"[first_line=$first_line]"' '"$first_line"' '"cannot find media"'

    # simulate a media
    mkdir -p "$media_dir/$user/$media"

    # initialize media
    cmd_stderr=$($run_cmd -u "$user" -m "$media" -P "$media_dir" initmedia 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_TRUE_} '$status'

    # verify expectation
    [[ $verbose -eq 1 ]] && ls -l "$expected_dir"

    test -d "$expected_dir"
    status=$?

    ${_ASSERT_TRUE_} '$status'

    # second initialization must succeed
    cmd_stderr=$($run_cmd -u "$user" -m "$media" -P "$media_dir" initmedia 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_TRUE_} '$status'
}

test_listmedia() {
    local cmd_stderr=""
    local first_line=""
    local status=0

    # missing user
    cmd_stderr=$($run_cmd_noenv listmedia 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_FALSE_} '$status'

    first_line=$(echo "$cmd_stderr" | grep "missing" | head -1)

    ${_ASSERT_NOT_NULL_} '"$first_line"'
    ${_ASSERT_CONTAINS_} '"[first_line=$first_line]"' '"$first_line"' '"missing user"'

    # missing status file
    cmd_stderr=$($run_cmd_noenv -u user listmedia 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_FALSE_} '$status'

    first_line=$(echo "$cmd_stderr" | grep "missing" | head -1)

    ${_ASSERT_NOT_NULL_} '"$first_line"'
    ${_ASSERT_CONTAINS_} '"[first_line=$first_line]"' '"$first_line"' '"missing status file"'

    export $ENV_DB_HOST="localhost"

    # we use the same statusfile for all commands
    status_file="$WORK_DIRECTORY/listmedia"
    expected_file="$WORK_DIRECTORY/expected"

    media_dir="$WORK_DIRECTORY/media"
    user="someuser"
    media1="USB1"
    media2="USB2"

    # start clean
    rm -rf "$media_dir"

    # simulate no media
    mkdir -p "$media_dir/$user"

    # empty list
    cmd_stderr=$($run_cmd -u "$user" -s "$status_file" -P "$media_dir" listmedia 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_TRUE_} '$status'

    # check result
    [[ $verbose -eq 1 ]] && { echo "status_file:" ; cat "$status_file" ; }

    true > "$expected_file"

    cmd_stderr=$(diff "$status_file" "$expected_file" 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_TRUE_} '$status'

    # simulate some media
    mkdir -p "$media_dir/$user/$media1"
    mkdir -p "$media_dir/$user/$media2/$BACKUPS_DIRECTORY"  # media2 is initialized

    # list all media even unitialized
    cmd_stderr=$($run_cmd -u "$user" -s "$status_file" -U -P "$media_dir" listmedia 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_TRUE_} '$status'

    # check result
    [[ $verbose -eq 1 ]] && { echo "status_file:" ; cat "$status_file" ; }

    cat > "$expected_file" <<%
$media1
$media2
%

    cmd_stderr=$(diff "$status_file" "$expected_file" 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_TRUE_} '$status'

    # list all initialized media
    cmd_stderr=$($run_cmd -u "$user" -s "$status_file" -P "$media_dir" listmedia 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_TRUE_} '$status'

    # check result
    [[ $verbose -eq 1 ]] && { echo "status_file:" ; cat "$status_file" ; }

    cat > "$expected_file" <<%
$media2
%

    cmd_stderr=$(diff "$status_file" "$expected_file" 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_TRUE_} '$status'
}

test_listarchive() {
    local cmd_stderr=""
    local first_line=""
    local status=0

    # missing user
    cmd_stderr=$($run_cmd_noenv listarchive 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_FALSE_} '$status'

    first_line=$(echo "$cmd_stderr" | grep "missing" | head -1)

    ${_ASSERT_NOT_NULL_} '"$first_line"'
    ${_ASSERT_CONTAINS_} '"[first_line=$first_line]"' '"$first_line"' '"missing user"'

    # missing status file
    cmd_stderr=$($run_cmd_noenv -u user listarchive 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_FALSE_} '$status'

    first_line=$(echo "$cmd_stderr" | grep "missing" | head -1)

    ${_ASSERT_NOT_NULL_} '"$first_line"'
    ${_ASSERT_CONTAINS_} '"[first_line=$first_line]"' '"$first_line"' '"missing status file"'

    export $ENV_DB_HOST="localhost"

    # we use the same statusfile for all commands
    status_file="$WORK_DIRECTORY/listarchive"
    expected_file="$WORK_DIRECTORY/expected"

    media_dir="$WORK_DIRECTORY/media"
    user="someuser"
    media="USB"

    # start clean
    rm -rf "$media_dir"

    # missing media
    cmd_stderr=$($run_cmd_noenv -u "$user" -s "$status_file" listarchive 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_FALSE_} '$status'

    first_line=$(echo "$cmd_stderr" | grep "missing" | head -1)

    ${_ASSERT_NOT_NULL_} '"$first_line"'
    ${_ASSERT_CONTAINS_} '"[first_line=$first_line]"' '"$first_line"' '"missing media"'

    # media absent
    mkdir -p "$media_dir/$user"

    cmd_stderr=$($run_cmd -u "$user" -s "$status_file" -m "$media" -P "$media_dir" listarchive 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_FALSE_} '$status'

    first_line=$(echo "$cmd_stderr" | grep "media" | head -1)

    ${_ASSERT_NOT_NULL_} '"$first_line"'
    ${_ASSERT_CONTAINS_} '"[first_line=$first_line]"' '"$first_line"' '"cannot find media"'

    # media not initialized
    mkdir -p "$media_dir/$user/$media"

    cmd_stderr=$($run_cmd -u "$user" -s "$status_file" -m "$media" -P "$media_dir" listarchive 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_FALSE_} '$status'

    first_line=$(echo "$cmd_stderr" | grep "media" | head -1)

    ${_ASSERT_NOT_NULL_} '"$first_line"'
    ${_ASSERT_CONTAINS_} '"[first_line=$first_line]"' '"$first_line"' '"not initialized"'

    # initialize media
    backup_dir="$media_dir/$user/$media/$BACKUPS_DIRECTORY"
    mkdir -p "$backup_dir"

    # empty list
    cmd_stderr=$($run_cmd -u "$user" -s "$status_file" -m "$media" -P "$media_dir" listarchive 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_TRUE_} '$status'

    # check result
    [[ $verbose -eq 1 ]] && { echo "status_file:" ; cat "$status_file" ; }

    true > "$expected_file"

    cmd_stderr=$(diff "$status_file" "$expected_file" 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_TRUE_} '$status'

    # simulate some archives
    backup1="backup_SIGL_2018-04-13_15h58m51s.tar.gz"
    backup2="backup_SIGL_2018-04-13_15h58m52s.tar.gz"
    backup3="backup_SIGL_2018-04-13_15h58m53s.tar.gz"
    backup4="backup_SIGL_2018-04-13_16h01m19s.tar.gz"

    touch "$backup_dir/$backup1"
    touch "$backup_dir/$backup2"
    touch "$backup_dir/$backup3"
    touch "$backup_dir/$backup4"

    # list archives
    cmd_stderr=$($run_cmd -u "$user" -s "$status_file" -m "$media" -P "$media_dir" listarchive 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_TRUE_} '$status'

    # check result
    [[ $verbose -eq 1 ]] && { echo "status_file:" ; cat "$status_file" ; }

    cat > "$expected_file" <<%
$backup1
$backup2
$backup3
$backup4
%

    cmd_stderr=$(diff "$status_file" "$expected_file" 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_TRUE_} '$status'
}

test_mountpoint() {
    local cmd_stderr=""
    local first_line=""
    local status=0

    # this command must run on the host, not in the container
    [[ $verbose -eq 1 ]] && echo "cmd=$WORK_DIRECTORY/$BACKUP_CMD -V $VOLUME_NAME mountpoint"

    cmd_stderr=$($WORK_DIRECTORY/$BACKUP_CMD -V "$VOLUME_NAME" mountpoint 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_TRUE_} '$status'

    first_line=$(echo "$cmd_stderr" | head -1)

    ${_ASSERT_NOT_NULL_} '"$first_line"'
    ${_ASSERT_CONTAINS_} '"[first_line=$first_line]"' '"$first_line"' '"$VOLUME_NAME"'
}

test_database() {
    local cmd_stderr=""
    local first_line=""
    local status=0

    # skip if mysql is not available or if we dont have access
    type mysql > /dev/null 2>&1 || startSkipping
    type mysqldump > /dev/null 2>&1 || startSkipping

    echo "drop database if exists $TEST_DB_NAME;" | \
        mysql --user "$TEST_DB_USER" --password="$TEST_DB_PASS" > /dev/null 2>&1 || startSkipping

    # we do not use containers for this test
    export $ENV_DB_HOST=""
    export $ENV_DB_NAME="$TEST_DB_NAME"
    export $ENV_DB_USER="$TEST_DB_USER"
    export $ENV_DB_PASS="$TEST_DB_PASS"

    [[ $verbose -eq 1 ]] && echo "cmd=$WORK_DIRECTORY/$BACKUP_CMD -V $VOLUME_NAME loaddb"

    # load database
    input_file="$WORK_DIRECTORY/input.sql"

    cp "$DUMP_TEST1" "$input_file" || return 1

    cmd_stderr=$($WORK_DIRECTORY/$BACKUP_CMD -i "$input_file" -T loaddb 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_TRUE_} '$status'

    # verify database is present
    cmd_stderr=$(echo "use $TEST_DB_NAME;" | mysql --user "$TEST_DB_USER" --password="$TEST_DB_PASS" > /dev/null 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_TRUE_} '$status'

    # dump database
    output_file="$WORK_DIRECTORY/output.sql"

    cmd_stderr=$($WORK_DIRECTORY/$BACKUP_CMD -o "$output_file" -T dumpdb 2>&1)
    status=$?

    [[ $verbose -eq 1 ]] && echo "cmd_stderr=$cmd_stderr"

    ${_ASSERT_TRUE_} '$status'

    # output file should be present
    test -f "$output_file"
    status=$?

    ${_ASSERT_TRUE_} '$status'
}

oneTimeTearDown() {
    if [[ $verbose -eq 1 ]]; then
        echo "Verbose mode: skipping rm -rf $WORK_DIRECTORY"
    else
        rm -rf "$WORK_DIRECTORY"
    fi

    cd "$saved_dir" || exit 1
}

docker_cmd=""
run_cmd=""
run_cmd_noenv=""
# change this flag manually for debug phase
verbose=0
this_script=$(basename "$0")
saved_dir=$(pwd)

# shellcheck disable=SC1091
source ./shunit2
