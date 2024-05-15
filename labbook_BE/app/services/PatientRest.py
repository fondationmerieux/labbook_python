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

        if patient['pat_birth']:
            patient['pat_birth'] = datetime.strftime(patient['pat_birth'], Constants.cst_isodate)

        # Replace None by empty string
        for key, value in list(patient.items()):
            if patient[key] is None:
                patient[key] = ''

        self.log.info(Logs.fileline() + ' : PatientDet id_pat=' + str(id_pat))
        return compose_ret(patient, Constants.cst_content_type_json, 200)

    def post(self, id_pat=0):
        args = request.get_json()

        if 'id_user' not in args:
            self.log.error(Logs.fileline() + ' : PatientDet ERROR id_user missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        self.log.info(Logs.fileline() + ' : TRACE PatientDet DEBUG args = ' + str(args))

        default_keys = ['id_user', 'pat_ano', 'pat_code', 'pat_code_lab', 'pat_name', 'pat_firstname', 'pat_birth',
                        'pat_sex', 'pat_address', 'pat_zipcode', 'pat_city', 'pat_phone1', 'pat_phone2', 'pat_profession',
                        'pat_maiden', 'pat_district', 'pat_pbox', 'pat_birth_approx', 'pat_age', 'pat_age_unit',
                        'pat_midname', 'pat_nationality', 'pat_resident', 'pat_blood_group', 'pat_blood_rhesus']

        default_values = {'pat_ano': 5,
                          'pat_code_lab': '',
                          'pat_name': '',
                          'pat_firstname': '',
                          'pat_sex': 3,
                          'pat_address': '',
                          'pat_zipcode': '',
                          'pat_city': '',
                          'pat_phone1' : '',
                          'pat_phone2' : '',
                          'pat_profession' : '',
                          'pat_maiden' : '',
                          'pat_district' : '',
                          'pat_pbox' : '',
                          'pat_birth_approx' : 5,
                          'pat_age' : 0,
                          'pat_age_unit' : 0,
                          'pat_midname' : '',
                          'pat_nationality' : 0,
                          'pat_resident' : 'Y',
                          'pat_blood_group' : 0,
                          'pat_blood_rhesus' : 0}

        # Update patient
        if id_pat != 0:
            patient = Patient.getPatient(id_pat)

            if not patient:
                self.log.error(Logs.fileline() + ' : PatientDet ERROR not found')
                return compose_ret('', Constants.cst_content_type_json, 500)

            if 'pat_birth' in args and args['pat_birth']:
                args['pat_birth'] = datetime.strptime(args['pat_birth'], Constants.cst_isodate)
            else:
                args['pat_birth'] = None

            # check if old elements are present, otherwise take the default value
            for key, value in default_values.items():
                if key not in args:
                    args[key] = value

            ret = Patient.updatePatient(id=id_pat,
                                        id_owner=args['id_user'],
                                        anonyme=args['pat_ano'],
                                        code=args['pat_code'],
                                        code_patient=args['pat_code_lab'],
                                        nom=args['pat_name'],
                                        prenom=args['pat_firstname'],
                                        ddn=args['pat_birth'],
                                        sexe=args['pat_sex'],
                                        adresse=args['pat_address'],
                                        cp=args['pat_zipcode'],
                                        ville=args['pat_city'],
                                        tel=args['pat_phone1'],
                                        phone2=args['pat_phone2'],
                                        profession=args['pat_profession'],
                                        nom_jf=args['pat_maiden'],
                                        quartier=args['pat_district'],
                                        bp=args['pat_pbox'],
                                        ddn_approx=args['pat_birth_approx'],
                                        age=args['pat_age'],
                                        unite=args['pat_age_unit'],
                                        midname=args['pat_midname'],
                                        nationality=args['pat_nationality'],
                                        resident=args['pat_resident'],
                                        blood_group=args['pat_blood_group'],
                                        blood_rhesus=args['pat_blood_rhesus'])

            if ret is False:
                self.log.error(Logs.alert() + ' : PatientDet ERROR update')
                return compose_ret('', Constants.cst_content_type_json, 500)

            res = {}
            res['id_pat'] = id_pat

            # insert additionnal custom field
            for key, value in args.items():
                if key not in default_keys:
                    # check if exist and active
                    if Patient.checkFormItem(id_pat, key):

                        # if not the same value
                        if not Patient.sameFormItem(id_pat, key, value, 'Y'):
                            # update active flag to No
                            ret = Patient.desactFormItem(id_pat, key)

                            if not ret:
                                self.log.error(Logs.alert() + ' : PatientDet ERROR desactFormItem')
                                return compose_ret('', Constants.cst_content_type_json, 500)

                            ret = Patient.insertFormItem(id_pat, key, value, args['id_user'])

                            if ret <= 0:
                                self.log.error(Logs.alert() + ' : PatientDet ERROR insertFormItem')
                                return compose_ret('', Constants.cst_content_type_json, 500)
                    else:
                        ret = Patient.insertFormItem(id_pat, key, value, args['id_user'])

                        if ret <= 0:
                            self.log.error(Logs.alert() + ' : PatientDet ERROR insertFormItem')
                            return compose_ret('', Constants.cst_content_type_json, 500)

        # Insert new patient
        else:
            if args['pat_birth']:
                args['pat_birth'] = datetime.strptime(args['pat_birth'], Constants.cst_isodate)
            else:
                args['pat_birth'] = None

            # check if old elements are present, otherwise take the default value
            for key, value in default_values.items():
                if key not in args:
                    args[key] = value

            ret = Patient.insertPatient(id_owner=args['id_user'],
                                        anonyme=args['pat_ano'],
                                        code=args['pat_code'],
                                        code_patient=args['pat_code_lab'],
                                        nom=args['pat_name'],
                                        prenom=args['pat_firstname'],
                                        ddn=args['pat_birth'],
                                        sexe=args['pat_sex'],
                                        adresse=args['pat_address'],
                                        cp=args['pat_zipcode'],
                                        ville=args['pat_city'],
                                        tel=args['pat_phone1'],
                                        phone2=args['pat_phone2'],
                                        profession=args['pat_profession'],
                                        nom_jf=args['pat_maiden'],
                                        quartier=args['pat_district'],
                                        bp=args['pat_pbox'],
                                        ddn_approx=args['pat_birth_approx'],
                                        age=args['pat_age'],
                                        unite=args['pat_age_unit'],
                                        midname=args['pat_midname'],
                                        nationality=args['pat_nationality'],
                                        resident=args['pat_resident'],
                                        blood_group=args['pat_blood_group'],
                                        blood_rhesus=args['pat_blood_rhesus'])

            if ret <= 0:
                self.log.error(Logs.alert() + ' : PatientDet ERROR insert')
                return compose_ret('', Constants.cst_content_type_json, 500)

            res = {}
            res['id_pat'] = ret

            # insert additionnal custom field
            for key, value in args.items():
                if key not in default_keys:
                    ret = Patient.insertFormItem(res['id_pat'], key, value, args['id_user'])

                    if ret <= 0:
                        self.log.error(Logs.alert() + ' : PatientDet ERROR insertFormItem')
                        return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE PatientDet id_pat=' + str(id_pat))
        return compose_ret(res, Constants.cst_content_type_json)


class PatientFormItem(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_pat):
        l_vals  = {}
        l_items = Patient.getFormItems(id_pat)

        if not l_items:
            self.log.error(Logs.fileline() + ' : ' + 'PatientFormItem WARNING not found')

        for item in l_items:
            key_val = str(item['pfi_key'])
            l_vals[key_val] = item['pfi_value']

        self.log.info(Logs.fileline() + ' : PatientFormItem id_pat=' + str(id_pat))
        return compose_ret(l_vals, Constants.cst_content_type_json, 200)


class PatientHistoric(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_pat):
        l_datas = {}

        patient = Patient.getPatient(id_pat)

        if not patient:
            self.log.error(Logs.fileline() + ' : ' + 'PatientHistoric ERROR not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        if patient['pat_birth']:
            patient['pat_birth'] = datetime.strftime(patient['pat_birth'], Constants.cst_isodate)

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
                ana['date_prescr'] = datetime.strftime(ana['date_prescr'], Constants.cst_isodate)

            if ana['type_rec'] and ana['type_rec'] == 183:
                ana['type_rec'] = 'E'
            else:
                ana['type_rec'] = 'I'

        l_datas['analyzes'] = analyzes

        self.log.info(Logs.fileline() + ' : PatientHistoric id_pat=' + str(id_pat))
        return compose_ret(l_datas, Constants.cst_content_type_json, 200)
