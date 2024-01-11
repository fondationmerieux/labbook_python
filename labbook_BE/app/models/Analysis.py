# -*- coding:utf-8 -*-
import logging
import mysql.connector

from flask import session

from app.models.Constants import *
from app.models.DB import DB
from app.models.Logs import Logs


class Analysis:
    log = logging.getLogger('log_db')

    @staticmethod
    def getAnalysisSearch(text, type="A", status=4, link_fam=[]):
        """Search in analysis table

        This function is call by search field on analyze or search form on setting analyze page

        Args:
            text (string): words of research.
            type (string): 'A' for search only analysis or 'P' for search only pathological product.
            status  (int): 4 for Eanbled or 5 for disabled

        Returns:
            dict: dictionnary of data.

        """

        cursor = DB.cursor()

        l_words = text.split(' ')

        cond  = 'ana.actif = 4'
        trans = ''

        if status == 5:
            cond  = 'ana.actif = 5'

        # only in analysis without sample analysis
        if type == "A":
            cond += ' and (ana.cote_unite != "PB" or ana.cote_unite is NULL)'
        # only in sample analysis
        elif type == "P":
            cond += ' and ana.cote_unite = "PB"'

        if session['lang_db'] == 'fr_FR':
            for word in l_words:
                cond = (cond +
                        ' and (ana.code like "' + word + '%" or '
                        'ana.nom like "%' + word + '%" or '
                        'ana.abbr like "%' + word + '%") ')
        else:
            trans = ('left join translations as tr on tr.tra_lang="' + str(session['lang_db']) + '" and '
                     'tr.tra_type="ana_name" and tr.tra_ref=ana.id_data ')

            for word in l_words:
                cond = (cond +
                        ' and (ana.code like "' + word + '%" or '
                        'tr.tra_text like "%' + word + '%" or '
                        'ana.abbr like "%' + word + '%") ')

        # Functionnal unit link with analyzes families
        if link_fam:

            cond_link_fam = ''
            # prepare list for sql
            for id_fam in list(link_fam):
                if not cond_link_fam:
                    cond_link_fam = '('

                cond_link_fam = cond_link_fam + str(id_fam) + ','

            if cond_link_fam:
                cond_link_fam = cond_link_fam[:-1] + ')'
                cond += ' and ana.famille in ' + cond_link_fam + ' '

        req = ('select ana.id_data as id, CONCAT(ana.code, " ", COALESCE(ana.abbr, "")) as code, '
               'ana.nom as name,  COALESCE(dict.label, "") as label '
               'from sigl_05_data as ana '
               'left join sigl_dico_data as dict on dict.id_data=ana.famille ' + trans +
               'where ' + cond + ' order by nom asc limit 1000')

        # Analysis.log.info(Logs.fileline() + ' : DEBUG-TRACE req = ' + str(req))

        cursor.execute(req)

        return cursor.fetchall()

    @staticmethod
    def getAnalysisVarSearch(text):
        """Search in variables table

        This function is call by search field on variables

        Args:
            text (string): words of research.

        Returns:
            dict: dictionnary of data.

        """

        cursor = DB.cursor()

        l_words = text.split(' ')

        cond  = 'var.libelle is not NULL '
        trans = ''

        if session['lang_db'] == 'fr_FR':
            for word in l_words:
                cond = (cond + ' and (var.libelle like "%' + word + '%") ')
        else:
            trans = ('left join translations as tr on tr.tra_lang="' + str(session['lang_db']) + '" and '
                     'tr.tra_type="var_name" and tr.tra_ref=var.id_data ')

            for word in l_words:
                cond = (cond + ' and (tr.tra_text like "%' + word + '%") ')

        req = ('select var.libelle as field_value, var.id_data '
               'from sigl_07_data as var ' + trans +
               'where ' + cond + ' order by field_value asc limit 1000')

        cursor.execute(req)

        return cursor.fetchall()

    @staticmethod
    def getAnalysis(id_ana):
        cursor = DB.cursor()

        req = ('select ana.id_data, ana.id_owner, ana.code, ana.nom, ana.abbr, ana.famille, ana.cote_unite, '
               'ana.cote_valeur, ana.commentaire, ana.produit_biologique, ana.type_prel, ana.type_analyse, ana.actif, '
               'CONCAT(samp.code, " ", COALESCE(samp.nom, "")) as product_label, ana.ana_whonet '
               'from sigl_05_data as ana '
               'left join sigl_05_data as samp on samp.id_data=ana.produit_biologique '
               'where ana.id_data=%s')

        cursor.execute(req, (id_ana,))

        return cursor.fetchone()

    @staticmethod
    def insertAnalysis(**params):
        try:
            if 'test' in params and params['test'] == 'Y':
                mode_test = '_test '
            else:
                mode_test = ' '

            cursor = DB.cursor()

            # try to insert to a specidfic id_data
            if 'id_data' in params and int(params['id_data']) > 0:
                lid_data = 'id_data, '
                vid_data = str(params['id_data']) + ', '
            else:
                lid_data = ''
                vid_data = ''

            req = ('insert into sigl_05_data' + mode_test +
                   '(' + lid_data + 'id_owner, code, nom, abbr, famille, type_prel, cote_unite, cote_valeur, commentaire, '
                   'produit_biologique, type_analyse, actif, ana_whonet) '
                   'values '
                   '(' + vid_data + '%(id_owner)s, %(code)s, %(name)s, %(abbr)s, %(type_ana)s, %(type_prod)s, %(unit)s, '
                   '%(value)s, %(comment)s, %(product)s, 170, %(stat)s, %(whonet)s)')

            cursor.execute(req, params)

            Analysis.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Analysis.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def updateAnalysis(**params):
        try:
            if 'test' in params and params['test'] == 'Y':
                mode_test = '_test '
            else:
                mode_test = ' '

            cursor = DB.cursor()

            cursor.execute('update sigl_05_data' + mode_test +
                           'set id_owner=%(id_owner)s, code=%(code)s, nom=%(name)s, abbr=%(abbr)s, actif=%(stat)s, '
                           'famille=%(type_ana)s, type_prel=%(type_prod)s, cote_unite=%(unit)s, cote_valeur=%(value)s, '
                           'commentaire=%(comment)s, produit_biologique=%(product)s, ana_whonet=%(whonet)s '
                           'where id_data=%(id_data)s', params)

            Analysis.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Analysis.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def deleteAnalysis(id_ana):
        try:
            cursor = DB.cursor()

            cursor.execute('delete from sigl_05_data '
                           'where id_data=%s', (id_ana,))

            cursor.execute('delete from sigl_05_07_data '
                           'where id_refanalyse=%s', (id_ana,))

            Analysis.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Analysis.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getProductType(id_data):
        cursor = DB.cursor()

        req = ('select id_data, id_owner, dico_name, label, short_label, position, code '
               'from sigl_dico_data '
               'where id_data=%s')

        cursor.execute(req, (id_data,))

        return cursor.fetchone()

    @staticmethod
    def getAnalysisReq(id_rec, type_ana):
        cursor = DB.cursor()

        # Only analysis
        if type_ana == 'Y':
            cond = ' and (cote_unite is NULL or cote_unite != "PB")'
        # Only samples
        elif type_ana == 'N':
            cond = ' and cote_unite="PB"'
        # Everything
        else:
            cond = ''

        req = ('select req_ana.id_data as id_data, req_ana.id_owner as id_owner, req_ana.id_dos as id_dos, '
               'req_ana.ref_analyse as ref_analyse, req_ana.prix as prix, req_ana.paye as paye, req_ana.urgent as urgent, '
               'req_ana.demande as demande, req_ana.req_outsourced as outsourced, ref_ana.code as code, ref_ana.nom as nom, '
               'ref_ana.cote_unite as cote_unite, ref_ana.cote_valeur as cote_valeur, '
               'ifnull(ref_ana.type_prel, 0) as type_samp, '
               'ifnull(ref_ana.produit_biologique, 0) as id_samp_act '
               'from sigl_04_data as req_ana '
               'left join sigl_05_data as ref_ana on ref_ana.id_data=ref_analyse '
               'where id_dos=%s' + cond)

        cursor.execute(req, (id_rec,))

        return cursor.fetchall()

    @staticmethod
    def getAnalysisOutsourced(id_rec, type_ana):
        cursor = DB.cursor()

        # Only analysis
        if type_ana == 'Y':
            cond = ' and (cote_unite is NULL or cote_unite != "PB")'
        # Only samples
        elif type_ana == 'N':
            cond = ' and cote_unite="PB"'
        # Everything
        else:
            cond = ''

        req = ('select req_ana.id_data as id_data, req_ana.id_dos as id_rec, '
               'req_ana.ref_analyse as ref_analyse, req_ana.urgent as urgent, req_ana.demande as demande, '
               'req_ana.req_outsourced as outsourced, ref_ana.code as code, ref_ana.nom as ana_name, '
               'ref_ana.commentaire as ana_comm, d1.label as ana_fam, '
               'ifnull(ref_ana.type_prel, 0) as type_samp, '
               'ifnull(ref_ana.produit_biologique, 0) as id_samp_act '
               'from sigl_04_data as req_ana '
               'left join sigl_05_data as ref_ana on ref_ana.id_data=ref_analyse '
               'left join sigl_dico_data as d1 on d1.id_data=ref_ana.famille '
               'where req_ana.id_dos=%s' + cond)

        cursor.execute(req, (id_rec,))

        return cursor.fetchall()

    @staticmethod
    def insertAnalysisReq(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into sigl_04_data '
                           '(id_owner, id_dos, ref_analyse, prix, paye, urgent, demande, req_outsourced) '
                           'values '
                           '(%(id_owner)s, %(id_dos)s, %(ref_analyse)s, %(prix)s, %(paye)s, %(urgent)s, '
                           '%(demande)s, %(outsourced)s)', params)

            Analysis.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Analysis.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def deleteAnalysisReq(id_req, id_rec, id_ana, type_samp):
        try:
            cursor = DB.cursor()

            if id_ana:
                # Count the number of analysis in this record that have in common the act of sampling
                cursor.execute('select count(*) as nb_samp_act from sigl_04_data as req '
                               'inner join sigl_05_data as ana on ana.id_data=req.ref_analyse '
                               'where req.id_dos=%s and ana.produit_biologique = '
                               '(select produit_biologique from sigl_05_data where id_data=%s)', (id_rec, id_ana))

                nb = cursor.fetchone()

                if nb:
                    if nb['nb_samp_act'] == 1:
                        # delete sample act request
                        cursor.execute('delete from sigl_04_data as req '
                                       'inner join sigl_05_data as ana on ana.id_data=req.ref_analyse '
                                       'where req.id_dos=%s and req.ref_analyse = '
                                       '(select produit_biologique from sigl_05_data where id_data=%s)', (id_rec, id_ana))

                    # delete all pathological product for this analysis
                    cursor.execute('delete from sigl_01_data '
                                   'where id_dos=%s and samp_id_ana=%s', (id_rec, id_ana))

            # delete analysis request
            cursor.execute('delete from sigl_04_data '
                           'where id_data=%s and id_dos=%s', (id_req, id_rec))

            Analysis.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Analysis.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getAllVariable():
        cursor = DB.cursor()

        req = ('select var.id_data as id_item, var.code_var, var.libelle as label, var.commentaire as comment, '
               'd1.label as type_res '
               'from sigl_07_data as var '
               'left join sigl_dico_data as d1 on d1.id_data=var.type_resultat '
               'order by var.libelle asc')

        cursor.execute(req)

        return cursor.fetchall()

    @staticmethod
    def getListVariable(id_ana, test='N'):
        cursor = DB.cursor()

        if test == 'Y':
            mode_test = '_test '
        else:
            mode_test = ' '

        req = ('select var.id_data, libelle as label, description as descr, unite as unit, normal_min as min, '
               'normal_max as max, commentaire as comment, type_resultat as type_res, unite2 as unit2, '
               'formule_unite2 as formula2, formule as formula, var.accuracy as accu, precision2 as accu2, '
               'link.position as pos, link.num_var as num_var, link.obligatoire as oblig, link.var_whonet, '
               'link.var_qrcode, link.id_data as id_link, d1.label as unit_label, var.id_data as id_item, '
               'var.code_var, var.var_show_minmax, var.var_highlight '
               'from sigl_07_data' + mode_test + ' as var '
               'inner join sigl_05_07_data' + mode_test + ' as link on link.id_refvariable=var.id_data '
               'left join sigl_dico_data as d1 on d1.id_data=var.unite '
               'where link.id_refanalyse=%s '
               'order by link.position, link.id_data')

        cursor.execute(req, (id_ana,))

        return cursor.fetchall()

    @staticmethod
    def getAnalysisVar(id_var):
        cursor = DB.cursor()

        req = ('select id_data, libelle as label, description as descr, unite as unit, normal_min as min, '
               'normal_max as max, commentaire as comment, type_resultat as type_res, unite2 as unit2, '
               'formule_unite2 as formula2, formule as formula, accuracy as accu, precision2 as accu2, code_var, '
               'var_show_minmax, var_highlight '
               'from sigl_07_data '
               'where id_data=%s')

        cursor.execute(req, (id_var,))

        return cursor.fetchone()

    @staticmethod
    def getLastAnalysisVar():
        cursor = DB.cursor()

        req = ('select id_data, libelle as label, description as descr, unite as unit, normal_min as min, '
               'normal_max as max, commentaire as comment, type_resultat as type_res, unite2 as unit2, '
               'formule_unite2 as formula2, formule as formula, accuracy as accu, precision2 as accu2, code_var, '
               'var_show_minmax, var_highlight '
               'from sigl_07_data '
               'order by id_data desc limit 1')

        cursor.execute(req)

        return cursor.fetchone()

    @staticmethod
    def getAnalysisVarExist(label, type_res, unit, var_min, var_max, code_var, test='N'):
        cursor = DB.cursor()

        if test == 'Y':
            mode_test = '_test '
        else:
            mode_test = ' '

        req = ('select id_data, libelle as label, description as descr, unite as unit, normal_min as min, '
               'normal_max as max, commentaire as comment, type_resultat as type_res, unite2 as unit2, '
               'formule_unite2 as formula2, formule as formula, accuracy as accu, precision2 as accu2, code_var, '
               'var_show_minmax, var_highlight '
               'from sigl_07_data' + mode_test +
               'where libelle=%s and type_resultat=%s and unite=%s and normal_min=%s and normal_max=%s and code_var=%s '
               'order by id_data asc limit 1')

        cursor.execute(req, (label, type_res, unit, var_min, var_max, code_var,))

        return cursor.fetchone()

    @staticmethod
    def insertAnalysisVar(**params):
        try:
            if 'test' in params and params['test'] == 'Y':
                mode_test = '_test '
            else:
                mode_test = ' '
                params['test'] = 'N'

            upd_code_var = False

            # avoid empty code_var
            if not params['code_var']:
                upd_code_var = True

                last_var = Analysis.getLastAnalysisVar()

                if last_var:
                    last_var = int(last_var['code_var']) + 1
                    params['code_var'] = str(last_var)
                else:
                    params['code_var'] = "NO_CODE_VAR"

            cursor = DB.cursor()

            cursor.execute('insert into sigl_07_data' + mode_test +
                           '(id_owner, libelle, description, unite, normal_min, normal_max, commentaire, type_resultat, '
                           'unite2, formule_unite2, formule, accuracy, precision2, code_var, var_show_minmax, var_highlight) '
                           'values '
                           '(%(id_owner)s, %(label)s, %(descr)s, %(unit)s, %(var_min)s, %(var_max)s, '
                           '%(comment)s, %(type_res)s, %(unit2)s, %(formula2)s, %(formula)s, '
                           '%(accu)s, %(accu2)s, %(code_var)s, %(var_show_minmax)s, %(var_highlight)s)', params)

            Analysis.log.info(Logs.fileline())

            id_var = cursor.lastrowid

            # if code_var is empty update with id_data
            if upd_code_var:
                Analysis.updateAnalysisVar(id_data=id_var,
                                           id_owner=params['id_owner'],
                                           label=params['label'],
                                           code_var=id_var,
                                           descr=params['descr'],
                                           type_res=params['type_res'],
                                           var_min=params['var_min'],
                                           var_max=params['var_max'],
                                           var_show_minmax=params['var_show_minmax'],
                                           var_highlight=params['var_highlight'],
                                           comment=params['comment'],
                                           formula=params['formula'],
                                           unit=params['unit'],
                                           accu=params['accu'],
                                           formula2=params['formula2'],
                                           unit2=params['unit2'],
                                           accu2=params['accu2'],
                                           test=params['test'])

                Analysis.log.info(Logs.fileline() + ' : update and init code_var')

            return id_var
        except mysql.connector.Error as e:
            Analysis.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def updateAnalysisVar(**params):
        try:
            if 'test' in params and params['test'] == 'Y':
                mode_test = '_test '
            else:
                mode_test = ' '

            cursor = DB.cursor()

            cursor.execute('update sigl_07_data' + mode_test +
                           'set id_owner=%(id_owner)s, libelle=%(label)s, description=%(descr)s, '
                           'unite=%(unit)s, normal_min=%(var_min)s, normal_max=%(var_max)s, '
                           'commentaire=%(comment)s, type_resultat=%(type_res)s, unite2=%(unit2)s, '
                           'formule_unite2=%(formula2)s, formule=%(formula)s, accuracy=%(accu)s, '
                           'precision2=%(accu2)s, code_var=%(code_var)s, var_show_minmax=%(var_show_minmax)s, '
                           'var_highlight=%(var_highlight)s '
                           'where id_data=%(id_data)s', params)

            Analysis.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Analysis.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getRefVariable(id_ana):
        cursor = DB.cursor()

        req = ('select id_data, id_owner, id_refanalyse, id_refvariable, position, num_var, obligatoire, var_whonet, '
               'var_qrcode '
               'from sigl_05_07_data '
               'where id_refanalyse=%s')

        cursor.execute(req, (id_ana,))

        return cursor.fetchall()

    @staticmethod
    def insertRefVariable(**params):
        try:
            if 'test' in params and params['test'] == 'Y':
                mode_test = '_test '
            else:
                mode_test = ' '

            cursor = DB.cursor()

            cursor.execute('insert into sigl_05_07_data' + mode_test +
                           '(id_owner, id_refanalyse, id_refvariable, position, num_var, obligatoire, var_whonet, '
                           'var_qrcode) '
                           'values '
                           '(%(id_owner)s, %(id_refana)s, %(id_refvar)s, %(var_pos)s, %(var_num)s, %(oblig)s, '
                           '%(var_whonet)s, %(var_qrcode)s)', params)

            Analysis.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Analysis.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def updateRefVariable(**params):
        try:
            if 'test' in params and params['test'] == 'Y':
                mode_test = '_test '
            else:
                mode_test = ' '

            cursor = DB.cursor()

            cursor.execute('update sigl_05_07_data' + mode_test +
                           'set id_owner=%(id_owner)s, id_refanalyse=%(id_refana)s, id_refvariable=%(id_refvar)s, '
                           'position=%(var_pos)s, num_var=%(var_num)s, obligatoire=%(oblig)s, var_whonet=%(var_whonet)s, '
                           'var_qrcode=%(var_qrcode)s '
                           'where id_data=%(id_data)s', params)

            Analysis.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Analysis.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def deleteRefVar(id_refana, id_refvar):
        try:
            cursor = DB.cursor()

            cursor.execute('delete from sigl_05_07_data '
                           'where id_refanalyse=%s and id_refvariable=%s', (id_refana, id_refvar,))

            Analysis.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Analysis.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getLastAnalysisReqByRefAna(ref_ana):
        cursor = DB.cursor()

        req = ('select id_data, id_owner, id_dos, ref_analyse, prix, paye, urgent, demande, req_outsourced as outsourced '
               'from sigl_04_data '
               'where ref_analyse=%s '
               'order by id_data desc limit 1')

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
        trans       = ''

        if not args:
            limit = 'LIMIT 2000'

            filter_cond += ' ana.actif=4 '  # remove deleted analyzes by default
        else:
            limit = 'LIMIT 2000'

            filter_cond += ' '  # remove deleted analyzes by default
            # filter conditions
            if 'status' in args and args['status'] > 0:
                filter_cond += ' ana.actif=' + str(args['status']) + ' '
            else:
                filter_cond += ' ana.actif=4 '  # keep only activated analyzes by default

            if session and session['lang_db'] == 'fr_FR':
                if 'name' in args and args['name']:
                    filter_cond += (' and (ana.nom LIKE "%' + args['name'] + '%" or ana.code LIKE "%' +
                                    args['name'] + '%" or ana.abbr LIKE "%' + args['name'] + '%") ')
            else:
                if 'name' in args and args['name']:
                    trans = ('left join translations as tr on tr.tra_lang="' + str(session['lang_db']) + '" and '
                             'tr.tra_type="ana_name" and tr.tra_ref=ana.id_data ')

                    filter_cond += (' and (tr.tra_text LIKE "%' + args['name'] + '%" or ana.code LIKE "%' +
                                    args['name'] + '%" or ana.abbr LIKE "%' + args['name'] + '%") ')

            if 'type_ana' in args and args['type_ana'] > 0:
                filter_cond += ' and ana.famille=' + str(args['type_ana']) + ' '

            if 'type_prod' in args and args['type_prod'] > 0:
                filter_cond += ' and ana.type_prel=' + str(args['type_prod']) + ' '

        req = ('select ana.id_data, ana.code, ana.nom as name, ana.abbr, ana.actif as stat, '
               'dico.label as type_ana, samp.nom as product, ana.produit_biologique as id_prod '
               'from sigl_05_data as ana '
               'left join sigl_dico_data as dico on dico.id_data=ana.famille '
               'left join sigl_05_data as samp on samp.id_data=ana.produit_biologique ' + trans +
               'where ' + filter_cond +
               'group by ana.code order by ana.code asc ' + limit)

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
               'inner join sigl_04_data as req on req.id_dos = rec.id_data '
               'inner join sigl_05_data as ref on ref.id_data = req.ref_analyse and ref.cote_unite != "PB" '
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
               'inner join sigl_04_data as req on req.id_dos = rec.id_data '
               'inner join sigl_05_data as ref on ref.id_data = req.ref_analyse and ref.cote_unite != "PB" '
               'where (rec.date_dos between %s and %s) and req.ref_analyse = %s and ref.actif=4')

        cursor.execute(req, (date_beg, date_end, id_ana))

        return cursor.fetchone()

    @staticmethod
    def getNbAnaByVar(id_var):
        cursor = DB.cursor()

        req = ('select count(*) as nb_link '
               'from sigl_05_07_data as link '
               'where link.id_refvariable = %s')

        cursor.execute(req, (id_var,))

        return cursor.fetchone()

    @staticmethod
    def getAnalyzesHistoDet(args):
        cursor = DB.cursor()

        date_beg = args['date_beg']
        date_end = args['date_end']
        id_ana   = args['id_ana']
        limit    = 'LIMIT ' + str(args['limit'])

        req = ('select ref.id_data, rec.id_data as id_rec, rec.date_prescription as date_prescr, rec.type as type_rec, '
               'if(param_num_rec.periode=1070, if(param_num_rec.format=1072,substring(rec.num_dos_mois from 7), '
               'rec.num_dos_mois), '
               'if(param_num_rec.format=1072, substring(rec.num_dos_an from 7), rec.num_dos_an)) as rec_num, '
               'ref_var.libelle as variable, '
               'IF("dico_" = substring(dict_type.short_label, 1, 5), dict_res.label, res.valeur) as result '
               'from sigl_02_data as rec '
               'inner join sigl_04_data as req on req.id_dos = rec.id_data '
               'inner join sigl_05_data as ref on ref.id_data = req.ref_analyse '
               'inner join sigl_09_data as res on res.id_analyse=req.id_data '
               'inner join sigl_07_data as ref_var on ref_var.id_data=res.ref_variable '
               'left join sigl_05_07_data as ref_link on ref_link.id_data=res.ref_variable '
               'left join sigl_dico_data as dict_type on dict_type.id_data=ref_var.type_resultat '
               'left join sigl_dico_data as dict_res on dict_res.id_data=res.valeur '
               'left join sigl_param_num_dos_data as param_num_rec on param_num_rec.id_data = 1 '
               'where (rec.date_dos between %s and %s) and ref.id_data=%s '
               'order by rec.num_dos_an desc ' + limit)

        cursor.execute(req, (date_beg, date_end, id_ana))

        return cursor.fetchall()

    @staticmethod
    def exist(code, test='N'):
        try:
            if test == 'Y':
                mode_test = '_test '
            else:
                mode_test = ' '

            cursor = DB.cursor()

            cursor.execute('select count(*) as nb_code '
                           'from sigl_05_data' + mode_test +
                           'where code=%s', (code,))

            ret = cursor.fetchone()

            if ret and ret['nb_code'] == 0:
                return False
            else:
                return True
        except mysql.connector.Error as e:
            Analysis.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return -1

    @staticmethod
    def freeIdAna(id_ana, test='N'):
        try:
            if test == 'Y':
                mode_test = '_test '
            else:
                mode_test = ' '

            cursor = DB.cursor()

            cursor.execute('select count(*) as nb_ana '
                           'from sigl_05_data' + mode_test +
                           'where id_data=%s', (id_ana,))

            ret = cursor.fetchone()

            if ret and ret['nb_ana'] == 0:
                return True
            else:
                return False
        except mysql.connector.Error as e:
            Analysis.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return -1

    @staticmethod
    def getAnalysisExport():
        cursor = DB.cursor()

        req = ('select ana.id_data, ana.id_owner, ana.code, ana.nom, ana.abbr, ana.famille, '
               'ana.cote_unite, ana.cote_valeur, ana.commentaire, ana.produit_biologique, ana.type_prel, '
               'ana.type_analyse, ana.actif, ana.ana_whonet, link.id_data as id_link, link.id_refanalyse, '
               'link.id_refvariable, link.position, link.num_var, link.obligatoire, link.var_whonet, link.var_qrcode, '
               'var.id_data as id_var, var.libelle, var.description, var.unite, var.normal_min, var.normal_max, '
               'var.commentaire as var_comm, var.type_resultat, var.unite2, var.formule_unite2, var.formule, '
               'var.accuracy, var.precision2, var.code_var, var.var_show_minmax, var.var_highlight '
               'from sigl_05_data as ana '
               'left join sigl_05_07_data as link on link.id_refanalyse=ana.id_data '
               'left join sigl_07_data as var on var.id_data=link.id_refvariable '
               'order by ana.id_data asc')

        cursor.execute(req)

        return cursor.fetchall()

    @staticmethod
    def getDataset(date_beg, date_end):
        cursor = DB.cursor()

        req = ('select rec.id_data as id_analysis, rec.rec_custody, rec.id_patient, d_type.label as type, '
               'date_format(rec.date_dos, %s) as record_date, rec.rec_num_int, rec.num_dos_an as rec_num_year, '
               'rec.num_dos_jour as rec_num_day, rec.num_dos_mois as rec_num_month, rec.rec_modified, '
               'rec.med_prescripteur as id_doctor, doctor.nom as doctor_lname, doctor.prenom as doctor_fname, '
               'date_format(rec.date_prescription, %s) as prescription_date, rec.service_interne as internal_service, '
               'rec.num_lit as bed_num, rec.rec_hosp_num, rec.prix as price, rec.remise as discount, '
               'rec.remise_pourcent as discount_percent, rec.assu_pourcent as insurance_percent, rec.a_payer as to_pay, '
               'd_status.label as status, date_format(rec.date_hosp, %s) as hosp_date, '
               'req.ref_analyse as id_analysis, req.prix as ana_price, req.urgent as ana_emergency, '
               'req.req_outsourced as ana_outsourced, ana.code as analysis_code, ana.nom as analysis_name, '
               'd_fam.label as analysis_family, date_format(pat.ddn, %s) as birth, pat.nom as pat_name, '
               'pat.prenom as pat_firstname, pat.age, d_sex.label as sex, '
               'd_age_unit.label as age_unit, pat.tel as phone1, pat.pat_phone2 as phone2 '
               'from sigl_02_data as rec '
               'inner join sigl_04_data as req on req.id_dos=rec.id_data '
               'inner join sigl_05_data as ana on ana.id_data=req.ref_analyse '
               'inner join sigl_dico_data as d_fam on d_fam.id_data=ana.famille and ana.famille > 0 '
               'left join sigl_08_data as doctor on doctor.id_data=rec.med_prescripteur '
               'left join sigl_dico_data as d_type on d_type.id_data=rec.type '
               'left join sigl_dico_data as d_status on d_status.id_data=rec.statut '
               'inner join sigl_03_data as pat on pat.id_data=rec.id_patient '
               'left join sigl_dico_data as d_age_unit on d_age_unit.id_data=pat.unite '
               'left join sigl_dico_data as d_sex on d_sex.id_data=pat.sexe '
               'where rec.date_dos between %s and %s '
               'order by rec.id_data desc')

        cursor.execute(req, (Constants.cst_isodate, Constants.cst_isodate, Constants.cst_isodate, Constants.cst_isodate, date_beg, date_end))

        return cursor.fetchall()

    @staticmethod
    def updateAnalysisStatus(status, id_ana):
        try:
            cursor = DB.cursor()

            # 29/03/2023 FMX ask for not disabled sample acts
            cond = ' (cote_unite != "PB" or cote_unite is NULL) '

            if status == 'E':
                status = 4
                cond += ' and actif != 4 '
            elif status == 'D':
                status = 5
                cond += ' and actif != 5 '

            # if a specific analysis
            if id_ana > 0:
                cond += ' and id_data=' + str(id_ana)

            req = ('update sigl_05_data '
                   'set actif=%s '
                   'where ' + cond)

            cursor.execute(req, (status,))

            Analysis.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Analysis.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def dropTableTest():
        try:
            cursor = DB.cursor()

            cursor.execute('truncate table sigl_05_data_test')
            cursor.execute('truncate table sigl_05_07_data_test')
            cursor.execute('truncate table sigl_07_data_test')

            return True
        except mysql.connector.Error as e:
            Analysis.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def initTableTest():
        try:
            cursor = DB.cursor()

            cursor.execute('insert into sigl_05_data_test select * from sigl_05_data')
            cursor.execute('insert into sigl_05_07_data_test select * from sigl_05_07_data')
            cursor.execute('insert into sigl_07_data_test select * from sigl_07_data')

            return True
        except mysql.connector.Error as e:
            Analysis.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def cleanGhostVar(test='N'):
        try:
            if test == 'Y':
                mode_test = '_test '
            else:
                mode_test = ' '

            cursor = DB.cursor()

            cursor.execute('delete from sigl_07_data' + mode_test + ' as var '
                           'where id_data not in (select id_refvariable from sigl_05_07_data' + mode_test + ')')

            return True
        except mysql.connector.Error as e:
            Analysis.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False
