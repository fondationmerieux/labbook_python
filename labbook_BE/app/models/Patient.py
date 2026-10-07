# -*- coding:utf-8 -*-
import calendar
import logging
import random
import uuid
from datetime import date, timedelta

import mysql.connector

from app.models.Constants import Constants
from app.models.DB import DB
from app.models.Logs import Logs


class Patient:
    log = logging.getLogger('log_db')

    @staticmethod
    def getPatientList(args):
        cursor = DB.cursor()

        filter_cond = ' code is not NULL '
        params = []

        if not args:
            limit = 'LIMIT 100000'
        else:
            if 'limit' in args and args['limit'] > 0:
                limit = 'LIMIT ' + str(args['limit'])
            else:
                limit = 'LIMIT 5000'

            # filter conditions
            if 'code' in args and args['code']:
                filter_cond += ' and code LIKE %s '
                params.append('%' + args['code'] + '%')

            if 'code_lab' in args and args['code_lab']:
                filter_cond += ' and code_patient LIKE %s '
                params.append('%' + args['code_lab'] + '%')

            if 'lastname' in args and args['lastname']:
                filter_cond += ' and nom LIKE %s '
                params.append('%' + args['lastname'] + '%')

            if 'firstname' in args and args['firstname']:
                filter_cond += ' and prenom LIKE %s '
                params.append('%' + args['firstname'] + '%')

            if 'phone' in args and args['phone']:
                filter_cond += ' and (tel LIKE %s or pat_phone2 LIKE %s) '
                params.append(args['phone'] + '%')
                params.append(args['phone'] + '%')

            if 'sex' in args and args['sex']:
                filter_cond += ' and sexe = %s '
                params.append(args['sex'])

        req = ('select id_data, id_owner, code, code_patient as code_lab, nom as lastname, prenom as firstname, '
               'nom_jf as maidenname, date_format(ddn, %s) as birth, sexe as sex, tel as phone1, pat_phone2 as phone2, '
               'pat_email as email, adresse as address, cp as zipcode, ville as city, profession as job, '
               'quartier as suburb, bp as pbox, ddn_approx as birth_approx, pat_midname as midname, '
               'pat_resident as resident, pat_lite as lite, pat_agreement as agreement '
               'from sigl_03_data '
               'where ' + filter_cond +
               'order by lastname asc, firstname asc ' + limit)

        params.insert(0, Constants.cst_isodate)

        cursor.execute(req, params)

        return cursor.fetchall()

    @staticmethod
    def getPatientSearch(text):
        cursor = DB.cursor()

        words = [w.strip() for w in text.split(' ') if w.strip()]
        if not words:
            return []

        conditions = []
        params = []

        for word in words:
            like = word + '%'
            block = "(" + " OR ".join([
                "pat.nom LIKE %s",
                "pat.prenom LIKE %s",
                "pat.code LIKE %s",
                "pat.code_patient LIKE %s",
                "pat.tel LIKE %s",
                "pat.pat_phone2 LIKE %s"
            ]) + ")"
            conditions.append(block)
            params.extend([like] * 6)

        where_clause = " AND ".join(conditions)

        query = (
            "SELECT pat.id_data AS id, pat.nom, pat.prenom, pat.nom_jf, pat.code, pat.tel AS pat_phone1, "
            "DATE_FORMAT(pat.ddn, %s) AS ddn, pat.code_patient, pat.age, "
            "d_age_unit.label AS age_unit, pat.pat_phone2 "
            "FROM sigl_03_data AS pat "
            "LEFT JOIN sigl_dico_data AS d_age_unit ON d_age_unit.id_data = pat.unite "
            f"WHERE {where_clause} "
            "ORDER BY pat.nom ASC "
            "LIMIT 1000"
        )

        cursor.execute(query, (Constants.cst_isodate, *params))
        return cursor.fetchall()

    @staticmethod
    def combinePatients(id_pat1, id_pat2):
        try:
            cursor = DB.cursor()

            cursor.execute('update sigl_02_data '
                           'set id_patient=%s '
                           'where id_patient=%s', (id_pat1, id_pat2,))

            cursor.execute('update sigl_02_deleted '
                           'set id_patient=%s '
                           'where id_patient=%s', (id_pat1, id_pat2,))

            # Move dynamic patient form items
            cursor.execute('update patient_form_item '
                           'set pfi_pat=%s '
                           'where pfi_pat=%s', (id_pat1, id_pat2,))

            # Move patient history form items
            cursor.execute('update patient_hist_form_item '
                           'set phfi_pat=%s '
                           'where phfi_pat=%s', (id_pat1, id_pat2,))

            # DELETE PATIENT 2
            cursor.execute('delete from sigl_03_data '
                           'where id_data=%s', (id_pat2,))

            Patient.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Patient.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getPatient(id_pat):
        cursor = DB.cursor()

        req = ('select id_data, id_owner as id_user, anonyme as pat_ano, code as pat_code, code_patient as pat_code_lab, '
               'nom as pat_name, prenom as pat_firstname, ddn as pat_birth, sexe as pat_sex, adresse as pat_address, '
               'cp as pat_zipcode, ville as pat_city, tel as pat_phone1, pat_phone2, profession as pat_profession, '
               'nom_jf as pat_maiden, quartier as pat_district, bp as pat_pbox, ddn_approx as pat_birth_approx, '
               'age as pat_age, unite as pat_age_unit, pat_email, pat_agreement, pat_amicare, '
               'pat_midname, pat_nation as pat_nationality, pat_resident, pat_blood_group, pat_blood_rhesus '
               'from sigl_03_data '
               'where id_data=%s')

        cursor.execute(req, (id_pat,))

        return cursor.fetchone()

    @staticmethod
    def estimateBirth(age, unit, today=None):
        """Return a birth date estimated from an age and its unit (1034 days to 1037 years), or None."""
        try:
            age  = int(age)
            unit = int(unit)
        except (TypeError, ValueError):
            return None

        if age <= 0:
            return None

        today = today or date.today()

        if unit == 1034:
            return today - timedelta(days=age)
        if unit == 1035:
            return today - timedelta(weeks=age)
        if unit in (1036, 1037):
            months = age if unit == 1036 else age * 12
            year, month = divmod(today.year * 12 + today.month - 1 - months, 12)
            month += 1
            return date(year, month, min(today.day, calendar.monthrange(year, month)[1]))

        return None

    @staticmethod
    def computeAge(born, today=None):
        """Return (age, unit) from a birth date in years, else months, else days, or (None, None) if in the future."""
        today = today or date.today()

        if born > today:
            return None, None

        months = (today.year - born.year) * 12 + today.month - born.month - (today.day < born.day)

        if months >= 12:
            return months // 12, 1037
        if months >= 1:
            return months, 1036

        return (today - born).days, 1034

    @staticmethod
    def getFormItems(id_pat):
        cursor = DB.cursor()

        req = ('select pfi_key, pfi_value '
               'from patient_form_item '
               'where pfi_pat=%s and pfi_act="Y"')

        cursor.execute(req, (id_pat,))

        return cursor.fetchall()

    @staticmethod
    def checkFormItem(id_pat, key):
        cursor = DB.cursor()

        req = ('select count(*) as nb_item '
               'from patient_form_item '
               'where pfi_pat=%s and pfi_key=%s and pfi_act="Y"')

        cursor.execute(req, (id_pat, key))

        ret = cursor.fetchone()

        return ret['nb_item']

    @staticmethod
    def sameFormItem(id_pat, key, value, act):
        cursor = DB.cursor()

        req = ('select count(*) as nb_item '
               'from patient_form_item '
               'where pfi_pat=%s and pfi_key=%s and pfi_value=%s and pfi_act=%s')

        cursor.execute(req, (id_pat, key, value, act))

        ret = cursor.fetchone()

        return ret['nb_item']

    @staticmethod
    def desactFormItem(id_pat, key):
        try:
            cursor = DB.cursor()

            req = ('update patient_form_item '
                   'set pfi_act="N" '
                   'where pfi_pat=%s and pfi_key=%s and pfi_act="Y"')

            cursor.execute(req, (id_pat, key))

            Patient.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Patient.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def insertFormItem(id_pat, key, value, id_user):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into patient_form_item '
                           '(pfi_date, pfi_pat, pfi_act, pfi_key, pfi_value, pfi_user) '
                           'values '
                           '(NOW(), %s, "Y", %s, %s, %s)', (id_pat, key, value, id_user))

            Patient.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Patient.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def getHistFormItems(id_pat):
        cursor = DB.cursor()
        sql = ('select phfi_evt, phfi_date, phfi_user, phfi_type, phfi_key, phfi_value, '
               'u.firstname, u.lastname, u.username '
               'from patient_hist_form_item '
               'left join sigl_user_data as u on u.id_data = phfi_user '
               'where phfi_pat=%s and phfi_act="Y" '
               'order by phfi_date desc, phfi_ser desc')
        cursor.execute(sql, (id_pat,))
        return cursor.fetchall()

    @staticmethod
    def insertHistFormItem(id_pat, id_user, block_id, fields):
        cursor = DB.cursor()

        phfi_evt = str(uuid.uuid4())  # event id

        Patient.log.info(Logs.fileline() + ' : SAVE hist evt=' + phfi_evt)

        sql = ('insert into patient_hist_form_item '
               '(phfi_evt, phfi_date, phfi_user, phfi_pat, phfi_act, phfi_type, phfi_key, phfi_value) '
               'values (%s, now(), %s, %s, %s, %s, %s, %s)')

        for key, val in fields.items():
            cursor.execute(sql, (phfi_evt, id_user, id_pat, 'Y', block_id, key, str(val)))

        return phfi_evt

    @staticmethod
    def deleteHistFormEvent(id_pat, evt_id):
        cursor = DB.cursor()
        sql = ('update patient_hist_form_item '
               'set phfi_act="N" '
               'where phfi_pat=%s and phfi_evt=%s')
        cursor.execute(sql, (id_pat, evt_id))
        return cursor.rowcount

    @staticmethod
    def getPatientByCode(code, code_lab):
        cursor = DB.cursor()

        cond = ''

        if code:
            cond = 'code="' + str(code) + '"'
        elif code_lab:
            cond = 'code_patient="' + str(code_lab) + '"'

        if not cond:
            return {}

        req = ('select id_data, id_owner, anonyme, code, code_patient, nom, prenom, ddn, sexe, '
               'adresse, cp, ville, tel, pat_phone2, profession, '
               'nom_jf, quartier, bp, ddn_approx, age, unite, '
               'pat_midname, pat_nation, pat_resident, pat_blood_group, pat_blood_rhesus, pat_agreement, pat_amicare '
               'from sigl_03_data '
               'where ' + cond)

        cursor.execute(req)

        return cursor.fetchone()

    @staticmethod
    def getPatientByIdentity(name, fname, sex, birth, age, age_unit):
        cursor = DB.cursor()

        if sex == 'M':
            sex = 1
        elif sex == 'F':
            sex = 2
        else:
            sex = 3

        if age_unit == 'D':
            age_unit = 1034
        elif age_unit == 'W':
            age_unit = 1035
        elif age_unit == 'M':
            age_unit = 1036
        else:
            age_unit = 1037

        if birth:
            cond = ' and ddn=%(birth)s'
        else:
            cond = ' and age=%(age)s and unite=%(age_unit)s'

        req = ('select id_data, id_owner, anonyme, code, code_patient, nom, prenom, ddn, sexe, '
               'adresse, cp, ville, tel, pat_phone2, profession, '
               'nom_jf, quartier, bp, ddn_approx, age, unite, '
               'pat_midname, pat_nation, pat_resident, pat_blood_group, pat_blood_rhesus, pat_agreement '
               'from sigl_03_data '
               'where nom=%(name)s and prenom=%(fname)s and sexe=%(sex)s ' + cond)

        cursor.execute(req, {'name': name, 'fname': fname, 'sex': sex, 'birth': birth, 'age': age,
                             'age_unit': age_unit})

        return cursor.fetchone()

    @staticmethod
    def updatePatient(**params):
        try:
            cursor = DB.cursor()

            if 'pat_email' not in params or params['pat_email'] is None:
                params['pat_email'] = ''

            if 'pat_lite' not in params or params['pat_lite'] is None:
                params['pat_lite'] = 0

            if 'pat_agreement' not in params or params['pat_agreement'] is None:
                params['pat_agreement'] = 'N'

            if 'pat_amicare' not in params or params['pat_amicare'] is None:
                params['pat_amicare'] = 0

            cursor.execute('update sigl_03_data '
                           'set id_owner=%(id_owner)s, anonyme=%(anonyme)s, code=%(code)s, code_patient=%(code_patient)s, '
                           'nom=%(nom)s, prenom=%(prenom)s, ddn=%(ddn)s, sexe=%(sexe)s, adresse=%(adresse)s, '
                           'cp=%(cp)s, ville=%(ville)s, pat_email=%(pat_email)s, tel=%(tel)s, pat_phone2=%(phone2)s, '
                           'profession=%(profession)s, nom_jf=%(nom_jf)s, quartier=%(quartier)s, bp=%(bp)s, '
                           'ddn_approx=%(ddn_approx)s, age=%(age)s, unite=%(unite)s, pat_midname=%(midname)s, '
                           'pat_nation=%(nationality)s, pat_resident=%(resident)s, pat_blood_group=%(blood_group)s, '
                           'pat_blood_rhesus=%(blood_rhesus)s, pat_lite=%(pat_lite)s, pat_agreement=%(pat_agreement)s, '
                           'pat_amicare=%(pat_amicare)s '
                           'where id_data=%(id)s', params)

            Patient.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Patient.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def insertPatient(**params):
        try:
            cursor = DB.cursor()

            if 'pat_email' not in params or params['pat_email'] is None:
                params['pat_email'] = ''

            if 'pat_lite' not in params or params['pat_lite'] is None:
                params['pat_lite'] = 0

            if 'pat_agreement' not in params or params['pat_agreement'] is None:
                params['pat_agreement'] = 'N'

            if 'pat_amicare' not in params or params['pat_amicare'] is None:
                params['pat_amicare'] = 0

            cursor.execute('insert into sigl_03_data '
                           '(id_owner, anonyme, code, code_patient, nom, prenom, ddn, sexe, adresse, cp, ville, '
                           'pat_email, tel, pat_phone2, profession, nom_jf, quartier, bp, ddn_approx, age, '
                           'unite, pat_midname, pat_nation, pat_resident, pat_blood_group, pat_blood_rhesus, pat_lite, '
                           'pat_agreement, pat_amicare) '
                           'values '
                           '(%(id_owner)s, %(anonyme)s, %(code)s, %(code_patient)s, %(nom)s, %(prenom)s, %(ddn)s, '
                           '%(sexe)s, %(adresse)s, %(cp)s, %(ville)s, %(pat_email)s, %(tel)s, %(phone2)s, '
                           '%(profession)s, %(nom_jf)s, %(quartier)s, %(bp)s, %(ddn_approx)s, %(age)s, '
                           '%(unite)s, %(midname)s, %(nationality)s, %(resident)s, %(blood_group)s, %(blood_rhesus)s, '
                           '%(pat_lite)s, %(pat_agreement)s, %(pat_amicare)s)', params)

            Patient.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Patient.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def newPatientCode(length=5, prefix=""):
        # Format by defaut 5 alphanumeric characters without zero

        chars   = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        numbers = "123456789"
        pool = chars + numbers

        # Ensure minimum code length of 5 characters
        length = max(5, length)

        ret = 'START'
        while ret:
            code = ""

            # Generate alphanumeric code of specified length
            for _ in range(length):
                code += random.choice(pool)  # nosec B311

            full_code = prefix + code

            # Check for uniqueness in the database
            cursor = DB.cursor()
            cursor.execute(
                'select code from sigl_03_data where code=%s',
                (full_code,)
            )
            ret = cursor.fetchone()

        return code

    @staticmethod
    def codeLab_exist(code):
        try:
            cursor = DB.cursor()

            cursor.execute('select count(*) as nb_code '
                           'from sigl_03_data '
                           'where code_patient=%s', (code,))

            ret = cursor.fetchone()

            if ret and ret['nb_code'] == 0:
                return False
            else:
                return True
        except mysql.connector.Error as e:
            Patient.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return -1

    @staticmethod
    def getPatientHistoric(id_pat):
        cursor = DB.cursor()

        req = ('select rec.id_data as id_rec, rec.type as type_rec, rec.date_prescription as date_prescr, ref.nom as analysis, '
               'if(rec_setting.rstg_period=1070, if(rec_setting.rstg_format=1072,substring(rec.num_dos_mois from 7), '
               'rec.num_dos_mois), '
               'if(rec_setting.rstg_format=1072, substring(rec.num_dos_an from 7), rec.num_dos_an)) as rec_num, '
               'ref_var.libelle as variable, '
               'IF("dico_" = substring(dict_type.short_label, 1, 5), dict_res.label, res.valeur) as result '
               'from sigl_03_data as pat '
               'inner join sigl_02_data as rec on rec.id_patient=pat.id_data '
               'inner join sigl_04_data as req on req.id_dos=rec.id_data '
               'inner join sigl_05_data as ref on ref.id_data=req.ref_analyse and ref.cote_unite != "PB" '
               'inner join sigl_09_data as res on res.id_analyse=req.id_data '
               'inner join sigl_07_data as ref_var on ref_var.id_data=res.ref_variable '
               'left join sigl_05_07_data as ref_link on ref_link.id_data=res.ref_variable '
               'left join sigl_dico_data as dict_type on dict_type.id_data=ref_var.type_resultat '
               'left join sigl_dico_data as dict_res on dict_res.id_data=res.valeur '
               'left join record_setting as rec_setting on rec_setting.rstg_ser = 1 '
               'where pat.id_data=%s '
               'order by rec.num_dos_an desc, ref.id_data asc limit 7000')

        cursor.execute(req, (id_pat,))

        return cursor.fetchall()

    @staticmethod
    def getDataset():
        cursor = DB.cursor()

        req = ('select pat.id_data as id_patient, pat.code, pat.code_patient as code_lab, pat.nom as lastname, '
               'pat.prenom as firstname, date_format(pat.ddn, %s) as birth, date_format(pat.ddn, "%Y") as birth_year, '
               'date_format(pat.ddn, "%m") as birth_month, date_format(pat.ddn, "%d") as birth_day, '
               'pat.ddn_approx as birth_approx, pat.age, d_age_unit.label as age_unit, d_sex.label as sex, '
               'pat.pat_midname as middle_name, pat.nom_jf as maiden_name, nat.nat_name as nation, '
               'nat.nat_code as nat_code, pat.pat_resident as resident, pat.cp as zipcode, pat.ville as city, '
               'pat.profession, d_blood.label as blood_group, d_rhesus.label as blood_rhesus, pat.pat_lite, '
               'pat.pat_agreement '
               'from sigl_03_data as pat '
               'left join sigl_dico_data as d_sex on d_sex.id_data=pat.sexe '
               'left join sigl_dico_data as d_blood on d_blood.id_data=pat.pat_blood_group '
               'left join sigl_dico_data as d_rhesus on d_rhesus.id_data=pat.pat_blood_rhesus '
               'left join sigl_dico_data as d_age_unit on d_age_unit.id_data=pat.unite '
               'left join nationality as nat on nat.nat_ser=pat.pat_nation '
               'order by id_patient desc')

        cursor.execute(req, (Constants.cst_isodate,))

        return cursor.fetchall()

    @staticmethod
    def update_amicare_id(id_pat, amicare_id):
        try:
            cursor = DB.cursor()
            cursor.execute('update sigl_03_data set pat_amicare=%s where id_data=%s', (amicare_id, id_pat))
            Patient.log.info(Logs.fileline())
            return True
        except mysql.connector.Error as e:
            Patient.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False
