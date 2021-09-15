# -*- coding:utf-8 -*-
import logging

from flask import request
from flask_restful import Resource

from app.models.General import compose_ret
from app.models.Constants import *
from app.models.Dict import *
from app.models.Logs import Logs
from app.models.Various import Various


class DictDet(Resource):
    log = logging.getLogger('log_services')

    def get(self, dict_name):
        l_dicts = Dict.getDictDetails(dict_name)

        if not l_dicts:
            self.log.error(Logs.fileline() + ' : TRACE DictDet no l_dicts')
            l_dicts = {}

        Various.needTranslationDB()

        for dict in l_dicts:
            # Replace None by empty string
            for key, value in list(dict.items()):
                if dict[key] is None:
                    dict[key] = ''
                elif key == 'label':
                    dict[key] = _(dict[key])
                elif key == 'short_label':
                    dict[key] = _(dict[key])

        self.log.info(Logs.fileline() + ' : TRACE DictDet')
        return compose_ret(l_dicts, Constants.cst_content_type_json)

    def post(self, dict_name):
        args = request.get_json()

        if 'list_val' not in args:
            self.log.error(Logs.fileline() + ' : DictDet ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # check if dict_name already exist
        dict = Dict.getDictDetails(dict_name)

        # update dict
        if dict and dict[0]['dico_name'] == dict_name:
            self.log.error(Logs.fileline() + ' : DictDet UPDATE dict')

            for val in args['list_val']:
                if val['id_data'] > 0:
                    ret = Dict.updateDict(id_data=val['id_data'],
                                          label=val['label'],
                                          short_label=val['short_label'],
                                          position=val['position'],
                                          code=val['code'],
                                          archived=0)
                else:
                    ret = Dict.insertDict(id_owner=val['id_owner'],
                                          dico_name=dict_name,
                                          label=val['label'],
                                          short_label=val['short_label'],
                                          position=val['position'],
                                          code=val['code'])

                if ret is False or ret <= 0:
                    self.log.info(Logs.fileline() + ' : TRACE DictDet ERROR update val dict')
                    return compose_ret('', Constants.cst_content_type_json, 500)

            # delete missing values compared to dict
            for db_val in dict:
                exist = False
                for ihm_val in args['list_val']:
                    if db_val['id_data'] == ihm_val['id_data']:
                        exist = True

                if not exist:
                    ret = Dict.deleteDictValue(db_val['id_data'])

                    if ret is False:
                        self.log.info(Logs.fileline() + ' : TRACE DictDet ERROR delete val dict')
                        return compose_ret('', Constants.cst_content_type_json, 500)

        # insert new dict
        else:
            self.log.error(Logs.fileline() + ' : DictDet INSERT dict')

            for val in args['list_val']:
                # insert in sigl_dico_data
                ret = Dict.insertDict(id_owner=val['id_owner'],
                                      dico_name=dict_name,
                                      label=val['label'],
                                      short_label=val['short_label'],
                                      position=val['position'],
                                      code=val['code'])

                if ret <= 0:
                    self.log.error(Logs.alert() + ' : DictDet ERROR insert dict')
                    return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE DictDet dict_name=' + str(dict_name))
        return compose_ret('', Constants.cst_content_type_json)

    def delete(self, dict_name):
        args = request.get_json()

        if 'id_owner' not in args:
            self.log.error(Logs.fileline() + ' : DictDet ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # TODO record log action by user

        ret = Dict.deleteDict(dict_name)

        if ret is False:
            self.log.info(Logs.fileline() + ' : TRACE DictDet ERROR delete dict')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE DictDet delete dict_name=' + str(dict_name))
        return compose_ret('', Constants.cst_content_type_json)


class DictList(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        if not args:
            args = {}

        l_dicts = Dict.getDictList(args)

        if not l_dicts:
            self.log.error(Logs.fileline() + ' : TRACE DictList not found')

        for dict in l_dicts:
            # Replace None by empty string
            for key, value in list(dict.items()):
                if dict[key] is None:
                    dict[key] = ''

        self.log.info(Logs.fileline() + ' : TRACE DictList')
        return compose_ret(l_dicts, Constants.cst_content_type_json)
