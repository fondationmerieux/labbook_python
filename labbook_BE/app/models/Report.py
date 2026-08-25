# -*- coding:utf-8 -*-
import logging

from app.models.DB import DB
from app.models.Setting import Setting


AND = ' and '
OR  = ' or '


class Report:
    log = logging.getLogger('log_db')

    @staticmethod
    def getNbResultRecevied(l_id_var, id_prod, date_beg, date_end, lite_filter='A', lite_user_id=0):
        cursor = DB.cursor()

        req = ('select count(distinct rec.id_data) as total '
               'from sigl_02_data as rec '
               'inner join sigl_04_data as req on req.id_dos = rec.id_data '
               'inner join sigl_05_data as ref on ref.id_data = req.ref_analyse '
               'inner join sigl_09_data as res on res.id_analyse = req.id_data '
               'where (rec.rec_date_receipt between %s and %s) and ref.type_prel = %s '
               'and res.ref_variable in (')

        for id_var in l_id_var:
            req = req + str(id_var) + ','

        req = req + '0)'

        lf = (lite_filter or 'A').upper()
        try:
            lite_user_id = int(lite_user_id)
        except Exception:
            lite_user_id = 0

        if lf == 'N':
            req += ' and rec.rec_lite = 0'
        elif lf == 'Y':
            req += ' and rec.rec_lite > 0'
            if lite_user_id > 0:
                req += ' and rec.id_owner = ' + str(lite_user_id)

        cursor.execute(req, (date_beg, date_end, id_prod,))

        return cursor.fetchone()

    @staticmethod
    def getNbResultReceviedV2(l_id_var, l_id_prod, date_beg, date_end, lite_filter='A', lite_user_id=0):
        cursor = DB.cursor()

        cond_id_prod = ''
        for id_prod in l_id_prod:
            if not cond_id_prod:
                cond_id_prod = '('
            cond_id_prod += str(id_prod) + ','

        if cond_id_prod:
            cond_id_prod = cond_id_prod[:-1] + ')'
        else:
            cond_id_prod = '(0)'

        req = ('select count(distinct rec.id_data) as total '
               'from sigl_02_data as rec '
               'inner join sigl_04_data as req on req.id_dos = rec.id_data '
               'inner join sigl_05_data as ref on ref.id_data = req.ref_analyse '
               'inner join sigl_09_data as res on res.id_analyse = req.id_data '
               'where (rec.rec_date_receipt between %s and %s) and ref.type_prel in ' + cond_id_prod + ' '
               'and res.ref_variable in (')

        for id_var in l_id_var:
            req = req + str(id_var) + ','

        req = req + '0)'

        lf = (lite_filter or 'A').upper()
        try:
            lite_user_id = int(lite_user_id)
        except Exception:
            lite_user_id = 0

        if lf == 'N':
            req += ' and rec.rec_lite = 0'
        elif lf == 'Y':
            req += ' and rec.rec_lite > 0'
            if lite_user_id > 0:
                req += ' and rec.id_owner = ' + str(lite_user_id)

        cursor.execute(req, (date_beg, date_end,))

        return cursor.fetchone()

    @staticmethod
    def getNbResultAnalyzed(l_id_var, id_prod, date_beg, date_end, lite_filter='A', lite_user_id=0):
        cursor = DB.cursor()

        req = ('select count(distinct rec.id_data) as total '
               'from sigl_02_data as rec '
               'inner join sigl_04_data as req on req.id_dos = rec.id_data '
               'inner join sigl_05_data as ref on ref.id_data = req.ref_analyse '
               'inner join sigl_09_data as res on res.id_analyse = req.id_data '
               'inner join sigl_10_data as vld on vld.id_resultat = res.id_data '
               'where (rec.rec_date_receipt between %s and %s) and ref.type_prel = %s '
               'and vld.type_validation = 252 and res.ref_variable in (')

        for id_var in l_id_var:
            req = req + str(id_var) + ','

        req = req + '0)'

        lf = (lite_filter or 'A').upper()
        try:
            lite_user_id = int(lite_user_id)
        except Exception:
            lite_user_id = 0

        if lf == 'N':
            req += ' and rec.rec_lite = 0'
        elif lf == 'Y':
            req += ' and rec.rec_lite > 0'
            if lite_user_id > 0:
                req += ' and rec.id_owner = ' + str(lite_user_id)

        cursor.execute(req, (date_beg, date_end, id_prod,))

        return cursor.fetchone()

    @staticmethod
    def getNbResultAnalyzedV2(l_id_var, l_id_prod, date_beg, date_end, lite_filter='A', lite_user_id=0):
        cursor = DB.cursor()

        cond_id_prod = ''
        for id_prod in l_id_prod:
            if not cond_id_prod:
                cond_id_prod = '('
            cond_id_prod += str(id_prod) + ','

        if cond_id_prod:
            cond_id_prod = cond_id_prod[:-1] + ')'
        else:
            cond_id_prod = '(0)'

        req = ('select count(distinct rec.id_data) as total '
               'from sigl_02_data as rec '
               'inner join sigl_04_data as req on req.id_dos = rec.id_data '
               'inner join sigl_05_data as ref on ref.id_data = req.ref_analyse '
               'inner join sigl_09_data as res on res.id_analyse = req.id_data '
               'inner join sigl_10_data as vld on vld.id_resultat = res.id_data '
               'where (rec.rec_date_receipt between %s and %s) and ref.type_prel in ' + cond_id_prod + ' '
               'and vld.type_validation = 252 and res.ref_variable in (')

        for id_var in l_id_var:
            req = req + str(id_var) + ','

        req = req + '0)'

        lf = (lite_filter or 'A').upper()
        try:
            lite_user_id = int(lite_user_id)
        except Exception:
            lite_user_id = 0

        if lf == 'N':
            req += ' and rec.rec_lite = 0'
        elif lf == 'Y':
            req += ' and rec.rec_lite > 0'
            if lite_user_id > 0:
                req += ' and rec.id_owner = ' + str(lite_user_id)

        cursor.execute(req, (date_beg, date_end,))

        return cursor.fetchone()

    """ OLD FUNCTION 23/09/2025
    @staticmethod
    def getResultEpidemio(**params):
        cursor = DB.cursor()

        req = ('select count(distinct rec.id_data) as value '
               'from sigl_02_data as rec ' + params['inner_req'] + ' '
               'where (rec.rec_date_receipt between %(date_beg)s and %(date_end)s) ' + params['end_req'])

        # rec_type filter option
        sql_params = dict(params)
        rec_type = params.get('rec_type')
        rec_type_code = 183 if rec_type == 'E' else (184 if rec_type == 'I' else None)

        if rec_type_code is not None:
            req += ' and rec.type = %(rec_type_code)s'
            sql_params['rec_type_code'] = rec_type_code

        Report.log.info('----------------------------------')
        Report.log.info('getResultEpidemio req=' + str(req))

        cursor.execute(req, params)

        return cursor.fetchone()"""

    @staticmethod
    def getResultIndicator(**params):
        cursor = DB.cursor()

        req = ('select count(distinct rec.id_data) as value '
               'from sigl_02_data as rec ' + params['inner_req'] + ' '
               'where (rec.rec_date_receipt between %(date_beg)s and %(date_end)s) ' + params['end_req'])

        lite_filter = params.get('lite_filter', 'A') or 'A'
        lite_user_id = params.get('lite_user_id', 0) or 0
        try:
            lite_user_id = int(lite_user_id)
        except Exception:
            lite_user_id = 0

        lf = lite_filter.upper()
        if lf == 'N':
            req += ' and rec.rec_lite = 0'
        elif lf == 'Y':
            req += ' and rec.rec_lite > 0'
            if lite_user_id > 0:
                req += ' and rec.id_owner = %(lite_user_id)s'
                params['lite_user_id'] = lite_user_id

        Report.log.info('----------------------------------')
        Report.log.info('getResultIndicator req=' + str(req))

        cursor.execute(req, params)

        return cursor.fetchone()

    @staticmethod
    def getActivityAge(date_beg, date_end, type_ana, lite_filter='A', lite_user_id=0):
        cursor = DB.cursor()

        cond = ''

        if type_ana > 0:
            cond = ' and ana.famille= ' + str(type_ana) + ' '

        # LabBook Lite filter: A = all, N = exclude Lite, Y = only Lite
        lf = (lite_filter or 'A').upper()
        if lf == 'N':
            cond += ' and (rec.rec_lite <= 0 or rec.rec_lite is null) '
        elif lf == 'Y':
            cond += ' and rec.rec_lite > 0 '
            try:
                lite_user_id_int = int(lite_user_id)
            except Exception:
                lite_user_id_int = 0
            if lite_user_id_int > 0:
                cond += ' and rec.id_owner=' + str(lite_user_id_int) + ' '

        req = (
            'select ana.nom as analysis, ana.code as code, pat.sexe as sex, pat.age, pat.unite, count(*) as nb_ana '
            'from sigl_02_data as rec '
            'inner join sigl_03_data as pat on pat.id_data = rec.id_patient '
            'inner join sigl_04_data as req on req.id_dos = rec.id_data '
            'inner join sigl_05_data as ana on ana.id_data = req.ref_analyse and ana.cote_unite != "PB" '
            'inner join ('
            '  select id_analyse, max(id_data) as res_id_data '
            '  from sigl_09_data where valeur is not null '
            '  group by id_analyse'
            ') as res on res.id_analyse = req.id_data '
            'where (rec.rec_date_receipt between %s and %s) and rec.statut in (255,256) ' + cond +
            ' and exists ('
            '   select 1 from sigl_10_data vld '
            '   where vld.id_resultat = res.res_id_data and vld.type_validation = 252'
            ' ) '
            'group by ana.id_data, pat.unite, pat.age, pat.sexe '
            'order by ana.nom asc'
        )

        cursor.execute(req, (date_beg, date_end,))
        return cursor.fetchall()

    @staticmethod
    def getActivityType(date_beg, date_end, type_ana, lite_filter='A', lite_user_id=0):
        cursor = DB.cursor()

        cond = ''

        if type_ana > 0:
            cond = ' and ana.famille= ' + str(type_ana) + ' '

        # LabBook Lite filter: A = all, N = exclude Lite, Y = only Lite
        lf = (lite_filter or 'A').upper()
        if lf == 'N':
            cond += ' and (rec.rec_lite <= 0 or rec.rec_lite is null) '
        elif lf == 'Y':
            cond += ' and rec.rec_lite > 0 '
            try:
                lite_user_id_int = int(lite_user_id)
            except Exception:
                lite_user_id_int = 0
            if lite_user_id_int > 0:
                cond += ' and rec.id_owner=' + str(lite_user_id_int) + ' '

        req = (
            'select ana.nom as analysis, ana.code as code, pat.sexe as sex, rec.type as rec_type, '
            'count(*) as nb_ana, rec.rec_custody '
            'from sigl_02_data as rec '
            'inner join sigl_03_data as pat on pat.id_data = rec.id_patient '
            'inner join sigl_04_data as req on req.id_dos = rec.id_data '
            'inner join sigl_05_data as ana on ana.id_data = req.ref_analyse and ana.cote_unite != "PB" '
            'inner join ('
            '  select id_analyse, max(id_data) as res_id_data '
            '  from sigl_09_data where valeur is not null '
            '  group by id_analyse'
            ') as res on res.id_analyse = req.id_data '
            'where (rec.rec_date_receipt between %s and %s) and rec.statut in (255,256) ' + cond +
            ' and exists ('
            '   select 1 from sigl_10_data vld '
            '   where vld.id_resultat = res.res_id_data and vld.type_validation = 252'
            ' ) '
            'group by ana.id_data, rec.type, pat.sexe order by ana.nom asc'
        )

        cursor.execute(req, (date_beg, date_end,))
        return cursor.fetchall()

    @staticmethod
    def getStatPatient(date_beg, date_end, service_int, lite_filter='A', lite_user_id=0):
        cursor = DB.cursor()

        cond = ''

        if service_int:
            cond += ' and rec.service_interne like "' + str(service_int) + '%" '

        lf = lite_filter.upper()
        if lf == 'N':
            cond += ' and rec.rec_lite = 0'
        elif lf == 'Y':
            cond += ' and rec.rec_lite > 0'
            if lite_user_id > 0:
                cond += ' and rec.id_owner = ' + str(lite_user_id)

        req = ('select pat.sexe as sex, pat.age, count(*) as nb_rec, rec.type as rec_type '
               'from sigl_02_data as rec '
               'inner join sigl_03_data as pat on pat.id_data = rec.id_patient '
               'where (rec.rec_date_receipt between %s and %s) ' + cond +
               ' group by pat.age order by age asc')

        cursor.execute(req, (date_beg, date_end,))

        return cursor.fetchall()

    @staticmethod
    def getStatPrescr(date_beg, date_end, service_int, lite_filter='A', lite_user_id=0):
        cursor = DB.cursor()

        cond = ''

        if service_int:
            cond += ' and rec.service_interne like "' + str(service_int) + '%" '

        lf = lite_filter.upper()
        if lf == 'N':
            cond += ' and rec.rec_lite = 0'
        elif lf == 'Y':
            cond += ' and rec.rec_lite > 0'
            if lite_user_id > 0:
                cond += ' and rec.id_owner = ' + str(lite_user_id)

        req = ('select doctor.nom as lastname, doctor.prenom as firstname, count(*) as nb_rec '
               'from sigl_02_data as rec '
               'inner join sigl_08_data as doctor on doctor.id_data = rec.med_prescripteur '
               'where (date_prescription between %s and %s) ' + cond +
               ' group by doctor.id_data order by lastname asc, firstname asc')

        cursor.execute(req, (date_beg, date_end,))

        return cursor.fetchall()

    @staticmethod
    def getStatSampler(date_beg, date_end, lite_filter='A', lite_user_id=0):
        cursor = DB.cursor()

        cond = ''

        lf = (lite_filter or 'A').upper()
        try:
            lite_user_id = int(lite_user_id)
        except Exception:
            lite_user_id = 0

        if lf == 'N':
            cond += ' and prod.id_owner = 0'
        elif lf == 'Y':
            cond += ' and prod.id_owner > 0'
            if lite_user_id > 0:
                cond += ' and prod.id_owner = ' + str(lite_user_id)

        req = ('select preleveur as sampler, count(*) as nb_prod '
               'from sigl_01_data as prod '
               'where (samp_date between %s and %s) ' + cond +
               ' group by sampler order by sampler asc')

        cursor.execute(req, (date_beg, date_end,))

        return cursor.fetchall()

    @staticmethod
    def getStatProduct(date_beg, date_end, lite_filter='A', lite_user_id=0):
        cursor = DB.cursor()

        cond = ''

        lf = (lite_filter or 'A').upper()
        try:
            lite_user_id = int(lite_user_id)
        except Exception:
            lite_user_id = 0

        if lf == 'N':
            cond += ' and prod.id_owner = 0'
        elif lf == 'Y':
            cond += ' and prod.id_owner > 0'
            if lite_user_id > 0:
                cond += ' and prod.id_owner = ' + str(lite_user_id)

        req = ('select dict.label as product, count(*) as nb_prod '
               'from sigl_01_data as prod '
               'inner join sigl_dico_data as dict on dict.id_data = prod.type_prel '
               'where (prod.samp_date between %s and %s) and statut=8 ' + cond +
               ' group by product order by product asc')

        cursor.execute(req, (date_beg, date_end,))

        return cursor.fetchall()

    @staticmethod
    def getStatNbPat(date_beg, date_end, service_int, lite_filter='A', lite_user_id=0):
        cursor = DB.cursor()

        cond = ''

        if service_int:
            cond += ' and rec.service_interne like "' + str(service_int) + '%" '

        lf = lite_filter.upper()
        if lf == 'N':
            cond += ' and rec.rec_lite = 0'
        elif lf == 'Y':
            cond += ' and rec.rec_lite > 0'
            if lite_user_id > 0:
                cond += ' and rec.id_owner = ' + str(lite_user_id)

        req = ('select pat.sexe as sex, rec.type, rec_custody, rec.statut '
               'from sigl_02_data as rec '
               'inner join sigl_03_data as pat on pat.id_data = rec.id_patient '
               'where (rec.rec_date_receipt between %s and %s) ' + cond +
               ' order by pat.sexe asc, rec.type asc, rec_custody asc')

        cursor.execute(req, (date_beg, date_end,))

        return cursor.fetchall()

    @staticmethod
    def getStatNbAna(date_beg, date_end, service_int, lite_filter='A', lite_user_id=0):
        cursor = DB.cursor()

        cond = ''

        if service_int:
            cond += ' and rec.service_interne like "' + str(service_int) + '%" '

        req = ('select pat.sexe as sex, rec.type, rec_custody '
               'from sigl_02_data as rec '
               'inner join sigl_03_data as pat on pat.id_data = rec.id_patient '
               'inner join sigl_04_data as req on req.id_dos = rec.id_data '
               'inner join sigl_05_data as ana on ana.id_data = req.ref_analyse '
               'where (rec.rec_date_receipt between %s and %s) and ana.cote_unite != "PB" ' + cond +
               ' order by pat.sexe asc, rec.type asc, rec_custody asc')

        cursor.execute(req, (date_beg, date_end,))

        return cursor.fetchall()

    @staticmethod
    def getBillingStatus(date_beg, date_end, id_user):
        cursor = DB.cursor()

        cond = ''

        if id_user > 0:
            cond = ' and rec.id_owner=' + str(id_user) + ' '

        req = ('select rec.id_data, rec.num_dos_jour as rec_num, rec.num_fact as bill_num, '
               'rec.prix as bill_price, rec.a_payer as bill_remain, rec.num_quittance as receipt_num '
               'from sigl_02_data as rec '
               'where (rec.rec_date_receipt between %s and %s) ' + cond +
               ' order by rec.id_data asc limit 7000')

        cursor.execute(req, (date_beg, date_end,))

        return cursor.fetchall()

    @staticmethod
    def getTodayList(date_beg, date_end, service_int):
        cursor = DB.cursor()

        cond = ''

        if service_int:
            cond += ' and rec.service_interne like "' + str(service_int) + '%" '

        req = ('select rec.id_data as id_rec, rec.type as type_rec, rec.rec_date_receipt as rec_date, ref.nom as analysis, dict_fam.label as family, '
               'if(rec_setting.rstg_period=1070, if(rec_setting.rstg_format=1072,substring(rec.num_dos_mois from 7), '
               'rec.num_dos_mois), '
               'if(rec_setting.rstg_format=1072, substring(rec.num_dos_an from 7), rec.num_dos_an)) as rec_num, '
               'group_concat(distinct dict.label order by dict.position asc separator ", ") as vld_type '
               'from `sigl_10_data` as vld '
               'inner join sigl_dico_data as dict on dict.id_data=vld.type_validation '
               'inner join sigl_09_data as res on res.id_data=vld.id_resultat '
               'inner join sigl_04_data as req on req.id_data=res.id_analyse '
               'inner join sigl_05_data as ref on ref.id_data=req.ref_analyse '
               'inner join sigl_02_data as rec on rec.id_data=req.id_dos '
               'left join record_setting as rec_setting on rec_setting.rstg_ser=1 '
               'left join sigl_dico_data as dict_fam on dict_fam.id_data=ref.famille '
               'where (rec.rec_date_receipt between %s and %s) ' + cond +
               ' group by req.id_data order by rec.id_data asc limit 7000')

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

    """ OLD FUNCTION 23/09/2025
    @staticmethod
    def ParseFormula(formula, id_prod):
        # used by export DHIS2 and Epidemio
        req = {}

        if formula != 'N/A':
            idx = 0

            req['inner'] = ('inner join sigl_04_data as req' + str(idx) +
                            ' on req' + str(idx) + '.id_dos = rec.id_data '
                            'inner join sigl_05_data as ref' + str(idx) +
                            ' on ref' + str(idx) + '.id_data = req' + str(idx) + '.ref_analyse '
                            'inner join sigl_09_data as res' + str(idx) +
                            ' on res' + str(idx) + '.id_analyse = req' + str(idx) + '.id_data '
                            'inner join sigl_10_data as vld' + str(idx) +
                            ' on vld' + str(idx) + '.id_resultat = res' + str(idx) + '.id_data ')

            # open first parenthesis, closed at the end
            req['end'] = (' and (')

            formula = ' '.join(formula.split())  # take off redundant white space
            formula = formula.replace(', ', ',')
            l_words = formula.split(' ')

            Report.log.info('l_words=' + str(l_words))

            for word in l_words:
                Report.log.info('DEBUG word = ' + str(word))

                # id_var pattern
                if word.startswith('$_'):
                    # Report.log.info('### id_var pattern ###')
                    # Report.log.info('word = ' + word)
                    id_var = ''

                    idx_beg = word.find('$_')

                    if idx_beg >= 0:
                        idx_beg = idx_beg + 2
                        id_var = word[idx_beg:]

                    if id_var:
                        if int(id_prod) == 0:
                            req['end'] = req['end'] + (' (vld' + str(idx) + '.type_validation=252 ')
                        else:
                            req['end'] = req['end'] + (' (ref' + str(idx) + '.type_prel=' + str(id_prod) + ' and vld' + str(idx) + '.type_validation=252 ')
                        req['end'] = req['end'] + ' and res' + str(idx) + '.ref_variable=' + id_var + ' and res' + str(idx) + '.valeur '
                    Report.log.info('DEBUG pattern $_x req end = ' + str(req['end']))

                # {id_var,id_var,...} pattern
                elif word.startswith('{') and word.endswith('}'):
                    # Report.log.info('### {id_var,id_var,...} pattern ###')
                    # Report.log.info('word = ' + word)
                    l_id_var = word[1:-1].split(',')

                    # Report.log.info('l_id_var=' + str(l_id_var))

                    if int(id_prod) == 0:
                        req['end'] = req['end'] + (' (vld' + str(idx) + '.type_validation=252 ')
                    else:
                        req['end'] = req['end'] + (' (ref' + str(idx) + '.type_prel=' + str(id_prod) + ' and vld' + str(idx) + '.type_validation=252 ')

                    first_id_var = False

                    for id_var in l_id_var:
                        if not first_id_var:
                            req['end'] = req['end'] + 'and ('
                            first_id_var = True

                        req['end'] = req['end'] + 'res' + str(idx) + '.ref_variable=' + id_var + OR

                    # take of last 'or' and add a ')'
                    req['end'] = req['end'][:-3] + ') and res' + str(idx) + '.valeur '

                    Report.log.info('DEBUG pattern {} req end = ' + str(req['end']))

                # [dict_name.code] pattern
                elif word.startswith('[') and word.endswith(']'):
                    # Report.log.info('### [dict_name.code] pattern ###')
                    # Report.log.info('word = ' + word)
                    id_val = Report.ParseDictVar(word)

                    if id_val:
                        req['end'] = req['end'] + str(id_val)

                    Report.log.info('DEBUG pattern [] req end = ' + str(req['end']))

                # list of [dict_name.code] pattern
                elif word.startswith('([') and word.endswith('])'):
                    # Report.log.info('### list of [dict_name.code] pattern ###')
                    # Report.log.info('word = ' + word)
                    l_dict_var = word[1:len(word) - 1]  # take off bracket
                    l_dict_var = l_dict_var.split(',')

                    req['end'] = req['end'] + '('
                    for dict_var in l_dict_var:
                        id_val = Report.ParseDictVar(dict_var)

                        if id_val:
                            req['end'] = req['end'] + str(id_val) + ','

                    req['end'] = req['end'][:len(req['end']) - 1] + ')'

                    Report.log.info('DEBUG pattern ([]) req end = ' + str(req['end']))
                # ON a list of analyzes codes
                elif word.startswith('ON(') and word.endswith(')'):
                    # Report.log.info('### list of analyzes codes ON(Bxxx,Bxxx) pattern ###')
                    l_code_ana = list(word[3:len(word) - 1].split(','))
                    # Report.log.info('l_code_ana = ' + str(l_code_ana))
                    l_cond_ana = ''

                    i = 0
                    for code_ana in l_code_ana:
                        if i == 0:
                            l_cond_ana = str(code_ana)
                        else:
                            l_cond_ana = l_cond_ana + ', ' + str(code_ana)

                        i = i + 1

                    req['end'] = req['end'] + ' and ref' + str(idx) + '.code IN (' + l_cond_ana + ')'

                    Report.log.info('DEBUG pattern ON() req end = ' + str(req['end']))

                # CAT filter on category like SEX and/or AGE
                elif word.startswith('CAT(') and word.endswith(')'):
                    # Report.log.info('### list of category CAT(SEX_x,AGE_x) pattern ###')
                    l_cat = list(word[4:len(word) - 1].split(','))
                    # Report.log.info('l_cat = ' + str(l_cat))
                    sex = 0
                    age_min = 0
                    age_max = 0
                    for cat in l_cat:
                        if cat.startswith('SEX_'):
                            if cat.endswith('M'):
                                sex = 1
                            elif cat.endswith('F'):
                                sex = 2
                            else:
                                sex = 3
                        elif cat.startswith('AGE_'):
                            num_cat_age = int(cat[4:]) - 1  # AGE_1 <=> interval 0 in list of interval
                            l_interval = Setting.getAgeInterval()

                            if num_cat_age < 0 or num_cat_age >= len(l_interval):
                                Report.log.error('ERROR wrong num_cat AGE=' + str(num_cat_age))
                                return req

                            i = 0
                            for interval in l_interval:
                                if i == num_cat_age:
                                    age_min = interval['ais_lower_bound']
                                    age_max = interval['ais_upper_bound']

                                    if not age_min:
                                        age_min = 0

                                    if not age_max:
                                        age_max = 150

                                i = i + 1
                        elif cat.startswith('AGE['):
                            idx_age_beg = cat.find('[')
                            idx_age_mid = cat.find('-')
                            idx_age_end = cat.find(']')

                            age_min = cat[idx_age_beg + 1:idx_age_mid]
                            age_max = cat[idx_age_mid + 1:idx_age_end]
                        else:
                            Report.log.error('ERROR CAT unknown cat=' + str(cat))

                    # Build SQL part for category
                    req['inner'] = (req['inner'] +
                                    'inner join sigl_03_data as pat' + str(idx) +
                                    ' on pat' + str(idx) + '.id_data=rec.id_patient ')

                    if sex > 0:
                        req['end'] = req['end'] + ') and (pat' + str(idx) + '.sexe=' + str(sex)

                    if age_min != 0 or age_max != 0:
                        req['end'] = (req['end'] + ') and (pat' + str(idx) + '.age >=' + str(age_min) +
                                      ' and pat' + str(idx) + '.age <=' + str(age_max))

                    Report.log.info('DEBUG pattern CAT() req end = ' + str(req['end']))

                # opening parenthesis to frame a block
                elif word == '(':
                    req['end'] = req['end'] + '( '

                    Report.log.info('DEBUG pattern ( req end = ' + str(req['end']))
                # closing parenthesis to frame a block
                elif word == ')':
                    req['end'] = req['end'] + ' )'

                    Report.log.info('DEBUG pattern ) req end = ' + str(req['end']))
                # double-quoted string literal: "text"
                elif len(word) >= 2 and word[0] == '"' and word[-1] == '"':
                    # strip outer double quotes and emit as SQL single-quoted literal
                    literal = word[1:-1]
                    # keep it safe if there is any single quote inside the value
                    req['end'] = req['end'] + " '" + literal.replace("'", "''") + "' "
                    Report.log.info('DEBUG pattern "string" req end = ' + str(req['end']))
                else:
                    if word == 'OR':
                        idx = idx + 1

                        req['inner'] = (req['inner'] +
                                        'inner join sigl_04_data as req' + str(idx) +
                                        ' on req' + str(idx) + '.id_dos = rec.id_data '
                                        'inner join sigl_05_data as ref' + str(idx) +
                                        ' on ref' + str(idx) + '.id_data = req' + str(idx) + '.ref_analyse '
                                        'inner join sigl_09_data as res' + str(idx) +
                                        ' on res' + str(idx) + '.id_analyse = req' + str(idx) + '.id_data '
                                        'inner join sigl_10_data as vld' + str(idx) +
                                        ' on vld' + str(idx) + '.id_resultat = res' + str(idx) + '.id_data ')

                        # same id_prod with OR

                        req['end'] = req['end'] + ') ' + word

                        Report.log.info('DEBUG pattern OR req end = ' + str(req['end']))

                    # add a another inner group
                    if word == 'AND':
                        idx = idx + 1

                        req['inner'] = (req['inner'] +
                                        'inner join sigl_04_data as req' + str(idx) +
                                        ' on req' + str(idx) + '.id_dos = rec.id_data '
                                        'inner join sigl_05_data as ref' + str(idx) +
                                        ' on ref' + str(idx) + '.id_data = req' + str(idx) + '.ref_analyse '
                                        'inner join sigl_09_data as res' + str(idx) +
                                        ' on res' + str(idx) + '.id_analyse = req' + str(idx) + '.id_data '
                                        'inner join sigl_10_data as vld' + str(idx) +
                                        ' on vld' + str(idx) + '.id_resultat = res' + str(idx) + '.id_data ')

                        req['end'] = req['end'] + ') ' + word

                        Report.log.info('DEBUG pattern AND req end = ' + str(req['end']))

                    # Report.log.info('###  ELSE ###')
                    # Report.log.info('word = ' + word)
                    if word != 'AND' and word != 'OR':
                        req['end'] = req['end'] + ' ' + word + ' '

                        Report.log.info('DEBUG pattern other req end = ' + str(req['end']))

            # close first parenthesis and last parenthesis of last block
            req['end'] = req['end'] + '))'

            Report.log.info('DEBUG END req end = ' + str(req['end']))

        return req"""

    @staticmethod
    def ParseFormulaV2(formula, l_id_prod):
        # used by export Indicator
        req = {}

        if formula != 'N/A':
            idx = 0

            req['inner'] = ('inner join sigl_04_data as req' + str(idx) +
                            ' on req' + str(idx) + '.id_dos = rec.id_data '
                            'inner join sigl_05_data as ref' + str(idx) +
                            ' on ref' + str(idx) + '.id_data = req' + str(idx) + '.ref_analyse '
                            'inner join sigl_09_data as res' + str(idx) +
                            ' on res' + str(idx) + '.id_analyse = req' + str(idx) + '.id_data '
                            'inner join sigl_10_data as vld' + str(idx) +
                            ' on vld' + str(idx) + '.id_resultat = res' + str(idx) + '.id_data ')

            id_prod = l_id_prod[idx]

            # open first parenthesis, closed at the end
            req['end'] = (' and (')

            formula = ' '.join(formula.split())  # take off redundant white space
            formula = formula.replace(', ', ',')
            l_words = formula.split(' ')

            Report.log.info('l_words=' + str(l_words))

            for word in l_words:
                Report.log.info('DEBUG word = ' + str(word))

                # id_var pattern
                if word.startswith('$_'):
                    # Report.log.info('### id_var pattern ###')
                    # Report.log.info('word = ' + word)
                    id_var = ''

                    idx_beg = word.find('$_')

                    if idx_beg >= 0:
                        idx_beg = idx_beg + 2
                        id_var = word[idx_beg:]

                    if id_var:
                        if int(id_prod) == 0:
                            req['end'] = req['end'] + (' (vld' + str(idx) + '.type_validation=252 ')
                        else:
                            req['end'] = req['end'] + (' (ref' + str(idx) + '.type_prel=' + str(id_prod) + ' and vld' + str(idx) + '.type_validation=252 ')
                        req['end'] = req['end'] + ' and res' + str(idx) + '.ref_variable=' + id_var + ' and res' + str(idx) + '.valeur '
                    Report.log.info('DEBUG 01 req end = ' + str(req['end']))

                # {id_var,id_var,...} pattern
                elif word.startswith('{') and word.endswith('}'):
                    # Report.log.info('### {id_var,id_var,...} pattern ###')
                    # Report.log.info('word = ' + word)
                    l_id_var = word[1:-1].split(',')

                    # Report.log.info('l_id_var=' + str(l_id_var))

                    if int(id_prod) == 0:
                        req['end'] = req['end'] + (' (vld' + str(idx) + '.type_validation=252 ')
                    else:
                        req['end'] = req['end'] + (' (ref' + str(idx) + '.type_prel=' + str(id_prod) + ' and vld' + str(idx) + '.type_validation=252 ')

                    first_id_var = False

                    for id_var in l_id_var:
                        if not first_id_var:
                            req['end'] = req['end'] + 'and ('
                            first_id_var = True

                        req['end'] = req['end'] + 'res' + str(idx) + '.ref_variable=' + id_var + OR

                    # take of last 'or' and add a ')'
                    req['end'] = req['end'][:-3] + ') and res' + str(idx) + '.valeur '

                    Report.log.info('DEBUG 02 req end = ' + str(req['end']))

                # [dict_name.code] pattern
                elif word.startswith('[') and word.endswith(']'):
                    # Report.log.info('### [dict_name.code] pattern ###')
                    # Report.log.info('word = ' + word)
                    id_val = Report.ParseDictVar(word)

                    if id_val:
                        req['end'] = req['end'] + str(id_val)

                    Report.log.info('DEBUG 03 req end = ' + str(req['end']))

                # list of [dict_name.code] pattern
                elif word.startswith('([') and word.endswith('])'):
                    # Report.log.info('### list of [dict_name.code] pattern ###')
                    # Report.log.info('word = ' + word)
                    l_dict_var = word[1:len(word) - 1]  # take off bracket
                    l_dict_var = l_dict_var.split(',')

                    req['end'] = req['end'] + '('
                    for dict_var in l_dict_var:
                        id_val = Report.ParseDictVar(dict_var)

                        if id_val:
                            req['end'] = req['end'] + str(id_val) + ','

                    req['end'] = req['end'][:len(req['end']) - 1] + ')'

                    Report.log.info('DEBUG 04 req end = ' + str(req['end']))

                # ON a list of analyzes codes
                elif word.startswith('ON(') and word.endswith(')'):
                    # Report.log.info('### list of analyzes codes ON(Bxxx,Bxxx) pattern ###')
                    l_code_ana = list(word[3:len(word) - 1].split(','))
                    # Report.log.info('l_code_ana = ' + str(l_code_ana))
                    l_cond_ana = ''

                    i = 0
                    for code_ana in l_code_ana:
                        if i == 0:
                            l_cond_ana = str(code_ana)
                        else:
                            l_cond_ana = l_cond_ana + ', ' + str(code_ana)

                        i = i + 1

                    req['end'] = req['end'] + ' and ref' + str(idx) + '.code IN (' + l_cond_ana + ')'

                    Report.log.info('DEBUG 05 req end = ' + str(req['end']))

                # CAT filter on category like SEX and/or AGE
                elif word.startswith('CAT(') and word.endswith(')'):
                    # Report.log.info('### list of category CAT(SEX_x,AGE_x) pattern ###')
                    l_cat = list(word[4:len(word) - 1].split(','))
                    # Report.log.info('l_cat = ' + str(l_cat))
                    sex = 0
                    age_min = 0
                    age_max = 0
                    for cat in l_cat:
                        if cat.startswith('SEX_'):
                            if cat.endswith('M'):
                                sex = 1
                            elif cat.endswith('F'):
                                sex = 2
                            else:
                                sex = 3
                        elif cat.startswith('AGE_'):
                            num_cat_age = int(cat[4:]) - 1  # AGE_1 <=> interval 0 in list of interval
                            l_interval = Setting.getAgeInterval()

                            if num_cat_age < 0 or num_cat_age >= len(l_interval):
                                Report.log.error('ERROR wrong num_cat AGE=' + str(num_cat_age))
                                return req

                            i = 0
                            for interval in l_interval:
                                if i == num_cat_age:
                                    age_min = interval['ais_lower_bound']
                                    age_max = interval['ais_upper_bound']

                                    if not age_min:
                                        age_min = 0

                                    if not age_max:
                                        age_max = 150

                                i = i + 1
                        elif cat.startswith('AGE['):
                            idx_age_beg = cat.find('[')
                            idx_age_mid = cat.find('-')
                            idx_age_end = cat.find(']')

                            age_min = cat[idx_age_beg + 1:idx_age_mid]
                            age_max = cat[idx_age_mid + 1:idx_age_end]
                        else:
                            Report.log.error('ERROR CAT unknown cat=' + str(cat))

                    # Build SQL part for category
                    req['inner'] = (req['inner'] +
                                    'inner join sigl_03_data as pat' + str(idx) +
                                    ' on pat' + str(idx) + '.id_data=rec.id_patient ')

                    if sex > 0:
                        req['end'] = req['end'] + ') and (pat' + str(idx) + '.sexe=' + str(sex)

                    if age_min != 0 or age_max != 0:
                        req['end'] = (req['end'] + ') and (pat' + str(idx) + '.age >=' + str(age_min) +
                                      ' and pat' + str(idx) + '.age <=' + str(age_max))

                    Report.log.info('DEBUG 06 req end = ' + str(req['end']))

                # opening parenthesis to frame a block
                elif word.startswith('('):
                    req['end'] = req['end'] + '( '

                    Report.log.info('DEBUG 07 req end = ' + str(req['end']))
                # closing parenthesis to frame a block
                elif word.startswith(')'):
                    req['end'] = req['end'] + ' )'

                    Report.log.info('DEBUG 08 req end = ' + str(req['end']))
                # double-quoted string literal: "text"
                elif len(word) >= 2 and word[0] == '"' and word[-1] == '"':
                    # strip outer double quotes and emit as SQL single-quoted literal
                    literal = word[1:-1]
                    # keep it safe if there is any single quote inside the value
                    req['end'] = req['end'] + " '" + literal.replace("'", "''") + "' "
                    Report.log.info('DEBUG 09 pattern "string" req end = ' + str(req['end']))
                else:
                    if word == 'OR':
                        idx = idx + 1

                        req['inner'] = (req['inner'] +
                                        'inner join sigl_04_data as req' + str(idx) +
                                        ' on req' + str(idx) + '.id_dos = rec.id_data '
                                        'inner join sigl_05_data as ref' + str(idx) +
                                        ' on ref' + str(idx) + '.id_data = req' + str(idx) + '.ref_analyse '
                                        'inner join sigl_09_data as res' + str(idx) +
                                        ' on res' + str(idx) + '.id_analyse = req' + str(idx) + '.id_data '
                                        'inner join sigl_10_data as vld' + str(idx) +
                                        ' on vld' + str(idx) + '.id_resultat = res' + str(idx) + '.id_data ')

                        req['end'] = req['end'] + ') ' + word

                        Report.log.info('DEBUG 09 req end = ' + str(req['end']))

                    # add a another inner group
                    if word == 'AND':
                        idx = idx + 1

                        req['inner'] = (req['inner'] +
                                        'inner join sigl_04_data as req' + str(idx) +
                                        ' on req' + str(idx) + '.id_dos = rec.id_data '
                                        'inner join sigl_05_data as ref' + str(idx) +
                                        ' on ref' + str(idx) + '.id_data = req' + str(idx) + '.ref_analyse '
                                        'inner join sigl_09_data as res' + str(idx) +
                                        ' on res' + str(idx) + '.id_analyse = req' + str(idx) + '.id_data '
                                        'inner join sigl_10_data as vld' + str(idx) +
                                        ' on vld' + str(idx) + '.id_resultat = res' + str(idx) + '.id_data ')

                        id_prod = l_id_prod[idx]

                        req['end'] = req['end'] + ') ' + word

                        Report.log.info('DEBUG 10 req end = ' + str(req['end']))

                    # Report.log.info('###  ELSE ###')
                    # Report.log.info('word = ' + word)
                    if word != 'AND' and word != 'OR':
                        req['end'] = req['end'] + ' ' + word + ' '
                        Report.log.info('DEBUG 11 req end = ' + str(req['end']))

            # close first parenthesis and last parenthesis of last block
            req['end'] = req['end'] + '))'

            Report.log.info('DEBUG END req end = ' + str(req['end']))

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

                    # Report.log.info('dict_name=' + dict_name)
                    # Report.log.info('code=' + code)

            id_val = Report.getIdValueForFormula(dict_name, code)

            # Report.log.info('id_val=' + str(id_val))

            if id_val:
                res = id_val['id_data']
            else:
                Report.log.error('ERROR dict value missing id_val=' + str(id_val) +
                                 ' for getIdValueForFormula(' + str(dict_name) + ', ' + str(code) + ')')

        return res

    @staticmethod
    def getTAT(date_beg, date_end, type_ana, id_ana, code_pat, rec_num, lite_filter='A', lite_user_id=0):
        cursor = DB.cursor()

        cond = ''

        if rec_num:
            cond += (' and (rec.num_dos_an LIKE "%' + str(rec_num) + '%" or rec.num_dos_mois LIKE "%' +
                     str(rec_num) + '%" or rec.rec_num_int LIKE "%' + str(rec_num) + '%") ')

        if id_ana:
            cond += ' and req.ref_analyse=' + str(id_ana) + ' '
        elif type_ana:
            cond += ' and fam.id_data=' + str(type_ana) + ' '

        if code_pat:
            cond += ' and (pat.code like "' + str(code_pat) + '%" or pat.code_patient like "' + str(code_pat) + '%") '

        # LabBook Lite filter on record
        lf = (lite_filter or 'A').upper()
        try:
            lite_user_id = int(lite_user_id)
        except Exception:
            lite_user_id = 0

        if lf == 'N':
            cond += ' and rec.rec_lite = 0'
        elif lf == 'Y':
            cond += ' and rec.rec_lite > 0'
            if lite_user_id > 0:
                cond += ' and rec.id_owner = ' + str(lite_user_id)

        req = ('select rec.rec_date_save, rec.rec_date_vld, rec.rec_num_int, rec.id_data as rec_id, rec.type as rec_type, '
               'if(rec_setting.rstg_period=1070, if(rec_setting.rstg_format=1072,substring(rec.num_dos_mois from 7), '
               'rec.num_dos_mois), if(rec_setting.rstg_format=1072, substring(rec.num_dos_an from 7), rec.num_dos_an)) '
               'as rec_num, if(rec_setting.rstg_period=1070, rec.num_dos_mois, rec.num_dos_an) as rec_num_long, '
               'rec.rec_date_receipt as rec_date, pat.nom as pat_name, pat.prenom as pat_firstname, pat.code as pat_code, '
               'pat.code_patient as pat_code_lab, ana.nom as ana_name, ana.code as ana_code, ana.ana_loinc, '
               'req.id_data as id_req '
               'from sigl_04_data as req '
               'inner join sigl_02_data as rec on rec.id_data = req.id_dos '
               'inner join sigl_03_data as pat on pat.id_data = rec.id_patient '
               'inner join sigl_05_data as ana on ana.id_data = req.ref_analyse '
               'left join sigl_dico_data as fam on fam.id_data = ana.famille '
               'left join record_setting as rec_setting on rec_setting.rstg_ser=1 '
               'where (rec.rec_date_receipt between %s and %s) and ana.cote_unite != "PB" and rec.statut=256 ' + cond +
               ' order by rec.id_data desc')

        cursor.execute(req, (date_beg, date_end,))

        return cursor.fetchall()

    @staticmethod
    def ParseFormula(formula: str, sample_type_id: int) -> dict:
        """
        Build EXISTS subqueries from DHIS2 filter syntax.
        Returns: {"exists_subqueries": [ "<SELECT 1 ... WHERE ...>", ... ]}
        One subquery per top-level OR group.
        """
        # --- helpers ---------------------------------------------------------
        def normalize_spaces(text: str) -> str:
            return ' '.join(text.split())

        def split_top_level_or(expr: str) -> list:
            """Split on OR at top level (outside parentheses)."""
            parts, depth, current = [], 0, []
            tokens = expr.replace('(', ' ( ').replace(')', ' ) ').split()
            i = 0
            while i < len(tokens):
                tok = tokens[i]
                if tok == '(':
                    depth += 1
                elif tok == ')':
                    depth -= 1
                if depth == 0 and tok.upper() == 'OR':
                    parts.append(' '.join(current).strip())
                    current = []
                else:
                    current.append(tok)
                i += 1
            if current:
                parts.append(' '.join(current).strip())
            return parts

        def distribute_leading_group(expr: str) -> str:
            """
            Rewrite "(A OR B) SUFFIX" into "A SUFFIX OR B SUFFIX".

            Parentheses alone would hide the OR from split_top_level_or, and every part
            would then be joined with AND, which no record can satisfy. Distributing what
            follows the group falls back on the repeated form, which is handled correctly.
            """
            text = expr.strip()

            if not text.startswith('('):
                return expr

            # find the parenthesis closing the leading group
            depth = 0
            close = -1
            for pos, char in enumerate(text):
                if char == '(':
                    depth += 1
                elif char == ')':
                    depth -= 1
                    if depth == 0:
                        close = pos
                        break

            if close < 0:
                Report.log.error("Unbalanced parenthesis in formula=%s", expr)
                return expr

            inner = text[1:close].strip()
            suffix = text[close + 1:].strip()

            # nothing to distribute, or no OR to protect: leave the formula untouched
            if not suffix or len(split_top_level_or(inner)) < 2:
                return expr

            return OR.join(f'{part} {suffix}'.strip() for part in split_top_level_or(inner))

        def parse_dictionary_token(dict_token: str) -> str:
            """
            [dictName.code] -> numeric value via existing Report.ParseDictVar
            """
            value = Report.ParseDictVar(dict_token)  # existing function
            return str(value) if value is not None else ''

        def sql_quote_string_literal(value: str) -> str:
            """Return SQL-safe single-quoted literal."""
            return "'" + value.replace("'", "''") + "'"

        def new_alias_set(index: int) -> dict:
            """Return aliases for one measurement constraint."""
            return {
                "req": f"req{index}",
                "ref": f"ref{index}",
                "res": f"res{index}",
                "vld": f"vld{index}",
            }

        def collect_parenthesized(tokens: list, open_paren_index: int) -> tuple:
            """Return inner text and index of the closing ')' starting at tokens[open_paren_index] which must be '('."""
            depth = 0
            j = open_paren_index + 1
            inner = []
            while j < len(tokens):
                t = tokens[j]
                if t == '(':
                    depth += 1
                    inner.append(t)
                elif t == ')':
                    if depth == 0:
                        return ' '.join(inner).strip(), j
                    depth -= 1
                    inner.append(t)
                else:
                    inner.append(t)
                j += 1
            Report.log.error("Unbalanced parentheses after function-like token")
            return '', open_paren_index

        def build_required_joins(aliases: dict, include_req_join: bool) -> str:
            """
            Build INNER JOIN chain for one measurement.
            If include_req_join is False, the req alias must appear in FROM.
            """
            parts = []
            if include_req_join:
                parts.append(
                    f" inner join sigl_04_data as {aliases['req']} on {aliases['req']}.id_dos = rec.id_data"
                )
            parts.append(
                f" inner join sigl_05_data as {aliases['ref']} on {aliases['ref']}.id_data = {aliases['req']}.ref_analyse"
            )
            parts.append(
                f" inner join sigl_09_data as {aliases['res']} on {aliases['res']}.id_analyse = {aliases['req']}.id_data"
            )
            parts.append(
                f" inner join sigl_10_data as {aliases['vld']} on {aliases['vld']}.id_resultat = {aliases['res']}.id_data"
            )
            return ''.join(parts)

        def start_measurement_conditions(aliases: dict, variable_id: int) -> list:
            """Base predicates for one $_<id> measurement."""
            conditions = []
            if int(sample_type_id) == 0:
                conditions.append(f"{aliases['vld']}.type_validation=252")
            else:
                conditions.append(f"{aliases['ref']}.type_prel={int(sample_type_id)}")
                conditions.append(f"{aliases['vld']}.type_validation=252")
            if variable_id:
                conditions.append(f"{aliases['res']}.ref_variable={int(variable_id)}")
            return conditions

        def apply_on_clause(aliases: dict, token: str, where_atoms: list):
            """
            Inject ref.code IN (...) into the last measurement atom.
            If no atom exists, append as standalone predicate.
            """
            raw_list = token[3:-1].strip()  # remove ON( ... )
            predicate = f"{aliases['ref']}.code IN ({raw_list})"
            # try to inject inside the last (...) atom
            for idx in range(len(where_atoms) - 1, -1, -1):
                atom = where_atoms[idx]
                if atom.startswith('(') and atom.endswith(')'):
                    where_atoms[idx] = atom[:-1] + f" and {predicate})"
                    return
            # fallback
            where_atoms.append(predicate)

        def ensure_patient_join(state: dict):
            """Add patient join once for the group."""
            if not state["patient_join_added"]:
                state["joins"].append(
                    f" inner join sigl_03_data as {state['patient_alias']} on {state['patient_alias']}.id_data=rec.id_patient"
                )
                state["patient_join_added"] = True

        def apply_cat_clause(state: dict, token: str):
            """
            CAT(...) -> patient-level filters
            CAT(SEX_M), CAT(SEX_F), CAT(AGE_n), CAT(AGE[a-b])
            """
            content = token[4:-1]  # inside CAT(...)
            parts = [p.strip() for p in content.split(',') if p.strip()]

            for item in parts:
                if item == 'SEX_M':
                    ensure_patient_join(state)
                    state["patient_conditions"].append(f"{state['patient_alias']}.sexe=1")
                elif item == 'SEX_F':
                    ensure_patient_join(state)
                    state["patient_conditions"].append(f"{state['patient_alias']}.sexe=2")
                elif item.startswith('AGE_'):
                    # AGE_N mapping from settings (1-based index)
                    num_cat = int(item[4:]) - 1
                    intervals = Setting.getAgeInterval()
                    if 0 <= num_cat < len(intervals):
                        age_min = intervals[num_cat]['ais_lower_bound'] or 0
                        age_max = intervals[num_cat]['ais_upper_bound'] or 150
                        ensure_patient_join(state)
                        state["patient_conditions"].append(
                            f"{state['patient_alias']}.age >={int(age_min)} and {state['patient_alias']}.age <={int(age_max)}"
                        )
                    else:
                        Report.log.error(f"ERROR wrong AGE category: {item}")
                elif item.startswith('AGE[') and item.endswith(']'):
                    brk1 = item.find('[')
                    brk2 = item.find('-')
                    brk3 = item.find(']')
                    age_min = int(item[brk1 + 1:brk2])
                    age_max = int(item[brk2 + 1:brk3])
                    ensure_patient_join(state)
                    state["patient_conditions"].append(
                        f"{state['patient_alias']}.age >={age_min} and {state['patient_alias']}.age <={age_max}"
                    )
                else:
                    Report.log.error(f"ERROR CAT unknown item: {item}")

        # --- main ------------------------------------------------------------
        if not formula or formula.strip().upper() == 'N/A':
            return {"exists_subqueries": []}

        formula = normalize_spaces(formula)
        formula = distribute_leading_group(formula)
        or_groups = split_top_level_or(formula)

        exists_subqueries = []

        for group_index, group_expr in enumerate(or_groups):
            alias_counter = 0
            current_aliases = None
            group_state = {
                "joins": [],
                "where_atoms": [],
                "patient_conditions": [],
                "patient_alias": f"pat{group_index}",
                "patient_join_added": False,
                "first_req_alias": None,  # will host the FROM alias
            }

            tokens = group_expr.replace('(', ' ( ').replace(')', ' ) ').split()
            i = 0
            while i < len(tokens):
                token = tokens[i]

                if token in ('(', ')'):
                    group_state["where_atoms"].append(token)
                    i += 1
                    continue

                upper_token = token.upper()
                if upper_token in ('AND', 'OR'):
                    group_state["where_atoms"].append(upper_token)
                    i += 1
                    continue

                if token.startswith('$_'):
                    variable_id = int(token[2:])
                    current_aliases = new_alias_set(alias_counter)
                    alias_counter += 1

                    # first measurement -> req goes in FROM, no join for req here
                    if group_state["first_req_alias"] is None:
                        group_state["first_req_alias"] = current_aliases['req']
                        group_state["joins"].append(
                            build_required_joins(current_aliases, include_req_join=False)
                        )
                    else:
                        group_state["joins"].append(
                            build_required_joins(current_aliases, include_req_join=True)
                        )

                    base_conditions = start_measurement_conditions(current_aliases, variable_id)

                    if i + 1 >= len(tokens):
                        Report.log.error("error on this formula=%s", formula)
                        Report.log.error("Unexpected end of tokens after variable id")
                        break

                    operator_token = tokens[i + 1].upper()

                    if operator_token in ('=', '!=', '<', '<=', '>', '>='):
                        if i + 2 >= len(tokens):
                            Report.log.error("Missing value after operator")
                            break
                        raw_value = tokens[i + 2]

                        if raw_value.startswith('[') and raw_value.endswith(']'):
                            value_for_sql = parse_dictionary_token(raw_value)
                            value_predicate = f"{current_aliases['res']}.valeur {operator_token} {value_for_sql}"
                        elif len(raw_value) >= 2 and raw_value[0] == '"' and raw_value[-1] == '"':
                            literal = raw_value[1:-1]
                            value_predicate = (
                                f"LOWER({current_aliases['res']}.valeur) {operator_token} LOWER({sql_quote_string_literal(literal)})"
                            )
                        else:
                            value_predicate = f"{current_aliases['res']}.valeur {operator_token} {raw_value}"

                        atom = '(' + AND.join(base_conditions + [value_predicate]) + ')'
                        group_state["where_atoms"].append(atom)
                        i += 3
                        continue

                    elif operator_token == 'IN' or (operator_token == 'NOT' and i + 2 < len(tokens) and tokens[i + 2].upper() == 'IN'):
                        # Handle: $_123 IN (...)  and  $_123 NOT IN (...)
                        not_prefix = (operator_token == 'NOT')
                        in_index = i + 2 if not_prefix else i + 1

                        # Expect '(' right after IN
                        if in_index + 1 >= len(tokens) or tokens[in_index + 1] != '(':
                            Report.log.error("IN/NOT IN without '('")
                            break

                        # Capture everything until the matching ')'
                        inner_text, close_idx = collect_parenthesized(tokens, in_index + 1)  # content without the outer pair
                        if inner_text == '':
                            Report.log.error("IN/NOT IN empty list")
                            break

                        # Map each item: [DICT.CODE] -> numeric id, "str" -> quoted, others pass-through
                        items = [s.strip() for s in inner_text.split(',') if s.strip()]
                        mapped = []
                        for it in items:
                            if it.startswith('[') and it.endswith(']'):
                                mapped.append(parse_dictionary_token(it))
                            elif len(it) >= 2 and it[0] == '"' and it[-1] == '"':
                                mapped.append(sql_quote_string_literal(it[1:-1]))
                            else:
                                mapped.append(it)

                        in_pred = f"{current_aliases['res']}.valeur IN ({', '.join(mapped)})"
                        if not_prefix:
                            in_pred = f"NOT ({in_pred})"

                        atom = '(' + AND.join(base_conditions + [in_pred]) + ')'
                        group_state["where_atoms"].append(atom)

                        # Consume up to the matching ')'
                        i = close_idx + 1
                        continue

                    elif tokens[i + 1].startswith('[') and tokens[i + 1].endswith(']'):
                        dict_value = parse_dictionary_token(tokens[i + 1])
                        atom = '(' + AND.join(base_conditions + [f"{current_aliases['res']}.valeur = {dict_value}"]) + ')'
                        group_state["where_atoms"].append(atom)
                        i += 2
                        continue

                    else:
                        # "$_123" alone, as documented in doc/dhis2.md: the result only has to
                        # exist, no value comparison. The next token (ON(...), CAT(...), AND...)
                        # is handled on the following pass and injected into this atom.
                        atom = '(' + AND.join(base_conditions) + ')'
                        group_state["where_atoms"].append(atom)
                        i += 1
                        continue

                elif token.startswith('{'):
                    # Merge tokens until closing '}' to support "{391, 344}" split as "{391," + "344}"
                    brace = token
                    while not brace.strip().endswith('}') and i + 1 < len(tokens):
                        i += 1
                        brace += ' ' + tokens[i]
                    brace = brace.strip()
                    if not brace.endswith('}'):
                        Report.log.error(f"Unbalanced curly list near: {brace}")
                        i += 1
                        continue

                    # Now we have the full "{...}" block
                    inner = brace[1:-1].replace(', ', ',')
                    var_ids = [t.strip() for t in inner.split(',') if t.strip()]

                    current_aliases = new_alias_set(alias_counter)
                    alias_counter += 1

                    if group_state["first_req_alias"] is None:
                        group_state["first_req_alias"] = current_aliases['req']
                        group_state["joins"].append(
                            build_required_joins(current_aliases, include_req_join=False)
                        )
                    else:
                        group_state["joins"].append(
                            build_required_joins(current_aliases, include_req_join=True)
                        )

                    base = start_measurement_conditions(current_aliases, variable_id=0)
                    or_parts = [f"{current_aliases['res']}.ref_variable={int(v)}" for v in var_ids]
                    atom = '(' + AND.join(base + ['(' + OR.join(or_parts) + ')']) + ')'
                    group_state["where_atoms"].append(atom)
                    i += 1
                    continue

                elif upper_token == 'ON':
                    # Expect '(' then a list of codes until the matching ')'
                    if i + 1 < len(tokens) and tokens[i + 1] == '(':
                        inner_text, close_idx = collect_parenthesized(tokens, i + 1)

                        # Ensure we have a current measurement alias to attach ON(...) to
                        if current_aliases is None:
                            current_aliases = new_alias_set(alias_counter)
                            alias_counter += 1
                            if group_state["first_req_alias"] is None:
                                group_state["first_req_alias"] = current_aliases['req']
                                group_state["joins"].append(
                                    build_required_joins(current_aliases, include_req_join=False)
                                )
                            else:
                                group_state["joins"].append(
                                    build_required_joins(current_aliases, include_req_join=True)
                                )
                            base_conditions = start_measurement_conditions(current_aliases, variable_id=0)
                            group_state["where_atoms"].append('(' + AND.join(base_conditions + ['1=1']) + ')')

                        # Rebuild the function call text and inject into the last measurement atom
                        apply_on_clause(current_aliases, f"ON({inner_text})", group_state["where_atoms"])
                        i = close_idx + 1
                        continue
                    else:
                        Report.log.error("ON without parenthesis")
                        i += 1
                        continue

                elif upper_token == 'CAT':
                    if i + 1 < len(tokens) and tokens[i + 1] == '(':
                        inner_text, close_idx = collect_parenthesized(tokens, i + 1)
                        apply_cat_clause(group_state, f"CAT({inner_text})")
                        i = close_idx + 1
                        continue
                    else:
                        Report.log.error("CAT without parenthesis")
                        i += 1
                        continue

                elif len(token) >= 2 and token[0] == '"' and token[-1] == '"':
                    group_state["where_atoms"].append(sql_quote_string_literal(token[1:-1]))
                    i += 1
                    continue

                else:
                    group_state["where_atoms"].append(token)
                    i += 1

            # build the EXISTS subquery for this OR group
            join_sql = ''.join(group_state["joins"])
            where_parts = []
            if group_state["where_atoms"]:
                where_parts.append(' '.join(group_state["where_atoms"]))
            if group_state["patient_conditions"]:
                where_parts.append(AND.join(group_state["patient_conditions"]))
            final_where = AND.join([p for p in where_parts if p]) or '1=1'

            base_req = group_state["first_req_alias"] or "req0"

            # ensure correlation with outer rec
            correlation = f"{base_req}.id_dos = rec.id_data"
            where_clause = f"{correlation} AND {final_where}" if final_where else correlation

            subquery = (
                f"SELECT 1 FROM sigl_04_data as {base_req}"
                f"{join_sql}"
                f" WHERE {where_clause} LIMIT 1"
            )

            exists_subqueries.append(subquery)

        return {"exists_subqueries": exists_subqueries}

    @staticmethod
    def getResultEpidemio(req_part, date_beg, date_end, rec_type=None, lite_filter="A", lite_user_id=0):
        """
        Execute COUNT(DISTINCT rec.id_data) with EXISTS subqueries built by ParseFormula.
        Always return {"value": <int>}.
        """
        cursor = DB.cursor()

        sql = (
            "SELECT COUNT(DISTINCT rec.id_data) AS value "
            "FROM sigl_02_data AS rec "
            "WHERE (rec.rec_date_receipt BETWEEN %(date_beg)s AND %(date_end)s)"
        )
        sql_params = {"date_beg": date_beg, "date_end": date_end}

        rec_type_code = 183 if rec_type == 'E' else (184 if rec_type == 'I' else None)
        if rec_type_code is not None:
            sql += " AND rec.type = %(rec_type_code)s"
            sql_params["rec_type_code"] = rec_type_code

        # LabBook Lite filter:
        #  - 'A' (All): no lite filter unless lite_user_id > 0
        #  - 'N' (Exclude Lite): rec.rec_lite = 0
        #  - 'Y' (Only Lite): rec.rec_lite > 0, and optionally filter by id_owner
        lf = (lite_filter or 'A').upper()
        try:
            lite_uid = int(lite_user_id)
        except Exception:
            lite_uid = 0

        if lf == 'N':
            sql += " AND rec.rec_lite = 0"
        elif lf == 'Y':
            sql += " AND rec.rec_lite > 0"
            if lite_uid > 0:
                sql += " AND rec.id_owner = %(lite_uid)s"
                sql_params["lite_uid"] = lite_uid
        elif lf == 'A' and lite_uid > 0:
            sql += " AND rec.rec_lite > 0 AND rec.id_owner = %(lite_uid)s"
            sql_params["lite_uid"] = lite_uid

        exists_parts = []
        if req_part and "exists_subqueries" in req_part:
            exists_parts = req_part["exists_subqueries"]

        if exists_parts:
            exists_sql = " OR ".join([f"EXISTS ({subq})" for subq in exists_parts])
            sql += f" AND ({exists_sql})"

        Report.log.info('getResultEpidemio (EXISTS) sql=' + sql)
        cursor.execute(sql, sql_params)
        row = cursor.fetchone()

        # normalize to dict with 'value'
        if row is None:
            return {"value": 0}
        if isinstance(row, dict):
            return {"value": row.get("value", 0)}
        if isinstance(row, (list, tuple)) and len(row) > 0:
            return {"value": row[0]}
        try:
            return {"value": int(row)}
        except Exception:
            Report.log.error(f"Unexpected row type from cursor.fetchone(): {type(row)} -> {row}")
            return {"value": 0}
