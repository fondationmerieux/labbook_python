# -*- coding:utf-8 -*-
import logging

from datetime import datetime
from flask import request
from flask_restful import Resource

from app.models.General import compose_ret
from app.models.Constants import *
from app.models.Various import *
from app.models.File import *
from app.models.Logs import Logs
from app.models.User import *


class FileDoc(Resource):
    log = logging.getLogger('log_services')

    def get(self, ref):
        # ref= id_file
        filedoc = File.getFileDoc(ref)

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

    def post(self, ref):
        # ref = id_rec
        args = request.get_json()

        if 'id_owner' not in args or 'original_name' not in args or 'generated_name' not in args or 'size' not in args or \
           'hash' not in args or 'ext' not in args or 'content_type' not in args or 'id_storage' not in args or 'end_path' not in args:
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

        # Get id_group of lab with id_group of user
        id_group_lab = User.getUserGroupParent(args['id_owner'])

        if not id_group_lab:
            self.log.error(Logs.fileline() + ' : FileDoc ERROR group not found')
            return compose_ret('', Constants.cst_content_type_json, 500)

        # insert sigl_file_data_data_group
        ret = File.insertFileDataGroup(id_data=res['id_file'],
                                         id_group=id_group_lab['id_group_parent'])

        if ret <= 0:
            self.log.error(Logs.alert() + ' : FileDoc ERROR insert group')
            return compose_ret('', Constants.cst_content_type_json, 500)

        # insert into sigl_dos_valisedoc__file_data
        ret = File.insertFileDoc(id_owner=args['id_owner'],
                                 id_ext=ref,
                                 id_file=res['id_file'])

        if ret <= 0:
            self.log.error(Logs.alert() + ' : FileDoc ERROR insert FileDoc')
            return compose_ret('', Constants.cst_content_type_json, 500)

        res = {}
        res['id_data'] = ret

        # insert sigl_file_data_data_group
        ret = File.insertFileDocGroup(id_data=res['id_data'],
                                      id_group=id_group_lab['id_group_parent'])

        if ret <= 0:
            self.log.error(Logs.alert() + ' : FileDoc ERROR insert group')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE FileDoc')
        return compose_ret('', Constants.cst_content_type_json)

    def delete(self, ref):
        # ref= id_file
        ret = File.deleteFileDoc(ref)

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
            for key, value in report.items():
                if report[key] is None:
                    report[key] = ''

            if report['date']:
                report['date'] = datetime.strftime(report['date'], '%Y-%m-%d %H:%M:%S')

        self.log.info(Logs.fileline() + ' : TRACE FileReport')
        return compose_ret(report, Constants.cst_content_type_json)


class FileStorage(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_group):
        storage = File.getLastFileStorage()

        if not storage:
            self.log.error(Logs.fileline() + ' : TRACE FileStorage not found')
            # We create a first storage
            ret = File.insertStorage(id_owner=id_group, path='/space/applisdata/labbook/storage')

            if ret <= 0:
                self.log.info(Logs.fileline() + ' : TRACE FileStorage ERROR insert storage')
                return compose_ret('', Constants.cst_content_type_json, 500)

            storage = File.getLastFileStorage()

        # Replace None by empty string
        for key, value in storage.items():
            if storage[key] is None:
                storage[key] = ''

        self.log.info(Logs.fileline() + ' : TRACE FileStorage')
        return compose_ret(storage, Constants.cst_content_type_json)
