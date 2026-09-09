#!/bin/bash
#
# Start gunicorn to serve the application in production mode
#
# PhB, 08/10/14
# PHM, 01/10/15 -> adaptation aux serveurs d'applications Web (amicare, borne, ...)
# AlC, 18/11/19 -> adaptation pour le projet labbook

# PHM le 19/11/19 : Passage Apache->gunicorn via port 8082
HOST="localhost"
PORT="8082"

#############
# Functions #
#############
#
# Display use
#
usage()
{
echo
echo "Run Gunicorn Labbook BACK END"
echo
echo "Use :"
echo "  $0 -h"
echo "  $0 -r"
echo
echo "Options:"
echo "  -h                 This help"
echo "  -r                 Add reload option"
echo
exit 2
}

######################
# START              #
######################
opt_reload=""

while getopts "hr" option
do
    case "$option" in
    h)
    usage
    ;;

    r)
    opt_reload="--reload"
    ;;

    *)
    echo "option $option unknown"
    usage
    ;;
    esac
done

test "$LABBOOK_DEBUG" -eq 1 && opt_reload="--reload"

# Application name
APP_NAME=labbook_BE

HOME_APP=/home/apps/$APP_NAME
APP_DIR=${HOME_APP}/${APP_NAME}
VENV_DIR=${APP_DIR}/venv
LOGS_DIR=/home/apps/logs
LOGS_PERM=/storage/log
GUNICORN_DIR=${HOME_APP}/gunicorn
GUNICORN_TIMEOUT=0  # Because restore and backup scripts that run synchronously

SHARED_SECRET=/storage/key/secret_key.py

# shellcheck disable=SC1091
source ${VENV_DIR}/bin/activate

# --- wait FE port ---
FE_HOST="localhost"
FE_PORT=8081
FE_WAIT_SEC=120

echo "[BE] wait FE ${FE_HOST}:${FE_PORT} ${FE_WAIT_SEC}s max"
for i in $(seq 1 "$FE_WAIT_SEC"); do
  # bash built-in TCP check (no curl/nc dependency)
  (echo > /dev/tcp/"$FE_HOST"/"$FE_PORT") >/dev/null 2>&1 && { echo "[BE] FE ready"; break; }
  sleep 1
done
(echo > /dev/tcp/"$FE_HOST"/"$FE_PORT") >/dev/null 2>&1 || { echo "[BE] FE not reachable"; exit 1; }
# --- end wait FE port ---

# create Gunicorn directory if necessary
mkdir -p ${GUNICORN_DIR}
mkdir -p ${LOGS_DIR}
mkdir -p "$(dirname "$SHARED_SECRET")"

# Generate shared SECRET_KEY if missing (can be omitted if FE starts first)
if [ ! -f "$SHARED_SECRET" ]; then
    echo "Shared SECRET_KEY file not found. Waiting for FE to generate it..."
    while [ ! -f "$SHARED_SECRET" ]; do
        sleep 1
    done
fi

# Operating environment
export LOCAL_SETTINGS=${HOME_APP}/local_settings.py

# if local_settings file doesnt exist we create one
# AlC 10/07/2025 comment replace by generate secret key
# from local_settings.py.sample in app directory
# test -f $LOCAL_SETTINGS || {
#    echo "$LOCAL_SETTINGS not found, local_settings.py file create"
#
#    cp ${APP_DIR}/local_settings.py.sample $LOCAL_SETTINGS || exit 1
# }

LOCAL_SETTINGS_SAMPLE=${APP_DIR}/local_settings.py.sample

# Create local_settings.py if missing, inject shared SECRET_KEY
if [ ! -f "$LOCAL_SETTINGS" ]; then
    echo "Creating $LOCAL_SETTINGS from sample and injecting shared SECRET_KEY"

    cp "$LOCAL_SETTINGS_SAMPLE" "$LOCAL_SETTINGS" || exit 1

    sed -i "/^SECRET_KEY/c\\$(cat $SHARED_SECRET)" "$LOCAL_SETTINGS"
fi

cd ${APP_DIR} || exit 1

# --- FE OAuth client secret for Alembic (export to env) ---
# Wait for the FE-generated shared secret file; do not generate anything here.
OAUTH_SHARED="$(dirname "$SHARED_SECRET")/oauth_client_secret.py"

echo "Waiting FE OAuth client secret..."
while [ ! -s "$OAUTH_SHARED" ]; do sleep 1; done

# Read the Python constant into an env var for the BE app (and migrations if needed).
export LABBOOK_OAUTH_FE_SECRET="$(
  python3 -c "ns={}; exec(open('$OAUTH_SHARED').read(), ns); print(ns.get('OAUTH_CLIENT_SECRET',''))"
)"
# --- end FE OAuth secret block ---

# run alembic upgrade
alembic upgrade head >> ${LOGS_PERM}/alembic.out 2>&1

# preload libreoffice
/usr/bin/python3 -m unoserver.server >> ${LOGS_PERM}/unoserver.out 2>&1 &

# Gunicorn is installed in the virtual environment
# When started by supervisord, exec is necessary for the signals to reach gunicorn.
# Another approach with catched signals is described here :
# http://serverfault.com/questions/425132/controlling-tomcat-with-supervisor
exec gunicorn \
    $opt_reload \
    --timeout ${GUNICORN_TIMEOUT} \
    --pid ${GUNICORN_DIR}/gunicorn.pid \
    --bind ${HOST}:${PORT} \
    --access-logfile ${LOGS_DIR}/gunicorn-BE-access.log \
    --access-logformat "%(h)s %(l)s %(u)s %(t)s \"%(r)s\" %(s)s %(b)s \"%(f)s\" \"%(a)s\" \"%({uniqueid}i)s\"" \
    --error-logfile ${LOGS_DIR}/gunicorn-BE-error.log \
    rungunicorn:app > ${LOGS_DIR}/gunicorn.out 2>&1

