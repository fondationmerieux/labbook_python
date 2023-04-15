# -*- coding:utf-8 -*-
import logging
import gettext

from datetime import datetime
from flask import request
from flask_restful import Resource

from app.models.General import compose_ret
from app.models.Constants import Constants
from app.models.Logs import Logs
from app.models.Quality import Quality
from app.models.File import File
from app.models.Setting import Setting
from app.models.Various import Various


class QualityLastMeeting(Resource):
    log = logging.getLogger('log_services')

    def get(self):
        meeting = Quality.getLastMeeting()

        if not meeting:
            self.log.error(Logs.fileline() + ' : ' + 'QualityLastMeeting ERROR not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        # Replace None by empty string
        for key, value in list(meeting.items()):
            if meeting[key] is None:
                meeting[key] = ''

        if meeting['sys_creation_date']:
            meeting['sys_creation_date'] = datetime.strftime(meeting['sys_creation_date'], '%Y-%m-%d')

        if meeting['sys_last_mod_date']:
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

        if 'date_beg' not in args or 'date_end' not in args:
            self.log.error(Logs.fileline() + ' : ConformityList ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        l_items = Quality.getConformityList(args['date_beg'], args['date_end'])

        if not l_items:
            self.log.error(Logs.fileline() + ' : TRACE ConformityList not found')

        for item in l_items:
            # Replace None by empty string
            for key, value in list(item.items()):
                if item[key] is None:
                    item[key] = ''

            if item['date_create']:
                item['date_create'] = datetime.strftime(item['date_create'], '%Y-%m-%d')

            if item['date_correction']:
                item['date_correction'] = datetime.strftime(item['date_correction'], '%Y-%m-%d')

            if item['close_date']:
                item['close_date'] = datetime.strftime(item['close_date'], '%Y-%m-%d')

        self.log.info(Logs.fileline() + ' : TRACE ConformityList')
        return compose_ret(l_items, Constants.cst_content_type_json)


class ConformityDet(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_item):
        item = Quality.getNonConformity(id_item)

        if not item:
            self.log.error(Logs.fileline() + ' : ' + 'ConformityDet ERROR not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        # Replace None by empty string
        for key, value in list(item.items()):
            if item[key] is None:
                item[key] = ''

        if item['date_create']:
            item['date_create'] = datetime.strftime(item['date_create'], '%Y-%m-%d')

        if item['flwd_when']:
            item['flwd_when'] = datetime.strftime(item['flwd_when'], '%Y-%m-%d')

        if item['flwd_action_date']:
            item['flwd_action_date'] = datetime.strftime(item['flwd_action_date'], '%Y-%m-%d')

        if item['close_date']:
            item['close_date'] = datetime.strftime(item['close_date'], '%Y-%m-%d')

        self.log.info(Logs.fileline() + ' : ConformityDet id_item=' + str(id_item))
        return compose_ret(item, Constants.cst_content_type_json, 200)

    def post(self, id_item):
        args = request.get_json()

        if 'id_owner' not in args or 'id_item' not in args or 'name' not in args or 'reporter' not in args or \
           'report_date' not in args or 'cat_preana' not in args or 'sub_preana_cat1' not in args or \
           'sub_preana_cat2' not in args or 'sub_preana_cat3' not in args or 'sub_preana_cat4' not in args or \
           'sub1_sub_preana_cat4' not in args or 'sub2_sub_preana_cat4' not in args or \
           'sub3_sub_preana_cat4' not in args or 'sub_preana_cat5' not in args or 'sub_preana_cat6' not in args or \
           'sub_preana_cat7' not in args or 'sub_preana_cat8' not in args or 'sub_preana_cat9' not in args or \
           'sub_preana_cat10' not in args or 'cat_analy' not in args or 'sub_analy_cat1' not in args or \
           'sub_analy_cat2' not in args or 'sub_analy_cat3' not in args or 'sub_analy_cat4' not in args or \
           'sub_analy_cat5' not in args or 'sub_analy_cat6' not in args or 'sub_analy_cat7' not in args or \
           'sub_analy_cat8' not in args or 'sub_analy_cat9' not in args or 'sub_analy_cat10' not in args or \
           'sub_analy_cat11' not in args or 'cat_postana' not in args or 'sub_postana_cat1' not in args or \
           'sub_postana_cat2' not in args or 'sub_postana_cat3' not in args or 'sub_postana_cat4' not in args or \
           'sub_postana_cat5' not in args or 'sub_postana_cat6' not in args or 'sub_postana_cat7' not in args or \
           'sub_postana_cat8' not in args or 'sub_postana_cat9' not in args or 'sub_postana_cat10' not in args or \
           'cat_res' not in args or 'sub_res_cat1' not in args or 'sub_res_cat2' not in args or \
           'sub_res_cat3' not in args or 'sub_res_cat4' not in args or 'sub_res_cat5' not in args or \
           'sub_res_cat6' not in args or 'sub_res_cat7' not in args or 'cat_hr' not in args or \
           'sub_hr_cat1' not in args or 'sub_hr_cat2' not in args or 'sub_hr_cat3' not in args or \
           'sub_hr_cat4' not in args or 'sub_hr_cat5' not in args or 'cat_eqp' not in args or \
           'sub_eqp_cat1' not in args or 'sub_eqp_cat2' not in args or 'sub_eqp_cat3' not in args or \
           'sub_eqp_cat4' not in args or 'sub_eqp_cat5' not in args or 'sub_eqp_cat6' not in args or \
           'equipment' not in args or 'cat_consu' not in args or 'sub_consu_cat1' not in args or \
           'sub_consu_cat2' not in args or 'sub_consu_cat3' not in args or 'sub_consu_cat4' not in args or \
           'sub_consu_cat5' not in args or 'sub_consu_cat6' not in args or 'supplier' not in args or \
           'cat_local' not in args or 'sub_local_cat1' not in args or 'sub_local_cat2' not in args or \
           'sub_local_cat3' not in args or 'sub_local_cat4' not in args or 'sub_local_cat5' not in args or \
           'sub_local_cat6' not in args or 'cat_si' not in args or 'sub_si_cat1' not in args or \
           'sub_si_cat2' not in args or 'sub_si_cat3' not in args or 'sub_si_cat4' not in args or \
           'sub_si_cat5' not in args or 'sub_si_cat6' not in args or 'cat_contract' not in args or \
           'sub_contract_cat1' not in args or 'sub_contract_cat2' not in args or 'sub_contract_cat3' not in args or \
           'sub_contract_cat4' not in args or 'sub_contract_cat5' not in args or 'cat_client' not in args or \
           'cat_other' not in args or 'about_pat_rec' not in args or 'pat_rec_num' not in args or \
           'description' not in args or 'impact_pat' not in args or 'impact_user' not in args or \
           'followed' not in args or 'flwd_what' not in args or 'flwd_when' not in args or 'impl_action' not in args or \
           'flwd_descr_action' not in args or 'flwd_action_date' not in args or 'incharge' not in args or \
           'close_comment' not in args or 'validate' not in args or 'close_date' not in args:
            self.log.error(Logs.fileline() + ' : ConformityDet ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # Update item
        if id_item > 0:
            self.log.info(Logs.fileline() + ' : TRACE update conformityDet')

            ret = Quality.updateNonConformity(id_data=id_item,
                                              id_owner=args['id_owner'],
                                              name=args['name'],
                                              reporter=args['reporter'],
                                              report_date=args['report_date'],
                                              cat_preana=args['cat_preana'],
                                              sub_preana_cat1=args['sub_preana_cat1'],
                                              sub_preana_cat2=args['sub_preana_cat2'],
                                              sub_preana_cat3=args['sub_preana_cat3'],
                                              sub_preana_cat4=args['sub_preana_cat4'],
                                              sub1_sub_preana_cat4=args['sub1_sub_preana_cat4'],
                                              sub2_sub_preana_cat4=args['sub2_sub_preana_cat4'],
                                              sub3_sub_preana_cat4=args['sub3_sub_preana_cat4'],
                                              sub_preana_cat5=args['sub_preana_cat5'],
                                              sub_preana_cat6=args['sub_preana_cat6'],
                                              sub_preana_cat7=args['sub_preana_cat7'],
                                              sub_preana_cat8=args['sub_preana_cat8'],
                                              sub_preana_cat9=args['sub_preana_cat9'],
                                              sub_preana_cat10=args['sub_preana_cat10'],
                                              cat_analy=args['cat_analy'],
                                              sub_analy_cat1=args['sub_analy_cat1'],
                                              sub_analy_cat2=args['sub_analy_cat2'],
                                              sub_analy_cat3=args['sub_analy_cat3'],
                                              sub_analy_cat4=args['sub_analy_cat4'],
                                              sub_analy_cat5=args['sub_analy_cat5'],
                                              sub_analy_cat6=args['sub_analy_cat6'],
                                              sub_analy_cat7=args['sub_analy_cat7'],
                                              sub_analy_cat8=args['sub_analy_cat8'],
                                              sub_analy_cat9=args['sub_analy_cat9'],
                                              sub_analy_cat10=args['sub_analy_cat10'],
                                              sub_analy_cat11=args['sub_analy_cat11'],
                                              cat_postana=args['cat_postana'],
                                              sub_postana_cat1=args['sub_postana_cat1'],
                                              sub_postana_cat2=args['sub_postana_cat2'],
                                              sub_postana_cat3=args['sub_postana_cat3'],
                                              sub_postana_cat4=args['sub_postana_cat4'],
                                              sub_postana_cat5=args['sub_postana_cat5'],
                                              sub_postana_cat6=args['sub_postana_cat6'],
                                              sub_postana_cat7=args['sub_postana_cat7'],
                                              sub_postana_cat8=args['sub_postana_cat8'],
                                              sub_postana_cat9=args['sub_postana_cat9'],
                                              sub_postana_cat10=args['sub_postana_cat10'],
                                              cat_res=args['cat_res'],
                                              sub_res_cat1=args['sub_res_cat1'],
                                              sub_res_cat2=args['sub_res_cat2'],
                                              sub_res_cat3=args['sub_res_cat3'],
                                              sub_res_cat4=args['sub_res_cat4'],
                                              sub_res_cat5=args['sub_res_cat5'],
                                              sub_res_cat6=args['sub_res_cat6'],
                                              sub_res_cat7=args['sub_res_cat7'],
                                              cat_hr=args['cat_hr'],
                                              sub_hr_cat1=args['sub_hr_cat1'],
                                              sub_hr_cat2=args['sub_hr_cat2'],
                                              sub_hr_cat3=args['sub_hr_cat3'],
                                              sub_hr_cat4=args['sub_hr_cat4'],
                                              sub_hr_cat5=args['sub_hr_cat5'],
                                              cat_eqp=args['cat_eqp'],
                                              sub_eqp_cat1=args['sub_eqp_cat1'],
                                              sub_eqp_cat2=args['sub_eqp_cat2'],
                                              sub_eqp_cat3=args['sub_eqp_cat3'],
                                              sub_eqp_cat4=args['sub_eqp_cat4'],
                                              sub_eqp_cat5=args['sub_eqp_cat5'],
                                              sub_eqp_cat6=args['sub_eqp_cat6'],
                                              equipment=args['equipment'],
                                              cat_consu=args['cat_consu'],
                                              sub_consu_cat1=args['sub_consu_cat1'],
                                              sub_consu_cat2=args['sub_consu_cat2'],
                                              sub_consu_cat3=args['sub_consu_cat3'],
                                              sub_consu_cat4=args['sub_consu_cat4'],
                                              sub_consu_cat5=args['sub_consu_cat5'],
                                              sub_consu_cat6=args['sub_consu_cat6'],
                                              supplier=args['supplier'],
                                              cat_local=args['cat_local'],
                                              sub_local_cat1=args['sub_local_cat1'],
                                              sub_local_cat2=args['sub_local_cat2'],
                                              sub_local_cat3=args['sub_local_cat3'],
                                              sub_local_cat4=args['sub_local_cat4'],
                                              sub_local_cat5=args['sub_local_cat5'],
                                              sub_local_cat6=args['sub_local_cat6'],
                                              cat_si=args['cat_si'],
                                              sub_si_cat1=args['sub_si_cat1'],
                                              sub_si_cat2=args['sub_si_cat2'],
                                              sub_si_cat3=args['sub_si_cat3'],
                                              sub_si_cat4=args['sub_si_cat4'],
                                              sub_si_cat5=args['sub_si_cat5'],
                                              sub_si_cat6=args['sub_si_cat6'],
                                              cat_contract=args['cat_contract'],
                                              sub_contract_cat1=args['sub_contract_cat1'],
                                              sub_contract_cat2=args['sub_contract_cat2'],
                                              sub_contract_cat3=args['sub_contract_cat3'],
                                              sub_contract_cat4=args['sub_contract_cat4'],
                                              sub_contract_cat5=args['sub_contract_cat5'],
                                              cat_client=args['cat_client'],
                                              cat_other=args['cat_other'],
                                              about_pat_rec=args['about_pat_rec'],
                                              pat_rec_num=args['pat_rec_num'],
                                              description=args['description'],
                                              impact_pat=args['impact_pat'],
                                              impact_user=args['impact_user'],
                                              followed=args['followed'],
                                              flwd_what=args['flwd_what'],
                                              flwd_when=args['flwd_when'],
                                              impl_action=args['impl_action'],
                                              flwd_descr_action=args['flwd_descr_action'],
                                              flwd_action_date=args['flwd_action_date'],
                                              incharge=args['incharge'],
                                              close_comment=args['close_comment'],
                                              validate=args['validate'],
                                              close_date=args['close_date'])

            if ret is False:
                self.log.error(Logs.alert() + ' : ConformityDet ERROR update')
                return compose_ret('', Constants.cst_content_type_json, 500)

        # Insert new item
        else:
            self.log.info(Logs.fileline() + ' : TRACE insert NonConformity')
            ret = Quality.insertNonConformity(id_owner=args['id_owner'],
                                              name=args['name'],
                                              reporter=args['reporter'],
                                              report_date=args['report_date'],
                                              cat_preana=args['cat_preana'],
                                              sub_preana_cat1=args['sub_preana_cat1'],
                                              sub_preana_cat2=args['sub_preana_cat2'],
                                              sub_preana_cat3=args['sub_preana_cat3'],
                                              sub_preana_cat4=args['sub_preana_cat4'],
                                              sub1_sub_preana_cat4=args['sub1_sub_preana_cat4'],
                                              sub2_sub_preana_cat4=args['sub2_sub_preana_cat4'],
                                              sub3_sub_preana_cat4=args['sub3_sub_preana_cat4'],
                                              sub_preana_cat5=args['sub_preana_cat5'],
                                              sub_preana_cat6=args['sub_preana_cat6'],
                                              sub_preana_cat7=args['sub_preana_cat7'],
                                              sub_preana_cat8=args['sub_preana_cat8'],
                                              sub_preana_cat9=args['sub_preana_cat9'],
                                              sub_preana_cat10=args['sub_preana_cat10'],
                                              cat_analy=args['cat_analy'],
                                              sub_analy_cat1=args['sub_analy_cat1'],
                                              sub_analy_cat2=args['sub_analy_cat2'],
                                              sub_analy_cat3=args['sub_analy_cat3'],
                                              sub_analy_cat4=args['sub_analy_cat4'],
                                              sub_analy_cat5=args['sub_analy_cat5'],
                                              sub_analy_cat6=args['sub_analy_cat6'],
                                              sub_analy_cat7=args['sub_analy_cat7'],
                                              sub_analy_cat8=args['sub_analy_cat8'],
                                              sub_analy_cat9=args['sub_analy_cat9'],
                                              sub_analy_cat10=args['sub_analy_cat10'],
                                              sub_analy_cat11=args['sub_analy_cat11'],
                                              cat_postana=args['cat_postana'],
                                              sub_postana_cat1=args['sub_postana_cat1'],
                                              sub_postana_cat2=args['sub_postana_cat2'],
                                              sub_postana_cat3=args['sub_postana_cat3'],
                                              sub_postana_cat4=args['sub_postana_cat4'],
                                              sub_postana_cat5=args['sub_postana_cat5'],
                                              sub_postana_cat6=args['sub_postana_cat6'],
                                              sub_postana_cat7=args['sub_postana_cat7'],
                                              sub_postana_cat8=args['sub_postana_cat8'],
                                              sub_postana_cat9=args['sub_postana_cat9'],
                                              sub_postana_cat10=args['sub_postana_cat10'],
                                              cat_res=args['cat_res'],
                                              sub_res_cat1=args['sub_res_cat1'],
                                              sub_res_cat2=args['sub_res_cat2'],
                                              sub_res_cat3=args['sub_res_cat3'],
                                              sub_res_cat4=args['sub_res_cat4'],
                                              sub_res_cat5=args['sub_res_cat5'],
                                              sub_res_cat6=args['sub_res_cat6'],
                                              sub_res_cat7=args['sub_res_cat7'],
                                              cat_hr=args['cat_hr'],
                                              sub_hr_cat1=args['sub_hr_cat1'],
                                              sub_hr_cat2=args['sub_hr_cat2'],
                                              sub_hr_cat3=args['sub_hr_cat3'],
                                              sub_hr_cat4=args['sub_hr_cat4'],
                                              sub_hr_cat5=args['sub_hr_cat5'],
                                              cat_eqp=args['cat_eqp'],
                                              sub_eqp_cat1=args['sub_eqp_cat1'],
                                              sub_eqp_cat2=args['sub_eqp_cat2'],
                                              sub_eqp_cat3=args['sub_eqp_cat3'],
                                              sub_eqp_cat4=args['sub_eqp_cat4'],
                                              sub_eqp_cat5=args['sub_eqp_cat5'],
                                              sub_eqp_cat6=args['sub_eqp_cat6'],
                                              equipment=args['equipment'],
                                              cat_consu=args['cat_consu'],
                                              sub_consu_cat1=args['sub_consu_cat1'],
                                              sub_consu_cat2=args['sub_consu_cat2'],
                                              sub_consu_cat3=args['sub_consu_cat3'],
                                              sub_consu_cat4=args['sub_consu_cat4'],
                                              sub_consu_cat5=args['sub_consu_cat5'],
                                              sub_consu_cat6=args['sub_consu_cat6'],
                                              supplier=args['supplier'],
                                              cat_local=args['cat_local'],
                                              sub_local_cat1=args['sub_local_cat1'],
                                              sub_local_cat2=args['sub_local_cat2'],
                                              sub_local_cat3=args['sub_local_cat3'],
                                              sub_local_cat4=args['sub_local_cat4'],
                                              sub_local_cat5=args['sub_local_cat5'],
                                              sub_local_cat6=args['sub_local_cat6'],
                                              cat_si=args['cat_si'],
                                              sub_si_cat1=args['sub_si_cat1'],
                                              sub_si_cat2=args['sub_si_cat2'],
                                              sub_si_cat3=args['sub_si_cat3'],
                                              sub_si_cat4=args['sub_si_cat4'],
                                              sub_si_cat5=args['sub_si_cat5'],
                                              sub_si_cat6=args['sub_si_cat6'],
                                              cat_contract=args['cat_contract'],
                                              sub_contract_cat1=args['sub_contract_cat1'],
                                              sub_contract_cat2=args['sub_contract_cat2'],
                                              sub_contract_cat3=args['sub_contract_cat3'],
                                              sub_contract_cat4=args['sub_contract_cat4'],
                                              sub_contract_cat5=args['sub_contract_cat5'],
                                              cat_client=args['cat_client'],
                                              cat_other=args['cat_other'],
                                              about_pat_rec=args['about_pat_rec'],
                                              pat_rec_num=args['pat_rec_num'],
                                              description=args['description'],
                                              impact_pat=args['impact_pat'],
                                              impact_user=args['impact_user'],
                                              followed=args['followed'],
                                              flwd_what=args['flwd_what'],
                                              flwd_when=args['flwd_when'],
                                              impl_action=args['impl_action'],
                                              flwd_descr_action=args['flwd_descr_action'],
                                              flwd_action_date=args['flwd_action_date'],
                                              incharge=args['incharge'],
                                              close_comment=args['close_comment'],
                                              validate=args['validate'],
                                              close_date=args['close_date'])

            if ret <= 0:
                self.log.error(Logs.alert() + ' : ConformityDet ERROR  insert')
                return compose_ret('', Constants.cst_content_type_json, 500)

            id_item = ret

        self.log.info(Logs.fileline() + ' : TRACE ConformityDet id_item=' + str(id_item))
        return compose_ret(id_item, Constants.cst_content_type_json)

    def delete(self, id_item):
        ret = Quality.deleteNonConformity(id_item)

        if not ret:
            self.log.error(Logs.fileline() + ' : TRACE ConformityDet delete ERROR')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE ConformityDet delete id_item=' + str(id_item))
        return compose_ret('', Constants.cst_content_type_json)


class ConformityExport(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        l_data = [['id_data', 'date_create', 'name', 'impact_patient', 'impact_user',
                   'correction', 'date_correction', 'close_date']]

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
                data.append(d['impact_patient'])
                data.append(d['impact_user'])
                data.append(d['correction'])

                if d['date_correction']:
                    data.append(d['date_correction'])
                else:
                    data.append('')

                if d['close_date']:
                    data.append(d['close_date'])
                else:
                    data.append('')

                l_data.append(data)

        # if no result to export
        if len(l_data) < 2:
            return compose_ret('', Constants.cst_content_type_json, 404)

        # write csv file
        try:
            import csv

            today = datetime.now().strftime("%Y%m%d")

            filename = 'nonconformity_' + str(today) + '.csv'

            with open('tmp/' + filename, mode='w', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=';')
                for line in l_data:
                    writer.writerow(line)

        except Exception as err:
            self.log.error(Logs.fileline() + ' : post ExportConformity failed, err=%s', err)
            return False

        self.log.info(Logs.fileline() + ' : TRACE ExportConformity')
        return compose_ret('', Constants.cst_content_type_json)


class ControlList(Resource):
    log = logging.getLogger('log_services')

    def get(self, type_ctrl):
        if type_ctrl != 'INT' and type_ctrl != 'EXT':
            self.log.error(Logs.fileline() + ' : ControlList ERROR wrong type')
            return compose_ret('', Constants.cst_content_type_json, 409)

        l_items = Quality.getControlList(type_ctrl)

        if not l_items:
            self.log.error(Logs.fileline() + ' : TRACE ControlList not found')

        for item in l_items:
            # Replace None by empty string
            for key, value in list(item.items()):
                if item[key] is None:
                    item[key] = ''

        self.log.info(Logs.fileline() + ' : TRACE ControlList type : ' + str(type_ctrl))
        return compose_ret(l_items, Constants.cst_content_type_json)


class ControlDet(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_item):
        item = Quality.getControlDet(id_item)

        if not item:
            self.log.error(Logs.fileline() + ' : ' + 'ControlDet ERROR not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        # Replace None by empty string
        for key, value in list(item.items()):
            if item[key] is None:
                item[key] = ''

        self.log.info(Logs.fileline() + ' : ControlDet id_item=' + str(id_item))
        return compose_ret(item, Constants.cst_content_type_json, 200)

    def post(self, id_item):
        args = request.get_json()

        if 'type_ctrl' not in args or 'type_val' not in args or 'name' not in args or 'id_eqp' not in args:
            self.log.error(Logs.fileline() + ' : ControlDet ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # Update item
        if id_item > 0:
            self.log.info(Logs.fileline() + ' : TRACE update controlDet')

            ret = Quality.updateControlDet(ctq_ser=id_item,
                                           ctq_type_ctrl=args['type_ctrl'],
                                           ctq_type_val=args['type_val'],
                                           ctq_name=args['name'],
                                           ctq_eqp=args['id_eqp'])

            if ret is False:
                self.log.error(Logs.alert() + ' : ControlDet ERROR update')
                return compose_ret('', Constants.cst_content_type_json, 500)

        # Insert new item
        else:
            self.log.info(Logs.fileline() + ' : TRACE insert ControlDet')
            ret = Quality.insertControlDet(ctq_type_ctrl=args['type_ctrl'],
                                           ctq_type_val=args['type_val'],
                                           ctq_name=args['name'],
                                           ctq_eqp=args['id_eqp'])

            if ret <= 0:
                self.log.error(Logs.alert() + ' : ControlDet ERROR  insert')
                return compose_ret('', Constants.cst_content_type_json, 500)

            id_item = ret

        self.log.info(Logs.fileline() + ' : TRACE ControlDet id_item=' + str(id_item))
        return compose_ret(id_item, Constants.cst_content_type_json)


class ControlIntExport(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        l_data = [['ctq_ser', 'ctq_name', 'ctq_type_ctrl', 'ctq_type_val', 'eqp_name', ]]
        dict_data = Quality.getControlList('INT')

        Various.useLangDB()

        if dict_data:
            for d in dict_data:
                data = []

                data.append(d['id_item'])
                data.append(d['ctq_name'])
                data.append(d['ctq_type_ctrl'])
                data.append(d['ctq_type_val'])
                data.append(d['eqp_name'])

                l_data.append(data)

        # if no result to export
        if len(l_data) < 2:
            return compose_ret('', Constants.cst_content_type_json, 404)

        # write csv file
        try:
            import csv

            today = datetime.now().strftime("%Y%m%d")

            filename = 'control_int_' + str(today) + '.csv'

            with open('tmp/' + filename, mode='w', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=';')
                for line in l_data:
                    writer.writerow(line)

        except Exception as err:
            self.log.error(Logs.fileline() + ' : post ControlIntExport failed, err=%s', err)
            return False

        self.log.info(Logs.fileline() + ' : TRACE ControlIntExport')
        return compose_ret('', Constants.cst_content_type_json)


class ControlIntResList(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_ctrl):
        l_items = Quality.getControlIntResList(id_ctrl)

        if not l_items:
            self.log.error(Logs.fileline() + ' : TRACE ControlIntResList not found')

        for item in l_items:
            # Replace None by empty string
            for key, value in list(item.items()):
                if item[key] is None:
                    item[key] = ''

            if item['cti_date']:
                item['cti_date'] = datetime.strftime(item['cti_date'], '%Y-%m-%d %H:%M')

        self.log.info(Logs.fileline() + ' : TRACE ControlIntResList id_ctrl : ' + str(id_ctrl))
        return compose_ret(l_items, Constants.cst_content_type_json)


class ControlIntRes(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_item):
        item = Quality.getControlIntRes(id_item)

        if not item:
            self.log.error(Logs.fileline() + ' : ' + 'ControlIntRes ERROR not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        # Replace None by empty string
        for key, value in list(item.items()):
            if item[key] is None:
                item[key] = ''

        if item['cti_date']:
            item['cti_date'] = datetime.strftime(item['cti_date'], '%Y-%m-%dT%H:%M')

        # if quantitative control we convert to float
        if item['cti_type'] == 'QN':
            if item['cti_target']:
                item['cti_target'] = float(item['cti_target'])
            else:
                item['cti_target'] = ''

            if item['cti_result']:
                item['cti_result'] = float(item['cti_result'])
            else:
                item['cti_result'] = ''

        self.log.info(Logs.fileline() + ' : ControlIntRes id_item=' + str(id_item))
        return compose_ret(item, Constants.cst_content_type_json, 200)

    def post(self, id_item):
        args = request.get_json()

        if 'cti_ctq' not in args or 'cti_date' not in args or 'cti_type' not in args or 'cti_target' not in args or \
           'cti_result' not in args or 'cti_comment' not in args:
            self.log.error(Logs.fileline() + ' : ControlIntRes ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # Update item
        if id_item > 0:
            self.log.info(Logs.fileline() + ' : TRACE update ControlIntRes')

            ret = Quality.updateControlIntRes(cti_ser=id_item,
                                              cti_ctq=args['cti_ctq'],
                                              cti_date=args['cti_date'],
                                              cti_type=args['cti_type'],
                                              cti_target=str(args['cti_target']),
                                              cti_result=str(args['cti_result']),
                                              cti_comment=args['cti_comment'])

            if ret is False:
                self.log.error(Logs.alert() + ' : ControlIntRes ERROR update')
                return compose_ret('', Constants.cst_content_type_json, 500)

        # Insert new item
        else:
            self.log.info(Logs.fileline() + ' : TRACE insert ControlIntRes')
            ret = Quality.insertControlIntRes(cti_ctq=args['cti_ctq'],
                                              cti_date=args['cti_date'],
                                              cti_type=args['cti_type'],
                                              cti_target=str(args['cti_target']),
                                              cti_result=str(args['cti_result']),
                                              cti_comment=args['cti_comment'])

            if ret <= 0:
                self.log.error(Logs.alert() + ' : ControlIntRes ERROR  insert')
                return compose_ret('', Constants.cst_content_type_json, 500)

            id_item = ret

        self.log.info(Logs.fileline() + ' : TRACE ControlIntRes id_item=' + str(id_item))
        return compose_ret(id_item, Constants.cst_content_type_json)


class ControlIntResExport(Resource):
    log = logging.getLogger('log_services')

    def post(self, id_ctrl):
        l_data = [['ctq_ser', 'ctq_name', 'ctq_type_val', 'eqp_name', 'cti_date', 'cti_target', 'cti_result', 'cti_comment', ]]
        controlDet = Quality.getControlDet(id_ctrl)

        if not controlDet:
            self.log.error(Logs.fileline() + ' : post ControlIntResExport failed no controlDet with id_ctrl=' + str(id_ctrl))
            return False

        ctq_type = controlDet['ctq_type_val']
        ctq_name = controlDet['ctq_name']
        eqp_name = controlDet['eqp_name']

        dict_data = Quality.getControlIntResList(id_ctrl)

        Various.useLangDB()

        if dict_data:
            for d in dict_data:
                data = []

                data.append(id_ctrl)
                data.append(ctq_name)
                data.append(ctq_type)
                data.append(eqp_name)

                if d['cti_date']:
                    data.append(datetime.strftime(d['cti_date'], '%Y-%m-%d %H:%M'))
                else:
                    data.append('')

                data.append(d['cti_target'])
                data.append(d['cti_result'])
                data.append(d['cti_comment'])

                l_data.append(data)

        # if no result to export
        if len(l_data) < 2:
            return compose_ret('', Constants.cst_content_type_json, 404)

        # write csv file
        try:
            import csv

            today = datetime.now().strftime("%Y%m%d")

            filename = 'control_int_' + str(id_ctrl) + '_' + str(today) + '.csv'

            with open('tmp/' + filename, mode='w', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=';')
                for line in l_data:
                    writer.writerow(line)

        except Exception as err:
            self.log.error(Logs.fileline() + ' : post ControlIntResExport failed, err=%s', err)
            return False

        self.log.info(Logs.fileline() + ' : TRACE ControlIntResExport id_ctrl=' + str(id_ctrl))
        return compose_ret('', Constants.cst_content_type_json)


class ControlExtExport(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        l_data = [['ctq_ser', 'ctq_name', 'ctq_type_ctrl', 'ctq_type_val', 'eqp_name', ]]
        dict_data = Quality.getControlList('EXT')

        Various.useLangDB()

        if dict_data:
            for d in dict_data:
                data = []

                data.append(d['id_item'])
                data.append(d['ctq_name'])
                data.append(d['ctq_type_ctrl'])
                data.append(d['ctq_type_val'])
                data.append(d['eqp_name'])

                l_data.append(data)

        # if no result to export
        if len(l_data) < 2:
            return compose_ret('', Constants.cst_content_type_json, 404)

        # write csv file
        try:
            import csv

            today = datetime.now().strftime("%Y%m%d")

            filename = 'control_ext_' + str(today) + '.csv'

            with open('tmp/' + filename, mode='w', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=';')
                for line in l_data:
                    writer.writerow(line)

        except Exception as err:
            self.log.error(Logs.fileline() + ' : post ControlExtExport failed, err=%s', err)
            return False

        self.log.info(Logs.fileline() + ' : TRACE ControlExtExport')
        return compose_ret('', Constants.cst_content_type_json)


class ControlExtResList(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_ctrl):
        l_items = Quality.getControlExtResList(id_ctrl)

        if not l_items:
            self.log.error(Logs.fileline() + ' : TRACE ControlExtResList not found')

        for item in l_items:
            # Replace None by empty string
            for key, value in list(item.items()):
                if item[key] is None:
                    item[key] = ''

            if item['cte_date']:
                item['cte_date'] = datetime.strftime(item['cte_date'], '%Y-%m-%d %H:%M')

            # search last id_file for each manual
            l_files = File.getFileDocList("CTRL", item['id_item'])

            if l_files and l_files[0]['id_data']:
                item['id_file'] = l_files[0]['id_data']
            else:
                item['id_file'] = 0

            if l_files and l_files[0]['name']:
                item['filename'] = l_files[0]['name']
            else:
                item['filename'] = ''

        self.log.info(Logs.fileline() + ' : TRACE ControlExtResList id_ctrl : ' + str(id_ctrl))
        return compose_ret(l_items, Constants.cst_content_type_json)


class ControlExtRes(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_item):
        item = Quality.getControlExtRes(id_item)

        if not item:
            self.log.error(Logs.fileline() + ' : ' + 'ControlExtRes ERROR not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        # Replace None by empty string
        for key, value in list(item.items()):
            if item[key] is None:
                item[key] = ''

        if item['cte_date']:
            item['cte_date'] = datetime.strftime(item['cte_date'], '%Y-%m-%dT%H:%M')

        self.log.info(Logs.fileline() + ' : ControlExtRes id_item=' + str(id_item))
        return compose_ret(item, Constants.cst_content_type_json, 200)

    def post(self, id_item):
        args = request.get_json()

        if 'cte_ctq' not in args or 'cte_date' not in args or 'cte_type' not in args or 'cte_organizer' not in args or \
           'cte_contact' not in args or 'cte_conform' not in args or 'cte_comment' not in args:
            self.log.error(Logs.fileline() + ' : ControlExtRes ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # Update item
        if id_item > 0:
            self.log.info(Logs.fileline() + ' : TRACE update ControlExtRes')
            ret = Quality.updateControlExtRes(cte_ser=id_item,
                                              cte_ctq=args['cte_ctq'],
                                              cte_date=args['cte_date'],
                                              cte_type=args['cte_type'],
                                              cte_organizer=args['cte_organizer'],
                                              cte_contact=args['cte_contact'],
                                              cte_conform=str(args['cte_conform']),
                                              cte_comment=args['cte_comment'])

            if ret is False:
                self.log.error(Logs.alert() + ' : ControlExtRes ERROR update')
                return compose_ret('', Constants.cst_content_type_json, 500)

        # Insert new item
        else:
            self.log.info(Logs.fileline() + ' : TRACE insert ControlExtRes')
            ret = Quality.insertControlExtRes(cte_ctq=args['cte_ctq'],
                                              cte_date=args['cte_date'],
                                              cte_type=args['cte_type'],
                                              cte_organizer=args['cte_organizer'],
                                              cte_contact=args['cte_contact'],
                                              cte_conform=str(args['cte_conform']),
                                              cte_comment=args['cte_comment'])

            if ret <= 0:
                self.log.error(Logs.alert() + ' : ControlExtRes ERROR insert')
                return compose_ret('', Constants.cst_content_type_json, 500)

            id_item = ret

        self.log.info(Logs.fileline() + ' : TRACE ControlExtRes id_item=' + str(id_item))
        return compose_ret(id_item, Constants.cst_content_type_json)


class ControlExtResExport(Resource):
    log = logging.getLogger('log_services')

    def post(self, id_ctrl):
        l_data = [['ctq_ser', 'ctq_name', 'ctq_type_val', 'eqp_name', 'cte_date', 'cte_organizer', 'cte_contact', 'cte_conform', 'cte_comment', ]]
        controlDet = Quality.getControlDet(id_ctrl)

        if not controlDet:
            self.log.error(Logs.fileline() + ' : post ControlExtResExport failed no controlDet with id_ctrl=' + str(id_ctrl))
            return False

        ctq_type = controlDet['ctq_type_val']
        ctq_name = controlDet['ctq_name']
        eqp_name = controlDet['eqp_name']

        dict_data = Quality.getControlExtResList(id_ctrl)

        Various.useLangDB()

        if dict_data:
            for d in dict_data:
                data = []

                data.append(id_ctrl)
                data.append(ctq_name)
                data.append(ctq_type)
                data.append(eqp_name)

                if d['cte_date']:
                    data.append(datetime.strftime(d['cte_date'], '%Y-%m-%d %H:%M'))
                else:
                    data.append('')

                data.append(d['cte_organizer'])
                data.append(d['cte_contact'])
                data.append(d['cte_conform'])
                data.append(d['cte_comment'])

                l_data.append(data)

        # if no result to export
        if len(l_data) < 2:
            return compose_ret('', Constants.cst_content_type_json, 404)

        # write csv file
        try:
            import csv

            today = datetime.now().strftime("%Y%m%d")

            filename = 'control_ext_' + str(id_ctrl) + '_' + str(today) + '.csv'

            with open('tmp/' + filename, mode='w', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=';')
                for line in l_data:
                    writer.writerow(line)

        except Exception as err:
            self.log.error(Logs.fileline() + ' : post ControlExtResExport failed, err=%s', err)
            return False

        self.log.info(Logs.fileline() + ' : TRACE ControlExtResExport id_ctrl=' + str(id_ctrl))
        return compose_ret('', Constants.cst_content_type_json)


class EquipmentList(Resource):
    log = logging.getLogger('log_services')

    def get(self):
        l_items = Quality.getEquipmentList()

        if not l_items:
            self.log.error(Logs.fileline() + ' : TRACE EquipmentList not found')

        Various.useLangDB()

        for item in l_items:
            # Replace None by empty string
            for key, value in list(item.items()):
                if item[key] is None:
                    item[key] = ''
                elif key == 'section' and item[key]:
                    item[key] = _(item[key].strip())

        self.log.info(Logs.fileline() + ' : TRACE EquipmentList')
        return compose_ret(l_items, Constants.cst_content_type_json)


class EquipmentSearch(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        l_items = Quality.getEquipmentSearch(args['term'])

        if not l_items:
            self.log.error(Logs.fileline() + ' : TRACE EquipmentSearch not found')

        self.log.info(Logs.fileline() + ' : TRACE EquipmentSearch')
        return compose_ret(l_items, Constants.cst_content_type_json)


class EquipmentDet(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_item):
        item = Quality.getEquipment(id_item)

        if not item:
            self.log.error(Logs.fileline() + ' : ' + 'EquipmentDet ERROR not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        # Replace None by empty string
        for key, value in list(item.items()):
            if item[key] is None:
                item[key] = ''

        l_lic = Quality.getListComment(id_item, 'E', 'B')

        if l_lic:
            item['breakdown'] = l_lic
        else:
            item['breakdown'] = []

        l_lic = Quality.getListComment(id_item, 'E', 'M')

        if l_lic:
            item['maintenance'] = l_lic
        else:
            item['maintenance'] = []

        if item['date_endcontract']:
            item['date_endcontract'] = datetime.strftime(item['date_endcontract'], '%Y-%m-%d')

        if item['date_receipt']:
            item['date_receipt'] = datetime.strftime(item['date_receipt'], '%Y-%m-%d')

        if item['date_buy']:
            item['date_buy'] = datetime.strftime(item['date_buy'], '%Y-%m-%d')

        if item['date_onduty']:
            item['date_onduty'] = datetime.strftime(item['date_onduty'], '%Y-%m-%d')

        if item['date_revoc']:
            item['date_revoc'] = datetime.strftime(item['date_revoc'], '%Y-%m-%d')

        self.log.info(Logs.fileline() + ' : EquipmentDet id_item=' + str(id_item))
        return compose_ret(item, Constants.cst_content_type_json, 200)

    def post(self, id_item):
        args = request.get_json()

        if 'id_owner' not in args or 'id_item' not in args or 'name' not in args or 'maker' not in args or 'model' not in args or \
           'funct' not in args or 'location' not in args or 'section' not in args or 'supplier' not in args or \
           'serial' not in args or 'inventory' not in args or 'incharge' not in args or 'manual' not in args or  \
           'procedur' not in args or 'breakdown' not in args or 'maintenance' not in args or 'calibration' not in args or \
           'contract' not in args or 'date_endcontract' not in args or 'date_receipt' not in args or 'date_buy' not in args or \
           'date_onduty' not in args or 'date_revoc' not in args or 'comment' not in args:
            self.log.error(Logs.fileline() + ' : EquipmentDet ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # Update item
        if id_item > 0:
            if args['breakdown']:
                ret = Quality.insertListComment(lic_ref=id_item,
                                                lic_type='E',
                                                lic_sub_type='B',
                                                lic_user=args['id_owner'],
                                                lic_comm=args['breakdown'])

                if not ret:
                    self.log.error(Logs.alert() + ' : EquipmentDet ERROR insert list comment breakdown')
                    return compose_ret('', Constants.cst_content_type_json, 500)

            if args['maintenance']:
                ret = Quality.insertListComment(lic_ref=id_item,
                                                lic_type='E',
                                                lic_sub_type='M',
                                                lic_user=args['id_owner'],
                                                lic_comm=args['maintenance'])

                if not ret:
                    self.log.error(Logs.alert() + ' : EquipmentDet ERROR insert list comment maintenance')
                    return compose_ret('', Constants.cst_content_type_json, 500)

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
                                          calibration=args['calibration'],
                                          contract=args['contract'],
                                          date_endcontract=args['date_endcontract'],
                                          date_receipt=args['date_receipt'],
                                          date_buy=args['date_buy'],
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
                                          calibration=args['calibration'],
                                          contract=args['contract'],
                                          date_endcontract=args['date_endcontract'],
                                          date_receipt=args['date_receipt'],
                                          date_buy=args['date_buy'],
                                          date_onduty=args['date_onduty'],
                                          date_revoc=args['date_revoc'],
                                          comment=args['comment'])

            if ret <= 0:
                self.log.error(Logs.alert() + ' : EquipmentDet ERROR  insert')
                return compose_ret('', Constants.cst_content_type_json, 500)

            id_item = ret

            if args['breakdown']:
                ret = Quality.insertListComment(lic_ref=id_item,
                                                lic_type='E',
                                                lic_sub_type='B',
                                                lic_user=args['id_owner'],
                                                lic_comm=args['breakdown'])

                if not ret:
                    self.log.error(Logs.alert() + ' : EquipmentDet ERROR insert list comment breakdown')
                    return compose_ret('', Constants.cst_content_type_json, 500)

            if args['maintenance']:
                ret = Quality.insertListComment(lic_ref=id_item,
                                                lic_type='E',
                                                lic_sub_type='M',
                                                lic_user=args['id_owner'],
                                                lic_comm=args['maintenance'])

                if not ret:
                    self.log.error(Logs.alert() + ' : EquipmentDet ERROR insert list comment maintenance')
                    return compose_ret('', Constants.cst_content_type_json, 500)

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

        Various.useLangDB()

        if dict_data:
            for d in dict_data:
                data = []

                data.append(d['id_data'])
                data.append(d['name'])
                data.append(d['maker'])
                data.append(d['model'])
                data.append(d['funct'])
                data.append(d['location'])
                section = d['section']
                if section:
                    data.append(_(section.strip()))
                else:
                    data.append('')

                l_data.append(data)

        # if no result to export
        if len(l_data) < 2:
            return compose_ret('', Constants.cst_content_type_json, 404)

        # write csv file
        try:
            import csv

            today = datetime.now().strftime("%Y%m%d")

            filename = 'equipment_' + str(today) + '.csv'

            with open('tmp/' + filename, mode='w', encoding='utf-8') as file:
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

        Various.useLangDB()

        for item in l_items:
            # Replace None by empty string
            for key, value in list(item.items()):
                if item[key] is None:
                    item[key] = ''
                elif key == 'section' and item[key]:
                    item[key] = _(item[key].strip())

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
        for key, value in list(item.items()):
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

        Various.useLangDB()

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
                section = d['section']
                if section:
                    data.append(_(section.strip()))
                else:
                    data.append('')

                l_data.append(data)

        # if no result to export
        if len(l_data) < 2:
            return compose_ret('', Constants.cst_content_type_json, 404)

        # write csv file
        try:
            import csv

            today = datetime.now().strftime("%Y%m%d")

            filename = 'manual_' + str(today) + '.csv'

            with open('tmp/' + filename, mode='w', encoding='utf-8') as file:
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

        Various.useLangDB()

        for item in l_items:
            # Replace None by empty string
            for key, value in list(item.items()):
                if item[key] is None:
                    item[key] = ''
                elif key == 'type' and item[key]:
                    item[key] = _(item[key].strip())

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
        for key, value in list(item.items()):
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
        l_data = [['id_data', 'date_meeting', 'type', 'type_id', 'promoter', 'report', ]]
        dict_data = Quality.getMeetingList()

        Various.useLangDB()

        if dict_data:
            for d in dict_data:
                data = []

                data.append(d['id_data'])
                data.append(d['date_meeting'])
                type = d['type']
                data.append(_(type.strip()))
                data.append(d['type_id'])
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

            with open('tmp/' + filename, mode='w', encoding='utf-8') as file:
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

        Various.useLangDB()

        for item in l_items:
            # Replace None by empty string
            for key, value in list(item.items()):
                if item[key] is None:
                    item[key] = ''
                elif key == 'section' and item[key]:
                    item[key] = _(item[key].strip())

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
        for key, value in list(item.items()):
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

        Various.useLangDB()

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
                section = d['section']
                if section:
                    data.append(_(section.strip()))
                else:
                    data.append('')

                l_data.append(data)

        # if no result to export
        if len(l_data) < 2:
            return compose_ret('', Constants.cst_content_type_json, 404)

        # write csv file
        try:
            import csv

            today = datetime.now().strftime("%Y%m%d")

            filename = 'procedure_' + str(today) + '.csv'

            with open('tmp/' + filename, mode='w', encoding='utf-8') as file:
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

        Various.useLangDB()

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
                section = d['section']
                if section:
                    data.append(_(section.strip()))
                else:
                    data.append('')
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

            with open('tmp/' + filename, mode='w', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=';')
                for line in l_data:
                    writer.writerow(line)

        except Exception as err:
            self.log.error(Logs.fileline() + ' : post ExportStaff failed, err=%s', err)
            return False

        self.log.info(Logs.fileline() + ' : TRACE ExportStaff')
        return compose_ret('', Constants.cst_content_type_json)


class StockCancelIO(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        if not args or 'id_stock' not in args or 'type_move' not in args or 'id_user' not in args:
            self.log.error(Logs.fileline() + ' : StockCancelIO ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        ret = Quality.cancelStockIO(id_stock=args['id_stock'], type_move=args['type_move'], id_user=args['id_user'])

        if ret is False:
            self.log.error(Logs.alert() + ' : StockCancelIO ERROR update')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE StockCancelIO')
        return compose_ret('', Constants.cst_content_type_json)


class StockList(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        if not args:
            args = {}

        l_stocks = Quality.getStockList(args)

        if not l_stocks:
            self.log.error(Logs.fileline() + ' : TRACE StockList not found')

        Various.useLangDB()

        for stock in l_stocks:
            # Replace None by empty string
            for key, value in list(stock.items()):
                if stock[key] is None:
                    stock[key] = ''
                elif key == 'type' and stock[key]:
                    stock[key] = _(stock[key].strip())
                elif key == 'conserv' and stock[key]:
                    stock[key] = _(stock[key].strip())

            if stock['pru_nb_pack']:
                stock['pru_nb_pack'] = float(stock['pru_nb_pack'])
            else:
                stock['pru_nb_pack'] = 0

            nb_supply = Quality.getSumStockSupply(stock['prs_prd'])
            if nb_supply:
                stock['prs_nb_pack'] = nb_supply['total']
                stock['prs_nb_pack'] = float(stock['prs_nb_pack']) - float(stock['pru_nb_pack'])
            else:
                stock['prs_nb_pack'] = 0

            stock['nb_total'] = float(stock['prs_nb_pack'] * stock['prd_nb_by_pack'])

            if stock['expir_date']:
                if stock['prd_expir_oblig'] == 'Y':
                    delta = stock['expir_date'] - datetime.now()
                    stock['day_to_expir'] = delta.days
                else:
                    stock['day_to_expir'] = 1000  # big number to not trigger stock alert
                stock['expir_date']   = datetime.strftime(stock['expir_date'], '%Y-%m-%d')
            else:
                if stock['prd_expir_oblig'] == 'Y':
                    stock['day_to_expir'] = 0
                else:
                    stock['day_to_expir'] = 1000  # big number to not trigger stock alert
                stock['expir_date'] = ''

        self.log.info(Logs.fileline() + ' : TRACE StockList')
        return compose_ret(l_stocks, Constants.cst_content_type_json)


class StockListDet(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_item):
        l_stocks = Quality.getStockListDet(id_item)

        if not l_stocks:
            self.log.error(Logs.fileline() + ' : TRACE StockListDet not found')

        for stock in l_stocks:
            # Replace None by empty string
            for key, value in list(stock.items()):
                if stock[key] is None:
                    stock[key] = ''

            if stock['prs_receipt_date']:
                stock['prs_receipt_date'] = datetime.strftime(stock['prs_receipt_date'], '%Y-%m-%d')

            if stock['prs_expir_date']:
                if stock['prd_expir_oblig'] == 'Y':
                    delta = stock['prs_expir_date'] - datetime.now()
                    stock['day_to_expir'] = delta.days
                else:
                    stock['day_to_expir'] = 1000  # big number to not trigger stock alert
                stock['prs_expir_date'] = datetime.strftime(stock['prs_expir_date'], '%Y-%m-%d')
            else:
                if stock['prd_expir_oblig'] == 'Y':
                    stock['day_to_expir'] = 0
                else:
                    stock['day_to_expir'] = 1000  # big number to not trigger stock alert

                stock['prs_expir_date'] = ''

            if stock['pru_nb_pack']:
                stock['pru_nb_pack'] = float(stock['pru_nb_pack'])
            else:
                stock['pru_nb_pack'] = 0

            if stock['prs_nb_pack']:
                stock['prs_nb_pack'] = float(stock['prs_nb_pack']) - float(stock['pru_nb_pack'])
            else:
                stock['prs_nb_pack'] = 0

        self.log.info(Logs.fileline() + ' : TRACE StockListDet')
        return compose_ret(l_stocks, Constants.cst_content_type_json)


class StockProductHist(Resource):
    log = logging.getLogger('log_services')

    def post(self, id_item):
        args = request.get_json()

        if 'date_beg' not in args or 'date_end' not in args:
            self.log.error(Logs.fileline() + ' : StockProductHist ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        l_stocks = Quality.getStockProductHist(id_item, args['date_beg'], args['date_end'])

        if not l_stocks:
            self.log.error(Logs.fileline() + ' : TRACE StockProductHist not found')

        for stock in l_stocks:
            # Replace None by empty string
            for key, value in list(stock.items()):
                if stock[key] is None:
                    stock[key] = ''

            if 'prs_ser' not in stock:
                stock['prs_ser'] = 0

            if 'username' not in stock:
                stock['username'] = ''

            if 'prs_rack' not in stock:
                stock['prs_rack'] = ''

            if 'prs_batch_num' not in stock:
                stock['prs_batch_num'] = ''

            if 'prs_buy_price' not in stock:
                stock['prs_buy_price'] = ''

            if 'prs_receipt_date' in stock and stock['prs_receipt_date']:
                stock['prs_receipt_date'] = datetime.strftime(stock['prs_receipt_date'], '%Y-%m-%d')
            else:
                stock['prs_receipt_date'] = ''

            if 'prs_expir_date' in stock and stock['prs_expir_date']:
                stock['prs_expir_date'] = datetime.strftime(stock['prs_expir_date'], '%Y-%m-%d')
            else:
                stock['prs_expir_date'] = ''

            if 'pru_nb_pack' in stock and stock['pru_nb_pack']:
                stock['pru_nb_pack'] = float(stock['pru_nb_pack'])
            else:
                stock['pru_nb_pack'] = 0

            if 'prs_nb_pack' in stock and stock['prs_nb_pack']:
                stock['prs_nb_pack'] = float(stock['prs_nb_pack'])
            else:
                stock['prs_nb_pack'] = 0

            if 'prs_lessor' not in stock:
                stock['prs_lessor'] = ''

            if stock['date_create']:
                stock['date_create'] = datetime.strftime(stock['date_create'], '%Y-%m-%d %H:%M')

        self.log.info(Logs.fileline() + ' : TRACE StockProductHist')
        return compose_ret(l_stocks, Constants.cst_content_type_json)


class StockProductList(Resource):
    log = logging.getLogger('log_services')

    def get(self):
        l_products = Quality.getStockProductList()

        if not l_products:
            self.log.error(Logs.fileline() + ' : TRACE StockProductList not found')

        Various.useLangDB()

        for product in l_products:
            # Replace None by empty string
            for key, value in list(product.items()):
                if product[key] is None:
                    product[key] = ''
                elif key == 'type' and product[key]:
                    product[key] = _(product[key].strip())
                elif key == 'conserv' and product[key]:
                    product[key] = _(product[key].strip())

        self.log.info(Logs.fileline() + ' : TRACE StockProductList')
        return compose_ret(l_products, Constants.cst_content_type_json)


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
        for key, value in list(stock.items()):
            if stock[key] is None:
                stock[key] = ''

        self.log.info(Logs.fileline() + ' : StockProductDet id_item=' + str(id_item))
        return compose_ret(stock, Constants.cst_content_type_json, 200)

    def post(self, id_item):
        args = request.get_json()

        if 'prd_name' not in args or 'prd_type' not in args or 'prd_nb_by_pack' not in args or \
           'prd_supplier' not in args or 'prd_ref_supplier' not in args or \
           'prd_conserv' not in args or 'prd_safe_limit' not in args or 'prd_expir_oblig' not in args:
            self.log.error(Logs.fileline() + ' : StockProductDet ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # Update stock product
        if id_item > 0:
            ret = Quality.updateStockProduct(prd_ser=id_item,
                                             prd_name=args['prd_name'],
                                             prd_type=args['prd_type'],
                                             prd_nb_by_pack=args['prd_nb_by_pack'],
                                             prd_safe_limit=args['prd_safe_limit'],
                                             prd_supplier=args['prd_supplier'],
                                             prd_ref_supplier=args['prd_ref_supplier'],
                                             prd_conserv=args['prd_conserv'],
                                             prd_expir_oblig=args['prd_expir_oblig'])

            if ret is False:
                self.log.error(Logs.alert() + ' : StockProductDet ERROR update')
                return compose_ret('', Constants.cst_content_type_json, 500)

        # Insert new stock product
        else:
            ret = Quality.insertStockProduct(prd_name=args['prd_name'],
                                             prd_type=args['prd_type'],
                                             prd_nb_by_pack=args['prd_nb_by_pack'],
                                             prd_safe_limit=args['prd_safe_limit'],
                                             prd_supplier=args['prd_supplier'],
                                             prd_ref_supplier=args['prd_ref_supplier'],
                                             prd_conserv=args['prd_conserv'],
                                             prd_expir_oblig=args['prd_expir_oblig'])

            if ret <= 0:
                self.log.error(Logs.alert() + ' : StockProductDet ERROR  insert')
                return compose_ret('', Constants.cst_content_type_json, 500)

            id_item = ret

        self.log.info(Logs.fileline() + ' : TRACE StockProductDet id_item=' + str(id_item))
        return compose_ret('', Constants.cst_content_type_json)

    def delete(self, id_item):
        ret = Quality.deleteStockProduct(id_item)

        if not ret:
            self.log.error(Logs.fileline() + ' : TRACE StockProductDet delete ERROR')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE StockProductDet delete id_item=' + str(id_item))
        return compose_ret('', Constants.cst_content_type_json)


class StockSupplyDet(Resource):
    log = logging.getLogger('log_services')

    def post(self, id_item):
        args = request.get_json()

        if 'prs_prd' not in args or 'prs_nb_pack' not in args or 'prs_user' not in args or \
           'prs_receipt_date' not in args or 'prs_rack' not in args or 'prs_expir_date' not in args or \
           'prs_batch_num' not in args or 'prs_buy_price' not in args or 'prs_lessor' not in args:
            self.log.error(Logs.fileline() + ' : StockSupplyDet ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        """ USELESS 26/08/2021
        # Update stock product
        if id_item > 0:
            ret = Quality.updateStockSupply(prs_ser=id_item,
                                            prs_user=args['prs_user'],
                                            prs_prd=args['prs_prd'],
                                            prs_nb_pack=args['prs_nb_pack'],
                                            prs_receipt_date=args['prs_receipt_date'],
                                            prs_expir_date=args['prs_expir_date'],
                                            prs_rack=args['prs_rack'],
                                            prs_batch_num=args['prs_batch_num'],
                                            prs_buy_price=args['prs_buy_price'],
                                            prs_lessor=args['prs_lessor'])

            if ret is False:
                self.log.error(Logs.alert() + ' : StockSupplyDet ERROR update')
                return compose_ret('', Constants.cst_content_type_json, 500)

        # Insert new supply product
        else:"""
        ret = Quality.insertStockSupply(prs_prd=args['prs_prd'],
                                        prs_user=args['prs_user'],
                                        prs_nb_pack=args['prs_nb_pack'],
                                        prs_receipt_date=args['prs_receipt_date'],
                                        prs_expir_date=args['prs_expir_date'],
                                        prs_rack=args['prs_rack'],
                                        prs_batch_num=args['prs_batch_num'],
                                        prs_buy_price=args['prs_buy_price'],
                                        prs_lessor=args['prs_lessor'])

        if ret <= 0:
            self.log.error(Logs.alert() + ' : StockSupplyDet ERROR insert')
            return compose_ret('', Constants.cst_content_type_json, 500)

        id_item = ret

        self.log.info(Logs.fileline() + ' : TRACE StockSupplyDet id_item=' + str(id_item))
        return compose_ret('', Constants.cst_content_type_json)


class StockUse(Resource):
    log = logging.getLogger('log_services')

    def get(self, prs_ser):
        stock_use = Quality.getNbStockUse(prs_ser)

        if not stock_use:
            self.log.error(Logs.fileline() + ' : ' + 'nb StockUse not found')
            nb_stock_use = 0
            return compose_ret(nb_stock_use, Constants.cst_content_type_json, 200)

        if stock_use['nb_pack']:
            nb_stock_use = float(stock_use['nb_pack'])
        else:
            nb_stock_use = 0

        self.log.info(Logs.fileline() + ' : nb StockUse prs_ser=' + str(prs_ser))
        return compose_ret(nb_stock_use, Constants.cst_content_type_json, 200)

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

        # check if it is the last pack to use
        PackSupply = Quality.getNbStockSupply(args['pru_prs'])
        PackUse    = Quality.getNbStockUse(args['pru_prs'])

        if (PackSupply['nb_pack'] - PackUse['nb_pack']) == 0:
            ret = Quality.emptyStockSupply(args['pru_prs'])

            if ret is False:
                self.log.error(Logs.alert() + ' : StockUse ERROR empty prs_ser=' + str(args['pru_prs']))
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

        l_data = [['prs_ser', 'name', 'nb_pack', 'nb_total', 'type', 'conserv', 'supplier']]
        dict_data = Quality.getStockList(args)

        Various.useLangDB()

        if dict_data:
            for d in dict_data:
                data = []

                if d['pru_nb_pack']:
                    d['pru_nb_pack'] = float(d['pru_nb_pack'])
                else:
                    d['pru_nb_pack'] = 0

                nb_supply = Quality.getSumStockSupply(d['prs_prd'])
                if nb_supply:
                    d['prs_nb_pack'] = nb_supply['total']
                    d['prs_nb_pack'] = float(d['prs_nb_pack']) - float(d['pru_nb_pack'])
                else:
                    d['prs_nb_pack'] = 0

                d['nb_total'] = float(d['prs_nb_pack'] * d['prd_nb_by_pack'])

                data.append(d['prs_ser'])
                data.append(d['prd_name'])
                data.append(d['prs_nb_pack'])
                data.append(d['nb_total'])
                type = d['type']
                if type:
                    data.append(_(type.strip()))
                else:
                    data.append('')
                conserv = d['conserv']
                if conserv:
                    data.append(_(conserv.strip()))
                else:
                    data.append('')
                data.append(d['supplier'])

                l_data.append(data)

        # if no result to export
        if len(l_data) < 2:
            return compose_ret('', Constants.cst_content_type_json, 404)

        # write csv file
        try:
            import csv

            today = datetime.now().strftime("%Y%m%d")

            filename = 'stock_' + str(today) + '.csv'

            with open('tmp/' + filename, mode='w', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=';')
                for line in l_data:
                    writer.writerow(line)

        except Exception as err:
            self.log.error(Logs.fileline() + ' : post StockExport failed, err=%s', err)
            return False

        self.log.info(Logs.fileline() + ' : TRACE StockExport')
        return compose_ret('', Constants.cst_content_type_json)


class StockProductsExport(Resource):
    log = logging.getLogger('log_services')

    def get(self):
        l_data = [['prd_ser', 'date', 'name', 'type', 'nb_by_pack', 'supplier', 'ref_supplier', 'conserv',
                   'safe_limit']]
        dict_data = Quality.getStockExportProducts()

        Various.useLangDB()

        if dict_data:
            for d in dict_data:
                data = []

                data.append(d['prd_ser'])
                data.append(d['prd_date'])
                data.append(d['prd_name'])

                type = d['type']
                if type:
                    data.append(_(type.strip()))
                else:
                    data.append('')

                data.append(d['prd_nb_by_pack'])
                data.append(d['supplier'])
                data.append(d['prd_ref_supplier'])

                conserv = d['conserv']
                if conserv:
                    data.append(_(conserv.strip()))
                else:
                    data.append('')

                data.append(d['prd_safe_limit'])

                l_data.append(data)

        # if no result to export
        if len(l_data) < 2:
            return compose_ret('', Constants.cst_content_type_json, 404)

        # write csv file
        try:
            import csv

            today = datetime.now().strftime("%Y%m%d")

            filename = 'stock_products_' + str(today) + '.csv'

            with open('tmp/' + filename, mode='w', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=';')
                for line in l_data:
                    writer.writerow(line)

        except Exception as err:
            self.log.error(Logs.fileline() + ' : post StockProductsExport failed, err=%s', err)
            return False

        self.log.info(Logs.fileline() + ' : TRACE StockProductsExport')
        return compose_ret('', Constants.cst_content_type_json)


class StockSuppliesExport(Resource):
    log = logging.getLogger('log_services')

    def get(self):
        l_data = [['prs_ser', 'date', 'product', 'nb_pack', 'receipt_date', 'expir_date', 'rack', 'batch_num',
                   'buy_price', 'user', 'empty', 'cancel', 'user_cancel', 'lessor']]
        dict_data = Quality.getStockExportSupplies()

        Various.useLangDB()

        if dict_data:
            for d in dict_data:
                data = []

                data.append(d['prs_ser'])
                data.append(d['prs_date'])
                data.append(d['product'])
                data.append(d['prs_nb_pack'])
                data.append(d['prs_receipt_date'])
                data.append(d['prs_expir_date'])
                data.append(d['prs_rack'])
                data.append(d['prs_batch_num'])
                data.append(d['prs_buy_price'] / 100)
                data.append(d['user'])
                data.append(d['prs_empty'])
                data.append(d['prs_cancel'])
                data.append(d['user_cancel'])
                data.append(d['prs_lessor'])

                l_data.append(data)

        # if no result to export
        if len(l_data) < 2:
            return compose_ret('', Constants.cst_content_type_json, 404)

        # write csv file
        try:
            import csv

            today = datetime.now().strftime("%Y%m%d")

            filename = 'stock_supplies_' + str(today) + '.csv'

            with open('tmp/' + filename, mode='w', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=';')
                for line in l_data:
                    writer.writerow(line)

        except Exception as err:
            self.log.error(Logs.fileline() + ' : post StockSuppliesExport failed, err=%s', err)
            return False

        self.log.info(Logs.fileline() + ' : TRACE StockSuppliesExport')
        return compose_ret('', Constants.cst_content_type_json)


class StockUsesExport(Resource):
    log = logging.getLogger('log_services')

    def get(self):
        l_data = [['pru_ser', 'date', 'product', 'nb_pack', 'user', 'cancel', 'user_cancel']]
        dict_data = Quality.getStockExportUses()

        Various.useLangDB()

        if dict_data:
            for d in dict_data:
                data = []

                data.append(d['pru_ser'])
                data.append(d['pru_date'])
                data.append(d['product'])
                data.append(d['pru_nb_pack'])
                data.append(d['user'])
                data.append(d['pru_cancel'])
                data.append(d['user_cancel'])

                l_data.append(data)

        # if no result to export
        if len(l_data) < 2:
            return compose_ret('', Constants.cst_content_type_json, 404)

        # write csv file
        try:
            import csv

            today = datetime.now().strftime("%Y%m%d")

            filename = 'stock_uses_' + str(today) + '.csv'

            with open('tmp/' + filename, mode='w', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=';')
                for line in l_data:
                    writer.writerow(line)

        except Exception as err:
            self.log.error(Logs.fileline() + ' : post StockUsesExport failed, err=%s', err)
            return False

        self.log.info(Logs.fileline() + ' : TRACE StockUsesExport')
        return compose_ret('', Constants.cst_content_type_json)


class SupplierList(Resource):
    log = logging.getLogger('log_services')

    def get(self):
        l_items = Quality.getSupplierList()

        if not l_items:
            self.log.error(Logs.fileline() + ' : TRACE SupplierList not found')

        for item in l_items:
            # Replace None by empty string
            for key, value in list(item.items()):
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
        for key, value in list(item.items()):
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

            with open('tmp/' + filename, mode='w', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=';')
                for line in l_data:
                    writer.writerow(line)

        except Exception as err:
            self.log.error(Logs.fileline() + ' : post ExportSupplier failed, err=%s', err)
            return False

        self.log.info(Logs.fileline() + ' : TRACE ExportSupplier')
        return compose_ret('', Constants.cst_content_type_json)


class ListComment(Resource):
    log = logging.getLogger('log_services')

    def delete(self, id_item):
        ret = Quality.deleteListComment(id_item)

        if not ret:
            self.log.error(Logs.fileline() + ' : TRACE ListComment delete ERROR')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE ListComment delete id_item=' + str(id_item))
        return compose_ret('', Constants.cst_content_type_json)
