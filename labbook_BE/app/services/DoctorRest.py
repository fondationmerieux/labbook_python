# -*- coding:utf-8 -*-
import logging

from datetime import datetime
from flask import request
from flask_restful import Resource

from app.models.Audit import Audit
from app.models.General import compose_ret
from app.models.Constants import Constants
from app.models.Doctor import Doctor
# from app.models.User import User
from app.models.Logs import Logs
from app.models.Various import Various
from app.security.oauth_routes import require_oauth


class DoctorList(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        if not args:
            args = {}

        l_doctors = Doctor.getDoctorList(args)

        if not l_doctors:
            self.log.error(Logs.fileline() + ' : TRACE DoctorList not found')

        Various.useLangDB()

        for doctor in l_doctors:
            # Replace None by empty string
            for key, value in list(doctor.items()):
                if doctor[key] is None:
                    doctor[key] = ''
                elif key == 'spe' and doctor[key]:
                    doctor[key] = _(doctor[key].strip())

        self.log.info(Logs.fileline() + ' : TRACE DoctorList')
        try:
            details = {"result": "SUCCESS", "count": len(l_doctors) if l_doctors else 0}
            Audit.insertAudit(audit_user, "DoctorList", "DOCTOR", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : DoctorList ERROR audit success')
        return compose_ret(l_doctors, Constants.cst_content_type_json)


class DoctorSearch(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        l_doctors = Doctor.getDoctorSearch(args['term'])

        if not l_doctors:
            self.log.error(Logs.fileline() + ' : TRACE DoctorSearch not found')

        self.log.info(Logs.fileline() + ' : TRACE DoctorSearch')
        try:
            details = {"result": "SUCCESS", "term": args.get('term'), "count": len(l_doctors) if l_doctors else 0}
            Audit.insertAudit(audit_user, "DoctorSearch", "DOCTOR", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : DoctorSearch ERROR audit success')
        return compose_ret(l_doctors, Constants.cst_content_type_json)


class DoctorDet(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self, id_doctor):
        audit_user = request.oauth_user
        doctor = Doctor.getDoctor(id_doctor)

        if not doctor:
            self.log.error(Logs.fileline() + ' : ' + 'DoctorDet ERROR not found')
            try:
                details = {"result": "ERROR", "reason": "NOT_FOUND", "id_doctor": int(id_doctor)}
                Audit.insertAudit(audit_user, "DoctorDet", "DOCTOR", id_doctor, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : DoctorDet ERROR audit not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        Various.useLangDB()

        # Replace None by empty string
        for key, value in list(doctor.items()):
            if doctor[key] is None:
                doctor[key] = ''
            elif key == 'spe_doctor' and doctor[key]:
                doctor[key] = _(doctor[key].strip())

        self.log.info(Logs.fileline() + ' : DoctorDet id_doctor=' + str(id_doctor))
        try:
            details = {"result": "SUCCESS", "id_doctor": id_doctor}
            Audit.insertAudit(audit_user, "DoctorDet", "DOCTOR", id_doctor, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : DoctorDet ERROR audit success')
        return compose_ret(doctor, Constants.cst_content_type_json, 200)

    @require_oauth()
    def post(self, id_doctor):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        if 'id_owner' not in args or 'id_doctor' not in args or 'code' not in args or 'title' not in args or \
           'lastname' not in args or 'firstname' not in args or 'initial' not in args or 'facility' not in args or \
           'service' not in args or 'address' not in args or 'city' not in args or 'zipcity' not in args or \
           'spe' not in args or 'phone' not in args or 'mobile' not in args or 'fax' not in args or 'email' not in args:
            self.log.error(Logs.fileline() + ' : DoctorDet ERROR args missing')
            try:
                details = {"result": "ERROR", "reason": "ARGS_MISSING", "id_doctor": id_doctor}
                Audit.insertAudit(audit_user, "DoctorDet", "DOCTOR", id_doctor, "ERROR", details, "U" if int(id_doctor) > 0 else "C")
            except Exception:
                self.log.exception(Logs.fileline() + ' : DoctorDet ERROR audit args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        if 'doc_agreement' not in args:
            args['doc_agreement'] = 'N'

        # Update doctor
        if id_doctor > 0:
            ret = Doctor.updateDoctor(id_data=id_doctor,
                                      id_owner=args['id_owner'],
                                      code=args['code'],
                                      nom=args['lastname'],
                                      prenom=args['firstname'],
                                      ville=args['city'],
                                      facility=args['facility'],
                                      specialite=args['spe'],
                                      tel=args['phone'],
                                      email=args['email'],
                                      titre=args['title'],
                                      initiale=args['initial'],
                                      service=args['service'],
                                      adresse=args['address'],
                                      mobile=args['mobile'],
                                      fax=args['fax'],
                                      zipcity=args['zipcity'],
                                      doc_agreement=args['doc_agreement'])

            if ret is False:
                self.log.error(Logs.alert() + ' : DoctorDet ERROR update')
                try:
                    details = {"result": "ERROR", "reason": "UPDATE_FAILED", "id_doctor": id_doctor}
                    Audit.insertAudit(audit_user, "DoctorDet", "DOCTOR", id_doctor, "ERROR", details, "U")
                except Exception:
                    self.log.exception(Logs.fileline() + ' : DoctorDet ERROR audit update failed')
                return compose_ret('', Constants.cst_content_type_json, 500)

        # Insert new doctor
        else:
            ret = Doctor.insertDoctor(id_owner=args['id_owner'],
                                      code=args['code'],
                                      nom=args['lastname'],
                                      prenom=args['firstname'],
                                      ville=args['city'],
                                      facility=args['facility'],
                                      specialite=args['spe'],
                                      tel=args['phone'],
                                      email=args['email'],
                                      titre=args['title'],
                                      initiale=args['initial'],
                                      service=args['service'],
                                      adresse=args['address'],
                                      mobile=args['mobile'],
                                      fax=args['fax'],
                                      zipcity=args['zipcity'],
                                      doc_agreement=args['doc_agreement'])

            if ret <= 0:
                self.log.error(Logs.alert() + ' : DoctorDet ERROR  insert')
                try:
                    details = {"result": "ERROR", "reason": "INSERT_FAILED", "id_doctor": id_doctor}
                    Audit.insertAudit(audit_user, "DoctorDet", "DOCTOR", id_doctor, "ERROR", details, "C")
                except Exception:
                    self.log.exception(Logs.fileline() + ' : DoctorDet ERROR audit insert failed')
                return compose_ret('', Constants.cst_content_type_json, 500)

            id_doctor = ret

        self.log.info(Logs.fileline() + ' : TRACE DoctorDet id_doctor=' + str(id_doctor))
        try:
            event_type = "U" if int(id_doctor) > 0 else "C"
            details = {"result": "SUCCESS", "id_doctor": int(id_doctor)}
            Audit.insertAudit(audit_user, "DoctorDet", "DOCTOR", int(id_doctor), "SUCCESS", details, event_type)
        except Exception:
            self.log.exception(Logs.fileline() + ' : DoctorDet ERROR audit success')
        return compose_ret('', Constants.cst_content_type_json)

    @require_oauth()
    def delete(self, id_doctor):
        audit_user = request.oauth_user
        ret = Doctor.deleteDoctor(id_doctor)

        if not ret:
            self.log.error(Logs.fileline() + ' : TRACE DoctorDet delete ERROR')
            try:
                details = {"result": "ERROR", "reason": "DELETE_FAILED", "id_doctor": id_doctor}
                Audit.insertAudit(audit_user, "DoctorDet", "DOCTOR", id_doctor, "ERROR", details, "D")
            except Exception:
                self.log.exception(Logs.fileline() + ' : DoctorDet ERROR audit delete failed')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE DoctorDet delete id_item=' + str(id_doctor))
        try:
            details = {"result": "SUCCESS", "id_doctor": id_doctor}
            Audit.insertAudit(audit_user, "DoctorDet", "DOCTOR", id_doctor, "SUCCESS", details, "D")
        except Exception:
            self.log.exception(Logs.fileline() + ' : DoctorDet ERROR audit success')
        return compose_ret('', Constants.cst_content_type_json)


class DoctorExport(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        if not args:
            args = {}

        args['limit'] = 50000  # for overpassed default limit

        l_data = [['id_data', 'id_owner', 'code', 'lastname', 'firstname', 'zipcity', 'city',
                   'facility', 'spe', 'spe_id', 'phone', 'mobile', 'fax', 'email', 'title',
                   'initial', 'service', 'address', 'agreement']]
        dict_data = Doctor.getDoctorList(args)

        Various.useLangDB()

        if dict_data:
            for d in dict_data:
                data = []

                data.append(d['id_data'])
                data.append(d['id_owner'])
                data.append(d['code'])
                data.append(d['lastname'])
                data.append(d['firstname'])
                data.append(d['doc_zipcity'])
                data.append(d['city'])
                data.append(d['facility'])
                spe = d['spe']
                if spe:
                    data.append(_(spe.strip()))
                else:
                    data.append('')
                data.append(d['spe_id'])
                data.append(d['phone'])
                data.append(d['mobile'])
                data.append(d['fax'])
                data.append(d['email'])
                data.append(d['title'])
                data.append(d['initial'])
                data.append(d['service'])
                data.append(d['address'])
                data.append(d['doc_agreement'])

                l_data.append(data)

        # if no result to export
        if len(l_data) < 2:
            try:
                details = {"result": "NOT_FOUND"}
                Audit.insertAudit(audit_user, "DoctorExport", "DOCTOR", None, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : DoctorExport ERROR audit not found')
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
            self.log.exception(Logs.fileline() + ' : post DoctorExport failed')
            try:
                details = {"result": "ERROR", "reason": "EXCEPTION", "error": str(err)}
                Audit.insertAudit(audit_user, "DoctorExport", "DOCTOR", None, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : DoctorExport ERROR audit exception')
            return False

        self.log.info(Logs.fileline() + ' : TRACE DoctorExport')
        try:
            details = {"result": "SUCCESS", "count": len(l_data) - 1}
            Audit.insertAudit(audit_user, "DoctorExport", "DOCTOR", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : DoctorExport ERROR audit success')
        return compose_ret('', Constants.cst_content_type_json)
