# -*- coding:utf-8 -*-
import logging
import mysql.connector

from app.models.DB import DB
from app.models.Logs import Logs
from app.models.Constants import Constants


class Various:
    log = logging.getLogger('log_db')

    @staticmethod
    def insertEvent(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into sigl_evtlog_data '
                           '(id_owner, evt_datetime, evt_type, evt_name, message) '
                           'values '
                           '(%(id_user)s, NOW(), %(type)s, %(name)s, %(message)s)', params)

            Various.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Various.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def getDicoById(id_data):
        cursor = DB.cursor()

        req = 'select id_data, id_owner, dico_name, label, short_label, position, code, dico_id, dico_value_id, archived '\
              'from sigl_dico_data '\
              'where id_data = %s '\
              'order by position'

        cursor.execute(req, (id_data,))

        return cursor.fetchone()

    @staticmethod
    def getDefaultValue(name):
        cursor = DB.cursor()

        req = 'select id_data, id_owner, identifiant, label, value '\
              'from sigl_06_data '\
              'where identifiant = %s'

        cursor.execute(req, (name,))

        return cursor.fetchone()

    @staticmethod
    def updateDefaultValue(name, value):
        try:
            cursor = DB.cursor()

            req = 'update sigl_06_data '\
                  'set value=%s '\
                  'where identifiant = %s'

            cursor.execute(req, (value, name,))

            Various.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Various.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getLastNumDos():
        cursor = DB.cursor()

        req = 'select num_dos_jour, num_dos_an, num_dos_mois '\
              'from sigl_02_data '\
              'order by id_data desc limit 1'

        cursor.execute(req)

        return cursor.fetchone()
