# -*- coding:utf-8 -*-
import logging

from datetime import datetime
from flask import request
from flask_restful import Resource

from app.models.General import compose_ret
from app.models.Constants import *
from app.models.Patient import *
from app.models.User import *
from app.models.Logs import Logs


class PatientSearch(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        l_pats = Patient.getPatientSearch(args['term'])

        if not l_pats:
            self.log.error(Logs.fileline() + ' : WARNING PatientSearch NOT FOUND')
            return compose_ret('', Constants.cst_content_type_json, 200)  # 200 if not select2 trigger an exception

        self.log.info(Logs.fileline() + ' : TRACE PatientSearch')
        return compose_ret(l_pats, Constants.cst_content_type_json)


class PatientCode(Resource):
    log = logging.getLogger('log_services')

    def get(self):
        code = Patient.newPatientCode()

        if not code:
            self.log.error(Logs.fileline() + ' : ERROR GeneratePatientCode not generate')
            return compose_ret('', Constants.cst_content_type_json, 404)

        self.log.info(Logs.fileline() + ' : TRACE GeneratePatientCode : ' + code)
        return compose_ret(code, Constants.cst_content_type_json)


class PatientDet(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_pat):
        patient = Patient.getPatient(id_pat)

        if not patient:
            self.log.error(Logs.fileline() + ' : ' + 'PatientDet ERROR not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        if patient['ddn']:
            patient['ddn'] = datetime.strftime(patient['ddn'], '%Y-%m-%d')

        # Replace None by empty string
        for key, value in patient.items():
            if patient[key] is None:
                patient[key] = ''

        self.log.info(Logs.fileline() + ' : PatientDet id_pat=' + str(id_pat))
        return compose_ret(patient, Constants.cst_content_type_json, 200)

    def post(self, id_pat=0):
        args = request.get_json()

        if 'id_owner' not in args or 'anonyme' not in args or 'code' not in args or 'code_patient' not in args or 'nom' not in args or \
           'prenom' not in args or 'ddn' not in args or 'sexe' not in args or 'ethnie' not in args or 'adresse' not in args or \
           'cp' not in args or 'ville' not in args or 'tel' not in args or 'profession' not in args or 'nom_jf' not in args or \
           'quartier' not in args or 'bp' not in args or 'ddn_approx' not in args or 'age' not in args or 'annee_naiss' not in args or \
           'semaine_naiss' not in args or 'mois_naiss' not in args or 'unite' not in args:
            self.log.error(Logs.fileline() + ' : PatientDet ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # Update patient
        if id_pat != 0:
            self.log.error(Logs.fileline() + ' : DEBUG PatientDet update')

            patient = Patient.getPatient(id_pat)

            if not patient:
                self.log.error(Logs.fileline() + ' : PatientDet ERROR not found')
                return compose_ret('', Constants.cst_content_type_json, 500)

            if args['ddn']:
                args['ddn'] = datetime.strptime(args['ddn'], Constants.cst_isodate)
            else:
                args['ddn'] = None

            ret = Patient.updatePatient(id=id_pat,
                                        id_owner=args['id_owner'],
                                        anonyme=args['anonyme'],
                                        code=args['code'],
                                        code_patient=args['code_patient'],
                                        nom=args['nom'],
                                        prenom=args['prenom'],
                                        ddn=args['ddn'],
                                        sexe=args['sexe'],
                                        ethnie=args['ethnie'],
                                        adresse=args['adresse'],
                                        cp=args['cp'],
                                        ville=args['ville'],
                                        tel=args['tel'],
                                        profession=args['profession'],
                                        nom_jf=args['nom_jf'],
                                        quartier=args['quartier'],
                                        bp=args['bp'],
                                        ddn_approx=args['ddn_approx'],
                                        age=args['age'],
                                        annee_naiss=args['annee_naiss'],
                                        semaine_naiss=args['semaine_naiss'],
                                        mois_naiss=args['mois_naiss'],
                                        unite=args['unite'])

            if ret is False:
                self.log.error(Logs.alert() + ' : PatientDet ERROR update')
                return compose_ret('', Constants.cst_content_type_json, 500)

            res = {}
            res['id_pat'] = id_pat

        # Insert new patient
        else:
            self.log.error(Logs.fileline() + ' : DEBUG PatientDet insert')

            if args['ddn']:
                args['ddn'] = datetime.strptime(args['ddn'], Constants.cst_isodate)
            else:
                args['ddn'] = None

            ret = Patient.insertPatient(id_owner=args['id_owner'],
                                        anonyme=args['anonyme'],
                                        code=args['code'],
                                        code_patient=args['code_patient'],
                                        nom=args['nom'],
                                        prenom=args['prenom'],
                                        ddn=args['ddn'],
                                        sexe=args['sexe'],
                                        ethnie=args['ethnie'],
                                        adresse=args['adresse'],
                                        cp=args['cp'],
                                        ville=args['ville'],
                                        tel=args['tel'],
                                        profession=args['profession'],
                                        nom_jf=args['nom_jf'],
                                        quartier=args['quartier'],
                                        bp=args['bp'],
                                        ddn_approx=args['ddn_approx'],
                                        age=args['age'],
                                        annee_naiss=args['annee_naiss'],
                                        semaine_naiss=args['semaine_naiss'],
                                        mois_naiss=args['mois_naiss'],
                                        unite=args['unite'])

            if ret <= 0:
                self.log.error(Logs.alert() + ' : PatientDet ERROR  insert')
                return compose_ret('', Constants.cst_content_type_json, 500)

            res = {}
            res['id_pat'] = ret

            # Get id_group of lab with id_group of user
            id_group_lab = User.getUserGroupParent(args['id_owner'])

            if not id_group_lab:
                self.log.error(Logs.fileline() + ' : PatientDet ERROR group not found')
                return compose_ret('', Constants.cst_content_type_json, 500)

            # insert sigl_03_data_group
            ret = Patient.insertPatientGroup(id_data=res['id_pat'],
                                             id_group=id_group_lab['id_group_parent'])

            if ret <= 0:
                self.log.error(Logs.alert() + ' : PatientDet ERROR  insert group')
                return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE PatientDet id_pat=' + str(res['id_pat']))
        return compose_ret(res, Constants.cst_content_type_json)
