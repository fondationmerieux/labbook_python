# -*- coding:utf-8 -*-
import logging
import mysql.connector

# from app.models.Constants import *
from app.models.DB import DB
from app.models.Logs import Logs


class Product:
    log = logging.getLogger('log_db')

    @staticmethod
    def getProductReq(id_rec):
        cursor = DB.cursor()

        req = 'select prod.id_data as id_data, prod.id_owner as id_owner, prod.date_prel as date_prel, prod.type_prel as type_prel, '\
              'prod.quantite as quantite, prod.statut as statut, prod.id_dos as id_dos, prod.preleveur as preleveur, '\
              'prod.date_reception as date_reception, prod.heure_reception as heure_reception, prod.commentaire as commentaire, '\
              'prod.lieu_prel as lieu_prel, prod.lieu_prel_plus as lieu_prel_plus, prod.localisation as localisation, '\
              'dico_type.label as type_prod, dico_stat.label as stat_prod '\
              'from sigl_01_data as prod '\
              'LEFT JOIN sigl_dico_data AS dico_type ON dico_type.dico_name="type_prel" '\
              'LEFT JOIN sigl_dico_data AS dico_stat ON dico_stat.dico_name="prel_statut" '\
              'where dico_type.id_data=type_prel and dico_stat.id_data=statut and prod.id_dos=%s'

        cursor.execute(req, (id_rec,))

        return cursor.fetchall()

    @staticmethod
    def insertProductReq(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into sigl_01_data '
                           '(id_owner, date_prel, type_prel, quantite, statut, id_dos, preleveur, date_reception, '
                           'heure_reception, commentaire, lieu_prel, lieu_prel_plus, localisation) '
                           'values '
                           '(%(id_owner)s, %(date_prel)s, %(type_prel)s, %(quantite)s, %(statut)s, %(id_dos)s, %(preleveur)s, %(date_reception)s, '
                           '%(heure_reception)s, %(commentaire)s, %(lieu_prel)s, %(lieu_prel_plus)s, %(localisation)s)', params)

            Product.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Product.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def insertProductReqGroup(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into sigl_01_data_group '
                           '(id_data, id_group) '
                           'values '
                           '(%(id_data)s, %(id_group)s )', params)

            Product.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Product.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def deleteProductByRecord(id_rec):
        try:
            cursor = DB.cursor()

            cursor.execute('select id_data '
                           'from sigl_01_data '
                           'where id_dos=%s', (id_rec,))

            l_product = cursor.fetchall()

            for product in l_product:
                cursor.execute('insert into sigl_01_deleted '
                               '(id_data, id_owner, date_prel, type_prel, quantite, statut, id_dos, preleveur, date_reception, heure_reception, '
                               'commentaire, lieu_prel, lieu_prel_plus, localisation) '
                               'select id_data, id_owner, date_prel, type_prel, quantite, statut, id_dos, preleveur, date_reception, heure_reception, '
                               'commentaire, lieu_prel, lieu_prel_plus, localisation '
                               'from sigl_01_data '
                               'where id_data=%s', (product['id_data'],))

                cursor.execute('delete from sigl_01_data_group_mode '
                               'where id_data_group=%s', (product['id_data'],))

                cursor.execute('delete from sigl_01_data_group '
                               'where id_data=%s', (product['id_data'],))

                cursor.execute('delete from sigl_01_data '
                               'where id_data=%s', (product['id_data'],))

            Product.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Product.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False
