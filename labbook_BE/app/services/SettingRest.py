# -*- coding:utf-8 -*-
import logging
import os
import subprocess
import csv
import re

from datetime import datetime
from flask import request
from flask_restful import Resource

from app.models.Audit import Audit
from app.models.General import compose_ret
from app.models.Constants import Constants
from app.models.Logs import Logs
from app.models.Quality import Quality
from app.models.Setting import Setting
from app.models.Various import Various
from app.security.oauth_routes import require_oauth


# Names exported when this module is imported with "*" (see app/__init__.py).
# Without __all__, "import *" also brings in this module's own imports
# (Constants, datetime, logging...) and they leak into the caller.
__all__ = [
    'SettingAgeInterval',
    'SettingReqServices',
    'SettingFuncUnitDet',
    'SettingFuncUnit',
    'SettingLinkUnit',
    'SettingLinkByUser',
    'SettingPref',
    'SettingRecNum',
    'SettingReport',
    'SettingBackup',
    'ScriptBackup',
    'ScriptGenkey',
    'ScriptInitMedia',
    'ScriptKeyexist',
    'ScriptListarchive',
    'ScriptListmedia',
    'ScriptProgbackup',
    'ScriptRestart',
    'ScriptRestore',
    'ScriptStatus',
    'TemplateList',
    'TemplateDet',
    'ZipCityAdd',
    'ZipCityDelAll',
    'ZipCityDet',
    'ZipCityList',
    'ZipCitySearch',
    'SettingStock',
    'SettingFormList',
    'SettingFormDet',
    'SettingManual',
    'SettingManualCat',
    'SettingDHIS2List',
    'SettingDHIS2Det',
    'SettingSendMethodList',
    'SettingSendMethodDet',
    'SettingSendMethodTest',
    'SettingSendModelList',
    'SettingSendModelDet',
    'SettingSendModelTest',
    'SettingSendReport',
    'SettingSendList',
    'SettingSendResend',
    'SettingOauthList',
    'SettingOauthDet',
]


def _is_plain_name(value, length):
    """
    True when `value` is a plain name: letters, digits, dot, underscore, dash.

    Used on values coming from the URL before they are passed to a script, so that
    nothing can be appended to the command line.
    """
    return bool(re.fullmatch(r"[A-Za-z0-9_.\-]{1,%d}" % length, str(value)))


class SettingAgeInterval(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self):
        audit_user = request.oauth_user
        l_datas = Setting.getAgeInterval()

        if not l_datas:
            self.log.error(Logs.fileline() + ' : ' + 'SettingAgeInterval ERROR not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        for data in l_datas:
            # Replace None by empty string
            for key, value in list(data.items()):
                if data[key] is None:
                    data[key] = ''

        self.log.info(Logs.fileline() + ' : SettingAgeInterval')
        try:
            details = {"result": "SUCCESS", "action": "QUERY"}
            Audit.insertAudit(audit_user, "SettingAgeInterval", "SETTING", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : SettingAgeInterval ERROR audit success')
        return compose_ret(l_datas, Constants.cst_content_type_json, 200)

    @require_oauth()
    def post(self):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        if 'list_val' not in args:
            self.log.error(Logs.fileline() + ' : SettingAgeInterval ERROR args missing')
            try:
                details = {"result": "ERROR", "reason": "ARGS_MISSING"}
                Audit.insertAudit(audit_user, "SettingAgeInterval", "SETTING", None, "ERROR", details, "U")
            except Exception:
                self.log.exception(Logs.fileline() + ' : SettingAgeInterval ERROR audit args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        l_interval = Setting.getAgeInterval()

        if not l_interval:
            self.log.info(Logs.fileline() + ' : TRACE SettingAgeInterval ERROR notfound age interval')
            try:
                details = {"result": "ERROR", "reason": "NOT_FOUND"}
                Audit.insertAudit(audit_user, "SettingAgeInterval", "SETTING", None, "ERROR", details, "U")
            except Exception:
                self.log.exception(Logs.fileline() + ' : SettingAgeInterval ERROR audit not found')
            return compose_ret('', Constants.cst_content_type_json, 500)

        for val in args['list_val']:
            lower = val['ais_lower_bound']
            upper = val['ais_upper_bound']

            if lower < 0:
                lower = None

            if upper < 0:
                upper = None

            if val['ais_ser'] > 0:
                ret = Setting.updateAgeInterval(ais_ser=val['ais_ser'],
                                                ais_rank=val['ais_rank'],
                                                ais_lower_bound=lower,
                                                ais_upper_bound=upper)
                action = "UPDATE"
            else:
                ret = Setting.insertAgeInterval(ais_rank=val['ais_rank'],
                                                ais_lower_bound=lower,
                                                ais_upper_bound=upper)
                action = "INSERT"

            if ret is False or ret <= 0:
                self.log.info(Logs.fileline() + ' : TRACE SettingAgeInterval ERROR update val age interval')
                try:
                    details = {"ais_ser": val['ais_ser'], "result": "ERROR", "action": action}
                    event_type = "C" if action == "INSERT" else "U"
                    Audit.insertAudit(audit_user, "SettingAgeInterval", "SETTING", None, "ERROR", details, event_type)
                except Exception:
                    self.log.exception(Logs.fileline() + ' : SettingAgeInterval ERROR audit')
                return compose_ret('', Constants.cst_content_type_json, 500)

        # delete missing values compared to age interval
        for db_val in l_interval:
            exist = False
            for ihm_val in args['list_val']:
                if db_val['ais_ser'] == ihm_val['ais_ser']:
                    exist = True

            if not exist:
                ret = Setting.deleteAgeInterval(db_val['ais_ser'])

                if ret is False:
                    self.log.info(Logs.fileline() + ' : TRACE SettingAgeInterval ERROR delete val age interval')
                    try:
                        details = {"ais_ser": db_val['ais_ser'], "result": "ERROR", "action": "DELETE"}
                        Audit.insertAudit(audit_user, "SettingAgeInterval", "SETTING", None, "ERROR", details, "D")
                    except Exception:
                        self.log.exception(Logs.fileline() + ' : SettingAgeInterval ERROR audit')
                    return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE SettingAgeInterval')
        try:
            details = {"count": len(args['list_val']), "result": "SUCCESS"}
            Audit.insertAudit(audit_user, "SettingAgeInterval", "SETTING", None, "SUCCESS", details, "U")
        except Exception:
            self.log.exception(Logs.fileline() + ' : SettingAgeInterval ERROR audit success')
        return compose_ret('', Constants.cst_content_type_json)


class SettingReqServices(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self):
        audit_user = request.oauth_user
        l_datas = Setting.getReqServices()

        if not l_datas:
            self.log.error(Logs.fileline() + ' : ' + 'SettingReqServices ERROR not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        for data in l_datas:
            # Replace None by empty string
            for key, value in list(data.items()):
                if data[key] is None:
                    data[key] = ''

        self.log.info(Logs.fileline() + ' : SettingReqServices')
        try:
            details = {"result": "SUCCESS", "action": "QUERY", "count": len(l_datas)}
            Audit.insertAudit(audit_user, "SettingReqServices", "SETTING", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : SettingReqServices ERROR audit success')
        return compose_ret(l_datas, Constants.cst_content_type_json, 200)

    @require_oauth()
    def post(self):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        if 'list_val' not in args:
            self.log.error(Logs.fileline() + ' : SettingReqServices ERROR args missing')
            try:
                details = {"result": "ERROR", "reason": "ARGS_MISSING"}
                Audit.insertAudit(audit_user, "SettingReqServices", "SETTING", None, "ERROR", details, "U")
            except Exception:
                self.log.exception(Logs.fileline() + ' : SettingReqServices ERROR audit args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        l_req_services = Setting.getReqServices()

        for val in args['list_val']:
            name = val['rqs_name']

            if val['rqs_ser'] > 0:
                ret = Setting.updateReqServices(rqs_ser=val['rqs_ser'],
                                                rqs_rank=val['rqs_rank'],
                                                rqs_name=name)
                action = "UPDATE"
            else:
                ret = Setting.insertReqServices(rqs_rank=val['rqs_rank'],
                                                rqs_name=name)
                action = "INSERT"

            if ret is False or ret <= 0:
                self.log.info(Logs.fileline() + ' : TRACE SettingReqServices ERROR updateReqServices')
                try:
                    details = {"rqs_ser": val['rqs_ser'], "result": "ERROR", "action": action}
                    event_type = "C" if action == "INSERT" else "U"
                    Audit.insertAudit(audit_user, "SettingReqServices", "SETTING", None, "ERROR", details, event_type)
                except Exception:
                    self.log.exception(Logs.fileline() + ' : SettingReqServices ERROR audit')
                return compose_ret('', Constants.cst_content_type_json, 500)

        # delete missing values compared to age interval
        for db_val in l_req_services:
            exist = False
            for ihm_val in args['list_val']:
                if db_val['rqs_ser'] == ihm_val['rqs_ser']:
                    exist = True

            if not exist:
                ret = Setting.deleteReqServices(db_val['rqs_ser'])

                if ret is False:
                    self.log.info(Logs.fileline() + ' : TRACE SettingReqServices ERROR deleteReqServices')
                    try:
                        details = {"rqs_ser": db_val['rqs_ser'], "result": "ERROR", "action": "DELETE"}
                        Audit.insertAudit(audit_user, "SettingReqServices", "SETTING", None, "ERROR", details, "D")
                    except Exception:
                        self.log.exception(Logs.fileline() + ' : SettingReqServices ERROR audit')
                    return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE SettingReqServices')
        try:
            details = {"count": len(args['list_val']), "result": "SUCCESS"}
            Audit.insertAudit(audit_user, "SettingReqServices", "SETTING", None, "SUCCESS", details, "U")
        except Exception:
            self.log.exception(Logs.fileline() + ' : SettingReqServices ERROR audit success')
        return compose_ret('', Constants.cst_content_type_json)


class SettingFuncUnitDet(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self, id_unit):
        audit_user = request.oauth_user
        func_unit = Setting.getFuncUnitDet(id_unit)

        if not func_unit:
            self.log.error(Logs.fileline() + ' : ' + 'SettingFuncUnit ERROR not found')
            try:
                details = {"id_unit": int(id_unit), "result": "ERROR", "reason": "NOT_FOUND"}
                Audit.insertAudit(audit_user, "SettingFuncUnitDet", "SETTING", int(id_unit), "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : SettingFuncUnitDet ERROR audit not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        # Replace None by empty string
        for key, value in list(func_unit.items()):
            if func_unit[key] is None:
                func_unit[key] = ''

        self.log.info(Logs.fileline() + ' : SettingFuncUnitDet')
        try:
            details = {"result": "SUCCESS", "action": "VIEW", "id_unit": int(id_unit)}
            Audit.insertAudit(audit_user, "SettingFuncUnitDet", "SETTING", int(id_unit), "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : SettingFuncUnitDet ERROR audit success')
        return compose_ret(func_unit, Constants.cst_content_type_json, 200)


class SettingFuncUnit(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self):
        audit_user = request.oauth_user
        l_datas = Setting.getFuncUnit()

        if not l_datas:
            self.log.error(Logs.fileline() + ' : ' + 'SettingFuncUnit ERROR not found')
            try:
                details = {"result": "ERROR", "reason": "NOT_FOUND"}
                Audit.insertAudit(audit_user, "SettingFuncUnit", "SETTING", None, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : SettingFuncUnit ERROR audit not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        for data in l_datas:
            # Replace None by empty string
            for key, value in list(data.items()):
                if data[key] is None:
                    data[key] = ''

                data['nb_user'] = 0
                data['nb_fam']  = 0

                nb_user = Setting.getNbFuncUnitLink(data['fun_ser'], 'U')

                if nb_user:
                    data['nb_user'] = nb_user['nb_link']

                nb_fam = Setting.getNbFuncUnitLink(data['fun_ser'], 'F')

                if nb_fam:
                    data['nb_fam'] = nb_fam['nb_link']

        self.log.info(Logs.fileline() + ' : SettingFuncUnit l_datas=' + str(l_datas))
        self.log.info(Logs.fileline() + ' : SettingFuncUnit')
        try:
            details = {"result": "SUCCESS", "action": "QUERY", "count": len(l_datas)}
            Audit.insertAudit(audit_user, "SettingFuncUnit", "SETTING", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : SettingFuncUnit ERROR audit success')
        return compose_ret(l_datas, Constants.cst_content_type_json, 200)

    @require_oauth()
    def post(self):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        if 'list_val' not in args:
            self.log.error(Logs.fileline() + ' : SettingFuncUnit ERROR args missing')
            try:
                details = {"result": "ERROR", "reason": "ARGS_MISSING"}
                Audit.insertAudit(audit_user, "SettingFuncUnit", "SETTING", None, "ERROR", details, "E")
            except Exception:
                self.log.exception(Logs.fileline() + ' : SettingFuncUnit ERROR audit args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        l_req_services = Setting.getFuncUnit()

        for val in args['list_val']:
            name = val['fun_name']

            if val['fun_ser'] > 0:
                ret = Setting.updateFuncUnit(fun_ser=val['fun_ser'],
                                             fun_rank=val['fun_rank'],
                                             fun_name=name)
                action = "UPDATE"
            else:
                ret = Setting.insertFuncUnit(fun_rank=val['fun_rank'],
                                             fun_name=name)
                action = "INSERT"

            if ret is False or ret <= 0:
                self.log.info(Logs.fileline() + ' : TRACE SettingFuncUnit ERROR updateFuncUnit')
                try:
                    details = {"fun_ser": val['fun_ser'], "result": "ERROR", "action": action}
                    event_type = "C" if action == "INSERT" else "U"
                    Audit.insertAudit(audit_user, "SettingFuncUnit", "SETTING", None, "ERROR", details, event_type)
                except Exception:
                    self.log.exception(Logs.fileline() + ' : SettingFuncUnit ERROR audit')
                return compose_ret('', Constants.cst_content_type_json, 500)

        # delete missing values compared to age interval
        for db_val in l_req_services:
            exist = False
            for ihm_val in args['list_val']:
                if db_val['fun_ser'] == ihm_val['fun_ser']:
                    exist = True

            if not exist:
                ret = Setting.deleteFuncUnit(db_val['fun_ser'])

                if ret is False:
                    self.log.info(Logs.fileline() + ' : TRACE SettingFuncUnit ERROR deleteFuncUnit')
                    try:
                        details = {"fun_ser": db_val['fun_ser'], "result": "ERROR", "action": "DELETE"}
                        Audit.insertAudit(audit_user, "SettingFuncUnit", "SETTING", None, "ERROR", details, "D")
                    except Exception:
                        self.log.exception(Logs.fileline() + ' : SettingFuncUnit ERROR audit')
                    return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE SettingFuncUnit')
        try:
            details = {"count": len(args['list_val']), "result": "SUCCESS"}
            Audit.insertAudit(audit_user, "SettingFuncUnit", "SETTING", None, "SUCCESS", details, "U")
        except Exception:
            self.log.exception(Logs.fileline() + ' : SettingFuncUnit ERROR audit success')
        return compose_ret('', Constants.cst_content_type_json)

    @require_oauth()
    def delete(self):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        if 'id_unit' not in args:
            self.log.error(Logs.fileline() + ' : SettingFuncUnit ERROR args missing')
            try:
                details = {"result": "ERROR", "reason": "ARGS_MISSING"}
                Audit.insertAudit(audit_user, "SettingFuncUnit", "SETTING", None, "ERROR", details, "E")
            except Exception:
                self.log.exception(Logs.fileline() + ' : SettingFuncUnit ERROR audit args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        ret = Setting.deleteFuncUnit(args['id_unit'])

        if not ret:
            self.log.error(Logs.fileline() + ' : TRACE SettingFuncUnit delete ERROR')
            try:
                details = {"fun_ser": args['id_unit'], "result": "ERROR", "action": "DELETE"}
                Audit.insertAudit(audit_user, "SettingFuncUnit", "SETTING", None, "ERROR", details, "D")
            except Exception:
                self.log.exception(Logs.fileline() + ' : SettingFuncUnit ERROR audit delete')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE SettingFuncUnit delete id_item=' + str(args['id_unit']))
        try:
            details = {"fun_ser": args['id_unit'], "result": "SUCCESS", "action": "DELETE"}
            Audit.insertAudit(audit_user, "SettingFuncUnit", "SETTING", None, "SUCCESS", details, "D")
        except Exception:
            self.log.exception(Logs.fileline() + ' : SettingFuncUnit ERROR audit delete success')
        return compose_ret('', Constants.cst_content_type_json)


class SettingLinkUnit(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self, type, id_unit):
        audit_user = request.oauth_user
        l_datas = Setting.getLinkUnit(type, id_unit)

        if not l_datas:
            self.log.error(Logs.fileline() + ' : ' + 'SettingLinkUnit ERROR not found')
            try:
                details = {"result": "ERROR", "reason": "NOT_FOUND", "type": type, "id_unit": int(id_unit)}
                Audit.insertAudit(audit_user, "SettingLinkUnit", "SETTING", None, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : SettingLinkUnit ERROR audit not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        Various.useLangDB()

        for data in l_datas:
            # Replace None by empty string
            for key, value in list(data.items()):
                if data[key] is None:
                    data[key] = ''
                elif key == 'role' and data[key]:
                    data[key] = _(data[key].strip())

        self.log.info(Logs.fileline() + ' : SettingLinkUnit')
        try:
            details = {"result": "SUCCESS", "action": "QUERY", "type": type, "id_unit": int(id_unit), "count": len(l_datas)}
            Audit.insertAudit(audit_user, "SettingLinkUnit", "SETTING", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : SettingLinkUnit ERROR audit success')
        return compose_ret(l_datas, Constants.cst_content_type_json, 200)

    @require_oauth()
    def post(self, type, id_unit):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        # self.log.info(Logs.fileline() + ' : DEBUG-TRACE args=' + str(args))

        if 'list_link' not in args:
            self.log.error(Logs.fileline() + ' : SettingLinkUnit ERROR args missing')
            try:
                details = {"result": "ERROR", "reason": "ARGS_MISSING", "type": type, "id_unit": int(id_unit)}
                Audit.insertAudit(audit_user, "SettingLinkUnit", "SETTING", None, "ERROR", details, "E")
            except Exception:
                self.log.exception(Logs.fileline() + ' : SettingLinkUnit ERROR audit args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        l_link_unit = Setting.getListLinkUnit(type, id_unit)

        for link in args['list_link']:
            if link['id_item'] and link['id_item'] not in l_link_unit:
                ret = Setting.insertLinkUnit(ful_fun=id_unit,
                                             ful_ref=link['id_item'],
                                             ful_type=type)

                if not ret:
                    self.log.info(Logs.fileline() + ' : TRACE SettingLinkUnit ERROR insertLinkUnit')
                    try:
                        details = {"type": type, "id_unit": id_unit, "id_item": link['id_item'], "result": "ERROR", "action": "INSERT"}
                        Audit.insertAudit(audit_user, "SettingLinkUnit", "SETTING", None, "ERROR", details, "C")
                    except Exception:
                        self.log.exception(Logs.fileline() + ' : SettingLinkUnit ERROR audit insert')
                    return compose_ret('', Constants.cst_content_type_json, 500)

        # delete missing values
        for db_val in l_link_unit:
            exist = False
            for ihm_val in args['list_link']:
                if db_val == ihm_val['id_item']:
                    exist = True

            if not exist:
                ret = Setting.deleteLinkUnit(type, id_unit, db_val)

                if ret is False:
                    self.log.info(Logs.fileline() + ' : TRACE SettingLinkUnit ERROR deleteLinkUnit')
                    try:
                        details = {"type": type, "id_unit": id_unit, "id_item": db_val, "result": "ERROR", "action": "DELETE"}
                        Audit.insertAudit(audit_user, "SettingLinkUnit", "SETTING", None, "ERROR", details, "D")
                    except Exception:
                        self.log.exception(Logs.fileline() + ' : SettingLinkUnit ERROR audit insert')
                    return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE SettingLinkUnit')
        try:
            details = {"type": type, "id_unit": id_unit, "count": len(args['list_link']), "result": "SUCCESS"}
            Audit.insertAudit(audit_user, "SettingLinkUnit", "SETTING", None, "SUCCESS", details, "U")
        except Exception:
            self.log.exception(Logs.fileline() + ' : SettingLinkUnit ERROR audit success')
        return compose_ret('', Constants.cst_content_type_json)


class SettingLinkByUser(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self, id_user):
        audit_user = request.oauth_user
        l_datas = Setting.getLinkByUser(id_user)

        if not l_datas:
            self.log.error(Logs.fileline() + ' : ' + 'SettingLinkByUser ERROR not found')
            try:
                details = {"result": "ERROR", "reason": "NOT_FOUND", "id_user": int(id_user)}
                Audit.insertAudit(audit_user, "SettingLinkByUser", "SETTING", int(id_user), "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : SettingLinkByUser ERROR audit not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        self.log.info(Logs.fileline() + ' : SettingLinkByUser id_ser=' + str(id_user))
        try:
            details = {"result": "SUCCESS", "action": "QUERY", "id_user": int(id_user), "count": len(l_datas)}
            Audit.insertAudit(audit_user, "SettingLinkByUser", "SETTING", int(id_user), "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : SettingLinkByUser ERROR audit success')
        return compose_ret(l_datas, Constants.cst_content_type_json, 200)


class SettingPref(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self):
        audit_user = request.oauth_user
        l_prefs = Setting.getPrefList()

        if not l_prefs:
            self.log.error(Logs.fileline() + ' : ' + 'SettingPref ERROR not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        for pref in l_prefs:
            # Replace None by empty string
            for key, value in list(pref.items()):
                if pref[key] is None:
                    pref[key] = ''

        self.log.info(Logs.fileline() + ' : SettingPref')
        try:
            details = {"result": "SUCCESS", "action": "QUERY"}
            Audit.insertAudit(audit_user, "SettingPref", "SETTING", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : SettingPref ERROR audit success')
        return compose_ret(l_prefs, Constants.cst_content_type_json, 200)

    @require_oauth()
    def post(self, id_owner):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        if id_owner < 1 or 'prix_acte' not in args or 'entete_1' not in args or 'entete_2' not in args or \
           'entete_3' not in args or 'entete_adr' not in args or 'entete_tel' not in args or 'entete_fax' not in args or \
           'entete_email' not in args or 'entete_ville' not in args or 'facturation_pat_hosp' not in args or \
           'unite_age_defaut' not in args or 'auto_logout' not in args or 'qualite' not in args or \
           'facturation' not in args or 'default_language' not in args or 'db_language' not in args or \
           'audit_purge_months' not in args:
            self.log.error(Logs.fileline() + ' : SettingPref ERROR args missing')
            try:
                details = {"id_owner": int(id_owner), "result": "ERROR", "reason": "ARGS_MISSING"}
                Audit.insertAudit(audit_user, "SettingPref", "SETTING", None, "ERROR", details, "E")
            except Exception:
                self.log.exception(Logs.fileline() + ' : SettingPref ERROR audit args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # Persist all preferences to DB only
        for key, value in list(args.items()):
            ret = Setting.updatePref(id_owner, key, value)
            if ret is False:
                self.log.error(Logs.alert() + ' : SettingPref ERROR update')
                try:
                    details = {"id_owner": id_owner, "key": key, "result": "ERROR", "action": "UPDATE"}
                    Audit.insertAudit(audit_user, "SettingPref", "SETTING", None, "ERROR", details, "U")
                except Exception:
                    self.log.exception(Logs.fileline() + ' : SettingPref ERROR audit')
                return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE SettingPref')
        try:
            details = {"id_owner": id_owner, "keys": list(args.keys()), "result": "SUCCESS"}
            Audit.insertAudit(audit_user, "SettingPref", "SETTING", None, "SUCCESS", details, "U")
        except Exception:
            self.log.exception(Logs.fileline() + ' : SettingPref ERROR audit success')
        return compose_ret('', Constants.cst_content_type_json)


class SettingRecNum(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self):
        audit_user = request.oauth_user
        setting = Setting.getRecNumSetting()

        if not setting:
            self.log.error(Logs.fileline() + ' : ERROR SettingRecNum not found')
            try:
                details = {"result": "ERROR", "reason": "NOT_FOUND"}
                Audit.insertAudit(audit_user, "SettingRecNum", "SETTING", None, "ERROR", details, "E")
            except Exception:
                self.log.exception(Logs.fileline() + ' : SettingRecNum ERROR audit not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        # Replace None by empty string
        for key, value in list(setting.items()):
            if setting[key] is None:
                setting[key] = ''

        if setting['rstg_date']:
            setting['rstg_date'] = datetime.strftime(setting['rstg_date'], '%Y-%m-%d %H:%M:%S')

        if setting['rstg_date_upd']:
            setting['rstg_date_upd'] = datetime.strftime(setting['rstg_date_upd'], '%Y-%m-%d %H:%M:%S')

        self.log.info(Logs.fileline() + ' : TRACE SettingRecNum')
        try:
            details = {"result": "SUCCESS", "action": "QUERY"}
            Audit.insertAudit(audit_user, "SettingRecNum", "SETTING", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : SettingRecNum ERROR audit success')
        return compose_ret(setting, Constants.cst_content_type_json)

    @require_oauth()
    def post(self):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        if 'id_owner' not in args or 'period' not in args or 'format' not in args or 'samp_mask' not in args or 'samp_regex' not in args:
            self.log.error(Logs.fileline() + ' : SettingRecNum ERROR args missing')
            try:
                details = {"id_owner": args.get('id_owner') if isinstance(args, dict) else None,
                           "period": args.get('period') if isinstance(args, dict) else None,
                           "format": args.get('format') if isinstance(args, dict) else None,
                           "result": "ERROR", "reason": "ARGS_MISSING"}
                Audit.insertAudit(audit_user, "SettingRecNum", "SETTING", None, "ERROR", details, "E")
            except Exception:
                self.log.exception(Logs.fileline() + ' : SettingRecNum ERROR audit args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        ret = Setting.updateRecNumSetting(id_owner=args['id_owner'],
                                          period=args['period'],
                                          format=args['format'],
                                          samp_mask=args['samp_mask'],
                                          samp_regex=args['samp_regex'])

        if ret is False:
            self.log.error(Logs.alert() + ' : SettingRecNum ERROR update')
            try:
                details = {"id_owner": args['id_owner'], "period": args['period'], "format": args['format'],
                           "result": "ERROR", "action": "UPDATE"}
                Audit.insertAudit(audit_user, "SettingRecNum", "SETTING", None, "ERROR", details, "U")
            except Exception:
                self.log.exception(Logs.fileline() + ' : SettingRecNum ERROR audit')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE SettingRecNum')
        try:
            details = {"id_owner": args['id_owner'], "period": args['period'], "format": args['format'],
                       "result": "SUCCESS", "action": "UPDATE"}
            Audit.insertAudit(audit_user, "SettingRecNum", "SETTING", None, "SUCCESS", details, "U")
        except Exception:
            self.log.exception(Logs.fileline() + ' : SettingRecNum ERROR audit success')
        return compose_ret('', Constants.cst_content_type_json)


class SettingReport(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self):
        audit_user = request.oauth_user
        setting = Setting.getReportSetting()

        if not setting:
            self.log.error(Logs.fileline() + ' : ERROR SettingReport not found')
            try:
                details = {"result": "ERROR", "reason": "NOT_FOUND"}
                Audit.insertAudit(audit_user, "SettingReport", "SETTING", None, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : SettingReport ERROR audit not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        # Replace None by empty string
        for key, value in list(setting.items()):
            if setting[key] is None:
                setting[key] = ''

        if setting['sys_creation_date']:
            setting['sys_creation_date'] = datetime.strftime(setting['sys_creation_date'], '%Y-%m-%d %H:%M:%S')

        if setting['sys_last_mod_date']:
            setting['sys_last_mod_date'] = datetime.strftime(setting['sys_last_mod_date'], '%Y-%m-%d %H:%M:%S')

        self.log.info(Logs.fileline() + ' : TRACE SettingReport')
        try:
            details = {"result": "SUCCESS", "action": "QUERY"}
            Audit.insertAudit(audit_user, "SettingReport", "SETTING", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : SettingReport ERROR audit success')
        return compose_ret(setting, Constants.cst_content_type_json)

    @require_oauth()
    def post(self):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        if 'id_owner' not in args or 'header' not in args or 'comment' not in args or 'report_pwd' not in args:
            self.log.error(Logs.fileline() + ' : SettingReport ERROR args missing')
            try:
                details = {"result": "ERROR", "reason": "ARGS_MISSING"}
                Audit.insertAudit(audit_user, "SettingReport", "SETTING", None, "ERROR", details, "U")
            except Exception:
                self.log.exception(Logs.fileline() + ' : SettingReport ERROR audit args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        ret = Setting.updateReportSetting(id_owner=args['id_owner'],
                                          header=args['header'],
                                          comment=args['comment'],
                                          report_pwd=args['report_pwd'])

        if ret is False:
            self.log.error(Logs.alert() + ' : SettingReport ERROR update')
            try:
                details = {"id_owner": args['id_owner'], "result": "ERROR", "action": "UPDATE"}
                Audit.insertAudit(audit_user, "SettingReport", "SETTING", None, "ERROR", details, "U")
            except Exception:
                self.log.exception(Logs.fileline() + ' : SettingReport ERROR audit')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE SettingReport')
        try:
            details = {"id_owner": args['id_owner'], "result": "SUCCESS", "action": "UPDATE"}
            Audit.insertAudit(audit_user, "SettingReport", "SETTING", None, "SUCCESS", details, "U")
        except Exception:
            self.log.exception(Logs.fileline() + ' : SettingReport ERROR audit success')
        return compose_ret('', Constants.cst_content_type_json)


class SettingBackup(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self):
        audit_user = request.oauth_user
        setting = Setting.getBackupSetting()

        if not setting:
            self.log.error(Logs.fileline() + ' : ERROR SettingBackup not found')
            try:
                details = {"result": "ERROR", "reason": "NOT_FOUND"}
                Audit.insertAudit(audit_user, "SettingBackup", "SETTING", None, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : SettingBackup ERROR audit not found')
            return compose_ret('1', Constants.cst_content_type_json, 404)

        # Replace None by empty string
        for key, value in list(setting.items()):
            if setting[key] is None:
                setting[key] = ''

        if setting['bks_start_time']:
            setting['bks_start_time'] = str(setting['bks_start_time'])

        self.log.info(Logs.fileline() + ' : TRACE SettingBackup')
        try:
            details = {"result": "SUCCESS", "action": "QUERY"}
            Audit.insertAudit(audit_user, "SettingBackup", "SETTING", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : SettingBackup ERROR audit success')
        return compose_ret(setting, Constants.cst_content_type_json)


class ScriptBackup(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self, media):
        audit_user = request.oauth_user

        if not _is_plain_name(media, 32):
            self.log.error(Logs.fileline() + ' : ScriptBackup ERROR invalid media')
            try:
                details = {"result": "ERROR", "reason": "INVALID_MEDIA"}
                Audit.insertAudit(audit_user, "ScriptBackup", "SETTING", None, "ERROR", details, "E")
            except Exception:
                self.log.exception(Logs.fileline() + ' : ScriptBackup ERROR audit invalid media')
            return compose_ret('1', Constants.cst_content_type_json, 400)

        script_path = os.path.join(Constants.cst_path_script, Constants.cst_script_backup)
        argv = ["sh", script_path, "-m", media, Constants.cst_io_backup]
        out_path = os.path.join(Constants.cst_io, 'backup.out')

        self.log.info(Logs.fileline() + ' : ScriptBackup argv=' + str(argv))

        # runs in the background, as the trailing "&" did
        with open(out_path, "w", encoding="utf-8", errors="ignore") as f:
            subprocess.Popen(argv, stdout=f, stderr=subprocess.STDOUT, start_new_session=True)  # nosec B603

        ret = 0

        self.log.info(Logs.fileline() + ' : TRACE ScriptBackup ret=' + str(ret))
        try:
            details = {"media": media, "cmd": argv, "ret": ret, "result": "CALLED"}
            Audit.insertAudit(audit_user, "ScriptBackup", "SETTING", None, "SUCCESS", details, "E")
        except Exception:
            self.log.exception(Logs.fileline() + ' : ScriptBackup ERROR audit')
        return compose_ret(ret, Constants.cst_content_type_json)


class ScriptGenkey(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        if 'pwd_key' not in args:
            self.log.error(Logs.fileline() + ' : ScriptGenkey ERROR args missing')
            try:
                details = {"result": "ERROR", "reason": "ARGS_MISSING"}
                Audit.insertAudit(audit_user, "ScriptGenkey", "SETTING", None, "ERROR", details, "E")
            except Exception:
                self.log.exception(Logs.fileline() + ' : ScriptGenkey ERROR audit args missing')
            return compose_ret('1', Constants.cst_content_type_json, 400)

        os.environ['LABBOOK_KEY_PWD'] = args['pwd_key']

        cmd = 'sh ' + Constants.cst_path_script + '/' + Constants.cst_script_backup + Constants.cst_io_genkey

        self.log.error(Logs.fileline() + ' : ScriptGenkey cmd=' + cmd)
        ret = os.system(cmd)

        self.log.info(Logs.fileline() + ' : TRACE ScriptGenkey ret=' + str(ret))
        try:
            details = {"cmd": cmd, "ret": ret, "result": "CALLED"}
            Audit.insertAudit(audit_user, "ScriptGenkey", "SETTING", None, "SUCCESS", details, "E")
        except Exception:
            self.log.exception(Logs.fileline() + ' : ScriptGenkey ERROR audit')
        return compose_ret(ret, Constants.cst_content_type_json)


class ScriptInitMedia(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self, media):
        audit_user = request.oauth_user

        if not _is_plain_name(media, 32):
            self.log.error(Logs.fileline() + ' : ScriptInitMedia ERROR invalid media')
            try:
                details = {"result": "ERROR", "reason": "INVALID_MEDIA"}
                Audit.insertAudit(audit_user, "ScriptInitMedia", "SETTING", None, "ERROR", details, "E")
            except Exception:
                self.log.exception(Logs.fileline() + ' : ScriptInitMedia ERROR audit invalid media')
            return compose_ret('1', Constants.cst_content_type_json, 400)

        script_path = os.path.join(Constants.cst_path_script, Constants.cst_script_backup)
        argv = ["sh", script_path, "-m", media, Constants.cst_io_initmedia]

        self.log.info(Logs.fileline() + ' : ScriptInitMedia argv=' + str(argv))

        # this one is awaited: the caller checks the return code
        ret = subprocess.run(argv, check=False).returncode  # nosec B603

        self.log.info(Logs.fileline() + ' : TRACE ScriptInitMedia ret=' + str(ret))
        try:
            details = {"media": media, "cmd": argv, "ret": ret, "result": "CALLED"}
            Audit.insertAudit(audit_user, "ScriptInitMedia", "SETTING", None, "SUCCESS", details, "E")
        except Exception:
            self.log.exception(Logs.fileline() + ' : ScriptInitMedia ERROR audit')
        return compose_ret(ret, Constants.cst_content_type_json)


class ScriptKeyexist(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self):
        audit_user = request.oauth_user
        cmd = 'sh ' + Constants.cst_path_script + '/' + Constants.cst_script_backup + Constants.cst_io_keyexist

        self.log.error(Logs.fileline() + ' : ScriptKeyexist cmd=' + cmd)
        ret = os.system(cmd)

        self.log.info(Logs.fileline() + ' : TRACE ScriptKeyexist ret=' + str(ret))
        try:
            details = {"cmd": cmd, "ret": ret, "result": "CALLED"}
            Audit.insertAudit(audit_user, "ScriptKeyexist", "SETTING", None, "SUCCESS", details, "E")
        except Exception:
            self.log.exception(Logs.fileline() + ' : ScriptKeyexist ERROR audit')
        return compose_ret(ret, Constants.cst_content_type_json)


class ScriptListarchive(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self, media):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        if 'user_pwd' not in args:
            self.log.error(Logs.fileline() + ' : ScriptListmedia ERROR args missing')
            try:
                details = {"media": str(media), "result": "ERROR", "reason": "ARGS_MISSING"}
                Audit.insertAudit(audit_user, "ScriptListarchive", "SETTING", None, "ERROR", details, "E")
            except Exception:
                self.log.exception(Logs.fileline() + ' : ScriptListarchive ERROR audit args missing')
            return compose_ret('1', Constants.cst_content_type_json, 400)

        if not _is_plain_name(media, 32):
            self.log.error(Logs.fileline() + ' : ScriptListarchive ERROR invalid media')
            try:
                details = {"result": "ERROR", "reason": "INVALID_MEDIA"}
                Audit.insertAudit(audit_user, "ScriptListarchive", "SETTING", None, "ERROR", details, "E")
            except Exception:
                self.log.exception(Logs.fileline() + ' : ScriptListarchive ERROR audit invalid media')
            return compose_ret('1', Constants.cst_content_type_json, 400)

        os.environ['LABBOOK_USER_PWD'] = args['user_pwd']

        script_path = os.path.join(Constants.cst_path_script, Constants.cst_script_backup)
        argv = ["sh", script_path, "-m", media, Constants.cst_io_listarchive]
        out_path = os.path.join(Constants.cst_io, 'listarchive.out')

        self.log.info(Logs.fileline() + ' : ScriptListarchive argv=' + str(argv))

        # runs in the background, as the trailing "&" did
        with open(out_path, "w", encoding="utf-8", errors="ignore") as f:
            subprocess.Popen(argv, stdout=f, stderr=subprocess.STDOUT, start_new_session=True)  # nosec B603

        ret = 0

        self.log.info(Logs.fileline() + ' : TRACE ScriptListarchive ret=' + str(ret))
        try:
            details = {"media": media, "cmd": argv, "ret": ret, "result": "CALLED"}
            Audit.insertAudit(audit_user, "ScriptListarchive", "SETTING", None, "SUCCESS", details, "E")
        except Exception:
            self.log.exception(Logs.fileline() + ' : ScriptListarchive ERROR audit')
        return compose_ret(ret, Constants.cst_content_type_json)


class ScriptListmedia(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self, type):
        audit_user = request.oauth_user
        if type == "U":
            type = ' -U '
        else:
            type = ' '

        args = request.get_json() or {}

        if 'user_pwd' not in args:
            self.log.error(Logs.fileline() + ' : ScriptListmedia ERROR args missing')
            try:
                details = {"reason": "ARGS_MISSING"}
                Audit.insertAudit(audit_user, "ScriptListmedia", "SETTING", None, "ERROR", details, "E")
            except Exception:
                self.log.exception(Logs.fileline() + ' : ScriptListmedia ERROR audit args missing')
            return compose_ret('1', Constants.cst_content_type_json, 400)

        os.environ['LABBOOK_USER_PWD'] = args['user_pwd']

        cmd = ('sh ' + Constants.cst_path_script + '/' + Constants.cst_script_backup + type +
               Constants.cst_io_listmedia + ' > ' + Constants.cst_io + 'listmedia.out 2>&1 &')

        self.log.error(Logs.fileline() + ' : ScriptListmedia cmd=' + cmd)
        ret = os.system(cmd)

        self.log.info(Logs.fileline() + ' : TRACE ScriptListmedia ret=' + str(ret))  # l_media=' + str(l_media))
        try:
            details = {"type": type, "cmd": cmd, "ret": ret, "result": "CALLED"}
            Audit.insertAudit(audit_user, "ScriptListmedia", "SETTING", None, "SUCCESS", details, "E")
        except Exception:
            self.log.exception(Logs.fileline() + ' : ScriptListmedia ERROR audit')
        return compose_ret(ret, Constants.cst_content_type_json)


class ScriptProgbackup(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        if 'start_time' not in args or 'user_pwd' not in args:
            self.log.error(Logs.fileline() + ' : ScriptProgbackup ERROR args missing')
            try:
                details = {"start_time": args.get('start_time') if args else None, "result": "ERROR",
                           "reason": "ARGS_MISSING"}
                Audit.insertAudit(audit_user, "ScriptProgbackup", "SETTING", None, "ERROR", details, "E")
            except Exception:
                self.log.exception(Logs.fileline() + ' : ScriptProgbackup ERROR audit')
            return compose_ret('1', Constants.cst_content_type_json, 400)

        # Extract inputs
        start_time = str(args.get('start_time', ''))
        user_pwd = args.get('user_pwd', '')

        # T and Z of the ISO format are already covered by A-Za-z
        if not re.fullmatch(r"[A-Za-z0-9 _:\-./]{1,64}", start_time):
            self.log.error(Logs.fileline() + ' : ScriptProgbackup ERROR invalid start_time')
            try:
                details = {"start_time": start_time, "result": "ERROR", "reason": "INVALID_START_TIME"}
                Audit.insertAudit(audit_user, "ScriptProgbackup", "SETTING", None, "ERROR", details, "E")
            except Exception:
                self.log.exception(Logs.fileline() + ' : ScriptProgbackup ERROR audit')
            return compose_ret('1', Constants.cst_content_type_json, 400)

        # Build absolute script path without string concatenation in the shell
        script_path = os.path.join(Constants.cst_path_script, Constants.cst_script_backup).strip()

        if not os.path.isfile(script_path):
            self.log.error(Logs.fileline() + f" : ScriptProgbackup ERROR script not found path={script_path}")
            try:
                details = {"start_time": start_time, "script_path": script_path, "result": "ERROR",
                           "reason": "SCRIPT_NOT_FOUND"}
                Audit.insertAudit(audit_user, "ScriptProgbackup", "SETTING", None, "ERROR", details, "E")
            except Exception:
                self.log.exception(Logs.fileline() + ' : ScriptProgbackup ERROR audit')
            return compose_ret('1', Constants.cst_content_type_json, 500)

        argv = [
            "sh",
            script_path,
            "-w",
            start_time,
            Constants.cst_io_progbackup
        ]

        env = os.environ.copy()
        env['LABBOOK_USER_PWD'] = user_pwd

        try:
            result = subprocess.run(
                argv,
                env=env,
                shell=False,          # Critical: no shell
                check=False,          # We handle return code ourselves
                capture_output=True,
                text=True,
                timeout=60            # Optional: avoid hanging
            )
        except Exception as exc:
            self.log.exception(Logs.fileline() + f" : ScriptProgbackup ERROR execution failed err={exc}")
            try:
                details = {"start_time": start_time, "script_path": script_path, "result": "ERROR",
                           "reason": "EXEC_FAILED", "err": str(exc)}
                Audit.insertAudit(audit_user, "ScriptProgbackup", "SETTING", None, "ERROR", details, "E")
            except Exception:
                self.log.exception(Logs.fileline() + ' : ScriptProgbackup ERROR audit')
            return compose_ret('1', Constants.cst_content_type_json, 500)

        # Handle return code
        if result.returncode != 0:
            self.log.error(Logs.fileline() + f" : ScriptProgbackup ERROR rc={result.returncode} stdout_len={len(result.stdout or '')} stderr_len={len(result.stderr or '')}")
            try:
                details = {"start_time": start_time, "script_path": script_path, "rc": result.returncode,
                           "result": "ERROR", "reason": "BAD_RC"}
                Audit.insertAudit(audit_user, "ScriptProgbackup", "SETTING", None, "ERROR", details, "E")
            except Exception:
                self.log.exception(Logs.fileline() + ' : ScriptProgbackup ERROR audit')
            return compose_ret('1', Constants.cst_content_type_json, 500)

        start_time_db = start_time
        if re.fullmatch(r"\d{2}:\d{2}", start_time):
            start_time_db = start_time + ':00'

        try:
            ret_db = Setting.updateBackupSetting(bks_start_time=start_time_db)
        except Exception as exc:
            self.log.exception(Logs.fileline() + f" : ScriptProgbackup ERROR DB update failed err={exc}")
            try:
                details = {"start_time": start_time, "start_time_db": start_time_db, "result": "ERROR",
                           "reason": "DB_EXCEPTION", "err": str(exc)}
                Audit.insertAudit(audit_user, "ScriptProgbackup", "SETTING", None, "ERROR", details, "E")
            except Exception:
                self.log.exception(Logs.fileline() + ' : ScriptProgbackup ERROR audit')
            return compose_ret('1', Constants.cst_content_type_json, 500)

        if not ret_db:
            self.log.error(Logs.fileline() + " : ScriptProgbackup ERROR DB update returned falsy")
            try:
                details = {"start_time": start_time, "start_time_db": start_time_db, "result": "ERROR",
                           "reason": "DB_FALSY"}
                Audit.insertAudit(audit_user, "ScriptProgbackup", "SETTING", None, "ERROR", details, "E")
            except Exception:
                self.log.exception(Logs.fileline() + ' : ScriptProgbackup ERROR audit')
            return compose_ret('1', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + f" : ScriptProgbackup done rc=0 stdout_len={len(result.stdout or '')} stderr_len={len(result.stderr or '')}")
        try:
            details = {"start_time": start_time, "start_time_db": start_time_db, "result": "CALLED"}
            Audit.insertAudit(audit_user, "ScriptProgbackup", "SETTING", None, "SUCCESS", details, "E")
        except Exception:
            self.log.exception(Logs.fileline() + ' : ScriptProgbackup ERROR audit success')
        return compose_ret('0', Constants.cst_content_type_json, 200)


class ScriptRestart(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        if 'pwd_user' not in args:
            self.log.error(Logs.fileline() + ' : ScriptRestart ERROR args missing')
            try:
                details = {"reason": "ARGS_MISSING"}
                Audit.insertAudit(audit_user, "ScriptRestart", "SETTING", None, "ERROR", details, "E")
            except Exception:
                self.log.exception(Logs.fileline() + ' : ScriptRestart ERROR audit args missing')
            return compose_ret('1', Constants.cst_content_type_json, 400)

        os.environ['LABBOOK_USER_PWD'] = args['pwd_user']

        cmd = 'sh ' + Constants.cst_path_script + '/' + Constants.cst_script_backup + Constants.cst_io_restart

        self.log.error(Logs.fileline() + ' : ScriptRestart cmd=' + cmd)
        ret = os.system(cmd)

        self.log.info(Logs.fileline() + ' : TRACE ScriptRestart ret=' + str(ret))
        try:
            details = {"cmd": cmd, "ret": ret, "result": "CALLED"}
            Audit.insertAudit(audit_user, "ScriptRestart", "SETTING", None, "SUCCESS", details, "E")
        except Exception:
            self.log.exception(Logs.fileline() + ' : ScriptRestart ERROR audit')
        return compose_ret(ret, Constants.cst_content_type_json)


class ScriptRestore(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        # Check mandatory arguments
        if 'media' not in args or 'pwd_key' not in args or 'archive' not in args:
            self.log.error(Logs.fileline() + ' : ScriptRestore ERROR args missing')
            try:
                details = {"result": "ERROR", "reason": "ARGS_MISSING"}
                Audit.insertAudit(audit_user, "ScriptRestore", "SETTING", None, "ERROR", details, "E")
            except Exception:
                self.log.exception(Logs.fileline() + ' : ScriptRestore ERROR audit args missing')
            return compose_ret('1', Constants.cst_content_type_json, 400)

        # Extract user inputs
        media = (str(args.get('media') or '')).strip()
        archive = (str(args.get('archive') or '')).strip()
        pwd_key = str(args.get('pwd_key') or '')

        # Validate media value (allowlist)
        if not re.fullmatch(r"[A-Za-z0-9_.\-]{1,32}", media):
            self.log.error(Logs.fileline() + ' : ScriptRestore ERROR invalid media')
            try:
                details = {"media": media, "result": "ERROR", "reason": "INVALID_MEDIA"}
                Audit.insertAudit(audit_user, "ScriptRestore", "SETTING", None, "ERROR", details, "E")
            except Exception:
                self.log.exception(Logs.fileline() + ' : ScriptRestore ERROR audit invalid media')
            return compose_ret('1', Constants.cst_content_type_json, 400)

        # Validate archive value (allowlist)
        if not re.fullmatch(r"[A-Za-z0-9 _.\-]{1,128}", archive):
            self.log.error(Logs.fileline() + ' : ScriptRestore ERROR invalid archive')
            try:
                details = {"archive": archive, "result": "ERROR", "reason": "INVALID_ARCHIVE"}
                Audit.insertAudit(audit_user, "ScriptRestore", "SETTING", None, "ERROR", details, "E")
            except Exception:
                self.log.exception(Logs.fileline() + ' : ScriptRestore ERROR audit invalid archive')
            return compose_ret('1', Constants.cst_content_type_json, 400)

        # Validate password key
        if not pwd_key:
            self.log.error(Logs.fileline() + ' : ScriptRestore ERROR invalid pwd_key')
            try:
                details = {"result": "ERROR", "reason": "INVALID_PWD_KEY"}
                Audit.insertAudit(audit_user, "ScriptRestore", "SETTING", None, "ERROR", details, "E")
            except Exception:
                self.log.exception(Logs.fileline() + ' : ScriptRestore ERROR audit invalid pwd_key')
            return compose_ret('1', Constants.cst_content_type_json, 400)

        # Build absolute script path
        script_path = os.path.join(Constants.cst_path_script, Constants.cst_script_backup).strip()
        if not os.path.isfile(script_path):
            self.log.error(Logs.fileline() + ' : ScriptRestore ERROR script not found path=' + script_path)
            try:
                details = {"script_path": script_path, "result": "ERROR", "reason": "SCRIPT_NOT_FOUND"}
                Audit.insertAudit(audit_user, "ScriptRestore", "SETTING", None, "ERROR", details, "E")
            except Exception:
                self.log.exception(Logs.fileline() + ' : ScriptRestore ERROR audit script not found')
            return compose_ret('1', Constants.cst_content_type_json, 500)

        # Build argv list (no shell, no string command)
        argv = ["sh", script_path, "-m", media, "-a", archive, Constants.cst_io_restore]

        # Set global environment variable (same behavior as os.system)
        os.environ['LABBOOK_KEY_PWD'] = pwd_key

        # Redirect stdout + stderr to restore.out (replacement for > file 2>&1)
        out_path = os.path.join(Constants.cst_io, "restore.out").strip()

        # Ensure output directory exists to avoid open() failure
        os.makedirs(os.path.dirname(out_path), exist_ok=True)

        # Execute script asynchronously (replacement for trailing &)
        with open(out_path, "w", encoding="utf-8", errors="ignore") as f:
            subprocess.Popen(argv, shell=False, stdout=f, stderr=subprocess.STDOUT, start_new_session=True)

        ret = 0

        # Audit success
        self.log.info(Logs.fileline() + ' : TRACE ScriptRestore ret=' + str(ret))
        try:
            details = {"media": media, "archive": archive, "argv": argv, "out": out_path, "ret": ret, "result": "CALLED"}
            Audit.insertAudit(audit_user, "ScriptRestore", "SETTING", None, "SUCCESS", details, "E")
        except Exception:
            self.log.exception(Logs.fileline() + ' : ScriptRestore ERROR audit')

        return compose_ret(ret, Constants.cst_content_type_json)


class ScriptStatus(Resource):
    log = logging.getLogger('log_services')

    def get(self, mode):
        date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            if mode == 'R':
                path = os.path.join(Constants.cst_io, Constants.cst_io_restore).strip()
            elif mode == 'B':
                path = os.path.join(Constants.cst_io, Constants.cst_io_backup).strip()
            elif mode == 'M':
                path = os.path.join(Constants.cst_io, Constants.cst_io_listmedia).strip()
            elif mode == 'A':
                path = os.path.join(Constants.cst_io, Constants.cst_io_listarchive).strip()
            else:
                self.log.info(Logs.fileline() + ' : ERROR ScriptStatus wrong mode : ' + str(mode))
                ret = "ERR;" + str(date_now) + ";Wrong mode"
                return compose_ret(ret, Constants.cst_content_type_json, 500)

            if not os.path.exists(path) or os.stat(path).st_size == 0:
                self.log.info(Logs.fileline() + ' : ERROR ScriptStatus impossible to open or empty : ' + str(path))
                ret = "WAIT;" + str(date_now) + ";Impossible to open : " + str(path)
                return compose_ret(ret, Constants.cst_content_type_json, 200)

            # No encoding forced because script return list from system so its depend of encoding of operating system
            last_line = ''

            with open(path, 'r') as f:
                for line in f:
                    last_line = line

            if not last_line:
                self.log.info(Logs.fileline() + ' : ERROR ScriptStatus impossible to open or read file, last line is empty')
                ret = "WAIT;" + str(date_now) + ";Impossible to open or read file, last line is empty"
                return compose_ret(ret, Constants.cst_content_type_json, 200)

            ret = last_line[:-1]

            if not ret or ((mode == 'M' or mode == 'A') and not ret.startswith('OK') and not ret.startswith('ERR')):
                ret = "WAIT;" + str(date_now) + ";Not finished"
            elif mode == 'M' and ret.startswith('OK'):
                l_media = {}

                l_media['ret']   = ret
                l_media['media'] = []

                try:
                    # No encoding forced because script return list from system so its depend of encoding of operating system
                    with open(os.path.join(Constants.cst_io, 'listmedia').strip(), 'r') as f:
                        for media in f:
                            l_media['media'].append(media[:-1])

                    l_media['media'] = l_media['media'][:-1]  # Remove last line

                    self.log.info(Logs.fileline() + ' : l_media=' + str(l_media))
                except Exception:
                    self.log.info(Logs.fileline() + ' : ERROR ScriptStatus impossible to open listmedia file')
                    ret = "WAIT;" + str(date_now) + ";Impossible to read listmedia file"
                    return compose_ret(ret, Constants.cst_content_type_json, 200)

                self.log.info(Logs.fileline() + ' : TRACE ScriptStatus l_media=' + str(l_media))
                return compose_ret(l_media, Constants.cst_content_type_json)

            elif mode == 'A' and ret.startswith('OK'):
                l_archive = {}

                l_archive['ret']   = ret
                l_archive['archive'] = []

                # read listarchive file
                try:
                    # No encoding forced because script return list from system so its depend of encoding of operating system
                    with open(os.path.join(Constants.cst_io, 'listarchive').strip(), 'r') as f:
                        for archive in f:
                            l_archive['archive'].append(archive[:-1])

                    l_archive['archive'] = l_archive['archive'][:-1]  # Remove last line

                    self.log.info(Logs.fileline() + ' : l_archive=' + str(l_archive))
                except Exception:
                    self.log.info(Logs.fileline() + ' : ERROR ScriptStatus impossible to open listarchive file')
                    ret = "WAIT;" + str(date_now) + ";Impossible to read listarchive file"
                    return compose_ret(l_archive, Constants.cst_content_type_json, 200)

                self.log.info(Logs.fileline() + ' : TRACE ScriptStatus l_archive=' + str(l_archive))
                return compose_ret(l_archive, Constants.cst_content_type_json)

        except Exception as e:
            date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.log.info(Logs.fileline() + ' : ERROR ScriptStatus impossible to open status file exception : ' + str(e))
            ret = "ERR;" + str(date_now) + ";Impossible to read status file"
            return compose_ret(ret, Constants.cst_content_type_json, 200)  # 200 : dont want to stop poll in ihm

        self.log.info(Logs.fileline() + ' : TRACE ScriptStatus ret=' + str(ret))
        return compose_ret(ret, Constants.cst_content_type_json)


class TemplateList(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self, type=''):
        audit_user = request.oauth_user
        l_items = Setting.getTemplateList(type)

        if not l_items:
            self.log.error(Logs.fileline() + ' : TRACE TemplateList not found')

        for item in l_items:
            # Replace None by empty string
            for key, value in list(item.items()):
                if item[key] is None:
                    item[key] = ''

        self.log.info(Logs.fileline() + ' : TRACE TemplateList')
        try:
            details = {"result": "SUCCESS", "action": "QUERY", "count": len(l_items)}
            Audit.insertAudit(audit_user, "TemplateList", "SETTING", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : TemplateList ERROR audit success')
        return compose_ret(l_items, Constants.cst_content_type_json)


class TemplateDet(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self, id_item):
        audit_user = request.oauth_user
        item = Setting.getTemplate(id_item)

        if not item:
            self.log.error(Logs.fileline() + ' : ' + 'TemplateDet ERROR not found')
            try:
                details = {"id_item": int(id_item), "result": "ERROR", "reason": "NOT_FOUND"}
                Audit.insertAudit(audit_user, "TemplateDet", "SETTING", int(id_item), "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : TemplateDet ERROR audit not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        # Replace None by empty string
        for key, value in list(item.items()):
            if item[key] is None:
                item[key] = ''

        self.log.info(Logs.fileline() + ' : TemplateDet id_item=' + str(id_item))
        try:
            details = {"result": "SUCCESS", "action": "VIEW", "id_item": int(id_item)}
            Audit.insertAudit(audit_user, "TemplateDet", "SETTING", int(id_item), "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : TemplateDet ERROR audit success')
        return compose_ret(item, Constants.cst_content_type_json, 200)

    @require_oauth()
    def post(self, id_item):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        if 'id_item' not in args or 'tpl_name' not in args or 'tpl_type' not in args or \
           'tpl_default' not in args or 'tpl_file' not in args:
            self.log.error(Logs.fileline() + ' : TemplateDet ERROR args missing')
            try:
                details = {"id_item": id_item, "result": "ERROR", "reason": "ARGS_MISSING"}
                Audit.insertAudit(audit_user, "TemplateDet", "SETTING", None, "ERROR", details, "E")
            except Exception:
                self.log.exception(Logs.fileline() + ' : TemplateDet ERROR audit args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        action = "UPDATE" if id_item > 0 else "INSERT"

        # Update item
        if id_item > 0:
            ret = Setting.updateTemplate(tpl_ser=id_item,
                                         tpl_name=args['tpl_name'],
                                         tpl_type=args['tpl_type'],
                                         tpl_default=args['tpl_default'],
                                         tpl_file=args['tpl_file'])

            action = "UPDATE"

            if ret is False:
                self.log.error(Logs.alert() + ' : TemplateDet ERROR update')
                try:
                    details = {"id_item": id_item, "tpl_name": args['tpl_name'], "result": "ERROR", "action": "UPDATE"}
                    Audit.insertAudit(audit_user, "TemplateDet", "SETTING", id_item, "ERROR", details, "U")
                except Exception:
                    self.log.exception(Logs.fileline() + ' : TemplateDet ERROR audit update')
                return compose_ret('', Constants.cst_content_type_json, 500)

        # Insert new item
        else:
            ret = Setting.insertTemplate(tpl_name=args['tpl_name'],
                                         tpl_type=args['tpl_type'],
                                         tpl_default=args['tpl_default'],
                                         tpl_file=args['tpl_file'])
            action = "INSERT"

            if ret <= 0:
                self.log.error(Logs.alert() + ' : TemplateDet ERROR  insert')
                try:
                    details = {"id_item": ret, "tpl_name": args['tpl_name'], "result": "ERROR", "action": "INSERT"}
                    Audit.insertAudit(audit_user, "TemplateDet", "SETTING", None, "ERROR", details, "C")
                except Exception:
                    self.log.exception(Logs.fileline() + ' : TemplateDet ERROR audit insert')
                return compose_ret('', Constants.cst_content_type_json, 500)

            id_item = ret

        self.log.info(Logs.fileline() + ' : TRACE TemplateDet id_item=' + str(id_item))
        try:
            details = {"id_item": id_item, "tpl_name": args['tpl_name'], "result": "SUCCESS", "action": action}
            event_type = "C" if action == "INSERT" else "U"
            Audit.insertAudit(audit_user, "TemplateDet", "SETTING", id_item, "SUCCESS", details, event_type)
        except Exception:
            self.log.exception(Logs.fileline() + ' : TemplateDet ERROR audit success')
        return compose_ret(id_item, Constants.cst_content_type_json)

    @require_oauth()
    def delete(self, id_item):
        audit_user = request.oauth_user
        ret = Setting.deleteTemplate(id_item)

        if not ret:
            self.log.error(Logs.fileline() + ' : TRACE TemplateDet delete ERROR')
            try:
                details = {"id_item": id_item, "result": "ERROR", "action": "DELETE"}
                Audit.insertAudit(audit_user, "TemplateDet", "SETTING", id_item, "ERROR", details, "D")
            except Exception:
                self.log.exception(Logs.fileline() + ' : TemplateDet ERROR audit delete')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE TemplateDet delete id_item=' + str(id_item))
        try:
            details = {"id_item": id_item, "result": "SUCCESS", "action": "DELETE"}
            Audit.insertAudit(audit_user, "TemplateDet", "SETTING", id_item, "SUCCESS", details, "D")
        except Exception:
            self.log.exception(Logs.fileline() + ' : TemplateDet ERROR audit delete success')
        return compose_ret('', Constants.cst_content_type_json)


class ZipCityAdd(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self, filename):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        if not args or 'id_user' not in args:
            self.log.error(Logs.fileline() + ' : ZipCityAdd ERROR args missing')
            try:
                details = {"filename": filename, "result": "ERROR", "reason": "ARGS_MISSING"}
                Audit.insertAudit(audit_user, "ZipCityAdd", "SETTING", None, "ERROR", details, "E")
            except Exception:
                self.log.exception(Logs.fileline() + ' : ZipCityAdd ERROR audit args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # Read CSV zipcity
        path = Constants.cst_path_tmp

        with open(os.path.join(path, filename).strip(), 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            l_rows = list(csv_reader)

        if not l_rows or len(l_rows) < 2:
            self.log.error(Logs.fileline() + ' : TRACE ZipCityAdd ERROR file empty')
            try:
                details = {"filename": filename, "result": "ERROR", "reason": "FILE_EMPTY"}
                Audit.insertAudit(audit_user, "ZipCityAdd", "SETTING", None, "ERROR", details, "E")
            except Exception:
                self.log.exception(Logs.fileline() + ' : ZipCityAdd ERROR audit file empty')
            return compose_ret('', Constants.cst_content_type_json, 500)

        # remove headers line
        l_rows.pop(0)

        for row in l_rows:
            if row:
                zip_code  = str(row[0])
                city_name = str(row[1])

                # insert into sigl_pj_group
                ret = Setting.insertZipCity(zic_zip=zip_code, zic_city=city_name)

                if ret <= 0:
                    self.log.error(Logs.alert() + ' : ZipCityAdd ERROR insert')
                    try:
                        details = {"zip": zip_code, "city": city_name, "result": "ERROR", "action": "INSERT"}
                        Audit.insertAudit(audit_user, "ZipCityAdd", "SETTING", None, "ERROR", details, "C")
                    except Exception:
                        self.log.exception(Logs.fileline() + ' : ZipCityAdd ERROR audit insert')
                    return compose_ret('', Constants.cst_content_type_json, 500)

        Various.insertEvent(id_user=args['id_user'],
                            type='14',
                            name='EVT_INSERT',
                            message='insert into zip_city')

        self.log.info(Logs.fileline() + ' : TRACE ZipCityAdd')
        try:
            details = {"filename": filename, "rows": len(l_rows), "result": "SUCCESS"}
            Audit.insertAudit(audit_user, "ZipCityAdd", "SETTING", None, "SUCCESS", details, "C")
        except Exception:
            self.log.exception(Logs.fileline() + ' : ZipCityAdd ERROR audit success')
        return compose_ret(ret, Constants.cst_content_type_json)


class ZipCityDelAll(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        if not args or 'id_user' not in args:
            self.log.error(Logs.fileline() + ' : ZipCityDelAll ERROR args missing')
            try:
                details = {"result": "ERROR", "reason": "ARGS_MISSING"}
                Audit.insertAudit(audit_user, "ZipCityDelAll", "SETTING", None, "ERROR", details, "E")
            except Exception:
                self.log.exception(Logs.fileline() + ' : ZipCityDelAll ERROR audit args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        ret = Setting.deleteAllZipCity()

        if not ret:
            self.log.error(Logs.fileline() + ' : TRACE ZipCityDelAll truncate ERROR')
            try:
                details = {"result": "ERROR", "action": "DELETE_ALL"}
                Audit.insertAudit(audit_user, "ZipCityDelAll", "SETTING", None, "ERROR", details, "D")
            except Exception:
                self.log.exception(Logs.fileline() + ' : ZipCityDelAll ERROR audit delete')
            return compose_ret('', Constants.cst_content_type_json, 500)

        Various.insertEvent(id_user=args['id_user'],
                            type='16',
                            name='EVT_DELETE',
                            message='truncate table zip_city')

        self.log.info(Logs.fileline() + ' : TRACE ZipCityDelAll')
        try:
            details = {"result": "SUCCESS", "action": "DELETE_ALL"}
            Audit.insertAudit(audit_user, "ZipCityDelAll", "SETTING", None, "SUCCESS", details, "D")
        except Exception:
            self.log.exception(Logs.fileline() + ' : ZipCityDelAll ERROR audit success')
        return compose_ret(ret, Constants.cst_content_type_json)


class ZipCityDet(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self, id_item):
        audit_user = request.oauth_user
        item = Setting.getZipCity(id_item)

        if not item:
            self.log.error(Logs.fileline() + ' : ' + 'ZipCityDet ERROR not found')
            try:
                details = {"id_item": int(id_item), "reason": "NOT_FOUND"}
                Audit.insertAudit(audit_user, "ZipCityDet", "SETTING", None, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : ZipCityDet ERROR audit not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        # Replace None by empty string
        for key, value in list(item.items()):
            if item[key] is None:
                item[key] = ''

        self.log.info(Logs.fileline() + ' : ZipCityDet id_item=' + str(id_item))
        try:
            details = {"result": "SUCCESS", "action": "QUERY"}
            Audit.insertAudit(audit_user, "ZipCityDet", "SETTING", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : ZipCityDet ERROR audit success')
        return compose_ret(item, Constants.cst_content_type_json, 200)


class ZipCityList(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        l_items = Setting.getZipCityList(args)

        if not l_items:
            self.log.error(Logs.fileline() + ' : TRACE ZipCityList not found')

        for item in l_items:
            # Replace None by empty string
            for key, value in list(item.items()):
                if item[key] is None:
                    item[key] = ''

        self.log.info(Logs.fileline() + ' : TRACE ZipCityList')
        try:
            details = {"result": "SUCCESS", "action": "QUERY", "count": len(l_items)}
            Audit.insertAudit(audit_user, "ZipCityList", "SETTING", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : ZipCityList ERROR audit success')
        return compose_ret(l_items, Constants.cst_content_type_json)


class ZipCitySearch(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        l_zipcity = Setting.getZipCitySearch(args['term'])

        if not l_zipcity:
            self.log.error(Logs.fileline() + ' : TRACE ZipCitySearch not found')

        self.log.info(Logs.fileline() + ' : TRACE ZipCitySearch')
        try:
            details = {"result": "SUCCESS", "action": "QUERY"}
            Audit.insertAudit(audit_user, "ZipCitySearch", "SETTING", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : ZipCitySearch ERROR audit success')
        return compose_ret(l_zipcity, Constants.cst_content_type_json)


class SettingStock(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self):
        audit_user = request.oauth_user
        setting = Setting.getStockSetting()

        if not setting:
            self.log.error(Logs.fileline() + ' : ERROR SettingStock not found')
            try:
                details = {"reason": "NOT_FOUND"}
                Audit.insertAudit(audit_user, "SettingStock", "SETTING", None, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : SettingStock ERROR audit not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        # Replace None by empty string
        for key, value in list(setting.items()):
            if setting[key] is None:
                setting[key] = ''

        self.log.info(Logs.fileline() + ' : TRACE SettingStock')
        try:
            details = {"result": "SUCCESS", "action": "VIEW"}
            Audit.insertAudit(audit_user, "SettingStock", "SETTING", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : SettingStock ERROR audit success')
        return compose_ret(setting, Constants.cst_content_type_json)

    @require_oauth()
    def post(self):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        if 'id_owner' not in args or 'expir_warning' not in args or 'expir_alert' not in args or \
           'list_local' not in args:
            self.log.error(Logs.fileline() + ' : SettingStock ERROR args missing')
            try:
                details = {"reason": "ARGS_MISSING"}
                Audit.insertAudit(audit_user, "SettingStock", "SETTING", None, "ERROR", details, "U")
            except Exception:
                self.log.exception(Logs.fileline() + ' : SettingStock ERROR audit args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        ret = Setting.updateStockSetting(id_owner=args['id_owner'],
                                         expir_warning=args['expir_warning'],
                                         expir_alert=args['expir_alert'])

        if ret is False:
            self.log.error(Logs.alert() + ' : SettingStock ERROR update')
            try:
                details = {"id_owner": args['id_owner'], "result": "ERROR", "action": "UPDATE_STOCK"}
                Audit.insertAudit(audit_user, "SettingStock", "SETTING", None, "ERROR", details, "U")
            except Exception:
                self.log.exception(Logs.fileline() + ' : SettingStock ERROR audit')
            return compose_ret('', Constants.cst_content_type_json, 500)

        if args['list_local']:
            l_local = Quality.getStockLocalList()

            for local in args['list_local']:
                name = local['prl_name']

                if local['prl_ser'] > 0:
                    ret = Setting.updateStockLocal(prl_ser=local['prl_ser'],
                                                   prl_rank=local['prl_rank'],
                                                   prl_name=name)
                    action = "UPDATE"
                else:
                    ret = Setting.insertStockLocal(prl_rank=local['prl_rank'],
                                                   prl_name=name)
                    action = "INSERT"

                if ret is False or ret <= 0:
                    self.log.info(Logs.fileline() + ' : TRACE SettingStock ERROR updateStockLocal')
                    try:
                        details = {"id_owner": args['id_owner'], "prl_ser": local['prl_ser'],
                                   "prl_rank": local['prl_rank'], "prl_name": name, "result": "ERROR", "action": action}
                        event_type = "C" if action == "INSERT" else "U"
                        Audit.insertAudit(audit_user, "SettingStock", "SETTING", None, "ERROR", details, event_type)
                    except Exception:
                        self.log.exception(Logs.fileline() + ' : SettingStock ERROR audit')
                    return compose_ret('', Constants.cst_content_type_json, 500)

            # delete missing values compared to local list
            for db_local in l_local:
                exist = False
                for ihm_local in args['list_local']:
                    if db_local['prl_ser'] == ihm_local['prl_ser']:
                        exist = True

                if not exist:
                    ret = Setting.deleteStockLocal(db_local['prl_ser'])

                    if ret is False:
                        self.log.info(Logs.fileline() + ' : TRACE SettingStock ERROR deleteStockLocal')
                        try:
                            details = {"id_owner": args['id_owner'], "result": "ERROR", "action": "DELETE",
                                       "prl_ser": db_local['prl_ser']}
                            Audit.insertAudit(audit_user, "SettingStock", "SETTING", None, "ERROR", details, "D")
                        except Exception:
                            self.log.exception(Logs.fileline() + ' : SettingStock ERROR audit')
                        return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE SettingStock')
        try:
            details = {"id_owner": args['id_owner'], "result": "SUCCESS", "action": "UPDATE",
                       "local_count": len(args['list_local'])}
            Audit.insertAudit(audit_user, "SettingStock", "SETTING", None, "SUCCESS", details, "U")
        except Exception:
            self.log.exception(Logs.fileline() + ' : SettingStock ERROR audit success')
        return compose_ret('', Constants.cst_content_type_json)


class SettingFormList(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self):
        audit_user = request.oauth_user
        l_items = Setting.getSettingFormList()

        if not l_items:
            self.log.error(Logs.fileline() + ' : TRACE SettingFormList not found')

        Various.useLangPDF()

        for item in l_items:
            # Replace None by empty string
            for key, value in list(item.items()):
                if item[key] is None:
                    item[key] = ''
                elif key == 'fos_name' and item[key]:
                    item[key] = _(item[key].strip())

        self.log.info(Logs.fileline() + ' : TRACE SettingFormList')
        try:
            details = {"result": "SUCCESS", "action": "QUERY"}
            Audit.insertAudit(audit_user, "SettingFormList", "SETTING", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : SettingFormList ERROR audit success')
        return compose_ret(l_items, Constants.cst_content_type_json)


class SettingFormDet(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        if 'id_owner' not in args or 'ref' not in args or 'stat' not in args:
            self.log.error(Logs.fileline() + ' : SettingFormDet ERROR args missing')
            try:
                details = {"reason": "ARGS_MISSING"}
                Audit.insertAudit(audit_user, "SettingFormDet", "SETTING", None, "ERROR", details, "U")
            except Exception:
                self.log.exception(Logs.fileline() + ' : SettingFormDet ERROR audit args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        ret = Setting.updateFormSetting(ref=args['ref'],
                                        stat=args['stat'])

        if ret is False:
            self.log.error(Logs.alert() + ' : SettingFormDet ERROR update')
            try:
                details = {"ref": args['ref'], "stat": args['stat'], "result": "ERROR", "action": "UPDATE"}
                Audit.insertAudit(audit_user, "SettingFormDet", "SETTING", None, "ERROR", details, "U")
            except Exception:
                self.log.exception(Logs.fileline() + ' : SettingFormDet ERROR audit')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE SettingFormDet')
        try:
            details = {"ref": args['ref'], "stat": args['stat'], "result": "SUCCESS", "action": "UPDATE"}
            Audit.insertAudit(audit_user, "SettingFormDet", "SETTING", None, "SUCCESS", details, "U")
        except Exception:
            self.log.exception(Logs.fileline() + ' : SettingFormDet ERROR audit success')
        return compose_ret('', Constants.cst_content_type_json)


class SettingManual(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self):
        audit_user = request.oauth_user
        l_datas = Setting.getManualSetting()

        if not l_datas:
            self.log.error(Logs.fileline() + ' : ' + 'SettingManual ERROR not found')
            try:
                details = {"result": "ERROR", "reason": "NOT_FOUND"}
                Audit.insertAudit(audit_user, "SettingManual", "SETTING", None, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : SettingManual ERROR audit not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        for data in l_datas:
            # Replace None by empty string
            for key, value in list(data.items()):
                if data[key] is None:
                    data[key] = ''

        self.log.info(Logs.fileline() + ' : SettingManual')
        try:
            details = {"result": "SUCCESS", "action": "VIEW"}
            Audit.insertAudit(audit_user, "SettingManual", "SETTING", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : SettingManual ERROR audit success')
        return compose_ret(l_datas, Constants.cst_content_type_json, 200)

    @require_oauth()
    def post(self):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        if 'list_val' not in args:
            self.log.error(Logs.fileline() + ' : SettingManual ERROR args missing')
            try:
                details = {"reason": "ARGS_MISSING"}
                Audit.insertAudit(audit_user, "SettingManual", "SETTING", None, "ERROR", details, "U")
            except Exception:
                self.log.exception(Logs.fileline() + ' : SettingManual ERROR audit args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        l_manuals = Setting.getManualSetting()

        for val in args['list_val']:
            name = val['mas_name']

            if val['mas_ser'] > 0:
                ret = Setting.updateManualSetting(mas_ser=val['mas_ser'],
                                                  mas_rank=val['mas_rank'],
                                                  mas_name=name)
                action = "UPDATE"
            else:
                ret = Setting.insertManualSetting(mas_rank=val['mas_rank'],
                                                  mas_name=name)
                action = "INSERT"

            if ret is False or ret <= 0:
                self.log.info(Logs.fileline() + ' : TRACE SettingManual ERROR updateManual')
                try:
                    details = {"mas_ser": val['mas_ser'], "result": "ERROR", "action": action}
                    event_type = "C" if action == "INSERT" else "U"
                    Audit.insertAudit(audit_user, "SettingManual", "SETTING", None, "ERROR", details, event_type)
                except Exception:
                    self.log.exception(Logs.fileline() + ' : SettingManual ERROR audit')
                return compose_ret('', Constants.cst_content_type_json, 500)

        # delete missing values compared to age interval
        for db_val in l_manuals:
            exist = False
            for ihm_val in args['list_val']:
                if db_val['mas_ser'] == ihm_val['mas_ser']:
                    exist = True

            if not exist:
                ret = Setting.deleteManualSetting(db_val['mas_ser'])

                if ret is False:
                    self.log.info(Logs.fileline() + ' : TRACE SettingManual ERROR deleteManual')
                    try:
                        details = {"mas_ser": db_val['mas_ser'], "result": "ERROR", "action": "DELETE"}
                        Audit.insertAudit(audit_user, "SettingManual", "SETTING", None, "ERROR", details, "D")
                    except Exception:
                        self.log.exception(Logs.fileline() + ' : SettingManual ERROR audit')
                    return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE SettingManual')
        try:
            details = {"count": len(args['list_val']), "result": "SUCCESS"}
            Audit.insertAudit(audit_user, "SettingManual", "SETTING", None, "SUCCESS", details, "U")
        except Exception:
            self.log.exception(Logs.fileline() + ' : SettingManual ERROR audit success')
        return compose_ret('', Constants.cst_content_type_json)


class SettingManualCat(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self):
        audit_user = request.oauth_user
        l_datas = Setting.getManualCategory()

        if not l_datas:
            self.log.error(Logs.fileline() + ' : ' + 'SettingManualCat ERROR not found')
            try:
                details = {"reason": "NOT_FOUND"}
                Audit.insertAudit(audit_user, "SettingManualCat", "SETTING", None, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : SettingManualCat ERROR audit not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        for data in l_datas:
            # Replace None by empty string
            for key, value in list(data.items()):
                if data[key] is None:
                    data[key] = ''

        self.log.info(Logs.fileline() + ' : SettingManualCat')
        try:
            details = {"result": "SUCCESS", "action": "VIEW"}
            Audit.insertAudit(audit_user, "SettingManualCat", "SETTING", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : SettingManualCat ERROR audit success')
        return compose_ret(l_datas, Constants.cst_content_type_json, 200)


class SettingDHIS2List(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self):
        audit_user = request.oauth_user
        l_items = Setting.getDHIS2List()

        if not l_items:
            self.log.error(Logs.fileline() + ' : TRACE SettingDHIS2List not found')

        for item in l_items:
            # Replace None by empty string
            for key, value in list(item.items()):
                if item[key] is None:
                    item[key] = ''

        self.log.info(Logs.fileline() + ' : TRACE SettingDHIS2List')
        try:
            details = {"result": "SUCCESS", "action": "QUERY"}
            Audit.insertAudit(audit_user, "SettingDHIS2List", "SETTING", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : SettingDHIS2List ERROR audit success')
        return compose_ret(l_items, Constants.cst_content_type_json)


class SettingDHIS2Det(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self, id_item):
        audit_user = request.oauth_user
        item = Setting.getDHIS2Det(id_item)

        if not item:
            self.log.error(Logs.fileline() + ' : ERROR SettingDHIS2Det not found')
            try:
                details = {"id_item": int(id_item), "reason": "NOT_FOUND"}
                Audit.insertAudit(audit_user, "SettingDHIS2Det", "SETTING", int(id_item), "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : SettingDHIS2Det ERROR audit not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        self.log.info(Logs.fileline() + ' : TRACE SettingDHIS2Det')
        try:
            details = {"result": "SUCCESS", "action": "VIEW", "id_item": int(id_item)}
            Audit.insertAudit(audit_user, "SettingDHIS2Det", "SETTING", int(id_item), "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : SettingDHIS2Det ERROR audit success')
        return compose_ret(item, Constants.cst_content_type_json)

    @require_oauth()
    def post(self, id_item):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        if 'id_user' not in args or 'name' not in args or 'login' not in args or 'pwd' not in args or \
           'url' not in args or 'default' not in args:
            self.log.error(Logs.fileline() + ' : SettingDHIS2Det ERROR args missing')
            try:
                details = {"id_item": int(id_item), "reason": "ARGS_MISSING"}
                Audit.insertAudit(audit_user, "SettingDHIS2Det", "SETTING", int(id_item), "ERROR", details, "U")
            except Exception:
                self.log.exception(Logs.fileline() + ' : SettingDHIS2Det ERROR audit args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        action = "UPDATE" if id_item > 0 else "INSERT"

        # Update item
        if id_item > 0:
            self.log.info(Logs.fileline() + ' : TRACE updateDHIS2Det')

            ret = Setting.updateDHIS2Det(id_item=id_item,
                                         user=args['id_user'],
                                         name=args['name'],
                                         login=args['login'],
                                         pwd=args['pwd'],
                                         url=args['url'],
                                         default=args['default'])

            action = "UPDATE"

            if ret is False:
                self.log.error(Logs.alert() + ' : SettingDHIS2Det ERROR update')
                try:
                    details = {"id_item": id_item, "id_user": args['id_user'], "name": args['name'],
                               "result": "ERROR", "action": "UPDATE"}
                    Audit.insertAudit(audit_user, "SettingDHIS2Det", "SETTING", id_item, "ERROR", details, "U")
                except Exception:
                    self.log.exception(Logs.fileline() + ' : SettingDHIS2Det ERROR audit')
                return compose_ret('', Constants.cst_content_type_json, 500)

        # Insert new item
        else:
            self.log.info(Logs.fileline() + ' : TRACE insertDHIS2Det')
            ret = Setting.insertDHIS2Det(user=args['id_user'],
                                         name=args['name'],
                                         login=args['login'],
                                         pwd=args['pwd'],
                                         url=args['url'],
                                         default=args['default'])

            action = "INSERT"

            if ret <= 0:
                self.log.error(Logs.alert() + ' : SettingDHIS2Det ERROR  insert')
                try:
                    details = {"id_item": ret, "id_user": args['id_user'], "name": args['name'],
                               "result": "ERROR", "action": "INSERT"}
                    Audit.insertAudit(audit_user, "SettingDHIS2Det", "SETTING", ret, "ERROR", details, "C")
                except Exception:
                    self.log.exception(Logs.fileline() + ' : SettingDHIS2Det ERROR audit')
                return compose_ret('', Constants.cst_content_type_json, 500)

            id_item = ret

        self.log.info(Logs.fileline() + ' : TRACE SettingDHIS2Det')
        try:
            details = {"id_item": id_item, "id_user": args['id_user'], "name": args['name'], "result": "SUCCESS",
                       "action": action}
            event_type = "C" if action == "INSERT" else "U"
            Audit.insertAudit(audit_user, "SettingDHIS2Det", "SETTING", id_item, "SUCCESS", details, event_type)
        except Exception:
            self.log.exception(Logs.fileline() + ' : SettingDHIS2Det ERROR audit success')
        return compose_ret('', Constants.cst_content_type_json)

    @require_oauth()
    def delete(self, id_item):
        audit_user = request.oauth_user
        ret = Setting.deleteDHIS2Det(id_item)

        if not ret:
            self.log.error(Logs.fileline() + ' : TRACE SettingDHIS2Det delete ERROR')
            try:
                details = {"id_item": id_item, "result": "ERROR", "action": "DELETE"}
                Audit.insertAudit(audit_user, "SettingDHIS2Det", "SETTING", id_item, "ERROR", details, "D")
            except Exception:
                self.log.exception(Logs.fileline() + ' : SettingDHIS2Det ERROR audit')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE SettingDHIS2Det delete id_item=' + str(id_item))
        try:
            details = {"id_item": id_item, "result": "SUCCESS", "action": "DELETE"}
            Audit.insertAudit(audit_user, "SettingDHIS2Det", "SETTING", id_item, "SUCCESS", details, "D")
        except Exception:
            self.log.exception(Logs.fileline() + ' : SettingDHIS2Det ERROR audit success')
        return compose_ret('', Constants.cst_content_type_json)


class SettingSendMethodList(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self):
        audit_user = request.oauth_user
        l_items = Setting.getSendingMethodList()

        if not l_items:
            self.log.info(Logs.fileline() + ' : TRACE SendingMethodList not found')

        for item in l_items:
            # Replace None by empty string
            for key, value in list(item.items()):
                if item[key] is None:
                    item[key] = ''

            if item['sdi_date']:
                item['sdi_date'] = datetime.strftime(item['sdi_date'], '%Y-%m-%d')

        self.log.info(Logs.fileline() + ' : TRACE SettingSendMethodList')
        try:
            details = {"result": "SUCCESS", "action": "QUERY", "count": len(l_items)}
            Audit.insertAudit(audit_user, "SettingSendMethodList", "SETTING", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : SettingSendMethodList ERROR audit success')
        return compose_ret(l_items, Constants.cst_content_type_json)


class SettingSendMethodDet(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self, type, id_item):
        audit_user = request.oauth_user
        item = Setting.getSendingMethodDet(type, id_item)

        if not item:
            self.log.error(Logs.fileline() + ' : ERROR SettingSendMethodDet not found')
            try:
                details = {"type": str(type), "id_item": int(id_item), "reason": "NOT_FOUND"}
                Audit.insertAudit(audit_user, "SettingSendMethodDet", "SETTING", int(id_item), "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : SettingSendMethodDet ERROR audit not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        # Replace None by empty string
        for key, value in list(item.items()):
            if item[key] is None:
                item[key] = ''
            elif isinstance(value, (bytes, bytearray)):
                item[key] = value.decode('utf-8', errors='ignore')
            elif hasattr(value, 'strftime'):
                item[key] = value.strftime('%Y-%m-%d')

        self.log.info(Logs.fileline() + ' : TRACE SettingSendMethodDet')
        try:
            details = {"result": "SUCCESS", "action": "VIEW", "type": type, "id_item": int(id_item)}
            Audit.insertAudit(audit_user, "SettingSendMethodDet", "SETTING", int(id_item), "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : SettingSendMethodDet ERROR audit success')
        return compose_ret(item, Constants.cst_content_type_json)

    @require_oauth()
    def post(self, type, id_item):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        if 'sdi_type' not in args or 'sdi_name' not in args or 'sdi_default' not in args:
            self.log.error(Logs.fileline() + ' : SettingSendMethodDet ERROR args missing')
            try:
                details = {"id_item": id_item, "sdi_type": args.get('sdi_type') if isinstance(args, dict) else None,
                           "result": "ERROR", "reason": "ARGS_MISSING"}
                Audit.insertAudit(audit_user, "SettingSendMethodDet", "SETTING", None, "ERROR", details, "E")
            except Exception:
                self.log.exception(Logs.fileline() + ' : SettingSendMethodDet ERROR audit args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        action = "UPDATE" if id_item > 0 else "INSERT"

        # Update item
        if id_item > 0:
            ret = Setting.updateSendingMethodDet(**args)

            action = "UPDATE"

            if ret is False:
                self.log.error(Logs.alert() + ' : SettingSendMethodDet ERROR update')
                try:
                    details = {"id_item": id_item, "sdi_type": args['sdi_type'], "sdi_name": args['sdi_name'],
                               "result": "ERROR", "action": "UPDATE"}
                    Audit.insertAudit(audit_user, "SettingSendMethodDet", "SETTING", id_item, "ERROR", details, "U")
                except Exception:
                    self.log.exception(Logs.fileline() + ' : SettingSendMethodDet ERROR audit update')
                return compose_ret('', Constants.cst_content_type_json, 500)

        # Insert new item
        else:
            ret = Setting.insertSendingMethodDet(**args)

            action = "INSERT"

            if ret <= 0:
                self.log.error(Logs.alert() + ' : SettingSendMethodDet ERROR insert')
                try:
                    details = {"id_item": ret, "sdi_type": args['sdi_type'], "sdi_name": args['sdi_name'],
                               "result": "ERROR", "action": "INSERT"}
                    Audit.insertAudit(audit_user, "SettingSendMethodDet", "SETTING", None, "ERROR", details, "C")
                except Exception:
                    self.log.exception(Logs.fileline() + ' : SettingSendMethodDet ERROR audit insert')
                return compose_ret('', Constants.cst_content_type_json, 500)

            id_item = ret

        self.log.info(Logs.fileline() + ' : TRACE SettingSendMethodDet')
        try:
            details = {"id_item": id_item, "sdi_type": args['sdi_type'], "sdi_name": args['sdi_name'],
                       "result": "SUCCESS", "action": action}
            event_type = "C" if action == "INSERT" else "U"
            Audit.insertAudit(audit_user, "SettingSendMethodDet", "SETTING", id_item, "SUCCESS", details, event_type)
        except Exception:
            self.log.exception(Logs.fileline() + ' : SettingSendMethodDet ERROR audit success')
        return compose_ret(id_item, Constants.cst_content_type_json)

    @require_oauth()
    def delete(self, type, id_item):
        audit_user = request.oauth_user
        ret = Setting.deleteSendingMethodDet(type, id_item)

        if not ret:
            self.log.error(Logs.fileline() + ' : TRACE SettingSendMethodDet delete ERROR')
            try:
                details = {"id_item": id_item, "result": "ERROR", "action": "DELETE"}
                Audit.insertAudit(audit_user, "SettingSendMethodDet", "SETTING", id_item, "ERROR", details, "D")
            except Exception:
                self.log.exception(Logs.fileline() + ' : SettingSendMethodDet ERROR audit delete')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE SettingSendMethodDet delete id_item=' + str(id_item))
        try:
            details = {"id_item": id_item, "result": "SUCCESS", "action": "DELETE"}
            Audit.insertAudit(audit_user, "SettingSendMethodDet", "SETTING", id_item, "SUCCESS", details, "D")
        except Exception:
            self.log.exception(Logs.fileline() + ' : SettingSendMethodDet ERROR audit delete success')
        return compose_ret('', Constants.cst_content_type_json)


class SettingSendMethodTest(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self, type, id_item):
        audit_user = request.oauth_user
        payload = request.get_json(silent=True) or {}
        to = payload.get('to')

        if type == 'S':
            ok, msg = Setting.testSmtpMethod(id_item, to)
        elif type == 'M':
            ok, msg = Setting.testMailjetMethod(id_item, to)
        elif type == 'W':
            ok, msg = Setting.testWhatsappMethod(id_item, to)
        else:
            return compose_ret({'error': 'Test not available for this type'}, Constants.cst_content_type_json, 400)

        if ok:
            self.log.info(Logs.fileline() + f' : {type} test OK for id={id_item}')
            try:
                details = {"id_item": id_item, "type": type, "to": to, "result": "SUCCESS"}
                Audit.insertAudit(audit_user, "SettingSendMethodTest", "SETTING", id_item, "SUCCESS", details, "E")
            except Exception:
                self.log.exception(Logs.fileline() + ' : SettingSendMethodTest ERROR audit success')
            return compose_ret({'message': msg}, Constants.cst_content_type_json)
        else:
            self.log.error(Logs.fileline() + f' : {type} test FAIL for id={id_item} -> {msg}')
            try:
                details = {"id_item": id_item, "type": type, "to": to, "result": "ERROR", "reason": msg}
                Audit.insertAudit(audit_user, "SettingSendMethodTest", "SETTING", id_item, "ERROR", details, "E")
            except Exception:
                self.log.exception(Logs.fileline() + ' : SettingSendMethodTest ERROR audit fail')
            return compose_ret({'error': msg}, Constants.cst_content_type_json, 400)


class SettingSendModelList(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self):
        audit_user = request.oauth_user
        l_items = Setting.getSendingModelList()

        if not l_items:
            self.log.info(Logs.fileline() + ' : TRACE SendingModelList not found')

        for item in l_items:
            # Replace None by empty string
            for key, value in list(item.items()):
                if item[key] is None:
                    item[key] = ''

            if item['mdl_date']:
                item['mdl_date'] = datetime.strftime(item['mdl_date'], '%Y-%m-%d')

        self.log.info(Logs.fileline() + ' : TRACE SettingSendModelList')
        try:
            details = {"result": "SUCCESS", "action": "QUERY", "count": len(l_items)}
            Audit.insertAudit(audit_user, "SettingSendModelList", "SETTING", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : SettingSendModelList ERROR audit success')
        return compose_ret(l_items, Constants.cst_content_type_json)


class SettingSendModelDet(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self, type, id_item):
        audit_user = request.oauth_user
        item = Setting.getSendingModelDet(type, id_item)

        if not item:
            self.log.error(Logs.fileline() + ' : ERROR SettingSendModelDet not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        # Replace None by empty string
        for key, value in list(item.items()):
            if item[key] is None:
                item[key] = ''
            elif hasattr(value, 'strftime'):
                item[key] = value.strftime('%Y-%m-%d')

        self.log.info(Logs.fileline() + ' : TRACE SettingSendModelDet')
        try:
            details = {"result": "SUCCESS", "action": "VIEW", "id_item": int(id_item)}
            Audit.insertAudit(audit_user, "SettingSendModelDet", "SETTING", int(id_item), "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : SettingSendModelDet ERROR audit success')
        return compose_ret(item, Constants.cst_content_type_json)

    @require_oauth()
    def post(self, type, id_item):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        if 'mdl_type' not in args or 'mdl_displayname' not in args or 'mdl_default' not in args:
            self.log.error(Logs.fileline() + ' : SettingSendModelDet ERROR args missing')
            try:
                details = {"id_item": id_item, "type": type, "result": "ERROR", "reason": "ARGS_MISSING"}
                Audit.insertAudit(audit_user, "SettingSendModelDet", "SETTING", None, "ERROR", details, "E")
            except Exception:
                self.log.exception(Logs.fileline() + ' : SettingSendModelDet ERROR audit args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        ret_id = id_item

        # Update item
        if id_item > 0:
            ret = Setting.updateSendingModelDet(**args)

            action = "UPDATE"

            if ret is False:
                self.log.error(Logs.alert() + ' : SettingSendModelDet ERROR update')
                try:
                    details = {"id_item": id_item, "type": type, "mdl_displayname": args.get('mdl_displayname'),
                               "result": "ERROR", "action": "UPDATE"}
                    Audit.insertAudit(audit_user, "SettingSendModelDet", "SETTING", id_item, "ERROR", details, "U")
                except Exception:
                    self.log.exception(Logs.fileline() + ' : SettingSendModelDet ERROR audit update')
                return compose_ret('', Constants.cst_content_type_json, 500)

        # Insert new item
        else:
            action = "INSERT"
            ret = Setting.insertSendingModelDet(**args)

            if ret <= 0:
                self.log.error(Logs.alert() + ' : SettingSendModelDet ERROR insert')
                try:
                    details = {"id_item": ret, "type": type, "mdl_displayname": args.get('mdl_displayname'),
                               "result": "ERROR", "action": "INSERT"}
                    Audit.insertAudit(audit_user, "SettingSendModelDet", "SETTING", None, "ERROR", details, "C")
                except Exception:
                    self.log.exception(Logs.fileline() + ' : SettingSendModelDet ERROR audit insert')
                return compose_ret('', Constants.cst_content_type_json, 500)

            id_item = ret
            ret_id = ret

        self.log.info(Logs.fileline() + ' : TRACE SettingSendModelDet')
        try:
            details = {"id_item": ret_id, "type": type, "mdl_displayname": args.get('mdl_displayname'),
                       "result": "SUCCESS", "action": action}
            event_type = "C" if action == "INSERT" else "U"
            Audit.insertAudit(audit_user, "SettingSendModelDet", "SETTING", ret_id, "SUCCESS", details, event_type)
        except Exception:
            self.log.exception(Logs.fileline() + ' : SettingSendModelDet ERROR audit success')
        return compose_ret(id_item, Constants.cst_content_type_json)

    @require_oauth()
    def delete(self, type, id_item):
        audit_user = request.oauth_user
        ret = Setting.deleteSendingModelDet(type, id_item)

        if not ret:
            self.log.error(Logs.fileline() + ' : TRACE SettingSendModelDet delete ERROR')
            try:
                details = {"id_item": id_item, "type": type, "result": "ERROR", "action": "DELETE"}
                Audit.insertAudit(audit_user, "SettingSendModelDet", "SETTING", id_item, "ERROR", details, "D")
            except Exception:
                self.log.exception(Logs.fileline() + ' : SettingSendModelDet ERROR audit delete')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE SettingSendModelDet delete id_item=' + str(id_item))
        try:
            details = {"id_item": id_item, "type": type, "result": "SUCCESS", "action": "DELETE"}
            Audit.insertAudit(audit_user, "SettingSendModelDet", "SETTING", id_item, "SUCCESS", details, "D")
        except Exception:
            self.log.exception(Logs.fileline() + ' : SettingSendModelDet ERROR audit delete success')
        return compose_ret('', Constants.cst_content_type_json)


class SettingSendModelTest(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self, type, mdl_ser):
        audit_user = request.oauth_user
        try:
            payload = request.get_json(force=True) or {}
            to   = (payload.get('to') or '').strip()
            override_method_id = payload.get('method_id')  # optional

            if not to:
                try:
                    details = {"mdl_ser": mdl_ser, "type": type, "result": "ERROR", "reason": "MISSING_RECIPIENT"}
                    Audit.insertAudit(audit_user, "SettingSendModelTest", "SETTING", mdl_ser, "ERROR", details, "E")
                except Exception:
                    self.log.exception(Logs.fileline() + ' : SettingSendModelTest ERROR audit missing recipient')
                return compose_ret({'error': 'missing recipient'}, Constants.cst_content_type_json, 400)

            # Load model
            model = Setting.getSendingModelDet(type, mdl_ser)
            if not model:
                try:
                    details = {"mdl_ser": mdl_ser, "type": type, "result": "ERROR", "reason": "MODEL_NOT_FOUND"}
                    Audit.insertAudit(audit_user, "SettingSendModelTest", "SETTING", mdl_ser, "ERROR", details, "E")
                except Exception:
                    self.log.exception(Logs.fileline() + ' : SettingSendModelTest ERROR audit model not found')
                return compose_ret({'error': 'model not found'}, Constants.cst_content_type_json, 404)

            # Pick method (override -> default -> last by date)
            method_id = Setting.pickMethodIdForTest(type, override_method_id)
            if not method_id:
                try:
                    details = {"mdl_ser": mdl_ser, "type": type, "result": "ERROR", "reason": "NO_METHOD_CONFIGURED"}
                    Audit.insertAudit(audit_user, "SettingSendModelTest", "SETTING", mdl_ser, "ERROR", details, "E")
                except Exception:
                    self.log.exception(Logs.fileline() + ' : SettingSendModelTest ERROR audit no method configured')
                return compose_ret({'error': 'no sending method configured for this type'}, Constants.cst_content_type_json, 412)

            # Dispatch by type
            ok = False
            type_up = (type or '').upper()[:1]
            subject = f"[TEST] {model.get('mdl_displayname') or 'Model'}"

            if type_up == 'S':
                # SMTP: plain text body
                body_text = model.get('mdl_text') or ''
                ok = Setting.send_test_smtp(method_id, to, subject, body_text)

            elif type_up == 'M':
                # Mailjet: HTML allowed
                html_body = model.get('mdl_text') or ''
                ok = Setting.send_test_mailjet(method_id, to, subject, html_body)

            elif type_up == 'W':
                # WhatsApp: template name
                template_name = model.get('mdl_name') or ''
                template_lang = (payload.get('lang') or model.get('mdl_lang') or 'en').strip()
                ok = Setting.send_test_whatsapp(method_id, to, template_name, template_lang)

            else:
                try:
                    details = {"mdl_ser": mdl_ser, "type": type, "method_id": method_id, "to": to,
                               "result": "ERROR", "reason": "INVALID_TYPE", "action": "TEST"}
                    Audit.insertAudit(audit_user, "SettingSendModelTest", "SETTING", mdl_ser, "ERROR", details, "E")
                except Exception:
                    self.log.exception(Logs.fileline() + ' : SettingSendModelTest ERROR audit success')
                return compose_ret({'error': 'invalid type'}, Constants.cst_content_type_json, 400)

            if ok:
                try:
                    details = {"mdl_ser": mdl_ser, "type": type, "method_id": method_id, "to": to,
                               "result": "SUCCESS", "action": "TEST"}
                    Audit.insertAudit(audit_user, "SettingSendModelTest", "SETTING", mdl_ser, "SUCCESS", details, "E")
                except Exception:
                    self.log.exception(Logs.fileline() + ' : SettingSendModelTest ERROR audit success')
                return compose_ret({'message': 'test sent'}, Constants.cst_content_type_json, 200)
            else:
                try:
                    details = {"mdl_ser": mdl_ser, "type": type, "method_id": method_id, "to": to,
                               "result": "ERROR", "action": "TEST"}
                    Audit.insertAudit(audit_user, "SettingSendModelTest", "SETTING", mdl_ser, "ERROR", details, "E")
                except Exception:
                    self.log.exception(Logs.fileline() + ' : SettingSendModelTest ERROR audit send failed')
                return compose_ret({'error': 'send failed'}, Constants.cst_content_type_json, 502)

        except Exception as e:
            self.log.exception(Logs.fileline() + f' : ERROR model test, err={e}')
            try:
                details = {"mdl_ser": mdl_ser, "type": type, "result": "ERROR", "reason": "EXCEPTION"}
                Audit.insertAudit(audit_user, "SettingSendModelTest", "SETTING", mdl_ser, "ERROR", details, "E")
            except Exception:
                self.log.exception(Logs.fileline() + ' : SettingSendModelTest ERROR audit exception')
            return compose_ret({'error': 'internal error'}, Constants.cst_content_type_json, 500)


class SettingSendReport(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self):
        audit_user = request.oauth_user

        data = request.get_json(silent=True) or {}
        method_id   = data.get("method_id") or 0
        method_type = data.get("method_type") or ''
        template_id = data.get("template_id") or 0
        recipient   = (data.get("recipient") or '').strip()
        filename    = (data.get("file") or '').strip()
        rec_num     = data.get("rec_num")
        pat_code    = data.get("pat_code") or ''
        id_user     = data.get("id_user") or 0

        try:
            ok, msg = Setting.sendReport(method_id=method_id,
                                         method_type=method_type,
                                         template_id=template_id,
                                         recipient=recipient,
                                         filename=filename,
                                         rec_num=rec_num,
                                         pat_code=pat_code,
                                         id_user=id_user)
        except Exception as e:
            self.log.exception(Logs.fileline() + ' : ERROR SettingSendReport exception err=' + str(e))
            try:
                details = {"method_id": method_id, "method_type": method_type, "template_id": template_id,
                           "recipient": recipient, "rec_num": rec_num, "pat_code": pat_code, "id_user": id_user, "result": "ERROR", "reason": "EXCEPTION"}
                Audit.insertAudit(audit_user, "SettingSendReport", "SETTING", None, "ERROR", details, "E")
            except Exception:
                self.log.exception(Logs.fileline() + ' : SettingSendReport ERROR audit exception')
            return compose_ret({'error': "Erreur lors de l’envoi."}, Constants.cst_content_type_json, 500)

        if not ok:
            self.log.error(Logs.fileline() + ' : SettingSendReport FAIL -> ' + str(msg))
            try:
                details = {"method_id": method_id, "method_type": method_type, "template_id": template_id,
                           "recipient": recipient, "rec_num": rec_num, "pat_code": pat_code, "id_user": id_user,
                           "result": "ERROR", "reason": "SEND_FAILED", "message": msg}
                Audit.insertAudit(audit_user, "SettingSendReport", "SETTING", None, "ERROR", details, "E")
            except Exception:
                self.log.exception(Logs.fileline() + ' : SettingSendReport ERROR audit send failed')
            return compose_ret({'error': msg or "Échec de l’envoi."}, Constants.cst_content_type_json, 502)

        self.log.info(Logs.fileline() + f' : SettingSendReport OK method={method_id} tpl={template_id} rec={rec_num} user={id_user}')

        try:
            details = {"method_id": method_id, "method_type": method_type, "template_id": template_id,
                       "recipient": recipient, "rec_num": rec_num, "pat_code": pat_code, "id_user": id_user,
                       "result": "SUCCESS", "reason": "SEND_OK"}
            Audit.insertAudit(audit_user, "SettingSendReport", "SETTING", None, "SUCCESS", details, "E")
        except Exception:
            self.log.exception(Logs.fileline() + ' : SettingSendReport ERROR audit success')
        return compose_ret({'message': "Envoi déclenché."}, Constants.cst_content_type_json, 200)


class SettingSendList(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self):
        """
        Return a list of sending_event rows for the DataTable.
        """
        audit_user = request.oauth_user
        args  = request.get_json(silent=True) or {}
        limit = args.get('limit') or 1000

        rows = Setting.getSendingList(limit=limit)

        for r in rows:
            try:
                if r.get('sde_date') and hasattr(r['sde_date'], 'strftime'):
                    r['sde_date'] = r['sde_date'].strftime('%Y-%m-%d %H:%M:%S')
            except Exception as err:
                # the date is returned unformatted rather than losing the whole row
                self.log.warning(Logs.fileline() + ' : sde_date formatting failed, err=' + str(err))

            for k, v in list(r.items()):
                if r[k] is None:
                    r[k] = ''

        self.log.info(Logs.fileline() + ' : SettingSendList count=' + str(len(rows)))
        try:
            details = {"result": "SUCCESS", "action": "QUERY", "count": len(rows), "limit": int(limit)}
            Audit.insertAudit(audit_user, "SettingSendList", "SETTING", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : SettingSendList ERROR audit success')
        return compose_ret(rows, Constants.cst_content_type_json, 200)


class SettingSendResend(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self, sde_ser):
        audit_user = request.oauth_user
        data = request.get_json(silent=True) or {}

        try:
            id_user = int(data.get("id_user") or 0)
        except Exception:
            id_user = 0

        try:
            ok, msg = Setting.resend(sde_ser=sde_ser, id_user=id_user)
        except Exception as e:
            self.log.exception(Logs.fileline() + ' : ERROR SettingSendResend exception err=' + str(e))
            try:
                details = {"sde_ser": sde_ser, "id_user": id_user, "result": "ERROR", "reason": "EXCEPTION",
                           "message": str(e)}
                Audit.insertAudit(audit_user, "SettingSendResend", "SETTING", sde_ser, "ERROR", details, "E")
            except Exception:
                self.log.exception(Logs.fileline() + ' : SettingSendResend ERROR audit exception')
            return compose_ret({'error': "Erreur lors du réenvoi."}, Constants.cst_content_type_json, 500)

        if not ok:
            self.log.error(Logs.fileline() + ' : SettingSendResend FAIL -> ' + str(msg))
            try:
                details = {"sde_ser": sde_ser, "id_user": id_user, "result": "ERROR", "reason": "RESEND_FAILED",
                           "message": msg}
                Audit.insertAudit(audit_user, "SettingSendResend", "SETTING", sde_ser, "ERROR", details, "E")
            except Exception:
                self.log.exception(Logs.fileline() + ' : SettingSendResend ERROR audit failed')
            return compose_ret({'error': msg or "Échec du réenvoi."}, Constants.cst_content_type_json, 502)

        self.log.info(Logs.fileline() + f' : SettingSendResend OK sde_ser={sde_ser} user={id_user}')
        try:
            details = {"sde_ser": sde_ser, "id_user": id_user, "result": "SUCCESS", "reason": "RESEND_OK"}
            Audit.insertAudit(audit_user, "SettingSendResend", "SETTING", sde_ser, "SUCCESS", details, "E")
        except Exception:
            self.log.exception(Logs.fileline() + ' : SettingSendResend ERROR audit success')
        return compose_ret({'message': "Réenvoi déclenché."}, Constants.cst_content_type_json, 200)


class SettingOauthList(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self):
        audit_user = request.oauth_user
        l_items = Setting.getSettingOauthList()

        if not l_items:
            self.log.error(Logs.fileline() + ' : TRACE SettingOauthList not found')

        for item in l_items:
            # Replace None by empty string
            for key, value in list(item.items()):
                if item[key] is None:
                    item[key] = ''

        self.log.info(Logs.fileline() + ' : TRACE SettingOauthList')
        try:
            details = {"result": "SUCCESS", "action": "QUERY", "count": len(l_items)}
            Audit.insertAudit(audit_user, "SettingOauthList", "SETTING", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : SettingOauthList ERROR audit success')
        return compose_ret(l_items, Constants.cst_content_type_json)


class SettingOauthDet(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self, id_item):
        audit_user = request.oauth_user
        item = Setting.getSettingOauth(id_item)

        if not item:
            self.log.error(Logs.fileline() + ' : ' + 'SettingOauthDet ERROR not found')
            try:
                details = {"id_item": int(id_item), "reason": "NOT_FOUND"}
                Audit.insertAudit(audit_user, "SettingOauthDet", "SETTING", int(id_item), "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : SettingOauthDet ERROR audit not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        # Replace None by empty string
        for key, value in list(item.items()):
            if item[key] is None:
                item[key] = ''

        self.log.info(Logs.fileline() + ' : SettingOauthDet id_item=' + str(id_item))
        try:
            details = {"result": "SUCCESS", "action": "VIEW", "id_item": int(id_item)}
            Audit.insertAudit(audit_user, "SettingOauthDet", "SETTING", int(id_item), "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : SettingOauthDet ERROR audit success')
        return compose_ret(item, Constants.cst_content_type_json, 200)

    @require_oauth()
    def post(self, id_item):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        # STEP 1: basic shape validation
        wanted = [
            'oacl_client_id', 'oacl_client_secret', 'oacl_client_name',
            'oacl_user_id', 'oacl_redirect_uris', 'oacl_scope',
            'oacl_grant_types', 'oacl_response_types',
            'oacl_token_endpoint_auth_method', 'oacl_is_active'
        ]
        # Provide server-side defaults to tolerate partial payloads
        defaults = {
            'oacl_client_secret': '',
            'oacl_user_id': 0,
            'oacl_redirect_uris': '',
            'oacl_scope': '',
            'oacl_grant_types': 'authorization_code',
            'oacl_response_types': 'code',
            'oacl_token_endpoint_auth_method': 'none',
            'oacl_is_active': 'Y',
        }
        params = {k: args.get(k, defaults.get(k)) for k in wanted}

        # STEP 2: protect the built-in FE client against any modification
        if id_item > 0:
            cur = Setting.getSettingOauth(id_item)
            if not cur:
                self.log.error(Logs.fileline() + ' : SettingOauthDet update target not found')
                try:
                    details = {"id_item": id_item, "result": "ERROR", "reason": "NOT_FOUND", "action": "UPDATE"}
                    Audit.insertAudit(audit_user, "SettingOauthDet", "SETTING", id_item, "ERROR", details, "U")
                except Exception:
                    self.log.exception(Logs.fileline() + ' : SettingOauthDet ERROR audit not found')
                return compose_ret('', Constants.cst_content_type_json, 404)
            if cur['oacl_client_id'] == 'labbook-FE':
                self.log.error(Logs.fileline() + ' : SettingOauthDet update forbidden for labbook-FE')
                try:
                    details = {"id_item": id_item, "client_id": cur.get('oacl_client_id'), "result": "ERROR",
                               "reason": "FORBIDDEN_FE_CLIENT", "action": "UPDATE"}
                    Audit.insertAudit(audit_user, "SettingOauthDet", "SETTING", id_item, "ERROR", details, "U")
                except Exception:
                    self.log.exception(Logs.fileline() + ' : SettingOauthDet ERROR audit forbidden')
                return compose_ret({'error': 'forbidden'}, Constants.cst_content_type_json, 403)
            # Carry id for WHERE clause
            params['oacl_ser'] = id_item

            # STEP 3: do update
            ok = Setting.updateSettingOauth(**params)

            if not ok:
                self.log.error(Logs.alert() + ' : SettingOauthDet ERROR update')
                try:
                    details = {"id_item": id_item, "client_id": params.get('oacl_client_id'), "result": "ERROR",
                               "reason": "UPDATE_FAILED", "action": "UPDATE"}
                    Audit.insertAudit(audit_user, "SettingOauthDet", "SETTING", id_item, "ERROR", details, "U")
                except Exception:
                    self.log.exception(Logs.fileline() + ' : SettingOauthDet ERROR audit update')
                return compose_ret('', Constants.cst_content_type_json, 500)

            self.log.info(Logs.fileline() + ' : SettingOauthDet updated id=' + str(id_item))
            try:
                details = {"id_item": id_item, "client_id": params.get('oacl_client_id'), "result": "SUCCESS",
                           "action": "UPDATE"}
                Audit.insertAudit(audit_user, "SettingOauthDet", "SETTING", id_item, "SUCCESS", details, "U")
            except Exception:
                self.log.exception(Logs.fileline() + ' : SettingOauthDet ERROR audit success update')
            return compose_ret(id_item, Constants.cst_content_type_json, 200)

        # STEP 4: insert new row
        new_id = Setting.insertSettingOauth(**params)

        action = "INSERT"

        if new_id <= 0:
            self.log.error(Logs.alert() + ' : SettingOauthDet ERROR insert')
            try:
                details = {"id_item": new_id, "client_id": params.get('oacl_client_id'), "result": "ERROR",
                           "reason": "INSERT_FAILED", "action": "INSERT"}
                Audit.insertAudit(audit_user, "SettingOauthDet", "SETTING", None, "ERROR", details, "C")
            except Exception:
                self.log.exception(Logs.fileline() + ' : SettingOauthDet ERROR audit insert')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : SettingOauthDet inserted id=' + str(new_id))
        try:
            details = {"id_item": new_id, "client_id": params.get('oacl_client_id'), "result": "SUCCESS",
                       "action": "INSERT"}
            event_type = "C" if action == "INSERT" else "U"
            Audit.insertAudit(audit_user, "SettingOauthDet", "SETTING", new_id, "SUCCESS", details, event_type)
        except Exception:
            self.log.exception(Logs.fileline() + ' : SettingOauthDet ERROR audit success insert')
        return compose_ret(new_id, Constants.cst_content_type_json, 200)

    @require_oauth()
    def delete(self, id_item):
        """Delete an OAuth client by id (forbidden for labbook-FE)."""
        audit_user = request.oauth_user
        cur = Setting.getSettingOauth(id_item)
        if not cur:
            try:
                details = {"id_item": id_item, "result": "ERROR", "reason": "NOT_FOUND", "action": "DELETE"}
                Audit.insertAudit(audit_user, "SettingOauthDet", "SETTING", id_item, "ERROR", details, "D")
            except Exception:
                self.log.exception(Logs.fileline() + ' : SettingOauthDet ERROR audit not found delete')
            return compose_ret('', Constants.cst_content_type_json, 404)

        if cur['oacl_client_id'] == 'labbook-FE':
            self.log.error(Logs.fileline() + ' : SettingOauthDet delete forbidden for labbook-FE')
            try:
                details = {"id_item": id_item, "client_id": cur.get('oacl_client_id'), "result": "ERROR",
                           "reason": "FORBIDDEN_FE_CLIENT", "action": "DELETE"}
                Audit.insertAudit(audit_user, "SettingOauthDet", "SETTING", id_item, "ERROR", details, "D")
            except Exception:
                self.log.exception(Logs.fileline() + ' : SettingOauthDet ERROR audit forbidden delete')
            return compose_ret({'error': 'forbidden'}, Constants.cst_content_type_json, 403)

        ok = Setting.deleteSettingOauth(id_item)
        if not ok:
            self.log.error(Logs.fileline() + ' : SettingOauthDet delete ERROR id=' + str(id_item))
            try:
                details = {"id_item": id_item, "client_id": cur.get('oacl_client_id'), "result": "ERROR",
                           "reason": "DELETE_FAILED", "action": "DELETE"}
                Audit.insertAudit(audit_user, "SettingOauthDet", "SETTING", id_item, "ERROR", details, "D")
            except Exception:
                self.log.exception(Logs.fileline() + ' : SettingOauthDet ERROR audit delete')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : SettingOauthDet delete id=' + str(id_item))
        try:
            details = {"id_item": id_item, "client_id": cur.get('oacl_client_id'), "result": "SUCCESS", "action": "DELETE"}
            Audit.insertAudit(audit_user, "SettingOauthDet", "SETTING", id_item, "SUCCESS", details, "D")
        except Exception:
            self.log.exception(Logs.fileline() + ' : SettingOauthDet ERROR audit success delete')
        return compose_ret('', Constants.cst_content_type_json, 200)
