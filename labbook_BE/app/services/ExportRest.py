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


class ExportWhonet(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        if 'date_beg' not in args or 'date_end' not in args:
            self.log.error(Logs.fileline() + ' : TRACE ExportWhonet ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # Data
        l_data = [["Laboratoire", "Lab adresse", "Lab ville", "Specialité", "Numéro d'identification", "Nom de famille",
                   "Prénom", "Nom et prénom ", "Sexe", "Date de naissance", "Age", "Catégorie d'âge", "Adresse (patient)",
                   "Ville (patient)", "Code postal (patient)", "Téléphone (patient)", "Profession (patient)",
                   "Date d'admission", "Service", "Type patient", "Isolate number",
                   "Date de prélèvement", "Type de prélèvement", "Commentaire", "Micro-organisme",
                   "Nom de l'antibiotique 1", "Methode de détermination",
                   "Method value", "Resultat d'antibiotique 1"]]
        dict_data = Export.getDataWhonet(args['date_beg'], args['date_end'])

        if dict_data:
            for d in dict_data:
                data = []

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

                if d['med_spe']:
                    data.append(d['med_spe'])
                else:
                    data.append('')

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
                    if d['cat_age'] == 1037:
                        data.append('Années')
                    elif d['cat_age'] == 1036:
                        data.append('Mois')
                    elif d['cat_age'] == 1035:
                        data.append('Semaines')
                    elif d['cat_age'] == 1034:
                        data.append('Jours')
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
