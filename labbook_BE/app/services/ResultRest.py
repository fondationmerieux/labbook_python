# -*- coding:utf-8 -*-
import logging

from datetime import datetime
from flask import request
from flask_restful import Resource

from app.models.General import compose_ret
from app.models.Logs import Logs
from app.models.Analysis import *
from app.models.Constants import *
from app.models.Dict import *
from app.models.File import *
from app.models.Pdf import *
from app.models.Record import *
from app.models.Result import *
from app.models.User import *
from app.models.Various import *


class ResultValue(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        if 'list_answer' not in args:
            self.log.error(Logs.fileline() + ' : TRACE Result ERROR list_answer missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        for answer in args['list_answer']:
            ret = Result.updateResult(id_data=answer['id_res'],
                                      id_owner=answer['id_owner'],
                                      valeur=answer['value'])

            if ret is False:
                self.log.error(Logs.fileline() + ' : TRACE Result updateResult ERROR')
                return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE Result')
        return compose_ret('', Constants.cst_content_type_json)


class ResultList(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        if not args or ('date_beg' not in args and 'date_end' not in args):
            self.log.error(Logs.fileline() + ' : ResultList args missing')
            return compose_ret('', Constants.cst_content_type_json, 500)

        # convert isodate format to ymd format
        args['date_beg'] = datetime.strptime(args['date_beg'], Constants.cst_isodate).strftime(Constants.cst_date_ymd)
        args['date_end'] = datetime.strptime(args['date_end'], Constants.cst_isodate).strftime(Constants.cst_date_ymd)

        l_results = Result.getResultList(args)

        if not l_results:
            self.log.error(Logs.fileline() + ' : TRACE ResultList not found')

        for result in l_results:
            if result['date_dos']:
                result['date_dos'] = datetime.strftime(result['date_dos'], '%Y-%m-%d')

            if result['date_prescr']:
                result['date_prescr'] = datetime.strftime(result['date_prescr'], '%Y-%m-%d')

            # Get validation info
            result['validation'] = Result.getResultValidation(result['id_res'])

            if result['validation']['date_validation']:
                result['validation']['date_validation'] = datetime.strftime(result['validation']['date_validation'], '%Y-%m-%d')

            # Replace None by empty string
            for key, value in result['validation'].items():
                if result['validation'][key] is None:
                    result['validation'][key] = ''

            # Get identity from user who validated this result
            result['user'] = User.getUserByIdGroup(result['validation']['utilisateur'])

            if result['user']:
                # Replace None by empty string
                for key, value in result['user'].items():
                    if result['user'][key] is None:
                        result['user'][key] = ''

            # Get status labels of record
            tmp = Various.getDicoById(str(result['stat']))
            result['stat_label'] = tmp['label']

            # Get result answer
            type_res             = ''
            result['unit']       = ''
            result['res_answer'] = []

            # Get unit label
            if result['unite']:
                unit = Various.getDicoById(result['unite'])

                # get short_label (without prefix "dico_") in type_res
                if unit and unit['label']:
                    result['unit'] = unit['label']

            if result['type_resultat']:
                type_res = Various.getDicoById(result['type_resultat'])

                # get short_label (without prefix "dico_") in type_res
                if type_res and type_res['short_label'].startswith("dico_"):
                        type_res = type_res['short_label'][5:]
                else:
                    type_res = ''

            # init list of answer
            if type_res:
                result['res_answer'] = Dict.getDictDetails(str(type_res))

            # Replace None by empty string
            for key, value in result.items():
                if result[key] is None:
                    result[key] = ''

        self.log.info(Logs.fileline() + ' : TRACE ResultList')
        return compose_ret(l_results, Constants.cst_content_type_json)


class ResultRecord(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_rec):
        l_results = Result.getResultRecord(id_rec)

        if not l_results:
            self.log.error(Logs.fileline() + ' : ' + 'ResultRecord ERROR not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        for result in l_results:
            if result['date_dos']:
                result['date_dos'] = datetime.strftime(result['date_dos'], '%Y-%m-%d')

            if result['date_prescr']:
                result['date_prescr'] = datetime.strftime(result['date_prescr'], '%Y-%m-%d')

            # Get validation info
            result['validation'] = Result.getResultValidation(result['id_res'])

            if result['validation']['date_validation']:
                result['validation']['date_validation'] = datetime.strftime(result['validation']['date_validation'], '%Y-%m-%d')

            # Replace None by empty string
            for key, value in result['validation'].items():
                if result['validation'][key] is None:
                    result['validation'][key] = ''

            # Get identity from user who validated this result
            result['user'] = User.getUserByIdGroup(result['validation']['utilisateur'])

            if result['user']:
                # Replace None by empty string
                for key, value in result['user'].items():
                    if result['user'][key] is None:
                        result['user'][key] = ''

            # Get status labels of record
            tmp = Various.getDicoById(str(result['stat']))
            result['stat_label'] = tmp['label']

            # Replace None by empty string
            for key, value in result.items():
                if result[key] is None:
                    result[key] = ''

        self.log.info(Logs.fileline() + ' : ResultRecord id_rec=' + str(id_rec))
        return compose_ret(l_results, Constants.cst_content_type_json, 200)


class ResultCreate(Resource):
    log = logging.getLogger('log_services')

    def post(self, id_rec):
        args = request.get_json()

        if 'id_owner' not in args or 'user_role' not in args:
            self.log.error(Logs.fileline() + ' : ResultCreate ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        type_validation = 250

        # In case of add new analysis
        if 'list_ref' in args:
            l_ana = args['list_ref']
            # GET last id_data in sigl_04_data with ref_analyse
            for ana in l_ana:
                req_ana = Analysis.getLastAnalysisReqByRefAna(ana['ref_analyse'])
                ana['id_data'] = req_ana['id_data']
        else:
            # get list of all analysis for this record (even samples)
            l_ana = Analysis.getAnalysisReq(id_rec, 'A')

        self.log.error(Logs.fileline() + ' : DEBUG ResultCreate l_ana=' + str(l_ana))

        if not l_ana:
            self.log.error(Logs.fileline() + ' : ' + 'ResultCreate ERROR l_ana not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        # Loop on list_ana
        for ana in l_ana:
            l_ref = Analysis.getRefVariable(ana['ref_analyse'])

            for ref in l_ref:
                if ref and ref['id_refvariable']:
                    ret = Result.insertResult(id_owner=args['id_owner'],
                                              id_analyse=ana['id_data'],
                                              ref_variable=ref['id_refvariable'],
                                              obligatoire=ref['obligatoire'])

                    if ret <= 0:
                        self.log.error(Logs.alert() + ' : ResultCreate ERROR  insert result')
                        return compose_ret('', Constants.cst_content_type_json, 500)

                    res = {}
                    res['id_res'] = ret

                    # Get id_group of lab with id_group of user
                    id_group_lab = User.getUserGroupParent(args['id_owner'])

                    if not id_group_lab:
                        self.log.error(Logs.fileline() + ' : ResultCreate ERROR group not found')
                        return compose_ret('', Constants.cst_content_type_json, 500)

                    # insert sigl_09_data_group
                    ret = Result.insertResultGroup(id_data=res['id_res'],
                                                   id_group=id_group_lab['id_group_parent'])

                    if ret <= 0:
                        self.log.error(Logs.alert() + ' : ResultCreate ERROR  insert group')
                        return compose_ret('', Constants.cst_content_type_json, 500)

                    # insert corresponding validation
                    ret = Result.insertValidation(id_owner=args['id_owner'],
                                                  id_resultat=res['id_res'],
                                                  date_validation=datetime.strftime(datetime.now(), "%Y/%m/%d %H:%M:%S"),
                                                  utilisateur=args['id_owner'],
                                                  valeur=None,
                                                  type_validation=type_validation,
                                                  commentaire=None,
                                                  motif_annulation=None)

                    if ret <= 0:
                        self.log.error(Logs.alert() + ' : ResultCreate ERROR  insert validation')
                        return compose_ret('', Constants.cst_content_type_json, 500)

                    res = {}
                    res['id_valid'] = ret

                    # Get id_group of lab with id_group of user
                    id_group_lab = User.getUserGroupParent(args['id_owner'])

                    if not id_group_lab:
                        self.log.error(Logs.fileline() + ' : ResultCreate ERROR group not found')
                        return compose_ret('', Constants.cst_content_type_json, 500)

                    # insert sigl_10_data_group
                    ret = Result.insertValidationGroup(id_data=res['id_valid'],
                                                       id_group=id_group_lab['id_group_parent'])

                    if ret <= 0:
                        self.log.error(Logs.alert() + ' : ResultCreate ERROR  insert group validation')
                        return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE ResultCreate')
        return compose_ret('', Constants.cst_content_type_json)


class ResultValid(Resource):
    log = logging.getLogger('log_services')

    def post(self, type_valid, id_rec):
        args = request.get_json()

        if 'list_valid' not in args:
            self.log.error(Logs.fileline() + ' : TRACE ResultValid ERROR list_valid missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        if type_valid == 'T':
            type_validation = 251  # Technical result
            stat_rec = 254         # Technical record
            comment = None
        elif type_valid == 'B':
            type_validation = 252  # Biological result
            stat_rec = 256         # Biological record
            if args['comm_valid']:
                comment = args['comm_valid']
            else:
                comment = None
        else:
            self.log.error(Logs.fileline() + ' : TRACE ResultValid type_valid ERROR')
            return compose_ret('', Constants.cst_content_type_json, 500)

        # VALIDATION : insert validation
        for valid in args['list_valid']:
            id_owner = valid['id_owner']
            ret = Result.insertValidation(id_owner=valid['id_owner'],
                                          id_resultat=valid['id_res'],
                                          date_validation=valid['date_valid'],
                                          utilisateur=valid['user_valid'],
                                          valeur=valid['value'],
                                          type_validation=type_validation,
                                          commentaire=comment,
                                          motif_annulation=None)

            if ret <= 0:
                self.log.error(Logs.fileline() + ' : TRACE ResultValid insertValidation ERROR')
                return compose_ret('', Constants.cst_content_type_json, 500)

            res = {}
            res['id_valid'] = ret

            # Get id_group of lab with id_group of user
            id_group_lab = User.getUserGroupParent(id_owner)

            if not id_group_lab:
                self.log.error(Logs.fileline() + ' : ResultValid ERROR group not found')
                return compose_ret('', Constants.cst_content_type_json, 500)

            # insert sigl_10_data_group
            ret = Result.insertValidationGroup(id_data=res['id_valid'],
                                               id_group=id_group_lab['id_group_parent'])

            if ret <= 0:
                self.log.error(Logs.alert() + ' : ResultValid ERROR  insert group validation')
                return compose_ret('', Constants.cst_content_type_json, 500)

        # check if it was the last validation to do
        l_res = Result.getResultRecord(id_rec)

        if not l_res:
            self.log.error(Logs.fileline() + ' : TRACE ResultValid getResultRecord ERROR')
            return compose_ret('', Constants.cst_content_type_json, 500)

        for res in l_res:
            last_type = Result.getLastTypeValidation(res['id_ana'])
            if last_type:
                if type_valid == 'T' and last_type['type_validation'] == 250:
                    stat_rec = 253  # Technical intermediate record
                elif type_valid == 'B' and last_type['type_validation'] < 252:
                    stat_rec = 255  # biological intermediate record

        # RECORD : update status record
        ret = Record.updateRecordStat(id_rec, stat_rec)

        if not ret:
            self.log.error(Logs.fileline() + ' : ERROR ResultValid record stat update')
            return compose_ret('', Constants.cst_content_type_json, 500)

        # REPORT PART
        if type_valid == 'B':
            ret = File.insertFileReport(id_owner=id_owner,
                                        id_dos=id_rec,
                                        doc_type=257)

            if ret <= 0:
                self.log.error(Logs.fileline() + ' : TRACE ResultValid insertFileReport ERROR')
                return compose_ret('', Constants.cst_content_type_json, 500)

            res = {}
            res['id_file'] = ret

            # Get id_group of lab with id_group of user
            id_group_lab = User.getUserGroupParent(id_owner)

            if not id_group_lab:
                self.log.error(Logs.fileline() + ' : ResultValid ERROR group not found')
                return compose_ret('', Constants.cst_content_type_json, 500)

            # insert sigl_11_data_group
            ret = File.insertFileReportGroup(id_data=res['id_file'],
                                             id_group=id_group_lab['id_group_parent'])

            if ret <= 0:
                self.log.error(Logs.alert() + ' : ResultValid ERROR  insert group validation')
                return compose_ret('', Constants.cst_content_type_json, 500)

            # Get uuid filename and create pdf
            fileReport = File.getFileReport(id_rec)

            if fileReport:
                Pdf.getPdfReport(id_rec, fileReport['file'])

        self.log.info(Logs.fileline() + ' : TRACE ResultValid')
        return compose_ret('', Constants.cst_content_type_json)


class ResultReset(Resource):
    log = logging.getLogger('log_services')

    def post(self, id_rec):
        args = request.get_json()

        if 'id_owner' not in args or 'id_res' not in args:
            self.log.error(Logs.fileline() + ' : TRACE ResultReset ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # Update value of result
        ret = Result.updateResult(id_data=args['id_res'],
                                  id_owner=args['id_owner'],
                                  valeur=None)

        if ret is False:
            self.log.error(Logs.fileline() + ' : TRACE ResultReset updateResult ERROR')
            return compose_ret('', Constants.cst_content_type_json, 500)

        # Insert new validation
        ret = Result.insertValidation(id_owner=args['id_owner'],
                                      id_resultat=args['id_res'],
                                      date_validation=datetime.strftime(datetime.now(), "%Y/%m/%d %H:%M:%S"),
                                      utilisateur=args['id_owner'],
                                      valeur=None,
                                      type_validation=250,
                                      commentaire=None,
                                      motif_annulation=None)

        if ret <= 0:
            self.log.error(Logs.fileline() + ' : TRACE ResultReset insertValidation ERROR')
            return compose_ret('', Constants.cst_content_type_json, 500)

        res = {}
        res['id_valid'] = ret

        # Get id_group of lab with id_group of user
        id_group_lab = User.getUserGroupParent(args['id_owner'])

        if not id_group_lab:
            self.log.error(Logs.fileline() + ' : ResultReset ERROR group not found')
            return compose_ret('', Constants.cst_content_type_json, 500)

        # insert sigl_10_data_group
        ret = Result.insertValidationGroup(id_data=res['id_valid'],
                                           id_group=id_group_lab['id_group_parent'])

        if ret <= 0:
            self.log.error(Logs.alert() + ' : ResultReset ERROR  insert group validation')
            return compose_ret('', Constants.cst_content_type_json, 500)

        # Update record status to status administrative intermediate
        stat_rec = 253

        # update status record
        ret = Record.updateRecordStat(id_rec, stat_rec)

        if not ret:
            self.log.error(Logs.fileline() + ' : ERROR ResultReset record stat update')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE ResultReset')
        return compose_ret('', Constants.cst_content_type_json)


class ResultCancel(Resource):
    log = logging.getLogger('log_services')

    def post(self, id_rec):
        args = request.get_json()

        if 'id_owner' not in args or 'id_res' not in args or 'reason' not in args or 'comment' not in args:
            self.log.error(Logs.fileline() + ' : TRACE ResultCancel ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # Update value of result
        ret = Result.updateResult(id_data=args['id_res'],
                                  id_owner=args['id_owner'],
                                  valeur=None)

        if ret is False:
            self.log.error(Logs.fileline() + ' : TRACE ResultCancel updateResult ERROR')
            return compose_ret('', Constants.cst_content_type_json, 500)

        # Insert new validation
        ret = Result.insertValidation(id_owner=args['id_owner'],
                                      id_resultat=args['id_res'],
                                      date_validation=datetime.strftime(datetime.now(), "%Y/%m/%d %H:%M:%S"),
                                      utilisateur=args['id_owner'],
                                      valeur=None,
                                      type_validation=252,
                                      commentaire=args['comment'],
                                      motif_annulation=args['reason'])

        if ret <= 0:
            self.log.error(Logs.fileline() + ' : TRACE ResultCancel insertValidation ERROR')
            return compose_ret('', Constants.cst_content_type_json, 500)

        res = {}
        res['id_valid'] = ret

        # Get id_group of lab with id_group of user
        id_group_lab = User.getUserGroupParent(args['id_owner'])

        if not id_group_lab:
            self.log.error(Logs.fileline() + ' : ResultCancel ERROR group not found')
            return compose_ret('', Constants.cst_content_type_json, 500)

        # insert sigl_10_data_group
        ret = Result.insertValidationGroup(id_data=res['id_valid'],
                                           id_group=id_group_lab['id_group_parent'])

        if ret <= 0:
            self.log.error(Logs.alert() + ' : ResultCancel ERROR  insert group validation')
            return compose_ret('', Constants.cst_content_type_json, 500)

        # Update record status to status administrative intermediate
        stat_rec = 253

        # update status record
        ret = Record.updateRecordStat(id_rec, stat_rec)

        if not ret:
            self.log.error(Logs.fileline() + ' : ERROR ResultCancel record stat update')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE ResultCancel')
        return compose_ret('', Constants.cst_content_type_json)


class ResultHisto(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_res):
        l_valid = Result.getResultListValidation(id_res)

        if not l_valid:
            self.log.error(Logs.fileline() + ' : ' + 'ResultHisto ERROR not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        for valid in l_valid:
            # Replace None by empty string
            for key, value in valid.items():
                if valid[key] is None:
                    valid[key] = ''

            valid['dico_valid']  = Various.getDicoById(str(valid['type_validation']))
            valid['dico_cancel'] = Various.getDicoById(str(valid['motif_annulation']))

            valid['user'] = User.getUserByIdGroup(valid['utilisateur'])

            if valid['date_validation']:
                valid['date_validation'] = datetime.strftime(valid['date_validation'], '%Y-%m-%d')

        self.log.info(Logs.fileline() + ' : ResultHisto id_res=' + str(id_res))
        return compose_ret(l_valid, Constants.cst_content_type_json, 200)
