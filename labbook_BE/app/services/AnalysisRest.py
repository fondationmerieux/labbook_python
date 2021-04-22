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
            for key, value in analysis.items():
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

            with open('tmp/' + filename, mode='w') as file:
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
            for key, value in analysis.items():
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
            for key, value in data.items():
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
        ret = Analysis.checkCodeAnalysis(code)

        if not ret:
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
        for key, value in analysis.items():
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

            for var in args['list_var']:
                if var['id_var'] > 0:
                    # update variable which already exist
                    ret = Analysis.updateAnalysisVar(id_data=var['id_var'],
                                                     id_owner=args['id_owner'],
                                                     label=var['var_label'],
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
                                                         oblig=var['var_oblig'])

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
                                                         oblig=var['var_oblig'])

                        if ret <= 0:
                            self.log.info(Logs.fileline() + ' : TRACE AnalysisDet ERROR update link var to analysis')
                            return compose_ret('', Constants.cst_content_type_json, 500)

                else:
                    # insert new variable
                    ret = Analysis.insertAnalysisVar(id_owner=args['id_owner'],
                                                     label=var['var_label'],
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
                                                     oblig=var['var_oblig'])

                    if ret <= 0:
                        self.log.info(Logs.fileline() + ' : TRACE AnalysisDet ERROR insert link var to analysis')
                        return compose_ret('', Constants.cst_content_type_json, 500)

            # delete missing link to variable compared to analysis
            db_l_var = Analysis.getListVariable(id_ana)

            for db_var in db_l_var:
                exist = False
                for ihm_var in args['list_var']:
                    if db_var['id_data'] == ihm_var['id_var']:
                        exist = True

                if not exist:
                    ret = Analysis.deleteRefVar(db_var['id_data'])

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
                                                     oblig=var['var_oblig'])

                    if ret <= 0:
                        self.log.info(Logs.fileline() + ' : TRACE AnalysisDet ERROR insert link var to analysis')
                        return compose_ret('', Constants.cst_content_type_json, 500)

                else:
                    # insert new variable
                    ret = Analysis.insertAnalysisVar(id_owner=args['id_owner'],
                                                     label=var['var_label'],
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
                                                     oblig=var['var_oblig'])

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
            for key, value in var.items():
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
        for key, value in ana_var.items():
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
        for key, value in type_prod.items():
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
            for key, value in analysis.items():
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
