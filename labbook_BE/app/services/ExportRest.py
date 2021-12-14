# -*- coding:utf-8 -*-
import logging

from gettext import gettext as _
from datetime import datetime, timedelta
from flask import request
from flask_restful import Resource

from app.models.General import compose_ret
from app.models.Constants import Constants
from app.models.Various import Various
from app.models.Export import Export
from app.models.Report import Report
from app.models.Logs import Logs
from app.models.User import User


class ExportCSV(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        if 'filename' not in args or 'csv_str' not in args:
            self.log.error(Logs.fileline() + ' : TRACE ExportCSV ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # write csv file
        try:
            f = open('tmp/' + args['filename'], "w")
            f.write(args['csv_str'])
            f.close()

        except Exception as err:
            self.log.error(Logs.fileline() + ' : post ExportWhonet failed, err=%s', err)
            return False

        self.log.info(Logs.fileline() + ' : TRACE ExportCSV')
        return compose_ret('', Constants.cst_content_type_json)


class ExportDHIS2(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        if 'date_beg' not in args or 'filename' not in args or 'id_user' not in args:
            self.log.error(Logs.fileline() + ' : TRACE ExportDHIS2 ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # Read CSV spreadsheet
        import os

        from csv import reader

        path = Constants.cst_dhis2

        with open(os.path.join(path, args['filename']), 'r', encoding='utf-8') as csv_file:
            csv_reader = reader(csv_file, delimiter=';')
            l_rows = list(csv_reader)

        if not l_rows or len(l_rows) < 2:
            self.log.error(Logs.fileline() + ' : TRACE ExportDHIS2 ERROR spreadsheet empty')
            return compose_ret('', Constants.cst_content_type_json, 500)

        version = l_rows[1][2]

        if version != 'v1':
            self.log.error(Logs.fileline() + ' : TRACE ExportDHIS2 ERROR spreadsheet wrong version')
            return compose_ret('', Constants.cst_content_type_json, 409)

        # Determine the period
        period = l_rows[1][1]

        # Determine orgunit
        orgunit = ''

        if version != 'v1' and l_rows[1][7]:
            orgunit = l_rows[1][7]

        # Determine storedby
        storedby = ''

        if version != 'v1' and l_rows[1][8]:
            storedby = l_rows[1][8]

        date_beg = datetime.strptime(args['date_beg'], '%Y-%m-%d')

        if period == 'M':
            month = date_beg.month

            if month < 10:
                month = '0' + str(month)

            period = str(date_beg.year) + month

            date_beg_db = date_beg.replace(day=1)

            # get close to the end of the month for any day, and add 4 days 'over'
            next_month = date_beg.replace(day=28) + timedelta(days=4)
            # subtract the number of remaining 'overage' days to get last day of current month,
            # or said programattically said, the previous day of the first of next month
            date_end_db = next_month - timedelta(days=next_month.day)
        elif period == 'W':
            period = str(date_beg.year) + 'W' + str(date_beg.isocalendar()[1])

            date_beg_db = date_beg - timedelta(days=date_beg.weekday())
            date_end_db = date_beg_db + timedelta(days=6)
        else:
            self.log.error(Logs.fileline() + ' : TRACE ExportDHIS2 ERROR period=' + str(period))
            return compose_ret('', Constants.cst_content_type_json, 500)

        # Data
        l_data = [["dataelement", "period", "orgunit", "categoryoptioncombo", "attributeoptioncombo", "value", "storedby",
                   "lastupdated", "comment", "followup", "deleted"]]

        date_now = datetime.now()

        lab_name = ''

        lab = Various.getDefaultValue('entete_1')

        if lab:
            lab_name = lab['value']

        user = User.getUserDetails(args['id_user'])

        user_ident = ''

        if user:
            user_ident = user['firstname'] + user['lastname']

        # remove space
        user_ident = user_ident.replace(' ', '')

        if l_rows:
            # remove headers line
            l_rows.pop(0)

            for l in l_rows:

                if l:
                    data = []

                    data.append(l[0])
                    data.append(period)

                    if orgunit:
                        data.append(orgunit)
                    else:
                        data.append(lab_name)

                    data.append(l[5])
                    data.append(l[6])

                    # Parse formula for result request
                    formula   = l[3]
                    type_samp = l[4]

                    req_part = ''

                    req_part = Report.ParseFormula(formula, type_samp)

                    result = Report.getResultEpidemio(inner_req=req_part['inner'],
                                                      end_req=req_part['end'],
                                                      date_beg=date_beg_db,
                                                      date_end=date_end_db)

                    if result:
                        data.append(str(result['value']))
                    else:
                        data.append('')

                    if storedby:
                        data.append(storedby)
                    else:
                        data.append(user_ident)

                    data.append(date_now.strftime("%Y-%m-%dT%H:%M:%S"))
                    data.append('')
                    data.append('FALSE')
                    data.append('')

                    l_data.append(data)

        self.log.error(Logs.fileline() + ' : l_data=' + str(l_data))

        # if no result to export
        if len(l_data) < 2:
            return compose_ret('', Constants.cst_content_type_json, 404)

        # write csv file
        try:
            import csv

            filename = 'dhis2_' + args['filename'][:-4] + '_' + args['date_beg'] + '.csv'

            with open('tmp/' + filename, mode='w', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=',')
                for line in l_data:
                    writer.writerow(line)

        except Exception as err:
            self.log.error(Logs.fileline() + ' : post ExportDHIS2 failed, err=%s', err)
            return False

        self.log.info(Logs.fileline() + ' : TRACE ExportDHIS2')
        return compose_ret('', Constants.cst_content_type_json)


class ExportWhonet(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        if 'date_beg' not in args or 'date_end' not in args:
            self.log.error(Logs.fileline() + ' : TRACE ExportWhonet ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # Data
        l_data = [["Laboratoire", "Lab adresse", "Lab ville", "Téléphone laboratoire", "Email laboratoire",
                   "Specialité du prescripteur", "Numéro d'identification", "Nom de famille",
                   "Prénom", "Nom et prénom ", "Sexe", "Date de naissance", "Age", "Catégorie d'âge", "Adresse (patient)",
                   "Ville (patient)", "Code postal (patient)", "Téléphone (patient)", "Profession (patient)",
                   "Date d'admission", "Service demandeur", "Numéro de lit", "Type patient", "Isolate number",
                   "Numéro de prélèvement", "Date de prélèvement", "Type de prélèvement", "Commentaire de prélèvement",
                   "Micro-organisme", "Nom de l'antibiotique", "Methode de détermination", "Method value",
                   "Resultat d'antibiotique"]]
        dict_data = Export.getDataWhonet(args['date_beg'], args['date_end'])

        Various.needTranslationDB()

        if dict_data:
            for d in dict_data:
                data = []

                # LAB PART
                if d['lab_name']:
                    data.append(d['lab_name'])
                else:
                    data.append('')

                if d['lab_addr']:
                    data.append(d['lab_addr'])
                else:
                    data.append('')

                if d['lab_city']:
                    data.append(d['lab_city'])
                else:
                    data.append('')

                if d['lab_phone']:
                    data.append(d['lab_phone'])
                else:
                    data.append('')

                if d['lab_email']:
                    data.append(d['lab_email'])
                else:
                    data.append('')

                if d['med_spe']:
                    spe = d['med_spe']
                    data.append(_(spe.strip()))
                else:
                    data.append('')

                # PATIENT PART
                if d['pat_code']:
                    data.append(d['pat_code'])
                else:
                    data.append('')

                if d['pat_name']:
                    data.append(d['pat_name'])
                else:
                    data.append('')

                if d['pat_fname']:
                    data.append(d['pat_fname'])
                else:
                    data.append('')

                if d['pat_name'] and d['pat_fname']:
                    data.append(d['pat_name'] + ' ' + d['pat_fname'])
                else:
                    data.append('')

                if d['sex']:
                    data.append(d['sex'])
                else:
                    data.append('Inconnu')

                if d['ddn']:
                    d['ddn'] = datetime.strftime(d['ddn'], '%Y-%m-%d')
                    data.append(d['ddn'])
                else:
                    data.append('')

                if d['age']:
                    data.append(d['age'])
                else:
                    data.append('')

                if d['cat_age']:
                    if int(d['cat_age']) == 1037:
                        data.append(_('Années'))
                    elif int(d['cat_age']) == 1036:
                        data.append(_('Mois'))
                    elif int(d['cat_age']) == 1035:
                        data.append(_('Semaines'))
                    elif int(d['cat_age']) == 1034:
                        data.append(_('Jours'))
                    else:
                        data.append('')
                else:
                    data.append('')

                if d['pat_addr']:
                    data.append(d['pat_addr'])
                else:
                    data.append('')

                if d['pat_city']:
                    data.append(d['pat_city'])
                else:
                    data.append('')

                if d['pat_zip']:
                    data.append(d['pat_zip'])
                else:
                    data.append('')

                if d['pat_phone']:
                    data.append(d['pat_phone'])
                else:
                    data.append('')

                if d['pat_class']:
                    data.append(d['pat_class'])
                else:
                    data.append('')

                if d['date_hosp']:
                    d['date_hosp'] = datetime.strftime(d['date_hosp'], '%Y-%m-%d')
                    data.append(d['date_hosp'])
                else:
                    data.append('')

                if d['service_interne']:
                    service = d['service_interne']
                    data.append(_(service.strip()))
                else:
                    data.append('')

                if d['num_lit']:
                    data.append(d['num_lit'])
                else:
                    data.append('')

                if d['rec_type']:
                    rec_type = d['rec_type']
                    data.append(_(rec_type.strip()))
                else:
                    data.append('')

                if d['ana_code']:
                    data.append(d['ana_code'])
                else:
                    data.append('')

                # SPECIMEN PART
                if d['spec_code']:
                    data.append(d['spec_code'])
                elif d['num_dos_an'] and d['code_patient']:
                    num_samp = str(d['num_dos_an']) + str(d['code_patient'])
                    data.append(num_samp)
                else:
                    data.append('')

                if d['spec_date']:
                    d['spec_date'] = datetime.strftime(d['spec_date'], '%Y-%m-%d')
                    data.append(d['spec_date'])
                else:
                    data.append('')

                if d['spec_type']:
                    spec_type = d['spec_type']
                    data.append(_(spec_type.strip()))
                else:
                    data.append('')

                if d['spec_comment']:
                    data.append(d['spec_comment'])
                else:
                    data.append('')

                # ANALYSIS PART
                if d['ana_name']:
                    ana_name = d['ana_name']
                    ana_name = ana_name[14:]  # delete "Antibiogramme"

                    start_meth = ana_name.find('[')  # search where method starts
                    end_meth   = ana_name.find(']')  # search where method ends

                    method_name = ana_name[start_meth + 1:end_meth]

                    ana_name = ana_name[0:start_meth - 1]

                    data.append(_(ana_name.strip()))
                    libel = d['libelle']
                    data.append(_(libel.strip()))
                    data.append(method_name)
                    data.append(d['method_value'])
                    data.append(d['valeur'])

                l_data.append(data)  # list(d.values()))

        self.log.error(Logs.fileline() + ' : l_data=' + str(l_data))

        # if no result to export
        if len(l_data) < 2:
            return compose_ret('', Constants.cst_content_type_json, 404)

        # write csv file
        try:
            import csv

            filename = 'whonet_' + args['date_beg'] + '_' + args['date_end'] + '.txt'

            with open('tmp/' + filename, mode='w', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter='\t')
                for line in l_data:
                    writer.writerow(line)

        except Exception as err:
            self.log.error(Logs.fileline() + ' : post ExportWhonet failed, err=%s', err)
            return False

        self.log.info(Logs.fileline() + ' : TRACE ExportWhonet')
        return compose_ret('', Constants.cst_content_type_json)
