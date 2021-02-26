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


class ProductDet(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_prod):
        prod = Product.getProductDet(id_prod)

        if not prod:
            self.log.error(Logs.fileline() + ' : TRACE ProductDet not found')

        for key, value in prod.items():
            if prod[key] is None:
                prod[key] = ''

        if prod['prod_date']:
            prod['prod_date'] = datetime.strftime(prod['prod_date'], '%Y-%m-%d')

        if prod['receipt_date']:
            prod['receipt_date'] = datetime.strftime(prod['receipt_date'], '%Y-%m-%d')

        self.log.info(Logs.fileline() + ' : TRACE ProductDet ' + str(id_prod))
        return compose_ret(prod, Constants.cst_content_type_json)

    def post(self, id_prod):
        args = request.get_json()

        if 'stat' not in args or 'type' not in args or 'storage' not in args or 'qty' not in args or \
           'prod_date' not in args or 'sampler' not in args or 'location' not in args or \
           'location_accu' not in args or 'receipt_date' not in args or 'receipt_time' not in args or \
           'comment' not in args:
            self.log.error(Logs.fileline() + ' : ProductDet ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        if id_prod > 0:

            ret = Product.updateProduct(id_data=id_prod,
                                        date_prel=args['prod_date'],
                                        type_prel=args['type'],
                                        quantite=args['qty'],
                                        statut=args['stat'],
                                        id_dos=args['id_rec'],
                                        preleveur=args['sampler'],
                                        date_reception=args['receipt_date'],
                                        heure_reception=args['receipt_time'],
                                        commentaire=args['comment'],
                                        lieu_prel=args['location'],
                                        lieu_prel_plus=args['location_accu'],
                                        localisation=args['storage'])

            if ret is False:
                self.log.info(Logs.fileline() + ' : TRACE ProductDet ERROR update product')
                return compose_ret('', Constants.cst_content_type_json, 500)

        else:
            if 'id_owner' not in args:
                self.log.error(Logs.fileline() + ' : ProductDet ERROR args missing')
                return compose_ret('', Constants.cst_content_type_json, 400)

            ret = Product.insertProductReq(id_owner=args['id_owner'],
                                           date_prel=args['prod_date'],
                                           type_prel=args['type'],
                                           quantite=args['qty'],
                                           statut=args['stat'],
                                           id_dos=args['id_rec'],
                                           preleveur=args['sampler'],
                                           date_reception=args['receipt_date'],
                                           heure_reception=args['receipt_time'],
                                           commentaire=args['comment'],
                                           lieu_prel=args['location'],
                                           lieu_prel_plus=args['location_accu'],
                                           localisation=args['storage'])

            if ret <= 0:
                self.log.error(Logs.alert() + ' : ProductDet ERROR insert product')
                return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE ProductDet')
        return compose_ret('', Constants.cst_content_type_json)


class ProductList(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        if not args:
            args = {}

        l_products = Product.getProductList(args)

        if not l_products:
            self.log.error(Logs.fileline() + ' : TRACE ProductList not found')

        self.log.info(Logs.fileline() + ' : TRACE ProductList')
        return compose_ret(l_products, Constants.cst_content_type_json)


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

            if prod['date_reception']:
                prod['date_reception'] = datetime.strftime(prod['date_reception'], '%Y-%m-%d')

            # TODO format time heure_reception ?
            prod['heure_reception'] = ''

        self.log.info(Logs.fileline() + ' : ProductReq id_rec=' + str(id_rec))
        return compose_ret(l_prod, Constants.cst_content_type_json, 200)

    def post(self):
        args = request.get_json()

        if 'list_prod' not in args:
            self.log.error(Logs.fileline() + ' : ProductReq ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # Loop on list_prod
        for prod in args['list_prod']:
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
