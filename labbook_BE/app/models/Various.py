# -*- coding:utf-8 -*-
import gettext
import logging

import mysql.connector
from flask import request

from app.models.Constants import Constants
from app.models.DB import DB
from app.models.Logs import Logs

# Names exported when this module is imported with "*" (see app/__init__.py).
# Without __all__, "import *" also brings in this module's own imports
# (Constants, datetime, logging...) and they leak into the caller.
__all__ = [
    'get_lang_pdf_default',
    'get_lang_db_default',
    'Various',
]


# --- Language helpers ---
def get_lang_pdf_default():
    # lang_pdf
    """
    Return the language of the reports, the default_language preference.
    """
    db_val = Various.getDefaultValue('default_language')
    Various.log.info(Logs.fileline() + ' : lang_pdf in database = ' + db_val['value'])
    return db_val['value']


def get_lang_db_default():
    # lang_db
    """
    Return the language of the database texts, the db_language preference.
    """
    db_val = Various.getDefaultValue('db_language')
    Various.log.info(Logs.fileline() + ' : lang_db in database = ' + db_val['value'])
    return db_val['value']


class Various:
    log = logging.getLogger('log_db')

    @staticmethod
    def useLangPDF():
        """
        Make _() translate into the language of the reports.
        gettext.install puts _ in the builtins, so it changes the language of the whole process,
        every request included, until the next call.
        """
        lang_code = get_lang_pdf_default()

        langPDF = gettext.translation('messages', Constants.cst_path_lang, [lang_code], fallback=False)
        langPDF.install()

    @staticmethod
    def useLangDB():
        """
        Make _() translate into the language of the database texts.
        gettext.install puts _ in the builtins, so it changes the language of the whole process,
        every request included, until the next call.
        """
        lang_code = get_lang_db_default()

        langDB = gettext.translation('messages', Constants.cst_path_lang, [lang_code], fallback=False)
        langDB.install()

    @staticmethod
    def insertEvent(**params):
        """
        Record an event in event_log (logins, imports...).

        Returns:
            int: new id, 0 on SQL error.
        """
        try:
            cursor = DB.cursor()

            cursor.execute('insert into event_log '
                           '(evl_user, evl_date, evl_type, evl_name, evl_message) '
                           'values '
                           '(%(id_user)s, NOW(), %(type)s, %(name)s, %(message)s)', params)

            Various.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Various.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def getDicoById(id_data):
        """
        Read one dictionary value of sigl_dico_data.
        """
        cursor = DB.cursor()

        req = ('select id_data, id_owner, dico_name, label, short_label, position, code, dict_formatting '
               'from sigl_dico_data '
               'where id_data = %s '
               'order by position')

        cursor.execute(req, (id_data,))

        return cursor.fetchone()

    @staticmethod
    def getDefaultValue(name):
        """
        Read one preference of sigl_06_data by its key (identifiant).
        """
        cursor = DB.cursor()

        req = ('select id_data, id_owner, identifiant, label, value '
               'from sigl_06_data '
               'where identifiant = %s')

        cursor.execute(req, (name,))

        return cursor.fetchone()

    @staticmethod
    def updateDefaultValue(name, value):
        """
        Set the value of one preference of sigl_06_data.

        Returns:
            bool: True on success, False on SQL error.
        """
        try:
            cursor = DB.cursor()

            req = ('update sigl_06_data '
                   'set value=%s '
                   'where identifiant = %s')

            cursor.execute(req, (value, name,))

            Various.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Various.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getLastNumDos():
        """
        Read the day, month and year numbers of the last record created, to compute the next ones.
        """
        cursor = DB.cursor()

        req = ('select num_dos_jour, num_dos_an, num_dos_mois '
               'from sigl_02_data '
               'order by id_data desc limit 1')

        cursor.execute(req)

        return cursor.fetchone()

    @staticmethod
    def getLastInitVersion():
        """
        Read the last row of init_version, which says whether the translations must be reloaded.
        """
        cursor = DB.cursor()

        req = ('select * '
               'from init_version '
               'order by ini_ser desc limit 1')

        cursor.execute(req)

        return cursor.fetchone()

    @staticmethod
    def updateInitVersion(ini_ser, stat):
        """
        Set the status of an init_version row, 'N' once the translations are reloaded.

        Returns:
            bool: True on success, False on SQL error.
        """
        try:
            cursor = DB.cursor()

            req = ('update init_version '
                   'set ini_stat = %s '
                   'where ini_ser = %s')

            cursor.execute(req, (stat, ini_ser,))

        except mysql.connector.Error as e:
            Various.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

        return True

    @staticmethod
    def updateTranslationsTable(lang):
        """
        Fill the translations table for one language with the translated names of analyses, variables
        and dictionary values, so searches work outside fr_FR.

        Returns:
            bool: True on success, False on SQL error.
        """
        try:
            # use lang en_GB for DB
            langDB = gettext.translation('messages', Constants.cst_path_lang, lang.split())
            langDB.install()

            cursor = DB.cursor()

            params = {'lang': '', 'ref': 0, 'type': '', 'text': ''}

            # --- Fill translations table with analysis name
            req = ('select nom as name, id_data as ref from sigl_05_data order by code asc')

            cursor.execute(req)

            l_ana = cursor.fetchall()

            for ana in l_ana:
                text = ana['name'].strip()

                # check if this ana name doesnt exist in translations table
                req = ('select count(*) as nb from translations '
                       'where tra_text=%s and tra_lang=%s and tra_type="ana_name"')

                cursor.execute(req, (_(text), lang,))
                res = cursor.fetchone()

                if res['nb'] == 0:
                    params['lang'] = lang
                    params['ref']  = ana['ref']
                    params['type'] = 'ana_name'
                    params['text'] = _(text)

                    # insert into translations
                    req = ('insert into translations (tra_date, tra_lang, tra_ref, tra_type, tra_text) '
                           'values (NOW(), %(lang)s, %(ref)s, %(type)s, %(text)s)')

                    cursor.execute(req, params)

            # --- Fill translations table with var name
            req = ('select libelle as name, id_data as ref from sigl_07_data')

            cursor.execute(req)

            l_var = cursor.fetchall()

            for var in l_var:
                text = var['name'].strip()

                # check if this var name doesnt exist in translations table
                req = ('select count(*) as nb from translations '
                       'where tra_text=%s and tra_lang=%s and tra_type="var_name"')

                cursor.execute(req, (_(text), lang,))
                res = cursor.fetchone()

                if res['nb'] == 0:
                    params['lang'] = lang
                    params['ref']  = var['ref']
                    params['type'] = 'var_name'
                    params['text'] = _(text)

                    # insert into translations
                    req = ('insert into translations (tra_date, tra_lang, tra_ref, tra_type, tra_text) '
                           'values (NOW(), %(lang)s, %(ref)s, %(type)s, %(text)s)')

                    cursor.execute(req, params)

            # --- Fill translations table with dictionnary name
            req = ('select distinct dico_name as name, id_data as ref from sigl_dico_data group by name')

            cursor.execute(req)

            l_dict = cursor.fetchall()

            for dict in l_dict:
                text = dict['name'].strip()

                # check if this var name doesnt exist in translations table
                req = ('select count(*) as nb from translations '
                       'where tra_text=%s and tra_lang=%s and tra_type="dict_name"')

                cursor.execute(req, (_(text), lang,))
                res = cursor.fetchone()

                if res['nb'] == 0:
                    params['lang'] = lang
                    params['ref']  = dict['ref']  # first id_data where dico_name is found
                    params['type'] = 'dict_name'
                    params['text'] = _(text)

                    # insert into translations
                    req = ('insert into translations (tra_date, tra_lang, tra_ref, tra_type, tra_text) '
                           'values (NOW(), %(lang)s, %(ref)s, %(type)s, %(text)s)')

                    cursor.execute(req, params)

            # --- Fill translations table with dictionnary label
            req = ('select label, id_data as ref from sigl_dico_data')

            cursor.execute(req)

            l_dict = cursor.fetchall()

            for dict in l_dict:
                text = dict['label'].strip()

                # check if this var name doesnt exist in translations table
                req = ('select count(*) as nb from translations '
                       'where tra_text=%s and tra_lang=%s and tra_type="dict_label"')

                cursor.execute(req, (_(text), lang,))
                res = cursor.fetchone()

                if res['nb'] == 0:
                    params['lang'] = lang
                    params['ref']  = dict['ref']
                    params['type'] = 'dict_label'
                    params['text'] = _(text)

                    # insert into translations
                    req = ('insert into translations (tra_date, tra_lang, tra_ref, tra_type, tra_text) '
                           'values (NOW(), %(lang)s, %(ref)s, %(type)s, %(text)s)')

                    cursor.execute(req, params)

            Various.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Various.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getNationalityList():
        """
        Read every nationality.
        """
        cursor = DB.cursor()

        req = ('select nat_ser, nat_name, nat_code '
               'from nationality '
               'order by nat_code')

        cursor.execute(req)

        return cursor.fetchall()

    @staticmethod
    def getNationalityById(id):
        """
        Read one nationality.
        """
        cursor = DB.cursor()

        req = ('select nat_ser, nat_name, nat_code '
               'from nationality '
               'where nat_ser=%s')

        cursor.execute(req, (id,))

        return cursor.fetchone()

    @staticmethod
    def get_client_ip():
        """Return real client IP using proxy headers if available."""
        xff = request.headers.get('X-Forwarded-For')
        if xff:
            return xff.split(',')[0].strip()
        ip = request.headers.get('X-Real-IP')
        if ip:
            return ip
        return request.remote_addr
