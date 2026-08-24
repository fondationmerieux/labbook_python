# -*- coding:utf-8 -*-
import logging
import gettext

from datetime import datetime
from flask import request
from flask_restful import Resource
from decimal import Decimal

from app.models.Audit import Audit
from app.models.Analysis import Analysis
from app.models.General import compose_ret
from app.models.Constants import Constants
from app.models.Doctor import Doctor
from app.models.File import File
from app.models.Patient import Patient
from app.models.Product import Product
from app.models.Record import Record
from app.models.Result import Result
from app.models.Various import Various
from app.models.Logs import Logs
from app.security.oauth_routes import require_oauth


class RecordList(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self, id_pres):
        audit_user = request.oauth_user
        args = request.get_json()

        if not args:
            args = {}

        l_records = Record.getRecordList(args, id_pres)

        if not l_records:
            l_records = []
            self.log.error(Logs.fileline() + ' : TRACE RecordList not found')

        for record in l_records:
            # Replace None by empty string
            for key, value in list(record.items()):
                if record[key] is None:
                    record[key] = ''

            if record['type_rec'] and record['type_rec'] == 183:
                record['type_rec'] = 'E'
            else:
                record['type_rec'] = 'I'

        self.log.info(Logs.fileline() + ' : TRACE RecordList')
        try:
            details = {"result": "SUCCESS", "id_pres": int(id_pres), "count": len(l_records) if l_records else 0}
            Audit.insertAudit(audit_user, "RecordList", "PRESCRIPTION", int(id_pres), "SUCCESS", details, "R")
        except Exception as err:
            self.log.error(Logs.fileline() + ' : RecordList ERROR audit success err=' + str(err))
        return compose_ret(l_records, Constants.cst_content_type_json)


class RecordListFromExt(Resource):
    log = logging.getLogger('log_services')

    @require_oauth('external/record')
    def post(self, id_pres):
        self.log.info(Logs.fileline() + ' : RecordListFromExt API access authorized')
        audit_user = request.oauth_user
        args = request.get_json()

        if not args:
            args = {}

        if 'stat_rec' in args and args['stat_rec']:
            if args['stat_rec'] == 'N':
                args['stat_rec'] = 181
            elif args['stat_rec'] == 'A':
                args['stat_rec'] = 182
            elif args['stat_rec'] == 'IA':
                args['stat_rec'] = 253
            elif args['stat_rec'] == 'T':
                args['stat_rec'] = 254
            elif args['stat_rec'] == 'IT':
                args['stat_rec'] = 255
            elif args['stat_rec'] == 'B':
                args['stat_rec'] = 256
            else:
                args['stat_rec'] = 0
        else:
            args['stat_rec'] = 0

        if 'emer' in args and args['emer']:
            if args['emer'] == 'Y':
                args['emer'] = 4
            else:
                args['emer'] = 0

        l_records = Record.getRecordList(args, id_pres)

        if not l_records:
            l_records = []
            self.log.error(Logs.fileline() + ' : TRACE RecordListFromExt not found')

        for record in l_records:
            # Replace None by empty string
            for key, value in list(record.items()):
                if record[key] is None:
                    record[key] = ''

            if record['type_rec'] and record['type_rec'] == 183:
                record['type_rec'] = 'E'
            else:
                record['type_rec'] = 'I'

        self.log.info(Logs.fileline() + ' : TRACE RecordListFromExt')
        try:
            details = {"result": "SUCCESS", "id_pres": int(id_pres), "count": len(l_records) if l_records else 0}
            Audit.insertAudit(audit_user, "RecordListFromExt", "PRESCRIPTION", int(id_pres), "SUCCESS", details, "R")
        except Exception as err:
            self.log.error(Logs.fileline() + ' : RecordListFromExt ERROR audit success err=' + str(err))
        return compose_ret(l_records, Constants.cst_content_type_json, 200)


class RecordDet(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self, id_rec):
        audit_user = request.oauth_user
        record = Record.getRecord(id_rec)

        if not record:
            self.log.error(Logs.fileline() + ' : ' + 'RecordDet ERROR not found')
            try:
                details = {"result": "ERROR", "reason": "NOT_FOUND", "id_rec": int(id_rec)}
                Audit.insertAudit(audit_user, "RecordDet", "RECORD", int(id_rec), "ERROR", details, "R")
            except Exception as err:
                self.log.error(Logs.fileline() + ' : RecordDet ERROR audit not found err=' + str(err))
            return compose_ret('', Constants.cst_content_type_json, 404)

        Various.useLangDB()

        # Replace None by empty string
        for key, value in list(record.items()):
            if record[key] is None:
                record[key] = ''
            elif key == 'remise' and record[key]:
                record[key] = _(record[key].strip())

        if record['rec_date_receipt']:
            record['rec_date_receipt'] = datetime.strftime(record['rec_date_receipt'], Constants.cst_dt_HM)

        if record['date_prescription']:
            record['date_prescription'] = datetime.strftime(record['date_prescription'], Constants.cst_isodate)

        if record['rec_parcel_date']:
            record['rec_parcel_date'] = datetime.strftime(record['rec_parcel_date'], Constants.cst_dt_HM)

        if record['date_hosp']:
            record['date_hosp'] = datetime.strftime(record['date_hosp'], Constants.cst_isodate)

        if record['rec_date_vld']:
            record['rec_date_vld'] = datetime.strftime(record['rec_date_vld'], Constants.cst_dt_HM)

        if record['rec_date_save']:
            record['rec_date_save'] = datetime.strftime(record['rec_date_save'], Constants.cst_dt_HM)

        # decimal number not serializable in JSON, convert except if empty string
        if record['prix']:
            record['prix'] = float(record['prix'])
        else:
            record['prix'] = 0

        if record['remise_pourcent']:
            record['remise_pourcent'] = float(record['remise_pourcent'])
        else:
            record['remise_pourcent'] = 0

        if record['assu_pourcent']:
            record['assu_pourcent'] = float(record['assu_pourcent'])
        else:
            record['assu_pourcent'] = 0

        if record['a_payer']:
            record['a_payer'] = float(record['a_payer'])
        else:
            record['a_payer'] = 0

        self.log.info(Logs.fileline() + ' : RecordDet id_rec=' + str(id_rec))
        try:
            details = {"result": "SUCCESS", "id_rec": int(id_rec)}
            Audit.insertAudit(audit_user, "RecordDet", "RECORD", int(id_rec), "SUCCESS", details, "R")
        except Exception as err:
            self.log.error(Logs.fileline() + ' : RecordDet ERROR audit success err=' + str(err))
        return compose_ret(record, Constants.cst_content_type_json, 200)

    @require_oauth()
    def post(self, id_rec=0):
        audit_user = request.oauth_user
        args = request.get_json(silent=True) or {}

        if int(id_rec) != 0:
            self.log.error(Logs.fileline() + ' : RecordDet ERROR update not supported')
            try:
                details = {"result": "ERROR", "reason": "UPDATE_NOT_SUPPORTED", "id_rec": int(id_rec)}
                Audit.insertAudit(audit_user, "RecordDet", "RECORD", int(id_rec), "ERROR", details, "U")
            except Exception as err:
                self.log.error(Logs.fileline() + ' : RecordDet ERROR audit update not supported err=' + str(err))
            return compose_ret('', Constants.cst_content_type_json, 405)

        if 'id_owner' not in args or 'type' not in args or 'date_record' not in args or 'id_med' not in args or \
           'date_prescr' not in args or 'service_int' not in args or 'bed_num' not in args or 'parcel_id' not in args or \
           'parcel_date' not in args or 'comm' not in args or 'parcel' not in args or 'date_hosp' not in args or \
           'price' not in args or 'discount' not in args or 'percent_discount' not in args or \
           'percent_insurance' not in args or 'bill_remain' not in args or 'receipt_num' not in args or \
           'bill_num' not in args or 'stat' not in args or 'id_patient' not in args or 'rec_custody' not in args or \
           'rec_num_int' not in args or 'rec_modified' not in args or 'rec_hosp_num' not in args:
            self.log.error(Logs.fileline() + ' : RecordDet ERROR args missing')
            try:
                details = {"result": "ERROR", "reason": "ARGS_MISSING", "id_rec": int(id_rec)}
                Audit.insertAudit(audit_user, "RecordDet", "RECORD", int(id_rec) if int(id_rec) > 0 else None, "ERROR", details, "C")
            except Exception as err:
                self.log.error(Logs.fileline() + ' : RecordDet ERROR audit args missing err=' + str(err))
            return compose_ret('', Constants.cst_content_type_json, 400)

        # Insert Record
        if id_rec == 0:
            args['date_record'] = datetime.strptime(args['date_record'], Constants.cst_dt_ext_HM)
            args['date_prescr'] = datetime.strptime(args['date_prescr'], Constants.cst_isodate)

            if args['parcel_date']:
                args['parcel_date'] = datetime.strptime(args['parcel_date'], Constants.cst_dt_ext_HM)

            if args['date_hosp']:
                args['date_hosp'] = datetime.strptime(args['date_hosp'], Constants.cst_isodate)

            # Increases num_dos_jour, num_dos_an and num_dos_mois
            # num_dos_jour = yyyymmddXXXX +1 if same day
            # num_dos_mois = yyyymmXXXX   +1 if same month
            # num_dos_an   = yyyyXXXXXX   +1 if same year

            num_dos = Various.getLastNumDos()

            if not num_dos:
                self.log.error(Logs.fileline() + ' : RecordDet num_dos not found, first num_dos')
                date_now = datetime.now().strftime("%Y%m%d")
                num_dos = {}
                num_dos['num_dos_jour'] = date_now + '0000'
                num_dos['num_dos_mois'] = date_now[:6] + '0000'
                num_dos['num_dos_an']   = date_now[:4] + '000000'

            num_dos_jour = num_dos['num_dos_jour']
            num_dos_mois = num_dos['num_dos_mois']
            num_dos_an   = num_dos['num_dos_an']

            date_now = datetime.now().strftime("%Y%m%d")

            date_record = args['date_record'].strftime("%Y%m%d")

            # Different day so we start a new number
            if num_dos_jour[:8] != date_now:
                self.log.info(Logs.fileline() + ' : DEBUG RecordDet num_dos_jour [' + str(num_dos_jour[:8]) + '] != date_now [' + str(date_now) + ']')
                num_dos_jour = date_record + '0001'
            else:
                num_jour  = num_dos_jour[8:]
                num_jour  = int(num_jour)
                num_jour += 1
                num_jour  = str(num_jour).rjust(4, '0')

                num_dos_jour = date_record + num_jour

            # Different month so we start a new number
            if num_dos_mois[:6] != date_now[:6]:
                self.log.info(Logs.fileline() + ' : DEBUG RecordDet num_dos_mois [' + str(num_dos_mois[:6]) + '] != date_now [' + str(date_now) + ']')
                num_dos_mois = date_record[:6] + '0001'
            else:
                num_mois  = num_dos_mois[6:]
                num_mois  = int(num_mois)
                num_mois += 1
                num_mois  = str(num_mois).rjust(4, '0')

                num_dos_mois = date_record[:6] + num_mois

            # Different year so we start a new number
            if num_dos_an[:4] != date_now[:4]:
                self.log.info(Logs.fileline() + ' : DEBUG RecordDet num_dos_an [' + str(num_dos_an[:4]) + '] != date_now[' + str(date_now) + ']')
                num_dos_an = date_record[:4] + '000001'
            else:
                num_an  = num_dos_an[4:]
                num_an  = int(num_an)
                num_an += 1
                num_an  = str(num_an).rjust(6, '0')

                num_dos_an = date_record[:4] + num_an

            ret = Record.insertRecord(id_owner=args['id_owner'],
                                      id_patient=args['id_patient'],
                                      type=args['type'],
                                      rec_date_receipt=args['date_record'],
                                      num_dos_jour=num_dos_jour,
                                      num_dos_an=num_dos_an,
                                      med_prescripteur=args['id_med'],
                                      date_prescription=args['date_prescr'],
                                      service_interne=args['service_int'],
                                      num_lit=args['bed_num'],
                                      id_colis=args['parcel_id'],
                                      rec_parcel_date=args['parcel_date'],
                                      rc=args['comm'],
                                      colis=args['parcel'],
                                      prix=args['price'],
                                      remise=args['discount'],
                                      remise_pourcent=args['percent_discount'],
                                      assu_pourcent=args['percent_insurance'],
                                      a_payer=args['bill_remain'],
                                      num_quittance=args['receipt_num'],
                                      num_fact=args['bill_num'],
                                      statut=args['stat'],
                                      num_dos_mois=num_dos_mois,
                                      date_hosp=args['date_hosp'],
                                      rec_custody=args['rec_custody'],
                                      rec_num_int=args['rec_num_int'],
                                      rec_modified=args['rec_modified'],
                                      rec_hosp_num=args['rec_hosp_num'])

            if ret <= 0:
                self.log.error(Logs.alert() + ' : RecordDet ERROR  insert')
                try:
                    details = {"result": "ERROR", "reason": "INSERT_RECORD_FAILED", "id_rec": int(id_rec),
                               "id_owner": args.get("id_owner"), "id_patient": args.get("id_patient"),
                               "type": args.get("type"), "stat": args.get("stat")}
                    Audit.insertAudit(audit_user, "RecordDet", "RECORD", int(id_rec) if int(id_rec) > 0 else None, "ERROR", details, "C")
                except Exception as err:
                    self.log.error(Logs.fileline() + ' : RecordDet ERROR audit insertRecord err=' + str(err))
                return compose_ret('', Constants.cst_content_type_json, 500)

            res = {}
            res['id_rec'] = ret

            # insert in sigl_pj_sequence num_dos_jour
            pattern = num_dos_jour[:8] + "%04d"  # make pattern for table
            end_num = int(num_dos_jour[8:])      # get end number without 0
            ret = Record.insertPjSequence("numdosjour", pattern, end_num)

            if ret <= 0:
                self.log.error(Logs.alert() + ' : RecordDet ERROR insertPjSequence numdosjour')

            # insert in sigl_pj_sequence num_dos_an
            pattern = num_dos_an[:4] + "%06d"
            end_num = int(num_dos_an[4:])
            ret = Record.insertPjSequence("numdosan", pattern, end_num)

            if ret <= 0:
                self.log.error(Logs.alert() + ' : RecordDet ERROR insertPjSequence numdosan')

            # insert in sigl_pj_sequence num_dos_mois
            pattern = num_dos_mois[:6] + "%04d"
            end_num = int(num_dos_mois[6:])
            ret = Record.insertPjSequence("numdosmois", pattern, end_num)

            if ret <= 0:
                self.log.error(Logs.alert() + ' : RecordDet ERROR insertPjSequence numdosmois')

        self.log.info(Logs.fileline() + ' : TRACE RecordDet id_rec=' + str(res['id_rec']))
        try:
            details = {"result": "SUCCESS", "id_rec": int(res.get("id_rec") or 0),
                       "id_owner": args.get("id_owner"), "id_patient": args.get("id_patient"),
                       "type": args.get("type"), "stat": args.get("stat"),
                       "num_dos_jour": num_dos_jour, "num_dos_mois": num_dos_mois, "num_dos_an": num_dos_an}
            Audit.insertAudit(audit_user, "RecordDet", "RECORD", int(res.get("id_rec") or 0), "SUCCESS", details, "C")
        except Exception as err:
            self.log.error(Logs.fileline() + ' : RecordDet ERROR audit success err=' + str(err))
        return compose_ret(res, Constants.cst_content_type_json)

    @require_oauth()
    def delete(self, id_rec):
        audit_user = request.oauth_user
        # delete sigl_11_data with id_dos = id_rec
        ret = File.deleteFileReportByRecord(id_rec)

        if not ret:
            self.log.error(Logs.fileline() + ' : TRACE RecordDet delete FileReport ERROR')
            try:
                details = {"result": "ERROR", "reason": "DELETE_FILE_REPORT_FAILED", "id_rec": int(id_rec)}
                Audit.insertAudit(audit_user, "RecordDetDelete", "RECORD", int(id_rec), "ERROR", details, "D")
            except Exception as err:
                self.log.error(Logs.fileline() + ' : RecordDet delete ERROR audit FileReport err=' + str(err))
            return compose_ret('', Constants.cst_content_type_json, 500)

        # delete sigl_dos_valisedoc__file_data with id_ext = id_rec
        ret = File.deleteFileDocByRecord(id_rec)

        if not ret:
            self.log.error(Logs.fileline() + ' : TRACE RecordDet delete FileDoc ERROR')
            try:
                details = {"result": "ERROR", "reason": "DELETE_FILE_DOC_FAILED", "id_rec": int(id_rec)}
                Audit.insertAudit(audit_user, "RecordDetDelete", "RECORD", int(id_rec), "ERROR", details, "D")
            except Exception as err:
                self.log.error(Logs.fileline() + ' : RecordDet delete ERROR audit FileDoc err=' + str(err))
            return compose_ret('', Constants.cst_content_type_json, 500)

        # load result requested with id_rec to get list of id_data
        l_res = Result.getResultRecord(id_rec)

        for res in l_res:
            # delete sigl_10_data with id_resultat = id_data list
            ret = Result.deleteValidationByResult(res['id_res'])

            if not ret:
                self.log.error(Logs.fileline() + ' : TRACE RecordDet delete Validation ERROR')
                try:
                    details = {"result": "ERROR", "reason": "DELETE_VALIDATION_FAILED", "id_rec": int(id_rec)}
                    Audit.insertAudit(audit_user, "RecordDetDelete", "RECORD", int(id_rec), "ERROR", details, "D")
                except Exception as err:
                    self.log.error(Logs.fileline() + ' : RecordDet delete ERROR audit validation err=' + str(err))
                return compose_ret('', Constants.cst_content_type_json, 500)

            # delete sigl_09_data with id_resultat = id_res
            ret = Result.deleteResult(res['id_res'])

            if not ret:
                self.log.error(Logs.fileline() + ' : TRACE RecordDet delete Result ERROR')
                try:
                    details = {"result": "ERROR", "reason": "DELETE_RESULT_FAILED", "id_rec": int(id_rec)}
                    Audit.insertAudit(audit_user, "RecordDetDelete", "RECORD", int(id_rec), "ERROR", details, "D")
                except Exception as err:
                    self.log.error(Logs.fileline() + ' : RecordDet delete ERROR audit Result err=' + str(err))
                return compose_ret('', Constants.cst_content_type_json, 500)

        # delete sigl_04_data with id_dos = id_rec
        ret = Analysis.deleteAnalysisByRecord(id_rec)

        if not ret:
            self.log.error(Logs.fileline() + ' : TRACE RecordDet delete Analysis ERROR')
            try:
                details = {"result": "ERROR", "reason": "DELETE_ANALYSIS_FAILED", "id_rec": int(id_rec)}
                Audit.insertAudit(audit_user, "RecordDetDelete", "RECORD", int(id_rec), "ERROR", details, "D")
            except Exception as err:
                self.log.error(Logs.fileline() + ' : RecordDet delete ERROR audit Analysis err=' + str(err))
            return compose_ret('', Constants.cst_content_type_json, 500)

        # delete sigl_01_data with id_dos = id_rec
        ret = Product.deleteProductByRecord(id_rec)

        if not ret:
            self.log.error(Logs.fileline() + ' : TRACE RecordDet delete Product ERROR')
            try:
                details = {"result": "ERROR", "reason": "DELETE_PRODUCT_FAILED", "id_rec": int(id_rec)}
                Audit.insertAudit(audit_user, "RecordDetDelete", "RECORD", int(id_rec), "ERROR", details, "D")
            except Exception as err:
                self.log.error(Logs.fileline() + ' : RecordDet delete ERROR audit Product err=' + str(err))
            return compose_ret('', Constants.cst_content_type_json, 500)

        # delete sigl_02_data with id_data = id_rec
        ret = Record.deleteRecord(id_rec)

        if not ret:
            self.log.error(Logs.fileline() + ' : TRACE RecordDet delete Record ERROR')
            try:
                details = {"result": "ERROR", "reason": "DELETE_RECORD_FAILED", "id_rec": int(id_rec)}
                Audit.insertAudit(audit_user, "RecordDetDelete", "RECORD", int(id_rec), "ERROR", details, "D")
            except Exception as err:
                self.log.error(Logs.fileline() + ' : RecordDet delete ERROR audit Record err=' + str(err))
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE RecordDet delete')
        try:
            details = {"result": "SUCCESS", "id_rec": int(id_rec)}
            Audit.insertAudit(audit_user, "RecordDetDelete", "RECORD", int(id_rec), "SUCCESS", details, "D")
        except Exception as err:
            self.log.error(Logs.fileline() + ' : RecordDet delete ERROR audit success err=' + str(err))
        return compose_ret('', Constants.cst_content_type_json)


class RecordDetFromExt(Resource):
    log = logging.getLogger('log_services')

    @require_oauth('external/record')
    def post(self, id_rec=0):
        self.log.info(Logs.fileline() + ' : RecordDetFromExt API access authorized')
        audit_user = request.oauth_user

        # Parse JSON body
        args = request.get_json(silent=True)
        if not args:
            self.log.error(Logs.alert() + ' : RecordDetFromExt ERROR JSON body missing')
            err = {"error": "JSON body required"}
            try:
                details = {"result": "ERROR", "reason": "JSON_BODY_MISSING"}
                Audit.insertAudit(audit_user, "RecordDetFromExt", "RECORD", None, "ERROR", details, "C")
            except Exception as err2:
                self.log.error(Logs.fileline() + ' : RecordDetFromExt ERROR audit json missing err=' + str(err2))
            return compose_ret(err, Constants.cst_content_type_json, 400)

        # --- DEFAULT VALUE ---
        price_act = Various.getDefaultValue('prix_acte')
        price_act = int(price_act['value'])  # > 0
        hosp_bill = Various.getDefaultValue('facturation_pat_hosp')
        hosp_bill = int(hosp_bill['value'])  # 1 or 0

        # --- PATIENT ---
        patient = args['patient']
        id_pat  = 0

        # check if patient exists by code
        pat = Patient.getPatientByCode(patient['pat_code'], patient['pat_code_lab'])

        if not pat:
            if not (patient['pat_name'] and patient['pat_firstname'] and patient['pat_sex']) and \
               not (patient['pat_birth'] or (not patient['pat_age'] and patient['pat_age_unit'])) and \
               patient['pat_anonymous'] == 'N':
                self.log.error(Logs.alert() + ' : RecordDetFromExt ERROR no patient indentity')
                err = {"error": "missing pat_name, pat_firstname, pat_sex, pat_birth or pat_age and pat_age_unit"}
                try:
                    details = {"result": "ERROR", "reason": "PATIENT_IDENTITY_MISSING"}
                    Audit.insertAudit(audit_user, "RecordDetFromExt", "PATIENT", None, "ERROR", details, "C")
                except Exception as err2:
                    self.log.error(Logs.fileline() + ' : RecordDetFromExt ERROR audit patient identity err=' + str(err2))
                return compose_ret(err, Constants.cst_content_type_json, 400)

            # check if patient exists by some infos
            pat = Patient.getPatientByIdentity(patient['pat_name'], patient['pat_firstname'],
                                               patient['pat_sex'], patient['pat_birth'],
                                               patient['pat_age'], patient['pat_age_unit'])

            if patient['pat_anonymous'] == 'Y':
                patient['pat_anonymous'] = 4
            else:
                patient['pat_anonymous'] = 5

            if patient['pat_date_approx'] == 'Y':
                patient['pat_date_approx'] = 4
            else:
                patient['pat_date_approx'] = 5

            if patient['pat_age_unit'] == 'D':
                patient['pat_age_unit'] = 1034
            elif patient['pat_age_unit'] == 'W':
                patient['pat_age_unit'] = 1035
            elif patient['pat_age_unit'] == 'M':
                patient['pat_age_unit'] = 1036
            else:
                patient['pat_age_unit'] = 1037

            if patient['pat_blood_group'] == 'A':
                patient['pat_blood_group'] = 901
            elif patient['pat_blood_group'] == 'B':
                patient['pat_blood_group'] = 902
            elif patient['pat_blood_group'] == 'AB':
                patient['pat_blood_group'] = 903
            elif patient['pat_blood_group'] == 'O':
                patient['pat_blood_group'] = 904
            else:
                patient['pat_blood_group'] = 0

            if patient['pat_blood_rhesus'] == '+':
                patient['pat_blood_rhesus'] = 232
            elif patient['pat_blood_rhesus'] == '-':
                patient['pat_blood_rhesus'] = 233
            else:
                patient['pat_blood_rhesus'] = 0

            if not pat:
                # generate a code
                patient['pat_code'] = Patient.newPatientCode()

                # insert new patient
                id_pat = Patient.insertPatient(id_owner=0,
                                               anonyme=patient['pat_anonymous'],
                                               code=patient['pat_code'],
                                               code_patient=patient['pat_code_lab'],
                                               nom=patient['pat_name'],
                                               prenom=patient['pat_firstname'],
                                               ddn=patient['pat_birth'],
                                               sexe=patient['pat_sex'],
                                               adresse=patient['pat_address'],
                                               cp=patient['pat_zipcode'],
                                               ville=patient['pat_city'],
                                               tel=patient['pat_phone1'],
                                               phone2=patient['pat_phone2'],
                                               profession=patient['pat_job'],
                                               nom_jf=patient['pat_maiden_name'],
                                               quartier=patient['pat_area'],
                                               bp=patient['pat_pbox'],
                                               ddn_approx=patient['pat_date_approx'],
                                               age=patient['pat_age'],
                                               unite=patient['pat_age_unit'],
                                               midname=patient['pat_middle_name'],
                                               nationality=patient['pat_nationality'],
                                               resident=patient['pat_resident'],
                                               blood_group=patient['pat_blood_group'],
                                               blood_rhesus=patient['pat_blood_rhesus'])

                if id_pat <= 0:
                    self.log.error(Logs.alert() + ' : RecordDetFromExt ERROR insertPatient')
                    err = {"error": "insertPatient SQL error"}
                    try:
                        details = {"result": "ERROR", "reason": "INSERT_PATIENT_FAILED",
                                   "pat_code": patient.get("pat_code"), "pat_code_lab": patient.get("pat_code_lab"),
                                   "pat_name": patient.get("pat_name"), "pat_firstname": patient.get("pat_firstname")}
                        Audit.insertAudit(audit_user, "RecordDetFromExt", "PATIENT", None, "ERROR", details, "C")
                    except Exception as err2:
                        self.log.error(Logs.fileline() + ' : RecordDetFromExt ERROR audit insert patient err=' + str(err2))
                    return compose_ret(err, Constants.cst_content_type_json, 500)
        else:
            id_pat = pat['id_data']

        # --- PRESCRIBER ---
        doctor = args['prescriber']
        id_doc = 0

        # check if doctor exists by code
        doc = Doctor.getDoctorByCode(doctor['prescr_code'])

        if not doc:
            if doctor['prescr_name'] and doctor['prescr_firstname']:
                # check if doctor exists by some infos
                doc = Doctor.getDoctorByIdentity(doctor['prescr_name'], doctor['prescr_firstname'])

                if doctor['prescr_title'] == 'MA':
                    doctor['prescr_title'] = 261
                elif doctor['prescr_title'] == 'SI':
                    doctor['prescr_title'] = 260
                elif doctor['prescr_title'] == 'MI':
                    doctor['prescr_title'] = 262
                elif doctor['prescr_title'] == 'DO':
                    doctor['prescr_title'] = 263
                elif doctor['prescr_title'] == 'PR':
                    doctor['prescr_title'] = 264
                else:
                    doctor['prescr_title'] = 0

                if doctor['prescr_spe'] == 'ALL':
                    doctor['prescr_spe'] = 186
                elif doctor['prescr_spe'] == 'ANDR':
                    doctor['prescr_spe'] = 187
                elif doctor['prescr_spe'] == 'ANAT':
                    doctor['prescr_spe'] = 189
                elif doctor['prescr_spe'] == 'ANES':
                    doctor['prescr_spe'] = 190
                elif doctor['prescr_spe'] == 'CANC':
                    doctor['prescr_spe'] = 192
                elif doctor['prescr_spe'] == 'CARD':
                    doctor['prescr_spe'] = 193
                elif doctor['prescr_spe'] == 'SURG':
                    doctor['prescr_spe'] = 194
                elif doctor['prescr_spe'] == 'DERM':
                    doctor['prescr_spe'] = 195
                elif doctor['prescr_spe'] == 'ENDO':
                    doctor['prescr_spe'] = 196
                elif doctor['prescr_spe'] == 'GAST':
                    doctor['prescr_spe'] = 197
                elif doctor['prescr_spe'] == 'GENE':
                    doctor['prescr_spe'] = 198
                elif doctor['prescr_spe'] == 'GERA':
                    doctor['prescr_spe'] = 199
                elif doctor['prescr_spe'] == 'GYNE':
                    doctor['prescr_spe'] = 200
                elif doctor['prescr_spe'] == 'HEMA':
                    doctor['prescr_spe'] = 201
                elif doctor['prescr_spe'] == 'INF':
                    doctor['prescr_spe'] = 202
                elif doctor['prescr_spe'] == 'GEN':
                    doctor['prescr_spe'] = 204
                elif doctor['prescr_spe'] == 'EMER':
                    doctor['prescr_spe'] = 205
                elif doctor['prescr_spe'] == 'NUTR':
                    doctor['prescr_spe'] = 207
                elif doctor['prescr_spe'] == 'NEPH':
                    doctor['prescr_spe'] = 208
                elif doctor['prescr_spe'] == 'ONCO':
                    doctor['prescr_spe'] = 211
                elif doctor['prescr_spe'] == 'OPHT':
                    doctor['prescr_spe'] = 212
                elif doctor['prescr_spe'] == 'OTO':
                    doctor['prescr_spe'] = 213
                elif doctor['prescr_spe'] == 'PEDI':
                    doctor['prescr_spe'] = 215
                elif doctor['prescr_spe'] == 'CHPS':
                    doctor['prescr_spe'] = 216
                elif doctor['prescr_spe'] == 'PSY':
                    doctor['prescr_spe'] = 217
                elif doctor['prescr_spe'] == 'RADIO':
                    doctor['prescr_spe'] = 219
                elif doctor['prescr_spe'] == 'RHEU':
                    doctor['prescr_spe'] = 220
                elif doctor['prescr_spe'] == 'DENT':
                    doctor['prescr_spe'] = 225
                elif doctor['prescr_spe'] == 'UROL':
                    doctor['prescr_spe'] = 222
                elif doctor['prescr_spe'] == 'ORTH':
                    doctor['prescr_spe'] = 1006
                elif doctor['prescr_spe'] == 'NURS':
                    doctor['prescr_spe'] = 1007
                elif doctor['prescr_spe'] == 'MIDW':
                    doctor['prescr_spe'] = 1008
                elif doctor['prescr_spe'] == 'PULM':
                    doctor['prescr_spe'] = 1009
                elif doctor['prescr_spe'] == 'INT':
                    doctor['prescr_spe'] = 1010
                else:
                    doctor['prescr_spe'] = 0

                if not doc:
                    id_doc = Doctor.insertDoctor(id_owner=0,
                                                 code=doctor['prescr_code'],
                                                 nom=doctor['prescr_name'],
                                                 prenom=doctor['prescr_firstname'],
                                                 ville=doctor['prescr_city'],
                                                 facility=doctor['prescr_workplace'],
                                                 specialite=doctor['prescr_spe'],
                                                 tel=doctor['prescr_phone'],
                                                 email=doctor['prescr_email'],
                                                 titre=doctor['prescr_title'],
                                                 initiale=doctor['prescr_initial'],
                                                 service=doctor['prescr_service'],
                                                 adresse=doctor['prescr_address'],
                                                 mobile=doctor['prescr_mobile'],
                                                 fax=doctor['prescr_fax'],
                                                 zipcity=doctor['prescr_zipcode'])

                    if id_doc <= 0:
                        self.log.error(Logs.alert() + ' : RecordDetFromExt ERROR insertDoctor')
                        err = {"error": "insertDoctor SQL error"}
                        try:
                            details = {"result": "ERROR", "reason": "INSERT_DOCTOR_FAILED",
                                       "prescr_code": doctor.get("prescr_code")}
                            Audit.insertAudit(audit_user, "RecordDetFromExt", "DOCTOR", None, "ERROR", details, "C")
                        except Exception as err2:
                            self.log.error(Logs.fileline() + ' : RecordDetFromExt ERROR audit insert doctor err=' + str(err2))
                        return compose_ret(err, Constants.cst_content_type_json, 500)
        else:
            id_doc = doc['id_data']

        # --- RECORD ---
        record = args['record']
        id_rec = 0

        if not (record['rec_type'] and record['rec_date'] and record['rec_date_prescr']):
            self.log.error(Logs.alert() + ' : RecordDetFromExt ERROR record missing args')
            err = {"error": "missing rec_type, rec_date or rec_date_prescr"}
            try:
                details = {"result": "ERROR", "reason": "RECORD_ARGS_MISSING"}
                Audit.insertAudit(audit_user, "RecordDetFromExtInsertRecord", "RECORD", None, "ERROR", details, "C")
            except Exception as err:
                self.log.error(Logs.fileline() + ' : RecordDetFromExt ERROR audit insert record err=' + str(err))
            return compose_ret(err, Constants.cst_content_type_json, 400)

        rec_parcel = 5  # No

        if record['rec_parcel_id'] or record['rec_parcel_date']:
            rec_parcel = 4  # Yes

        # Increases num_dos_jour, num_dos_an and num_dos_mois
        # num_dos_jour = yyyymmddXXXX +1 if same day
        # num_dos_mois = yyyymmXXXX   +1 if same month
        # num_dos_an   = yyyyXXXXXX   +1 if same year

        num_dos = Various.getLastNumDos()

        if not num_dos:
            self.log.info(Logs.fileline() + ' : RecordDetFromExt num_dos not found, first num_dos')
            date_now = datetime.now().strftime("%Y%m%d")
            num_dos = {}
            num_dos['num_dos_jour'] = date_now + '0000'
            num_dos['num_dos_mois'] = date_now[:6] + '0000'
            num_dos['num_dos_an']   = date_now[:4] + '000000'

        num_dos_jour = num_dos['num_dos_jour']
        num_dos_mois = num_dos['num_dos_mois']
        num_dos_an   = num_dos['num_dos_an']

        date_now = datetime.now().strftime("%Y%m%d")

        date_record = datetime.strptime(record['rec_date'][:16], Constants.cst_dt_ext_HM)
        date_record = date_record.strftime("%Y%m%d")

        # Different day so we start a new number
        if num_dos_jour[:8] != date_now:
            self.log.info(Logs.fileline() + ' : DEBUG RecordDetFromExt num_dos_jour [' + str(num_dos_jour[:8]) + '] != date_now [' + str(date_now) + ']')
            num_dos_jour = date_record + '0001'
        else:
            num_jour  = num_dos_jour[8:]
            num_jour  = int(num_jour)
            num_jour += 1
            num_jour  = str(num_jour).rjust(4, '0')

            num_dos_jour = date_record + num_jour

        # Different month so we start a new number
        if num_dos_mois[:6] != date_now[:6]:
            self.log.info(Logs.fileline() + ' : DEBUG RecordDetFromExt num_dos_mois [' + str(num_dos_mois[:6]) + '] != date_now [' + str(date_now) + ']')
            num_dos_mois = date_record[:6] + '0001'
        else:
            num_mois  = num_dos_mois[6:]
            num_mois  = int(num_mois)
            num_mois += 1
            num_mois  = str(num_mois).rjust(4, '0')

            num_dos_mois = date_record[:6] + num_mois

        # Different year so we start a new number
        if num_dos_an[:4] != date_now[:4]:
            self.log.info(Logs.fileline() + ' : DEBUG RecordDetFromExt num_dos_an [' + str(num_dos_an[:4]) + '] != date_now[' + str(date_now) + ']')
            num_dos_an = date_record[:4] + '000001'
        else:
            num_an  = num_dos_an[4:]
            num_an  = int(num_an)
            num_an += 1
            num_an  = str(num_an).rjust(6, '0')

            num_dos_an = date_record[:4] + num_an

        if record['rec_invoice_discount'] == 'S':
            record['rec_invoice_discount'] = 267
        elif record['rec_invoice_discount'] == 'E':
            record['rec_invoice_discount'] = 268
        elif record['rec_invoice_discount'] == 'O':
            record['rec_invoice_discount'] = 269
        else:
            record['rec_invoice_discount'] = 0

        if record['rec_type'] == 'I':
            record['rec_type'] = 184
        else:
            record['rec_type'] = 183

        id_rec = Record.insertRecord(id_owner=0,
                                     id_patient=id_pat,
                                     type=record['rec_type'],
                                     rec_date_receipt=record['rec_date'][:16],
                                     num_dos_jour=num_dos_jour,
                                     num_dos_an=num_dos_an,
                                     med_prescripteur=id_doc,
                                     date_prescription=record['rec_date_prescr'],
                                     service_interne=record['rec_int_service'],
                                     num_lit=record['rec_bed_num'],
                                     id_colis=record['rec_parcel_id'],
                                     rec_parcel_date=record['rec_parcel_date'],
                                     rc=record['rec_comm'],
                                     colis=rec_parcel,
                                     prix=0,
                                     remise=record['rec_invoice_discount'],
                                     remise_pourcent=record['rec_percent_discount'],
                                     assu_pourcent=record['rec_insurance_cover'],
                                     a_payer=0,
                                     num_quittance=record['rec_receipt_num'],
                                     num_fact='',
                                     statut=181,
                                     num_dos_mois=num_dos_mois,
                                     date_hosp=record['rec_date_hosp'],
                                     rec_custody=record['rec_custody'],
                                     rec_num_int=record['rec_num_int'],
                                     rec_modified='N',
                                     rec_hosp_num=record['rec_hosp_num'])

        if id_rec <= 0:
            self.log.error(Logs.alert() + ' : RecordDetFromExt ERROR insertRecord')
            err = {"error": "insertRecord SQL error"}
            try:
                details = {"result": "ERROR", "reason": "INSERT_RECORD_FAILED"}
                Audit.insertAudit(audit_user, "RecordDetFromExt", "RECORD", None, "ERROR", details, "C")
            except Exception as err2:
                self.log.error(Logs.fileline() + ' : RecordDetFromExt ERROR audit insert record err=' + str(err2))
            return compose_ret(err, Constants.cst_content_type_json, 500)

        # insert in sigl_pj_sequence num_dos_jour
        pattern = num_dos_jour[:8] + "%04d"  # make pattern for table
        end_num = int(num_dos_jour[8:])      # get end number without 0
        ret = Record.insertPjSequence("numdosjour", pattern, end_num)

        if ret <= 0:
            self.log.error(Logs.alert() + ' : RecordDetFromExt ERROR insertPjSequence numdosjour')

        # insert in sigl_pj_sequence num_dos_an
        pattern = num_dos_an[:4] + "%06d"
        end_num = int(num_dos_an[4:])
        ret = Record.insertPjSequence("numdosan", pattern, end_num)

        if ret <= 0:
            self.log.error(Logs.alert() + ' : RecordDetFromExt ERROR insertPjSequence numdosan')

        # insert in sigl_pj_sequence num_dos_mois
        pattern = num_dos_mois[:6] + "%04d"
        end_num = int(num_dos_mois[6:])
        ret = Record.insertPjSequence("numdosmois", pattern, end_num)

        if ret <= 0:
            self.log.error(Logs.alert() + ' : RecordDetFromExt ERROR insertPjSequence numdosmois')

        # --- ANALYSIS ---
        l_ana       = args['ana_list']
        l_ana_code  = []
        l_id_act    = []
        l_samp      = args['samp_list']
        l_type_prel = []

        tot_price = 0

        for ana in l_ana:
            if ana.get('ana_code'):
                l_ana_code.append(ana['ana_code'])

        # make list of (ana_code,type_prel) from l_samp
        for samp in l_samp:
            # check if samp_ana in l_ana_code
            if samp['samp_ana'] in l_ana_code:
                if samp['samp_type'] == 'APF':
                    elem = (samp['samp_code'], 102)
                elif samp['samp_type'] == 'APFL':
                    elem = (samp['samp_code'], 35)
                elif samp['samp_type'] == 'BAL':
                    elem = (samp['samp_code'], 56)
                elif samp['samp_type'] == 'BIO':
                    elem = (samp['samp_code'], 38)
                elif samp['samp_type'] == 'BLD':
                    elem = (samp['samp_code'], 138)
                elif samp['samp_type'] == 'BPF':
                    elem = (samp['samp_code'], 100)
                elif samp['samp_type'] == 'CSF':
                    elem = (samp['samp_code'], 99)
                elif samp['samp_type'] == 'DW':
                    elem = (samp['samp_code'], 1014)
                elif samp['samp_type'] == 'GS':
                    elem = (samp['samp_code'], 1000)
                elif samp['samp_type'] == 'JPFL':
                    elem = (samp['samp_code'], 34)
                elif samp['samp_type'] == 'OTH':
                    elem = (samp['samp_code'], 163)
                elif samp['samp_type'] == 'PPF':
                    elem = (samp['samp_code'], 104)
                elif samp['samp_type'] == 'PS':
                    elem = (samp['samp_code'], 1189)
                elif samp['samp_type'] == 'SPUT':
                    elem = (samp['samp_code'], 50)
                elif samp['samp_type'] == 'STL':
                    elem = (samp['samp_code'], 141)
                elif samp['samp_type'] == 'SW':
                    elem = (samp['samp_code'], 1016)
                elif samp['samp_type'] == 'TS':
                    elem = (samp['samp_code'], 75)
                elif samp['samp_type'] == 'URN':
                    elem = (samp['samp_code'], 153)
                elif samp['samp_type'] == 'US':
                    elem = (samp['samp_code'], 152)
                elif samp['samp_type'] == 'VS':
                    elem = (samp['samp_code'], 162)
                elif samp['samp_type'] == 'WW':
                    elem = (samp['samp_code'], 1015)
                else:
                    self.log.error(Logs.alert() + ' : RecordDetFromExt ERROR samp_type does not match')
                    err = {"error": "samp_type does not match"}
                    try:
                        details = {"result": "ERROR", "reason": "SAMP_TYPE_MISMATCH", "id_rec": int(id_rec)}
                        Audit.insertAudit(audit_user, "RecordDetFromExt", "RECORD", int(id_rec), "ERROR", details, "C")
                    except Exception as err2:
                        self.log.error(Logs.fileline() + ' : RecordDetFromExt ERROR audit samp type mismatch err=' + str(err2))
                    return compose_ret(err, Constants.cst_content_type_json, 400)

                l_type_prel.append(elem)

        for ana in l_ana:
            if not ana['ana_code']:
                self.log.error(Logs.alert() + ' : RecordDetFromExt ERROR ana_list missing args')
                err = {"error": "missing ana_code"}
                try:
                    details = {"result": "ERROR", "reason": "ANA_CODE_MISSING", "id_rec": int(id_rec)}
                    Audit.insertAudit(audit_user, "RecordDetFromExt", "RECORD", int(id_rec), "ERROR", details, "C")
                except Exception as err2:
                    self.log.error(Logs.fileline() + ' : RecordDetFromExt ERROR audit ana_code missing err=' + str(err2))
                return compose_ret(err, Constants.cst_content_type_json, 400)

            tmp_ana = Analysis.getAnalysisByCode(ana['ana_code'])

            if not tmp_ana:
                self.log.error(Logs.alert() + ' : RecordDetFromExt ERROR analysis not found with code : ' + Logs.clean(ana['ana_code']))
                err = {"error": "analysis not found with code = " + str(ana['ana_code'])}
                try:
                    details = {"result": "ERROR", "reason": "ANALYSIS_NOT_FOUND", "ana_code": str(ana.get('ana_code')), "id_rec": int(id_rec)}
                    Audit.insertAudit(audit_user, "RecordDetFromExt", "RECORD", int(id_rec), "ERROR", details, "C")
                except Exception as err2:
                    self.log.error(Logs.fileline() + ' : RecordDetFromExt ERROR audit analysis not found err=' + str(err2))
                return compose_ret(err, Constants.cst_content_type_json, 404)

            # calc price
            ana_price = price_act * tmp_ana['cote_valeur']

            # No bill if internal record and hosp bill pref set to 0
            if record['rec_type'] == 'I' and not hosp_bill:
                ana_price = 0

            if ana['ana_emer'] == 'Y':
                ana['ana_emer'] = 4
            else:
                ana['ana_emer'] = 5

            if ana['ana_req'] == 'N':
                ana['ana_req'] = 5
            else:
                ana['ana_req'] = 4

            if ana['ana_out'] == 'Y':
                ana['ana_out'] = 4
            else:
                ana['ana_out'] = 5

            tot_price += ana_price

            id_req = Analysis.insertAnalysisReq(id_owner=0,
                                                id_dos=id_rec,
                                                ref_analyse=tmp_ana['id_data'],
                                                prix=ana_price,
                                                paye=5,  # TODO useless column ?
                                                urgent=ana['ana_emer'],
                                                demande=ana['ana_req'],
                                                outsourced=ana['ana_out'])

            if id_req <= 0:
                self.log.error(Logs.alert() + ' : RecordDetFromExt ERROR insertAnalysisReq')
                err = {"error": "insertAnalysisReq SQL error"}
                try:
                    details = {"result": "ERROR", "reason": "INSERT_ANALYSIS_REQ_FAILED", "id_rec": int(id_rec)}
                    Audit.insertAudit(audit_user, "RecordDetFromExt", "RECORD", int(id_rec), "ERROR", details, "C")
                except Exception as err2:
                    self.log.error(Logs.fileline() + ' : RecordDetFromExt ERROR audit insert analysis req err=' + str(err2))
                return compose_ret(err, Constants.cst_content_type_json, 500)

            # insert sampling act
            if tmp_ana['produit_biologique'] and tmp_ana['produit_biologique'] not in l_id_act:
                tmp_act = Analysis.getAnalysis(tmp_ana['produit_biologique'])

                if not tmp_ana:
                    self.log.error(Logs.alert() + ' : RecordDetFromExt ERROR sampling act associated to analysis not found with code : ' + Logs.clean(ana['ana_code']))
                    err = {"error": "sampling act associated to analysis not found with code = " + str(ana['ana_code'])}
                    return compose_ret(err, Constants.cst_content_type_json, 404)

                # calc price of this act
                ana_act_price = price_act * tmp_act['cote_valeur']

                # No bill if internal record and hosp bill pref set to 0
                if record['rec_type'] == 'I' and not hosp_bill:
                    ana_act_price = 0

                tot_price += ana_act_price

                id_act_req = Analysis.insertAnalysisReq(id_owner=0,
                                                        id_dos=id_rec,
                                                        ref_analyse=tmp_ana['produit_biologique'],
                                                        prix=ana_act_price,
                                                        paye=5,  # TODO useless column ?
                                                        urgent=5,
                                                        demande=4,
                                                        outsourced='N')

                if id_act_req <= 0:
                    self.log.error(Logs.alert() + ' : RecordDetFromExt ERROR insertAnalysisReq')
                    err = {"error": "insertAnalysisReq for sampling act SQL error"}
                    try:
                        details = {"result": "ERROR", "reason": "INSERT_ANALYSIS_REQ_FAILED", "id_rec": int(id_rec)}
                        Audit.insertAudit(audit_user, "RecordDetFromExt", "RECORD", int(id_rec), "ERROR", details, "C")
                    except Exception as err2:
                        self.log.error(Logs.fileline() + ' : RecordDetFromExt ERROR audit insert analysis req err=' + str(err2))
                    return compose_ret(err, Constants.cst_content_type_json, 500)

                l_id_act.append(tmp_ana['produit_biologique'])

            # insert defaut sample associated to sampling act if not already required by received data
            elem = (ana['ana_code'], tmp_ana['type_prel'])

            if tmp_ana['type_prel'] and elem not in l_type_prel:
                id_samp = Product.insertProductReq(id_owner=0,
                                                   samp_date='',
                                                   type_prel=elem[1],
                                                   samp_id_ana=tmp_ana['id_data'],
                                                   statut=9,
                                                   id_dos=id_rec,
                                                   preleveur='',
                                                   samp_receipt_date='',
                                                   commentaire='',
                                                   lieu_prel=0,
                                                   lieu_prel_plus='',
                                                   localisation='',
                                                   code=elem[0])

                if id_samp <= 0:
                    self.log.error(Logs.alert() + ' : RecordDetFromExt ERROR insertProduct')
                    err = {"error": "insertProduct SQL error"}
                    try:
                        details = {"result": "ERROR", "reason": "INSERT_PRODUCT_FAILED", "id_rec": int(id_rec)}
                        Audit.insertAudit(audit_user, "RecordDetFromExt", "RECORD", int(id_rec), "ERROR", details, "C")
                    except Exception as err2:
                        self.log.error(Logs.fileline() + ' : RecordDetFromExt ERROR audit insert product err=' + str(err2))
                    return compose_ret(err, Constants.cst_content_type_json, 500)

        # --- SAMPLE ---
        for samp in l_samp:
            # check if samp_ana in l_ana_code
            if samp['samp_ana'] in l_ana_code:
                tmp_ana = Analysis.getAnalysisByCode(samp['samp_ana'])

                if samp['samp_type'] == 'APF':
                    samp['samp_type'] = 102
                elif samp['samp_type'] == 'APFL':
                    samp['samp_type'] = 35
                elif samp['samp_type'] == 'BAL':
                    samp['samp_type'] = 56
                elif samp['samp_type'] == 'BIO':
                    samp['samp_type'] = 38
                elif samp['samp_type'] == 'BLD':
                    samp['samp_type'] = 138
                elif samp['samp_type'] == 'BPF':
                    samp['samp_type'] = 100
                elif samp['samp_type'] == 'CSF':
                    samp['samp_type'] = 99
                elif samp['samp_type'] == 'DW':
                    samp['samp_type'] = 1014
                elif samp['samp_type'] == 'GS':
                    samp['samp_type'] = 1000
                elif samp['samp_type'] == 'JPFL':
                    samp['samp_type'] = 34
                elif samp['samp_type'] == 'OTH':
                    samp['samp_type'] = 163
                elif samp['samp_type'] == 'PPF':
                    samp['samp_type'] = 104
                elif samp['samp_type'] == 'PS':
                    samp['samp_type'] = 1189
                elif samp['samp_type'] == 'SPUT':
                    samp['samp_type'] = 50
                elif samp['samp_type'] == 'STL':
                    samp['samp_type'] = 141
                elif samp['samp_type'] == 'SW':
                    samp['samp_type'] = 1016
                elif samp['samp_type'] == 'TS':
                    samp['samp_type'] = 75
                elif samp['samp_type'] == 'URN':
                    samp['samp_type'] = 153
                elif samp['samp_type'] == 'US':
                    samp['samp_type'] = 152
                elif samp['samp_type'] == 'VS':
                    samp['samp_type'] = 162
                elif samp['samp_type'] == 'WW':
                    samp['samp_type'] = 1015
                else:
                    self.log.error(Logs.alert() + ' : RecordDetFromExt ERROR samp_type does not match')
                    err = {"error": "samp_type does not match"}
                    try:
                        details = {"result": "ERROR", "reason": "SAMP_TYPE_MISMATCH", "ana_code": str(ana.get('samp_ana')), "id_rec": int(id_rec)}
                        Audit.insertAudit(audit_user, "RecordDetFromExt", "RECORD", int(id_rec), "ERROR", details, "C")
                    except Exception as err2:
                        self.log.error(Logs.fileline() + ' : RecordDetFromExt ERROR audit sampling act not found err=' + str(err2))
                    return compose_ret(err, Constants.cst_content_type_json, 400)

                if samp['samp_status'] == 'D':
                    samp['samp_status'] = 8
                elif samp['samp_status'] == 'P':
                    samp['samp_status'] = 10
                else:
                    samp['samp_status'] = 9

                id_samp = Product.insertProductReq(id_owner=0,
                                                   samp_date=samp['samp_date'],
                                                   type_prel=samp['samp_type'],
                                                   samp_id_ana=tmp_ana['id_data'],
                                                   statut=samp['samp_status'],
                                                   id_dos=id_rec,
                                                   preleveur=samp['samp_name'],
                                                   samp_receipt_date=samp['samp_date_receipt'],
                                                   commentaire=samp['samp_comm'],
                                                   lieu_prel=0,
                                                   lieu_prel_plus='',
                                                   localisation='',
                                                   code=samp['samp_code'])

                if id_samp <= 0:
                    self.log.error(Logs.alert() + ' : RecordDetFromExt ERROR insertProduct')
                    err = {"error": "insertProduct SQL error"}
                    try:
                        details = {"result": "ERROR", "reason": "INSERT_PRODUCT_FAILED", "id_rec": int(id_rec)}
                        Audit.insertAudit(audit_user, "RecordDetFromExt", "RECORD", int(id_rec), "ERROR", details, "C")
                    except Exception as err2:
                        self.log.error(Logs.fileline() + ' : RecordDetFromExt ERROR audit insert product err=' + str(err2))
                    return compose_ret(err, Constants.cst_content_type_json, 500)

        # update prix, a_payer after insert analysis and calculate tot_remain
        tot_remain = Decimal(tot_price)

        if record['rec_percent_discount']:
            tot_remain = tot_remain * (1 - Decimal(record['rec_percent_discount']) / 100)

        if record['rec_insurance_cover']:
            tot_remain = tot_remain * (1 - Decimal(record['rec_insurance_cover']) / 100)

        ret = Record.updateRecordBill(id_rec, tot_price, tot_remain)

        if not ret:
            self.log.error(Logs.fileline() + ' : RecordDetFromExt updateRecordBill ERROR')
            err = {"error": "updateRecordBill SQL error"}
            try:
                details = {"result": "ERROR", "reason": "UPDATE_RECORD_BILL_FAILED", "id_rec": int(id_rec)}
                Audit.insertAudit(audit_user, "RecordDetFromExt", "RECORD", int(id_rec), "ERROR", details, "C")
            except Exception as err2:
                self.log.error(Logs.fileline() + ' : RecordDetFromExt ERROR audit update bill err=' + str(err2))
            return compose_ret(err, Constants.cst_content_type_json, 500)

        # --- RESULT AND VALIDATION ---
        type_validation = 250  # Administrative validation

        l_ana = Analysis.getAnalysisReq(id_rec, 'A')

        if not l_ana:
            self.log.error(Logs.fileline() + ' : ' + 'RecordDetFromExt ERROR l_ana empty')
            err = {"error": "getAnalysisReq SQL error for create result entry"}
            try:
                details = {"result": "ERROR", "reason": "GET_ANALYSIS_REQ_FAILED", "id_rec": int(id_rec)}
                Audit.insertAudit(audit_user, "RecordDetFromExt", "RECORD", int(id_rec), "ERROR", details, "C")
            except Exception as err2:
                self.log.error(Logs.fileline() + ' : RecordDetFromExt ERROR audit get analysis req err=' + str(err2))
            return compose_ret(err, Constants.cst_content_type_json, 500)

        # Loop on list_ana
        for ana in l_ana:
            l_ref = Analysis.getRefVariable(ana['ref_analyse'])

            for ref in l_ref:
                if ref and ref['id_refvariable']:
                    ret = Result.insertResult(id_owner=0,
                                              id_analyse=ana['id_data'],
                                              ref_variable=ref['id_refvariable'],
                                              obligatoire=ref['obligatoire'])

                    if ret <= 0:
                        self.log.error(Logs.alert() + ' : RecordDetFromExt ERROR  insert result')
                        err = {"error": "insertResult SQL error"}
                        try:
                            details = {"result": "ERROR", "reason": "INSERT_RESULT_FAILED", "id_rec": int(id_rec)}
                            Audit.insertAudit(audit_user, "RecordDetFromExt", "RECORD", int(id_rec), "ERROR", details, "C")
                        except Exception as err2:
                            self.log.error(Logs.fileline() + ' : RecordDetFromExt ERROR audit insert result err=' + str(err2))
                        return compose_ret(err, Constants.cst_content_type_json, 500)

                    res = {}
                    res['id_res'] = ret

                    # insert corresponding validation
                    ret = Result.insertValidation(id_owner=0,
                                                  id_resultat=res['id_res'],
                                                  date_validation=datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S"),
                                                  utilisateur=0,
                                                  valeur=None,
                                                  type_validation=type_validation,
                                                  commentaire=None,
                                                  motif_annulation=None)

                    if ret <= 0:
                        self.log.error(Logs.alert() + ' : RecordDetFromExt ERROR  insert validation')
                        err = {"error": "insertValidation SQL error"}
                        try:
                            details = {"result": "ERROR", "reason": "INSERT_VALIDATION_FAILED", "id_rec": int(id_rec)}
                            Audit.insertAudit(audit_user, "RecordDetFromExt", "RECORD", int(id_rec), "ERROR", details, "C")
                        except Exception as err2:
                            self.log.error(Logs.fileline() + ' : RecordDetFromExt ERROR audit insert validation err=' + str(err2))
                        return compose_ret(err, Constants.cst_content_type_json, 500)

        # update status of record an date of validation
        ret = Record.updateRecordStat(id_rec, 182)

        if not ret:
            self.log.error(Logs.fileline() + ' : RecordDetFromExt ERROR RecordStat update')
            err = {"error": "updateRecordStat SQL error"}
            try:
                details = {"result": "ERROR", "reason": "UPDATE_RECORD_STAT_FAILED", "id_rec": int(id_rec)}
                Audit.insertAudit(audit_user, "RecordDetFromExt", "RECORD", int(id_rec), "ERROR", details, "U")
            except Exception as err2:
                self.log.error(Logs.fileline() + ' : RecordDetFromExt ERROR audit update stat err=' + str(err2))
            return compose_ret(err, Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE RecordDetFromExt')
        try:
            details = {"result": "SUCCESS", "id_rec": int(id_rec),
                       "num_dos_jour": num_dos_jour, "num_dos_mois": num_dos_mois, "num_dos_an": num_dos_an}
            Audit.insertAudit(audit_user, "RecordDetFromExt", "RECORD", int(id_rec), "SUCCESS", details, "C")
        except Exception as err2:
            self.log.error(Logs.fileline() + ' : RecordDetFromExt ERROR audit success err=' + str(err2))
        return compose_ret(id_rec, Constants.cst_content_type_json, 200)


class RecordComm(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self, id_rec):
        audit_user = request.oauth_user
        args = request.get_json()

        if 'comm' not in args:
            self.log.error(Logs.fileline() + ' : RecordComm ERROR args missing')
            try:
                details = {"result": "ERROR", "reason": "ARGS_MISSING", "missing": ["comm"], "id_rec": int(id_rec)}
                Audit.insertAudit(audit_user, "RecordComm", "RECORD", int(id_rec), "ERROR", details, "U")
            except Exception as err:
                self.log.error(Logs.fileline() + ' : RecordComm ERROR audit args missing err=' + str(err))
            return compose_ret('', Constants.cst_content_type_json, 400)

        ret = Record.updateRecordComm(id_rec, args['comm'])

        if not ret:
            self.log.error(Logs.fileline() + ' : ERROR RecordComm update')
            try:
                details = {"result": "ERROR", "reason": "UPDATE_RECORD_COMM_FAILED", "id_rec": int(id_rec)}
                Audit.insertAudit(audit_user, "RecordComm", "RECORD", int(id_rec), "ERROR", details, "U")
            except Exception as err:
                self.log.error(Logs.fileline() + ' : RecordComm ERROR audit update err=' + str(err))
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE RecordComm')
        try:
            details = {"result": "SUCCESS", "id_rec": int(id_rec)}
            Audit.insertAudit(audit_user, "RecordComm", "RECORD", int(id_rec), "SUCCESS", details, "U")
        except Exception as err:
            self.log.error(Logs.fileline() + ' : RecordComm ERROR audit success err=' + str(err))
        return compose_ret('', Constants.cst_content_type_json)


class RecordLast(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self):
        audit_user = request.oauth_user
        record = Record.getLastRecord()

        if not record:
            self.log.error(Logs.fileline() + ' : ' + 'RecordLast ERROR not found')
            try:
                details = {"result": "ERROR", "reason": "NOT_FOUND"}
                Audit.insertAudit(audit_user, "RecordLast", "RECORD", None, "ERROR", details, "R")
            except Exception as err:
                self.log.error(Logs.fileline() + ' : RecordLast ERROR audit not found err=' + str(err))
            return compose_ret('', Constants.cst_content_type_json, 404)

        # Replace None by empty string
        for key, value in list(record.items()):
            if record[key] is None:
                record[key] = ''

        if record['rec_date_receipt']:
            record['rec_date_receipt'] = datetime.strftime(record['rec_date_receipt'], Constants.cst_dt_HM)

        if record['date_prescription']:
            record['date_prescription'] = datetime.strftime(record['date_prescription'], Constants.cst_isodate)

        if record['rec_parcel_date']:
            record['rec_parcel_date'] = datetime.strftime(record['rec_parcel_date'], Constants.cst_dt_HM)

        if record['rec_date_save']:
            record['rec_date_save'] = datetime.strftime(record['rec_date_save'], Constants.cst_dt_HM)

        if record['date_hosp']:
            record['date_hosp'] = datetime.strftime(record['date_hosp'], Constants.cst_isodate)

        # decimal number not serializable in JSON, convert except if empty string
        if record['prix']:
            record['prix'] = float(record['prix'])
        else:
            record['prix'] = 0

        if record['remise_pourcent']:
            record['remise_pourcent'] = float(record['remise_pourcent'])
        else:
            record['remise_pourcent'] = 0

        if record['assu_pourcent']:
            record['assu_pourcent'] = float(record['assu_pourcent'])
        else:
            record['assu_pourcent'] = 0

        if record['a_payer']:
            record['a_payer'] = float(record['a_payer'])
        else:
            record['a_payer'] = 0

        self.log.info(Logs.fileline() + ' : RecordLast')
        try:
            id_rec = record.get("id_rec")
            details = {"result": "SUCCESS", "id_rec": int(id_rec) if id_rec else None}
            Audit.insertAudit(audit_user, "RecordLast", "RECORD", int(id_rec) if id_rec else None, "SUCCESS", details, "R")
        except Exception as err:
            self.log.error(Logs.fileline() + ' : RecordLast ERROR audit success err=' + str(err))
        return compose_ret(record, Constants.cst_content_type_json, 200)


class RecordFile(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self, id_rec):
        audit_user = request.oauth_user
        l_files = Record.getRecordFile(id_rec)

        if not l_files:
            self.log.error(Logs.fileline() + ' : TRACE RecordFile not found')

        for files in l_files:
            # Replace None by empty string
            for key, value in list(files.items()):
                if files[key] is None:
                    files[key] = ''

        self.log.info(Logs.fileline() + ' : TRACE RecordFile')
        try:
            details = {"result": "SUCCESS", "id_rec": int(id_rec), "count": len(l_files) if l_files else 0}
            Audit.insertAudit(audit_user, "RecordFile", "RECORD", int(id_rec), "SUCCESS", details, "R")
        except Exception as err:
            self.log.error(Logs.fileline() + ' : RecordFile ERROR audit success err=' + str(err))
        return compose_ret(l_files, Constants.cst_content_type_json)


class RecordNext(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self, id_rec):
        audit_user = request.oauth_user
        id_rec_next = 0

        rec = Record.getRecordNext(id_rec)

        if not rec:
            self.log.error(Logs.fileline() + ' : TRACE RecordNext not found')
        else:
            id_rec_next = rec['id_data']

        self.log.info(Logs.fileline() + ' : TRACE RecordNext')
        try:
            details = {"result": "SUCCESS", "id_rec": int(id_rec)}
            Audit.insertAudit(audit_user, "RecordNext", "RECORD", int(id_rec), "SUCCESS", details, "R")
        except Exception as err:
            self.log.error(Logs.fileline() + ' : RecordNext ERROR audit success err=' + str(err))
        return compose_ret(id_rec_next, Constants.cst_content_type_json)


class RecordStat(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self, id_rec):
        audit_user = request.oauth_user
        args = request.get_json()

        if 'stat' not in args:
            self.log.error(Logs.fileline() + ' : RecordStat ERROR args missing')
            try:
                details = {"result": "ERROR", "reason": "ARGS_MISSING", "missing": ["stat"], "id_rec": int(id_rec)}
                Audit.insertAudit(audit_user, "RecordStat", "RECORD", int(id_rec), "ERROR", details, "U")
            except Exception as err:
                self.log.error(Logs.fileline() + ' : RecordStat ERROR audit args missing err=' + str(err))
            return compose_ret('', Constants.cst_content_type_json, 400)

        ret = Record.updateRecordStat(id_rec, args['stat'])

        if not ret:
            self.log.error(Logs.fileline() + ' : ERROR RecordStat update')
            try:
                details = {"result": "ERROR", "reason": "UPDATE_RECORD_STAT_FAILED", "id_rec": int(id_rec)}
                Audit.insertAudit(audit_user, "RecordStat", "RECORD", int(id_rec), "ERROR", details, "U")
            except Exception as err:
                self.log.error(Logs.fileline() + ' : RecordStat ERROR audit update err=' + str(err))
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE RecordStat')
        try:
            details = {"result": "SUCCESS", "id_rec": int(id_rec), "stat": args.get("stat")}
            Audit.insertAudit(audit_user, "RecordStat", "RECORD", int(id_rec), "SUCCESS", details, "U")
        except Exception as err:
            self.log.error(Logs.fileline() + ' : RecordStat ERROR audit success err=' + str(err))
        return compose_ret('', Constants.cst_content_type_json)


class RecordListAna(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self, id_rec):
        audit_user = request.oauth_user
        l_datas = Record.getRecordListAnalysis(id_rec)

        if not l_datas:
            self.log.error(Logs.fileline() + ' : ' + 'RecordListAna ERROR not found')
            try:
                details = {"result": "ERROR", "reason": "NOT_FOUND", "id_rec": int(id_rec)}
                Audit.insertAudit(audit_user, "RecordListAna", "RECORD", int(id_rec), "ERROR", details, "R")
            except Exception as err:
                self.log.error(Logs.fileline() + ' : RecordListAna ERROR audit not found err=' + str(err))
            return compose_ret('', Constants.cst_content_type_json, 404)

        Various.useLangDB()

        for data in l_datas:
            # Replace None by empty string
            for key, value in list(data.items()):
                if data[key] is None:
                    data[key] = ''
                elif key == 'name' and data[key]:
                    data[key] = _(data[key].strip())

        self.log.info(Logs.fileline() + ' : RecordListAna id_rec=' + str(id_rec))
        try:
            details = {"result": "SUCCESS", "id_rec": int(id_rec), "count": len(l_datas) if l_datas else 0}
            Audit.insertAudit(audit_user, "RecordListAna", "RECORD", int(id_rec), "SUCCESS", details, "R")
        except Exception as err:
            self.log.error(Logs.fileline() + ' : RecordListAna ERROR audit success err=' + str(err))
        return compose_ret(l_datas, Constants.cst_content_type_json, 200)


class RecordNbEmer(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self):
        audit_user = request.oauth_user
        args = request.get_json()

        if not args:
            args = {}

        res = Record.getRecordNbEmer(args)

        if not res:
            self.log.error(Logs.fileline() + ' : TRACE RecordNbEmer not found')
            nb_emer = 0
        else:
            nb_emer = res['nb_emer']

        self.log.info(Logs.fileline() + ' : TRACE RecordNbEmer')
        try:
            details = {"result": "SUCCESS", "nb_emer": int(nb_emer)}
            Audit.insertAudit(audit_user, "RecordNbEmer", "RECORD", None, "SUCCESS", details, "R")
        except Exception as err:
            self.log.error(Logs.fileline() + ' : RecordNbEmer ERROR audit success err=' + str(err))
        return compose_ret(nb_emer, Constants.cst_content_type_json)


class RecordNbRecTech(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self):
        audit_user = request.oauth_user
        res = Record.getRecordNbRecTech()

        if not res:
            self.log.error(Logs.fileline() + ' : TRACE RecordNbRecTech not found')
            nb_rec_tech = 0
        else:
            nb_rec_tech = res['nb_rec_tech']

        self.log.info(Logs.fileline() + ' : TRACE RecordNbRecTech')
        try:
            details = {"result": "SUCCESS", "nb_rec_tech": int(nb_rec_tech)}
            Audit.insertAudit(audit_user, "RecordNbRecTech", "RECORD", None, "SUCCESS", details, "R")
        except Exception as err:
            self.log.error(Logs.fileline() + ' : RecordNbRecTech ERROR audit success err=' + str(err))
        return compose_ret(nb_rec_tech, Constants.cst_content_type_json)


class RecordNbRecBio(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self):
        audit_user = request.oauth_user
        res = Record.getRecordNbRecBio()

        if not res:
            self.log.error(Logs.fileline() + ' : TRACE RecordNbRecBio not found')
            nb_rec_bio = 0
        else:
            nb_rec_bio = res['nb_rec_bio']

        self.log.info(Logs.fileline() + ' : TRACE RecordNbRecBio')
        try:
            details = {"result": "SUCCESS", "nb_rec_bio": int(nb_rec_bio)}
            Audit.insertAudit(audit_user, "RecordNbRecBio", "RECORD", None, "SUCCESS", details, "R")
        except Exception as err:
            self.log.error(Logs.fileline() + ' : RecordNbRecBio ERROR audit success err=' + str(err))
        return compose_ret(nb_rec_bio, Constants.cst_content_type_json)


class RecordNbRec(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self):
        audit_user = request.oauth_user
        res = Record.getRecordNbRec()

        if not res:
            self.log.error(Logs.fileline() + ' : TRACE RecordNbRec not found')
            nb_rec = 0
        else:
            nb_rec = res['nb_rec']

        self.log.info(Logs.fileline() + ' : TRACE RecordNbRec')
        try:
            details = {"result": "SUCCESS", "nb_rec": int(nb_rec)}
            Audit.insertAudit(audit_user, "RecordNbRec", "RECORD", None, "SUCCESS", details, "R")
        except Exception as err:
            self.log.error(Logs.fileline() + ' : RecordNbRec ERROR audit success err=' + str(err))
        return compose_ret(nb_rec, Constants.cst_content_type_json)


class RecordNbRecToday(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self):
        audit_user = request.oauth_user
        num_today = datetime.now().strftime("%Y%m%d")

        res = Record.getRecordNbRecToday(num_today)

        if not res:
            self.log.error(Logs.fileline() + ' : TRACE RecordNbRecToday not found')
            nb_rec_today = 0
        else:
            nb_rec_today = res['nb_rec_today']

        self.log.info(Logs.fileline() + ' : TRACE RecordNbRecToday')
        try:
            details = {"result": "SUCCESS", "nb_rec_today": int(nb_rec_today)}
            Audit.insertAudit(audit_user, "RecordNbRecToday", "RECORD", None, "SUCCESS", details, "R")
        except Exception as err:
            self.log.error(Logs.fileline() + ' : RecordNbRecToday ERROR audit success err=' + str(err))
        return compose_ret(nb_rec_today, Constants.cst_content_type_json)


class RecordValid(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self, id_rec):
        audit_user = request.oauth_user
        rev = Record.getRecordValidation(id_rec)

        if not rev:
            self.log.error(Logs.fileline() + ' : TRACE RecordValid not found')
            try:
                details = {"result": "ERROR", "reason": "NOT_FOUND", "id_rec": int(id_rec)}
                Audit.insertAudit(audit_user, "RecordValid", "RECORD", int(id_rec), "ERROR", details, "R")
            except Exception as err:
                self.log.error(Logs.fileline() + ' : RecordValid ERROR audit not found err=' + str(err))
            return compose_ret('', Constants.cst_content_type_json, 404)

        if rev['rev_date']:
            rev['rev_date'] = datetime.strftime(rev['rev_date'], Constants.cst_dt_HM)

        self.log.info(Logs.fileline() + ' : TRACE RecordValid')
        try:
            details = {"result": "SUCCESS", "id_rec": int(id_rec)}
            Audit.insertAudit(audit_user, "RecordValid", "RECORD", int(id_rec), "SUCCESS", details, "R")
        except Exception as err:
            self.log.error(Logs.fileline() + ' : RecordValid ERROR audit success err=' + str(err))
        return compose_ret(rev, Constants.cst_content_type_json)

    @require_oauth()
    def post(self, id_rec):
        audit_user = request.oauth_user
        args = request.get_json()

        if 'id_user' not in args or 'comm' not in args:
            self.log.error(Logs.fileline() + ' : ERROR RecordValid args missing')
            try:
                details = {"result": "ERROR", "reason": "ARGS_MISSING", "missing": ["id_user", "comm"], "id_rec": int(id_rec)}
                Audit.insertAudit(audit_user, "RecordValid", "RECORD", int(id_rec), "ERROR", details, "U")
            except Exception as err:
                self.log.error(Logs.fileline() + ' : RecordValid ERROR audit args missing err=' + str(err))
            return compose_ret('', Constants.cst_content_type_json, 400)

        ret = Record.insertRecordValidation(id_user=args['id_user'], id_rec=id_rec, comm=args['comm'])

        if not ret:
            self.log.error(Logs.fileline() + ' : ERROR RecordValid insert')
            try:
                details = {"result": "ERROR", "reason": "INSERT_RECORD_VALIDATION_FAILED", "id_rec": int(id_rec),
                           "id_user": args.get("id_user")}
                Audit.insertAudit(audit_user, "RecordValid", "RECORD", int(id_rec), "ERROR", details, "U")
            except Exception as err:
                self.log.error(Logs.fileline() + ' : RecordValid ERROR audit insert err=' + str(err))
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE RecordValid')
        try:
            details = {"result": "SUCCESS", "id_rec": int(id_rec), "id_user": args.get("id_user")}
            Audit.insertAudit(audit_user, "RecordValid", "RECORD", int(id_rec), "SUCCESS", details, "U")
        except Exception as err:
            self.log.error(Logs.fileline() + ' : RecordValid ERROR audit success err=' + str(err))
        return compose_ret('', Constants.cst_content_type_json)


class RecordNumInt(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self, rec_num_int):
        audit_user = request.oauth_user
        ret = Record.rec_num_int_exist(rec_num_int)

        if ret and ret == -1:
            self.log.error(Logs.fileline() + ' : ' + 'RecordNumInt ERROR sql')
            try:
                details = {"result": "ERROR", "reason": "SQL_ERROR", "rec_num_int": str(rec_num_int)}
                Audit.insertAudit(audit_user, "RecordNumInt", "RECORD", None, "ERROR", details, "R")
            except Exception as err:
                self.log.error(Logs.fileline() + ' : RecordNumInt ERROR audit sql err=' + str(err))
            return compose_ret(-1, Constants.cst_content_type_json, 500)

        if ret:
            self.log.info(Logs.fileline() + ' : ' + 'RecordNumInt WARNING code already exist')
            try:
                details = {"result": "SUCCESS", "rec_num_int": str(rec_num_int), "exists": "Y"}
                Audit.insertAudit(audit_user, "RecordNumInt", "RECORD", None, "SUCCESS", details, "R")
            except Exception as err:
                self.log.error(Logs.fileline() + ' : RecordNumInt ERROR audit exists err=' + str(err))
            return compose_ret(1, Constants.cst_content_type_json, 200)
        else:
            self.log.info(Logs.fileline() + ' : RecordNumInt code ok :' + str(rec_num_int))
            try:
                details = {"result": "SUCCESS", "rec_num_int": str(rec_num_int), "exists": "N"}
                Audit.insertAudit(audit_user, "RecordNumInt", "RECORD", None, "SUCCESS", details, "R")
            except Exception as err:
                self.log.error(Logs.fileline() + ' : RecordNumInt ERROR audit ok err=' + str(err))
            return compose_ret(0, Constants.cst_content_type_json, 200)
