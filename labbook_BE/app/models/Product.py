# -*- coding:utf-8 -*-
import logging
import mysql.connector

from app.models.Constants import Constants
from app.models.DB import DB
from app.models.Logs import Logs


class Product:
    log = logging.getLogger('log_db')

    @staticmethod
    def getProductDet(id_prod):
        """
        Read one sample of sigl_01_data with the code of its analysis.
        """
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
    def getOrderDetForLab27(id_prod):
        """
        Read a sample with its record, analysis and patient for a LAB-27 answer.
        Despite its name, id_prod is compared with the sample code, not its id.
        """
        cursor = DB.cursor()

        req = ("""
               SELECT samp.id_data as id_samp, samp.code as code, samp.samp_date, d1.label as type_samp,
               rec.num_dos_an as num_record, ana.code as ana_code, ana.nom as ana_name, ana.ana_loinc,
               pat.code as pat_code, pat.nom as pat_name, pat.prenom as pat_firstname, pat.nom_jf as pat_maiden,
               pat.ddn as pat_birth, pat.sexe as pat_sex, pat.adresse as pat_address, pat.ville as pat_city,
               pat.cp as pat_zip, pat.tel as pat_phone1, pat.pat_email
               from sigl_01_data samp
               left join sigl_dico_data d1 on d1.id_data = samp.type_prel
               left join sigl_02_data rec on rec.id_data = samp.id_dos
               left join  sigl_03_data pat on pat.id_data = rec.id_patient
               left join sigl_05_data ana on ana.id_data = samp.samp_id_ana
               where samp.code = %s;
               """)

        cursor.execute(req, (id_prod,))

        return cursor.fetchone()

    @staticmethod
    def getOrdersForLab27():
        """
        Retrieve all valid sample orders eligible for LAB-27 response (RSP^K11).

        Includes:
        - samples with non-empty code
        - active associated analysis
        - records with statut 182 or 253
        """
        try:
            cursor = DB.cursor()

            req = (
                "select "
                "samp.id_data as id_data, samp.code as code, samp.samp_date, "
                "d1.label as type_samp, rec.id_data as id_rec, "
                "ana.code as ana_code, ana.nom as ana_name, ana.ana_loinc, "
                "pat.code as pat_code, pat.nom as pat_name, pat.prenom as pat_firstname, "
                "pat.ddn as pat_birth, pat.sexe as pat_sex "
                "from sigl_01_data samp "
                "left join sigl_dico_data d1 on d1.id_data = samp.type_prel "
                "left join sigl_02_data rec on rec.id_data = samp.id_dos "
                "left join sigl_03_data pat on pat.id_data = rec.id_patient "
                "left join sigl_05_data ana on ana.id_data = samp.samp_id_ana "
                "where samp.code is not null and samp.code != '' "
                "and samp.samp_id_ana > 0 and ana.actif = 4 and rec.statut in (182, 253) "
                "order by samp.samp_date desc"
            )

            cursor.execute(req)
            return cursor.fetchall()

        except Exception as e:
            Product.log.error(Logs.fileline() + f" : error in getOrdersForLab27: {str(e)}")
            return []

    @staticmethod
    def getProductList(args):
        """
        Read the samples with their record and patient. With an empty args, only samples of records
        not yet biologically validated, limited to 1000, otherwise limited to 15000.
        args: link_fam, family ids joined into the SQL text without parameters.
        """
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
                cond_link_fam = ','.join(str(id_fam) for id_fam in args['link_fam'])
                if cond_link_fam:
                    filter_cond += f' and ref.famille in ({cond_link_fam}) '

        req = '''
              SELECT DISTINCT
              IF(rec_setting.rstg_period=1070,
              IF(rec_setting.rstg_format=1072, SUBSTRING(rec.num_dos_mois FROM 7), rec.num_dos_mois),
              IF(rec_setting.rstg_format=1072, SUBSTRING(rec.num_dos_an FROM 7), rec.num_dos_an)) AS rec_num,
              DATE_FORMAT(rec.rec_date_receipt, %s) AS rec_date,
              pat.nom AS lastname, pat.nom_jf AS maidenname, pat.prenom AS firstname,
              ana.nom AS analysis_name, prod.type_prel AS type_prel, prod.statut AS statut, prod.id_data AS id_prod,
              rec.id_data AS id_rec, dico.label AS type_prel_label, prod.code as samp_code
              FROM sigl_01_data AS prod
              inner join sigl_02_data AS rec ON prod.id_dos = rec.id_data
              inner join sigl_03_data AS pat ON rec.id_patient = pat.id_data
              inner join record_setting AS rec_setting ON rec_setting.rstg_ser = 1
              LEFT JOIN sigl_05_data AS ana ON prod.samp_id_ana = ana.id_data
              inner join sigl_04_data AS req ON prod.samp_id_ana = req.ref_analyse
              inner join sigl_05_data AS ref ON req.ref_analyse = ref.id_data
              left join sigl_dico_data AS dico ON prod.type_prel = dico.id_data
              {table_cond}
              WHERE {filter_cond}
              ORDER BY rec.num_dos_an DESC
              {limit}
              '''

        req = req.format(table_cond=table_cond, filter_cond=filter_cond, limit=limit)

        # Product.log.info(Logs.fileline() + ' : DEBUG-TRACE req = ' + str(req))

        cursor.execute(req, (Constants.cst_isodate,))

        return cursor.fetchall()

    @staticmethod
    def getProductReq(id_rec):
        """
        Read the samples of a record with the labels of their type, status and sampling place.
        """
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
        """
        Insert a sample in sigl_01_data.

        Returns:
            int: new id, 0 on SQL error.
        """
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
        """
        Update a sample of sigl_01_data.

        Returns:
            bool: True on success, False on SQL error.
        """
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
        """
        Move the samples of a record to sigl_01_deleted.

        Returns:
            bool: True on success, False on SQL error.
        """
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

    @staticmethod
    def resolveProductId(specimen_id):
        """
        Try to resolve specimen_id as a numeric primary key (id_data).
        If not found, fallback to search by code (string).
        Returns the corresponding id_data or 0 if not found.
        """
        cursor = DB.cursor()

        # First attempt: check if specimen_id is a numeric id_data
        if str(specimen_id).isdigit():
            cursor.execute('select id_data from sigl_01_data where id_data = %s', (int(specimen_id),))
            row = cursor.fetchone()
            if row:
                return row['id_data']

        # Second attempt: check if specimen_id matches the 'code' field
        cursor.execute('''
            select id_data from sigl_01_data where code = %s
            order by samp_date DESC, id_data desc limit 1
            ''', (specimen_id,))
        row = cursor.fetchone()
        if row:
            return row['id_data']

        # Not found
        return 0

    @staticmethod
    def getSampleIdsByRecordVar(id_rec, id_samp=0):
        """
        Map code_var -> id_data of the sample whose analysis holds this variable, for one record.
        The sample id_samp comes first, so it keeps the variables of its own analysis.
        """
        cursor = DB.cursor()

        cursor.execute('select ref_var.code_var, samp.id_data from sigl_01_data as samp '
                       'inner join sigl_05_07_data as var_pos on var_pos.id_refanalyse = samp.samp_id_ana '
                       'inner join sigl_07_data as ref_var on ref_var.id_data = var_pos.id_refvariable '
                       'where samp.id_dos = %s '
                       'order by samp.id_data = %s desc, samp.id_data asc limit 1000', (id_rec, id_samp))

        # First sample wins when a variable appears in several analyses
        samples = {}
        for row in cursor.fetchall():
            samples.setdefault(row['code_var'], row['id_data'])

        return samples

    @staticmethod
    def getLastSampleCode(samp_regex):
        """
        Read the last sample code matching samp_regex, used to prefill the next code.

        Returns:
            str: code, empty when samp_regex is empty, nothing matches or on SQL error.
        """
        try:
            samp_regex = (samp_regex or '').strip()
            if not samp_regex:
                Product.log.info(Logs.fileline() + ' : getLastSampleCode empty regex')
                return ''

            cursor = DB.cursor()
            cursor.execute(
                'select code '
                'from sigl_01_data '
                'where code is not null and code != "" '
                'and code regexp %s '
                'order by id_data desc '
                'limit 1',
                (samp_regex,)
            )

            row = cursor.fetchone()

            if not row:
                return ''

            code = row.get('code') if isinstance(row, dict) else row[0]
            return code or ''

        except mysql.connector.Error as err:
            Product.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(err))
            return ''

    @staticmethod
    def getExistingSampleCodes(codes):
        """
        Tell which of these sample codes are already used.

        Returns:
            list: codes found, empty on SQL error.
        """
        if not codes:
            return []

        try:
            cursor = DB.cursor()
            placeholders = ','.join(['%s'] * len(codes))

            cursor.execute(
                'select distinct code '
                'from sigl_01_data '
                'where code in (' + placeholders + ')',
                codes
            )

            rows = cursor.fetchall()
            Product.log.info(Logs.fileline() + ' : Product.getExistingSampleCodes')

            existing = []

            for row in rows:
                if isinstance(row, dict):
                    val = row.get('code')
                else:
                    val = row[0]
                if val:
                    existing.append(val)

            return existing

        except mysql.connector.Error as e:
            Product.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return []
