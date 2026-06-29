# -*- coding:utf-8 -*-
import logging
import mysql.connector
import smtplib
import socket
import ssl
import json
import requests
import binascii
import os
import time
import pikepdf
import base64

from email.message import EmailMessage
from mailjet_rest import Client

from app.models.DB import DB
from app.models.Logs import Logs
from app.models.Constants import Constants
from app.models.Patient import Patient


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

        req = ('select rstg_ser, rstg_user, rstg_date, rstg_date_upd, rstg_user_upd, rstg_period, rstg_format, '
               'rstg_samp_mask, rstg_samp_regex '
               'from record_setting '
               'order by rstg_ser desc limit 1')

        cursor.execute(req)

        return cursor.fetchone()

    @staticmethod
    def updateRecNumSetting(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('update record_setting '
                           'set rstg_user_upd=%(id_owner)s, rstg_date_upd=NOW(), rstg_period=%(period)s, '
                           'rstg_format=%(format)s, rstg_samp_mask=%(samp_mask)s, rstg_samp_regex=%(samp_regex)s '
                           'where rstg_ser=1', params)

            Setting.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Setting.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getReportSetting():
        cursor = DB.cursor()

        req = ('select id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, entete, commentaire, report_pwd '
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
                           'entete=%(header)s, commentaire=%(comment)s, report_pwd=%(report_pwd)s '
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

        req = ('select fun_ser, fun_rank, fun_name '
               'from functionnal_unit '
               'order by fun_rank asc')

        cursor.execute(req,)

        return cursor.fetchall()

    @staticmethod
    def getNbFuncUnitLink(fun_ser, ful_type):
        cursor = DB.cursor()

        req = ('select count(*) as nb_link '
               'from functionnal_unit '
               'inner join functionnal_unit_link on ful_fun=fun_ser and ful_type=%s '
               'where fun_ser=%s')

        cursor.execute(req, (ful_type, fun_ser,))

        return cursor.fetchone()

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
            cursor.execute('delete from functionnal_unit_link where ful_fun=%s', (fun_ser,))

            cursor.execute('delete from functionnal_unit where fun_ser=%s', (fun_ser,))

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
                   'where role_type not in("A","Z","API") '
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
    def getLinkByUser(id_user):
        # get list of ful_fun matching with id_user
        cursor = DB.cursor()

        req = ('select ful_fun '
               'from functionnal_unit_link '
               'where ful_type="U" and ful_ref=%s '
               'group by ful_fun')

        cursor.execute(req, (id_user,))

        ret = cursor.fetchall()

        if ret:
            l_ful_fun = ''

            for item in ret:
                if not l_ful_fun:
                    l_ful_fun = '('

                l_ful_fun = l_ful_fun + str(item['ful_fun']) + ','

            if l_ful_fun:
                l_ful_fun = l_ful_fun[:-1] + ')'

            # get list of id_fam matching with ful_fun in list of ful_fun
            req = ('select ful_ref as id_fam '
                   'from functionnal_unit_link '
                   'where ful_type="F" and ful_fun in ' + str(l_ful_fun) + ' '
                   'group by ful_ref')

            cursor.execute(req)

            return cursor.fetchall()
        else:
            return []

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
               'where tpl_default="Y" and tpl_type=%s')

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
        """Multi-word search against zip and city using a single query."""
        cursor = DB.cursor()
        words = (text or "").strip().split()
        # Base condition
        cond = ["zic_ser > 0"]
        params = []

        # Add (zip LIKE ? OR city LIKE ?) for each word with AND between words
        for w in words:
            cond.append("(zic_zip LIKE %s OR zic_city LIKE %s)")
            params.extend([w + "%", "%" + w + "%"])

        where_clause = " AND ".join(cond)

        req = (
            "SELECT TRIM(CONCAT(TRIM(COALESCE(zic_zip,'')),' - ',TRIM(COALESCE(zic_city,'')))) AS field_value, "
            "       zic_ser AS id_item "
            "FROM zip_city "
            f"WHERE {where_clause} "
            "ORDER BY zic_zip ASC "
            "LIMIT 1000"
        )

        cursor.execute(req, tuple(params))
        return cursor.fetchall()

    @staticmethod
    def getStockSetting():
        cursor = DB.cursor()

        req = ('select sos_ser, sos_expir_warning, sos_expir_alert '
               'from stock_setting '
               'order by sos_ser desc limit 1')

        cursor.execute(req)

        return cursor.fetchone()

    @staticmethod
    def updateStockSetting(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('update stock_setting '
                           'set sos_date=NOW(), sos_expir_warning=%(expir_warning)s, '
                           'sos_expir_alert=%(expir_alert)s', params)

            Setting.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Setting.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def insertStockLocal(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into product_local '
                           '(prl_date, prl_rank, prl_name) '
                           'values (NOW(), %(prl_rank)s, %(prl_name)s)', params)

            Setting.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Setting.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def updateStockLocal(**params):
        try:
            cursor = DB.cursor()

            req = ('update product_local set prl_rank=%(prl_rank)s, prl_name=%(prl_name)s '
                   'where prl_ser=%(prl_ser)s')

            cursor.execute(req, params)

            Setting.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Setting.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def deleteStockLocal(prl_ser):
        try:
            cursor = DB.cursor()

            cursor.execute('delete from product_local '
                           'where prl_ser=%s', (prl_ser,))

            cursor.execute('update product_supply set prs_prl=0 '
                           'where prs_prl=%s', (prl_ser,))

            Setting.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Setting.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getSettingFormList():
        cursor = DB.cursor()

        req = ('select fos_ser, fos_name, fos_type, fos_ref, fos_stat '
               'from form_setting '
               'where fos_type != "PAT" '  # 10/04/2024 : Added to avoid old form setting for patient
               'order by fos_rank asc, fos_type asc, fos_name asc ')

        cursor.execute(req)

        return cursor.fetchall()

    @staticmethod
    def updateFormSetting(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('update form_setting '
                           'set fos_date=NOW(), fos_stat=%(stat)s '
                           'where fos_ref=%(ref)s', params)

            Setting.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Setting.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getManualSetting():
        cursor = DB.cursor()

        req = ('select mas_ser, mas_rank, mas_name '
               'from manual_setting '
               'order by mas_rank asc')

        cursor.execute(req,)

        return cursor.fetchall()

    @staticmethod
    def insertManualSetting(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into manual_setting '
                           '(mas_date, mas_rank, mas_name) '
                           'values (NOW(), %(mas_rank)s, %(mas_name)s)', params)

            Setting.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Setting.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def updateManualSetting(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('update manual_setting '
                           'set mas_rank=%(mas_rank)s, mas_name= %(mas_name)s '
                           'where mas_ser=%(mas_ser)s', params)

            Setting.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Setting.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def deleteManualSetting(mas_ser):
        try:
            cursor = DB.cursor()

            cursor.execute('delete from manual_setting '
                           'where mas_ser=%s', (mas_ser,))

            Setting.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Setting.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getManualCategory():
        cursor = DB.cursor()

        req = ('select mas_ser, mas_name, mas_rank '
               'from manual_setting '
               'order by mas_rank asc, mas_name asc ')

        cursor.execute(req)

        return cursor.fetchall()

    @staticmethod
    def getDHIS2List():
        cursor = DB.cursor()

        req = ('select dhs_ser, dhs_user, dhs_name, dhs_login, dhs_url, dhs_default '
               'from dhis2_setting '
               'order by dhs_name asc')

        cursor.execute(req,)

        return cursor.fetchall()

    @staticmethod
    def getDHIS2Det(id_item):
        cursor = DB.cursor()

        req = ('select dhs_ser, dhs_user, dhs_name, dhs_login, dhs_pwd, dhs_url, dhs_default '
               'from dhis2_setting '
               'where dhs_ser=%s')

        cursor.execute(req, (id_item,))

        return cursor.fetchone()

    @staticmethod
    def getDefaultDHIS2Det():
        cursor = DB.cursor()

        req = ('select dhs_ser, dhs_user, dhs_name, dhs_login, dhs_pwd, dhs_url, dhs_default '
               'from dhis2_setting '
               'where dhs_default="Y"')

        cursor.execute(req)

        return cursor.fetchone()

    @staticmethod
    def insertDHIS2Det(**params):
        try:
            cursor = DB.cursor()

            if params['default'] == 'Y':
                # removes the default character on others
                Setting.UndefaultDHIS2Det()

            cursor.execute('insert into dhis2_setting '
                           '(dhs_date, dhs_user, dhs_name, dhs_login, dhs_pwd, dhs_url, dhs_default) '
                           'values (NOW(), %(user)s, %(name)s, %(login)s, %(pwd)s, %(url)s, %(default)s)', params)

            Setting.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Setting.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def updateDHIS2Det(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('update dhis2_setting '
                           'set dhs_user=%(user)s, dhs_name=%(name)s, dhs_login=%(login)s, dhs_pwd=%(pwd)s, '
                           'dhs_url=%(url)s, dhs_default=%(default)s '
                           'where dhs_ser=%(id_item)s', params)

            Setting.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Setting.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def deleteDHIS2Det(id_item):
        try:
            cursor = DB.cursor()

            cursor.execute('delete from dhis2_setting '
                           'where dhs_ser=%s', (id_item,))

            Setting.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Setting.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def UndefaultDHIS2Det():
        try:
            cursor = DB.cursor()

            cursor.execute('update dhis2_setting '
                           'set dhs_default="N" '
                           'where dhs_default="Y"')

            Setting.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Setting.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getSendingMethodList():
        cursor = DB.cursor()

        req = ('SELECT sdi_ser, sdi_type, sdi_name, sdi_default, sdi_date, sdi_user '
               'FROM sending_method '
               'ORDER BY sdi_type, sdi_name')

        cursor.execute(req,)

        return cursor.fetchall()

    @staticmethod
    def getSendingMethodDet(type, id_item):
        cursor = DB.cursor()

        if type == 'S':
            # SMTP: join only SMTP detail
            req = (
                "SELECT "
                "  m.sdi_ser, m.sdi_type, m.sdi_name, m.sdi_default, m.sdi_date, m.sdi_user, "
                "  s.sds_ser, s.sds_sdi, s.sds_host, s.sds_port, s.sds_username, s.sds_password, "
                "  s.sds_ssl, s.sds_starttls, s.sds_from_email, s.sds_from_name "
                "FROM sending_method m "
                "LEFT JOIN sending_method_smtp s ON s.sds_sdi = m.sdi_ser "
                "WHERE m.sdi_ser = %s AND m.sdi_type = 'S' LIMIT 1"
            )

        elif type == 'M':
            # Mailjet: join only Mailjet detail
            req = (
                "SELECT "
                "  m.sdi_ser, m.sdi_type, m.sdi_name, m.sdi_default, m.sdi_date, m.sdi_user, "
                "  mj.sdm_ser, mj.sdm_sdi, mj.sdm_from_email, mj.sdm_from_name, mj.sdm_api_key, mj.sdm_api_secret "
                "FROM sending_method m "
                "LEFT JOIN sending_method_mailjet mj ON mj.sdm_sdi = m.sdi_ser "
                "WHERE m.sdi_ser = %s AND m.sdi_type = 'M' LIMIT 1"
            )

        elif type == 'W':
            # WhatsApp: join only WhatsApp detail (no api_token selected)
            req = (
                "SELECT "
                "  m.sdi_ser, m.sdi_type, m.sdi_name, m.sdi_default, m.sdi_date, m.sdi_user, "
                "  w.sdw_ser, w.sdw_sdi, w.sdw_provider, w.sdw_phone_number, w.sdw_phone_number_id, w.sdw_api_token "
                "FROM sending_method m "
                "LEFT JOIN sending_method_whatsapp w ON w.sdw_sdi = m.sdi_ser "
                "WHERE m.sdi_ser = %s AND m.sdi_type = 'W' LIMIT 1"
            )

        cursor.execute(req, (id_item,))

        return cursor.fetchone()

    @staticmethod
    def insertSendingMethodDet(**params):
        try:
            cursor = DB.cursor()

            # Unset previous default if this one is set as default
            if params.get('sdi_default') == 'Y':
                cursor.execute("UPDATE sending_method SET sdi_default='N' WHERE sdi_default='Y'")

            cursor.execute(
                "INSERT INTO sending_method "
                "(sdi_type, sdi_name, sdi_default, sdi_date, sdi_user) "
                "VALUES (%s, %s, %s, NOW(), %s)",
                (
                    params.get('sdi_type'),
                    params.get('sdi_name'),
                    params.get('sdi_default'),
                    params.get('sdi_user')
                )
            )
            sdi_ser = cursor.lastrowid

            if params.get('sdi_type') == 'S':
                pwd = params.get('sds_password')
                if isinstance(pwd, str):
                    pwd = (pwd.encode('utf-8') if pwd != '' else None)

                cursor.execute(
                    "INSERT INTO sending_method_smtp ("
                    "  sds_sdi, sds_host, sds_port, sds_username, sds_password, "
                    "  sds_ssl, sds_starttls, sds_from_email, sds_from_name"
                    ") VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (
                        sdi_ser,
                        params.get('sds_host'),
                        params.get('sds_port'),
                        params.get('sds_username'),
                        pwd,
                        params.get('sds_ssl', 'N'),
                        params.get('sds_starttls', 'N'),
                        params.get('sds_from_email'),
                        params.get('sds_from_name')
                    )
                )

            elif params.get('sdi_type') == 'M':
                api_key = params.get('sdm_api_key')
                api_sec = params.get('sdm_api_secret')
                if isinstance(api_key, str):
                    api_key = (api_key.encode('utf-8') if api_key != '' else None)
                if isinstance(api_sec, str):
                    api_sec = (api_sec.encode('utf-8') if api_sec != '' else None)

                cursor.execute(
                    "INSERT INTO sending_method_mailjet ("
                    "  sdm_sdi, sdm_api_key, sdm_api_secret, sdm_from_email, sdm_from_name"
                    ") VALUES (%s,%s,%s,%s,%s)",
                    (
                        sdi_ser,
                        api_key,
                        api_sec,
                        params.get('sdm_from_email'),
                        params.get('sdm_from_name')
                    )
                )

            elif params.get('sdi_type') == 'W':
                token = params.get('sdw_api_token')
                if isinstance(token, str):
                    token = (token.encode('utf-8') if token != '' else None)

                cursor.execute(
                    "INSERT INTO sending_method_whatsapp ("
                    "  sdw_sdi, sdw_provider, sdw_api_token, sdw_phone_number, sdw_phone_number_id"
                    ") VALUES (%s,%s,%s,%s,%s)",
                    (
                        sdi_ser,
                        params.get('sdw_provider', 'meta'),
                        token,
                        params.get('sdw_phone_number'),
                        params.get('sdw_phone_number_id'),
                    )
                )

                Setting.log.info(Logs.fileline())

            return sdi_ser
        except mysql.connector.Error as e:
            Setting.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def updateSendingMethodDet(**params):
        try:
            cursor = DB.cursor()

            # Unset previous default if this one is set as default
            if params.get('sdi_default') == 'Y':
                cursor.execute("UPDATE sending_method SET sdi_default='N' WHERE sdi_default='Y'")

            sdi_ser  = params['sdi_ser']
            sdi_type = params['sdi_type']

            cursor.execute(
                "UPDATE sending_method SET "
                "  sdi_name=%s, sdi_default=%s, sdi_date=NOW(), sdi_user=%s "
                "WHERE sdi_ser=%s AND sdi_type=%s",
                (
                    params['sdi_name'],
                    params['sdi_default'],
                    params.get('sdi_user', 0),
                    sdi_ser,
                    sdi_type
                )
            )

            if sdi_type == 'S':
                smtp_password = params.get('sds_password')
                if isinstance(smtp_password, str) and smtp_password != '':
                    cursor.execute(
                        "UPDATE sending_method_smtp SET "
                        "  sds_host=%s, sds_port=%s, sds_username=%s, sds_password=%s, "
                        "  sds_ssl=%s, sds_starttls=%s, sds_from_email=%s, sds_from_name=%s "
                        "WHERE sds_sdi=%s",
                        (
                            params.get('sds_host'),
                            params.get('sds_port'),
                            params.get('sds_username'),
                            smtp_password.encode('utf-8'),
                            params.get('sds_ssl', 'N'),
                            params.get('sds_starttls', 'N'),
                            params.get('sds_from_email'),
                            params.get('sds_from_name'),
                            sdi_ser
                        )
                    )
                else:
                    cursor.execute(
                        "UPDATE sending_method_smtp SET "
                        "  sds_host=%s, sds_port=%s, sds_username=%s, "
                        "  sds_ssl=%s, sds_starttls=%s, sds_from_email=%s, sds_from_name=%s "
                        "WHERE sds_sdi=%s",
                        (
                            params.get('sds_host'),
                            params.get('sds_port'),
                            params.get('sds_username'),
                            params.get('sds_ssl', 'N'),
                            params.get('sds_starttls', 'N'),
                            params.get('sds_from_email'),
                            params.get('sds_from_name'),
                            sdi_ser
                        )
                    )

            elif sdi_type == 'M':
                mailjet_api_key    = params.get('sdm_api_key')
                mailjet_api_secret = params.get('sdm_api_secret')

                if isinstance(mailjet_api_key, str) and mailjet_api_key != '' and isinstance(mailjet_api_secret, str) and mailjet_api_secret != '':
                    cursor.execute(
                        "UPDATE sending_method_mailjet SET "
                        "  sdm_api_key=%s, sdm_api_secret=%s, sdm_from_email=%s, sdm_from_name=%s "
                        "WHERE sdm_sdi=%s",
                        (
                            mailjet_api_key.encode('utf-8'),
                            mailjet_api_secret.encode('utf-8'),
                            params.get('sdm_from_email'),
                            params.get('sdm_from_name'),
                            sdi_ser
                        )
                    )
                elif isinstance(mailjet_api_key, str) and mailjet_api_key != '':
                    cursor.execute(
                        "UPDATE sending_method_mailjet SET "
                        "  sdm_api_key=%s, sdm_from_email=%s, sdm_from_name=%s "
                        "WHERE sdm_sdi=%s",
                        (
                            mailjet_api_key.encode('utf-8'),
                            params.get('sdm_from_email'),
                            params.get('sdm_from_name'),
                            sdi_ser
                        )
                    )
                elif isinstance(mailjet_api_secret, str) and mailjet_api_secret != '':
                    cursor.execute(
                        "UPDATE sending_method_mailjet SET "
                        "  sdm_api_secret=%s, sdm_from_email=%s, sdm_from_name=%s "
                        "WHERE sdm_sdi=%s",
                        (
                            mailjet_api_secret.encode('utf-8'),
                            params.get('sdm_from_email'),
                            params.get('sdm_from_name'),
                            sdi_ser
                        )
                    )
                else:
                    cursor.execute(
                        "UPDATE sending_method_mailjet SET "
                        "  sdm_from_email=%s, sdm_from_name=%s "
                        "WHERE sdm_sdi=%s",
                        (
                            params.get('sdm_from_email'),
                            params.get('sdm_from_name'),
                            sdi_ser
                        )
                    )

            elif sdi_type == 'W':
                whatsapp_api_token = params.get('sdw_api_token')

                if isinstance(whatsapp_api_token, str) and whatsapp_api_token != '':
                    cursor.execute(
                        "UPDATE sending_method_whatsapp SET "
                        "  sdw_provider=%s, sdw_api_token=%s, sdw_phone_number=%s, sdw_phone_number_id=%s "
                        "WHERE sdw_sdi=%s",
                        (
                            params.get('sdw_provider', 'meta'),
                            whatsapp_api_token.encode('utf-8'),
                            params.get('sdw_phone_number'),
                            params.get('sdw_phone_number_id'),
                            sdi_ser
                        )
                    )
                else:
                    cursor.execute(
                        "UPDATE sending_method_whatsapp SET "
                        "  sdw_provider=%s, sdw_phone_number=%s, sdw_phone_number_id=%s "
                        "WHERE sdw_sdi=%s",
                        (
                            params.get('sdw_provider', 'meta'),
                            params.get('sdw_phone_number'),
                            params.get('sdw_phone_number_id'),
                            sdi_ser
                        )
                    )

                    Setting.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Setting.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def deleteSendingMethodDet(type, id_item):
        try:
            cursor = DB.cursor()

            if type == 'S':
                cursor.execute("DELETE FROM sending_method_smtp WHERE sds_sdi=%s", (id_item,))
            elif type == 'M':
                cursor.execute("DELETE FROM sending_method_mailjet WHERE sdm_sdi=%s", (id_item,))
            elif type == 'W':
                cursor.execute("DELETE FROM sending_method_whatsapp WHERE sdw_sdi=%s", (id_item,))
            else:
                Setting.log.error(Logs.fileline() + f' : ERROR unknown type {type}')
                return False

            cursor.execute("DELETE FROM sending_method WHERE sdi_ser=%s AND sdi_type=%s", (id_item, type))

            Setting.log.info(Logs.fileline() + f' : DELETE sending_method {type}/{id_item}')
            return True

        except mysql.connector.Error as e:
            Setting.log.error(Logs.fileline() + ' : ERROR SQL deleteSendingMethod = ' + str(e))
            return False

    @staticmethod
    def testSmtpMethod(id_item, to_addr=None, subject=None, body_text=None):
        if not to_addr:
            to_addr = Constants.cst_email_test

        try:
            cursor = DB.cursor()
            cursor.execute(
                "SELECT s.sds_host, s.sds_port, s.sds_username, s.sds_password, "
                "       s.sds_ssl, s.sds_starttls, s.sds_from_email, s.sds_from_name "
                "FROM sending_method m "
                "JOIN sending_method_smtp s ON s.sds_sdi = m.sdi_ser "
                "WHERE m.sdi_ser=%s AND m.sdi_type='S' "
                "LIMIT 1",
                (id_item,)
            )
            row = cursor.fetchone()

            if not row:
                return (False, "SMTP configuration not found")

            host         = row.get('sds_host')
            port         = int(row.get('sds_port') or 0)
            username     = row.get('sds_username') or ''
            password     = row.get('sds_password') or b''
            use_ssl      = (row.get('sds_ssl') == 'Y')
            use_starttls = (row.get('sds_starttls') == 'Y')
            from_email   = row.get('sds_from_email') or ''
            from_name    = row.get('sds_from_name') or ''

            if isinstance(password, (bytes, bytearray)):
                try:
                    password = password.decode('utf-8', errors='ignore')
                except Exception:
                    password = ''

            if not host or not port:
                return (False, "SMTP host/port missing.")
            if not from_email:
                return (False, "Sender address (from) missing.")

            # Compose message
            msg = EmailMessage()
            msg['Subject'] = subject or "LabBook – Test de la méthode d’envoi SMTP"
            msg['From'] = f"{from_name} <{from_email}>" if from_name else from_email
            msg['To'] = to_addr
            msg.set_content(
                body_text or (
                    "Bonjour,\n\n"
                    "Ceci est un email de test envoyé depuis LabBook pour vérifier la configuration SMTP.\n"
                    "Si vous recevez ce message, la méthode d'envoi SMTP est opérationnelle.\n\n"
                    "— LabBook\n"
                )
            )

            # Connexion
            timeout = 15
            context = ssl.create_default_context()
            context.minimum_version = ssl.TLSVersion.TLSv1_2
            if use_ssl:
                server = smtplib.SMTP_SSL(host=host, port=port, timeout=timeout, context=context)
            else:
                server = smtplib.SMTP(host=host, port=port, timeout=timeout)

            try:
                server.ehlo()
                if (not use_ssl) and use_starttls:
                    server.starttls(context=context)
                    server.ehlo()

                if username:
                    server.login(username, password or '')

                server.send_message(msg)
                server.quit()
            except Exception:
                # Ensures closure if an exception occurs after opening
                try:
                    server.quit()
                except Exception:
                    try:
                        server.close()
                    except Exception:
                        pass
                raise

            mode = "SSL" if use_ssl else ("STARTTLS" if use_starttls else "plain")
            auth = " + AUTH" if username else ""
            return (True, f"Test email sent to {to_addr} via {host}:{port} ({mode}{auth}).")

        except smtplib.SMTPAuthenticationError as e:
            return (False, f"Authentication failed: {e}")
        except (smtplib.SMTPConnectError, smtplib.SMTPServerDisconnected) as e:
            return (False, f"Connection failed: {e}")
        except (socket.timeout, socket.gaierror) as e:
            return (False, f"Network/timeout: {e}")
        except Exception as e:
            return (False, f"Error: {e}")

    @staticmethod
    def testMailjetMethod(id_item, to_addr=None, subject=None, html_part=None):
        if not to_addr:
            to_addr = Constants.cst_email_test

        try:
            cursor = DB.cursor()
            cursor.execute(
                "SELECT mj.sdm_api_key, mj.sdm_api_secret, mj.sdm_from_email, mj.sdm_from_name "
                "FROM sending_method m "
                "JOIN sending_method_mailjet mj ON mj.sdm_sdi = m.sdi_ser "
                "WHERE m.sdi_ser=%s AND m.sdi_type='M' "
                "LIMIT 1",
                (id_item,)
            )
            row = cursor.fetchone()

            if not row:
                return (False, "Mailjet configuration not found")

            api_key_raw    = row.get('sdm_api_key') or b''
            api_secret_raw = row.get('sdm_api_secret') or b''
            from_email     = row.get('sdm_from_email') or ''
            from_name      = row.get('sdm_from_name') or ''

            # Decode VARBINARY -> str
            api_key = api_key_raw.decode('utf-8', errors='ignore') if isinstance(api_key_raw, (bytes, bytearray)) else str(api_key_raw)
            api_secret = api_secret_raw.decode('utf-8', errors='ignore') if isinstance(api_secret_raw, (bytes, bytearray)) else str(api_secret_raw)

            if not api_key or not api_secret:
                return (False, "Missing Mailjet API keys")
            if not from_email:
                return (False, "Sender address (from) missing")

            client = Client(auth=(api_key, api_secret), version='v3.1')
            # If you need to force a region/URL : , api_url='https://api.mailjet.com')

            # Payload v3.1
            payload = {
                "Messages": [{
                    "From": {"Email": from_email, **({"Name": from_name} if from_name else {})},
                    "To": [{"Email": to_addr}],
                    "Subject": subject or "LabBook – Test de la méthode d’envoi Mailjet",
                    "TextPart": (
                        "Bonjour,\n\n"
                        "Ceci est un email de test envoyé depuis LabBook pour vérifier la configuration Mailjet.\n"
                        "Si vous recevez ce message, la méthode d'envoi Mailjet est opérationnelle.\n\n"
                        "— LabBook\n"
                    ),
                    "HTMLPart": html_part or """\
                            <!doctype html>
                        <html lang="fr">
                          <body style="font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;line-height:1.5;">
                            <h2 style="margin:0 0 12px;">Test Mailjet – LabBook</h2>
                            <p>Bonjour,</p>
                            <p>Ceci est un email de test envoyé depuis <em>LabBook</em> pour vérifier la configuration Mailjet.</p>
                            <p>Si vous recevez ce message, la méthode d'envoi Mailjet est opérationnelle.</p>
                            <hr style="border:none;border-top:1px solid #e5e5e5;margin:16px 0;">
                            <p style="color:#666;margin:0;">— LabBook</p>
                          </body>
                        </html>"""
                }]
            }

            result = client.send.create(data=payload)
            status = getattr(result, 'status_code', None)
            try:
                body = result.json()
            except Exception:
                body = {}

            if status not in (200, 201):
                # Returns the error returned by the API
                return (False, f"HTTP {status}: {json.dumps(body or {'text': getattr(result, 'text', '')})[:500]}")

            # Structure attendue: {"Messages":[{"Status":"success", "To":[{"Email":"...","MessageID":...}], ...}]}
            messages = body.get("Messages") or []
            first = messages[0] if messages else {}
            if first.get("Status") != "success":
                return (False, f"Failed to send: {json.dumps(first)[:500]}")

            to_info = (first.get("To") or [{}])[0]
            message_id = to_info.get("MessageID")
            return (True, f"Mailjet test email sent to {to_addr} (MessageID={message_id}).")

        except Exception as e:
            return (False, f"Error: {e}")

    @staticmethod
    def testWhatsappMethod(id_item, to_phone=None, template_name=None, lang='fr'):
        try:
            cursor = DB.cursor()
            cursor.execute(
                "SELECT w.sdw_api_token, w.sdw_phone_number_id "
                "FROM sending_method m "
                "JOIN sending_method_whatsapp w ON w.sdw_sdi = m.sdi_ser "
                "WHERE m.sdi_ser=%s AND m.sdi_type='W' "
                "LIMIT 1",
                (id_item,)
            )
            row = cursor.fetchone()

            if not row:
                return (False, "Configuration WhatsApp introuvable")

            token_raw = row.get('sdw_api_token') or b''
            phone_number_id = (row.get('sdw_phone_number_id') or '').strip()

            # Decode VARBINARY -> str
            token = (Setting.decode_token(token_raw) or '').strip()

            if not token or not phone_number_id:
                return (False, "Jeton API ou identifiant de numéro manquant")

            # Default recipient (your number in E.164 format)
            if not to_phone:
                return (False, "Numéro de destinataire requis (format E.164)")

            to_phone = Setting.normalize_fr_e164(to_phone)

            used_tpl = (template_name or Constants.cst_model_test_whatsapp)

            # Determine if template expects an attachment (from sending_model)
            cursor.execute(
                "SELECT mdl_has_attachment, mdl_lang "
                "FROM sending_model "
                "WHERE mdl_type='W' AND mdl_name=%s "
                "LIMIT 1",
                (used_tpl,)
            )
            mdl_row = cursor.fetchone()
            has_attachment = (mdl_row and (mdl_row.get('mdl_has_attachment') or 'N') == 'Y')
            used_lang = (lang or (mdl_row.get('mdl_lang') if mdl_row else None) or "en")

            msg_url   = Constants.cst_msg_whatsapp.format(pnid=phone_number_id)
            media_url = Constants.cst_media_whatsapp.format(pnid=phone_number_id)

            headers_json = {
                "Authorization": f"Bearer {token}",
                "Content-Type": Constants.cst_content_type_json
            }

            if not has_attachment:
                payload = {
                    "messaging_product": "whatsapp",
                    "to": to_phone,
                    "type": "template",
                    "template": {
                        "name": used_tpl,
                        "language": {"code": used_lang}
                    }
                }

                resp = requests.post(msg_url, headers=headers_json, json=payload, timeout=20)
                ok = resp.status_code in (200, 201)

                try:
                    body = resp.json()
                except Exception:
                    body = {"text": resp.text[:300]}

                if not ok:
                    return (False, f"HTTP {resp.status_code}: {json.dumps(body)[:600]}")

                return (True, f"WhatsApp message (template ‘{used_tpl}’) sent to {to_phone}.")

            else:
                base_tmp = Constants.cst_path_tmp.rstrip('/')
                filename = f"whatsapp_dummy_{int(time.time())}.pdf"
                tmp_path = os.path.join(base_tmp, filename).strip()

                # Create a minimal dummy PDF (no external dependency)
                # Note: This is a very small, valid-enough PDF for testing uploads.
                dummy_pdf_bytes = (
                    b"%PDF-1.4\n"
                    b"1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj\n"
                    b"2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj\n"
                    b"3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 200 200] /Contents 4 0 R >> endobj\n"
                    b"4 0 obj << /Length 44 >> stream\n"
                    b"BT /F1 12 Tf 72 120 Td (Dummy WhatsApp Test) Tj ET\n"
                    b"endstream endobj\n"
                    b"5 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj\n"
                    b"xref\n"
                    b"0 6\n"
                    b"0000000000 65535 f \n"
                    b"0000000010 00000 n \n"
                    b"0000000061 00000 n \n"
                    b"0000000115 00000 n \n"
                    b"0000000205 00000 n \n"
                    b"0000000311 00000 n \n"
                    b"trailer << /Size 6 /Root 1 0 R >>\n"
                    b"startxref\n"
                    b"380\n"
                    b"%%EOF\n"
                )

                # Write file to disk
                with open(tmp_path, 'wb') as fh:
                    fh.write(dummy_pdf_bytes)

                # Upload media to Meta (multipart/form-data)
                with open(tmp_path, 'rb') as fh:
                    files = {"file": (filename, fh, Constants.cst_content_type_pdf)}
                    data = {"messaging_product": "whatsapp", "type": "document"}
                    headers_media = {"Authorization": f"Bearer {token}"}
                    media_resp = requests.post(media_url, headers=headers_media, data=data, files=files, timeout=30)

                ok_media = media_resp.status_code in (200, 201)
                try:
                    media_body = media_resp.json()
                except Exception:
                    media_body = {"text": media_resp.text[:300]}

                if not ok_media or "id" not in media_body:
                    # cleanup on failure
                    try:
                        os.remove(tmp_path)
                    except Exception:
                        pass
                    return (False, f"Échec de l’upload média (HTTP {media_resp.status_code}) : {json.dumps(media_body)[:600]}")

                media_id = media_body["id"]

                # cleanup on success
                try:
                    os.remove(tmp_path)
                except Exception:
                    pass

            # Send the template with a header document referencing the uploaded media
            payload_with_doc = {
                "messaging_product": "whatsapp",
                "to": to_phone,
                "type": "template",
                "template": {
                    "name": used_tpl,
                    "language": {"code": used_lang},
                    "components": [
                        {
                            "type": "header",
                            "parameters": [
                                {
                                    "type": "document",
                                    "document": {"id": media_id}  # optionally add "filename": "test.pdf"
                                }
                            ]
                        }
                    ]
                }
            }

            resp2 = requests.post(msg_url, headers=headers_json, json=payload_with_doc, timeout=20)
            ok2 = resp2.status_code in (200, 201)

            try:
                body2 = resp2.json()
            except Exception:
                body2 = {"text": resp2.text[:300]}

            if not ok2:
                return (False, f"HTTP {resp2.status_code}: {json.dumps(body2)[:600]}")

            return (True, f"Message WhatsApp (modèle « {used_tpl} » avec pièce jointe) envoyé à {to_phone}.")

        except requests.exceptions.RequestException as e:
            return (False, f"Erreur réseau WhatsApp : {e}")
        except Exception as e:
            return (False, f"Erreur : {e}")

    # Simple normalization to E.164 FR if necessary
    @staticmethod
    def normalize_fr_e164(n: str) -> str:
        n = (n or "").strip().replace(" ", "").replace(".", "").replace("-", "").replace("(", "").replace(")", "")
        if n.startswith("+"):
            return n
        if n.startswith("00"):
            return "+" + n[2:]
        if n.startswith("0"):
            return "+33" + n[1:]
        return n  # Leave it as is if it is already in the correct format.

    @staticmethod
    def decode_token(x):
        # MySQL VARBINARY -> bytes -> str
        if isinstance(x, (bytes, bytearray, memoryview)):
            try:
                return bytes(x).decode('utf-8')
            except UnicodeDecodeError:
                try:
                    return binascii.unhexlify(bytes(x)).decode('utf-8')
                except Exception:
                    return ''
        # Si jamais stocké en "0x...."
        s = str(x or '')
        if s.startswith(('0x', '0X')):
            try:
                return binascii.unhexlify(s[2:]).decode('utf-8')
            except Exception:
                return ''
        return s

    @staticmethod
    def getSendingModelList():
        cursor = DB.cursor()

        req = ('SELECT mdl_ser, mdl_type, mdl_displayname, mdl_name, mdl_lang, mdl_default, mdl_date, mdl_user '
               'FROM sending_model '
               'ORDER BY mdl_type, mdl_displayname')

        cursor.execute(req,)

        return cursor.fetchall()

    @staticmethod
    def getSendingModelDet(type, id_item):
        cursor = DB.cursor()

        req = ('SELECT mdl_ser, mdl_type, mdl_displayname, mdl_name, mdl_lang, mdl_text, '
               '       mdl_default, mdl_date, mdl_user, mdl_has_attachment '
               'FROM sending_model '
               'WHERE mdl_ser = %s AND mdl_type = %s')

        cursor.execute(req, (id_item, type))

        return cursor.fetchone()

    @staticmethod
    def insertSendingModelDet(**params):
        try:
            cursor = DB.cursor()

            mdl_type = (params.get('mdl_type') or '').upper()[:1]
            mdl_default = (params.get('mdl_default') or 'N')[:1]
            mdl_user = params.get('mdl_user')
            mdl_name = params.get('mdl_name')
            mdl_text = params.get('mdl_text')
            mdl_displayname = params.get('mdl_displayname')
            mdl_lang        = (params.get('mdl_lang') or 'fr').strip()

            # Ensure non-null language
            if not mdl_lang:
                mdl_lang = 'fr'

            mdl_has_attachment = (params.get('mdl_has_attachment') or 'N')
            if mdl_type != 'W':
                mdl_has_attachment = 'N'

            req = (
                "INSERT INTO sending_model "
                "(mdl_type, mdl_displayname, mdl_name, mdl_lang, mdl_text, mdl_has_attachment, mdl_default, mdl_date, mdl_user) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), %s)"
            )
            cursor.execute(req, (mdl_type, mdl_displayname, mdl_name, mdl_lang, mdl_text, mdl_has_attachment, mdl_default, mdl_user))

            mdl_ser = cursor.lastrowid

            # If set to default = ‘Y’, disables others of this type
            if mdl_default == 'Y':
                cursor.execute("UPDATE sending_model SET mdl_default='N' "
                               "WHERE mdl_type=%s AND mdl_ser<>%s AND mdl_default='Y'", (mdl_type, mdl_ser))

                Setting.log.info(Logs.fileline())

            return mdl_ser
        except mysql.connector.Error as e:
            Setting.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def updateSendingModelDet(**params):
        try:
            cursor = DB.cursor()

            mdl_ser         = params.get('mdl_ser')
            mdl_type        = params.get('mdl_type')
            mdl_displayname = params.get('mdl_displayname')
            mdl_name        = params.get('mdl_name')
            mdl_text        = params.get('mdl_text')
            mdl_default     = params.get('mdl_default', 'N')
            mdl_user        = params.get('mdl_user')
            mdl_lang        = params.get('mdl_lang')

            mdl_has_attachment = (params.get('mdl_has_attachment') or 'N')
            if mdl_type != 'W':
                mdl_has_attachment = 'N'

            req = ("UPDATE sending_model "
                   "SET mdl_type=%s, mdl_displayname=%s, mdl_name=%s, mdl_lang=%s, mdl_text=%s, "
                   "    mdl_has_attachment=%s, mdl_default=%s, mdl_user=%s, mdl_date=NOW() "
                   "WHERE mdl_ser=%s")

            cursor.execute(req, (mdl_type, mdl_displayname, mdl_name, mdl_lang, mdl_text,
                                 mdl_has_attachment, mdl_default, mdl_user, mdl_ser))

            if mdl_default == 'Y':
                cursor.execute("UPDATE sending_model SET mdl_default='N' "
                               "WHERE mdl_type=%s AND mdl_ser<>%s AND mdl_default='Y'", (mdl_type, mdl_ser))

                Setting.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Setting.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def deleteSendingModelDet(type, id_item):
        try:
            cursor = DB.cursor()

            cursor.execute("DELETE FROM sending_model WHERE mdl_ser=%s AND mdl_type=%s", (id_item, type))

            Setting.log.info(Logs.fileline() + f' : DELETE sending_model {type}/{id_item}')
            return True

        except mysql.connector.Error as e:
            Setting.log.error(Logs.fileline() + ' : ERROR SQL deleteSendingModel = ' + str(e))
            return False

    @staticmethod
    def pickMethodIdForTest(type, override_id=None):
        """Select method for given type: override -> default -> newest."""
        if override_id is not None:
            return int(override_id)

        cursor = DB.cursor()

        # default of same type
        cursor.execute(
            "SELECT sdi_ser FROM sending_method "
            "WHERE sdi_type=%s AND sdi_default='Y' "
            "ORDER BY IFNULL(sdi_date,'1970-01-01') DESC, sdi_ser DESC LIMIT 1",
            (type,)
        )
        row = cursor.fetchone()
        if row and row.get('sdi_ser'):
            return int(row['sdi_ser'])

        # else newest of same type
        cursor.execute(
            "SELECT sdi_ser FROM sending_method "
            "WHERE sdi_type=%s "
            "ORDER BY IFNULL(sdi_date,'1970-01-01') DESC, sdi_ser DESC LIMIT 1",
            (type,)
        )
        row = cursor.fetchone()
        return int(row['sdi_ser']) if row and row.get('sdi_ser') else None

    @staticmethod
    def send_test_smtp(method_id, to_email, subject, body_text):
        # Delegate to low-level tester; return boolean
        ok, _ = Setting.testSmtpMethod(method_id, to_addr=to_email, subject=subject, body_text=body_text)
        return ok

    @staticmethod
    def send_test_mailjet(method_id, to_email, subject, html_body):
        # Provide HTML; TextPart can be None
        ok, _ = Setting.testMailjetMethod(method_id, to_addr=to_email, subject=subject, html_part=html_body)
        return ok

    @staticmethod
    def send_test_whatsapp(method_id, to_phone, template_name, lang='fr'):
        ok, _ = Setting.testWhatsappMethod(method_id, to_phone=to_phone, template_name=template_name, lang=lang)
        return ok

    @staticmethod
    def testSendingModel(type, mdl_ser, to, method_id_override=None, lang='fr'):
        """Send a test using a model (S/M uses mdl_text, W uses mdl_name). Returns (ok, message)."""

        # Load model
        model = Setting.getSendingModelDet(type, mdl_ser)
        if not model:
            return (False, "Model not found")

        # Pick sending method for this type
        method_id = Setting.pickMethodIdForTest(type, method_id_override)
        if not method_id:
            return (False, "No sending method for this type")

        # Dispatch by type
        if type == 'S':
            subject = f"[TEST] {model.get('mdl_displayname') or 'SMTP model'}"
            body    = model.get('mdl_text') or ''
            ok = Setting.send_test_smtp(method_id, to, subject, body)
            return (ok, "SMTP test sent" if ok else "SMTP send failed")

        if type == 'M':
            subject = f"[TEST] {model.get('mdl_displayname') or 'Mailjet model'}"
            html    = model.get('mdl_text') or ''
            ok = Setting.send_test_mailjet(method_id, to, subject, html)
            return (ok, "Mailjet test sent" if ok else "Mailjet send failed")

        if type == 'W':
            tpl = model.get('mdl_name') or ''
            if not tpl:
                return (False, "WhatsApp template name missing in model")
            lang_eff = lang or (model.get('mdl_lang') or 'fr')
            ok = Setting.send_test_whatsapp(method_id, to, tpl, lang_eff)
            return (ok, "WhatsApp test sent" if ok else "WhatsApp send failed")

        return (False, "Invalid type")

    @staticmethod
    def sendReport(**params):
        cursor = DB.cursor()

        rec_num  = params.get('rec_num')
        pat_code = params.get('pat_code') or ''
        id_user  = int(params.get('id_user') or 0)

        if not rec_num:
            return (False, _("numéro de compte rendu manquant"))

        display_name = f"cr_{rec_num}.pdf"

        pdf_filename = (params.get('filename') or '').strip()
        if not pdf_filename.lower().endswith('.pdf'):
            pdf_filename += '.pdf'

        ok, tmp_path, info = Setting.make_pdf_copy_protected(
            generated_name=pdf_filename,
            rec_num=params.get('rec_num'),
            pat_code=pat_code
        )
        if not ok:
            return (False, info)

        if not tmp_path or not os.path.exists(tmp_path):
            Setting.log.error(Logs.fileline() + f" : PDF NOT FOUND -> {tmp_path}")
            return (False, "PDF introuvable après génération")

        # get details of patient
        pat = Patient.getPatientByCode(pat_code, '')
        if not pat:
            return (False, _("patient introuvable"))

        # --- AMICARE DIRECT MODE (no DB method/model) ---
        if params['method_type'] == 'A':

            try:
                ok, msg = Setting.sendAmicare(
                    None,
                    pat_code,
                    tmp_path,
                    display_name,
                    rec_num,
                    id_user
                )

                if ok:
                    Setting.log.info("sendReport AMICARE OK")
                else:
                    Setting.log.error(f"sendReport AMICARE FAIL -> {msg}")

                return (ok, msg)

            except Exception as e:
                Setting.log.error(f"sendReport AMICARE EXCEPTION -> {e}")
                return (False, str(e))

            finally:
                try:
                    if tmp_path and os.path.exists(tmp_path):
                        os.remove(tmp_path)
                except Exception:
                    pass
        # -------------------------------------------------

        method = Setting.getSendingMethodDet(params['method_type'], params['method_id'])
        if not method:
            return (False, _("méthode d’envoi introuvable"))

        model = Setting.getSendingModelDet(params['method_type'], params['template_id'])
        if not model:
            return (False, _("modèle d’envoi introuvable"))

        info_pat = {'pat_lname': pat['nom'], 'pat_fname': pat['prenom']}

        # Trace the sending event: insert with state Q (queued)
        sde_ser = None
        try:
            sde_ser = Setting.insert_sending_event(cursor, params)
        except Exception as err:
            # If insertion fails, we continue sending but without DB trace
            Setting.log.error(Logs.fileline() + f" : ERROR insert_sending_event = {err}")

        try:
            mtype = params['method_type']
            recipient = params.get('recipient')

            # SMTP MESSAGE
            if mtype == 'S':
                subject = Setting.render_vars(model.get('mdl_displayname') or '', info_pat).strip()
                body_txt = (Setting.render_vars(model.get('mdl_text') or '', info_pat) or '').strip()

                ok, msg = Setting.sendSmtpWithAttachment(
                    method,
                    recipient,
                    subject,
                    body_txt,
                    tmp_path,
                    filename=display_name
                )

            # MAILJET MESSAGE
            elif mtype == 'M':
                subject   = Setting.render_vars(model.get('mdl_displayname') or '', info_pat).strip()
                html_body = Setting.render_vars(model.get('mdl_text') or '', info_pat)
                text_body = (html_body or '')

                ok, msg = Setting.sendMailjetWithAttachment(
                    method, recipient, subject, html_body, text_body, tmp_path, filename=display_name
                )

            # WHATSAPP MESSSAGE
            elif mtype == 'W':
                tpl_name = model.get('mdl_name') or ''

                if not tpl_name:
                    return (False, _("nom de modèle WhatsApp manquant dans le modèle d’envoi"))

                has_att  = (model.get('mdl_has_attachment') == 'Y')
                tpl_lang = (model.get('mdl_lang') or 'fr')

                ok, msg = Setting.sendWhatsappTemplate(
                    method,
                    recipient,
                    tpl_name,
                    attach_path=(tmp_path if has_att else None),
                    lang=tpl_lang,
                    template_vars=info_pat,
                    filename=display_name
                )

            else:
                # Unknown type
                if sde_ser:
                    Setting.update_sending_event_fail(cursor, sde_ser, ("type de méthode invalide"), id_user)
                return (False, _("type de méthode invalide"))

            # Update sending_event according to result
            if sde_ser:
                if ok:
                    Setting.update_sending_event_success(cursor, sde_ser, id_user)
                else:
                    Setting.update_sending_event_fail(cursor, sde_ser, msg or ("échec d’envoi"), id_user)

            return (ok, msg if msg else (_("envoyé") if ok else _("échec d’envoi")))

        except Exception as err:
            # Update as failed on exception
            if sde_ser:
                Setting.update_sending_event_fail(cursor, sde_ser, err, id_user)
            return (False, f"Erreur lors de l’envoi : {err}")

        # remove temporary copy of report
        finally:
            try:
                if tmp_path and os.path.exists(tmp_path):
                    os.remove(tmp_path)
            except Exception:
                pass

    @staticmethod
    def sendAmicare(method, pat_code, file_path, filename, rec_num, id_user):
        try:
            from app import AMICARE_CONFIG
            from datetime import datetime

            if not AMICARE_CONFIG or not AMICARE_CONFIG.get('enabled'):
                return (False, ("AmiCare désactivé"))

            # --- patient ---
            pat = Patient.getPatientByCode(pat_code, '')
            if not pat:
                return (False, ("patient introuvable"))

            id_amicare = pat.get('pat_amicare')
            if not id_amicare or int(id_amicare) <= 0:
                return (False, ("patient sans compte AmiCare"))

            # --- config ---
            base_url = AMICARE_CONFIG.get('base_url')
            endpoint = (AMICARE_CONFIG.get('endpoints') or {}).get('send_document')
            auth_cfg = AMICARE_CONFIG.get('auth') or {}
            timeout  = (AMICARE_CONFIG.get('options') or {}).get('timeout_sec', 10)

            if not base_url or not endpoint:
                return (False, ("configuration AmiCare invalide"))

            url = base_url.rstrip('/') + endpoint

            username = auth_cfg.get('username')
            password = auth_cfg.get('password')

            Setting.log.error(f"AMICARE URL -> {url}")
            Setting.log.error(f"AMICARE AUTH -> user={username}")

            if not username or not password:
                return (False, ("auth AmiCare invalide"))

            # --- JSON index expected ---
            payload = {
                "lot_documents": {
                    "expediteur": {
                        "hopital": {
                            "login": username
                        }
                    },
                    "destinataire": {
                        "patient": {
                            "id_amicare": int(id_amicare)
                        }
                    },
                    "documents": [
                        {
                            "id": 1,
                            "nom": "file1",
                            "titre": "Compte rendu LabBook",
                            "date": datetime.now().strftime("%Y-%m-%d"),
                            "patient": {
                                "id_amicare": int(id_amicare)
                            }
                        }
                    ]
                }
            }

            Setting.log.error("AMICARE PAYLOAD JSON -> " + json.dumps(payload))
            Setting.log.error(f"AMICARE FILE -> path={file_path} name={filename}")

            with open(file_path, "rb") as f:
                resp = requests.post(
                    url,
                    auth=(username, password),
                    files={
                        "file1": ("cr_%s.pdf" % rec_num, f, Constants.cst_content_type_pdf),
                        "index": (None, json.dumps(payload), Constants.cst_content_type_json)
                    },
                    timeout=10
                )

            Setting.log.error(f"AMICARE RESPONSE -> status={resp.status_code} body={resp.text}")

            if resp.status_code not in (200, 201):
                return (False, f"AmiCare HTTP {resp.status_code} : {resp.text}")

            return (True, "AmiCare envoyé")

        except Exception as e:
            return (False, f"AmiCare error: {e}")

    @staticmethod
    def make_pdf_copy_protected(generated_name: str, rec_num, pat_code: str):
        """Create a tmp copy of report as 'cr_<rec_num>.pdf' and protect it with pat_code."""
        if not generated_name:
            return (False, None, _("nom de fichier source manquant"))

        if not pat_code:
            return (False, None, _("code patient manquant pour le mot de passe PDF"))

        base_dir = getattr(Constants, "cst_report", "/storage/report")
        src_path = os.path.join(base_dir, generated_name).strip()

        # hashed reports may be stored without ".pdf" on disk
        if not os.path.isfile(src_path) and generated_name.lower().endswith(".pdf"):
            alt_name = generated_name[:-4]  # remove ".pdf"
            alt_path = os.path.join(base_dir, alt_name).strip()
            if os.path.isfile(alt_path):
                src_path = alt_path

        if not os.path.isfile(src_path):
            return (False, None, f"fichier source introuvable : {generated_name}")

        dst_name = f"cr_{rec_num or 0}.pdf"
        dst_path = os.path.join(Constants.cst_path_tmp, dst_name).strip()

        try:
            # Open source and save encrypted copy (no unprotected copy is written)
            with pikepdf.open(src_path) as pdf:
                title = os.path.splitext(dst_name)[0]
                if title:
                    pdf.docinfo['/Title'] = title

                pdf.save(
                    dst_path,
                    encryption=pikepdf.Encryption(
                        owner=pat_code,  # owner password
                        user=pat_code,   # user/open password
                        R=4              # 128-bit AES; keep compatibility
                    )
                )
            return (True, dst_path, "")
        except pikepdf.PasswordError as e:
            return (False, None, f"erreur de mot de passe PDF: {e}")
        except pikepdf.PdfError as e:
            return (False, None, f"erreur pdf : {e}")
        except Exception as e:
            return (False, None, f"erreur de protection PDF : {e}")

    @staticmethod
    def sendSmtpWithAttachment(method_row, to_addr, subject, body_text, attach_path, filename):
        """Send a mail via SMTP using an already-fetched DB row (no extra query)."""
        try:
            host         = method_row.get('sds_host')
            port         = int(method_row.get('sds_port') or 0)
            username     = method_row.get('sds_username') or ''
            pwd_raw      = method_row.get('sds_password') or b''
            use_ssl      = (method_row.get('sds_ssl') == 'Y')
            use_starttls = (method_row.get('sds_starttls') == 'Y')
            from_email   = method_row.get('sds_from_email') or ''
            from_name    = method_row.get('sds_from_name') or ''

            # Decode VARBINARY password if needed
            if isinstance(pwd_raw, (bytes, bytearray)):
                try:
                    password = pwd_raw.decode('utf-8', errors='ignore')
                except Exception:
                    password = ''
            else:
                password = str(pwd_raw or '')

            if not host or not port:
                return (False, "Hôte/port SMTP manquant")
            if not from_email:
                return (False, "Adresse expéditeur manquante")
            if not to_addr:
                return (False, "Destinataire manquant")

            msg = EmailMessage()
            msg['Subject'] = subject
            msg['From'] = f"{from_name} <{from_email}>" if from_name else from_email
            msg['To'] = to_addr
            msg.set_content(body_text or "")

            with open(attach_path, 'rb') as fh:
                msg.add_attachment(fh.read(), maintype='application', subtype='pdf',
                                   filename=(filename or os.path.basename(attach_path)))

            timeout = 20
            context = ssl.create_default_context()
            context.minimum_version = ssl.TLSVersion.TLSv1_2
            if use_ssl:
                server = smtplib.SMTP_SSL(host=host, port=port, timeout=timeout, context=context)
            else:
                server = smtplib.SMTP(host=host, port=port, timeout=timeout)

            try:
                server.ehlo()
                if (not use_ssl) and use_starttls:
                    server.starttls(context=context)
                    server.ehlo()
                if username:
                    server.login(username, password or '')
                server.send_message(msg)
                server.quit()
            except Exception:
                try:
                    server.quit()
                except Exception:
                    try:
                        server.close()
                    except Exception:
                        pass
                raise

            return (True, "E-mail SMTP envoyé")

        except smtplib.SMTPAuthenticationError as e:
            return (False, f"Échec d’authentification SMTP : {e}")
        except (smtplib.SMTPConnectError, smtplib.SMTPServerDisconnected) as e:
            return (False, f"Échec de connexion SMTP : {e}")
        except (socket.timeout, socket.gaierror) as e:
            return (False, f"Erreur réseau/timeout SMTP : {e}")
        except Exception as e:
            return (False, f"Erreur d’envoi SMTP : {e}")

    @staticmethod
    def sendMailjetWithAttachment(method_row, to_addr, subject, html_body, text_body, attach_path, filename):
        """Send via Mailjet v3.1 using method_row (already fetched)."""
        try:
            # Decode secrets (VARBINARY -> str)
            api_key_raw    = method_row.get('sdm_api_key') or b''
            api_secret_raw = method_row.get('sdm_api_secret') or b''
            api_key    = api_key_raw.decode('utf-8', errors='ignore') if isinstance(api_key_raw, (bytes, bytearray)) else str(api_key_raw or '')
            api_secret = api_secret_raw.decode('utf-8', errors='ignore') if isinstance(api_secret_raw, (bytes, bytearray)) else str(api_secret_raw or '')

            from_email = method_row.get('sdm_from_email') or ''
            from_name  = method_row.get('sdm_from_name') or ''

            if not api_key or not api_secret:
                return (False, "Clés API Mailjet manquantes")
            if not from_email:
                return (False, "Adresse expéditeur manquante")
            if not to_addr:
                return (False, "Destinataire manquant")

            # Read and base64-encode attachment
            with open(attach_path, 'rb') as fh:
                b64 = base64.b64encode(fh.read()).decode('ascii')

            client = Client(auth=(api_key, api_secret), version='v3.1')

            payload = {
                "Messages": [{
                    "From": {"Email": from_email, **({"Name": from_name} if from_name else {})},
                    "To": [{"Email": to_addr}],
                    "Subject": subject,
                    "TextPart": text_body or "",
                    "HTMLPart": html_body or "",
                    "Attachments": [{
                        "ContentType": Constants.cst_content_type_pdf,
                        "Filename": (filename or os.path.basename(attach_path)),
                        "Base64Content": b64
                    }]
                }]
            }

            result = client.send.create(data=payload)
            status = getattr(result, 'status_code', None)
            try:
                body = result.json()
            except Exception:
                body = {"text": getattr(result, 'text', '')[:300]}

            if status not in (200, 201):
                return (False, f"HTTP {status}: {json.dumps(body)[:600]}")

            msg0 = (body.get("Messages") or [{}])[0]
            if msg0.get("Status") != "success":
                return (False, f"Échec d’envoi: {json.dumps(msg0)[:600]}")

            return (True, "E-mail Mailjet envoyé")

        except Exception as e:
            return (False, f"Erreur Mailjet : {e}")

    @staticmethod
    def sendWhatsappTemplate(method_row, to_phone, template_name, attach_path=None, lang='fr', template_vars=None, filename=None):
        """Send a WhatsApp template message; if attach_path is set, attach as header document."""
        try:
            token_raw = method_row.get('sdw_api_token') or b''
            phone_number_id = (method_row.get('sdw_phone_number_id') or '').strip()

            token = (Setting.decode_token(token_raw) or '').strip()
            if not token or not phone_number_id:
                return (False, "Configuration WhatsApp incomplète (token / phone_number_id)")

            if not to_phone:
                return (False, "Destinataire manquant")
            to_phone = Setting.normalize_fr_e164(to_phone)

            msg_url   = Constants.cst_msg_whatsapp.format(pnid=phone_number_id)
            media_url = Constants.cst_media_whatsapp.format(pnid=phone_number_id)

            headers_json  = {"Authorization": f"Bearer {token}", "Content-Type": Constants.cst_content_type_json}
            headers_media = {"Authorization": f"Bearer {token}"}

            media_id = None
            if attach_path:
                # Upload document first
                with open(attach_path, 'rb') as fh:
                    files = {"file": (os.path.basename(attach_path), fh, Constants.cst_content_type_pdf)}
                    data  = {"messaging_product": "whatsapp", "type": "document"}
                    r_up = requests.post(media_url, headers=headers_media, data=data, files=files, timeout=30)

                ok_up = r_up.status_code in (200, 201)
                try:
                    body_up = r_up.json()
                except Exception:
                    body_up = {"text": r_up.text[:300]}

                if not ok_up or "id" not in body_up:
                    return (False, f"Échec de l’upload média (HTTP {r_up.status_code}) : {json.dumps(body_up)[:600]}")
                media_id = body_up["id"]

            template_name = (template_name or "").strip()
            if not template_name:
                return (False, _("Nom de modèle WhatsApp manquant"))

            components = []

            # Build template payload
            if media_id:
                components.append({
                    "type": "header",
                    "parameters": [{
                        "type": "document",
                        "document": {"id": media_id, **({"filename": filename} if filename else {})}
                    }]
                })

            body_params = []
            if template_vars is not None:
                if not isinstance(template_vars, dict):
                    return (False, "template_vars must be a dict with named keys")
                for _key, value in template_vars.items():
                    body_params.append({
                        "type": "text",
                        "text": "" if value is None else str(value),
                        "parameter_name": _key
                    })

            if body_params:
                components.append({"type": "body", "parameters": body_params})

            template = {
                "name": template_name,
                "language": {"code": (lang or "fr")}
            }
            if components:
                template["components"] = components

            payload = {
                "messaging_product": "whatsapp",
                "to": to_phone,
                "type": "template",
                "template": template
            }

            try:
                Setting.log.info(Logs.fileline() + " : WA payload=" + json.dumps(payload, ensure_ascii=False))
            except Exception:
                pass

            r_msg = requests.post(msg_url, headers=headers_json, json=payload, timeout=20)
            ok_msg = r_msg.status_code in (200, 201)
            try:
                body_msg = r_msg.json()
            except Exception:
                body_msg = {"text": r_msg.text[:300]}

            if not ok_msg:
                return (False, f"Échec d’envoi WhatsApp (HTTP {r_msg.status_code}) : {json.dumps(body_msg)[:600]}")

            return (True, "Message WhatsApp envoyé")
        except requests.exceptions.RequestException as e:
            return (False, f"Erreur réseau WhatsApp : {e}")
        except Exception as e:
            return (False, f"Erreur WhatsApp : {e}")

    @staticmethod
    def insert_sending_event(cursor, params):
        payload = {
            "method_type": params.get('method_type'),
            "method_id":   params.get('method_id'),
            "template_id": params.get('template_id'),
            "recipient":   params.get('recipient'),
            "rec_num":     params.get('rec_num'),
            "filename":    params.get('filename'),
            "pat_code":    params.get('pat_code'),
            "options":     {"pdf_protected": True}
        }
        payload_json = json.dumps(payload, ensure_ascii=False)

        # Insert a new sending_event row with initial state Q (queued)
        cursor.execute("""
            INSERT INTO sending_event
            (sde_user, sde_rec_num, sde_type, sde_method, sde_model, sde_recipient, sde_state, sde_payload)
            VALUES (%s,%s,%s,%s,%s,%s,'Q', CAST(%s AS JSON))
        """, (
            params.get('id_user'),
            params.get('rec_num'),
            params['method_type'],
            params.get('method_id'),
            params.get('template_id'),
            params['recipient'],
            payload_json
        ))
        return cursor.lastrowid

    @staticmethod
    def update_sending_event_success(cursor, sde_ser, id_user):
        # Update sending_event row to state S (sent)
        cursor.execute("""
            UPDATE sending_event
            SET sde_state='S', sde_sent=NOW(), sde_user=%s
            WHERE sde_ser=%s
        """, (id_user, sde_ser,))

    @staticmethod
    def update_sending_event_fail(cursor, sde_ser, error_text, id_user):
        # Update sending_event row to state F (failed)
        cursor.execute("""
            UPDATE sending_event
            SET sde_state='F', sde_error=%s, sde_user=%s
            WHERE sde_ser=%s
        """, (str(error_text)[:65535], id_user, sde_ser))

    @staticmethod
    def getSendingList(limit=1000):
        """
        Return raw rows from sending_event for listing (no mapping, no decoration).
        Same style as getPrefList(): DB.cursor(), execute, fetchall(), return.
        """
        cursor = DB.cursor()

        req = ('SELECT se.sde_ser, se.sde_date, se.sde_sent, se.sde_user, '
               '       se.sde_rec_num, se.sde_type, se.sde_method, se.sde_model, '
               '       se.sde_recipient, se.sde_state, se.sde_error, se.sde_payload, '
               '       u.lastname  AS user_lastname, u.firstname AS user_firstname, u.username  AS user_username '
               'FROM sending_event as se '
               'LEFT JOIN sigl_user_data AS u ON u.id_data = se.sde_user '
               'ORDER BY sde_ser DESC '
               'LIMIT %s')

        cursor.execute(req, (limit,))
        return cursor.fetchall()

    @staticmethod
    def getSendingEvent(sde_ser):
        cursor = DB.cursor()
        cursor.execute(
            "SELECT sde_ser, sde_date, sde_sent, sde_user, sde_rec_num, sde_type, "
            "       sde_method, sde_model, sde_recipient, sde_state, sde_error, sde_payload "
            "FROM sending_event WHERE sde_ser=%s LIMIT 1",
            (sde_ser,)
        )
        return cursor.fetchone()

    @staticmethod
    def update_sending_event_queue(cursor, sde_ser, id_user):
        """Mark event as queued again (clear error/sent)."""
        cursor.execute("""
            UPDATE sending_event
               SET sde_state='Q',
                   sde_error=NULL,
                   sde_date=NOW(),
                   sde_sent=NULL,
                   sde_user=%s
             WHERE sde_ser=%s
        """, (id_user, sde_ser,))

    @staticmethod
    def resend(sde_ser, id_user=0):
        """
        Re-send using the SAME sending_event row (no new row).
        - reload event and payload
        - recompute inputs
        - send via method-specific helpers
        - update the same sde_ser to S/F
        """
        try:
            row = Setting.getSendingEvent(sde_ser)
            if not row:
                return (False, "Event not found")

            # Parse payload JSON if present
            payload = {}
            raw = row.get('sde_payload')
            if raw:
                try:
                    if isinstance(raw, (bytes, bytearray)):
                        raw = raw.decode('utf-8', errors='ignore')
                    payload = json.loads(raw or "{}")
                except Exception:
                    payload = {}

            method_type = (payload.get('method_type') or row.get('sde_type') or '').strip()[:1]
            method_id   = payload.get('method_id') or row.get('sde_method')
            template_id = payload.get('template_id') or row.get('sde_model')
            recipient   = (payload.get('recipient') or row.get('sde_recipient') or '').strip()
            rec_num     = payload.get('rec_num') or row.get('sde_rec_num')
            filename    = (payload.get('filename') or '').strip()
            pat_code    = (payload.get('pat_code') or '').strip()

            # get details of patient
            pat = Patient.getPatientByCode(pat_code, '')
            if not pat:
                return (False, "patient not found")

            info_pat = {}
            info_pat['pat_lname'] = pat['nom']
            info_pat['pat_fname'] = pat['prenom']

            if method_type not in ('S', 'M', 'W'):
                return (False, "Invalid method type")
            if not method_id or not template_id:
                return (False, "Missing method or model")
            if not recipient:
                return (False, "Missing recipient")

            # Load method + model
            method = Setting.getSendingMethodDet(method_type, int(method_id))
            if not method:
                return (False, "Sending method not found")

            model  = Setting.getSendingModelDet(method_type, int(template_id))
            if not model:
                return (False, "Sending model not found")

            # For S/M we need a protected PDF; for W only if model says it has an attachment.
            need_pdf = (method_type in ('S', 'M'))
            if method_type == 'W':
                need_pdf = ((model.get('mdl_has_attachment') or 'N') == 'Y')

            tmp_path = None
            try:
                if need_pdf:
                    ok_pdf, tmp_path, info = Setting.make_pdf_copy_protected(
                        generated_name=filename,
                        rec_num=rec_num,
                        pat_code=pat_code
                    )
                    if not ok_pdf:
                        # Mark as fail and return
                        cursor = DB.cursor()
                        Setting.update_sending_event_fail(cursor, sde_ser, info or "PDF preparation failed", id_user)
                        return (False, info or "PDF preparation failed")

                # Put event back to queued before sending
                cursor = DB.cursor()
                Setting.update_sending_event_queue(cursor, sde_ser, id_user)

                # Dispatch send
                if method_type == 'S':
                    subject_tpl  = f"{model.get('mdl_displayname') or 'Report'} – dossier"
                    body_txt_tpl = (model.get('mdl_text') or "Veuillez trouver le compte rendu en pièce jointe.") + "\n"

                    subject  = Setting.render_vars(subject_tpl, info_pat)
                    body_txt = Setting.render_vars(body_txt_tpl, info_pat) + "\n"

                    ok, msg  = Setting.sendSmtpWithAttachment(method, recipient, subject, body_txt, tmp_path, filename)

                elif method_type == 'M':
                    subject_tpl   = f"{model.get('mdl_displayname') or 'Report'} – dossier"
                    html_body_tpl = (model.get('mdl_text') or "<p>Veuillez trouver le compte rendu en pièce jointe.</p>")
                    text_body_tpl = "Veuillez trouver le compte rendu en pièce jointe."

                    subject   = Setting.render_vars(subject_tpl, info_pat)
                    html_body = Setting.render_vars(html_body_tpl, info_pat)
                    text_body = Setting.render_vars(text_body_tpl, info_pat)

                    ok, msg   = Setting.sendMailjetWithAttachment(method, recipient, subject, html_body, text_body, tmp_path, filename=filename)

                else:  # 'W'
                    tpl_name = model.get('mdl_name') or ''
                    tpl_lang = (model.get('mdl_lang') or 'fr')
                    ok, msg  = Setting.sendWhatsappTemplate(method, recipient, tpl_name,
                                                            attach_path=(tmp_path if need_pdf else None),
                                                            lang=tpl_lang, template_vars=info_pat, filename=filename)

                # Update same event with result
                if ok:
                    Setting.update_sending_event_success(cursor, sde_ser, id_user)
                else:
                    Setting.update_sending_event_fail(cursor, sde_ser, msg or _("Echec envoi"), id_user)

                return (ok, msg if msg else (_("Réenvoyer") if ok else _("Echec réenvoi")))

            except Exception as e:
                cursor = DB.cursor()
                Setting.update_sending_event_fail(cursor, sde_ser, f"{e}", id_user)
                return (False, f"Send error: {e}")

            finally:
                try:
                    if tmp_path and os.path.exists(tmp_path):
                        os.remove(tmp_path)
                except Exception:
                    pass

        except Exception as e:
            Setting.log.error(Logs.fileline() + f" : ERROR resend err={e}")
            return (False, "Internal error")

    @staticmethod
    def render_vars(tpl: str, ctx: dict) -> str:
        """
        Very small {{ var }} renderer (no logic, just replacements).
        - Unknown keys -> left as-is.
        - None -> replaced by empty string.
        """
        if not tpl:
            return ''
        import re

        def repl(m):
            key = (m.group(1) or '').strip()
            val = ctx.get(key)
            return '' if val is None else str(val)

        # Matches {{ something }}
        return re.sub(r"\{\{\s*(.*?)\s*\}\}", repl, tpl)

    @staticmethod
    def getSettingOauthList():
        cursor = DB.cursor()

        req = ('SELECT oacl_ser, oacl_client_id, oacl_client_secret, oacl_client_name, '
               'oacl_user_id, oacl_redirect_uris, oacl_scope, oacl_grant_types, '
               'oacl_response_types, oacl_token_endpoint_auth_method, oacl_is_active, '
               'oacl_created_at, oacl_updated_at '
               'FROM oauth2_client '
               'ORDER BY oacl_created_at DESC, oacl_ser DESC')

        cursor.execute(req)

        return cursor.fetchall()

    @staticmethod
    def getSettingOauth(id_item):
        cursor = DB.cursor()

        req = ('SELECT * FROM oauth2_client WHERE oacl_ser=%s LIMIT 1')

        cursor.execute(req, (id_item,))

        return cursor.fetchone()

    @staticmethod
    def insertSettingOauth(**params):
        try:
            cursor = DB.cursor()

            cursor.execute(
                'INSERT INTO oauth2_client ('
                ' oacl_client_id, oacl_client_secret, oacl_client_name, oacl_user_id,'
                ' oacl_redirect_uris, oacl_scope, oacl_grant_types, oacl_response_types,'
                ' oacl_token_endpoint_auth_method, oacl_is_active'
                ') VALUES ('
                ' %(oacl_client_id)s, %(oacl_client_secret)s, %(oacl_client_name)s, %(oacl_user_id)s,'
                ' %(oacl_redirect_uris)s, %(oacl_scope)s, %(oacl_grant_types)s, %(oacl_response_types)s,'
                ' %(oacl_token_endpoint_auth_method)s, %(oacl_is_active)s)', params
            )

            Setting.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Setting.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def updateSettingOauth(**params):
        try:
            cursor = DB.cursor()

            cursor.execute(
                'UPDATE oauth2_client SET '
                ' oacl_client_id=%(oacl_client_id)s,'
                ' oacl_client_secret=%(oacl_client_secret)s,'
                ' oacl_client_name=%(oacl_client_name)s,'
                ' oacl_user_id=%(oacl_user_id)s,'
                ' oacl_redirect_uris=%(oacl_redirect_uris)s,'
                ' oacl_scope=%(oacl_scope)s,'
                ' oacl_grant_types=%(oacl_grant_types)s,'
                ' oacl_response_types=%(oacl_response_types)s,'
                ' oacl_token_endpoint_auth_method=%(oacl_token_endpoint_auth_method)s,'
                ' oacl_is_active=%(oacl_is_active)s '
                'WHERE oacl_ser=%(oacl_ser)s AND oacl_client_id <> "labbook-FE"', params
            )

            Setting.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Setting.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def deleteSettingOauth(id_item):
        try:
            cursor = DB.cursor()

            cursor.execute('delete from oauth2_client '
                           'where oacl_ser=%s AND oacl_client_id <> "labbook-FE"', (id_item,))

            Setting.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Setting.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def isAuditTrailEnabled():
        """
        Return True if audit trail is enabled (value = "1"), otherwise False.
        """
        cursor = DB.cursor()
        cursor.execute(
            'SELECT value FROM sigl_06_data WHERE identifiant=%s LIMIT 1',
            ('audit_trail_enabled',)
        )
        row = cursor.fetchone()

        return bool(row and str(row["value"]).strip() == "1")
