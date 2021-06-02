# -*- coding:utf-8 -*-
import logging

from datetime import datetime
from flask import request
from flask_restful import Resource

from app.models.General import compose_ret
from app.models.Constants import *
from app.models.Analysis import *
from app.models.User import *
from app.models.Logs import Logs


class AnalysisSearch(Resource):
    log = logging.getLogger('log_services')

    def post(self, type):
        args = request.get_json()

        l_analysis = Analysis.getAnalysisSearch(args['term'], type)

        if not l_analysis:
            self.log.error(Logs.fileline() + ' : TRACE AnalysisSearch not found')

        self.log.info(Logs.fileline() + ' : TRACE AnalysisSearch')
        return compose_ret(l_analysis, Constants.cst_content_type_json)


class AnalysisVarSearch(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        l_vars = Analysis.getAnalysisVarSearch(args['term'])

        if not l_vars:
            self.log.error(Logs.fileline() + ' : TRACE AnalysisVarSearch not found')

        self.log.info(Logs.fileline() + ' : TRACE AnalysisVarSearch')
        return compose_ret(l_vars, Constants.cst_content_type_json)


class AnalysisList(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        if not args:
            args = {}

        l_analyzes = Analysis.getAnalyzesList(args)

        if not l_analyzes:
            self.log.error(Logs.fileline() + ' : TRACE AnalysisList not found')

        for analysis in l_analyzes:
            # Replace None by empty string
            for key, value in list(analysis.items()):
                if analysis[key] is None:
                    analysis[key] = ''

        self.log.info(Logs.fileline() + ' : TRACE AnalysisList')
        return compose_ret(l_analyzes, Constants.cst_content_type_json)


class AnalysisHistoExport(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        l_data = [['id_data', 'code', 'fam_name', 'name']]

        if 'date_beg' not in args or 'date_end' not in args:
            self.log.error(Logs.fileline() + ' : AnalysisHistoExport ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        args['limit'] = 50000  # for overpassed default limit

        dict_data = Analysis.getAnalyzesHistoList(args)

        if dict_data:
            for d in dict_data:
                data = []

                data.append(d['id_data'])
                data.append(d['code'])
                data.append(d['fam_name'])
                data.append(d['name'])

                l_data.append(data)

        # if no result to export
        if len(l_data) < 2:
            self.log.info(Logs.fileline() + ' : TRACE AnalysisHistoExport NOT FOUND')
            return compose_ret('', Constants.cst_content_type_json, 404)

        # write csv file
        try:
            import csv

            today = datetime.now().strftime("%Y%m%d")

            filename = 'analyzes_' + str(today) + '.csv'

            with open('tmp/' + filename, mode='w', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=';')
                for line in l_data:
                    writer.writerow(line)

        except Exception as err:
            self.log.error(Logs.fileline() + ' : post AnalysisHistoExport failed, err=%s', err)
            return False

        self.log.info(Logs.fileline() + ' : TRACE AnalysisHistoExport')
        return compose_ret('', Constants.cst_content_type_json)


class AnalysisHistoList(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        if 'date_beg' not in args or 'date_end' not in args:
            self.log.error(Logs.fileline() + ' : AnalysisHistoList ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        args['limit'] = 7000

        l_analyzes = Analysis.getAnalyzesHistoList(args)

        if not l_analyzes:
            self.log.error(Logs.fileline() + ' : TRACE AnalysisHistoList not found')

        for analysis in l_analyzes:
            # Replace None by empty string
            for key, value in list(analysis.items()):
                if analysis[key] is None:
                    analysis[key] = ''

            nb_ana = Analysis.getNbAnalysis(args['date_beg'], args['date_end'], analysis['id_data'])

            if nb_ana:
                analysis['nb_ana'] = nb_ana['total']

        self.log.info(Logs.fileline() + ' : TRACE AnalysisHistoList')
        return compose_ret(l_analyzes, Constants.cst_content_type_json)


class AnalysisHistoDet(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        if 'date_beg' not in args or 'date_end' not in args or 'id_ana' not in args:
            self.log.error(Logs.fileline() + ' : AnalysisHistoDet ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        args['limit'] = 7000

        l_datas = Analysis.getAnalyzesHistoDet(args)

        if not l_datas:
            self.log.error(Logs.fileline() + ' : TRACE AnalysisHistoDet not found')

        for data in l_datas:
            # Replace None by empty string
            for key, value in list(data.items()):
                if data[key] is None:
                    data[key] = ''

            if data['date_prescr']:
                data['date_prescr'] = datetime.strftime(data['date_prescr'], '%Y-%m-%d')

            if data['type_rec'] and data['type_rec'] == 183:
                data['type_rec'] = 'E'
            else:
                data['type_rec'] = 'I'

        self.log.info(Logs.fileline() + ' : TRACE AnalysisHistoDet')
        return compose_ret(l_datas, Constants.cst_content_type_json)


class AnalysisCode(Resource):
    log = logging.getLogger('log_services')

    def get(self, code):
        ret = Analysis.exist(code)

        if ret and ret == -1:
            self.log.error(Logs.fileline() + ' : ' + 'AnalysisCode ERROR sql')
            return compose_ret(-1, Constants.cst_content_type_json, 500)

        if ret:
            self.log.error(Logs.fileline() + ' : ' + 'AnalysisCode WARNING code already exist')
            return compose_ret(1, Constants.cst_content_type_json, 200)
        else:
            self.log.info(Logs.fileline() + ' : AnalysisCode code ok :' + str(code))
            return compose_ret(0, Constants.cst_content_type_json, 200)


class AnalysisDet(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_ana):
        analysis = Analysis.getAnalysis(id_ana)

        if not analysis:
            self.log.error(Logs.fileline() + ' : ' + 'AnalysisDet ERROR not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        # Replace None by empty string
        for key, value in list(analysis.items()):
            if analysis[key] is None:
                analysis[key] = ''

        self.log.info(Logs.fileline() + ' : AnalysisDet id_data=' + str(id_ana))
        return compose_ret(analysis, Constants.cst_content_type_json, 200)

    def post(self, id_ana):
        args = request.get_json()

        if 'id_ana' not in args or 'code' not in args or 'name' not in args or 'abbr' not in args or \
           'type_ana' not in args or 'type_prod' not in args or 'unit' not in args or 'value' not in args or \
           'stat' not in args or 'comment' not in args or 'product' not in args or 'list_var' not in args or \
           'whonet' not in args:
            self.log.error(Logs.fileline() + ' : AnalysisDet ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        id_ana = args['id_ana']

        # check if analysis already exist
        analysis = Analysis.getAnalysis(id_ana)

        # UPDATE ANALYSIS...
        if analysis and analysis['id_data'] == id_ana:
            self.log.error(Logs.fileline() + ' : AnalysisDet UPDATE analysis')

            # update analysis
            ret = Analysis.updateAnalysis(id_data=id_ana,
                                          id_owner=args['id_owner'],
                                          code=args['code'],
                                          name=args['name'],
                                          abbr=args['abbr'],
                                          type_ana=args['type_ana'],
                                          type_prod=args['type_prod'],
                                          unit=args['unit'],
                                          value=args['value'],
                                          stat=args['stat'],
                                          comment=args['comment'],
                                          product=args['product'],
                                          whonet=args['whonet'])

            if ret is False:
                self.log.info(Logs.fileline() + ' : TRACE AnalysisDet ERROR update analysis')
                return compose_ret('', Constants.cst_content_type_json, 500)

            # delete missing link to variable compared to analysis (get list before add new var)
            db_l_var = Analysis.getListVariable(id_ana)

            for var in args['list_var']:
                if var['id_var'] > 0:
                    # update variable which already exist
                    ret = Analysis.updateAnalysisVar(id_data=var['id_var'],
                                                     id_owner=args['id_owner'],
                                                     label=var['var_label'],
                                                     code_var=var['var_code'],
                                                     descr=var['var_descr'],
                                                     type_res=var['var_type_res'],
                                                     var_min=var['var_min'],
                                                     var_max=var['var_max'],
                                                     comment=var['var_comment'],
                                                     formula=var['var_formula'],
                                                     unit=var['var_unit'],
                                                     accu=var['var_accu'],
                                                     formula2=var['var_formula2'],
                                                     unit2=var['var_unit2'],
                                                     accu2=var['var_accu2'])

                    if ret is False:
                        self.log.info(Logs.fileline() + ' : TRACE AnalysisDet ERROR update var analysis')
                        return compose_ret('', Constants.cst_content_type_json, 500)

                    # new link with analysis
                    if var['id_link'] == 0:
                        ret = Analysis.insertRefVariable(id_owner=args['id_owner'],
                                                         id_refana=id_ana,
                                                         id_refvar=var['id_var'],
                                                         var_pos=var['var_pos'],
                                                         var_num=var['var_num'],
                                                         oblig=var['var_oblig'],
                                                         var_whonet=var['var_whonet'])

                        if ret <= 0:
                            self.log.info(Logs.fileline() + ' : TRACE AnalysisDet ERROR insert link var to analysis')
                            return compose_ret('', Constants.cst_content_type_json, 500)
                    else:
                        ret = Analysis.updateRefVariable(id_data=var['id_link'],
                                                         id_owner=args['id_owner'],
                                                         id_refana=id_ana,
                                                         id_refvar=var['id_var'],
                                                         var_pos=var['var_pos'],
                                                         var_num=var['var_num'],
                                                         oblig=var['var_oblig'],
                                                         var_whonet=var['var_whonet'])

                        if not ret:
                            self.log.info(Logs.fileline() + ' : TRACE AnalysisDet ERROR update link var to analysis')
                            return compose_ret('', Constants.cst_content_type_json, 500)

                else:
                    # insert new variable
                    ret = Analysis.insertAnalysisVar(id_owner=args['id_owner'],
                                                     label=var['var_label'],
                                                     code_var=var['var_code'],
                                                     descr=var['var_descr'],
                                                     type_res=var['var_type_res'],
                                                     var_min=var['var_min'],
                                                     var_max=var['var_max'],
                                                     comment=var['var_comment'],
                                                     formula=var['var_formula'],
                                                     unit=var['var_unit'],
                                                     accu=var['var_accu'],
                                                     formula2=var['var_formula2'],
                                                     unit2=var['var_unit2'],
                                                     accu2=var['var_accu2'])

                    if ret is False:
                        self.log.info(Logs.fileline() + ' : TRACE AnalysisDet ERROR insert var analysis')
                        return compose_ret('', Constants.cst_content_type_json, 500)

                    id_var = ret

                    # link variable
                    ret = Analysis.insertRefVariable(id_owner=args['id_owner'],
                                                     id_refana=id_ana,
                                                     id_refvar=id_var,
                                                     var_pos=var['var_pos'],
                                                     var_num=var['var_num'],
                                                     oblig=var['var_oblig'],
                                                     var_whonet=var['var_whonet'])

                    if ret <= 0:
                        self.log.info(Logs.fileline() + ' : TRACE AnalysisDet ERROR insert link var to analysis')
                        return compose_ret('', Constants.cst_content_type_json, 500)

            for db_var in db_l_var:
                exist = False
                for ihm_var in args['list_var']:
                    if db_var['id_data'] == ihm_var['id_var']:
                        exist = True

                if not exist:
                    ret = Analysis.deleteRefVar(id_ana, db_var['id_data'])

                    if ret is False:
                        self.log.info(Logs.fileline() + ' : TRACE AnalysisDet ERROR delete link var analysis')
                        return compose_ret('', Constants.cst_content_type_json, 500)

        # INSERT NEW ANALYSIS...
        else:
            self.log.error(Logs.fileline() + ' : AnalysisDet INSERT analysis')

            # insert analysis
            ret = Analysis.insertAnalysis(id_owner=args['id_owner'],
                                          code=args['code'],
                                          name=args['name'],
                                          abbr=args['abbr'],
                                          type_ana=args['type_ana'],
                                          type_prod=args['type_prod'],
                                          unit=args['unit'],
                                          value=args['value'],
                                          stat=args['stat'],
                                          comment=args['comment'],
                                          product=args['product'],
                                          whonet=args['whonet'])

            if ret <= 0:
                self.log.info(Logs.fileline() + ' : TRACE AnalysisDet ERROR insert analysis')
                return compose_ret('', Constants.cst_content_type_json, 500)

            id_ana = ret

            for var in args['list_var']:
                if var['id_var'] > 0:
                    # update variable which already exist
                    ret = Analysis.updateAnalysisVar(id_data=var['id_var'],
                                                     id_owner=args['id_owner'],
                                                     label=var['var_label'],
                                                     code_var=var['var_code'],
                                                     descr=var['var_descr'],
                                                     type_res=var['var_type_res'],
                                                     var_min=var['var_min'],
                                                     var_max=var['var_max'],
                                                     comment=var['var_comment'],
                                                     formula=var['var_formula'],
                                                     unit=var['var_unit'],
                                                     accu=var['var_accu'],
                                                     formula2=var['var_formula2'],
                                                     unit2=var['var_unit2'],
                                                     accu2=var['var_accu2'])

                    if ret is False:
                        self.log.info(Logs.fileline() + ' : TRACE AnalysisDet ERROR update var analysis')
                        return compose_ret('', Constants.cst_content_type_json, 500)

                    # link variable
                    ret = Analysis.insertRefVariable(id_owner=args['id_owner'],
                                                     id_refana=id_ana,
                                                     id_refvar=var['id_var'],
                                                     var_pos=var['var_pos'],
                                                     var_num=var['var_num'],
                                                     oblig=var['var_oblig'],
                                                     var_whonet=var['var_whonet'])

                    if ret <= 0:
                        self.log.info(Logs.fileline() + ' : TRACE AnalysisDet ERROR insert link var to analysis')
                        return compose_ret('', Constants.cst_content_type_json, 500)

                else:
                    # insert new variable
                    ret = Analysis.insertAnalysisVar(id_owner=args['id_owner'],
                                                     label=var['var_label'],
                                                     code_var=var['var_code'],
                                                     descr=var['var_descr'],
                                                     type_res=var['var_type_res'],
                                                     var_min=var['var_min'],
                                                     var_max=var['var_max'],
                                                     comment=var['var_comment'],
                                                     formula=var['var_formula'],
                                                     unit=var['var_unit'],
                                                     accu=var['var_accu'],
                                                     formula2=var['var_formula2'],
                                                     unit2=var['var_unit2'],
                                                     accu2=var['var_accu2'])

                    if ret is False:
                        self.log.info(Logs.fileline() + ' : TRACE AnalysisDet ERROR insert var analysis')
                        return compose_ret('', Constants.cst_content_type_json, 500)

                    id_var = ret

                    # link variable
                    ret = Analysis.insertRefVariable(id_owner=args['id_owner'],
                                                     id_refana=id_ana,
                                                     id_refvar=id_var,
                                                     var_pos=var['var_pos'],
                                                     var_num=var['var_num'],
                                                     oblig=var['var_oblig'],
                                                     var_whonet=var['var_whonet'])

                    if ret <= 0:
                        self.log.info(Logs.fileline() + ' : TRACE AnalysisDet ERROR insert link var to analysis')
                        return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE AnalysisDet id_ana=' + str(id_ana))
        return compose_ret('', Constants.cst_content_type_json)

    def delete(self, id_ana):
        ret = Analysis.deleteAnalysis(id_ana)

        if not ret:
            self.log.error(Logs.fileline() + ' : TRACE AnalysisDet delete ERROR')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE AnalysisDet delete id_item=' + str(id_ana))
        return compose_ret('', Constants.cst_content_type_json)


class AnalysisVarList(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_ana):
        l_vars = Analysis.getListVariable(id_ana)

        if not l_vars:
            self.log.error(Logs.fileline() + ' : ' + 'AnalysisVarList ERROR not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        for var in l_vars:
            # Replace None by empty string
            for key, value in list(var.items()):
                if var[key] is None:
                    var[key] = ''

        self.log.info(Logs.fileline() + ' : AnalysisVarList id_data=' + str(id_ana))
        return compose_ret(l_vars, Constants.cst_content_type_json, 200)


class AnalysisVarDet(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_var):
        ana_var = Analysis.getAnalysisVar(id_var)

        if not ana_var:
            self.log.error(Logs.fileline() + ' : ' + 'AnalysisVarDet ERROR not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        # Replace None by empty string
        for key, value in list(ana_var.items()):
            if ana_var[key] is None:
                ana_var[key] = ''

        self.log.info(Logs.fileline() + ' : AnalysisVarDet id_data=' + str(id_var))
        return compose_ret(ana_var, Constants.cst_content_type_json, 200)


class AnalysisTypeProd(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_type_prod):
        type_prod = Analysis.getProductType(id_type_prod)

        if not type_prod:
            self.log.error(Logs.fileline() + ' : ' + 'AnalysisTypeProd ERROR not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        # Replace None by empty string
        for key, value in list(type_prod.items()):
            if type_prod[key] is None:
                type_prod[key] = ''

        self.log.info(Logs.fileline() + ' : AnalysistypeProd id_type_prod' + str(id_type_prod))
        return compose_ret(type_prod, Constants.cst_content_type_json, 200)


class AnalysisReq(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_rec, type_ana='A'):
        l_ana = Analysis.getAnalysisReq(id_rec, type_ana)

        if not l_ana:
            self.log.error(Logs.fileline() + ' : ' + 'AnalysisReq ERROR not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        for analysis in l_ana:
            # Replace None by empty string
            for key, value in list(analysis.items()):
                if analysis[key] is None:
                    analysis[key] = ''

            if analysis['prix'] != '':
                analysis['prix'] = float(analysis['prix'])

        self.log.info(Logs.fileline() + ' : AnalysisReq id_rec=' + str(id_rec))
        return compose_ret(l_ana, Constants.cst_content_type_json, 200)

    def post(self):
        args = request.get_json()

        if 'list_ana' not in args:
            self.log.error(Logs.fileline() + ' : AnalysisReq ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # Loop on list_ana
        for ana in args['list_ana']:

            if 'id_owner' not in ana or 'id_rec' not in ana or 'id_ana' not in ana or 'price' not in ana or \
               'paid' not in ana or 'emer' not in ana or 'req' not in ana:
                self.log.error(Logs.fileline() + ' : AnalysisReq ERROR ana missing')
                return compose_ret('', Constants.cst_content_type_json, 400)

            ret = Analysis.insertAnalysisReq(id_owner=ana['id_owner'],
                                             id_dos=ana['id_rec'],
                                             ref_analyse=ana['id_ana'],
                                             prix=ana['price'],
                                             paye=ana['paid'],
                                             urgent=ana['emer'],
                                             demande=ana['req'])

            if ret <= 0:
                self.log.error(Logs.alert() + ' : AnalysisReq ERROR  insert')
                return compose_ret('', Constants.cst_content_type_json, 500)

            res = {}
            res['id_req'] = ret

        self.log.info(Logs.fileline() + ' : TRACE AnalysisReq')
        return compose_ret('', Constants.cst_content_type_json)


class AnalysisExport(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        l_data = [['id_data', 'id_owner', 'code', 'nom', 'abbr', 'famille', 'paillasse', 'cote_unite', 'cote_valeur',
                   'commentaire', 'produit_biologique', 'type_prel', 'type_analyse', 'actif', 'ana_whonet', 'id_link',
                   'id_refanalyse', 'id_refvariable', 'position', 'num_var', 'obligatoire', 'id_var', 'libelle',
                   'description', 'unite', 'normal_min', 'normal_max', 'var_comm', 'type_resultat', 'unite2',
                   'formule_unite2', 'formule', 'accuracy', 'precision2', 'version', 'code_var', 'var_whonet']]

        if 'id_user' not in args:
            self.log.error(Logs.fileline() + ' : AnalysisExport ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        dict_data = Analysis.getAnalysisExport()

        if dict_data:
            for d in dict_data:
                data = []

                # ANALYSIS
                if d['id_data']:
                    data.append(d['id_data'])
                else:
                    data.append('')

                if d['id_owner']:
                    data.append(d['id_owner'])
                else:
                    data.append('')

                if d['code']:
                    data.append(d['code'])
                else:
                    data.append('')

                if d['nom']:
                    data.append(d['nom'])
                else:
                    data.append('')

                if d['abbr']:
                    data.append(d['abbr'])
                else:
                    data.append('')

                if d['famille']:
                    data.append(d['famille'])
                else:
                    data.append('')

                if d['paillasse']:
                    data.append(d['paillasse'])
                else:
                    data.append('')

                if d['cote_unite']:
                    data.append(d['cote_unite'])
                else:
                    data.append('')

                if d['cote_valeur']:
                    data.append(d['cote_valeur'])
                else:
                    data.append('')

                if d['commentaire']:
                    data.append(d['commentaire'])
                else:
                    data.append('')

                if d['produit_biologique']:
                    data.append(d['produit_biologique'])
                else:
                    data.append('')

                if d['type_prel']:
                    data.append(d['type_prel'])
                else:
                    data.append('')

                if d['type_analyse']:
                    data.append(d['type_analyse'])
                else:
                    data.append('')

                if d['actif']:
                    data.append(d['actif'])
                else:
                    data.append('')

                if d['ana_whonet']:
                    data.append(d['ana_whonet'])
                else:
                    data.append('')

                # LINK
                if d['id_link']:
                    data.append(d['id_link'])
                else:
                    data.append('')

                if d['id_refanalyse']:
                    data.append(d['id_refanalyse'])
                else:
                    data.append('')

                if d['id_refvariable']:
                    data.append(d['id_refvariable'])
                else:
                    data.append('')

                if d['position']:
                    data.append(d['position'])
                else:
                    data.append('')

                if d['num_var']:
                    data.append(d['num_var'])
                else:
                    data.append('')

                if d['obligatoire']:
                    data.append(d['obligatoire'])
                else:
                    data.append('')

                # VARIABLE
                if d['id_var']:
                    data.append(d['id_var'])
                else:
                    data.append('')

                if d['libelle']:
                    data.append(d['libelle'])
                else:
                    data.append('')

                if d['description']:
                    data.append(d['description'])
                else:
                    data.append('')

                if d['unite']:
                    data.append(d['unite'])
                else:
                    data.append('')

                if d['normal_min']:
                    data.append(d['normal_min'])
                else:
                    data.append('')

                if d['normal_max']:
                    data.append(d['normal_max'])
                else:
                    data.append('')

                if d['commentaire']:
                    data.append(d['commentaire'])
                else:
                    data.append('')

                if d['type_resultat']:
                    data.append(d['type_resultat'])
                else:
                    data.append('')

                if d['unite2']:
                    data.append(d['unite2'])
                else:
                    data.append('')

                if d['formule_unite2']:
                    data.append(d['formule_unite2'])
                else:
                    data.append('')

                if d['formule']:
                    data.append(d['formule'])
                else:
                    data.append('')

                if d['accuracy']:
                    data.append(d['accuracy'])
                else:
                    data.append('')

                if d['precision2']:
                    data.append(d['precision2'])
                else:
                    data.append('')

                data.append('v1')

                if d['code_var']:
                    data.append(d['code_var'])
                else:
                    data.append('')

                if d['var_whonet']:
                    data.append(d['var_whonet'])
                else:
                    data.append('')

                l_data.append(data)

        # if no result to export
        if len(l_data) < 2:
            return compose_ret('', Constants.cst_content_type_json, 404)

        # write csv file
        try:
            import csv

            today = datetime.now().strftime("%Y%m%d")

            filename = 'analyzes_' + str(today) + '.csv'

            with open('tmp/' + filename, mode='w', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=';')
                for line in l_data:
                    writer.writerow(line)

        except Exception as err:
            self.log.error(Logs.fileline() + ' : post AnalysisExport failed, err=%s', err)
            return False

        self.log.info(Logs.fileline() + ' : TRACE AnalysisExport')
        return compose_ret('', Constants.cst_content_type_json)


class AnalysisImport(Resource):
    log = logging.getLogger('log_services')

    def get(self, filename, type, id_user):

        if not filename or not type or id_user <= 0:
            self.log.error(Logs.fileline() + ' : AnalysisImport ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # Read CSV user
        import os

        from csv import reader

        path = Constants.cst_path_tmp

        with open(os.path.join(path, filename), 'r', encoding='utf-8') as csv_file:
            csv_reader = reader(csv_file, delimiter=';')
            l_rows = list(csv_reader)

        if not l_rows or len(l_rows) < 2:
            self.log.error(Logs.fileline() + ' : TRACE AnalysisImport ERROR file empty')
            return compose_ret('', Constants.cst_content_type_json, 500)

        # remove headers line
        l_rows.pop(0)

        # check version
        if l_rows[0][34] != 'v1':
            self.log.error(Logs.fileline() + ' : TRACE AnalysisImport ERROR wrong version')
            return compose_ret('', Constants.cst_content_type_json, 409)

        # check number of column (dont forget version columns)
        if len(l_rows[0]) != 35:
            self.log.error(Logs.fileline() + ' : TRACE AnalysisImport ERROR wrong number of column')
            return compose_ret('', Constants.cst_content_type_json, 409)

        # UPDATE MODE
        if type == 'U':
            code_prev = ''

            for l in l_rows:
                if l:
                    id_ana             = l[0]
                    id_owner           = l[1]
                    code               = l[2]
                    nom                = l[3]
                    abbr               = l[4]
                    famille            = l[5]
                    # paillasse          = l[6]   # useless
                    cote_unite         = l[7]
                    cote_valeur        = l[8]
                    commentaire        = l[9]
                    produit_biologique = l[10]
                    type_prel          = l[11]
                    # type_analyse       = l[12]  # useless
                    actif              = l[13]
                    ana_whonet         = l[14]

                    id_link            = l[15]
                    # id_refanalyse      = l[16]
                    id_refvariable     = l[17]
                    position           = l[18]
                    num_var            = l[19]
                    obligatoire        = l[20]

                    id_var             = l[21]
                    libelle            = l[22]
                    description        = l[23]
                    unite              = l[24]
                    normal_min         = l[25]
                    normal_max         = l[26]
                    var_comm           = l[27]
                    type_resultat      = l[28]
                    unite2             = l[29]
                    formule_unite2     = l[30]
                    formule            = l[31]
                    accuracy           = l[32]
                    precision2         = l[33]

                    code_var           = l[35]
                    var_whonet         = l[36]

                    ret = Analysis.exist(code)

                    if ret == -1:
                        self.log.info(Logs.fileline() + ' : TRACE AnalysisImport ERROR sql')
                        return compose_ret('', Constants.cst_content_type_json, 500)

                    # same analysis
                    if ret:
                        # next analysis
                        if code != code_prev:
                            # update analysis
                            ret = Analysis.updateAnalysis(id_data=id_ana,
                                                          id_owner=id_owner,
                                                          code=code,
                                                          name=nom,
                                                          abbr=abbr,
                                                          type_ana=famille,
                                                          type_prod=type_prel,
                                                          unit=cote_unite,
                                                          value=cote_valeur,
                                                          stat=actif,
                                                          comment=commentaire,
                                                          product=produit_biologique,
                                                          whonet=ana_whonet)

                            if ret is False:
                                self.log.info(Logs.fileline() + ' : TRACE AnalysisImport ERROR update analysis')
                                return compose_ret('', Constants.cst_content_type_json, 500)

                            code_prev = code

                        # Get list of link
                        l_link = Analysis.getListVariable(id_ana)

                        for link in l_link:
                            if link['id_data'] == id_refvariable:
                                # UPDATE VAR
                                ret = Analysis.updateAnalysisVar(id_data=id_var,
                                                                 id_owner=id_owner,
                                                                 label=libelle,
                                                                 code_var=code_var,
                                                                 descr=description,
                                                                 type_res=type_resultat,
                                                                 var_min=normal_min,
                                                                 var_max=normal_max,
                                                                 comment=var_comm,
                                                                 formula=formule,
                                                                 unit=unite,
                                                                 accu=accuracy,
                                                                 formula2=formule_unite2,
                                                                 unit2=unite2,
                                                                 accu2=precision2)

                                if ret is False:
                                    self.log.info(Logs.fileline() + ' : TRACE AnalysisImport ERROR update var analysis')
                                    return compose_ret('', Constants.cst_content_type_json, 500)

                                # UPDATE LINK
                                ret = Analysis.updateRefVariable(id_data=id_link,
                                                                 id_owner=id_owner,
                                                                 id_refana=id_ana,
                                                                 id_refvar=id_var,
                                                                 var_pos=position,
                                                                 var_num=num_var,
                                                                 oblig=obligatoire,
                                                                 var_whonet=var_whonet)

                                if not ret:
                                    self.log.info(Logs.fileline() + ' : TRACE AnalysisImport ERROR update link var to analysis')
                                    return compose_ret('', Constants.cst_content_type_json, 500)

        # ADD MODE
        elif type == 'A':
            code_prev = ''

            for l in l_rows:
                if l:
                    id_ana             = l[0]
                    id_owner           = l[1]
                    code               = l[2]
                    nom                = l[3]
                    abbr               = l[4]
                    famille            = l[5]
                    # paillasse          = l[6]   # useless
                    cote_unite         = l[7]
                    cote_valeur        = l[8]
                    commentaire        = l[9]
                    produit_biologique = l[10]
                    type_prel          = l[11]
                    # type_analyse       = l[12]  # useless
                    actif              = l[13]
                    ana_whonet         = l[14]

                    id_link            = l[15]
                    # id_refanalyse      = l[16]
                    id_refvariable     = l[17]
                    position           = l[18]
                    num_var            = l[19]
                    obligatoire        = l[20]

                    id_var             = l[21]
                    libelle            = l[22]
                    description        = l[23]
                    unite              = l[24]
                    normal_min         = l[25]
                    normal_max         = l[26]
                    var_comm           = l[27]
                    type_resultat      = l[28]
                    unite2             = l[29]
                    formule_unite2     = l[30]
                    formule            = l[31]
                    accuracy           = l[32]
                    precision2         = l[33]
                    code_var           = l[34]
                    var_whonet         = l[35]

                    ret = Analysis.exist(code)

                    if ret == -1:
                        self.log.info(Logs.fileline() + ' : TRACE AnalysisImport ERROR sql')
                        return compose_ret('', Constants.cst_content_type_json, 500)

                    # New analysis code or same analysis after insert
                    if not ret or code == code_prev:
                        # different analysis
                        if code != code_prev:
                            # check if id_data is available
                            ret = Analysis.freeIdAna(id_ana)

                            if ret == -1:
                                self.log.info(Logs.fileline() + ' : TRACE AnalysisImport ERROR sql')
                                return compose_ret('', Constants.cst_content_type_json, 500)

                            if ret:
                                id_data = id_ana
                            else:
                                id_data = 0

                            # insert analysis
                            ret = Analysis.insertAnalysis(id_owner=id_owner,
                                                          code=code,
                                                          name=nom,
                                                          abbr=abbr,
                                                          type_ana=famille,
                                                          type_prod=type_prel,
                                                          unit=cote_unite,
                                                          value=cote_valeur,
                                                          stat=actif,
                                                          comment=commentaire,
                                                          product=produit_biologique,
                                                          whonet=ana_whonet,
                                                          id_data=id_data)

                            if ret <= 0:
                                self.log.info(Logs.fileline() + ' : TRACE AnalysisImport ERROR insert analysis')
                                return compose_ret('', Constants.cst_content_type_json, 500)

                            id_ana = ret

                            code_prev = code

                        # get same variable from these criteria
                        var = Analysis.getAnalysisVar(libelle, type_resultat, unite, accuracy, normal_min, normal_max)

                        if var:
                            id_var = var['id_data']
                        else:
                            # INSERT UNKNOW VAR
                            ret = Analysis.insertAnalysisVar(id_owner=id_owner,
                                                             label=libelle,
                                                             code_var=code_var,
                                                             descr=description,
                                                             type_res=type_resultat,
                                                             var_min=normal_min,
                                                             var_max=normal_max,
                                                             comment=var_comm,
                                                             formula=formule,
                                                             unit=unite,
                                                             accu=accuracy,
                                                             formula2=formule_unite2,
                                                             unit2=unite2,
                                                             accu2=precision2)

                            if ret is False:
                                self.log.info(Logs.fileline() + ' : AnalysisImport ERROR insert var analysis')
                                return compose_ret('', Constants.cst_content_type_json, 500)

                            id_var = ret

                        # INSERT NEW LINK
                        ret = Analysis.insertRefVariable(id_owner=id_owner,
                                                         id_refana=id_ana,
                                                         id_refvar=id_var,
                                                         var_pos=position,
                                                         var_num=num_var,
                                                         oblig=obligatoire,
                                                         var_whonet=var_whonet)

                        if ret <= 0:
                            self.log.info(Logs.fileline() + ' : AnalysisImport ERROR insert link var to analysis')
                            return compose_ret('', Constants.cst_content_type_json, 500)

        else:
            self.log.error(Logs.fileline() + ' : TRACE AnalysisImport ERROR wrong type')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE AnalysisImport')
        return compose_ret('', Constants.cst_content_type_json, 200)
