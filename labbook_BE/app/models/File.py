# -*- coding:utf-8 -*-
import logging
import mysql.connector

# from app.models.Constants import *
from app.models.DB import DB
from app.models.Logs import Logs


class File:
    log = logging.getLogger('log_db')

    @staticmethod
    def getFileDocList(type_ref, id_ref):
        cursor = DB.cursor()

        # RECORD
        if type_ref == 'REC':
            tablename = 'sigl_dos_valisedoc__file_data'
        # CALIBRATION CERTIFICAT
        elif type_ref == 'EQCC':
            tablename = 'sigl_equipement_certif_etalonnage__file_data'
        # MAINTENANCE CONTRACT
        elif type_ref == 'EQMC':
            tablename = 'sigl_equipement_contrat_maintenance__file_data'
        # BILL OF EQUIPMENT
        elif type_ref == 'EQBI':
            tablename = 'sigl_equipement_facture__file_data'
        # PREVENTIVE MAINTENANCE
        elif type_ref == 'EQPM':
            tablename = 'sigl_equipement_maintenance_preventive__file_data'
        # BREAKDOWN
        elif type_ref == 'EQBD':
            tablename = 'sigl_equipement_pannes__file_data'
        # PHOTO OF EQUIPMENT
        elif type_ref == 'EQPH':
            tablename = 'sigl_equipement_photo__file_data'
        # LABORATORY
        elif type_ref == 'LABO':
            tablename = 'sigl_laboratoire_organigramme__file_data'
        # MANUALS
        elif type_ref == 'MANU':
            tablename = 'sigl_manuels_document__file_data'
        # PROCEDURES
        elif type_ref == 'PROC':
            tablename = 'sigl_procedures_document__file_data'
        # MEETINGS
        elif type_ref == 'MEET':
            tablename = 'sigl_reunion_pj__file_data'
        # CV
        elif type_ref == 'USCV':
            tablename = 'sigl_user_cv__file_data'
        # DIPLOMA
        elif type_ref == 'USDI':
            tablename = 'sigl_user_diplomes__file_data'
        # EVALUATION
        elif type_ref == 'USEV':
            tablename = 'sigl_user_evaluation__file_data'
        # TRAININGS
        elif type_ref == 'USTR':
            tablename = 'sigl_user_formations__file_data'
        else:
            File.log.error(Logs.fileline() + ' : ERROR getFileDocList type_ref=' + str(type_ref))
            return []

        req = 'select file.id_data as id_data, file.original_name as name, file.path as dir, storage.path as storage '\
              'from ' + tablename + ' as valise, sigl_file_data as file, sigl_storage_data as storage '\
              'where file.id_data=valise.id_file and storage.id_data=file.id_storage and valise.id_ext=%s '\
              'order by id_data desc '

        cursor.execute(req, (id_ref,))

        return cursor.fetchall()

    @staticmethod
    def getFileData(id_file):
        cursor = DB.cursor()

        req = 'select id_data, id_owner, status, original_name, generated_name, id_storage, path '\
              'from sigl_file_data '\
              'where id_data=%s'

        cursor.execute(req, (id_file,))

        return cursor.fetchone()

    @staticmethod
    def insertFileData(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into sigl_file_data '
                           '(id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, status, date_creation, '
                           'original_name, generated_name, size, hash, ext, content_type, id_storage, path) '
                           'values '
                           '(%(id_owner)s, NOW(), NOW(), %(id_owner)s, 1, NOW(), %(original_name)s, %(generated_name)s, '
                           '%(size)s, %(hash)s, %(ext)s, %(content_type)s, %(id_storage)s, %(path)s)', params)

            File.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            File.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def insertFileDoc(**params):
        try:
            cursor = DB.cursor()

            # RECORD
            if params['type_ref'] == 'REC':
                tablename = 'sigl_dos_valisedoc__file_data'
            # CALIBRATION CERTIFICAT
            elif params['type_ref'] == 'EQCC':
                tablename = 'sigl_equipement_certif_etalonnage__file_data'
            # MAINTENANCE CONTRACT
            elif params['type_ref'] == 'EQMC':
                tablename = 'sigl_equipement_contrat_maintenance__file_data'
            # BILL OF EQUIPMENT
            elif params['type_ref'] == 'EQBI':
                tablename = 'sigl_equipement_facture__file_data'
            # PREVENTIVE MAINTENANCE
            elif params['type_ref'] == 'EQPM':
                tablename = 'sigl_equipement_maintenance_preventive__file_data'
            # BREAKDOWN
            elif params['type_ref'] == 'EQBD':
                tablename = 'sigl_equipement_pannes__file_data'
            # PHOTO OF EQUIPMENT
            elif params['type_ref'] == 'EQPH':
                tablename = 'sigl_equipement_photo__file_data'
            # LABORATORY
            elif params['type_ref'] == 'LABO':
                tablename = 'sigl_laboratoire_organigramme__file_data'
            # MANUALS
            elif params['type_ref'] == 'MANU':
                tablename = 'sigl_manuels_document__file_data'
            # PROCEDURES
            elif params['type_ref'] == 'PROC':
                tablename = 'sigl_procedures_document__file_data'
            # MEETINGS
            elif params['type_ref'] == 'MEET':
                tablename = 'sigl_reunion_pj__file_data'
            # CV
            elif params['type_ref'] == 'USCV':
                tablename = 'sigl_user_cv__file_data'
            # DIPLOMA
            elif params['type_ref'] == 'USDI':
                tablename = 'sigl_user_diplomes__file_data'
            # EVALUATION
            elif params['type_ref'] == 'USEV':
                tablename = 'sigl_user_evaluation__file_data'
            # TRAININGS
            elif params['type_ref'] == 'USTR':
                tablename = 'sigl_user_formations__file_data'
            else:
                return 0

            cursor.execute('insert into ' + tablename + ' '
                           '(id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, id_ext, id_file) '
                           'values '
                           '(%(id_owner)s, NOW(), NOW(), %(id_owner)s, %(id_ext)s, %(id_file)s)', params)

            File.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            File.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def deleteFileDoc(type_ref, id_file):
        try:
            cursor = DB.cursor()

            # RECORD
            if type_ref == 'REC':
                tablename = 'sigl_dos_valisedoc__file_data'
            # CALIBRATION CERTIFICAT
            elif type_ref == 'EQCC':
                tablename = 'sigl_equipement_certif_etalonnage__file_data'
            # MAINTENANCE CONTRACT
            elif type_ref == 'EQMC':
                tablename = 'sigl_equipement_contrat_maintenance__file_data'
            # BILL OF EQUIPMENT
            elif type_ref == 'EQBI':
                tablename = 'sigl_equipement_facture__file_data'
            # PREVENTIVE MAINTENANCE
            elif type_ref == 'EQPM':
                tablename = 'sigl_equipement_maintenance_preventive__file_data'
            # BREAKDOWN
            elif type_ref == 'EQBD':
                tablename = 'sigl_equipement_pannes__file_data'
            # PHOTO OF EQUIPMENT
            elif type_ref == 'EQPH':
                tablename = 'sigl_equipement_photo__file_data'
            # LABORATORY
            elif type_ref == 'LABO':
                tablename = 'sigl_laboratoire_organigramme__file_data'
            # MANUALS
            elif type_ref == 'MANU':
                tablename = 'sigl_manuels_document__file_data'
            # PROCEDURES
            elif type_ref == 'PROC':
                tablename = 'sigl_procedures_document__file_data'
            # MEETINGS
            elif type_ref == 'MEET':
                tablename = 'sigl_reunion_pj__file_data'
            # CV
            elif type_ref == 'USCV':
                tablename = 'sigl_user_cv__file_data'
            # DIPLOMA
            elif type_ref == 'USDI':
                tablename = 'sigl_user_diplomes__file_data'
            # EVALUATION
            elif type_ref == 'USEV':
                tablename = 'sigl_user_evaluation__file_data'
            # TRAININGS
            elif type_ref == 'USTR':
                tablename = 'sigl_user_formations__file_data'
            else:
                File.log.error(Logs.fileline() + ' : ERROR deleteFileDoc type_ref=' + str(type_ref))
                return False

            cursor.execute('delete from ' + tablename + ' '
                           'where id_file=%s', (id_file,))

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
    def getLastFileStorage():
        cursor = DB.cursor()

        req = 'select id_data, id_owner, path '\
              'from sigl_storage_data '\
              'order by id_data desc limit 1'

        cursor.execute(req)

        return cursor.fetchone()

    @staticmethod
    def insertStorage(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into sigl_storage_data '
                           '(id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, path) '
                           'values '
                           '(%(id_owner)s, NOW(), NOW(), %(id_owner)s, %(path)s)', params)

            File.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            File.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def getFileReport(id_rec):
        cursor = DB.cursor()

        req = 'select id_data, id_owner, id_dos, file, file_type, doc_type, date '\
              'from sigl_11_data '\
              'where id_dos=%s and doc_type=257 '\
              'order by id_data desc limit 1'

        cursor.execute(req, (id_rec,))

        return cursor.fetchone()

    @staticmethod
    def insertFileReport(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into sigl_11_data '
                           '(id_owner, id_dos, file, file_type, doc_type, date) '
                           'values '
                           '(%(id_owner)s, %(id_dos)s, UUID(), 259, %(doc_type)s, NOW())', params)

            File.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            File.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

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

                cursor.execute('delete from sigl_11_data '
                               'where id_data=%s', (filedata['id_data'],))

            File.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            File.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getFileNbManuals():
        cursor = DB.cursor()

        # Number of records
        req = 'select count(*) as nb_manuals '\
              'from sigl_manuels_data'

        cursor.execute(req)

        return cursor.fetchone()
