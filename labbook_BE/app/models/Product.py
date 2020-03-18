# -*- coding:utf-8 -*-
import logging
import mysql.connector

# from app.models.Constants import *
from app.models.DB import DB
from app.models.Logs import Logs


class Product:
    log = logging.getLogger('log_db')

    """
    @staticmethod
    def getProductSearch(text, id_lab, id_group):
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
    def getProduct(id_ana):
        cursor = DB.cursor()

        req = 'select id_data, id_owner, code, nom, abbr, famille, paillasse, cote_unite, cote_valeur, '\
              'commentaire, produit_biologique, type_prel, type_analyse, actif '\
              'from sigl_05_data '\
              'where id_data=%s'

        cursor.execute(req, (id_ana,))

        return cursor.fetchone()

    @staticmethod
    def insertProduct(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into sigl_03_data '
                           '(id_owner, anonyme, code, code_analysis, nom, prenom, ddn, sexe, ethnie, adresse, cp, ville, '
                           'tel, profession, nom_jf, quartier, bp, ddn_approx, age, annee_naiss, semaine_naiss, mois_naiss, unite) '
                           'values '
                           '(%(id_owner)s, %(anonyme)s, %(code)s, %(code_analysis)s, %(nom)s, %(prenom)s, %(ddn)s, %(sexe)s, %(ethnie)s, %(adresse)s, %(cp)s, %(ville)s, '
                           '%(tel)s, %(profession)s, %(nom_jf)s, %(quartier)s, %(bp)s, %(ddn_approx)s, %(age)s, %(annee_naiss)s, '
                           '%(semaine_naiss)s, %(mois_naiss)s, %(unite)s )', params)

            Product.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Product.log.error(Logs.fileline() + ' : ERROR SQL ' + str(e.errno))
            return 0

    @staticmethod
    def insertProductGroup(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into sigl_03_data_group '\
                           '(id_data, id_group) '\
                           'values '\
                           '(%(id_data)s, %(id_group)s )', params)

            Product.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Product.log.error(Logs.fileline() + ' : ERROR SQL ' + str(e.errno))
            return 0


    @staticmethod
    def getProductType(id_data):
        cursor = DB.cursor()

        req = 'select id_data, id_owner, dico_name, label, short_label, position, code, dico_id, dico_value_id, archived '\
              'from sigl_dico_data '\
              'where id_data=%s'

        cursor.execute(req, (id_data,))

        return cursor.fetchone()"""

    @staticmethod
    def getProductReq(id_rec):
        cursor = DB.cursor()

        req = 'select prod.id_data as id_data, prod.id_owner as id_owner, prod.date_prel as date_prel, prod.type_prel as type_prel, '\
              'prod.quantite as quantite, prod.statut as statut, prod.id_dos as id_dos, prod.preleveur as preleveur, '\
              'prod.date_reception as date_reception, prod.heure_reception as heure_reception, prod.commentaire as commentaire, '\
              'prod.lieu_prel as lieu_prel, prod.lieu_prel_plus as lieu_prel_plus, prod.localisation as localisation, '\
              'dico_type.label as type_prod, dico_stat.label as stat_prod '\
              'from sigl_01_data as prod '\
              'LEFT JOIN sigl_dico_data AS dico_type ON dico_type.dico_name="type_prel" '\
              'LEFT JOIN sigl_dico_data AS dico_stat ON dico_stat.dico_name="prel_statut" '\
              'where dico_type.id_data=type_prel and dico_stat.id_data=statut and prod.id_dos=%s'

        cursor.execute(req, (id_rec,))

        return cursor.fetchall()

    @staticmethod
    def insertProductReq(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into sigl_01_data '
                           '(id_owner, date_prel, type_prel, quantite, statut, id_dos, preleveur, date_reception, '
                           'heure_reception, commentaire, lieu_prel, lieu_prel_plus, localisation) '
                           'values '
                           '(%(id_owner)s, %(date_prel)s, %(type_prel)s, %(quantite)s, %(statut)s, %(id_dos)s, %(preleveur)s, %(date_reception)s, '
                           '%(heure_reception)s, %(commentaire)s, %(lieu_prel)s, %(lieu_prel_plus)s, %(localisation)s)', params)

            Product.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Product.log.error(Logs.fileline() + ' : ERROR SQL ' + str(e.errno))
            return 0

    @staticmethod
    def insertProductReqGroup(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into sigl_01_data_group '
                           '(id_data, id_group) '
                           'values '
                           '(%(id_data)s, %(id_group)s )', params)

            Product.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Product.log.error(Logs.fileline() + ' : ERROR SQL ' + str(e.errno))
            return 0
