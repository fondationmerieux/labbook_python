#!/usr/bin/env sh
#
# Start gunicorn to serve the application in production mode
#
# PhB, 08/10/14
# PHM, 01/10/15 -> adaptation aux serveurs d'applications Web (amicare, borne, ...)
# AlC, 18/11/19 -> adaptation pour le projet labbook

# PHM le 19/11/19 : Passage Apache->gunicorn via port 8081
HOST="localhost"
PORT="8081"

export INFORMIXDIR=/home/informix
export INFORMIXSERVER=sigl_tcp
export ONCONFIG=onconfig

#############
# Fonctions #
#############
#
# Affiche l'usage et sort
#
usage()
{
echo
echo "Lancement Gunicorn Labbook FRONT END"
echo
echo "Usage :"
echo "  $0 -h"
echo "  $0 -r"
echo
echo "Options:"
echo "  -h                 Cette aide"
echo "  -r                 Ajoute l'attribut reload au lancement"
echo
exit 2
}

######################
# Début du programme #
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
    echo "option $option inconnue"
    usage
    ;;
    esac
done

# Application amicare
APP_NAME=labbook_FE

HOME_APP=/home/www/apps/labbook/current/$APP_NAME
VENV_DIR=${HOME_APP}/venv
LOGS_DIR=${HOME_APP}/logs
GUNICORN_DIR=${HOME_APP}/gunicorn
GUNICORN_TIMEOUT=60

source ${VENV_DIR}/bin/activate

# create Gunicorn directory if necessary
mkdir -p ${GUNICORN_DIR}

cd ${HOME_APP}

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
    --error-logfile ${LOGS_DIR}/gunicorn-error.log \
    rungunicorn:app > ${LOGS_DIR}/gunicorn.out 2>&1
