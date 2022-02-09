# -*- coding:utf-8 -*-
import logging
import gettext

from datetime import datetime
from flask import request
from flask_restful import Resource

from app.models.General import compose_ret
from app.models.Constants import Constants
from app.models.File import File
from app.models.Logs import Logs


class FileDocList(Resource):
    log = logging.getLogger('log_services')

    def get(self, type_ref, ref):
        l_files = File.getFileDocList(type_ref, ref)

        if not l_files:
            self.log.error(Logs.fileline() + ' : TRACE FileDocList not found')

        for files in l_files:
            # Replace None by empty string
            for key, value in list(files.items()):
                if files[key] is None:
                    files[key] = ''

        self.log.info(Logs.fileline() + ' : TRACE FileDocList')
        return compose_ret(l_files, Constants.cst_content_type_json)


class FileDoc(Resource):
    log = logging.getLogger('log_services')

    def get(self, type_ref, ref):
        # ref= id_file
        filedata = File.getFileData(ref)

        if not filedata:
            self.log.error(Logs.fileline() + ' : TRACE FileDoc not found')

        filestorage = File.getFileStorage(filedata['id_storage'])

        if not filestorage:
            self.log.error(Logs.fileline() + ' : TRACE FileDoc storage not found')

        filedata['storage'] = filestorage['path']

        # Replace None by empty string
        for key, value in list(filedata.items()):
            if filedata[key] is None:
                filedata[key] = ''

        self.log.info(Logs.fileline() + ' : TRACE FileDoc')
        return compose_ret(filedata, Constants.cst_content_type_json)

    def post(self, type_ref, ref):
        # ref = id_rec
        args = request.get_json()

        if 'id_owner' not in args or 'original_name' not in args or 'generated_name' not in args or \
           'size' not in args or 'hash' not in args or 'ext' not in args or 'content_type' not in args or \
           'id_storage' not in args or 'end_path' not in args:
            self.log.error(Logs.fileline() + ' : TRACE FileDoc ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # insert into sigl_file_data
        ret = File.insertFileData(id_owner=args['id_owner'],
                                  original_name=args['original_name'],
                                  generated_name=args['generated_name'],
                                  size=args['size'],
                                  hash=args['hash'],
                                  ext=args['ext'],
                                  content_type=args['content_type'],
                                  id_storage=args['id_storage'],
                                  path=args['end_path'])

        if ret <= 0:
            self.log.error(Logs.alert() + ' : FileDoc ERROR insert FileData')
            return compose_ret('', Constants.cst_content_type_json, 500)

        res = {}
        res['id_file'] = ret

        # insert into sigl_XXXX__file_data
        ret = File.insertFileDoc(id_owner=args['id_owner'],
                                 id_ext=ref,
                                 id_file=res['id_file'],
                                 type_ref=type_ref)

        if ret <= 0:
            self.log.error(Logs.alert() + ' : FileDoc ERROR insert FileDoc')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE FileDoc')
        return compose_ret('', Constants.cst_content_type_json)

    def delete(self, type_ref, ref):
        # ref= id_file
        ret = File.deleteFileDoc(type_ref, ref)

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
        else:
            # Replace None by empty string
            for key, value in list(report.items()):
                if report[key] is None:
                    report[key] = ''

            if report['date']:
                report['date'] = datetime.strftime(report['date'], '%Y-%m-%d %H:%M:%S')

        self.log.info(Logs.fileline() + ' : TRACE FileReport')
        return compose_ret(report, Constants.cst_content_type_json)


class FileStorage(Resource):
    log = logging.getLogger('log_services')

    def get(self):
        storage = File.getLastFileStorage()

        if not storage:
            self.log.error(Logs.fileline() + ' : TRACE FileStorage not found')
            # We create a first storage
            ret = File.insertStorage(path=Constants.cst_storage)

            if ret <= 0:
                self.log.info(Logs.fileline() + ' : TRACE FileStorage ERROR insert storage')
                return compose_ret('', Constants.cst_content_type_json, 500)

            storage = File.getLastFileStorage()

        # Replace None by empty string
        for key, value in list(storage.items()):
            if storage[key] is None:
                storage[key] = ''

        self.log.info(Logs.fileline() + ' : TRACE FileStorage')
        return compose_ret(storage, Constants.cst_content_type_json)


class FileNbManual(Resource):
    log = logging.getLogger('log_services')

    def get(self):
        res = File.getFileNbManuals()

        if not res:
            self.log.error(Logs.fileline() + ' : TRACE FileNbManual not found')
            nb_manuals = 0
        else:
            nb_manuals = res['nb_manuals']

        self.log.info(Logs.fileline() + ' : TRACE FileNbManual')
        return compose_ret(nb_manuals, Constants.cst_content_type_json)
