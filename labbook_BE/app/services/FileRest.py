# -*- coding:utf-8 -*-
import logging

from datetime import datetime
from flask_restful import Resource

from app.models.General import compose_ret
from app.models.Constants import *
from app.models.Various import *
from app.models.File import *
from app.models.Logs import Logs


class FileDoc(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_file):
        filedoc = File.getFileDoc(id_file)

        if not filedoc:
            self.log.error(Logs.fileline() + ' : TRACE FileDoc not found')

        filestorage = File.getFileStorage(filedoc['id_storage'])

        if not filestorage:
            self.log.error(Logs.fileline() + ' : TRACE FileDoc storage not found')

        filedoc['storage'] = filestorage['path']

        # Replace None by empty string
        for key, value in filedoc.items():
            if filedoc[key] is None:
                filedoc[key] = ''

        self.log.info(Logs.fileline() + ' : TRACE FileDoc')
        return compose_ret(filedoc, Constants.cst_content_type_json)

    def delete(self, id_file):
        ret = File.deleteFileDoc(id_file)

        if not ret:
            self.log.error(Logs.fileline() + ' : TRACE FileDoc delete ERROR')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE FileDoc delete')
        return compose_ret('', Constants.cst_content_type_json)


class FileReport(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_rec):
        report = File.getFileReport(id_rec)

        if not report:
            self.log.error(Logs.fileline() + ' : TRACE FileReport not found')

        # Replace None by empty string
        for key, value in report.items():
            if report[key] is None:
                report[key] = ''

        if report['date']:
            report['date'] = datetime.strftime(report['date'], '%Y-%m-%d %H:%M:%S')

        self.log.info(Logs.fileline() + ' : TRACE FileReport')
        return compose_ret(report, Constants.cst_content_type_json)
