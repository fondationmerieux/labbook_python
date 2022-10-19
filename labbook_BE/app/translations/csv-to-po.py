# -*- coding:utf-8 -*-
import sys
import getopt
import logging
import locale

from datetime import datetime
from logging.handlers import WatchedFileHandler

locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')


def prep_log(logger_nom, log_fich, niveau=logging.INFO):
    logger = logging.getLogger(logger_nom)
    formatter = logging.Formatter('%(asctime)s : %(message)s')
    fileHandler = WatchedFileHandler(log_fich)
    fileHandler.setFormatter(formatter)

    logger.setLevel(niveau)
    logger.addHandler(fileHandler)


prep_log('log_script', r'/home/apps/labbook_BE/logs/log_script.log')

log = logging.getLogger('log_script')


def conv_csv_to_po(test=False, verbose=False):
    ret_sc = True

    dt_start_script = datetime.now()

    log.info('csv-to-po date_now = ' + str(dt_start_script))

    # Read csv file
    import os

    from csv import reader

    path_csv     = '/home/apps/labbook_BE/labbook_BE/tmp/'
    filename_csv = 'LBK-IHM_PT.csv'  # TODO ask by args
    path_po      = '/home/apps/labbook_BE/labbook_BE/tmp/'
    filename_po  = 'messages.po'
    filename_ref = 'messages_pybabel.py'

    with open(os.path.join(path_csv, filename_csv), 'r', encoding='utf-8') as csv_file:
        csv_reader = reader(csv_file, delimiter=';')
        l_rows = list(csv_reader)

    # Check csv file
    if not l_rows or len(l_rows) < 1:
        log.error('csv-to-po ERROR file empty')
        return False

    # Compose string to write
    po  = ''  # string to write for po file
    ref = ''  # string to write to get file to parse by pybabel
    for rows in l_rows:
        po += "msgid \"" + rows[0] + "\"\n"
        po += "msgstr \"" + rows[1] + "\"\n\n"

        ref += "_(\"" + rows[0] + "\")\n"

    # Write file with the pairs msgid /msgstr
    try:
        f = open(os.path.join(path_po, filename_po), 'w', encoding='utf-8')
        f.write(po)
        f.close()

        f2 = open(os.path.join(path_po, filename_ref), 'w', encoding='utf-8')
        f2.write(ref)
        f2.close()

    except Exception as err:
        log.error('csv-to-po ERROR write file, err=%s', err)
        return False

    # To do manually : ??? TODO WRITE

    dt_stop_script = datetime.now()
    dt_time_script = dt_stop_script - dt_start_script

    log.info('csv-to-po time = ' + str(dt_time_script))

    return ret_sc


def usage():
    print("Usage : %s [-h|--help] [-v|--verbose]" % sys.argv[0])
    print("   -h : display usage")
    print("   -t : test mode, doesn't write the file")
    print("   -v : verbose mode")


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "htv", ["help", "test", "verbose"])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
        sys.exit(2)

    test    = False
    verbose = False
    statut  = 1

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif opt in ("-t", "--test"):
            test = True
        elif opt in ("-v", "--verbose"):
            verbose = True
        else:
            usage()
            sys.exit(2)

    if conv_csv_to_po(test, verbose):
        statut = 0

    sys.exit(statut)


if __name__ == "__main__":
    main()
