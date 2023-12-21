#!/usr/bin/env sh
#
# Start gunicorn to serve the application in production mode
#

######################
# Run program        #
######################
APP_NAME=labbook_BE

HOME_APP=/home/apps/$APP_NAME
APP_DIR=${HOME_APP}/${APP_NAME}
VENV_DIR=${APP_DIR}/venv
LOGS_DIR=/home/apps/logs

source ${VENV_DIR}/bin/activate

LOG=${LOGS_DIR}/log_script_analyzer.log

export LOCAL_SETTINGS=${HOME_APP}/local_settings.py
export PYTHONPATH=${PYTHONPATH}:${APP_DIR}/

echo "`date` PYTHONPATH=$PYTHONPATH" >> $LOG

cd ${APP_DIR}

python script/analyzer.py $* >> $LOG 2>&1
