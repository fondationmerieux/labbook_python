# -*- coding:utf-8 -*-
import logging

# from app.models.Constants import *
from app.models.DB import DB
from app.models.Constants import Constants


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

    """
    @staticmethod
    def getRecord(id_ana):
        cursor = DB.cursor()

        req = 'select id_data, id_owner, code, nom, abbr, famille, paillasse, cote_unite, cote_valeur, '\
              'commentaire, produit_biologique, type_prel, type_analyse, actif '\
              'from sigl_05_data '\
              'where id_data=%s'

        cursor.execute(req, (id_ana,))

        return cursor.fetchone()


    @staticmethod
    def insertRecord(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into sigl_03_data '
                           '(id_owner, anonyme, code, code_record, nom, prenom, ddn, sexe, ethnie, adresse, cp, ville, '
                           'tel, profession, nom_jf, quartier, bp, ddn_approx, age, annee_naiss, semaine_naiss, mois_naiss, unite) '
                           'values '
                           '(%(id_owner)s, %(anonyme)s, %(code)s, %(code_record)s, %(nom)s, %(prenom)s, %(ddn)s, %(sexe)s, %(ethnie)s, %(adresse)s, %(cp)s, %(ville)s, '
                           '%(tel)s, %(profession)s, %(nom_jf)s, %(quartier)s, %(bp)s, %(ddn_approx)s, %(age)s, %(annee_naiss)s, '
                           '%(semaine_naiss)s, %(mois_naiss)s, %(unite)s )', params)

            Record.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Record.log.error(Logs.fileline() + ' : ERROR SQL ' + str(e.errno))
            return 0

    @staticmethod
    def insertRecordGroup(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into sigl_03_data_group '\
                           '(id_data, id_group) '\
                           'values '\
                           '(%(id_data)s, %(id_group)s )', params)

            Record.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Record.log.error(Logs.fileline() + ' : ERROR SQL ' + str(e.errno))
            return 0


    @staticmethod
    def getProductType(id_data):
        cursor = DB.cursor()

        req = 'select id_data, id_owner, dico_name, label, short_label, position, code, dico_id, dico_value_id, archived '\
              'from sigl_dico_data '\
              'where id_data=%s'

        cursor.execute(req, (id_data,))

        return cursor.fetchone()"""
