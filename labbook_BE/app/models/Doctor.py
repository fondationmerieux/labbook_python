# -*- coding:utf-8 -*-
import logging
import mysql.connector

# from app.models.Constants import *
from app.models.DB import DB
from app.models.Logs import Logs


class Doctor:
    log = logging.getLogger('log_db')

    @staticmethod
    def getDoctorList(args):
        cursor = DB.cursor()

        filter_cond = ' nom is not NULL '

        if not args:
            limit = 'LIMIT 500'
        else:
            if 'limit' in args and args['limit'] > 0:
                limit = 'LIMIT ' + str(args['limit'])
            else:
                limit = 'LIMIT 500'

            # filter conditions
            if args['code']:
                filter_cond += ' and code LIKE "%' + args['code'] + '%" '

            if args['lastname']:
                filter_cond += ' and nom LIKE "%' + args['lastname'] + '%" '

            if args['firstname']:
                filter_cond += ' and prenom LIKE "%' + args['firstname'] + '%" '

            if args['service']:
                filter_cond += ' and service LIKE "%' + args['service'] + '%" '

            if args['city']:
                filter_cond += ' and ville LIKE "%' + args['city'] + '%" '

        req = 'select id_data, id_owner, code, nom as lastname, prenom as firstname, ville as city, '\
              'etablissement as work_place, specialite as spe, tel as phone, email, titre as title, '\
              'initiale as initial, service, adresse as address, mobile, fax '\
              'from sigl_08_data '\
              'where ' + filter_cond +\
              'order by lastname asc, firstname asc ' + limit

        cursor.execute(req)

        return cursor.fetchall()

    @staticmethod
    def getDoctorSearch(text, id_lab, id_group):
        cursor = DB.cursor()

        l_words = text.split(' ')

        cond = 'doctor.id_data > 0'

        for word in l_words:
            cond = (cond +
                    ' and (doctor.nom like "' + word + '%" or '
                    'doctor.prenom like "' + word + '%" or '
                    'doctor.code like "' + word + '%") ')

        req = 'SELECT TRIM(CONCAT(TRIM(COALESCE(doctor.code, ""))," - ",'\
              'TRIM(COALESCE(doctor.nom, ""))," ",TRIM(COALESCE(doctor.prenom, ""))," - ",'\
              'TRIM(COALESCE(dict.label, "")))) AS field_value,'\
              'doctor.id_data AS id_doctor '\
              'from sigl_08_data AS doctor '\
              'left join sigl_dico_data as dict on dict.id_data=doctor.specialite '\
              'where ' + cond + ' order by doctor.nom asc limit 1000'

        cursor.execute(req)

        return cursor.fetchall()

    @staticmethod
    def getDoctor(id_doctor):
        cursor = DB.cursor()

        req = 'select doctor.id_data as id_data, doctor.id_owner as id_owner, doctor.code as code, doctor.nom as nom, '\
              'doctor.prenom as prenom, doctor.ville as ville, doctor.etablissement as etablissement, '\
              'doctor.specialite as specialite, doctor.tel as tel, doctor.email as email, doctor.titre as titre,'\
              'doctor.initiale as initiale, doctor.service as service, doctor.adresse as adresse, '\
              'doctor.mobile as mobile, doctor.fax as fax, dico.label as spe_doctor '\
              'from sigl_08_data as doctor '\
              'left join sigl_dico_data as dico on dico.id_data = doctor.specialite '\
              'where doctor.id_data=%s'

        cursor.execute(req, (id_doctor,))

        return cursor.fetchone()

    @staticmethod
    def insertDoctor(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into sigl_08_data '
                           '(id_owner, code, nom, prenom, ville, etablissement, specialite, tel, email, '
                           'titre, initiale, service, adresse, mobile, fax) '
                           'values '
                           '(%(id_owner)s, %(code)s, %(nom)s, %(prenom)s, %(ville)s, %(etablissement)s, %(specialite)s, '
                           '%(tel)s, %(email)s, %(titre)s, %(initiale)s, %(service)s, %(adresse)s, %(mobile)s, %(fax)s)', params)

            Doctor.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Doctor.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def updateDoctor(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('update sigl_08_data '
                           'set code=%(code)s, nom=%(nom)s, prenom=%(prenom)s, ville=%(ville)s, '
                           'etablissement=%(etablissement)s, specialite=%(specialite)s, tel=%(tel)s, email=%(email)s, '
                           'titre=%(titre)s, initiale=%(initiale)s, service=%(service)s, adresse=%(adresse)s, '
                           'mobile=%(mobile)s, fax=%(fax)s '
                           'where id_data=%(id_data)s', params)

            Doctor.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Doctor.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False
