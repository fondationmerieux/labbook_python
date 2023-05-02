# -*- coding:utf-8 -*-
import logging
import gettext

from datetime import datetime
from flask import request
from flask_restful import Resource

from app.models.Analysis import Analysis
from app.models.General import compose_ret
from app.models.Constants import Constants
from app.models.File import File
from app.models.Product import Product
from app.models.Record import Record
from app.models.Result import Result
from app.models.Various import Various
from app.models.Logs import Logs


class RecordList(Resource):
    log = logging.getLogger('log_services')

    def post(self, id_pres):
        args = request.get_json()

        if not args:
            args = {}

        l_records = Record.getRecordList(args, id_pres)

        if not l_records:
            self.log.error(Logs.fileline() + ' : TRACE RecordList not found')

        for record in l_records:
            # Replace None by empty string
            for key, value in list(record.items()):
                if record[key] is None:
                    record[key] = ''

            if record['type_rec'] and record['type_rec'] == 183:
                record['type_rec'] = 'E'
            else:
                record['type_rec'] = 'I'

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
        for key, value in list(record.items()):
            if record[key] is None:
                record[key] = ''

        if record['date_dos']:
            record['date_dos'] = datetime.strftime(record['date_dos'], '%Y-%m-%d')

        if record['date_prescription']:
            record['date_prescription'] = datetime.strftime(record['date_prescription'], '%Y-%m-%d')

        if record['date_reception_colis']:
            record['date_reception_colis'] = datetime.strftime(record['date_reception_colis'], '%Y-%m-%d')

        if record['date_hosp']:
            record['date_hosp'] = datetime.strftime(record['date_hosp'], '%Y-%m-%d')

        if record['rec_date_vld']:
            record['rec_date_vld'] = datetime.strftime(record['rec_date_vld'], '%Y-%m-%d %H:%M')

        # decimal number not serializable in JSON, convert except if empty string
        if record['prix']:
            record['prix'] = float(record['prix'])
        else:
            record['prix'] = 0

        if record['remise_pourcent']:
            record['remise_pourcent'] = float(record['remise_pourcent'])
        else:
            record['remise_pourcent'] = 0

        if record['assu_pourcent']:
            record['assu_pourcent'] = float(record['assu_pourcent'])
        else:
            record['assu_pourcent'] = 0

        if record['a_payer']:
            record['a_payer'] = float(record['a_payer'])
        else:
            record['a_payer'] = 0

        self.log.info(Logs.fileline() + ' : RecordDet id_rec=' + str(id_rec))
        return compose_ret(record, Constants.cst_content_type_json, 200)

    def post(self, id_rec=0):
        args = request.get_json()

        if 'id_owner' not in args or 'type' not in args or 'date_record' not in args or 'id_med' not in args or \
           'date_prescr' not in args or 'service_int' not in args or 'bed_num' not in args or 'parcel_id' not in args or \
           'date_parcel' not in args or 'comm' not in args or 'parcel' not in args or 'date_hosp' not in args or \
           'price' not in args or 'discount' not in args or 'percent_discount' not in args or \
           'percent_insurance' not in args or 'bill_remain' not in args or 'receipt_num' not in args or \
           'bill_num' not in args or 'stat' not in args or 'id_patient' not in args or 'rec_custody' not in args or \
           'rec_num_int' not in args or 'rec_modified' not in args:
            self.log.error(Logs.fileline() + ' : RecordDet ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # Insert Record
        if id_rec == 0:
            args['date_record'] = datetime.strptime(args['date_record'], Constants.cst_isodate)
            args['date_prescr'] = datetime.strptime(args['date_prescr'], Constants.cst_isodate)

            if args['date_parcel']:
                args['date_parcel'] = datetime.strptime(args['date_parcel'], Constants.cst_isodate)

            if args['date_hosp']:
                args['date_hosp'] = datetime.strptime(args['date_hosp'], Constants.cst_isodate)

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
                self.log.info(Logs.fileline() + ' : DEBUG RecordDet num_dos_jour [' + str(num_dos_jour[:8]) + '] != date_now [' + str(date_now) + ']')
                num_dos_jour = date_record + '0001'
            else:
                num_jour  = num_dos_jour[8:]
                num_jour  = int(num_jour)
                num_jour += 1
                num_jour  = str(num_jour).rjust(4, '0')

                num_dos_jour = date_record + num_jour

            # Different month so we start a new number
            if num_dos_mois[:6] != date_now[:6]:
                self.log.info(Logs.fileline() + ' : DEBUG RecordDet num_dos_mois [' + str(num_dos_mois[:6]) + '] != date_now [' + str(date_now) + ']')
                num_dos_mois = date_record[:6] + '0001'
            else:
                num_mois  = num_dos_mois[6:]
                num_mois  = int(num_mois)
                num_mois += 1
                num_mois  = str(num_mois).rjust(4, '0')

                num_dos_mois = date_record[:6] + num_mois

            # Different year so we start a new number
            if num_dos_an[:4] != date_now[:4]:
                self.log.info(Logs.fileline() + ' : DEBUG RecordDet num_dos_an [' + str(num_dos_an[:4]) + '] != date_now[' + str(date_now) + ']')
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
                                      num_dos_mois=num_dos_mois,
                                      date_hosp=args['date_hosp'],
                                      rec_custody=args['rec_custody'],
                                      rec_num_int=args['rec_num_int'],
                                      rec_modified=args['rec_modified'])

            if ret <= 0:
                self.log.error(Logs.alert() + ' : RecordDet ERROR  insert')
                return compose_ret('', Constants.cst_content_type_json, 500)

            res = {}
            res['id_rec'] = ret

            # insert in sigl_pj_sequence num_dos_jour
            pattern = num_dos_jour[:8] + "%04d"  # make pattern for table
            end_num = int(num_dos_jour[8:])      # get end number without 0
            ret = Record.insertPjSequence("numdosjour", pattern, end_num)

            if ret <= 0:
                self.log.error(Logs.alert() + ' : RecordDet ERROR  insertPjSequence numdosjour')

            # insert in sigl_pj_sequence num_dos_an
            pattern = num_dos_an[:4] + "%06d"
            end_num = int(num_dos_an[4:])
            ret = Record.insertPjSequence("numdosan", pattern, end_num)

            if ret <= 0:
                self.log.error(Logs.alert() + ' : RecordDet ERROR  insertPjSequence numdosan')

            # insert in sigl_pj_sequence num_dos_mois
            pattern = num_dos_mois[:6] + "%04d"
            end_num = int(num_dos_mois[6:])
            ret = Record.insertPjSequence("numdosmois", pattern, end_num)

            if ret <= 0:
                self.log.error(Logs.alert() + ' : RecordDet ERROR  insertPjSequence numdosmois')

        self.log.info(Logs.fileline() + ' : TRACE RecordDet id_rec=' + str(res['id_rec']))
        return compose_ret(res, Constants.cst_content_type_json)

    def delete(self, id_rec):
        # delete sigl_11_data with id_dos = id_rec
        ret = File.deleteFileReportByRecord(id_rec)

        if not ret:
            self.log.error(Logs.fileline() + ' : TRACE RecordDet delete FileReport ERROR')
            return compose_ret('', Constants.cst_content_type_json, 500)

        # delete sigl_dos_valisedoc__file_data with id_ext = id_rec
        ret = File.deleteFileDocByRecord(id_rec)

        if not ret:
            self.log.error(Logs.fileline() + ' : TRACE RecordDet delete FileDoc ERROR')
            return compose_ret('', Constants.cst_content_type_json, 500)

        # load result requested with id_rec to get list of id_data
        l_res = Result.getResultRecord(id_rec)

        for res in l_res:
            # delete sigl_10_data with id_resultat = id_data list
            ret = Result.deleteValidationByResult(res['id_res'])

            if not ret:
                self.log.error(Logs.fileline() + ' : TRACE RecordDet delete Validation ERROR')
                return compose_ret('', Constants.cst_content_type_json, 500)

            # delete sigl_09_data with id_resultat = id_res
            ret = Result.deleteResult(res['id_res'])

            if not ret:
                self.log.error(Logs.fileline() + ' : TRACE RecordDet delete Result ERROR')
                return compose_ret('', Constants.cst_content_type_json, 500)

        # delete sigl_04_data with id_dos = id_rec
        ret = Analysis.deleteAnalysisByRecord(id_rec)

        if not ret:
            self.log.error(Logs.fileline() + ' : TRACE RecordDet delete Analysis ERROR')
            return compose_ret('', Constants.cst_content_type_json, 500)

        # delete sigl_01_data with id_dos = id_rec
        ret = Product.deleteProductByRecord(id_rec)

        if not ret:
            self.log.error(Logs.fileline() + ' : TRACE RecordDet delete Product ERROR')
            return compose_ret('', Constants.cst_content_type_json, 500)

        # delete sigl_02_data with id_data = id_rec
        ret = Record.deleteRecord(id_rec)

        if not ret:
            self.log.error(Logs.fileline() + ' : TRACE RecordDet delete Record ERROR')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE RecordDet delete')
        return compose_ret('', Constants.cst_content_type_json)


class RecordComm(Resource):
    log = logging.getLogger('log_services')

    def post(self, id_rec):
        args = request.get_json()

        if 'comm' not in args:
            self.log.error(Logs.fileline() + ' : RecordComm ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        ret = Record.updateRecordComm(id_rec, args['comm'])

        if not ret:
            self.log.error(Logs.fileline() + ' : ERROR RecordComm update')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE RecordComm')
        return compose_ret('', Constants.cst_content_type_json)


class RecordLast(Resource):
    log = logging.getLogger('log_services')

    def get(self):
        record = Record.getLastRecord()

        if not record:
            self.log.error(Logs.fileline() + ' : ' + 'RecordLast ERROR not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        # Replace None by empty string
        for key, value in list(record.items()):
            if record[key] is None:
                record[key] = ''

        if record['date_dos']:
            record['date_dos'] = datetime.strftime(record['date_dos'], '%Y-%m-%d')

        if record['date_prescription']:
            record['date_prescription'] = datetime.strftime(record['date_prescription'], '%Y-%m-%d')

        if record['date_reception_colis']:
            record['date_reception_colis'] = datetime.strftime(record['date_reception_colis'], '%Y-%m-%d')

        if record['date_hosp']:
            record['date_hosp'] = datetime.strftime(record['date_hosp'], '%Y-%m-%d')

        # decimal number not serializable in JSON, convert except if empty string
        if record['prix']:
            record['prix'] = float(record['prix'])
        else:
            record['prix'] = 0

        if record['remise_pourcent']:
            record['remise_pourcent'] = float(record['remise_pourcent'])
        else:
            record['remise_pourcent'] = 0

        if record['assu_pourcent']:
            record['assu_pourcent'] = float(record['assu_pourcent'])
        else:
            record['assu_pourcent'] = 0

        if record['a_payer']:
            record['a_payer'] = float(record['a_payer'])
        else:
            record['a_payer'] = 0

        self.log.info(Logs.fileline() + ' : RecordLast')
        return compose_ret(record, Constants.cst_content_type_json, 200)


class RecordFile(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_rec):
        l_files = Record.getRecordFile(id_rec)

        if not l_files:
            self.log.error(Logs.fileline() + ' : TRACE RecordFile not found')

        for files in l_files:
            # Replace None by empty string
            for key, value in list(files.items()):
                if files[key] is None:
                    files[key] = ''

        self.log.info(Logs.fileline() + ' : TRACE RecordFile')
        return compose_ret(l_files, Constants.cst_content_type_json)


class RecordNext(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_rec):
        id_rec_next = 0

        rec = Record.getRecordNext(id_rec)

        if not rec:
            self.log.error(Logs.fileline() + ' : TRACE RecordNext not found')
        else:
            id_rec_next = rec['id_data']

        self.log.info(Logs.fileline() + ' : TRACE RecordNext')
        return compose_ret(id_rec_next, Constants.cst_content_type_json)


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


class RecordListAna(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_rec):
        l_datas = Record.getRecordListAnalysis(id_rec)

        if not l_datas:
            self.log.error(Logs.fileline() + ' : ' + 'RecordListAna ERROR not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        Various.useLangDB()

        for data in l_datas:
            # Replace None by empty string
            for key, value in list(data.items()):
                if data[key] is None:
                    data[key] = ''
                elif key == 'name' and data[key]:
                    data[key] = _(data[key].strip())

        self.log.info(Logs.fileline() + ' : RecordListAna id_rec=' + str(id_rec))
        return compose_ret(l_datas, Constants.cst_content_type_json, 200)


class RecordNbEmer(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        if not args:
            args = {}

        res = Record.getRecordNbEmer(args)

        if not res:
            self.log.error(Logs.fileline() + ' : TRACE RecordNbEmer not found')
            nb_emer = 0
        else:
            nb_emer = res['nb_emer']

        self.log.info(Logs.fileline() + ' : TRACE RecordNbEmer')
        return compose_ret(nb_emer, Constants.cst_content_type_json)


class RecordNbRecTech(Resource):
    log = logging.getLogger('log_services')

    def get(self):
        res = Record.getRecordNbRecTech()

        if not res:
            self.log.error(Logs.fileline() + ' : TRACE RecordNbRecTech not found')
            nb_rec_tech = 0
        else:
            nb_rec_tech = res['nb_rec_tech']

        self.log.info(Logs.fileline() + ' : TRACE RecordNbRecTech')
        return compose_ret(nb_rec_tech, Constants.cst_content_type_json)


class RecordNbRecBio(Resource):
    log = logging.getLogger('log_services')

    def get(self):
        res = Record.getRecordNbRecBio()

        if not res:
            self.log.error(Logs.fileline() + ' : TRACE RecordNbRecBio not found')
            nb_rec_bio = 0
        else:
            nb_rec_bio = res['nb_rec_bio']

        self.log.info(Logs.fileline() + ' : TRACE RecordNbRecBio')
        return compose_ret(nb_rec_bio, Constants.cst_content_type_json)


class RecordNbRec(Resource):
    log = logging.getLogger('log_services')

    def get(self):
        res = Record.getRecordNbRec()

        if not res:
            self.log.error(Logs.fileline() + ' : TRACE RecordNbRec not found')
            nb_rec = 0
        else:
            nb_rec = res['nb_rec']

        self.log.info(Logs.fileline() + ' : TRACE RecordNbRec')
        return compose_ret(nb_rec, Constants.cst_content_type_json)


class RecordNbRecToday(Resource):
    log = logging.getLogger('log_services')

    def get(self):
        num_today = datetime.now().strftime("%Y%m%d")

        res = Record.getRecordNbRecToday(num_today)

        if not res:
            self.log.error(Logs.fileline() + ' : TRACE RecordNbRecToday not found')
            nb_rec_today = 0
        else:
            nb_rec_today = res['nb_rec_today']

        self.log.info(Logs.fileline() + ' : TRACE RecordNbRecToday')
        return compose_ret(nb_rec_today, Constants.cst_content_type_json)
