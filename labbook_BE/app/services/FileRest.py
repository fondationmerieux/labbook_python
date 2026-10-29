# -*- coding:utf-8 -*-
import logging

from datetime import datetime
from flask import request
from flask_restful import Resource

from app.models.General import compose_ret
from app.models.Constants import Constants
from app.models.Audit import Audit
from app.models.File import File
from app.models.Logs import Logs
from app.models.Record import Record
from app.models.User import User
from app.security.oauth_routes import require_oauth


# Names exported when this module is imported with "*" (see app/__init__.py).
# Without __all__, "import *" also brings in this module's own imports
# (Constants, datetime, logging...) and they leak into the caller.
__all__ = [
    'FileDocList',
    'FileDoc',
    'FileReport',
    'FileReportCopy',
    'FileReportNbDL',
    'FileStorage',
    'FileNbManual',
]


class FileDocList(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self, type_ref, ref):
        """
        Return the documents attached to an item.

        Args:
            type_ref (str): kind of owner, REC record, EQxx equipment, USxx user, MANU, PROC, MEET, CTRL, MSG, SIGN...
            ref (int): id of the item.

        Returns:
            200: list of documents, None replaced by ''.
        """
        audit_user = request.oauth_user

        # a prescriber only reads his own records
        id_pres = User.getCallerPrescriber(audit_user)
        if type_ref == 'REC' and id_pres is not None and not Record.isRecordOfPrescriber(ref, id_pres):
            self.log.error(Logs.fileline() + ' : FileDocList ERROR record of another prescriber ref=' + str(ref))
            return compose_ret('', Constants.cst_content_type_json, 403)

        l_files = File.getFileDocList(type_ref, ref)

        if not l_files:
            self.log.info(Logs.fileline() + ' : TRACE FileDocList not found')

        for files in l_files:
            # Replace None by empty string
            for key, value in list(files.items()):
                if files[key] is None:
                    files[key] = ''

        self.log.info(Logs.fileline() + ' : TRACE FileDocList')
        try:
            details = {"result": "SUCCESS", "action": "QUERY", "type_ref": type_ref, "ref": str(ref), "count": len(l_files) if l_files else 0}
            Audit.insertAudit(audit_user, "FileDocList", "FILE", None, "SUCCESS", details, "R")
        except Exception as err:
            self.log.error(Logs.fileline() + ' : FileDocList ERROR audit success err=' + str(err))
        return compose_ret(l_files, Constants.cst_content_type_json)


class FileDoc(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self, type_ref, ref):
        """
        Return the details of one document with its storage path.

        Args:
            type_ref (str): kind of owner, REC record, EQxx equipment, USxx user, MANU, PROC, MEET, CTRL, MSG, SIGN...
            ref (int): document id (id_file), not the item id.

        Returns:
            200: document fields, storage path in 'storage'.
            404: document or its storage not found.
        """
        audit_user = request.oauth_user
        # ref = id_file
        filedata = File.getFileData(ref)

        if not filedata:
            self.log.error(Logs.fileline() + ' : TRACE FileDoc not found')
            try:
                details = {"result": "ERROR", "reason": "NOT_FOUND", "id_file": str(ref), "type_ref": type_ref}
                Audit.insertAudit(audit_user, "FileDoc", "FILE", int(ref), "ERROR", details, "R")
            except Exception as err:
                self.log.error(Logs.fileline() + ' : FileDoc ERROR audit not found err=' + str(err))
            return compose_ret(filedata, Constants.cst_content_type_json, 404)

        filestorage = File.getFileStorage(filedata['id_storage'])

        if not filestorage:
            self.log.error(Logs.fileline() + ' : TRACE FileDoc storage not found')
            try:
                details = {"result": "ERROR", "reason": "NOT_FOUND", "id_file": str(ref),
                           "id_storage": filedata.get('id_storage'), "type_ref": type_ref}
                Audit.insertAudit(audit_user, "FileDoc", "FILE", int(ref), "ERROR", details, "R")
            except Exception as err:
                self.log.error(Logs.fileline() + ' : FileDoc ERROR audit storage not found err=' + str(err))
            return compose_ret(filedata, Constants.cst_content_type_json, 404)

        filedata['storage'] = filestorage['path']

        # Replace None by empty string
        for key, value in list(filedata.items()):
            if filedata[key] is None:
                filedata[key] = ''

        self.log.info(Logs.fileline() + ' : TRACE FileDoc')
        try:
            details = {"result": "SUCCESS", "action": "VIEW", "id_file": str(ref)}
            Audit.insertAudit(audit_user, "FileDoc", "FILE", int(ref), "SUCCESS", details, "R")
        except Exception as err:
            self.log.error(Logs.fileline() + ' : FileDoc ERROR audit success err=' + str(err))
        return compose_ret(filedata, Constants.cst_content_type_json)

    @require_oauth()
    def post(self, type_ref, ref):
        """
        Register a file already written to disk and attach it to an item.

        Args:
            type_ref (str): kind of owner, REC record, EQxx equipment, USxx user, MANU, PROC, MEET, CTRL, MSG, SIGN...
            ref (int): id of the item.

        Body:
            id_owner, original_name, generated_name, size, hash, ext, content_type, id_storage,
            end_path: file fields, all required.

        Returns:
            200: empty body.
            400: a field is missing.
            500: database write failed.
        """
        audit_user = request.oauth_user
        # ref = id_rec
        args = request.get_json()

        if 'id_owner' not in args or 'original_name' not in args or 'generated_name' not in args or \
           'size' not in args or 'hash' not in args or 'ext' not in args or 'content_type' not in args or \
           'id_storage' not in args or 'end_path' not in args:
            self.log.error(Logs.fileline() + ' : TRACE FileDoc ERROR args missing')
            try:
                details = {"result": "ERROR", "reason": "ARGS_MISSING", "action": "INSERT", "type_ref": type_ref, "id_ext": str(ref)}
                Audit.insertAudit(audit_user, "FileDoc", "FILE", None, "ERROR", details, "E")
            except Exception as err:
                self.log.error(Logs.fileline() + ' : FileDoc ERROR audit args missing err=' + str(err))
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
            try:
                details = {"result": "ERROR", "reason": "INSERT_FAILED", "action": "INSERT", "step": "insertFileData",
                           "type_ref": type_ref, "id_ext": str(ref), "id_owner": args.get('id_owner')}
                Audit.insertAudit(audit_user, "FileDoc", "FILE", None, "ERROR", details, "C")
            except Exception as err:
                self.log.error(Logs.fileline() + ' : FileDoc ERROR audit insertFileData err=' + str(err))
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
            try:
                details = {"result": "ERROR", "reason": "INSERT_FAILED", "action": "INSERT", "step": "insertFileDoc",
                           "type_ref": type_ref, "id_ext": str(ref), "id_file": int(res.get('id_file') or 0),
                           "id_owner": args.get('id_owner')}
                Audit.insertAudit(audit_user, "FileDoc", "FILE", int(res.get('id_file') or 0) if res.get('id_file') else None, "ERROR", details, "C")
            except Exception as err:
                self.log.error(Logs.fileline() + ' : FileDoc ERROR audit insertFileDoc err=' + str(err))
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE FileDoc')
        try:
            details = {"result": "SUCCESS", "action": "INSERT", "type_ref": type_ref, "id_ext": str(ref), "id_file": int(res.get('id_file') or 0), "id_owner": args.get('id_owner')}
            Audit.insertAudit(audit_user, "FileDoc", "FILE", int(res.get('id_file') or 0) if res.get('id_file') else None, "SUCCESS", details, "C")
        except Exception as err:
            self.log.error(Logs.fileline() + ' : FileDoc ERROR audit success err=' + str(err))
        return compose_ret('', Constants.cst_content_type_json)

    @require_oauth()
    def delete(self, type_ref, ref):
        """
        Detach a document from its item. The file and its sigl_file_data row are kept.

        Args:
            type_ref (str): kind of owner, REC record, EQxx equipment, USxx user, MANU, PROC, MEET, CTRL, MSG, SIGN...
            ref (int): document id (id_file).

        Returns:
            200: empty body.
            500: deletion failed or unknown type_ref.
        """
        audit_user = request.oauth_user
        # ref= id_file
        ret = File.deleteFileDoc(type_ref, ref)

        if not ret:
            self.log.error(Logs.fileline() + ' : TRACE FileDoc delete ERROR')
            try:
                details = {"result": "ERROR", "reason": "DELETE_FAILED", "type_ref": type_ref, "ref": str(ref)}
                Audit.insertAudit(audit_user, "FileDoc", "FILE", None, "ERROR", details, "D")
            except Exception as e:
                self.log.error(Logs.fileline() + " : FileDoc DELETE audit error " + str(e))
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE FileDoc delete')
        try:
            details = {"result": "SUCCESS", "action": "DELETE", "type_ref": type_ref, "ref": str(ref)}
            Audit.insertAudit(audit_user, "FileDoc", "FILE", None, "SUCCESS", details, "D")
        except Exception as e:
            self.log.error(Logs.fileline() + " : FileDoc DELETE audit error " + str(e))
        return compose_ret('', Constants.cst_content_type_json)


class FileReport(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self, id_rec):
        """
        Return the reports generated for a record.

        Args:
            id_rec (int): record id.

        Returns:
            200: list of reports with date, template name and download count.
        """
        audit_user = request.oauth_user

        # a prescriber only reads his own records
        id_pres = User.getCallerPrescriber(audit_user)
        if id_pres is not None and not Record.isRecordOfPrescriber(id_rec, id_pres):
            self.log.error(Logs.fileline() + ' : FileReport ERROR record of another prescriber id_rec=' + str(id_rec))
            return compose_ret('', Constants.cst_content_type_json, 403)

        l_report = File.getAllFileReport(id_rec)

        if not l_report:
            self.log.error(Logs.fileline() + ' : TRACE FileReport not found')
        else:
            for report in l_report:
                # Replace None by empty string
                for key, value in list(report.items()):
                    if report[key] is None:
                        report[key] = ''

                if report['date']:
                    report['date'] = datetime.strftime(report['date'], '%Y-%m-%d %H:%M:%S')

        self.log.info(Logs.fileline() + ' : TRACE FileReport')
        try:
            details = {"result": "SUCCESS", "id_rec": str(id_rec)}
            Audit.insertAudit(audit_user, "FileReport", "FILE", None, "SUCCESS", details, "R")
        except Exception as e:
            self.log.error(Logs.fileline() + " : FileReport QUERY audit error " + str(e))
        return compose_ret(l_report, Constants.cst_content_type_json)


class FileReportCopy(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self, filename, copy_name):
        """
        Write a copy of a report to the tmp directory, with a DUPLICATA watermark on every page.

        Args:
            filename (str): report file name, in the report directory.
            copy_name (str): name of the copy.

        Returns:
            200: empty body.
            500: copy failed.
        """
        audit_user = request.oauth_user
        ret = File.copyReport(filename, copy_name)

        if ret is False:
            self.log.error(Logs.fileline() + ' : TRACE FileReportCopy ERROR')
            try:
                details = {"result": "ERROR", "reason": "COPY_FAILED", "action": "COPY", "filename": filename, "copy_name": copy_name}
                Audit.insertAudit(audit_user, "FileReportCopy", "FILE", None, "ERROR", details, "E")
            except Exception as err:
                self.log.error(Logs.fileline() + ' : FileReportCopy ERROR audit err=' + str(err))
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE FileReportCopy')
        try:
            details = {"result": "SUCCESS", "action": "COPY", "filename": filename, "copy_name": copy_name}
            Audit.insertAudit(audit_user, "FileReportCopy", "FILE", None, "SUCCESS", details, "E")
        except Exception as err:
            self.log.error(Logs.fileline() + ' : FileReportCopy ERROR audit success err=' + str(err))
        return compose_ret('', Constants.cst_content_type_json)


class FileReportNbDL(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self, filename):
        """
        Add one to the download count of a report.

        Args:
            filename (str): report file name.

        Returns:
            200: empty body.
            500: update failed.
        """
        audit_user = request.oauth_user
        ret = File.raiseReportNbDL(filename)

        if ret is False:
            self.log.error(Logs.fileline() + ' : TRACE FileReportNbDL ERROR update raiseReportNbDL')
            try:
                details = {"result": "ERROR", "reason": "UPDATE_FAILED", "action": "UPDATE", "filename": filename, "step": "raiseReportNbDL"}
                Audit.insertAudit(audit_user, "FileReportNbDL", "FILE", None, "ERROR", details, "U")
            except Exception as err:
                self.log.error(Logs.fileline() + ' : FileReportNbDL ERROR audit err=' + str(err))
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE FileReportNbDL')
        try:
            details = {"result": "SUCCESS", "action": "UPDATE", "filename": filename, "step": "raiseReportNbDL"}
            Audit.insertAudit(audit_user, "FileReportNbDL", "FILE", None, "SUCCESS", details, "U")
        except Exception as err:
            self.log.error(Logs.fileline() + ' : FileReportNbDL ERROR audit success err=' + str(err))
        return compose_ret('', Constants.cst_content_type_json)


class FileStorage(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self):
        """
        Return the current storage, created on first call when none exists.

        Returns:
            200: storage fields.
            500: storage could not be created.
        """
        audit_user = request.oauth_user
        storage = File.getLastFileStorage()

        if not storage:
            self.log.error(Logs.fileline() + ' : TRACE FileStorage not found')
            # We create a first storage
            ret = File.insertStorage(path=Constants.cst_storage)

            if ret <= 0:
                self.log.error(Logs.fileline() + ' : TRACE FileStorage ERROR insert storage')
                try:
                    details = {"result": "ERROR", "reason": "INSERT_FAILED", "action": "INSERT",
                               "path": Constants.cst_storage, "step": "insertStorage"}
                    Audit.insertAudit(audit_user, "FileStorage", "FILE", None, "ERROR", details, "C")
                except Exception as err:
                    self.log.error(Logs.fileline() + ' : FileStorage ERROR audit insert err=' + str(err))
                return compose_ret('', Constants.cst_content_type_json, 500)

            storage = File.getLastFileStorage()

        # Replace None by empty string
        for key, value in list(storage.items()):
            if storage[key] is None:
                storage[key] = ''

        self.log.info(Logs.fileline() + ' : TRACE FileStorage')
        try:
            details = {"result": "SUCCESS", "action": "QUERY", "id_storage": int(storage.get('id_storage') or 0)}
            Audit.insertAudit(audit_user, "FileStorage", "FILE", int(storage.get('id_storage') or 0) if storage.get('id_storage') else None, "SUCCESS", details, "R")
        except Exception as err:
            self.log.error(Logs.fileline() + ' : FileStorage ERROR audit success err=' + str(err))
        return compose_ret(storage, Constants.cst_content_type_json)


class FileNbManual(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self):
        """
        Return the number of quality manuals.

        Returns:
            200: count as a raw scalar.
        """
        audit_user = request.oauth_user
        res = File.getFileNbManuals()

        if not res:
            self.log.error(Logs.fileline() + ' : TRACE FileNbManual not found')
            nb_manuals = 0
        else:
            nb_manuals = res['nb_manuals']

        self.log.info(Logs.fileline() + ' : TRACE FileNbManual')
        try:
            details = {"result": "SUCCESS", "action": "QUERY", "nb_manuals": int(nb_manuals)}
            Audit.insertAudit(audit_user, "FileNbManual", "FILE", None, "SUCCESS", details, "R")
        except Exception as err:
            self.log.error(Logs.fileline() + ' : FileNbManual ERROR audit success err=' + str(err))
        return compose_ret(nb_manuals, Constants.cst_content_type_json)
