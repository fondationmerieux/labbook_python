import logging
# import hashlib

# from datetime import datetime
from flask import request
from flask_restful import Resource

from app.models.General import *
from app.models.Logs import Logs
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


class DicoList(Resource):
    log = logging.getLogger('log_services')

    def get(self, dico_name):
        l_dico = Various.getDicoList(dico_name)

        if not l_dico:
            self.log.error(Logs.fileline() + ' : TRACE DicoList not found : ' + dico_name)
            l_dico = {}

        for dico in l_dico:
            # Replace None by empty string
            for key, value in dico.items():
                if dico[key] is None:
                    dico[key] = ''

        self.log.info(Logs.fileline() + ' : TRACE DicoList : ' + dico_name)
        return compose_ret(l_dico, Constants.cst_content_type_json)


class DicoById(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_data):
        dico = Various.getDicoById(id_data)

        if not dico:
            self.log.error(Logs.fileline() + ' : TRACE DicoById not found : ' + str(id_data))
            dico = {}

        # Replace None by empty string
        for key, value in dico.items():
            if dico[key] is None:
                dico[key] = ''

        self.log.info(Logs.fileline() + ' : TRACE DicoById : ' + str(id_data))
        return compose_ret(dico, Constants.cst_content_type_json)


class DefaultValue(Resource):
    log = logging.getLogger('log_services')

    def get(self, name):
        val = Various.getDefaultValue(name)

        if not val:
            self.log.error(Logs.fileline() + ' : ERROR DefaultValue not found : ' + name)
            return compose_ret('', Constants.cst_content_type_json, 404)

        # Replace None by empty string
        for key, value in val.items():
            if val[key] is None:
                val[key] = ''

        self.log.info(Logs.fileline() + ' : TRACE DefaultValue : ' + name)
        return compose_ret(val, Constants.cst_content_type_json)
