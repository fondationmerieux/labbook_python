# -*- coding:utf-8 -*-
import logging

# from app.models.Constants import *
from app.models.DB import DB


class Result:
    log = logging.getLogger('log_db')

    @staticmethod
    def getResultList(args):
        cursor = DB.cursor()

        filter_cond = ''

        limit = 'LIMIT 200'
        # filter conditions
        date_beg = args['date_beg']
        date_end = args['date_end']

        # NULL (5 sometimes) or 4 in base
        if args['emer_ana'] and args['emer_ana'] == 4:
            filter_cond += ' and ana.urgent=4 and ref_var.type_resultat not in ("229", "265") '

        # TODO condition type_ana  ???
        # TODO condition valid_res ???

        # ref_ana, id_ana, id_dos, nom, famille, id_res, ref_var.*
        req = 'select ana.ref_analyse as ref_ana, ana.id_data as id_ana, dos.id_data as id_dos, '\
              'ref.nom as nom, fam.label as famille, res.id_data as id_res, ref_var.* '\
              'from sigl_04_data as ana '\
              'inner join sigl_02_data as dos on dos.id_data = ana.id_dos '\
              'inner join sigl_05_data as ref on ana.ref_analyse = ref.id_data '\
              'left join sigl_dico_data as fam on fam.id_data = ref.famille '\
              'inner join sigl_09_data as res on ana.id_data = res.id_analyse '\
              'inner join sigl_07_data as ref_var on ref_var.id_data = res.ref_variable '\
              'where (cast(substring(num_dos_jour, 1, 8) as UNSIGNED) >= %s) and '\
              '(cast(substring(num_dos_jour, 1, 8) as UNSIGNED) <= %s) ' + filter_cond +\
              'order by nom asc, id_dos asc ' + limit

        cursor.execute(req, (date_beg, date_end,))

        return cursor.fetchall()

    """
    @staticmethod
    def getResult(id_ana):
        cursor = DB.cursor()

        req = 'select id_data, id_owner, code, nom, abbr, famille, paillasse, cote_unite, cote_valeur, '\
              'commentaire, produit_biologique, type_prel, type_analyse, actif '\
              'from sigl_05_data '\
              'where id_data=%s'

        cursor.execute(req, (id_ana,))

        return cursor.fetchone()


    @staticmethod
    def insertResult(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into sigl_03_data '
                           '(id_owner, anonyme, code, code_record, nom, prenom, ddn, sexe, ethnie, adresse, cp, ville, '
                           'tel, profession, nom_jf, quartier, bp, ddn_approx, age, annee_naiss, semaine_naiss, mois_naiss, unite) '
                           'values '
                           '(%(id_owner)s, %(anonyme)s, %(code)s, %(code_record)s, %(nom)s, %(prenom)s, %(ddn)s, %(sexe)s, %(ethnie)s, %(adresse)s, %(cp)s, %(ville)s, '
                           '%(tel)s, %(profession)s, %(nom_jf)s, %(quartier)s, %(bp)s, %(ddn_approx)s, %(age)s, %(annee_naiss)s, '
                           '%(semaine_naiss)s, %(mois_naiss)s, %(unite)s )', params)

            Result.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Result.log.error(Logs.fileline() + ' : ERROR SQL ' + str(e.errno))
            return 0

    @staticmethod
    def insertResultGroup(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into sigl_03_data_group '\
                           '(id_data, id_group) '\
                           'values '\
                           '(%(id_data)s, %(id_group)s )', params)

            Result.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Result.log.error(Logs.fileline() + ' : ERROR SQL ' + str(e.errno))
            return 0


    @staticmethod
    def getProductType(id_data):
        cursor = DB.cursor()

        req = 'select id_data, id_owner, dico_name, label, short_label, position, code, dico_id, dico_value_id, archived '\
              'from sigl_dico_data '\
              'where id_data=%s'

        cursor.execute(req, (id_data,))

        return cursor.fetchone()"""
