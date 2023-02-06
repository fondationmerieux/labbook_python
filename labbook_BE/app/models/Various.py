# -*- coding:utf-8 -*-
import logging
import mysql.connector
import gettext

from flask import session

from app.models.Constants import *
from app.models.DB import DB
from app.models.Logs import Logs


class Various:
    log = logging.getLogger('log_db')

    @staticmethod
    def initSessionLang():
        if not session or 'lang_pdf' not in session or 'lang_db' not in session:
            pdf_val = Various.getDefaultValue('default_language')
            session['lang_pdf'] = pdf_val['value']

            db_val = Various.getDefaultValue('db_language')
            session['lang_db'] = db_val['value']
            session.modified = True
            Various.log.info(Logs.fileline() + ' : lang_pdf in database = ' + session['lang_pdf'])
            Various.log.info(Logs.fileline() + ' : lang_db in database  = ' + session['lang_db'])

    @staticmethod
    def useLangPDF():
        Various.initSessionLang()

        langPDF = gettext.translation('messages', Constants.cst_path_lang, session['lang_pdf'].split())
        langPDF.install()

    @staticmethod
    def useLangDB():
        Various.initSessionLang()

        langDB = gettext.translation('messages', Constants.cst_path_lang, session['lang_db'].split())
        langDB.install()

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

        req = ('select id_data, id_owner, dico_name, label, short_label, position, code, dict_formatting '
               'from sigl_dico_data '
               'where id_data = %s '
               'order by position')

        cursor.execute(req, (id_data,))

        return cursor.fetchone()

    @staticmethod
    def getDefaultValue(name):
        cursor = DB.cursor()

        req = ('select id_data, id_owner, identifiant, label, value '
               'from sigl_06_data '
               'where identifiant = %s')

        cursor.execute(req, (name,))

        return cursor.fetchone()

    @staticmethod
    def updateDefaultValue(name, value):
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
        cursor = DB.cursor()

        req = ('select num_dos_jour, num_dos_an, num_dos_mois '
               'from sigl_02_data '
               'order by id_data desc limit 1')

        cursor.execute(req)

        return cursor.fetchone()

    @staticmethod
    def getLastInitVersion():
        cursor = DB.cursor()

        req = ('select * '
               'from init_version '
               'order by ini_ser desc limit 1')

        cursor.execute(req)

        return cursor.fetchone()

    @staticmethod
    def updateInitVersion(ini_ser, stat):
        try:
            cursor = DB.cursor()

            req = ('update init_version '
                   'set ini_stat = %s '
                   'where ini_ser = %s')

            cursor.execute(req, (stat, ini_ser,))

        except mysql.connector.Error as e:
            Various.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def updateTranslationsTable(lang):
        try:
            # init lang
            Various.initSessionLang()

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
        cursor = DB.cursor()

        req = ('select nat_ser, nat_name, nat_code '
               'from nationality '
               'order by nat_code')

        cursor.execute(req)

        return cursor.fetchall()

    @staticmethod
    def getNationalityById(id):
        cursor = DB.cursor()

        req = ('select nat_ser, nat_name, nat_code '
               'from nationality '
               'where nat_ser=%s')

        cursor.execute(req, (id,))

        return cursor.fetchone()
