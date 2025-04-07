# -*- coding:utf-8 -*-
import logging
import gettext
import os

from flask import request
from flask_restful import Resource

from app.models.General import compose_ret
from app.models.Constants import *
from app.models.Pdf import *
from app.models.Logs import Logs
from app.models.Record import *
from app.models.Report import *


class PdfBillList(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        if 'date_beg' not in args or 'date_end' not in args:
            self.log.error(Logs.fileline() + ' : PdfBillList ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        l_datas = Report.getBillingStatus(args['date_beg'], args['date_end'], 0)

        if not l_datas:
            self.log.error(Logs.fileline() + ' : TRACE list current billing not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        for data in l_datas:
            for key, value in list(data.items()):
                if data[key] is None:
                    data[key] = ''

        ret = Pdf.getPdfBillList(l_datas, args['date_beg'], args['date_end'])

        if not ret:
            self.log.error(Logs.fileline() + ' : PdfBillList failed')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE PdfBillList')
        return compose_ret('', Constants.cst_content_type_json)


class PdfInvoice(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_rec, template, filename):
        tpl = Setting.getTemplateByFile(template)

        if not tpl:
            self.log.error(Logs.fileline() + ' : PdfInvoice template not found, template=%s', str(template))
            return compose_ret(-1, Constants.cst_content_type_json, 500)

        ret = Pdf.getPdfInvoice(id_rec, template, filename)

        if not ret:
            self.log.error(Logs.fileline() + ' : PdfInvoice failed id_rec=%s', str(id_rec))
            return compose_ret(-1, Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE PdfInvoice')
        return compose_ret(0, Constants.cst_content_type_json)


class PdfReport(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_rec, template, filename, reedit='N', id_user=0):
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
                return compose_ret('', Constants.cst_content_type_json, 500)

            # Get uuid filename
            fileReport = File.getFileReport(id_rec)

            if fileReport:
                ret = Pdf.getPdfReport(id_rec, template, fileReport['file'], reedit)

                if not ret:
                    ret_del = File.deleteFileReportById(fileReport['id_data'])

                    if not ret_del:
                        self.log.error(Logs.fileline() + ' : PdfReport failed delete id_file=%s', str(fileReport['id_data']))
                    return compose_ret('', Constants.cst_content_type_json, 500)
            else:
                self.log.error(Logs.fileline() + ' : PdfReport failed id_rec=%s', str(id_rec))
                return compose_ret('', Constants.cst_content_type_json, 500)
        else:
            ret = Pdf.getPdfReport(id_rec, template, filename, reedit)

        if not ret:
            self.log.error(Logs.fileline() + ' : PdfReport failed id_rec=%s', str(id_rec))
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE PdfReport')
        return compose_ret('', Constants.cst_content_type_json)


class PdfReportGeneric(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        if 'html' not in args or 'filename' not in args:
            self.log.error(Logs.fileline() + ' : PdfReportGeneric ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        ret = Pdf.getPdfReportGeneric(args['html'], args['filename'])

        if not ret:
            self.log.error(Logs.fileline() + ' : PdfReportGeneric failed id_rec=%s', str(id_rec))
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE PdfReportGeneric')
        return compose_ret('', Constants.cst_content_type_json)


class PdfReportGrouped(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        if 'l_id_rec_vld' not in args or 'filename' not in args:
            self.log.error(Logs.fileline() + ' : PdfReportGrouped ERROR args missing')
            return compose_ret(-1, Constants.cst_content_type_json, 400)

        ret = Pdf.getPdfReportGrouped(args['filename'], args['l_id_rec_vld'])

        if not ret:
            self.log.error(Logs.fileline() + ' : PdfReportGrouped failed')
            return compose_ret(-1, Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE PdfReportGrouped')
        return compose_ret(0, Constants.cst_content_type_json)


class PdfReportGlobal(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        if 'exclu' not in args or 'date_beg' not in args or 'date_end' not in args or 'filename' not in args:
            self.log.error(Logs.fileline() + ' : PdfReportGlobal ERROR args missing')
            return compose_ret(-1, Constants.cst_content_type_json, 400)

        ret = Pdf.getPdfReportGlobal(args['filename'], args['exclu'], args['date_beg'], args['date_end'])

        if ret == 500:
            self.log.error(Logs.fileline() + ' : PdfReportGlobal failed')
            return compose_ret(-1, Constants.cst_content_type_json, 500)
        elif ret == 404:
            self.log.error(Logs.fileline() + ' : PdfReportGlobal failed')
            return compose_ret(0, Constants.cst_content_type_json, 404)
        elif ret == 409:
            self.log.error(Logs.fileline() + ' : PdfReportGlobal failed partially')
            return compose_ret(0, Constants.cst_content_type_json, 409)

        self.log.info(Logs.fileline() + ' : TRACE PdfReportGlobal')
        return compose_ret(0, Constants.cst_content_type_json)


class PdfSticker(Resource):
    log = logging.getLogger('log_services')

    def post(self, template):
        args = request.get_json()

        if 'id' not in args or 'type_id' not in args:
            self.log.error(Logs.fileline() + ' : PdfSticker ERROR args missing')
            return compose_ret(-1, Constants.cst_content_type_json, 400)

        ret = Pdf.getPdfSticker(args['id'], args['type_id'], template)

        if not ret:
            self.log.error(Logs.fileline() + ' : PdfSticker failed id=%s, type_id=%s, template=%s', str(args['id']), args['type_id'], template)
            return compose_ret(-1, Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE PdfSticker')
        return compose_ret(0, Constants.cst_content_type_json)


class PdfTemplate(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_item):
        tpl = Setting.getTemplate(id_item)

        if not tpl:
            self.log.error(Logs.fileline() + ' : PdfTemplate failed get id_item=%s', str(id_item))
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
            return compose_ret(-1, Constants.cst_content_type_json, 500)

        if not ret:
            self.log.error(Logs.fileline() + ' : PdfTemplate print failed id=%s, type_id=%s, template=%s', str(tpl['tpl_ser']), tpl['tpl_type'], tpl['tpl_file'])
            return compose_ret(-1, Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE PdfTemplate')
        return compose_ret(0, Constants.cst_content_type_json)


class PdfOutsourced(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_rec, template, filename):
        tpl = Setting.getTemplateByFile(template)

        if not tpl:
            self.log.error(Logs.fileline() + ' : PdfOutsourced template not found, template=%s', str(template))
            return compose_ret('', Constants.cst_content_type_json, 500)

        ret = Pdf.getPdfOutsourced(id_rec, template, filename)

        if not ret:
            self.log.error(Logs.fileline() + ' : PdfOutsourced failed id_rec=%s', str(id_rec))
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE PdfOutsourced')
        return compose_ret('', Constants.cst_content_type_json)


class PdfReportToday(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        if 'date_beg' not in args or 'date_end' not in args or 'service_int' not in args or 'filename' not in args:
            self.log.error(Logs.fileline() + ' : PdfReportToday ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        l_data = Report.getTodayList(args['date_beg'], args['date_end'], args['service_int'])

        # if no result to write
        if not l_data:
            return compose_ret('', Constants.cst_content_type_json, 404)

        ret = Pdf.getPdfReportToday(l_data, args['date_beg'], args['date_end'], args['service_int'], args['filename'])

        if not ret:
            self.log.error(Logs.fileline() + ' : PdfReportToday getPdfReportToday failed')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE PdfReportToday')
        return compose_ret('', Constants.cst_content_type_json)


class PrintByScript(Resource):
    log = logging.getLogger('log_services')

    def post(self, script_name):
        args = request.get_json()

        # TODO get args for script

        cmd = ('sh ' + Constants.cst_printer + '/' + script_name + ' > ' + Constants.cst_io + 'print.out 2>&1 &')

        self.log.error(Logs.fileline() + ' : PrintByScript cmd=' + cmd)
        ret = os.system(cmd)

        self.log.info(Logs.fileline() + ' : TRACE PrintByScript')
        return compose_ret('', Constants.cst_content_type_json)
