# -*- coding:utf-8 -*-
import logging

from datetime import datetime
from flask import request
from flask_restful import Resource

from app.models.General import compose_ret
from app.models.Constants import *
from app.models.Logs import Logs
from app.models.Quality import *
from app.models.File import *


class QualityLastMeeting(Resource):
    log = logging.getLogger('log_services')

    def get(self):
        meeting = Quality.getLastMeeting()

        if not meeting:
            self.log.error(Logs.fileline() + ' : ' + 'QualityLastMeeting ERROR not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        # Replace None by empty string
        for key, value in meeting.items():
            if meeting[key] is None:
                meeting[key] = ''

        meeting['sys_creation_date'] = datetime.strftime(meeting['sys_creation_date'], '%Y-%m-%d')
        meeting['sys_last_mod_date'] = datetime.strftime(meeting['sys_last_mod_date'], '%Y-%m-%d')

        if meeting['date']:
            meeting['date'] = datetime.strftime(meeting['date'], '%Y-%m-%d')

        self.log.info(Logs.fileline() + ' : QualityLastMeeting')
        return compose_ret(meeting, Constants.cst_content_type_json, 200)


class QualityNbNonCompl(Resource):
    log = logging.getLogger('log_services')

    def get(self, period):
        res = Quality.getNbNonCompliance(period)

        if not res:
            self.log.error(Logs.fileline() + ' : TRACE QualityNbNonCompl not found')
            nb_noncompliance = 0
        else:
            nb_noncompliance = res['nb_noncompliance']

        self.log.info(Logs.fileline() + ' : TRACE QualityNbNonCompl')
        return compose_ret(nb_noncompliance, Constants.cst_content_type_json)


class ConformityList(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        l_items = Quality.getConformityList(args['term'])

        if not l_items:
            self.log.error(Logs.fileline() + ' : TRACE ConformityList not found')

        for item in l_items:
            # Replace None by empty string
            for key, value in item.items():
                if item[key] is None:
                    item[key] = ''

            if item['date_create']:
                item['date_create'] = datetime.strftime(item['date_create'], '%Y-%m-%d')

            if item['date_correction']:
                item['date_correction'] = datetime.strftime(item['date_correction'], '%Y-%m-%d')

            if item['date_close']:
                item['date_close'] = datetime.strftime(item['date_close'], '%Y-%m-%d')

        self.log.info(Logs.fileline() + ' : TRACE ConformityList')
        return compose_ret(l_items, Constants.cst_content_type_json)


class ConformityDet(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_item):
        item = Quality.getConformity(id_item)

        if not item:
            self.log.error(Logs.fileline() + ' : ' + 'ConformityDet ERROR not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        # Replace None by empty string
        for key, value in item.items():
            if item[key] is None:
                item[key] = ''

        if item['date_create']:
            item['date_create'] = datetime.strftime(item['date_create'], '%Y-%m-%d')

        if item['date_correction']:
            item['date_correction'] = datetime.strftime(item['date_correction'], '%Y-%m-%d')

        if item['date_close']:
            item['date_close'] = datetime.strftime(item['date_close'], '%Y-%m-%d')

        self.log.info(Logs.fileline() + ' : ConformityDet id_item=' + str(id_item))
        return compose_ret(item, Constants.cst_content_type_json, 200)

    def post(self, id_item):
        args = request.get_json()

        if 'id_owner' not in args or 'id_item' not in args or 'date_meeting' not in args or \
           'type' not in args or 'promoter' not in args or 'report' not in args:
            self.log.error(Logs.fileline() + ' : ConformityDet ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # Update item
        if id_item > 0:
            ret = Quality.updateConformity(id_data=id_item,
                                           id_owner=args['id_owner'],
                                           date_meeting=args['date_meeting'],
                                           type=args['type'],
                                           promoter=args['promoter'],
                                           report=args['report'])

            if ret is False:
                self.log.error(Logs.alert() + ' : ConformityDet ERROR update')
                return compose_ret('', Constants.cst_content_type_json, 500)

        # Insert new item
        else:
            ret = Quality.insertConformity(id_owner=args['id_owner'],
                                           date_meeting=args['date_meeting'],
                                           type=args['type'],
                                           promoter=args['promoter'],
                                           report=args['report'])

            if ret <= 0:
                self.log.error(Logs.alert() + ' : ConformityDet ERROR  insert')
                return compose_ret('', Constants.cst_content_type_json, 500)

            id_item = ret

        self.log.info(Logs.fileline() + ' : TRACE ConformityDet id_item=' + str(id_item))
        return compose_ret(id_item, Constants.cst_content_type_json)

    def delete(self, id_item):
        ret = Quality.deleteConformity(id_item)

        if not ret:
            self.log.error(Logs.fileline() + ' : TRACE ConformityDet delete ERROR')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE ConformityDet delete id_item=' + str(id_item))
        return compose_ret('', Constants.cst_content_type_json)


class ConformityExport(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        l_data = [['id_data', 'date_create', 'name', 'category', 'impact_patient', 'impact_user',
                   'correction', 'date_correction', 'date_close']]

        if 'date_beg' not in args or 'date_end' not in args:
            self.log.error(Logs.fileline() + ' : ConformityExport ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        dict_data = Quality.getConformityList(args['date_beg'], args['date_end'])

        if dict_data:
            for d in dict_data:
                data = []

                data.append(d['id_data'])
                data.append(d['date_create'])
                data.append(d['name'])
                data.append(d['category'])
                data.append(d['impact_patient'])
                data.append(d['impact_user'])
                data.append(d['correction'])
                data.append(d['date_correction'])
                data.append(d['date_close'])

                l_data.append(data)

        # if no result to export
        if len(l_data) < 2:
            return compose_ret('', Constants.cst_content_type_json, 404)

        # write csv file
        try:
            import csv

            today = datetime.now().strftime("%Y%m%d")

            filename = 'conformity_' + str(today) + '.csv'

            with open('tmp/' + filename, mode='w') as file:
                writer = csv.writer(file, delimiter=';')
                for line in l_data:
                    writer.writerow(line)

        except Exception as err:
            self.log.error(Logs.fileline() + ' : post ExportConformity failed, err=%s', err)
            return False

        self.log.info(Logs.fileline() + ' : TRACE ExportConformity')
        return compose_ret('', Constants.cst_content_type_json)


class EquipmentList(Resource):
    log = logging.getLogger('log_services')

    def get(self):
        l_items = Quality.getEquipmentList()

        if not l_items:
            self.log.error(Logs.fileline() + ' : TRACE EquipmentList not found')

        for item in l_items:
            # Replace None by empty string
            for key, value in item.items():
                if item[key] is None:
                    item[key] = ''

        self.log.info(Logs.fileline() + ' : TRACE EquipmentList')
        return compose_ret(l_items, Constants.cst_content_type_json)


class EquipmentDet(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_item):
        item = Quality.getEquipment(id_item)

        if not item:
            self.log.error(Logs.fileline() + ' : ' + 'EquipmentDet ERROR not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        # Replace None by empty string
        for key, value in item.items():
            if item[key] is None:
                item[key] = ''

        self.log.info(Logs.fileline() + ' : EquipmentDet id_item=' + str(id_item))
        return compose_ret(item, Constants.cst_content_type_json, 200)

    def post(self, id_item):
        args = request.get_json()

        if 'id_owner' not in args or 'id_item' not in args or 'name' not in args or 'maker' not in args or 'model' not in args or \
           'funct' not in args or 'location' not in args or 'section' not in args or 'supplier' not in args or \
           'serial' not in args or 'inventory' not in args or 'incharge' not in args or 'manual' not in args or  \
           'procedur' not in args or 'breakdown' not in args or 'maintenance' not in args or 'calibration' not in args or \
           'contract' not in args or 'date_endcontract' not in args or 'date_receipt' not in args or 'date_buy' not in args or \
           'date_procur' not in args or 'date_onduty' not in args or 'date_revoc' not in args or 'comment' not in args:
            self.log.error(Logs.fileline() + ' : EquipmentDet ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # Update item
        if id_item > 0:
            ret = Quality.updateEquipment(id_data=id_item,
                                          id_owner=args['id_owner'],
                                          name=args['name'],
                                          maker=args['maker'],
                                          model=args['model'],
                                          funct=args['funct'],
                                          location=args['location'],
                                          section=args['section'],
                                          supplier=args['supplier'],
                                          serial=args['serial'],
                                          inventory=args['inventory'],
                                          incharge=args['incharge'],
                                          manual=args['manual'],
                                          procedur=args['procedur'],
                                          breakdown=args['breakdown'],
                                          maintenance=args['maintenance'],
                                          calibration=args['calibration'],
                                          contract=args['contract'],
                                          date_endcontract=args['date_endcontract'],
                                          date_receipt=args['date_receipt'],
                                          date_buy=args['date_buy'],
                                          date_procur=args['date_procur'],
                                          date_onduty=args['date_onduty'],
                                          date_revoc=args['date_revoc'],
                                          comment=args['comment'])

            if ret is False:
                self.log.error(Logs.alert() + ' : EquipmentDet ERROR update')
                return compose_ret('', Constants.cst_content_type_json, 500)

        # Insert new item
        else:
            ret = Quality.insertEquipment(id_owner=args['id_owner'],
                                          name=args['name'],
                                          maker=args['maker'],
                                          model=args['model'],
                                          funct=args['funct'],
                                          location=args['location'],
                                          section=args['section'],
                                          supplier=args['supplier'],
                                          serial=args['serial'],
                                          inventory=args['inventory'],
                                          incharge=args['incharge'],
                                          manual=args['manual'],
                                          procedur=args['procedur'],
                                          breakdown=args['breakdown'],
                                          maintenance=args['maintenance'],
                                          calibration=args['calibration'],
                                          contract=args['contract'],
                                          date_endcontract=args['date_endcontract'],
                                          date_receipt=args['date_receipt'],
                                          date_buy=args['date_buy'],
                                          date_procur=args['date_procur'],
                                          date_onduty=args['date_onduty'],
                                          date_revoc=args['date_revoc'],
                                          comment=args['comment'])

            if ret <= 0:
                self.log.error(Logs.alert() + ' : EquipmentDet ERROR  insert')
                return compose_ret('', Constants.cst_content_type_json, 500)

            id_item = ret

        self.log.info(Logs.fileline() + ' : TRACE EquipmentDet id_item=' + str(id_item))
        return compose_ret(id_item, Constants.cst_content_type_json)

    def delete(self, id_item):
        ret = Quality.deleteEquipment(id_item)

        if not ret:
            self.log.error(Logs.fileline() + ' : TRACE EquipmentDet delete ERROR')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE EquipmentDet delete id_item=' + str(id_item))
        return compose_ret('', Constants.cst_content_type_json)


class EquipmentExport(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        l_data = [['id_data', 'name', 'maker', 'model', 'funct', 'location', 'section', ]]
        dict_data = Quality.getEquipmentList()

        if dict_data:
            for d in dict_data:
                data = []

                data.append(d['id_data'])
                data.append(d['name'])
                data.append(d['maker'])
                data.append(d['model'])
                data.append(d['funct'])
                data.append(d['location'])
                data.append(d['section'])

                l_data.append(data)

        # if no result to export
        if len(l_data) < 2:
            return compose_ret('', Constants.cst_content_type_json, 404)

        # write csv file
        try:
            import csv

            today = datetime.now().strftime("%Y%m%d")

            filename = 'equipment_' + str(today) + '.csv'

            with open('tmp/' + filename, mode='w') as file:
                writer = csv.writer(file, delimiter=';')
                for line in l_data:
                    writer.writerow(line)

        except Exception as err:
            self.log.error(Logs.fileline() + ' : post ExportEquipment failed, err=%s', err)
            return False

        self.log.info(Logs.fileline() + ' : TRACE ExportEquipment')
        return compose_ret('', Constants.cst_content_type_json)


class ManualList(Resource):
    log = logging.getLogger('log_services')

    def get(self):
        l_items = Quality.getManualList()

        if not l_items:
            self.log.error(Logs.fileline() + ' : TRACE ManualList not found')

        for item in l_items:
            # Replace None by empty string
            for key, value in item.items():
                if item[key] is None:
                    item[key] = ''

            if item['date_insert']:
                item['date_insert'] = datetime.strftime(item['date_insert'], '%Y-%m-%d')

            if item['date_apply']:
                item['date_apply'] = datetime.strftime(item['date_apply'], '%Y-%m-%d')

            if item['date_update']:
                item['date_update'] = datetime.strftime(item['date_update'], '%Y-%m-%d')

            # search last id_file for each manual
            l_files = File.getFileDocList("MANU", item['id_data'])

            if l_files and l_files[0]['id_data']:
                item['id_file'] = l_files[0]['id_data']
            else:
                item['id_file'] = 0

            if l_files and l_files[0]['name']:
                item['filename'] = l_files[0]['name']
            else:
                item['filename'] = ''

        self.log.info(Logs.fileline() + ' : TRACE ManualList')
        return compose_ret(l_items, Constants.cst_content_type_json)


class ManualDet(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_item):
        item = Quality.getManual(id_item)

        if not item:
            self.log.error(Logs.fileline() + ' : ' + 'ManualDet ERROR not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        # Replace None by empty string
        for key, value in item.items():
            if item[key] is None:
                item[key] = ''

        if item['date_insert']:
            item['date_insert'] = datetime.strftime(item['date_insert'], '%Y-%m-%d')

        if item['date_apply']:
            item['date_apply'] = datetime.strftime(item['date_apply'], '%Y-%m-%d')

        if item['date_update']:
            item['date_update'] = datetime.strftime(item['date_update'], '%Y-%m-%d')

        self.log.info(Logs.fileline() + ' : ManualDet id_item=' + str(id_item))
        return compose_ret(item, Constants.cst_content_type_json, 200)

    def post(self, id_item):
        args = request.get_json()

        if 'id_owner' not in args or 'id_item' not in args or 'reference' not in args or 'title' not in args or \
           'writer' not in args or 'auditor' not in args or 'approver' not in args or 'date_insert' not in args or \
           'date_apply' not in args or 'date_update' not in args or 'section' not in args:
            self.log.error(Logs.fileline() + ' : ManualDet ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # Update item
        if id_item > 0:
            ret = Quality.updateManual(id_data=id_item,
                                       id_owner=args['id_owner'],
                                       reference=args['reference'],
                                       title=args['title'],
                                       writer=args['writer'],
                                       auditor=args['auditor'],
                                       approver=args['approver'],
                                       date_insert=args['date_insert'],
                                       date_apply=args['date_apply'],
                                       date_update=args['date_update'],
                                       section=args['section'])

            if ret is False:
                self.log.error(Logs.alert() + ' : ManualDet ERROR update')
                return compose_ret('', Constants.cst_content_type_json, 500)

        # Insert new item
        else:
            ret = Quality.insertManual(id_owner=args['id_owner'],
                                       reference=args['reference'],
                                       title=args['title'],
                                       writer=args['writer'],
                                       auditor=args['auditor'],
                                       approver=args['approver'],
                                       date_insert=args['date_insert'],
                                       date_apply=args['date_apply'],
                                       date_update=args['date_update'],
                                       section=args['section'])

            if ret <= 0:
                self.log.error(Logs.alert() + ' : ManualDet ERROR  insert')
                return compose_ret('', Constants.cst_content_type_json, 500)

            id_item = ret

        self.log.info(Logs.fileline() + ' : TRACE ManualDet id_item=' + str(id_item))
        return compose_ret(id_item, Constants.cst_content_type_json)

    def delete(self, id_item):
        ret = Quality.deleteManual(id_item)

        if not ret:
            self.log.error(Logs.fileline() + ' : TRACE ManualDet delete ERROR')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE ManualDet delete id_item=' + str(id_item))
        return compose_ret('', Constants.cst_content_type_json)


class ManualExport(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        l_data = [['id_data', 'title', 'reference', 'writer', 'auditor', 'approver', 'date_insert',
                   'date_apply', 'date_update', 'section', ]]
        dict_data = Quality.getManualList()

        if dict_data:
            for d in dict_data:
                data = []

                data.append(d['id_data'])
                data.append(d['title'])
                data.append(d['reference'])
                data.append(d['writer'])
                data.append(d['auditor'])
                data.append(d['approver'])
                data.append(d['date_insert'])
                data.append(d['date_apply'])
                data.append(d['date_update'])
                data.append(d['section'])

                l_data.append(data)

        # if no result to export
        if len(l_data) < 2:
            return compose_ret('', Constants.cst_content_type_json, 404)

        # write csv file
        try:
            import csv

            today = datetime.now().strftime("%Y%m%d")

            filename = 'manual_' + str(today) + '.csv'

            with open('tmp/' + filename, mode='w') as file:
                writer = csv.writer(file, delimiter=';')
                for line in l_data:
                    writer.writerow(line)

        except Exception as err:
            self.log.error(Logs.fileline() + ' : post ExportManual failed, err=%s', err)
            return False

        self.log.info(Logs.fileline() + ' : TRACE ExportManual')
        return compose_ret('', Constants.cst_content_type_json)


class ManualSearch(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        l_items = Quality.getManualSearch(args['term'])

        if not l_items:
            self.log.error(Logs.fileline() + ' : TRACE ManualSearch not found')

        self.log.info(Logs.fileline() + ' : TRACE ManualSearch')
        return compose_ret(l_items, Constants.cst_content_type_json)


class MeetingList(Resource):
    log = logging.getLogger('log_services')

    def get(self):
        l_items = Quality.getMeetingList()

        if not l_items:
            self.log.error(Logs.fileline() + ' : TRACE MeetingList not found')

        for item in l_items:
            # Replace None by empty string
            for key, value in item.items():
                if item[key] is None:
                    item[key] = ''

            if item['date_meeting']:
                item['date_meeting'] = datetime.strftime(item['date_meeting'], '%Y-%m-%d')

            # search last id_file for each meeting
            l_files = File.getFileDocList("MEET", item['id_data'])

            if l_files and l_files[0]['id_data']:
                item['id_file'] = l_files[0]['id_data']
            else:
                item['id_file'] = 0

            if l_files and l_files[0]['name']:
                item['filename'] = l_files[0]['name']
            else:
                item['filename'] = ''

        self.log.info(Logs.fileline() + ' : TRACE MeetingList')
        return compose_ret(l_items, Constants.cst_content_type_json)


class MeetingDet(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_item):
        item = Quality.getMeeting(id_item)

        if not item:
            self.log.error(Logs.fileline() + ' : ' + 'MeetingDet ERROR not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        # Replace None by empty string
        for key, value in item.items():
            if item[key] is None:
                item[key] = ''

        if item['date_meeting']:
            item['date_meeting'] = datetime.strftime(item['date_meeting'], '%Y-%m-%d')

        self.log.info(Logs.fileline() + ' : MeetingDet id_item=' + str(id_item))
        return compose_ret(item, Constants.cst_content_type_json, 200)

    def post(self, id_item):
        args = request.get_json()

        if 'id_owner' not in args or 'id_item' not in args or 'date_meeting' not in args or \
           'type' not in args or 'promoter' not in args or 'report' not in args:
            self.log.error(Logs.fileline() + ' : MeetingDet ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # Update item
        if id_item > 0:
            ret = Quality.updateMeeting(id_data=id_item,
                                        id_owner=args['id_owner'],
                                        date_meeting=args['date_meeting'],
                                        type=args['type'],
                                        promoter=args['promoter'],
                                        report=args['report'])

            if ret is False:
                self.log.error(Logs.alert() + ' : MeetingDet ERROR update')
                return compose_ret('', Constants.cst_content_type_json, 500)

        # Insert new item
        else:
            ret = Quality.insertMeeting(id_owner=args['id_owner'],
                                        date_meeting=args['date_meeting'],
                                        type=args['type'],
                                        promoter=args['promoter'],
                                        report=args['report'])

            if ret <= 0:
                self.log.error(Logs.alert() + ' : MeetingDet ERROR  insert')
                return compose_ret('', Constants.cst_content_type_json, 500)

            id_item = ret

        self.log.info(Logs.fileline() + ' : TRACE MeetingDet id_item=' + str(id_item))
        return compose_ret(id_item, Constants.cst_content_type_json)

    def delete(self, id_item):
        ret = Quality.deleteMeeting(id_item)

        if not ret:
            self.log.error(Logs.fileline() + ' : TRACE MeetingDet delete ERROR')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE MeetingDet delete id_item=' + str(id_item))
        return compose_ret('', Constants.cst_content_type_json)


class MeetingExport(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        l_data = [['id_data', 'date_meeting', 'type', 'promoter', 'report', ]]
        dict_data = Quality.getMeetingList()

        if dict_data:
            for d in dict_data:
                data = []

                data.append(d['id_data'])
                data.append(d['date_meeting'])
                data.append(d['type'])
                data.append(d['promoter'])
                data.append(d['report'])

                l_data.append(data)

        # if no result to export
        if len(l_data) < 2:
            return compose_ret('', Constants.cst_content_type_json, 404)

        # write csv file
        try:
            import csv

            today = datetime.now().strftime("%Y%m%d")

            filename = 'meeting_' + str(today) + '.csv'

            with open('tmp/' + filename, mode='w') as file:
                writer = csv.writer(file, delimiter=';')
                for line in l_data:
                    writer.writerow(line)

        except Exception as err:
            self.log.error(Logs.fileline() + ' : post ExportMeeting failed, err=%s', err)
            return False

        self.log.info(Logs.fileline() + ' : TRACE ExportMeeting')
        return compose_ret('', Constants.cst_content_type_json)


class ProcedureList(Resource):
    log = logging.getLogger('log_services')

    def get(self):
        l_items = Quality.getProcedureList()

        if not l_items:
            self.log.error(Logs.fileline() + ' : TRACE ProcedureList not found')

        for item in l_items:
            # Replace None by empty string
            for key, value in item.items():
                if item[key] is None:
                    item[key] = ''

            if item['date_insert']:
                item['date_insert'] = datetime.strftime(item['date_insert'], '%Y-%m-%d')

            if item['date_apply']:
                item['date_apply'] = datetime.strftime(item['date_apply'], '%Y-%m-%d')

            if item['date_update']:
                item['date_update'] = datetime.strftime(item['date_update'], '%Y-%m-%d')

            # search last id_file for each manual
            l_files = File.getFileDocList("PROC", item['id_data'])

            if l_files and l_files[0]['id_data']:
                item['id_file'] = l_files[0]['id_data']
            else:
                item['id_file'] = 0

            if l_files and l_files[0]['name']:
                item['filename'] = l_files[0]['name']
            else:
                item['filename'] = ''

        self.log.info(Logs.fileline() + ' : TRACE ProcedureList')
        return compose_ret(l_items, Constants.cst_content_type_json)


class ProcedureDet(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_item):
        item = Quality.getProcedure(id_item)

        if not item:
            self.log.error(Logs.fileline() + ' : ' + 'ProcedureDet ERROR not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        # Replace None by empty string
        for key, value in item.items():
            if item[key] is None:
                item[key] = ''

        if item['date_insert']:
            item['date_insert'] = datetime.strftime(item['date_insert'], '%Y-%m-%d')

        if item['date_apply']:
            item['date_apply'] = datetime.strftime(item['date_apply'], '%Y-%m-%d')

        if item['date_update']:
            item['date_update'] = datetime.strftime(item['date_update'], '%Y-%m-%d')

        self.log.info(Logs.fileline() + ' : ProcedureDet id_item=' + str(id_item))
        return compose_ret(item, Constants.cst_content_type_json, 200)

    def post(self, id_item):
        args = request.get_json()

        if 'id_owner' not in args or 'id_item' not in args or 'reference' not in args or 'title' not in args or \
           'writer' not in args or 'auditor' not in args or 'approver' not in args or 'date_insert' not in args or \
           'date_apply' not in args or 'date_update' not in args or 'section' not in args:
            self.log.error(Logs.fileline() + ' : ProcedureDet ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # Update item
        if id_item > 0:
            ret = Quality.updateProcedure(id_data=id_item,
                                          id_owner=args['id_owner'],
                                          reference=args['reference'],
                                          title=args['title'],
                                          writer=args['writer'],
                                          auditor=args['auditor'],
                                          approver=args['approver'],
                                          date_insert=args['date_insert'],
                                          date_apply=args['date_apply'],
                                          date_update=args['date_update'],
                                          section=args['section'])

            if ret is False:
                self.log.error(Logs.alert() + ' : ProcedureDet ERROR update')
                return compose_ret('', Constants.cst_content_type_json, 500)

        # Insert new item
        else:
            ret = Quality.insertProcedure(id_owner=args['id_owner'],
                                          reference=args['reference'],
                                          title=args['title'],
                                          writer=args['writer'],
                                          auditor=args['auditor'],
                                          approver=args['approver'],
                                          date_insert=args['date_insert'],
                                          date_apply=args['date_apply'],
                                          date_update=args['date_update'],
                                          section=args['section'])

            if ret <= 0:
                self.log.error(Logs.alert() + ' : ProcedureDet ERROR  insert')
                return compose_ret('', Constants.cst_content_type_json, 500)

            id_item = ret

        self.log.info(Logs.fileline() + ' : TRACE ProcedureDet id_item=' + str(id_item))
        return compose_ret(id_item, Constants.cst_content_type_json)

    def delete(self, id_item):
        ret = Quality.deleteProcedure(id_item)

        if not ret:
            self.log.error(Logs.fileline() + ' : TRACE ProcedureDet delete ERROR')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE ProcedureDet delete id_item=' + str(id_item))
        return compose_ret('', Constants.cst_content_type_json)


class ProcedureExport(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        l_data = [['id_data', 'title', 'reference', 'writer', 'auditor', 'approver', 'date_insert',
                   'date_apply', 'date_update', 'section', ]]
        dict_data = Quality.getProcedureList()

        if dict_data:
            for d in dict_data:
                data = []

                data.append(d['id_data'])
                data.append(d['title'])
                data.append(d['reference'])
                data.append(d['writer'])
                data.append(d['auditor'])
                data.append(d['approver'])
                data.append(d['date_insert'])
                data.append(d['date_apply'])
                data.append(d['date_update'])
                data.append(d['section'])

                l_data.append(data)

        # if no result to export
        if len(l_data) < 2:
            return compose_ret('', Constants.cst_content_type_json, 404)

        # write csv file
        try:
            import csv

            today = datetime.now().strftime("%Y%m%d")

            filename = 'procedure_' + str(today) + '.csv'

            with open('tmp/' + filename, mode='w') as file:
                writer = csv.writer(file, delimiter=';')
                for line in l_data:
                    writer.writerow(line)

        except Exception as err:
            self.log.error(Logs.fileline() + ' : post ExportProcedure failed, err=%s', err)
            return False

        self.log.info(Logs.fileline() + ' : TRACE ExportProcedure')
        return compose_ret('', Constants.cst_content_type_json)


class ProcedureSearch(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        l_items = Quality.getProcedureSearch(args['term'])

        if not l_items:
            self.log.error(Logs.fileline() + ' : TRACE ProcedureSearch not found')

        self.log.info(Logs.fileline() + ' : TRACE ProcedureSearch')
        return compose_ret(l_items, Constants.cst_content_type_json)


class StaffExport(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        l_data = [['id_data', 'lastname', 'firstname', 'initial', 'birth', 'address',
                   'phone', 'email', 'arrived', 'position', 'section', 'last_eval', 'username', ]]
        dict_data = Quality.getStaffList()

        if dict_data:
            for d in dict_data:
                data = []

                data.append(d['id_data'])
                data.append(d['lastname'])
                data.append(d['firstname'])
                data.append(d['initial'])
                data.append(d['birth'])
                data.append(d['address'])
                data.append(d['phone'])
                data.append(d['email'])
                data.append(d['arrived'])
                data.append(d['position'])
                data.append(d['section'])
                data.append(d['last_eval'])
                data.append(d['username'])

                l_data.append(data)

        # if no result to export
        if len(l_data) < 2:
            return compose_ret('', Constants.cst_content_type_json, 404)

        # write csv file
        try:
            import csv

            today = datetime.now().strftime("%Y%m%d")

            filename = 'staff_' + str(today) + '.csv'

            with open('tmp/' + filename, mode='w') as file:
                writer = csv.writer(file, delimiter=';')
                for line in l_data:
                    writer.writerow(line)

        except Exception as err:
            self.log.error(Logs.fileline() + ' : post ExportStaff failed, err=%s', err)
            return False

        self.log.info(Logs.fileline() + ' : TRACE ExportStaff')
        return compose_ret('', Constants.cst_content_type_json)


class StockList(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        if not args:
            args = {}

        l_stocks = Quality.getStockList(args)

        self.log.error(Logs.fileline() + ' : DEBUG l_stocks=' + str(l_stocks))

        if not l_stocks:
            self.log.error(Logs.fileline() + ' : TRACE StockList not found')

        for stock in l_stocks:
            # Replace None by empty string
            for key, value in stock.items():
                if stock[key] is None:
                    stock[key] = ''

            if stock['pru_nb_pack']:
                stock['pru_nb_pack'] = float(stock['pru_nb_pack'])
            else:
                stock['pru_nb_pack'] = 0

            if stock['prs_nb_pack']:
                stock['prs_nb_pack'] = float(stock['prs_nb_pack']) - float(stock['pru_nb_pack'])
            else:
                stock['prs_nb_pack'] = 0

            stock['nb_total'] = float(stock['prs_nb_pack'] * stock['prd_nb_by_pack'])

            if stock['receipt_date']:
                stock['receipt_date'] = datetime.strftime(stock['receipt_date'], '%Y-%m-%d')

            if stock['expir_date']:
                stock['expir_date'] = datetime.strftime(stock['expir_date'], '%Y-%m-%d')

        self.log.info(Logs.fileline() + ' : TRACE StockList')
        return compose_ret(l_stocks, Constants.cst_content_type_json)


class StockProductSearch(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        l_items = Quality.getStockProductSearch(args['term'])

        if not l_items:
            self.log.error(Logs.fileline() + ' : TRACE StockProductSearch not found')

        self.log.info(Logs.fileline() + ' : TRACE StockProductSearch')
        return compose_ret(l_items, Constants.cst_content_type_json)


class StockProductDet(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_item):
        stock = Quality.getStockProduct(id_item)

        if not stock:
            self.log.error(Logs.fileline() + ' : ' + 'StockProductDet ERROR not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        # Replace None by empty string
        for key, value in stock.items():
            if stock[key] is None:
                stock[key] = ''

        self.log.info(Logs.fileline() + ' : StockProductDet id_item=' + str(id_item))
        return compose_ret(stock, Constants.cst_content_type_json, 200)

    def post(self, id_item):
        args = request.get_json()

        if 'prd_name' not in args or 'prd_type' not in args or 'prd_nb_by_pack' not in args or \
           'prd_supplier' not in args or 'prd_ref_supplier' not in args or 'prd_conserv' not in args:
            self.log.error(Logs.fileline() + ' : StockProductDet ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # Update stock product
        if id_item > 0:
            ret = Quality.updateStockProduct(prd_ser=id_item,
                                             prd_name=args['prd_name'],
                                             prd_type=args['prd_type'],
                                             prd_nb_by_pack=args['prd_nb_by_pack'],
                                             prd_supplier=args['prd_supplier'],
                                             prd_ref_supplier=args['prd_ref_supplier'],
                                             prd_conserv=args['prd_conserv'])

            if ret is False:
                self.log.error(Logs.alert() + ' : StockProductDet ERROR update')
                return compose_ret('', Constants.cst_content_type_json, 500)

        # Insert new stock product
        else:
            ret = Quality.insertStockProduct(prd_name=args['prd_name'],
                                             prd_type=args['prd_type'],
                                             prd_nb_by_pack=args['prd_nb_by_pack'],
                                             prd_supplier=args['prd_supplier'],
                                             prd_ref_supplier=args['prd_ref_supplier'],
                                             prd_conserv=args['prd_conserv'])

            if ret <= 0:
                self.log.error(Logs.alert() + ' : StockProductDet ERROR  insert')
                return compose_ret('', Constants.cst_content_type_json, 500)

            id_item = ret

        self.log.info(Logs.fileline() + ' : TRACE StockProductDet id_item=' + str(id_item))
        return compose_ret('', Constants.cst_content_type_json)


class StockSupplyDet(Resource):
    log = logging.getLogger('log_services')

    def post(self, id_item):
        args = request.get_json()

        if 'prs_prd' not in args or 'prs_nb_pack' not in args or 'prs_status' not in args or \
           'prs_receipt_date' not in args or 'prs_expir_date' not in args or 'prs_rack' not in args or \
           'prs_batch_num' not in args or 'prs_buy_price' not in args or 'prs_sell_price' not in args:
            self.log.error(Logs.fileline() + ' : StockSupplyDet ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # Update stock product
        if id_item > 0:
            ret = Quality.updateStockProduct(prs_ser=id_item,
                                             prs_prd=args['prs_prd'],
                                             prs_nb_pack=args['prs_nb_pack'],
                                             prs_status=args['prs_status'],
                                             prs_receipt_date=args['prs_receipt_date'],
                                             prs_expir_date=args['prs_expir_date'],
                                             prs_rack=args['prs_rack'],
                                             prs_batch_num=args['prs_batch_num'],
                                             prs_buy_price=args['prs_buy_price'],
                                             prs_sell_price=args['prs_sell_price'])

            if ret is False:
                self.log.error(Logs.alert() + ' : StockSupplyDet ERROR update')
                return compose_ret('', Constants.cst_content_type_json, 500)

        # Insert new supply product
        else:
            ret = Quality.insertStockSupply(prs_prd=args['prs_prd'],
                                            prs_nb_pack=args['prs_nb_pack'],
                                            prs_status=args['prs_status'],
                                            prs_receipt_date=args['prs_receipt_date'],
                                            prs_expir_date=args['prs_expir_date'],
                                            prs_rack=args['prs_rack'],
                                            prs_batch_num=args['prs_batch_num'],
                                            prs_buy_price=args['prs_buy_price'],
                                            prs_sell_price=args['prs_sell_price'])

            if ret <= 0:
                self.log.error(Logs.alert() + ' : StockSupplyDet ERROR insert')
                return compose_ret('', Constants.cst_content_type_json, 500)

            id_item = ret

        self.log.info(Logs.fileline() + ' : TRACE StockSupplyDet id_item=' + str(id_item))
        return compose_ret('', Constants.cst_content_type_json)


class StockUse(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        if 'pru_user' not in args or 'pru_prs' not in args or 'pru_nb_pack' not in args:
            self.log.error(Logs.fileline() + ' : StockUse ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        ret = Quality.insertStockUse(pru_user=args['pru_user'],
                                     pru_prs=args['pru_prs'],
                                     pru_nb_pack=args['pru_nb_pack'])

        if ret <= 0:
            self.log.error(Logs.alert() + ' : StockUse ERROR insert')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE StockUse pru_prs=' + str(args['pru_prs']))
        return compose_ret('', Constants.cst_content_type_json)


class StockExport(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        if not args:
            args = {}

        args['limit'] = 50000  # for overpassed default limit

        l_data = [['prs_ser', 'name', 'nb_pack', 'nb_by_pack', 'nb_total', 'type', 'receipt_date', 'rack', 'conserv',
                   'expir_date', 'batch_num', 'status', 'supplier', 'buy_price', 'sell_price', ]]
        dict_data = Quality.getStockList(args)

        if dict_data:
            for d in dict_data:
                data = []

                if d['pru_nb_pack']:
                    d['pru_nb_pack'] = float(d['pru_nb_pack'])
                else:
                    d['pru_nb_pack'] = 0

                if d['prs_nb_pack']:
                    d['prs_nb_pack'] = float(d['prs_nb_pack']) - float(d['pru_nb_pack'])
                else:
                    d['prs_nb_pack'] = 0

                d['nb_total'] = float(d['prs_nb_pack'] * d['prd_nb_by_pack'])

                if d['receipt_date']:
                    d['receipt_date'] = datetime.strftime(d['receipt_date'], '%Y-%m-%d')

                if d['expir_date']:
                    d['expir_date'] = datetime.strftime(d['expir_date'], '%Y-%m-%d')

                data.append(d['prs_ser'])
                data.append(d['prd_name'])
                data.append(d['prs_nb_pack'])
                data.append(d['prd_nb_by_pack'])
                data.append(d['nb_total'])
                data.append(d['type'])
                data.append(d['receipt_date'])
                data.append(d['prs_rack'])
                data.append(d['conserv'])
                data.append(d['expir_date'])
                data.append(d['prs_batch_num'])
                data.append(d['status'])
                data.append(d['supplier'])
                data.append(d['prs_buy_price'])
                data.append(d['prs_sell_price'])

                l_data.append(data)

        # if no result to export
        if len(l_data) < 2:
            return compose_ret('', Constants.cst_content_type_json, 404)

        # write csv file
        try:
            import csv

            today = datetime.now().strftime("%Y%m%d")

            filename = 'stock_' + str(today) + '.csv'

            with open('tmp/' + filename, mode='w') as file:
                writer = csv.writer(file, delimiter=';')
                for line in l_data:
                    writer.writerow(line)

        except Exception as err:
            self.log.error(Logs.fileline() + ' : post StockExport failed, err=%s', err)
            return False

        self.log.info(Logs.fileline() + ' : TRACE StockExport')
        return compose_ret('', Constants.cst_content_type_json)


class SupplierList(Resource):
    log = logging.getLogger('log_services')

    def get(self):
        l_items = Quality.getSupplierList()

        if not l_items:
            self.log.error(Logs.fileline() + ' : TRACE SupplierList not found')

        for item in l_items:
            # Replace None by empty string
            for key, value in item.items():
                if item[key] is None:
                    item[key] = ''

        self.log.info(Logs.fileline() + ' : TRACE SupplierList')
        return compose_ret(l_items, Constants.cst_content_type_json)


class SupplierSearch(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        l_items = Quality.getSupplierSearch(args['term'])

        if not l_items:
            self.log.error(Logs.fileline() + ' : TRACE SupplierSearch not found')

        self.log.info(Logs.fileline() + ' : TRACE SupplierSearch')
        return compose_ret(l_items, Constants.cst_content_type_json)


class SupplierDet(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_item):
        item = Quality.getSupplier(id_item)

        if not item:
            self.log.error(Logs.fileline() + ' : ' + 'SupplierDet ERROR not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        # Replace None by empty string
        for key, value in item.items():
            if item[key] is None:
                item[key] = ''

        self.log.info(Logs.fileline() + ' : SupplierDet id_item=' + str(id_item))
        return compose_ret(item, Constants.cst_content_type_json, 200)

    def post(self, id_item):
        args = request.get_json()

        if 'id_owner' not in args or 'id_item' not in args or 'supplier' not in args or 'funct' not in args or \
           'lastname' not in args or 'firstname' not in args or 'address' not in args or 'comment' not in args or \
           'phone' not in args or 'mobile' not in args or 'fax' not in args or 'email' not in args:
            self.log.error(Logs.fileline() + ' : SupplierDet ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # Update item
        if id_item > 0:
            ret = Quality.updateSupplier(id_data=id_item,
                                         id_owner=args['id_owner'],
                                         supplier=args['supplier'],
                                         lastname=args['lastname'],
                                         firstname=args['firstname'],
                                         address=args['address'],
                                         phone=args['phone'],
                                         email=args['email'],
                                         funct=args['funct'],
                                         comment=args['comment'],
                                         mobile=args['mobile'],
                                         fax=args['fax'])

            if ret is False:
                self.log.error(Logs.alert() + ' : SupplierDet ERROR update')
                return compose_ret('', Constants.cst_content_type_json, 500)

        # Insert new item
        else:
            ret = Quality.insertSupplier(id_owner=args['id_owner'],
                                         supplier=args['supplier'],
                                         lastname=args['lastname'],
                                         firstname=args['firstname'],
                                         address=args['address'],
                                         phone=args['phone'],
                                         email=args['email'],
                                         funct=args['funct'],
                                         comment=args['comment'],
                                         mobile=args['mobile'],
                                         fax=args['fax'])

            if ret <= 0:
                self.log.error(Logs.alert() + ' : SupplierDet ERROR  insert')
                return compose_ret('', Constants.cst_content_type_json, 500)

            id_item = ret

        self.log.info(Logs.fileline() + ' : TRACE SupplierDet id_item=' + str(id_item))
        return compose_ret('', Constants.cst_content_type_json)

    def delete(self, id_item):
        ret = Quality.deleteSupplier(id_item)

        if not ret:
            self.log.error(Logs.fileline() + ' : TRACE SupplierDet delete ERROR')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE SupplierDet delete id_item=' + str(id_item))
        return compose_ret('', Constants.cst_content_type_json)


class SupplierExport(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        l_data = [['id_data', 'id_owner', 'supplier', 'lastname', 'firstname', 'funct', 'address',
                   'phone', 'mobile', 'fax', 'email', 'comment',
                   'date_create', 'date_update', 'id_user_upd', ]]
        dict_data = Quality.getSupplierList()

        if dict_data:
            for d in dict_data:
                data = []

                data.append(d['id_data'])
                data.append(d['id_owner'])
                data.append(d['supplier'])
                data.append(d['lastname'])
                data.append(d['firstname'])
                data.append(d['funct'])
                data.append(d['address'])
                data.append(d['phone'])
                data.append(d['mobile'])
                data.append(d['fax'])
                data.append(d['email'])
                data.append(d['comment'])
                data.append(d['date_create'])
                data.append(d['date_update'])
                data.append(d['id_user_upd'])

                l_data.append(data)

        # if no result to export
        if len(l_data) < 2:
            return compose_ret('', Constants.cst_content_type_json, 404)

        # write csv file
        try:
            import csv

            today = datetime.now().strftime("%Y%m%d")

            filename = 'supplier_' + str(today) + '.csv'

            with open('tmp/' + filename, mode='w') as file:
                writer = csv.writer(file, delimiter=';')
                for line in l_data:
                    writer.writerow(line)

        except Exception as err:
            self.log.error(Logs.fileline() + ' : post ExportSupplier failed, err=%s', err)
            return False

        self.log.info(Logs.fileline() + ' : TRACE ExportSupplier')
        return compose_ret('', Constants.cst_content_type_json)
