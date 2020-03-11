# -*- coding:utf-8 -*-
import logging

from flask import request
from flask_restful import Resource

from app.models.General import compose_ret
from app.models.Constants import *
from app.models.Record import *
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


"""
class RecordDet(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_ana):
        Record = Record.getRecord(id_ana)

        if not Record:
            self.log.error(Logs.fileline() + ' : ' + 'RecordDet ERROR not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        # Replace None by empty string
        for key, value in Record.items():
            if Record[key] is None:
                Record[key] = ''

        self.log.info(Logs.fileline() + ' : RecordDet id_data=' + str(id_ana))
        return compose_ret(Record, Constants.cst_content_type_json, 200)


    def post(self, id_pat=0):
        args = request.get_json()

        if 'id_owner' not in args or 'anonyme' not in args or 'code' not in args or 'code_Record' not in args or 'nom' not in args or \
           'prenom' not in args or 'ddn' not in args or 'sexe' not in args or 'ethnie' not in args or 'adresse' not in args or \
           'cp' not in args or 'ville' not in args or 'tel' not in args or 'profession' not in args or 'nom_jf' not in args or \
           'quartier' not in args or 'bp' not in args or 'ddn_approx' not in args or 'age' not in args or 'annee_naiss' not in args or \
           'semaine_naiss' not in args or 'mois_naiss' not in args or 'unite' not in args:
            self.log.error(Logs.fileline() + ' : RecordDet ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # Update Record
        if id_pat != 0:
            self.log.error(Logs.fileline() + ' : DEBUG RecordDet update')

            Record = Record.getRecord(id_pat)

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
            res['id_pat'] = id_pat

        # Insert new Record
        else:
            self.log.error(Logs.fileline() + ' : DEBUG RecordDet insert')

            args['ddn'] = datetime.strptime(args['ddn'], Constants.cst_isodate)

            ret = Record.insertRecord(id_owner=args['id_owner'],
                                        anonyme=args['anonyme'],
                                        code=args['code'],
                                        code_Record=args['code_Record'],
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
                self.log.error(Logs.alert() + ' : RecordDet ERROR  insert')
                return compose_ret('', Constants.cst_content_type_json, 500)

            res = {}
            res['id_pat'] = ret

            # Get id_group of lab with id_group of user
            id_group_lab = User.getUserGroupParent(args['id_owner'])

            if not id_group_lab:
                self.log.error(Logs.fileline() + ' : RecordDet ERROR group not found')
                return compose_ret('', Constants.cst_content_type_json, 500)

            # insert sigl_03_data_group
            ret = Record.insertRecordGroup(id_data=res['id_pat'],
                                             id_group=id_group_lab['id_group_parent'])

            if ret <= 0:
                self.log.error(Logs.alert() + ' : RecordDet ERROR  insert group')
                return compose_ret('', Constants.cst_content_type_json, 500)


        self.log.info(Logs.fileline() + ' : TRACE RecordDet id_pat=' + str(res['id_pat']))
        return compose_ret(res, Constants.cst_content_type_json)


class RecordTypeProd(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_type_prod):
        type_prod = Record.getProductType(id_type_prod)

        if not type_prod:
            self.log.error(Logs.fileline() + ' : ' + 'RecordTypeProd ERROR not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        # Replace None by empty string
        for key, value in type_prod.items():
            if type_prod[key] is None:
                type_prod[key] = ''

        self.log.info(Logs.fileline() + ' : RecordtypeProd id_type_prod' + str(id_type_prod))
        return compose_ret(type_prod, Constants.cst_content_type_json, 200)
"""
