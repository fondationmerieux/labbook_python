# -*- coding:utf-8 -*-
import logging

from flask_restful import Resource

from app.models.General import compose_ret
from app.models.Constants import *
from app.models.Pdf import *
from app.models.Logs import Logs
from app.models.Record import *


class PdfBarcode(Resource):
    log = logging.getLogger('log_services')

    def get(self, num):
        ret = Pdf.getPdfBarcode(num)

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


class PdfReport(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_rec, filename):
        ret = Pdf.getPdfReport(id_rec, filename)

        if not ret:
            self.log.error(Logs.fileline() + ' : PdfReport failed id_rec=%s', str(id_rec))
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE PdfReport')
        return compose_ret('', Constants.cst_content_type_json)
