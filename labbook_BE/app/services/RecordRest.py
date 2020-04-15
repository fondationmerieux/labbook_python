# -*- coding:utf-8 -*-
import logging

from datetime import datetime
from flask import request
from flask_restful import Resource

from app.models.General import compose_ret
from app.models.Constants import *
from app.models.Record import *
from app.models.Various import *
from app.models.User import *
from app.models.Logs import Logs


class RecordList(Resource):
    log = logging.getLogger('log_services')

    def post(self, id_group):
        args = request.get_json()

        id_lab = User.getUserGroupParent(id_group)

        if not args:
            args = {}

        l_records = Record.getRecordList(args, id_lab['id_group_parent'], id_group)

        if not l_records:
            self.log.error(Logs.fileline() + ' : TRACE RecordList not found')

        self.log.info(Logs.fileline() + ' : TRACE RecordList')
        return compose_ret(l_records, Constants.cst_content_type_json)


class RecordDet(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_rec):
        record = Record.getRecord(id_rec)

        if not record:
            self.log.error(Logs.fileline() + ' : ' + 'RecordDet ERROR not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        # Replace None by empty string
        for key, value in record.items():
            if record[key] is None:
                record[key] = ''

        record['date_dos'] = datetime.strftime(record['date_dos'], '%Y-%m-%d')
        record['date_prescription'] = datetime.strftime(record['date_prescription'], '%Y-%m-%d')

        if record['date_reception_colis']:
            record['date_reception_colis'] = datetime.strftime(record['date_reception_colis'], '%Y-%m-%d')

        # decimal number not serializable in JSON, convert except if empty string
        if record['prix'] != '':
            record['prix'] = float(record['prix'])

        if record['remise_pourcent'] != '':
            record['remise_pourcent'] = float(record['remise_pourcent'])

        if record['assu_pourcent'] != '':
            record['assu_pourcent'] = float(record['assu_pourcent'])

        if record['a_payer'] != '':
            record['a_payer'] = float(record['a_payer'])

        self.log.info(Logs.fileline() + ' : DEBUG RecordDet record=' + str(record))

        self.log.info(Logs.fileline() + ' : RecordDet id_rec=' + str(id_rec))
        return compose_ret(record, Constants.cst_content_type_json, 200)

    def post(self, id_rec=0):
        args = request.get_json()

        if 'id_owner' not in args or 'type' not in args or 'date_record' not in args or 'id_med' not in args or 'date_prescr' not in args or 'service_int' not in args or \
           'bed_num' not in args or 'parcel_id' not in args or 'date_parcel' not in args or 'comm' not in args or 'parcel' not in args or \
           'price' not in args or 'discount' not in args or 'percent_discount' not in args or 'percent_insurance' not in args or \
           'bill_remain' not in args or 'receipt_num' not in args or 'bill_num' not in args or 'stat' not in args or 'id_patient' not in args:
            self.log.error(Logs.fileline() + ' : RecordDet ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # Update Record
        if id_rec != 0:
            self.log.error(Logs.fileline() + ' : DEBUG TODO ? RecordDet update')

            """
            Record = Record.getRecord(id_rec)

            if not Record:
                self.log.error(Logs.fileline() + ' : RecordDet ERROR not found')
                return compose_ret('', Constants.cst_content_type_json, 500)

            ret = Record.updateRecord(id=id_pat,
                                        id_owner=args['id_owner'],
                                        anonyme=args['anonyme'],
                                        code=args['code'],
                                        code_Record=args['code_Record'],
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
                self.log.error(Logs.alert() + ' : RecordDet ERROR update')
                return compose_ret('', Constants.cst_content_type_json, 500)

            res = {}
            res['id_rec'] = id_rec"""

        # Insert new Record
        else:
            self.log.error(Logs.fileline() + ' : DEBUG RecordDet insert')

            args['date_record'] = datetime.strptime(args['date_record'], Constants.cst_isodate)
            args['date_prescr'] = datetime.strptime(args['date_prescr'], Constants.cst_isodate)

            if args['date_parcel']:
                args['date_parcel'] = datetime.strptime(args['date_parcel'], Constants.cst_isodate)

            # Increases num_dos_jour, num_dos_an and num_dos_mois
            # num_dos_jour = yyyymmddXXXX +1 if same day
            # num_dos_mois = yyyymmXXXX   +1 if same month
            # num_dos_an   = yyyyXXXXXX   +1 if same year

            num_dos = Various.getLastNumDos()

            if not num_dos:
                self.log.error(Logs.fileline() + ' : RecordDet num_dos not found, first num_dos')
                date_now = datetime.now().strftime("%Y%m%d")
                num_dos = {}
                num_dos['num_dos_jour'] = date_now + '0000'
                num_dos['num_dos_mois'] = date_now[:6] + '0000'
                num_dos['num_dos_an']   = date_now[:4] + '000000'

            num_dos_jour = num_dos['num_dos_jour']
            num_dos_mois = num_dos['num_dos_mois']
            num_dos_an   = num_dos['num_dos_an']

            date_now = datetime.now().strftime("%Y%m%d")

            date_record = args['date_record'].strftime("%Y%m%d")

            # Different day so we start a new number
            if num_dos_jour[:8] != date_now:
                num_dos_jour = date_record + '0001'
            else:
                num_jour  = num_dos_jour[8:]
                num_jour  = int(num_jour)
                num_jour += 1
                num_jour  = str(num_jour).rjust(4, '0')

                num_dos_jour = date_record + num_jour

            # Different month so we start a new number
            if num_dos_mois[:6] != date_now[:6]:
                num_dos_mois = date_record[:6] + '0001'
            else:
                num_mois  = num_dos_mois[6:]
                num_mois  = int(num_mois)
                num_mois += 1
                num_mois  = str(num_mois).rjust(4, '0')

                num_dos_mois = date_record[:6] + num_mois

            # Different year so we start a new number
            if num_dos_an[:4] != date_now[:4]:
                num_dos_an = date_record[:4] + '000001'
            else:
                num_an  = num_dos_an[4:]
                num_an  = int(num_an)
                num_an += 1
                num_an  = str(num_an).rjust(6, '0')

                num_dos_an = date_record[:4] + num_an

            ret = Record.insertRecord(id_owner=args['id_owner'],
                                      id_patient=args['id_patient'],
                                      type=args['type'],
                                      date_dos=args['date_record'],
                                      num_dos_jour=num_dos_jour,
                                      num_dos_an=num_dos_an,
                                      med_prescripteur=args['id_med'],
                                      date_prescription=args['date_prescr'],
                                      service_interne=args['service_int'],
                                      num_lit=args['bed_num'],
                                      id_colis=args['parcel_id'],
                                      date_reception_colis=args['date_parcel'],
                                      rc=args['comm'],
                                      colis=args['parcel'],
                                      prix=args['price'],
                                      remise=args['discount'],
                                      remise_pourcent=args['percent_discount'],
                                      assu_pourcent=args['percent_insurance'],
                                      a_payer=args['bill_remain'],
                                      num_quittance=args['receipt_num'],
                                      num_fact=args['bill_num'],
                                      statut=args['stat'],
                                      num_dos_mois=num_dos_mois)

            if ret <= 0:
                self.log.error(Logs.alert() + ' : RecordDet ERROR  insert')
                return compose_ret('', Constants.cst_content_type_json, 500)

            res = {}
            res['id_rec'] = ret

            # Get id_group of lab with id_group of user
            id_group_lab = User.getUserGroupParent(args['id_owner'])

            if not id_group_lab:
                self.log.error(Logs.fileline() + ' : RecordDet ERROR group not found')
                return compose_ret('', Constants.cst_content_type_json, 500)

            # insert sigl_02_data_group
            ret = Record.insertRecordGroup(id_data=res['id_rec'],
                                           id_group=id_group_lab['id_group_parent'])

            if ret <= 0:
                self.log.error(Logs.alert() + ' : RecordDet ERROR  insert group')
                return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE RecordDet id_rec=' + str(res['id_rec']))
        return compose_ret(res, Constants.cst_content_type_json)


class RecordStat(Resource):
    log = logging.getLogger('log_services')

    def post(self, id_rec):
        args = request.get_json()

        if 'stat' not in args:
            self.log.error(Logs.fileline() + ' : RecordStat ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        ret = Record.updateRecordStat(id_rec, args['stat'])

        if not ret:
            self.log.error(Logs.fileline() + ' : ERROR RecordStat update')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE RecordStat')
        return compose_ret('', Constants.cst_content_type_json)


class RecordTypeNumber(Resource):
    log = logging.getLogger('log_services')

    def get(self):
        param = Record.getRecordTypeNumber()

        if not param:
            self.log.error(Logs.fileline() + ' : ERROR RecordTypeNumber not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        # Replace None by empty string
        for key, value in param.items():
            if param[key] is None:
                param[key] = ''

        if param['sys_creation_date']:
            param['sys_creation_date'] = datetime.strftime(param['sys_creation_date'], '%Y-%m-%d %H:%M:%S')

        if param['sys_last_mod_date']:
            param['sys_last_mod_date'] = datetime.strftime(param['sys_last_mod_date'], '%Y-%m-%d %H:%M:%S')

        self.log.info(Logs.fileline() + ' : TRACE RecordTypeNumber')
        return compose_ret(param, Constants.cst_content_type_json)
