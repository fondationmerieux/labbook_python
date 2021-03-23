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

    @staticmethod
    def getStickerSetting():
        cursor = DB.cursor()

        req = 'select sts_ser, sts_width, sts_height, sts_margin_top, sts_margin_bottom, '\
              'sts_margin_left, sts_margin_right '\
              'from sticker_setting '\
              'order by sts_ser desc limit 1'

        cursor.execute(req)

        return cursor.fetchone()

    @staticmethod
    def updateStickerSetting(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('update sticker_setting '
                           'set sts_width=%(sts_width)s, sts_height=%(sts_height)s, '
                           'sts_margin_top=%(sts_margin_top)s, sts_margin_bottom=%(sts_margin_bottom)s, '
                           'sts_margin_left=%(sts_margin_left)s, sts_margin_right=%(sts_margin_right)s '
                           'where sts_ser=%(sts_ser)s', params)

            Setting.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Setting.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getAgeInterval():
        cursor = DB.cursor()

        req = 'select ais_ser, ais_rank, ais_lower_bound, ais_upper_bound '\
              'from age_interval_setting '\
              'order by ais_rank asc'

        cursor.execute(req,)

        return cursor.fetchall()

    @staticmethod
    def getAgeIntervalById(ais_ser):
        cursor = DB.cursor()

        req = 'select ais_ser, ais_rank, ais_lower_bound, ais_upper_bound '\
              'from age_interval_setting '\
              'where ais_ser=%s'

        cursor.execute(req, (ais_ser,))

        return cursor.fetchall()

    @staticmethod
    def insertAgeInterval(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into age_interval_setting '
                           '(ais_rank, ais_lower_bound, ais_upper_bound) '
                           'values (%(ais_rank)s, %(ais_lower_bound)s, %(ais_upper_bound)s)', params)

            Setting.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Setting.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def updateAgeInterval(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('update age_interval_setting '
                           'set ais_rank=%(ais_rank)s, ais_lower_bound= %(ais_lower_bound)s, '
                           'ais_upper_bound=%(ais_upper_bound)s '
                           'where ais_ser=%(ais_ser)s', params)

            Setting.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Setting.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def deleteAgeInterval(ais_ser):
        try:
            cursor = DB.cursor()

            cursor.execute('delete from age_interval_setting '
                           'where ais_ser=%s', (ais_ser,))

            Setting.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Setting.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getBackupSetting():
        cursor = DB.cursor()

        req = 'select bks_ser, bks_start_time '\
              'from backup_setting '\
              'order by bks_ser desc limit 1'

        cursor.execute(req)

        return cursor.fetchone()

    @staticmethod
    def updateBackupSetting(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('update backup_setting '
                           'set bks_start_time=%(bks_start_time)s '
                           'where bks_ser=1', params)

            Setting.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Setting.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False
