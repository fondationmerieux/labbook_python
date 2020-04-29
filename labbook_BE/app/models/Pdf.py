# -*- coding:utf-8 -*-
import logging
import mysql.connector
import barcode
import pdfkit

from barcode.writer import ImageWriter

from app.models.DB import DB
from app.models.Logs import Logs
from app.models.Constants import Constants
from app.models.Record import Record
from app.models.Various import Various


class Pdf:
    log = logging.getLogger('log_db')

    @staticmethod
    def getPdfBarcode(num):
        try:
            checksum = False

            CODE39 = barcode.get_barcode_class('code39')

            options = {'font_size': 10, 'text_distance': 1.0}
            options['center_text'] = True

            ean = CODE39(str(num), writer=ImageWriter(), add_checksum=checksum)
            ean.save('tmp/etiquette_' + num, options=options)
        except Exception as err:
            Pdf.log.error(Logs.fileline() + ' : getPdfBarcode failed, err=%s , num=%s', err, str(num))
            return False

        return True

    @staticmethod
    def getPdfBill(id_rec):
        path = 'tmp/'

        # Get record details
        record = Record.getRecord(id_rec)

        num_rec_y = record['num_dos_an']

        page_header = Pdf.getPdfHeader()
        page_body   = ''
        page_footer = '</div>'

        filename = 'facture_' + num_rec_y + '.pdf'

        form_cont = page_header + page_body + page_footer

        options = {'--encoding': 'utf-8',
                   'page-size': 'A4',
                   'margin-top': '100.00mm',
                   'margin-right': '100.00mm',
                   'margin-bottom': '100.00mm',
                   'margin-left': '100.00mm',
                   'no-outline': None}

        pdfkit.from_string(form_cont, path + filename, options=options)

        return True

    @staticmethod
    def getPdfHeader():
        header = """<div style='padding:0px;width:1000px;height:1400px;border:0px;font-family:arial;background-color:#AAA;color:black;font-size:20px;'>"""

        head_logo = ''

        head_name  = Various.getDefaultValue('entete_1')
        head_line2 = Various.getDefaultValue('entete_2')
        head_line3 = Various.getDefaultValue('entete_3')
        head_addr  = Various.getDefaultValue('entete_adr')
        head_phone = Various.getDefaultValue('entete_tel')
        head_fax   = Various.getDefaultValue('entete_fax')
        head_email = Various.getDefaultValue('entete_email')

        header += """\
                <div><span>""" + head_name['value'] + """</span></div>
                <div><span>""" + head_line2['value'] + """</span></div>
                <div><span>""" + head_line3['value'] + """</span></div>
                <div><span>""" + head_addr['value'] + """</span></div>
                <div><span>""" + head_phone['value'] + """</span><span>""" + head_fax['value'] + """</span><span>""" + head_email['value'] + """</span></div>"""

        return header
