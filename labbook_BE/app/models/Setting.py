# -*- coding:utf-8 -*-
import logging
import mysql.connector

from app.models.DB import DB
from app.models.Logs import Logs


class Setting:
    log = logging.getLogger('log_db')

    @staticmethod
    def getPrefList():
        cursor = DB.cursor()

        req = ('select id_data, id_owner, identifiant, label, value '
               'from sigl_06_data '
               'order by id_data')

        cursor.execute(req,)

        return cursor.fetchall()

    @staticmethod
    def updatePref(id_owner, key, value):
        try:
            cursor = DB.cursor()

            cursor.execute('update sigl_06_data '
                           'set id_owner=%s, value=%s '
                           'where identifiant=%s', (id_owner, value, key))

            Setting.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Setting.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getRecNumSetting():
        cursor = DB.cursor()

        req = ('select id_data, id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, periode, format '
               'from sigl_param_num_dos_data '
               'order by id_data desc limit 1')

        cursor.execute(req)

        return cursor.fetchone()

    @staticmethod
    def updateRecNumSetting(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('update sigl_param_num_dos_data '
                           'set sys_last_mod_user=%(id_owner)s, sys_last_mod_date=NOW(), '
                           'periode=%(period)s, format=%(format)s '
                           'where id_data=1', params)

            Setting.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Setting.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getReportSetting():
        cursor = DB.cursor()

        req = ('select id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, entete, commentaire '
               'from sigl_param_cr_data '
               'order by id_data desc limit 1')

        cursor.execute(req)

        return cursor.fetchone()

    @staticmethod
    def updateReportSetting(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('update sigl_param_cr_data '
                           'set sys_last_mod_user=%(id_owner)s, sys_last_mod_date=NOW(), '
                           'entete=%(header)s, commentaire=%(comment)s '
                           'where id_data=1', params)

            Setting.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Setting.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getStickerSetting():
        cursor = DB.cursor()

        req = ('select sts_ser, sts_width, sts_height, sts_margin_top, sts_margin_bottom, '
               'sts_margin_left, sts_margin_right '
               'from sticker_setting '
               'order by sts_ser desc limit 1')

        cursor.execute(req)

        return cursor.fetchone()

    @staticmethod
    def updateStickerSetting(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('update sticker_setting '
                           'set sts_width=%(sts_width)s, sts_height=%(sts_height)s, '
                           'sts_margin_top=%(sts_margin_top)s, sts_margin_bottom=%(sts_margin_bottom)s, '
                           'sts_margin_left=%(sts_margin_left)s, sts_margin_right=%(sts_margin_right)s '
                           'where sts_ser=%(sts_ser)s', params)

            Setting.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Setting.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getAgeInterval():
        cursor = DB.cursor()

        req = ('select ais_ser, ais_rank, ais_lower_bound, ais_upper_bound '
               'from age_interval_setting '
               'order by ais_rank asc')

        cursor.execute(req,)

        return cursor.fetchall()

    @staticmethod
    def insertAgeInterval(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into age_interval_setting '
                           '(ais_rank, ais_lower_bound, ais_upper_bound) '
                           'values (%(ais_rank)s, %(ais_lower_bound)s, %(ais_upper_bound)s)', params)

            Setting.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Setting.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def updateAgeInterval(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('update age_interval_setting '
                           'set ais_rank=%(ais_rank)s, ais_lower_bound= %(ais_lower_bound)s, '
                           'ais_upper_bound=%(ais_upper_bound)s '
                           'where ais_ser=%(ais_ser)s', params)

            Setting.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Setting.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def deleteAgeInterval(ais_ser):
        try:
            cursor = DB.cursor()

            cursor.execute('delete from age_interval_setting '
                           'where ais_ser=%s', (ais_ser,))

            Setting.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Setting.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getReqServices():
        cursor = DB.cursor()

        req = ('select rqs_ser, rqs_rank, rqs_name '
               'from requesting_services '
               'order by rqs_rank asc')

        cursor.execute(req,)

        return cursor.fetchall()

    @staticmethod
    def insertReqServices(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into requesting_services '
                           '(rqs_date, rqs_rank, rqs_name) '
                           'values (NOW(), %(rqs_rank)s, %(rqs_name)s)', params)

            Setting.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Setting.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def updateReqServices(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('update requesting_services '
                           'set rqs_rank=%(rqs_rank)s, rqs_name= %(rqs_name)s '
                           'where rqs_ser=%(rqs_ser)s', params)

            Setting.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Setting.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def deleteReqServices(rqs_ser):
        try:
            cursor = DB.cursor()

            cursor.execute('delete from requesting_services '
                           'where rqs_ser=%s', (rqs_ser,))

            Setting.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Setting.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getFuncUnitDet(id_unit):
        cursor = DB.cursor()

        req = ('select fun_ser, fun_rank, fun_name '
               'from functionnal_unit '
               'where fun_ser=%s')

        cursor.execute(req, (id_unit,))

        return cursor.fetchone()

    @staticmethod
    def getFuncUnit():
        cursor = DB.cursor()

        req = ('select fun_ser, fun_rank, fun_name, count(t_user.ful_ser) as nb_user, count(t_fam.ful_ser) as nb_fam '
               'from functionnal_unit '
               'left join functionnal_unit_link as t_user on t_user.ful_fun=fun_ser and t_user.ful_type="U" '
               'left join functionnal_unit_link as t_fam on t_fam.ful_fun=fun_ser and t_fam.ful_type="F" '
               'order by fun_rank asc')

        cursor.execute(req,)

        return cursor.fetchall()

    @staticmethod
    def insertFuncUnit(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into functionnal_unit '
                           '(fun_date, fun_rank, fun_name) '
                           'values (NOW(), %(fun_rank)s, %(fun_name)s)', params)

            Setting.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Setting.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def updateFuncUnit(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('update functionnal_unit '
                           'set fun_rank=%(fun_rank)s, fun_name= %(fun_name)s '
                           'where fun_ser=%(fun_ser)s', params)

            Setting.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Setting.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def deleteFuncUnit(fun_ser):
        try:
            cursor = DB.cursor()

            # delete link too
            cursor.execute('delete from functionnal_unit_link '
                           'where ful_fun=%s', (fun_ser,))

            cursor.execute('delete from functionnal_unit '
                           'where fun_ser=%s', (fun_ser,))

            Setting.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Setting.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getLinkUnit(type, id_unit):
        cursor = DB.cursor()

        req = ''

        if type == 'U':
            req = ('select id_data as id_user, firstname, lastname, username, role_type, d_role.label as role, '
                   'ifnull(ful_fun, 0) as ful_fun '
                   'from sigl_user_data '
                   'inner join sigl_pj_role as d_role on d_role.type=role_type '
                   'left join functionnal_unit_link on ful_ref=id_data and ful_type="U" and ful_fun=%s '
                   'where role_type != "A" '
                   'order by ful_fun desc, lastname asc, firstname asc')
        elif type == 'F':
            req = ('select id_data as id_fam, label, ifnull(ful_fun, 0) as ful_fun '
                   'from sigl_dico_data '
                   'left join functionnal_unit_link on ful_ref=id_data and ful_type="F" and ful_fun=%s '
                   'where dico_name="famille_analyse" '
                   'order by ful_fun desc, position asc')

        cursor.execute(req, (id_unit,))

        return cursor.fetchall()

    @staticmethod
    def getListLinkUnit(type, id_unit):
        cursor = DB.cursor()

        ret = []

        req = ('select ful_ref '
               'from functionnal_unit_link '
               'where ful_type=%s and ful_fun=%s '
               'order by ful_ref asc')

        cursor.execute(req, (type, id_unit))

        l_items = cursor.fetchall()

        for item in l_items:
            ret.append(item['ful_ref'])

        return ret

    @staticmethod
    def insertLinkUnit(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into functionnal_unit_link '
                           '(ful_date, ful_fun, ful_ref, ful_type) '
                           'values (NOW(), %(ful_fun)s, %(ful_ref)s, %(ful_type)s)', params)

            Setting.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Setting.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def deleteLinkUnit(type, id_unit, ref):
        try:
            cursor = DB.cursor()

            cursor.execute('delete from functionnal_unit_link '
                           'where ful_type=%s and ful_fun=%s and ful_ref=%s', (type, id_unit, ref))

            Setting.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Setting.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getBackupSetting():
        cursor = DB.cursor()

        req = ('select bks_ser, bks_start_time '
               'from backup_setting '
               'order by bks_ser desc limit 1')

        cursor.execute(req)

        return cursor.fetchone()

    @staticmethod
    def updateBackupSetting(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('update backup_setting '
                           'set bks_start_time=%(bks_start_time)s '
                           'where bks_ser=1', params)

            Setting.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Setting.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getTemplateList(type=''):
        cursor = DB.cursor()

        cond = ''

        if type:
            cond = 'where tpl_type="' + type + '" '

        req = ('select tpl_ser as id_item, tpl_name, tpl_type, tpl_default, tpl_file '
               'from template_setting ' + cond +
               'order by tpl_name, tpl_type asc ')

        cursor.execute(req)

        return cursor.fetchall()

    @staticmethod
    def getTemplate(id_item):
        cursor = DB.cursor()

        req = ('select tpl_ser, tpl_name, tpl_type, tpl_default, tpl_file '
               'from template_setting '
               'where tpl_ser=%s')

        cursor.execute(req, (id_item,))

        return cursor.fetchone()

    @staticmethod
    def getTemplateByFile(tpl_file):
        cursor = DB.cursor()

        req = ('select tpl_ser, tpl_name, tpl_type, tpl_default, tpl_file '
               'from template_setting '
               'where tpl_file=%s limit 1')

        cursor.execute(req, (tpl_file,))

        return cursor.fetchone()

    @staticmethod
    def getDefaultTemplate(type):
        cursor = DB.cursor()

        req = ('select tpl_ser, tpl_name, tpl_type, tpl_default, tpl_file '
               'from template_setting '
               'where tpl_type=%s')

        cursor.execute(req, (type,))

        return cursor.fetchone()

    @staticmethod
    def insertTemplate(**params):
        try:
            cursor = DB.cursor()

            if params['tpl_default'] == 'Y':
                # removes the default character on others of the same type
                Setting.UndefaultTemplate(tpl_type=params['tpl_type'])

            cursor.execute('insert into template_setting '
                           '(tpl_date, tpl_name, tpl_type, tpl_default, tpl_file) '
                           'values '
                           '(NOW(), %(tpl_name)s, %(tpl_type)s, %(tpl_default)s, %(tpl_file)s)', params)

            Setting.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Setting.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def updateTemplate(**params):
        try:
            cursor = DB.cursor()

            if params['tpl_default'] == 'Y':
                # removes the default character on others of the same type
                Setting.UndefaultTemplate(tpl_type=params['tpl_type'])

            cursor.execute('update template_setting '
                           'set tpl_name=%(tpl_name)s , tpl_type=%(tpl_type)s, '
                           'tpl_default=%(tpl_default)s, tpl_file=%(tpl_file)s '
                           'where tpl_ser=%(tpl_ser)s', params)

            Setting.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Setting.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def deleteTemplate(id_item):
        try:
            cursor = DB.cursor()

            cursor.execute('delete from template_setting '
                           'where tpl_ser=%s', (id_item,))

            Setting.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Setting.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def UndefaultTemplate(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('update template_setting '
                           'set tpl_default="N" '
                           'where tpl_default="Y" and tpl_type=%(tpl_type)s', params)

            Setting.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Setting.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def insertZipCity(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into zip_city (zic_date, zic_zip, zic_city) '
                           'values (NOW(), %(zic_zip)s, %(zic_city)s)', params)

            Setting.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Setting.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def deleteAllZipCity():
        try:
            cursor = DB.cursor()

            cursor.execute('truncate table zip_city')

            Setting.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Setting.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getZipCity(id_item):
        cursor = DB.cursor()

        req = ('select zic_ser, zic_zip, zic_city '
               'from zip_city '
               'where zic_ser=%s')

        cursor.execute(req, (id_item,))

        return cursor.fetchone()

    @staticmethod
    def getZipCityList(args):
        cursor = DB.cursor()

        filter_cond = ' zic_ser > 0 '

        if not args:
            limit = 'LIMIT 50000'
        else:
            if 'limit' in args and args['limit'] > 0:
                limit = 'LIMIT ' + str(args['limit'])
            else:
                limit = 'LIMIT 500'

        req = ('select zic_ser as id_item, zic_zip, zic_city '
               'from zip_city '
               'where ' + filter_cond + ' ' +
               'order by zic_zip asc, zic_city asc ' + limit)

        cursor.execute(req)

        return cursor.fetchall()

    @staticmethod
    def getZipCitySearch(text):
        cursor = DB.cursor()

        l_words = text.split(' ')

        cond = 'zic_ser > 0'

        for word in l_words:
            cond = (cond +
                    ' and (zic_zip like "' + word + '%" or '
                    'zic_city like "%' + word + '%") ')

        req = ('SELECT TRIM(CONCAT(TRIM(COALESCE(zic_zip, ""))," - ",'
               'TRIM(COALESCE(zic_city, "")) )) AS field_value,'
               'zic_ser AS id_item '
               'from zip_city '
               'where ' + cond + ' order by zic_zip asc limit 1000')

        cursor.execute(req)

        return cursor.fetchall()

    @staticmethod
    def getStockSetting():
        cursor = DB.cursor()

        req = ('select sos_ser, sos_expir_oblig, sos_expir_warning, sos_expir_alert '
               'from stock_setting '
               'order by sos_ser desc limit 1')

        cursor.execute(req)

        return cursor.fetchone()

    @staticmethod
    def updateStockSetting(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('update stock_setting '
                           'set sos_date=NOW(), sos_expir_oblig=%(expir_oblig)s, sos_expir_warning=%(expir_warning)s, '
                           'sos_expir_alert=%(expir_alert)s', params)

            Setting.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Setting.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False
