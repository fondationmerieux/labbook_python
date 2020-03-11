# -*- coding:utf-8 -*-
import logging

from flask import request
from flask_restful import Resource

from app.models.General import compose_ret
from app.models.Constants import *
from app.models.Doctor import *
from app.models.User import *
from app.models.Logs import Logs


class DoctorSearch(Resource):
    log = logging.getLogger('log_services')

    def post(self, id_group):
        args = request.get_json()

        id_lab = User.getUserGroupParent(id_group)

        l_doctors = Doctor.getDoctorSearch(args['term'], id_lab['id_group_parent'], id_group)

        if not l_doctors:
            self.log.error(Logs.fileline() + ' : TRACE DoctorSearch not found')

        self.log.info(Logs.fileline() + ' : TRACE DoctorSearch')
        return compose_ret(l_doctors, Constants.cst_content_type_json)

"""
class DoctorDet(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_pat):
        doctor = Doctor.getDoctor(id_pat)

        if not doctor:
            self.log.error(Logs.fileline() + ' : ' + 'DoctorDet ERROR not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        doctor['ddn'] = datetime.strftime(doctor['ddn'], '%Y-%m-%d')

        # Replace None by empty string
        for key, value in doctor.items():
            if doctor[key] is None:
                doctor[key] = ''

        self.log.info(Logs.fileline() + ' : DoctorDet id_pat=' + str(id_pat))
        return compose_ret(doctor, Constants.cst_content_type_json, 200)

    def post(self, id_pat=0):
        args = request.get_json()

        if 'id_owner' not in args or 'anonyme' not in args or 'code' not in args or 'code_doctor' not in args or 'nom' not in args or \
           'prenom' not in args or 'ddn' not in args or 'sexe' not in args or 'ethnie' not in args or 'adresse' not in args or \
           'cp' not in args or 'ville' not in args or 'tel' not in args or 'profession' not in args or 'nom_jf' not in args or \
           'quartier' not in args or 'bp' not in args or 'ddn_approx' not in args or 'age' not in args or 'annee_naiss' not in args or \
           'semaine_naiss' not in args or 'mois_naiss' not in args or 'unite' not in args:
            self.log.error(Logs.fileline() + ' : DoctorDet ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # Update doctor
        if id_pat != 0:
            self.log.error(Logs.fileline() + ' : DEBUG DoctorDet update')

            doctor = Doctor.getDoctor(id_pat)

            if not doctor:
                self.log.error(Logs.fileline() + ' : DoctorDet ERROR not found')
                return compose_ret('', Constants.cst_content_type_json, 500)

            ret = Doctor.updateDoctor(id=id_pat,
                                        id_owner=args['id_owner'],
                                        anonyme=args['anonyme'],
                                        code=args['code'],
                                        code_doctor=args['code_doctor'],
                                        nom=args['nom'],
                                        prenom=args['prenom'],
                                        ddn=args[''],
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
                self.log.error(Logs.alert() + ' : DoctorDet ERROR update')
                return compose_ret('', Constants.cst_content_type_json, 500)

            res = {}
            res['id_pat'] = id_pat

        # Insert new doctor
        else:
            self.log.error(Logs.fileline() + ' : DEBUG DoctorDet insert')

            args['ddn'] = datetime.strptime(args['ddn'], Constants.cst_isodate)

            ret = Doctor.insertDoctor(id_owner=args['id_owner'],
                                        anonyme=args['anonyme'],
                                        code=args['code'],
                                        code_doctor=args['code_doctor'],
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
                self.log.error(Logs.alert() + ' : DoctorDet ERROR  insert')
                return compose_ret('', Constants.cst_content_type_json, 500)

            res = {}
            res['id_pat'] = ret

            # Get id_group of lab with id_group of user
            id_group_lab = User.getUserGroupParent(args['id_owner'])

            if not id_group_lab:
                self.log.error(Logs.fileline() + ' : DoctorDet ERROR group not found')
                return compose_ret('', Constants.cst_content_type_json, 500)

            # insert sigl_03_data_group
            ret = Doctor.insertDoctorGroup(id_data=res['id_pat'],
                                             id_group=id_group_lab['id_group_parent'])

            if ret <= 0:
                self.log.error(Logs.alert() + ' : DoctorDet ERROR  insert group')
                return compose_ret('', Constants.cst_content_type_json, 500)


        self.log.info(Logs.fileline() + ' : TRACE DoctorDet id_pat=' + str(res['id_pat']))
        return compose_ret(res, Constants.cst_content_type_json)"""
