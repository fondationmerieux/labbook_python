#!/usr/bin/env sh
#
# Start gunicorn to serve the application in production mode
#
# PhB, 08/10/14
# PHM, 01/10/15 -> adaptation aux serveurs d'applications Web (amicare, borne, ...)
# AlC, 18/11/19 -> adaptation pour le projet labbook

# PHM le 19/11/19 : Passage Apache->gunicorn via port 8082
HOST="localhost"
PORT="8082"

export INFORMIXDIR=/home/informix
export INFORMIXSERVER=informix
export ONCONFIG=onconfig

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

# Application name
APP_NAME=labbook_BE

HOME_APP=/home/apps/$APP_NAME
APP_DIR=${HOME_APP}/${APP_NAME}
VENV_DIR=${APP_DIR}/venv
LOGS_DIR=${HOME_APP}/logs
LOGS_PERM=/storage/log
GUNICORN_DIR=${HOME_APP}/gunicorn
GUNICORN_TIMEOUT=0  # Because restore and backup scripts that run synchronously

source ${VENV_DIR}/bin/activate

# create Gunicorn directory if necessary
mkdir -p ${GUNICORN_DIR}
mkdir -p ${LOGS_DIR}

# Operating environment
export LOCAL_SETTINGS=${HOME_APP}/local_settings.py

# if local_settings file doesnt exist we create one
# from local_settings.py.sample in app directory
test -f $LOCAL_SETTINGS || {
    echo "$LOCAL_SETTINGS not found, local_settings.py file create"

    cp ${APP_DIR}/local_settings.py.sample $LOCAL_SETTINGS || exit 1
}

cd ${APP_DIR} || exit 1

# run alembic upgrade
alembic upgrade head >> ${LOGS_PERM}/alembic.out

# Gunicorn is installed in the virtual environment
# When started by supervisord, exec is necessary for the signals to reach gunicorn.
# Another approach with catched signals is described here :
# http://serverfault.com/questions/425132/controlling-tomcat-with-supervisor
exec gunicorn \
    $opt_reload \
    --timeout ${GUNICORN_TIMEOUT} \
    --pid ${GUNICORN_DIR}/gunicorn.pid \
    --bind ${HOST}:${PORT} \
    --access-logfile ${LOGS_DIR}/gunicorn-access.log \
    --access-logformat "%(h)s %(l)s %(u)s %(t)s \"%(r)s\" %(s)s %(b)s \"%(f)s\" \"%(a)s\" \"%({uniqueid}i)s\"" \
    --error-logfile ${LOGS_DIR}/gunicorn-error.log \
    rungunicorn:app > ${LOGS_DIR}/gunicorn.out 2>&1

