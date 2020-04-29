# -*- coding:utf-8 -*-
import logging

from flask_restful import Resource

from app.models.General import compose_ret
from app.models.Constants import *
from app.models.Pdf import *
from app.models.Logs import Logs


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
        ret = Pdf.getPdfBill(id_rec)

        if not ret:
            self.log.error(Logs.fileline() + ' : PdfBill failed num=%s', str(num))
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE PdfBill')
        return compose_ret('', Constants.cst_content_type_json)
