# -*- coding:utf-8 -*-
import logging
import mysql.connector

from app.models.Constants import *
from app.models.DB import DB
from app.models.Logs import Logs


class Product:
    log = logging.getLogger('log_db')

    @staticmethod
    def getProductDet(id_prod):
        cursor = DB.cursor()

        req = ('select id_data, id_owner, date_prel as prod_date, type_prel as prod_type, '
               'quantite as qty, statut as stat, id_dos as id_rec, preleveur as sampler, '
               'date_reception as receipt_date, time_format(heure_reception, "%T") as receipt_time, '
               'commentaire as comment, lieu_prel as prod_location, lieu_prel_plus as prod_location_accu, '
               'localisation as storage '
               'from sigl_01_data '
               'where id_data=%s')

        cursor.execute(req, (id_prod,))

        return cursor.fetchone()

    @staticmethod
    def getProductList(args):
        cursor = DB.cursor()

        filter_cond = 'type_prel is not NULL '

        if not args:
            limit = 'LIMIT 1000'

            # show only products from non-validated records by default
            filter_cond += ' and rec.statut != 256 '
        else:
            limit = 'LIMIT 15000'

        # take lastest product of blood, stool, urine and other for each record
        req = ('select if(param_num_dos.periode=1070, if(param_num_dos.format=1072,substring(rec.num_dos_mois from 7), rec.num_dos_mois), '
               'if(param_num_dos.format=1072, substring(rec.num_dos_an from 7), rec.num_dos_an)) as rec_num, '
               'date_format(rec.date_dos, %s) as rec_date, '
               'pat.nom as lastname, pat.nom_jf as maidenname, pat.prenom as firstname, '
               'MAX(CASE when (prod.type_prel in (78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 127, 138, 142) and prod.statut in (8, 9, 10)) '
               'then prod.id_data END) as id_prod_blood, '
               'MAX(CASE when (prod.type_prel = 141 and prod.statut IN (8, 9, 10)) then prod.id_data END) as id_prod_stool, '
               'MAX(CASE when (prod.type_prel in (153, 154, 155, 156, 157, 158, 159, 160, 161) and prod.statut in (9,10)) '
               'then prod.id_data END) as id_prod_urine, '
               'MAX(CASE when (prod.type_prel not in (78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 127, 138, 142, 141, 153, 154, 155, 156, 157, 158, 159, 160, 161) '
               'and prod.statut in (9,10)) then prod.id_data END) as id_prod_other, '
               'MAX(CASE when (prod.type_prel in (78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 127, 138, 142)) then prod.statut END) as stat_blood, '
               'MAX(CASE when (prod.type_prel = 141) then prod.statut END) as stat_stool, '
               'MAX(CASE when (prod.type_prel in (153, 154, 155, 156, 157, 158, 159, 160, 161)) then prod.statut END) as stat_urine, '
               'MAX(CASE when (prod.type_prel not in (78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 127, 138, 142, 141, 153, 154, 155, 156, 157, 158, 159, 160, 161)) '
               'then prod.statut END) as stat_other, '
               'prod.id_dos as id_rec '
               'from sigl_01_data as prod '
               'inner join sigl_02_data as rec on prod.id_dos=rec.id_data '
               'inner join sigl_03_data as pat on rec.id_patient=pat.id_data '
               'left join sigl_param_num_dos_data as param_num_dos on param_num_dos.id_data=1 '
               'where ' + filter_cond +
               'group by prod.id_dos order by rec.num_dos_an desc ' + limit)

        cursor.execute(req, (Constants.cst_isodate,))

        return cursor.fetchall()

    @staticmethod
    def getProductReq(id_rec):
        cursor = DB.cursor()

        req = ('select prod.id_data as id_data, prod.id_owner as id_owner, prod.date_prel as date_prel, prod.type_prel as type_prel, '
               'prod.quantite as quantite, prod.statut as statut, prod.id_dos as id_dos, prod.preleveur as preleveur, '
               'prod.date_reception as date_reception, prod.heure_reception as heure_reception, prod.commentaire as commentaire, '
               'prod.lieu_prel as lieu_prel, prod.lieu_prel_plus as lieu_prel_plus, prod.localisation as localisation, '
               'dico_type.label as type_prod, dico_stat.label as stat_prod '
               'from sigl_01_data as prod '
               'LEFT JOIN sigl_dico_data AS dico_type ON dico_type.dico_name="type_prel" '
               'LEFT JOIN sigl_dico_data AS dico_stat ON dico_stat.dico_name="prel_statut" '
               'where dico_type.id_data=type_prel and dico_stat.id_data=statut and prod.id_dos=%s')

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
    def updateProduct(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('update sigl_01_data '
                           'set date_prel=%(date_prel)s, type_prel=%(type_prel)s, quantite=%(quantite)s, '
                           'statut=%(statut)s, id_dos=%(id_dos)s, preleveur=%(preleveur)s, '
                           'date_reception=%(date_reception)s, heure_reception=%(heure_reception)s, '
                           'commentaire=%(commentaire)s, lieu_prel=%(lieu_prel)s, '
                           'lieu_prel_plus=%(lieu_prel_plus)s, localisation=%(localisation)s '
                           'where id_data=%(id_data)s', params)

            Product.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Product.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

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

                cursor.execute('delete from sigl_01_data '
                               'where id_data=%s', (product['id_data'],))

            Product.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Product.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False
