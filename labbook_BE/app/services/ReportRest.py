import logging
import configparser
import gettext

from datetime import datetime
from flask import request
from flask_restful import Resource

from app.models.General import *
from app.models.Logs import Logs
from app.models.Report import Report
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
        import os

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

            # self.log.error(Logs.fileline() + ' : DEBUG ##########################')
            # self.log.error(Logs.fileline() + ' : DEBUG disease=' + disease['disease'])
            # self.log.error(Logs.fileline() + ' : DEBUG sample=' + disease['sample'])

            nb_res = int(config.get('DISEASE_' + x, 'nb_res'))

            disease['details'] = []

            id_prod = 0
            l_id_var = []
            # Loop on result to calculate
            for r in range(nb_res):
                y = str(r + 1)
                details = {}

                details['res_label'] = config.get('DISEASE_' + x, 'res_label_' + y)

                # self.log.error(Logs.fileline() + ' : DEBUG res_label=' + details['res_label'])

                formula = config.get('DISEASE_' + x, 'formula_' + y)

                # self.log.error(Logs.fileline() + ' : DEBUG formula=' + formula)

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

                    # self.log.error(Logs.fileline() + ' : DEBUG req_part=' + str(req_part))
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

        if Various.needTranslationDB():
            for stat_type in stat['type']:
                stat_ana = stat_type['analysis']
                stat_type['analysis']  = _(stat_ana.strip())

        stat['age'] = Report.getActivityAge(args['date_beg'], args['date_end'], args['type_ana'])

        if not stat['age']:
            self.log.error(Logs.fileline() + ' : TRACE stat age not found')
            stat['age'] = []

        if Various.needTranslationDB():
            for stat_age in stat['age']:
                stat_ana = stat_age['analysis']
                stat_age['analysis']  = _(stat_ana.strip())

        self.log.info(Logs.fileline() + ' : TRACE ReportActivity')
        return compose_ret(stat, Constants.cst_content_type_json)


class ReportStat(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        if 'date_beg' not in args or 'date_end' not in args:
            self.log.error(Logs.fileline() + ' : ReportStat ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        stat = {}

        stat['patient'] = Report.getStatPatient(args['date_beg'], args['date_end'])

        if not stat['patient']:
            self.log.error(Logs.fileline() + ' : TRACE stat patient not found')

        stat['prescr'] = Report.getStatPrescr(args['date_beg'], args['date_end'])

        if not stat['prescr']:
            self.log.error(Logs.fileline() + ' : TRACE stat prescr not found')

        stat['sampler'] = Report.getStatSampler(args['date_beg'], args['date_end'])

        if not stat['sampler']:
            self.log.error(Logs.fileline() + ' : TRACE stat sampler not found')

        stat['product'] = Report.getStatProduct(args['date_beg'], args['date_end'])

        if not stat['product']:
            self.log.error(Logs.fileline() + ' : TRACE stat product not found')

        self.log.info(Logs.fileline() + ' : TRACE ReportStat')
        return compose_ret(stat, Constants.cst_content_type_json)


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

            if data['bill_price'] != '':
                data['bill_price'] = float(data['bill_price'])

            if data['bill_remain'] != '':
                data['bill_remain'] = float(data['bill_remain'])

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

        Various.needTranslationDB()

        for data in l_datas:
            for key, value in list(data.items()):
                if data[key] is None:
                    data[key] = ''
                elif key == 'analysis':
                    data[key] = _(data[key].strip())
                elif key == 'family':
                    data[key] = _(data[key].strip())

            if data['rec_date'] != '':
                data['rec_date'] = datetime.strftime(data['rec_date'], '%Y-%m-%d')

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

        Various.needTranslationDB()

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
            import csv

            today = datetime.now().strftime("%Y%m%d")

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
