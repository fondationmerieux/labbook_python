# -*- coding:utf-8 -*-
import logging
import gettext
import shlex
import subprocess  # nosec B404
import os

from datetime import datetime
from flask import request
from flask_restful import Resource

from app.models.General import compose_ret
from app.models.Analyzer import Analyzer
from app.models.Constants import *
from app.models.Product import *
from app.models.User import *
from app.models.Logs import Logs
from app.models.Various import Various


class ProductDet(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_prod):
        prod = Product.getProductDet(id_prod)

        if not prod:
            self.log.error(Logs.fileline() + ' : TRACE ProductDet not found')

        for key, value in list(prod.items()):
            if prod[key] is None:
                prod[key] = ''

        if prod['prod_date']:
            prod['prod_date'] = datetime.strftime(prod['prod_date'], Constants.cst_dt_HM)

        if prod['receipt_date']:
            prod['receipt_date'] = datetime.strftime(prod['receipt_date'], Constants.cst_dt_HM)

        self.log.info(Logs.fileline() + ' : TRACE ProductDet ' + str(id_prod))
        return compose_ret(prod, Constants.cst_content_type_json)

    def post(self, id_prod):
        args = request.get_json()

        if 'stat' not in args or 'type' not in args or 'storage' not in args or 'ana' not in args or \
           'prod_date' not in args or 'sampler' not in args or 'location' not in args or \
           'location_accu' not in args or 'receipt_date' not in args or \
           'comment' not in args or 'code' not in args:
            self.log.error(Logs.fileline() + ' : ProductDet ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        if id_prod > 0:

            ret = Product.updateProduct(id_data=id_prod,
                                        samp_date=args['prod_date'],
                                        type_prel=args['type'],
                                        samp_id_ana=args['ana'],
                                        statut=args['stat'],
                                        id_dos=args['id_rec'],
                                        preleveur=args['sampler'],
                                        samp_receipt_date=args['receipt_date'],
                                        commentaire=args['comment'],
                                        lieu_prel=args['location'],
                                        lieu_prel_plus=args['location_accu'],
                                        localisation=args['storage'],
                                        code=args['code'])

            if ret is False:
                self.log.info(Logs.fileline() + ' : TRACE ProductDet ERROR update product')
                return compose_ret('', Constants.cst_content_type_json, 500)

        else:
            if 'id_owner' not in args:
                self.log.error(Logs.fileline() + ' : ProductDet ERROR args missing')
                return compose_ret('', Constants.cst_content_type_json, 400)

            ret = Product.insertProductReq(id_owner=args['id_owner'],
                                           samp_date=args['prod_date'],
                                           type_prel=args['type'],
                                           samp_id_ana=args['ana'],
                                           statut=args['stat'],
                                           id_dos=args['id_rec'],
                                           preleveur=args['sampler'],
                                           samp_receipt_date=args['receipt_date'],
                                           commentaire=args['comment'],
                                           lieu_prel=args['location'],
                                           lieu_prel_plus=args['location_accu'],
                                           localisation=args['storage'],
                                           code=args['code'])

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

        Various.useLangDB()

        for prod in l_prod:
            # Replace None by empty string
            for key, value in list(prod.items()):
                if prod[key] is None:
                    prod[key] = ''
                elif key == 'type_prod' and prod[key]:
                    prod[key] = _(prod[key].strip())
                elif key == 'stat_prod' and prod[key]:
                    prod[key] = _(prod[key].strip())

            if prod['samp_date']:
                prod['samp_date'] = datetime.strftime(prod['samp_date'], Constants.cst_dt_HM)

            if prod['samp_receipt_date']:
                prod['samp_receipt_date'] = datetime.strftime(prod['samp_receipt_date'], Constants.cst_dt_HM)

        self.log.info(Logs.fileline() + ' : ProductReq id_rec=' + str(id_rec))
        return compose_ret(l_prod, Constants.cst_content_type_json, 200)

    def post(self):
        args = request.get_json()

        if 'list_prod' not in args:
            self.log.error(Logs.fileline() + ' : ProductReq ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # Check if an analyzer is configured
        l_analyzer = Analyzer.getAnalyzerList()

        # Loop on list_prod
        for prod in args['list_prod']:
            if 'id_owner' not in prod or 'date_samp' not in prod or 'type_samp' not in prod or 'ana' not in prod or \
               'stat' not in prod or 'id_rec' not in prod or 'sampler' not in prod or 'date_receipt' not in prod or \
               'time_receipt' not in prod or 'comm' not in prod or 'locat_samp' not in prod or \
               'locat_samp_more' not in prod or 'location' not in prod or 'code' not in prod:
                self.log.error(Logs.fileline() + ' : ProductReq ERROR prod missing')
                return compose_ret('', Constants.cst_content_type_json, 400)

            if prod['date_samp']:
                prod['date_samp'] = datetime.strptime(prod['date_samp'], Constants.cst_dt_ext_HM)

            if prod['date_receipt']:
                prod['date_receipt'] = datetime.strptime(prod['date_receipt'], Constants.cst_dt_ext_HM)

            ret = Product.insertProductReq(id_owner=prod['id_owner'],
                                           samp_date=prod['date_samp'],
                                           type_prel=prod['type_samp'],
                                           samp_id_ana=prod['ana'],
                                           statut=prod['stat'],
                                           id_dos=prod['id_rec'],
                                           preleveur=prod['sampler'],
                                           samp_receipt_date=prod['date_receipt'],
                                           commentaire=prod['comm'],
                                           lieu_prel=prod['locat_samp'],
                                           lieu_prel_plus=prod['locat_samp_more'],
                                           localisation=prod['location'],
                                           code=prod['code'])

            if ret <= 0:
                self.log.error(Logs.alert() + ' : ProductReq ERROR  insert')
                return compose_ret('', Constants.cst_content_type_json, 500)

            res = {}
            res['id_req'] = ret

            # prepare task and run script for analyzer
            if l_analyzer:
                Analyzer.log.info(Logs.fileline() + ' DEBUG prepare task LAB28 for id_req=' + str(res['id_req']))
                # prepare task to save for analyzer
                ret = Analyzer.buildLab28(res['id_req'])

                if ret:
                    # run script analyzer for LAB28 request
                    cmd = 'sh ' + Constants.cst_path_script + Constants.cst_script_analyzer
                    cmd_split = shlex.split(cmd)

                    out_file = Constants.cst_path_log + 'log_script_analyzer.log'
                    out_file = os.open(out_file, os.O_CREAT | os.O_APPEND)

                    self.log.info(Logs.fileline() + ' : RecordStat script analyzer cmd_split : ' + str(cmd_split))

                    subprocess.Popen(cmd_split, stdout=out_file, stderr=subprocess.STDOUT)  # nosec B603

        self.log.info(Logs.fileline() + ' : TRACE ProductReq')
        return compose_ret('', Constants.cst_content_type_json)
