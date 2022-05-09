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

        req = ('select id_data, id_owner, dico_name, label, short_label, position, code, archived, dico_descr '
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

        req = ('select id_data, id_owner, dico_name, label, short_label, position, code, archived, dico_descr '
               'from sigl_dico_data '
               'where dico_name = %s '
               'order by position')

        cursor.execute(req, (dict_name,))

        return cursor.fetchall()

    @staticmethod
    def insertDict(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into sigl_dico_data '
                           '(id_owner, dico_name, label, short_label, position, code, archived) '
                           'values (%(id_owner)s, %(dico_name)s, %(label)s, %(short_label)s, '
                           '%(position)s, %(code)s, 0)', params)

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
                           'code=%(code)s, archived=%(archived)s '
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
    def getDictList(args):
        cursor = DB.cursor()

        filter_cond = ''
        trans       = ''

        if not args:
            limit = 'LIMIT 2000'

            filter_cond += ' (archived=0 or archived is NULL) '  # remove deleted dicts by default
        else:
            limit = 'LIMIT 2000'

            filter_cond += ' (archived=0 or archived is NULL) '  # remove deleted dicts by default

            if session['lang_db'] == 'fr_FR':
                if args['name']:
                    filter_cond += ' and dico_name LIKE "%' + str(args['name']) + '%" '

                if args['label']:
                    filter_cond += ' and label LIKE "%' + str(args['label']) + '%" '
            else:
                if args['name']:
                    trans = ('left join translations as tr on tr.tra_lang="' + str(session['lang_db']) + '" and '
                             'tr.tra_type="dict_name" and tr.tra_ref=id_data ')

                    filter_cond += (' and (tr.tra_text LIKE "%' + str(args['name']) + '%" or '
                                    ' dico_name LIKE "%' + str(args['name']) + '%") ')

                if args['label']:
                    trans = ('left join translations as tr on tr.tra_lang="' + str(session['lang_db']) + '" and '
                             'tr.tra_type="dict_label" and tr.tra_ref=id_data ')

                    filter_cond += (' and tr.tra_text LIKE "%' + str(args['label']) + '%" or '
                                    ' label LIKE "%' + str(args['name']) + '%") ')

            if args['code']:
                filter_cond += ' and code LIKE "%' + str(args['code']) + '%" '

        req = ('select id_data, dico_name as name, dico_descr '
               'from sigl_dico_data ' + trans +
               'where ' + filter_cond +
               'group by dico_name order by dico_name asc ' + limit)

        cursor.execute(req)

        return cursor.fetchall()
