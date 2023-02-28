# -*- coding:utf-8 -*-
import logging
import gettext

from datetime import datetime
from flask import request
from flask_restful import Resource

from app.models.General import compose_ret
from app.models.Constants import *
from app.models.Analysis import *
from app.models.User import *
from app.models.DB import *
from app.models.Logs import Logs
from app.models.Various import Various


class AnalysisSearch(Resource):
    log = logging.getLogger('log_services')

    def post(self, type):
        args = request.get_json()

        if 'status' in args and args['status']:
            status = args['status']
        else:
            status = 4

        if 'link_fam' in args and args['link_fam']:
            link_fam = args['link_fam']
        else:
            link_fam = []

        l_analysis = Analysis.getAnalysisSearch(args['term'], type, status, link_fam)

        if not l_analysis:
            self.log.error(Logs.fileline() + ' : TRACE AnalysisSearch not found')

        # TRANSLATION
        Various.useLangDB()
        for analysis in l_analysis:
            ana_name  = analysis['name']
            ana_label = analysis['label']

            if ana_name:
                analysis['name'] = _(ana_name.strip())
            else:
                analysis['name'] = ''

            if ana_label:
                analysis['label'] = _(ana_label.strip())
            else:
                analysis['label'] = ''

        self.log.info(Logs.fileline() + ' : TRACE AnalysisSearch')
        return compose_ret(l_analysis, Constants.cst_content_type_json)


class AnalysisVarSearch(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        l_vars = Analysis.getAnalysisVarSearch(args['term'])

        if not l_vars:
            self.log.error(Logs.fileline() + ' : TRACE AnalysisVarSearch not found')

        # TRANSLATION
        Various.useLangDB()
        for var in l_vars:
            var_libel = var['field_value']

            if var_libel:
                var['field_value'] = _(var_libel.strip())
            else:
                var['field_value'] = ''

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

        Various.useLangDB()

        for analysis in l_analyzes:
            # Replace None by empty string
            for key, value in list(analysis.items()):
                if analysis[key] is None:
                    analysis[key] = ''
                elif key == 'name' and analysis[key]:
                    analysis[key] = _(analysis[key].strip())
                elif key == 'type_ana' and analysis[key]:
                    analysis[key] = _(analysis[key].strip())
                elif key == 'product' and analysis[key]:
                    analysis[key] = _(analysis[key].strip())

        self.log.info(Logs.fileline() + ' : TRACE AnalysisList')
        return compose_ret(l_analyzes, Constants.cst_content_type_json)


class AnalysisHistoExport(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        l_data = [['id_data', 'code', 'fam_name', 'name', 'nb_ana']]

        if 'date_beg' not in args or 'date_end' not in args:
            self.log.error(Logs.fileline() + ' : AnalysisHistoExport ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        args['limit'] = 50000  # for overpassed default limit

        l_analyzes = Analysis.getAnalyzesHistoList(args)

        Various.useLangDB()

        for analysis in l_analyzes:
            # Replace None by empty string
            for key, value in list(analysis.items()):
                if analysis[key] is None:
                    analysis[key] = ''
                elif key == 'fam_name' and analysis[key]:
                    analysis[key] = _(analysis[key].strip())
                elif key == 'name' and analysis[key]:
                    analysis[key] = _(analysis[key].strip())

            nb_ana = Analysis.getNbAnalysis(args['date_beg'], args['date_end'], analysis['id_data'])

            if nb_ana:
                analysis['nb_ana'] = nb_ana['total']
            else:
                analysis['nb_ana'] = 0

            data = []

            data.append(analysis['id_data'])
            data.append(analysis['code'])
            data.append(analysis['fam_name'])
            data.append(analysis['name'])

            data.append(analysis['nb_ana'])

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

        Various.useLangDB()

        for analysis in l_analyzes:
            # Replace None by empty string
            for key, value in list(analysis.items()):
                if analysis[key] is None:
                    analysis[key] = ''
                elif key == 'fam_name':
                    analysis[key] = _(analysis[key].strip())
                elif key == 'name':
                    analysis[key] = _(analysis[key].strip())

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

        Various.useLangDB()

        for data in l_datas:
            # Replace None by empty string
            for key, value in list(data.items()):
                if data[key] is None:
                    data[key] = ''
                elif key == 'variable' and data[key]:
                    data[key] = _(data[key].strip())
                elif key == 'result' and data[key]:
                    data[key] = _(data[key].strip())

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

        Various.useLangDB()

        # Replace None by empty string
        for key, value in list(analysis.items()):
            if analysis[key] is None:
                analysis[key] = ''
            elif key == 'nom' and analysis[key]:
                analysis[key] = _(analysis[key].strip())

        if analysis['cote_valeur']:
            analysis['cote_valeur'] = float(analysis['cote_valeur'])
        else:
            analysis['cote_valeur'] = 0

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

            if args['value'] == '':
                args['value'] = 0

            # update analysis
            ret = Analysis.updateAnalysis(id_data=id_ana,
                                          id_owner=args['id_owner'],
                                          code=args['code'],
                                          name=args['name'],
                                          abbr=args['abbr'],
                                          type_ana=args['type_ana'],
                                          type_prod=args['type_prod'],
                                          unit=args['unit'],
                                          value=float(args['value']),
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
                                                     var_highlight=var['var_highlight'],
                                                     comment=var['var_comment'],
                                                     formula=var['var_formula'],
                                                     unit=var['var_unit'],
                                                     accu=var['var_accu'],
                                                     formula2='',  # var['var_formula2'],
                                                     unit2=0,      # var['var_unit2'],
                                                     accu2=0)      # var['var_accu2'])

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
                                                         var_whonet=var['var_whonet'],
                                                         var_qrcode=var['var_qrcode'])

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
                                                         var_whonet=var['var_whonet'],
                                                         var_qrcode=var['var_qrcode'])

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
                                                     var_highlight=var['var_highlight'],
                                                     comment=var['var_comment'],
                                                     formula=var['var_formula'],
                                                     unit=var['var_unit'],
                                                     accu=var['var_accu'],
                                                     formula2='',  # var['var_formula2'],
                                                     unit2=0,      # var['var_unit2'],
                                                     accu2=0)      # var['var_accu2'])

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
                                                     var_whonet=var['var_whonet'],
                                                     var_qrcode=var['var_qrcode'])

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
                                                     formula2='',  # var['var_formula2'],
                                                     unit2=0,      # var['var_unit2'],
                                                     accu2=0)      # var['var_accu2'])

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
                                                     var_whonet=var['var_whonet'],
                                                     var_qrcode=var['var_qrcode'])

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
                                                     var_highlight=var['var_highlight'],
                                                     comment=var['var_comment'],
                                                     formula=var['var_formula'],
                                                     unit=var['var_unit'],
                                                     accu=var['var_accu'],
                                                     formula2='',  # var['var_formula2'],
                                                     unit2=0,      # var['var_unit2'],
                                                     accu2=0)      # var['var_accu2'])

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
                                                     var_whonet=var['var_whonet'],
                                                     var_qrcode=var['var_qrcode'])

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


class AnalysisVarAll(Resource):
    log = logging.getLogger('log_services')

    def get(self):
        l_vars = Analysis.getAllVariable()

        if not l_vars:
            self.log.error(Logs.fileline() + ' : ' + 'AnalysisVarAll ERROR not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        Various.useLangDB()

        for var in l_vars:
            # Replace None by empty string
            for key, value in list(var.items()):
                if var[key] is None:
                    var[key] = ''
                elif key == 'label' and var[key]:
                    var[key] = _(var[key].strip())
                elif key == 'comment' and var[key]:
                    var[key] = _(var[key].strip())

                nb = Analysis.getNbAnaByVar(var['id_item'])

                if nb:
                    var['nb_link'] = nb['nb_link']
                else:
                    var['nb_link'] = 0

        self.log.info(Logs.fileline() + ' : AnalysisVarAlll')
        return compose_ret(l_vars, Constants.cst_content_type_json, 200)


class AnalysisVarList(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_ana):
        l_vars = Analysis.getListVariable(id_ana)

        if not l_vars:
            self.log.error(Logs.fileline() + ' : ' + 'AnalysisVarList ERROR not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        Various.useLangDB()

        for var in l_vars:
            # Replace None by empty string
            for key, value in list(var.items()):
                if var[key] is None:
                    var[key] = ''
                elif key == 'label' and var[key]:
                    var[key] = _(var[key].strip())
                elif key == 'comment' and var[key]:
                    var[key] = _(var[key].strip())

        self.log.info(Logs.fileline() + ' : AnalysisVarList id_data=' + str(id_ana))
        return compose_ret(l_vars, Constants.cst_content_type_json, 200)


class AnalysisVarDet(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_var):
        ana_var = Analysis.getAnalysisVar(id_var)

        if not ana_var:
            self.log.error(Logs.fileline() + ' : ' + 'AnalysisVarDet ERROR not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        Various.useLangDB()

        # Replace None by empty string
        for key, value in list(ana_var.items()):
            if ana_var[key] is None:
                ana_var[key] = ''
            elif key == 'label' and ana_var[key]:
                ana_var[key] = _(ana_var[key].strip())
            elif key == 'comment' and ana_var[key]:
                ana_var[key] = _(ana_var[key].strip())

        self.log.info(Logs.fileline() + ' : AnalysisVarDet id_data=' + str(id_var))
        return compose_ret(ana_var, Constants.cst_content_type_json, 200)


class AnalysisTypeProd(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_type_prod):
        type_prod = Analysis.getProductType(id_type_prod)

        if not type_prod:
            self.log.error(Logs.fileline() + ' : ' + 'AnalysisTypeProd ERROR not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        Various.useLangDB()

        # Replace None by empty string
        for key, value in list(type_prod.items()):
            if type_prod[key] is None:
                type_prod[key] = ''
            elif key == 'label' and type_prod[key]:
                type_prod[key] = _(type_prod[key].strip())

        self.log.info(Logs.fileline() + ' : AnalysistypeProd id_type_prod' + str(id_type_prod))
        return compose_ret(type_prod, Constants.cst_content_type_json, 200)


class AnalysisReq(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_rec, type_ana='A'):
        l_ana = Analysis.getAnalysisReq(id_rec, type_ana)

        if not l_ana:
            self.log.error(Logs.fileline() + ' : ' + 'AnalysisReq ERROR not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        Various.useLangDB()

        for analysis in l_ana:
            # Replace None by empty string
            for key, value in list(analysis.items()):
                if analysis[key] is None:
                    analysis[key] = ''
                elif key == 'nom' and analysis[key]:
                    analysis[key] = _(analysis[key].strip())

            if analysis['prix']:
                analysis['prix'] = float(analysis['prix'])
            else:
                analysis['prix'] = 0

            if analysis['cote_valeur']:
                analysis['cote_valeur'] = float(analysis['cote_valeur'])
            else:
                analysis['cote_valeur'] = 0

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
               'paid' not in ana or 'emer' not in ana or 'req' not in ana or 'outsourced' not in ana:
                self.log.error(Logs.fileline() + ' : AnalysisReq ERROR ana missing')
                return compose_ret('', Constants.cst_content_type_json, 400)

            ret = Analysis.insertAnalysisReq(id_owner=ana['id_owner'],
                                             id_dos=ana['id_rec'],
                                             ref_analyse=ana['id_ana'],
                                             prix=ana['price'],
                                             paye=ana['paid'],
                                             urgent=ana['emer'],
                                             demande=ana['req'],
                                             outsourced=ana['outsourced'])

            if ret <= 0:
                self.log.error(Logs.alert() + ' : AnalysisReq ERROR  insert')
                return compose_ret('', Constants.cst_content_type_json, 500)

            res = {}
            res['id_req'] = ret

        self.log.info(Logs.fileline() + ' : TRACE AnalysisReq')
        return compose_ret('', Constants.cst_content_type_json)

    def delete(self, id_req):
        args = request.get_json()

        if 'id_rec' not in args or 'id_samp_act' not in args or 'type_samp' not in args:
            self.log.error(Logs.fileline() + ' : AnalysisReq ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        ret = Analysis.deleteAnalysisReq(id_req, args['id_rec'], args['id_samp_act'], args['type_samp'])

        if not ret:
            self.log.error(Logs.fileline() + ' : TRACE AnalysisReq delete ERROR')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE AnalysisReq delete id_item=' + str(id_req))
        return compose_ret('', Constants.cst_content_type_json)


class AnalysisExport(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        l_data = [['version', 'id_ana', 'id_owner', 'ana_code', 'ana_name', 'ana_abbr', 'ana_family', 'ana_unit_rating',
                   'ana_value_rating', 'ana_comment', 'ana_bio_product', 'ana_sample_type', 'ana_type', 'ana_active',
                   'ana_whonet', 'id_link', 'link_ana_ref', 'link_var_ref', 'link_pos', 'link_num_var', 'link_oblig',
                   'id_var', 'var_label', 'var_descr', 'var_unit', 'var_min', 'var_max', 'var_comment', 'var_res_type',
                   'var_formula', 'var_accu', 'var_code', 'var_whonet', 'var_qrcode', 'var_highlight']]

        if 'id_user' not in args:
            self.log.error(Logs.fileline() + ' : AnalysisExport ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        Various.useLangDB()

        dict_data = Analysis.getAnalysisExport()

        if dict_data:
            for d in dict_data:
                data = []

                data.append('v3')

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
                    nom = d['nom']
                    data.append(_(nom.strip()))
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

                if d['cote_unite']:
                    data.append(d['cote_unite'])
                else:
                    data.append('')

                if d['cote_valeur']:
                    data.append(float(d['cote_valeur']))
                else:
                    data.append('0')

                if d['commentaire']:
                    comment = d['commentaire']
                    data.append(_(comment.strip()))
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
                    if d['actif'] == 4:
                        data.append('Y')
                    else:
                        data.append('N')
                else:
                    data.append('')

                if d['ana_whonet']:
                    if d['ana_whonet'] == 4:
                        data.append('Y')
                    else:
                        data.append('N')
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
                    if d['obligatoire'] == 4:
                        data.append('Y')
                    else:
                        data.append('N')
                else:
                    data.append('')

                # VARIABLE
                if d['id_var']:
                    data.append(d['id_var'])
                else:
                    data.append('')

                if d['libelle']:
                    libel = d['libelle']
                    data.append(_(libel.strip()))
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
                    comment = d['commentaire']
                    data.append(_(comment.strip()))
                else:
                    data.append('')

                if d['type_resultat']:
                    data.append(d['type_resultat'])
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

                if d['code_var']:
                    data.append(d['code_var'])
                else:
                    data.append('')

                if d['var_whonet']:
                    if d['var_whonet'] == 4:
                        data.append('Y')
                    else:
                        data.append('N')
                else:
                    data.append('')

                if d['var_qrcode']:
                    data.append(d['var_qrcode'])
                else:
                    data.append('N')

                if d['var_highlight']:
                    data.append(d['var_highlight'])
                else:
                    data.append('N')

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
            DB.insertDbStatus(stat='ERR;AnalysisImport ERROR file empty', type='ANA')
            return compose_ret('', Constants.cst_content_type_json, 500)

        head_line = l_rows[0]

        # remove headers line
        l_rows.pop(0)

        # check version
        if l_rows[0][0] != 'v3':
            self.log.error(Logs.fileline() + ' : TRACE AnalysisImport ERROR wrong version')
            DB.insertDbStatus(stat='ERR;AnalysisImport ERROR wrong version', type='ANA')
            return compose_ret('', Constants.cst_content_type_json, 409)

        # check name of column
        head_list = ['version', 'id_ana', 'id_owner', 'ana_code', 'ana_name', 'ana_abbr', 'ana_family', 'ana_unit_rating',
                     'ana_value_rating', 'ana_comment', 'ana_bio_product', 'ana_sample_type', 'ana_type', 'ana_active',
                     'ana_whonet', 'id_link', 'link_ana_ref', 'link_var_ref', 'link_pos', 'link_num_var', 'link_oblig',
                     'id_var', 'var_label', 'var_descr', 'var_unit', 'var_min', 'var_max', 'var_comment', 'var_res_type',
                     'var_formula', 'var_accu', 'var_code', 'var_whonet', 'var_qrcode', 'var_highlight']

        i = 0
        for head in head_line:
            if head != head_list[i]:
                self.log.error(Logs.fileline() + ' : TRACE AnalysisImport ERROR wrong column or order : ' + str(head))
                DB.insertDbStatus(stat='ERR;AnalysisImport ERROR wrong column or order : ' + str(head), type='ANA')
                return compose_ret('', Constants.cst_content_type_json, 409)
            i = i + 1

        # UPDATE MODE
        if type == 'U':
            code_prev = ''

            i = 1
            for row in l_rows:
                i = i + 1
                if row:
                    id_ana             = row[1]
                    id_owner           = row[2]
                    code               = row[3]
                    nom                = row[4]
                    abbr               = row[5]
                    famille            = row[6]
                    cote_unite         = row[7]

                    if row[8]:
                        cote_valeur = float(row[8])
                    else:
                        cote_valeur = 0
                    commentaire        = row[9]
                    produit_biologique = row[10]
                    type_prel          = row[11]
                    # type_analyse       = row[12]  # useless

                    if row[13] and row[13] == 'Y':
                        actif = 4
                    else:
                        actif = 5

                    if row[14] and row[14] == 'Y':
                        ana_whonet = 4
                    else:
                        ana_whonet = 5

                    id_link            = row[15]
                    # id_refanalyse      = row[16]
                    id_refvariable     = row[17]
                    position           = row[18]
                    num_var            = row[19]

                    if row[20] and row[20] == 'Y':
                        obligatoire = 4
                    else:
                        obligatoire = 5

                    id_var             = row[21]
                    libelle            = row[22]
                    description        = row[23]
                    unite              = row[24]
                    normal_min         = row[25]
                    normal_max         = row[26]
                    var_comm           = row[27]
                    type_resultat      = row[28]
                    formule            = row[29]
                    accuracy           = row[30]
                    code_var           = row[31]

                    if row[32] and row[32] == 'Y':
                        var_whonet = 4
                    else:
                        var_whonet = 5

                    var_qrcode         = row[33]
                    var_highlight      = row[34]

                    ret = Analysis.exist(code)

                    if ret == -1:
                        self.log.info(Logs.fileline() + ' : TRACE AnalysisImport ERROR sql')
                        DB.insertDbStatus(stat='ERR;AnalysisImport ERROR SQL verify code analysis code=' + str(code), type='ANA')
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
                                self.log.info(Logs.fileline() + ' : TRACE AnalysisImport ERROR update analysis code: ' + str(code) + ' | csv_line=' + str(i))
                                DB.insertDbStatus(stat='ERR;AnalysisImport ERROR update analysis code: ' + str(code), type='ANA')
                                return compose_ret('', Constants.cst_content_type_json, 500)

                            code_prev = code

                        # Get list of link
                        l_link = Analysis.getListVariable(id_ana)

                        for link in l_link:
                            if int(link['id_data']) == int(id_refvariable):
                                # UPDATE VAR
                                ret = Analysis.updateAnalysisVar(id_data=id_var,
                                                                 id_owner=id_owner,
                                                                 label=libelle,
                                                                 code_var=code_var,
                                                                 descr=description,
                                                                 type_res=type_resultat,
                                                                 var_min=normal_min,
                                                                 var_max=normal_max,
                                                                 var_highlight=var_highlight,
                                                                 comment=var_comm,
                                                                 formula=formule,
                                                                 unit=unite,
                                                                 accu=accuracy,
                                                                 formula2='',  # formule_unite2,
                                                                 unit2=0,      # unite2,
                                                                 accu2=0)      # precision2)

                                if ret is False:
                                    self.log.info(Logs.fileline() + ' : TRACE AnalysisImport ERROR update var analysis code: ' + str(code) + ' | csv_line=' + str(i))
                                    DB.insertDbStatus(stat='ERR;AnalysisImport ERROR update var analysis code: ' + str(code), type='ANA')
                                    return compose_ret('', Constants.cst_content_type_json, 500)

                                # UPDATE LINK
                                ret = Analysis.updateRefVariable(id_data=id_link,
                                                                 id_owner=id_owner,
                                                                 id_refana=id_ana,
                                                                 id_refvar=id_var,
                                                                 var_pos=position,
                                                                 var_num=num_var,
                                                                 oblig=obligatoire,
                                                                 var_whonet=var_whonet,
                                                                 var_qrcode=var_qrcode)

                                if not ret:
                                    self.log.info(Logs.fileline() + ' : TRACE AnalysisImport ERROR update link var to analysis code: ' + str(code) + ' | csv_line=' + str(i))
                                    DB.insertDbStatus(stat='ERR;AnalysisImport ERROR update link var to analysis code: ' + str(code), type='ANA')
                                    return compose_ret('', Constants.cst_content_type_json, 500)

        # ADD MODE
        elif type == 'A':
            code_prev = ''

            i = 1
            for row in l_rows:
                i = i + 1
                self.log.info(Logs.fileline() + ' : DEBUG-TRACE IMPORT LINE ' + str(i) + ' #############')
                self.log.info(Logs.fileline() + ' : DEBUG-TRACE IMPORT row=' + str(row))
                if row:
                    id_ana             = row[1]
                    id_owner           = row[2]
                    code               = row[3]
                    nom                = row[4]
                    abbr               = row[5]
                    famille            = row[6]
                    cote_unite         = row[7]

                    if row[8]:
                        cote_valeur = float(row[8])
                    else:
                        cote_valeur = 0

                    commentaire        = row[9]
                    produit_biologique = row[10]
                    type_prel          = row[11]
                    # type_analyse       = row[12]  # useless

                    if row[13] and row[13] == 'Y':
                        actif = 4
                    else:
                        actif = 5

                    if row[14] and row[14] == 'Y':
                        ana_whonet = 4
                    else:
                        ana_whonet = 5

                    id_link            = row[15]
                    # id_refanalyse      = row[16]
                    id_refvariable     = row[17]
                    position           = row[18]
                    num_var            = row[19]

                    if row[20] and row[20] == 'Y':
                        obligatoire = 4
                    else:
                        obligatoire = 5

                    id_var             = row[21]
                    libelle            = row[22]
                    description        = row[23]
                    unite              = row[24]
                    normal_min         = row[25]
                    normal_max         = row[26]
                    var_comm           = row[27]
                    type_resultat      = row[28]
                    formule            = row[29]
                    accuracy           = row[30]
                    code_var           = row[31]

                    if row[32] and row[32] == 'Y':
                        var_whonet = 4
                    else:
                        var_whonet = 5

                    var_qrcode     = row[33]
                    var_highlight  = row[34]

                    ret = Analysis.exist(code)

                    if ret == -1:
                        self.log.info(Logs.fileline() + ' : TRACE AnalysisImport ERROR sql')
                        DB.insertDbStatus(stat='ERR;AnalysisImport ERROR SQL verify code analysis code=' + str(code), type='ANA')
                        return compose_ret('', Constants.cst_content_type_json, 500)

                    # New analysis code or same analysis after insert
                    if not ret or code == code_prev:
                        self.log.info(Logs.fileline() + ' : DEBUG-TRACE IMPORT not ret or code == code_prev')
                        # different analysis
                        if code != code_prev:
                            self.log.info(Logs.fileline() + ' : DEBUG-TRACE IMPORT code != code_prev')
                            # check if id_data is available
                            ret = Analysis.freeIdAna(id_ana)

                            if ret == -1:
                                self.log.info(Logs.fileline() + ' : TRACE AnalysisImport ERROR sql')
                                DB.insertDbStatus(stat='ERR;AnalysisImport ERROR SQL verify id analysis=' + str(id_ana), type='ANA')
                                return compose_ret('', Constants.cst_content_type_json, 500)

                            if ret:
                                id_data = id_ana
                            else:
                                id_data = 0

                            self.log.info(Logs.fileline() + ' : DEBUG-TRACE IMPORT insert analysis code=' + code)
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
                                self.log.info(Logs.fileline() + ' : TRACE AnalysisImport ERROR insert analysis code: ' + str(code) + ' | csv_line=' + str(i))
                                DB.insertDbStatus(stat='ERR;AnalysisImport ERROR insert analysis code: ' + str(code), type='ANA')
                                return compose_ret('', Constants.cst_content_type_json, 500)

                            id_ana = ret

                            code_prev = code

                        if id_link and int(id_link) > 0:
                            # get same variable from these criteria
                            self.log.info(Logs.fileline() + ' : DEBUG-TRACE IMPORT criteria code_var=' + str(code_var))
                            var = Analysis.getAnalysisVarExist(libelle, type_resultat, unite, normal_min, normal_max, code_var)
                            self.log.info(Logs.fileline() + ' : DEBUG-TRACE IMPORT criteria var=' + str(var))

                            if var:
                                self.log.info(Logs.fileline() + ' : DEBUG-TRACE IMPORT variable exist id_data=' + str(var['id_data']))
                                id_var = var['id_data']
                            else:
                                self.log.info(Logs.fileline() + ' : DEBUG-TRACE IMPORT variable NOT exist')
                                self.log.info(Logs.fileline() + ' : DEBUG-TRACE IMPORT insert VAR code_var=' + code_var)
                                # INSERT UNKNOW VAR
                                ret = Analysis.insertAnalysisVar(id_owner=id_owner,
                                                                 label=libelle,
                                                                 code_var=code_var,
                                                                 descr=description,
                                                                 type_res=type_resultat,
                                                                 var_min=normal_min,
                                                                 var_max=normal_max,
                                                                 var_highlight=var_highlight,
                                                                 comment=var_comm,
                                                                 formula=formule,
                                                                 unit=unite,
                                                                 accu=accuracy,
                                                                 formula2='',  # formule_unite2,
                                                                 unit2=0,      # unite2,
                                                                 accu2=0)      # precision2)

                                if ret <= 0:
                                    self.log.info(Logs.fileline() + ' : AnalysisImport ERROR insert var analysis code: ' + str(code) + ' | csv_line=' + str(i))
                                    DB.insertDbStatus(stat='ERR;AnalysisImport ERROR insert var analysis code: ' + str(code), type='ANA')
                                    return compose_ret('', Constants.cst_content_type_json, 500)

                                id_var = ret

                            self.log.info(Logs.fileline() + ' : DEBUG-TRACE IMPORT id_var=' + str(id_var))
                            self.log.info(Logs.fileline() + ' : DEBUG-TRACE IMPORT insert LINK')

                            # INSERT NEW LINK
                            ret = Analysis.insertRefVariable(id_owner=id_owner,
                                                             id_refana=id_ana,
                                                             id_refvar=id_var,
                                                             var_pos=position,
                                                             var_num=num_var,
                                                             oblig=obligatoire,
                                                             var_whonet=var_whonet,
                                                             var_qrcode=var_qrcode)

                            if ret <= 0:
                                self.log.info(Logs.fileline() + ' : AnalysisImport ERROR insert link var to analysis code: ' + str(code) + ' | csv_line=' + str(i))
                                DB.insertDbStatus(stat='ERR;AnalysisImport ERROR insert link var analysis code: ' + str(code), type='ANA')
                                return compose_ret('', Constants.cst_content_type_json, 500)

        else:
            self.log.error(Logs.fileline() + ' : TRACE AnalysisImport ERROR wrong type')
            DB.insertDbStatus(stat='ERR;AnalysisImport ERROR wrong type', type='ANA')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE AnalysisImport')
        DB.insertDbStatus(stat='OK;AnalysisImport ended OK', type='ANA')
        return compose_ret('', Constants.cst_content_type_json, 200)


class AnalysisStatus(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        if 'status' not in args or 'id_ana' not in args or 'id_user' not in args:
            self.log.error(Logs.fileline() + ' : AnalysisStatus ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        ret = Analysis.updateAnalysisStatus(args['status'], args['id_ana'])

        if not ret:
            self.log.error(Logs.fileline() + ' : TRACE AnalysisStatus ERROR ')

        self.log.info(Logs.fileline() + ' : TRACE AnalysisStatus by user:' + str(args['id_user']))
        return compose_ret('', Constants.cst_content_type_json)
