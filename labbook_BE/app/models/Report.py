# -*- coding:utf-8 -*-
import logging

from app.models.DB import DB
from app.models.Setting import Setting


class Report:
    log = logging.getLogger('log_db')

    @staticmethod
    def getNbResultRecevied(l_id_var, id_prod, date_beg, date_end):
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

        cursor.execute(req, (date_beg, date_end, id_prod,))

        return cursor.fetchone()

    @staticmethod
    def getNbResultReceviedV2(l_id_var, l_id_prod, date_beg, date_end):
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

        cursor.execute(req, (date_beg, date_end,))

        return cursor.fetchone()

    @staticmethod
    def getNbResultAnalyzed(l_id_var, id_prod, date_beg, date_end):
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

        cursor.execute(req, (date_beg, date_end, id_prod,))

        return cursor.fetchone()

    @staticmethod
    def getNbResultAnalyzedV2(l_id_var, l_id_prod, date_beg, date_end):
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

        cursor.execute(req, (date_beg, date_end,))

        return cursor.fetchone()

    @staticmethod
    def getResultEpidemio(**params):
        cursor = DB.cursor()

        req = ('select count(distinct rec.id_data) as value '
               'from sigl_02_data as rec ' + params['inner_req'] + ' '
               'where (rec.rec_date_receipt between %(date_beg)s and %(date_end)s) ' + params['end_req'])

        Report.log.info('----------------------------------')
        Report.log.info('getResultEpidemio req=' + str(req))

        cursor.execute(req, params)

        return cursor.fetchone()

    @staticmethod
    def getResultIndicator(**params):
        cursor = DB.cursor()

        req = ('select count(distinct rec.id_data) as value '
               'from sigl_02_data as rec ' + params['inner_req'] + ' '
               'where (rec.rec_date_receipt between %(date_beg)s and %(date_end)s) ' + params['end_req'])

        Report.log.info('----------------------------------')
        Report.log.info('getResultIndicator req=' + str(req))

        cursor.execute(req, params)

        return cursor.fetchone()

    @staticmethod
    def getActivityAge(date_beg, date_end, type_ana):
        cursor = DB.cursor()

        cond = ''

        if type_ana > 0:
            cond = ' and ana.famille= ' + str(type_ana) + ' '

        req = ('select ana.nom as analysis, ana.code as code, pat.sexe as sex, pat.age, pat.unite, count(*) as nb_ana '
               'from sigl_02_data as rec '
               'inner join sigl_03_data as pat on pat.id_data = rec.id_patient '
               'inner join sigl_04_data as req on req.id_dos = rec.id_data '
               'inner join sigl_05_data as ana on ana.id_data = req.ref_analyse and ana.cote_unite != "PB" '
               'inner join (select id_analyse, min(id_data) as min_id_data from sigl_09_data where valeur is not null '
               'group by id_analyse) as res on res.id_analyse = req.id_data '
               'inner join sigl_10_data as vld on vld.id_resultat = res.min_id_data '
               'where (rec.rec_date_receipt between %s and %s) and rec.statut in (255,256) ' + cond +
               'and vld.type_validation = 252 '
               'group by ana.id_data, pat.unite, pat.age, pat.sexe order by ana.nom asc')

        cursor.execute(req, (date_beg, date_end,))

        return cursor.fetchall()

    @staticmethod
    def getActivityType(date_beg, date_end, type_ana):
        cursor = DB.cursor()

        cond = ''

        if type_ana > 0:
            cond = ' and ana.famille= ' + str(type_ana) + ' '

        req = ('select ana.nom as analysis, ana.code as code, pat.sexe as sex, rec.type as rec_type, '
               'count(*) as nb_ana, rec.rec_custody '
               'from sigl_02_data as rec '
               'inner join sigl_03_data as pat on pat.id_data = rec.id_patient '
               'inner join sigl_04_data as req on req.id_dos = rec.id_data '
               'inner join sigl_05_data as ana on ana.id_data = req.ref_analyse and ana.cote_unite != "PB" '
               'inner join (select id_analyse, min(id_data) as min_id_data from sigl_09_data where valeur is not null '
               'group by id_analyse) as res on res.id_analyse = req.id_data '
               'inner join sigl_10_data as vld on vld.id_resultat = res.min_id_data '
               'where (rec.rec_date_receipt between %s and %s) and rec.statut in (255,256) ' + cond +
               'and vld.type_validation = 252 '
               'group by ana.id_data, rec.type, pat.sexe order by ana.nom asc')

        cursor.execute(req, (date_beg, date_end,))

        return cursor.fetchall()

    @staticmethod
    def getStatPatient(date_beg, date_end, service_int):
        cursor = DB.cursor()

        cond = ''

        if service_int:
            cond += ' and rec.service_interne like "' + str(service_int) + '%" '

        req = ('select pat.sexe as sex, pat.age, count(*) as nb_rec, rec.type as rec_type '
               'from sigl_02_data as rec '
               'inner join sigl_03_data as pat on pat.id_data = rec.id_patient '
               'where (rec.rec_date_receipt between %s and %s) ' + cond +
               'group by pat.age order by age asc')

        cursor.execute(req, (date_beg, date_end,))

        return cursor.fetchall()

    @staticmethod
    def getStatPrescr(date_beg, date_end, service_int):
        cursor = DB.cursor()

        cond = ''

        if service_int:
            cond += ' and rec.service_interne like "' + str(service_int) + '%" '

        req = ('select doctor.nom as lastname, doctor.prenom as firstname, count(*) as nb_rec '
               'from sigl_02_data as rec '
               'inner join sigl_08_data as doctor on doctor.id_data = rec.med_prescripteur '
               'where (date_prescription between %s and %s) ' + cond +
               'group by doctor.id_data order by lastname asc, firstname asc')

        cursor.execute(req, (date_beg, date_end,))

        return cursor.fetchall()

    @staticmethod
    def getStatSampler(date_beg, date_end):
        cursor = DB.cursor()

        req = ('select preleveur as sampler, count(*) as nb_prod '
               'from sigl_01_data '
               'where (samp_date between %s and %s) '
               'group by sampler order by sampler asc')

        cursor.execute(req, (date_beg, date_end,))

        return cursor.fetchall()

    @staticmethod
    def getStatProduct(date_beg, date_end):
        cursor = DB.cursor()

        req = ('select dict.label as product, count(*) as nb_prod '
               'from sigl_01_data as prod '
               'inner join sigl_dico_data as dict on dict.id_data = prod.type_prel '
               'where (prod.samp_date between %s and %s) and statut=8 '
               'group by product order by product asc')

        cursor.execute(req, (date_beg, date_end,))

        return cursor.fetchall()

    @staticmethod
    def getStatNbPat(date_beg, date_end, service_int):
        cursor = DB.cursor()

        cond = ''

        if service_int:
            cond += ' and rec.service_interne like "' + str(service_int) + '%" '

        req = ('select pat.sexe as sex, rec.type, rec_custody, rec.statut '
               'from sigl_02_data as rec '
               'inner join sigl_03_data as pat on pat.id_data = rec.id_patient '
               'where (rec.rec_date_receipt between %s and %s) ' + cond +
               'order by pat.sexe asc, rec.type asc, rec_custody asc')

        cursor.execute(req, (date_beg, date_end,))

        return cursor.fetchall()

    @staticmethod
    def getStatNbAna(date_beg, date_end, service_int):
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
               'order by pat.sexe asc, rec.type asc, rec_custody asc')

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
               'order by rec.id_data asc limit 7000')

        cursor.execute(req, (date_beg, date_end,))

        return cursor.fetchall()

    @staticmethod
    def getTodayList(date_beg, date_end, service_int):
        cursor = DB.cursor()

        cond = ''

        if service_int:
            cond += ' and rec.service_interne like "' + str(service_int) + '%" '

        req = ('select rec.id_data as id_rec, rec.type as type_rec, rec.rec_date_receipt as rec_date, ref.nom as analysis, dict_fam.label as family, '
               'if(param_num_rec.periode=1070, if(param_num_rec.format=1072,substring(rec.num_dos_mois from 7), '
               'rec.num_dos_mois), '
               'if(param_num_rec.format=1072, substring(rec.num_dos_an from 7), rec.num_dos_an)) as rec_num, '
               'group_concat(distinct dict.label order by dict.position asc separator ", ") as vld_type '
               'from `sigl_10_data` as vld '
               'inner join sigl_dico_data as dict on dict.id_data=vld.type_validation '
               'inner join sigl_09_data as res on res.id_data=vld.id_resultat '
               'inner join sigl_04_data as req on req.id_data=res.id_analyse '
               'inner join sigl_05_data as ref on ref.id_data=req.ref_analyse '
               'inner join sigl_02_data as rec on rec.id_data=req.id_dos '
               'left join sigl_param_num_dos_data as param_num_rec on param_num_rec.id_data=1 '
               'left join sigl_dico_data as dict_fam on dict_fam.id_data=ref.famille '
               'where (rec.rec_date_receipt between %s and %s) ' + cond +
               'group by req.id_data order by rec.id_data asc limit 7000')

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

                        req['end'] = req['end'] + 'res' + str(idx) + '.ref_variable=' + id_var + ' or '

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

        return req

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

                        req['end'] = req['end'] + 'res' + str(idx) + '.ref_variable=' + id_var + ' or '

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
    def getTAT(date_beg, date_end, type_ana, id_ana, code_pat, rec_num):
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

        req = ('select rec.rec_date_save, rec.rec_date_vld, rec.rec_num_int, rec.id_data as rec_id, rec.type as rec_type, '
               'if(param_num_rec.periode=1070, if(param_num_rec.format=1072,substring(rec.num_dos_mois from 7), '
               'rec.num_dos_mois), if(param_num_rec.format=1072, substring(rec.num_dos_an from 7), rec.num_dos_an)) '
               'as rec_num, if(param_num_rec.periode=1070, rec.num_dos_mois, rec.num_dos_an) as rec_num_long, '
               'rec.rec_date_receipt as rec_date, pat.nom as pat_name, pat.prenom as pat_firstname, pat.code as pat_code, '
               'pat.code_patient as pat_code_lab, ana.nom as ana_name, ana.code as ana_code, req.id_data as id_req '
               'from sigl_04_data as req '
               'inner join sigl_02_data as rec on rec.id_data = req.id_dos '
               'inner join sigl_03_data as pat on pat.id_data = rec.id_patient '
               'inner join sigl_05_data as ana on ana.id_data = req.ref_analyse '
               'left join sigl_dico_data as fam on fam.id_data = ana.famille '
               'left join sigl_param_num_dos_data as param_num_rec on param_num_rec.id_data=1 '
               'where (rec.rec_date_receipt between %s and %s) and ana.cote_unite != "PB" and rec.statut=256 ' + cond +
               'order by rec.id_data desc')

        cursor.execute(req, (date_beg, date_end,))

        return cursor.fetchall()
