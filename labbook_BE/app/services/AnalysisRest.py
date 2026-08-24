# -*- coding:utf-8 -*-
import logging
import gettext
import os

from datetime import datetime
from flask import request
from flask_restful import Resource
from pathlib import Path
from csv import reader

from app.models.General import compose_ret
from app.models.Constants import Constants
from app.models.Audit import Audit
from app.models.Analysis import Analysis
from app.models.Record import Record
from app.models.DB import DB
from app.models.Logs import Logs
from app.models.Various import Various
from app.security.oauth_routes import require_oauth


def save_analysis_variables(id_ana, args, audit_user, log):
    """
    Create or update the variables attached to an analysis and their link to it.
    Handles both cases: a brand new analysis carries id_link 0 for every variable.
    Returns the error response to send back, or None when everything went through.
    """
    for var in args['list_var']:
        # shared by the update and insert calls below
        var_fields = {
            'id_owner': args['id_owner'],
            'label': var['var_label'],
            'code_var': var['var_code'],
            'descr': var['var_descr'],
            'type_res': var['var_type_res'],
            'var_min': var['var_min'],
            'var_max': var['var_max'],
            'var_show_minmax': var['var_show_minmax'],
            'var_highlight': var['var_highlight'],
            'var_in_report': var['var_in_report'],
            'comment': var['var_comment'],
            'formula': var['var_formula'],
            'unit': var['var_unit'],
            'accu': var['var_accu'],
            'formula2': var['var_formula2'],
            'unit2': var['var_unit2'],
            'accu2': var['var_accu2'],
        }

        if var['id_var'] > 0:
            # update variable which already exist
            ret = Analysis.updateAnalysisVar(id_data=var['id_var'], **var_fields)

            if ret is False:
                log.info(Logs.fileline() + ' : TRACE AnalysisDet ERROR update var analysis')
                try:
                    details = {"result": "ERROR", "reason": "UPDATE_VAR_ANALYSIS", "id_ana": id_ana}
                    Audit.insertAudit(audit_user, "AnalysisDet", "ANALYSIS", id_ana, "ERROR", details, "U")
                except Exception:
                    log.exception(Logs.fileline() + ' : AnalysisDet ERROR audit update var analysis')
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
                    log.info(Logs.fileline() + ' : TRACE AnalysisDet ERROR insert link var to analysis')
                    try:
                        details = {"result": "ERROR", "reason": "INSERT_LINK_VAR", "id_ana": id_ana}
                        Audit.insertAudit(audit_user, "AnalysisDet", "ANALYSIS", id_ana, "ERROR", details, "C")
                    except Exception:
                        log.exception(Logs.fileline() + ' : AnalysisDet ERROR audit insert link var')
                    return compose_ret('', Constants.cst_content_type_json, 500)
            else:
                ret = Analysis.updateRefVariable(id_data=var['id_link'],
                                                 id_owner=args['id_owner'],
                                                 var_pos=var['var_pos'],
                                                 var_num=var['var_num'],
                                                 oblig=var['var_oblig'],
                                                 var_whonet=var['var_whonet'],
                                                 var_qrcode=var['var_qrcode'])

                if ret is False:
                    log.info(Logs.fileline() + ' : TRACE AnalysisDet ERROR update link var to analysis')
                    try:
                        details = {"result": "ERROR", "reason": "UPDATE_LINK_VAR", "id_ana": id_ana,
                                   "id_link": var.get('id_link')}
                        Audit.insertAudit(audit_user, "AnalysisDet", "ANALYSIS", id_ana, "ERROR", details, "U")
                    except Exception:
                        log.exception(Logs.fileline() + ' : AnalysisDet ERROR audit update link var')
                    return compose_ret('', Constants.cst_content_type_json, 500)

        else:
            # insert new variable
            ret = Analysis.insertAnalysisVar(**var_fields)

            if ret is False:
                log.info(Logs.fileline() + ' : TRACE AnalysisDet ERROR insert var analysis')
                try:
                    details = {"result": "ERROR", "reason": "INSERT_VAR_ANALYSIS", "id_ana": id_ana}
                    Audit.insertAudit(audit_user, "AnalysisDet", "ANALYSIS", id_ana, "ERROR", details, "C")
                except Exception:
                    log.exception(Logs.fileline() + ' : AnalysisDet ERROR audit insert var analysis')
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
                log.info(Logs.fileline() + ' : TRACE AnalysisDet ERROR insert link var to analysis')
                try:
                    details = {"result": "ERROR", "reason": "INSERT_LINK_VAR", "id_ana": id_ana, "id_var": id_var}
                    Audit.insertAudit(audit_user, "AnalysisDet", "ANALYSIS", id_ana, "ERROR", details, "C")
                except Exception:
                    log.exception(Logs.fileline() + ' : AnalysisDet ERROR audit insert link var')
                return compose_ret('', Constants.cst_content_type_json, 500)


    return None


class AnalysisSearch(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self, type):
        audit_user = request.oauth_user
        args = request.get_json() or {}

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
            self.log.info(Logs.fileline() + ' : TRACE AnalysisSearch not found')

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
        try:
            details = {"result": "SUCCESS", "type": str(type), "status": status, "count": len(l_analysis) if l_analysis else 0}
            Audit.insertAudit(audit_user, "AnalysisSearch", "ANALYSIS", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : AnalysisSearch ERROR audit success')
        return compose_ret(l_analysis, Constants.cst_content_type_json)


class AnalysisVarSearch(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        l_vars = Analysis.getAnalysisVarSearch(args['term'])

        if not l_vars:
            self.log.info(Logs.fileline() + ' : TRACE AnalysisVarSearch not found')

        # TRANSLATION
        Various.useLangDB()
        for var in l_vars:
            var_libel = var['field_value']

            if var_libel:
                var['field_value'] = _(var_libel.strip())
            else:
                var['field_value'] = ''

        self.log.info(Logs.fileline() + ' : TRACE AnalysisVarSearch')
        try:
            details = {"result": "SUCCESS", "count": len(l_vars) if l_vars else 0}
            Audit.insertAudit(audit_user, "AnalysisVarSearch", "ANALYSIS", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : AnalysisVarSearch ERROR audit success')
        return compose_ret(l_vars, Constants.cst_content_type_json)


class AnalysisList(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        if 'status' in args and args['status']:
            if args['status'] == 'A':
                args['status'] = 4
            elif args['status'] == 'I':
                args['status'] = 5

        l_analyzes = Analysis.getAnalyzesList(args)

        if not l_analyzes:
            self.log.info(Logs.fileline() + ' : TRACE AnalysisList not found')

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
        try:
            details = {"result": "SUCCESS", "count": len(l_analyzes) if l_analyzes else 0}
            Audit.insertAudit(audit_user, "AnalysisList", "ANALYSIS", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : AnalysisList ERROR audit success')
        return compose_ret(l_analyzes, Constants.cst_content_type_json)


class AnalysisListFromExt(Resource):
    log = logging.getLogger('log_services')

    @require_oauth('external/analysis')
    def post(self):
        self.log.info(Logs.fileline() + ' : AnalysisListFromExt API access authorized')
        audit_user = request.oauth_user
        args = request.get_json() or {}

        if not args:
            args = {}
        else:
            if 'status' in args and args['status']:
                if args['status'] == 'A':
                    args['status'] = 4
                elif args['status'] == 'I':
                    args['status'] = 5

        l_analyzes = Analysis.getAnalyzesList(args)

        if not l_analyzes:
            self.log.info(Logs.fileline() + ' : TRACE AnalysisListFromExt not found')

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

        self.log.info(Logs.fileline() + ' : TRACE AnalysisListFromExt')
        try:
            details = {"result": "SUCCESS", "count": len(l_analyzes) if l_analyzes else 0}
            Audit.insertAudit(audit_user, "AnalysisListFromExt", "ANALYSIS", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : AnalysisListFromExt ERROR audit success')
        return compose_ret(l_analyzes, Constants.cst_content_type_json, 200)


class AnalysisHistoExport(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        l_data = [['id_data', 'code', 'fam_name', 'name', 'nb_ana']]

        if 'date_beg' not in args or 'date_end' not in args:
            self.log.error(Logs.fileline() + ' : AnalysisHistoExport ERROR args missing')
            try:
                details = {"result": "ERROR", "reason": "ARGS_MISSING", "missing": ["date_beg", "date_end"]}
                Audit.insertAudit(audit_user, "AnalysisHistoExport", "ANALYSIS", None, "ERROR", details, "E")
            except Exception:
                self.log.exception(Logs.fileline() + ' : AnalysisHistoExport ERROR audit args missing')
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
            try:
                details = {"result": "ERROR", "reason": "NO_DATA", "date_beg": args.get("date_beg"),
                           "date_end": args.get("date_end")}
                Audit.insertAudit(audit_user, "AnalysisHistoExport", "ANALYSIS", None, "ERROR", details, "E")
            except Exception:
                self.log.exception(Logs.fileline() + ' : AnalysisHistoExport ERROR audit not found')
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
            self.log.exception(Logs.fileline() + ' : post AnalysisHistoExport failed')
            try:
                details = {"result": "ERROR", "reason": "WRITE_CSV_FAILED", "error": str(err),
                           "date_beg": args.get("date_beg"), "date_end": args.get("date_end")}
                Audit.insertAudit(audit_user, "AnalysisHistoExport", "ANALYSIS", None, "ERROR", details, "E")
            except Exception:
                self.log.exception(Logs.fileline() + ' : AnalysisHistoExport ERROR audit exception')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE AnalysisHistoExport')
        try:
            details = {"result": "SUCCESS", "date_beg": args.get("date_beg"), "date_end": args.get("date_end"),
                       "count": len(l_data) - 1}
            Audit.insertAudit(audit_user, "AnalysisHistoExport", "ANALYSIS", None, "SUCCESS", details, "E")
        except Exception:
            self.log.exception(Logs.fileline() + ' : AnalysisHistoExport ERROR audit success')
        return compose_ret('', Constants.cst_content_type_json)


class AnalysisHistoList(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        if 'date_beg' not in args or 'date_end' not in args:
            self.log.error(Logs.fileline() + ' : AnalysisHistoList ERROR args missing')
            try:
                details = {"result": "ERROR", "reason": "ARGS_MISSING", "missing": ["date_beg", "date_end"]}
                Audit.insertAudit(audit_user, "AnalysisHistoList", "ANALYSIS", None, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : AnalysisHistoList ERROR audit args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        args['limit'] = 7000

        l_analyzes = Analysis.getAnalyzesHistoList(args)

        if not l_analyzes:
            self.log.info(Logs.fileline() + ' : TRACE AnalysisHistoList not found')

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
        try:
            details = {"result": "SUCCESS", "date_beg": args.get("date_beg"), "date_end": args.get("date_end"),
                       "count": len(l_analyzes) if l_analyzes else 0}
            Audit.insertAudit(audit_user, "AnalysisHistoList", "ANALYSIS", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : AnalysisHistoList ERROR audit success')
        return compose_ret(l_analyzes, Constants.cst_content_type_json)


class AnalysisHistoDet(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        if 'date_beg' not in args or 'date_end' not in args or 'id_ana' not in args:
            self.log.error(Logs.fileline() + ' : AnalysisHistoDet ERROR args missing')
            try:
                details = {"result": "ERROR", "reason": "ARGS_MISSING", "missing": ["date_beg", "date_end", "id_ana"]}
                Audit.insertAudit(audit_user, "AnalysisHistoDet", "ANALYSIS", None, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : AnalysisHistoDet ERROR audit args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        args['limit'] = 7000

        l_datas = Analysis.getAnalyzesHistoDet(args)

        if not l_datas:
            self.log.info(Logs.fileline() + ' : TRACE AnalysisHistoDet not found')

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
        try:
            details = {"result": "SUCCESS", "date_beg": args.get("date_beg"), "date_end": args.get("date_end"),
                       "id_ana": args.get("id_ana"), "count": len(l_datas) if l_datas else 0}
            Audit.insertAudit(audit_user, "AnalysisHistoDet", "ANALYSIS", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : AnalysisHistoDet ERROR audit success')
        return compose_ret(l_datas, Constants.cst_content_type_json)


class AnalysisCode(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self, code):
        audit_user = request.oauth_user
        ret = Analysis.exist(code)

        if ret and ret == -1:
            self.log.error(Logs.fileline() + ' : ' + 'AnalysisCode ERROR sql')
            try:
                details = {"result": "ERROR", "reason": "SQL_ERROR", "code": str(code)}
                Audit.insertAudit(audit_user, "AnalysisCode", "ANALYSIS", None, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : AnalysisCode ERROR audit sql')
            return compose_ret(-1, Constants.cst_content_type_json, 500)

        if ret:
            self.log.info(Logs.fileline() + ' : ' + 'AnalysisCode WARNING code already exist')
            try:
                details = {"result": "SUCCESS", "code": str(code)}
                Audit.insertAudit(audit_user, "AnalysisCode", "ANALYSIS", None, "SUCCESS", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : AnalysisCode ERROR audit success')
            return compose_ret(1, Constants.cst_content_type_json, 200)
        else:
            self.log.info(Logs.fileline() + ' : AnalysisCode code ok :' + str(code))
            try:
                details = {"result": "SUCCESS", "code": str(code)}
                Audit.insertAudit(audit_user, "AnalysisCode", "ANALYSIS", None, "SUCCESS", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : AnalysisCode ERROR audit success')
            return compose_ret(0, Constants.cst_content_type_json, 200)


class AnalysisCodeFromExt(Resource):
    log = logging.getLogger('log_services')

    @require_oauth('external/analysis')
    def get(self, code):
        self.log.info(Logs.fileline() + ' : AnalysisCodeFromExt API access authorized')
        audit_user = request.oauth_user
        ret = Analysis.exist(code)

        if ret and ret == -1:
            self.log.error(Logs.fileline() + ' : ' + 'AnalysisCodeFromExt ERROR sql')
            try:
                details = {"result": "ERROR", "reason": "SQL_ERROR", "code": str(code)}
                Audit.insertAudit(audit_user, "AnalysisCodeFromExt", "ANALYSIS", None, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : AnalysisCodeFromExt ERROR audit sql')
            return compose_ret(-1, Constants.cst_content_type_json, 500)

        if ret:
            self.log.info(Logs.fileline() + ' : ' + 'AnalysisCodeFromExt WARNING code already exist')
            try:
                details = {"result": "SUCCESS", "code": str(code)}
                Audit.insertAudit(audit_user, "AnalysisCodeFromExt", "ANALYSIS", None, "SUCCESS", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : AnalysisCode ERROR audit success')
            return compose_ret(1, Constants.cst_content_type_json, 200)
        else:
            self.log.info(Logs.fileline() + ' : AnalysisCodeFromExt code ok :' + str(code))
            try:
                details = {"result": "SUCCESS", "code": str(code)}
                Audit.insertAudit(audit_user, "AnalysisCodeFromExt", "ANALYSIS", None, "SUCCESS", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : AnalysisCodeFromExt ERROR audit success')
            return compose_ret(0, Constants.cst_content_type_json, 200)


class AnalysisDet(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self, id_ana):
        audit_user = request.oauth_user
        analysis = Analysis.getAnalysis(id_ana)

        if not analysis:
            self.log.error(Logs.fileline() + ' : ' + 'AnalysisDet ERROR not found')
            try:
                details = {"result": "ERROR", "reason": "NOT_FOUND", "id_ana": id_ana}
                Audit.insertAudit(audit_user, "AnalysisDet", "ANALYSIS", id_ana, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : AnalysisDet ERROR audit not found')
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
        try:
            details = {"result": "SUCCESS", "id_ana": id_ana}
            Audit.insertAudit(audit_user, "AnalysisDet", "ANALYSIS", id_ana, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : AnalysisDet ERROR audit success')
        return compose_ret(analysis, Constants.cst_content_type_json, 200)

    @require_oauth()
    def post(self, id_ana):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        if 'id_ana' not in args or 'code' not in args or 'name' not in args or 'abbr' not in args or \
           'type_ana' not in args or 'type_prod' not in args or 'unit' not in args or 'value' not in args or \
           'stat' not in args or 'comment' not in args or 'product' not in args or 'list_var' not in args or \
           'whonet' not in args or 'ana_ast' not in args or 'ana_lite' not in args:
            self.log.error(Logs.fileline() + ' : AnalysisDet ERROR args missing')
            try:
                details = {"result": "ERROR", "reason": "ARGS_MISSING"}
                Audit.insertAudit(audit_user, "AnalysisDet", "ANALYSIS", None, "ERROR", details, "U")
            except Exception:
                self.log.exception(Logs.fileline() + ' : AnalysisDet ERROR audit args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        id_ana = args['id_ana']

        # check if analysis already exist
        analysis = Analysis.getAnalysis(id_ana)

        # UPDATE ANALYSIS...
        if analysis and analysis['id_data'] == id_ana:
            self.log.info(Logs.fileline() + ' : AnalysisDet UPDATE analysis')

            if args['value'] == '':
                args['value'] = 0

            # update analysis
            ret = Analysis.updateAnalysis(id_data=id_ana,
                                          id_owner=args['id_owner'],
                                          code=args['code'],
                                          ana_loinc=args['ana_loinc'],
                                          name=args['name'],
                                          abbr=args['abbr'],
                                          type_ana=args['type_ana'],
                                          type_prod=args['type_prod'],
                                          unit=args['unit'],
                                          value=float(args['value']),
                                          stat=args['stat'],
                                          comment=args['comment'],
                                          product=args['product'],
                                          whonet=args['whonet'],
                                          ana_ast=args['ana_ast'],
                                          ana_lite=args['ana_lite'])

            if ret is False:
                self.log.info(Logs.fileline() + ' : TRACE AnalysisDet ERROR update analysis')
                try:
                    details = {"result": "ERROR", "reason": "UPDATE_ANALYSIS", "id_ana": id_ana}
                    Audit.insertAudit(audit_user, "AnalysisDet", "ANALYSIS", id_ana, "ERROR", details, "U")
                except Exception:
                    self.log.exception(Logs.fileline() + ' : AnalysisDet ERROR audit')
                return compose_ret('', Constants.cst_content_type_json, 500)

            # delete missing link to variable compared to analysis (get list before add new var)
            db_l_var = Analysis.getListVariable(id_ana)

            err = save_analysis_variables(id_ana, args, audit_user, self.log)
            if err:
                return err
            for db_var in db_l_var:
                exist = False
                for ihm_var in args['list_var']:
                    if db_var['id_data'] == ihm_var['id_var']:
                        exist = True

                if not exist:
                    ret = Analysis.deleteRefVar(id_ana, db_var['id_data'])

                    if ret is False:
                        self.log.info(Logs.fileline() + ' : TRACE AnalysisDet ERROR delete link var analysis')
                        try:
                            details = {"result": "ERROR", "reason": "DELETE_LINK_VAR", "id_ana": id_ana, "id_var": db_var.get('id_data')}
                            Audit.insertAudit(audit_user, "AnalysisDet", "ANALYSIS", id_ana, "ERROR", details, "D")
                        except Exception:
                            self.log.exception(Logs.fileline() + ' : AnalysisDet ERROR audit delete link var')
                        return compose_ret('', Constants.cst_content_type_json, 500)

        # INSERT NEW ANALYSIS...
        else:
            self.log.info(Logs.fileline() + ' : AnalysisDet INSERT analysis')

            # insert analysis
            ret = Analysis.insertAnalysis(id_owner=args['id_owner'],
                                          code=args['code'],
                                          ana_loinc=args['ana_loinc'],
                                          name=args['name'],
                                          abbr=args['abbr'],
                                          type_ana=args['type_ana'],
                                          type_prod=args['type_prod'],
                                          unit=args['unit'],
                                          value=args['value'],
                                          stat=args['stat'],
                                          comment=args['comment'],
                                          product=args['product'],
                                          whonet=args['whonet'],
                                          ana_ast=args['ana_ast'],
                                          ana_lite=args['ana_lite'])

            if ret <= 0:
                self.log.info(Logs.fileline() + ' : TRACE AnalysisDet ERROR insert analysis')
                try:
                    details = {"result": "ERROR", "reason": "INSERT_ANALYSIS"}
                    Audit.insertAudit(audit_user, "AnalysisDet", "ANALYSIS", None, "ERROR", details, "C")
                except Exception:
                    self.log.exception(Logs.fileline() + ' : AnalysisDet ERROR audit insert analysis')
                return compose_ret('', Constants.cst_content_type_json, 500)

            id_ana = ret

            err = save_analysis_variables(id_ana, args, audit_user, self.log)
            if err:
                return err
        self.log.info(Logs.fileline() + ' : TRACE AnalysisDet id_ana=' + str(id_ana))
        try:
            details = {"result": "SUCCESS", "id_ana": id_ana}
            Audit.insertAudit(audit_user, "AnalysisDet", "ANALYSIS", id_ana, "SUCCESS", details, "U")
        except Exception:
            self.log.exception(Logs.fileline() + ' : AnalysisDet ERROR audit success')
        return compose_ret('', Constants.cst_content_type_json)

    @require_oauth()
    def delete(self, id_ana):
        audit_user = request.oauth_user
        ret = Analysis.deleteAnalysis(id_ana)

        if not ret:
            self.log.error(Logs.fileline() + ' : TRACE AnalysisDet delete ERROR')
            try:
                details = {"result": "ERROR", "reason": "DELETE_FAILED", "id_ana": id_ana}
                Audit.insertAudit(audit_user, "AnalysisDet", "ANALYSIS", id_ana, "ERROR", details, "D")
            except Exception:
                self.log.exception(Logs.fileline() + ' : AnalysisDet ERROR audit delete')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE AnalysisDet delete id_item=' + str(id_ana))
        try:
            details = {"result": "SUCCESS", "id_ana": id_ana}
            Audit.insertAudit(audit_user, "AnalysisDet", "ANALYSIS", id_ana, "SUCCESS", details, "D")
        except Exception:
            self.log.exception(Logs.fileline() + ' : AnalysisDet ERROR audit success')
        return compose_ret('', Constants.cst_content_type_json)


class AnalysisDetFromExt(Resource):
    log = logging.getLogger('log_services')

    @require_oauth('external/analysis')
    def get(self, id_ana):
        self.log.info(Logs.fileline() + ' : AnalysisDetFromExt API access authorized')
        audit_user = request.oauth_user
        analysis = Analysis.getAnalysis(id_ana)

        if not analysis:
            self.log.error(Logs.fileline() + ' : ' + 'AnalysisDetExt ERROR not found')
            try:
                details = {"result": "ERROR", "reason": "NOT_FOUND", "id_ana": id_ana}
                Audit.insertAudit(audit_user, "AnalysisDetFromExt", "ANALYSIS", id_ana, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : AnalysisDetFromExt ERROR audit not found')
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

        self.log.info(Logs.fileline() + ' : AnalysisDetExt id_data=' + str(id_ana))
        try:
            details = {"result": "SUCCESS", "id_ana": id_ana}
            Audit.insertAudit(audit_user, "AnalysisDetFromExt", "ANALYSIS", id_ana, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : AnalysisDetFromExt ERROR audit success')
        return compose_ret(analysis, Constants.cst_content_type_json, 200)


class AnalysisVarAll(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self):
        audit_user = request.oauth_user
        l_vars = Analysis.getAllVariable()

        if not l_vars:
            self.log.error(Logs.fileline() + ' : ' + 'AnalysisVarAll ERROR not found')
            try:
                details = {"result": "ERROR", "reason": "NOT_FOUND"}
                Audit.insertAudit(audit_user, "AnalysisVarAll", "ANALYSIS", None, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : AnalysisVarAll ERROR audit not found')
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

        self.log.info(Logs.fileline() + ' : AnalysisVarAll')
        try:
            details = {"result": "SUCCESS", "count": len(l_vars) if l_vars else 0}
            Audit.insertAudit(audit_user, "AnalysisVarAll", "ANALYSIS", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : AnalysisVarAll ERROR audit success')
        return compose_ret(l_vars, Constants.cst_content_type_json, 200)


class AnalysisVarList(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self, id_ana):
        audit_user = request.oauth_user
        l_vars = Analysis.getListVariable(id_ana)

        if not l_vars:
            self.log.error(Logs.fileline() + ' : ' + 'AnalysisVarList ERROR not found')
            try:
                details = {"result": "ERROR", "reason": "NOT_FOUND", "id_ana": id_ana}
                Audit.insertAudit(audit_user, "AnalysisVarList", "ANALYSIS", id_ana, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : AnalysisVarList ERROR audit not found')
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
        try:
            details = {"result": "SUCCESS", "id_ana": id_ana, "count": len(l_vars) if l_vars else 0}
            Audit.insertAudit(audit_user, "AnalysisVarList", "ANALYSIS", id_ana, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : AnalysisVarList ERROR audit success')
        return compose_ret(l_vars, Constants.cst_content_type_json, 200)


class AnalysisVarDet(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self, id_var):
        audit_user = request.oauth_user
        ana_var = Analysis.getAnalysisVar(id_var)

        if not ana_var:
            self.log.error(Logs.fileline() + ' : ' + 'AnalysisVarDet ERROR not found')
            try:
                details = {"result": "ERROR", "reason": "NOT_FOUND", "id_var": id_var}
                Audit.insertAudit(audit_user, "AnalysisVarDet", "ANALYSIS", id_var, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : AnalysisVarDet ERROR audit not found')
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
        try:
            details = {"result": "SUCCESS", "id_var": id_var}
            Audit.insertAudit(audit_user, "AnalysisVarDet", "ANALYSIS", id_var, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : AnalysisVarDet ERROR audit success')
        return compose_ret(ana_var, Constants.cst_content_type_json, 200)


class AnalysisTypeProd(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self, id_type_prod):
        audit_user = request.oauth_user
        type_prod = Analysis.getProductType(id_type_prod)

        if not type_prod:
            self.log.error(Logs.fileline() + ' : ' + 'AnalysisTypeProd ERROR not found')
            try:
                details = {"result": "ERROR", "reason": "NOT_FOUND", "id_type_prod": id_type_prod}
                Audit.insertAudit(audit_user, "AnalysisTypeProd", "ANALYSIS", id_type_prod, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : AnalysisTypeProd ERROR audit not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        Various.useLangDB()

        # Replace None by empty string
        for key, value in list(type_prod.items()):
            if type_prod[key] is None:
                type_prod[key] = ''
            elif key == 'label' and type_prod[key]:
                type_prod[key] = _(type_prod[key].strip())

        self.log.info(Logs.fileline() + ' : AnalysistypeProd id_type_prod' + str(id_type_prod))
        try:
            details = {"result": "SUCCESS", "id_type_prod": id_type_prod}
            Audit.insertAudit(audit_user, "AnalysisTypeProd", "ANALYSIS", id_type_prod, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : AnalysisTypeProd ERROR audit success')
        return compose_ret(type_prod, Constants.cst_content_type_json, 200)


class AnalysisReq(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self, id_rec, type_ana='A'):
        audit_user = request.oauth_user
        l_ana = Analysis.getAnalysisReq(id_rec, type_ana)

        if not l_ana:
            self.log.error(Logs.fileline() + ' : ' + 'AnalysisReq ERROR not found')
            try:
                details = {"result": "ERROR", "reason": "NOT_FOUND", "id_rec": id_rec, "type_ana": str(type_ana)}
                Audit.insertAudit(audit_user, "AnalysisReq", "RECORD", id_rec, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : AnalysisReq ERROR audit not found')
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
        try:
            details = {"result": "SUCCESS", "id_rec": id_rec, "type_ana": str(type_ana), "count": len(l_ana) if l_ana else 0}
            Audit.insertAudit(audit_user, "AnalysisReq", "RECORD", id_rec, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : AnalysisReq ERROR audit success')
        return compose_ret(l_ana, Constants.cst_content_type_json, 200)

    @require_oauth()
    def post(self):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        if 'list_ana' not in args:
            self.log.error(Logs.fileline() + ' : AnalysisReq ERROR args missing')
            try:
                details = {"result": "ERROR", "reason": "ARGS_MISSING", "missing": ["list_ana"]}
                Audit.insertAudit(audit_user, "AnalysisReq", "RECORD", None, "ERROR", details, "C")
            except Exception:
                self.log.exception(Logs.fileline() + ' : AnalysisReq ERROR audit args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # Loop on list_ana
        for ana in args['list_ana']:

            if 'id_owner' not in ana or 'id_rec' not in ana or 'id_ana' not in ana or 'price' not in ana or \
               'paid' not in ana or 'emer' not in ana or 'req' not in ana or 'outsourced' not in ana:
                self.log.error(Logs.fileline() + ' : AnalysisReq ERROR ana missing')
                try:
                    details = {"result": "ERROR", "reason": "ANA_MISSING"}
                    Audit.insertAudit(audit_user, "AnalysisReq", "RECORD", ana.get('id_rec'), "ERROR", details, "C")
                except Exception:
                    self.log.exception(Logs.fileline() + ' : AnalysisReq ERROR audit ana missing')
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
                try:
                    details = {"result": "ERROR", "reason": "INSERT_FAILED", "id_rec": ana.get('id_rec'), "id_ana": ana.get('id_ana')}
                    Audit.insertAudit(audit_user, "AnalysisReq", "RECORD", ana.get('id_rec'), "ERROR", details, "C")
                except Exception:
                    self.log.exception(Logs.fileline() + ' : AnalysisReq ERROR audit insert')
                return compose_ret('', Constants.cst_content_type_json, 500)

            res = {}
            res['id_req'] = ret

        self.log.info(Logs.fileline() + ' : TRACE AnalysisReq')
        try:
            details = {"result": "SUCCESS"}
            Audit.insertAudit(audit_user, "AnalysisReq", "RECORD", None, "SUCCESS", details, "C")
        except Exception:
            self.log.exception(Logs.fileline() + ' : AnalysisReq ERROR audit success')
        return compose_ret('', Constants.cst_content_type_json)

    @require_oauth()
    def delete(self, id_req):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        if 'id_rec' not in args or 'id_ana' not in args or 'type_samp' not in args or 'price' not in args:
            self.log.error(Logs.fileline() + ' : AnalysisReq ERROR args missing')
            try:
                details = {"result": "ERROR", "reason": "ARGS_MISSING", "id_req": id_req}
                Audit.insertAudit(audit_user, "AnalysisReq", "RECORD", id_req, "ERROR", details, "D")
            except Exception:
                self.log.exception(Logs.fileline() + ' : AnalysisReq ERROR audit args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        if args['price'] > 0:
            ret = Record.removeRecordBill(args['id_rec'], args['price'])

            if not ret:
                self.log.error(Logs.fileline() + ' : TRACE AnalysisReq removeRecordBill ERROR')
                try:
                    details = {"result": "ERROR", "reason": "REMOVE_BILL_FAILED", "id_req": id_req, "id_rec": args.get('id_rec')}
                    Audit.insertAudit(audit_user, "AnalysisReq", "RECORD", id_req, "ERROR", details, "D")
                except Exception:
                    self.log.exception(Logs.fileline() + ' : AnalysisReq ERROR audit remove bill')
                return compose_ret('', Constants.cst_content_type_json, 500)

        ret = Analysis.deleteAnalysisReq(id_req, args['id_rec'], args['id_ana'], args['type_samp'])

        if not ret:
            self.log.error(Logs.fileline() + ' : TRACE AnalysisReq delete ERROR')
            try:
                details = {"result": "ERROR", "reason": "DELETE_FAILED", "id_req": id_req, "id_rec": args.get('id_rec'),
                           "id_ana": args.get('id_ana'), "type_samp": args.get('type_samp')}
                Audit.insertAudit(audit_user, "AnalysisReq", "RECORD", id_req, "ERROR", details, "D")
            except Exception:
                self.log.exception(Logs.fileline() + ' : AnalysisReq ERROR audit delete')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE AnalysisReq delete id_item=' + str(id_req))
        try:
            details = {"result": "SUCCESS", "id_req": id_req, "id_rec": args.get('id_rec'), "id_ana": args.get('id_ana')}
            Audit.insertAudit(audit_user, "AnalysisReq", "RECORD", id_req, "SUCCESS", details, "D")
        except Exception:
            self.log.exception(Logs.fileline() + ' : AnalysisReq ERROR audit success')
        return compose_ret('', Constants.cst_content_type_json)


class AnalysisExport(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        l_data = [['version', 'id_ana', 'id_owner', 'ana_code', 'ana_name', 'ana_abbr', 'ana_family', 'ana_unit_rating',
                   'ana_value_rating', 'ana_comment', 'ana_bio_product', 'ana_sample_type', 'ana_type', 'ana_active',
                   'ana_whonet', 'id_link', 'link_ana_ref', 'link_var_ref', 'link_pos', 'link_num_var', 'link_oblig',
                   'id_var', 'var_label', 'var_descr', 'var_unit', 'var_min', 'var_max', 'var_comment', 'var_res_type',
                   'var_formula', 'var_accu', 'var_code', 'var_whonet', 'var_qrcode', 'var_highlight', 'var_show_minmax',
                   # v4
                   'var_formula_conv', 'var_unit_conv', 'var_accu_conv', 'ana_ast',
                   # v5
                   'ana_lite', 'ana_loinc',
                   # v6
                   'var_in_report']]

        if 'id_user' not in args:
            self.log.error(Logs.fileline() + ' : AnalysisExport ERROR args missing')
            try:
                details = {"result": "ERROR", "reason": "ARGS_MISSING", "missing": ["id_user"]}
                Audit.insertAudit(audit_user, "AnalysisExport", "ANALYSIS", None, "ERROR", details, "E")
            except Exception:
                self.log.exception(Logs.fileline() + ' : AnalysisExport ERROR audit args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        Various.useLangDB()

        dict_data = Analysis.getAnalysisExport()

        if dict_data:
            for d in dict_data:
                data = []

                data.append('v6')

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
                    data.append('"' + _(nom.strip()) + '"')
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

                if d['var_comm']:
                    comment = d['var_comm']
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

                if d['var_show_minmax']:
                    data.append(d['var_show_minmax'])
                else:
                    data.append('N')

                # --- added in v4 ---
                if d['formule_unite2']:
                    data.append(d['formule_unite2'])
                else:
                    data.append('')

                if d['unite2']:
                    data.append(d['unite2'])
                else:
                    data.append('')

                if d['precision2']:
                    data.append(d['precision2'])
                else:
                    data.append('')

                if d['ana_ast']:
                    if d['ana_ast'] == 'Y':
                        data.append('Y')
                    else:
                        data.append('N')
                else:
                    data.append('')

                # --- added in v5 ---
                if d['ana_lite']:
                    if d['ana_lite'] == 'Y':
                        data.append('Y')
                    else:
                        data.append('N')
                else:
                    data.append('')

                if d['ana_loinc']:
                    data.append(d['ana_loinc'])
                else:
                    data.append('')

                # --- added in v6 ---
                if d['var_in_report']:
                    data.append(d['var_in_report'])
                else:
                    data.append('Y')

                l_data.append(data)

        # if no result to export
        if len(l_data) < 2:
            try:
                details = {"result": "ERROR", "reason": "NO_DATA"}
                Audit.insertAudit(audit_user, "AnalysisExport", "ANALYSIS", None, "ERROR", details, "E")
            except Exception:
                self.log.exception(Logs.fileline() + ' : AnalysisExport ERROR audit no data')
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
            self.log.exception(Logs.fileline() + ' : post AnalysisExport failed')
            try:
                details = {"result": "ERROR", "reason": "WRITE_CSV_FAILED", "error": str(err)}
                Audit.insertAudit(audit_user, "AnalysisExport", "ANALYSIS", None, "ERROR", details, "E")
            except Exception:
                self.log.exception(Logs.fileline() + ' : AnalysisExport ERROR audit write csv')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE AnalysisExport')
        try:
            details = {"result": "SUCCESS"}
            Audit.insertAudit(audit_user, "AnalysisExport", "ANALYSIS", None, "SUCCESS", details, "E")
        except Exception:
            self.log.exception(Logs.fileline() + ' : AnalysisExport ERROR audit success')
        return compose_ret('', Constants.cst_content_type_json)


class AnalysisImport(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        if 'filename' not in args or 'type' not in args or 'id_user' not in args or 'test' not in args:
            self.log.error(Logs.fileline() + ' : AnalysisImport ERROR args missing')
            try:
                details = {"result": "ERROR", "reason": "ARGS_MISSING"}
                Audit.insertAudit(audit_user, "AnalysisImport", "ANALYSIS", None, "ERROR", details, "E")
            except Exception:
                self.log.exception(Logs.fileline() + ' : AnalysisImport ERROR audit args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        filename = args['filename']
        type     = args['type']
        # id_user  = args['id_user']
        test     = args['test']

        if test and test == 'Y':
            # empty the test tables
            ret = Analysis.dropTableTest()

            if not ret:
                self.log.error(Logs.fileline() + ' : TEST AnalysisImport ERROR dropTableTest')
                DB.insertDbStatus(stat='ERR;TEST AnalysisImport ERROR dropTableTest', type='ANA')
                try:
                    details = {"result": "ERROR", "reason": "DROP_TABLE_TEST"}
                    Audit.insertAudit(audit_user, "AnalysisImport", "ANALYSIS", None, "ERROR", details, "E")
                except Exception:
                    self.log.exception(Logs.fileline() + ' : AnalysisImport ERROR audit dropTableTest')
                return compose_ret('', Constants.cst_content_type_json, 500)

            # copy the production tables in the test tables
            ret = Analysis.initTableTest()

            if not ret:
                self.log.error(Logs.fileline() + ' : TEST AnalysisImport ERROR initTableTest')
                DB.insertDbStatus(stat='ERR;TEST AnalysisImport ERROR initTableTest', type='ANA')
                try:
                    details = {"result": "ERROR", "reason": "INIT_TABLE_TEST"}
                    Audit.insertAudit(audit_user, "AnalysisImport", "ANALYSIS", None, "ERROR", details, "E")
                except Exception:
                    self.log.exception(Logs.fileline() + ' : AnalysisImport ERROR audit initTableTest')
                return compose_ret('', Constants.cst_content_type_json, 500)

        # --- Read CSV user ---
        base_dir = Path(Constants.cst_path_tmp).resolve()

        raw_filename = filename
        if not isinstance(raw_filename, str) or not raw_filename:
            self.log.error(Logs.fileline() + ' : TRACE AnalysisImport ERROR invalid filename (empty or not a string)')
            DB.insertDbStatus(stat='ERR;AnalysisImport ERROR invalid filename', type='ANA')
            try:
                details = {"result": "ERROR", "reason": "INVALID_FILENAME"}
                Audit.insertAudit(audit_user, "AnalysisImport", "ANALYSIS", None, "ERROR", details, "E")
            except Exception:
                self.log.exception(Logs.fileline() + ' : AnalysisImport ERROR audit invalid filename')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # Keep only the final component; if it changes, separators were present -> reject
        safe_name = os.path.basename(raw_filename)
        if safe_name != raw_filename:
            self.log.error(Logs.fileline() + f' : TRACE AnalysisImport ERROR invalid filename "{Logs.clean(raw_filename)}" (path separators)')
            DB.insertDbStatus(stat='ERR;AnalysisImport ERROR invalid filename (separators)', type='ANA')
            try:
                details = {"result": "ERROR", "reason": "INVALID_FILENAME_SEPARATORS"}
                Audit.insertAudit(audit_user, "AnalysisImport", "ANALYSIS", None, "ERROR", details, "E")
            except Exception:
                self.log.exception(Logs.fileline() + ' : AnalysisImport ERROR audit filename separators')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # Enforce .csv extension
        if not safe_name.lower().endswith('.csv'):
            self.log.error(Logs.fileline() + f' : TRACE AnalysisImport ERROR invalid extension for "{Logs.clean(safe_name)}" (must be .csv)')
            DB.insertDbStatus(stat='ERR;AnalysisImport ERROR invalid extension', type='ANA')
            try:
                details = {"result": "ERROR", "reason": "INVALID_EXTENSION"}
                Audit.insertAudit(audit_user, "AnalysisImport", "ANALYSIS", None, "ERROR", details, "E")
            except Exception:
                self.log.exception(Logs.fileline() + ' : AnalysisImport ERROR audit invalid extension')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # Build and validate the final path, then ensure it stays under base_dir
        candidate_path = (base_dir / safe_name).resolve()
        try:
            if os.path.commonpath([str(candidate_path), str(base_dir)]) != str(base_dir):
                raise ValueError('path escapes base_dir')
        except Exception:
            self.log.exception(Logs.fileline() + f' : TRACE AnalysisImport ERROR path traversal detected for "{safe_name}"')
            DB.insertDbStatus(stat='ERR;AnalysisImport ERROR path traversal', type='ANA')
            try:
                details = {"result": "ERROR", "reason": "PATH_TRAVERSAL"}
                Audit.insertAudit(audit_user, "AnalysisImport", "ANALYSIS", None, "ERROR", details, "E")
            except Exception:
                self.log.exception(Logs.fileline() + ' : AnalysisImport ERROR audit path traversal')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # Ensure file exists
        if not candidate_path.is_file():
            self.log.error(Logs.fileline() + f' : TRACE AnalysisImport ERROR file not found "{candidate_path}"')
            DB.insertDbStatus(stat='ERR;AnalysisImport ERROR file not found', type='ANA')
            try:
                details = {"result": "ERROR", "reason": "FILE_NOT_FOUND"}
                Audit.insertAudit(audit_user, "AnalysisImport", "ANALYSIS", None, "ERROR", details, "E")
            except Exception:
                self.log.exception(Logs.fileline() + ' : AnalysisImport ERROR audit file not found')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # Safe open
        with candidate_path.open('r', encoding='utf-8') as csv_file:
            csv_reader = reader(csv_file, delimiter=';', quotechar='"')
            l_rows = list(csv_reader)

        # --- CSV treament ---
        # clean double quotes
        l_rows = [[col.strip('"') if col else col for col in row] for row in l_rows]

        if not l_rows or len(l_rows) < 2:
            self.log.error(Logs.fileline() + ' : TRACE AnalysisImport ERROR file empty')
            DB.insertDbStatus(stat='ERR;AnalysisImport ERROR file empty', type='ANA')
            try:
                details = {"result": "ERROR", "reason": "FILE_EMPTY"}
                Audit.insertAudit(audit_user, "AnalysisImport", "ANALYSIS", None, "ERROR", details, "E")
            except Exception:
                self.log.exception(Logs.fileline() + ' : AnalysisImport ERROR audit file empty')
            return compose_ret('', Constants.cst_content_type_json, 500)

        head_line = l_rows[0]

        # remove headers line
        l_rows.pop(0)

        version = l_rows[0][0]

        # check version
        if version not in ('v3', 'v4', 'v5', 'v6'):
            self.log.error(Logs.fileline() + ' : TRACE AnalysisImport ERROR wrong version : ' + str(version))
            DB.insertDbStatus(stat='ERR;AnalysisImport ERROR wrong version', type='ANA')
            try:
                details = {"result": "ERROR", "reason": "WRONG_VERSION", "version": str(version)}
                Audit.insertAudit(audit_user, "AnalysisImport", "ANALYSIS", None, "ERROR", details, "E")
            except Exception:
                self.log.exception(Logs.fileline() + ' : AnalysisImport ERROR audit wrong version')
            return compose_ret('', Constants.cst_content_type_json, 409)

        # check name of column
        head_list = ['version', 'id_ana', 'id_owner', 'ana_code', 'ana_name', 'ana_abbr', 'ana_family', 'ana_unit_rating',
                     'ana_value_rating', 'ana_comment', 'ana_bio_product', 'ana_sample_type', 'ana_type', 'ana_active',
                     'ana_whonet', 'id_link', 'link_ana_ref', 'link_var_ref', 'link_pos', 'link_num_var', 'link_oblig',
                     'id_var', 'var_label', 'var_descr', 'var_unit', 'var_min', 'var_max', 'var_comment', 'var_res_type',
                     'var_formula', 'var_accu', 'var_code', 'var_whonet', 'var_qrcode', 'var_highlight', 'var_show_minmax']

        if version in ('v4', 'v5', 'v6'):
            head_list += ['var_formula_conv', 'var_unit_conv', 'var_accu_conv', 'ana_ast']

        if version in ('v5', 'v6'):
            head_list += ['ana_lite', 'ana_loinc']

        if version == 'v6':
            head_list += ['var_in_report']

        i = 0
        for head in head_line:
            if head != head_list[i]:
                self.log.error(Logs.fileline() + ' : TRACE AnalysisImport ERROR wrong column or order : ' + str(head))
                DB.insertDbStatus(stat='ERR;AnalysisImport ERROR wrong column or order : ' + str(head), type='ANA')
                try:
                    details = {"result": "ERROR", "reason": "WRONG_COLUMN_OR_ORDER", "head": str(head)}
                    Audit.insertAudit(audit_user, "AnalysisImport", "ANALYSIS", None, "ERROR", details, "E")
                except Exception:
                    self.log.exception(Logs.fileline() + ' : AnalysisImport ERROR audit wrong column')
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

                    if len(row) > 35:
                        var_show_minmax = row[35]
                    else:
                        var_show_minmax = 'N'

                    # re-add formula2, unit2, accu2
                    if (version == 'v4' or version == 'v5' or version == 'v6') and len(row) > 39:
                        var_formula_conv = row[36]
                        var_unit_conv = row[37]
                        var_accu_conv = row[38]
                        ana_ast = row[39]
                    else:
                        var_formula_conv = ''
                        var_unit_conv = 0
                        var_accu_conv = 0
                        ana_ast = 'N'

                    if (version == 'v5' or version == 'v6') and len(row) > 40:
                        ana_lite = row[40]
                        ana_loinc = row[41]
                    else:
                        ana_lite  = 'N'
                        ana_loinc = ''

                    if version == 'v6' and len(row) > 41:
                        var_in_report = row[42]
                    else:
                        var_in_report  = 'Y'

                    ret = Analysis.exist(code, test)

                    if ret == -1:
                        self.log.info(Logs.fileline() + ' : TRACE AnalysisImport ERROR sql')
                        if test == 'N':
                            DB.insertDbStatus(stat='ERR;AnalysisImport ERROR SQL verify code analysis code=' + str(code), type='ANA')
                        else:
                            DB.insertDbStatus(stat='ERR;TEST AnalysisImport ERROR SQL verify code analysis code=' + str(code), type='ANA')
                        try:
                            details = {"result": "ERROR", "reason": "SQL_ERROR_VERIFY_CODE", "code": str(code), "csv_line": i}
                            Audit.insertAudit(audit_user, "AnalysisImport", "ANALYSIS", None, "ERROR", details, "E")
                        except Exception:
                            self.log.exception(Logs.fileline() + ' : AnalysisImport ERROR audit sql verify code')
                        return compose_ret('', Constants.cst_content_type_json, 500)

                    # same analysis
                    if ret:
                        ana_local = Analysis.getAnalysisByCode(code)

                        if ana_local and int(ana_local['id_data']) != int(id_ana):
                            id_ana = ana_local['id_data']

                        # next analysis
                        if code != code_prev:
                            # update analysis
                            ret = Analysis.updateAnalysis(id_data=id_ana,
                                                          id_owner=id_owner,
                                                          code=code,
                                                          ana_loinc=ana_loinc,
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
                                                          ana_ast=ana_ast,
                                                          ana_lite=ana_lite,
                                                          test=test)

                            if ret is False:
                                self.log.info(Logs.fileline() + ' : TRACE AnalysisImport ERROR update analysis code: ' + str(code) + ' | csv_line=' + str(i))
                                if test == 'N':
                                    DB.insertDbStatus(stat='ERR;AnalysisImport ERROR update analysis code: ' + str(code) + ' | csv_line=' + str(i), type='ANA')
                                else:
                                    DB.insertDbStatus(stat='ERR;TEST AnalysisImport ERROR update analysis code: ' + str(code) + ' | csv_line=' + str(i), type='ANA')
                                try:
                                    details = {"result": "ERROR", "reason": "UPDATE_ANALYSIS", "code": str(code), "csv_line": i}
                                    Audit.insertAudit(audit_user, "AnalysisImport", "ANALYSIS", None, "ERROR", details, "E")
                                except Exception:
                                    self.log.exception(Logs.fileline() + ' : AnalysisImport ERROR audit update analysis')
                                return compose_ret('', Constants.cst_content_type_json, 500)

                            code_prev = code

                        # Get list of link
                        l_link = Analysis.getListVariable(id_ana, test)

                        for link in l_link:
                            if int(link['id_item']) == int(id_refvariable):
                                # UPDATE VAR
                                ret = Analysis.updateAnalysisVar(id_data=id_var,
                                                                 id_owner=id_owner,
                                                                 label=libelle,
                                                                 code_var=code_var,
                                                                 descr=description,
                                                                 type_res=type_resultat,
                                                                 var_min=normal_min,
                                                                 var_max=normal_max,
                                                                 var_show_minmax=var_show_minmax,
                                                                 var_highlight=var_highlight,
                                                                 var_in_report=var_in_report,
                                                                 comment=var_comm,
                                                                 formula=formule,
                                                                 unit=unite,
                                                                 accu=accuracy,
                                                                 formula2=var_formula_conv,
                                                                 unit2=var_unit_conv,
                                                                 accu2=var_accu_conv,
                                                                 test=test)

                                if ret is False:
                                    self.log.info(Logs.fileline() + ' : TRACE AnalysisImport ERROR update var analysis code: ' + str(code) + ' | csv_line=' + str(i))
                                    if test == 'N':
                                        DB.insertDbStatus(stat='ERR;AnalysisImport ERROR update var analysis code: ' + str(code) + ' | csv_line=' + str(i), type='ANA')
                                    else:
                                        DB.insertDbStatus(stat='ERR;TEST AnalysisImport ERROR update var analysis code: ' + str(code) + ' | csv_line=' + str(i), type='ANA')
                                    try:
                                        details = {"result": "ERROR", "reason": "UPDATE_VAR_ANALYSIS", "code": str(code), "csv_line": i}
                                        Audit.insertAudit(audit_user, "AnalysisImport", "ANALYSIS", None, "ERROR", details, "E")
                                    except Exception:
                                        self.log.exception(Logs.fileline() + ' : AnalysisImport ERROR audit update var')
                                    return compose_ret('', Constants.cst_content_type_json, 500)

                                # UPDATE LINK
                                position = int(position) if str(position).strip().isdigit() else None
                                num_var  = int(num_var) if str(num_var).strip().isdigit() else None

                                ret = Analysis.updateRefVariable(id_data=link['id_data'],
                                                                 id_owner=id_owner,
                                                                 var_pos=position,
                                                                 var_num=num_var,
                                                                 oblig=obligatoire,
                                                                 var_whonet=var_whonet,
                                                                 var_qrcode=var_qrcode,
                                                                 test=test)

                                if ret is False:
                                    self.log.info(Logs.fileline() + ' : TRACE AnalysisImport ERROR update link var to analysis code: ' + str(code) + ' | csv_line=' + str(i))
                                    if test == 'N':
                                        DB.insertDbStatus(stat='ERR;AnalysisImport ERROR update link var to analysis code: ' + str(code) + ' | csv_line=' + str(i), type='ANA')
                                    else:
                                        DB.insertDbStatus(stat='ERR;TEST AnalysisImport ERROR update link var to analysis code: ' + str(code) + ' | csv_line=' + str(i), type='ANA')
                                    try:
                                        details = {"result": "ERROR", "reason": "UPDATE_LINK_VAR", "code": str(code), "csv_line": i}
                                        Audit.insertAudit(audit_user, "AnalysisImport", "ANALYSIS", None, "ERROR", details, "E")
                                    except Exception:
                                        self.log.exception(Logs.fileline() + ' : AnalysisImport ERROR audit update link var')
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

                    if len(row) > 35:
                        var_show_minmax = row[35]
                    else:
                        var_show_minmax = 'N'

                    # re-add formula2, unit2, accu2
                    if (version == 'v4' or version == 'v5' or version == 'v6') and len(row) > 39:
                        var_formula_conv = row[36]
                        var_unit_conv = row[37]
                        var_accu_conv = row[38]
                        ana_ast = row[39]
                    else:
                        var_formula_conv = ''
                        var_unit_conv = 0
                        var_accu_conv = 0
                        ana_ast = 'N'

                    if (version == 'v5' or version == 'v6') and len(row) > 40:
                        ana_lite = row[40]
                        ana_loinc = row[41]
                    else:
                        ana_lite  = 'N'
                        ana_loinc = ''

                    if version == 'v6' and len(row) > 41:
                        var_in_report = row[42]
                    else:
                        var_in_report = 'Y'

                    ret = Analysis.exist(code, test)

                    if ret == -1:
                        self.log.info(Logs.fileline() + ' : TRACE AnalysisImport ERROR sql')
                        if test == 'N':
                            DB.insertDbStatus(stat='ERR;AnalysisImport ERROR SQL verify code analysis code=' + str(code), type='ANA')
                        else:
                            DB.insertDbStatus(stat='ERR;TEST AnalysisImport ERROR SQL verify code analysis code=' + str(code), type='ANA')
                        try:
                            details = {"result": "ERROR", "reason": "SQL_ERROR_GET_ANALYSIS", "code": str(code), "csv_line": i}
                            Audit.insertAudit(audit_user, "AnalysisImport", "ANALYSIS", None, "ERROR", details, "E")
                        except Exception:
                            self.log.exception(Logs.fileline() + ' : AnalysisImport ERROR audit sql get analysis')
                        return compose_ret('', Constants.cst_content_type_json, 500)

                    # New analysis code or same analysis after insert
                    if not ret or code == code_prev:
                        self.log.info(Logs.fileline() + ' : DEBUG-TRACE IMPORT not ret or code == code_prev')
                        # different analysis
                        if code != code_prev:
                            self.log.info(Logs.fileline() + ' : DEBUG-TRACE IMPORT code != code_prev')
                            # check if id_data is available
                            ret = Analysis.freeIdAna(id_ana, test)

                            if ret == -1:
                                self.log.info(Logs.fileline() + ' : TRACE AnalysisImport ERROR sql')
                                if test == 'N':
                                    DB.insertDbStatus(stat='ERR;AnalysisImport ERROR SQL verify id analysis=' + str(id_ana), type='ANA')
                                else:
                                    DB.insertDbStatus(stat='ERR;TEST AnalysisImport ERROR SQL verify id analysis=' + str(id_ana), type='ANA')
                                try:
                                    details = {"result": "ERROR", "reason": "SQL_ERROR_GET_VAR", "code": str(code), "csv_line": i}
                                    Audit.insertAudit(audit_user, "AnalysisImport", "ANALYSIS", None, "ERROR", details, "E")
                                except Exception:
                                    self.log.exception(Logs.fileline() + ' : AnalysisImport ERROR audit sql get var')
                                return compose_ret('', Constants.cst_content_type_json, 500)

                            if ret:
                                id_data = id_ana
                            else:
                                id_data = 0

                            self.log.info(Logs.fileline() + ' : DEBUG-TRACE IMPORT insert analysis code=' + code)
                            # insert analysis
                            ret = Analysis.insertAnalysis(id_owner=id_owner,
                                                          code=code,
                                                          ana_loinc=ana_loinc,
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
                                                          ana_ast=ana_ast,
                                                          ana_lite=ana_lite,
                                                          id_data=id_data,
                                                          test=test)

                            if ret <= 0:
                                self.log.info(Logs.fileline() + ' : TRACE AnalysisImport ERROR insert analysis code: ' + str(code) + ' | csv_line=' + str(i))
                                if test == 'N':
                                    DB.insertDbStatus(stat='ERR;AnalysisImport ERROR insert analysis code: ' + str(code) + ' | csv_line=' + str(i), type='ANA')
                                else:
                                    DB.insertDbStatus(stat='ERR;TEST AnalysisImport ERROR insert analysis code: ' + str(code) + ' | csv_line=' + str(i), type='ANA')
                                try:
                                    details = {"result": "ERROR", "reason": "INSERT_ANALYSIS", "code": str(code), "csv_line": i}
                                    Audit.insertAudit(audit_user, "AnalysisImport", "ANALYSIS", None, "ERROR", details, "E")
                                except Exception:
                                    self.log.exception(Logs.fileline() + ' : AnalysisImport ERROR audit insert analysis')
                                return compose_ret('', Constants.cst_content_type_json, 500)

                            id_ana = ret

                            code_prev = code

                        if id_link and int(id_link) > 0:
                            # get same variable from these criteria
                            self.log.info(Logs.fileline() + ' : DEBUG-TRACE IMPORT criteria code_var=' + str(code_var))
                            var = Analysis.getAnalysisVarExist(libelle, type_resultat, unite, normal_min, normal_max, code_var, test)
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
                                                                 var_show_minmax=var_show_minmax,
                                                                 var_highlight=var_highlight,
                                                                 var_in_report=var_in_report,
                                                                 comment=var_comm,
                                                                 formula=formule,
                                                                 unit=unite,
                                                                 accu=accuracy,
                                                                 formula2=var_formula_conv,
                                                                 unit2=var_unit_conv,
                                                                 accu2=var_accu_conv,
                                                                 test=test)

                                if ret <= 0:
                                    self.log.info(Logs.fileline() + ' : AnalysisImport ERROR insert var analysis code: ' + str(code) + ' | csv_line=' + str(i))
                                    if test == 'N':
                                        DB.insertDbStatus(stat='ERR;AnalysisImport ERROR insert var analysis code: ' + str(code) + ' | csv_line=' + str(i), type='ANA')
                                    else:
                                        DB.insertDbStatus(stat='ERR;TEST AnalysisImport ERROR insert var analysis code: ' + str(code) + ' | csv_line=' + str(i), type='ANA')
                                    try:
                                        details = {"result": "ERROR", "reason": "INSERT_VAR_ANALYSIS", "code": str(code), "csv_line": i}
                                        Audit.insertAudit(audit_user, "AnalysisImport", "ANALYSIS", None, "ERROR", details, "E")
                                    except Exception:
                                        self.log.exception(Logs.fileline() + ' : AnalysisImport ERROR audit insert var')
                                    return compose_ret('', Constants.cst_content_type_json, 500)

                                id_var = ret

                            self.log.info(Logs.fileline() + ' : DEBUG-TRACE IMPORT id_var=' + str(id_var))
                            self.log.info(Logs.fileline() + ' : DEBUG-TRACE IMPORT insert LINK')

                            # INSERT NEW LINK
                            position = int(position) if str(position).strip().isdigit() else 0
                            num_var  = int(num_var) if str(num_var).strip().isdigit() else 0

                            ret = Analysis.insertRefVariable(id_owner=id_owner,
                                                             id_refana=id_ana,
                                                             id_refvar=id_var,
                                                             var_pos=position,
                                                             var_num=num_var,
                                                             oblig=obligatoire,
                                                             var_whonet=var_whonet,
                                                             var_qrcode=var_qrcode,
                                                             test=test)

                            if ret <= 0:
                                self.log.info(Logs.fileline() + ' : AnalysisImport ERROR insert link var to analysis code: ' + str(code) + ' | csv_line=' + str(i))
                                if test == 'N':
                                    DB.insertDbStatus(stat='ERR;AnalysisImport ERROR insert link var analysis code: ' + str(code) + ' | csv_line=' + str(i), type='ANA')
                                else:
                                    DB.insertDbStatus(stat='ERR;TEST AnalysisImport ERROR insert link var analysis code: ' + str(code) + ' | csv_line=' + str(i), type='ANA')
                                try:
                                    details = {"result": "ERROR", "reason": "INSERT_LINK_VAR", "code": str(code), "csv_line": i}
                                    Audit.insertAudit(audit_user, "AnalysisImport", "ANALYSIS", None, "ERROR", details, "E")
                                except Exception:
                                    self.log.exception(Logs.fileline() + ' : AnalysisImport ERROR audit insert link var')
                                return compose_ret('', Constants.cst_content_type_json, 500)

        else:
            self.log.error(Logs.fileline() + ' : TRACE AnalysisImport ERROR wrong type')
            DB.insertDbStatus(stat='ERR;AnalysisImport ERROR wrong type', type='ANA')
            try:
                details = {"result": "ERROR", "reason": "WRONG_TYPE"}
                Audit.insertAudit(audit_user, "AnalysisImport", "ANALYSIS", None, "ERROR", details, "E")
            except Exception:
                self.log.exception(Logs.fileline() + ' : AnalysisImport ERROR audit wrong type')
            return compose_ret('', Constants.cst_content_type_json, 500)

        ret = Analysis.cleanGhostVar(test)

        if not ret:
            self.log.info(Logs.fileline() + ' : TRACE AnalysisImport ERROR clean ghost var with no link')
            if test == 'N':
                DB.insertDbStatus(stat='ERR;AnalysisImport ERROR clean ghost var with no link', type='ANA')
            else:
                DB.insertDbStatus(stat='ERR;TEST AnalysisImport ERROR clean ghost var with no link', type='ANA')
            try:
                details = {"result": "ERROR", "reason": "CLEAN_GHOST_VAR"}
                Audit.insertAudit(audit_user, "AnalysisImport", "ANALYSIS", None, "ERROR", details, "E")
            except Exception:
                self.log.exception(Logs.fileline() + ' : AnalysisImport ERROR audit clean ghost var')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE AnalysisImport')

        if test == 'N':
            DB.insertDbStatus(stat='OK;AnalysisImport ended OK', type='ANA')
        else:
            DB.insertDbStatus(stat='OK;TEST AnalysisImport ended OK', type='ANA')
        try:
            details = {"result": "SUCCESS"}
            Audit.insertAudit(audit_user, "AnalysisImport", "ANALYSIS", None, "SUCCESS", details, "E")
        except Exception:
            self.log.exception(Logs.fileline() + ' : AnalysisImport ERROR audit success')
        return compose_ret('', Constants.cst_content_type_json, 200)


class AnalysisStatus(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        if 'status' not in args or 'id_ana' not in args or 'id_user' not in args:
            self.log.error(Logs.fileline() + ' : AnalysisStatus ERROR args missing')
            try:
                details = {"result": "ERROR", "reason": "ARGS_MISSING", "missing": ["status", "id_ana", "id_user"]}
                Audit.insertAudit(audit_user, "AnalysisStatus", "ANALYSIS", args.get('id_ana'), "ERROR", details, "U")
            except Exception:
                self.log.exception(Logs.fileline() + ' : AnalysisStatus ERROR audit args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        ret = Analysis.updateAnalysisStatus(args['status'], args['id_ana'])

        if not ret:
            self.log.error(Logs.fileline() + ' : TRACE AnalysisStatus ERROR')
            try:
                details = {"result": "ERROR", "reason": "UPDATE_FAILED", "id_ana": args.get('id_ana'),
                           "status": args.get('status'), "id_user": args.get('id_user')}
                Audit.insertAudit(audit_user, "AnalysisStatus", "ANALYSIS", args.get('id_ana'), "ERROR", details, "U")
            except Exception:
                self.log.exception(Logs.fileline() + ' : AnalysisStatus ERROR audit error')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE AnalysisStatus by user:' + str(args['id_user']))
        try:
            details = {"result": "SUCCESS", "id_ana": args.get('id_ana'), "status": args.get('status'),
                       "id_user": args.get('id_user')}
            Audit.insertAudit(audit_user, "AnalysisStatus", "ANALYSIS", args.get('id_ana'), "SUCCESS", details, "U")
        except Exception:
            self.log.exception(Logs.fileline() + ' : AnalysisStatus ERROR audit success')
        return compose_ret('', Constants.cst_content_type_json)
