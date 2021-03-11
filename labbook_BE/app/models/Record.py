# -*- coding:utf-8 -*-
import logging
import mysql.connector

# from app.models.Constants import *
from app.models.DB import DB
from app.models.Constants import Constants
from app.models.Logs import Logs


class Record:
    log = logging.getLogger('log_db')

    @staticmethod
    def getRecordList(args, id_pres):
        cursor = DB.cursor()

        filter_cond = 'length(dos.num_dos_an) = 10 '

        if not args:
            limit = 'LIMIT 1000'
        else:
            limit = 'LIMIT 4000'
            # filter conditions
            if args['num_rec']:
                filter_cond += ' and (dos.num_dos_an LIKE "%' + args['num_rec'] + '%" or dos.num_dos_mois LIKE "%' + args['num_rec'] + '%") '

            if 'stat_work' in args and args['stat_work']:
                filter_cond += ' and dos.statut IN ' + str(args['stat_work']) + ' '

            if args['stat_rec'] and args['stat_rec'] > 0:
                filter_cond += ' and dos.statut=' + str(args['stat_rec']) + ' '

            if 'lastname' in args and args['lastname']:
                filter_cond += ' and pat.nom LIKE "' + args['lastname'] + '%" '

            if 'firstname' in args and args['firstname']:
                filter_cond += ' and pat.prenom LIKE "' + args['firstname'] + '%" '

            if 'code' in args and args['code']:
                filter_cond += ' and (pat.code LIKE "%' + args['code'] + '%" or pat.code_patient LIKE "%' + args['code'] + '%") '

            if args['date_beg']:
                filter_cond += ' and dos.date_dos >= "' + args['date_beg'] + '" '

            if args['date_end']:
                filter_cond += ' and dos.date_dos <= "' + args['date_end'] + '" '

            # 4 in base for yes
            if args['emer'] and args['emer'] == 4:
                filter_cond += ' and ana.urgent=4 '

        # Prescriber list
        if id_pres > 0:
            filter_cond += ' and dos.med_prescripteur=' + str(id_pres) + ' '

        # struct : stat, urgent, num_dos, id_data, date_dos, code, nom, prenom, id_pat
        req = 'select dos.statut as stat, '\
              'if(param_num_dos.periode=1070, if(param_num_dos.format=1072,substring(dos.num_dos_mois from 7), dos.num_dos_mois), '\
              'if(param_num_dos.format=1072, substring(dos.num_dos_an from 7), dos.num_dos_an)) as num_dos, '\
              'if(param_num_dos.periode=1070, dos.num_dos_mois, dos.num_dos_an) as num_dos_long, '\
              'dos.id_data as id_data, date_format(dos.date_dos, %s) as date_dos, pat.code as code, pat.nom as nom, pat.prenom as prenom, pat.id_data as id_pat '\
              'from sigl_02_data as dos '\
              'inner join sigl_03_data as pat on dos.id_patient=pat.id_data '\
              'inner join sigl_04_data as ana on ana.id_dos=dos.id_data '\
              'left join sigl_param_num_dos_data as param_num_dos on param_num_dos.id_data=1 '\
              'where ' + filter_cond +\
              'group by dos.id_data order by dos.num_dos_an desc ' + limit

        cursor.execute(req, (Constants.cst_isodate,))

        l_rec = cursor.fetchall()

        req = 'select count(*) as nb_emer '\
              'from sigl_04_data '\
              'where id_dos=%s and urgent=4 '

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
    def getRecord(id_rec):
        cursor = DB.cursor()

        req = 'select id_data, id_owner, id_patient, type, date_dos, num_dos_jour, num_dos_an, med_prescripteur, date_prescription, service_interne, num_lit, '\
              'id_colis, date_reception_colis, rc, colis, prix, remise, remise_pourcent, assu_pourcent, a_payer, num_quittance, num_fact, statut, num_dos_mois, '\
              'date_hosp '\
              'from sigl_02_data '\
              'where id_data=%s'

        cursor.execute(req, (id_rec,))

        return cursor.fetchone()

    @staticmethod
    def getLastRecord():
        cursor = DB.cursor()

        req = 'select id_data, id_owner, id_patient, type, date_dos, num_dos_jour, num_dos_an, med_prescripteur, date_prescription, service_interne, num_lit, '\
              'id_colis, date_reception_colis, rc, colis, prix, remise, remise_pourcent, assu_pourcent, a_payer, num_quittance, num_fact, statut, num_dos_mois, '\
              'date_hosp '\
              'from sigl_02_data '\
              'order by id_data desc limit 1'

        cursor.execute(req)

        return cursor.fetchone()

    @staticmethod
    def getRecordListAnalysis(id_rec):
        cursor = DB.cursor()

        req = ('select refana.nom as name, max(vld.type_validation) as last_vld '
               'from sigl_04_data as ana '
               'inner join sigl_05_data as refana on refana.id_data=ana.ref_analyse '
               'inner join sigl_09_data as res on res.id_analyse=ana.id_data '
               'inner join sigl_10_data as vld on vld.id_resultat=res.id_data '
               'where (refana.cote_unite != "PB" or refana.cote_unite is null) and ana.id_dos=%s '
               'group by name order by last_vld asc, name asc')

        cursor.execute(req, (id_rec,))

        return cursor.fetchall()

    @staticmethod
    def getRecordNext(id_rec):
        cursor = DB.cursor()

        req = 'select id_data '\
              'from sigl_02_data '\
              'where statut in (254,255) or id_data=%s '\
              'order by num_dos_an desc'

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
                           '(id_owner, id_patient, type, date_dos, num_dos_jour, num_dos_an, med_prescripteur, date_prescription, service_interne, num_lit, '
                           'id_colis, date_reception_colis, rc, colis, prix, remise, remise_pourcent, assu_pourcent, a_payer, num_quittance, num_fact,statut, '
                           'num_dos_mois, date_hosp) '
                           'values '
                           '(%(id_owner)s, %(id_patient)s, %(type)s, %(date_dos)s, %(num_dos_jour)s, %(num_dos_an)s, %(med_prescripteur)s, %(date_prescription)s, '
                           '%(service_interne)s, %(num_lit)s, %(id_colis)s, %(date_reception_colis)s, %(rc)s, %(colis)s, %(prix)s, %(remise)s, %(remise_pourcent)s, '
                           '%(assu_pourcent)s, %(a_payer)s, %(num_quittance)s, %(num_fact)s, %(statut)s, %(num_dos_mois)s, %(date_hosp)s)', params)

            Record.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Record.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def updateRecordStat(id_rec, stat):
        try:
            cursor = DB.cursor()

            req = 'update sigl_02_data '\
                  'set statut=%s '\
                  'where id_data=%s'

            cursor.execute(req, (stat, id_rec,))

            Record.log.info(Logs.fileline() + ' : updateRecordStat id_rec=' + str(id_rec))

            return True
        except mysql.connector.Error as e:
            Record.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def deleteRecord(id_rec):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into sigl_02_deleted '
                           '(id_data, id_owner, id_patient, type, date_dos, num_dos_jour, num_dos_an, med_prescripteur, '
                           'date_prescription, service_interne, num_lit, id_colis, date_reception_colis, rc, colis, prix, '
                           'remise, remise_pourcent, assu_pourcent, a_payer, num_quittance, num_fact,statut, num_dos_mois) '
                           'select id_data, id_owner, id_patient, type, date_dos, num_dos_jour, num_dos_an, med_prescripteur, '
                           'date_prescription, service_interne, num_lit, id_colis, date_reception_colis, rc, colis, prix, '
                           'remise, remise_pourcent, assu_pourcent, a_payer, num_quittance, num_fact,statut, num_dos_mois '
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
    def getRecordNbEmer():
        cursor = DB.cursor()

        req = 'select count(*) as nb_emer '\
              'from sigl_02_data as rec '\
              'inner join sigl_04_data as ana on ana.id_dos=rec.id_data '\
              'where ana.urgent=4 and rec.statut in (182,253,254,255) '\
              'group by rec.id_data'

        cursor.execute(req)

        return cursor.fetchone()

    @staticmethod
    def getRecordNbRecTech():
        cursor = DB.cursor()

        # Number of records to validate by a technician
        req = 'select count(*) as nb_rec_tech '\
              'from sigl_02_data '\
              'where statut in (182,253)'

        cursor.execute(req)

        return cursor.fetchone()

    @staticmethod
    def getRecordNbRecBio():
        cursor = DB.cursor()

        # Number of records to validate by a biologist
        req = 'select count(*) as nb_rec_bio '\
              'from sigl_02_data '\
              'where statut in (254,255)'

        cursor.execute(req)

        return cursor.fetchone()

    @staticmethod
    def getRecordNbRec():
        cursor = DB.cursor()

        # Number of records
        req = 'select count(*) as nb_rec '\
              'from sigl_02_data'

        cursor.execute(req)

        return cursor.fetchone()

    @staticmethod
    def getRecordNbRecToday(num_today):
        cursor = DB.cursor()

        # Number of records validated today
        req = 'select count(*) as nb_rec_today '\
              'from sigl_02_data '\
              'where statut=256 and num_dos_jour like "%s%"'

        cursor.execute(req, (num_today,))

        return cursor.fetchone()

    @staticmethod
    def generateBillNumber(id_rec):
        try:
            # Get last number
            cursor = DB.cursor()

            req = 'select num_fact '\
                  'from sigl_02_data '\
                  'order by num_fact desc limit 1'

            cursor.execute(req)

            num = cursor.fetchone()

            if num['num_fact']:
                bill_num = int(num['num_fact']) + 1
                bill_num = str(bill_num).rjust(10, '0')
            else:
                bill_num = '0000000001'

            cursor = DB.cursor()

            req = 'update sigl_02_data '\
                  'set num_fact=%s '\
                  'where id_data=%s'

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
