# import informixdb
import logging
import mysql.connector

from app.models.Constants import *
from app.models.BDD import BDD
from app.models.Logs import Logs


class Various:
    log = logging.getLogger('log_bdd')

    @staticmethod
    def getDicoList(dico_name):
        cursor = BDD.cursor()

        req = 'select id_data, id_owner, dico_name, label, short_label, position, code, dico_id, dico_value_id, archived '\
              'from sigl_dico_data '\
              'where dico_name = %s'

        cursor.execute(req, (dico_name,))

        return cursor.fetchall()

    @staticmethod
    def getDefaultValue(name):
        cursor = BDD.cursor()

        req = 'select id_data, id_owner, identifiant, label, value '\
              'from sigl_06_data '\
              'where identifiant = %s'

        cursor.execute(req, (name,))

        return cursor.fetchone()
