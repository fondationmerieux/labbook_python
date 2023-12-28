#! /home/www/amicare/venv/bin python
# -*- coding:utf-8 -*-
# from analyzer.sh
""" Request LAB28 to analyzers """

import sys
import getopt
import logging
import locale
import os
import fcntl
import signal
import hl7apy
import requests

from datetime import datetime

from app.models.Logs import Logs
from app.models.Constants import Constants
from app.models.Analyzer import Analyzer

# log = logging.getLogger('log_service')

locale.setlocale(locale.LC_TIME, 'C.UTF-8')


lock_file_path = "analyzer.lock"


def analyzer(test=False, verbose=False):
    ret_sc = True

    dt_start_script = datetime.now()

    date_now  = datetime.now()

    print("BEGIN script today=", date_now)
    print("TEST appel constantes Constants.cst_script_analyzer = ", Constants.cst_script_analyzer)

    # log.info(Logs.fileline() + ' : ANALYZER date_now = ' + str(date_now) + ' test : ' + str(test))

    print("cst_path_log = " + Constants.cst_path_log)

    # voir un auto unlock si le programme tombe
    # check if a lock file exist
    if check_lock_file(lock_file_path):
        # log.info(Logs.fileline() + ' : ANALYZER lock file exists')
        print("debug lock exists")
    else:
        # log.info(Logs.fileline() + ' : ANALYZER lock file doesnt exist we create this lock file')
        print("debug lock doesnt exist")
        create_lock_file(lock_file_path)

    try:
        print("Corps du script")
        # get list of pending LAB28 tasks
        l_tasks = Analyzer.listTaskLab28('PD')

        while l_tasks:
            for task in l_tasks:
                print('OML_O33 : ' + task['anl_OML_O33'])
                OML_O33 = task['anl_OML_O33']

                analyzer_setting = Analyzer.getAnalyzerDet(task['anl_ans'])

                if not analyzer_setting:
                    print('analyzer_setting causes an error, ans_ser = ' + str(task['anl_ans']))
                    return False

                id_analyzer = analyzer_setting['ans_id']

                url_lab28 = analyzer_setting['ans_lab28'] + str(id_analyzer)

                # send OML33 to Connect
                req = requests.post(url_lab28 , data=OML_O33, headers={"Content-Type": "application/hl7-v2"})

                print('req.status_code : ' + str(req.status_code))

                if req.status_code == 200:
                    # get ORL^34
                    ORL_O34 = req.text
                    print('ORL_O34 received : ', ORL_O34)

                    # update status
                    ret = Analyzer.updateLab28_ORL_O34(id_task=task['anl_ser'], stat='CO', ORL_O34=ORL_O34)

            # if l_tasks is empty we reload before exit this script
            l_tasks = Analyzer.listTaskLab28('PD')

    except Exception as e:
        print("Corps du script en erreur e : ", e)

    dt_stop_script = datetime.now()
    dt_time_script = dt_stop_script - dt_start_script

    # log.info(Logs.fileline() + ' : ANALYZER time to analyzer = ' + str(dt_time_script))

    remove_lock_file(lock_file_path)
    print ("END script")

    return ret_sc


def check_lock_file(file_path):
    try:
        # Ouvre le fichier en mode écriture et crée un verrou partagé (LOCK_SH | LOCK_NB)
        with open(file_path, 'w') as file:
            fcntl.flock(file, fcntl.LOCK_SH | fcntl.LOCK_NB)
            # Si le verrou est obtenu avec succès, le fichier n'est pas verrouillé par un autre processus
            print(f"Le fichier {file_path} n'est pas verrouillé.")
            fcntl.flock(file, fcntl.LOCK_UN)
            return False
    except IOError as e:
        # Si le fichier est verrouillé, une IOError sera levée
        print(f"Le fichier {file_path} est verrouillé par un autre processus.")
        return True

def create_lock_file(file_path):
    try:
        # Try to create lock file
        with open(file_path, 'w+') as file:
            fcntl.flock(file, fcntl.LOCK_EX)
        # log.info(Logs.fileline() + ' : ANALYZER create lock file')
            print("lock file created")
            # Définir le gestionnaire de signal pour le signal SIGTERM
            signal.signal(signal.SIGTERM, handle_signal)
    except IOError as e:
        # log.info(Logs.fileline() + ' : ERROR ANALYZER create lock file : ' + str(e))
        print("create_lock err : ", e)


def remove_lock_file(file_path):
    try:
        # delete lock file if exists
        os.remove(file_path)
        print("lock file removed")
        # log.info(Logs.fileline() + ' : ANALYZER remove lock file')
    except Exception as e:
        # log.info(Logs.fileline() + ' : ERROR ANALYZER remove lock file : ' + str(e))
        print("remove_lock err : ", e)


def handle_signal(signum, frame):
    # Ce gestionnaire de signal est appelé lorsqu'un signal SIGTERM est reçu
    print(f"Signal {signum} reçu. Libération du verrou.")
    remove_lock()
    sys.exit(1)


def use():
    print("Use : %s [-h|--help] [-v|--verbose]" % sys.argv[0])
    print(" -h : display help")
    print(" -t : test mode")
    print(" -v : verbose mode")


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "htv", ["help", "test", "verbose"])
    except getopt.GetoptError as err:
        print(str(err))
        use()
        sys.exit(2)

    test    = False
    verbose = False
    status  = 1

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            use()
            sys.exit(0)
        elif opt in ("-t", "--test"):
            test = True
        elif opt in ("-v", "--verbose"):
            verbose = True
        else:
            usage()
            sys.exit(2)

    if analyzer(test, verbose):
        status = 0

    sys.exit(status)


if __name__ == "__main__":
    main()

