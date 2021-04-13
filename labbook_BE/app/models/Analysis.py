# -*- coding:utf-8 -*-
import logging
import mysql.connector

# from app.models.Constants import *
from app.models.DB import DB
from app.models.Logs import Logs


class Analysis:
    log = logging.getLogger('log_db')

    @staticmethod
    def getAnalysisSearch(text, type="A"):
        cursor = DB.cursor()

        l_words = text.split(' ')

        cond = 'ref.actif = 4'

        if type == "A":
            cond += ' and ref.cote_unite != "PB"'
        elif type == "P":
            cond += ' and ref.cote_unite = "PB"'

        for word in l_words:
            cond = (cond +
                    ' and (ref.code like "' + word + '%" or '
                    'ref.nom like "%' + word + '%" or '
                    'ref.abbr like "%' + word + '%") ')

        req = 'select ref.id_data as id, CONCAT(ref.code, " ", COALESCE(ref.abbr, "")) as code, '\
              'ref.nom as name,  COALESCE(dict.label, "") as label '\
              'from sigl_05_data as ref '\
              'left join sigl_dico_data as dict on dict.id_data=ref.famille '\
              'where ' + cond + ' order by nom asc limit 1000'

        cursor.execute(req)

        return cursor.fetchall()

    @staticmethod
    def getAnalysisVarSearch(text):
        cursor = DB.cursor()

        l_words = text.split(' ')

        cond = 'libelle is not NULL '

        for word in l_words:
            cond = (cond + ' and (libelle like "%' + word + '%") ')

        req = ('select libelle as field_value, id_data '
               'from sigl_07_data '
               'where ' + cond + ' order by field_value asc limit 1000')

        cursor.execute(req)

        return cursor.fetchall()

    @staticmethod
    def getAnalysis(id_ana):
        cursor = DB.cursor()

        req = ('select ana.id_data, ana.id_owner, ana.code, ana.nom, ana.abbr, ana.famille, ana.cote_unite, '
               'ana.cote_valeur, ana.commentaire, ana.produit_biologique, ana.type_prel, ana.type_analyse, ana.actif, '
               'CONCAT(samp.code, " ", COALESCE(samp.nom, "")) as product_label '
               'from sigl_05_data as ana '
               'left join sigl_05_data as samp on samp.id_data=ana.produit_biologique '
               'where ana.id_data=%s')

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

        # Only analysis
        if type_ana == 'O':
            cond = ' and (cote_unite is NULL or cote_unite != "PB")'
        # Only samples
        elif type_ana == 'N':
            cond = ' and cote_unite="PB"'
        # Everything
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
    def getListVariable(id_ana):
        cursor = DB.cursor()

        req = ('select var.id_data, libelle as label, description as descr, unite as unit, normal_min as min, '
               'normal_max as max, commentaire as comment, type_resultat as type_res, unite2 as unit2, '
               'formule_unite2 as formula2, formule as formula, var.accuracy as accu, precision2 as accu2, '
               'link.position as pos, link.num_var as num_var, link.obligatoire as oblig, link.id_data as id_link, '
               'd1.label as unit_label '
               'from sigl_07_data as var '
               'inner join sigl_05_07_data as link on link.id_refvariable=var.id_data '
               'left join sigl_dico_data as d1 on d1.id_data=var.unite '
               'where link.id_refanalyse=%s '
               'order by link.position, link.id_data')

        cursor.execute(req, (id_ana,))

        return cursor.fetchall()

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

                cursor.execute('delete from sigl_04_data '
                               'where id_data=%s', (ana['id_data'],))

            Analysis.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Analysis.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getAnalyzesList(args):
        cursor = DB.cursor()

        filter_cond = ''

        if not args:
            limit = 'LIMIT 2000'

            filter_cond += ' ana.actif=4 '  # remove deleted analyzes by default
        else:
            limit = 'LIMIT 2000'

            filter_cond += ' '  # remove deleted analyzes by default
            # filter conditions
            if args['status'] and args['status'] > 0:
                filter_cond += ' ana.actif=' + str(args['status']) + ' '
            else:
                filter_cond += ' ana.actif=4 '  # keep only activated analyzes by default

            if args['name']:
                filter_cond += ' and (ana.nom LIKE "%' + args['name'] + '%" or ana.code LIKE "%' + args['name'] + '%" or ana.abbr LIKE "%' + args['name'] + '%") '

            if args['type_ana'] and args['type_ana'] > 0:
                filter_cond += ' and ana.famille=' + str(args['type_ana']) + ' '

            if args['type_prod'] and args['type_prod'] > 0:
                filter_cond += ' and ana.type_prel=' + str(args['type_prod']) + ' '

        req = 'select ana.id_data, ana.code, ana.nom as name, ana.abbr, ana.actif as stat, '\
              'dico.label as type_ana, samp.nom as product, ana.produit_biologique as id_prod '\
              'from sigl_05_data as ana '\
              'left join sigl_dico_data as dico on dico.id_data=ana.famille '\
              'left join sigl_05_data as samp on samp.id_data=ana.produit_biologique '\
              'where ' + filter_cond +\
              'group by ana.code order by ana.code asc ' + limit

        cursor.execute(req)

        return cursor.fetchall()

    @staticmethod
    def getAnalyzesHistoList(args):
        cursor = DB.cursor()

        filter_cond = ' '

        limit    = 'LIMIT 500'
        date_beg = args['date_beg']
        date_end = args['date_end']

        if 'limit' in args and args['limit'] > 0:
            limit = 'LIMIT ' + str(args['limit'])

        # filter conditions
        if 'name' in args and args['name']:
            filter_cond += ' and (ref.nom LIKE "%' + args['name'] + '%" or ref.abbr LIKE "%' + args['name'] + '%") '

        if 'code' in args and args['code']:
            filter_cond += ' and (ref.code LIKE "%' + args['code'] + '%" or ref.abbr LIKE "%' + args['code'] + '%") '

        if 'type_ana' in args and args['type_ana'] > 0:
            filter_cond += ' and ref.famille=' + str(args['type_ana']) + ' '

        req = ('select ref.id_data, ref.code, dict.label as fam_name, ref.nom as name '
               'from sigl_02_data as rec '
               'inner join sigl_04_data as ana on ana.id_dos = rec.id_data '
               'inner join sigl_05_data as ref on ref.id_data = ana.ref_analyse and ref.cote_unite != "PB" '
               'left join sigl_dico_data as dict on dict.id_data=ref.famille '
               'where (rec.date_dos between %s and %s) and ref.actif=4 ' + filter_cond +
               'group by ref.code order by ref.code asc ' + limit)

        cursor.execute(req, (date_beg, date_end,))

        return cursor.fetchall()

    @staticmethod
    def getNbAnalysis(date_beg, date_end, id_ana):
        cursor = DB.cursor()

        req = ('select count(*) as total '
               'from sigl_02_data as rec '
               'inner join sigl_04_data as ana on ana.id_dos = rec.id_data '
               'inner join sigl_05_data as ref on ref.id_data = ana.ref_analyse and ref.cote_unite != "PB" '
               'where (rec.date_dos between %s and %s) and ana.ref_analyse = %s and ref.actif=4')

        cursor.execute(req, (date_beg, date_end, id_ana))

        return cursor.fetchone()

    @staticmethod
    def getAnalyzesHistoDet(args):
        cursor = DB.cursor()

        date_beg = args['date_beg']
        date_end = args['date_end']
        id_ana   = args['id_ana']
        limit    = 'LIMIT ' + str(args['limit'])

        req = ('select ref.id_data, rec.date_prescription as date_prescr, '
               'if(param_num_rec.periode=1070, if(param_num_rec.format=1072,substring(rec.num_dos_mois from 7), '
               'rec.num_dos_mois), '
               'if(param_num_rec.format=1072, substring(rec.num_dos_an from 7), rec.num_dos_an)) as rec_num, '
               'ref_var.libelle as variable, '
               'IF("dico_" = substring(dict_type.short_label, 1, 5), dict_res.label, res.valeur) as result '
               'from sigl_02_data as rec '
               'inner join sigl_04_data as ana on ana.id_dos = rec.id_data '
               'inner join sigl_05_data as ref on ref.id_data = ana.ref_analyse '
               'inner join sigl_09_data as res on res.id_analyse=ana.id_data '
               'inner join sigl_07_data as ref_var on ref_var.id_data=res.ref_variable '
               'left join sigl_05_07_data as ref_link on ref_link.id_data=res.ref_variable '
               'left join sigl_dico_data as dict_type on dict_type.id_data=ref_var.type_resultat '
               'left join sigl_dico_data as dict_res on dict_res.id_data=res.valeur '
               'left join sigl_param_num_dos_data as param_num_rec on param_num_rec.id_data = 1 '
               'where (rec.date_dos between %s and %s) and ref.id_data=%s '
               'order by rec.num_dos_an desc ' + limit)

        cursor.execute(req, (date_beg, date_end, id_ana))

        return cursor.fetchall()
