# -*- coding:utf-8 -*-
import logging

from datetime import datetime
from flask import request
from flask_restful import Resource

from app.models.General import compose_ret
from app.models.Constants import *
from app.models.Logs import Logs
from app.models.Setting import *


class SettingAgeInterval(Resource):
    log = logging.getLogger('log_services')

    def get(self):
        l_datas = Setting.getAgeInterval()

        if not l_datas:
            self.log.error(Logs.fileline() + ' : ' + 'SettingAgeInterval ERROR not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        for data in l_datas:
            # Replace None by empty string
            for key, value in data.items():
                if data[key] is None:
                    data[key] = ''

        self.log.info(Logs.fileline() + ' : SettingAgeInterval')
        return compose_ret(l_datas, Constants.cst_content_type_json, 200)

    def post(self):
        args = request.get_json()

        if 'list_val' not in args:
            self.log.error(Logs.fileline() + ' : SettingAgeInterval ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        l_interval = Setting.getAgeInterval()

        if not l_interval:
            self.log.info(Logs.fileline() + ' : TRACE SettingAgeInterval ERROR notfound age interval')
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
            else:
                ret = Setting.insertAgeInterval(ais_rank=val['ais_rank'],
                                                ais_lower_bound=lower,
                                                ais_upper_bound=upper)

            if ret is False or ret <= 0:
                self.log.info(Logs.fileline() + ' : TRACE SettingAgeInterval ERROR update val age interval')
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
                    return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE SettingAgeInterval')
        return compose_ret('', Constants.cst_content_type_json)


class SettingPref(Resource):
    log = logging.getLogger('log_services')

    def get(self):
        l_prefs = Setting.getPrefList()

        if not l_prefs:
            self.log.error(Logs.fileline() + ' : ' + 'SettingPref ERROR not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        for pref in l_prefs:
            # Replace None by empty string
            for key, value in pref.items():
                if pref[key] is None:
                    pref[key] = ''

        self.log.info(Logs.fileline() + ' : SettingPref')
        return compose_ret(l_prefs, Constants.cst_content_type_json, 200)

    def post(self, id_owner):
        args = request.get_json()

        if id_owner < 1 or 'prix_acte' not in args or 'entete_1' not in args or 'entete_2' not in args or \
           'entete_3' not in args or 'entete_adr' not in args or 'entete_tel' not in args or 'entete_fax' not in args or \
           'entete_email' not in args or 'entete_ville' not in args or 'facturation_pat_hosp' not in args or \
           'unite_age_defaut' not in args or 'auto_logout' not in args or 'qualite' not in args or 'facturation' not in args:
            self.log.error(Logs.fileline() + ' : SettingPref ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        for key, value in args.items():
            ret = Setting.updatePref(id_owner, key, value)

            if ret is False:
                self.log.error(Logs.alert() + ' : SettingPref ERROR update')
                return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE SettingPref')
        return compose_ret('', Constants.cst_content_type_json)


class SettingRecNum(Resource):
    log = logging.getLogger('log_services')

    def get(self):
        setting = Setting.getRecNumSetting()

        if not setting:
            self.log.error(Logs.fileline() + ' : ERROR SettingRecNum not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        # Replace None by empty string
        for key, value in setting.items():
            if setting[key] is None:
                setting[key] = ''

        if setting['sys_creation_date']:
            setting['sys_creation_date'] = datetime.strftime(setting['sys_creation_date'], '%Y-%m-%d %H:%M:%S')

        if setting['sys_last_mod_date']:
            setting['sys_last_mod_date'] = datetime.strftime(setting['sys_last_mod_date'], '%Y-%m-%d %H:%M:%S')

        self.log.info(Logs.fileline() + ' : TRACE SettingRecNum')
        return compose_ret(setting, Constants.cst_content_type_json)

    def post(self):
        args = request.get_json()

        if 'id_owner' not in args or 'period' not in args or 'format' not in args:
            self.log.error(Logs.fileline() + ' : SettingRecNum ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        ret = Setting.updateRecNumSetting(id_owner=args['id_owner'],
                                          period=args['period'],
                                          format=args['format'])

        if ret is False:
            self.log.error(Logs.alert() + ' : SettingRecNum ERROR update')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE SettingRecNum')
        return compose_ret('', Constants.cst_content_type_json)


class SettingReport(Resource):
    log = logging.getLogger('log_services')

    def get(self):
        setting = Setting.getReportSetting()

        if not setting:
            self.log.error(Logs.fileline() + ' : ERROR SettingReport not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        # Replace None by empty string
        for key, value in setting.items():
            if setting[key] is None:
                setting[key] = ''

        if setting['sys_creation_date']:
            setting['sys_creation_date'] = datetime.strftime(setting['sys_creation_date'], '%Y-%m-%d %H:%M:%S')

        if setting['sys_last_mod_date']:
            setting['sys_last_mod_date'] = datetime.strftime(setting['sys_last_mod_date'], '%Y-%m-%d %H:%M:%S')

        self.log.info(Logs.fileline() + ' : TRACE SettingReport')
        return compose_ret(setting, Constants.cst_content_type_json)

    def post(self):
        args = request.get_json()

        if 'id_owner' not in args or 'header' not in args or 'comment' not in args:
            self.log.error(Logs.fileline() + ' : SettingReport ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        ret = Setting.updateReportSetting(id_owner=args['id_owner'],
                                          header=args['header'],
                                          comment=args['comment'])

        if ret is False:
            self.log.error(Logs.alert() + ' : SettingReport ERROR update')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE SettingReport')
        return compose_ret('', Constants.cst_content_type_json)


class SettingSticker(Resource):
    log = logging.getLogger('log_services')

    def get(self):
        setting = Setting.getStickerSetting()

        if not setting:
            self.log.error(Logs.fileline() + ' : ERROR SettingSticker not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        # Replace None by empty string
        for key, value in setting.items():
            if setting[key] is None:
                setting[key] = ''

        self.log.info(Logs.fileline() + ' : TRACE SettingSticker')
        return compose_ret(setting, Constants.cst_content_type_json)

    def post(self, sts_ser):
        args = request.get_json()

        if 'sts_width' not in args or 'sts_height' not in args or \
           'sts_margin_top' not in args or 'sts_margin_bottom' not in args or \
           'sts_margin_left' not in args or 'sts_margin_right' not in args:
            self.log.error(Logs.fileline() + ' : SettingSticker ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        ret = Setting.updateStickerSetting(sts_ser=sts_ser,
                                           sts_width=args['sts_width'],
                                           sts_height=args['sts_height'],
                                           sts_margin_top=args['sts_margin_top'],
                                           sts_margin_bottom=args['sts_margin_bottom'],
                                           sts_margin_left=args['sts_margin_left'],
                                           sts_margin_right=args['sts_margin_right'])

        if ret is False:
            self.log.error(Logs.alert() + ' : SettingSticker ERROR update')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE SettingSticker')
        return compose_ret('', Constants.cst_content_type_json)


class SettingBackup(Resource):
    log = logging.getLogger('log_services')

    def get(self):
        setting = Setting.getBackupSetting()

        if not setting:
            self.log.error(Logs.fileline() + ' : ERROR SettingBackup not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        # Replace None by empty string
        for key, value in setting.items():
            if setting[key] is None:
                setting[key] = ''

        if setting['bks_start_time']:
            setting['bks_start_time'] = str(setting['bks_start_time'])

        self.log.info(Logs.fileline() + ' : TRACE SettingBackup')
        return compose_ret(setting, Constants.cst_content_type_json)

    def post(self):
        args = request.get_json()

        if 'start_time' not in args:
            self.log.error(Logs.fileline() + ' : SettingBackup ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        ret = Setting.updateBackupSetting(bks_start_time=args['start_time'])

        if ret is False:
            self.log.error(Logs.alert() + ' : SettingBackup ERROR update')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE SettingBackup')
        return compose_ret('', Constants.cst_content_type_json)


class ScriptKeyexist(Resource):
    log = logging.getLogger('log_services')

    def get(self):
        # TODO run script
        import os
        nom = "toto"
        cmd = 'sh ' + Constants.cst_script + '/' + Constants.cst_io_keyexist + ' -p ' + str(666) + ' -n "' + nom + '" >> /tmp/file_TODO.log 2>&1 &'

        self.log.error(Logs.fileline() + ' : ScriptKeyexist cmd=' + cmd)
        ret = os.system(cmd)

        self.log.info(Logs.fileline() + ' : TRACE ScriptKeyexist')
        return compose_ret(ret, Constants.cst_content_type_json)


class ScriptBackup(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        if 'script_user' not in args or 'script_pwd' not in args:
            self.log.error(Logs.fileline() + ' : ScriptBackup ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # TODO run script
        import os
        cmd = 'sh PATH/NOM_DU_SCRIPT.sh -p ' + str(666) + ' -n "' + args['nom'] + '" >> /tmp/file_TODO.log 2>&1 &'

        self.log.error(Logs.fileline() + ' : ScriptBackup cmd=' + cmd)
        ret = os.system(cmd)

        self.log.info(Logs.fileline() + ' : TRACE ScriptBackup')
        return compose_ret('', Constants.cst_content_type_json)


class ScriptRestore(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        if 'script_user' not in args or 'script_pwd' not in args:
            self.log.error(Logs.fileline() + ' : ScriptRestore ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # TODO run script
        import os
        cmd = 'sh PATH/NOM_DU_SCRIPT.sh -p ' + str(666) + ' -n "' + args['nom'] + '" >> /tmp/file_TODO.log 2>&1 &'

        self.log.error(Logs.fileline() + ' : ScriptRestore cmd=' + cmd)
        ret = os.system(cmd)

        self.log.info(Logs.fileline() + ' : TRACE ScriptRestore')
        return compose_ret('', Constants.cst_content_type_json)
