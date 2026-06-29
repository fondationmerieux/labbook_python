# -*- coding:utf-8 -*-
import logging
import gettext
import re
import csv
import os

from datetime import datetime
from flask import request
from flask_restful import Resource
from pathlib import Path

from app.models.General import compose_ret
from app.models.Constants import Constants
from app.models.Audit import Audit
from app.models.DB import DB
from app.models.Dict import Dict
from app.models.Logs import Logs
from app.models.Various import Various
from app.security.oauth_routes import require_oauth


class DictDescr(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self, dict_name):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        if 'dico_descr' not in args:
            self.log.error(Logs.fileline() + ' : DictDescr ERROR args missing')
            try:
                details = {"result": "ERROR", "reason": "ARGS_MISSING", "dict_name": str(dict_name)}
                Audit.insertAudit(audit_user, "DictDescr", "DICT", None, "ERROR", details, "U")
            except Exception:
                self.log.exception(Logs.fileline() + ' : DictDescr ERROR')
            return compose_ret('', Constants.cst_content_type_json, 400)

        ret = Dict.updateDescr(dict_name=dict_name, dico_descr=args['dico_descr'])

        if ret is False:
            self.log.info(Logs.fileline() + ' : TRACE DictDescr ERROR update dico_descr')
            try:
                details = {"result": "ERROR", "reason": "UPDATE_FAILED", "dict_name": str(dict_name)}
                Audit.insertAudit(audit_user, "DictDescr", "DICT", None, "ERROR", details, "U")
            except Exception:
                self.log.exception(Logs.fileline() + ' : DictDescr ERROR')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE DictDescr dict_name=' + str(dict_name))
        try:
            details = {"result": "SUCCESS", "dict_name": str(dict_name)}
            Audit.insertAudit(audit_user, "DictDescr", "DICT", None, "SUCCESS", details, "U")
        except Exception:
            self.log.exception(Logs.fileline() + ' : DictDescr ERROR audit success')
        return compose_ret('', Constants.cst_content_type_json)


class DictDet(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self, dict_name):
        audit_user = request.oauth_user
        l_dicts = Dict.getDictDetails(dict_name)

        if not l_dicts:
            self.log.error(Logs.fileline() + ' : TRACE DictDet no l_dicts')
            l_dicts = {}

        Various.useLangDB()

        for dict in l_dicts:
            # Replace None by empty string
            for key, value in list(dict.items()):
                if dict[key] is None:
                    dict[key] = ''
                elif key == 'label' and dict[key]:
                    dict[key] = _(dict[key].strip())
                elif key == 'short_label' and dict[key]:
                    dict[key] = _(dict[key].strip())
                elif key == 'dico_descr' and dict[key]:
                    dict[key] = _(dict[key].strip())

        self.log.info(Logs.fileline() + ' : TRACE DictDet')
        try:
            details = {"dict_name": str(dict_name), "count": len(l_dicts) if isinstance(l_dicts, list) else 0}
            Audit.insertAudit(audit_user, "DictDet", "DICT", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : DictDet ERROR audit success')
        return compose_ret(l_dicts, Constants.cst_content_type_json)

    @require_oauth()
    def post(self, dict_name):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        if 'list_val' not in args:
            self.log.error(Logs.fileline() + ' : DictDet ERROR args missing')
            try:
                details = {"reason": "ARGS_MISSING", "dict_name": str(dict_name), "missing": ["list_val"]}
                Audit.insertAudit(audit_user, "DictDet", "DICT", None, "ERROR", details, "U")
            except Exception:
                self.log.exception(Logs.fileline() + ' : DictDet ERROR')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # check if dict_name already exist
        dict = Dict.getDictDetails(dict_name)

        event_type = "U"

        # update dict
        if dict and dict[0]['dico_name'] == dict_name:
            self.log.error(Logs.fileline() + ' : DictDet UPDATE dict')

            for val in args['list_val']:
                if val['id_data'] > 0:
                    ret = Dict.updateDict(id_data=val['id_data'],
                                          label=val['label'],
                                          short_label=val['short_label'],
                                          position=val['position'],
                                          code=val['code'],
                                          dict_formatting=val['formatting'])
                else:
                    ret = Dict.insertDict(id_owner=val['id_owner'],
                                          dico_name=dict_name,
                                          label=val['label'],
                                          short_label=val['short_label'],
                                          position=val['position'],
                                          code=val['code'],
                                          dict_formatting=val['formatting'])

                    event_type = "C"

                if ret is False or ret <= 0:
                    self.log.info(Logs.fileline() + ' : TRACE DictDet ERROR update val dict')
                    try:
                        details = {"reason": "UPDATE_FAILED", "dict_name": str(dict_name)}
                        Audit.insertAudit(audit_user, "DictDet", "DICT", None, "ERROR", details, event_type)
                    except Exception:
                        self.log.exception(Logs.fileline() + ' : DictDet ERROR')
                    return compose_ret('', Constants.cst_content_type_json, 500)

            # delete missing values compared to dict
            for db_val in dict:
                exist = False
                for ihm_val in args['list_val']:
                    if db_val['id_data'] == ihm_val['id_data']:
                        exist = True

                if not exist:
                    ret = Dict.deleteDictValue(db_val['id_data'])

                    if ret is False:
                        self.log.info(Logs.fileline() + ' : TRACE DictDet ERROR delete val dict')
                        try:
                            details = {"reason": "DELETE_FAILED", "dict_name": str(dict_name), "id_data": int(db_val['id_data'])}
                            Audit.insertAudit(audit_user, "DictDet", "DICT", None, "ERROR", details, "D")
                        except Exception:
                            self.log.exception(Logs.fileline() + ' : DictDet ERROR')
                        return compose_ret('', Constants.cst_content_type_json, 500)

        # insert new dict
        else:
            self.log.error(Logs.fileline() + ' : DictDet INSERT dict')

            for val in args['list_val']:
                # insert in sigl_dico_data
                ret = Dict.insertDict(id_owner=val['id_owner'],
                                      dico_name=dict_name,
                                      label=val['label'],
                                      short_label=val['short_label'],
                                      position=val['position'],
                                      code=val['code'],
                                      dict_formatting=val['formatting'])

                event_type = "C"

                if ret <= 0:
                    self.log.error(Logs.alert() + ' : DictDet ERROR insert dict')
                    try:
                        details = {"reason": "INSERT_FAILED", "dict_name": str(dict_name)}
                        Audit.insertAudit(audit_user, "DictDet", "DICT", None, "ERROR", details, "C")
                    except Exception:
                        self.log.exception(Logs.fileline() + ' : DictDet ERROR')
                    return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE DictDet dict_name=' + str(dict_name))
        try:
            details = {"dict_name": str(dict_name)}
            Audit.insertAudit(audit_user, "DictDet", "DICT", None, "SUCCESS", details, event_type)
        except Exception:
            self.log.exception(Logs.fileline() + ' : DictDet ERROR audit success')
        return compose_ret('', Constants.cst_content_type_json)

    @require_oauth()
    def delete(self, dict_name):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        if 'id_owner' not in args:
            self.log.error(Logs.fileline() + ' : DictDet ERROR args missing')
            try:
                details = {"reason": "ARGS_MISSING", "dict_name": str(dict_name), "missing": ["id_owner"]}
                Audit.insertAudit(audit_user, "DictDet", "DICT", None, "ERROR", details, "D")
            except Exception:
                self.log.exception(Logs.fileline() + ' : DictDet ERROR')
            return compose_ret('', Constants.cst_content_type_json, 400)

        ret = Dict.deleteDict(dict_name)

        if ret is False:
            self.log.info(Logs.fileline() + ' : TRACE DictDet ERROR delete dict')
            try:
                details = {"reason": "DELETE_FAILED", "dict_name": str(dict_name)}
                Audit.insertAudit(audit_user, "DictDet", "DICT", None, "ERROR", details, "D")
            except Exception:
                self.log.exception(Logs.fileline() + ' : DictDet ERROR')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE DictDet delete dict_name=' + str(dict_name))
        try:
            details = {"dict_name": str(dict_name)}
            Audit.insertAudit(audit_user, "DictDet", "DICT", None, "SUCCESS", details, "D")
        except Exception:
            self.log.exception(Logs.fileline() + ' : DictDet ERROR audit success')
        return compose_ret('', Constants.cst_content_type_json)


class DictDetById(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self, id_dict):
        audit_user = request.oauth_user
        l_dicts = Dict.getDictDetailsById(id_dict)

        if not l_dicts:
            self.log.error(Logs.fileline() + ' : TRACE DictDetById no l_dicts')
            l_dicts = {}

        Various.useLangDB()

        for dict in l_dicts:
            # Replace None by empty string
            for key, value in list(dict.items()):
                if dict[key] is None:
                    dict[key] = ''
                elif key == 'label' and dict[key]:
                    dict[key] = _(dict[key].strip())
                elif key == 'short_label' and dict[key]:
                    dict[key] = _(dict[key].strip())
                elif key == 'dico_descr' and dict[key]:
                    dict[key] = _(dict[key].strip())

        self.log.info(Logs.fileline() + ' : TRACE DictDetById id_dict=' + str(id_dict))
        try:
            details = {"id_dict": int(id_dict), "count": len(l_dicts) if isinstance(l_dicts, list) else 0}
            Audit.insertAudit(audit_user, "DictDetById", "DICT", int(id_dict), "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : DictDetById ERROR audit success')
        return compose_ret(l_dicts, Constants.cst_content_type_json)


class DictList(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self):
        audit_user = request.oauth_user
        args = request.get_json()

        if not args:
            args = {}

        l_dicts = Dict.getDictList(args)

        if not l_dicts:
            self.log.error(Logs.fileline() + ' : TRACE DictList not found')

        Various.useLangDB()

        for dict in l_dicts:
            # Replace None by empty string
            for key, value in list(dict.items()):
                if dict[key] is None:
                    dict[key] = ''
                elif key == 'name' and dict[key]:
                    trans = dict[key].strip()
                    dict['key'] = trans        # keep key untranslated to get details of this dict
                    dict[key]   = _(trans)     # dict name translated

        self.log.info(Logs.fileline() + ' : TRACE DictList')
        try:
            details = {"count": len(l_dicts) if l_dicts else 0}
            Audit.insertAudit(audit_user, "DictList", "DICT", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : DictList ERROR audit success')
        return compose_ret(l_dicts, Constants.cst_content_type_json)


class DictExport(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        l_data = [['version', 'id_data', 'id_owner', 'dico_name', 'label', 'short_label', 'position', 'code',
                   'dico_descr', 'dict_formatting']]

        if 'id_user' not in args or 'dico_name' not in args:
            self.log.error(Logs.fileline() + ' : DictExport ERROR args missing')
            try:
                details = {"reason": "ARGS_MISSING", "missing": ["id_user", "dico_name"]}
                Audit.insertAudit(audit_user, "DictExport", "DICT", None, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : DictExport ERROR')
            return compose_ret('', Constants.cst_content_type_json, 400)

        Various.useLangDB()

        dico_name = args['dico_name']

        dict_data = Dict.getDictExport(dico_name)

        if dict_data:
            for d in dict_data:
                data = []

                data.append('v1')

                # ANALYSIS
                if d['id_data']:
                    data.append(d['id_data'])
                else:
                    data.append('')

                if d['id_owner']:
                    data.append(d['id_owner'])
                else:
                    data.append('')

                if d['dico_name']:
                    name = d['dico_name']
                    data.append(_(name.strip()))
                else:
                    data.append('')

                if d['label']:
                    label = d['label']
                    data.append(_(label.strip()))
                else:
                    data.append('')

                if d['short_label']:
                    short_label = d['short_label']
                    data.append(_(short_label.strip()))
                else:
                    data.append('')

                if d['position']:
                    data.append(d['position'])
                else:
                    data.append('')

                if d['code']:
                    data.append(d['code'])
                else:
                    data.append('')

                if d['dico_descr']:
                    dico_descr = d['dico_descr']
                    data.append(_(dico_descr.strip()))
                else:
                    data.append('')

                if d['dict_formatting']:
                    data.append(d['dict_formatting'])
                else:
                    data.append('N')

                l_data.append(data)

        # if no result to export
        if len(l_data) < 2:
            try:
                details = {"reason": "NOT_FOUND", "dico_name": str(dico_name)}
                Audit.insertAudit(audit_user, "DictExport", "DICT", None, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : DictExport ERROR')
            return compose_ret('', Constants.cst_content_type_json, 404)

        # write csv file
        try:
            today = datetime.now().strftime("%Y%m%d")

            raw = str(dico_name) if dico_name else ''
            safe = re.sub(Constants.cst_safe_pattern, '_', raw).strip('_')
            suffix = f"-{safe}" if safe else ""

            filename = f"dict{suffix}_{today}.csv"

            tmp_dir = Path("tmp")
            tmp_dir.mkdir(parents=True, exist_ok=True)

            file_path = tmp_dir / filename
            with file_path.open(mode="w", encoding="utf-8", newline="") as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerows(l_data)

        except Exception as err:
            self.log.exception(Logs.fileline() + ' : ERROR post DictExport failed')
            try:
                details = {"reason": "EXCEPTION", "err": str(err), "dico_name": args.get("dico_name")}
                Audit.insertAudit(audit_user, "DictExport", "DICT", None, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : DictExport ERROR audit')
            return False

        self.log.info(Logs.fileline() + ' : TRACE DictExport')
        try:
            details = {"dico_name": str(dico_name), "filename": filename, "count": len(l_data) - 1}
            Audit.insertAudit(audit_user, "DictExport", "DICT", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : DictExport ERROR audit success')
        return compose_ret('', Constants.cst_content_type_json)


class DictImport(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self, filename, id_user):
        audit_user = request.oauth_user

        if not filename or id_user <= 0:
            self.log.error(Logs.fileline() + ' : DictImport ERROR args missing')
            try:
                details = {"reason": "ARGS_MISSING", "filename": str(filename), "id_user": int(id_user)}
                Audit.insertAudit(audit_user, "DictImport", "DICT", None, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : DictImport ERROR')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # Read CSV user
        path = Constants.cst_path_tmp

        with open(os.path.join(path, filename), 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';', quotechar='"')
            l_rows = list(csv_reader)

        # clean double quotes
        l_rows = [[col.strip('"') if col else col for col in row] for row in l_rows]

        if not l_rows or len(l_rows) < 2:
            self.log.error(Logs.fileline() + ' : TRACE DictImport ERROR file empty')
            DB.insertDbStatus(stat='ERR;DictImport ERROR file empty', type='DIC')
            try:
                details = {"reason": "FILE_EMPTY", "filename": str(filename), "id_user": int(id_user)}
                Audit.insertAudit(audit_user, "DictImport", "DICT", None, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : DictImport ERROR')
            return compose_ret('', Constants.cst_content_type_json, 500)

        head_line = l_rows[0]

        # remove headers line
        l_rows.pop(0)

        # check version
        if l_rows[0][0] != 'v1':
            self.log.error(Logs.fileline() + ' : TRACE DictImport ERROR wrong version')
            DB.insertDbStatus(stat='ERR;DictImport ERROR wrong version', type='DIC')
            try:
                details = {"reason": "WRONG_VERSION", "filename": str(filename), "id_user": int(id_user), "version": str(l_rows[0][0])}
                Audit.insertAudit(audit_user, "DictImport", "DICT", None, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : DictImport ERROR')
            return compose_ret('', Constants.cst_content_type_json, 409)

        # check name of column
        head_list = ['version', 'id_data', 'id_owner', 'dico_name', 'label', 'short_label', 'position', 'code',
                     'dico_descr', 'dict_formatting']

        i = 0
        for head in head_line:
            if head != head_list[i]:
                self.log.error(Logs.fileline() + ' : TRACE DictImport ERROR wrong column or order : ' + str(head))
                DB.insertDbStatus(stat='ERR;DictImport ERROR wrong column or order', type='DIC')
                try:
                    details = {"reason": "WRONG_COLUMNS", "filename": str(filename), "id_user": int(id_user), "bad_head": str(head)}
                    Audit.insertAudit(audit_user, "DictImport", "DICT", None, "ERROR", details, "R")
                except Exception:
                    self.log.exception(Logs.fileline() + ' : DictImport ERROR')
                return compose_ret('', Constants.cst_content_type_json, 409)
            i = i + 1

        i = 1
        for row in l_rows:
            i = i + 1
            self.log.info(Logs.fileline() + ' : DEBUG-TRACE IMPORT LINE ' + str(i) + ' #############')
            self.log.info(Logs.fileline() + ' : DEBUG-TRACE IMPORT row=' + str(row))
            if row:
                id_data            = row[1]
                id_owner           = row[2]
                dico_name          = row[3]
                label              = row[4]
                short_label        = row[5]
                position           = row[6]
                code               = row[7]
                dico_descr         = row[8]
                dict_formatting    = row[9]

                # inser dictt
                if not id_data or int(id_data) == 0:
                    self.log.info(Logs.fileline() + ' : DEBUG-TRACE IMPORT insert dict dico_name=' + dico_name)
                    ret = Dict.insertDict(id_owner=id_owner,
                                          dico_name=dico_name,
                                          label=label,
                                          short_label=short_label,
                                          position=position,
                                          code=code,
                                          dict_formatting=dict_formatting)

                    if ret <= 0:
                        self.log.info(Logs.fileline() + ' : TRACE DictImport ERROR insert dict dico_name ' + str(dico_name) + ' | csv_line=' + str(i))
                        DB.insertDbStatus(stat='ERR;DictImport ERROR insert dict dico_name: ' + str(dico_name), type='DIC')
                        try:
                            details = {"reason": "INSERT_FAILED", "filename": str(filename), "id_user": int(id_user),
                                       "dico_name": str(dico_name), "csv_line": int(i)}
                            Audit.insertAudit(audit_user, "DictImport", "DICT", None, "ERROR", details, "R")
                        except Exception:
                            self.log.exception(Logs.fileline() + ' : DictImport ERROR')
                        return compose_ret('', Constants.cst_content_type_json, 500)

                # update dict
                elif int(id_data) > 0:
                    self.log.info(Logs.fileline() + ' : DEBUG-TRACE IMPORT update dict id_data=' + str(id_data))
                    ret = Dict.updateDict(id_data=id_data,
                                          label=label,
                                          short_label=short_label,
                                          position=position,
                                          code=code,
                                          dict_formatting=dict_formatting)

                    if ret is False:
                        self.log.info(Logs.fileline() + ' : TRACE DictImport ERROR update dict id_data ' + str(id_data) + ' | csv_line=' + str(i))
                        DB.insertDbStatus(stat='ERR;DictImport ERROR update dict id_data=' + str(id_data) + ' dico_name: ' + str(dico_name), type='DIC')
                        try:
                            details = {"reason": "UPDATE_FAILED", "filename": str(filename), "id_user": int(id_user),
                                       "id_data": int(id_data), "dico_name": str(dico_name), "csv_line": int(i)}
                            Audit.insertAudit(audit_user, "DictImport", "DICT", None, "ERROR", details, "R")
                        except Exception:
                            self.log.exception(Logs.fileline() + ' : DictImport ERROR')
                        return compose_ret('', Constants.cst_content_type_json, 500)

                # update dict descr
                ret = Dict.updateDescr(dict_name=dico_name, dico_descr=dico_descr)

                if ret is False:
                    self.log.info(Logs.fileline() + ' : TRACE DictDescr ERROR update dico_descr')
                    DB.insertDbStatus(stat='ERR;DictImport ERROR insert dict descr: ' + str(dico_descr), type='DIC')
                    try:
                        details = {"reason": "UPDATE_DESCR_FAILED", "filename": str(filename), "id_user": int(id_user),
                                   "dico_name": str(dico_name), "csv_line": int(i)}
                        Audit.insertAudit(audit_user, "DictImport", "DICT", None, "ERROR", details, "R")
                    except Exception:
                        self.log.exception(Logs.fileline() + ' : DictImport ERROR')
                    return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE DictImport')
        DB.insertDbStatus(stat='OK;DictImport ended OK', type='DIC')
        try:
            details = {"filename": str(filename), "id_user": int(id_user), "count": len(l_rows)}
            Audit.insertAudit(audit_user, "DictImport", "DICT", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : DictImport ERROR audit success')
        return compose_ret('', Constants.cst_content_type_json, 200)
