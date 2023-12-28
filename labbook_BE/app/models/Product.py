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

        req = ('select samp.id_data, samp.id_owner, samp.samp_date as prod_date, samp.type_prel as prod_type, '
               'samp.samp_id_ana, samp.statut as stat, samp.id_dos as id_rec, samp.preleveur as sampler, '
               'samp.samp_receipt_date as receipt_date, '
               'samp.commentaire as comment, samp.lieu_prel as prod_location, samp.lieu_prel_plus as prod_location_accu, '
               'samp.localisation as storage, samp.code, ana.code as code_ana '
               'from sigl_01_data as samp '
               'left join sigl_05_data as ana on ana.id_data=samp_id_ana '
               'where samp.id_data=%s')

        cursor.execute(req, (id_prod,))

        return cursor.fetchone()

    @staticmethod
    def getProductList(args):
        cursor = DB.cursor()

        table_cond  = ''
        filter_cond = 'prod.type_prel is not NULL '

        if not args:
            limit = 'LIMIT 1000'

            # show only products from non-validated records by default
            filter_cond += ' and rec.statut != 256 '
        else:
            limit = 'LIMIT 15000'

            if 'link_fam' in args and args['link_fam']:
                # avoid redundance of table if filter type_ana exist
                table_cond += (' inner join sigl_04_data as req on req.id_dos=rec.id_data '
                               'inner join sigl_05_data as ref on req.ref_analyse = ref.id_data ')

                cond_link_fam = ''
                # prepare list for sql
                for id_fam in args['link_fam']:
                    if not cond_link_fam:
                        cond_link_fam = '('

                    cond_link_fam = cond_link_fam + str(id_fam) + ','

                if cond_link_fam:
                    cond_link_fam = cond_link_fam[:-1] + ')'
                    filter_cond += ' and ref.famille in ' + cond_link_fam + ' '

        # take lastest product of blood, stool, urine and other for each record
        req = ('select if(param_num_rec.periode=1070, if(param_num_rec.format=1072,substring(rec.num_dos_mois from 7), rec.num_dos_mois), '
               'if(param_num_rec.format=1072, substring(rec.num_dos_an from 7), rec.num_dos_an)) as rec_num, '
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
               'left join sigl_param_num_dos_data as param_num_rec on param_num_rec.id_data=1 ' + table_cond +
               'where ' + filter_cond +
               'group by prod.id_dos order by rec.num_dos_an desc ' + limit)

        # Product.log.info(Logs.fileline() + ' : DEBUG-TRACE req = ' + str(req))

        cursor.execute(req, (Constants.cst_isodate,))

        return cursor.fetchall()

    @staticmethod
    def getProductReq(id_rec):
        cursor = DB.cursor()

        req = ('select prod.id_data as id_data, prod.id_owner as id_owner, prod.samp_date, prod.type_prel as type_prel, '
               'ana.code as code_ana, prod.statut as statut, prod.id_dos as id_dos, prod.preleveur as preleveur, '
               'prod.samp_receipt_date, prod.commentaire as commentaire, '
               'prod.lieu_prel as lieu_prel, prod.lieu_prel_plus as lieu_prel_plus, prod.localisation as localisation, '
               'dico_type.label as type_prod, dico_stat.label as stat_prod, prod.code, dico_local.label as location '
               'from sigl_01_data as prod '
               'left join sigl_dico_data AS dico_type ON dico_type.id_data=prod.type_prel '
               'left join sigl_dico_data AS dico_stat ON dico_stat.id_data=prod.statut '
               'left join sigl_dico_data as dico_local on dico_local.id_data=prod.lieu_prel '
               'left join sigl_05_data as ana on ana.id_data=prod.samp_id_ana '
               'where prod.id_dos=%s')

        cursor.execute(req, (id_rec,))

        return cursor.fetchall()

    @staticmethod
    def insertProductReq(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into sigl_01_data '
                           '(id_owner, samp_date, type_prel, samp_id_ana, statut, id_dos, preleveur, samp_receipt_date, '
                           'commentaire, lieu_prel, lieu_prel_plus, localisation, code) '
                           'values '
                           '(%(id_owner)s, %(samp_date)s, %(type_prel)s, %(samp_id_ana)s, %(statut)s, %(id_dos)s, %(preleveur)s, '
                           ' %(samp_receipt_date)s, %(commentaire)s, %(lieu_prel)s, %(lieu_prel_plus)s, %(localisation)s, '
                           '%(code)s)', params)

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
                           'set samp_date=%(samp_date)s, type_prel=%(type_prel)s, samp_id_ana=%(samp_id_ana)s, '
                           'statut=%(statut)s, id_dos=%(id_dos)s, preleveur=%(preleveur)s, '
                           'samp_receipt_date=%(samp_receipt_date)s, '
                           'commentaire=%(commentaire)s, lieu_prel=%(lieu_prel)s, '
                           'lieu_prel_plus=%(lieu_prel_plus)s, localisation=%(localisation)s, code=%(code)s '
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
                               '(id_data, id_owner, samp_date, type_prel, samp_id_ana, statut, id_dos, preleveur, samp_receipt_date, '
                               'commentaire, lieu_prel, lieu_prel_plus, localisation, code) '
                               'select id_data, id_owner, samp_date, type_prel, samp_id_ana, statut, id_dos, preleveur, samp_receipt_date, '
                               'commentaire, lieu_prel, lieu_prel_plus, localisation, code '
                               'from sigl_01_data '
                               'where id_data=%s', (product['id_data'],))

                cursor.execute('delete from sigl_01_data '
                               'where id_data=%s', (product['id_data'],))

            Product.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Product.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False
