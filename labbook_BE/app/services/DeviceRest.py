# -*- coding:utf-8 -*-
import logging
import gettext

from datetime import datetime
from flask import request
from flask_restful import Resource

from app.models.General import compose_ret
from app.models.Constants import *
from app.models.Analyzer import *
from app.models.Record import *
from app.models.User import *
from app.models.DB import *
from app.models.Logs import Logs
from app.models.Various import Various


class AnalyzerList(Resource):
    log = logging.getLogger('log_services')

    def get(self):
        l_analyzers = Analyzer.getAnalyzerList()

        if not l_analyzers:
            self.log.error(Logs.fileline() + ' : TRACE AnalyzerList not found')

        self.log.info(Logs.fileline() + ' : TRACE AnalyzerList')
        return compose_ret(l_analyzers, Constants.cst_content_type_json)


class AnalyzerDet(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_analyzer):
        item = Analyzer.getAnalyzerDet(id_analyzer)

        if not item:
            self.log.error(Logs.fileline() + ' : ' + 'AnalyzerDet ERROR not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        # Replace None by empty string
        for key, value in list(item.items()):
            if item[key] is None:
                item[key] = ''

        self.log.info(Logs.fileline() + ' : AnalyzerDet id_analyzer=' + str(id_analyzer))
        return compose_ret(item, Constants.cst_content_type_json, 200)

    def post(self, id_analyzer):
        args = request.get_json()

        if 'id_user' not in args or 'rank' not in args or 'name' not in args or 'key' not in args or \
           'lab28' not in args or 'mapping' not in args or 'filename' not in args:
            self.log.error(Logs.fileline() + ' : AnalyzerDet ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # Update item
        if id_analyzer > 0:
            self.log.info(Logs.fileline() + ' : TRACE update AnalyzerDet')

            ret = Analyzer.updateAnalyzerDet(id_analyzer=id_analyzer,
                                             id_user=args['id_user'],
                                             rank=args['rank'],
                                             name=args['name'],
                                             id=args['key'],
                                             lab28=args['lab28'],
                                             mapping=args['mapping'],
                                             filename=args['filename'])

            if ret is False:
                self.log.error(Logs.alert() + ' : AnalyzerDet ERROR update')
                return compose_ret('', Constants.cst_content_type_json, 500)

        # Insert new item
        else:
            self.log.info(Logs.fileline() + ' : TRACE insert AnalyzerDet')
            ret = Analyzer.insertAnalyzerDet(id_user=args['id_user'],
                                             rank=args['rank'],
                                             name=args['name'],
                                             id=args['key'],
                                             lab28=args['lab28'],
                                             mapping=args['mapping'],
                                             filename=args['filename'])

            if ret <= 0:
                self.log.error(Logs.alert() + ' : AnalyzerDet ERROR  insert')
                return compose_ret('', Constants.cst_content_type_json, 500)

            id_analyzer = ret

        self.log.info(Logs.fileline() + ' : TRACE AnalyzerDet id_analyzer=' + str(id_analyzer))
        return compose_ret(id_analyzer, Constants.cst_content_type_json)

    def delete(self, id_analyzer):
        args = request.get_json()

        if args and 'id_user' in args:
            self.log.error(Logs.fileline() + ' : TRACE AnalyzerDet delete by id_user=' + str(args['id_user']))

        ret = Analyzer.deleteAnalyzer(id_analyzer)

        if not ret:
            self.log.error(Logs.fileline() + ' : TRACE AnalyzerDet delete ERROR')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE AnalyzerDet delete id_analyzer=' + str(id_analyzer))
        return compose_ret('', Constants.cst_content_type_json)


class AnalyzerFile(Resource):
    log = logging.getLogger('log_services')

    def get(self):
        l_analyzers = Analyzer.getAnalyzerFiles()

        if not l_analyzers:
            self.log.error(Logs.fileline() + ' : TRACE AnalyzerFile not found')

        self.log.info(Logs.fileline() + ' : TRACE AnalyzerFile')
        return compose_ret(l_analyzers, Constants.cst_content_type_json)


class AnalyzerLab27(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        msg_hl7 = request.data.decode('utf-8')

        if msg_hl7:
            self.log.info(Logs.fileline() + ' : TRACE AnalyzerLab27 msg_hl7 : ' + str(msg_hl7))

        # TODO

        self.log.info(Logs.fileline() + ' : TRACE AnalyzerLab27')
        return compose_ret('', Constants.cst_content_type_json)


class AnalyzerLab29(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        msg_hl7 = request.data.decode('utf-8')

        if msg_hl7:
            self.log.info(Logs.fileline() + ' : TRACE AnalyzerLab29 msg_hl7 : ' + str(msg_hl7))

        # save result in DB
        Analyzer.saveResult(msg_hl7)

        self.log.info(Logs.fileline() + ' : TRACE AnalyzerLab29')
        return compose_ret('', Constants.cst_content_type_json)
