# -*- coding:utf-8 -*-
import logging

from datetime import datetime
from flask import request
from flask_restful import Resource
from hl7apy.parser import parse_message
from hl7apy.core import Message
# from hl7apy.consts import VALIDATION_LEVEL

from app.models.General import compose_ret
from app.models.Constants import Constants
from app.models.Audit import Audit
from app.models.Analyzer import Analyzer
# from app.models.Record import Record
from app.models.Product import Product
# from app.models.User import User
# from app.models.DB import DB
from app.models.Logs import Logs
from app.security.oauth_routes import require_oauth


class ConnectSetting(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self):
        audit_user = request.oauth_user
        setting = Analyzer.getConnectSetting()

        if not setting:
            self.log.error(Logs.alert() + ' : ConnectSetting ERROR get')
            try:
                details = {"result": "ERROR", "reason": "GET_FAILED"}
                Audit.insertAudit(audit_user, "ConnectSetting", "DEVICE", None, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : ConnectSetting ERROR audit get')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE ConnectSetting')
        try:
            details = {"result": "SUCCESS"}
            Audit.insertAudit(audit_user, "ConnectSetting", "DEVICE", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : ConnectSetting ERROR audit success')
        return compose_ret(setting, Constants.cst_content_type_json)

    @require_oauth()
    def post(self):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        if 'id_user' not in args or 'url' not in args:
            self.log.error(Logs.fileline() + ' : ConnectSetting ERROR args missing')
            try:
                details = {"result": "ERROR", "reason": "ARGS_MISSING", "missing": ["id_user", "url"]}
                Audit.insertAudit(audit_user, "ConnectSetting", "DEVICE", None, "ERROR", details, "U")
            except Exception:
                self.log.exception(Logs.fileline() + ' : ConnectSetting ERROR audit args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        ret = Analyzer.updateConnectSetting(id_user=args['id_user'], url=args['url'])

        if ret is False:
            self.log.error(Logs.alert() + ' : ConnectSetting ERROR update')
            try:
                details = {"result": "ERROR", "reason": "UPDATE_FAILED", "id_user": args.get('id_user'), "url": args.get('url')}
                Audit.insertAudit(audit_user, "ConnectSetting", "DEVICE", None, "ERROR", details, "U")
            except Exception:
                self.log.exception(Logs.fileline() + ' : ConnectSetting ERROR audit update')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE ConnectSetting')
        try:
            details = {"result": "SUCCESS", "id_user": args.get('id_user'), "url": args.get('url')}
            Audit.insertAudit(audit_user, "ConnectSetting", "DEVICE", None, "SUCCESS", details, "U")
        except Exception:
            self.log.exception(Logs.fileline() + ' : ConnectSetting ERROR audit success')
        return compose_ret('', Constants.cst_content_type_json)


class AnalyzerList(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self):
        audit_user = request.oauth_user
        l_analyzers = Analyzer.getAnalyzerList()

        if not l_analyzers:
            self.log.info(Logs.fileline() + ' : TRACE AnalyzerList not found')

        self.log.info(Logs.fileline() + ' : TRACE AnalyzerList')
        try:
            details = {"result": "SUCCESS", "count": len(l_analyzers) if l_analyzers else 0}
            Audit.insertAudit(audit_user, "AnalyzerList", "DEVICE", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : AnalyzerList ERROR audit')
        return compose_ret(l_analyzers, Constants.cst_content_type_json)


class AnalyzerDet(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self, id_analyzer):
        audit_user = request.oauth_user
        item = Analyzer.getAnalyzerDet(id_analyzer)

        if not item:
            self.log.error(Logs.fileline() + ' : AnalyzerDet ERROR not found')
            try:
                details = {"result": "ERROR", "reason": "NOT_FOUND", "id_analyzer": id_analyzer}
                Audit.insertAudit(audit_user, "AnalyzerDet", "DEVICE", id_analyzer, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : AnalyzerDet ERROR audit not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        # Replace None by empty string
        for key, value in list(item.items()):
            if item[key] is None:
                item[key] = ''

        self.log.info(Logs.fileline() + ' : AnalyzerDet id_analyzer=' + str(id_analyzer))
        try:
            details = {"result": "SUCCESS", "id_analyzer": id_analyzer}
            Audit.insertAudit(audit_user, "AnalyzerDet", "DEVICE", id_analyzer, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : AnalyzerDet ERROR audit success')
        return compose_ret(item, Constants.cst_content_type_json, 200)

    @require_oauth()
    def post(self, id_analyzer):
        audit_user = request.oauth_user
        args = request.get_json()

        if 'id_user' not in args or 'rank' not in args or 'name' not in args or 'key' not in args or \
           'batch' not in args or 'filename' not in args:
            self.log.error(Logs.fileline() + ' : AnalyzerDet ERROR args missing')
            try:
                details = {"result": "ERROR", "reason": "ARGS_MISSING", "id_analyzer": id_analyzer}
                Audit.insertAudit(audit_user, "AnalyzerDet", "DEVICE", id_analyzer, "ERROR", details, "U")
            except Exception:
                self.log.exception(Logs.fileline() + ' : AnalyzerDet ERROR audit args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # Update item
        if id_analyzer > 0:
            self.log.info(Logs.fileline() + ' : TRACE update AnalyzerDet')

            ret = Analyzer.updateAnalyzerDet(id_analyzer=id_analyzer,
                                             id_user=args['id_user'],
                                             rank=args['rank'],
                                             name=args['name'],
                                             id=args['key'],
                                             batch=args['batch'],
                                             filename=args['filename'])

            if ret is False:
                self.log.error(Logs.alert() + ' : AnalyzerDet ERROR update')
                try:
                    details = {"result": "ERROR", "reason": "UPDATE_FAILED", "id_analyzer": id_analyzer, "id_user": args.get('id_user')}
                    Audit.insertAudit(audit_user, "AnalyzerDet", "DEVICE", id_analyzer, "ERROR", details, "U")
                except Exception:
                    self.log.exception(Logs.fileline() + ' : AnalyzerDet ERROR audit update')
                return compose_ret('', Constants.cst_content_type_json, 500)

        # Insert new item
        else:
            self.log.info(Logs.fileline() + ' : TRACE insert AnalyzerDet')
            ret = Analyzer.insertAnalyzerDet(id_user=args['id_user'],
                                             rank=args['rank'],
                                             name=args['name'],
                                             id=args['key'],
                                             batch=args['batch'],
                                             filename=args['filename'])

            if ret <= 0:
                self.log.error(Logs.alert() + ' : AnalyzerDet ERROR  insert')
                try:
                    details = {"result": "ERROR", "reason": "INSERT_FAILED", "id_analyzer": id_analyzer, "id_user": args.get('id_user')}
                    Audit.insertAudit(audit_user, "AnalyzerDet", "DEVICE", id_analyzer, "ERROR", details, "C")
                except Exception:
                    self.log.exception(Logs.fileline() + ' : AnalyzerDet ERROR audit insert')
                return compose_ret('', Constants.cst_content_type_json, 500)

            id_analyzer = ret

        self.log.info(Logs.fileline() + ' : TRACE AnalyzerDet id_analyzer=' + str(id_analyzer))
        try:
            details = {"result": "SUCCESS", "id_analyzer": id_analyzer, "id_user": args.get('id_user')}
            Audit.insertAudit(audit_user, "AnalyzerDet", "DEVICE", id_analyzer, "SUCCESS", details, "C")
        except Exception:
            self.log.exception(Logs.fileline() + ' : AnalyzerDet ERROR audit success')
        return compose_ret(id_analyzer, Constants.cst_content_type_json)

    @require_oauth()
    def delete(self, id_analyzer):
        audit_user = request.oauth_user
        args = request.get_json()

        if args and 'id_user' in args:
            self.log.error(Logs.fileline() + ' : TRACE AnalyzerDet delete by id_user=' + Logs.clean(args['id_user']))

        ret = Analyzer.deleteAnalyzer(id_analyzer)

        if not ret:
            self.log.error(Logs.fileline() + ' : TRACE AnalyzerDet delete ERROR')
            try:
                details = {"result": "ERROR", "reason": "DELETE_FAILED", "id_analyzer": id_analyzer, "id_user": args.get('id_user') if args else None}
                Audit.insertAudit(audit_user, "AnalyzerDet", "DEVICE", id_analyzer, "ERROR", details, "D")
            except Exception:
                self.log.exception(Logs.fileline() + ' : AnalyzerDet ERROR audit delete')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE AnalyzerDet delete id_analyzer=' + str(id_analyzer))
        try:
            details = {"result": "SUCCESS", "id_analyzer": id_analyzer, "id_user": args.get('id_user') if args else None}
            Audit.insertAudit(audit_user, "AnalyzerDet", "DEVICE", id_analyzer, "SUCCESS", details, "D")
        except Exception:
            self.log.exception(Logs.fileline() + ' : AnalyzerDet ERROR audit success')
        return compose_ret('', Constants.cst_content_type_json)


class AnalyzerFile(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self):
        audit_user = request.oauth_user
        l_analyzers = Analyzer.getAnalyzerFiles()

        if not l_analyzers:
            self.log.error(Logs.fileline() + ' : TRACE AnalyzerFile not found')

        self.log.info(Logs.fileline() + ' : TRACE AnalyzerFile')
        try:
            details = {"result": "SUCCESS", "count": len(l_analyzers) if l_analyzers else 0}
            Audit.insertAudit(audit_user, "AnalyzerFile", "DEVICE", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : AnalyzerFile ERROR audit')
        return compose_ret(l_analyzers, Constants.cst_content_type_json)


class AnalyzerLab27(Resource):
    log = logging.getLogger('log_services')

    def post(self, id_analyzer):
        msg_hl7 = request.data.decode('utf-8').strip()

        if not msg_hl7:
            msg_ack = Analyzer.generate_ack_response(None, "AR", "Empty HL7 message")
            self.log.info(Logs.fileline() + f' : ERROR AnalyzerLab27 msg_hl7 missing, msg_ack : {msg_ack}')
            return compose_ret(msg_ack, Constants.cst_content_type_hl7, 400)

        self.log.info(Logs.fileline() + f' : DEBUG Raw HL7 message (repr) = {repr(msg_hl7)}')
        msg_hl7 = msg_hl7.replace("\n", "\r")

        analyzer = Analyzer.getAnalyzerDetById(id_analyzer)
        if not analyzer:
            msg_ack = Analyzer.generate_ack_response(None, "AR", "Id analyzer not found")
            self.log.error(Logs.fileline() + ' : AnalyzerLab27 ERROR analyzer not found')
            return compose_ret(msg_ack, Constants.cst_content_type_hl7, 400)

        if not msg_hl7.startswith("MSH|"):
            msg_ack = Analyzer.generate_ack_response(None, "AE", "Invalid HL7 format")
            self.log.error(Logs.fileline() + " : ERROR - Invalid HL7 message format")
            return compose_ret(msg_ack, Constants.cst_content_type_hl7, 400)

        id_msg = Analyzer.insertLabTransactions(
            ans_ser=analyzer['ans_ser'], id_samp=0, stat=Constants.cst_stat_init,
            recv=msg_hl7.replace("\r", "\n"), sent='', tot='LAB-27'
        )

        if not id_msg:
            self.log.error(Logs.fileline() + ' ERROR insertLabTransactions LAB-27 failed')
            msg_ack = Analyzer.generate_ack_response(None, "AE", "Database insert failed")
            return compose_ret(msg_ack, Constants.cst_content_type_hl7, 500)

        try:
            hl7_msg = parse_message(msg_hl7, find_groups=False, validation_level=2)
            self.log.info(Logs.fileline() + f' : DEBUG hl7_msg type = {type(hl7_msg)}')

            if not isinstance(hl7_msg, Message):
                msg_ack = Analyzer.generate_ack_response(None, "AE", "HL7 parsing failed")
                Analyzer.updateLab27_ACK(id_task=id_msg, stat="AE", msg=msg_ack)
                return compose_ret(msg_ack, Constants.cst_content_type_hl7, 400)

            message_type = hl7_msg.MSH.msh_9.value
            self.log.info(Logs.fileline() + f' : DEBUG message_type = {message_type}')

            if not message_type.startswith("QBP^Q11"):
                msg_ack = Analyzer.generate_ack_response(hl7_msg, "AE", f"Unexpected message type ({message_type})")
                Analyzer.updateLab27_ACK(id_task=id_msg, stat="AE", msg=msg_ack)
                return compose_ret(msg_ack, Constants.cst_content_type_hl7, 400)

            # Extract QPD-3 (filter parameter)
            qpd_id = hl7_msg.QPD.qpd_3[0].value if hl7_msg.QPD.qpd_3 else ""
            self.log.info(Logs.fileline() + f' : DEBUG QPD-3 value = {qpd_id}')

            if not qpd_id or qpd_id.upper() == "ALL":
                self.log.info(Logs.fileline() + " : INFO QPD-3 = ALL → request for all available orders")
            else:
                self.log.info(Logs.fileline() + f" : INFO QPD-3 = {qpd_id} → request for specific specimen/order")

            # === Call to final response generator ===
            msg_rsp = Analyzer.generate_rsp_k11_response(hl7_msg)

            if not msg_rsp:
                self.log.error(Logs.fileline() + " : ERROR - Failed to build RSP^K11 response")
                msg_ack = Analyzer.generate_ack_response(hl7_msg, "AE", "Failed to generate RSP^K11")
                Analyzer.updateLab27_ACK(id_task=id_msg, stat="AE", msg=msg_ack)
                return compose_ret(msg_ack, Constants.cst_content_type_hl7, 500)

            Analyzer.updateLab27_ACK(id_task=id_msg, stat="AA", msg=msg_rsp)
            return compose_ret(msg_rsp, Constants.cst_content_type_hl7)

        except Exception as e:
            self.log.exception(Logs.fileline() + f' : ERROR - HL7 parsing exception: {str(e)}')
            msg_ack = Analyzer.generate_ack_response(None, "AE", "HL7 parsing failed")
            Analyzer.updateLab27_ACK(id_task=id_msg, stat="AE", msg=msg_ack)
            return compose_ret(msg_ack, Constants.cst_content_type_hl7, 400)


class AnalyzerLab29(Resource):
    log = logging.getLogger('log_services')

    def post(self, id_analyzer):
        msg_hl7 = request.data.decode('utf-8').strip()

        if not msg_hl7:
            msg_ack = Analyzer.generate_ack_response(None, "AR", "Empty HL7 message")
            self.log.info(Logs.fileline() + f' : ERROR AnalyzerLab29 msg_hl7 missing, msg_ack : {msg_ack}')
            return compose_ret(msg_ack, Constants.cst_content_type_hl7, 400)

        # Log raw HL7 message
        self.log.info(Logs.fileline() + f' : DEBUG Raw HL7 message (repr) = {repr(msg_hl7)}')

        # Ensure proper segment separator
        msg_hl7 = msg_hl7.replace("\n", "\r")

        # get analyzer details from id_analyzer
        analyzer = Analyzer.getAnalyzerDetById(id_analyzer)

        if not analyzer:
            msg_ack = Analyzer.generate_ack_response(None, "AR", "Id analyzer not found")
            self.log.error(Logs.fileline() + ' : ' + 'AnalyzerLab29 ERROR analyzer not found')
            return compose_ret(msg_ack, Constants.cst_content_type_hl7, 400)

        if not msg_hl7.startswith("MSH|"):
            msg_ack = Analyzer.generate_ack_response(None, "AE", "Invalid HL7 format")
            self.log.error(Logs.fileline() + " : ERROR - Invalid HL7 message format")
            return compose_ret(msg_ack, Constants.cst_content_type_hl7, 400)

        # stock in DB the message received
        id_msg = Analyzer.insertLabTransactions(ans_ser=analyzer['ans_ser'], id_samp=0, stat=Constants.cst_stat_init, recv=msg_hl7.replace("\r", "\n"), sent='', tot='LAB-29')

        if not id_msg:
            self.log.error(Logs.fileline() + ' ERROR insertLabTransactions LAB-29 for id_analyzer=' + str("id_analyzer"))
            msg_ack = Analyzer.generate_ack_response(None, "AE", "Database insert failed")
            return compose_ret(msg_ack, Constants.cst_content_type_hl7, 500)

        self.log.info(Logs.fileline() + ' : TRACE AnalyzerLab29 msg_hl7 (after correction) : ' + str(msg_hl7))

        try:
            # Parse HL7 message
            hl7_msg = parse_message(msg_hl7, find_groups=False, validation_level=2)

            # Log message type
            self.log.info(Logs.fileline() + f' : DEBUG hl7_msg type = {type(hl7_msg)}')

            if not isinstance(hl7_msg, Message):
                self.log.error(Logs.fileline() + f' : ERROR - HL7 parsing failed, returned type: {type(hl7_msg)}')
                self.log.error(Logs.fileline() + f' : ERROR - HL7 parsing returned: {hl7_msg}')
                msg_ack = Analyzer.generate_ack_response(None, "AE", "HL7 parsing failed")
                Analyzer.updateLab29_ACK(id_task=id_msg, id_samp=0, stat="AE", msg=msg_ack)
                return compose_ret(msg_ack, Constants.cst_content_type_hl7, 400)

            # Extract MSH-9 safely
            try:
                message_type = hl7_msg.MSH.msh_9.value
            except AttributeError:
                self.log.exception(Logs.fileline() + ' : ERROR - MSH-9 missing or incorrect format')
                msg_ack = Analyzer.generate_ack_response(hl7_msg, "AE", "MSH-9 missing or incorrect format")
                Analyzer.updateLab29_ACK(id_task=id_msg, id_samp=0, stat="AE", msg=msg_ack)
                return compose_ret(msg_ack, Constants.cst_content_type_hl7, 400)

            self.log.info(Logs.fileline() + ' : DEBUG message_type = ' + str(message_type))

            if not message_type.startswith("OUL^R22"):
                msg_ack = Analyzer.generate_ack_response(hl7_msg, "AE", f"Unexpected message type ({message_type})")
                self.log.error(Logs.fileline() + f' : ERROR AnalyzerLab29 Unexpected message type, msg_ack : {msg_ack}')
                Analyzer.updateLab29_ACK(id_task=id_msg, id_samp=0, stat="AE", msg=msg_ack)
                return compose_ret(msg_ack, Constants.cst_content_type_hl7, 400)

            # Extract patient, specimen, and test details
            patient_id = hl7_msg.PID.pid_3.value if hasattr(hl7_msg, 'PID') else "UNKNOWN"
            self.log.info(Logs.fileline() + ' : DEBUG patient_id  = ' + str(patient_id))

            # Extract specimen identifier from SPM-2
            raw_specimen_id = hl7_msg.SPM.spm_2.value.split('&')[0] if hasattr(hl7_msg, 'SPM') and hasattr(hl7_msg.SPM, 'spm_2') else "UNKNOWN"
            self.log.info(Logs.fileline() + f' : DEBUG raw_specimen_id = {raw_specimen_id}')

            # Resolve the specimen ID to an internal id_data if possible
            resolved_id = Product.resolveProductId(raw_specimen_id)
            if resolved_id:
                specimen_id = resolved_id
                self.log.info(Logs.fileline() + f' : INFO specimen_id resolved to id_data = {specimen_id}')
            else:
                specimen_id = raw_specimen_id  # fallback to original value
                self.log.warning(Logs.fileline() + f' : WARNING specimen_id not found as id_data or code: {raw_specimen_id}')

            test_id = hl7_msg.OBR.obr_4.value if hasattr(hl7_msg, 'OBR') else "UNKNOWN"
            self.log.info(Logs.fileline() + ' : DEBUG test_id  = ' + str(test_id))

            order_status = hl7_msg.ORC.orc_1.value if hasattr(hl7_msg, 'ORC') else "UNKNOWN"
            self.log.info(Logs.fileline() + ' : DEBUG order_status  = ' + str(order_status))

            self.log.info(Logs.fileline() + ' : TRACE AnalyzerLab29 - Message processed successfully')

            # Generate an ACK^R22 HL7 response
            msg_ack = Analyzer.generate_ack_response(hl7_msg, "AA", "Message processed successfully")

            self.log.info(Logs.fileline() + f' : TRACE AnalyzerLab29 msg_ack : {msg_ack}')

            ack_status = "AA" if "AA" in msg_ack else "AE" if "AE" in msg_ack else "AR"

            # update transaction in DB
            ret = Analyzer.updateLab29_ACK(id_task=id_msg, id_samp=specimen_id, stat=ack_status, msg=msg_ack)

            has_obx = any(segment.name == "OBX" for segment in hl7_msg.children)

            # Save results matching with specimen_id
            if has_obx:
                obx_segments = [segment for segment in hl7_msg.children if segment.name == "OBX"]

                # Extract raw OBX segments from original HL7 message (DO NOT use hl7apy for this)
                raw_segments = msg_hl7.split("\r")
                obx_raw_list = [s for s in raw_segments if s.startswith("OBX|")]

                for i, obx in enumerate(obx_segments):
                    try:
                        obs_id = obx.obx_3.value if hasattr(obx, "obx_3") else "UNKNOWN"
                        obs_value = obx.obx_5.value if hasattr(obx, "obx_5") else ""
                        obs_unit = obx.obx_6.value if hasattr(obx, "obx_6") else ""

                        # Read OBX-11 (result status)
                        obs_status = ""
                        if i < len(obx_raw_list):
                            raw_obx = obx_raw_list[i]
                            self.log.info(Logs.fileline() + f" : DEBUG raw_obx={raw_obx}")
                            fields = raw_obx.strip().split("|")
                            obs_status = fields[11] if len(fields) > 11 else ""

                        obs_status = (obs_status or "").strip().upper()

                        lb_code = None
                        obs_id = (obs_id or "").strip()
                        if obs_id and len(obs_id) <= 10:
                            lb_code = obs_id

                        # Filter only final results
                        if obs_status == "F":
                            ret = Analyzer.insertAnalyzerResult(
                                ans_ser=analyzer['ans_ser'],
                                code=obs_id,
                                samp=specimen_id,
                                value=obs_value,
                                unit=obs_unit,
                                lb_code=lb_code
                            )
                            if not ret:
                                self.log.warning(Logs.fileline() + f" : INSERT FAILED for {obs_id} (sample={specimen_id}, analyzer={id_analyzer})")
                            else:
                                self.log.info(Logs.fileline() + f" : SAVED result: {obs_id} = {obs_value} {obs_unit}")
                        else:
                            self.log.info(Logs.fileline() + f" : SKIPPED non-final result: {obs_id} (status={obs_status})")

                    except Exception as e:
                        self.log.exception(Logs.fileline() + f" : ERROR while parsing OBX: {str(e)}")

            # Return HL7 ACK^R22 as a response
            return compose_ret(msg_ack, Constants.cst_content_type_hl7)

        except Exception as e:
            self.log.exception(Logs.fileline() + f' : ERROR - HL7 parsing exception: {str(e)}')
            msg_ack = Analyzer.generate_ack_response(None, "AE", "HL7 parsing failed")
            Analyzer.updateLab29_ACK(id_task=id_msg, id_samp=0, stat="AE", msg=msg_ack)
            return compose_ret(msg_ack, Constants.cst_content_type_hl7, 400)


class AnalyzerMsgList(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self):
        audit_user = request.oauth_user
        args = request.get_json()

        l_msg = Analyzer.getAnalyzerMsgList(args)

        if not l_msg:
            self.log.info(Logs.fileline() + ' : TRACE AnalyzerMsgList not found')
            try:
                details = {"result": "ERROR", "reason": "NOT_FOUND"}
                Audit.insertAudit(audit_user, "AnalyzerMsgList", "DEVICE", None, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : AnalyzerMsgList ERROR audit not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        for msg in l_msg:
            # Replace None by empty string
            for key, value in list(msg.items()):
                if msg[key] is None:
                    msg[key] = ''
                elif key == 'anm_date' or key == 'anm_date_upd':
                    if msg[key]:
                        msg[key] = datetime.strftime(msg[key], Constants.cst_dt_HM)

        self.log.info(Logs.fileline() + ' : TRACE AnalyzerMsgList')
        try:
            details = {"result": "SUCCESS", "count": len(l_msg)}
            Audit.insertAudit(audit_user, "AnalyzerMsgList", "DEVICE", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : AnalyzerMsgList ERROR audit success')
        return compose_ret({"data": l_msg}, Constants.cst_content_type_json)


class AnalyzerMsgDet(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def delete(self, id_msg):
        audit_user = request.oauth_user
        ret = Analyzer.deleteMsgAnalyzer(id_msg)

        if not ret:
            self.log.error(Logs.fileline() + ' : TRACE AnalyzerMsgDet delete ERROR')
            try:
                details = {"result": "ERROR", "reason": "DELETE_FAILED", "id_msg": id_msg}
                Audit.insertAudit(audit_user, "AnalyzerMsgDet", "DEVICE", id_msg, "ERROR", details, "D")
            except Exception:
                self.log.exception(Logs.fileline() + ' : AnalyzerMsgDet ERROR audit delete')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE AnalyzerMsgDet delete id_msg=' + str(id_msg))
        try:
            details = {"result": "SUCCESS", "id_msg": id_msg}
            Audit.insertAudit(audit_user, "AnalyzerMsgDet", "DEVICE", id_msg, "SUCCESS", details, "D")
        except Exception:
            self.log.exception(Logs.fileline() + ' : AnalyzerMsgDet ERROR audit success')
        return compose_ret('', Constants.cst_content_type_json)
