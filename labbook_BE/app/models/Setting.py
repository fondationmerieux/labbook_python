# -*- coding:utf-8 -*-
import logging
import mysql.connector

# from app.models.Constants import *
from app.models.DB import DB
from app.models.Logs import Logs
from app.models.Constants import Constants


class Setting:
    log = logging.getLogger('log_db')

    @staticmethod
    def getPrefList():
        cursor = DB.cursor()

        req = 'select id_data, id_owner, identifiant, label, value '\
              'from sigl_06_data '\
              'order by id_data'

        cursor.execute(req,)

        return cursor.fetchall()

    @staticmethod
    def updatePref(id_owner, key, value):
        try:
            cursor = DB.cursor()

            cursor.execute('update sigl_06_data '
                           'set id_owner=%s, value=%s '
                           'where identifiant=%s', (id_owner, value, key))

            Setting.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Setting.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getRecNumSetting():
        cursor = DB.cursor()

        req = 'select id_data, id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, periode, format '\
              'from sigl_param_num_dos_data '\
              'order by id_data desc limit 1'

        cursor.execute(req)

        return cursor.fetchone()

    @staticmethod
    def updateRecNumSetting(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('update sigl_param_num_dos_data '
                           'set sys_last_mod_user=%(id_owner)s, sys_last_mod_date=NOW(), '
                           'periode=%(period)s, format=%(format)s '
                           'where id_data=1', params)

            Setting.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Setting.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getReportSetting():
        cursor = DB.cursor()

        req = 'select id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, entete, commentaire '\
              'from sigl_param_cr_data '\
              'order by id_data desc limit 1'

        cursor.execute(req)

        return cursor.fetchone()

    @staticmethod
    def updateReportSetting(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('update sigl_param_cr_data '
                           'set sys_last_mod_user=%(id_owner)s, sys_last_mod_date=NOW(), '
                           'entete=%(header)s, commentaire=%(comment)s '
                           'where id_data=1', params)

            Setting.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Setting.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False
