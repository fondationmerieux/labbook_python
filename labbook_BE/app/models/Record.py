# -*- coding:utf-8 -*-
import logging
import mysql.connector

from app.models.Constants import Constants
from app.models.DB import DB
from app.models.General import *
from app.models.Logs import Logs


class Record:
    log = logging.getLogger('log_db')

    @staticmethod
    def getRecordList(args, id_pres):
        cursor = DB.cursor()

        table_cond  = ''
        filter_cond = 'length(rec.num_dos_an) = 10 '
        params = [Constants.cst_dt_HM_SQL]

        if not args:
            limit = 'LIMIT 1000'
        else:
            limit = 'LIMIT 4000'
            # filter conditions
            if 'num_rec' in args and args['num_rec']:
                filter_cond += (' and (rec.num_dos_an LIKE %s or rec.num_dos_mois LIKE %s or rec.rec_num_int LIKE %s or rec.rec_num_lite LIKE %s) ')
                params.extend(['%' + args['num_rec'] + '%'] * 4)  # Adding num_rec value for all 3 LIKE conditions

            if 'stat_work' in args and args['stat_work']:
                raw = str(args['stat_work'])
                values = [int(val.strip()) for val in raw.split(',') if val.strip().isdigit()]
                if values:
                    placeholders = ','.join(['%s'] * len(values))
                    filter_cond += f' and rec.statut IN ({placeholders}) '
                    params.extend(values)  # Convert list to string for SQL

            if 'type_rec' in args and args['type_rec']:
                if args['type_rec'] == 'C':
                    filter_cond += ' and rec.rec_custody="Y" '
                elif args['type_rec'] == 'E':
                    filter_cond += ' and rec.type=183 '
                elif args['type_rec'] == 'I':
                    filter_cond += ' and rec.type=184 '

            if 'stat_rec' in args and args['stat_rec'] > 0:
                filter_cond += ' and rec.statut=%s '
                params.append(str(args['stat_rec']))

            if 'lastname' in args and args['lastname']:
                filter_cond += ' and pat.nom LIKE %s '
                params.append(args['lastname'] + '%')

            if 'firstname' in args and args['firstname']:
                filter_cond += ' and pat.prenom LIKE %s '
                params.append(args['firstname'] + '%')

            if 'code' in args and args['code']:
                filter_cond += ' and (pat.code LIKE %s or pat.code_patient LIKE %s) '
                params.extend(['%' + args['code'] + '%'] * 2)

            if 'date_beg' in args and args['date_beg']:
                date_beg = parse_date_safe(args['date_beg']).strftime("%Y-%m-%d %H:%M:%S")
                filter_cond += ' and rec.rec_date_receipt >= %s '
                params.append(date_beg)

            if 'date_end' in args and args['date_end']:
                date_end = parse_date_safe(args['date_end']).strftime("%Y-%m-%d %H:%M:%S")
                filter_cond += ' and rec.rec_date_receipt <= %s '
                params.append(date_end)

            # Analysis family
            if 'type_ana' in args and args['type_ana'] > 0:
                table_cond += (' inner join sigl_05_data as ref on req.ref_analyse = ref.id_data ' +
                               'left join sigl_dico_data as fam on fam.id_data = ref.famille ')
                filter_cond += ' and fam.id_data=%s '
                params.append(str(args['type_ana']))

            # Code patient
            if 'code_pat' in args and args['code_pat']:
                filter_cond += ' and (pat.code_patient like %s) '
                params.append('%' + str(args['code_pat']) + '%')

            # 4 in base for yes
            if 'emer' in args and args['emer'] == 4:
                filter_cond += ' and req.urgent=4 '

            # Functionnal unit link with analyzes families
            if 'link_fam' in args and args['link_fam']:
                # avoid redundance of table if filter type_ana exist
                if 'type_ana' not in args or not args['type_ana']:
                    table_cond += (' inner join sigl_05_data as ref on req.ref_analyse = ref.id_data ')

                cond_link_fam = ''
                # prepare list for sql
                for id_fam in args['link_fam']:
                    if not cond_link_fam:
                        cond_link_fam = '('

                    cond_link_fam = cond_link_fam + str(id_fam) + ','

                if cond_link_fam:
                    cond_link_fam = cond_link_fam[:-1] + ')'
                    filter_cond += ' and ref.famille in ' + cond_link_fam + ' '

        # Prescriber list
        if id_pres > 0:
            filter_cond += ' and rec.med_prescripteur=%s '
            params.append(str(id_pres))

        # struct : stat, urgent, num_dos, id_data, rec_date_receipt, code, nom, prenom, id_pat
        req = ('select rec.statut as stat, rec.type as type_rec, rec.rec_num_int, '
               'if(param_num_rec.periode=1070, if(param_num_rec.format=1072,substring(rec.num_dos_mois from 7), '
               'rec.num_dos_mois), if(param_num_rec.format=1072, substring(rec.num_dos_an from 7), rec.num_dos_an)) '
               'as num_dos, if(param_num_rec.periode=1070, rec.num_dos_mois, rec.num_dos_an) as num_dos_long, '
               'rec.id_data as id_data, date_format(rec.rec_date_receipt, %s) as rec_date_receipt, pat.code as code, pat.nom as nom, '
               'pat.prenom as prenom, pat.id_data as id_pat, pat.code_patient as code_lab, rec.rec_num_lite '
               'from sigl_02_data as rec '
               'inner join sigl_03_data as pat on rec.id_patient=pat.id_data '
               'inner join sigl_04_data as req on req.id_dos=rec.id_data '
               'left join sigl_param_num_dos_data as param_num_rec on param_num_rec.id_data=1 ' + table_cond +
               'where ' + filter_cond +
               'group by rec.id_data order by rec.id_data desc ' + limit)

        cursor.execute(req, params)

        l_rec = cursor.fetchall()

        req = ('select count(*) as nb_emer '
               'from sigl_04_data '
               'where id_dos=%s and urgent=4 ')

        # Search for emergency status
        for rec in l_rec:
            cursor.execute(req, (rec['id_data'],))
            emer = cursor.fetchone()

            if emer['nb_emer'] > 0:
                rec['urgent'] = 'O'
            else:
                rec['urgent'] = ''

        return l_rec

    @staticmethod
    def getRecordListGlobal(date_beg, date_end):
        cursor = DB.cursor()

        filter_cond = ' '

        limit = 'LIMIT 1000'
        # filter conditions
        if date_beg:
            filter_cond += ' and rec.rec_date_receipt >= "' + date_beg + '" '

        if date_end:
            filter_cond += ' and rec.rec_date_receipt <= "' + date_end + '" '

        """
        # Prescriber list
        if id_pres > 0:
            filter_cond += ' and rec.med_prescripteur=' + str(id_pres) + ' '"""

        # struct : stat, urgent, num_dos, id_data, rec_date_receipt, code, nom, prenom, id_pat
        req = ('select rec.id_data as id_rec '
               'from sigl_02_data as rec '
               'where rec.statut = 256 ' + filter_cond +
               'group by rec.id_data order by rec.rec_date_receipt asc ' + limit)

        cursor.execute(req)

        return cursor.fetchall()

    @staticmethod
    def getRecord(id_rec):
        cursor = DB.cursor()

        req = ('select rec.id_data, rec.id_owner, rec.id_patient, rec.type, rec.rec_date_receipt, rec.num_dos_jour, '
               'rec.num_dos_an, rec.med_prescripteur, rec.date_prescription, rec.service_interne, rec.num_lit, '
               'rec.id_colis, rec.rec_parcel_date, rec.rc, rec.colis, rec.prix, rec.rec_date_vld, '
               'rec.remise_pourcent, rec.assu_pourcent, rec.a_payer, rec.num_quittance, rec.num_fact, rec.statut, '
               'rec.num_dos_mois, rec.date_hosp, rec.rec_custody, rec.rec_num_int, rec.rec_modified, rec.rec_hosp_num, '
               'if(param_num_rec.periode=1070, rec.num_dos_mois, rec.num_dos_an) as num_rec, rec.rec_date_save, '
               'd_doc_title.label as prescriber_title, d_remise.label as remise, rec_num_lite, '
               'TRIM(CONCAT((COALESCE(pres.nom, ""))," ",TRIM(COALESCE(pres.prenom, "")))) as prescriber '
               'from sigl_02_data as rec '
               'left join sigl_08_data as pres on pres.id_data = rec.med_prescripteur '
               'left join sigl_param_num_dos_data as param_num_rec on param_num_rec.id_data=1 '
               'left join sigl_dico_data as d_doc_title on d_doc_title.id_data=pres.titre '
               'left join sigl_dico_data as d_remise on d_remise.id_data=rec.remise '
               'where rec.id_data=%s')

        cursor.execute(req, (id_rec,))

        return cursor.fetchone()

    @staticmethod
    def getLastRecord():
        cursor = DB.cursor()

        req = ('select id_data, id_owner, id_patient, type, rec_date_receipt, num_dos_jour, num_dos_an, med_prescripteur, '
               'date_prescription, service_interne, num_lit, id_colis, rec_parcel_date, rc, colis, prix, remise, '
               'remise_pourcent, assu_pourcent, a_payer, num_quittance, num_fact, statut, num_dos_mois, date_hosp, '
               'rec_custody, rec_num_int, rec_modified, rec_hosp_num, rec_date_save '
               'from sigl_02_data '
               'order by id_data desc limit 1')

        cursor.execute(req)

        return cursor.fetchone()

    @staticmethod
    def getRecordListAnalysis(id_rec):
        cursor = DB.cursor()

        req = ('select refana.nom as name, max(vld.type_validation) as last_vld '
               'from sigl_04_data as req '
               'inner join sigl_05_data as refana on refana.id_data=req.ref_analyse '
               'inner join sigl_09_data as res on res.id_analyse=req.id_data '
               'inner join sigl_10_data as vld on vld.id_resultat=res.id_data '
               'where (refana.cote_unite != "PB" or refana.cote_unite is null) and req.id_dos=%s '
               'group by name order by last_vld asc, name asc')

        cursor.execute(req, (id_rec,))

        return cursor.fetchall()

    @staticmethod
    def getRecordNext(id_rec):
        cursor = DB.cursor()

        req = ('select id_data '
               'from sigl_02_data '
               'where statut in (254,255) or id_data=%s '
               'order by num_dos_an desc')

        cursor.execute(req, (id_rec,))

        l_rec = cursor.fetchall()

        rec_next = False

        for rec in l_rec:
            if rec_next:
                rec_next = rec
                break

            if rec['id_data'] == id_rec:
                rec_next = True

        return rec_next

    @staticmethod
    def insertRecord(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into sigl_02_data '
                           '(id_owner, id_patient, type, rec_date_receipt, num_dos_jour, num_dos_an, med_prescripteur, '
                           'date_prescription, service_interne, num_lit, id_colis, rec_parcel_date, rc, colis, '
                           'prix, remise, remise_pourcent, assu_pourcent, a_payer, num_quittance, num_fact,statut, '
                           'num_dos_mois, date_hosp, rec_custody, rec_num_int, rec_modified, rec_hosp_num, rec_date_save) '
                           'values '
                           '(%(id_owner)s, %(id_patient)s, %(type)s, %(rec_date_receipt)s, %(num_dos_jour)s, %(num_dos_an)s, '
                           '%(med_prescripteur)s, %(date_prescription)s, %(service_interne)s, %(num_lit)s, %(id_colis)s, '
                           '%(rec_parcel_date)s, %(rc)s, %(colis)s, %(prix)s, %(remise)s, %(remise_pourcent)s, '
                           '%(assu_pourcent)s, %(a_payer)s, %(num_quittance)s, %(num_fact)s, %(statut)s, '
                           '%(num_dos_mois)s, %(date_hosp)s, %(rec_custody)s, %(rec_num_int)s, %(rec_modified)s, '
                           '%(rec_hosp_num)s, NOW())', params)

            Record.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Record.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def updateRecordComm(id_rec, comm):
        try:
            cursor = DB.cursor()

            req = ('update sigl_02_data '
                   'set rc=%s '
                   'where id_data=%s')

            cursor.execute(req, (comm, id_rec,))

            Record.log.info(Logs.fileline() + ' : updateRecordComm id_rec=' + str(id_rec))

            return True
        except mysql.connector.Error as e:
            Record.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def updateRecordStat(id_rec, stat):
        try:
            cursor = DB.cursor()

            req = ('update sigl_02_data '
                   'set statut=%s, rec_date_vld=NOW() '
                   'where id_data=%s')

            cursor.execute(req, (stat, id_rec,))

            Record.log.info(Logs.fileline() + ' : updateRecordStat id_rec=' + str(id_rec))

            return True
        except mysql.connector.Error as e:
            Record.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def updateRecordModified(id_rec, modified):
        try:
            cursor = DB.cursor()

            req = ('update sigl_02_data '
                   'set rec_modified=%s '
                   'where id_data=%s')

            cursor.execute(req, (modified, id_rec))

            Record.log.info(Logs.fileline() + ' : updateRecordModified id_rec=' + str(id_rec))

            return True
        except mysql.connector.Error as e:
            Record.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def removeRecordBill(id_rec, diff_price):
        try:
            cursor = DB.cursor()

            # take discounts into account when recalculating
            rec = Record.getRecord(id_rec)

            if not rec:
                Record.log.error(Logs.fileline() + ' : ' + 'getRecord ERROR not found with id = ' + str(id_rec))
                return False

            price     = rec['prix'] - diff_price
            remain    = rec['a_payer']
            discount  = rec['remise_pourcent']
            insurance = rec['assu_pourcent']

            if discount > 0 and insurance > 0:
                remain = (price - (price * discount / 100)) * (100 - insurance) / 100
            elif discount > 0:
                remain = price - (price * discount / 100)
            elif insurance > 0:
                remain = price - (price * insurance / 100)
            else:
                remain = price

            req = ('update sigl_02_data '
                   'set prix = %s, a_payer = %s '
                   'where id_data=%s')

            cursor.execute(req, (price, remain, id_rec,))

            Record.log.info(Logs.fileline() + ' : removeRecordBill id_rec=' + str(id_rec))

            return True
        except mysql.connector.Error as e:
            Record.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def updateRecordBill(id_rec, price, remain):
        try:
            cursor = DB.cursor()

            req = ('update sigl_02_data '
                   'set prix = %s, a_payer = %s '
                   'where id_data=%s')

            cursor.execute(req, (price, remain, id_rec,))

            Record.log.info(Logs.fileline() + ' : updateRecordBill id_rec=' + str(id_rec))

            return True
        except mysql.connector.Error as e:
            Record.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def deleteRecord(id_rec):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into sigl_02_deleted '
                           '(id_data, id_owner, id_patient, type, rec_date_receipt, num_dos_jour, num_dos_an, med_prescripteur, '
                           'date_prescription, service_interne, num_lit, id_colis, rec_parcel_date, rc, colis, prix, '
                           'remise, remise_pourcent, assu_pourcent, a_payer, num_quittance, num_fact,statut,num_dos_mois, '
                           'date_hosp, rec_custody, rec_num_int, rec_date_vld, rec_modified, rec_hosp_num, rec_date_save) '
                           'select id_data, id_owner, id_patient, type, rec_date_receipt, num_dos_jour, num_dos_an, med_prescripteur, '
                           'date_prescription, service_interne, num_lit, id_colis, rec_parcel_date, rc, colis, prix, '
                           'remise, remise_pourcent, assu_pourcent, a_payer, num_quittance, num_fact,statut,num_dos_mois, '
                           'date_hosp, rec_custody, rec_num_int, rec_date_vld, rec_modified, rec_hosp_num, rec_date_save '
                           'from sigl_02_data '
                           'where id_data=%s', (id_rec,))

            cursor.execute('delete from sigl_02_data '
                           'where id_data=%s', (id_rec,))

            Record.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Record.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getRecordNbEmer(args):
        cursor = DB.cursor()

        table_cond = ''
        filter_cond = ''

        # Functionnal unit link with analyzes families
        if 'link_fam' in args and args['link_fam']:
            # avoid redundance of table if filter type_ana exist
            table_cond += (' inner join sigl_05_data as ref on req.ref_analyse = ref.id_data ')

            cond_link_fam = ''
            # prepare list for sql
            for id_fam in args['link_fam']:
                if not cond_link_fam:
                    cond_link_fam = '('

                cond_link_fam = cond_link_fam + str(id_fam) + ','

            if cond_link_fam:
                cond_link_fam = cond_link_fam[:-1] + ')'
                filter_cond += ' and ref.famille in ' + cond_link_fam + ' '

        req = ('select count(distinct(rec.id_data)) as nb_emer '
               'from sigl_02_data as rec '
               'inner join sigl_04_data as req on req.id_dos=rec.id_data ' + table_cond +
               'where req.urgent=4 and rec.statut in (181,182,253,254,255) ' + filter_cond)

        cursor.execute(req)

        return cursor.fetchone()

    @staticmethod
    def getRecordNbRecTech():
        cursor = DB.cursor()

        # Number of records to validate by a technician
        req = ('select count(*) as nb_rec_tech '
               'from sigl_02_data '
               'where statut in (182,253)')

        cursor.execute(req)

        return cursor.fetchone()

    @staticmethod
    def getRecordNbRecBio():
        cursor = DB.cursor()

        # Number of records to validate by a biologist
        req = ('select count(*) as nb_rec_bio '
               'from sigl_02_data '
               'where statut in (254,255)')

        cursor.execute(req)

        return cursor.fetchone()

    @staticmethod
    def getRecordNbRec():
        cursor = DB.cursor()

        # Number of records
        req = ('select count(*) as nb_rec '
               'from sigl_02_data')

        cursor.execute(req)

        return cursor.fetchone()

    @staticmethod
    def getRecordNbRecToday(num_today):
        cursor = DB.cursor()

        # Number of records validated today
        req = ('select count(*) as nb_rec_today '
               'from sigl_02_data '
               'where statut=256 and num_dos_jour like "' + str(num_today) + '%"')

        cursor.execute(req)

        return cursor.fetchone()

    @staticmethod
    def generateBillNumber(id_rec):
        try:
            # Get last number
            cursor = DB.cursor()

            req = ('select num_fact '
                   'from sigl_02_data '
                   'order by num_fact desc limit 1')

            cursor.execute(req)

            num = cursor.fetchone()

            if num['num_fact']:
                bill_num = int(num['num_fact']) + 1
                bill_num = str(bill_num).rjust(10, '0')
            else:
                bill_num = '0000000001'

            cursor = DB.cursor()

            req = ('update sigl_02_data '
                   'set num_fact=%s '
                   'where id_data=%s')

            cursor.execute(req, (bill_num, id_rec,))

            Record.log.info(Logs.fileline() + ' : generateBillNumber id_rec=' + str(id_rec))

            # insert in sigl_pj_sequence num_fact
            pattern = "%010d"        # make pattern for table
            end_num = int(bill_num)  # get end number without 0
            ret = Record.insertPjSequence("num_fact", pattern, end_num)

            if ret <= 0:
                Record.log.error(Logs.alert() + ' : generateBillNumber ERROR  insertPjSequence num_fact')

            return True
        except mysql.connector.Error as e:
            Record.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def insertPjSequence(sid, pattern, num):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into sigl_pj_sequence '
                           '(sid, pattern, num) '
                           'values '
                           '(%s, %s, %s )', (sid, pattern, num))

            Record.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Record.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def getDataset(date_beg, date_end):
        cursor = DB.cursor()

        req = ('select rec.id_data as id_record, rec.rec_custody, rec.id_patient,  d_type.label as type, rec.rec_num_int, '
               'date_format(rec.rec_date_receipt, %s) as record_date, date_format(rec.rec_date_save, %s) as record_created, '
               'rec.num_dos_an as rec_num_year, rec.num_dos_jour as rec_num_day, rec.num_dos_mois as rec_num_month, '
               'rec.rec_num_lite, rec.rec_modified, '
               'rec.med_prescripteur as id_doctor, doctor.nom as doctor_lname, doctor.prenom as doctor_fname, '
               'date_format(rec.date_prescription, %s) as prescription_date, rec.rec_hosp_num, '
               'rec.service_interne as internal_service, rec.num_lit as bed_num, rec.prix as price, '
               'rec.remise as discount, rec.remise_pourcent as discount_percent, rec.assu_pourcent as insurance_percent, '
               'rec.a_payer as to_pay, d_status.label as status, date_format(rec.date_hosp, %s) as hosp_date, '
               'd_sex.label as sex, date_format(pat.ddn, %s) as birth, pat.age, d_age_unit.label as age_unit, '
               'pat.nom as pat_name, pat.prenom as pat_firstname, pat.tel as phone1, pat.pat_phone2 as phone2 '
               'from sigl_02_data as rec '
               'inner join sigl_03_data as pat on pat.id_data=rec.id_patient '
               'left join sigl_08_data as doctor on doctor.id_data=rec.med_prescripteur '
               'left join sigl_dico_data as d_type on d_type.id_data=rec.type '
               'left join sigl_dico_data as d_status on d_status.id_data=rec.statut '
               'left join sigl_dico_data as d_sex on d_sex.id_data=pat.sexe '
               'left join sigl_dico_data as d_age_unit on d_age_unit.id_data=pat.unite '
               'where rec_date_receipt between %s and %s '
               'order by id_record desc')

        cursor.execute(req, (Constants.cst_dt_HM_SQL, Constants.cst_dt_HM_SQL, Constants.cst_isodate, Constants.cst_isodate, Constants.cst_isodate, date_beg, date_end))

        return cursor.fetchall()

    @staticmethod
    def getRecordValidation(id_rec):
        cursor = DB.cursor()

        # return last validation
        req = ('select rev_date, rev_user, rev_rec, rev_comm '
               'from record_validation '
               'where rev_rec=%s '
               'order by rev_ser desc limit 1')

        cursor.execute(req, (id_rec,))

        return cursor.fetchone()

    @staticmethod
    def insertRecordValidation(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into record_validation '
                           '(rev_date, rev_user, rev_rec, rev_comm) '
                           'values '
                           '(NOW(), %(id_user)s, %(id_rec)s, %(comm)s)', params)

            Record.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Record.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def rec_num_int_exist(rec_num_int):
        try:
            cursor = DB.cursor()

            cursor.execute('select count(*) as nb_code '
                           'from sigl_02_data '
                           'where rec_num_int=%s', (rec_num_int,))

            ret = cursor.fetchone()

            if ret and ret['nb_code'] == 0:
                return False
            else:
                return True
        except mysql.connector.Error as e:
            Record.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return -1
