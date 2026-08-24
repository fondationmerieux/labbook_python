# -*- coding:utf-8 -*-
import logging
import gettext
import os

from flask import request
from flask_restful import Resource

from app.models.General import compose_ret
from app.models.Constants import Constants
from app.models.Audit import Audit
from app.models.Pdf import Pdf
from app.models.Logs import Logs
from app.models.Report import Report
from app.models.Setting import Setting
from app.models.File import File
from app.models.Various import Various
from app.security.oauth_routes import require_oauth


class PdfBillList(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        if 'date_beg' not in args or 'date_end' not in args or 'tpl_file' not in args or 'filename' not in args:
            self.log.error(Logs.fileline() + ' : PdfBillList ERROR args missing')
            try:
                details = {"reason": "ARGS_MISSING"}
                Audit.insertAudit(audit_user, "PdfBillList", "PDF", None, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : PdfBillList ERROR audit')
            return compose_ret('', Constants.cst_content_type_json, 400)

        l_datas = Report.getBillingStatus(args['date_beg'], args['date_end'], 0)

        if not l_datas:
            self.log.error(Logs.fileline() + ' : TRACE list current billing not found')
            try:
                details = {"reason": "NOT_FOUND", "date_beg": args.get("date_beg"), "date_end": args.get("date_end")}
                Audit.insertAudit(audit_user, "PdfBillList", "PDF", None, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : PdfBillList ERROR audit')
            return compose_ret('', Constants.cst_content_type_json, 404)

        for data in l_datas:
            for key, value in list(data.items()):
                if data[key] is None:
                    data[key] = ''

        ret = Pdf.getPdfBillList(l_datas, args['date_beg'], args['date_end'], args['tpl_file'], args['filename'])

        if not ret:
            self.log.error(Logs.fileline() + ' : PdfBillList failed')
            try:
                details = {"reason": "PDF_FAILED", "filename": args.get("filename"), "tpl_file": args.get("tpl_file")}
                Audit.insertAudit(audit_user, "PdfBillList", "PDF", None, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : PdfBillList ERROR audit')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE PdfBillList')
        try:
            details = {"filename": args.get("filename"), "tpl_file": args.get("tpl_file")}
            Audit.insertAudit(audit_user, "PdfBillList", "PDF", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : PdfBillList ERROR audit success')
        return compose_ret('', Constants.cst_content_type_json)


class PdfInvoice(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self, id_rec, template, filename):
        audit_user = request.oauth_user
        tpl = Setting.getTemplateByFile(template)

        if not tpl:
            self.log.error(Logs.fileline() + ' : PdfInvoice template not found, template=%s', str(template))
            try:
                details = {"reason": "TEMPLATE_NOT_FOUND", "id_rec": int(id_rec), "template": str(template), "filename": str(filename)}
                Audit.insertAudit(audit_user, "PdfInvoice", "RECORD", int(id_rec), "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : PdfInvoice ERROR audit')
            return compose_ret(-1, Constants.cst_content_type_json, 500)

        ret = Pdf.getPdfInvoice(id_rec, template, filename)

        if not ret:
            self.log.error(Logs.fileline() + ' : PdfInvoice failed id_rec=%s', str(id_rec))
            try:
                details = {"reason": "PDF_FAILED", "id_rec": int(id_rec), "template": str(template), "filename": str(filename)}
                Audit.insertAudit(audit_user, "PdfInvoice", "RECORD", int(id_rec), "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : PdfInvoice ERROR audit')
            return compose_ret(-1, Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE PdfInvoice')
        try:
            details = {"id_rec": int(id_rec), "template": str(template), "filename": str(filename)}
            Audit.insertAudit(audit_user, "PdfInvoice", "RECORD", int(id_rec), "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : PdfInvoice ERROR audit success')
        return compose_ret(0, Constants.cst_content_type_json)


class PdfReport(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self, id_rec, template, filename, reedit='N', id_user=0):
        audit_user = request.oauth_user
        if reedit == 'Y':
            tpl = Setting.getTemplateByFile(template)

            id_tpl = 0

            if tpl:
                id_tpl = tpl['tpl_ser']

            ret = File.insertFileReport(id_owner=id_user,
                                        id_dos=id_rec,
                                        doc_type=257,
                                        id_tpl=id_tpl)

            if ret <= 0:
                self.log.error(Logs.fileline() + ' : PdfReport insertFileReport failed id_rec=%s', str(id_rec))
                try:
                    details = {"reason": "INSERT_FILE_FAILED", "id_rec": int(id_rec), "id_user": int(id_user), "template": str(template)}
                    Audit.insertAudit(audit_user, "PdfReport", "RECORD", int(id_rec), "ERROR", details, "R")
                except Exception:
                    self.log.exception(Logs.fileline() + ' : PdfReport ERROR audit')
                return compose_ret('', Constants.cst_content_type_json, 500)

            # Get uuid filename
            fileReport = File.getFileReport(id_rec)

            if fileReport:
                ret = Pdf.getPdfReport(id_rec, template, fileReport['file'], reedit)

                if not ret:
                    ret_del = File.deleteFileReportById(fileReport['id_data'])

                    if not ret_del:
                        self.log.error(Logs.fileline() + ' : PdfReport failed delete id_file=%s', str(fileReport['id_data']))

                    try:
                        details = {"reason": "PDF_FAILED_REEDIT", "id_rec": int(id_rec), "template": str(template), "id_file": int(fileReport.get('id_data', 0))}
                        Audit.insertAudit(audit_user, "PdfReport", "RECORD", int(id_rec), "ERROR", details, "R")
                    except Exception:
                        self.log.exception(Logs.fileline() + ' : PdfReport ERROR audit')
                    return compose_ret('', Constants.cst_content_type_json, 500)
            else:
                self.log.error(Logs.fileline() + ' : PdfReport failed id_rec=%s', str(id_rec))
                try:
                    details = {"reason": "FILE_NOT_FOUND", "id_rec": int(id_rec), "template": str(template)}
                    Audit.insertAudit(audit_user, "PdfReport", "RECORD", int(id_rec), "ERROR", details, "R")
                except Exception:
                    self.log.exception(Logs.fileline() + ' : PdfReport ERROR audit')
                return compose_ret('', Constants.cst_content_type_json, 500)
        else:
            ret = Pdf.getPdfReport(id_rec, template, filename, reedit)

        if not ret:
            self.log.error(Logs.fileline() + ' : PdfReport failed id_rec=%s', str(id_rec))
            try:
                details = {"reason": "PDF_FAILED", "id_rec": int(id_rec), "template": str(template), "filename": str(filename), "reedit": str(reedit)}
                Audit.insertAudit(audit_user, "PdfReport", "RECORD", int(id_rec), "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : PdfReport ERROR audit')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE PdfReport')
        try:
            details = {"id_rec": int(id_rec), "template": str(template), "filename": str(filename), "reedit": str(reedit)}
            Audit.insertAudit(audit_user, "PdfReport", "RECORD", int(id_rec), "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : PdfReport ERROR audit success')
        return compose_ret('', Constants.cst_content_type_json)


class PdfReportGeneric(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        if 'html' not in args or 'filename' not in args:
            self.log.error(Logs.fileline() + ' : PdfReportGeneric ERROR args missing')
            try:
                details = {"reason": "ARGS_MISSING", "missing": ["html", "filename"]}
                Audit.insertAudit(audit_user, "PdfReportGeneric", "PDF", None, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : PdfReportGeneric ERROR audit')
            return compose_ret('', Constants.cst_content_type_json, 400)

        ret = Pdf.getPdfReportGeneric(args['html'], args['filename'])

        if not ret:
            self.log.error(Logs.fileline() + ' : PdfReportGeneric failed')
            try:
                details = {"reason": "PDF_FAILED", "filename": str(args.get("filename"))}
                Audit.insertAudit(audit_user, "PdfReportGeneric", "PDF", None, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : PdfReportGeneric ERROR audit')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE PdfReportGeneric')
        try:
            details = {"filename": str(args.get("filename"))}
            Audit.insertAudit(audit_user, "PdfReportGeneric", "PDF", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : PdfReportGeneric ERROR audit success')
        return compose_ret('', Constants.cst_content_type_json)


class PdfReportGrouped(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        if 'l_id_rec_vld' not in args or 'filename' not in args:
            self.log.error(Logs.fileline() + ' : PdfReportGrouped ERROR args missing')
            try:
                details = {"reason": "ARGS_MISSING", "missing": ["l_id_rec_vld", "filename"]}
                Audit.insertAudit(audit_user, "PdfReportGrouped", "PDF", None, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : PdfReportGrouped ERROR audit')
            return compose_ret(-1, Constants.cst_content_type_json, 400)

        ret = Pdf.getPdfReportGrouped(args['filename'], args['l_id_rec_vld'])

        if not ret:
            self.log.error(Logs.fileline() + ' : PdfReportGrouped failed')
            try:
                details = {"reason": "PDF_FAILED", "filename": str(args.get("filename")),
                           "count": len(args.get("l_id_rec_vld") or [])}
                Audit.insertAudit(audit_user, "PdfReportGrouped", "PDF", None, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : PdfReportGrouped ERROR audit')
            return compose_ret(-1, Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE PdfReportGrouped')
        try:
            details = {"filename": str(args.get("filename")), "count": len(args.get("l_id_rec_vld") or [])}
            Audit.insertAudit(audit_user, "PdfReportGrouped", "PDF", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : PdfReportGrouped ERROR audit success')
        return compose_ret(0, Constants.cst_content_type_json)


class PdfReportGlobal(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        if 'exclu' not in args or 'date_beg' not in args or 'date_end' not in args or 'filename' not in args:
            self.log.error(Logs.fileline() + ' : PdfReportGlobal ERROR args missing')
            try:
                details = {"reason": "ARGS_MISSING"}
                Audit.insertAudit(audit_user, "PdfReportGlobal", "PDF", None, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : PdfReportGlobal ERROR audit')
            return compose_ret(-1, Constants.cst_content_type_json, 400)

        ret = Pdf.getPdfReportGlobal(args['filename'], args['exclu'], args['date_beg'], args['date_end'])

        if ret == 500:
            self.log.error(Logs.fileline() + ' : PdfReportGlobal failed')
            try:
                details = {"reason": "PDF_FAILED", "ret": 500, "filename": str(args.get("filename"))}
                Audit.insertAudit(audit_user, "PdfReportGlobal", "PDF", None, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : PdfReportGlobal ERROR audit')
            return compose_ret(-1, Constants.cst_content_type_json, 500)
        elif ret == 404:
            self.log.error(Logs.fileline() + ' : PdfReportGlobal failed')
            try:
                details = {"reason": "NOT_FOUND", "ret": 404, "date_beg": args.get("date_beg"), "date_end": args.get("date_end")}
                Audit.insertAudit(audit_user, "PdfReportGlobal", "PDF", None, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : PdfReportGlobal ERROR audit')
            return compose_ret(0, Constants.cst_content_type_json, 404)
        elif ret == 409:
            self.log.error(Logs.fileline() + ' : PdfReportGlobal failed partially')
            try:
                details = {"reason": "PARTIAL", "ret": 409, "filename": str(args.get("filename"))}
                Audit.insertAudit(audit_user, "PdfReportGlobal", "PDF", None, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : PdfReportGlobal ERROR audit')
            return compose_ret(0, Constants.cst_content_type_json, 409)

        self.log.info(Logs.fileline() + ' : TRACE PdfReportGlobal')
        try:
            details = {"filename": str(args.get("filename")), "exclu": str(args.get("exclu")),
                       "date_beg": args.get("date_beg"), "date_end": args.get("date_end")}
            Audit.insertAudit(audit_user, "PdfReportGlobal", "PDF", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : PdfReportGlobal ERROR audit success')
        return compose_ret(0, Constants.cst_content_type_json)


class PdfSticker(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self, template):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        if 'id' not in args or 'type_id' not in args:
            self.log.error(Logs.fileline() + ' : PdfSticker ERROR args missing')
            try:
                details = {"reason": "ARGS_MISSING", "template": str(template)}
                Audit.insertAudit(audit_user, "PdfSticker", "PDF", None, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : PdfSticker ERROR audit')
            return compose_ret(-1, Constants.cst_content_type_json, 400)

        ret = Pdf.getPdfSticker(args['id'], args['type_id'], template)

        if not ret:
            self.log.error(Logs.fileline() + ' : PdfSticker failed id=%s, type_id=%s, template=%s', Logs.clean(args['id']), Logs.clean(args['type_id']), Logs.clean(template))
            try:
                details = {"reason": "PDF_FAILED", "id": args.get("id"), "type_id": args.get("type_id"), "template": str(template)}
                Audit.insertAudit(audit_user, "PdfSticker", "PDF", None, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : PdfSticker ERROR audit')
            return compose_ret(-1, Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE PdfSticker')
        try:
            details = {"id": args.get("id"), "type_id": args.get("type_id"), "template": str(template)}
            Audit.insertAudit(audit_user, "PdfSticker", "PDF", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : PdfSticker ERROR audit success')
        return compose_ret(0, Constants.cst_content_type_json)


class PdfTemplate(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self, id_item):
        audit_user = request.oauth_user
        tpl = Setting.getTemplate(id_item)

        if not tpl:
            self.log.error(Logs.fileline() + ' : PdfTemplate failed get id_item=%s', str(id_item))
            try:
                details = {"reason": "GET_TEMPLATE_FAILED", "id_item": int(id_item)}
                Audit.insertAudit(audit_user, "PdfTemplate", "TEMPLATE", int(id_item), "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : PdfTemplate ERROR audit')
            return compose_ret(-1, Constants.cst_content_type_json, 500)

        if tpl['tpl_type'] == 'RES':
            ret = Pdf.getPdfReport(0, tpl['tpl_file'], 'test_template', 'N')
        elif tpl['tpl_type'] == 'STI':
            ret = Pdf.getPdfSticker(0, 'REC', tpl['tpl_file'])
        elif tpl['tpl_type'] == 'OUT':
            ret = Pdf.getPdfOutsourced(0, tpl['tpl_file'], 'test_template')
        elif tpl['tpl_type'] == 'INV':
            ret = Pdf.getPdfInvoice(0, tpl['tpl_file'], 'test_template')
        else:
            self.log.error(Logs.fileline() + ' : PdfTemplate failed unknow type=%s', str(tpl['tpl_type']))
            try:
                details = {"reason": "UNKNOWN_TYPE", "id_item": int(id_item), "tpl_type": str(tpl.get('tpl_type'))}
                Audit.insertAudit(audit_user, "PdfTemplate", "TEMPLATE", int(id_item), "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : PdfTemplate ERROR audit')
            return compose_ret(-1, Constants.cst_content_type_json, 500)

        if not ret:
            self.log.error(Logs.fileline() + ' : PdfTemplate print failed id=%s, type_id=%s, template=%s', str(tpl['tpl_ser']), tpl['tpl_type'], tpl['tpl_file'])
            try:
                details = {"reason": "PRINT_FAILED", "id_item": int(id_item), "tpl_ser": int(tpl.get('tpl_ser', 0)),
                           "tpl_type": str(tpl.get('tpl_type')), "tpl_file": str(tpl.get('tpl_file'))}
                Audit.insertAudit(audit_user, "PdfTemplate", "TEMPLATE", int(id_item), "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : PdfTemplate ERROR audit')
            return compose_ret(-1, Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE PdfTemplate')
        try:
            details = {"id_item": int(id_item), "tpl_ser": int(tpl.get('tpl_ser', 0)),
                       "tpl_type": str(tpl.get('tpl_type')), "tpl_file": str(tpl.get('tpl_file'))}
            Audit.insertAudit(audit_user, "PdfTemplate", "TEMPLATE", int(id_item), "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : PdfTemplate ERROR audit success')
        return compose_ret(0, Constants.cst_content_type_json)


class PdfOutsourced(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self, id_rec, template, filename):
        audit_user = request.oauth_user
        tpl = Setting.getTemplateByFile(template)

        if not tpl:
            self.log.error(Logs.fileline() + ' : PdfOutsourced template not found, template=%s', str(template))
            try:
                details = {"reason": "TEMPLATE_NOT_FOUND", "id_rec": int(id_rec), "template": str(template), "filename": str(filename)}
                Audit.insertAudit(audit_user, "PdfOutsourced", "RECORD", int(id_rec), "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : PdfOutsourced ERROR audit')
            return compose_ret('', Constants.cst_content_type_json, 500)

        ret = Pdf.getPdfOutsourced(id_rec, template, filename)

        if not ret:
            self.log.error(Logs.fileline() + ' : PdfOutsourced failed id_rec=%s', str(id_rec))
            try:
                details = {"reason": "PDF_FAILED", "id_rec": int(id_rec), "template": str(template), "filename": str(filename)}
                Audit.insertAudit(audit_user, "PdfOutsourced", "RECORD", int(id_rec), "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : PdfOutsourced ERROR audit')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE PdfOutsourced')
        try:
            details = {"id_rec": int(id_rec), "template": str(template), "filename": str(filename)}
            Audit.insertAudit(audit_user, "PdfOutsourced", "RECORD", int(id_rec), "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : PdfOutsourced ERROR audit success')
        return compose_ret('', Constants.cst_content_type_json)


class PdfReportToday(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        if 'date_beg' not in args or 'date_end' not in args or 'service_int' not in args or 'filename' not in args:
            self.log.error(Logs.fileline() + ' : PdfReportToday ERROR args missing')
            try:
                details = {"reason": "ARGS_MISSING", "missing": ["date_beg", "date_end", "service_int", "filename"]}
                Audit.insertAudit(audit_user, "PdfReportToday", "PDF", None, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : PdfReportToday ERROR audit')
            return compose_ret('', Constants.cst_content_type_json, 400)

        l_data = Report.getTodayList(args['date_beg'], args['date_end'], args['service_int'])

        # if no result to write
        if not l_data:
            try:
                details = {"reason": "NOT_FOUND", "date_beg": args.get("date_beg"), "date_end": args.get("date_end"),
                           "service_int": args.get("service_int")}
                Audit.insertAudit(audit_user, "PdfReportToday", "PDF", None, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : PdfReportToday ERROR audit')
            return compose_ret('', Constants.cst_content_type_json, 404)

        ret = Pdf.getPdfReportToday(l_data, args['date_beg'], args['date_end'], args['service_int'], args['filename'])

        if not ret:
            self.log.error(Logs.fileline() + ' : PdfReportToday getPdfReportToday failed')
            try:
                details = {"reason": "PDF_FAILED", "filename": args.get("filename")}
                Audit.insertAudit(audit_user, "PdfReportToday", "PDF", None, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : PdfReportToday ERROR audit')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE PdfReportToday')
        try:
            details = {"filename": args.get("filename"), "date_beg": args.get("date_beg"), "date_end": args.get("date_end"),
                       "service_int": args.get("service_int"), "count": len(l_data) if l_data else 0}
            Audit.insertAudit(audit_user, "PdfReportToday", "PDF", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : PdfReportToday ERROR audit success')
        return compose_ret('', Constants.cst_content_type_json)


class PdfActivityReport(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        if ('date_beg' not in args or 'date_end' not in args or 'type_ana' not in args or 'tpl_file' not in args or
           'filename' not in args):
            self.log.error(Logs.fileline() + ' : PdfActivityReport missing args')
            try:
                details = {"reason": "ARGS_MISSING"}
                Audit.insertAudit(audit_user, "PdfActivityReport", "PDF", None, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : PdfActivityReport ERROR audit')
            return compose_ret('', Constants.cst_content_type_json, 400)

        date_beg = args['date_beg']
        date_end = args['date_end']
        type_ana = args['type_ana']
        tpl_file = args['tpl_file']
        filename = args['filename']

        stat_type = Report.getActivityType(date_beg, date_end, type_ana)
        if not stat_type:
            self.log.error(Logs.fileline() + ' : stat_type empty')
            stat_type = []

        Various.useLangDB()

        try:
            type_ana_int = int(type_ana)
        except Exception:
            type_ana_int = 0

        family_label = ''
        if type_ana_int > 0:
            dico_row = Various.getDicoById(type_ana_int)
            if dico_row:
                family_label = dico_row['label']

        for row in stat_type:
            ana = row.get('analysis') or ''
            row['analysis'] = _(ana.strip())

        stat_age = Report.getActivityAge(date_beg, date_end, type_ana)
        if not stat_age:
            self.log.error(Logs.fileline() + ' : stat_age empty')
            stat_age = []

        Various.useLangDB()
        for row in stat_age:
            ana = row.get('analysis') or ''
            row['analysis'] = _(ana.strip())

            unit = row.get('unite')
            age  = row.get('age')
            if age is not None:
                if unit == 1034:
                    row['age'] = int(age // 365)
                elif unit == 1035:
                    row['age'] = int(age // 52)
                elif unit == 1036:
                    row['age'] = int(age // 12)

        for row in stat_type:
            for k, v in list(row.items()):
                if v is None:
                    row[k] = ''

        for row in stat_age:
            for k, v in list(row.items()):
                if v is None:
                    row[k] = ''

        ret = Pdf.getPdfActivityReport(stat_type, stat_age, date_beg, date_end, tpl_file, filename, family_label)
        if not ret:
            self.log.error(Logs.fileline() + ' : getPdfActivityReport failed')
            try:
                details = {"reason": "PDF_FAILED", "date_beg": date_beg, "date_end": date_end, "type_ana": type_ana,
                           "tpl_file": tpl_file, "filename": filename}
                Audit.insertAudit(audit_user, "PdfActivityReport", "PDF", None, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : PdfActivityReport ERROR audit')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : PdfActivityReport ok')
        try:
            details = {"date_beg": date_beg, "date_end": date_end, "type_ana": type_ana, "tpl_file": tpl_file,
                       "filename": filename, "count_type": len(stat_type), "count_age": len(stat_age)}
            Audit.insertAudit(audit_user, "PdfActivityReport", "PDF", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : PdfActivityReport ERROR audit success')
        return compose_ret('', Constants.cst_content_type_json)


class PrintByScript(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self, script_name):
        audit_user = request.oauth_user
        # args = request.get_json() or {}

        # TODO get args for script

        cmd = ('sh ' + Constants.cst_printer + '/' + script_name + ' > ' + Constants.cst_io + 'print.out 2>&1 &')

        self.log.error(Logs.fileline() + ' : PrintByScript cmd=' + cmd)
        ret = os.system(cmd)

        self.log.info(Logs.fileline() + ' : TRACE PrintByScript ret =' + str(ret))
        status = "SUCCESS" if int(ret) == 0 else "ERROR"
        try:
            details = {"script_name": str(script_name), "ret": int(ret)}
            Audit.insertAudit(audit_user, "PrintByScript", "PDF", None, status, details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : PrintByScript ERROR audit success')
        return compose_ret('', Constants.cst_content_type_json)
