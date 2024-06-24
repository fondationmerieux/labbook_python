import logging
import configparser
import gettext
import os
import csv
import json

from datetime import datetime, timedelta
from flask import request
from flask_restful import Resource

from app.models.General import *
from app.models.Logs import Logs
from app.models.Report import Report
from app.models.Result import Result
from app.models.Various import Various


class ReportEpidemio(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        if 'date_beg' not in args or 'date_end' not in args:
            self.log.error(Logs.fileline() + ' : ReportEpidemio ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        data = []

        # Read epidemio.ini
        config = configparser.ConfigParser()
        config.read(os.path.join(Constants.cst_epidemio, "epidemio.ini"), encoding='utf-8')

        nb_disease = int(config.get('SETTINGS', 'nb_disease'))

        if not config or nb_disease < 1:
            self.log.error(Logs.fileline() + ' : TRACE epidemio settings not found')

        # Loop on disease
        for d in range(nb_disease):
            x = str(d + 1)

            disease = {}

            disease['disease'] = config.get('DISEASE_' + x, 'disease')

            # Get label for sample_type
            dict_sample = Various.getDicoById(config.get('DISEASE_' + x, 'sample_type'))

            if dict_sample:
                disease['sample'] = dict_sample['label']
            else:
                disease['sample'] = 'UNKNOWN'

            # self.log.error(Logs.fileline() + ' : DEBUG-TRACE ##########################')
            # self.log.error(Logs.fileline() + ' : DEBUG-TRACE disease=' + disease['disease'])
            # self.log.error(Logs.fileline() + ' : DEBUG-TRACE sample=' + disease['sample'])

            nb_res = int(config.get('DISEASE_' + x, 'nb_res'))

            disease['details'] = []

            id_prod = 0
            l_id_var = []
            # Loop on result to calculate
            for r in range(nb_res):
                y = str(r + 1)
                details = {}

                details['res_label'] = config.get('DISEASE_' + x, 'res_label_' + y)

                # self.log.error(Logs.fileline() + ' : DEBUG-TRACE res_label=' + details['res_label'])

                formula = config.get('DISEASE_' + x, 'formula_' + y)

                # self.log.error(Logs.fileline() + ' : DEBUG-TRACE formula=' + formula)

                if not formula:
                    details['res_type'] = 'T'  # Title
                elif formula == 'N/A':
                    formula = ''
                    details['res_type']  = 'R'
                    details['res_value'] = 'N/A'
                else:
                    details['res_type'] = 'R'  # Result

                    id_prod = config.get('DISEASE_' + x, 'sample_type_' + y)

                    # Parse formula for result request
                    req_part = ''

                    req_part = Report.ParseFormula(formula, id_prod)

                    # self.log.error(Logs.fileline() + ' : DEBUG-TRACE req_part=' + str(req_part))
                    result = Report.getResultEpidemio(inner_req=req_part['inner'],
                                                      end_req=req_part['end'],
                                                      date_beg=args['date_beg'],
                                                      date_end=args['date_end'])

                    if result:
                        details['res_value'] = result['value']

                    # Parse id_var for NbResult request
                    id_var = 0

                    idx_beg = formula.find("$_")

                    if idx_beg >= 0:
                        idx_end = formula.find(" ", idx_beg)
                        idx_beg = idx_beg + 2
                        if idx_end > idx_beg:
                            id_var = int(formula[idx_beg:idx_end])

                    if id_var > 0:
                        l_id_var.append(id_var)

                disease['details'].append(details)

            l_id_var  = list(set(l_id_var))
            disease['total_received'] = 0

            received = Report.getNbResultRecevied(l_id_var, id_prod, args['date_beg'], args['date_end'])
            analyzed = Report.getNbResultAnalyzed(l_id_var, id_prod, args['date_beg'], args['date_end'])

            if received:
                disease['total_received'] = received['total']

            if analyzed:
                disease['total_analyzed'] = analyzed['total']

            data.append(disease)

        self.log.info(Logs.fileline() + ' : TRACE ReportEpidemio')
        return compose_ret(data, Constants.cst_content_type_json)


class ReportIndicator(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        if 'date_beg' not in args or 'date_end' not in args:
            self.log.error(Logs.fileline() + ' : ReportIndicator ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        data = []

        # Read indicator.ini
        config = configparser.ConfigParser()
        config.read(os.path.join(Constants.cst_indicator, "indicator.ini"), encoding='utf-8')

        nb_disease = int(config.get('SETTINGS', 'nb_disease'))

        if not config or nb_disease < 1:
            self.log.error(Logs.fileline() + ' : TRACE indicator settings not found')

        # Loop on disease
        for d in range(nb_disease):
            x = str(d + 1)

            disease = {}

            disease['disease'] = config.get('DISEASE_' + x, 'disease')
            disease['sample']  = ''

            l_dict_sample = json.loads(config.get('DISEASE_' + x, 'sample_type'))

            for dict_sample in l_dict_sample:
                # Get label for sample_type
                dict_sample = Various.getDicoById(dict_sample)

                if dict_sample:
                    disease['sample'] += dict_sample['label'] + ', '
                else:
                    disease['sample'] += 'UNKNOWN  '

            if disease['sample']:
                disease['sample'] = disease['sample'][:-2]

            # self.log.error(Logs.fileline() + ' : DEBUG-TRACE ##########################')
            # self.log.error(Logs.fileline() + ' : DEBUG-TRACE disease=' + disease['disease'])
            # self.log.error(Logs.fileline() + ' : DEBUG-TRACE sample=' + disease['sample'])

            nb_res = int(config.get('DISEASE_' + x, 'nb_res'))

            disease['details'] = []

            l_id_prod = [0]
            l_id_var = []
            # Loop on result to calculate
            for r in range(nb_res):
                y = str(r + 1)
                details = {}

                details['res_label'] = config.get('DISEASE_' + x, 'res_label_' + y)

                # self.log.info(Logs.fileline() + ' : DEBUG-TRACE res_label=' + details['res_label'])

                formula = config.get('DISEASE_' + x, 'formula_' + y)

                # self.log.info(Logs.fileline() + ' : DEBUG-TRACE formula=' + formula)

                if not formula:
                    details['res_type'] = 'T'  # Title
                elif formula == 'N/A':
                    formula = ''
                    details['res_type']  = 'R'
                    details['res_value'] = 'N/A'
                else:
                    details['res_type'] = 'R'  # Result

                    l_id_prod = json.loads(config.get('DISEASE_' + x, 'sample_type_' + y))

                    # BUILD PART of request
                    req_part = ''

                    req_part = Report.ParseFormulaV2(formula, l_id_prod)

                    # GET RESULT
                    result = Report.getResultIndicator(inner_req=req_part['inner'],
                                                       end_req=req_part['end'],
                                                       date_beg=args['date_beg'],
                                                       date_end=args['date_end'])

                    if result:
                        self.log.info(Logs.fileline() + ' : DEBUG-TRACE result = ' + str(result))
                        details['res_value'] = result['value']

                    # Parse id_var for NbResult request
                    id_var = 0

                    idx_beg = formula.find("$_")

                    if idx_beg >= 0:
                        idx_end = formula.find(" ", idx_beg)
                        idx_beg = idx_beg + 2
                        if idx_end > idx_beg:
                            id_var = int(formula[idx_beg:idx_end])

                    if id_var > 0:
                        l_id_var.append(id_var)

                disease['details'].append(details)

            l_id_var  = list(set(l_id_var))
            disease['total_received'] = 0

            received = Report.getNbResultReceviedV2(l_id_var, l_id_prod, args['date_beg'], args['date_end'])
            analyzed = Report.getNbResultAnalyzedV2(l_id_var, l_id_prod, args['date_beg'], args['date_end'])

            if received:
                disease['total_received'] = received['total']

            if analyzed:
                disease['total_analyzed'] = analyzed['total']

            data.append(disease)

        self.log.info(Logs.fileline() + ' : TRACE ReportIndicator')
        return compose_ret(data, Constants.cst_content_type_json)


class ReportActivity(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        if 'date_beg' not in args or 'date_end' not in args or 'type_ana' not in args:
            self.log.error(Logs.fileline() + ' : ReportActivity ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        stat = {}

        stat['type'] = Report.getActivityType(args['date_beg'], args['date_end'], args['type_ana'])

        if not stat['type']:
            self.log.error(Logs.fileline() + ' : TRACE stat type not found')
            stat['type'] = []

        Various.useLangDB()
        for stat_type in stat['type']:
            stat_ana = stat_type['analysis']
            if stat_ana:
                stat_type['analysis'] = _(stat_ana.strip())
            else:
                stat_type['analysis'] = ''

        stat['age'] = Report.getActivityAge(args['date_beg'], args['date_end'], args['type_ana'])

        if not stat['age']:
            self.log.error(Logs.fileline() + ' : TRACE stat age not found')
            stat['age'] = []

        Various.useLangDB()
        for stat_age in stat['age']:
            stat_ana = stat_age['analysis']
            if stat_ana:
                stat_age['analysis'] = _(stat_ana.strip())
            else:
                stat_age['analysis'] = ''

            # converted age in years
            if stat_age['unite'] == 1034:
                stat_age['age'] = int(stat_age['age'] // 365)
            elif stat_age['unite'] == 1035:
                stat_age['age'] = int(stat_age['age'] // 52)
            elif stat_age['unite'] == 1036:
                stat_age['age'] = int(stat_age['age'] // 12)

        self.log.info(Logs.fileline() + ' : TRACE ReportActivity')
        return compose_ret(stat, Constants.cst_content_type_json)


class ReportStat(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        if 'date_beg' not in args or 'date_end' not in args or 'service_int' not in args:
            self.log.error(Logs.fileline() + ' : ReportStat ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        stat = {}

        stat['patient'] = Report.getStatPatient(args['date_beg'], args['date_end'], args['service_int'])

        if not stat['patient']:
            self.log.error(Logs.fileline() + ' : TRACE stat patient not found')

        stat['prescr'] = Report.getStatPrescr(args['date_beg'], args['date_end'], args['service_int'])

        if not stat['prescr']:
            self.log.error(Logs.fileline() + ' : TRACE stat prescr not found')

        stat['sampler'] = Report.getStatSampler(args['date_beg'], args['date_end'])

        if not stat['sampler']:
            self.log.error(Logs.fileline() + ' : TRACE stat sampler not found')

        stat['product'] = Report.getStatProduct(args['date_beg'], args['date_end'])

        if not stat['product']:
            self.log.error(Logs.fileline() + ' : TRACE stat product not found')

        stat['nb_pat'] = Report.getStatNbPat(args['date_beg'], args['date_end'], args['service_int'])

        if not stat['nb_pat']:
            self.log.error(Logs.fileline() + ' : TRACE stat nb_pat not found')

        stat['nb_ana'] = Report.getStatNbAna(args['date_beg'], args['date_end'], args['service_int'])

        if not stat['nb_ana']:
            self.log.error(Logs.fileline() + ' : TRACE stat nb_ana not found')

        self.log.info(Logs.fileline() + ' : TRACE ReportStat')
        return compose_ret(stat, Constants.cst_content_type_json)


class ReportTAT(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        if 'date_beg' not in args or 'date_end' not in args or 'type_ana' not in args or 'id_ana' not in args or \
           'code_pat' not in args or 'rec_num' not in args:
            self.log.error(Logs.fileline() + ' : ReportTAT ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        l_TAT = Report.getTAT(date_beg=args['date_beg'],
                              date_end=args['date_end'],
                              type_ana=args['type_ana'],
                              id_ana=args['id_ana'],
                              code_pat=args['code_pat'],
                              rec_num=args['rec_num'])

        if not l_TAT:
            self.log.error(Logs.fileline() + ' : TRACE TAT not found')

        nb_tat = 0
        nb_tat_tech = 0
        nb_tat_ana = 0

        total_tat = timedelta()
        total_tat_tech = timedelta()
        total_tat_ana = timedelta()

        for data in l_TAT:
            for key, value in list(data.items()):
                if data[key] is None:
                    data[key] = ''

            date_save     = ''
            date_vld      = ''
            date_vld_tech = ''
            date_vld_ana  = ''

            res_tech = Result.getValidationByReq(data['id_req'], 251)
            res_bio  = Result.getValidationByReq(data['id_req'], 252)

            if res_tech and res_tech['date_vld']:
                date_vld_tech = res_tech['date_vld']

            if res_bio and res_bio['date_vld']:
                date_vld_ana = res_bio['date_vld']

            if data['rec_date']:
                data['rec_date'] = datetime.strftime(data['rec_date'], Constants.cst_dt_HM)
            else:
                data['rec_date'] = ''

            if data['rec_date_save']:
                data['rec_date_save'] = datetime.strftime(data['rec_date_save'], Constants.cst_dt_HMS)
                date_save = datetime.strptime(data['rec_date_save'], Constants.cst_dt_HMS)
                data['rec_date_save'] = data['rec_date_save'][:-3]
            else:
                data['rec_date_save'] = ''

            if data['rec_date_vld']:
                data['rec_date_vld'] = datetime.strftime(data['rec_date_vld'], Constants.cst_dt_HMS)
                date_vld = datetime.strptime(data['rec_date_vld'], Constants.cst_dt_HMS)
                data['rec_date_vld'] = data['rec_date_vld'][:-3]
            else:
                data['rec_date_vld'] = ''

            # TAT Record calculation
            if date_save and date_vld:
                diff_date = date_vld - date_save
                data['tat_days']  = diff_date.days
                data['tat_hours'], remain = divmod(diff_date.seconds, 3600)
                data['tat_mins'], data['tat_secs'] = divmod(remain, 60)

                nb_tat += 1

                total_tat = ((total_tat * (nb_tat - 1)) + diff_date) / nb_tat

            if total_tat:
                data['tot_days']  = total_tat.days
                data['tot_hours'], remain = divmod(total_tat.seconds, 3600)
                data['tot_mins'], data['tat_secs'] = divmod(remain, 60)

            # TAT technical validation calculation
            if date_save and date_vld_tech:
                diff_date = date_save - date_vld_tech
                data['tat_tech_days']  = diff_date.days
                data['tat_tech_hours'], remain = divmod(diff_date.seconds, 3600)
                data['tat_tech_mins'], data['tat_tech_secs'] = divmod(remain, 60)

                nb_tat_tech += 1

                total_tat_tech = ((total_tat_tech * (nb_tat_tech - 1)) + diff_date) / nb_tat_tech

            if total_tat_tech:
                data['tot_tech_days']  = total_tat_tech.days
                data['tot_tech_hours'], remain = divmod(total_tat_tech.seconds, 3600)
                data['tot_tech_mins'], data['tot_tech_secs'] = divmod(remain, 60)
            else:
                data['tot_tech_days']  = 0
                data['tot_tech_hours'] = 0
                data['tot_tech_mins']  = 0
                data['tot_tech_secs']  = 0

            # TAT Analysis calculation
            if date_save and date_vld_ana:
                diff_date = date_save - date_vld_ana
                data['tat_ana_days']  = diff_date.days
                data['tat_ana_hours'], remain = divmod(diff_date.seconds, 3600)
                data['tat_ana_mins'], data['tat_ana_secs'] = divmod(remain, 60)

                nb_tat_ana += 1

                total_tat_ana = ((total_tat_ana * (nb_tat_ana - 1)) + diff_date) / nb_tat_ana

            if total_tat_ana:
                data['tot_ana_days']  = total_tat_ana.days
                data['tot_ana_hours'], remain = divmod(total_tat_ana.seconds, 3600)
                data['tot_ana_mins'], data['tot_ana_secs'] = divmod(remain, 60)
            else:
                data['tot_ana_days']  = 0
                data['tot_ana_hours'] = 0
                data['tot_ana_mins']  = 0
                data['tot_ana_secs']  = 0

        self.log.info(Logs.fileline() + ' : TRACE ReportTAT')
        return compose_ret(l_TAT, Constants.cst_content_type_json)


class ReportBilling(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        if 'date_beg' not in args or 'date_end' not in args or 'id_user' not in args:
            self.log.error(Logs.fileline() + ' : ReportBilling ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        l_datas = Report.getBillingStatus(args['date_beg'], args['date_end'], args['id_user'])

        if not l_datas:
            self.log.error(Logs.fileline() + ' : TRACE list current billing not found')

        for data in l_datas:
            for key, value in list(data.items()):
                if data[key] is None:
                    data[key] = ''

            if data['bill_price']:
                data['bill_price'] = float(data['bill_price'])
            else:
                data['bill_price'] = 0

            if data['bill_remain']:
                data['bill_remain'] = float(data['bill_remain'])
            else:
                data['bill_remain'] = 0

        self.log.info(Logs.fileline() + ' : TRACE ReportBilling')
        return compose_ret(l_datas, Constants.cst_content_type_json)


class ReportToday(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        if 'date_beg' not in args or 'date_end' not in args:
            self.log.error(Logs.fileline() + ' : ReportToday ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        l_datas = Report.getTodayList(args['date_beg'], args['date_end'])

        if not l_datas:
            self.log.error(Logs.fileline() + ' : TRACE list today record not found')

        Various.useLangDB()

        for data in l_datas:
            for key, value in list(data.items()):
                if data[key] is None:
                    data[key] = ''
                elif key == 'analysis' and data[key]:
                    data[key] = _(data[key].strip())
                elif key == 'family' and data[key]:
                    data[key] = _(data[key].strip())

            if data['rec_date']:
                data['rec_date'] = datetime.strftime(data['rec_date'], Constants.cst_isodate)
            else:
                data['rec_date'] = ''

            if data['type_rec'] and data['type_rec'] == 183:
                data['type_rec'] = 'E'
            else:
                data['type_rec'] = 'I'

        self.log.info(Logs.fileline() + ' : TRACE ReportToday')
        return compose_ret(l_datas, Constants.cst_content_type_json)


class ReportTodayExport(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        l_data = [['id_rec', 'rec_date', 'rec_num', 'family', 'analysis', 'vld_type']]

        if 'date_beg' not in args or 'date_end' not in args:
            self.log.error(Logs.fileline() + ' : ReportTodayExport ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        dict_data = Report.getTodayList(args['date_beg'], args['date_end'])

        Various.useLangDB()

        if dict_data:
            for d in dict_data:
                data = []

                data.append(d['id_rec'])
                data.append(d['rec_date'])
                data.append(d['rec_num'])
                fam = d['family']
                data.append(_(fam.strip()))
                ana = d['analysis']
                data.append(_(ana.strip()))
                data.append(d['vld_type'])

                l_data.append(data)

        # if no result to export
        if len(l_data) < 2:
            return compose_ret('', Constants.cst_content_type_json, 404)

        # write csv file
        try:
            today = datetime.now().strftime(Constants.cst_date_ymd)

            filename = 'report_today_' + str(today) + '.csv'

            with open('tmp/' + filename, mode='w', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=';')
                for line in l_data:
                    writer.writerow(line)

        except Exception as err:
            self.log.error(Logs.fileline() + ' : post ReportTodayExport failed, err=%s', err)
            return False

        self.log.info(Logs.fileline() + ' : TRACE ReportTodayExport')
        return compose_ret('', Constants.cst_content_type_json)
