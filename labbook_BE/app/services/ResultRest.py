# -*- coding:utf-8 -*-
import logging

from datetime import datetime
from flask import request
from flask_restful import Resource

from app.models.General import compose_ret
from app.models.Constants import *
from app.models.Various import *
from app.models.Result import *
from app.models.Analysis import *
from app.models.User import *
from app.models.Logs import Logs


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
            if result['date_prescr']:
                result['date_prescr'] = datetime.strftime(result['date_prescr'], '%Y-%m-%d')

            # Get result answer
            type_res             = ''
            result['unit']       = ''
            result['res_answer'] = []

            # get unit label
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
                result['res_answer'] = Various.getDicoList(str(type_res))

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
            # Replace None by empty string
            for key, value in result.items():
                if result[key] is None:
                    result[key] = ''

            if result['date_prescr']:
                    result['date_prescr'] = datetime.strftime(result['date_prescr'], '%Y-%m-%d')

        self.log.info(Logs.fileline() + ' : ResultRecord id_rec=' + str(id_rec))
        return compose_ret(l_results, Constants.cst_content_type_json, 200)

    """
    def post(self, id_pat=0):
        args = request.get_json()

        if 'id_owner' not in args or 'anonyme' not in args or 'code' not in args or 'code_Result' not in args or 'nom' not in args or \
           'prenom' not in args or 'ddn' not in args or 'sexe' not in args or 'ethnie' not in args or 'adresse' not in args or \
           'cp' not in args or 'ville' not in args or 'tel' not in args or 'profession' not in args or 'nom_jf' not in args or \
           'quartier' not in args or 'bp' not in args or 'ddn_approx' not in args or 'age' not in args or 'annee_naiss' not in args or \
           'semaine_naiss' not in args or 'mois_naiss' not in args or 'unite' not in args:
            self.log.error(Logs.fileline() + ' : ResultDet ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # Update Result
        if id_pat != 0:
            self.log.error(Logs.fileline() + ' : DEBUG ResultDet update')

            Result = Result.getResult(id_pat)

            if not Result:
                self.log.error(Logs.fileline() + ' : ResultDet ERROR not found')
                return compose_ret('', Constants.cst_content_type_json, 500)

            ret = Result.updateResult(id=id_pat,
                                        id_owner=args['id_owner'],
                                        anonyme=args['anonyme'],
                                        code=args['code'],
                                        code_Result=args['code_Result'],
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
                self.log.error(Logs.alert() + ' : ResultDet ERROR update')
                return compose_ret('', Constants.cst_content_type_json, 500)

            res = {}
            res['id_pat'] = id_pat

        # Insert new Result
        else:
            self.log.error(Logs.fileline() + ' : DEBUG ResultDet insert')

            args['ddn'] = datetime.strptime(args['ddn'], Constants.cst_isodate)

            ret = Result.insertResult(id_owner=args['id_owner'],
                                        anonyme=args['anonyme'],
                                        code=args['code'],
                                        code_Result=args['code_Result'],
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
                self.log.error(Logs.alert() + ' : ResultDet ERROR  insert')
                return compose_ret('', Constants.cst_content_type_json, 500)

            res = {}
            res['id_pat'] = ret

            # Get id_group of lab with id_group of user
            id_group_lab = User.getUserGroupParent(args['id_owner'])

            if not id_group_lab:
                self.log.error(Logs.fileline() + ' : ResultDet ERROR group not found')
                return compose_ret('', Constants.cst_content_type_json, 500)

            # insert sigl_03_data_group
            ret = Result.insertResultGroup(id_data=res['id_pat'],
                                             id_group=id_group_lab['id_group_parent'])

            if ret <= 0:
                self.log.error(Logs.alert() + ' : ResultDet ERROR  insert group')
                return compose_ret('', Constants.cst_content_type_json, 500)


        self.log.info(Logs.fileline() + ' : TRACE ResultDet id_pat=' + str(res['id_pat']))
        return compose_ret(res, Constants.cst_content_type_json)


class ResultTypeProd(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_type_prod):
        type_prod = Result.getProductType(id_type_prod)

        if not type_prod:
            self.log.error(Logs.fileline() + ' : ' + 'ResultTypeProd ERROR not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        # Replace None by empty string
        for key, value in type_prod.items():
            if type_prod[key] is None:
                type_prod[key] = ''

        self.log.info(Logs.fileline() + ' : ResulttypeProd id_type_prod' + str(id_type_prod))
        return compose_ret(type_prod, Constants.cst_content_type_json, 200)
"""


class ResultCreate(Resource):
    log = logging.getLogger('log_services')

    """
    def get(self, id_rec, bio_prod='O'):
        l_res = Result.getResultCreate(id_rec, bio_prod)

        if not l_res:
            self.log.error(Logs.fileline() + ' : ' + 'ResultCreate ERROR not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        for analysis in l_res:
            # Replace None by empty string
            for key, value in analysis.items():
                if analysis[key] is None:
                    analysis[key] = ''

            analysis['prix'] = float(analysis['prix'])

        self.log.info(Logs.fileline() + ' : ResultCreate id_rec=' + str(id_rec))
        return compose_ret(l_res, Constants.cst_content_type_json, 200)"""

    def post(self, id_rec):
        args = request.get_json()

        if 'id_owner' not in args or 'user_role' not in args:
            self.log.error(Logs.fileline() + ' : ResultCreate ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        if args['user_role'] == 'secretaire':
            type_validation = 250
        elif args['user_role'] == 'technicien':
            type_validation = 251
        elif args['user_role'] == 'biologiste':
            type_validation = 252
        else:
            type_validation = 250

        # get list of all analysis (even samples)
        l_ana = Analysis.getAnalysisReq(id_rec, 'A')

        if not l_ana:
            self.log.error(Logs.fileline() + ' : ' + 'ResultCreate ERROR l_ana not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        # Loop on list_ana
        for ana in l_ana:

            ref = Analysis.getRefVariable(ana['id_data'])

            if ref and ref['id_refvariable']:
                ret = Result.insertResult(id_owner=args['id_owner'],
                                          id_analyse=ref['id_refanalyse'],
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
                                              utilisateur=args['id_owner'],
                                              type_validation=type_validation)

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
