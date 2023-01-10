# -*- coding:utf-8 -*-
import logging
import gettext

from datetime import datetime
from flask import request
from flask_restful import Resource

from app.models.General import compose_ret
from app.models.Constants import *
from app.models.Patient import *
from app.models.User import *
from app.models.Logs import Logs
from app.models.Various import Various


class PatientList(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        if not args:
            args = {}

        l_patients = Patient.getPatientList(args)

        # self.log.info(Logs.fileline() + ' : TRACE l_patients=' + str(l_patients))

        if not l_patients:
            self.log.error(Logs.fileline() + ' : TRACE PatientList not found')

        for patient in l_patients:
            # Replace None by empty string
            for key, value in list(patient.items()):
                if patient[key] is None:
                    patient[key] = ''

        self.log.info(Logs.fileline() + ' : TRACE PatientList')
        return compose_ret(l_patients, Constants.cst_content_type_json)


class PatientListExport(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        l_data = [['id_data', 'id_owner', 'code', 'code_lab', 'lastname', 'firstname', 'birth', 'sex']]

        if 'code' not in args or 'code_lab' not in args or 'lastname' not in args or 'firstname' not in args:
            self.log.error(Logs.fileline() + ' : PatientListExport ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        args['limit'] = 50000  # for overpassed default limit

        dict_data = Patient.getPatientList(args)

        if dict_data:
            for d in dict_data:
                data = []

                data.append(d['id_data'])
                data.append(d['id_owner'])
                data.append(d['code'])
                data.append(d['code_lab'])
                data.append(d['lastname'])
                data.append(d['firstname'])
                data.append(d['birth'])
                data.append(d['sex'])

                l_data.append(data)

        # if no result to export
        if len(l_data) < 2:
            return compose_ret('', Constants.cst_content_type_json, 404)

        # write csv file
        try:
            import csv

            today = datetime.now().strftime("%Y%m%d")

            filename = 'patients_' + str(today) + '.csv'

            with open('tmp/' + filename, mode='w', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=';')
                for line in l_data:
                    writer.writerow(line)

        except Exception as err:
            self.log.error(Logs.fileline() + ' : post PatientListExport failed, err=%s', err)
            return False

        self.log.info(Logs.fileline() + ' : TRACE PatientListExport')
        return compose_ret('', Constants.cst_content_type_json)


class PatientSearch(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        l_pats = Patient.getPatientSearch(args['term'])

        if not l_pats:
            self.log.error(Logs.fileline() + ' : WARNING PatientSearch NOT FOUND')
            return compose_ret('', Constants.cst_content_type_json, 200)  # 200 if not select2 trigger an exception

        Various.useLangPDF()

        for pat in l_pats:
            # Replace None by empty string
            for key, value in list(pat.items()):
                if pat[key] is None:
                    pat[key] = ''
                elif key == 'age_unit' and pat[key]:
                    pat[key] = _(pat[key].strip())

        self.log.info(Logs.fileline() + ' : TRACE PatientSearch')
        return compose_ret(l_pats, Constants.cst_content_type_json)


class PatientCode(Resource):
    log = logging.getLogger('log_services')

    def get(self):
        code = Patient.newPatientCode()

        if not code:
            self.log.error(Logs.fileline() + ' : ERROR GeneratePatientCode not generate')
            return compose_ret('', Constants.cst_content_type_json, 404)

        self.log.info(Logs.fileline() + ' : TRACE GeneratePatientCode : ' + code)
        return compose_ret(code, Constants.cst_content_type_json)


class PatientCombine(Resource):
    log = logging.getLogger('log_services')

    def post(self, id_pat1, id_pat2):
        if id_pat1 <= 0 or id_pat2 <= 0:
            self.log.error(Logs.fileline() + ' : ' + 'PatientCombine ERROR wrong id_pat')
            return compose_ret('', Constants.cst_content_type_json, 500)

        ret = Patient.combinePatients(id_pat1, id_pat2)

        if not ret:
            self.log.error(Logs.fileline() + ' : ERROR PatientCombine')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE PatientCombine id_pat1=' + str(id_pat1) + ' | id_pat2=' + str(id_pat2))
        return compose_ret('', Constants.cst_content_type_json)


class PatientDet(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_pat):
        patient = Patient.getPatient(id_pat)

        if not patient:
            self.log.error(Logs.fileline() + ' : ' + 'PatientDet ERROR not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        if patient['ddn']:
            patient['ddn'] = datetime.strftime(patient['ddn'], '%Y-%m-%d')

        # Replace None by empty string
        for key, value in list(patient.items()):
            if patient[key] is None:
                patient[key] = ''

        self.log.info(Logs.fileline() + ' : PatientDet id_pat=' + str(id_pat))
        return compose_ret(patient, Constants.cst_content_type_json, 200)

    def post(self, id_pat=0):
        args = request.get_json()

        if 'id_owner' not in args or 'anonyme' not in args or 'code' not in args or 'code_patient' not in args or \
           'nom' not in args or 'prenom' not in args or 'ddn' not in args or 'sexe' not in args or \
           'adresse' not in args or 'cp' not in args or 'ville' not in args or 'phone2' not in args or \
           'tel' not in args or 'profession' not in args or 'nom_jf' not in args or 'quartier' not in args or \
           'bp' not in args or 'ddn_approx' not in args or 'age' not in args or \
           'midname' not in args or 'nationality' not in args or 'resident' not in args or 'blood_group' not in args or \
           'blood_rhesus' not in args or 'unite' not in args:
            self.log.error(Logs.fileline() + ' : PatientDet ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # Update patient
        if id_pat != 0:
            patient = Patient.getPatient(id_pat)

            if not patient:
                self.log.error(Logs.fileline() + ' : PatientDet ERROR not found')
                return compose_ret('', Constants.cst_content_type_json, 500)

            if args['ddn']:
                args['ddn'] = datetime.strptime(args['ddn'], Constants.cst_isodate)
            else:
                args['ddn'] = None

            ret = Patient.updatePatient(id=id_pat,
                                        id_owner=args['id_owner'],
                                        anonyme=args['anonyme'],
                                        code=args['code'],
                                        code_patient=args['code_patient'],
                                        nom=args['nom'],
                                        prenom=args['prenom'],
                                        ddn=args['ddn'],
                                        sexe=args['sexe'],
                                        adresse=args['adresse'],
                                        cp=args['cp'],
                                        ville=args['ville'],
                                        tel=args['tel'],
                                        phone2=args['phone2'],
                                        profession=args['profession'],
                                        nom_jf=args['nom_jf'],
                                        quartier=args['quartier'],
                                        bp=args['bp'],
                                        ddn_approx=args['ddn_approx'],
                                        age=args['age'],
                                        unite=args['unite'],
                                        midname=args['midname'],
                                        nationality=args['nationality'],
                                        resident=args['resident'],
                                        blood_group=args['blood_group'],
                                        blood_rhesus=args['blood_rhesus'])

            if ret is False:
                self.log.error(Logs.alert() + ' : PatientDet ERROR update')
                return compose_ret('', Constants.cst_content_type_json, 500)

            res = {}
            res['id_pat'] = id_pat

        # Insert new patient
        else:
            if args['ddn']:
                args['ddn'] = datetime.strptime(args['ddn'], Constants.cst_isodate)
            else:
                args['ddn'] = None

            ret = Patient.insertPatient(id_owner=args['id_owner'],
                                        anonyme=args['anonyme'],
                                        code=args['code'],
                                        code_patient=args['code_patient'],
                                        nom=args['nom'],
                                        prenom=args['prenom'],
                                        ddn=args['ddn'],
                                        sexe=args['sexe'],
                                        adresse=args['adresse'],
                                        cp=args['cp'],
                                        ville=args['ville'],
                                        tel=args['tel'],
                                        phone2=args['phone2'],
                                        profession=args['profession'],
                                        nom_jf=args['nom_jf'],
                                        quartier=args['quartier'],
                                        bp=args['bp'],
                                        ddn_approx=args['ddn_approx'],
                                        age=args['age'],
                                        unite=args['unite'],
                                        midname=args['midname'],
                                        nationality=args['nationality'],
                                        resident=args['resident'],
                                        blood_group=args['blood_group'],
                                        blood_rhesus=args['blood_rhesus'])

            if ret <= 0:
                self.log.error(Logs.alert() + ' : PatientDet ERROR  insert')
                return compose_ret('', Constants.cst_content_type_json, 500)

            res = {}
            res['id_pat'] = ret

        self.log.info(Logs.fileline() + ' : TRACE PatientDet id_pat=' + str(res['id_pat']))
        return compose_ret(res, Constants.cst_content_type_json)


class PatientHistoric(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_pat):
        l_datas = {}

        patient = Patient.getPatient(id_pat)

        if not patient:
            self.log.error(Logs.fileline() + ' : ' + 'PatientHistoric ERROR not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        if patient['ddn']:
            patient['ddn'] = datetime.strftime(patient['ddn'], '%Y-%m-%d')

        # Replace None by empty string
        for key, value in list(patient.items()):
            if patient[key] is None:
                patient[key] = ''

        l_datas['patient'] = patient

        analyzes = Patient.getPatientHistoric(id_pat)

        if not analyzes:
            self.log.error(Logs.fileline() + ' : ' + 'PatientHistoric ERROR not found')
            analyzes = {}

        Various.useLangDB()

        for ana in analyzes:
            # Replace None by empty string
            for key, value in list(ana.items()):
                if ana[key] is None:
                    ana[key] = ''
                elif key == 'analysis' and ana[key]:
                    ana[key] = _(ana[key].strip())
                elif key == 'variable' and ana[key]:
                    ana[key] = _(ana[key].strip())
                elif key == 'result' and ana[key]:
                    ana[key] = _(ana[key].strip())

            if ana['date_prescr']:
                ana['date_prescr'] = datetime.strftime(ana['date_prescr'], '%Y-%m-%d')

            if ana['type_rec'] and ana['type_rec'] == 183:
                ana['type_rec'] = 'E'
            else:
                ana['type_rec'] = 'I'

        l_datas['analyzes'] = analyzes

        self.log.info(Logs.fileline() + ' : PatientHistoric id_pat=' + str(id_pat))
        return compose_ret(l_datas, Constants.cst_content_type_json, 200)
