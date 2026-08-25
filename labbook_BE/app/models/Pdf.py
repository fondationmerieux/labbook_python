# -*- coding:utf-8 -*-
import os
import logging
import barcode
import pdfkit
import pikepdf
import qrcode

from barcode.writer import ImageWriter
from contextlib import ExitStack
from datetime import datetime
from io import BytesIO
from relatorio.templates.opendocument import Template
from decimal import Decimal

from app.models.Analysis import Analysis
from app.models.DB import DB
from app.models.Logs import Logs
from app.models.Constants import Constants
from app.models.File import File
from app.models.General import *
from app.models.Patient import Patient
from app.models.Product import Product
from app.models.Record import Record
from app.models.Result import Result
from app.models.Setting import Setting
from app.models.Various import Various
from app.models.User import User


class Pdf:
    log = logging.getLogger('log_db')

    @staticmethod
    def getPdfBillList(l_datas, date_beg, date_end, tpl_file, filename):
        """Build a PDF bill list

        This function is call by report billing template

        Args:
            l_datas       (json): Billing datas.
            date_beg  (datetime): Start date of the period.
            date_end  (datetime): End date of the period.
            tpl_file    (string): name of template file.
            filename    (string): name of file to build.

        Returns:
            bool: True for success, False otherwise.

        """

        Pdf.log.info(Logs.fileline() + ' : DEBUG-TRACE billing status datas : ' + str(l_datas))

        Various.useLangPDF()

        # convert l_datas to data for template
        data = {}  # dictionnary of data for build Billing status document

        # === Logo details ===
        filepath = os.path.join(Constants.cst_resource, 'logo.png')

        with open(filepath, 'rb') as fh:
            data['logo'] = (fh.read(), 'image/png')

        # === Label details ===
        data['label'] = {}

        data['label']['phone']   = str(_("Tél"))
        data['label']['fax']     = str(_("Fax"))
        data['label']['email']   = str(_("Email"))
        data['label']['edit']    = str(_("édité le"))
        data['label']['total']   = str(_("Total"))
        data['label']['total_remain'] = str(_("Total à payer"))
        data['label']['billing_status'] = str(_("État de la facturation"))
        data['label']['from_']    = str(_("du"))
        data['label']['to_']      = str(_("au"))
        data['label']['rec_num'] = str(_("N° dossier"))
        data['label']['receipt_num'] = str(_("N° quittance"))
        data['label']['bill_num'] = str(_("N° facture"))
        data['label']['price'] = str(_("Prix"))
        data['label']['remain'] = str(_("A payer"))

        # === Laboratory details ===
        data['lab'] = {}

        name  = Various.getDefaultValue('entete_1')
        line2 = Various.getDefaultValue('entete_2')
        line3 = Various.getDefaultValue('entete_3')
        addr  = Various.getDefaultValue('entete_adr')
        phone = Various.getDefaultValue('entete_tel')
        fax   = Various.getDefaultValue('entete_fax')
        email = Various.getDefaultValue('entete_email')

        data['lab']['name']  = str(name['value'])
        data['lab']['head2'] = str(line2['value'])
        data['lab']['head3'] = str(line3['value'])
        data['lab']['addr']  = str(addr['value'])
        data['lab']['phone'] = ''
        data['lab']['fax']   = ''
        data['lab']['email'] = ''

        if phone['value']:
            data['lab']['phone'] = str(phone['value'])

        if fax['value']:
            data['lab']['fax'] = str(fax['value'])

        if email['value']:
            data['lab']['email'] = str(email['value'])

        # === Billing status details ===
        data['bill'] = {}

        data['bill']['title']    = str(_("État de la facturation"))
        data['bill']['date_now'] = datetime.strftime(datetime.now(), Constants.cst_date_eu)
        data['bill']['time_now'] = datetime.strftime(datetime.now(), Constants.cst_time_HM)
        data['bill']['date_beg'] = str(date_beg).split('T', 1)[0].split(' ', 1)[0]
        data['bill']['date_end'] = str(date_end).split('T', 1)[0].split(' ', 1)[0]

        # === Data billing status ===
        total_price  = Decimal('0.00')
        total_remain = Decimal('0.00')

        data['l_data'] = []

        for bill in l_datas:
            price_dec  = Decimal(str(bill.get('bill_price') or 0))
            remain_dec = Decimal(str(bill.get('bill_remain') or 0))

            tmp_bill = {
                "rec_num":     bill.get('rec_num', '') or '',
                "receipt_num": bill.get('receipt_num', '') or '',
                "bill_num":    bill.get('bill_num', '') or '',
                "bill_price":  f"{price_dec:.2f}",
                "bill_remain": f"{remain_dec:.2f}",
            }

            total_price  += price_dec
            total_remain += remain_dec

            data['l_data'].append(tmp_bill)

        data['bill']['bill_total']  = f"{total_price:.2f}"
        data['bill']['bill_remain'] = f"{total_remain:.2f}"

        ret = Pdf.buildPdf('BIL', tpl_file, filename, data)

        if not ret:
            Pdf.log.error(Logs.fileline() + ' : getPdfBillList ERROR buildPdf')
            return False

        return True

    @staticmethod
    def getPdfReportGeneric(html_part, filename=''):
        """Build a Generic PDF Report

        This function is call by report statistic, report epidemio, report indicator, report activity,
        enter result and list result templates

        Args:
            html_part (string): html string.
            filename  (string): filename.

        Returns:
            bool: True for success, False otherwise.

        """

        path = Constants.cst_path_tmp

        date_now = datetime.now()
        today    = date_now.strftime(Constants.cst_date_ymd)

        filename = filename + '_' + today + '.pdf'

        # Get format header
        pdfpref = Pdf.getPdfPref()

        full_header = True

        if pdfpref and pdfpref['entete'] == 1069:
            full_header = False

        page_header = Pdf.getPdfHeader(full_header)

        page_body = ('<div style="width:1000px;">' + html_part + '</div>')

        page_footer = '</div>'

        form_cont = page_header + page_body + page_footer

        options = {'--encoding': 'utf-8',
                   'page-size': 'A4',
                   'margin-top': '12mm',
                   'margin-right': '0mm',
                   'margin-bottom': '0mm',
                   'margin-left': '0mm',
                   'no-outline': None,
                   'enable-local-file-access': None,
                   'load-error-handling': 'ignore',
                   'load-media-error-handling': 'ignore',
                   'disable-javascript': None}

        try:
            pdfkit.from_string(form_cont, path + filename, options=options)
        except Exception:
            Pdf.log.exception("ERROR PDF pdfkit.from_string failed")
            return False

        return True

    @staticmethod
    def getPdfReportToday(l_data, date_beg, date_end, service_int, filename):
        """Build a Today PDF Report

        This function is call by report today,

        Args:
            l_data        (json): Today datas.
            date_beg  (datetime): Start date of the period.
            date_end  (datetime): End date of the period.
            service_int (string): label of internal service.
            filename    (string): filename.

        Returns:
            bool: True for success, False otherwise.

        """

        Various.useLangPDF()

        html_part = '<p>' + str(date_beg) + ' - ' + str(date_end) + '&nbsp;&nbsp;&nbsp;' + str(service_int) + '</p>'
        html_part += ('<table class="table table-striped table-hover col-lg-12 table-lbk"><thead><tr>'
                      '<th class="text-start"><span>' + _("Date") + '</span></th>'
                      '<th class="text-start"><span>' + _("N° dossier") + '</span></th>'
                      '<th class="text-start"><span>' + _("Famille") + '</span></th>'
                      '<th class="text-start"><span>' + _("Analyse") + '</span></th>'
                      '<th class="text-start"><span>' + _("Validation") + '</span></th></tr></thead>'
                      '<tbody id="tbody_today" style="">')

        for data in l_data:
            html_part += ('<tr><td><div class="text-start">' + str(data['rec_date']) + '</div></td>'
                          '<td><div class="text-start">' + str( data['rec_num']) + '</div></td>'
                          '<td><div class="text-start">' + str(data['family']) + '</div></td>'
                          '<td><div class="text-start">' + str(data['analysis']) + '</div></td>'
                          '<td><div class="text-start">' + str(data['vld_type']) + '</div></td></tr>')

        html_part += '</tbody></table>'

        path = Constants.cst_path_tmp

        date_now = datetime.now()
        today    = date_now.strftime(Constants.cst_date_ymd)

        filename = filename + '_' + today + '.pdf'

        # Get format header
        pdfpref = Pdf.getPdfPref()

        full_header = True

        if pdfpref and pdfpref['entete'] == 1069:
            full_header = False

        page_header = Pdf.getPdfHeader(full_header)

        page_body = ('<div style="width:1000px;">' + html_part + '</div>')

        page_footer = '</div>'

        form_cont = page_header + page_body + page_footer

        options = {'--encoding': 'utf-8',
                   'page-size': 'A4',
                   'margin-top': '12mm',
                   'margin-right': '0mm',
                   'margin-bottom': '0mm',
                   'margin-left': '0mm',
                   'no-outline': None,
                   'enable-local-file-access': None,
                   'load-error-handling': 'ignore',
                   'load-media-error-handling': 'ignore',
                   'disable-javascript': None}

        try:
            pdfkit.from_string(form_cont, path + filename, options=options)
        except Exception:
            Pdf.log.exception("ERROR PDF pdfkit.from_string failed")
            return False

        return True

    @staticmethod
    def getPdfReportGrouped(filename, l_id_rec):
        """Build a Grouped PDF Report

        This function is call by biological-validationin group mode

        Args:
            l_id_rec   (array): list of id of record.
            filename  (string): filename.

        Returns:
            bool: True for success, False otherwise.

        """

        path = Constants.cst_path_tmp

        l_file_rec = []

        for id_rec in l_id_rec:
            report = File.getFileReport(id_rec)

            if not report:
                Pdf.log.error(Logs.fileline() + ' : TRACE getPdfReportGrouped report not found, id_rec=' + str(id_rec))
                continue

            # increase nb_download
            if not File.raiseReportNbDL(report['file']):
                Pdf.log.error(Logs.fileline() + ' : TRACE getPdfReportGrouped raise nb_download, id_rec=' + str(id_rec))

            l_file_rec.append(report['file'])

        if l_file_rec:
            try:
                # merge list of file in one PDF
                pdf = pikepdf.Pdf.new()

                # sources stay open until the save, then the stack closes them all
                with ExitStack() as stack:
                    for file_rec in l_file_rec:
                        filepath = os.path.join(Constants.cst_report, file_rec)
                        src = stack.enter_context(pikepdf.Pdf.open(filepath))
                        pdf.pages.extend(src.pages)

                    filepath = os.path.join(path, filename)

                    pdf.save(filepath)
            except Exception as err:
                Pdf.log.error(Logs.fileline() + ' : getPdfReportGrouped failed, err=%s', err)
                return False
        else:
            return False

        return True

    @staticmethod
    def getPdfReportGlobal(filename, exclu, date_beg, date_end):
        """Build a Grouped PDF Report

        This function is call by biological-validationin group mode

        Args:
            exclu     (string): O/N exclude report already donwloaded
            date_beg  (string): yyyy-mm-dd for the begin of the interval
            date_end  (string): yyyy-mm-dd for the end of the interval

        Returns:
            bool: True for success, False otherwise.

        """

        path = Constants.cst_path_tmp

        l_file_rec = []
        missing = 0

        l_id_rec = Record.getRecordListGlobal(date_beg, date_end)

        for id_rec in l_id_rec:
            report = File.getFileReport(id_rec['id_rec'])

            if not report:
                Pdf.log.error(Logs.fileline() + ' : TRACE getPdfReportGlobal report not found, id_rec=' + str(id_rec['id_rec']))
                continue

            if exclu == 'N' or (exclu == 'O' and report['nb_download'] == 0):
                # increase nb_download
                if not File.raiseReportNbDL(report['file']):
                    Pdf.log.error(Logs.fileline() + ' : TRACE getPdfReportGlobal raise nb_download, id_rec=' + str(id_rec['id_rec']))

                l_file_rec.append(report['file'])

        if l_file_rec:
            try:
                # merge list of file in one PDF
                pdf = pikepdf.Pdf.new()

                # sources stay open until the save, then the stack closes them all
                with ExitStack() as stack:
                    for file_rec in l_file_rec:
                        filepath = os.path.join(Constants.cst_report, file_rec)
                        # test if file exist
                        if os.path.exists(filepath) and os.stat(filepath).st_size > 0:
                            src = stack.enter_context(pikepdf.Pdf.open(filepath))
                            pdf.pages.extend(src.pages)
                        else:
                            missing += 1

                    filepath = os.path.join(path, filename)

                    pdf.save(filepath)
            except Exception as err:
                Pdf.log.error(Logs.fileline() + ' : getPdfReportGlobal failed, err=%s', err)
                return 500
        else:
            return 404

        if missing > 0:
            return 409

        return 200

    @staticmethod
    def getPdfHeader(full_header, report_status='&nbsp;'):
        """Start HTML page for PDF document

        This function is call by ??? template

        Args:
            full_header     (bool): full header or not.
            report_status (string): status of report (optional).

        Returns:
            bool: True for success, False otherwise.

        """

        Various.useLangPDF()

        # Width 47px <=> 1cm, Height 47px <=> 1cm
        header = """\
                <style>
                .ft_lab_name
                {
                font        : 26px Helvetica;
                font-weight : normal;
                font-style  : normal;
                }

                .ft_header
                {
                font        : 15px Helvetica;
                font-weight : normal;
                font-style  : normal;
                }

                .ft_bill_num
                {
                font        : 26px Helvetica;
                font-weight : bold;
                font-style  : normal;
                }

                .ft_bill_rec
                {
                font        : 18px Helvetica;
                font-weight : normal;
                font-style  : normal;
                }

                .ft_rec_det
                {
                font        : 15px Helvetica;
                font-weight : normal;
                font-style  : normal;
                }

                .ft_pat_ident
                {
                font        : 20px Helvetica;
                font-weight : bold;
                font-style  : normal;
                }

                .ft_pat_addr
                {
                font        : 15px Helvetica;
                font-weight : normal;
                font-style  : normal;
                }

                .ft_bill_det_tit
                {
                font        : 15px Helvetica;
                font-weight : bold;
                font-style  : normal;
                }

                .ft_bill_det
                {
                font        : 18px Courier;
                font-weight : normal;
                font-style  : normal;
                }

                .ft_bill_det_tot
                {
                font        : 18px Courier;
                font-weight : bold;
                font-style  : normal;
                }

                .ft_report_tit
                {
                font        : 20px Courier;
                font-weight : bold;
                font-style  : normal;
                }

                .ft_cat_tit
                {
                font        : 13px Courier;
                font-weight : normal;
                font-style  : normal;
                }

                .ft_res_fam
                {
                font        : 26px Helvetica;
                font-weight : bold;
                font-style  : normal;
                }

                .ft_res_name
                {
                font        : 18px Helvetica;
                font-weight : bold;
                font-style  : normal;
                }

                .ft_res_label
                {
                font        : 18px Courier;
                font-weight : normal;
                font-style  : normal;
                }

                .ft_res_value
                {
                font        : 18px Courier;
                font-weight : normal;
                font-style  : normal;
                }

                .ft_res_ref
                {
                font        : 16px Courier;
                font-weight : normal;
                font-style  : normal;
                }

                .ft_res_prev
                {
                font        : 15px Courier;
                font-weight : normal;
                font-style  : italic;
                }

                .ft_res_comm
                {
                font        : 18px Courier;
                font-weight : normal;
                font-style  : italic;
                }

                .ft_res_valid
                {
                font        : 18px Courier;
                font-weight : normal;
                font-style  : italic;
                }

                .ft_footer
                {
                font        : 18px Courier;
                font-weight : normal;
                font-style  : italic;
                }
                </style>
                <div style='padding-top:0px;padding-left:50px;padding-right:50px;padding-bottom:50px;width:1000px;height:1410px;border:0px;font-family:arial;background-color:#FFF;color:black;font-size:20px;'>"""

        head_logo = '<img src="' + Constants.cst_resource + 'logo.png" max-width="230px;" width="230px;" alt="">'

        head_name  = Various.getDefaultValue('entete_1')
        head_line2 = Various.getDefaultValue('entete_2')
        head_line3 = Various.getDefaultValue('entete_3')
        head_addr  = Various.getDefaultValue('entete_adr')
        head_phone = Various.getDefaultValue('entete_tel')
        head_fax   = Various.getDefaultValue('entete_fax')
        head_email = Various.getDefaultValue('entete_email')

        extra_header = ''

        if full_header:
            extra_header += ('<div><span style="font:15px Helvetica;">' + str(head_line2['value']) + '</span></div>'
                             '<div><span style="font:15px Helvetica;">' + str(head_line3['value']) + '</span></div>')

        if head_phone['value']:
            phone = ('<span class="ft_header">' + _("Tél") + ' : ' + str(head_phone['value']) + '&nbsp;</span>')
        else:
            phone = ''

        if head_fax['value']:
            fax = ('<span class="ft_header">' + _("Fax") + ' : ' + str(head_fax['value']) + '&nbsp;</span>')
        else:
            fax = ''

        if head_email['value']:
            email = ('<span class="ft_header">' + _("Email") + ' : ' + str(head_email['value']) + '&nbsp;</span>')
        else:
            email = ''

        header += ('<div style="width:1000px;height:140px;background-color:#FFF;">'
                   '<div style="float:left;width:235px;background-color:#FFF;">' + head_logo + '</div>'
                   '<div style="float:right;width:755px;background-color:#FFF;">'
                   '<div><span class="ft_lab_name">' + str(head_name['value']) + '</span></div>' + extra_header +
                   '<div><span class="ft_header">' + str(head_addr['value']) + '</span></div>'
                   '<div>' + phone + fax + email + '</div></div></div>'
                   '<div style="width:1000px;text-align:right;margin-bottom:5px;">' + _(report_status) + '</div>')

        return header

    @staticmethod
    def getPdfPref():
        """Get Report settings for PDF

        This function is call by function of this class.

        Returns:
            dict: flags of header and comment preferences.

        """

        cursor = DB.cursor()

        req = ('select id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, entete, commentaire, report_pwd '
               'from sigl_param_cr_data '
               'limit 1')

        cursor.execute(req)

        return cursor.fetchone()

    @staticmethod
    def qrcodeByTemplate(filename, data):
        """Generate a QR code image by a template

        This function is call by getDataReport if a analysis variable with QR code.

        Args:
            filename  (string): filename of image.

        Returns:
            bool: True for success, False otherwise.

        """

        from jinja2 import Template

        # 1 - load default QRC template
        tpl = Setting.getDefaultTemplate('QRC')

        if not tpl:
            Pdf.log.error(Logs.fileline() + ' : qrcodeByTemplate no default template')
            return False

        # 2 - render template with data
        try:
            import tomli

            filepath = os.path.join(Constants.cst_template, tpl['tpl_file'])

            with open(filepath, "rb") as f:
                qrc_tpl = tomli.load(f)

            # tpl_version = qrc_tpl['version']

            qrc_version = int(qrc_tpl['QRcode']['version'])
            qrc_error   = qrc_tpl['QRcode']['error_correction']
            qrc_text    = qrc_tpl['QRcode']['text']

            template = Template(qrc_text)
            tpl_str  = template.render(data)
        except Exception as err:
            Pdf.log.error(Logs.fileline() + ' : qrcodeByTemplate render template failed, err=%s , filename=%s', err, str(filename))
            return False

        # 3 - generate QR code image
        try:
            if qrc_version > 0:
                fit = False
            else:
                qrc_version = 1
                fit = True

            if qrc_error == 'L':
                qrc_error = qrcode.constants.ERROR_CORRECT_L
            elif qrc_error == 'M':
                qrc_error = qrcode.constants.ERROR_CORRECT_M
            elif qrc_error == 'Q':
                qrc_error = qrcode.constants.ERROR_CORRECT_Q
            elif qrc_error == 'H':
                qrc_error = qrcode.constants.ERROR_CORRECT_H
            else:
                qrc_error = qrcode.constants.ERROR_CORRECT_L

            qrc = qrcode.QRCode(version=qrc_version, error_correction=qrc_error)

            qrc.add_data(str(tpl_str))

            qrc.make(fit=fit)

            img = qrc.make_image(fill_color="black", back_color="white")

            type(img)

            img.save('tmp/' + filename)
        except Exception as err:
            Pdf.log.error(Logs.fileline() + ' : qrcodeByTemplate generate QR image failed, err=%s , filename=%s', err, str(filename))
            return False

        Pdf.log.info(Logs.fileline() + ' : qrcodeByTemplate')
        return True

    @staticmethod
    def getPdfSticker(id, type_id, template):
        """Initiates a PDF Barcode page

        This function is call by administrative record or settings stickers templates.

        Args:
            id         (int): serial.
            type_id (string): specify which type of serial.

        Returns:
            bool: True for success, False otherwise.

        """

        Various.useLangPDF()

        # --------------------------------------------------
        data = {}  # dictionnary of data for build report

        filename = ''

        # Get data
        if type_id == 'REC':
            if id > 0:
                record = Record.getRecord(id)

                if not record:
                    Pdf.log.error(Logs.fileline() + ' : ERRROR getPdfSticker cant load record details')
                    return False

                num = record['num_rec']

                filename = 'sticker_REC' + str(id)

                imgcode39_name  = 'sticker_code39_' + str(num) + '.png'
                imgqrcode_name  = 'sticker_qrcode_' + str(num) + '.png'

                # Generate barcode code39 type
                try:
                    checksum = False

                    CODE39 = barcode.get_barcode_class('code39')

                    options = {'font_size': 0,
                               'text_distance': 0.0,
                               'module_height': 24.0,
                               'quiet_zone': 0.0}
                    options['center_text'] = False

                    ean = CODE39(str(num), writer=ImageWriter(), add_checksum=checksum)
                    ean.save('tmp/sticker_code39_' + num, options=options)
                except Exception as err:
                    Pdf.log.error(Logs.fileline() + ' : getPdfSticker failed, err=%s , num=%s', err, str(num))
                    return False

                # Generate qrcode type
                try:
                    img = qrcode.make(str(num))

                    type(img)

                    img.save('tmp/' + imgqrcode_name)
                except Exception as err:
                    Pdf.log.error(Logs.fileline() + ' : getPdfSticker failed, err=%s , num=%s', err, str(num))
                    return False

                filepath_code39 = os.path.join(Constants.cst_path_tmp, imgcode39_name)
                filepath_qrcode = os.path.join(Constants.cst_path_tmp, imgqrcode_name)

                data['img'] = {}
                with open(filepath_code39, 'rb') as fh:
                    data['img']['code39'] = BytesIO(fh.read())
                with open(filepath_qrcode, 'rb') as fh:
                    data['img']['qrcode'] = BytesIO(fh.read())

                data['rec'] = {}
                data['rec']['num']   = str(record['num_rec'])
                data['rec']['num_y'] = str(record['num_dos_an'])
                data['rec']['num_m'] = str(record['num_dos_mois'])
                data['rec']['num_d'] = str(record['num_dos_jour'])

                if record['rec_date_receipt']:
                    data['rec']['rec_date'] = datetime.strftime(record['rec_date_receipt'], Constants.cst_date_eu)
                else:
                    data['rec']['rec_date'] = ''

                # --- Patient details
                data['pat'] = {}

                pat = Patient.getPatient(record['id_patient'])

                data['pat'].update(Pdf.getDataFormItem(record['id_patient']))

                if not pat:
                    Pdf.log.error(Logs.fileline() + ' : ERRROR getPdfSticker cant load patient details')
                    return False

                # --- Patient details for getPdfSticker
                data['pat']['code']         = str(pat['pat_code'])
                data['pat']['code_lab']     = ''
                data['pat']['lastname']     = ''
                data['pat']['firstname']    = ''
                data['pat']['maidenname']   = ''
                data['pat']['middlename']   = ''
                data['pat']['birth']        = ''
                data['pat']['age']          = ''
                data['pat']['age_unit']     = ''
                data['pat']['age_days']     = ''
                data['pat']['sex']          = _('Inconnu')
                data['pat']['addr']         = ''
                data['pat']['zipcode']      = ''
                data['pat']['city']         = ''
                data['pat']['district']     = ''
                data['pat']['pbox']         = ''
                data['pat']['phone']        = ''
                data['pat']['phone2']       = ''
                data['pat']['profession']   = ''
                data['pat']['nationality']  = ''
                data['pat']['resident']     = str(pat['pat_resident'])
                data['pat']['blood_group']  = ''
                data['pat']['blood_rhesus'] = ''

                if pat['pat_ano'] and pat['pat_ano'] == 4:
                    data['pat']['anonymous'] = 'Y'
                else:
                    data['pat']['anonymous'] = 'N'

                if pat['pat_code_lab']:
                    data['pat']['code_lab'] = str(pat['pat_code_lab'])

                if pat['pat_name']:
                    data['pat']['lastname'] = str(pat['pat_name'])

                if pat['pat_firstname']:
                    data['pat']['firstname'] = str(pat['pat_firstname'])

                if pat['pat_maiden']:
                    data['pat']['maidenname'] = str(pat['pat_maiden'])

                if pat['pat_midname']:
                    data['pat']['middlename'] = str(pat['pat_midname'])

                if pat['pat_birth']:
                    data['pat']['birth'] = datetime.strftime(pat['pat_birth'], Constants.cst_date_eu)

                    # calc age
                    today = datetime.now()
                    born  = datetime.strptime(str(pat['pat_birth']), Constants.cst_isodate)

                    age = (today - born).days

                    data['pat']['age_days'] = str(age)

                    if age >= 365:
                        data['pat']['age']  = str(today.year - born.year)
                        data['pat']['age_unit'] = _('ans')
                    elif age > 0 and age <= 31:
                        data['pat']['age']  = str((today - born).days)
                        data['pat']['age_unit'] = _('jours')
                    elif today.month - born.month > 0:
                        tmp_age = int((today - born).days / 28)
                        data['pat']['age']  = str(tmp_age)
                        data['pat']['age_unit'] = _('mois')
                elif pat['pat_age']:
                    data['pat']['age'] = str(pat['pat_age'])

                    if pat['pat_age_unit'] == 1037:
                        data['pat']['age_unit'] = _('ans')
                        age = int(pat['pat_age']) * 365
                        data['pat']['age_days'] = str(age)
                    elif pat['pat_age_unit'] == 1036:
                        data['pat']['age_unit'] = _('mois')
                        age = int(pat['pat_age']) * 30
                        data['pat']['age_days'] = str(age)
                    elif pat['pat_age_unit'] == 1035:
                        data['pat']['age_unit'] = _('semaines')
                        age = int(pat['pat_age']) * 7
                        data['pat']['age_days'] = str(age)
                    elif pat['pat_age_unit'] == 1034:
                        data['pat']['age_unit'] = _('jours')
                        data['pat']['age_days'] = str(pat['pat_age'])

                if pat['pat_sex'] == 1:
                    data['pat']['sex'] = _('Masculin')
                elif pat['pat_sex'] == 2:
                    data['pat']['sex'] = _('Féminin')

                if pat['pat_address']:
                    data['pat']['addr'] = str(pat['pat_address'])

                if pat['pat_zipcode']:
                    data['pat']['zipcode'] = str(pat['pat_zipcode'])

                if pat['pat_city']:
                    data['pat']['city'] = str(pat['pat_city'])

                if pat['pat_district']:
                    data['pat']['district'] = str(pat['pat_district'])

                if pat['pat_pbox']:
                    data['pat']['pbox'] = str(pat['pat_pbox'])

                if pat['pat_phone1']:
                    data['pat']['phone'] = str(pat['pat_phone1'])

                if pat['pat_phone2']:
                    data['pat']['phone2'] = str(pat['pat_phone2'])

                if pat['pat_profession']:
                    data['pat']['profession'] = str(pat['pat_profession'])

                if pat['pat_nationality'] and pat['pat_nationality'] > 0:
                    nat = Various.getNationalityById(pat['pat_nationality'])

                    if nat:
                        Various.useLangDB()
                        trans = nat['nat_name'].strip()
                        data['pat']['nationality'] = _(trans)
                        Various.useLangPDF()

                if pat['pat_blood_group'] and pat['pat_blood_group'] == 902:
                    data['pat']['blood_group'] = 'A'
                elif pat['pat_blood_group'] and pat['pat_blood_group'] == 903:
                    data['pat']['blood_group'] = 'AB'
                elif pat['pat_blood_group'] and pat['pat_blood_group'] == 904:
                    data['pat']['blood_group'] = 'O'

                if pat['pat_blood_rhesus'] and pat['pat_blood_rhesus'] == 232:
                    data['pat']['blood_rhesus'] = '+'
                elif pat['pat_blood_rhesus'] and pat['pat_blood_rhesus'] == 233:
                    data['pat']['blood_rhesus'] = '-'

            # PDF test
            else:
                num = '2021000001'

                filename = 'test_template'

                imgcode39_name  = 'sticker_code39_' + str(num) + '.png'
                imgqrcode_name  = 'sticker_qrcode_' + str(num) + '.png'

                # Generate barcode code39 type
                try:
                    filepath = os.path.join(Constants.cst_path_tmp, 'sticker_code39_' + num)

                    checksum = False

                    CODE39 = barcode.get_barcode_class('code39')

                    options = {'font_size': 0,
                               'text_distance': 0.0,
                               'module_height': 24.0,
                               'quiet_zone': 0.0}
                    options['center_text'] = False

                    ean = CODE39(str(num), writer=ImageWriter(), add_checksum=checksum)
                    ean.save(filepath, options=options)
                except Exception as err:
                    Pdf.log.error(Logs.fileline() + ' : getPdfSticker failed, err=%s , num=%s', err, str(num))
                    return False

                # Generate qrcode type
                try:
                    filepath = os.path.join(Constants.cst_path_tmp, imgqrcode_name)

                    img = qrcode.make(str(num))

                    type(img)

                    img.save(filepath)
                except Exception as err:
                    Pdf.log.error(Logs.fileline() + ' : getPdfSticker failed, err=%s , num=%s', err, str(num))
                    return False

                filepath_code39 = os.path.join(Constants.cst_path_tmp, imgcode39_name)
                filepath_qrcode = os.path.join(Constants.cst_path_tmp, imgqrcode_name)

                data['img'] = {}
                with open(filepath_code39, 'rb') as fh:
                    data['img']['code39'] = BytesIO(fh.read())
                with open(filepath_qrcode, 'rb') as fh:
                    data['img']['qrcode'] = BytesIO(fh.read())

                data['rec'] = {}
                data['rec']['num']   = '2021000001'
                data['rec']['num_y'] = '2021000001'
                data['rec']['num_d'] = '2022010001'
                data['rec']['num_m'] = '202201010001'
                data['rec']['rec_date'] = datetime.strftime(datetime.now(), Constants.cst_date_eu)

                # --- Patient details TEST for getPdfSticker
                data['pat'] = {}

                data['pat']['anonymous']    = ''
                data['pat']['code']         = 'Z1X2Y3'
                data['pat']['code_lab']     = 'PAT123'
                data['pat']['lastname']     = 'TEST'
                data['pat']['firstname']    = 'Alexandre'
                data['pat']['maidenname']   = 'PERRIERS'
                data['pat']['middlename']   = 'Monica'
                data['pat']['birth']        = '30/01/1940'
                data['pat']['age']          = '42'
                data['pat']['age_unit']     = _('ans')
                age = int(data['pat']['age']) * 365
                data['pat']['age_days']     = str(age)
                data['pat']['sex']          = _('Masculin')
                data['pat']['addr']         = '3 rue du Paradis'
                data['pat']['zipcode']      = '12345'
                data['pat']['city']         = 'Testville'
                data['pat']['district']     = ''
                data['pat']['pbox']         = 'BP 123'
                data['pat']['phone']        = '0607080910'
                data['pat']['phone2']       = '0700000002'
                data['pat']['profession']   = 'Architecte'
                data['pat']['nationality']  = ''
                data['pat']['resident']     = 'Y'
                data['pat']['blood_group']  = 'AB'
                data['pat']['blood_rhesus'] = '-'

        ret = Pdf.buildPdf('STI', template, filename, data)

        if not ret:
            Pdf.log.error(Logs.fileline() + ' : getPdfSticker ERROR buildPdf STI')
            return False

        Pdf.log.info(Logs.fileline() + ' : getPdfSticker')
        return True

    @staticmethod
    def getPdfReport(id_rec, template, filename, reedit='N'):
        """Initiates a PDF Report

        This function is call by administrative record and biological validation template

        Args:
            id_rec      (int): record serial.
            filename (string): filename.
            template (string): template filename.
            reedit     (flag): rebuild (Y) or not (N) this document.

        Returns:
            bool: True for success, False otherwise.

        """

        # 1 - get data
        datas = Pdf.getDataReport(id_rec, filename, reedit)

        # 2 - run data with template
        # 3 - convert odt to PDF
        # Pdf.log.error(Logs.fileline() + ' : DEBUG-TRACE data : ' + str(datas))

        ret = Pdf.buildReport(template, filename, datas, id_rec)

        if not ret:
            Pdf.log.error(Logs.fileline() + ' : getPdfReport ERROR')
            return False

        Pdf.log.error(Logs.fileline() + ' : getPdfReport')
        return True

    @staticmethod
    def buildLabelData():
        """
        Build the labels common to the report, outsourcing and invoice PDFs.
        Each caller adds its own extra labels to the returned dict.
        """
        label = {}

        label['phone']      = str(_("Tél"))
        label['fax']        = str(_("Fax"))
        label['email']      = str(_("Email"))
        label['record']     = str(_("Dossier"))
        label['code']       = str(_("Code"))
        label['born']       = str(_("Né(e) le"))
        label['admit']      = str(_("Admis le"))
        label['at']         = str(_("en"))
        label['bed']        = str(_("Lit"))
        label['by']         = str(_("par"))
        label['exam_presc'] = str(_("Examen prescrit le"))
        label['save']       = str(_("Enregistré le"))
        label['edit']       = str(_("édité le"))
        label['analyzes']   = str(_("ANALYSE"))
        label['results']    = str(_("RESULTAT"))
        label['references'] = str(_("Références"))
        label['previous']   = str(_("Antériorités"))
        label['comm']       = str(_("Commentaire"))
        label['validate']   = str(_("validé par"))

        return label

    @staticmethod
    def buildLaboratoryData():
        """
        Build the laboratory header shared by the generated PDFs.
        Values come from the lab settings; phone, fax and email stay empty when unset.
        """
        lab_data = {}

        name  = Various.getDefaultValue('entete_1')
        line2 = Various.getDefaultValue('entete_2')
        line3 = Various.getDefaultValue('entete_3')
        addr  = Various.getDefaultValue('entete_adr')
        phone = Various.getDefaultValue('entete_tel')
        fax   = Various.getDefaultValue('entete_fax')
        email = Various.getDefaultValue('entete_email')

        lab_data['name']  = str(name['value'])
        lab_data['head2'] = str(line2['value'])
        lab_data['head3'] = str(line3['value'])
        lab_data['addr']  = str(addr['value'])
        lab_data['phone'] = ''
        lab_data['fax']   = ''
        lab_data['email'] = ''

        if phone['value']:
            lab_data['phone'] = str(phone['value'])

        if fax['value']:
            lab_data['fax'] = str(fax['value'])

        if email['value']:
            lab_data['email'] = str(email['value'])

        return lab_data

    @staticmethod
    def buildPatientData(record):
        """
        Build the patient section shared by the report, outsourcing and invoice PDFs.
        Falls back on a dummy patient when the record carries none: this is what the
        template test print relies on.
        """
        pat_data = {}

        if record['id_patient'] > 0:
            pat = Patient.getPatient(record['id_patient'])

            pat_data.update(Pdf.getDataFormItem(record['id_patient']))
        # For print test patient
        else:
            pat = {}
            pat['pat_ano']       = 'N'
            pat['pat_code']      = 'Z1X2Y3'
            pat['pat_code_lab']  = 'PAT123'
            pat['pat_name']      = 'PATIENT'
            pat['pat_firstname'] = 'Pauline'
            pat['pat_maiden']    = 'PERRIERS'
            pat['pat_midname']   = 'Monica'
            pat['pat_birth']     = datetime.strptime('1979-04-01', Constants.cst_isodate).date()
            pat['pat_age']       = 42
            pat['pat_age_unit']  = '1037'
            pat['pat_sex']       = '2'
            pat['pat_address']   = '3 rue du Paradis'
            pat['pat_zipcode']   = '12345'
            pat['pat_city']      = 'Testville'
            pat['pat_district']  = ''
            pat['pat_pbox']      = 'BP 123'
            pat['pat_phone1']    = '0607080910'
            pat['pat_phone2']    = '0700000002'
            pat['pat_profession']   = 'Architecte'
            pat['pat_nationality']  = 49
            pat['pat_resident']     = 'Y'
            pat['pat_blood_group']  = 904
            pat['pat_blood_rhesus'] = 232

        pat_data['anonymous']    = ''
        pat_data['code']         = str(pat['pat_code'])
        pat_data['code_lab']     = ''
        pat_data['lastname']     = ''
        pat_data['firstname']    = ''
        pat_data['maidenname']   = ''
        pat_data['middlename']   = ''
        pat_data['birth']        = ''
        pat_data['age']          = ''
        pat_data['age_unit']     = ''
        pat_data['age_days']     = ''
        pat_data['sex']          = _('Inconnu')
        pat_data['addr']         = ''
        pat_data['zipcode']      = ''
        pat_data['city']         = ''
        pat_data['district']     = ''
        pat_data['pbox']         = ''
        pat_data['phone']        = ''
        pat_data['phone2']       = ''
        pat_data['profession']   = ''
        pat_data['nationality']  = ''
        pat_data['resident']     = str(pat['pat_resident'])
        pat_data['blood_group']  = ''
        pat_data['blood_rhesus'] = ''

        if pat['pat_ano'] and pat['pat_ano'] == 4:
            pat_data['anonymous'] = 'Y'
        else:
            pat_data['anonymous'] = 'N'

        if pat['pat_code_lab']:
            pat_data['code_lab'] = str(pat['pat_code_lab'])

        if pat['pat_name']:
            pat_data['lastname'] = str(pat['pat_name'])

        if pat['pat_firstname']:
            pat_data['firstname'] = str(pat['pat_firstname'])

        if pat['pat_maiden']:
            pat_data['maidenname'] = str(pat['pat_maiden'])

        if pat['pat_midname']:
            pat_data['middlename'] = str(pat['pat_midname'])

        if pat['pat_birth']:
            pat_data['birth'] = datetime.strftime(pat['pat_birth'], Constants.cst_date_eu)

            # calc age
            today = datetime.now()
            born  = datetime.strptime(str(pat['pat_birth']), Constants.cst_isodate)

            age = (today - born).days

            pat_data['age_days'] = str(age)

            if age >= 365:
                pat_data['age']  = str(today.year - born.year)
                pat_data['age_unit'] = _('ans')
            elif age > 0 and age <= 31:
                pat_data['age']  = str((today - born).days)
                pat_data['age_unit'] = _('jours')
            elif today.month - born.month > 0:
                tmp_age = int((today - born).days / 28)
                pat_data['age']  = str(tmp_age)
                pat_data['age_unit'] = _('mois')
        elif pat['pat_age']:
            pat_data['age'] = str(pat['pat_age'])

            if pat['pat_age_unit'] == 1037:
                pat_data['age_unit'] = _('ans')
                age = int(pat['pat_age']) * 365
                pat_data['age_days'] = str(age)
            elif pat['pat_age_unit'] == 1036:
                pat_data['age_unit'] = _('mois')
                age = int(pat['pat_age']) * 30
                pat_data['age_days'] = str(age)
            elif pat['pat_age_unit'] == 1035:
                pat_data['age_unit'] = _('semaines')
                age = int(pat['pat_age']) * 7
                pat_data['age_days'] = str(age)
            elif pat['pat_age_unit'] == 1034:
                pat_data['age_unit'] = _('jours')
                pat_data['age_days'] = str(pat['pat_age'])

        if pat['pat_sex'] == 1:
            pat_data['sex'] = _('Masculin')
        elif pat['pat_sex'] == 2:
            pat_data['sex'] = _('Féminin')

        if pat['pat_address']:
            pat_data['addr'] = str(pat['pat_address'])

        if pat['pat_zipcode']:
            pat_data['zipcode'] = str(pat['pat_zipcode'])

        if pat['pat_city']:
            pat_data['city'] = str(pat['pat_city'])

        if pat['pat_district']:
            pat_data['district'] = str(pat['pat_district'])

        if pat['pat_pbox']:
            pat_data['pbox'] = str(pat['pat_pbox'])

        if pat['pat_phone1']:
            pat_data['phone'] = str(pat['pat_phone1'])

        if pat['pat_phone2']:
            pat_data['phone2'] = str(pat['pat_phone2'])

        if pat['pat_profession']:
            pat_data['profession'] = str(pat['pat_profession'])

        if pat['pat_nationality'] and pat['pat_nationality'] > 0:
            nat = Various.getNationalityById(pat['pat_nationality'])

            if nat:
                Various.useLangDB()
                trans = nat['nat_name'].strip()
                pat_data['nationality'] = _(trans)
                Various.useLangPDF()

        if pat['pat_blood_group'] and pat['pat_blood_group'] == 902:
            pat_data['blood_group'] = 'A'
        elif pat['pat_blood_group'] and pat['pat_blood_group'] == 903:
            pat_data['blood_group'] = 'AB'
        elif pat['pat_blood_group'] and pat['pat_blood_group'] == 904:
            pat_data['blood_group'] = 'O'

        if pat['pat_blood_rhesus'] and pat['pat_blood_rhesus'] == 232:
            pat_data['blood_rhesus'] = '+'
        elif pat['pat_blood_rhesus'] and pat['pat_blood_rhesus'] == 233:
            pat_data['blood_rhesus'] = '-'

        return pat_data

    @staticmethod
    def getDataReport(id_rec, filename, reedit):
        """Build dict of data for Report

        This function is call by getPdfReport

        Args:
            id_rec      (int): record serial.
            filename (string): filename.
            reedit     (flag): rebuild (Y) or not (N) this document.

        Returns:
            dict: dictionnary of data

        """

        Various.useLangPDF()

        data = {}  # dictionnary of data for build report

        # === Logo details ===
        filepath = os.path.join(Constants.cst_resource, 'logo.png')

        with open(filepath, 'rb') as fh:
            data['logo'] = (fh.read(), 'image/png')
        data['signature'] = ""  # filled further when you know the validator

        # === Label details ===
        data['label'] = Pdf.buildLabelData()
        data['label']['technician'] = str(_("technicien"))
        data['label']['sampling_info'] = str(_("Informations de prélèvement"))
        data['label']['sampled_at']    = str(_("Prélève le"))
        data['label']['received_at']   = str(_("reçu le"))

        # === Laboratory details ===
        data['lab'] = Pdf.buildLaboratoryData()
        # === Report details ===
        data['report'] = {}

        data['report']['title']  = _("Compte rendu")
        data['report']['status'] = ''
        data['report']['full_comm'] = 'N'
        data['report']['full_head'] = 'N'

        # Get format header
        pdfpref = Pdf.getPdfPref()

        if pdfpref and pdfpref['commentaire'] == 1049:
            data['report']['full_comm'] = 'Y'

        if pdfpref and pdfpref['entete'] == 1069:
            data['report']['full_head'] = 'Y'

        if pdfpref and pdfpref['report_pwd']:
            data['report']['report_pwd'] = pdfpref['report_pwd']

        # Partial or Full
        data['report']['status'] = _("COMPLET")

        if id_rec > 0:
            l_req = Analysis.getAnalysisReq(id_rec, 'Y')

            for req in l_req:
                nb_res_vld = Result.countResValidate(req['id_data'])

                if not nb_res_vld or nb_res_vld['nb_vld'] == 0:
                    data['report']['status'] = _("PARTIEL")

        data['report']['replace'] = ''
        data['report']['replace_date'] = ''
        # regenerated a report
        if reedit == 'Y':
            data['report']['replace'] = _("Annule et remplace le précédent")

            # get date of previous report
            prev_report = File.getPreviousFileReport(id_rec)

            if not prev_report:
                Pdf.log.error(Logs.fileline() + ' : ERROR getPreviousFileReport not found')
                return False

            data['report']['replace_date'] = datetime.strftime(prev_report['date'], Constants.cst_dt_HM)

            if id_rec > 0:
                # update date of file
                ret = File.updateReportDate(filename)

                if not ret:
                    Pdf.log.error(Logs.fileline() + ' : ERROR getDataReport cant update date report')
                    return False

        data['report']['date_now'] = datetime.strftime(datetime.now(), Constants.cst_date_eu)
        data['report']['time_now'] = datetime.strftime(datetime.now(), Constants.cst_time_HM)

        # === Record details ===
        data['rec'] = {}

        if id_rec > 0:
            record = Record.getRecord(id_rec)
        # For print test record
        else:
            Various.useLangDB()
            record = {}
            record['rec_date_receipt']  = datetime.now()
            record['num_rec']           = '2022000001'
            record['num_dos_an']        = '2022000001'
            record['num_dos_mois']      = '2022010001'
            record['num_dos_jour']      = '202201010001'
            record['type']              = 184
            record['date_hosp']         = datetime.now()
            record['service_interne']   = _("Microbiologie")
            record['num_lit']           = 'BED_NUM_123'
            record['rec_hosp_num']      = 'HOSP_NUM_123'
            record['date_prescription'] = datetime.now()
            record['prescriber']        = 'Damien DOC'
            record['rc']                = 'commentaire dossier\n2eme ligne'
            record['id_patient']        = 0
            record['rec_custody']       = 'Y'
            record['rec_num_int']       = 'rec-num-int-123'
            record['rec_date_vld']      = datetime.now()
            record['rec_date_save']     = datetime.now()
            Various.useLangPDF()

        data['rec']['rec_date'] = datetime.strftime(record['rec_date_receipt'], Constants.cst_date_eu)

        data['rec']['num']   = str(record['num_rec'])
        data['rec']['num_y'] = str(record['num_dos_an'])
        data['rec']['num_m'] = str(record['num_dos_mois'])
        data['rec']['num_d'] = str(record['num_dos_jour'])
        data['rec']['num_int'] = str(record['rec_num_int'])

        data['rec']['hosp']         = 'N'
        data['rec']['hosp_date']    = ''
        data['rec']['hosp_service'] = ''
        data['rec']['hosp_bed']     = ''

        data['rec']['presc_date'] = ''
        data['rec']['presc_name'] = ''

        data['rec']['custody'] = 'N'

        if 'type' in record and record['type'] == 184:
            data['rec']['hosp'] = 'Y'
            data['rec']['custody'] = str(record['rec_custody'])

            if record['date_hosp']:
                data['rec']['hosp_date'] = datetime.strftime(record['date_hosp'], Constants.cst_date_eu)

            if record['service_interne']:
                data['rec']['hosp_service'] = str(record['service_interne'])

            if record['num_lit']:
                data['rec']['hosp_bed'] = str(record['num_lit'])

            if record['rec_hosp_num']:
                data['rec']['rec_hosp_num'] = str(record['rec_hosp_num'])

        if record['date_prescription']:
            data['rec']['presc_date'] = datetime.strftime(record['date_prescription'], Constants.cst_date_eu)

        if record['prescriber']:
            if 'prescriber_title' in record and record['prescriber_title']:
                Various.useLangDB()
                trans = record['prescriber_title']
                data['rec']['presc_name'] += _(trans) + ' '
                Various.useLangPDF()

            data['rec']['presc_name'] += str(record['prescriber'])

        data['rec']['comm_title'] = _("Renseignements cliniques")
        data['rec']['comm'] = record['rc'].split("\n") if record.get('rc') else []

        if record['rec_date_vld']:
            data['rec']['date_vld'] = datetime.strftime(record['rec_date_vld'], Constants.cst_dt_HM)
        else:
            data['rec']['date_vld'] = ''

        if record['rec_date_save']:
            data['rec']['date_save'] = datetime.strftime(record['rec_date_save'], Constants.cst_dt_HM)
        else:
            data['rec']['date_save'] = ''

        # === Patient details ===
        data['pat'] = Pdf.buildPatientData(record)

        # === ANALYZES details ===
        data['l_data'] = []
        analysis       = {"fam_name": "", "ana_name": "", "ana_code": "", "ana_loinc": "", "ana_comm": "", "l_res": [],
                          "validate": "", "ana_outsourced": "", "ana_ast": "N", "ana_with_one_result": "N",
                          "tech_validate": ""}
        result         = {"label": "", "value": "", "unit": "", "references": "", "prev_date": "", "prev_val": "",
                          "prev_unit": "", "comm": "", "var_comm": "", "bold_value": "N", "highlight": "N",
                          "in_report": "Y", "formatting": "N", "valueConv": "", "unitConv": ""}

        """
        [{'analysis': {'fam_name': FAMILY, 'ana_name': NAME, 'ana_code': CODE, 'ana_loinc': LOINC_CODE,
                       'ana_comm': COMMENT, "ana_outsourced": Y/N, 'ana_ast': Y/N,
                       'ana_with_one_result': Y/N
                       'l_res': [{'label': VAR_NAME,
                                  'value': RESULT_VALUE,
                                  'unit': UNIT_RESULT_VALUE,
                                  'references': RANGE_VALUE,
                                  'prev_date': PREVIOUS_DATE,
                                  'prev_val': PREVIOUS_VALUE,
                                  'prev_unit': PREVIOUS_UNIT,
                                  'bold_value': BOLD_VALUE,
                                  'highlight': highlight,
                                  'in_report': in_report,
                                  'formatting': formatting,
                                  'valueConv': RESULT_VALUE_CONVERTED,
                                  'unitConv': UNIT_RESULT_VALUE_CONVERTED,}] }
        }]
        """

        # temp var for build l_data
        tmp_ana = analysis.copy()

        # init var for previous value
        id_req_ana_p    = 0  # previous id request analysis
        id_res_p        = 0  # previous id result
        id_user_valid_p = 0  # previous id user who makes validation
        id_user_tech_valid_p = 0  # previous id user who makes technical validation

        if id_rec > 0:
            # GET all results for a record
            list_result = Result.getResultRecordForReport(id_rec)

            if list_result:
                res_fam   = ''       # family result
                res_fam_p = 'empty'  # previous result family
                with_fam  = False    # with or without family

                # Pdf.log.error(Logs.fileline() + ' : DEBUG-TRACE list_result = ' + str(list_result))

                # ----- LOOP RESULT -----
                for res in list_result:
                    # if variable is biologically validated or variable is labeled type
                    test_res_valid = Result.getResultValidation(res['id_res'])

                    if test_res_valid['type_validation'] == Constants.cst_bio_vld or res['type_resultat'] == 265:
                        # Pdf.log.error(Logs.fileline() + ' : DEBUG-TRACE res to displayed, res[id_res] = ' + str(res['id_res']))

                        # NEW ANALYSIS
                        # if id request of this analysis is different of previous one
                        # and id result is different of previous one.
                        if res['id_req_ana'] != id_req_ana_p and res['id_res'] != id_res_p:
                            # --- close PREVIOUS analysis ---
                            if id_req_ana_p > 0:
                                # comment and who make validation
                                res_valid_p = Result.getResultValidation(id_res_p)
                                res_tech_valid_p = Result.getResultValidation(id_res_p, Constants.cst_tech_vld)

                                # If valid user change we display who valid previous analisys
                                if id_user_valid_p > 0 and res_valid_p['utilisateur'] != id_user_valid_p:
                                    id_user_valid_p = res_valid_p['utilisateur']

                                    ret_user = User.getUserDetails(res_valid_p['utilisateur'])

                                    user = ''

                                    if ret_user['title_label']:
                                        Various.useLangDB()
                                        trans = ret_user['title_label']
                                        user += str(_(trans)) + ' '
                                        Various.useLangPDF()

                                    if ret_user['lastname'] and ret_user['firstname']:
                                        user += ret_user['lastname'] + ' ' + ret_user['firstname']
                                    else:
                                        user += ret_user['username']

                                    if res_valid_p['commentaire']:
                                        res_comm = res_valid_p['commentaire'].split("\n")
                                    else:
                                        res_comm = ''

                                    tmp_ana['l_res'][-1]["comm"] = res_comm

                                    tmp_ana['validate'] = str(user)

                                    # processing signature of validator
                                    Pdf.log.error(Logs.fileline() + ' : DEBUG-TRACE TRAITEMENT SIGNATURE')

                                    ret_sign = File.getUserSignature(res_valid_p['utilisateur'])

                                    if ret_sign:
                                        filesign = os.path.join(Constants.cst_upload, ret_sign['path'])
                                        filesign = os.path.join(filesign, ret_sign['generated_name'])

                                        Pdf.log.error(Logs.fileline() + ' : DEBUG-TRACE filesign = ' + str(filesign))

                                        with open(filesign, 'rb') as fh:
                                            data['signature'] = (fh.read(), 'image/png')
                                    else:
                                        Pdf.log.error(Logs.fileline() + ' : DEBUG-TRACE no ret_sign')
                                        data['signature'] = ""

                                # If technical valid user change we display who valid previous analisys
                                if id_user_tech_valid_p > 0 and res_tech_valid_p['utilisateur'] != id_user_tech_valid_p:
                                    id_user_tech_valid_p = res_tech_valid_p['utilisateur']

                                    ret_user_tech = User.getUserDetails(res_valid_p['utilisateur'])

                                    user_tech = ''

                                    if ret_user_tech['title_label']:
                                        Various.useLangDB()
                                        trans = ret_user_tech['title_label']
                                        user_tech += str(_(trans)) + ' '
                                        Various.useLangPDF()

                                    if ret_user_tech['lastname'] and ret_user_tech['firstname']:
                                        user_tech += ret_user_tech['lastname'] + ' ' + ret_user_tech['firstname']
                                    else:
                                        user_tech += ret_user_tech['username']

                                    tmp_ana['tech_validate'] = str(user_tech)

                                # Add previous analysis to list of data
                                data['l_data'].append(tmp_ana)
                                # Pdf.log.error(Logs.fileline() + ' : DEBUG-TRACE tmp_ana = ' + str(tmp_ana))

                            # --- end of close previous analysis ---

                            # init new analysis
                            tmp_ana = {"fam_name": "", "ana_name": "", "ana_code": "", "ana_loinc": "", "ana_comm": "",
                                       "l_res": [], "validate": "", "ana_outsourced": "", "ana_ast": "N",
                                       "ana_with_one_result": "N", "tech_validate": ""}

                            tmp_ana['ana_with_one_result'] = "Y" if res.get('res_count', 0) == 1 else "N"

                            id_req_ana_p = res['id_req_ana']
                            id_res_p     = res['id_res']

                            # if family analysis exist and is different of previous one
                            if res['ana_fam'] and res['ana_fam'] != res_fam_p:
                                res_fam   = res['ana_fam']
                                res_fam_p = res_fam
                                with_fam  = True
                            # analysis without family
                            else:
                                res_fam = ' '
                                with_fam = False

                            # ==== ANALYSIS FAMILY ====
                            if with_fam:
                                Various.useLangDB()
                                if res_fam and res_fam != ' ':
                                    res_fam = _(res_fam.strip())

                                tmp_ana['fam_name'] = res_fam
                                Various.useLangPDF()

                            # ==== ANALYSIS NAME ====
                            if res['ana_name']:
                                Various.useLangDB()
                                trans = res['ana_name'].strip()

                                if trans:
                                    tmp_ana['ana_name'] = _(trans)
                                else:
                                    tmp_ana['ana_name'] = ''

                                Various.useLangPDF()

                            # ==== ANALYSIS CODE AND LOINC CODE ====
                            tmp_ana['ana_code']  = res['ana_code'] if res.get('ana_code') else ''
                            tmp_ana['ana_loinc'] = res['ana_loinc'] if res.get('ana_loinc') else ''

                            if res['ana_comm'] and not res['ana_comm'].startswith('Project-Id-Version'):
                                tmp_ana['ana_comm'] = res['ana_comm'].split("\n")
                            else:
                                tmp_ana['ana_comm'] = ''

                            if res['ana_outsourced'] == 'Y':
                                tmp_ana['ana_outsourced'] = _("Sous-traitée")

                            if res['ana_ast'] == 'Y':
                                tmp_ana['ana_ast'] = 'Y'

                        # init new result
                        tmp_res = {"label": "", "value": "", "unit": "", "value_ast": "", "references": "",
                                   "prev_date": "", "prev_val": "", "prev_unit": "", "comm": "", "bold_value": "N",
                                   "highlight": "N", "in_report": "Y", "formatting": "N", "valueConv": "", "unitConv": ""}

                        # Start to get previous result if exist
                        prev_date = ''
                        prev_res  = ''
                        prev_unit = ''

                        formatting = 'N'

                        res_valid    = Result.getResultValidation(id_res_p)
                        res_date_vld = datetime.strftime(res_valid['date_validation'], Constants.cst_dt_HMS)

                        res_prev = Result.getPreviousResult(res['id_pat'], res['id_ref_ana'], res['id_data'], res['id_res'], res_date_vld)

                        if res_prev and res_prev['date_valid']:
                            prev_date = datetime.strftime(res_prev['date_valid'], Constants.cst_date_eu)

                        # Get label of value
                        type_res = Various.getDicoById(res['type_resultat'])

                        if type_res and type_res['short_label'].startswith("dico_"):
                            Various.useLangDB()
                            trans = type_res['short_label'][5:]
                            type_res = _(trans.strip())
                            Various.useLangPDF()
                        else:
                            type_res = ''

                        # Value to be interpreted
                        if type_res and res['value']:
                            Various.useLangDB()
                            if res['value'] != '0':
                                val = Various.getDicoById(res['value'])
                                trans = val['label']

                                if res['ana_ast'] == 'Y':
                                    if trans == 'Résistant':
                                        tmp_res['value_ast'] = 'R'
                                    elif trans == 'Intermédiaire':
                                        tmp_res['value_ast'] = 'I'
                                    elif trans == 'Sensible':
                                        tmp_res['value_ast'] = 'S'

                                if trans:
                                    formatting = val['dict_formatting']
                                    val = _(trans.strip())
                                else:
                                    val = ''
                            else:
                                val = ''

                            # specific response for bold format
                            if trans == 'Positif':
                                tmp_res['bold_value'] = 'Y'

                            # specific response for partial report
                            if trans == 'en cours':
                                data['report']['status'] = _("PARTIEL")

                            # interpreted previous value
                            if res_prev and res_prev['valeur']:
                                label_prev = Various.getDicoById(res_prev['valeur'])
                                trans = label_prev['label'].strip()

                                if trans:
                                    prev_res = _(trans)
                                else:
                                    prev_res = ''
                            else:
                                prev_res = ''

                            Various.useLangPDF()
                        # Numerical value or canceled
                        else:
                            val = res['value']
                            # Cancel result
                            if not val:
                                val  = _("Annulée")
                                # result of type labeled
                                if res['type_resultat'] == 265:
                                    val = ''

                                prev_res = ''
                            elif res_prev and res_prev['valeur']:
                                prev_res = res_prev['valeur']

                            if res['normal_min'] or res['normal_max']:
                                if val != _("Annulée"):
                                    # bold style if out of range min/max
                                    try:
                                        if res['normal_min'] and float(val) < float(res['normal_min']):
                                            tmp_res['bold_value'] = 'Y'
                                        elif res['normal_max'] and float(val) > float(res['normal_max']):
                                            tmp_res['bold_value'] = 'Y'
                                    except Exception:
                                        Pdf.log.error(Logs.fileline() + ' : ERROR convert to float, val=' + str(val))

                            if res['unite'] and val != _("Annulée"):
                                unit = Various.getDicoById(res['unite'])

                                if unit:
                                    tmp_res['unit'] = unit['label']

                                    if prev_res:
                                        prev_unit = unit['label']

                            # Converted numerical value
                            if res['unite2'] and res['formule_unite2'] and val and val != _("Annulée"):
                                unit2 = Various.getDicoById(res['unite2'])

                                if unit2:
                                    tmp_res['unitConv'] = unit2['label']

                                if not res['precision2']:
                                    res['precision2'] = 2

                                try:
                                    tmp_res['valueConv'] = round(eval(res['formule_unite2'].replace('$', str(val))), res['precision2'])
                                except Exception:
                                    Pdf.log.error(Logs.fileline() + ' : ERROR convert to formula2, valueConv=' + str(tmp_res['valueConv']))
                                    tmp_res['valueConv'] = ''

                        if res['var_highlight']:
                            tmp_res['highlight'] = res['var_highlight']

                        if res['var_in_report']:
                            tmp_res['in_report'] = res['var_in_report']

                        tmp_res['prev_date'] = prev_date
                        tmp_res['prev_val']  = prev_res
                        tmp_res['prev_unit'] = prev_unit

                        # Get normal of value
                        if res['normal_min'] and res['normal_max']:
                            tmp_res['references'] = str(res['normal_min']) + ' - ' + str(res['normal_max'])
                        elif res['normal_min']:
                            tmp_res['references'] = '> ' + str(res['normal_min'])
                        elif res['normal_max']:
                            tmp_res['references'] = '< ' + str(res['normal_max'])

                        # ==== ANALYSIS RESULT ====
                        Various.useLangDB()
                        trans = ''

                        if res['libelle'].strip():
                            trans = str(res['libelle'].strip())
                            tmp_res['label'] = _(trans)
                        else:
                            tmp_res['label'] = ''

                        tmp_res['value'] = str(val)
                        tmp_res['formatting'] = str(formatting)
                        Various.useLangPDF()

                        if res['commentaire'] and not res['commentaire'].startswith('Project-Id-Version'):
                            tmp_res['var_comm'] = res['commentaire'].split("\n")
                        else:
                            tmp_res['var_comm'] = ''

                        # check if we need to generate a QR code
                        if res['var_qrcode'] == 'Y':
                            qrc_filename = 'tpl_qrcode.png'

                            data['res'] = {}
                            data['res']['value']      = tmp_res['value']
                            data['res']['unit']       = tmp_res['unit']
                            data['res']['qrcode']     = ''

                            # to keep same syntaxe of odt template
                            qrc_data = {}
                            qrc_data['o'] = data

                            res_valid = Result.getResultValidation(id_res_p)
                            data['res']['valid_date'] = datetime.strftime(res_valid['date_validation'], Constants.cst_date_eu)

                            # 1 - call function generate QR code
                            ret_qr = Pdf.qrcodeByTemplate(qrc_filename, qrc_data)

                            # 2 - add qr code image in data structure
                            if ret_qr:
                                filepath = os.path.join(Constants.cst_path_tmp, qrc_filename)

                                if os.path.exists(filepath) and os.stat(filepath).st_size > 0:
                                    with open(filepath, 'rb') as fh:
                                        data['res']['qrcode'] = (fh.read(), 'image/png')
                                else:
                                    Pdf.log.error(Logs.fileline() + ' :file doesnt exist path=' + str(path))
                                    data['res']['qrcode'] = ''

                        # Add this result to list of result of this analysis
                        tmp_ana['l_res'].append(tmp_res)
                        # Pdf.log.error(Logs.fileline() + ' : DEBUG-TRACE tmp_res = ' + str(tmp_res))

                # --- END OF LOOP RESULT ---

                # add last comment and who make validation
                l_validators = Result.getListValidators(id_rec)

                id_user_p = 0
                user      = ''
                id_user_tech_p = 0
                user_tech = ''
                res_comm  = []

                for validator in l_validators:

                    id_user = validator['user']
                    """ TODO USELESS 03/01/2024 we try record_validation
                    comment = validator['comment']"""

                    if id_user != id_user_p:
                        ret_user = User.getUserDetails(id_user)

                        if user:
                            user = user + ', '

                        if ret_user['title_label']:
                            Various.useLangDB()
                            trans = ret_user['title_label']
                            user += str(_(trans)) + ' '
                            Various.useLangPDF()

                        if ret_user['lastname'] and ret_user['firstname']:
                            user += ret_user['lastname'] + ' ' + ret_user['firstname']
                        else:
                            user += ret_user['username']

                        # processing signature of validator
                        Pdf.log.error(Logs.fileline() + ' : DEBUG-TRACE TRAITEMENT SIGNATURE')

                        ret_sign = File.getUserSignature(id_user)

                        if ret_sign:
                            filesign = os.path.join(Constants.cst_upload, ret_sign['path'])
                            filesign = os.path.join(filesign, ret_sign['generated_name'])

                            Pdf.log.error(Logs.fileline() + ' : DEBUG-TRACE filesign = ' + str(filesign))

                            with open(filesign, 'rb') as fh:
                                data['signature'] = (fh.read(), 'image/png')
                        else:
                            Pdf.log.error(Logs.fileline() + ' : DEBUG-TRACE no ret_sign')
                            data['signature'] = ""

                        id_user_p = id_user

                    """ TODO USELESS 03/01/2024 we try record_validation
                    if comment:
                        res_comm = comment.split("\n")"""

                # who make technical validation
                l_tech_validators = Result.getListValidators(id_rec, Constants.cst_tech_vld)
                id_user_tech_p = 0
                user_tech = ''

                for tech_validator in l_tech_validators:

                    id_user_tech = tech_validator['user']

                    if id_user_tech != id_user_tech_p:
                        ret_user_tech = User.getUserDetails(id_user_tech)

                        if user_tech:
                            user_tech = user_tech + ', '

                        if ret_user_tech['title_label']:
                            Various.useLangDB()
                            trans = ret_user_tech['title_label']
                            user_tech += str(_(trans)) + ' '
                            Various.useLangPDF()

                        if ret_user_tech['lastname'] and ret_user_tech['firstname']:
                            user_tech += ret_user_tech['lastname'] + ' ' + ret_user_tech['firstname']
                        else:
                            user_tech += ret_user_tech['username']

                        id_user_tech_p = id_user_tech

                rev = Record.getRecordValidation(id_rec)

                res_comm = ''

                if rev and rev['rev_comm']:
                    res_comm = rev['rev_comm'].split("\n")

                tmp_ana['l_res'][-1]["comm"] = res_comm

                tmp_ana['validate'] = str(user)
                tmp_ana['tech_validate'] = str(user_tech)

                # Add last analysis to list of data
                data['l_data'].append(tmp_ana)

        # For print test analysis
        else:
            Various.useLangDB()

            result['label']      = _("Albumine")
            result['value']      = _("Absent")
            result['unit']       = ''
            result['references'] = ''
            result['prev_date']  = '01/12/2022'
            result['prev_val']   = _("Présent")
            result['prev_unit']  = ''
            result['comm']       = 'commentaire validation\n2eme ligne'.split('\n')
            result['bold_value'] = 'N'
            result['highlight']  = 'Y'
            result['formatting'] = 'N'
            result['unitConv']   = ''

            analysis['fam_name'] = _("Biochimie urinaire")
            analysis['ana_name'] = _("Bandelettes urinaires")
            analysis['ana_comm'] = "commentaire d'analyse\n2eme ligne".split('\n')
            analysis['ana_outsourced'] = ""
            analysis['ana_ast']  = "N"
            analysis['l_res'].append(result)
            analysis['validate'] = 'BIO Bernard'
            analysis['tech_validate'] = 'TECH Tierry'

            data['l_data'].append(analysis)

            # QR code testing part
            qrc_filename = 'tpl_qrcode.png'

            trans = 'Positif'

            data['res'] = {}
            data['res']['value']      = _(trans)
            data['res']['unit']       = ''
            data['res']['valid_date'] = '08/03/2022'
            data['res']['qrcode']     = ''

            # to keep same syntaxe of odt template
            qrc_data = {}
            qrc_data['o'] = data

            # 1 - call function generate QR code
            ret_qr = Pdf.qrcodeByTemplate(qrc_filename, qrc_data)

            # 2 - add qr code image in data structure
            if ret_qr:
                filepath = os.path.join(Constants.cst_path_tmp, qrc_filename)

                if os.path.exists(filepath) and os.stat(filepath).st_size > 0:
                    with open(filepath, 'rb') as fh:
                        data['res']['qrcode'] = (fh.read(), 'image/png')
                else:
                    Pdf.log.error(Logs.fileline() + ' :file doesnt exist path=' + str(path))
                    data['res']['qrcode'] = ''

            Various.useLangPDF()

        # samples
        """
        [{'sample': {'date': DATE,
                     'type': LABEL,
                     'qty': NUMBER,
                     'stat': LABEL,
                     'sampler': STRING,
                     'date_receipt': DATE,
                     'comm': STRING,
                     'location': LABEL,
                     'location_det': STRING,
                     'storage': STRING,
                     'code': STRING}
        }]
        """

        data['samples'] = []
        sample = {"date": "", "type": "", "qty": '0', "stat": "", "sampler": "", "date_receipt": "",
                  "comm": "", "location": "", "location_det": "", "storage": "", "code": ""}

        if id_rec > 0:
            list_samples = Product.getProductReq(id_rec)

            for sample in list_samples:
                tmp_sample = {"date": "", "type": "", "code_ana": '', "stat": "", "sampler": "", "date_receipt": "",
                              "comm": "", "location": "", "location_det": "", "storage": "",
                              "code": ""}

                tmp_sample['date']         = sample.get('samp_date', "")
                tmp_sample['type']         = sample.get('type_prod', "")
                tmp_sample['code_ana']     = str(sample.get('code_ana', ""))
                tmp_sample['stat']         = sample.get('stat_prod', "")
                tmp_sample['sampler']      = sample.get('preleveur', "")
                tmp_sample['date_receipt'] = sample.get('samp_receipt_date', "")
                tmp_sample['comm']         = sample.get('commentaire', "").split('\n')
                tmp_sample['location']     = sample.get('location', "")
                tmp_sample['location_det'] = str(sample.get('lieu_prel_plus', ""))
                tmp_sample['storage']      = str(sample.get('localisation', ""))
                tmp_sample['code']         = str(sample.get('code', ""))

                # Replace None by empty string
                for key, value in list(tmp_sample.items()):
                    if tmp_sample[key] is None:
                        tmp_sample[key] = ""

                Various.useLangDB()

                if tmp_sample['type']:
                    trans = tmp_sample['type'].strip()
                    tmp_sample['type'] = _(trans)

                if tmp_sample['stat']:
                    trans = tmp_sample['stat'].strip()
                    tmp_sample['stat'] = _(trans)

                if tmp_sample['location']:
                    trans = tmp_sample['location'].strip()
                    tmp_sample['location'] = _(trans)

                Various.useLangPDF()

                data['samples'].append(tmp_sample)

        # For print test sample
        else:
            Various.useLangDB()

            sample['date']         = datetime.strptime('2025-12-02', Constants.cst_isodate)
            sample['type']         = str(_("Sang"))
            sample['qty']          = str(1)
            sample['stat']         = str(_("Fait"))
            sample['sampler']      = "Martin Prel"
            sample['date_receipt'] = "03/12/2025"
            sample['time_receipt'] = "09:45"
            sample['comm']         = "Commentaire".split('\n')
            sample['location']     = str(_("Interne au labo"))
            sample['location_det'] = ""
            sample['storage']      = ""
            sample['code']         = "CODE_TEST_01"

            data['samples'].append(sample)

        # Pdf.log.error(Logs.fileline() + ' : DEBUG-TRACE data : ' + str(data))

        return data

    @staticmethod
    def buildReport(template, filename, data, id_rec):
        """Build a PDF from a template with data

        This function is call by getPdfReport()

        Args:
            template (string): name of template.
            filename (string): filename.
            data       (flag): data to fill the template.
            id_rec      (int): serial of record

        Returns:
            bool: True for success, False otherwise.

        """

        tmp_odt = os.path.join(Constants.cst_path_tmp, filename)
        report_pwd = 'N'
        password = ''

        # get password protection or not and if yes get password with pat_code
        if data and 'report' in data and data['report'].get('report_pwd') == 'Y':
            report_pwd = 'Y'

            if 'pat' not in data or 'code' not in data['pat'] or not data['pat']['code']:
                Pdf.log.error(Logs.fileline() + ' : buildReport requires data["pat"]["code"] when report_pwd == Y')
                return False

            password = data['pat']['code']

        if id_rec > 0:
            out_pdf = os.path.join(Constants.cst_report, filename)
        else:
            out_pdf = os.path.join(Constants.cst_path_tmp, filename + '.pdf')

        # write odt with data and template
        try:
            Pdf.log.error(Logs.fileline() + ' : buildReport data = ' + str(data))

            # write data sticker in a file for debugging or testing
            path_debug = os.path.join(Constants.cst_template, Constants.cst_filedata_report)

            with open(path_debug, "w") as file_debug:
                file_debug.write(str(data))

            tpl_path = os.path.join(Constants.cst_template, template)

            tpl = Template(source="", filepath=tpl_path)

            with open(tmp_odt, "wb") as f:
                f.write(tpl.generate(o=data).render().getvalue())
        except Exception as err:
            Pdf.log.error(Logs.fileline() + ' : buildReport failed, err=' + str(err) + ' , template=' + str(template) + ', filename=' + str(filename))
            return False

        # convert odt to pdf via openoffice
        try:
            cmd = ('unoconv -e SelectPdfVersion=1 -f pdf -o ' + out_pdf + ' ' + tmp_odt + ' > ' + Constants.cst_log + 'unoconv.out 2>&1')

            Pdf.log.error(Logs.fileline() + ' : buildReport cmd=' + cmd)
            os.system(cmd)

            if id_rec > 0:
                file_exists = os.path.exists(out_pdf + '.pdf')

                # if file ends by .pdf remove it
                if file_exists:
                    Pdf.log.error(Logs.fileline() + ' : buildReport remove .pdf from ' + out_pdf + '.pdf')
                    import shutil

                    shutil.move(out_pdf + '.pdf', out_pdf)
        except Exception as err:
            Pdf.log.error(Logs.fileline() + ' : buildReport convert odt to PDF failed, err=%s , template=%s, filename=%s', err, str(template), str(filename))
            return False

        # protect pdf with password
        if report_pwd == 'Y':
            try:
                protected_pdf = out_pdf + '.protected'

                Pdf.log.error(Logs.fileline() + f" : buildReport applying password protection to {out_pdf}")

                with pikepdf.open(out_pdf) as pdf:
                    pdf.save(
                        protected_pdf,
                        encryption=pikepdf.Encryption(
                            owner=password,
                            user=password,
                            allow=pikepdf.Permissions(accessibility=True, extract=False, print_lowres=True,
                                                      print_highres=False, modify_annotation=False, modify_form=False,
                                                      modify_assembly=False, modify_other=False)
                        )
                    )

                os.replace(protected_pdf, out_pdf)

            except Exception as err:
                Pdf.log.error(Logs.fileline() + f" : buildReport PDF password protection failed: {err}")
                return False

        return True

    @staticmethod
    def buildPdf(type, template, filename, data):
        """Build a PDF from a template with data

        This function is call by getPdfSticker(), getPdfOutsourced(), getPdfInvoice(), getPdfBillList(), getPdfActivityReport()

        Args:
            type     (string): type of template.
            template (string): name of template.
            filename (string): filename without extension pdf.
            data       (flag): data to fill the template.

        Returns:
            bool: True for success, False otherwise.
        """

        tmp_odt = os.path.join(Constants.cst_path_tmp, filename)

        out_pdf = os.path.join(Constants.cst_path_tmp, filename + '.pdf')

        if type == 'STI':
            debug_filename_data = Constants.cst_filedata_sticker
        elif type == 'OUT':
            debug_filename_data = Constants.cst_filedata_outsourced
        elif type == 'INV':
            debug_filename_data = Constants.cst_filedata_invoice
        elif type == 'BIL':
            debug_filename_data = Constants.cst_filedata_billing_status
        elif type == 'ACT':
            debug_filename_data = Constants.cst_filedata_activity_report

        # write odt with data and template
        try:
            Pdf.log.error(Logs.fileline() + ' : type = ' + str(type) + ' | buildPdf data = ' + str(data))

            # write data sticker in a file for debugging or testing
            path_debug = os.path.join(Constants.cst_template, debug_filename_data)

            with open(path_debug, "w") as file_debug:
                file_debug.write(str(data))

            tpl_path = os.path.join(Constants.cst_template, template)

            tpl = Template(source="", filepath=tpl_path)

            with open(tmp_odt, "wb") as f:
                f.write(tpl.generate(o=data).render().getvalue())
        except Exception as err:
            err_type = err.__class__.__name__
            err_msg = str(err)
            Pdf.log.error(Logs.fileline() + ' : buildPdf failed, err_type=' + err_type + ', err_msg=' + err_msg + ', template=' + str(template) + ', filename=' + str(filename))
            return False

        # convert odt to pdf via openoffice
        try:
            cmd = ('unoconv -e SelectPdfVersion=1 -f pdf -o ' + out_pdf + ' ' + tmp_odt + ' > ' + Constants.cst_log + 'unoconv.out 2>&1')

            Pdf.log.error(Logs.fileline() + ' : buildPdf cmd=' + cmd)
            os.system(cmd)

        except Exception as err:
            Pdf.log.error(Logs.fileline() + ' : buildPdf convert odt to PDF failed, err=%s , template=%s, filename=%s', err, str(template), str(filename))
            return False

        return True

    @staticmethod
    def getPdfOutsourced(id_rec, template, filename):
        """Initiates a PDF Outsourced

        This function is call by administrative record

        Args:
            id_rec      (int): record serial.
            template (string): template filename.

        Returns:
            bool: True for success, False otherwise.

        """

        # 1 - get data
        datas = Pdf.getDataOutsourced(id_rec)

        # 2 - run data with template
        # 3 - convert odt to PDF
        Pdf.log.error(Logs.fileline() + ' : DEBUG-TRACE Outsourced datas : ' + str(datas))

        ret = Pdf.buildPdf('OUT', template, filename, datas)

        if not ret:
            Pdf.log.error(Logs.fileline() + ' : getPdfOutsourced ERROR buildPdf')
            return False

        Pdf.log.error(Logs.fileline() + ' : getPdfOutsourced')
        return True

    @staticmethod
    def getDataOutsourced(id_rec):
        """Build dict of data for Outsourced document

        This function is call by getPdfOutsourced

        Args:
            id_rec      (int): record serial.

        Returns:
            dict: dictionnary of data

        """

        Various.useLangPDF()

        data = {}  # dictionnary of data for build Outsourced document

        # === Logo details ===
        filepath = os.path.join(Constants.cst_resource, 'logo.png')

        with open(filepath, 'rb') as fh:
            data['logo'] = (fh.read(), 'image/png')

        # === Label details ===
        data['label'] = Pdf.buildLabelData()

        # === Laboratory details ===
        data['lab'] = Pdf.buildLaboratoryData()
        # === Report details ===
        data['report'] = {}

        data['report']['title']  = _("Bon de transfert")
        data['report']['full_comm'] = 'N'
        data['report']['full_head'] = 'N'

        # Get format header
        pdfpref = Pdf.getPdfPref()

        if pdfpref and pdfpref['commentaire'] == 1049:
            data['report']['full_comm'] = 'Y'

        if pdfpref and pdfpref['entete'] == 1069:
            data['report']['full_head'] = 'Y'

        data['report']['date_now'] = datetime.strftime(datetime.now(), Constants.cst_date_eu)
        data['report']['time_now'] = datetime.strftime(datetime.now(), Constants.cst_time_HM)

        # === Record details ===
        data['rec'] = {}

        if id_rec > 0:
            record = Record.getRecord(id_rec)
        # For print test record
        else:
            Various.useLangDB()
            record = {}
            record['rec_date_receipt']  = datetime.now()
            record['num_rec']           = '2022000001'
            record['num_dos_an']        = '2022000001'
            record['num_dos_mois']      = '2022010001'
            record['num_dos_jour']      = '202201010001'
            record['type']              = 184
            record['date_hosp']         = datetime.now()
            record['service_interne']   = _("Microbiologie")
            record['num_lit']           = 'BED_NUM_123'
            record['rec_hosp_num']      = 'HOSP_NUM_123'
            record['date_prescription'] = datetime.now()
            record['prescriber']        = 'Damien DOC'
            record['rc']                = 'commentaire dossier\n2eme ligne'
            record['id_patient']        = 0
            record['rec_custody']       = 'Y'
            record['rec_num_int']       = 'rec-num-int-123'
            record['rec_date_vld']      = datetime.now()
            record['rec_date_save']     = datetime.now()
            Various.useLangPDF()

        data['rec']['rec_date'] = datetime.strftime(record['rec_date_receipt'], Constants.cst_date_eu)

        data['rec']['num']   = str(record['num_rec'])
        data['rec']['num_y'] = str(record['num_dos_an'])
        data['rec']['num_m'] = str(record['num_dos_mois'])
        data['rec']['num_d'] = str(record['num_dos_jour'])
        data['rec']['num_int'] = str(record['rec_num_int'])

        data['rec']['hosp']         = 'N'
        data['rec']['hosp_date']    = ''
        data['rec']['hosp_service'] = ''
        data['rec']['hosp_bed']     = ''

        data['rec']['presc_date'] = ''
        data['rec']['presc_name'] = ''

        data['rec']['custody'] = 'N'

        if 'type' in record and record['type'] == 184:
            data['rec']['hosp'] = 'Y'
            data['rec']['custody'] = str(record['rec_custody'])

            if record['date_hosp']:
                data['rec']['hosp_date'] = datetime.strftime(record['date_hosp'], Constants.cst_date_eu)

            if record['service_interne']:
                data['rec']['hosp_service'] = str(record['service_interne'])

            if record['num_lit']:
                data['rec']['hosp_bed'] = str(record['num_lit'])

            if record['rec_hosp_num']:
                data['rec']['rec_hosp_num'] = str(record['rec_hosp_num'])

        if record['date_prescription']:
            data['rec']['presc_date'] = datetime.strftime(record['date_prescription'], Constants.cst_date_eu)

        if record['prescriber']:
            data['rec']['presc_name'] = str(record['prescriber'])

        data['rec']['comm_title'] = _("Renseignements cliniques")
        data['rec']['comm'] = record['rc'].split("\n")

        if record['rec_date_vld']:
            data['rec']['date_vld'] = datetime.strftime(record['rec_date_vld'], Constants.cst_dt_HM)
        else:
            data['rec']['date_vld'] = ''

        if record['rec_date_save']:
            data['rec']['date_save'] = datetime.strftime(record['rec_date_save'], Constants.cst_dt_HM)
        else:
            data['rec']['date_save'] = ''

        # === Patient details ===
        data['pat'] = Pdf.buildPatientData(record)

        # === ANALYZES details ===
        data['l_data'] = []
        analysis       = {"fam_name": "", "ana_name": "", "ana_comm": "", "ana_outsourced": ""}

        # temp var for build l_data
        tmp_ana = analysis.copy()

        # init var for previous value
        id_req_ana_p    = 0  # previous id request analysis

        if id_rec > 0:
            # GET all analysis for a record
            list_ana = Analysis.getAnalysisOutsourced(id_rec, 'Y')

            # Pdf.log.info(Logs.fileline() + ' : DEBUG-TRACE list_ana=' + str(list_ana))

            if list_ana:
                res_fam   = ''       # family result
                res_fam_p = 'empty'  # previous result family
                with_fam  = False    # with or without family

                # ----- LOOP RESULT -----
                for res in list_ana:
                    # NEW ANALYSIS
                    # if id request of this analysis is different of previous one
                    # and id result is different of previous one.
                    if res['id_data'] != id_req_ana_p:

                        # init new analysis
                        tmp_ana = {"fam_name": "", "ana_name": "", "ana_comm": "", "ana_outsourced": "", "ana_ast": "N"}

                        id_req_ana_p = res['id_data']

                        # if family analysis exist and is different of previous one
                        if res['ana_fam'] and res['ana_fam'] != res_fam_p:
                            res_fam   = res['ana_fam']
                            res_fam_p = res_fam
                            with_fam  = True
                        # analysis without family
                        else:
                            res_fam = ' '
                            with_fam = False

                        # ==== ANALYSIS FAMILY ====
                        if with_fam:
                            Various.useLangDB()
                            if res_fam and res_fam != ' ':
                                res_fam = _(res_fam.strip())

                            tmp_ana['fam_name'] = res_fam
                            Various.useLangPDF()

                        # ==== ANALYSIS NAME ====
                        if res['ana_name']:
                            Various.useLangDB()
                            trans = res['ana_name'].strip()

                            if trans:
                                tmp_ana['ana_name'] = _(trans)
                            else:
                                tmp_ana['ana_name'] = ''

                            Various.useLangPDF()

                        if res['ana_comm'] and not res['ana_comm'].startswith('Project-Id-Version'):
                            tmp_ana['ana_comm'] = res['ana_comm'].split("\n")
                        else:
                            tmp_ana['ana_comm'] = ''

                        if res['outsourced'] == 'Y':
                            tmp_ana['ana_outsourced'] = _("Sous-traitée")

                        data['l_data'].append(tmp_ana)

                # --- END OF LOOP ANALYSIS ---

                # Pdf.log.error(Logs.fileline() + ' : DEBUG-TRACE l_data=' + str(data['l_data']))
        # For print test analysis
        else:
            Various.useLangDB()

            analysis['fam_name'] = _("Biochimie urinaire")
            analysis['ana_name'] = _("Bandelettes urinaires")
            analysis['ana_comm'] = "commentaire d'analyse\n2eme ligne".split('\n')
            analysis['ana_outsourced'] = _("Sous-traitée")
            analysis['ana_ast'] = "N"

            data['l_data'].append(analysis)

            Various.useLangPDF()

        # samples
        """
        [{'sample': {'date': DATE,
                     'type': LABEL,
                     'qty': NUMBER,
                     'stat': LABEL,
                     'sampler': STRING,
                     'date_receipt': DATE,
                     'comm': STRING,
                     'location': LABEL,
                     'location_det': STRING,
                     'storage': STRING,
                     'code': STRING}
        }]
        """

        data['samples'] = []
        sample = {"date": "", "type": "", "qty": '0', "stat": "", "sampler": "", "date_receipt": "",
                  "comm": "", "location": "", "location_det": "", "storage": "", "code": ""}

        if id_rec > 0:
            list_samples = Product.getProductReq(id_rec)

            for sample in list_samples:
                tmp_sample = {"date": "", "type": "", "code_ana": '', "stat": "", "sampler": "", "date_receipt": "",
                              "comm": "", "location": "", "location_det": "", "storage": "",
                              "code": ""}

                tmp_sample['date']         = sample.get('samp_date', "")
                tmp_sample['type']         = sample.get('type_prod', "")
                tmp_sample['code_ana']     = str(sample.get('code_ana', ""))
                tmp_sample['stat']         = sample.get('stat_prod', "")
                tmp_sample['sampler']      = sample.get('preleveur', "")
                tmp_sample['date_receipt'] = sample.get('samp_receipt_date', "")
                tmp_sample['comm']         = sample.get('commentaire', "").split('\n')
                tmp_sample['location']     = sample.get('location', "")
                tmp_sample['location_det'] = str(sample.get('lieu_prel_plus', ""))
                tmp_sample['storage']      = str(sample.get('localisation', ""))
                tmp_sample['code']         = str(sample.get('code', ""))

                # Replace None by empty string
                for key, value in list(tmp_sample.items()):
                    if tmp_sample[key] is None:
                        tmp_sample[key] = ""

                Various.useLangDB()

                if tmp_sample['type']:
                    trans = tmp_sample['type'].strip()
                    tmp_sample['type'] = _(trans)

                if tmp_sample['stat']:
                    trans = tmp_sample['stat'].strip()
                    tmp_sample['stat'] = _(trans)

                if tmp_sample['location']:
                    trans = tmp_sample['location'].strip()
                    tmp_sample['location'] = _(trans)

                Various.useLangPDF()

                data['samples'].append(tmp_sample)

        # For print test sample
        else:
            Various.useLangDB()

            sample['date']         = "01/12/2022"
            sample['type']         = str(_("Sang"))
            sample['qty']          = str(1)
            sample['stat']         = str(_("Fait"))
            sample['sampler']      = "Martin Prel"
            sample['date_receipt'] = "03/12/2022"
            sample['time_receipt'] = "09:45"
            sample['comm']         = "Commentaire".split('\n')
            sample['location']     = str(_("Interne au labo"))
            sample['location_det'] = ""
            sample['storage']      = ""
            sample['code']         = "CODE_TEST_01"

            data['samples'].append(sample)

        # Pdf.log.error(Logs.fileline() + ' : DEBUG-TRACE outsourced data : ' + str(data))

        return data

    @staticmethod
    def getDataFormItem(id_pat):
        """Build additionnal dict of data for document
        Data from customizable patient form

        Args:
            id_pat      (int): patient serial.

        Returns:
            dict: dictionnary of data

        """

        data = {}

        l_items = Patient.getFormItems(id_pat)

        if not l_items:
            Pdf.log.warning(Logs.fileline() + ' : ' + 'getDataFormItem WARNING not found')

        for item in l_items:
            key_val = str(item['pfi_key'])
            data[key_val] = item['pfi_value']

        return data

    @staticmethod
    def getPdfInvoice(id_rec, template, filename):
        """Initiates a PDF Invoice

        This function is call by administrative record

        Args:
            id_rec      (int): record serial.
            template (string): template filename.

        Returns:
            bool: True for success, False otherwise.

        """

        # 1 - get data
        datas = Pdf.getDataInvoice(id_rec)

        # 2 - run data with template
        # 3 - convert odt to PDF
        Pdf.log.debug(Logs.fileline() + ' : DEBUG-TRACE Invoice datas : ' + str(datas))

        ret = Pdf.buildPdf('INV', template, filename, datas)

        if not ret:
            Pdf.log.error(Logs.fileline() + ' : getPdfInvoice ERROR buildPdf')
            return False

        Pdf.log.info(Logs.fileline() + ' : getPdfInvoice')
        return True

    @staticmethod
    def getDataInvoice(id_rec):
        """Build dict of data for Invoice document

        This function is call by getPdfInvoice

        Args:
            id_rec      (int): record serial.

        Returns:
            dict: dictionnary of data

        """

        Various.useLangPDF()

        data = {}  # dictionnary of data for build Invoice document

        # === Logo details ===
        filepath = os.path.join(Constants.cst_resource, 'logo.png')

        with open(filepath, 'rb') as fh:
            data['logo'] = (fh.read(), 'image/png')

        # === Label details ===
        data['label'] = Pdf.buildLabelData()
        data['label']['total']      = str(_("Total"))
        data['label']['total_remain'] = str(_("Total à payer"))
        data['label']['analyzes_requested'] = str(_("Analyses demandées"))
        data['label']['discount']   = str(_("Remise sur la facturation"))
        data['label']['percent_discount'] = str(_("Pourcentage de la remise"))
        data['label']['percent_insurance'] = str(_("Pourcentage assurance maladie / mutuelle"))

        # === Laboratory details ===
        data['lab'] = Pdf.buildLaboratoryData()
        # === Invoice details ===
        data['invoice'] = {}

        data['invoice']['title'] = _("Facture")

        data['invoice']['date_now'] = datetime.strftime(datetime.now(), Constants.cst_date_eu)
        data['invoice']['time_now'] = datetime.strftime(datetime.now(), Constants.cst_time_HM)

        # === Record details ===
        data['rec'] = {}

        if id_rec > 0:
            record = Record.getRecord(id_rec)
        # For print test record
        else:
            Various.useLangDB()
            record = {}
            record['rec_date_receipt']  = datetime.now()
            record['num_rec']           = '2022000001'
            record['num_dos_an']        = '2022000001'
            record['num_dos_mois']      = '2022010001'
            record['num_dos_jour']      = '202201010001'
            record['type']              = 184
            record['date_hosp']         = datetime.now()
            record['service_interne']   = _("Microbiologie")
            record['num_lit']           = 'BED_NUM_123'
            record['rec_hosp_num']      = 'HOSP_NUM_123'
            record['date_prescription'] = datetime.now()
            record['prescriber']        = 'Damien DOC'
            record['rc']                = 'commentaire dossier\n2eme ligne'
            record['id_patient']        = 0
            record['rec_custody']       = 'Y'
            record['rec_num_int']       = 'rec-num-int-123'
            record['rec_date_vld']      = datetime.now()
            record['rec_date_save']     = datetime.now()
            record['num_fact']          = '0000000123'
            record['remise']            = _("Personnel hospitalier")
            record['remise_pourcent']   = '12.5'
            record['assu_pourcent']     = '20'
            record['prix']              = '3500.00'
            record['a_payer']           = '2450.00'

            Various.useLangPDF()

        data['rec']['rec_date'] = datetime.strftime(record['rec_date_receipt'], Constants.cst_date_eu)

        data['rec']['num']   = str(record['num_rec'])
        data['rec']['num_y'] = str(record['num_dos_an'])
        data['rec']['num_m'] = str(record['num_dos_mois'])
        data['rec']['num_d'] = str(record['num_dos_jour'])
        data['rec']['num_int'] = str(record['rec_num_int'])

        data['rec']['hosp']         = 'N'
        data['rec']['hosp_date']    = ''
        data['rec']['hosp_service'] = ''
        data['rec']['hosp_bed']     = ''

        data['rec']['presc_date'] = ''
        data['rec']['presc_name'] = ''

        data['rec']['custody'] = 'N'

        if 'type' in record and record['type'] == 184:
            data['rec']['hosp'] = 'Y'
            data['rec']['custody'] = str(record['rec_custody'])

            if record['date_hosp']:
                data['rec']['hosp_date'] = datetime.strftime(record['date_hosp'], Constants.cst_date_eu)

            if record['service_interne']:
                data['rec']['hosp_service'] = str(record['service_interne'])

            if record['num_lit']:
                data['rec']['hosp_bed'] = str(record['num_lit'])

            if record['rec_hosp_num']:
                data['rec']['rec_hosp_num'] = str(record['rec_hosp_num'])

        if record['date_prescription']:
            data['rec']['presc_date'] = datetime.strftime(record['date_prescription'], Constants.cst_date_eu)

        if record['prescriber']:
            data['rec']['presc_name'] = str(record['prescriber'])

        # get or create num_fact
        if record['num_fact']:
            data['rec']['invoice_num'] = str(record['num_fact'])
        else:
            ret = Record.generateBillNumber(id_rec)

            if not ret:
                self.log.error(Logs.fileline() + ' : PdfBill bill number failed id_rec=%s', str(id_rec))
                return compose_ret('', Constants.cst_content_type_json, 500)

            det_record = Record.getRecord(id_rec)

            if det_record['num_fact']:
                data['rec']['invoice_num'] = str(det_record['num_fact'])

        if record['remise']:
            Various.useLangPDF()
            trans = record['remise']
            data['rec']['type_discount'] = _(trans)
        else:
            data['rec']['type_discount'] = ''

        if record['remise_pourcent']:
            data['rec']['percent_discount'] = str(record['remise_pourcent'])
        else:
            data['rec']['percent_discount'] = ''

        if record['assu_pourcent']:
            data['rec']['percent_insurance'] = str(record['assu_pourcent'])
        else:
            data['rec']['percent_insurance'] = ''

        if record['prix']:
            data['rec']['invoice_total'] = str(record['prix'])
        else:
            data['rec']['invoice_total'] = '0.00'

        if record['a_payer']:
            data['rec']['invoice_remain'] = str(record['a_payer'])
        else:
            data['rec']['invoice_remain'] = '0.00'

        # === Patient details ===
        data['pat'] = Pdf.buildPatientData(record)

        # === ANALYZES details ===
        data['l_data'] = []
        analysis       = {"ana_name": "", "ana_code": "", "ana_loinc": "", "ana_outsourced": "", "ana_price": '0.00'}

        if id_rec > 0:
            # GET all analysis for a record
            list_ana = Analysis.getAnalysisInvoice(id_rec, 'Y')

            for ana in list_ana:
                tmp_ana = {"ana_name": "", "ana_code": "", "ana_loinc": "", "ana_outsourced": "", "ana_price": '0.00'}

                # ==== ANALYSIS NAME ====
                if ana['ana_name']:
                    Various.useLangDB()
                    trans = ana['ana_name'].strip()

                    if trans:
                        tmp_ana['ana_name'] = _(trans)
                    else:
                        tmp_ana['ana_name'] = ''

                    Various.useLangPDF()

                if ana['ana_code']:
                    tmp_ana['ana_code'] = ana['ana_code']
                else:
                    tmp_ana['ana_code'] = ''

                if ana['ana_loinc']:
                    tmp_ana['ana_loinc'] = ana['ana_loinc']
                else:
                    tmp_ana['ana_loinc'] = ''

                if ana['outsourced'] == 'Y':
                    tmp_ana['ana_outsourced'] = _("Sous-traitée")

                if ana['ana_price']:
                    tmp_ana['ana_price'] = str(ana['ana_price'])
                else:
                    tmp_ana['ana_price'] = '0.00'

                data['l_data'].append(tmp_ana)

        # For print test analysis
        else:
            Various.useLangDB()

            analysis['ana_name'] = _("Détermination du groupe sanguin ABO et Rhésus standard (D)")
            analysis['ana_code'] = "B157"
            analysis['ana_loinc'] = "93923-1"
            analysis['ana_outsourced'] = _("Sous-traitée")
            analysis['ana_price'] = "3500.00"

            data['l_data'].append(analysis)

            Various.useLangPDF()

        # Pdf.log.error(Logs.fileline() + ' : DEBUG-TRACE invoice data : ' + str(data))

        return data

    @staticmethod
    def getPdfActivityReport(l_type, l_age, date_beg, date_end, tpl_file, filename, family_label=''):
        """Build PDF for activity report from ODT template."""

        data = {}

        # Load logo
        try:
            logo_path = os.path.join(Constants.cst_resource, 'logo.png')
            with open(logo_path, 'rb') as fh:
                data['logo'] = (fh.read(), 'image/png')
        except Exception as err:
            Pdf.log.error(Logs.fileline() + ' : getPdfActivityReport logo err=' + str(err))
            data['logo'] = None

        # Translations
        Various.useLangPDF()
        data['label'] = {}
        data['label']['phone']     = str(_("Tél"))
        data['label']['fax']       = str(_("Fax"))
        data['label']['email']     = str(_("Email"))
        data['label']['analyzes']  = str(_("Analyses"))
        data['label']['by_type']   = str(_("Analyses par type de demande"))
        data['label']['by_age']    = str(_("Analyses par tranche d'âge"))
        data['label']['external']  = str(_("Externes"))
        data['label']['inpatient'] = str(_("Hospitalisés"))
        data['label']['oncall']    = str(_("Gardes"))
        data['label']['total']     = str(_("Total"))
        data['label']['from_']     = str(_("du"))
        data['label']['to_']       = str(_("au"))
        data['label']['legend']    = str(_("H = Homme, F = Femme, I = Inconnu"))
        data['label']['activity_report'] = str(_("Rapport d'activité"))
        data['label']['edit']      = str(_("édité le"))
        data['label']['analysis_family'] = str(_("Famille d'analyse"))

        # Age column labels: dynamic from age_interval_setting
        try:
            raw_intervals = Setting.getAgeInterval() or []
        except Exception as err:
            Pdf.log.error(Logs.fileline() + " : getPdfActivityReport getAgeInterval err=" + str(err))
            raw_intervals = []

        age_intervals = []
        for r in raw_intervals:
            age_intervals.append({
                'lower': r.get('ais_lower_bound'),
                'upper': r.get('ais_upper_bound'),
            })

        # Fallback legacy config if table empty
        if not age_intervals:
            age_intervals = [
                {'lower': None, 'upper': 5},
                {'lower': 5,    'upper': 20},
                {'lower': 20,   'upper': 40},
                {'lower': 40,   'upper': None},
            ]

        def build_age_label(lower, upper, index):
            """Build translated age label using placeholders."""
            if lower is None and upper is not None:
                # "Moins de %s ans"
                return str(_("<= %s ans")) % upper
            if lower is not None and upper is None:
                # "Plus de %s ans"
                return str(_(">= %s ans")) % lower
            if lower is not None and upper is not None:
                # "De %s à %s ans"
                return str(_("%s à %s ans")) % (lower, upper)
            # Fully open interval, should not happen in pratique
            return "Col %d" % index

        # Fill data['label']['age_colX'] for each interval
        for idx, itv in enumerate(age_intervals, start=1):
            lower = itv.get('lower')
            upper = itv.get('upper')
            key = 'age_col%d' % idx
            data['label'][key] = build_age_label(lower, upper, idx)

        data['label']['M'] = str(_("H"))
        data['label']['F'] = str(_("F"))
        data['label']['U'] = str(_("I"))

        # Lab info
        data['lab'] = {}
        try:
            name  = Various.getDefaultValue('entete_1')
            line2 = Various.getDefaultValue('entete_2')
            line3 = Various.getDefaultValue('entete_3')
            addr  = Various.getDefaultValue('entete_adr')
            phone = Various.getDefaultValue('entete_tel')
            fax   = Various.getDefaultValue('entete_fax')
            email = Various.getDefaultValue('entete_email')

            data['lab']['name']  = str(name['value'])
            data['lab']['head2'] = str(line2['value'])
            data['lab']['head3'] = str(line3['value'])
            data['lab']['addr']  = str(addr['value'])
            data['lab']['phone'] = str(phone['value'] or '')
            data['lab']['fax']   = str(fax['value'] or '')
            data['lab']['email'] = str(email['value'] or '')
        except Exception as err:
            Pdf.log.error(Logs.fileline() + ' : getPdfActivityReport lab err=' + str(err))

        # Activity header
        data['activity'] = {}
        data['activity']['title']    = str(_("Rapport d'activité"))
        data['activity']['date_now'] = datetime.strftime(datetime.now(), Constants.cst_date_eu)
        data['activity']['time_now'] = datetime.strftime(datetime.now(), Constants.cst_time_HM)
        data['activity']['family']   = ''

        if family_label:
            data['activity']['family'] = str(_(family_label))

        try:
            dt_beg = datetime.strptime(date_beg, Constants.cst_dt_HM)
        except Exception:
            try:
                dt_beg = datetime.strptime(date_beg, Constants.cst_isodate)
            except Exception:
                dt_beg = datetime.now()

        try:
            dt_end = datetime.strptime(date_end, Constants.cst_dt_HM)
        except Exception:
            try:
                dt_end = datetime.strptime(date_end, Constants.cst_isodate)
            except Exception:
                dt_end = datetime.now()

        data['activity']['date_beg'] = dt_beg.strftime(Constants.cst_date_eu)
        data['activity']['date_end'] = dt_end.strftime(Constants.cst_date_eu)

        # Build table by type
        def sex_key(sex):
            # Returns suffix for M/F/U
            if sex == 1:
                return '_M'
            if sex == 2:
                return '_F'
            return '_U'

        type_map = {}
        order_type = []

        for row in l_type:
            code = row.get('code', '')
            ana  = row.get('analysis', '')
            rec_custody = row.get('rec_custody', '')
            rec_type    = row.get('rec_type', 0)
            sex = row.get('sex')
            nb  = int(row.get('nb_ana', 0) or 0)

            if code not in type_map:
                type_map[code] = {
                    'ana_name': ana,
                    'ana_code': code,
                    'ext_M': 0, 'ext_F': 0, 'ext_U': 0,
                    'inp_M': 0, 'inp_F': 0, 'inp_U': 0,
                    'onc_M': 0, 'onc_F': 0, 'onc_U': 0,
                    'tot_M': 0, 'tot_F': 0, 'tot_U': 0,

                    # totals
                    'ext_tot': 0,
                    'inp_tot': 0,
                    'onc_tot': 0,
                    'type_tot': 0,

                    'm_tot': 0,
                    'f_tot': 0,
                    'u_tot': 0,
                }

                order_type.append(code)

            k = sex_key(sex)

            if rec_custody == 'Y':
                bucket = 'onc'
            elif rec_type == 183:
                bucket = 'ext'
            else:
                bucket = 'inp'

            type_map[code][bucket + k] += nb
            type_map[code]['tot' + k] += nb

        data['l_type'] = [type_map[c] for c in order_type]

        # Compute per-line totals for table by type
        for r in data['l_type']:
            r['ext_tot'] = r['ext_M'] + r['ext_F'] + r['ext_U']
            r['inp_tot'] = r['inp_M'] + r['inp_F'] + r['inp_U']
            r['onc_tot'] = r['onc_M'] + r['onc_F'] + r['onc_U']

            r['m_tot'] = r['tot_M']
            r['f_tot'] = r['tot_F']
            r['u_tot'] = r['tot_U']

            r['type_tot'] = r['ext_tot'] + r['inp_tot'] + r['onc_tot']

        for row in data['l_type']:
            for k in (
                'ext_M', 'ext_F', 'ext_U',
                'inp_M', 'inp_F', 'inp_U',
                'onc_M', 'onc_F', 'onc_U',
                'ext_tot', 'inp_tot', 'onc_tot',
                'm_tot', 'f_tot', 'u_tot',
                'type_tot'
            ):
                if row.get(k) == 0:
                    row[k] = '-'

        # Build table by age (dynamic age_colX_* based on age_interval_setting)
        def age_bucket_index(a, intervals):
            """Return interval index (0..N-1) for given age in years, or None."""
            if a is None:
                return None
            try:
                v = int(a)
            except Exception:
                return None

            for idx, iv in enumerate(intervals):
                lower = iv.get('lower')
                upper = iv.get('upper')

                if lower is None and upper is not None:
                    # ]-inf, upper[
                    if v < upper:
                        return idx
                elif lower is not None and upper is None:
                    # [lower, +inf[
                    if v >= lower:
                        return idx
                elif lower is not None and upper is not None:
                    # [lower, upper[
                    if v >= lower and v < upper:
                        return idx
            return None

        age_map = {}
        order_age = []
        bucket_count = len(age_intervals)

        for row in l_age:
            code = row.get('code', '')
            ana  = row.get('analysis', '')
            sex  = row.get('sex')
            a    = row.get('age')
            nb   = int(row.get('nb_ana', 0) or 0)

            if code not in age_map:
                # Init structure for this analysis with ALL dynamic columns
                base = {
                    'ana_name': ana,
                    'ana_code': code,

                    'age_tot_M': 0,
                    'age_tot_F': 0,
                    'age_tot_U': 0,

                    # Total global sex
                    'sex_tot': 0,
                }
                for i in range(1, bucket_count + 1):
                    base['age_col%d_M' % i] = 0
                    base['age_col%d_F' % i] = 0
                    base['age_col%d_U' % i] = 0
                age_map[code] = base
                order_age.append(code)

            k = sex_key(sex)  # "_M", "_F", "_U"

            # Always increment total per sex
            age_map[code]['age_tot' + k] += nb

            # Assign to correct age bucket if possible
            idx = age_bucket_index(a, age_intervals)
            if idx is not None:
                col_prefix = "age_col%d" % (idx + 1)
                key = col_prefix + k
                age_map[code][key] += nb

        data['l_age'] = [age_map[c] for c in order_age]

        for r in data['l_age']:
            r['age_tot'] = r['age_tot_M'] + r['age_tot_F'] + r['age_tot_U']

        for row in data['l_age']:
            for k, v in list(row.items()):
                if k.startswith('age_col') and v == 0:
                    row[k] = '-'

        for row in data['l_age']:
            if row.get('age_tot') == 0:
                row['age_tot'] = '-'

        ret = Pdf.buildPdf('ACT', tpl_file, filename, data)
        if not ret:
            Pdf.log.error(Logs.fileline() + ' : getPdfActivityReport buildPdf failed')
            return False

        return True
