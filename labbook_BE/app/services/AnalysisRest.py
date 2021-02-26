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

    def post(self, id_group):
        args = request.get_json()

        id_lab = User.getUserGroupParent(id_group)

        l_analysis = Analysis.getAnalysisSearch(args['term'], id_lab['id_group_parent'], id_group)

        if not l_analysis:
            self.log.error(Logs.fileline() + ' : TRACE AnalysisSearch not found')

        self.log.info(Logs.fileline() + ' : TRACE AnalysisSearch')
        return compose_ret(l_analysis, Constants.cst_content_type_json)


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

        self.log.info(Logs.fileline() + ' : TRACE AnalysisHistoDet')
        return compose_ret(l_datas, Constants.cst_content_type_json)


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

            # Get id_group of lab with id_group of user
            id_group_lab = User.getUserGroupParent(ana['id_owner'])

            if not id_group_lab:
                self.log.error(Logs.fileline() + ' : AnalysisReq ERROR group not found')
                return compose_ret('', Constants.cst_content_type_json, 500)

            # insert sigl_04_data_group
            ret = Analysis.insertAnalysisReqGroup(id_data=res['id_req'],
                                                  id_group=id_group_lab['id_group_parent'])

            if ret <= 0:
                self.log.error(Logs.alert() + ' : AnalysisReq ERROR  insert group')
                return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE AnalysisReq')
        return compose_ret('', Constants.cst_content_type_json)
