# -*- coding:utf-8 -*-
# import informixdb
import mysql.connector
import logging
import re

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
            DB.open_cnx()
            try:
                cursor = DB.cnx.cursor(dictionary=True)
            except mysql.connector.Error as e:
                DB.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
                DB.cnx = None
                cursor = DB.open_cnx().cursor(dictionary=True)

        return cursor

    @staticmethod
    def open_cnx():
        try:
            if DB.cnx is None:
                # read default_settings.py
                # file_path = '/home/apps/labbook_BE/labbook_BE/default_settings.py'
                # desact 14/05/2024 return to use current_app : config_data = DB.read_config_file(file_path)

                if current_app.config['DB_TYPE'] == 'MYSQL':
                    DB.log.info(Logs.fileline() + ' : open_cnx() TRACE connect MYSQL')
                    DB.cnx = mysql.connector.connect(user=current_app.config['DB_USER'],
                                                     password=current_app.config['DB_PWD'],
                                                     host=current_app.config['DB_HOST'],
                                                     database=current_app.config['DB_NAME'])
                    DB.cnx.autocommit = True
                else:
                    DB.log.critical(Logs.fileline() + ' : open_cnx() error DB_TYPE = %s', current_app.config['DB_TYPE'])

            return DB.cnx

        except Exception as e:
            DB.log.critical(Logs.fileline() + ' : open_cnx() error: %s ', e)
            raise DBException(repr(e))

    @staticmethod
    def insertDbStatus(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into database_status '
                           '(dbs_date, dbs_stat, dbs_type) '
                           'values '
                           '(NOW(), %(stat)s, %(type)s)', params)

            DB.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            DB.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def getLastStatus(type):
        cursor = DB.cursor()

        cursor.execute('select dbs_date, dbs_stat, dbs_type '
                       'from database_status '
                       'where dbs_type=%s '
                       'order by dbs_date desc limit 1', (type,))

        return cursor.fetchone()

    @staticmethod
    def read_config_file(file_path):
        config = {}

        with open(file_path, 'r') as file:
            content = file.read()

            matches = re.findall(r'(\w+)\s*=\s*([\'"])(.*?)\2', content)

            for match in matches:
                key, _, value = match
                config[key] = value

        return config
