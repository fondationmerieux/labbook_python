import logging

from datetime import datetime
from flask import request
from flask_restful import Resource

from app.models.General import *
from app.models.Logs import Logs
from app.models.Report import Report


class ReportEpidemio(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        if 'date_beg' not in args or 'date_end' not in args:
            self.log.error(Logs.fileline() + ' : ReportEpidemio ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        data = {}

        data = Report.getListEpidemio()

        if not data:
            self.log.error(Logs.fileline() + ' : TRACE list epidemio not found')

        for disease in data:
            disease['details'] = Report.getStatEpidemio(disease['id_data'])

            if not disease['details']:
                self.log.error(Logs.fileline() + ' : TRACE stat epidemio not found')

            id_prod = 0  # NOTE : id_prod from sigl_15_data (precision) different from sigl_14_data (wide category)
            l_id_var = []
            for det in disease['details']:
                # looking for pattern "$_xxx " to get xxx
                formula = det['formula']

                if formula and formula != 'N/A':
                    id_prod = det['id_prod']

                    # Parse formula for result request
                    req_part = ''

                    req_part = Report.ParseFormula(formula, id_prod)

                    # self.log.error(Logs.fileline() + ' : DEBUG req_part=' + str(req_part))
                    result = Report.getResultEpidemio(inner_req=req_part['inner'],
                                                      end_req=req_part['end'],
                                                      date_beg=args['date_beg'],
                                                      date_end=args['date_end'])

                    if result:
                        det['res_value'] = result['value']

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
                else:
                    det['res_value'] = 'N/A'

            l_id_var  = list(set(l_id_var))
            disease['total_received'] = 0

            received = Report.getNbResultRecevied(l_id_var, id_prod, args['date_beg'], args['date_end'])
            analyzed = Report.getNbResultAnalyzed(l_id_var, id_prod, args['date_beg'], args['date_end'])

            if received:
                disease['total_received'] = received['total']

            if analyzed:
                disease['total_analyzed'] = analyzed['total']

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

        stat['age'] = Report.getActivityAge(args['date_beg'], args['date_end'], args['type_ana'])

        if not stat['age']:
            self.log.error(Logs.fileline() + ' : TRACE stat age not found')
            stat['age'] = []

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
            for key, value in data.items():
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

        for data in l_datas:
            for key, value in data.items():
                if data[key] is None:
                    data[key] = ''

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

        if dict_data:
            for d in dict_data:
                data = []

                data.append(d['id_rec'])
                data.append(d['rec_date'])
                data.append(d['rec_num'])
                data.append(d['family'])
                data.append(d['analysis'])
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
