# -*- coding:utf-8 -*-
import logging
import mysql.connector

from datetime import datetime, date
from app.models.Constants import Constants
from app.models.DB import DB
from app.models.Logs import Logs


class Result:
    log = logging.getLogger('log_db')

    @staticmethod
    def getResultList(args):
        cursor = DB.cursor()

        table_cond  = ''
        filter_cond = ''

        limit = 'LIMIT 500'
        # filter conditions
        date_beg = args['date_beg']
        date_end = args['date_end']

        # NULL (5 sometimes) or 4 in base
        if 'emer_ana' in args and args['emer_ana'] == 4:
            filter_cond += ' and urgent=4 and ref_var.type_resultat not in ("229", "265") '

        # Analysis family
        if 'type_ana' in args and args['type_ana'] > 0:
            filter_cond += ' and fam.id_data=' + str(args['type_ana']) + ' '

        # Analysis specific
        if 'id_ana' in args and args['id_ana'] > 0:
            filter_cond += ' and req.ref_analyse=' + str(args['id_ana']) + ' '

        # Code patient
        if 'code_pat' in args and args['code_pat']:
            filter_cond += ' and (pat.code_patient like "%' + str(args['code_pat']) + '%") '
            table_cond += ' inner join sigl_03_data as pat on pat.id_data=rec.id_patient '

        # Without valid result
        if 'valid_res' in args and args['valid_res'] > 0:
            filter_cond += ' and res.id_data not in (select id_resultat from sigl_10_data where type_validation > 250 and res.id_data=id_resultat) and rec.statut < 254 '

        # Functionnal unit link with analyzes families
        if 'link_fam' in args and args['link_fam']:
            cond_link_fam = ''
            # prepare list for sql
            for id_fam in args['link_fam']:
                if not cond_link_fam:
                    cond_link_fam = '('

                cond_link_fam = cond_link_fam + str(id_fam) + ','

            if cond_link_fam:
                cond_link_fam = cond_link_fam[:-1] + ')'
                filter_cond += ' and ref.famille in ' + cond_link_fam + ' '

        req = ('select req.ref_analyse as ref_ana, req.id_data as id_ana, rec.id_data as id_dos, rec.id_patient, '
               'ref.nom as nom, fam.label as famille, res.id_data as id_res, res.valeur as valeur, ref_var.*, '
               'rec.num_dos_mois as num_dos_mois, rec.num_dos_an as num_dos_an, rec.date_dos as date_dos, '
               'rec.date_prescription as date_prescr, rec.statut as stat, req.urgent as urgent, rec.rec_modified, '
               'req.id_owner as id_owner, var_pos.position as position, var_pos.num_var as num_var, '
               'var_pos.obligatoire as oblig, req.req_outsourced as outsourced '
               'from sigl_04_data as req '
               'inner join sigl_02_data as rec on rec.id_data = req.id_dos '
               'inner join sigl_05_data as ref on req.ref_analyse = ref.id_data '
               'left join sigl_dico_data as fam on fam.id_data = ref.famille '
               'inner join sigl_09_data as res on req.id_data = res.id_analyse '
               'inner join sigl_07_data as ref_var on ref_var.id_data = res.ref_variable '
               'inner join sigl_05_07_data as var_pos on ref_var.id_data = var_pos.id_refvariable '
               'and ref.id_data = var_pos.id_refanalyse ' + table_cond +
               'where (rec.date_dos between %s and %s) ' + filter_cond +
               'order by nom asc, id_dos asc, id_ana asc, position asc ' + limit)

        cursor.execute(req, (date_beg, date_end,))

        return cursor.fetchall()

    @staticmethod
    def getResultRecord(id_rec, empty=True, link_fam=[]):
        cursor = DB.cursor()

        cond = ''

        # avoid empty result of this request
        if not empty:
            cond = ' and res.valeur is not NULL and res.valeur != "" and res.valeur != 1013 '

        # Functionnal unit link with analyzes families
        if link_fam:
            cond_link_fam = ''
            # prepare list for sql
            for id_fam in link_fam:
                if not cond_link_fam:
                    cond_link_fam = '('

                cond_link_fam = cond_link_fam + str(id_fam) + ','

            if cond_link_fam:
                cond_link_fam = cond_link_fam[:-1] + ')'
                cond += ' and ref.famille in ' + cond_link_fam + ' '

        req = ('select req.ref_analyse as ref_ana, req.id_data as id_ana, rec.id_data as id_dos, '
               'ref.nom as nom, fam.label as famille, res.id_data as id_res, res.valeur as valeur, ref_var.*, '
               'rec.num_dos_mois as num_dos_mois, rec.num_dos_an as num_dos_an, rec.date_dos as date_dos, '
               'rec.date_prescription as date_prescr, rec.statut as stat, req.urgent as urgent, rec_modified, '
               'req.id_owner as id_owner, rec.id_patient as id_pat, req.req_outsourced as outsourced, '
               'var_pos.position as position, var_pos.num_var as num_var, var_pos.obligatoire as oblig '
               'from sigl_04_data as req '
               'inner join sigl_02_data as rec on rec.id_data = req.id_dos '
               'inner join sigl_05_data as ref on req.ref_analyse = ref.id_data '
               'left join sigl_dico_data as fam on fam.id_data = ref.famille '
               'inner join sigl_09_data as res on req.id_data = res.id_analyse '
               'inner join sigl_07_data as ref_var on ref_var.id_data = res.ref_variable '
               'inner join sigl_05_07_data as var_pos on ref_var.id_data = var_pos.id_refvariable '
               'and ref.id_data = var_pos.id_refanalyse '
               'where id_dos=%s ' + cond +
               'order by nom asc, id_ana asc, position asc')

        cursor.execute(req, (id_rec,))

        return cursor.fetchall()

    @staticmethod
    def getPreviousResult(id_pat, ref_ana, ref_var, id_res, date_vld=''):
        cursor = DB.cursor()

        if not date_vld:
            date_today = datetime.strftime(date.today(), Constants.cst_isodatetime)
        else:
            date_today = datetime.strptime(date_vld, '%d/%m/%Y %H:%M:%S')

        req = ('select res.valeur as valeur, vld.date_validation as date_valid '
               'from sigl_09_data as res '
               'inner join sigl_05_07_data as ref on ref.id_refvariable = res.ref_variable '
               'inner join sigl_04_data as dem on dem.ref_analyse = ref.id_refanalyse and dem.id_data = res.id_analyse '
               'inner join sigl_02_data as rec on rec.id_data = dem.id_dos '
               'inner join sigl_10_data as vld on vld.id_resultat = res.id_data '
               'where rec.id_patient=%s and dem.ref_analyse=%s and res.ref_variable=%s '
               'and vld.type_validation=252 and vld.motif_annulation is NULL and res.id_data != %s '
               'and vld.date_validation < %s '
               'order by vld.date_validation desc limit 1')

        cursor.execute(req, (id_pat, ref_ana, ref_var, id_res, date_today))

        return cursor.fetchone()

    @staticmethod
    def insertResult(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into sigl_09_data '
                           '(id_owner, id_analyse, ref_variable, obligatoire) '
                           'values '
                           '(%(id_owner)s, %(id_analyse)s, %(ref_variable)s, %(obligatoire)s)', params)

            Result.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Result.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def deleteResult(id_res):
        try:
            cursor = DB.cursor()

            cursor.execute('select id_data '
                           'from sigl_09_data '
                           'where id_data=%s', (id_res,))

            l_result = cursor.fetchall()

            for result in l_result:
                cursor.execute('insert into sigl_09_deleted '
                               '(id_data, id_owner, id_analyse, ref_variable, valeur, obligatoire) '
                               'select id_data, id_owner, id_analyse, ref_variable, valeur, obligatoire '
                               'from sigl_09_data '
                               'where id_data=%s', (result['id_data'],))

                cursor.execute('delete from sigl_09_data '
                               'where id_data=%s', (result['id_data'],))

            Result.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Result.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getResultValidation(id_res):
        cursor = DB.cursor()

        req = ('select v.id_data as id_data, v.id_owner as id_owner, v.id_resultat as id_resultat, '
               'v.date_validation as date_validation, v.utilisateur as utilisateur, v.valeur as valeur, '
               'v.type_validation as type_validation, v.commentaire as commentaire, '
               'v.motif_annulation as motif_annulation, dico.label as label_motif '
               'from sigl_10_data as v '
               'left join sigl_dico_data as dico on dico.id_data=motif_annulation '
               'where id_resultat=%s '
               'order by id_data desc limit 1')

        cursor.execute(req, (id_res,))

        return cursor.fetchone()

    @staticmethod
    def getResultListValidation(id_res):
        cursor = DB.cursor()

        req = ('select v.id_data as id_data, v.id_owner as id_owner, v.id_resultat as id_resultat, '
               'v.date_validation as date_validation, v.utilisateur as utilisateur, v.valeur as valeur, '
               'v.type_validation as type_validation, v.commentaire as commentaire, v.motif_annulation as motif_annulation '
               'from sigl_10_data as v '
               'where id_resultat=%s '
               'order by id_data')

        cursor.execute(req, (id_res,))

        return cursor.fetchall()

    @staticmethod
    def getLastTypeValidation(id_ana):
        cursor = DB.cursor()

        req = ('select valid.type_validation as type_validation '
               'from sigl_10_data as valid, sigl_09_data as res '
               'where valid.id_resultat=res.id_data and res.id_analyse=%s '
               'order by valid.id_data desc limit 1')

        cursor.execute(req, (id_ana,))

        return cursor.fetchone()

    @staticmethod
    def getListValidators(id_rec):
        cursor = DB.cursor()

        req = ('select vld.utilisateur as user, vld.commentaire as comment '
               'from sigl_10_data as vld '
               'inner join sigl_09_data as res on res.id_data = vld.id_resultat '
               'inner join sigl_04_data as req on req.id_data = res.id_analyse '
               'where req.id_dos=%s and vld.type_validation=252 '
               'group by vld.utilisateur, vld.commentaire order by vld.id_data ')

        cursor.execute(req, (id_rec,))

        return cursor.fetchall()

    @staticmethod
    def insertValidation(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into sigl_10_data '
                           '(id_owner, id_resultat, date_validation, utilisateur, valeur, type_validation, commentaire, motif_annulation) '
                           'values '
                           '(%(id_owner)s, %(id_resultat)s, %(date_validation)s, %(utilisateur)s, %(valeur)s, %(type_validation)s, %(commentaire)s, %(motif_annulation)s )', params)

            Result.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Result.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def deleteValidationByResult(id_res):
        try:
            cursor = DB.cursor()

            cursor.execute('select id_data '
                           'from sigl_10_data '
                           'where id_resultat=%s', (id_res,))

            l_valid = cursor.fetchall()

            for valid in l_valid:
                cursor.execute('insert into sigl_10_deleted '
                               '(id_data, id_owner, id_resultat, date_validation, utilisateur, valeur, type_validation, commentaire, motif_annulation ) '
                               'select id_data, id_owner, id_resultat, date_validation, utilisateur, valeur, type_validation, commentaire, motif_annulation '
                               'from sigl_10_data '
                               'where id_data=%s', (valid['id_data'],))

                cursor.execute('delete from sigl_10_data '
                               'where id_data=%s', (valid['id_data'],))

            Result.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Result.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def updateResult(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('update sigl_09_data set '
                           'id_owner=%(id_owner)s, '
                           'valeur=%(valeur)s '
                           'where id_data=%(id_data)s', params)

            Result.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Result.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getResultRecordForReport(id_rec):
        # sort and group id_fam by id_req_ana
        cursor = DB.cursor()

        req = ('select ref.famille as id_fam '
               'from sigl_04_data as req '
               'inner join sigl_02_data as rec on rec.id_data = req.id_dos '
               'inner join sigl_05_data as ref on req.ref_analyse = ref.id_data '
               'inner join sigl_09_data as res on req.id_data = res.id_analyse '
               'inner join sigl_07_data as var on var.id_data = res.ref_variable '
               'inner join sigl_05_07_data as link on var.id_data = link.id_refvariable '
               'and ref.id_data = link.id_refanalyse '
               'where req.id_dos=%s and res.valeur is not NULL and res.valeur != "" and res.valeur != 1013 '
               'group by ref.famille order by req.id_data asc')

        cursor.execute(req, (id_rec,))

        l_id_fam = cursor.fetchall()

        l_items = []

        for id_fam in l_id_fam:
            fam_cond = ' ref.famille=' + str(id_fam['id_fam'])

            # some analyzes doesnt have a family
            if not id_fam['id_fam']:
                fam_cond = ' ref.famille is null '

            # Note 1 : var.type_resultat=265 to get result of type labeled
            # Note 2 : res.valeur != 1013 to avoid unspecified result
            req = ('select req.ref_analyse as id_ref_ana, req.id_data as id_req_ana, rec.id_data as id_rec, rec.rec_modified, '
                   'ref.nom as ana_name, ref.commentaire as ana_comm, fam.label as ana_fam, res.id_data as id_res, '
                   'res.valeur as value, var.*, rec.num_dos_mois as rec_num_month, rec.num_dos_an as rec_num_year, '
                   'rec.date_dos as rec_date, rec.date_prescription as prescr_date, rec.statut as rec_stat, '
                   'req.req_outsourced as ana_outsourced, req.id_owner as id_owner, rec.id_patient as id_pat, '
                   'link.position as var_pos, link.var_qrcode '
                   'from sigl_04_data as req '
                   'inner join sigl_02_data as rec on rec.id_data = req.id_dos '
                   'inner join sigl_05_data as ref on req.ref_analyse = ref.id_data '
                   'left join sigl_dico_data as fam on fam.id_data = ref.famille '
                   'inner join sigl_09_data as res on req.id_data = res.id_analyse '
                   'inner join sigl_07_data as var on var.id_data = res.ref_variable '
                   'inner join sigl_05_07_data as link on var.id_data = link.id_refvariable '
                   'and ref.id_data = link.id_refanalyse '
                   'where req.id_dos=%s and ' + fam_cond + ' and (var.type_resultat=265 or '
                   '(res.valeur is not NULL and res.valeur != "" and res.valeur != 1013)) '
                   'order by id_req_ana asc,  ana_name asc, var_pos asc')

            cursor.execute(req, (id_rec,))

            l_items.extend(cursor.fetchall())

        return l_items

    @staticmethod
    def countResValidate(id_req_ana):
        cursor = DB.cursor()

        req = ('select count(*) as nb_vld '
               'from sigl_04_data as req '
               'inner join sigl_05_data as ref on ref.id_data = req.ref_analyse '
               'and (cote_unite is NULL or cote_unite != "PB") '
               'inner join sigl_09_data as res on res.id_analyse = req.id_data '
               'inner join sigl_10_data as vld on vld.id_resultat = res.id_data and vld.type_validation=252 '
               'where req.id_data=%s')

        cursor.execute(req, (id_req_ana,))

        return cursor.fetchone()

    @staticmethod
    def getDataset(date_beg, date_end):
        cursor = DB.cursor()

        req = ('select rec.id_data as id_analysis, rec.rec_custody, rec.id_patient, d_type.label as type, '
               'date_format(rec.date_dos, %s) as record_date, rec.num_dos_an as rec_num_year, '
               'rec.num_dos_jour as rec_num_day, rec.num_dos_mois as rec_num_month, rec.rec_modified, '
               'rec.med_prescripteur as id_doctor, doctor.nom as doctor_lname, doctor.prenom as doctor_fname, '
               'date_format(rec.date_prescription, %s) as prescription_date, rec.service_interne as internal_service, '
               'rec.num_lit as bed_num, rec.rec_hosp_num, rec.prix as price, rec.remise as discount, '
               'rec.remise_pourcent as discount_percent, rec.assu_pourcent as insurance_percent, rec.a_payer as to_pay, '
               'd_status.label as status, date_format(rec.date_hosp, %s) as hosp_date, '
               'req.ref_analyse as id_analysis, req.prix as ana_price, req.urgent as ana_emergency, '
               'req.req_outsourced as ana_outsourced, ref.code as analysis_code, ref.nom as analysis_name, '
               'd_fam.label as analysis_family, res.valeur as result_value, var.libelle as variable_name, '
               'var.type_resultat as type_result, d_unit.label as result_unit, '
               'date_format(pat.ddn, %s) as birth, pat.age, d_age_unit.label as age_unit, d_sex.label as sex, '
               'pat.tel as phone1, pat.pat_phone2 as phone2 '
               'from sigl_02_data as rec '
               'inner join sigl_04_data as req on req.id_dos=rec.id_data '
               'inner join sigl_05_data as ref on ref.id_data=req.ref_analyse '
               'left join sigl_dico_data as d_fam on d_fam.id_data=ref.famille and ref.famille > 0 '
               'left join sigl_dico_data as d_type on d_type.id_data=rec.type '
               'left join sigl_dico_data as d_status on d_status.id_data=rec.statut '
               'inner join sigl_09_data as res on req.id_data = res.id_analyse '
               'inner join sigl_07_data as var on var.id_data = res.ref_variable '
               'left join sigl_08_data as doctor on doctor.id_data=rec.med_prescripteur '
               'left join sigl_dico_data as d_unit on d_unit.id_data=var.unite '
               'inner join sigl_05_07_data as link on var.id_data = link.id_refvariable '
               'and ref.id_data = link.id_refanalyse '
               'inner join sigl_03_data as pat on pat.id_data=rec.id_patient '
               'left join sigl_dico_data as d_age_unit on d_age_unit.id_data=pat.unite '
               'left join sigl_dico_data as d_sex on d_sex.id_data=pat.sexe '
               'where rec.statut in (255, 256) and rec.date_dos between %s and %s '
               'order by rec.id_data desc')

        cursor.execute(req, (Constants.cst_isodate, Constants.cst_isodate, Constants.cst_isodate, Constants.cst_isodate, date_beg, date_end))

        return cursor.fetchall()
