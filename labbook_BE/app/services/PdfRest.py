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
        try:
            ret = Pdf.getPdfBarcode(num)

            if not ret:
                self.log.error(Logs.fileline() + ' : PdfBarcode failed num=%s', str(num))
                return compose_ret('', Constants.cst_content_type_json, 500)

        except Exception as err:
            self.log.error(Logs.fileline() + ' : PdfBarcode failed, err=%s , num=%s', err, str(num))
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE PdfBarcode')
        return compose_ret('', Constants.cst_content_type_json)
