# -*- coding:utf-8 -*-
import logging

from datetime import datetime
from flask import request
from flask_restful import Resource

from app.models.General import compose_ret
from app.models.Constants import *
from app.models.Analysis import *
from app.models.User import *
from app.models.Logs import Logs


class AnalysisSearch(Resource):
    log = logging.getLogger('log_service')

    def post(self, id_group):
        args = request.get_json()

        id_lab = User.getUserGroupParent(id_group)

        l_analysis = Analysis.getAnalysisSearch(args['term'], id_lab['id_group_parent'], id_group)

        if not l_analysis:
            self.log.error(Logs.fileline() + ' : TRACE AnalysisSearch not found')

        self.log.info(Logs.fileline() + ' : TRACE AnalysisSearch')
        return compose_ret(l_analysis, Constants.cst_content_type_json)


class AnalysisDet(Resource):
    log = logging.getLogger('log_service')

    def get(self, id_ana):
        analysis = Analysis.getAnalysis(id_ana)

        if not analysis:
            self.log.error(Logs.fileline() + ' : ' + 'AnalysisDet ERROR not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        # Replace None by empty string
        for key, value in analysis.items():
            if analysis[key] is None:
                analysis[key] = ''

        self.log.info(Logs.fileline() + ' : AnalysisDet id_data=' + str(id_ana))
        return compose_ret(analysis, Constants.cst_content_type_json, 200)

"""
    def post(self, id_pat=0):
        args = request.get_json()

        if 'id_owner' not in args or 'anonyme' not in args or 'code' not in args or 'code_analysis' not in args or 'nom' not in args or \
           'prenom' not in args or 'ddn' not in args or 'sexe' not in args or 'ethnie' not in args or 'adresse' not in args or \
           'cp' not in args or 'ville' not in args or 'tel' not in args or 'profession' not in args or 'nom_jf' not in args or \
           'quartier' not in args or 'bp' not in args or 'ddn_approx' not in args or 'age' not in args or 'annee_naiss' not in args or \
           'semaine_naiss' not in args or 'mois_naiss' not in args or 'unite' not in args:
            self.log.error(Logs.fileline() + ' : AnalysisDet ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # Update analysis
        if id_pat != 0:
            self.log.error(Logs.fileline() + ' : DEBUG AnalysisDet update')

            analysis = Analysis.getAnalysis(id_pat)

            if not analysis:
                self.log.error(Logs.fileline() + ' : AnalysisDet ERROR not found')
                return compose_ret('', Constants.cst_content_type_json, 500)

            ret = Analysis.updateAnalysis(id=id_pat,
                                        id_owner=args['id_owner'],
                                        anonyme=args['anonyme'],
                                        code=args['code'],
                                        code_analysis=args['code_analysis'],
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
                self.log.error(Logs.alerte() + ' : AnalysisDet ERROR update')
                return compose_ret('', Constants.cst_content_type_json, 500)

            res = {}
            res['id_pat'] = id_pat

        # Insert new analysis
        else:
            self.log.error(Logs.fileline() + ' : DEBUG AnalysisDet insert')

            args['ddn'] = datetime.strptime(args['ddn'], Constants.cst_isodate)

            ret = Analysis.insertAnalysis(id_owner=args['id_owner'],
                                        anonyme=args['anonyme'],
                                        code=args['code'],
                                        code_analysis=args['code_analysis'],
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
                self.log.error(Logs.alerte() + ' : AnalysisDet ERROR  insert')
                return compose_ret('', Constants.cst_content_type_json, 500)

            res = {}
            res['id_pat'] = ret

            # Get id_group of lab with id_group of user
            id_group_lab = User.getUserGroupParent(args['id_owner'])

            if not id_group_lab:
                self.log.error(Logs.fileline() + ' : AnalysisDet ERROR group not found')
                return compose_ret('', Constants.cst_content_type_json, 500)

            # insert sigl_03_data_group
            ret = Analysis.insertAnalysisGroup(id_data=res['id_pat'],
                                             id_group=id_group_lab['id_group_parent'])

            if ret <= 0:
                self.log.error(Logs.alerte() + ' : AnalysisDet ERROR  insert group')
                return compose_ret('', Constants.cst_content_type_json, 500)


        self.log.info(Logs.fileline() + ' : TRACE AnalysisDet id_pat=' + str(res['id_pat']))
        return compose_ret(res, Constants.cst_content_type_json)"""


class AnalysisTypeProd(Resource):
    log = logging.getLogger('log_service')

    def get(self, id_type_prod):
        type_prod = Analysis.getProductType(id_type_prod)

        if not type_prod:
            self.log.error(Logs.fileline() + ' : ' + 'AnalysisTypeProd ERROR not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        # Replace None by empty string
        for key, value in type_prod.items():
            if type_prod[key] is None:
                type_prod[key] = ''

        self.log.info(Logs.fileline() + ' : AnalysistypeProd id_type_prod' + str(id_type_prod))
        return compose_ret(type_prod, Constants.cst_content_type_json, 200)
