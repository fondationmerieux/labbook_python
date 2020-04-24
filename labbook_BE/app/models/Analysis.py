# -*- coding:utf-8 -*-
import logging
import mysql.connector

# from app.models.Constants import *
from app.models.DB import DB
from app.models.Logs import Logs


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

    @staticmethod
    def getProductType(id_data):
        cursor = DB.cursor()

        req = 'select id_data, id_owner, dico_name, label, short_label, position, code, dico_id, dico_value_id, archived '\
              'from sigl_dico_data '\
              'where id_data=%s'

        cursor.execute(req, (id_data,))

        return cursor.fetchone()

    @staticmethod
    def getAnalysisReq(id_rec, type_ana):
        cursor = DB.cursor()

        if type_ana == 'O':
            cond = ' and (cote_unite is NULL or cote_unite != "PB")'
        elif type_ana == 'N':
            cond = ' and cote_unite="PB"'
        else:
            cond = ''

        req = 'select req_ana.id_data as id_data, req_ana.id_owner as id_owner, req_ana.id_dos as id_dos, '\
              'req_ana.ref_analyse as ref_analyse, req_ana.prix as prix, req_ana.paye as paye, req_ana.urgent as urgent, '\
              'req_ana.demande as demande, ref_ana.code as code, ref_ana.nom as nom, ref_ana.cote_unite as cote_unite, ref_ana.cote_valeur as cote_valeur '\
              'from sigl_04_data as req_ana '\
              'LEFT JOIN sigl_05_data as ref_ana on ref_ana.id_data=ref_analyse '\
              'where id_dos=%s' + cond

        cursor.execute(req, (id_rec,))

        return cursor.fetchall()

    @staticmethod
    def insertAnalysisReq(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into sigl_04_data '
                           '(id_owner, id_dos, ref_analyse, prix, paye, urgent, demande) '
                           'values '
                           '(%(id_owner)s, %(id_dos)s, %(ref_analyse)s, %(prix)s, %(paye)s, %(urgent)s, %(demande)s)', params)

            Analysis.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Analysis.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def insertAnalysisReqGroup(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into sigl_04_data_group '
                           '(id_data, id_group) '
                           'values '
                           '(%(id_data)s, %(id_group)s )', params)

            Analysis.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Analysis.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def getRefVariable(id_ana):
        cursor = DB.cursor()

        req = 'select id_data, id_owner, id_refanalyse, id_refvariable, position, num_var, obligatoire '\
              'from sigl_05_07_data '\
              'where id_refanalyse=%s'

        cursor.execute(req, (id_ana,))

        return cursor.fetchall()

    @staticmethod
    def getLastAnalysisReqByRefAna(ref_ana):
        cursor = DB.cursor()

        req = 'select id_data, id_owner, id_dos, ref_analyse, prix, paye, urgent, demande '\
              'from sigl_04_data '\
              'where ref_analyse=%s '\
              'order by id_data desc limit 1'

        cursor.execute(req, (ref_ana,))

        return cursor.fetchone()

    @staticmethod
    def deleteAnalysisByRecord(id_rec):
        try:
            cursor = DB.cursor()

            cursor.execute('select id_data '
                           'from sigl_04_data '
                           'where id_dos=%s', (id_rec,))

            l_ana = cursor.fetchall()

            for ana in l_ana:
                cursor.execute('insert into sigl_04_deleted '
                               '(id_data, id_owner, id_dos, ref_analyse, prix, paye, urgent, demande ) '
                               'select id_data, id_owner, id_dos, ref_analyse, prix, paye, urgent, demande '
                               'from sigl_04_data '
                               'where id_data=%s', (ana['id_data'],))

                cursor.execute('delete from sigl_04_data_group_mode '
                               'where id_data_group=%s', (ana['id_data'],))

                cursor.execute('delete from sigl_04_data_group '
                               'where id_data=%s', (ana['id_data'],))

                cursor.execute('delete from sigl_04_data '
                               'where id_data=%s', (ana['id_data'],))

            Analysis.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Analysis.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False
