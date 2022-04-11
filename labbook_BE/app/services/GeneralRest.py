import logging
import gettext

from datetime import datetime
from flask import request
from flask_restful import Resource

from app.models.General import *
from app.models.Logs import Logs
from app.models.Analysis import Analysis
from app.models.Patient import Patient
from app.models.Record import Record
from app.models.Result import Result
from app.models.Various import Various


class Test(Resource):
    log = logging.getLogger('log_services')

    def get(self):
        self.log.info(Logs.fileline() + ' : TRACE Test GET')
        return compose_ret('Test GET OK', Constants.cst_content_type_json)

    def post(self):
        self.log.info(Logs.fileline() + ' : TRACE Test POST')

        args = request.get_json()

        return compose_ret('args = ' + str(args), Constants.cst_content_type_json)


class DicoById(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_data):
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
            elif key == 'short_label' and dico[key] != "":
                dico[key] = _(dico[key].strip())

        self.log.info(Logs.fileline() + ' : TRACE DicoById : ' + str(id_data))
        return compose_ret(dico, Constants.cst_content_type_json)


class DefaultValue(Resource):
    log = logging.getLogger('log_services')

    def get(self, name):
        Various.useLangDB()

        val = Various.getDefaultValue(name)

        if not val:
            self.log.error(Logs.fileline() + ' : ERROR DefaultValue not found : ' + name)
            return compose_ret('', Constants.cst_content_type_json, 404)

        # Replace None by empty string
        for key, value in list(val.items()):
            if val[key] is None:
                val[key] = ''

        self.log.info(Logs.fileline() + ' : TRACE DefaultValue : ' + name)
        return compose_ret(val, Constants.cst_content_type_json)

    def post(self, name, value):
        ret = Various.updateDefaultValue(name, value)

        if ret is False:
            self.log.error(Logs.fileline() + ' : ERROR DefaultValue update identifiant : ' + name)
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE DefaultValue : ' + name)
        return compose_ret(ret, Constants.cst_content_type_json)


class InitVersion(Resource):
    log = logging.getLogger('log_services')

    def get(self):
        # check if need to init version
        ini = Various.getLastInitVersion()

        if ini['ini_stat'] == 'Y':
            if Various.updateTranslationsTable('en_GB'):
                Various.updateInitVersion(ini['ini_ser'], 'N')

        self.log.info(Logs.fileline() + ' : TRACE InitVersion ini_ser=' + str(ini['ini_ser']))
        return compose_ret('', Constants.cst_content_type_json)


class NationalityList(Resource):
    log = logging.getLogger('log_services')

    def get(self):
        l_items = Various.getNationalityList()

        if not l_items:
            self.log.error(Logs.fileline() + ' : ERROR NationalityList not found')
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
        return compose_ret(l_items, Constants.cst_content_type_json)


class DatasetByName(Resource):
    log = logging.getLogger('log_services')

    def post(self, name):
        args = request.get_json()

        if name == 'patient':
            l_items = Patient.getDataset()
        else:
            args = request.get_json()

            if not args or ('date_beg' not in args and 'date_end' not in args):
                self.log.error(Logs.fileline() + ' : DatasetByName args missing')
                return compose_ret('', Constants.cst_content_type_json, 500)

            # convert isodate format to ymd format
            date_beg = datetime.strptime(args['date_beg'], Constants.cst_isodate).strftime(Constants.cst_date_ymd)
            date_end = datetime.strptime(args['date_end'], Constants.cst_isodate).strftime(Constants.cst_date_ymd)

        if name == 'record':
            l_items = Record.getDataset(date_beg, date_end)
        elif name == 'analysis':
            l_items = Analysis.getDataset(date_beg, date_end)
        elif name == 'result':
            l_items = Result.getDataset(date_beg, date_end)

        if not l_items:
            self.log.error(Logs.fileline() + ' : ERROR dataset not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        import decimal

        Various.useLangDB()

        # self.log.error(Logs.fileline() + ' : DEBUG l_items=' + str(l_items))

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
        return compose_ret(l_items, Constants.cst_content_type_json)
