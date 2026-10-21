# -*- coding:utf-8 -*-
import logging

import mysql.connector

from app.models.DB import DB
from app.models.Logs import Logs


class External:
    log = logging.getLogger('log_db')

    @staticmethod
    def getIdByRef(system, object_type, ref):
        """Return the LabBook id linked to an external reference, 0 when unknown."""
        cursor = DB.cursor()

        cursor.execute('select exr_ref_int '
                       'from external_ref '
                       'where exr_type_ext=%(system)s and exr_type_int=%(object)s and exr_ref_ext=%(ref)s',
                       {'system': str(system), 'object': str(object_type), 'ref': str(ref)})

        row = cursor.fetchone()

        if not row:
            return 0

        return row['exr_ref_int']

    @staticmethod
    def getRefById(system, object_type, id_int):
        """Return the external reference of a LabBook object, empty when unknown."""
        cursor = DB.cursor()

        cursor.execute('select exr_ref_ext '
                       'from external_ref '
                       'where exr_type_ext=%(system)s and exr_type_int=%(object)s and exr_ref_int=%(id)s',
                       {'system': str(system), 'object': str(object_type), 'id': int(id_int)})

        row = cursor.fetchone()

        if not row:
            return ''

        return row['exr_ref_ext']

    @staticmethod
    def insertRef(**params):
        """Link an external reference to a LabBook object, 0 when it already exists."""
        try:
            cursor = DB.cursor()

            cursor.execute('insert into external_ref '
                           '(exr_date, exr_by_user, exr_type_ext, exr_ref_ext, exr_type_int, exr_ref_int) '
                           'values '
                           '(NOW(), %(user)s, %(system)s, %(ref)s, %(object)s, %(id)s)', params)

            External.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            External.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0
