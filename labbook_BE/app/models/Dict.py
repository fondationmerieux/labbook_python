# -*- coding:utf-8 -*-
import logging
import mysql.connector

from flask import session

from app.models.DB import DB
from app.models.Logs import Logs


class Dict:
    log = logging.getLogger('log_db')

    @staticmethod
    def getDictValue(id_value):
        cursor = DB.cursor()

        req = ('select id_data, id_owner, dico_name, label, short_label, position, code, dico_descr '
               'from sigl_dico_data '
               'where id_data = %s')

        cursor.execute(req, (id_value,))

        return cursor.fetchall()

    @staticmethod
    def deleteDictValue(id_value):
        try:
            cursor = DB.cursor()

            cursor.execute('delete from sigl_dico_data '
                           'where id_data=%s', (id_value,))

            Dict.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Dict.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getDictDetails(dict_name):
        cursor = DB.cursor()

        req = ('select id_data, id_owner, dico_name, label, short_label, position, code, dico_descr, dict_formatting '
               'from sigl_dico_data '
               'where dico_name = %s '
               'order by position')

        cursor.execute(req, (dict_name,))

        return cursor.fetchall()

    @staticmethod
    def getDictDetailsById(id_dict):
        cursor = DB.cursor()

        req = ('select id_data, id_owner, dico_name, label, short_label, position, code, dico_descr, dict_formatting '
               'from sigl_dico_data '
               'where dico_name = (select SUBSTRING_INDEX(short_label, "_", -1) AS dico_name '
               'from sigl_dico_data where id_data=%s) '
               'order by position')

        cursor.execute(req, (id_dict,))

        return cursor.fetchall()

    @staticmethod
    def insertDict(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into sigl_dico_data '
                           '(id_owner, dico_name, label, short_label, position, code, dict_formatting) '
                           'values (%(id_owner)s, %(dico_name)s, %(label)s, %(short_label)s, '
                           '%(position)s, %(code)s, %(dict_formatting)s)', params)

            Dict.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Dict.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def updateDict(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('update sigl_dico_data '
                           'set label=%(label)s, short_label=%(short_label)s, position=%(position)s, '
                           'code=%(code)s, dict_formatting=%(dict_formatting)s '
                           'where id_data=%(id_data)s', params)

            Dict.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Dict.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def deleteDict(dict_name):
        try:
            cursor = DB.cursor()

            cursor.execute('delete from sigl_dico_data '
                           'where dico_name=%s', (dict_name,))

            Dict.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Dict.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def updateDescr(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('update sigl_dico_data '
                           'set dico_descr=%(dico_descr)s '
                           'where dico_name=%(dict_name)s', params)

            Dict.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Dict.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def exist(dico_name):
        try:
            cursor = DB.cursor()

            cursor.execute('select count(*) as nb_dico_name '
                           'from sigl_dico_data '
                           'where dico_name=%s', (dico_name,))

            ret = cursor.fetchone()

            if ret and ret['nb_dico_name'] == 0:
                return False
            else:
                return True
        except mysql.connector.Error as e:
            Dict.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return -1

    @staticmethod
    def getDictList(args):
        cursor = DB.cursor()

        filter_cond = ''
        trans       = ''

        if not args:
            limit = 'LIMIT 2000'

            filter_cond += ' id_data > 0 '  # remove deleted dicts by default
        else:
            limit = 'LIMIT 2000'

            filter_cond += ' id_data > 0 '  # remove deleted dicts by default

            if session['lang_db'] == 'fr_FR':
                if 'name' in args and args['name']:
                    filter_cond += ' and dico_name LIKE "%' + str(args['name']) + '%" '

                if 'label' in args and args['label']:
                    filter_cond += ' and label LIKE "%' + str(args['label']) + '%" '
            else:
                if 'name' in args and args['name']:
                    trans = ('left join translations as tr on tr.tra_lang="' + str(session['lang_db']) + '" and '
                             'tr.tra_type="dict_name" and tr.tra_ref=id_data ')

                    filter_cond += (' and (tr.tra_text LIKE "%' + str(args['name']) + '%" or '
                                    ' dico_name LIKE "%' + str(args['name']) + '%") ')

                if 'label' in args and args['label']:
                    trans = ('left join translations as tr on tr.tra_lang="' + str(session['lang_db']) + '" and '
                             'tr.tra_type="dict_label" and tr.tra_ref=id_data ')

                    filter_cond += (' and tr.tra_text LIKE "%' + str(args['label']) + '%" or '
                                    ' label LIKE "%' + str(args['name']) + '%") ')

            if 'code' in args and args['code']:
                filter_cond += ' and code LIKE "%' + str(args['code']) + '%" '

        req = ('select id_data, dico_name as name, dico_descr '
               'from sigl_dico_data ' + trans +
               'where ' + filter_cond +
               'group by dico_name order by dico_name asc ' + limit)

        cursor.execute(req)

        return cursor.fetchall()

    @staticmethod
    def getDictExport(dico_name):
        cursor = DB.cursor()

        cond = ''

        if dico_name:
            cond = ' where dico_name="' + str(dico_name) + '"'

        req = ('select id_data, id_owner, dico_name, label, short_label, position, code, dico_descr, dict_formatting '
               'from sigl_dico_data ' + cond + ' order by dico_name')

        cursor.execute(req)

        return cursor.fetchall()
