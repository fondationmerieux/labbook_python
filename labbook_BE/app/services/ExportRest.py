# -*- coding:utf-8 -*-
import logging

from datetime import datetime
from flask import request
from flask_restful import Resource

from app.models.General import compose_ret
from app.models.Constants import *
# from app.models.Various import *
from app.models.Export import *
from app.models.Logs import Logs
# from app.models.User import *


class ExportWhonet(Resource):
    log = logging.getLogger('log_services')

    def get(self):

        json = Export.getDataWhonet("2020-10-01", "2020-10-30")

        for res in json:
            if res['date_hosp']:
                res['date_hosp'] = datetime.strftime(res['date_hosp'], '%Y-%m-%d')
            if res['ddn']:
                res['ddn'] = datetime.strftime(res['ddn'], '%Y-%m-%d')

        self.log.info(Logs.fileline() + ' : TRACE TEST ExportWhonet')
        return compose_ret(json, Constants.cst_content_type_json)

    def post(self):
        args = request.get_json()

        if 'date_beg' not in args or 'date_end' not in args:
            self.log.error(Logs.fileline() + ' : TRACE ExportWhonet ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        dt_start_req = datetime.now()

        # Data
        l_data = [['Patient number', 'Firstname', 'Lastname', 'Sex', 'Date of birth (or age)',
                   'Date of admission', 'Patient location', 'Type of location', 'Exam number',
                   'Specimen date', 'Specimen type', 'Organism', 'Antibiotic', 'Method', 'Method value', 'Result']]
        dict_data = Export.getDataWhonet(args['date_beg'], args['date_end'])

        if dict_data:
            for d in dict_data:
                data = []

                data.append(d['pat_code'])
                data.append(d['pat_fname'])
                data.append(d['pat_name'])
                data.append(d['sex'])

                if d['ddn']:
                    d['ddn'] = datetime.strftime(d['ddn'], '%Y-%m-%d')
                    data.append(d['ddn'])
                else:
                    data.append(d['age'])

                if d['date_hosp']:
                    d['date_hosp'] = datetime.strftime(d['date_hosp'], '%Y-%m-%d')
                    data.append(d['date_hosp'])
                else:
                    data.append('')

                data.append(d['service_interne'])
                data.append(d['rec_type'])
                data.append(d['ana_code'])

                # specimen part
                if d['spec_date']:
                    d['spec_date'] = datetime.strftime(d['spec_date'], '%Y-%m-%d')

                data.append(d['spec_date'])
                data.append(d['spec_type'])

                # analysis part
                if d['ana_name']:
                    ana_name = d['ana_name']
                    ana_name = ana_name[14:]  # delete "Antibiogramme"

                    start_meth = ana_name.find('[')  # search where method starts
                    end_meth   = ana_name.find(']')  # search where method ends

                    method_name = ana_name[start_meth + 1:end_meth]

                    ana_name = ana_name[0:start_meth - 1]

                    data.append(ana_name)
                    data.append(d['libelle'])
                    data.append(method_name)
                    data.append(d['method_value'])
                    data.append(d['valeur'])

                l_data.append(data)  # list(d.values()))

        # self.log.error(Logs.fileline() + ' : WHONET l_data=' + str(l_data))

        # if no result to export
        if len(l_data) < 2:
            return compose_ret('', Constants.cst_content_type_json, 404)

        # write csv file
        try:
            import csv

            filename = 'whonet_' + args['date_beg'] + '_' + args['date_end'] + '.txt'

            with open('tmp/' + filename, mode='w') as file:
                writer = csv.writer(file, delimiter='\t')
                for line in l_data:
                    writer.writerow(line)

        except Exception as err:
            self.log.error(Logs.fileline() + ' : post ExportWhonet failed, err=%s , num=%s', err, str(num))
            return False

        dt_stop_req = datetime.now()
        dt_time_req = dt_stop_req - dt_start_req

        self.log.info(Logs.fileline() + ' : DEBUG ExportWhonet processing time = ' + str(dt_time_req))

        self.log.info(Logs.fileline() + ' : TRACE ExportWhonet')
        return compose_ret('', Constants.cst_content_type_json)
