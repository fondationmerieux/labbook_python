# -*- coding:utf-8 -*-
import logging
import mysql.connector

# from app.models.Constants import *
from app.models.DB import DB
from app.models.Logs import Logs
from app.models.Constants import Constants


class Patient:
    log = logging.getLogger('log_db')

    @staticmethod
    def getPatientSearch(text):
        cursor = DB.cursor()

        code = text
        text = '%' + text + '%'

        req = 'select id_data as id, nom, prenom, nom_jf, code, '\
              'date_format(ddn, %s) as ddn, code_patient '\
              'from sigl_03_data '\
              'where ((nom LIKE %s or nom_jf LIKE %s or prenom LIKE %s) AND IFNULL(anonyme, 5) = 5) or code = %s or code_patient LIKE %s'

        cursor.execute(req, (Constants.cst_isodate, text, text, text, code, text))

        return cursor.fetchall()

    @staticmethod
    def getPatient(id_pat):
        cursor = DB.cursor()

        req = 'select id_data, id_owner, anonyme, code, code_patient, nom, prenom, ddn, sexe, ethnie, adresse, cp, ville, tel, profession, '\
              'nom_jf, quartier, bp, ddn_approx, age, annee_naiss, semaine_naiss, mois_naiss, unite '\
              'from sigl_03_data '\
              'where id_data=%s'

        cursor.execute(req, (id_pat,))

        return cursor.fetchone()

    @staticmethod
    def insertPatient(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into sigl_03_data '
                           '(id_owner, anonyme, code, code_patient, nom, prenom, ddn, sexe, ethnie, adresse, cp, ville, '
                           'tel, profession, nom_jf, quartier, bp, ddn_approx, age, annee_naiss, semaine_naiss, mois_naiss, unite) '
                           'values '
                           '(%(id_owner)s, %(anonyme)s, %(code)s, %(code_patient)s, %(nom)s, %(prenom)s, %(ddn)s, %(sexe)s, %(ethnie)s, %(adresse)s, %(cp)s, %(ville)s, '
                           '%(tel)s, %(profession)s, %(nom_jf)s, %(quartier)s, %(bp)s, %(ddn_approx)s, %(age)s, %(annee_naiss)s, '
                           '%(semaine_naiss)s, %(mois_naiss)s, %(unite)s )', params)

            Patient.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Patient.log.error(Logs.fileline() + ' : ERROR SQL ' + str(e.errno))
            return 0

    @staticmethod
    def insertPatientGroup(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into sigl_03_data_group '
                           '(id_data, id_group) '
                           'values '
                           '(%(id_data)s, %(id_group)s )', params)

            Patient.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Patient.log.error(Logs.fileline() + ' : ERROR SQL ' + str(e.errno))
            return 0
