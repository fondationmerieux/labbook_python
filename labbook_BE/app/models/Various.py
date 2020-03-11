# -*- coding:utf-8 -*-
# import informixdb
import logging

from app.models.DB import DB


class Various:
    log = logging.getLogger('log_db')

    @staticmethod
    def getDicoList(dico_name):
        cursor = DB.cursor()

        req = 'select id_data, id_owner, dico_name, label, short_label, position, code, dico_id, dico_value_id, archived '\
              'from sigl_dico_data '\
              'where dico_name = %s'

        cursor.execute(req, (dico_name,))

        return cursor.fetchall()

    @staticmethod
    def getDefaultValue(name):
        cursor = DB.cursor()

        req = 'select id_data, id_owner, identifiant, label, value '\
              'from sigl_06_data '\
              'where identifiant = %s'

        cursor.execute(req, (name,))

        return cursor.fetchone()
