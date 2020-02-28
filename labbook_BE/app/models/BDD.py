# -*- coding:utf-8 -*-
# import informixdb
import mysql.connector
import logging

from app.Config import Config
from app.exception.DBException import DBException
from app.models.Logs import Logs


class BDD:
    log = logging.getLogger('log_service')
    cnx = None

    @staticmethod
    def cursor(ecr=False):
        if ecr is True:
            cursor = BDD.ouvre_cnx().cursor()
        else:
            if Config.BDD_TYPE == 'MYSQL':
                BDD.log.info(Logs.fileline() + ' : cursor() MYSQL')
                BDD.ouvre_cnx()
                try:
                    cursor = BDD.cnx.cursor(dictionary=True)
                except mysql.connector.Error as e:
                    BDD.log.error(Logs.fileline() + ' : ERROR SQL ' + str(e.errno))
                    BDD.cnx = None
                    cursor = BDD.ouvre_cnx().cursor(dictionary=True)

            elif Config.BDD_TYPE == 'IFX':
                # cursor = BDD.ouvre_cnx().cursor(rowformat = informixdb.ROW_AS_DICT)
                BDD.log.critical(Logs.fileline() + ' : cursor() erreur TODO IFX')
            else:
                BDD.log.critical(Logs.fileline() + ' : cursor() erreur BDD_TYPE = %s', Config.BDD_TYPE)

        return cursor

    @staticmethod
    def ouvre_cnx():
        try:
            if BDD.cnx is None:
                if Config.BDD_TYPE == 'MYSQL':
                    BDD.log.info(Logs.fileline() + ' : ouvre_cnx() TRACE connect MYSQL')
                    BDD.cnx = mysql.connector.connect(user=Config.BDD_UTIL,
                                                      password=Config.BDD_MDP,
                                                      host=Config.BDD_HOST,
                                                      database=Config.BDD_NOM)
                    BDD.cnx.autocommit = True
                elif Config.BDD_TYPE == 'IFX':
                    BDD.log.critical(Logs.fileline() + ' : cursor() erreur TODO')
                    '''BDD.cnx = informixdb.connect(Config.BDD_NOM,
                                                 Config.BDD_UTIL,
                                                 Config.BDD_MDP)
                    BDD.cnx.autocommit = True'''
                else:
                    BDD.log.critical(Logs.fileline() + ' : ouvre_cnx() erreur BDD_TYPE = %s', Config.BDD_TYPE)

            return BDD.cnx

        except Exception as e:
            BDD.log.critical(Logs.fileline() + ' : ouvre_cnx() erreur: %s %s', e.errno, e)
            raise DBException(repr(e))
