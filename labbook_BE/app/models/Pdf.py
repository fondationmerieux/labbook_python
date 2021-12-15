# -*- coding:utf-8 -*-
import logging
import barcode
import pdfkit
import qrcode

from barcode.writer import ImageWriter
from datetime import datetime
from relatorio.templates.opendocument import Template

from app.models.Analysis import Analysis
from app.models.DB import DB
from app.models.Logs import Logs
from app.models.Constants import Constants
from app.models.File import File
from app.models.General import *
from app.models.Patient import Patient
from app.models.Record import Record
from app.models.Result import Result
from app.models.Setting import Setting
from app.models.Various import Various
from app.models.User import User


class Pdf:
    log = logging.getLogger('log_db')

    @staticmethod
    def getPdfBarcode(num, args=''):
        """Build a PDF Barcode page

        This function is call by administrative record or settings stickers templates.

        Args:
            num   (int): record serial.
            args (dict): optional, dictionnary of value, specify size.

        Returns:
            bool: True for success, False otherwise.

        """

        sts_width         = 62
        sts_height        = 28
        sts_margin_top    = 10
        sts_margin_bottom = 10
        sts_margin_left   = 10
        sts_margin_right  = 10

        # setting unsaved to test
        if args:
            if args['sts_width']:
                sts_width = args['sts_width']

            if args['sts_height']:
                sts_height = args['sts_height']

            if args['sts_margin_top']:
                sts_margin_top = args['sts_margin_top']

            if args['sts_margin_bottom']:
                sts_margin_bottom = args['sts_margin_bottom']

            if args['sts_margin_left']:
                sts_margin_left = args['sts_margin_left']

            if args['sts_margin_right']:
                sts_margin_right = args['sts_margin_right']
        else:
            setting = Setting.getStickerSetting()

            if not setting:
                Pdf.log.error(Logs.fileline() + ' : ERRROR getPdfBarcode no sticker setting found')
                return False

            sts_width         = setting['sts_width'] + 2   # +2 for border 1px
            sts_height        = setting['sts_height'] + 2  # +2 for border 1px
            sts_margin_top    = max(setting['sts_margin_top'], 10)     # impossible to reduce margin under 10 !
            sts_margin_bottom = max(setting['sts_margin_bottom'], 10)  # impossible to reduce margin under 10 !
            sts_margin_left   = max(setting['sts_margin_left'], 10)    # impossible to reduce margin under 10 !
            sts_margin_right  = max(setting['sts_margin_right'], 10)   # impossible to reduce margin under 10 !

        # Generate barcode code39 type
        try:
            checksum = False

            CODE39 = barcode.get_barcode_class('code39')

            options = {'font_size': 10,
                       'text_distance': 1.0,
                       'module_height': sts_height - 4,  # substract distance text + text
                       'quiet_zone': 4.0}
            options['center_text'] = True

            ean = CODE39(str(num), writer=ImageWriter(), add_checksum=checksum)
            ean.save('tmp/sticker_' + num, options=options)
        except Exception as err:
            Pdf.log.error(Logs.fileline() + ' : getPdfBarcode failed, err=%s , num=%s', err, str(num))
            return False

        # Generate PDF
        path = Constants.cst_path_tmp

        page_w = int(210 - (sts_margin_left + sts_margin_right))
        page_h = int(297 - (sts_margin_top + sts_margin_bottom))

        # Need coeff convert to works !
        sticker = ('<img src="' + path + '/sticker_' + num + '.png" width="' + str(sts_width * 3.7795275591) + 'mm" ' +
                   'height="' + str(sts_height * 4.6) + 'mm">')

        nb_col  = int(page_w / sts_width)
        nb_line = int(page_h / sts_height)

        div_stickers  = '<table width="100%" style="border:1px solid #DDD;" cellspacing="1px;" cellpadding="0">'
        line_stickers = '<tr>'

        for c in range(nb_col):
            line_stickers += '<td style="border:1px solid #DDD;">' + sticker + '</td>'

        line_stickers += '</tr>'

        for l in range(nb_line):
            div_stickers += line_stickers

        div_stickers += '</table>'

        page_body = ('<div style="position:absolute;top:0;left:0;width:' + str(210) + 'mm;height:' + str(297) +
                     'mm;background-color:#FFF;">' + div_stickers + '</div>')

        filename = 'barcode_' + num + '.pdf'

        form_cont = page_body

        options = {'--encoding': 'utf-8',
                   'page-size': 'A4',
                   'margin-top': str(sts_margin_bottom) + 'mm',
                   'margin-right': str(sts_margin_right) + 'mm',
                   'margin-bottom': str(sts_margin_bottom) + 'mm',
                   'margin-left': str(sts_margin_left) + 'mm',
                   'no-outline': None}

        pdfkit.from_string(form_cont, path + filename, options=options)

        return True

    @staticmethod
    def getPdfBill(id_rec):
        """Build a PDF bill

        This function is call by administrative record template

        Args:
            id_rec (int): record serial.

        Returns:
            bool: True for success, False otherwise.

        """

        path = Constants.cst_path_tmp

        # Get format header
        pdfpref = Pdf.getPdfPref()

        full_header = True

        if pdfpref and pdfpref['entete'] == 1069:
            full_header = False

        # Get record details
        record = Record.getRecord(id_rec)

        if not record:
            return False

        num_rec_y   = record['num_dos_an']
        bill_num    = record['num_fact']
        receipt_num = record['num_quittance']

        Various.useLangPDF()

        if receipt_num:
            receipt_num = '<div><span class="ft_bill_rec">' + _("N° quittance") + ' : ' + str(receipt_num) + '</span></div>'
        else:
            receipt_num = ''

        # Get Patient details
        pat = Patient.getPatient(record['id_patient'])

        addr_div = ''

        if pat:
            addr_div += ('<div style="width:475px;border:2px solid dimgrey;border-radius:10px;padding:10px;'
                         'background-color:#FFF;float:right;">')

            if pat['nom'] or pat['prenom']:
                pat_lname = ''
                pat_fname = ''

                if pat['nom']:
                    pat_lname = pat['nom']

                if pat['nom_jf']:
                    pat_lname += '&nbsp;' + pat['nom_jf']

                if pat['prenom']:
                    pat_fname = pat['prenom']

                addr_div += '<div><span class="ft_pat_ident">' + str(pat_lname) + '&nbsp;' + str(pat_fname) + '</span></div>'

            if pat['adresse']:
                addr_div += '<div><span class="ft_pat_addr">' + str(pat['adresse']) + '</span></div>'

            if pat['cp'] or pat['ville']:
                pat_zip = ''
                pat_city = ''

                if pat['cp']:
                    pat_zip = pat['cp']

                if pat['ville']:
                    pat_city = pat['ville']

                addr_div += '<div><span class="ft_pat_addr">' + str(pat_zip) + '&nbsp;' + str(pat_city) + '</span></div>'

            addr_div += '</div>'

        l_ana = Analysis.getAnalysisReq(id_rec, 'A')

        bill_div = ''
        ana_div  = ''
        samp_div = ''

        if l_ana:
            bill_div += ('<div style="width:980px;height:1000px;border:2px solid dimgrey;border-radius:10px;'
                         'padding:10px;margin-top:20px;background-color:#FFF;">')

            label01 = _("Analyses demandées")
            label02 = _("Actes de prélèvements")

            Various.useLangDB()

            # LOOP ANALYZES
            for ana in l_ana:
                # Requested analysis
                if ana['cote_unite'] is None or ana['cote_unite'] != 'PB':
                    if not ana_div:
                        ana_div += '<div><span class="ft_bill_det_tit">' + label01 + '</span></div>'

                    trans = ana['nom'].strip()
                    ana_div += ('<div><span class="ft_bill_det" style="width:90px;display:inline-block;'
                                'text-align:left;">' + str(ana['code']) + '</span>'
                                '<span class="ft_bill_det" style="width:750px;display:inline-block;">' +
                                str(_(trans)) + '</span>'
                                '<span class="ft_bill_det" style="width:120px;display:inline-block;'
                                'text-align:right;">' + str(ana['prix']) + '</span></div>')

                # Requested samples
                if ana['cote_unite'] == 'PB':
                    if not samp_div:
                        samp_div += '<div><span class="ft_bill_det_tit">' + label02 + '</span></div>'

                    # No display of samples without price
                    if ana['prix'] > 0:
                        trans  = ana['code'].strip()
                        trans2 = ana['nom'].strip()
                        trans3 = ana['prix']
                        samp_div += ('<div><span class="ft_bill_det" style="width:90px;display:inline-block;'
                                     'text-align:left;">' + str(trans) + '</span>'
                                     '<span class="ft_bill_det" style="width:750px;display:inline-block;">' +
                                     str(_(trans2)) + '</span>'
                                     '<span class="ft_bill_det" style="width:120px;display:inline-block;'
                                     'text-align:right;">' + str(trans3) + '</span></div>')

            Various.useLangPDF()

            if ana_div:
                bill_div += ana_div + '<br />'

            if samp_div:
                bill_div += samp_div + '<br />'

            # bill_price and bill_remain
            bill_div += ('<div><span class="ft_bill_det_tit" style="width:100px;display:inline-block;text-align:left;">' +
                         _("Total") + '</span>'
                         '<span class="ft_bill_det_tot" style="width:870px;display:inline-block;text-align:right;"">' +
                         str(record['prix']) + '</span></div>'
                         '<div><span class="ft_bill_det_tit" style="width:160px;display:inline-block;text-align:left;">' +
                         _("Total à payer") + '</span>'
                         '<span class="ft_bill_det_tot" style="width:810px;display:inline-block;text-align:right;">' +
                         str(record['a_payer']) + '</span></div></div>')

        page_header = Pdf.getPdfHeader(full_header)

        page_body = ('<div style="width:1000px;">'
                     '<div style="width:475px;padding:10px;background-color:#FFF;float:left;">'
                     '<div><span class="ft_bill_num">' + _("FACTURE") + ' : ' + str(bill_num) + '</span></div>'
                     '<div><span class="ft_bill_rec">' + _("N° dossier") + ' : ' + str(num_rec_y) + '</span>'
                     '</div>' + receipt_num + '</div>' + addr_div + '<div style="clear:both;"></div>' + bill_div + '</div>')

        date_now = datetime.strftime(datetime.now(), "%d/%m/%Y à %H:%M")

        page_footer = ('<div style="width:1000px;margin-top:5px;background-color:#FFF;">'
                       '<div><span class="ft_footer" style="width:900px;display:inline-block;text-align:left;">' +
                       _("Facture n°") + str(bill_num) + ', ' + _("édité le") + ' ' + str(date_now) + '</span>'
                       '<span class="ft_footer" style="width:90px;display:inline-block;text-align:right;">' +
                       _("Page") + ' 1/1</span></div></div></div>')

        filename = 'facture_' + num_rec_y + '.pdf'

        form_cont = page_header + page_body + page_footer

        options = {'--encoding': 'utf-8',
                   'page-size': 'A4',
                   'margin-top': '12.00mm',
                   'margin-right': '0.00mm',
                   'margin-bottom': '0.00mm',
                   'margin-left': '0.00mm',
                   'no-outline': None}

        pdfkit.from_string(form_cont, path + filename, options=options)

        return True

    @staticmethod
    def getPdfBillList(l_datas, date_beg, date_end):
        """Build a PDF bill list

        This function is call by report billing template

        Args:
            l_datas       (json): Billing datas.
            date_beg  (datetime): Start date of the period.
            date_end  (datetime): End date of the period.

        Returns:
            bool: True for success, False otherwise.

        """

        path = Constants.cst_path_tmp

        Various.useLangPDF()

        # Get format header
        pdfpref = Pdf.getPdfPref()

        full_header = True

        if pdfpref and pdfpref['entete'] == 1069:
            full_header = False

        bill_div = ''

        total_price  = 0
        total_remain = 0

        bill_div += ('<span>' + _("ETAT DE LA FACTURATION DU") + ' ' + str(date_beg) + ' ' + _("AU") + ' ' +
                     str(date_end) + '</span>'
                     '<div style="width:980px;height:600px;border:2px solid dimgrey;border-radius:10px;padding:10px;'
                     'margin-top:20px;background-color:#FFF;">'
                     '<table style="width:100%"><thead>'
                     '<th style="text-align:left;">' + _("N° dossier") + '</th>'
                     '<th style="text-align:left;">' + _("N° quittance") + '</th>'
                     '<th style="text-align:left;">' + _("N° facture") + '</th>'
                     '<th>' + _("Prix") + '</th>'
                     '<th>' + _("A payer") + '</th></thead>'
                     '<tr><td colspan="5"></td></tr>')

        for data in l_datas:
            bill_div += ('<tr><td style="text-align:left;">' + data['rec_num'] + '</td>'
                         '<td style="text-align:left;">' + data['receipt_num'] + '</td>'
                         '<td style="text-align:left;">' + data['bill_num'] + '</td>'
                         '<td style="text-align:right;">' + str(data['bill_price']) + '</td>'
                         '<td style="text-align:right;">' + str(data['bill_remain']) + '</td></tr>')

            total_price  += data['bill_price']
            total_remain += data['bill_remain']

        # bill_price and bill_remain
        bill_div += ('<tr><td colspan="5"></td></tr>'
                     '<tr><td class="ft_bill_det_tit" style="text-align:left;">' + _("Total") + '</td>'
                     '<td colspan="3" class="ft_bill_det_tot" style="text-align:right;"">' + str(total_price) + '</td>'
                     '<td class="ft_bill_det_tot" style="text-align:right;">' + str(total_remain) + '</td></tr>')

        bill_div += '</table></div>'

        page_header = Pdf.getPdfHeader(full_header)

        page_body = bill_div

        date_now = datetime.strftime(datetime.now(), "%d/%m/%Y %H:%M")

        page_footer = ('<div style="width:1000px;margin-top:5px;background-color:#FFF;">'
                       '<div><span class="ft_footer" style="width:900px;display:inline-block;text-align:left;">' +
                       _("Etat de la facturation, édité le") + ' ' + str(date_now) + '</span>'
                       '<span class="ft_footer" style="width:90px;display:inline-block;text-align:right;">' +
                       _("Page") + ' 1/1</span></div></div>'
                       '<hr style="width:100%;border-top: 2px dashed dimgrey;"></div>')

        date_now = datetime.now()
        today    = date_now.strftime("%Y%m%d")

        filename = 'list_bill_' + today + '.pdf'

        form_cont = page_header + page_body + page_footer

        options = {'--encoding': 'utf-8',
                   'page-size': 'A4',
                   'margin-top': '12.00mm',
                   'margin-right': '0.00mm',
                   'margin-bottom': '0.00mm',
                   'margin-left': '0.00mm',
                   'no-outline': None}

        pdfkit.from_string(form_cont, path + filename, options=options)

        return True

    @staticmethod
    def getPdfReportGeneric(html_part, filename=''):
        """Build a Generic PDF Report

        This function is call by report statistic, report epidemio, report activity, enter result and list result templates

        Args:
            html_part (string): html string.
            filename  (string): filename.

        Returns:
            bool: True for success, False otherwise.

        """

        path = Constants.cst_path_tmp

        date_now = datetime.now()
        today    = date_now.strftime("%Y%m%d")

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
                   'no-outline': None}

        pdfkit.from_string(form_cont, path + filename, options=options)

        return True

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

        req = ('select id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, entete, commentaire '
               'from sigl_param_cr_data '
               'limit 1')

        cursor.execute(req)

        return cursor.fetchone()

    @staticmethod
    def getPdfReport(id_rec, template, filename, reedit='N'):
        """Build a PDF Report

        This function is call by adminstrative record and biological validation template

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
        # Pdf.log.error(Logs.fileline() + ' : DEBUG data : ' + str(datas))

        ret = Pdf.buildPDF(template, filename, datas, id_rec)

        if not ret:
            Pdf.log.error(Logs.fileline() + ' : getPdfReport ERROR')
            return False

        Pdf.log.error(Logs.fileline() + ' : getPdfReport')
        return True

    @staticmethod
    def getDataReport(id_rec, filename, reedit):
        """Build dict of data for Report

        This function is call by getPdfReport

        Args:
            id_rec      (int): record serial.
            reedit     (flag): rebuild (Y) or not (N) this document.

        Returns:
            dict: dictionnary of data

        """

        Various.useLangPDF()

        data = {}  # dictionnary of data for build report

        # --- Logo details
        from os.path import join

        data['logo'] = (open(join(Constants.cst_resource, 'logo.png'), 'rb'), 'image/png')

        # --- Label details
        data['label'] = {}

        data['label']['phone']      = str(_("Tél"))
        data['label']['fax']        = str(_("Fax"))
        data['label']['email']      = str(_("Email"))
        data['label']['record']     = str(_("Dossier"))
        data['label']['code']       = str(_("Code"))
        data['label']['born']       = str(_("Né le"))
        data['label']['admit']      = str(_("Admis le"))
        data['label']['at']         = str(_("en"))
        data['label']['bed']        = str(_("Lit"))
        data['label']['by']         = str(_("par"))
        data['label']['exam_presc'] = str(_("Examen prescrit le"))
        data['label']['save']       = str(_("Enregistré le"))
        data['label']['edit']       = str(_("édité le"))
        data['label']['analyzes']   = str(_("ANALYSE"))
        data['label']['results']    = str(_("RESULTAT"))
        data['label']['references'] = str(_("Références"))
        data['label']['previous']   = str(_("Antériorités"))
        data['label']['comm']       = str(_("Commentaire"))
        data['label']['validate']   = str(_("validé par"))

        # --- Laboratory details
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

        # --- Report details
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

        # Partial or Full
        if reedit == 'N':
            data['report']['status'] = _("COMPLET")

            if id_rec > 0:
                l_req = Analysis.getAnalysisReq(id_rec, 'Y')

                for req in l_req:
                    nb_res_vld = Result.countResValidate(req['id_data'])

                    if not nb_res_vld or nb_res_vld['nb_vld'] == 0:
                        data['report']['status'] = _("PARTIEL")

        # regenerated a report
        if reedit == 'Y':
            data['report']['status'] = _("ANNULE ET REMPLACE")

            if id_rec > 0:
                # update date of file
                ret = File.updateReportDate(filename)

                if not ret:
                    Pdf.log.error(Logs.fileline() + ' : ERRROR getDataReport cant update date report')
                    return False

        data['report']['date_now'] = datetime.strftime(datetime.now(), "%d/%m/%Y")
        data['report']['time_now'] = datetime.strftime(datetime.now(), "%H:%M")

        # --- Record details
        data['rec'] = {}

        if id_rec > 0:
            record = Record.getRecord(id_rec)
        # For print test
        else:
            Various.useLangDB()
            record = {}
            record['date_dos']          = datetime.now()
            record['num_dos_an']        = '2022000001'
            record['num_dos_mois']      = '2022010001'
            record['num_dos_jour']      = '202201010001'
            record['type']              = 184
            record['date_hosp']         = datetime.now()
            record['service_interne']   = _("Microbiologie")
            record['num_lit']           = 'ABC123'
            record['date_prescription'] = datetime.now()
            record['prescriber']        = 'Damien DOC'
            record['rc']                = _("Test de grossesse")
            record['id_patient']        = 0
            Various.useLangPDF()

        data['rec']['rec_date'] = datetime.strftime(record['date_dos'], '%d/%m/%Y')

        data['rec']['num_y'] = str(record['num_dos_an'])
        data['rec']['num_m'] = str(record['num_dos_mois'])
        data['rec']['num_d'] = str(record['num_dos_jour'])

        data['rec']['hosp']         = 'N'
        data['rec']['hosp_date']    = ''
        data['rec']['hosp_service'] = ''
        data['rec']['hosp_bed']     = ''

        data['rec']['presc_date'] = ''
        data['rec']['presc_name'] = ''

        if 'type' in record and record['type'] == 184:
            data['rec']['hosp'] = 'Y'

            if record['date_hosp']:
                data['rec']['hosp_date'] = datetime.strftime(record['date_hosp'], '%d/%m/%Y')

            if record['service_interne']:
                data['rec']['hosp_service'] = str(record['service_interne'])

            if record['num_lit']:
                data['rec']['hosp_bed'] = str(record['num_lit'])

        if record['date_prescription']:
            data['rec']['presc_date'] = datetime.strftime(record['date_prescription'], '%d/%m/%Y')

        if record['prescriber']:
            data['rec']['presc_name'] = str(record['prescriber'])

        data['rec']['comm_title'] = _("Renseignements cliniques")
        data['rec']['comm'] = str(record['rc'])

        # --- Patient details
        data['pat'] = {}

        if record['id_patient'] > 0:
            pat = Patient.getPatient(record['id_patient'])
        # For print test
        else:
            pat = {}
            pat['code']         = 'Z1X2Y3'
            pat['code_patient'] = 'PAT123'
            pat['nom']          = 'PATIENT'
            pat['prenom']       = 'Pauline'
            pat['nom_jf']       = 'PERRIERS'
            pat['pat_midname']  = 'Monica'
            pat['ddn']          = datetime.strptime('1979-04-01', '%Y-%m-%d').date()
            pat['age']          = '42'
            pat['unite']        = '1037'
            pat['sexe']         = '2'
            pat['adresse']      = '3 rue du Paradis'
            pat['cp']           = '12345'
            pat['ville']        = 'Testville'
            pat['quartier']     = ''
            pat['bp']           = 'BP 123'
            pat['tel']          = '0607080910'
            pat['profession']   = 'Architecte'

        data['pat']['code']       = str(pat['code'])
        data['pat']['code_lab']   = ''
        data['pat']['lastname']   = ''
        data['pat']['firstname']  = ''
        data['pat']['maidenname'] = ''
        data['pat']['middlename'] = ''
        data['pat']['birth']      = ''
        data['pat']['age']        = ''
        data['pat']['age_unit']   = ''
        data['pat']['age_days']   = ''
        data['pat']['sex']        = _('Inconnu')
        data['pat']['addr']       = ''
        data['pat']['zipcode']    = ''
        data['pat']['city']       = ''
        data['pat']['district']   = ''
        data['pat']['pbox']       = ''
        data['pat']['phone']      = ''
        data['pat']['profession'] = ''

        if pat['code_patient']:
            data['pat']['code_lab'] = str(pat['code_patient'])

        if pat['nom']:
            data['pat']['lastname'] = str(pat['nom'])

        if pat['prenom']:
            data['pat']['firstname'] = str(pat['prenom'])

        if pat['nom_jf']:
            data['pat']['maidenname'] = str(pat['nom_jf'])

        if pat['pat_midname']:
            data['pat']['middlename'] = str(pat['pat_midname'])

        if pat['ddn']:
            data['pat']['birth'] = datetime.strftime(pat['ddn'], '%d/%m/%Y')

            # calc age
            today = datetime.now()
            born  = datetime.strptime(str(pat['ddn']), '%Y-%m-%d')

            age = (today - born).days

            data['pat']['age_days'] = str(age)

            if age >= 365:
                data['pat']['age']  = str(today.year - born.year)
                data['pat']['age_unit'] = _('ans')
            elif age > 0 and age <= 31:
                data['pat']['age']  = (today - born).days
                data['pat']['age_unit'] = _('jours')
            elif today.month - born.month > 0:
                data['pat']['age']  = today.month - born.month + ' ' + _('mois')
                data['pat']['age_unit'] = _('mois')
        elif pat['age']:
            data['pat']['age'] = str(pat['age'])

            if pat['unite'] == 1037:
                data['pat']['age_unit'] = _('ans')
                data['pat']['age_days'] = str(pat['age'] * 365)
            elif pat['unite'] == 1036:
                data['pat']['age_unit'] = _('mois')
                data['pat']['age_days'] = str(pat['age'] * 30)
            elif pat['unite'] == 1035:
                data['pat']['age_unit'] = _('semaines')
                data['pat']['age_days'] = str(pat['age'] * 7)
            elif pat['unite'] == 1034:
                data['pat']['age_unit'] = _('jours')
                data['pat']['age_days'] = str(pat['age'])

        if pat['sexe'] == 1:
            data['pat']['sex'] = _('Masculin')
        elif pat['sexe'] == 2:
            data['pat']['sex'] = _('Feminin')

        if pat['adresse']:
            data['pat']['addr'] = str(pat['adresse'])

        if pat['cp']:
            data['pat']['zipcode'] = str(pat['cp'])

        if pat['ville']:
            data['pat']['city'] = str(pat['ville'])

        if pat['quartier']:
            data['pat']['district'] = str(pat['quartier'])

        if pat['bp']:
            data['pat']['pbox'] = str(pat['bp'])

        if pat['tel']:
            data['pat']['phone'] = str(pat['tel'])

        if pat['profession']:
            data['pat']['profession'] = str(pat['profession'])

        # --- ANALYZES details
        data['l_data'] = []
        analysis       = {"fam_name": "", "ana_name": "", "l_res": [], "validate": ""}
        result         = {"label": "", "value": "", "unit": "", "references": "", "prev_date": "", "prev_val": "",
                          "prev_unit": "", "comm": "", "var_comm": "", "bold_value": "N"}

        """
        [{'analysis': {'fam_name': FAMILY_NAME, 'ana_name': ANALYSIS_NAME,
                       'l_res': [{'label': VAR_NAME,
                                  'value': RESULT_VALUE,
                                  'unit': UNIT_RESULT_VALUE,
                                  'references': RANGE_VALUE,
                                  'prev_date': PREVIOUS_DATE,
                                  'prev_val': PREVIOUS_VALUE,
                                  'prev_unit': PREVIOUS_UNIT,
                                  'bold_value': BOLD_VALUE}] }
        }]
        """

        # temp var for build l_data
        tmp_ana = analysis.copy()

        # init var for previous value
        id_req_ana_p    = 0  # previous id request analysis
        id_res_p        = 0  # previous id result
        id_user_valid_p = 0  # previous id user who makes validation

        if id_rec > 0:
            # GET all results for a record
            list_result = Result.getResultRecordForReport(id_rec)

            if list_result:
                res_fam   = ''       # family result
                res_fam_p = 'empty'  # previous result family
                with_fam  = False    # with or without family

                # ----- LOOP RESULT -----
                for res in list_result:
                    # NEW ANALYSIS
                    # if id request of this analysis is different of previous one
                    # and id result is different of previous one.
                    if res['id_req_ana'] != id_req_ana_p and res['id_res'] != id_res_p:
                        # --- close PREVIOUS analysis ---
                        if id_req_ana_p > 0:
                            # comment and who make validation
                            res_valid = Result.getResultValidation(id_res_p)

                            # If valid user change we display who valid previous analisys
                            if id_user_valid_p > 0 and res_valid['utilisateur'] != id_user_valid_p:
                                id_user_valid_p = res_valid['utilisateur']

                                user = User.getUserByIdGroup(res_valid['utilisateur'])

                                if not user:
                                    user = User.getUserDetails(res_valid['utilisateur'])

                                if user['lastname'] and user['firstname']:
                                    user = user['lastname'] + ' ' + user['firstname']
                                else:
                                    user = user['username']

                                if res_valid['commentaire']:
                                    res_comm = res_valid['commentaire']
                                else:
                                    res_comm = ''

                                tmp_ana['l_res'][-1]["comm"] = str(res_comm)

                                tmp_ana['validate'] = str(user)

                            # Add previous analysis to list of data
                            data['l_data'].append(tmp_ana)

                        # --- end of close previous analysis ---

                        # init new analysis
                        tmp_ana = {"fam_name": "", "ana_name": "", "l_res": [], "validate": ""}

                        id_req_ana_p = res['id_req_ana']
                        id_res_p     = res['id_res']

                        # if family analysis exist and is different of previous one
                        if res['ana_fam'] and res['ana_fam'] != res_fam_p:
                            res_fam   = res['ana_fam']
                            res_fam_p = res_fam
                            with_fam  = True
                        else:
                            with_fam = False

                        # ==== ANALYSIS FAMILY ====
                        if with_fam:
                            Various.useLangDB()
                            tmp_ana['fam_name'] = _(res_fam.strip())
                            Various.useLangPDF()

                        # ==== ANALYSIS NAME ====
                        if res['ana_name']:
                            Various.useLangDB()
                            trans = res['ana_name'].strip()
                            tmp_ana['ana_name'] = _(trans)
                            Various.useLangPDF()

                    # init new result
                    tmp_res = {"label": "", "value": "", "unit": "", "references": "", "prev_date": "", "prev_val": "", "prev_unit": "", "comm": "", "bold_value": "N"}

                    # Start to get previous result if exist
                    prev_date = ''
                    prev_res  = ''
                    prev_unit = ''

                    res_prev = Result.getPreviousResult(res['id_pat'], res['id_ref_ana'], res['id_data'], res['id_res'])

                    if res_prev:
                        prev_date = datetime.strftime(res_prev['date_valid'], '%d/%m/%Y')

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
                            val = _(trans.strip())
                        else:
                            val = ''

                        # specific response for bold format
                        if trans == 'Positif':
                            tmp_res['bold_value'] = 'Y'

                        # specific response for patial report
                        if trans == 'en cours':
                            data['report']['status'] = _("PARTIEL")

                        # interpreted previous value
                        if res_prev and res_prev['valeur']:
                            label_prev = Various.getDicoById(res_prev['valeur'])
                            trans = label_prev['label'].strip()
                            prev_res = _(trans)
                        else:
                            prev_res = ''

                        Various.useLangPDF()
                    # Numerical value or canceled
                    else:
                        val = res['value']
                        # Cancel result
                        if not val:
                            val  = _("Annulée")
                            prev_res = ''
                        elif res_prev and res_prev['valeur']:
                            prev_res = res_prev['valeur']

                        if res['normal_min'] and res['normal_max']:
                            if val != _("Annulée"):
                                # bold style if out of range min/max
                                if float(val) < float(res['normal_min']) or float(val) > float(res['normal_max']):
                                    tmp_res['bold_value'] = 'Y'

                        if res['unite'] and val != _("Annulée"):
                            unit = Various.getDicoById(res['unite'])

                            if unit:
                                tmp_res['unit'] = unit['label']

                                if prev_res:
                                    prev_unit = unit['label']

                    tmp_res['prev_date'] = prev_date
                    tmp_res['prev_val']  = prev_res
                    tmp_res['prev_unit'] = prev_unit

                    # Get normal of value
                    if res['normal_min'] and res['normal_max']:
                        tmp_res['references'] = '[ ' + str(res['normal_min']) + ' - ' + str(res['normal_max']) + ' ]'

                    # ==== ANALYSIS RESULT ====
                    Various.useLangDB()
                    trans = str(res['libelle'].strip())
                    tmp_res['label'] = _(trans)
                    tmp_res['value'] = str(val)
                    Various.useLangPDF()

                    tmp_res['var_comm'] = res['commentaire']

                    # Add this result to list of result of this analysis
                    tmp_ana['l_res'].append(tmp_res)
                # --- END OF LOOP RESULT ---

                # add last comment and who make validation
                res_valid = Result.getResultValidation(id_res_p)

                user = User.getUserByIdGroup(res_valid['utilisateur'])

                if not user:
                    user = User.getUserDetails(res_valid['utilisateur'])

                Pdf.log.error(Logs.fileline() + ' : DEBUG user=' + str(user) + ' for id_group=' + str(res_valid['utilisateur']))

                if user['lastname'] and user['firstname']:
                    user = user['lastname'] + ' ' + user['firstname']
                else:
                    user = user['username']

                if res_valid['commentaire']:
                    res_comm = res_valid['commentaire']
                else:
                    res_comm = ''

                tmp_ana['l_res'][-1]["comm"] = str(res_comm)

                tmp_ana['validate'] = str(user)

                # Add last analysis to list of data
                data['l_data'].append(tmp_ana)

                # Pdf.log.error(Logs.fileline() + ' : DEBUG l_data=' + str(data['l_data']))
        # For print test
        else:
            Various.useLangDB()

            result['label']      = _("Albumine")
            result['value']      = _("Absent")
            result['unit']       = ''
            result['references'] = ''
            result['prev_date']  = '01/12/2021'
            result['prev_val']   = _("Présent")
            result['prev_unit']  = ''
            result['comm']       = ''
            result['bold_value'] = 'N'

            analysis['fam_name'] = _("Biochimie urinaire")
            analysis['ana_name'] = _("Bandelettes urinaires")
            analysis['l_res'].append(result)
            analysis['validate'] = 'BIO Bernard'

            data['l_data'].append(analysis)
            Various.useLangPDF()

        return data

    @staticmethod
    def buildPDF(template, filename, data, id_rec):
        """Build a PDF from a template

        This function is call by getPdfReport()

        Args:
            tpl_nam  (string): name of template.
            filename (string): filename.
            data       (flag): data to fill the template.

        Returns:
            bool: True for success, False otherwise.

        """

        from os.path import join
        tmp_odt = join(Constants.cst_path_tmp, filename)

        if id_rec > 0:
            out_pdf = join(Constants.cst_report, filename)
        else:
            out_pdf = join(Constants.cst_path_tmp, filename + '.pdf')

        # write odt with data and template
        try:
            tpl_path = join(Constants.cst_template, template)

            tpl = Template(source="", filepath=tpl_path)

            f = open(tmp_odt, "wb")
            f.write(tpl.generate(o=data).render().getvalue())
        except Exception as err:
            Pdf.log.error(Logs.fileline() + ' : buildPDF failed, err=%s , template=%s, filename=%s', err, str(template), str(filename))
            return False

        # convert odt to pdf via openoffice
        try:
            import os

            # TODO replace python 3.6 by 3.9 and install unoserver instead
            cmd = ('unoconv -f pdf -o ' + out_pdf + ' ' + tmp_odt + ' > ' + Constants.cst_log + 'unoconv.out 2>&1')

            Pdf.log.error(Logs.fileline() + ' : buildPDF cmd=' + cmd)
            os.system(cmd)

            if id_rec > 0:
                from os.path import exists

                file_exists = exists(out_pdf + '.pdf')

                # if file ends by .pdf remove it
                if file_exists:
                    Pdf.log.error(Logs.fileline() + ' : buildPDF remove .pdf from ' + out_pdf + '.pdf')
                    import shutil

                    shutil.move(out_pdf + '.pdf', out_pdf)
        except Exception as err:
            Pdf.log.error(Logs.fileline() + ' : buildPDF convert odt to PDF failed, err=%s , template=%s, filename=%s', err, str(template), str(filename))
            return False

        return True

    @staticmethod
    def getPdfSticker(id, type_id, template):
        """Build a PDF Barcode page

        This function is call by administrative record or settings stickers templates.

        Args:
            id         (int): serial.
            type_id (string): specify which type of serial.

        Returns:
            bool: True for success, False otherwise.

        """

        from os.path import join

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

                num = record['num_dos_an']

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

                data['img'] = {}
                data['img']['code39'] = open(join(Constants.cst_path_tmp, imgcode39_name), 'rb')
                data['img']['qrcode'] = open(join(Constants.cst_path_tmp, imgqrcode_name), 'rb')

                data['rec'] = {}
                data['rec']['num_y'] = str(record['num_dos_an'])
                data['rec']['num_d'] = str(record['num_dos_mois'])
                data['rec']['num_m'] = str(record['num_dos_jour'])
                data['rec']['rec_date'] = datetime.strftime(record['date_dos'], '%d/%m/%Y')

                # --- Patient details
                data['pat'] = {}

                pat = Patient.getPatient(record['id_patient'])

                if not pat:
                    Pdf.log.error(Logs.fileline() + ' : ERRROR getPdfSticker cant load patient details')
                    return False

                data['pat']['lastname']  = pat['nom']
                data['pat']['firstname'] = pat['prenom']
                data['pat']['birth']     = ''
                data['pat']['sex']       = _('Inconnu')

                if pat['ddn']:
                    data['pat']['birth'] = datetime.strftime(pat['ddn'], '%d/%m/%Y')

                if pat['sexe'] == 1:
                    data['pat']['sex'] = _('Masculin')
                elif pat['sexe'] == 2:
                    data['pat']['sex'] = _('Feminin')

            # PDF test
            else:
                num = '2021000001'

                filename = 'test_template'

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

                data['img'] = {}
                data['img']['code39'] = open(join(Constants.cst_path_tmp, imgcode39_name), 'rb')
                data['img']['qrcode'] = open(join(Constants.cst_path_tmp, imgqrcode_name), 'rb')

                data['rec'] = {}
                data['rec']['num_y'] = '2021000001'
                data['rec']['num_d'] = '2022010001'
                data['rec']['num_m'] = '202201010001'
                data['rec']['rec_date'] = datetime.strftime(datetime.now(), "%d/%m/%Y")

                # --- Patient details
                data['pat'] = {}

                data['pat']['lastname']  = 'TEST'
                data['pat']['firstname'] = 'Alexandre'
                data['pat']['birth']     = '30/01/1940'
                data['pat']['sex']       = _('Masculin')

        Pdf.log.error(Logs.fileline() + ' : buildPDF DEBUG data : ' + str(data))

        tmp_odt  = join(Constants.cst_path_tmp, filename)
        out_pdf  = join(Constants.cst_path_tmp, filename + '.pdf')

        # write odt with data and template
        try:
            tpl_path = join(Constants.cst_template, template)

            tpl = Template(source="", filepath=tpl_path)

            f = open(tmp_odt, "wb")
            f.write(tpl.generate(o=data).render().getvalue())
        except Exception as err:
            Pdf.log.error(Logs.fileline() + ' : buildPDF failed, err=%s , template=%s, filename=%s', err, str(template), str(filename))
            return False

        # convert odt to pdf via openoffice
        try:
            import os

            cmd = ('unoconv -f pdf -o ' + out_pdf + ' ' + tmp_odt + ' > ' + Constants.cst_log + 'unoconv.out 2>&1')

            Pdf.log.error(Logs.fileline() + ' : getPdfSticker cmd=' + cmd)
            os.system(cmd)
        except Exception as err:
            Pdf.log.error(Logs.fileline() + ' : getPdfSticker convert odt to PDF failed, err=%s , template=%s, filename=%s', err, str(template), str(filename))
            return False

        Pdf.log.error(Logs.fileline() + ' : getPdfSticker')
        return True
