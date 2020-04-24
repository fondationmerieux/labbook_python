# -*- coding:utf-8 -*-
import logging
import mysql.connector

# from app.models.Constants import *
from app.models.DB import DB
from app.models.Logs import Logs


class File:
    log = logging.getLogger('log_db')

    @staticmethod
    def getFileDoc(id_file):
        cursor = DB.cursor()

        req = 'select id_data, id_owner, status, original_name, generated_name, id_storage, path '\
              'from sigl_file_data '\
              'where id_data=%s'

        cursor.execute(req, (id_file,))

        return cursor.fetchone()

    @staticmethod
    def deleteFileDoc(id_file):
        try:
            cursor = DB.cursor()

            cursor.execute('select id_data '
                           'from sigl_dos_valisedoc__file_data '
                           'where id_file=%s', (id_file,))

            ret = cursor.fetchone()

            if not ret and ret['id_data'] > 0:
                return False

            cursor.execute('insert into sigl_dos_valisedoc__file_deleted '
                           '(id_data, id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, id_ext, id_file) '
                           'select id_data, id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, id_ext, id_file '
                           'from sigl_dos_valisedoc__file_data '
                           'where id_data=%s', (ret['id_data'],))

            cursor.execute('delete from sigl_dos_valisedoc__file_data_group_mode '
                           'where id_data_group=%s', (ret['id_data'],))

            cursor.execute('delete from sigl_dos_valisedoc__file_data_group '
                           'where id_data=%s', (ret['id_data'],))

            cursor.execute('delete from sigl_dos_valisedoc__file_data '
                           'where id_data=%s', (ret['id_data'],))

            File.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            File.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def deleteFileDocByRecord(id_rec):
        try:
            cursor = DB.cursor()

            cursor.execute('select id_data '
                           'from sigl_dos_valisedoc__file_data '
                           'where id_ext=%s', (id_rec,))

            l_file = cursor.fetchall()

            for filedata in l_file:
                cursor.execute('insert into sigl_dos_valisedoc__file_deleted '
                               '(id_data, id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, id_ext, id_file) '
                               'select id_data, id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, id_ext, id_file '
                               'from sigl_dos_valisedoc__file_data '
                               'where id_data=%s', (filedata['id_data'],))

                cursor.execute('delete from sigl_dos_valisedoc__file_data_group_mode '
                               'where id_data_group=%s', (filedata['id_data'],))

                cursor.execute('delete from sigl_dos_valisedoc__file_data_group '
                               'where id_data=%s', (filedata['id_data'],))

                cursor.execute('delete from sigl_dos_valisedoc__file_data '
                               'where id_data=%s', (filedata['id_data'],))

            File.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            File.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getFileStorage(id_storage):
        cursor = DB.cursor()

        req = 'select id_data, id_owner, path '\
              'from sigl_storage_data '\
              'where id_data=%s'

        cursor.execute(req, (id_storage,))

        return cursor.fetchone()

    @staticmethod
    def getFileReport(id_rec):
        cursor = DB.cursor()

        req = 'select id_data, id_owner, id_dos, file, file_type, doc_type, date '\
              'from sigl_11_data '\
              'where id_dos=%s and doc_type=257'

        cursor.execute(req, (id_rec,))

        return cursor.fetchone()

    @staticmethod
    def deleteFileReportByRecord(id_rec):
        try:
            cursor = DB.cursor()

            cursor.execute('select id_data '
                           'from sigl_11_data '
                           'where id_dos=%s', (id_rec,))

            l_file = cursor.fetchall()

            for filedata in l_file:
                cursor.execute('insert into sigl_11_deleted '
                               '(id_data, id_owner, id_dos, file, file_type, doc_type, date) '
                               'select id_data, id_owner, id_dos, file, file_type, doc_type, date '
                               'from sigl_11_data '
                               'where id_data=%s', (filedata['id_data'],))

                cursor.execute('delete from sigl_11_data_group_mode '
                               'where id_data_group=%s', (filedata['id_data'],))

                cursor.execute('delete from sigl_11_data_group '
                               'where id_data=%s', (filedata['id_data'],))

                cursor.execute('delete from sigl_11_data '
                               'where id_data=%s', (filedata['id_data'],))

            File.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            File.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False
