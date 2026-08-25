import logging

from datetime import datetime
from flask import request
from flask_restful import Resource

from app.models.Constants import Constants
from app.models.General import compose_ret
from app.models.Logs import Logs
from app.models.Audit import Audit
from app.models.Analysis import Analysis
from app.models.Patient import Patient
from app.models.Record import Record
from app.models.Result import Result
from app.models.Various import Various
from app.security.oauth_routes import require_oauth


# Names exported when this module is imported with "*" (see app/__init__.py).
# Without __all__, "import *" also brings in this module's own imports
# (Constants, datetime, logging...) and they leak into the caller.
__all__ = [
    'Test',
    'DicoById',
    'DefaultValue',
    'InitVersion',
    'NationalityList',
    'DatasetByName',
]


class Test(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self):
        self.log.info(Logs.fileline() + ' : TRACE Test GET')
        audit_user = request.oauth_user
        try:
            details = {"result": "SUCCESS", "method": "GET"}
            Audit.insertAudit(audit_user, "Test", "GENERAL", None, "SUCCESS", details, "R")
        except Exception as err:
            self.log.error(Logs.fileline() + ' : Test ERROR audit err=' + str(err))
        return compose_ret('Test GET OK', Constants.cst_content_type_json)

    @require_oauth()
    def post(self):
        self.log.info(Logs.fileline() + ' : TRACE Test POST')

        audit_user = request.oauth_user
        args = request.get_json()
        try:
            details = {"result": "SUCCESS", "method": "POST"}
            Audit.insertAudit(audit_user, "Test", "GENERAL", None, "SUCCESS", details, "E")
        except Exception as err:
            self.log.error(Logs.fileline() + ' : Test ERROR audit err=' + str(err))
        return compose_ret('args = ' + str(args), Constants.cst_content_type_json)


class DicoById(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self, id_data):
        audit_user = request.oauth_user
        dico = Various.getDicoById(id_data)

        if not dico:
            self.log.error(Logs.fileline() + ' : TRACE DicoById not found : ' + str(id_data))
            dico = {}

        Various.useLangDB()

        # Replace None by empty string
        for key, value in list(dico.items()):
            if dico[key] is None:
                dico[key] = ''
            elif key == 'label' and dico[key] != "":
                dico[key] = _(dico[key].strip())
            # short_label is left untranslated: it is compared as a technical code elsewhere

        self.log.info(Logs.fileline() + ' : TRACE DicoById : ' + str(id_data))
        try:
            details = {"result": "SUCCESS", "id_data": id_data}
            Audit.insertAudit(audit_user, "DicoById", "GENERAL", id_data, "SUCCESS", details, "R")
        except Exception as err:
            self.log.error(Logs.fileline() + ' : DicoById ERROR audit success err=' + str(err))
        return compose_ret(dico, Constants.cst_content_type_json)


class DefaultValue(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self, name):
        audit_user = request.oauth_user
        Various.useLangDB()

        val = Various.getDefaultValue(name)

        if not val:
            self.log.error(Logs.fileline() + ' : ERROR DefaultValue not found : ' + name)
            try:
                details = {"result": "NOT_FOUND", "name": name}
                Audit.insertAudit(audit_user, "DefaultValue", "GENERAL", name, "ERROR", details, "R")
            except Exception as err:
                self.log.error(Logs.fileline() + ' : DefaultValue ERROR audit not found err=' + str(err))
            return compose_ret('', Constants.cst_content_type_json, 404)

        # Replace None by empty string
        for key, value in list(val.items()):
            if val[key] is None:
                val[key] = ''

        self.log.info(Logs.fileline() + ' : TRACE DefaultValue : ' + name)
        try:
            details = {"result": "SUCCESS", "name": name}
            Audit.insertAudit(audit_user, "DefaultValue", "GENERAL", name, "SUCCESS", details, "R")
        except Exception as err:
            self.log.error(Logs.fileline() + ' : DefaultValue ERROR audit success err=' + str(err))
        return compose_ret(val, Constants.cst_content_type_json)

    @require_oauth()
    def post(self, name, value):
        audit_user = request.oauth_user
        ret = Various.updateDefaultValue(name, value)

        if ret is False:
            self.log.error(Logs.fileline() + ' : ERROR DefaultValue update identifiant : ' + name)
            try:
                details = {"result": "ERROR", "reason": "UPDATE_FAILED", "name": name, "value": value}
                Audit.insertAudit(audit_user, "DefaultValue", "GENERAL", name, "ERROR", details, "U")
            except Exception as err:
                self.log.error(Logs.fileline() + ' : DefaultValue ERROR audit update failed err=' + str(err))
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE DefaultValue : ' + name)
        try:
            details = {"result": "SUCCESS", "name": name, "value": value}
            Audit.insertAudit(audit_user, "DefaultValue", "GENERAL", name, "SUCCESS", details, "U")
        except Exception as err:
            self.log.error(Logs.fileline() + ' : DefaultValue ERROR audit success err=' + str(err))
        return compose_ret(ret, Constants.cst_content_type_json)


class InitVersion(Resource):
    log = logging.getLogger('log_services')

    def get(self):
        # check if need to init version
        ini = Various.getLastInitVersion()

        if ini['ini_stat'] == 'Y':
            locales = ['en_GB', 'pt']  # add Portuguese
            ok = all(Various.updateTranslationsTable(loc) for loc in locales)
            if ok:
                Various.updateInitVersion(ini['ini_ser'], 'N')

        self.log.info(Logs.fileline() + ' : TRACE InitVersion ini_ser=' + str(ini['ini_ser']))
        return compose_ret('', Constants.cst_content_type_json)


class NationalityList(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self):
        audit_user = request.oauth_user
        l_items = Various.getNationalityList()

        if not l_items:
            self.log.error(Logs.fileline() + ' : ERROR NationalityList not found')
            try:
                details = {"result": "ERROR", "reason": "NOT_FOUND"}
                Audit.insertAudit(audit_user, "NationalityList", "GENERAL", None, "ERROR", details, "R")
            except Exception as err:
                self.log.error(Logs.fileline() + ' : NationalityList ERROR audit not found err=' + str(err))
            return compose_ret('', Constants.cst_content_type_json, 404)

        Various.useLangDB()

        for item in l_items:
            for key, value in list(item.items()):
                if item[key] is None:
                    item[key] = ''
                if key == 'nat_code':
                    item[key] = item[key].upper()
                if key == 'nat_name' and item[key]:
                    item[key] = _(item[key].strip())

        self.log.info(Logs.fileline() + ' : TRACE NationalityList')
        try:
            details = {"result": "SUCCESS", "count": len(l_items)}
            Audit.insertAudit(audit_user, "NationalityList", "GENERAL", None, "SUCCESS", details, "R")
        except Exception as err:
            self.log.error(Logs.fileline() + ' : NationalityList ERROR audit success err=' + str(err))
        return compose_ret(l_items, Constants.cst_content_type_json)


class DatasetByName(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self, name):
        audit_user = request.oauth_user
        args = request.get_json()

        if name == 'patient':
            l_items = Patient.getDataset()

            for item in l_items:
                for key, value in list(item.items()):
                    if isinstance(item[key], datetime):
                        self.log.error(Logs.fileline() + ' : DEBUG item[key] = ' + str(item[key]))
                        item[key] = datetime.strftime(item[key], Constants.cst_isodate)

                l_form_items = Patient.getFormItems(item['id_patient'])

                for form_item in list(l_form_items):
                    if isinstance(form_item['pfi_value'], datetime):
                        item[str(form_item['pfi_key'])] = datetime.strftime(form_item['pfi_value'], Constants.cst_isodate)
                    else:
                        item[str(form_item['pfi_key'])] = str(form_item['pfi_value'])
        else:
            if not args or ('date_beg' not in args and 'date_end' not in args):
                self.log.error(Logs.fileline() + ' : DatasetByName args missing')
                try:
                    details = {"result": "ERROR", "reason": "ARGS_MISSING", "name": name}
                    Audit.insertAudit(audit_user, "DatasetByName", "GENERAL", name, "ERROR", details, "R")
                except Exception as err:
                    self.log.error(Logs.fileline() + ' : DatasetByName ERROR audit args missing err=' + str(err))
                return compose_ret('', Constants.cst_content_type_json, 500)

            # convert isodate format to ymd format
            date_beg = datetime.strptime(args['date_beg'], Constants.cst_dt_HM)
            date_end = datetime.strptime(args['date_end'], Constants.cst_dt_HM)

        if name == 'record':
            l_items = Record.getDataset(date_beg, date_end)
        elif name == 'analysis':
            l_items = Analysis.getDataset(date_beg, date_end)
        elif name == 'result':
            l_items = Result.getDataset(date_beg, date_end)

        self.log.info(Logs.fileline() + ' : DEBUG dataset l_items = ' + str(l_items))

        if not l_items:
            self.log.error(Logs.fileline() + ' : ERROR dataset not found')
            try:
                details = {"result": "NOT_FOUND", "name": name}
                Audit.insertAudit(audit_user, "DatasetByName", "GENERAL", name, "ERROR", details, "R")
            except Exception as err:
                self.log.error(Logs.fileline() + ' : DatasetByName ERROR audit not found err=' + str(err))
            return compose_ret('', Constants.cst_content_type_json, 404)

        import decimal

        Various.useLangDB()

        # self.log.error(Logs.fileline() + ' : DEBUG-TRACE l_items=' + str(l_items))

        for item in l_items:
            for key, value in list(item.items()):
                if item[key] is None:
                    item[key] = ''
                if isinstance(item[key], decimal.Decimal):
                    item[key] = float(item[key])
                # translate
                if isinstance(item[key], str) and item[key] != "":
                    item[key] = _(item[key].strip())

            # get label of result value and unit
            if 'type_result' in item and item['type_result'] and item['type_result'] > 0:
                type_res = Various.getDicoById(item['type_result'])

                if type_res and type_res['short_label'].startswith("dico_"):
                    trans = type_res['short_label'][5:]
                    item['type_result'] = _(trans.strip())
                else:
                    item['type_result'] = ''

                # Value to be interpreted
                if item['type_result'] and item['result_value']:
                    if item['result_value'] != '0':
                        val = Various.getDicoById(item['result_value'])
                        trans = ''

                        if val and 'label' in val and val['label']:
                            trans = val['label']

                        if trans:
                            item['result_value'] = _(trans.strip())
                        else:
                            item['result_value'] = ''
                    else:
                        item['result_value'] = ''

            if 'ana_emergency' in item and item['ana_emergency'] and item['ana_emergency'] == 4:
                item['ana_emergency'] = 'Y'
            else:
                item['ana_emergency'] = 'N'

        self.log.info(Logs.fileline() + ' : TRACE DatasetByName')
        try:
            details = {"result": "SUCCESS", "name": name, "count": len(l_items) if l_items else 0}
            Audit.insertAudit(audit_user, "DatasetByName", "GENERAL", name, "SUCCESS", details, "R")
        except Exception as err:
            self.log.error(Logs.fileline() + ' : DatasetByName ERROR audit success err=' + str(err))
        return compose_ret(l_items, Constants.cst_content_type_json)
