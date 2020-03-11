# -*- coding:utf-8 -*-
import logging

# from app.models.Constants import *
from app.models.DB import DB


class Analysis:
    log = logging.getLogger('log_db')

    @staticmethod
    def getAnalysisSearch(text, id_lab, id_group):
        cursor = DB.cursor()

        code = text
        text = '%' + text + '%'

        req = 'SELECT ref_ana.id_data AS id, CONCAT(ref_ana.code, " ", COALESCE(ref_ana.abbr, "")) AS code, ref_ana.nom AS name,  COALESCE(dico.label, "") AS label '\
              'FROM sigl_05_data AS ref_ana '\
              'LEFT JOIN sigl_dico_data AS dico ON dico.id_data=ref_ana.famille '\
              'WHERE (ref_ana.actif = 4 AND (ref_ana.code = %s or ref_ana.nom like %s or ref_ana.abbr like %s)) '\
              'AND (ref_ana.id_data is NULL or (exists(select 1 from sigl_05_data_group where sigl_05_data_group.id_group in (%s) '\
              'and sigl_05_data_group.id_data = ref_ana.id_data)) '\
              'OR ( exists( select 1 from sigl_05_data_group inner join sigl_05_data_group_mode on sigl_05_data_group.id_data_group=sigl_05_data_group_mode.id_data_group '\
              'where sigl_05_data_group.id_group = %s and sigl_05_data_group.id_data = ref_ana.id_data and sigl_05_data_group_mode.mode & 292 '\
              'AND (sigl_05_data_group_mode.date_valid IS NULL OR CURRENT_DATE <= sigl_05_data_group_mode.date_valid)))) '\
              'ORDER BY nom ASC LIMIT 7000'

        cursor.execute(req, (code, text, text, id_lab, id_group,))

        return cursor.fetchall()

    @staticmethod
    def getAnalysis(id_ana):
        cursor = DB.cursor()

        req = 'select id_data, id_owner, code, nom, abbr, famille, paillasse, cote_unite, cote_valeur, '\
              'commentaire, produit_biologique, type_prel, type_analyse, actif '\
              'from sigl_05_data '\
              'where id_data=%s'

        cursor.execute(req, (id_ana,))

        return cursor.fetchone()

    """
    @staticmethod
    def insertAnalysis(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into sigl_03_data '
                           '(id_owner, anonyme, code, code_analysis, nom, prenom, ddn, sexe, ethnie, adresse, cp, ville, '
                           'tel, profession, nom_jf, quartier, bp, ddn_approx, age, annee_naiss, semaine_naiss, mois_naiss, unite) '
                           'values '
                           '(%(id_owner)s, %(anonyme)s, %(code)s, %(code_analysis)s, %(nom)s, %(prenom)s, %(ddn)s, %(sexe)s, %(ethnie)s, %(adresse)s, %(cp)s, %(ville)s, '
                           '%(tel)s, %(profession)s, %(nom_jf)s, %(quartier)s, %(bp)s, %(ddn_approx)s, %(age)s, %(annee_naiss)s, '
                           '%(semaine_naiss)s, %(mois_naiss)s, %(unite)s )', params)

            Analysis.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Analysis.log.error(Logs.fileline() + ' : ERROR SQL ' + str(e.errno))
            return 0

    @staticmethod
    def insertAnalysisGroup(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into sigl_03_data_group '\
                           '(id_data, id_group) '\
                           'values '\
                           '(%(id_data)s, %(id_group)s )', params)

            Analysis.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Analysis.log.error(Logs.fileline() + ' : ERROR SQL ' + str(e.errno))
            return 0"""

    @staticmethod
    def getProductType(id_data):
        cursor = DB.cursor()

        req = 'select id_data, id_owner, dico_name, label, short_label, position, code, dico_id, dico_value_id, archived '\
              'from sigl_dico_data '\
              'where id_data=%s'

        cursor.execute(req, (id_data,))

        return cursor.fetchone()
