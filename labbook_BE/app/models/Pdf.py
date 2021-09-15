# -*- coding:utf-8 -*-
import logging
import barcode
import pdfkit
import math

from barcode.writer import ImageWriter
from datetime import datetime

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
        """Built a PDF Barcode page

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
        """Built a PDF bill

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

                    trans = ana['nom']
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
                        trans  = ana['code']
                        trans2 = ana['nom']
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
        """Built a PDF bill list

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
    def getPdfReport(id_rec, filename, reedit='N'):
        """Built a PDF Report

        This function is call by adminstrative record and biological validation template

        Args:
            id_rec      (int): record serial.
            filename (string): filename.
            reedit     (flag): rebuilt (Y) or not (N) this document.

        Returns:
            bool: True for success, False otherwise.

        """

        path = Constants.cst_report

        Various.useLangPDF()

        form_cont = ''

        h_max  = 1410  # maximum page height in pixels
        h_now  = 0     # page height under construction
        h_fam  = 36
        h_name = 24
        h_res  = 36
        h_res2 = 24

        h_header = 30
        h_footer = 30

        num_page = 1

        report_status = ''

        # Partial or Full
        if reedit == 'N':
            l_req = Analysis.getAnalysisReq(id_rec, 'Y')

            report_status = _("COMPLET")

            for req in l_req:
                nb_res_vld = Result.countResValidate(req['id_data'])

                if not nb_res_vld or nb_res_vld['nb_vld'] == 0:
                    report_status = _("PARTIEL")

        # regenerated a report
        if reedit == 'Y':
            # update date of file
            ret = File.updateReportDate(filename)

            report_status = _("ANNULE ET REMPLACE")

            if not ret:
                Pdf.log.error(Logs.fileline() + ' : ERRROR getPdfReport cant update date report')
                return False

        # Get format header
        pdfpref = Pdf.getPdfPref()

        full_header = True
        full_comm   = False

        if pdfpref and pdfpref['entete'] == 1069:
            full_header = False

        if pdfpref and pdfpref['commentaire'] == 1049:
            full_comm = True

        # FOR header page
        h_now += 150 + 80

        # Get record details
        record = Record.getRecord(id_rec)

        num_rec_y = record['num_dos_an']

        # Get Patient details
        pat = Patient.getPatient(record['id_patient'])

        # Patient birth
        birth = _("Né le") + ' '

        if pat['ddn']:
            birth += datetime.strftime(pat['ddn'], '%d/%m/%Y') + ' - '
        else:
            birth = ''

        # Patient Age
        age = str(pat['age'])

        if pat['unite'] == 1037:
            age += ' ' + _('ans')
        elif pat['unite'] == 1036:
            age += ' ' + _('mois')
        elif pat['unite'] == 1035:
            age += ' ' + _('semaines')
        elif pat['unite'] == 1034:
            age += ' ' + _('jours')

        # Patient Sex
        sex = ''

        if pat['sexe'] == 1:
            sex += _('Masculin')
        elif pat['sexe'] == 2:
            sex += _('Feminin')
        elif pat['sexe'] == 3:
            sex += _('Inconnu')

        # BLOCK DET RECORD
        date_now = datetime.strftime(datetime.now(), "%d/%m/%Y")

        rec_div  = ('<div style="width:465px;height:100px;border:2px solid dimgrey;border-radius:10px;padding:10px;'
                    'background-color:#FFF;float:left;">'
                    '<div><span class="ft_rec_det">' + _("Dossier") + ' ' + str(num_rec_y) + ' ' + _("de") + ' ' +
                    str(pat['prenom']) + '&nbsp;' + str(pat['nom']) + '</span></div>'
                    '<div><span class="ft_rec_det">' + str(birth) + str(age) + ' - ' + str(sex) + ' - Code ')

        if pat['code_patient']:
            rec_div += str(pat['code_patient']) + ' / ' + str(pat['code']) + '</span></div>'
        else:
            rec_div += str(pat['code']) + '</span></div>'

        if 'type' in record and record['type'] == 184:
            rec_div += '<div><span class="ft_rec_det">'

            if record['date_hosp']:
                rec_div += _("Admis le") + ' ' + datetime.strftime(record['date_hosp'], '%d/%m/%Y') + ' '

            if record['service_interne']:
                rec_div += _("en") + ' ' + str(record['service_interne']) + ' - '

            if record['num_lit']:
                rec_div += _("Lit") + ' ' + str(record['num_lit'])

            rec_div += '</span></div>'

        if full_comm is True and record['prescriber']:
            prescriber = ' ' + _("par") + ' ' + str(record['prescriber'])
        else:
            prescriber = ''

        rec_div += ('<div><span class="ft_rec_det">' + _("Examen prescrit le") + ' ' +
                    datetime.strftime(record['date_prescription'], '%d/%m/%Y') + prescriber + '</span></div>')
        rec_div += ('<div><span class="ft_rec_det">' + _("Enregistré le") + ' ' +
                    datetime.strftime(record['date_dos'], '%d/%m/%Y') + ', ' + _("édité le") + ' ' + str(date_now) +
                    '</span></div>')

        rec_div += '</div>'

        # BLOCK PATIENT address
        addr_div = ''

        if pat:
            addr_div += ('<div style="width:465px;height:100px;border:2px solid dimgrey;'
                         'border-radius:10px;padding:10px;background-color:#FFF;float:right;">')

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

                addr_div += '<div><span class="ft_pat_addr">' + pat_zip + '&nbsp;' + pat_city + '</span></div>'

            addr_div += '</div>'

        # FOR details record and patient block
        h_now += 100 + 30

        # CLINICAL INFORMATION (= commentary in record)
        rec_comm = ''

        if full_comm and record['rc']:
            rec_comm  = ('<div style="width:980px;border:2px solid dimgrey;'
                         'border-radius:10px;padding:10px;margin-top:5px;background-color:#FFF;">'
                         '<span class="ft_res_name">' + _("Renseignements cliniques") + '</span><br />'
                         '<span class="ft_rec_det">' + str(record['rc']) + '</span></div>')

            nb_rc = math.ceil(len(record['rc']) / 134)

            # FOR comment block
            h_now += 55 + (25 * nb_rc)

        div_first_page = ('<div style="width:1000px;background-color:#FFF;overflow:auto;">' + rec_div + addr_div + '</div>'
                          '<div class="ft_report_tit" style="clear:both;text-align:center;padding-top:10px;'
                          'background-color:#FFF;">' + _("Compte rendu") + '</div>' + rec_comm)

        # ANALYZES PART
        l_res = Result.getResultRecordForReport(id_rec)

        # Pdf.log.error(Logs.fileline() + ' : DEBUG l_res=' + str(l_res))

        id_req_ana_p = 0
        id_res_p = 0
        id_user_valid_p = 0

        h_page = h_max - h_now - h_header - h_footer

        # Pdf.log.error(Logs.fileline() + ' : DEBUG h_page=' + str(h_page))

        result_div = ''

        if l_res:
            res_fam   = ''
            res_fam_p = 'empty'
            with_fam  = False

            # ----- LOOP RESULT -----
            for res in l_res:
                # NEW ANALYSIS DIV
                if res['id_req_ana'] != id_req_ana_p and res['id_res'] != id_res_p:

                    # --- close PREVIOUS analysis ---
                    if id_req_ana_p > 0:
                        # comment and who make validation
                        res_valid = Result.getResultValidation(id_res_p)

                        # If valid user change we display who valid previous analisys
                        if id_user_valid_p > 0 and res_valid['utilisateur'] != id_user_valid_p:
                            id_user_valid_p = res_valid['utilisateur']

                            user = User.getUserByIdGroup(res_valid['utilisateur'])

                            if user['lastname'] and user['firstname']:
                                user = user['lastname'] + ' ' + user['firstname']
                            else:
                                user = user['username']

                            if res_valid['commentaire']:
                                res_comm = res_valid['commentaire']
                            else:
                                res_comm = ''

                            if full_comm:
                                comm_div = ('<div><span class="ft_res_comm" style="width:970px;display:inline-block;'
                                            'text-align:left;"">' + str(res_comm) + '</span></div>')

                                h_now += h_res2
                            else:
                                comm_div = ''

                            result_div = (result_div + comm_div + '<div><span class="ft_res_valid" '
                                          'style="width:970px;display:inline-block;text-align:left;">' +
                                          _("validé par") + ' : ' + str(user) + '</span></div>')

                            h_now += h_res2
                    # --- end of close previous analysis ---

                    id_req_ana_p = res['id_req_ana']
                    id_res_p = res['id_res']

                    # Pdf.log.error(Logs.fileline() + ' : DEBUG id_req_ana=' + str(id_req_ana_p) + ' | id_res=' + str(id_res_p) + ' | id_ref_ana=' + str(res['id_ref_ana']))

                    if res['ana_fam'] and res['ana_fam'] != res_fam_p:
                        res_fam   = res['ana_fam']
                        res_fam_p = res_fam
                        with_fam  = True
                    else:
                        with_fam = False

                    # ==== ANALYSIS FAMILY ====
                    if with_fam:
                        Various.useLangDB()
                        result_div = (result_div + '<div><span class="ft_res_fam" style="width:960px;'
                                      'display:inline-block;text-align:center;">' + _(res_fam) + '</span></div>')
                        h_now += h_fam
                        Various.useLangPDF()

                        # IF family title on 2 lines
                        if len(res_fam) > 70:
                            h_now += h_fam
                            # Pdf.log.error(Logs.fileline() + ' : DEBUG FAM on 2 lines h_now=' + str(h_now))

                        # Pdf.log.error(Logs.fileline() + ' : DEBUG FAMILY=' + res_fam + '\n==========')

                    # AFTER a new line CUT PAGE OR NOT
                    if h_now > (h_max - h_res):
                        # Pdf.log.error(Logs.fileline() + ' : DEBUG FAM h_now=' + str(h_now) + ' > h_max - h_res =' + str(h_max - h_res))
                        form_cont = Pdf.PdfReportCutPageOrNot(form_cont, num_page, h_page, report_status, div_first_page, rec_comm, result_div, full_header, num_rec_y)

                        num_page = num_page + 1

                        # REINIT for next page
                        h_now  = 0
                        h_page = h_max - h_footer - h_header

                        result_div = ''

                    # ==== ANALYSIS NAME ====
                    if res['ana_name']:
                        Various.useLangDB()
                        trans = res['ana_name']
                        result_div = (result_div + '<div><span class="ft_res_name" style="width:960px;'
                                      'display:inline-block;text-align:left;">' + _(trans) + '</span></div>')
                        h_now += h_name
                        Various.useLangPDF()

                        # IF name title on 2 lines
                        if len(res['ana_name']) > 90:
                            h_now += h_name
                            # Pdf.log.error(Logs.fileline() + ' : DEBUG ANA on 2 lines h_now=' + str(h_now))

                        # Pdf.log.error(Logs.fileline() + ' : DEBUG NAME=' + res['ana_name'] + '\n---------')

                    # AFTER a new line CUT PAGE OR NOT
                    if h_now > (h_max - h_res):
                        # Pdf.log.error(Logs.fileline() + ' : DEBUG ANA h_now=' + str(h_now) + ' > h_max - h_res =' + str(h_max - h_res))
                        form_cont = Pdf.PdfReportCutPageOrNot(form_cont, num_page, h_page, report_status, div_first_page, rec_comm, result_div, full_header, num_rec_y)

                        num_page = num_page + 1

                        # REINIT for next page
                        h_now  = 0
                        h_page = h_max - h_footer - h_header

                        result_div = ''

                # Start to get previous result if exist
                prev = ''

                res_prev = Result.getPreviousResult(res['id_pat'], res['id_ref_ana'], res['id_data'], res['id_res'])

                if res_prev:
                    prev = datetime.strftime(res_prev['date_valid'], '%d/%m/%Y') + ' : '

                # Get label of value
                type_res = Various.getDicoById(res['type_resultat'])

                if type_res and type_res['short_label'].startswith("dico_"):
                    Various.useLangDB()
                    trans = type_res['short_label'][5:]
                    type_res = _(trans)
                    Various.useLangPDF()
                else:
                    type_res = ''

                # Value to be interpreted
                if type_res and res['value']:
                    Various.useLangDB()
                    val = Various.getDicoById(res['value'])
                    trans = val['label']
                    val = _(trans)

                    if res_prev and res_prev['valeur']:
                        label_prev = Various.getDicoById(res_prev['valeur'])
                        trans = label_prev['label']
                        prev += _(trans)
                    else:
                        prev = ''

                    Various.useLangPDF()
                # Numerical value or canceled
                else:
                    is_bold = False

                    val = res['value']
                    # Cancel result
                    if not val:
                        val  = _("Annulée")
                        prev = ''
                    elif res_prev and res_prev['valeur']:
                        prev += res_prev['valeur']

                    if res['normal_min'] and res['normal_max']:
                        if val != _("Annulée"):
                            # bold style if out of range min/max
                            if float(val) < float(res['normal_min']) or float(val) > float(res['normal_max']):
                                val = '<b>' + val + '</b>'
                                is_bold = True

                    if res['unite'] and val != _("Annulée"):
                        unit = Various.getDicoById(res['unite'])

                        if unit:
                            if is_bold:
                                val  += '&nbsp;<b>' + unit['label'] + '</b>'
                            else:
                                val  += '&nbsp;' + unit['label']

                            if prev:
                                prev += '&nbsp;' + unit['label']

                # Get normal of value
                ref = ''

                if res['normal_min'] and res['normal_max']:
                    ref = '[ ' + str(res['normal_min']) + ' - ' + str(res['normal_max']) + ' ]'

                # ==== ANALYSIS RESULT ====
                Various.useLangDB()
                trans = str(res['libelle'])
                result_div += ('<div style="margin-bottom:10px;">'
                               '<span class="ft_res_label" style="width:365px;display:inline-block;text-align:left;'
                               'padding-left:12px;">' + _(trans) + '</span>'
                               '<span class="ft_res_value" style="width:150px;display:inline-block;text-align:right;">' +
                               str(val) + '</span>'
                               '<span class="ft_res_ref" style="width:210px;display:inline-block;text-align:center;">' +
                               str(ref) + '</span>'
                               '<span class="ft_res_prev" style="width:220px;display:inline-block;text-align:right;">' +
                               str(prev) + '</span></div>')
                h_now += h_res

                # IF libelle on 2 lines
                trans = res['libelle']
                if len(_(trans)) > 46 or len(val) > 16 or len(prev) > 32:
                    nb_lib  = math.ceil(len(_(trans)) / 46)
                    nb_val  = math.ceil(len(val) / 16)
                    nb_prev = math.ceil(len(prev) / 32)

                    nb_line = max(nb_lib, nb_val, nb_prev)

                    h_now = h_now + nb_line * h_res2

                    # Pdf.log.error(Logs.fileline() + ' : DEBUG RES ' + res['libelle'] + ' on ' + str(nb_line) + ' lines h_now=' + str(h_now))
                Various.useLangPDF()

                # Pdf.log.error(Logs.fileline() + ' : DEBUG res[libelle]=' + str(res['libelle']))
                # Pdf.log.error(Logs.fileline() + ' : DEBUG h_now=' + str(h_now) + ' | h_max - h_res=' + str(h_max - h_res) + '\n')

                # AFTER a new line CUT PAGE OR NOT
                if h_now > (h_max - h_res):
                    # Pdf.log.error(Logs.fileline() + ' : DEBUG RES h_now=' + str(h_now) + ' > h_max - h_res =' + str(h_max - h_res))
                    form_cont = Pdf.PdfReportCutPageOrNot(form_cont, num_page, h_page, report_status, div_first_page, rec_comm, result_div, full_header, num_rec_y)

                    num_page = num_page + 1

                    # REINIT for next page
                    h_now  = 0
                    h_page = h_max - h_footer - h_header

                    result_div = ''

            # --- END OF LOOP RESULT ---

            if result_div:
                # comment and who make validation
                res_valid = Result.getResultValidation(id_res_p)

                user = User.getUserByIdGroup(res_valid['utilisateur'])

                if user['lastname'] and user['firstname']:
                    user = user['lastname'] + ' ' + user['firstname']
                else:
                    user = user['username']

                if res_valid['commentaire']:
                    res_comm = res_valid['commentaire']
                else:
                    res_comm = ''

                if full_comm:
                    comm_div = ('<div><span class="ft_res_comm" style="width:970px;display:inline-block;'
                                'text-align:left;"">' + str(res_comm) + '</span></div>')
                else:
                    comm_div = ''

                result_div = (result_div + comm_div + '<div><span class="ft_res_valid" style="width:970px;'
                              'display:inline-block;text-align:left;">' + _("validé par") + ' : ' + str(user) +
                              '</span></div')

                form_cont = Pdf.PdfReportCutPageOrNot(form_cont, num_page, h_page, report_status, div_first_page, rec_comm, result_div, full_header, num_rec_y)

            form_cont = form_cont.replace("tot_page", str(num_page))

        options = {'encoding': 'utf-8',
                   'page-size': 'A4',
                   'margin-top': '12.00mm',
                   'margin-right': '0.00mm',
                   'margin-bottom': '0.00mm',
                   'margin-left': '0.00mm',
                   'no-outline': None}

        # Pdf.log.error(Logs.fileline() + ' : DEBUG form_cont=' + str(form_cont))

        pdfkit.from_string(form_cont, path + filename, options=options)

        return True

    @staticmethod
    def PdfReportCutPageOrNot(form_cont, num_page, h_page, report_status, div_first_page, rec_comm, result_div, full_header, num_rec_y):
        """End html of current page for report

        This function is call by getPdfReport

        Args:
            form_cont      (string): html string of all pages.
            num_page          (int): current page number.
            h_page            (int): height of page in pixels.
            report_status  (string): status of report.
            div_first_page (string): html string to start a first page.
            rec_comm       (string): record comment.
            result_div     (string): html string of last result.
            full_header    (string): html string of header page.
            num_rec_y         (int): record number.

        Returns:
            string: html string.

        """

        Various.useLangPDF()

        report_div = ('<div style="width:980px;min-height:' + str(h_page) + 'px;' +
                      'border:2px solid dimgrey;border-radius:10px;padding:10px;margin-top:20px;' +
                      'background-color:#FFF;">')

        report_div = report_div + result_div + '</div>'  # closing report_div

        if num_page == 1:
            report_status = ('<span style="max-height:60px;padding:2px;border:2px double #000;">' +
                             _(report_status) + '</span>')

            page_header = Pdf.getPdfHeader(full_header, report_status)

            page_body = (div_first_page + '<div style="width:1000px;margin-top:10px;margin-bottom:0px;'
                         'background-color:#FFF;">'
                         '<span class="ft_cat_tit" style="width:400px;display:inline-block;text-align:left;'
                         'padding-left:20px;">' + _("ANALYSE") + '</span>'
                         '<span class="ft_cat_tit" style="width:150px;display:inline-block;text-align:center;">' +
                         _("RESULTAT") + '</span>'
                         '<span class="ft_cat_tit" style="width:200px;display:inline-block;text-align:center;">' +
                         _("Intervalle de référence") + '</span>'
                         '<span class="ft_cat_tit" style="width:180px;display:inline-block;text-align:right;'
                         'padding-right:20px;">' + _("Antériorités") + '</span></div>'
                         '<div style="width:1000px;margin-top:-18px;background-color:#FFF;">' + report_div + '</div>')
        else:
            page_header = ''
            page_body   = ''
            page_body += ('<div style="width:1000px;margin-top:58px;">&nbsp;</div>'
                          '<div style="width:1000px;margin-top:10px;margin-bottom:0px;background-color:#FFF;">'
                          '<span class="ft_cat_tit" style="width:400px;display:inline-block;text-align:left;'
                          'padding-left:20px;">' + _("ANALYSE") + '</span>'
                          '<span class="ft_cat_tit" style="width:150px;display:inline-block;text-align:center;">' +
                          _("RESULTAT") + '</span>'
                          '<span class="ft_cat_tit" style="width:200px;display:inline-block;text-align:center;">' +
                          _("Intervalle de référence") + '</span>'
                          '<span class="ft_cat_tit" style="width:180px;display:inline-block;text-align:right;'
                          'padding-right:20px;">' + _("Antériorités") + '</span></div>'
                          '<div style="width:1000px;margin-top:-18px;background-color:#FFF;">' + report_div + '</div>')

        date_now = datetime.strftime(datetime.now(), "%d/%m/%Y à %H:%M")

        page_footer = ('<div style="width:1000px;margin-top:5px;background-color:#FFF;">'
                       '<div><span class="ft_footer" style="width:900px;display:inline-block;text-align:left;">' +
                       _("Dossier") + str(num_rec_y) + ', ' + _("édité le ") + str(date_now) + '</span>'
                       '<span class="ft_footer" style="width:90px;display:inline-block;text-align:right;">' +
                       _("Page") + ' ' + str(num_page) + '/tot_page</span></div></div>')

        form_cont += page_header + page_body + page_footer

        return form_cont

    @staticmethod
    def getPdfReportGeneric(html_part, filename=''):
        """Built a Generic PDF Report

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
        full_comm   = False

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
    def getPdfHeader(full_header, report_status=''):
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
