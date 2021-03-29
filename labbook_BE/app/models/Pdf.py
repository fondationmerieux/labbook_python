# -*- coding:utf-8 -*-
import logging
import barcode
import pdfkit

from barcode.writer import ImageWriter
from datetime import datetime

from app.models.Analysis import Analysis
from app.models.DB import DB
from app.models.Logs import Logs
from app.models.Constants import Constants
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

        if receipt_num:
            receipt_num = '<div><span class="ft_bill_rec">N° quittance : ' + str(receipt_num) + '</span></div>'
        else:
            receipt_num = ''

        # Get Patient details
        pat = Patient.getPatient(record['id_patient'])

        addr_div = ''

        if pat:
            addr_div += '<div style="width:475px;border:2px solid dimgrey;border-radius:10px;padding:10px;background-color:#FFF;float:right;">'

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

        l_ana = Analysis.getAnalysisReq(id_rec, '')

        bill_div = ''
        ana_div  = ''
        samp_div = ''

        if l_ana:
            bill_div += '<div style="width:980px;height:460px;border:2px solid dimgrey;border-radius:10px;padding:10px;margin-top:20px;background-color:#FFF;">'

            for ana in l_ana:
                # Requested analysis
                if ana['cote_unite'] is None or ana['cote_unite'] != 'PB':
                    if not ana_div:
                        ana_div += '<div><span class="ft_bill_det_tit">Analyses demandées</span></div>'

                    ana_div += """\
                            <div><span class="ft_bill_det" style="width:90px;display:inline-block;text-align:left;">""" + str(ana['code']) + """</span>
                                 <span class="ft_bill_det" style="width:750px;display:inline-block;">""" + str(ana['nom']) + """</span>
                                 <span class="ft_bill_det" style="width:120px;display:inline-block;text-align:right;">""" + str(ana['prix']) + """</span></div>"""

                # Requested samples
                if ana['cote_unite'] == 'PB':
                    if not samp_div:
                        samp_div += '<div><span class="ft_bill_det_tit">Actes de prélèvements</span></div>'

                    # No display of samples without price
                    if ana['prix'] > 0:
                        samp_div += """\
                                <div><span class="ft_bill_det" style="width:90px;display:inline-block;text-align:left;">""" + str(ana['code']) + """</span>
                                     <span class="ft_bill_det" style="width:750px;display:inline-block;">""" + str(ana['nom']) + """</span>
                                     <span class="ft_bill_det" style="width:120px;display:inline-block;text-align:right;">""" + str(ana['prix']) + """</span></div>"""

            if ana_div:
                bill_div += ana_div + '<br />'

            if samp_div:
                bill_div += samp_div + '<br />'

            # bill_price and bill_remain
            bill_div += """\
                    <div><span class="ft_bill_det_tit" style="width:100px;display:inline-block;text-align:left;">Total</span>
                         <span class="ft_bill_det_tot" style="width:870px;display:inline-block;text-align:right;"">""" + str(record['prix']) + """</span>
                    </div>
                    <div><span class="ft_bill_det_tit" style="width:160px;display:inline-block;text-align:left;">Total à payer</span>
                         <span class="ft_bill_det_tot" style="width:810px;display:inline-block;text-align:right;">""" + str(record['a_payer']) + """</span>
                    </div>"""

            bill_div += '</div>'

        page_header = Pdf.getPdfHeader(full_header)

        page_body = """\
                <div style="width:1000px;">
                    <div style="width:475px;padding:10px;background-color:#FFF;float:left;">
                        <div><span class="ft_bill_num">FACTURE : """ + str(bill_num) + """</span></div>
                        <div><span class="ft_bill_rec">N° dossier : """ + str(num_rec_y) + """</span></div>
                        """ + receipt_num + """
                    </div>
                    """ + addr_div + """
                    <div style="clear:both;"></div>
                    """ + bill_div + """
                </div>"""

        date_now = datetime.strftime(datetime.now(), "%d/%m/%Y à %H:%M")

        page_footer = """\
                <div style="width:1000px;margin-top:5px;background-color:#FFF;">
                    <div><span class="ft_footer" style="width:900px;display:inline-block;text-align:left;">Facture n°""" + str(bill_num) + """, édité le """ + str(date_now) + """</span>
                         <span class="ft_footer" style="width:90px;display:inline-block;text-align:right;">Page 1/1</span></div>
                </div>
                <hr style="width:100%;border-top: 2px dashed dimgrey;">"""

        page_footer += '</div>'

        filename = 'facture_' + num_rec_y + '.pdf'

        form_cont = page_header + page_body + page_footer

        options = {'--encoding': 'utf-8',
                   'page-size': 'A4',
                   'margin-top': '0.00mm',
                   'margin-right': '0.00mm',
                   'margin-bottom': '0.00mm',
                   'margin-left': '0.00mm',
                   'no-outline': None}

        pdfkit.from_string(form_cont, path + filename, options=options)

        return True

    @staticmethod
    def getPdfBillList(l_datas, date_beg, date_end):
        path = Constants.cst_path_tmp

        # Get format header
        pdfpref = Pdf.getPdfPref()

        full_header = True

        if pdfpref and pdfpref['entete'] == 1069:
            full_header = False

        bill_div = ''

        total_price  = 0
        total_remain = 0

        bill_div += ('<span>ETAT DE LA FACTURATION DU ' + str(date_beg) + ' AU ' + str(date_end) + '</span>'
                     '<div style="width:980px;height:600px;border:2px solid dimgrey;border-radius:10px;padding:10px;margin-top:20px;background-color:#FFF;">'
                     '<table style="width:100%"><thead>'
                     '<th style="text-align:left;">N° dossier</th>'
                     '<th style="text-align:left;">N° quittance</th>'
                     '<th style="text-align:left;">N° facture</th>'
                     '<th>Prix</th>'
                     '<th>A payer</th></thead>'
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
        bill_div += """\
                <tr><td colspan="5"></td></tr>
                <tr><td class="ft_bill_det_tit" style="text-align:left;">Total</td>
                    <td colspan="3" class="ft_bill_det_tot" style="text-align:right;"">""" + str(total_price) + """</td>
                    <td class="ft_bill_det_tot" style="text-align:right;">""" + str(total_remain) + """</td>
                </tr>"""

        bill_div += '</table></div>'

        page_header = Pdf.getPdfHeader(full_header)

        page_body = bill_div

        date_now = datetime.strftime(datetime.now(), "%d/%m/%Y à %H:%M")

        page_footer = """\
                <div style="width:1000px;margin-top:5px;background-color:#FFF;">
                    <div><span class="ft_footer" style="width:900px;display:inline-block;text-align:left;">Etat de la facturation, édité le """ + str(date_now) + """</span>
                         <span class="ft_footer" style="width:90px;display:inline-block;text-align:right;">Page 1/1</span></div>
                </div>
                <hr style="width:100%;border-top: 2px dashed dimgrey;">"""

        page_footer += '</div>'

        date_now = datetime.now()
        today    = date_now.strftime("%Y%m%d")

        filename = 'list_bill_' + today + '.pdf'

        form_cont = page_header + page_body + page_footer

        options = {'--encoding': 'utf-8',
                   'page-size': 'A4',
                   'margin-top': '0.00mm',
                   'margin-right': '0.00mm',
                   'margin-bottom': '0.00mm',
                   'margin-left': '0.00mm',
                   'no-outline': None}

        pdfkit.from_string(form_cont, path + filename, options=options)

        return True

    @staticmethod
    def getPdfReport(id_rec, filename):
        path = Constants.cst_report

        # Get format header
        pdfpref = Pdf.getPdfPref()

        full_header = True
        full_comm   = False

        if pdfpref and pdfpref['entete'] == 1069:
            full_header = False

        if pdfpref and pdfpref['commentaire'] == 1049:
            full_comm = True

        # Get record details
        record = Record.getRecord(id_rec)

        num_rec_y = record['num_dos_an']

        # Get Patient details
        pat = Patient.getPatient(record['id_patient'])

        # Patient birth
        birth = 'Né le '

        if pat['ddn']:
            birth += datetime.strftime(pat['ddn'], '%d/%m/%Y') + ' - '
        else:
            birth = ''

        # Patient Age
        age = str(pat['age'])

        if pat['unite'] == 1037:
            age += ' ans'
        elif pat['unite'] == 1036:
            age += ' mois'
        elif pat['unite'] == 1035:
            age += ' semaines'
        elif pat['unite'] == 1034:
            age += ' jours'

        # Patient Sex
        sex = ''

        if pat['sexe'] == 1:
            sex += 'Masculin'
        elif pat['sexe'] == 2:
            sex += 'Feminin'
        elif pat['sexe'] == 3:
            sex += 'Inconnu'

        # Block det record
        date_now = datetime.strftime(datetime.now(), "%d/%m/%Y")

        rec_div  = '<div style="width:465px;height:100px;border:2px solid dimgrey;border-radius:10px;padding:10px;background-color:#FFF;float:left;">'

        rec_div += '<div><span class="ft_rec_det">Dossier ' + str(num_rec_y) + ' de ' + str(pat['prenom']) + '&nbsp;' + str(pat['nom']) + '</span></div>'
        rec_div += '<div><span class="ft_rec_det">' + str(birth) + str(age) + ' - ' + str(sex) + ' - Code '

        if pat['code_patient']:
            rec_div += str(pat['code_patient']) + ' / ' + str(pat['code']) + '</span></div>'
        else:
            rec_div += str(pat['code']) + '</span></div>'

        if 'type' in record and record['type'] == 184:
            rec_div += '<div><span class="ft_rec_det">'

            if record['date_hosp']:
                rec_div += 'Admis le ' + datetime.strftime(record['date_hosp'], '%d/%m/%Y') + ' '

            if record['service_interne']:
                rec_div += 'en ' + str(record['service_interne']) + ' - '

            if record['num_lit']:
                rec_div += 'Lit ' + str(record['num_lit'])

            rec_div += '</span></div>'
            
        rec_div += '<div><span class="ft_rec_det">Examen prescrit le ' + datetime.strftime(record['date_prescription'], '%d/%m/%Y') + '</span></div>'
        rec_div += '<div><span class="ft_rec_det">Enregistré le ' + datetime.strftime(record['date_dos'], '%d/%m/%Y') + ', édité le ' + str(date_now) + '</span></div>'

        rec_div += '</div>'

        # Block patient address
        addr_div = ''

        if pat:
            addr_div += '<div style="width:465px;height:100px;border:2px solid dimgrey;border-radius:10px;padding:10px;background-color:#FFF;float:right;">'

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

        # clinical information (= commentary in record)
        rec_comm = ''

        if full_comm and record['rc']:
            rec_comm  = '<div style="width:980px;border:2px solid dimgrey;border-radius:10px;padding:10px;margin-top:5px;background-color:#FFF;">'
            rec_comm += '<span class="ft_res_name">Renseignements cliniques</span><br />'
            rec_comm += '<span class="ft_rec_det">' + str(record['rc']) + '</span></div>'

        l_res = Result.getResultRecord(id_rec, False)

        id_ana_p = 0
        id_res_p = 0
        id_user_valid_p = 0

        report_div = '<div style="width:980px;min-height:900px;border:2px solid dimgrey;border-radius:10px;padding:10px;margin-top:20px;background-color:#FFF;">'
        res_div    = ''

        if l_res:
            for res in l_res:
                # New analysis div
                if res['id_ana'] != id_ana_p and res['id_res'] != id_res_p:
                    # close previous analysis div
                    if id_ana_p > 0:
                        res_div += '</div>'
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
                                comm_div = '<div><span class="ft_res_comm" style="width:970px;display:inline-block;text-align:left;"">' + str(res_comm) + '</span></div>'
                            else:
                                comm_div = ''

                            res_div += comm_div + """\
                                    <div><span class="ft_res_valid" style="width:970px;display:inline-block;text-align:left;">validé par : """ + str(user) + """</span></div>"""

                    id_ana_p = res['id_ana']
                    id_res_p = res['id_res']

                    Pdf.log.error(Logs.fileline() + ' : DEBUG id_ana=' + str(id_ana_p) + ' | id_res=' + str(id_res_p) + ' | ref_ana=' + str(res['ref_ana']))

                    res_name = ''
                    res_fam  = ''

                    if res['famille']:
                        res_fam = res['famille']

                    if res['nom']:
                        res_name = res['nom']

                    # Start div of an analysis
                    res_div += '<div>'

                    if res_fam:
                        res_div += '<span class="ft_res_fam" style="width:960px;display:inline-block;text-align:center;">' + res_fam + '</span>'

                    if res_name:
                        res_div += '<span class="ft_res_name" style="width:960px;display:inline-block;text-align:left;">' + res_name + '</span>'

                # Start to get previous result if exist
                prev = ''

                res_prev = Result.getPreviousResult(res['id_pat'], res['ref_ana'], res['id_data'], res['id_res'])

                if res_prev:
                    prev = datetime.strftime(res_prev['date_valid'], '%d/%m/%Y') + ' : '

                # Get label of value
                type_res = Various.getDicoById(res['type_resultat'])

                if type_res and type_res['short_label'].startswith("dico_"):
                    type_res = type_res['short_label'][5:]
                else:
                    type_res = ''

                if type_res and res['valeur']:
                    val = Various.getDicoById(res['valeur'])
                    val = val['label']

                    if res_prev and res_prev['valeur']:
                        label_prev = Various.getDicoById(res_prev['valeur'])
                        prev += label_prev['label']
                    else:
                        prev = ''
                else:
                    val = res['valeur']
                    # Cancel result
                    if not val:
                        val  = 'Annulée'
                        prev = ''
                    elif res_prev and res_prev['valeur']:
                        prev += res_prev['valeur']

                    if res['unite'] and val != 'Annulée':
                        unit = Various.getDicoById(res['unite'])
                        if unit:
                            val  += '&nbsp;' + unit['label']
                            if prev:
                                prev += '&nbsp;' + unit['label']

                # Get normal of value
                ref = ''

                if res['normal_min'] and res['normal_max']:
                    ref = '[ ' + str(res['normal_min']) + ' - ' + str(res['normal_max']) + ' ]'

                # new line of result
                res_div += """<div style="margin-bottom:10px;">\
                             <span class="ft_res_label" style="width:360px;display:inline-block;text-align:left;padding-left:15px;">""" + str(res['libelle']) + """</span>
                             <span class="ft_res_value" style="width:150px;display:inline-block;text-align:right;">""" + str(val) + """</span>
                             <span class="ft_res_ref" style="width:210px;display:inline-block;text-align:center;">""" + str(ref) + """</span>
                             <span class="ft_res_prev" style="width:220px;display:inline-block;text-align:right;">""" + str(prev) + """</span></div>"""

            if res_div:
                report_div += res_div

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
                    comm_div = '<div><span class="ft_res_comm" style="width:970px;display:inline-block;text-align:left;"">' + str(res_comm) + '</span></div>'
                else:
                    comm_div = ''

                report_div += comm_div + """\
                        <div><span class="ft_res_valid" style="width:970px;display:inline-block;text-align:left;">validé par : """ + str(user) + """</span></div>
                        </div>"""

        report_div += '</div>'

        page_header = Pdf.getPdfHeader(full_header)

        page_body = """\
                <div style="width:1000px;">""" + rec_div + addr_div + """</div>
                <div class="ft_report_tit" style="clear:both;text-align:center;padding-top:10px;background-color:#FFF;">Compte rendu</div>
                """ + rec_comm + """
                <div style="width:1000px;margin-top:10px;margin-bottom:0px;background-color:#FFF;">
                    <span class="ft_cat_tit" style="width:400px;display:inline-block;text-align:left;padding-left:20px;">ANALYSE</span>
                    <span class="ft_cat_tit" style="width:150px;display:inline-block;text-align:center;">RESULTAT</span>
                    <span class="ft_cat_tit" style="width:200px;display:inline-block;text-align:center;">Intervalle de référence</span>
                    <span class="ft_cat_tit" style="width:180px;display:inline-block;text-align:right;padding-right:20px;">Antériorités</span>
                </div>
                <div style="width:1000px;margin-top:-18px;background-color:#FFF;">""" + report_div + """</div>"""

        page_footer = """\
                <div style="width:1000px;margin-top:5px;background-color:#FFF;">
                    <div><span class="ft_footer" style="width:970px;display:inline-block;text-align:right;">Page 1/1</span></div>
                </div>"""

        page_footer += '</div>'

        form_cont = page_header + page_body + page_footer

        options = {'--encoding': 'utf-8',
                   'page-size': 'A4',
                   'margin-top': '0.00mm',
                   'margin-right': '0.00mm',
                   'margin-bottom': '0.00mm',
                   'margin-left': '0.00mm',
                   'no-outline': None}

        pdfkit.from_string(form_cont, path + filename, options=options)

        return True

    @staticmethod
    def getPdfReportGeneric(html_part, filename=''):
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

        page_body = """<div style="width:1000px;">""" + html_part + """</div>"""

        page_footer = '</div>'

        form_cont = page_header + page_body + page_footer

        options = {'--encoding': 'utf-8',
                   'page-size': 'A4',
                   'margin-top': '0mm',
                   'margin-right': '0mm',
                   'margin-bottom': '0mm',
                   'margin-left': '0mm',
                   'no-outline': None}

        pdfkit.from_string(form_cont, path + filename, options=options)

        return True

    @staticmethod
    def getPdfHeader(full_header):
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
                <div style='padding:50px;width:1000px;height:1410px;border:0px;font-family:arial;background-color:#FFF;color:black;font-size:20px;'>"""

        head_logo = '<img src="' + Constants.cst_resource + 'logo.png" width="230px;">'

        head_name  = Various.getDefaultValue('entete_1')
        head_line2 = Various.getDefaultValue('entete_2')
        head_line3 = Various.getDefaultValue('entete_3')
        head_addr  = Various.getDefaultValue('entete_adr')
        head_phone = Various.getDefaultValue('entete_tel')
        head_fax   = Various.getDefaultValue('entete_fax')
        head_email = Various.getDefaultValue('entete_email')

        extra_header = ''

        if full_header:
            extra_header += """\
                        <div><span style="font: 15px 'Helvetica';">""" + str(head_line2['value']) + """</span></div>
                        <div><span style="font: 15px 'Helvetica';">""" + str(head_line3['value']) + """</span></div>"""

        if head_phone['value']:
            phone = """<span class="ft_header">TEL : """ + str(head_phone['value']) + """&nbsp;</span>"""
        else:
            phone = ''

        if head_fax['value']:
            fax = """<span class="ft_header">FAX : """ + str(head_fax['value']) + """&nbsp;</span>"""
        else:
            fax = ''

        if head_email['value']:
            email = """<span class="ft_header">EMAIL : """ + str(head_email['value']) + """&nbsp;</span>"""
        else:
            email = ''

        header += """\
                <div style="width:1000px;height:140px;background-color:#FFF;">
                    <div style="float:left;width:250px;">""" + head_logo + """</div>
                    <div style="float:right;width:750px;">
                        <div><span class="ft_lab_name">""" + str(head_name['value']) + """</span></div>
                        """ + extra_header + """
                        <div><span class="ft_header">""" + str(head_addr['value']) + """</span></div>
                        <div>""" + phone + fax + email + """</div>
                    </div>
                </div>"""

        return header

    @staticmethod
    def getPdfPref():
        cursor = DB.cursor()

        req = 'select id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, entete, commentaire '\
              'from sigl_param_cr_data '\
              'limit 1'

        cursor.execute(req)

        return cursor.fetchone()
