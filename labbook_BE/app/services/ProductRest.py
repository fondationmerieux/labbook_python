# -*- coding:utf-8 -*-
import logging

from datetime import datetime
from flask import request
from flask_restful import Resource

from app.models.General import compose_ret
from app.models.Constants import *
from app.models.Product import *
from app.models.User import *
from app.models.Logs import Logs

"""
class ProductSearch(Resource):
    log = logging.getLogger('log_services')

    def post(self, id_group):
        args = request.get_json()

        id_lab = User.getUserGroupParent(id_group)

        l_analysis = Product.getProductSearch(args['term'], id_lab['id_group_parent'], id_group)

        if not l_analysis:
            self.log.error(Logs.fileline() + ' : TRACE ProductSearch not found')

        self.log.info(Logs.fileline() + ' : TRACE ProductSearch')
        return compose_ret(l_analysis, Constants.cst_content_type_json)


class ProductDet(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_ana):
        analysis = Product.getProduct(id_ana)

        if not analysis:
            self.log.error(Logs.fileline() + ' : ' + 'ProductDet ERROR not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        # Replace None by empty string
        for key, value in analysis.items():
            if analysis[key] is None:
                analysis[key] = ''

        self.log.info(Logs.fileline() + ' : ProductDet id_data=' + str(id_ana))
        return compose_ret(analysis, Constants.cst_content_type_json, 200)

    def post(self, id_group, id_rec=0):
        args = request.get_json()

        if 'id_owner' not in args or 'anonyme' not in args or 'code' not in args or 'code_analysis' not in args or 'nom' not in args or \
           'prenom' not in args or 'ddn' not in args or 'sexe' not in args or 'ethnie' not in args or 'adresse' not in args or \
           'cp' not in args or 'ville' not in args or 'tel' not in args or 'profession' not in args or 'nom_jf' not in args or \
           'quartier' not in args or 'bp' not in args or 'ddn_approx' not in args or 'age' not in args or 'annee_naiss' not in args or \
           'semaine_naiss' not in args or 'mois_naiss' not in args or 'unite' not in args:
            self.log.error(Logs.fileline() + ' : ProductDet ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # Update analysis
        if id_rec != 0:
            self.log.error(Logs.fileline() + ' : DEBUG ProductDet update')

            analysis = Product.getProduct(id_rec)

            if not analysis:
                self.log.error(Logs.fileline() + ' : ProductDet ERROR not found')
                return compose_ret('', Constants.cst_content_type_json, 500)

            ret = Product.updateProduct(id=id_pat,
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
                self.log.error(Logs.alert() + ' : ProductDet ERROR update')
                return compose_ret('', Constants.cst_content_type_json, 500)

            res = {}
            res['id_pat'] = id_pat

        # Insert new analysis
        else:
            self.log.error(Logs.fileline() + ' : DEBUG ProductDet insert')

            args['ddn'] = datetime.strptime(args['ddn'], Constants.cst_isodate)

            ret = Product.insertProduct(id_owner=args['id_owner'],
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
                self.log.error(Logs.alert() + ' : ProductDet ERROR  insert')
                return compose_ret('', Constants.cst_content_type_json, 500)

            res = {}
            res['id_rec'] = ret

            # Get id_group of lab with id_group of user
            id_group_lab = User.getUserGroupParent(args['id_owner'])

            if not id_group_lab:
                self.log.error(Logs.fileline() + ' : ProductDet ERROR group not found')
                return compose_ret('', Constants.cst_content_type_json, 500)

            # insert sigl_03_data_group
            ret = Product.insertProductGroup(id_data=res['id_pat'],
                                             id_group=id_group_lab['id_group_parent'])

            if ret <= 0:
                self.log.error(Logs.alert() + ' : ProductDet ERROR  insert group')
                return compose_ret('', Constants.cst_content_type_json, 500)


        self.log.info(Logs.fileline() + ' : TRACE ProductDet id_pat=' + str(res['id_pat']))
        return compose_ret(res, Constants.cst_content_type_json)


class ProductTypeProd(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_type_prod):
        type_prod = Product.getProductType(id_type_prod)

        if not type_prod:
            self.log.error(Logs.fileline() + ' : ' + 'ProductTypeProd ERROR not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        # Replace None by empty string
        for key, value in type_prod.items():
            if type_prod[key] is None:
                type_prod[key] = ''

        self.log.info(Logs.fileline() + ' : ProducttypeProd id_type_prod' + str(id_type_prod))
        return compose_ret(type_prod, Constants.cst_content_type_json, 200)"""


class ProductReq(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_rec):
        l_prod = Product.getProductReq(id_rec)

        if not l_prod:
            self.log.error(Logs.fileline() + ' : ' + 'AnalysisReq ERROR not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        for prod in l_prod:
            # Replace None by empty string
            for key, value in prod.items():
                if prod[key] is None:
                    prod[key] = ''

            if prod['date_prel']:
                prod['date_prel'] = datetime.strftime(prod['date_prel'], '%Y-%m-%d')

            if prod['date_reception']
                prod['date_reception'] = datetime.strftime(prod['date_reception'], '%Y-%m-%d')

            # TODO format time heure_reception ?
            prod['heure_reception']= ''

        self.log.info(Logs.fileline() + ' : ProductReq id_rec=' + str(id_rec))
        return compose_ret(l_prod, Constants.cst_content_type_json, 200)

    def post(self):
        args = request.get_json()

        if 'list_prod' not in args:
            self.log.error(Logs.fileline() + ' : ProductReq ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # Loop on list_prod
        for prod in args['list_prod']:
            self.log.error(Logs.fileline() + ' : DEBUG ProductReq insert')

            if 'id_owner' not in prod or 'date_samp' not in prod or 'type_samp' not in prod or 'qty' not in prod or 'stat' not in prod or \
               'id_rec' not in prod or 'sampler' not in prod or 'date_receipt' not in prod or 'time_receipt' not in prod or \
               'comm' not in prod or 'locat_samp' not in prod or 'locat_samp_more' not in prod or 'location' not in prod:
                self.log.error(Logs.fileline() + ' : ProductReq ERROR prod missing')
                return compose_ret('', Constants.cst_content_type_json, 400)

            if prod['date_samp']:
                prod['date_samp'] = datetime.strptime(prod['date_samp'], Constants.cst_isodate)

            if prod['date_receipt']:
                prod['date_receipt'] = datetime.strptime(prod['date_receipt'], Constants.cst_isodate)

            ret = Product.insertProductReq(id_owner=prod['id_owner'],
                                           date_prel=prod['date_samp'],
                                           type_prel=prod['type_samp'],
                                           quantite=prod['qty'],
                                           statut=prod['stat'],
                                           id_dos=prod['id_rec'],
                                           preleveur=prod['sampler'],
                                           date_reception=prod['date_receipt'],
                                           heure_reception=prod['time_receipt'],
                                           commentaire=prod['comm'],
                                           lieu_prel=prod['locat_samp'],
                                           lieu_prel_plus=prod['locat_samp_more'],
                                           localisation=prod['location'])

            if ret <= 0:
                self.log.error(Logs.alert() + ' : ProductReq ERROR  insert')
                return compose_ret('', Constants.cst_content_type_json, 500)

            res = {}
            res['id_req'] = ret

            # Get id_group of lab with id_group of user
            id_group_lab = User.getUserGroupParent(prod['id_owner'])

            if not id_group_lab:
                self.log.error(Logs.fileline() + ' : ProductReq ERROR group not found')
                return compose_ret('', Constants.cst_content_type_json, 500)

            # insert sigl_01_data_group
            ret = Product.insertProductReqGroup(id_data=res['id_req'],
                                                id_group=id_group_lab['id_group_parent'])

            if ret <= 0:
                self.log.error(Logs.alert() + ' : ProductReq ERROR  insert group')
                return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE ProductReq')
        return compose_ret('', Constants.cst_content_type_json)
