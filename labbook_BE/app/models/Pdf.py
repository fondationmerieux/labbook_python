# -*- coding:utf-8 -*-
import logging
import mysql.connector
import barcode

from barcode.writer import ImageWriter

from app.models.DB import DB
from app.models.Logs import Logs
from app.models.Constants import Constants


class Pdf:
    log = logging.getLogger('log_db')

    @staticmethod
    def getPdfBarcode(num):
        try:
            checksum = False

            CODE39 = barcode.get_barcode_class('code39')

            options ={'font_size': 10, 'text_distance':1.0}
            options['center_text'] = True

            ean = CODE39(str(num), writer=ImageWriter(), add_checksum=checksum)
            ean.save('tmp/etiquette_' + num, options=options)
        except Exception as err:
            Pdf.log.error(Logs.fileline() + ' : getPdfBarcode failed, err=%s , num=%s', err, str(num))
            return False

        return True
