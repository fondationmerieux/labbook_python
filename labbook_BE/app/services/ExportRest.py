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

    def post(self):
        self.log.error(Logs.fileline() + ' : TRACE ExportWhonet START DEBUG')

        args = request.get_json()

        if 'date_beg' not in args or 'date_end' not in args:
            self.log.error(Logs.fileline() + ' : TRACE ExportWhonet ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # Data
        l_data = [['Laboratory', 'Lab address', 'Lab city', 'Speciality', 'Identification number', 'First name', 'Last name', 'Sex', 'Date of birth', 'Age',
                   'Date of admission', 'Service', 'Type of location', 'Exam number',
                   'Specimen date', 'Specimen type', 'Specimen comment', 'Organism', 'Antibiotic', 'Method', 'Method value', 'Result']]
        dict_data = Export.getDataWhonet(args['date_beg'], args['date_end'])

        if dict_data:
            for d in dict_data:
                data = []

                data.append(d['lab_name'])
                data.append(d['lab_addr'])
                data.append(d['lab_city'])

                if d['med_spe']:
                    data.append(d['med_spe'])
                else:
                    data.append('')

                data.append(d['pat_code'])
                data.append(d['pat_fname'])
                data.append(d['pat_name'])
                data.append(d['sex'])

                if d['ddn']:
                    d['ddn'] = datetime.strftime(d['ddn'], '%Y-%m-%d')
                    data.append(d['ddn'])
                else:
                    data.append('')

                if d['age']:
                    data.append(d['age'])
                else:
                    data.append('')

                if d['date_hosp']:
                    d['date_hosp'] = datetime.strftime(d['date_hosp'], '%Y-%m-%d')
                    data.append(d['date_hosp'])
                else:
                    data.append('')

                if d['service_interne']:
                    data.append(d['service_interne'])
                else:
                    data.append('')

                if d['rec_type']:
                    data.append(d['rec_type'])
                else:
                    data.append('')

                if d['ana_code']:
                    data.append(d['ana_code'])
                else:
                    data.append('')

                # specimen part
                if d['spec_date']:
                    d['spec_date'] = datetime.strftime(d['spec_date'], '%Y-%m-%d')
                    data.append(d['spec_date'])
                else:
                    data.append('')

                if d['spec_type']:
                    data.append(d['spec_type'])
                else:
                    data.append('')

                if d['spec_comment']:
                    data.append(d['spec_comment'])
                else:
                    data.append('')

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

        self.log.error(Logs.fileline() + ' : l_data=' + str(l_data))

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
            self.log.error(Logs.fileline() + ' : post ExportWhonet failed, err=%s', err)
            return False

        self.log.info(Logs.fileline() + ' : TRACE ExportWhonet')
        return compose_ret('', Constants.cst_content_type_json)
