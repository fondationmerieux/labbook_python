# -*- coding:utf-8 -*-
import logging
import mysql.connector

from app.models.DB import DB
from app.models.Logs import Logs
from app.models.Constants import Constants


class Patient:
    log = logging.getLogger('log_db')

    @staticmethod
    def getPatientList(args):
        cursor = DB.cursor()

        filter_cond = ' code is not NULL '

        if not args:
            limit = 'LIMIT 5000'
        else:
            if 'limit' in args and args['limit'] > 0:
                limit = 'LIMIT ' + str(args['limit'])
            else:
                limit = 'LIMIT 5000'

            # filter conditions
            if args['code']:
                filter_cond += ' and code LIKE "%' + args['code'] + '%" '

            if args['code_lab']:
                filter_cond += ' and code_patient LIKE "%' + args['code_lab'] + '%" '

            if args['lastname']:
                filter_cond += ' and nom LIKE "%' + args['lastname'] + '%" '

            if args['firstname']:
                filter_cond += ' and prenom LIKE "%' + args['firstname'] + '%" '

        req = ('select id_data, id_owner, code, code_patient as code_lab, nom as lastname, prenom as firstname, '
               'date_format(ddn, %s) as birth, sexe as sex '
               'from sigl_03_data '
               'where ' + filter_cond +
               'order by lastname asc, firstname asc ' + limit)

        cursor.execute(req, (Constants.cst_isodate,))

        return cursor.fetchall()

    @staticmethod
    def getPatientSearch(text):
        cursor = DB.cursor()

        l_words = text.split(' ')

        cond = '(anonyme=5 or anonyme is NULL)'

        for word in l_words:
            cond = (cond +
                    ' and (nom like "' + word + '%" or '
                    'prenom like "' + word + '%" or '
                    'code like "' + word + '%" or '
                    'code_patient like "' + word + '%") ')

        req = 'select id_data as id, nom, prenom, nom_jf, code, '\
              'date_format(ddn, %s) as ddn, code_patient '\
              'from sigl_03_data '\
              'where ' + cond + ' order by nom asc limit 1000'

        cursor.execute(req, (Constants.cst_isodate,))

        return cursor.fetchall()

    @staticmethod
    def combinePatients(id_pat1, id_pat2):
        try:
            cursor = DB.cursor()

            # NOTE : Dont knwow the use of these tables
            # sigl_01_dico_analyse_data
            # sigl_01_dico_analyse_deleted
            # sigl_12_data
            # sigl_12_deleted

            cursor.execute('update sigl_01_dico_analyse_data '
                           'set id_pat=%s '
                           'where id_pat=%s', (id_pat1, id_pat2,))

            cursor.execute('update sigl_01_dico_analyse_deleted '
                           'set id_pat=%s '
                           'where id_pat=%s', (id_pat1, id_pat2,))

            cursor.execute('update sigl_02_data '
                           'set id_patient=%s '
                           'where id_patient=%s', (id_pat1, id_pat2,))

            cursor.execute('update sigl_02_deleted '
                           'set id_patient=%s '
                           'where id_patient=%s', (id_pat1, id_pat2,))

            cursor.execute('update sigl_12_data '
                           'set id_patient=%s '
                           'where id_patient=%s', (id_pat1, id_pat2,))

            cursor.execute('update sigl_12_deleted '
                           'set id_patient=%s '
                           'where id_patient=%s', (id_pat1, id_pat2,))

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

        req = 'select id_data, id_owner, anonyme, code, code_patient, nom, prenom, ddn, sexe, ethnie, '\
              'adresse, cp, ville, tel, profession, '\
              'nom_jf, quartier, bp, ddn_approx, age, annee_naiss, semaine_naiss, mois_naiss, unite '\
              'from sigl_03_data '\
              'where id_data=%s'

        cursor.execute(req, (id_pat,))

        return cursor.fetchone()

    @staticmethod
    def updatePatient(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('update sigl_03_data '
                           'set id_owner=%(id_owner)s, anonyme=%(anonyme)s, code=%(code)s, code_patient=%(code_patient)s, '
                           'nom=%(nom)s, prenom=%(prenom)s, ddn=%(ddn)s, sexe=%(sexe)s, ethnie=%(ethnie)s, adresse=%(adresse)s, '
                           'cp=%(cp)s, ville=%(ville)s, tel=%(tel)s, profession=%(profession)s, nom_jf=%(nom_jf)s, '
                           'quartier=%(quartier)s, bp=%(bp)s, ddn_approx=%(ddn_approx)s, age=%(age)s, '
                           'annee_naiss=%(annee_naiss)s, semaine_naiss=%(semaine_naiss)s, mois_naiss=%(mois_naiss)s, unite=%(unite)s '
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

            cursor.execute('insert into sigl_03_data '
                           '(id_owner, anonyme, code, code_patient, nom, prenom, ddn, sexe, ethnie, adresse, cp, ville, '
                           'tel, profession, nom_jf, quartier, bp, ddn_approx, age, annee_naiss, semaine_naiss, mois_naiss, unite) '
                           'values '
                           '(%(id_owner)s, %(anonyme)s, %(code)s, %(code_patient)s, %(nom)s, %(prenom)s, %(ddn)s, %(sexe)s, %(ethnie)s, %(adresse)s, %(cp)s, %(ville)s, '
                           '%(tel)s, %(profession)s, %(nom_jf)s, %(quartier)s, %(bp)s, %(ddn_approx)s, %(age)s, %(annee_naiss)s, '
                           '%(semaine_naiss)s, %(mois_naiss)s, %(unite)s )', params)

            Patient.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Patient.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def newPatientCode():
        import random

        # Format ABCD3, 4 letters + 1 digit

        chars   = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        numbers = "123456789"
        length  = 4
        ret     = 'START'

        while ret:
            code = ""

            for i in range(length):
                code += random.choice(chars)

            for i in range(1):
                code += random.choice(numbers)

            # check if code not already exist in DB
            cursor = DB.cursor()

            req = 'select code '\
                  'from sigl_03_data '\
                  'where code=%s'

            cursor.execute(req, (code,))

            ret = cursor.fetchone()

        return code

    @staticmethod
    def getPatientHistoric(id_pat):
        cursor = DB.cursor()

        req = ('select rec.id_data, rec.date_prescription as date_prescr, ref.nom as analysis, '
               'if(param_num_rec.periode=1070, if(param_num_rec.format=1072,substring(rec.num_dos_mois from 7), '
               'rec.num_dos_mois), '
               'if(param_num_rec.format=1072, substring(rec.num_dos_an from 7), rec.num_dos_an)) as rec_num, '
               'ref_var.libelle as variable, '
               'IF("dico_" = substring(dict_type.short_label, 1, 5), dict_res.label, res.valeur) as result '
               'from sigl_03_data as pat '
               'inner join sigl_02_data as rec on rec.id_patient=pat.id_data '
               'inner join sigl_04_data as ana on ana.id_dos=rec.id_data '
               'inner join sigl_05_data as ref on ref.id_data=ana.ref_analyse and ref.cote_unite != "PB" '
               'inner join sigl_09_data as res on res.id_analyse=ana.id_data '
               'inner join sigl_07_data as ref_var on ref_var.id_data=res.ref_variable '
               'left join sigl_05_07_data as ref_link on ref_link.id_data=res.ref_variable '
               'left join sigl_dico_data as dict_type on dict_type.id_data=ref_var.type_resultat '
               'left join sigl_dico_data as dict_res on dict_res.id_data=res.valeur '
               'left join sigl_param_num_dos_data as param_num_rec on param_num_rec.id_data = 1 '
               'where pat.id_data=%s '
               'order by rec.num_dos_an desc, ref.id_data asc limit 7000')

        cursor.execute(req, (id_pat,))

        return cursor.fetchall()
