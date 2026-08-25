# -*- coding:utf-8 -*-
import logging
import requests

from datetime import datetime
from flask import request
from flask_restful import Resource

from app.models.General import compose_ret
from app.models.Constants import Constants
from app.models.Audit import Audit
from app.models.Patient import Patient
from app.models.Logs import Logs
from app.models.Various import Various
from app.security.oauth_routes import require_oauth


# Names exported when this module is imported with "*" (see app/__init__.py).
# Without __all__, "import *" also brings in this module's own imports
# (Constants, datetime, logging...) and they leak into the caller.
__all__ = [
    'PatientList',
    'PatientListFromExt',
    'PatientListExport',
    'PatientSearch',
    'PatientCode',
    'PatientCodeLab',
    'PatientCombine',
    'PatientDet',
    'PatientFormItem',
    'PatientHistFormItem',
    'PatientHistoric',
]


class PatientList(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        l_patients = Patient.getPatientList(args)

        # self.log.info(Logs.fileline() + ' : TRACE l_patients=' + str(l_patients))

        if not l_patients:
            self.log.warning(Logs.fileline() + ' : TRACE PatientList not found')

        for patient in l_patients:
            # Replace None by empty string
            for key, value in list(patient.items()):
                if patient[key] is None:
                    patient[key] = ''

        self.log.info(Logs.fileline() + ' : TRACE PatientList')
        try:
            details = {"result": "SUCCESS", "count": len(l_patients) if l_patients else 0}
            Audit.insertAudit(audit_user, "PatientList", "PATIENT", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : PatientList ERROR audit')
        return compose_ret(l_patients, Constants.cst_content_type_json)


class PatientListFromExt(Resource):
    log = logging.getLogger('log_services')

    @require_oauth('external/patient')
    def post(self):
        self.log.info(Logs.fileline() + ' : PatientListFromExt API access authorized')
        audit_user = request.oauth_user
        args = request.get_json() or {}

        l_patients = Patient.getPatientList(args)

        # self.log.info(Logs.fileline() + ' : TRACE l_patients=' + str(l_patients))

        if not l_patients:
            self.log.warning(Logs.fileline() + ' : TRACE PatientListFromExt not found')

        sex_map = {1: 'M', 2: 'F', 3: 'U'}

        for patient in l_patients:
            patient['sex'] = sex_map.get(patient.get('sex'), 'U')

            lite_val = patient.get('lite')
            patient['lite'] = 'Y' if lite_val and int(lite_val) > 0 else 'N'

            birth_val = patient.get('birth_approx')
            if birth_val == 4:
                patient['birth_approx'] = 'Y'
            if birth_val == 5:
                patient['birth_approx'] = 'N'

            # Replace None by empty string
            for key, value in list(patient.items()):
                if patient[key] is None:
                    patient[key] = ''

        self.log.info(Logs.fileline() + ' : TRACE PatientListFromExt')
        try:
            details = {"result": "SUCCESS", "count": len(l_patients) if l_patients else 0}
            Audit.insertAudit(audit_user, "PatientListFromExt", "PATIENT", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : PatientListFromExt ERROR audit')
        return compose_ret(l_patients, Constants.cst_content_type_json)


class PatientListExport(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        l_data = [['id_data', 'id_owner', 'code', 'code_lab', 'lastname', 'firstname', 'birth', 'sex']]

        if 'code' not in args or 'code_lab' not in args or 'lastname' not in args or 'firstname' not in args:
            self.log.error(Logs.fileline() + ' : PatientListExport ERROR args missing')
            try:
                details = {"result": "ERROR", "reason": "ARGS_MISSING", "missing": ["code", "code_lab", "lastname", "firstname"]}
                Audit.insertAudit(audit_user, "PatientListExport", "PATIENT", None, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : PatientListExport ERROR audit args missing')
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
            try:
                details = {"result": "ERROR", "reason": "NO_DATA", "code": args.get("code"), "code_lab": args.get("code_lab"),
                           "lastname": args.get("lastname"), "firstname": args.get("firstname")}
                Audit.insertAudit(audit_user, "PatientListExport", "PATIENT", None, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : PatientListExport ERROR audit no data')
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
            self.log.exception(Logs.fileline() + ' : post PatientListExport failed')
            try:
                details = {"result": "ERROR", "reason": "WRITE_CSV_FAILED", "error": str(err)}
                Audit.insertAudit(audit_user, "PatientListExport", "PATIENT", None, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : PatientListExport ERROR audit write csv')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE PatientListExport')
        try:
            details = {"result": "SUCCESS", "filename": filename}
            Audit.insertAudit(audit_user, "PatientListExport", "PATIENT", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : PatientListExport ERROR audit success')
        return compose_ret('', Constants.cst_content_type_json)


class PatientSearch(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        l_pats = Patient.getPatientSearch(args['term'])

        if not l_pats:
            self.log.warning(Logs.fileline() + ' : WARNING PatientSearch NOT FOUND')
            try:
                details = {"result": "SUCCESS", "count": 0, "term": args.get('term') if args else None}
                Audit.insertAudit(audit_user, "PatientSearch", "PATIENT", None, "SUCCESS", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : PatientSearch ERROR audit')
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
        try:
            details = {"result": "SUCCESS", "count": len(l_pats), "term": args.get('term') if args else None}
            Audit.insertAudit(audit_user, "PatientSearch", "PATIENT", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : PatientSearch ERROR audit')
        return compose_ret(l_pats, Constants.cst_content_type_json)


class PatientCode(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self):
        audit_user = request.oauth_user
        code = Patient.newPatientCode()

        if not code:
            self.log.error(Logs.fileline() + ' : ERROR GeneratePatientCode not generate')
            try:
                details = {"result": "ERROR", "reason": "NOT_GENERATED"}
                Audit.insertAudit(audit_user, "PatientCode", "PATIENT", None, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : PatientCode ERROR audit')
            return compose_ret('', Constants.cst_content_type_json, 404)

        self.log.info(Logs.fileline() + ' : TRACE GeneratePatientCode : ' + code)
        try:
            details = {"result": "SUCCESS"}
            Audit.insertAudit(audit_user, "PatientCode", "PATIENT", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : PatientCode ERROR audit')
        return compose_ret(code, Constants.cst_content_type_json)


class PatientCodeLab(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self, pat_code_lab):
        audit_user = request.oauth_user
        ret = Patient.codeLab_exist(pat_code_lab)

        if ret and ret == -1:
            self.log.error(Logs.fileline() + ' : ' + 'PatientCodeLab ERROR sql')
            try:
                details = {"result": "ERROR", "reason": "SQL_ERROR", "pat_code_lab": pat_code_lab}
                Audit.insertAudit(audit_user, "PatientCodeLab", "PATIENT", None, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : PatientCodeLab ERROR audit')
            return compose_ret(-1, Constants.cst_content_type_json, 500)

        if ret:
            self.log.warning(Logs.fileline() + ' : ' + 'PatientCodeLab WARNING code already exist')
            try:
                details = {"result": "SUCCESS", "exists": 1, "pat_code_lab": pat_code_lab}
                Audit.insertAudit(audit_user, "PatientCodeLab", "PATIENT", None, "SUCCESS", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : PatientCodeLab ERROR audit')
            return compose_ret(1, Constants.cst_content_type_json, 200)
        else:
            self.log.info(Logs.fileline() + ' : PatientCodeLab code ok :' + str(pat_code_lab))
            try:
                details = {"result": "SUCCESS", "exists": 0, "pat_code_lab": pat_code_lab}
                Audit.insertAudit(audit_user, "PatientCodeLab", "PATIENT", None, "SUCCESS", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : PatientCodeLab ERROR audit')
            return compose_ret(0, Constants.cst_content_type_json, 200)


class PatientCombine(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self, id_pat1, id_pat2):
        audit_user = request.oauth_user

        if id_pat1 <= 0 or id_pat2 <= 0:
            self.log.error(Logs.fileline() + ' : ' + 'PatientCombine ERROR wrong id_pat')
            try:
                details = {"result": "ERROR", "reason": "WRONG_ID", "id_pat1": id_pat1, "id_pat2": id_pat2}
                Audit.insertAudit(audit_user, "PatientCombine", "PATIENT", None, "ERROR", details, "U")
            except Exception:
                self.log.exception(Logs.fileline() + ' : PatientCombine ERROR audit wrong id')
            return compose_ret('', Constants.cst_content_type_json, 400)

        ret = Patient.combinePatients(id_pat1, id_pat2)

        if not ret:
            self.log.error(Logs.fileline() + ' : ERROR PatientCombine')
            try:
                details = {"result": "ERROR", "reason": "COMBINE_FAILED", "id_pat1": id_pat1, "id_pat2": id_pat2}
                Audit.insertAudit(audit_user, "PatientCombine", "PATIENT", None, "ERROR", details, "U")
            except Exception:
                self.log.exception(Logs.fileline() + ' : PatientCombine ERROR audit failed')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE PatientCombine id_pat1=' + str(id_pat1) + ' | id_pat2=' + str(id_pat2))
        try:
            details = {"result": "SUCCESS", "id_pat1": id_pat1, "id_pat2": id_pat2}
            Audit.insertAudit(audit_user, "PatientCombine", "PATIENT", None, "SUCCESS", details, "U")
        except Exception:
            self.log.exception(Logs.fileline() + ' : PatientCombine ERROR audit success')
        return compose_ret('', Constants.cst_content_type_json)


class PatientDet(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self, id_pat):
        audit_user = request.oauth_user
        patient = Patient.getPatient(id_pat)

        if not patient:
            self.log.error(Logs.fileline() + ' : ' + 'PatientDet ERROR not found')
            try:
                details = {"result": "ERROR", "reason": "NOT_FOUND", "id_pat": id_pat}
                Audit.insertAudit(audit_user, "PatientDet", "PATIENT", id_pat, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : PatientDet ERROR audit not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        if patient['pat_birth']:
            patient['pat_birth'] = datetime.strftime(patient['pat_birth'], Constants.cst_isodate)

        # Replace None by empty string
        for key, value in list(patient.items()):
            if patient[key] is None:
                patient[key] = ''

        self.log.info(Logs.fileline() + ' : PatientDet id_pat=' + str(id_pat))
        try:
            details = {"result": "SUCCESS", "id_pat": id_pat}
            Audit.insertAudit(audit_user, "PatientDet", "PATIENT", id_pat, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : PatientDet ERROR audit success')
        return compose_ret(patient, Constants.cst_content_type_json, 200)

    @require_oauth()
    def post(self, id_pat=0):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        if 'id_user' not in args:
            self.log.error(Logs.fileline() + ' : PatientDet ERROR id_user missing')
            try:
                details = {"result": "ERROR", "reason": "ID_USER_MISSING", "id_pat": id_pat}
                Audit.insertAudit(audit_user, "PatientDet", "PATIENT", id_pat if id_pat else None, "ERROR", details, "U")
            except Exception:
                self.log.exception(Logs.fileline() + ' : PatientDet ERROR audit id_user missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        self.log.info(Logs.fileline() + ' : TRACE PatientDet DEBUG args = ' + str(args))

        default_keys = ['id_user', 'pat_ano', 'pat_code', 'pat_code_lab', 'pat_name', 'pat_firstname', 'pat_birth',
                        'pat_sex', 'pat_address', 'pat_zipcode', 'pat_city', 'pat_phone1', 'pat_phone2', 'pat_profession',
                        'pat_maiden', 'pat_district', 'pat_pbox', 'pat_birth_approx', 'pat_age', 'pat_age_unit',
                        'pat_midname', 'pat_nationality', 'pat_resident', 'pat_blood_group', 'pat_blood_rhesus',
                        'pat_email', 'pat_agreement', 'pat_amicare']

        default_values = {'pat_ano': 5,
                          'pat_code_lab': '',
                          'pat_name': '',
                          'pat_firstname': '',
                          'pat_sex': 3,
                          'pat_address': '',
                          'pat_zipcode': '',
                          'pat_city': '',
                          'pat_phone1': '',
                          'pat_phone2': '',
                          'pat_profession': '',
                          'pat_maiden': '',
                          'pat_district': '',
                          'pat_pbox': '',
                          'pat_birth_approx': 5,
                          'pat_age': 0,
                          'pat_age_unit': 0,
                          'pat_midname': '',
                          'pat_nationality': 0,
                          'pat_resident': 'Y',
                          'pat_blood_group': 0,
                          'pat_blood_rhesus': 0,
                          'pat_agreement': 'N',
                          'pat_amicare': 0,
                          'pat_email': ''}

        # Update patient
        if id_pat != 0:
            patient = Patient.getPatient(id_pat)

            if not patient:
                self.log.error(Logs.fileline() + ' : PatientDet ERROR not found')
                try:
                    details = {"result": "ERROR", "reason": "NOT_FOUND", "id_pat": id_pat}
                    Audit.insertAudit(audit_user, "PatientDet", "PATIENT", id_pat if id_pat else None, "ERROR", details, "U")
                except Exception:
                    self.log.exception(Logs.fileline() + ' : PatientDet ERROR audit')
                return compose_ret('', Constants.cst_content_type_json, 500)

            # AmiCare account creation (only if asked)
            if (not patient.get('pat_amicare') or patient.get('pat_amicare') == 0) and args.get('pat_amicare') == 1:
                self.create_amicare_account(args, id_pat)

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
                                        pat_email=args['pat_email'],
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
                                        blood_rhesus=args['pat_blood_rhesus'],
                                        pat_agreement=args['pat_agreement'],
                                        pat_amicare=args['pat_amicare'])

            if ret is False:
                self.log.error(Logs.alert() + ' : PatientDet ERROR update')
                try:
                    details = {"result": "ERROR", "reason": "UPDATE_FAILED", "id_pat": id_pat}
                    Audit.insertAudit(audit_user, "PatientDet", "PATIENT", id_pat if id_pat else None, "ERROR", details, "U")
                except Exception:
                    self.log.exception(Logs.fileline() + ' : PatientDet ERROR audit')
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
                                try:
                                    details = {"result": "ERROR", "reason": "DESACT_FORM_ITEM_FAILED", "id_pat": id_pat}
                                    Audit.insertAudit(audit_user, "PatientDet", "PATIENT", id_pat if id_pat else None, "ERROR", details, "U")
                                except Exception:
                                    self.log.exception(Logs.fileline() + ' : PatientDet ERROR audit')
                                return compose_ret('', Constants.cst_content_type_json, 500)

                            ret = Patient.insertFormItem(id_pat, key, value, args['id_user'])

                            if ret <= 0:
                                self.log.error(Logs.alert() + ' : PatientDet ERROR insertFormItem')
                                try:
                                    details = {"result": "ERROR", "reason": "INSERT_FORM_ITEM_FAILED", "id_pat": id_pat}
                                    Audit.insertAudit(audit_user, "PatientDet", "PATIENT", id_pat if id_pat else None, "ERROR", details, "U")
                                except Exception:
                                    self.log.exception(Logs.fileline() + ' : PatientDet ERROR audit')
                                return compose_ret('', Constants.cst_content_type_json, 500)
                    else:
                        ret = Patient.insertFormItem(id_pat, key, value, args['id_user'])

                        if ret <= 0:
                            self.log.error(Logs.alert() + ' : PatientDet ERROR insertFormItem')
                            try:
                                details = {"result": "ERROR", "reason": "INSERT_FORM_ITEM_FAILED", "id_pat": id_pat}
                                Audit.insertAudit(audit_user, "PatientDet", "PATIENT", id_pat if id_pat else None, "ERROR", details, "U")
                            except Exception:
                                self.log.exception(Logs.fileline() + ' : PatientDet ERROR audit')
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
                                        pat_email=args['pat_email'],
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
                                        blood_rhesus=args['pat_blood_rhesus'],
                                        pat_agreement=args['pat_agreement'],
                                        pat_amicare=0)

            if ret <= 0:
                self.log.error(Logs.alert() + ' : PatientDet ERROR insert')
                try:
                    details = {"result": "ERROR", "reason": "INSERT_FAILED", "id_pat": id_pat}
                    Audit.insertAudit(audit_user, "PatientDet", "PATIENT", id_pat if id_pat else None, "ERROR", details, "C")
                except Exception:
                    self.log.exception(Logs.fileline() + ' : PatientDet ERROR audit')
                return compose_ret('', Constants.cst_content_type_json, 500)

            res = {}
            res['id_pat'] = ret

            # AmiCare account creation (only if enabled)
            if args.get('pat_amicare') == 1:
                self.create_amicare_account(args, res['id_pat'])

            # insert additionnal custom field
            for key, value in args.items():
                if key not in default_keys:
                    ret = Patient.insertFormItem(res['id_pat'], key, value, args['id_user'])

                    if ret <= 0:
                        self.log.error(Logs.alert() + ' : PatientDet ERROR insertFormItem')
                        try:
                            details = {"result": "ERROR", "reason": "INSERT_FORM_ITEM_FAILED", "id_pat": id_pat}
                            Audit.insertAudit(audit_user, "PatientDet", "PATIENT", id_pat if id_pat else None, "ERROR", details, "U")
                        except Exception:
                            self.log.exception(Logs.fileline() + ' : PatientDet ERROR audit')
                        return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE PatientDet id_pat=' + str(id_pat))
        try:
            details = {"result": "SUCCESS", "id_pat": res.get('id_pat') if isinstance(res, dict) else None}
            Audit.insertAudit(audit_user, "PatientDet", "PATIENT", res.get('id_pat') if isinstance(res, dict) else None, "SUCCESS", details, "U")
        except Exception:
            self.log.exception(Logs.fileline() + ' : PatientDet ERROR audit success')
        return compose_ret(res, Constants.cst_content_type_json)

    def create_amicare_account(self, args, id_pat):
        from app import AMICARE_CONFIG
        if args.get('pat_amicare') != 1:
            return

        try:
            url = AMICARE_CONFIG['base_url'] + AMICARE_CONFIG['endpoints']['create_patient']

            payload = {
                "patient": {
                    "nom": args.get('pat_name'),
                    "pnom": args.get('pat_firstname'),
                    "login": args.get('pat_email'),
                    "pwd": args.get('pat_email'),
                    "mail": args.get('pat_email'),
                    "sexe": "M" if args.get('pat_sex') == 1 else "F",
                    "tel": args.get('pat_phone1'),
                    "dn": args.get('pat_birth').strftime('%Y%m%d') if args.get('pat_birth') else None,
                    "id_ami": id_pat,
                    "id_amic": 0
                }
            }

            response = requests.post(url, json=payload, auth=(AMICARE_CONFIG['auth']['username'], AMICARE_CONFIG['auth']['password']), timeout=10)

            if response.status_code == 200:
                res = response.json()
                amicare_id = res.get('id_pat')

                if amicare_id:
                    Patient.update_amicare_id(id_pat, amicare_id)

            self.log.info(Logs.fileline() + ' : AMICARE status=' + str(response.status_code))
        except Exception:
            self.log.exception(Logs.fileline() + ' : AMICARE')


class PatientFormItem(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self, id_pat):
        audit_user = request.oauth_user

        l_vals  = {}
        l_items = Patient.getFormItems(id_pat)

        if not l_items:
            self.log.error(Logs.fileline() + ' : ' + 'PatientFormItem WARNING not found')

        for item in l_items:
            key_val = str(item['pfi_key'])
            l_vals[key_val] = item['pfi_value']

        self.log.info(Logs.fileline() + ' : PatientFormItem id_pat=' + str(id_pat))
        try:
            details = {"result": "SUCCESS", "id_pat": id_pat, "count": len(l_items) if l_items else 0}
            Audit.insertAudit(audit_user, "PatientFormItem", "PATIENT", id_pat, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : PatientFormItem ERROR audit')
        return compose_ret(l_vals, Constants.cst_content_type_json, 200)


class PatientHistFormItem(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self, id_pat):
        audit_user = request.oauth_user

        l_items = Patient.getHistFormItems(id_pat)

        if not l_items:
            self.log.error(Logs.fileline() + ' : PatientHistFormItem WARNING not found')
            try:
                details = {"result": "ERROR", "reason": "NOT_FOUND", "id_pat": id_pat}
                Audit.insertAudit(audit_user, "PatientHistFormItem", "PATIENT", id_pat, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : PatientHistFormItem ERROR audit not found')
            return compose_ret([], Constants.cst_content_type_json, 200)

        events = {}

        for row in l_items:
            evt_id   = row['phfi_evt']
            evt_type = row['phfi_type']

            if evt_id not in events:
                evt = {}
                evt['evt'] = evt_id
                evt['block_id'] = evt_type

                firstname = row.get('firstname') or ''
                lastname = row.get('lastname') or ''
                username = row.get('username') or ''
                user_label = ''

                if firstname or lastname:
                    user_label = (firstname + ' ' + lastname).strip()
                    if username:
                        user_label += ' (' + username + ')'
                elif username:
                    user_label = username
                else:
                    user_label = str(row['phfi_user'])

                evt['user_name'] = user_label

                phfi_date = row['phfi_date']
                if phfi_date is not None:
                    evt['datetime'] = phfi_date.strftime(Constants.cst_dt_HM)
                else:
                    evt['datetime'] = ''

                evt['fields'] = {}
                events[evt_id] = evt

            key = str(row['phfi_key'])
            val = row['phfi_value']
            events[evt_id]['fields'][key] = val

        l_vals = list(events.values())

        self.log.info(Logs.fileline() + ' : PatientHistFormItem get id_pat=' + str(id_pat))
        try:
            details = {"result": "SUCCESS", "count": len(l_vals) if l_vals else 0, "id_pat": id_pat}
            Audit.insertAudit(audit_user, "PatientHistFormItem", "PATIENT", id_pat, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : PatientHistFormItem ERROR audit')
        return compose_ret(l_vals, Constants.cst_content_type_json, 200)

    @require_oauth()
    def post(self, id_pat):
        audit_user = request.oauth_user
        args = request.get_json(silent=True) or {}

        id_user  = args.get('id_user')
        block_id = args.get('block_id')
        fields   = args.get('fields')

        if not id_pat or id_pat <= 0:
            self.log.error(Logs.fileline() + ' : PatientHistFormItem ERROR id_pat invalid')
            try:
                details = {"result": "ERROR", "reason": "ID_PAT_INVALID", "id_pat": id_pat}
                Audit.insertAudit(audit_user, "PatientHistFormItem", "PATIENT", id_pat, "ERROR", details, "U")
            except Exception:
                self.log.exception(Logs.fileline() + ' : PatientHistFormItem ERROR audit id_pat invalid')
            return compose_ret('', Constants.cst_content_type_json, 400)

        if not id_user or not block_id or not isinstance(fields, dict) or not fields:
            self.log.error(Logs.fileline() + ' : PatientHistFormItem ERROR invalid payload')
            try:
                details = {"result": "ERROR", "reason": "INVALID_PAYLOAD", "id_pat": id_pat, "id_user": id_user, "block_id": block_id}
                Audit.insertAudit(audit_user, "PatientHistFormItem", "PATIENT", id_pat, "ERROR", details, "U")
            except Exception:
                self.log.exception(Logs.fileline() + ' : PatientHistFormItem ERROR audit invalid payload')
            return compose_ret('', Constants.cst_content_type_json, 400)

        evt = Patient.insertHistFormItem(id_pat, id_user, block_id, fields)

        self.log.info(Logs.fileline() + ' : PatientHistFormItem saved evt=' + str(evt))
        try:
            details = {"result": "SUCCESS", "id_pat": id_pat, "id_user": id_user, "block_id": block_id, "evt": evt}
            Audit.insertAudit(audit_user, "PatientHistFormItem", "PATIENT", id_pat, "SUCCESS", details, "U")
        except Exception:
            self.log.exception(Logs.fileline() + ' : PatientHistFormItem ERROR audit success')
        return compose_ret({'evt': evt}, Constants.cst_content_type_json, 200)

    @require_oauth()
    def delete(self, id_pat, evt_id):
        audit_user = request.oauth_user

        if not evt_id:
            self.log.error(Logs.fileline() + ' : PatientHistFormItem DELETE missing evt_id')
            try:
                details = {"result": "ERROR", "reason": "EVT_ID_MISSING", "id_pat": id_pat, "evt_id": evt_id}
                Audit.insertAudit(audit_user, "PatientHistFormItem", "PATIENT", id_pat, "ERROR", details, "D")
            except Exception:
                self.log.exception(Logs.fileline() + ' : PatientHistFormItem ERROR audit delete missing evt_id')
            return compose_ret('', Constants.cst_content_type_json, 400)

        deleted = Patient.deleteHistFormEvent(id_pat, evt_id)
        if not deleted:
            self.log.error(Logs.fileline() + ' : PatientHistFormItem DELETE not found id_pat=' + str(id_pat) + ' evt_id=' + str(evt_id))
            try:
                details = {"result": "ERROR", "reason": "NOT_FOUND", "id_pat": id_pat, "evt_id": evt_id}
                Audit.insertAudit(audit_user, "PatientHistFormItem", "PATIENT", id_pat, "ERROR", details, "D")
            except Exception:
                self.log.exception(Logs.fileline() + ' : PatientHistFormItem ERROR audit delete not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        self.log.info(Logs.fileline() + ' : PatientHistFormItem DELETE id_pat=' + str(id_pat) + ' evt_id=' + str(evt_id))
        try:
            details = {"result": "SUCCESS", "id_pat": id_pat, "evt_id": evt_id}
            Audit.insertAudit(audit_user, "PatientHistFormItem", "PATIENT", id_pat, "SUCCESS", details, "D")
        except Exception:
            self.log.exception(Logs.fileline() + ' : PatientHistFormItem ERROR audit delete success')
        return compose_ret({'deleted': deleted}, Constants.cst_content_type_json, 200)


class PatientHistoric(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self, id_pat):
        audit_user = request.oauth_user

        l_datas = {}
        no_analyzes = False

        patient = Patient.getPatient(id_pat)

        if not patient:
            self.log.error(Logs.fileline() + ' : ' + 'PatientHistoric ERROR not found')
            try:
                details = {"result": "ERROR", "reason": "NOT_FOUND", "id_pat": id_pat}
                Audit.insertAudit(audit_user, "PatientHistoric", "PATIENT", id_pat, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : PatientHistoric ERROR audit not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        if patient.get('pat_birth'):
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
            no_analyzes = True

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
        try:
            if no_analyzes:
                details = {"result": "SUCCESS", "reason": "NO_ANALYZES", "id_pat": id_pat}
                Audit.insertAudit(audit_user, "PatientHistoric", "PATIENT", id_pat, "SUCCESS", details, "R")
            else:
                details = {"result": "SUCCESS", "id_pat": id_pat}
                Audit.insertAudit(audit_user, "PatientHistoric", "PATIENT", id_pat, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : PatientHistoric ERROR audit')
        return compose_ret(l_datas, Constants.cst_content_type_json, 200)
