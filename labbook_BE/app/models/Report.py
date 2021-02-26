# -*- coding:utf-8 -*-
import logging
import mysql.connector

from app.models.DB import DB
from app.models.Logs import Logs
from app.models.Constants import Constants


class Report:
    log = logging.getLogger('log_db')

    @staticmethod
    def getListEpidemio():
        cursor = DB.cursor()

        req = 'select epi.id_data, epi.id_owner, epi.surveillance as disease, epi.nature_prel as id_prod, '\
              'epi.dhis2_tab, epi.dhis2_tab_num, dict.label as product '\
              'from sigl_14_data as epi '\
              'left join sigl_dico_data as dict on dict.id_data = epi.nature_prel '\
              'where epi.surveillance is not NULL '\
              'order by disease asc'

        cursor.execute(req)

        return cursor.fetchall()

    @staticmethod
    def getStatEpidemio(id_disease):
        cursor = DB.cursor()

        req = 'select nom_amont as res_cat, formule as formula, id_surveillance as id_disease, '\
              'libelle_ind as res_label, nature_prel as id_prod '\
              'from sigl_15_data '\
              'where id_surveillance = %s '\
              'order by id_data asc'

        cursor.execute(req, (id_disease,))

        return cursor.fetchall()

    @staticmethod
    def getNbResultRecevied(l_id_var, id_prod, date_beg, date_end):
        cursor = DB.cursor()

        req = 'select count(distinct rec.id_data) as total '\
              'from sigl_02_data as rec '\
              'inner join sigl_04_data as ana on ana.id_dos = rec.id_data '\
              'inner join sigl_05_data as ref on ref.id_data = ana.ref_analyse '\
              'inner join sigl_09_data as res on res.id_analyse = ana.id_data '\
              'where (rec.date_dos between %s and %s) and ref.type_prel = %s '\
              'and res.ref_variable in ('

        for id_var in l_id_var:
            req = req + str(id_var) + ','

        req = req + '0)'

        cursor.execute(req, (date_beg, date_end, id_prod,))

        return cursor.fetchone()

    @staticmethod
    def getNbResultAnalyzed(l_id_var, id_prod, date_beg, date_end):
        cursor = DB.cursor()

        req = 'select count(distinct rec.id_data) as total '\
              'from sigl_02_data as rec '\
              'inner join sigl_04_data as ana on ana.id_dos = rec.id_data '\
              'inner join sigl_05_data as ref on ref.id_data = ana.ref_analyse '\
              'inner join sigl_09_data as res on res.id_analyse = ana.id_data '\
              'inner join sigl_10_data as vld on vld.id_resultat = res.id_data '\
              'where (rec.date_dos between %s and %s) and ref.type_prel = %s '\
              'and vld.type_validation = 252 and res.ref_variable in ('

        for id_var in l_id_var:
            req = req + str(id_var) + ','

        req = req + '0)'

        cursor.execute(req, (date_beg, date_end, id_prod,))

        return cursor.fetchone()

    @staticmethod
    def getResultEpidemio(**params):
        cursor = DB.cursor()

        req = ('select count(distinct rec.id_data) as value '
               'from sigl_02_data as rec ' + params['inner_req'] + ' '
               'where (rec.date_dos between %(date_beg)s and %(date_end)s) ' + params['end_req'])

        cursor.execute(req, params)

        return cursor.fetchone()

    @staticmethod
    def getStatPatient(date_beg, date_end):
        cursor = DB.cursor()

        req = 'select pat.sexe as sex, pat.age, count(*) as nb_rec, rec.type as rec_type '\
              'from sigl_02_data as rec '\
              'inner join sigl_03_data as pat on pat.id_data = rec.id_patient '\
              'where (rec.date_dos between %s and %s) '\
              'group by pat.age order by age asc'

        cursor.execute(req, (date_beg, date_end,))

        return cursor.fetchall()

    @staticmethod
    def getStatPrescr(date_beg, date_end):
        cursor = DB.cursor()

        req = 'select doctor.nom as lastname, doctor.prenom as firstname, count(*) as nb_rec '\
              'from sigl_02_data as rec '\
              'left join sigl_08_data as doctor on doctor.id_data = rec.med_prescripteur '\
              'where (date_prescription between %s and %s) '\
              'group by doctor.id_data asc order by lastname asc, firstname asc'

        cursor.execute(req, (date_beg, date_end,))

        return cursor.fetchall()

    @staticmethod
    def getStatSampler(date_beg, date_end):
        cursor = DB.cursor()

        req = 'select preleveur as sampler, count(*) as nb_prod '\
              'from sigl_01_data '\
              'where (date_prel between %s and %s) '\
              'group by sampler asc order by sampler asc'

        cursor.execute(req, (date_beg, date_end,))

        return cursor.fetchall()

    @staticmethod
    def getStatProduct(date_beg, date_end):
        cursor = DB.cursor()

        req = 'select dict.label as product, count(*) as nb_prod '\
              'from sigl_01_data as prod '\
              'inner join sigl_dico_data as dict on dict.id_data = prod.type_prel '\
              'where (prod.date_prel between %s and %s) '\
              'group by product asc order by product asc'

        cursor.execute(req, (date_beg, date_end,))

        return cursor.fetchall()

    @staticmethod
    def getBillingStatus(date_beg, date_end, id_user):
        cursor = DB.cursor()

        cond = ''

        if id_user > 0:
            cond = ' and user.id_data=' + str(id_user) + ' '

        req = ('select rec.id_data, rec.num_dos_jour as rec_num, rec.num_fact as bill_num, '
               'rec.prix as bill_price, rec.a_payer as bill_remain, rec.num_quittance as receipt_num '
               'from sigl_02_data as rec '
               'inner join sigl_user_data as user on rec.id_owner=user.id_group '
               'where (rec.date_dos between %s and %s) ' + cond +
               'order by rec.id_data asc limit 7000')

        cursor.execute(req, (date_beg, date_end,))

        return cursor.fetchall()

    @staticmethod
    def getTodayList(date_beg, date_end):
        cursor = DB.cursor()

        req = ('select rec.id_data, rec.date_dos as rec_date, ref.nom as analysis, dict_fam.label as family, '
               'if(param_num_rec.periode=1070, if(param_num_rec.format=1072,substring(rec.num_dos_mois from 7), '
               'rec.num_dos_mois), '
               'if(param_num_rec.format=1072, substring(rec.num_dos_an from 5), rec.num_dos_an)) as rec_num, '
               'group_concat(distinct dict.label order by dict.position asc separator ", ") as vld_type '
               'from `sigl_10_data` as vld '
               'inner join sigl_dico_data AS dict on dict.id_data=vld.type_validation '
               'inner join sigl_09_data as res on res.id_data=vld.id_resultat '
               'inner join sigl_04_data as ana on ana.id_data=res.id_analyse '
               'inner join sigl_05_data as ref on ref.id_data=ana.ref_analyse '
               'inner join sigl_02_data as rec on rec.id_data=ana.id_dos '
               'left join sigl_param_num_dos_data AS param_num_rec on param_num_rec.id_data=1 '
               'left join sigl_dico_data as dict_fam on dict_fam.id_data=ref.famille '
               'where (rec.date_dos between %s and %s) '
               'group by ana.id_data order by rec.id_data asc limit 7000')

        cursor.execute(req, (date_beg, date_end,))

        return cursor.fetchall()

    @staticmethod
    def getIdValueForFormula(dict_name, code):
        cursor = DB.cursor()

        req = ('select id_data '
               'from sigl_dico_data '
               'where dico_name = %s and code = %s')

        cursor.execute(req, (dict_name, code,))

        return cursor.fetchone()

    @staticmethod
    def ParseFormula(formula):
        req = {}

        if formula != 'N/A':
            idx = 0

            req['inner'] = ('inner join sigl_04_data as ana' + str(idx) +
                            ' on ana' + str(idx) + '.id_dos = rec.id_data '
                            'inner join sigl_05_data as ref' + str(idx) +
                            ' on ref' + str(idx) + '.id_data = ana' + str(idx) + '.ref_analyse '
                            'inner join sigl_09_data as res' + str(idx) +
                            ' on res' + str(idx) + '.id_analyse = ana' + str(idx) + '.id_data '
                            'inner join sigl_10_data as vld' + str(idx) +
                            ' on vld' + str(idx) + '.id_resultat = res' + str(idx) + '.id_data ')

            req['end'] = (' and ref' + str(idx) + '.type_prel=%(id_prod)s and vld' + str(idx) + '.type_validation=252 ')

            formula = ' '.join(formula.split())  # take off redundant white space
            formula = formula.replace(', ', ',')
            l_words = formula.split(' ')

            # Report.log.error('l_words=' + str(l_words))

            for word in l_words:
                # id_var pattern
                if word.startswith('$_'):
                    # Report.log.error('### id_var pattern ###')
                    # Report.log.error('word = ' + word)
                    id_var = ''

                    idx_beg = word.find('$_')

                    if idx_beg >= 0:
                        idx_beg = idx_beg + 2
                        id_var = word[idx_beg:]

                    if id_var:
                        req['end'] = req['end'] + ' and res' + str(idx) + '.ref_variable=' + id_var + ' and res' + str(idx) + '.valeur '

                # [dict_name.code] pattern
                elif word.startswith('[') and word.endswith(']'):
                    # Report.log.error('### [dict_name.code] pattern ###')
                    # Report.log.error('word = ' + word)
                    id_val = Report.ParseDictVar(word)

                    if id_val:
                        req['end'] = req['end'] + str(id_val)

                # list of [dict_name.code] pattern
                elif word.startswith('([') and word.endswith('])'):
                    # Report.log.error('### list of [dict_name.code] pattern ###')
                    # Report.log.error('word = ' + word)
                    l_dict_var = word[1:len(word) - 1]  # take off bracket
                    l_dict_var = l_dict_var.split(',')

                    req['end'] = req['end'] + '('
                    for dict_var in l_dict_var:
                        id_val = Report.ParseDictVar(dict_var)

                        if id_val:
                            req['end'] = req['end'] + str(id_val) + ','

                    req['end'] = req['end'][:len(req['end']) - 1] + ')'
                else:
                    # TODO rule for OR
                    if word == 'OR':
                        return req

                    # add a another inner group
                    if word == 'AND':
                        idx = idx + 1

                        req['inner'] = (req['inner'] +
                                        'inner join sigl_04_data as ana' + str(idx) +
                                        ' on ana' + str(idx) + '.id_dos = rec.id_data '
                                        'inner join sigl_05_data as ref' + str(idx) +
                                        ' on ref' + str(idx) + '.id_data = ana' + str(idx) + '.ref_analyse '
                                        'inner join sigl_09_data as res' + str(idx) +
                                        ' on res' + str(idx) + '.id_analyse = ana' + str(idx) + '.id_data '
                                        'inner join sigl_10_data as vld' + str(idx) +
                                        ' on vld' + str(idx) + '.id_resultat = res' + str(idx) + '.id_data ')

                        req['end'] = (req['end'] + ' ' + word + ' ref' + str(idx) + '.type_prel=%(id_prod)s and vld' + str(idx) + '.type_validation=252 ')

                    # Report.log.error('###  ELSE ###')
                    # Report.log.error('word = ' + word)
                    if word != 'AND':
                        req['end'] = req['end'] + ' ' + word + ' '

        return req

    @staticmethod
    def ParseDictVar(dict_var):
        res = 0

        # [dict_name.code] pattern
        if dict_var.startswith('[') and dict_var.endswith(']'):
            dict_name = ''
            code      = ''

            idx_beg = dict_var.find("[")

            if idx_beg >= 0:
                idx_end = dict_var.find(".", idx_beg)
                idx_beg = idx_beg + 1
                if idx_end > idx_beg:
                    dict_name = str(dict_var[idx_beg:idx_end])
                    code      = str(dict_var[idx_end + 1:len(dict_var) - 1])

                    # Report.log.error('dict_name=' + dict_name)
                    # Report.log.error('code=' + code)

            id_val = Report.getIdValueForFormula(dict_name, code)

            # Report.log.error('id_val=' + str(id_val))

            if id_val:
                res = id_val['id_data']

        return res
