# -*- coding:utf-8 -*-
import logging

from flask import request
from flask_restful import Resource

from app.models.General import compose_ret
from app.models.Constants import *
from app.models.Pdf import *
from app.models.Logs import Logs
from app.models.Record import *
from app.models.Report import *


class PdfBarcode(Resource):
    log = logging.getLogger('log_services')

    def get(self, num):
        ret = Pdf.getPdfBarcode(num)

        if not ret:
            self.log.error(Logs.fileline() + ' : PdfBarcode failed num=%s', str(num))
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE PdfBarcode')
        return compose_ret('', Constants.cst_content_type_json)

    def post(self, num):
        args = request.get_json()

        if 'sts_width' not in args or 'sts_height' not in args or \
           'sts_margin_top' not in args or 'sts_margin_bottom' not in args or \
           'sts_margin_left' not in args or 'sts_margin_right' not in args:
            self.log.error(Logs.fileline() + ' : PdfBarcode ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        ret = Pdf.getPdfBarcode(num, args)

        if not ret:
            self.log.error(Logs.fileline() + ' : PdfBarcode failed num=%s', str(num))
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE PdfBarcode')
        return compose_ret('', Constants.cst_content_type_json)


class PdfBill(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_rec):
        # if any bill number in DB then insert a new one
        record = Record.getRecord(id_rec)

        if not record:
            self.log.error(Logs.fileline() + ' : PdfBill get record failed id_rec=%s', str(id_rec))
            return compose_ret('', Constants.cst_content_type_json, 500)

        if not record['num_fact']:
            ret = Record.generateBillNumber(id_rec)

            if not ret:
                self.log.error(Logs.fileline() + ' : PdfBill bill number failed id_rec=%s', str(id_rec))
                return compose_ret('', Constants.cst_content_type_json, 500)

        ret = Pdf.getPdfBill(id_rec)

        if not ret:
            self.log.error(Logs.fileline() + ' : PdfBill failed id_rec=%s', str(id_rec))
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE PdfBill')
        return compose_ret('', Constants.cst_content_type_json)


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
            for key, value in data.items():
                if data[key] is None:
                    data[key] = ''

        ret = Pdf.getPdfBillList(l_datas, args['date_beg'], args['date_end'])

        if not ret:
            self.log.error(Logs.fileline() + ' : PdfBillList failed')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE PdfBillList')
        return compose_ret('', Constants.cst_content_type_json)


class PdfReport(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_rec, filename):
        ret = Pdf.getPdfReport(id_rec, filename)

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
