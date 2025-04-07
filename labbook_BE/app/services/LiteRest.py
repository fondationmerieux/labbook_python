# -*- coding:utf-8 -*-
import logging
import gettext
import bcrypt

from datetime import datetime
from flask import request
from flask_restful import Resource

from app.models.General import compose_ret
from app.models.Constants import Constants
from app.models.Logs import Logs
from app.models.Lite import Lite
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

        if 'name' not in args or 'login' not in args or 'pwd' not in args or 'users' not in args:
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
                                       pwd=pwd_hashed)

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
                                       pwd=pwd_hashed)

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
            "lite_ser": setting['lite_ser']
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
                {"name": "address", "type": "TEXT"},
                {"name": "phone", "type": "TEXT"},
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
                {"name": "rating_unit", "type": "TEXT"},
                {"name": "rating_value", "type": "REAL"},
                {"name": "comment", "type": "TEXT"},
                {"name": "bio_product", "type": "INTEGER"},
                {"name": "sample_type", "type": "INTEGER"},
                {"name": "analysis_type", "type": "INTEGER"},
                {"name": "active", "type": "INTEGER"},
                {"name": "ana_whonet", "type": "INTEGER"},
                {"name": "ana_ast", "type": "TEXT"},
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
                {"name": "var_whonet", "type": "INTEGER"},
                {"name": "var_qrcode", "type": "TEXT"}
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
                {"name": "pat_email", "type": "TEXT"}
            ]
        }

        setup["patients"] = Lite.getLitePatients()

        # 5 - recover preferences sigl_06_data
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

        # 6 - recover nationality
        NATIONALITY_TABLE_SCHEMA = {
            "table": "nationality",
            "columns": [
                {"name": "nat_ser", "type": "INTEGER PRIMARY KEY"},
                {"name": "nat_name", "type": "TEXT"},
                {"name": "nat_code", "type": "TEXT"}
            ]
        }

        setup["nationality"] = Lite.getLiteNationalities()

        # 7 - schemas for receive data
        SAMPLE_TABLE_SCHEMA = {
            "table": "sample",
            "columns": [
                {"name": "id_data", "type": "INTEGER PRIMARY KEY"},
                {"name": "samp_date", "type": "DATETIME"},
                {"name": "sample_type", "type": "INTEGER"},
                {"name": "statu", "type": "INTEGER"},
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
                {"name": "num_dos_jour", "type": "TEXT"},
                {"name": "num_dos_an", "type": "TEXT"},
                {"name": "med_prescripteur", "type": "INTEGER"},
                {"name": "date_prescription", "type": "DATE"},
                {"name": "service_interne", "type": "TEXT"},
                {"name": "num_lit", "type": "INTEGER"},
                {"name": "id_colis", "type": "TEXT"},
                {"name": "rec_parcel_date", "type": "DATETIME"},
                {"name": "rc", "type": "TEXT"},
                {"name": "colis", "type": "INTEGER"},
                {"name": "prix", "type": "DECIMAL(10,2)"},
                {"name": "remise", "type": "INTEGER"},
                {"name": "remise_pourcent", "type": "DECIMAL(10,2)"},
                {"name": "assu_pourcent", "type": "DECIMAL(10,2)"},
                {"name": "a_payer", "type": "DECIMAL(10,2)"},
                {"name": "num_quittance", "type": "TEXT"},
                {"name": "num_fact", "type": "TEXT"},
                {"name": "statut", "type": "INTEGER"},
                {"name": "num_dos_mois", "type": "TEXT"},
                {"name": "date_hosp", "type": "DATE"},
                {"name": "rec_custody", "type": "TEXT"},
                {"name": "rec_num_int", "type": "TEXT"},
                {"name": "rec_date_vld", "type": "DATETIME"},
                {"name": "rec_modified", "type": "TEXT"},
                {"name": "rec_hosp_num", "type": "TEXT"},
                {"name": "rec_date_save", "type": "DATETIME"}
            ]
        }

        setup["record"] = []

        REQUEST_TABLE_SCHEMA = {
            "table": "analysis_request",
            "columns": [
                {"name": "id_data", "type": "INTEGER PRIMARY KEY"},
                {"name": "id_dos", "type": "INTEGER"},
                {"name": "ref_analyse", "type": "INTEGER"},
                {"name": "prix", "type": "DECIMAL(10,2)"},
                {"name": "paye", "type": "INTEGER"},
                {"name": "urgent", "type": "INTEGER"},
                {"name": "demande", "type": "INTEGER"},
                {"name": "req_outsourced", "type": "TEXT"}
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
                {"name": "obligatoire", "type": "INTEGER"},
                {"name": "res_recovery", "type": "TEXT"}
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
            "preferences": PREFERENCES_TABLE_SCHEMA,
            "nationality" : NATIONALITY_TABLE_SCHEMA,
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
