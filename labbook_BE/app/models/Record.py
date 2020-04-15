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
    def getRecordList(args, id_lab, id_group):
        cursor = DB.cursor()

        filter_cond = ''

        if not args:
            limit = 'LIMIT 20'
        else:
            limit = 'LIMIT 200'
            # filter conditions
            if args['num_rec']:
                filter_cond += ' and (dos.num_dos_an LIKE "' + args['num_rec'] + '%" or dos.num_dos_mois LIKE "' + args['num_rec'] + '%") '

            if args['stat_rec'] and args['stat_rec'] > 0:
                filter_cond += ' and dos.statut=' + str(args['stat_rec']) + ' '

            if args['patient']:
                filter_cond += ' and (pat.nom LIKE "' + args['patient'] + '%"'\
                               ' or pat.prenom LIKE "' + args['patient'] + '%"'\
                               ' or pat.code LIKE "' + args['patient'] + '") '

            if args['date_beg']:
                filter_cond += ' and dos.date_dos >= "' + args['date_beg'] + '" '

            if args['date_end']:
                filter_cond += ' and dos.date_dos <= "' + args['date_end'] + '" '

            # NULL (5 sometimes) or 4 in base
            if args['emer'] and args['emer'] == 4:
                filter_cond += ' and ana.urgent=4 '

        # struct : stat, urgent, num_dos, id_data, date_dos, code, nom, prenom, id_pat
        req = 'select statut.id_data as stat, '\
              'if(ana.urgent LIKE "%4%", "O", "") as urgent, '\
              'if(param_num_dos.periode=1070, if(param_num_dos.format=1072,cast(substring(dos.num_dos_mois from 7) as UNSIGNED), dos.num_dos_mois), '\
              'if(param_num_dos.format=1072, cast(substring(dos.num_dos_an from 5) as UNSIGNED), dos.num_dos_an)) as num_dos, '\
              'dos.id_data as id_data, date_format(dos.date_dos, %s) as date_dos, pat.code as code, pat.nom as nom, pat.prenom as prenom, pat.id_data as id_pat '\
              'from sigl_02_data as dos '\
              'inner join sigl_dico_data as statut on dos.statut=statut.id_data and statut.dico_name = "statut_dossier" '\
              'inner join sigl_03_data as pat on dos.id_patient=pat.id_data '\
              'inner join sigl_04_data as ana on ana.id_dos=dos.id_data '\
              'left join sigl_09_data as res on res.id_analyse=ana.id_data '\
              'left join sigl_param_num_dos_data as param_num_dos on param_num_dos.id_data=1 '\
              'where length(dos.num_dos_an) = 10 ' + filter_cond +\
              'and (dos.id_data is NULL or (exists(select 1 from sigl_02_data_group where sigl_02_data_group.id_group in (%s) and sigl_02_data_group.id_data = dos.id_data)) '\
              'or ( exists( select 1 from sigl_02_data_group inner join sigl_02_data_group_mode on sigl_02_data_group.id_data_group=sigl_02_data_group_mode.id_data_group '\
              'where sigl_02_data_group.id_group=%s and sigl_02_data_group.id_data = dos.id_data and sigl_02_data_group_mode.mode & 292 '\
              'and (sigl_02_data_group_mode.date_valid IS NULL or CURRENT_DATE <= sigl_02_data_group_mode.date_valid)))) '\
              'and (pat.id_data is NULL or (exists(select 1 from sigl_03_data_group where sigl_03_data_group.id_group in (%s) and sigl_03_data_group.id_data = pat.id_data)) '\
              'or ( exists( select 1 from sigl_03_data_group inner join sigl_03_data_group_mode on sigl_03_data_group.id_data_group=sigl_03_data_group_mode.id_data_group '\
              'where sigl_03_data_group.id_group=%s and sigl_03_data_group.id_data = pat.id_data and sigl_03_data_group_mode.mode & 292 '\
              'and (sigl_03_data_group_mode.date_valid IS NULL or CURRENT_DATE <= sigl_03_data_group_mode.date_valid)))) '\
              'and (ana.id_data is NULL or (exists(select 1 from sigl_04_data_group where sigl_04_data_group.id_group in (%s) and sigl_04_data_group.id_data = ana.id_data)) '\
              'or ( exists( select 1 from sigl_04_data_group inner join sigl_04_data_group_mode on sigl_04_data_group.id_data_group=sigl_04_data_group_mode.id_data_group '\
              'where sigl_04_data_group.id_group=%s and sigl_04_data_group.id_data = ana.id_data and sigl_04_data_group_mode.mode & 292 '\
              'and (sigl_04_data_group_mode.date_valid IS NULL or CURRENT_DATE <= sigl_04_data_group_mode.date_valid)))) '\
              'and (res.id_data is NULL or (exists(select 1 from sigl_09_data_group where sigl_09_data_group.id_group in (%s) and sigl_09_data_group.id_data = res.id_data)) '\
              'or ( exists( select 1 from sigl_09_data_group inner join sigl_09_data_group_mode on sigl_09_data_group.id_data_group=sigl_09_data_group_mode.id_data_group '\
              'where sigl_09_data_group.id_group=%s and sigl_09_data_group.id_data = res.id_data and sigl_09_data_group_mode.mode & 292 '\
              'and (sigl_09_data_group_mode.date_valid IS NULL or CURRENT_DATE <= sigl_09_data_group_mode.date_valid)))) '\
              'and (param_num_dos.id_data is NULL or (exists(select 1 from sigl_param_num_dos_data_group where sigl_param_num_dos_data_group.id_group in (%s) '\
              'and sigl_param_num_dos_data_group.id_data = param_num_dos.id_data)) or ( exists( select 1 from sigl_param_num_dos_data_group '\
              'inner join sigl_param_num_dos_data_group_mode on sigl_param_num_dos_data_group.id_data_group=sigl_param_num_dos_data_group_mode.id_data_group '\
              'where sigl_param_num_dos_data_group.id_group=%s and sigl_param_num_dos_data_group.id_data=param_num_dos.id_data and sigl_param_num_dos_data_group_mode.mode & 292 '\
              'and (sigl_param_num_dos_data_group_mode.date_valid IS NULL or CURRENT_DATE <= sigl_param_num_dos_data_group_mode.date_valid)))) '\
              'group by dos.id_data order by dos.num_dos_an desc ' + limit

        cursor.execute(req, (Constants.cst_isodate, id_lab, id_group, id_lab, id_group, id_lab, id_group, id_lab, id_group, id_lab, id_group,))

        return cursor.fetchall()

    @staticmethod
    def getRecord(id_rec):
        cursor = DB.cursor()

        req = 'select id_data, id_owner, id_patient, type, date_dos, num_dos_jour, num_dos_an, med_prescripteur, date_prescription, service_interne, num_lit, '\
              'id_colis, date_reception_colis, rc, colis, prix, remise, remise_pourcent, assu_pourcent, a_payer, num_quittance, num_fact, statut, num_dos_mois '\
              'from sigl_02_data '\
              'where id_data=%s'

        cursor.execute(req, (id_rec,))

        return cursor.fetchone()

    @staticmethod
    def getRecordFile(id_rec):
        cursor = DB.cursor()

        req = 'select file.id_data as id_data, file.original_name as name, file.path as dir, storage.path as storage '\
              'from sigl_dos_valisedoc__file_data as valise, sigl_file_data as file, sigl_storage_data as storage '\
              'where file.id_data=valise.id_file and storage.id_data=file.id_storage and valise.id_ext=%s'

        cursor.execute(req, (id_rec,))

        return cursor.fetchall()

    @staticmethod
    def insertRecord(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into sigl_02_data '
                           '(id_owner, id_patient, type, date_dos, num_dos_jour, num_dos_an, med_prescripteur, date_prescription, service_interne, num_lit, '
                           'id_colis, date_reception_colis, rc, colis, prix, remise, remise_pourcent, assu_pourcent, a_payer, num_quittance, num_fact,statut, num_dos_mois) '
                           'values '
                           '(%(id_owner)s, %(id_patient)s, %(type)s, %(date_dos)s, %(num_dos_jour)s, %(num_dos_an)s, %(med_prescripteur)s, %(date_prescription)s, '
                           '%(service_interne)s, %(num_lit)s, %(id_colis)s, %(date_reception_colis)s, %(rc)s, %(colis)s, %(prix)s, %(remise)s, %(remise_pourcent)s, '
                           '%(assu_pourcent)s, %(a_payer)s, %(num_quittance)s, %(num_fact)s, %(statut)s, %(num_dos_mois)s )', params)

            Record.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Record.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def insertRecordGroup(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into sigl_02_data_group '
                           '(id_data, id_group) '
                           'values '
                           '(%(id_data)s, %(id_group)s )', params)

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
    def getRecordTypeNumber():
        cursor = DB.cursor()

        req = 'select id_data, id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, periode, format '\
              'from sigl_param_num_dos_data '\
              'order by id_data desc limit 1'

        cursor.execute(req)

        return cursor.fetchone()
