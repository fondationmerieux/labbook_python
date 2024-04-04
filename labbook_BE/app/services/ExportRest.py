# -*- coding:utf-8 -*-
import logging
import gettext

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
from app.models.Setting import Setting


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

        if 'date_beg' not in args or 'date_end' not in args or 'filename' not in args or 'id_user' not in args or \
           'period' not in args:
            self.log.error(Logs.fileline() + ' : TRACE ExportDHIS2 ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        period   = args['period']
        filename = args['filename'][:-4]

        l_period = []

        # build list of period
        if period == 'W':
            firstday = datetime.strptime(args['date_beg'], '%Y-%m-%d')
            lastday  = datetime.strptime(args['date_end'], '%Y-%m-%d')

            # firstday has to be a monday and lastday a sunday
            firstday = firstday + timedelta(days=-firstday.weekday())
            lastday  = lastday + timedelta(days=6 - lastday.weekday())

            next_monday = firstday + timedelta(days=7)  # firstday + timedelta(days=-firstday.weekday(), weeks=1)
            next_sunday = next_monday - timedelta(days=1)  # next_monday - timedelta(days=1)

            while next_monday < lastday:
                period_interv = []

                tmp_period = datetime.strftime(firstday, "%YW") + str(firstday.isocalendar().week)

                period_interv.append(tmp_period)
                period_interv.append(firstday)
                period_interv.append(next_sunday)

                l_period.append(period_interv)

                firstday = next_monday
                next_monday = firstday + timedelta(days=7)
                next_sunday = next_monday - timedelta(days=1)

            period_interv = []

            tmp_period = datetime.strftime(firstday, "%YW") + str(firstday.isocalendar().week)

            period_interv.append(tmp_period)
            period_interv.append(firstday)
            period_interv.append(lastday)

            l_period.append(period_interv)

        elif period == 'M':
            firstday = datetime.strptime(args['date_beg'], '%Y-%m-%d')
            firstday = firstday.replace(day=1)
            lastday  = datetime.strptime(args['date_end'], '%Y-%m-%d')

            firstday_of_nextmonth = firstday + timedelta(days=31)
            firstday_of_nextmonth = firstday_of_nextmonth.replace(day=1)
            lastday_of_month  = firstday_of_nextmonth - timedelta(days=1)

            while firstday_of_nextmonth < lastday:
                period_interv = []

                tmp_period = datetime.strftime(firstday, "%Y%m")

                period_interv.append(tmp_period)
                period_interv.append(firstday)
                period_interv.append(lastday_of_month)

                l_period.append(period_interv)

                firstday = firstday_of_nextmonth
                firstday_of_nextmonth = firstday + timedelta(days=31)
                firstday_of_nextmonth = firstday_of_nextmonth.replace(day=1)
                lastday_of_month  = firstday_of_nextmonth - timedelta(days=1)

            period_interv = []

            tmp_period = datetime.strftime(firstday, "%Y%m")

            firstday_of_nextmonth = firstday + timedelta(days=31)
            firstday_of_nextmonth = firstday_of_nextmonth.replace(day=1)
            lastday_of_month  = firstday_of_nextmonth - timedelta(days=1)

            period_interv.append(tmp_period)
            period_interv.append(firstday)
            period_interv.append(lastday_of_month)

            l_period.append(period_interv)
        else:
            self.log.error(Logs.fileline() + ' : TRACE ExportDHIS2 ERROR wrong period : ' + str(period))
            return compose_ret('', Constants.cst_content_type_json, 409)

        # --- BUILD DATA ---

        # Pre-defined export
        if filename == "LIST_OUTSOURCING":
            self.log.error(Logs.fileline() + ' : TRACE ExportDHIS2 LIST_OUTSOURCING')

            # Data headers
            l_data = [["period", "code patient", "record number", "record date", "analysis outsourced"]]

            for period in l_period:
                l_rows = Export.getListOutsourcing(period[1], period[2])

                for row in l_rows:
                    if row:

                        data = []

                        code = str(row['code'])

                        if row['code_patient']:
                            code += ' / ' + str(row['code_patient'])

                        num_rec = str(row['num_dos_an'])

                        date_rec = str(row['date_rec'])

                        ana_outsourced = str(row['ana_code']) + ' ' + str(row['ana_name'])

                        data.append(period[0])
                        data.append(code)
                        data.append(num_rec)
                        data.append(date_rec)
                        data.append(ana_outsourced)

                        l_data.append(data)
        else:
            # Data headers
            l_data = [["dataelement", "period", "orgunit", "categoryoptioncombo", "attributeoptioncombo", "value",
                       "storedby", "lastupdated", "comment", "followup", "deleted"]]

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

            l_cols = l_rows[0]  # keep first row to read l_cols of csv

            idx_version = l_cols.index("version")

            if idx_version:
                version = l_rows[1][idx_version]

                if version != 'v1' and version != 'v2' and version != 'v3':
                    self.log.error(Logs.fileline() + ' : TRACE ExportDHIS2 ERROR spreadsheet wrong version :' + str(version))
                    return compose_ret('', Constants.cst_content_type_json, 409)
            else:
                self.log.error(Logs.fileline() + ' : TRACE ExportDHIS2 ERROR spreadsheet not found version')
                return compose_ret('', Constants.cst_content_type_json, 409)

            # 09/03/2023 period comes by ihm no longer by spreadsheet
            """
            idx_period = l_cols.index("period")

            if not idx_period:
                self.log.error(Logs.fileline() + ' : TRACE ExportDHIS2 ERROR spreadsheet not found period')
                return compose_ret('', Constants.cst_content_type_json, 409)

            # Determine the period
            period = l_rows[1][idx_period]
            """

            # Determine orgunit
            orgunit = ''

            idx_orgunit = l_cols.index("orgunit")

            if idx_orgunit:
                orgunit = l_rows[1][idx_orgunit]

            if not orgunit:
                lab = Various.getDefaultValue('entete_1')

                if lab:
                    orgunit = lab['value']

            # Determine storedby
            storedby = ''

            idx_storedby = l_cols.index("storedby")

            if idx_storedby:
                storedby = l_rows[1][idx_storedby]

            if not storedby:
                user = User.getUserDetails(args['id_user'])

                if user:
                    storedby = user['firstname'] + user['lastname']

            # remove space
            storedby = storedby.replace(' ', '')

            date_now = datetime.now()

            if l_rows:
                # remove headers line
                l_rows.pop(0)

                for period in l_period:
                    for row in l_rows:

                        if row:
                            data = []

                            if version == 'v3':
                                data.append(row[0])
                                data.append(period[0])
                                data.append(orgunit)
                                data.append(row[4])
                                data.append(row[5])
                            else:
                                data.append(row[0])
                                data.append(period[0])
                                data.append(orgunit)
                                data.append(row[5])
                                data.append(row[6])

                            period_beg_db = period[1]
                            period_end_db = period[2]

                            if version == 'v3':
                                filter_row = row[2].strip()
                            else:
                                filter_row = row[3].strip()

                            # --- check if formula or others statistic object  ---
                            # formula case
                            if filter_row.startswith("$") or filter_row.startswith("{"):
                                # Parse formula for result request
                                formula   = filter_row

                                if version == 'v3':
                                    type_samp = row[3]
                                else:
                                    type_samp = row[4]

                                self.log.error(Logs.fileline() + ' : TRACE ExportDHIS2 --- before ParseFormula ---')
                                self.log.error(Logs.fileline() + ' : TRACE ExportDHIS2 formula=%s', formula)
                                self.log.error(Logs.fileline() + ' : TRACE ExportDHIS2 type_samp=%s', type_samp)

                                req_part = ''

                                req_part = Report.ParseFormula(formula, type_samp)

                                result = Report.getResultEpidemio(inner_req=req_part['inner'],
                                                                  end_req=req_part['end'],
                                                                  date_beg=period_beg_db,
                                                                  date_end=period_end_db)

                                if result:
                                    data.append(str(result['value']))
                                else:
                                    data.append('')

                            # statistic case
                            else:
                                result = Export.getStatDHIS2(period_beg_db, period_end_db, filter_row)

                                if result:
                                    data.append(str(result['value']))
                                else:
                                    data.append('')

                            data.append(storedby)
                            data.append(date_now.strftime("%Y-%m-%dT%H:%M:%S"))
                            data.append('')
                            data.append('FALSE')
                            data.append('')

                            l_data.append(data)

        # --- WRITE FILE ---

        # if no result to export
        if len(l_data) < 2:
            return compose_ret('', Constants.cst_content_type_json, 404)

        # write csv file
        try:
            import csv

            filename = 'dhis2_' + filename + '_' + args['date_beg'] + '-' + args['date_end'] + '.csv'

            with open('tmp/' + filename, mode='w', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=',')
                for line in l_data:
                    writer.writerow(line)

        except Exception as err:
            self.log.error(Logs.fileline() + ' : post ExportDHIS2 failed, err=%s', err)
            return False

        self.log.info(Logs.fileline() + ' : TRACE ExportDHIS2')
        return compose_ret('', Constants.cst_content_type_json)


class ExportDHIS2Api(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        if 'date_beg' not in args or 'date_end' not in args or 'filename' not in args or 'id_user' not in args or \
           'period' not in args or 'dhs_ser' not in args:
            self.log.error(Logs.fileline() + ' : TRACE ExportDHIS2Api ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        period   = args['period']
        filename = args['filename'][:-4]

        l_period = []

        # build list of period
        if period == 'W':
            firstday = datetime.strptime(args['date_beg'], '%Y-%m-%d')
            lastday  = datetime.strptime(args['date_end'], '%Y-%m-%d')

            # firstday has to be a monday and lastday a sunday
            firstday = firstday + timedelta(days=-firstday.weekday())
            lastday  = lastday + timedelta(days=6 - lastday.weekday())

            next_monday = firstday + timedelta(days=7)  # firstday + timedelta(days=-firstday.weekday(), weeks=1)
            next_sunday = next_monday - timedelta(days=1)  # next_monday - timedelta(days=1)

            while next_monday < lastday:
                period_interv = []

                tmp_period = datetime.strftime(firstday, "%YW") + str(firstday.isocalendar().week)

                period_interv.append(tmp_period)
                period_interv.append(firstday)
                period_interv.append(next_sunday)

                l_period.append(period_interv)

                firstday = next_monday
                next_monday = firstday + timedelta(days=7)
                next_sunday = next_monday - timedelta(days=1)

            period_interv = []

            tmp_period = datetime.strftime(firstday, "%YW") + str(firstday.isocalendar().week)

            period_interv.append(tmp_period)
            period_interv.append(firstday)
            period_interv.append(lastday)

            l_period.append(period_interv)

        elif period == 'M':
            firstday = datetime.strptime(args['date_beg'], '%Y-%m-%d')
            firstday = firstday.replace(day=1)
            lastday  = datetime.strptime(args['date_end'], '%Y-%m-%d')

            firstday_of_nextmonth = firstday + timedelta(days=31)
            firstday_of_nextmonth = firstday_of_nextmonth.replace(day=1)
            lastday_of_month  = firstday_of_nextmonth - timedelta(days=1)

            while firstday_of_nextmonth < lastday:
                period_interv = []

                tmp_period = datetime.strftime(firstday, "%Y%m")

                period_interv.append(tmp_period)
                period_interv.append(firstday)
                period_interv.append(lastday_of_month)

                l_period.append(period_interv)

                firstday = firstday_of_nextmonth
                firstday_of_nextmonth = firstday + timedelta(days=31)
                firstday_of_nextmonth = firstday_of_nextmonth.replace(day=1)
                lastday_of_month  = firstday_of_nextmonth - timedelta(days=1)

            period_interv = []

            tmp_period = datetime.strftime(firstday, "%Y%m")

            firstday_of_nextmonth = firstday + timedelta(days=31)
            firstday_of_nextmonth = firstday_of_nextmonth.replace(day=1)
            lastday_of_month  = firstday_of_nextmonth - timedelta(days=1)

            period_interv.append(tmp_period)
            period_interv.append(firstday)
            period_interv.append(lastday_of_month)

            l_period.append(period_interv)
        else:
            self.log.error(Logs.fileline() + ' : TRACE ExportDHIS2Api ERROR wrong period : ' + str(period))
            return compose_ret('', Constants.cst_content_type_json, 409)

        # --- BUILD DATA ---

        # Pre-defined export
        if filename == "LIST_OUTSOURCING":
            self.log.error(Logs.fileline() + ' : TRACE ExportDHIS2Api LIST_OUTSOURCING')

            # Data headers
            l_data = [["period", "code patient", "record number", "record date", "analysis outsourced"]]

            for period in l_period:
                l_rows = Export.getListOutsourcing(period[1], period[2])

                for row in l_rows:
                    if row:

                        data = []

                        code = str(row['code'])

                        if row['code_patient']:
                            code += ' / ' + str(row['code_patient'])

                        num_rec = str(row['num_dos_an'])

                        date_rec = str(row['date_rec'])

                        ana_outsourced = str(row['ana_code']) + ' ' + str(row['ana_name'])

                        data.append(period[0])
                        data.append(code)
                        data.append(num_rec)
                        data.append(date_rec)
                        data.append(ana_outsourced)

                        l_data.append(data)
        else:
            # Data headers
            l_data = [["dataelement", "period", "orgunit", "categoryoptioncombo", "attributeoptioncombo", "value",
                       "storedby", "lastupdated", "comment", "followup", "deleted"]]

            # Read CSV spreadsheet
            import os

            from csv import reader

            path = Constants.cst_dhis2

            with open(os.path.join(path, args['filename']), 'r', encoding='utf-8') as csv_file:
                csv_reader = reader(csv_file, delimiter=';')
                l_rows = list(csv_reader)

            if not l_rows or len(l_rows) < 2:
                self.log.error(Logs.fileline() + ' : TRACE ExportDHIS2Api ERROR spreadsheet empty')
                return compose_ret('', Constants.cst_content_type_json, 500)

            l_cols = l_rows[0]  # keep first row to read l_cols of csv

            idx_version = l_cols.index("version")

            if idx_version:
                version = l_rows[1][idx_version]

                if version != 'v1' and version != 'v2' and version != 'v3':
                    self.log.error(Logs.fileline() + ' : TRACE ExportDHIS2Api ERROR spreadsheet wrong version :' + str(version))
                    return compose_ret('', Constants.cst_content_type_json, 409)
            else:
                self.log.error(Logs.fileline() + ' : TRACE ExportDHIS2Api ERROR spreadsheet not found version')
                return compose_ret('', Constants.cst_content_type_json, 409)

            # Determine orgunit
            orgunit = ''

            idx_orgunit = l_cols.index("orgunit")

            if idx_orgunit:
                orgunit = l_rows[1][idx_orgunit]

            if not orgunit:
                lab = Various.getDefaultValue('entete_1')

                if lab:
                    orgunit = lab['value']

            # Determine storedby
            storedby = ''

            idx_storedby = l_cols.index("storedby")

            if idx_storedby:
                storedby = l_rows[1][idx_storedby]

            if not storedby:
                user = User.getUserDetails(args['id_user'])

                if user:
                    storedby = user['firstname'] + user['lastname']

            # remove space
            storedby = storedby.replace(' ', '')

            date_now = datetime.now()

            if l_rows:
                # remove headers line
                l_rows.pop(0)

                for period in l_period:
                    for row in l_rows:

                        if row:
                            data = []

                            if version == 'v3':
                                data.append(row[0])
                                data.append(period[0])
                                data.append(orgunit)
                                data.append(row[4])
                                data.append(row[5])
                            else:
                                data.append(row[0])
                                data.append(period[0])
                                data.append(orgunit)
                                data.append(row[5])
                                data.append(row[6])

                            period_beg_db = period[1]
                            period_end_db = period[2]

                            if version == 'v3':
                                filter_row = row[2].strip()
                            else:
                                filter_row = row[3].strip()

                            # --- check if formula or others statistic object  ---
                            # formula case
                            if filter_row.startswith("$") or filter_row.startswith("{"):
                                # Parse formula for result request
                                formula   = filter_row

                                if version == 'v3':
                                    type_samp = row[3]
                                else:
                                    type_samp = row[4]

                                self.log.error(Logs.fileline() + ' : TRACE ExportDHIS2Api --- before ParseFormula ---')
                                self.log.error(Logs.fileline() + ' : TRACE ExportDHIS2Api formula=%s', formula)
                                self.log.error(Logs.fileline() + ' : TRACE ExportDHIS2Api type_samp=%s', type_samp)

                                req_part = ''

                                req_part = Report.ParseFormula(formula, type_samp)

                                result = Report.getResultEpidemio(inner_req=req_part['inner'],
                                                                  end_req=req_part['end'],
                                                                  date_beg=period_beg_db,
                                                                  date_end=period_end_db)

                                if result:
                                    data.append(str(result['value']))
                                else:
                                    data.append('')

                            # statistic case
                            else:
                                result = Export.getStatDHIS2(period_beg_db, period_end_db, filter_row)

                                if result:
                                    data.append(str(result['value']))
                                else:
                                    data.append('')

                            data.append(storedby)
                            data.append(date_now.strftime("%Y-%m-%dT%H:%M:%S"))
                            data.append('')
                            data.append('FALSE')
                            data.append('')

                            l_data.append(data)

        # Send data to api DHIS2 (3 steps)
        # 1 - Get api settings
        api = Setting.getDHIS2Det(args['dhs_ser'])

        if not api:
            self.log.error(Logs.fileline() + ' : TRACE ExportDHIS2Api ERROR api setting not found version')
            return compose_ret('', Constants.cst_content_type_json, 405)

        # 2 - send data
        url   = api['dhs_url'] + str("/dataValueSets")
        login = api['dhs_login']
        pwd   = api['dhs_pwd']

        # convert l_data to CSV string
        from io import StringIO

        import csv

        csv_data = StringIO()
        csv_writer = csv.writer(csv_data)
        csv_writer.writerows(l_data)

        headers = {"Content-Type": "application/csv"}

        auth = (login, pwd)

        try:
            import requests

            resp = requests.post(url, data=csv_data.getvalue(), headers=headers, auth=auth)

            # 3 - analyze the return
            if resp.status_code == 200:
                self.log.info(Logs.fileline() + ' : post ExportDHIS2Api requests OK resp = ' + str(resp.text))
            else:
                self.log.error(Logs.fileline() + ' : post ExportDHIS2Api requests KO code:' + str(resp.status_code) + 'resp = ' + str(resp.text))
                return compose_ret(resp.text, Constants.cst_content_type_json, resp.status_code)
        except Exception as err:
            self.log.error(Logs.fileline() + ' : post ExportDHIS2Api requests post failed, err=%s', err)
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE ExportDHIS2Api')
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
                   "Date d'admission", "Service demandeur", "Numéro de lit", "Identification hôpital", "Type patient",
                   "Isolate number", "Numéro de prélèvement", "Date de prélèvement", "Type de prélèvement",
                   "Commentaire de prélèvement", "Micro-organisme", "Nom de l'antibiotique", "Methode de détermination",
                   "Method value", "Resultat d'antibiotique"]]
        dict_data = Export.getDataWhonet(args['date_beg'], args['date_end'])

        Various.useLangDB()

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

                if d['rec_hosp_num']:
                    data.append(d['rec_hosp_num'])
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
