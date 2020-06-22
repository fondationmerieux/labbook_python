# -*- coding:utf-8 -*-
import logging
import mysql.connector

from datetime import datetime, date
from app.models.Constants import *
from app.models.DB import DB
from app.models.Logs import Logs


class Result:
    log = logging.getLogger('log_db')

    @staticmethod
    def getResultList(args):
        cursor = DB.cursor()

        filter_cond = ''

        limit = 'LIMIT 500'
        # filter conditions
        date_beg = args['date_beg']
        date_end = args['date_end']

        # NULL (5 sometimes) or 4 in base
        if args['emer_ana'] and args['emer_ana'] == 4:
            filter_cond += ' and urgent=4 and ref_var.type_resultat not in ("229", "265") '

        # Analysis family
        if args['type_ana'] and args['type_ana'] > 0:
            filter_cond += ' and fam.id_data=' + str(args['type_ana']) + ' '

        # Without valid result
        if args['valid_res'] and args['valid_res'] > 0:
            filter_cond += ' and res.id_data not in (select id_resultat from sigl_10_data where type_validation > 250 and res.id_data=id_resultat) '

        # ref_ana, id_ana, id_dos, nom, famille, id_res, valeur, ref_var.*, num_dos_mois, num_dos_an,
        # date_dos, date_prescr, stat, urgent, id_owner
        req = 'select ana.ref_analyse as ref_ana, ana.id_data as id_ana, dos.id_data as id_dos, '\
              'ref.nom as nom, fam.label as famille, res.id_data as id_res, res.valeur as valeur, ref_var.*, '\
              'dos.num_dos_mois as num_dos_mois, dos.num_dos_an as num_dos_an, dos.date_dos as date_dos, '\
              'dos.date_prescription as date_prescr, dos.statut as stat, ana.urgent as urgent, '\
              'ana.id_owner as id_owner, var_pos.position as position, var_pos.num_var as num_var '\
              'from sigl_04_data as ana '\
              'inner join sigl_02_data as dos on dos.id_data = ana.id_dos '\
              'inner join sigl_05_data as ref on ana.ref_analyse = ref.id_data '\
              'left join sigl_dico_data as fam on fam.id_data = ref.famille '\
              'inner join sigl_09_data as res on ana.id_data = res.id_analyse '\
              'inner join sigl_07_data as ref_var on ref_var.id_data = res.ref_variable '\
              'inner join sigl_05_07_data as var_pos on ref_var.id_data = var_pos.id_refvariable '\
              'and ref.id_data = var_pos.id_refanalyse '\
              'where substring(num_dos_jour, 1, 8) >= %s and '\
              'substring(num_dos_jour, 1, 8) <= %s ' + filter_cond +\
              'order by nom asc, id_dos asc, id_ana asc, position asc ' + limit

        cursor.execute(req, (date_beg, date_end,))

        return cursor.fetchall()

    @staticmethod
    def getResultRecord(id_rec):
        cursor = DB.cursor()

        req = 'select ana.ref_analyse as ref_ana, ana.id_data as id_ana, dos.id_data as id_dos, '\
              'ref.nom as nom, fam.label as famille, res.id_data as id_res, res.valeur as valeur, ref_var.*, '\
              'dos.num_dos_mois as num_dos_mois, dos.num_dos_an as num_dos_an, dos.date_dos as date_dos, '\
              'dos.date_prescription as date_prescr, dos.statut as stat, ana.urgent as urgent, '\
              'ana.id_owner as id_owner, dos.id_patient as id_pat, '\
              'var_pos.position as position, var_pos.num_var as num_var '\
              'from sigl_04_data as ana '\
              'inner join sigl_02_data as dos on dos.id_data = ana.id_dos '\
              'inner join sigl_05_data as ref on ana.ref_analyse = ref.id_data '\
              'left join sigl_dico_data as fam on fam.id_data = ref.famille '\
              'inner join sigl_09_data as res on ana.id_data = res.id_analyse '\
              'inner join sigl_07_data as ref_var on ref_var.id_data = res.ref_variable '\
              'inner join sigl_05_07_data as var_pos on ref_var.id_data = var_pos.id_refvariable '\
              'and ref.id_data = var_pos.id_refanalyse '\
              'where id_dos=%s '\
              'order by nom asc, id_ana asc, position asc'

        cursor.execute(req, (id_rec,))

        return cursor.fetchall()

    @staticmethod
    def getPreviousResult(id_pat, ref_ana, ref_var, id_res):
        cursor = DB.cursor()

        date_today = datetime.strftime(date.today(), Constants.cst_isodate) + ' 00:00' 

        req = 'select res.valeur as valeur, vld.date_validation as date_valid '\
              'from sigl_09_data as res '\
              'inner join sigl_05_07_data as ref on ref.id_refvariable = res.ref_variable '\
              'inner join sigl_04_data as dem on dem.ref_analyse = ref.id_refanalyse and dem.id_data = res.id_analyse '\
              'inner join sigl_02_data as dos on dos.id_data = dem.id_dos '\
              'inner join sigl_10_data as vld on vld.id_resultat = res.id_data '\
              'where dos.id_patient=%s and dem.ref_analyse=%s and res.ref_variable=%s '\
              'and vld.type_validation=252 and vld.motif_annulation is NULL and res.id_data != %s '\
              'and vld.date_validation < %s '\
              'order by vld.date_validation desc limit 1'

        cursor.execute(req, (id_pat, ref_ana, ref_var, id_res, date_today))

        return cursor.fetchone()

    @staticmethod
    def insertResult(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into sigl_09_data '
                           '(id_owner, id_analyse, ref_variable, obligatoire) '
                           'values '
                           '(%(id_owner)s, %(id_analyse)s, %(ref_variable)s, %(obligatoire)s)', params)

            Result.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Result.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def insertResultGroup(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into sigl_09_data_group '
                           '(id_data, id_group) '
                           'values '
                           '(%(id_data)s, %(id_group)s )', params)

            Result.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Result.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def deleteResult(id_res):
        try:
            cursor = DB.cursor()

            cursor.execute('select id_data '
                           'from sigl_09_data '
                           'where id_data=%s', (id_res,))

            l_result = cursor.fetchall()

            for result in l_result:
                cursor.execute('insert into sigl_09_deleted '
                               '(id_data, id_owner, id_analyse, ref_variable, valeur, obligatoire) '
                               'select id_data, id_owner, id_analyse, ref_variable, valeur, obligatoire '
                               'from sigl_09_data '
                               'where id_data=%s', (result['id_data'],))

                cursor.execute('delete from sigl_09_data_group_mode '
                               'where id_data_group=%s', (result['id_data'],))

                cursor.execute('delete from sigl_09_data_group '
                               'where id_data=%s', (result['id_data'],))

                cursor.execute('delete from sigl_09_data '
                               'where id_data=%s', (result['id_data'],))

            Result.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Result.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getResultValidation(id_res):
        cursor = DB.cursor()

        req = 'select v.id_data as id_data, v.id_owner as id_owner, v.id_resultat as id_resultat, '\
              'v.date_validation as date_validation, v.utilisateur as utilisateur, v.valeur as valeur, '\
              'v.type_validation as type_validation, v.commentaire as commentaire, '\
              'v.motif_annulation as motif_annulation, dico.label as label_motif '\
              'from sigl_10_data as v '\
              'left join sigl_dico_data as dico on dico.id_data=motif_annulation '\
              'where id_resultat=%s '\
              'order by id_data desc limit 1'

        cursor.execute(req, (id_res,))

        return cursor.fetchone()

    @staticmethod
    def getResultListValidation(id_res):
        cursor = DB.cursor()

        req = 'select v.id_data as id_data, v.id_owner as id_owner, v.id_resultat as id_resultat, '\
              'v.date_validation as date_validation, v.utilisateur as utilisateur, v.valeur as valeur, '\
              'v.type_validation as type_validation, v.commentaire as commentaire, v.motif_annulation as motif_annulation '\
              'from sigl_10_data as v '\
              'where id_resultat=%s '\
              'order by id_data'

        cursor.execute(req, (id_res,))

        return cursor.fetchall()

    @staticmethod
    def getLastTypeValidation(id_ana):
        cursor = DB.cursor()

        req = 'select valid.type_validation as type_validation '\
              'from sigl_10_data as valid, sigl_09_data as res '\
              'where valid.id_resultat=res.id_data and res.id_analyse=%s '\
              'order by valid.id_data desc limit 1'

        cursor.execute(req, (id_ana,))

        return cursor.fetchone()

    @staticmethod
    def insertValidation(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into sigl_10_data '
                           '(id_owner, id_resultat, date_validation, utilisateur, valeur, type_validation, commentaire, motif_annulation) '
                           'values '
                           '(%(id_owner)s, %(id_resultat)s, %(date_validation)s, %(utilisateur)s, %(valeur)s, %(type_validation)s, %(commentaire)s, %(motif_annulation)s )', params)

            Result.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Result.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def insertValidationGroup(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into sigl_10_data_group '
                           '(id_data, id_group) '
                           'values '
                           '(%(id_data)s, %(id_group)s )', params)

            Result.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Result.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def deleteValidationByResult(id_res):
        try:
            cursor = DB.cursor()

            cursor.execute('select id_data '
                           'from sigl_10_data '
                           'where id_resultat=%s', (id_res,))

            l_valid = cursor.fetchall()

            for valid in l_valid:
                cursor.execute('insert into sigl_10_deleted '
                               '(id_data, id_owner, id_resultat, date_validation, utilisateur, valeur, type_validation, commentaire, motif_annulation ) '
                               'select id_data, id_owner, id_resultat, date_validation, utilisateur, valeur, type_validation, commentaire, motif_annulation '
                               'from sigl_10_data '
                               'where id_data=%s', (valid['id_data'],))

                cursor.execute('delete from sigl_10_data_group_mode '
                               'where id_data_group=%s', (valid['id_data'],))

                cursor.execute('delete from sigl_10_data_group '
                               'where id_data=%s', (valid['id_data'],))

                cursor.execute('delete from sigl_10_data '
                               'where id_data=%s', (valid['id_data'],))

            Result.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Result.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def updateResult(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('update sigl_09_data set '
                           'id_owner=%(id_owner)s, '
                           'valeur=%(valeur)s '
                           'where id_data=%(id_data)s', params)

            Result.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Result.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False
