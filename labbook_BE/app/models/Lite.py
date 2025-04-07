# -*- coding:utf-8 -*-
import logging
import mysql.connector

# from app.models.Constants import *
from app.models.DB import DB
from app.models.Constants import Constants
from app.models.Logs import Logs


class Lite:
    log = logging.getLogger('log_db')

    @staticmethod
    def getLiteSetupList():
        cursor = DB.cursor()

        req = ('select lite_ser, lite_name, lite_login, lite_pwd, COUNT(u.litu_user) AS nb_user '
               'from lite_setting '
               'LEFT JOIN lite_users u on u.litu_lite = lite_ser '
               'GROUP BY lite_ser, lite_name, lite_login, lite_pwd '
               'order by lite_date desc')

        cursor.execute(req)

        return cursor.fetchall()

    @staticmethod
    def getLiteSetup(id_item):
        cursor = DB.cursor()

        req = ('select lite_ser, lite_name, lite_login, lite_pwd '
               'from lite_setting '
               'where lite_ser=%s')

        cursor.execute(req, (id_item,))

        return cursor.fetchone()

    @staticmethod
    def insertLiteSetup(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into lite_setting '
                           '(lite_date, lite_name, lite_login, lite_pwd) '
                           'values '
                           '(NOW(), %(name)s, %(login)s, %(pwd)s)', params)

            Lite.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Lite.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def updateLiteSetup(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('update lite_setting '
                           'set lite_name=%(name)s , lite_login=%(login)s, lite_pwd=%(pwd)s '
                           'where lite_ser=%(id_item)s', params)

            Lite.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Lite.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def deleteLiteSetup(id_item):
        try:
            cursor = DB.cursor()

            cursor.execute('delete from lite_setting '
                           'where lite_ser=%s', (id_item,))

            Lite.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Lite.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getLiteUsers(id_lite):
        try:
            cursor = DB.cursor()
    
            cursor.execute(
                'SELECT litu_user FROM lite_users WHERE litu_lite = %s',
                (id_lite,)
            )
    
            rows = cursor.fetchall()
            return [row['litu_user'] for row in rows]
    
        except mysql.connector.Error as e:
            Lite.log.error(Logs.fileline() + ' : ERROR getLiteUsers SQL = ' + str(e))
            return []

    @staticmethod
    def insertLiteUsers(id_lite, users):
        try:
            cursor = DB.cursor()

            # Delete existing user associations for this lite device
            cursor.execute('DELETE FROM lite_users WHERE litu_lite = %s', (id_lite,))
    
            # Insert new user associations
            for user_id in users:
                cursor.execute(
                    'INSERT INTO lite_users (litu_lite, litu_user, litu_date) VALUES (%s, %s, NOW())',
                    (id_lite, user_id)
                )
    
            Lite.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Lite.log.error(Logs.fileline() + ' : ERROR insertLiteUsers SQL = ' + str(e))
            return False
    
    @staticmethod
    def getLiteSetupByLogin(login):
        try:
            cursor = DB.cursor()
    
            cursor.execute('SELECT lite_ser, lite_name, lite_pwd FROM lite_setting WHERE lite_login = %s', (login,))
            return cursor.fetchone()
    
        except mysql.connector.Error as e:
            Lite.log.error(Logs.fileline() + ' : ERROR getLiteSetupByLogin SQL = ' + str(e))
            return None

    @staticmethod
    def getLiteUsersByIds(user_ids):
        if not user_ids:
            return []
    
        try:
            placeholders = ','.join(['%s'] * len(user_ids))
            req = f"""
                  SELECT id_data, firstname, lastname, username,
                  password, titre as `title`, email, locale,
                  initiale as `initial`, adresse as `address`, tel as `phone`, role_type
                  FROM sigl_user_data
                  WHERE id_data IN ({placeholders})
                  """
            cursor = DB.cursor()
            cursor.execute(req, tuple(user_ids))
            return cursor.fetchall()
        except mysql.connector.Error as e:
            Lite.log.error(Logs.fileline() + ' : ERROR getLiteUsersByIds SQL = ' + str(e))
            return []
    

    @staticmethod
    def getLiteAnalysis():
        try:
            req = """
                  SELECT id_data, code, nom as `name`, abbr, famille as `family`,
                  cote_unite as `rating_unit`, cote_valeur as `rating_value`, commentaire as `comment`,
                  produit_biologique as `bio_product`, type_prel as `sample_type`, type_analyse as `analysis_type`,
                  actif as `active`, ana_whonet, ana_ast, ana_loinc
                  FROM sigl_05_data
                  WHERE ana_lite = 'Y'
                  """
            cursor = DB.cursor()
            cursor.execute(req)
            return cursor.fetchall()
        except mysql.connector.Error as e:
            Lite.log.error(Logs.fileline() + ' : ERROR getLiteAnalysis SQL = ' + str(e))
            return []
    
    @staticmethod
    def getLiteLinksAnalysisVar(ana_ids):
        if not ana_ids:
            return []
    
        try:
            placeholders = ','.join(['%s'] * len(ana_ids))
            req = f"""
                  SELECT id_data, id_refanalyse as `analysis_id`, id_refvariable as `variable_id`, position,
                  num_var as `var_number`, obligatoire as `required`, var_whonet, var_qrcode
                  FROM sigl_05_07_data
                  WHERE id_refanalyse IN ({placeholders})
                  """
            cursor = DB.cursor()
            cursor.execute(req, tuple(ana_ids))
            return cursor.fetchall()
        except mysql.connector.Error as e:
            Lite.log.error(Logs.fileline() + ' : ERROR getLiteLinksAnalysisVar SQL = ' + str(e))
            return []

    @staticmethod
    def getLiteVAnalysisVarByIds(variable_ids):
        if not variable_ids:
            return []
    
        try:
            placeholders = ','.join(['%s'] * len(variable_ids))
            req = f"""
                  SELECT id_data, libelle as `label`, description, unite as `unit`, normal_min, normal_max,
                  commentaire as `comment`, type_resultat as `result_type`, unite2 as `unit2`, formule_unite2 as `formula_unit2`,
                  formule as `formula`, accuracy, precision2 as `accuracy2`, code_var as `var_code`,
                  var_highlight, var_show_minmax
                  FROM sigl_07_data
                  WHERE id_data IN ({placeholders})
                  """
            cursor = DB.cursor()
            cursor.execute(req, tuple(variable_ids))
            return cursor.fetchall()
        except mysql.connector.Error as e:
            Lite.log.error(Logs.fileline() + ' : ERROR getLiteVAnalysisVarByIds SQL = ' + str(e))
            return []
    
    @staticmethod
    def getLiteAnalysisByIds(ids):
        if not ids:
            return []
    
        try:
            placeholders = ','.join(['%s'] * len(ids))
            req = f"""
                  SELECT id_data, code, nom as `name`, abbr, famille as `family`,
                  cote_unite as `rating_unit`, cote_valeur as `rating_value`, commentaire as `comment`,
                  produit_biologique as `bio_product`, type_prel as `sample_type`, type_analyse as `analysis_type`,
                  actif as `active`, ana_whonet, ana_ast, ana_loinc
                  FROM sigl_05_data
                  WHERE id_data IN ({placeholders})
                  """
            cursor = DB.cursor()
            cursor.execute(req, tuple(ids))
            return cursor.fetchall()
        except mysql.connector.Error as e:
            Lite.log.error(Logs.fileline() + ' : ERROR getLiteAnalysisByIds SQL = ' + str(e))
            return []

    @staticmethod
    def getLiteDictionary():
        try:
            req = f"""
                  SELECT id_data, dico_name, label, short_label,
                  code, dico_descr, dict_formatting
                  FROM sigl_dico_data
                  """
            cursor = DB.cursor()
            cursor.execute(req)
            return cursor.fetchall()
        except mysql.connector.Error as e:
            Lite.log.error(Logs.fileline() + ' : ERROR getLiteDictionary SQL = ' + str(e))
            return []

    @staticmethod
    def getLitePatients():
        try:
            req = """
                  SELECT
                  id_data AS id_data, anonyme AS pat_ano, code AS pat_code_lab, code_patient AS pat_code,
                  nom AS pat_name, pat_midname AS pat_midname, nom_jf AS pat_maiden, prenom AS pat_firstname,
                  sexe AS pat_sex, ddn AS pat_birth, ddn_approx AS pat_birth_approx, age AS pat_age,
                  unite AS pat_age_unit, pat_nation AS pat_nationality, pat_resident AS pat_resident,
                  pat_blood_group AS pat_blood_group, pat_blood_rhesus AS pat_blood_rhesus,
                  adresse AS pat_address, tel AS pat_phone1, pat_phone2 AS pat_phone2,
                  profession AS pat_profession, cp AS pat_zipcode, ville AS pat_city, bp AS pat_pbox,
                  quartier AS pat_district, pat_email
                  FROM sigl_03_data
                  """
            with DB.cursor() as cursor:
                cursor.execute(req)
                return cursor.fetchall()
        except mysql.connector.Error as e:
            Lite.log.error(Logs.fileline() + ' : ERROR getLitePatients SQL = ' + str(e))
            return []

    @staticmethod
    def getLitePreferences():
        try:
            req = """
                  SELECT id_data, identifiant as `key`, label, value
                  FROM sigl_06_data
                  """
            cursor = DB.cursor()
            cursor.execute(req)
            return cursor.fetchall()
        except mysql.connector.Error as e:
            Lite.log.error(Logs.fileline() + ' : ERROR getLitePreferences SQL = ' + str(e))
            return []

    @staticmethod
    def getLiteNationalities():
        try:
            req = "SELECT nat_ser, nat_name, nat_code FROM nationality order by nat_name"
            with DB.cursor() as cursor:
                cursor.execute(req)
                return cursor.fetchall()
        except Exception as e:
            Lite.log.error(Logs.fileline() + f" : ERROR getLiteNationalities() : {str(e)}")
            return []
    
