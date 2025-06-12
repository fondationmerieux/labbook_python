# -*- coding:utf-8 -*-
import logging
import gettext
import bcrypt
import os
import base64
import shutil
import uuid

from datetime import datetime
from flask import request
from flask_restful import Resource

from app.models.General import compose_ret
from app.models.Constants import Constants
from app.models.Logs import Logs
from app.models.Lite import Lite
from app.models.Analysis import Analysis
from app.models.File import File
from app.models.Patient import Patient
from app.models.Product import Product
from app.models.Record import Record
from app.models.Result import Result
from app.models.Various import Various


class LiteSetupList(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        l_setup = Lite.getLiteSetupList()

        if not l_setup:
            self.log.error(Logs.fileline() + ' : TRACE LiteSetupList not found')

        for setup in l_setup:
            # Replace None by empty string
            for key, value in list(setup.items()):
                if setup[key] is None:
                    setup[key] = ''

        self.log.info(Logs.fileline() + ' : TRACE LiteSetupList')
        return compose_ret({"data": l_setup}, Constants.cst_content_type_json)


class LiteSetupDet(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_item):
        item = Lite.getLiteSetup(id_item)

        if not item:
            self.log.error(Logs.fileline() + ' : ' + 'LiteSetupDet ERROR not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        # Replace None by empty string
        for key, value in list(item.items()):
            if item[key] is None:
                item[key] = ''

        # Add associated users (only user IDs)
        item['lite_users'] = Lite.getLiteUsers(id_item)

        self.log.info(Logs.fileline() + ' : LiteSetupDet id_item=' + str(id_item))
        return compose_ret(item, Constants.cst_content_type_json, 200)

    def post(self, id_item):
        args = request.get_json()

        if 'name' not in args or 'login' not in args or 'pwd' not in args or 'users' not in args or \
           'report_pwd' not in args:
            self.log.error(Logs.fileline() + ' : LiteSetupDet ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        try:
            pwd_hashed = bcrypt.hashpw(args['pwd'].encode(), bcrypt.gensalt()).decode()
        except Exception as e:
            self.log.error(Logs.alert() + f' : LiteSetupDet bcrypt error = {str(e)}')
            return compose_ret('', Constants.cst_content_type_json, 500)

        # Update item
        if id_item > 0:
            ret = Lite.updateLiteSetup(id_item=id_item,
                                       name=args['name'],
                                       login=args['login'],
                                       pwd=pwd_hashed,
                                       report_pwd=args['report_pwd'])

            if ret is False:
                self.log.error(Logs.alert() + ' : LiteSetupDet ERROR update setup')
                return compose_ret('', Constants.cst_content_type_json, 500)

            ret = Lite.insertLiteUsers(id_lite=id_item, users=args['users'])

            if ret is False:
                self.log.error(Logs.alert() + ' : LiteSetupDet ERROR insert users')
                return compose_ret('', Constants.cst_content_type_json, 500)

        # Insert new item
        else:
            ret = Lite.insertLiteSetup(name=args['name'],
                                       login=args['login'],
                                       pwd=pwd_hashed,
                                       report_pwd=args['report_pwd'])

            if ret <= 0:
                self.log.error(Logs.alert() + ' : LiteSetupDet ERROR insert setup')
                return compose_ret('', Constants.cst_content_type_json, 500)

            id_item = ret

            ret = Lite.insertLiteUsers(id_lite=id_item, users=args['users'])

            if ret is False:
                self.log.error(Logs.alert() + ' : LiteSetupDet ERROR insert users')
                return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE LiteSetupDet id_item=' + str(id_item))
        return compose_ret(id_item, Constants.cst_content_type_json)


class LiteSetupLoad(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        if 'login' not in args or 'pwd' not in args:
            self.log.error(Logs.fileline() + ' : LiteSetupLoad ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        login = args['login']
        password = args['pwd']

        # Get the Lite setting by login
        setting = Lite.getLiteSetupByLogin(login)

        if not setting:
            self.log.error(Logs.fileline() + f' : LiteSetupLoad ERROR login "{login}" not found')
            return compose_ret('', Constants.cst_content_type_json, 401)

        # Compare hash
        if not bcrypt.checkpw(password.encode(), setting['lite_pwd'].encode()):
            self.log.error(Logs.fileline() + f' : LiteSetupLoad ERROR invalid password for login "{login}"')
            return compose_ret('', Constants.cst_content_type_json, 401)

        l_users = Lite.getLiteUsers(setting['lite_ser'])

        # If auth successful load setup
        setup = {
            "lite_name": setting['lite_name'],
            "lite_ser": setting['lite_ser'],
            "lite_report_pwd": setting['lite_report_pwd']
        }

        # 1 - retrieve users from sigl_user_data with id_data in l_users
        USER_TABLE_SCHEMA = {
            "table": "user",
            "columns": [
                {"name": "id_data", "type": "INTEGER PRIMARY KEY"},
                {"name": "firstname", "type": "TEXT"},
                {"name": "lastname", "type": "TEXT"},
                {"name": "username", "type": "TEXT"},
                {"name": "password", "type": "TEXT"},
                {"name": "title", "type": "INTEGER"},
                {"name": "email", "type": "TEXT"},
                {"name": "locale", "type": "INTEGER"},
                {"name": "initial", "type": "TEXT"},
                {"name": "role_type", "type": "TEXT"}
            ]
        }

        setup["users"] = Lite.getLiteUsersByIds(l_users)

        # 2 - retrieve primary analysis info from 3 tables sigl_05_data, sigl_05_07_data, sigl_07_data
        ANALYSIS_TABLE_SCHEMA = {
            "table": "analysis",
            "columns": [
                {"name": "id_data", "type": "INTEGER PRIMARY KEY"},
                {"name": "code", "type": "TEXT"},
                {"name": "name", "type": "TEXT"},
                {"name": "abbr", "type": "TEXT"},
                {"name": "family", "type": "INTEGER"},
                {"name": "comment", "type": "TEXT"},
                {"name": "bio_product", "type": "INTEGER"},
                {"name": "sample_type", "type": "INTEGER"},
                {"name": "analysis_type", "type": "INTEGER"},
                {"name": "active", "type": "INTEGER"},
                {"name": "ana_loinc", "type": "TEXT"}
            ]
        }

        analysis = Lite.getLiteAnalysis()
        setup["analysis"] = analysis

        ANA_LINK_TABLE_SCHEMA = {
            "table": "ana_link",
            "columns": [
                {"name": "id_data", "type": "INTEGER PRIMARY KEY"},
                {"name": "analysis_id", "type": "INTEGER"},
                {"name": "variable_id", "type": "INTEGER"},
                {"name": "position", "type": "INTEGER"},
                {"name": "var_number", "type": "INTEGER"},
                {"name": "required", "type": "INTEGER"},
            ]
        }

        # Extra IDs from produit_biologique fields
        ana_samp_ids = list({
            a["produit_biologique"]
            for a in analysis
            if a.get("produit_biologique") and a["produit_biologique"] > 0
        })

        # Retrieve analyses referenced by produit_biologique
        analysis_samp = Lite.getLiteAnalysisByIds(ana_samp_ids)

        # Combine and deduplicate by id_data
        analysis += analysis_samp
        analysis = list({a["id_data"]: a for a in analysis}.values())

        # Save in setup
        setup["analysis"] = analysis

        ana_ids = [a["id_data"] for a in analysis]
        setup["ana_link"] = Lite.getLiteLinksAnalysisVar(ana_ids)

        ANA_VAR_TABLE_SCHEMA = {
            "table": "ana_var",
            "columns": [
                {"name": "id_data", "type": "INTEGER PRIMARY KEY"},
                {"name": "label", "type": "TEXT"},
                {"name": "short_label", "type": "TEXT"},
                {"name": "description", "type": "TEXT"},
                {"name": "unit", "type": "INTEGER"},
                {"name": "normal_min", "type": "TEXT"},
                {"name": "normal_max", "type": "TEXT"},
                {"name": "comment", "type": "TEXT"},
                {"name": "result_type", "type": "INTEGER"},
                {"name": "unit2", "type": "INTEGER"},
                {"name": "formula_unit2", "type": "TEXT"},
                {"name": "formula", "type": "TEXT"},
                {"name": "accuracy", "type": "INTEGER"},
                {"name": "accuracy2", "type": "INTEGER"},
                {"name": "var_code", "type": "TEXT"},
                {"name": "var_highlight", "type": "TEXT"},
                {"name": "var_show_minmax", "type": "TEXT"}
            ]
        }

        var_ids = list({l["variable_id"] for l in setup["ana_link"]})
        setup["ana_var"] = Lite.getLiteVAnalysisVarByIds(var_ids)

        # 3 - recover dictionary sigl_dico_data
        DICT_TABLE_SCHEMA = {
            "table": "dictionary",
            "columns": [
                {"name": "id_data", "type": "INTEGER PRIMARY KEY"},
                {"name": "dico_name", "type": "TEXT"},
                {"name": "label", "type": "TEXT"},
                {"name": "short_label", "type": "TEXT"},
                {"name": "position", "type": "INTEGER"},
                {"name": "code", "type": "TEXT"},
                {"name": "dico_descr", "type": "TEXT"},
                {"name": "dict_formatting", "type": "TEXT"}
            ]
        }

        setup["dictionary"] = Lite.getLiteDictionary()

        # 4 - recover patients sigl_03_data
        PATIENT_TABLE_SCHEMA = {
            "table": "patient",
            "columns": [
                {"name": "id_data", "type": "INTEGER PRIMARY KEY"},
                {"name": "pat_ano", "type": "INTEGER"},
                {"name": "pat_code_lab", "type": "TEXT"},
                {"name": "pat_code", "type": "TEXT"},
                {"name": "pat_name", "type": "TEXT"},
                {"name": "pat_midname", "type": "TEXT"},
                {"name": "pat_maiden", "type": "TEXT"},
                {"name": "pat_firstname", "type": "TEXT"},
                {"name": "pat_sex", "type": "INTEGER"},
                {"name": "pat_birth", "type": "TEXT"},
                {"name": "pat_birth_approx", "type": "INTEGER"},
                {"name": "pat_age", "type": "INTEGER"},
                {"name": "pat_age_unit", "type": "INTEGER"},
                {"name": "pat_nationality", "type": "INTEGER"},
                {"name": "pat_resident", "type": "TEXT"},
                {"name": "pat_blood_group", "type": "INTEGER"},
                {"name": "pat_blood_rhesus", "type": "INTEGER"},
                {"name": "pat_address", "type": "TEXT"},
                {"name": "pat_phone1", "type": "TEXT"},
                {"name": "pat_phone2", "type": "TEXT"},
                {"name": "pat_profession", "type": "TEXT"},
                {"name": "pat_zipcode", "type": "TEXT"},
                {"name": "pat_city", "type": "TEXT"},
                {"name": "pat_pbox", "type": "TEXT"},
                {"name": "pat_district", "type": "TEXT"},
                {"name": "pat_email", "type": "TEXT"},
                {"name": "pat_lite", "type": "TEXT"}
            ]
        }

        setup["patients"] = Lite.getLitePatients()

        # 5 - recover prescriber sigl_08_data
        PRESCRIBER_TABLE_SCHEMA = {
            "table": "prescriber",
            "columns": [
                {"name": "id_data", "type": "INTEGER PRIMARY KEY"},
                {"name": "code", "type": "TEXT"},
                {"name": "lastname", "type": "TEXT"},
                {"name": "firstname", "type": "TEXT"},
                {"name": "city", "type": "TEXT"},
                {"name": "institution", "type": "TEXT"},
                {"name": "speciality", "type": "INTEGER"},
                {"name": "phone", "type": "TEXT"},
                {"name": "email", "type": "TEXT"},
                {"name": "title", "type": "INTEGER"},
                {"name": "initial", "type": "TEXT"},
                {"name": "department", "type": "TEXT"},
                {"name": "address", "type": "TEXT"},
                {"name": "mobile", "type": "TEXT"},
                {"name": "fax", "type": "TEXT"},
                {"name": "zip_city", "type": "TEXT"}
            ]
        }

        setup["prescribers"] = Lite.getLitePrescribers()

        # 6 - recover preferences sigl_06_data
        PREFERENCES_TABLE_SCHEMA = {
            "table": "preferences",
            "columns": [
                {"name": "id_data", "type": "INTEGER PRIMARY KEY"},
                {"name": "key", "type": "TEXT"},
                {"name": "label", "type": "TEXT"},
                {"name": "value", "type": "TEXT"}
            ]
        }

        setup["preferences"] = Lite.getLitePreferences()

        # 7 - recover nationality
        NATIONALITY_TABLE_SCHEMA = {
            "table": "nationality",
            "columns": [
                {"name": "nat_ser", "type": "INTEGER PRIMARY KEY"},
                {"name": "nat_name", "type": "TEXT"},
                {"name": "nat_code", "type": "TEXT"}
            ]
        }

        setup["nationality"] = Lite.getLiteNationalities()

        # 8 - schemas for receive data
        SAMPLE_TABLE_SCHEMA = {
            "table": "sample",
            "columns": [
                {"name": "id_data", "type": "INTEGER PRIMARY KEY"},
                {"name": "samp_date", "type": "DATETIME"},
                {"name": "sample_type", "type": "INTEGER"},
                {"name": "status", "type": "INTEGER"},
                {"name": "record_id", "type": "INTEGER"},
                {"name": "sampler", "type": "TEXT"},
                {"name": "samp_receipt_date", "type": "DATETIME"},
                {"name": "comment", "type": "TEXT"},
                {"name": "location_id", "type": "INTEGER"},
                {"name": "location_plus", "type": "TEXT"},
                {"name": "localization", "type": "TEXT"},
                {"name": "code", "type": "TEXT"},
                {"name": "samp_id_ana", "type": "INTEGER"}
            ]
        }

        setup["sample"] = []

        RECORD_TABLE_SCHEMA = {
            "table": "record",
            "columns": [
                {"name": "id_data", "type": "INTEGER PRIMARY KEY"},
                {"name": "id_patient", "type": "INTEGER"},
                {"name": "type", "type": "INTEGER"},
                {"name": "rec_date_receipt", "type": "DATETIME"},
                {"name": "med_prescripteur", "type": "INTEGER"},
                {"name": "date_prescription", "type": "DATE"},
                {"name": "rc", "type": "TEXT"},
                {"name": "statut", "type": "INTEGER"},
                {"name": "rec_num_int", "type": "TEXT"},
                {"name": "rec_date_vld", "type": "DATETIME"},
                {"name": "rec_modified", "type": "TEXT"},
                {"name": "rec_date_save", "type": "DATETIME"},
                {"name": "rec_num", "type": "TEXT"},  # specific for Lite
                {"name": "rec_lite", "type": "TEXT"}
            ]
        }

        setup["record"] = []

        REQUEST_TABLE_SCHEMA = {
            "table": "analysis_request",
            "columns": [
                {"name": "id_data", "type": "INTEGER PRIMARY KEY"},
                {"name": "id_dos", "type": "INTEGER"},
                {"name": "ref_analyse", "type": "INTEGER"},
                {"name": "urgent", "type": "INTEGER"}
            ]
        }

        setup["analysis_request"] = []

        RESULT_TABLE_SCHEMA = {
            "table": "analysis_result",
            "columns": [
                {"name": "id_data", "type": "INTEGER PRIMARY KEY"},
                {"name": "id_analyse", "type": "INTEGER"},
                {"name": "ref_variable", "type": "INTEGER"},
                {"name": "valeur", "type": "TEXT"},
                {"name": "obligatoire", "type": "INTEGER"}
            ]
        }

        setup["analysis_result"] = []

        VALIDATION_TABLE_SCHEMA = {
            "table": "analysis_validation",
            "columns": [
                {"name": "id_data", "type": "INTEGER PRIMARY KEY"},
                {"name": "id_resultat", "type": "INTEGER"},
                {"name": "date_validation", "type": "DATETIME"},
                {"name": "utilisateur", "type": "INTEGER"},
                {"name": "valeur", "type": "TEXT"},
                {"name": "type_validation", "type": "INTEGER"},
                {"name": "commentaire", "type": "TEXT"},
                {"name": "motif_annulation", "type": "INTEGER"}
            ]
        }

        setup["analysis_validation"] = []

        setup["schemas"] = {
            "user": USER_TABLE_SCHEMA,
            "analysis": ANALYSIS_TABLE_SCHEMA,
            "ana_link": ANA_LINK_TABLE_SCHEMA,
            "ana_var": ANA_VAR_TABLE_SCHEMA,
            "dictionary": DICT_TABLE_SCHEMA,
            "patient": PATIENT_TABLE_SCHEMA,
            "prescriber": PRESCRIBER_TABLE_SCHEMA,
            "preferences": PREFERENCES_TABLE_SCHEMA,
            "nationality": NATIONALITY_TABLE_SCHEMA,
            "sample": SAMPLE_TABLE_SCHEMA,
            "record": RECORD_TABLE_SCHEMA,
            "analysis_request": REQUEST_TABLE_SCHEMA,
            "analysis_result": RESULT_TABLE_SCHEMA,
            "analysis_validation": VALIDATION_TABLE_SCHEMA
        }

        # TODO for DEBUG during test
        import json
        from decimal import Decimal
        from datetime import date, datetime
        import base64

        def safe_json_default(obj):
            if isinstance(obj, Decimal):
                return float(obj)
            elif isinstance(obj, (datetime, date)):
                return obj.isoformat()
            elif isinstance(obj, bytes):
                try:
                    return obj.decode("utf-8")
                except UnicodeDecodeError:
                    return base64.b64encode(obj).decode("ascii")
            return str(obj)

        # add logo.png for PDF report
        import os
        with open(os.path.join(Constants.cst_resource, "logo.png"), "rb") as f:
            encoded_logo = base64.b64encode(f.read()).decode("ascii")
            setup["logo_base64"] = encoded_logo

        json_str = json.dumps(setup, ensure_ascii=True, default=safe_json_default)
        size_bytes = len(json_str.encode("utf-8"))
        self.log.info(Logs.fileline() + f' : DEBUG size setup : {size_bytes} bytes')

        self.log.info(Logs.fileline() + f' : LiteSetupLoad OK for login "{login}"')
        return compose_ret(setup, Constants.cst_content_type_json)


class LiteDataRecovery(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        if 'login' not in args or 'pwd' not in args:
            self.log.error(Logs.fileline() + ' : LiteDataRecovery ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        login = args['login']
        password = args['pwd']

        # Get the Lite setting by login
        setting = Lite.getLiteSetupByLogin(login)

        if not setting:
            self.log.error(Logs.fileline() + f' : LiteDataRecovery ERROR login "{login}" not found')
            return compose_ret('', Constants.cst_content_type_json, 401)

        # Compare hash
        if not bcrypt.checkpw(password.encode(), setting['lite_pwd'].encode()):
            self.log.error(Logs.fileline() + f' : LiteDataRecovery ERROR invalid password for login "{login}"')
            return compose_ret('', Constants.cst_content_type_json, 401)

        self.log.info(Logs.fileline() + ' : DEBUG LiteDataRecovery args = ' + str(args))

        # 1 - insert new patients and update existing ones (same code)
        patient_id_map = {}
        patients = args.get('patients', [])
        inserted = 0
        updated = 0

        for pat in patients:
            try:
                old_id = pat.get('id_data')
                code = pat.get('pat_code')

                pat_lite = pat.get('pat_lite', 0)

                # skip all patients without code starting by LT or pat_lite <= 0
                if not code or not code.startswith("LT") or pat_lite <= 0:
                    continue

                existing = Patient.getPatientByCode(code, "")

                # convert fields if needed
                pat['id_owner'] = 0  # TODO add tracability in Android app too
                pat['anonyme'] = pat.get('pat_ano', 'N')
                pat['code'] = code
                pat['code_patient'] = pat.get('pat_code_lab')
                pat['nom'] = pat.get('pat_name')
                pat['prenom'] = pat.get('pat_firstname')
                pat['ddn_approx'] = pat.get('pat_birth_approx')
                pat['sexe'] = pat.get('pat_sex')
                pat['adresse'] = pat.get('pat_address')
                pat['cp'] = pat.get('pat_zipcode')
                pat['ville'] = pat.get('pat_city')
                pat['email'] = pat.get('pat_email')
                pat['tel'] = pat.get('pat_phone1')
                pat['phone2'] = pat.get('pat_phone2')
                pat['profession'] = pat.get('pat_profession')
                pat['nom_jf'] = pat.get('pat_maiden')
                pat['quartier'] = pat.get('pat_district')
                pat['bp'] = pat.get('pat_pbox')
                pat['age'] = pat.get('pat_age')
                pat['unite'] = pat.get('pat_age_unit')
                pat['midname'] = pat.get('pat_midname')
                pat['nationality'] = pat.get('pat_nationality')
                pat['resident'] = pat.get('pat_resident')
                pat['blood_group'] = pat.get('pat_blood_group')
                pat['blood_rhesus'] = pat.get('pat_blood_rhesus')
                pat['pat_lite'] = pat.get('pat_lite', 0)

                # convert ddn (date of birth) to datetime.date
                if pat.get('pat_birth'):
                    try:
                        pat['ddn'] = datetime.strptime(pat['pat_birth'], "%Y-%m-%d").date()
                    except Exception as e:
                        self.log.warning(Logs.fileline() + f' : LiteDataRecovery Invalid patient birth date → {e}')
                        pat['ddn'] = None
                else:
                    pat['ddn'] = None

                if existing:
                    same_age = str(existing['age']) == str(pat.get('pat_age'))
                    same_sex = str(existing['sexe']) == str(pat.get('pat_sex'))

                    if same_age and same_sex:
                        # update patient
                        pat['id'] = existing['id_data']
                        Patient.updatePatient(**pat)
                        updated += 1
                        new_id = existing['id_data']
                    else:
                        # create new patient with new code
                        try:
                            new_code = Patient.newPatientCode(6, "LT")
                            pat['code'] = new_code
                            new_id = Patient.insertPatient(**pat)
                            inserted += 1
                        except Exception as e:
                            self.log.error(Logs.fileline() + f' : LiteDataRecovery Failed to insert duplicate patient with new code → {e}')
                            continue
                else:
                    new_id = Patient.insertPatient(**pat)
                    inserted += 1

                if old_id and new_id:
                    patient_id_map[old_id] = new_id

            except Exception as e:
                self.log.error(Logs.fileline() + f' : LiteDataRecovery Patient insert/update error → {e}')

        self.log.info(Logs.fileline() + f' : LiteDataRecovery Patients processed → {inserted} inserted, {updated} updated')

        # 2 - insert records
        records = args.get('records', [])
        record_id_map = {}
        record_inserted = 0
        record_skipped = 0

        for rec in records:
            try:
                old_pat_id = rec.get('patient_id')
                new_pat_id = patient_id_map.get(old_pat_id)

                if not new_pat_id:
                    log_id = rec.get("rec_num_lite") or rec.get("rec_num_int")
                    self.log.warning(Logs.fileline() + f' : LiteDataRecovery Skipping record {log_id} → unknown patient id {old_pat_id}')
                    record_skipped += 1
                    continue

                # Step 1 - Retrieve and increment records numbers
                date_now = datetime.now()
                last_num = Various.getLastNumDos()

                if not last_num:
                    base_jour = date_now.strftime("%Y%m%d") + "0000"
                    base_mois = date_now.strftime("%Y%m") + "0000"
                    base_an = date_now.strftime("%Y") + "000000"
                    last_num = {
                        "num_dos_jour": base_jour,
                        "num_dos_mois": base_mois,
                        "num_dos_an": base_an
                    }

                # --- Prefix ---
                day_prefix = date_now.strftime("%Y%m%d")
                month_prefix = day_prefix[:6]
                year_prefix = day_prefix[:4]

                # Extract and increment suffixes
                day_suffix = int(last_num['num_dos_jour'][8:]) + 1
                month_suffix = int(last_num['num_dos_mois'][6:]) + 1
                year_suffix = int(last_num['num_dos_an'][4:]) + 1

                # Format new records numbers
                num_dos_jour = f"{day_prefix}{day_suffix:04d}"
                num_dos_mois = f"{month_prefix}{month_suffix:04d}"
                num_dos_an = f"{year_prefix}{year_suffix:06d}"

                # Step 2 - Save these into sigl_pj_sequence
                ret = Record.insertPjSequence("numdosjour", f"{day_prefix}%04d", day_suffix)
                if ret == 0:
                    self.log.warning(Logs.fileline() + " : LiteDataRecovery PJSequence jour duplicate, retrying")
                    day_suffix += 1
                    num_dos_jour = f"{day_prefix}{day_suffix:04d}"
                    Record.insertPjSequence("numdosjour", f"{day_prefix}%04d", day_suffix)

                ret = Record.insertPjSequence("numdosmois", f"{month_prefix}%04d", month_suffix)
                if ret == 0:
                    self.log.warning(Logs.fileline() + " : LiteDataRecovery PJSequence mois duplicate, retrying")
                    month_suffix += 1
                    num_dos_mois = f"{month_prefix}{month_suffix:04d}"
                    Record.insertPjSequence("numdosmois", f"{month_prefix}%04d", month_suffix)

                ret = Record.insertPjSequence("numdosan", f"{year_prefix}%06d", year_suffix)
                if ret == 0:
                    self.log.warning(Logs.fileline() + " : LiteDataRecovery PJSequence an duplicate, retrying")
                    year_suffix += 1
                    num_dos_an = f"{year_prefix}{year_suffix:06d}"
                    Record.insertPjSequence("numdosan", f"{year_prefix}%06d", year_suffix)

                # Step 3 - inject into the record object before insert
                rec['num_dos_jour'] = num_dos_jour
                rec['num_dos_mois'] = num_dos_mois
                rec['num_dos_an'] = num_dos_an

                new_id = Lite.insertLiteRecord(rec, new_pat_id, 0)
                if new_id:
                    record_id_map[rec['id_data']] = new_id
                    record_inserted += 1

            except Exception as e:
                self.log.error(Logs.fileline() + f' : LiteDataRecovery Record insert error → {e}')

        self.log.info(Logs.fileline() + f' : LiteDataRecovery Records processed → {record_inserted} inserted, {record_skipped} skipped')

        # 3 - insert analysis request
        analysis_requests = args.get('analysis_request', [])
        request_id_map = {}
        request_inserted = 0
        request_skipped = 0

        for req in analysis_requests:
            try:
                old_record_id = req.get('recordId')
                new_record_id = record_id_map.get(old_record_id)

                if not new_record_id:
                    self.log.warning(Logs.fileline() + f' : LiteDataRecovery Skipping analysis request → unknown record id {old_record_id}')
                    request_skipped += 1
                    continue

                params = {
                    'id_owner': 0,
                    'id_dos': new_record_id,
                    'ref_analyse': req.get('analysisRef'),
                    'urgent': req.get('isUrgent', 0),
                    'demande': 5,
                    'paye': 4,
                    'prix': 0.0,
                    'outsourced': 'N'
                }

                new_id = Analysis.insertAnalysisReq(**params)
                if new_id:
                    request_id_map[req['id']] = new_id
                    request_inserted += 1

            except Exception as e:
                self.log.error(Logs.fileline() + f' : LiteDataRecovery Analysis request insert error → {e}')

        self.log.info(Logs.fileline() + f' : LiteDataRecovery Analysis requests processed → {request_inserted} inserted, {request_skipped} skipped')

        # 4 - insert analysis samples
        samples = args.get('samples', [])
        sample_id_map = {}
        sample_inserted = 0
        sample_skipped = 0

        for samp in samples:
            try:
                old_rec_id = samp.get('record_id')
                new_rec_id = record_id_map.get(old_rec_id)

                if not new_rec_id:
                    self.log.warning(Logs.fileline() + f' : LiteDataRecovery Skipping sample with old record ID {old_rec_id} → unknown record')
                    sample_skipped += 1
                    continue

                params = {
                    'id_owner': 0,
                    'samp_date': Lite.parse_datetime(samp.get('samp_date')),
                    'type_prel': samp.get('sample_type'),
                    'samp_id_ana': samp.get('samp_id_ana', 0),
                    'statut': samp.get('status'),
                    'id_dos': new_rec_id,
                    'preleveur': samp.get('sampler', ''),
                    'samp_receipt_date': Lite.parse_datetime(samp.get('samp_receipt_date')),
                    'commentaire': samp.get('comment', ''),
                    'lieu_prel': samp.get('location_id'),
                    'lieu_prel_plus': samp.get('location_plus', ''),
                    'localisation': samp.get('localization', ''),
                    'code': samp.get('code', ''),
                }

                new_id = Product.insertProductReq(**params)
                if new_id:
                    sample_id_map[samp['id_data']] = new_id
                    sample_inserted += 1

            except Exception as e:
                self.log.error(Logs.fileline() + f' : LiteDataRecovery Sample insert error → {e}')

        self.log.info(Logs.fileline() + f' : LiteDataRecovery Samples processed → {sample_inserted} inserted, {sample_skipped} skipped')

        # 5 - insert analysis results
        results = args.get('analysis_result', [])
        result_id_map = {}
        result_inserted = 0
        result_skipped = 0

        for res in results:
            try:
                old_req_id = res.get('analysisId')
                new_req_id = request_id_map.get(old_req_id)

                if not new_req_id:
                    self.log.warning(Logs.fileline() + f' : LiteDataRecovery Skipping result with old request ID {old_req_id} → unknown analysis request')
                    result_skipped += 1
                    continue

                params = {
                    'id_owner': 0,
                    'id_analyse': new_req_id,
                    'ref_variable': res.get('variableRef'),
                    'valeur': res.get('value'),
                    'obligatoire': res.get('isRequired', 4),
                    'res_recovery': 'M',
                }

                new_id = Result.insertResult(**params)
                if new_id:
                    result_id_map[res['id']] = new_id
                    result_inserted += 1

            except Exception as e:
                self.log.error(Logs.fileline() + f' : LiteDataRecovery Result insert error → {e}')

        self.log.info(Logs.fileline() + f' : LiteDataRecovery Results processed → {result_inserted} inserted, {result_skipped} skipped')

        # 6 - insert analysis validations
        validations = args.get('analysis_validation', [])
        validation_inserted = 0
        validation_skipped = 0

        for val in validations:
            try:
                old_result_id = val.get('resultId')
                new_result_id = result_id_map.get(old_result_id)

                if not new_result_id:
                    self.log.warning(Logs.fileline() + f' : LiteDataRecovery Skipping validation → unknown result ID {old_result_id}')
                    validation_skipped += 1
                    continue

                params = {
                    'id_owner': 0,
                    'id_resultat': new_result_id,
                    'date_validation': Lite.parse_datetime(val.get('validationDate')),
                    'utilisateur': val.get('userId'),
                    'valeur': val.get('value'),
                    'type_validation': val.get('validationType'),
                    'commentaire': val.get('comment'),
                    'motif_annulation': val.get('cancelReason')
                }

                Result.insertValidation(**params)
                validation_inserted += 1

            except Exception as e:
                self.log.error(Logs.fileline() + f' : LiteDataRecovery Validation insert error → {e}')

        self.log.info(Logs.fileline() + f' : LiteDataRecovery Validations processed → {validation_inserted} inserted, {validation_skipped} skipped')

        # 7 - convert pdf report and insert entry in DB for each PDF report
        report_id_map = {}
        pdfs = args.get("pdf_reports", [])

        for pdf in pdfs:
            try:
                old_rec_id = pdf.get("recordId")
                new_rec_id = record_id_map.get(old_rec_id)

                if not new_rec_id:
                    self.log.warning(Logs.fileline() + f" : LiteDataRecovery Skipping PDF → unknown recordId {old_rec_id}")
                    continue

                filename = pdf.get("filename")  # ex: cr_LT-202505250001.pdf
                file_path = os.path.join(Constants.cst_upload, filename)

                if not os.path.exists(file_path):
                    self.log.warning(Logs.fileline() + f" : LiteDataRecovery PDF file not found → {filename}")
                    continue

                # generate UUID and rename file
                generated_uuid = str(uuid.uuid4())
                new_path = os.path.join(Constants.cst_report, generated_uuid)

                shutil.move(file_path, new_path)

                params = {
                    "id_owner": 0,
                    "id_dos": new_rec_id,
                    "doc_type": 257,
                    "id_tpl": 0,
                    "file": generated_uuid,
                    "date": Lite.parse_datetime(pdf["creationDate"]) if "creationDate" in pdf else datetime.now()
                }

                report_id = File.insertFileReport(**params)
                if report_id:
                    report_id_map[filename] = report_id
                    self.log.info(Logs.fileline() + f" : LiteDataRecovery PDF report linked as {generated_uuid}")
                else:
                    self.log.warning(Logs.fileline() + f" : LiteDataRecovery Failed to insert report for {filename}")

            except Exception as e:
                self.log.error(Logs.fileline() + f" : LiteDataRecovery insertFileReport error → {e}")

        # Clean up leftover cr_LT*.pdf files in upload directory
        try:
            uploaded_files = set(os.listdir(Constants.cst_upload))
            inserted_files = set(report_id_map.keys())

            for leftover in uploaded_files:
                if leftover.startswith("cr_LT") and leftover.endswith(".pdf") and leftover not in inserted_files:
                    try:
                        os.remove(os.path.join(Constants.cst_upload, leftover))
                        self.log.info(Logs.fileline() + f" : LiteDataRecovery Removed leftover file {leftover}")
                    except Exception as e:
                        self.log.warning(Logs.fileline() + f" : LiteDataRecovery Could not delete file {leftover} → {e}")
        except Exception as e:
            self.log.error(Logs.fileline() + f" : LiteDataRecovery Cleanup error in cst_upload → {e}")

        self.log.info(Logs.fileline() + f' : LiteDataRecovery OK for login "{login}"')
        return compose_ret({'success': True}, Constants.cst_content_type_json)


class LiteReportRecovery(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        if 'login' not in args or 'pwd' not in args:
            self.log.error(Logs.fileline() + ' : LiteReportRecovery ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        login = args['login']
        password = args['pwd']

        # Get the Lite setting by login
        setting = Lite.getLiteSetupByLogin(login)

        if not setting:
            self.log.error(Logs.fileline() + f' : LiteReportRecovery ERROR login "{login}" not found')
            return compose_ret('', Constants.cst_content_type_json, 401)

        # Compare hash
        if not bcrypt.checkpw(password.encode(), setting['lite_pwd'].encode()):
            self.log.error(Logs.fileline() + f' : LiteReportRecovery ERROR invalid password for login "{login}"')
            return compose_ret('', Constants.cst_content_type_json, 401)

        # puts pdf reports in a directory : Constants.cst_upload
        pdf_files = args.get('pdf_files', [])
        target_dir = Constants.cst_upload
        os.makedirs(target_dir, exist_ok=True)

        for pdf in pdf_files:
            try:
                filename = pdf.get('filename')
                content_b64 = pdf.get('content_base64')
                if not filename or not content_b64:
                    continue

                pdf_path = os.path.join(target_dir, filename)
                with open(pdf_path, 'wb') as f:
                    f.write(base64.b64decode(content_b64))

                self.log.info(Logs.fileline() + f' : LiteReportRecovery Saved PDF {filename} for login "{login}"')

            except Exception as e:
                self.log.error(Logs.fileline() + f' : LiteReportRecovery Error saving PDF {filename} → {e}')
                return compose_ret({'success': False,
                                    'error': f"Erreur lors de la sauvegarde du fichier : {filename}"},
                                    Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + f' : LiteReportRecovery OK for login "{login}"')
        return compose_ret({'success': True}, Constants.cst_content_type_json)
