# -*- coding:utf-8 -*-
# import informixdb
import mysql.connector
import logging

from flask import current_app
from app.exception.DBException import DBException
from app.models.Logs import Logs


class DB:
    log = logging.getLogger('log_services')
    cnx = None

    @staticmethod
    def cursor(ecr=False):
        if ecr is True:
            cursor = DB.open_cnx().cursor()
        else:
            if current_app.config['DB_TYPE'] == 'MYSQL':
                # DB.log.info(Logs.fileline() + ' : cursor() MYSQL')
                DB.open_cnx()
                try:
                    cursor = DB.cnx.cursor(dictionary=True)
                except mysql.connector.Error as e:
                    DB.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
                    DB.cnx = None
                    cursor = DB.open_cnx().cursor(dictionary=True)

            elif current_app.config['DB_TYPE'] == 'IFX':
                # cursor = DB.open_cnx().cursor(rowformat = informixdb.ROW_AS_DICT)
                DB.log.critical(Logs.fileline() + ' : cursor() error TODO IFX')
            else:
                DB.log.critical(Logs.fileline() + ' : cursor() error DB_TYPE = %s', current_app.config['DB_TYPE'])

        return cursor

    @staticmethod
    def open_cnx():
        try:
            if DB.cnx is None:
                if current_app.config['DB_TYPE'] == 'MYSQL':
                    DB.log.info(Logs.fileline() + ' : open_cnx() TRACE connect MYSQL')
                    DB.cnx = mysql.connector.connect(user=current_app.config['DB_USER'],
                                                     password=current_app.config['DB_PWD'],
                                                     host=current_app.config['DB_HOST'],
                                                     database=current_app.config['DB_NAME'])
                    DB.cnx.autocommit = True
                elif current_app.config['DB_TYPE'] == 'IFX':
                    DB.log.critical(Logs.fileline() + ' : cursor() error TODO')
                    '''DB.cnx = informixdb.connect(current_app.config.DB_NAME,
                                                   current_app.config.DB_USER,
                                                   current_app.config.DB_PWD)
                    DB.cnx.autocommit = True'''
                else:
                    DB.log.critical(Logs.fileline() + ' : open_cnx() error DB_TYPE = %s', current_app.config.DB_TYPE)

            return DB.cnx

        except Exception as e:
            DB.log.critical(Logs.fileline() + ' : open_cnx() error: %s %s', e.errno, e)
            raise DBException(repr(e))

    @staticmethod
    def insertDbStatus(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into database_status '
                           '(dbs_date, dbs_stat) '
                           'values '
                           '(NOW(), %(stat)s)', params)

            DB.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            DB.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def getLastStatus():
        cursor = DB.cursor()

        cursor.execute('select dbs_date, dbs_stat '
                       'from database_status '
                       'order by dbs_date desc limit 1')

        return cursor.fetchone()
