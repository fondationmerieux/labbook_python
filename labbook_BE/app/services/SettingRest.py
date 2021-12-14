# -*- coding:utf-8 -*-
import logging
import os

from gettext import gettext as _
from datetime import datetime
from flask import request, session
from flask_restful import Resource

from app.models.General import compose_ret
from app.models.Constants import Constants
from app.models.Logs import Logs
from app.models.Setting import Setting


class SettingAgeInterval(Resource):
    log = logging.getLogger('log_services')

    def get(self):
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
            for key, value in list(pref.items()):
                if pref[key] is None:
                    pref[key] = ''

        self.log.info(Logs.fileline() + ' : SettingPref')
        return compose_ret(l_prefs, Constants.cst_content_type_json, 200)

    def post(self, id_owner):
        args = request.get_json()

        if id_owner < 1 or 'prix_acte' not in args or 'entete_1' not in args or 'entete_2' not in args or \
           'entete_3' not in args or 'entete_adr' not in args or 'entete_tel' not in args or 'entete_fax' not in args or \
           'entete_email' not in args or 'entete_ville' not in args or 'facturation_pat_hosp' not in args or \
           'unite_age_defaut' not in args or 'auto_logout' not in args or 'qualite' not in args or \
           'facturation' not in args or 'default_language' not in args or 'db_language' not in args:
            self.log.error(Logs.fileline() + ' : SettingPref ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        for key, value in list(args.items()):
            if key == 'db_language':
                session['lang_db'] = value
                session.modified = True

            if key == 'default_language':
                session['lang_pdf'] = value
                session.modified = True

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
        for key, value in list(setting.items()):
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
        for key, value in list(setting.items()):
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
        for key, value in list(setting.items()):
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
            return compose_ret('1', Constants.cst_content_type_json, 404)

        # Replace None by empty string
        for key, value in list(setting.items()):
            if setting[key] is None:
                setting[key] = ''

        if setting['bks_start_time']:
            setting['bks_start_time'] = str(setting['bks_start_time'])

        self.log.info(Logs.fileline() + ' : TRACE SettingBackup')
        return compose_ret(setting, Constants.cst_content_type_json)


class ScriptBackup(Resource):
    log = logging.getLogger('log_services')

    def post(self, media):
        cmd = ('sh ' + Constants.cst_path_script + '/' + Constants.cst_script_backup + ' -m "' + media +
               '" ' + Constants.cst_io_backup + ' > ' + Constants.cst_io + 'backup.out 2>&1 &')

        self.log.error(Logs.fileline() + ' : ScriptBackup cmd=' + cmd)
        ret = os.system(cmd)

        self.log.info(Logs.fileline() + ' : TRACE ScriptBackup ret=' + str(ret))
        return compose_ret(ret, Constants.cst_content_type_json)


class ScriptGenkey(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        if 'pwd_key' not in args:
            self.log.error(Logs.fileline() + ' : ScriptGenkey ERROR args missing')
            return compose_ret('1', Constants.cst_content_type_json, 400)

        os.environ['LABBOOK_KEY_PWD'] = args['pwd_key']

        cmd = 'sh ' + Constants.cst_path_script + '/' + Constants.cst_script_backup + Constants.cst_io_genkey

        self.log.error(Logs.fileline() + ' : ScriptGenkey cmd=' + cmd)
        ret = os.system(cmd)

        self.log.info(Logs.fileline() + ' : TRACE ScriptGenkey ret=' + str(ret))
        return compose_ret(ret, Constants.cst_content_type_json)


class ScriptInitmedia(Resource):
    log = logging.getLogger('log_services')

    def post(self, media):
        cmd = ('sh ' + Constants.cst_path_script + '/' + Constants.cst_script_backup + ' -m "' + media +
               '" ' + Constants.cst_io_initmedia)

        self.log.error(Logs.fileline() + ' : ScriptInitMedia cmd=' + cmd)
        ret = os.system(cmd)

        self.log.info(Logs.fileline() + ' : TRACE ScriptInitMedia ret=' + str(ret))
        return compose_ret(ret, Constants.cst_content_type_json)


class ScriptKeyexist(Resource):
    log = logging.getLogger('log_services')

    def get(self):
        cmd = 'sh ' + Constants.cst_path_script + '/' + Constants.cst_script_backup + Constants.cst_io_keyexist

        self.log.error(Logs.fileline() + ' : ScriptKeyexist cmd=' + cmd)
        ret = os.system(cmd)

        self.log.info(Logs.fileline() + ' : TRACE ScriptKeyexist ret=' + str(ret))
        return compose_ret(ret, Constants.cst_content_type_json)


class ScriptListarchive(Resource):
    log = logging.getLogger('log_services')

    def post(self, media):
        args = request.get_json()

        if 'user_pwd' not in args:
            self.log.error(Logs.fileline() + ' : ScriptListmedia ERROR args missing')
            return compose_ret('1', Constants.cst_content_type_json, 400)

        os.environ['LABBOOK_USER_PWD'] = args['user_pwd']

        cmd = 'sh ' + Constants.cst_path_script + '/' + Constants.cst_script_backup + ' -m "' + media + '" ' + Constants.cst_io_listarchive

        self.log.error(Logs.fileline() + ' : ScriptListarchive cmd=' + cmd)
        ret = os.system(cmd)

        l_archive = {}

        l_archive['ret']   = ret
        l_archive['archive'] = []

        # read listarchive file
        if ret == 0:
            try:
                # No encoding forced because script return list from system so its depend of encoding of operating system
                f = open(os.path.join(Constants.cst_io, 'listarchive'), 'r')
                for archive in f:
                    l_archive['archive'].append(archive[:-1])
            except:
                self.log.info(Logs.fileline() + ' : ERROR ScriptListarchive impossible to open listarchive file')
                return compose_ret(l_archive, Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE ScriptListarchive l_archive=' + str(l_archive))
        return compose_ret(l_archive, Constants.cst_content_type_json)


class ScriptListmedia(Resource):
    log = logging.getLogger('log_services')

    def post(self, type):
        if type == "U":
            type = ' -U '
        else:
            type = ' '

        args = request.get_json()

        if 'user_pwd' not in args:
            self.log.error(Logs.fileline() + ' : ScriptListmedia ERROR args missing')
            return compose_ret('1', Constants.cst_content_type_json, 400)

        os.environ['LABBOOK_USER_PWD'] = args['user_pwd']

        cmd = 'sh ' + Constants.cst_path_script + '/' + Constants.cst_script_backup + type + Constants.cst_io_listmedia

        self.log.error(Logs.fileline() + ' : ScriptListmedia cmd=' + cmd)
        ret = os.system(cmd)

        l_media = {}

        l_media['ret']   = ret
        l_media['media'] = []

        # read listmedia file
        if ret == 0:
            try:
                # No encoding forced because script return list from system so its depend of encoding of operating system
                f = open(os.path.join(Constants.cst_io, 'listmedia'), 'r')
                for media in f:
                    l_media['media'].append(media[:-1])
            except:
                self.log.info(Logs.fileline() + ' : ERROR ScriptListmedia impossible to open listmedia file')
                return compose_ret(l_media, Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE ScriptListmedia l_media=' + str(l_media))
        return compose_ret(l_media, Constants.cst_content_type_json)


class ScriptProgbackup(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        if 'start_time' not in args or 'user_pwd' not in args:
            self.log.error(Logs.fileline() + ' : ScriptProgbackup ERROR args missing')
            return compose_ret('1', Constants.cst_content_type_json, 400)

        start_time = str(args['start_time'])

        os.environ['LABBOOK_USER_PWD'] = args['user_pwd']

        cmd = 'sh ' + Constants.cst_path_script + '/' + Constants.cst_script_backup + ' -w "' + start_time + '" ' + Constants.cst_io_progbackup

        self.log.error(Logs.fileline() + ' : ScriptProgbackup cmd=' + cmd)
        ret = os.system(cmd)

        if ret == 0:
            start_time = start_time + ':00'  # add seconds default value
            ret_db = Setting.updateBackupSetting(bks_start_time=start_time)

            if ret_db is False:
                self.log.error(Logs.alert() + ' : ScriptProgbackup ERROR update')
                return compose_ret('1', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE ScriptProgbackup ret=' + str(ret))
        return compose_ret(ret, Constants.cst_content_type_json)


class ScriptRestart(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        if 'pwd_user' not in args:
            self.log.error(Logs.fileline() + ' : ScriptRestart ERROR args missing')
            return compose_ret('1', Constants.cst_content_type_json, 400)

        os.environ['LABBOOK_USER_PWD'] = args['pwd_user']

        cmd = 'sh ' + Constants.cst_path_script + '/' + Constants.cst_script_backup + Constants.cst_io_restart

        self.log.error(Logs.fileline() + ' : ScriptRestart cmd=' + cmd)
        ret = os.system(cmd)

        self.log.info(Logs.fileline() + ' : TRACE ScriptRestart ret=' + str(ret))
        return compose_ret(ret, Constants.cst_content_type_json)


class ScriptRestore(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        if 'media' not in args or 'pwd_key' not in args or 'archive' not in args:
            self.log.error(Logs.fileline() + ' : ScriptRestore ERROR args missing')
            return compose_ret('1', Constants.cst_content_type_json, 400)

        media   = str(args['media'])
        archive = str(args['archive'])

        os.environ['LABBOOK_KEY_PWD'] = args['pwd_key']

        cmd = ('sh ' + Constants.cst_path_script + '/' + Constants.cst_script_backup + ' -m "' + media +
               '" -a "' + archive + '" ' + Constants.cst_io_restore + ' > ' + Constants.cst_io + 'restore.out 2>&1 &')

        self.log.error(Logs.fileline() + ' : ScriptRestore cmd=' + cmd)
        ret = os.system(cmd)

        self.log.info(Logs.fileline() + ' : TRACE ScriptRestore ret=' + str(ret))
        return compose_ret(ret, Constants.cst_content_type_json)


class ScriptStatus(Resource):
    log = logging.getLogger('log_services')

    def get(self, mode):
        try:
            if mode == 'R':
                path = os.path.join(Constants.cst_io, Constants.cst_io_restore)
            elif mode == 'B':
                path = os.path.join(Constants.cst_io, Constants.cst_io_backup)
            else:
                date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.log.info(Logs.fileline() + ' : ERROR ScriptStatus wrong mode : ' + str(mode))
                ret = "ERR;" + str(date_now) + ";Wrong mode"
                return compose_ret(ret, Constants.cst_content_type_json, 500)

            # No encoding forced because script return list from system so its depend of encoding of operating system
            f = open(path, 'r')
            for line in f:
                pass

            ret = line[:-1]
        except:
            date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.log.info(Logs.fileline() + ' : ERROR ScriptStatus impossible to open status file')
            ret = "ERR;" + str(date_now) + ";Impossible to read status file"
            return compose_ret(ret, Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE ScriptStatus ret=' + str(ret))
        return compose_ret(ret, Constants.cst_content_type_json)


class TemplateList(Resource):
    log = logging.getLogger('log_services')

    def get(self, type=''):
        l_items = Setting.getTemplateList(type)

        if not l_items:
            self.log.error(Logs.fileline() + ' : TRACE TemplateList not found')

        for item in l_items:
            # Replace None by empty string
            for key, value in list(item.items()):
                if item[key] is None:
                    item[key] = ''

        self.log.info(Logs.fileline() + ' : TRACE TemplateList')
        return compose_ret(l_items, Constants.cst_content_type_json)


class TemplateDet(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_item):
        item = Setting.getTemplate(id_item)

        if not item:
            self.log.error(Logs.fileline() + ' : ' + 'TemplateDet ERROR not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        # Replace None by empty string
        for key, value in list(item.items()):
            if item[key] is None:
                item[key] = ''

        self.log.info(Logs.fileline() + ' : TemplateDet id_item=' + str(id_item))
        return compose_ret(item, Constants.cst_content_type_json, 200)

    def post(self, id_item):
        args = request.get_json()

        if 'id_item' not in args or 'tpl_name' not in args or 'tpl_type' not in args or \
           'tpl_default' not in args or 'tpl_file' not in args:
            self.log.error(Logs.fileline() + ' : TemplateDet ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # Update item
        if id_item > 0:
            ret = Setting.updateTemplate(tpl_ser=id_item,
                                         tpl_name=args['tpl_name'],
                                         tpl_type=args['tpl_type'],
                                         tpl_default=args['tpl_default'],
                                         tpl_file=args['tpl_file'])

            if ret is False:
                self.log.error(Logs.alert() + ' : TemplateDet ERROR update')
                return compose_ret('', Constants.cst_content_type_json, 500)

        # Insert new item
        else:
            ret = Setting.insertTemplate(tpl_name=args['tpl_name'],
                                         tpl_type=args['tpl_type'],
                                         tpl_default=args['tpl_default'],
                                         tpl_file=args['tpl_file'])

            if ret <= 0:
                self.log.error(Logs.alert() + ' : TemplateDet ERROR  insert')
                return compose_ret('', Constants.cst_content_type_json, 500)

            id_item = ret

        self.log.info(Logs.fileline() + ' : TRACE TemplateDet id_item=' + str(id_item))
        return compose_ret(id_item, Constants.cst_content_type_json)

    def delete(self, id_item):
        ret = Setting.deleteTemplate(id_item)

        if not ret:
            self.log.error(Logs.fileline() + ' : TRACE TemplateDet delete ERROR')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE TemplateDet delete id_item=' + str(id_item))
        return compose_ret('', Constants.cst_content_type_json)
