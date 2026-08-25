# -*- coding:utf-8 -*-
import logging
import shlex
import subprocess  # nosec B404
import os

from datetime import datetime
from flask import request
from flask_restful import Resource

from app.models.General import compose_ret
from app.models.Audit import Audit
from app.models.Analyzer import Analyzer
from app.models.Constants import Constants
from app.models.Product import Product
from app.models.Setting import Setting
from app.models.Logs import Logs
from app.models.Various import Various
from app.security.oauth_routes import require_oauth


class ProductDet(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self, id_prod):
        audit_user = request.oauth_user
        prod = Product.getProductDet(id_prod)

        if not prod:
            self.log.error(Logs.fileline() + ' : TRACE ProductDet not found')
            try:
                details = {"reason": "NOT_FOUND", "id_prod": int(id_prod)}
                Audit.insertAudit(audit_user, "ProductDet", "PRODUCT", int(id_prod), "ERROR", details, "R")
            except Exception as err:
                self.log.error(Logs.fileline() + ' : ProductDet ERROR audit not found err=' + str(err))
            return compose_ret('', Constants.cst_content_type_json, 404)

        for key, value in list(prod.items()):
            if prod[key] is None:
                prod[key] = ''

        if prod['prod_date']:
            prod['prod_date'] = datetime.strftime(prod['prod_date'], Constants.cst_dt_HM)

        if prod['receipt_date']:
            prod['receipt_date'] = datetime.strftime(prod['receipt_date'], Constants.cst_dt_HM)

        self.log.info(Logs.fileline() + ' : TRACE ProductDet ' + str(id_prod))
        try:
            details = {"result": "SUCCESS", "id_prod": int(id_prod)}
            Audit.insertAudit(audit_user, "ProductDet", "PRODUCT", int(id_prod), "SUCCESS", details, "R")
        except Exception as err:
            self.log.error(Logs.fileline() + ' : ProductDet ERROR audit success err=' + str(err))
        return compose_ret(prod, Constants.cst_content_type_json)

    @require_oauth()
    def post(self, id_prod):
        audit_user = request.oauth_user
        args = request.get_json()

        if 'stat' not in args or 'type' not in args or 'storage' not in args or 'ana' not in args or \
           'prod_date' not in args or 'sampler' not in args or 'location' not in args or \
           'location_accu' not in args or 'receipt_date' not in args or \
           'comment' not in args or 'code' not in args:
            self.log.error(Logs.fileline() + ' : ProductDet ERROR args missing')
            try:
                details = {"result": "ERROR", "reason": "ARGS_MISSING", "id_prod": int(id_prod)}
                Audit.insertAudit(audit_user, "ProductDet", "PRODUCT", int(id_prod) if int(id_prod) > 0 else None, "ERROR", details, "U")
            except Exception as err:
                self.log.error(Logs.fileline() + ' : ProductDet ERROR audit args missing err=' + str(err))
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
                try:
                    details = {"result": "ERROR", "reason": "UPDATE_FAILED", "id_prod": int(id_prod)}
                    Audit.insertAudit(audit_user, "ProductDet", "PRODUCT", int(id_prod), "ERROR", details, "U")
                except Exception as err:
                    self.log.error(Logs.fileline() + ' : ProductDet ERROR audit update failed err=' + str(err))
                return compose_ret('', Constants.cst_content_type_json, 500)

        else:
            if 'id_owner' not in args:
                self.log.error(Logs.fileline() + ' : ProductDet ERROR args missing')
                try:
                    details = {"reason": "ARGS_MISSING", "missing": ["id_owner"]}
                    Audit.insertAudit(audit_user, "ProductDet", "PRODUCT", None, "ERROR", details, "C")
                except Exception as err:
                    self.log.error(Logs.fileline() + ' : ProductDet ERROR audit err=' + str(err))
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
                try:
                    details = {"reason": "INSERT_FAILED", "id_owner": args.get('id_owner')}
                    Audit.insertAudit(audit_user, "ProductDet", "PRODUCT", None, "ERROR", details, "C")
                except Exception as err:
                    self.log.error(Logs.fileline() + ' : ProductDet ERROR audit err=' + str(err))
                return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE ProductDet')
        try:
            details = {"id_prod": int(id_prod) if int(id_prod) > 0 else int(ret)}
            Audit.insertAudit(audit_user, "ProductDet", "PRODUCT",
                              int(id_prod) if int(id_prod) > 0 else int(ret), "SUCCESS", details,
                              "U" if int(id_prod) > 0 else "C")
        except Exception as err:
            self.log.error(Logs.fileline() + ' : ProductDet ERROR audit success err=' + str(err))
        return compose_ret('', Constants.cst_content_type_json)


class ProductList(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        l_products = Product.getProductList(args)

        if not l_products:
            self.log.error(Logs.fileline() + ' : TRACE ProductList not found')

        self.log.info(Logs.fileline() + ' : TRACE ProductList')
        try:
            details = {"result": "SUCCESS", "filters": args, "count": len(l_products) if l_products else 0}
            Audit.insertAudit(audit_user, "ProductList", "PRODUCT", None, "SUCCESS", details, "R")
        except Exception as err:
            self.log.error(Logs.fileline() + ' : ProductList ERROR audit success err=' + str(err))
        return compose_ret(l_products, Constants.cst_content_type_json)


class ProductReq(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self, id_rec):
        audit_user = request.oauth_user
        l_prod = Product.getProductReq(id_rec)

        if not l_prod:
            self.log.error(Logs.fileline() + ' : ' + 'AnalysisReq ERROR not found')
            try:
                details = {"reason": "NOT_FOUND", "id_rec": int(id_rec)}
                Audit.insertAudit(audit_user, "ProductReq", "RECORD", int(id_rec), "ERROR", details, "R")
            except Exception as err:
                self.log.error(Logs.fileline() + ' : ProductReq ERROR audit err=' + str(err))
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
        try:
            details = {"id_rec": int(id_rec), "count": len(l_prod)}
            Audit.insertAudit(audit_user, "ProductReq", "PRODUCT", int(id_rec), "SUCCESS", details, "R")
        except Exception as err:
            self.log.error(Logs.fileline() + ' : ProductReq ERROR audit success err=' + str(err))
        return compose_ret(l_prod, Constants.cst_content_type_json, 200)

    @require_oauth()
    def post(self):
        audit_user = request.oauth_user
        args = request.get_json()

        if 'list_prod' not in args:
            self.log.error(Logs.fileline() + ' : ProductReq ERROR args missing')
            try:
                details = {"reason": "ARGS_MISSING", "missing": ["list_prod"]}
                Audit.insertAudit(audit_user, "ProductReq", "PRODUCT", None, "ERROR", details, "C")
            except Exception as err:
                self.log.error(Logs.fileline() + ' : ProductReq ERROR audit err=' + str(err))
            return compose_ret('', Constants.cst_content_type_json, 400)

        # Check if an analyzer is configured
        l_analyzer = Analyzer.getAnalyzerList()
        has_batch_analyzer = any(
            analyzer.get('ans_batch') == 'Y'
            for analyzer in (l_analyzer or [])
        )

        # Loop on list_prod
        for prod in args['list_prod']:
            if 'id_owner' not in prod or 'date_samp' not in prod or 'type_samp' not in prod or 'ana' not in prod or \
               'stat' not in prod or 'id_rec' not in prod or 'sampler' not in prod or 'date_receipt' not in prod or \
               'time_receipt' not in prod or 'comm' not in prod or 'locat_samp' not in prod or \
               'locat_samp_more' not in prod or 'location' not in prod or 'code' not in prod:
                self.log.error(Logs.fileline() + ' : ProductReq ERROR prod missing')
                try:
                    details = {"reason": "PROD_MISSING_FIELDS"}
                    Audit.insertAudit(audit_user, "ProductReq", "PRODUCT", None, "ERROR", details, "C")
                except Exception as err:
                    self.log.error(Logs.fileline() + ' : ProductReq ERROR audit err=' + str(err))
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
                try:
                    details = {"reason": "INSERT_FAILED", "id_rec": prod.get("id_rec"), "id_owner": prod.get("id_owner")}
                    Audit.insertAudit(audit_user, "ProductReq", "PRODUCT", None, "ERROR", details, "C")
                except Exception as err:
                    self.log.error(Logs.fileline() + ' : ProductReq ERROR audit err=' + str(err))
                return compose_ret('', Constants.cst_content_type_json, 500)

            res = {}
            res['id_req'] = ret

            # prepare task and run script for analyzer
            if has_batch_analyzer:
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
        try:
            details = {"count": len(args.get("list_prod") or [])}
            Audit.insertAudit(audit_user, "ProductReq", "PRODUCT", None, "SUCCESS", details, "C")
        except Exception as err:
            self.log.error(Logs.fileline() + ' : ProductReq ERROR audit success err=' + str(err))
        return compose_ret('', Constants.cst_content_type_json)


class ProductLastCode(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self):
        audit_user = request.oauth_user
        last_code = ''

        try:
            rstg = Setting.getRecNumSetting() or {}
            samp_regex = rstg.get('rstg_samp_regex') if isinstance(rstg, dict) else ''
            samp_regex = (samp_regex or '').strip()

            # No regex => no format => no prefill
            if samp_regex:
                last_code = Product.getLastSampleCode(samp_regex)
            else:
                last_code = ''

        except Exception as err:
            last_code = ''
            self.log.error(Logs.fileline() + ' : ProductLastCode ERROR read setting err=' + str(err))

        body = {'last_code': last_code}

        self.log.info(Logs.fileline() + ' : TRACE ProductLastCode')

        try:
            details = {"last_code": last_code}
            Audit.insertAudit(audit_user, "ProductLastCode", "PRODUCT", None, "SUCCESS", details, "R")
        except Exception as err:
            self.log.error(Logs.fileline() + ' : ProductLastCode ERROR audit success err=' + str(err))

        return compose_ret(body, Constants.cst_content_type_json)


class ProductCheckCode(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        if 'codes' not in args or not isinstance(args['codes'], list):
            self.log.error(Logs.fileline() + ' : ProductCheckCode ERROR args missing or invalid')
            try:
                details = {"reason": "ARGS_MISSING_OR_INVALID"}
                Audit.insertAudit(audit_user, "ProductCheckCode", "PRODUCT", None, "ERROR", details, "R")
            except Exception as err:
                self.log.error(Logs.fileline() + ' : ProductCheckCode ERROR audit err=' + str(err))
            return compose_ret('', Constants.cst_content_type_json, 400)

        raw_codes = args['codes'] or []
        codes = []

        for c in raw_codes:
            if c is None:
                continue
            val = str(c).strip()
            if val:
                codes.append(val)

        existing = Product.getExistingSampleCodes(codes)
        body = {'existing_codes': list(existing)}

        self.log.info(Logs.fileline() + ' : TRACE ProductCheckCode')
        try:
            details = {"count_in": len(codes), "count_existing": len(body['existing_codes'])}
            Audit.insertAudit(audit_user, "ProductCheckCode", "PRODUCT", None, "SUCCESS", details, "R")
        except Exception as err:
            self.log.error(Logs.fileline() + ' : ProductCheckCode ERROR audit success err=' + str(err))
        return compose_ret(body, Constants.cst_content_type_json)
