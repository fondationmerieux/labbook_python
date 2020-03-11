# -*- coding:utf-8 -*-
import logging

# from app.models.Constants import *
from app.models.DB import DB


class Doctor:
    log = logging.getLogger('log_db')

    @staticmethod
    def getDoctorSearch(text, id_lab, id_group):
        cursor = DB.cursor()

        text = '%' + text + '%'

        req = 'SELECT TRIM(CONCAT(TRIM(COALESCE(prat.code, ""))," - ",'\
              'TRIM(COALESCE(prat.nom, ""))," ",TRIM(COALESCE(prat.prenom, ""))," - ",'\
              'TRIM(COALESCE(dico_prat.label, "")))) AS field_value,'\
              'prat.id_data AS id_doctor '\
              'FROM sigl_08_data AS prat '\
              'LEFT JOIN `sigl_dico_data` AS `dico_prat` ON dico_prat.id_data=prat.specialite '\
              'WHERE (prat.nom LIKE %s OR prat.prenom LIKE %s) AND (prat.id_data is NULL or '\
              '(exists(select 1 from sigl_08_data_group where sigl_08_data_group.id_group in (%s) and sigl_08_data_group.id_data = prat.id_data)) '\
              'OR ( exists( select 1 from sigl_08_data_group inner join sigl_08_data_group_mode '\
              'on sigl_08_data_group.id_data_group=sigl_08_data_group_mode.id_data_group where sigl_08_data_group.id_group = %s '\
              'and sigl_08_data_group.id_data = prat.id_data and sigl_08_data_group_mode.mode & 292 '\
              'AND (sigl_08_data_group_mode.date_valid IS NULL OR CURRENT_DATE <= sigl_08_data_group_mode.date_valid)))) LIMIT 7000'

        cursor.execute(req, (text, text, id_lab, id_group))

        return cursor.fetchall()

"""
    @staticmethod
    def getDoctor(id_pat):
        cursor = DB.cursor()

        req = 'select id_data, id_owner, anonyme, code, code_doctor, nom, prenom, ddn, sexe, ethnie, adresse, cp, ville, tel, profession, '\
              'nom_jf, quartier, bp, ddn_approx, age, annee_naiss, semaine_naiss, mois_naiss, unite '\
              'from sigl_03_data '\
              'where id_data=%s'

        cursor.execute(req, (id_pat,))

        return cursor.fetchone()

    @staticmethod
    def insertDoctor(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into sigl_03_data '
                           '(id_owner, anonyme, code, code_doctor, nom, prenom, ddn, sexe, ethnie, adresse, cp, ville, '
                           'tel, profession, nom_jf, quartier, bp, ddn_approx, age, annee_naiss, semaine_naiss, mois_naiss, unite) '
                           'values '
                           '(%(id_owner)s, %(anonyme)s, %(code)s, %(code_doctor)s, %(nom)s, %(prenom)s, %(ddn)s, %(sexe)s, %(ethnie)s, %(adresse)s, %(cp)s, %(ville)s, '
                           '%(tel)s, %(profession)s, %(nom_jf)s, %(quartier)s, %(bp)s, %(ddn_approx)s, %(age)s, %(annee_naiss)s, '
                           '%(semaine_naiss)s, %(mois_naiss)s, %(unite)s )', params)

            Doctor.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Doctor.log.error(Logs.fileline() + ' : ERROR SQL ' + str(e.errno))
            return 0

    @staticmethod
    def insertDoctorGroup(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into sigl_03_data_group '\
                           '(id_data, id_group) '\
                           'values '\
                           '(%(id_data)s, %(id_group)s )', params)

            Doctor.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Doctor.log.error(Logs.fileline() + ' : ERROR SQL ' + str(e.errno))
            return 0"""
