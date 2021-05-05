# -*- coding:utf-8 -*-
import logging

from datetime import datetime
from flask import request
from flask_restful import Resource

from app.models.General import compose_ret
from app.models.Constants import *
from app.models.Doctor import *
from app.models.User import *
from app.models.Logs import Logs


class DoctorList(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        if not args:
            args = {}

        l_doctors = Doctor.getDoctorList(args)

        if not l_doctors:
            self.log.error(Logs.fileline() + ' : TRACE DoctorList not found')

        for doctor in l_doctors:
            # Replace None by empty string
            for key, value in doctor.items():
                if doctor[key] is None:
                    doctor[key] = ''

        self.log.info(Logs.fileline() + ' : TRACE DoctorList')
        return compose_ret(l_doctors, Constants.cst_content_type_json)


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


class DoctorDet(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_doctor):
        doctor = Doctor.getDoctor(id_doctor)

        if not doctor:
            self.log.error(Logs.fileline() + ' : ' + 'DoctorDet ERROR not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        # Replace None by empty string
        for key, value in doctor.items():
            if doctor[key] is None:
                doctor[key] = ''

        self.log.info(Logs.fileline() + ' : DoctorDet id_doctor=' + str(id_doctor))
        return compose_ret(doctor, Constants.cst_content_type_json, 200)

    def post(self, id_doctor):
        args = request.get_json()

        if 'id_owner' not in args or 'id_doctor' not in args or 'code' not in args or 'title' not in args or \
           'lastname' not in args or 'firstname' not in args or 'initial' not in args or 'work_place' not in args or \
           'service' not in args or 'address' not in args or 'city' not in args or 'spe' not in args or \
           'phone' not in args or 'mobile' not in args or 'fax' not in args or 'email' not in args:
            self.log.error(Logs.fileline() + ' : DoctorDet ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # Update doctor
        if id_doctor > 0:
            ret = Doctor.updateDoctor(id_data=id_doctor,
                                      id_owner=args['id_owner'],
                                      code=args['code'],
                                      nom=args['lastname'],
                                      prenom=args['firstname'],
                                      ville=args['city'],
                                      etablissement=args['work_place'],
                                      specialite=args['spe'],
                                      tel=args['phone'],
                                      email=args['email'],
                                      titre=args['title'],
                                      initiale=args['initial'],
                                      service=args['service'],
                                      adresse=args['address'],
                                      mobile=args['mobile'],
                                      fax=args['fax'])

            if ret is False:
                self.log.error(Logs.alert() + ' : DoctorDet ERROR update')
                return compose_ret('', Constants.cst_content_type_json, 500)

        # Insert new doctor
        else:
            ret = Doctor.insertDoctor(id_owner=args['id_owner'],
                                      code=args['code'],
                                      nom=args['lastname'],
                                      prenom=args['firstname'],
                                      ville=args['city'],
                                      etablissement=args['work_place'],
                                      specialite=args['spe'],
                                      tel=args['phone'],
                                      email=args['email'],
                                      titre=args['title'],
                                      initiale=args['initial'],
                                      service=args['service'],
                                      adresse=args['address'],
                                      mobile=args['mobile'],
                                      fax=args['fax'])

            if ret <= 0:
                self.log.error(Logs.alert() + ' : DoctorDet ERROR  insert')
                return compose_ret('', Constants.cst_content_type_json, 500)

            id_doctor = ret

        self.log.info(Logs.fileline() + ' : TRACE DoctorDet id_doctor=' + str(id_doctor))
        return compose_ret('', Constants.cst_content_type_json)

    def delete(self, id_doctor):
        ret = Doctor.deleteDoctor(id_doctor)

        if not ret:
            self.log.error(Logs.fileline() + ' : TRACE DoctorDet delete ERROR')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE DoctorDet delete id_item=' + str(id_doctor))
        return compose_ret('', Constants.cst_content_type_json)


class DoctorExport(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        if not args:
            args = {}

        args['limit'] = 50000  # for overpassed default limit

        l_data = [['id_data', 'id_owner', 'code', 'lastname', 'firstname', 'city',
                   'work_place', 'spe', 'spe_id', 'phone', 'mobile', 'fax', 'email', 'title',
                   'initial', 'service', 'address', ]]
        dict_data = Doctor.getDoctorList(args)

        if dict_data:
            for d in dict_data:
                data = []

                data.append(d['id_data'])
                data.append(d['id_owner'])
                data.append(d['code'])
                data.append(d['lastname'])
                data.append(d['firstname'])
                data.append(d['city'])
                data.append(d['work_place'])
                data.append(d['spe'])
                data.append(d['spe_id'])
                data.append(d['phone'])
                data.append(d['mobile'])
                data.append(d['fax'])
                data.append(d['email'])
                data.append(d['title'])
                data.append(d['initial'])
                data.append(d['service'])
                data.append(d['address'])

                l_data.append(data)

        # if no result to export
        if len(l_data) < 2:
            return compose_ret('', Constants.cst_content_type_json, 404)

        # write csv file
        try:
            import csv

            today = datetime.now().strftime("%Y%m%d")

            filename = 'doctor_' + str(today) + '.csv'

            with open('tmp/' + filename, mode='w', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=';')
                for line in l_data:
                    writer.writerow(line)

        except Exception as err:
            self.log.error(Logs.fileline() + ' : post DoctorExport failed, err=%s', err)
            return False

        self.log.info(Logs.fileline() + ' : TRACE DoctorExport')
        return compose_ret('', Constants.cst_content_type_json)
