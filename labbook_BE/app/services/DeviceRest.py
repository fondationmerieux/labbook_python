# -*- coding:utf-8 -*-
import logging
import gettext

from datetime import datetime
from flask import request
from flask_restful import Resource
from hl7apy.parser import parse_message
from hl7apy.core import Message

from app.models.General import compose_ret
from app.models.Constants import *
from app.models.Analyzer import *
from app.models.Record import *
from app.models.User import *
from app.models.DB import *
from app.models.Logs import Logs
from app.models.Various import Various


class AnalyzerList(Resource):
    log = logging.getLogger('log_services')

    def get(self):
        l_analyzers = Analyzer.getAnalyzerList()

        if not l_analyzers:
            self.log.error(Logs.fileline() + ' : TRACE AnalyzerList not found')

        self.log.info(Logs.fileline() + ' : TRACE AnalyzerList')
        return compose_ret(l_analyzers, Constants.cst_content_type_json)


class AnalyzerDet(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_analyzer):
        item = Analyzer.getAnalyzerDet(id_analyzer)

        if not item:
            self.log.error(Logs.fileline() + ' : ' + 'AnalyzerDet ERROR not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        # Replace None by empty string
        for key, value in list(item.items()):
            if item[key] is None:
                item[key] = ''

        self.log.info(Logs.fileline() + ' : AnalyzerDet id_analyzer=' + str(id_analyzer))
        return compose_ret(item, Constants.cst_content_type_json, 200)

    def post(self, id_analyzer):
        args = request.get_json()

        if 'id_user' not in args or 'rank' not in args or 'name' not in args or 'key' not in args or \
           'connect' not in args or 'mapping' not in args or 'filename' not in args:
            self.log.error(Logs.fileline() + ' : AnalyzerDet ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # Update item
        if id_analyzer > 0:
            self.log.info(Logs.fileline() + ' : TRACE update AnalyzerDet')

            ret = Analyzer.updateAnalyzerDet(id_analyzer=id_analyzer,
                                             id_user=args['id_user'],
                                             rank=args['rank'],
                                             name=args['name'],
                                             id=args['key'],
                                             connect=args['connect'],
                                             mapping=args['mapping'],
                                             filename=args['filename'])

            if ret is False:
                self.log.error(Logs.alert() + ' : AnalyzerDet ERROR update')
                return compose_ret('', Constants.cst_content_type_json, 500)

        # Insert new item
        else:
            self.log.info(Logs.fileline() + ' : TRACE insert AnalyzerDet')
            ret = Analyzer.insertAnalyzerDet(id_user=args['id_user'],
                                             rank=args['rank'],
                                             name=args['name'],
                                             id=args['key'],
                                             connect=args['connect'],
                                             mapping=args['mapping'],
                                             filename=args['filename'])

            if ret <= 0:
                self.log.error(Logs.alert() + ' : AnalyzerDet ERROR  insert')
                return compose_ret('', Constants.cst_content_type_json, 500)

            id_analyzer = ret

        self.log.info(Logs.fileline() + ' : TRACE AnalyzerDet id_analyzer=' + str(id_analyzer))
        return compose_ret(id_analyzer, Constants.cst_content_type_json)

    def delete(self, id_analyzer):
        args = request.get_json()

        if args and 'id_user' in args:
            self.log.error(Logs.fileline() + ' : TRACE AnalyzerDet delete by id_user=' + str(args['id_user']))

        ret = Analyzer.deleteAnalyzer(id_analyzer)

        if not ret:
            self.log.error(Logs.fileline() + ' : TRACE AnalyzerDet delete ERROR')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE AnalyzerDet delete id_analyzer=' + str(id_analyzer))
        return compose_ret('', Constants.cst_content_type_json)


class AnalyzerFile(Resource):
    log = logging.getLogger('log_services')

    def get(self):
        l_analyzers = Analyzer.getAnalyzerFiles()

        if not l_analyzers:
            self.log.error(Logs.fileline() + ' : TRACE AnalyzerFile not found')

        self.log.info(Logs.fileline() + ' : TRACE AnalyzerFile')
        return compose_ret(l_analyzers, Constants.cst_content_type_json)


class AnalyzerLab27(Resource):
    log = logging.getLogger('log_services')

    def post(self, id_analyzer):
        msg_hl7 = request.data.decode('utf-8').strip()

        if not msg_hl7:
            msg_ack = Analyzer.generate_ack_response(None, "AR", "Empty HL7 message")
            self.log.info(Logs.fileline() + f' : ERROR AnalyzerLab27 msg_hl7 missing, msg_ack : {msg_ack}')
            return compose_ret(msg_ack, Constants.cst_content_type_hl7, 400)

        # Log raw HL7 message
        self.log.info(Logs.fileline() + f' : DEBUG Raw HL7 message (repr) = {repr(msg_hl7)}')

        # Ensure proper segment separator
        msg_hl7 = msg_hl7.replace("\n", "\r")

        # get analyzer details from id_analyzer
        analyzer = Analyzer.getAnalyzerDetById(id_analyzer)

        if not analyzer:
            msg_ack = Analyzer.generate_ack_response(None, "AR", "Id analyzer not found")
            self.log.error(Logs.fileline() + ' : ' + 'AnalyzerLab27 ERROR analyzer not found')
            return compose_ret(msg_ack, Constants.cst_content_type_hl7, 400)

        if not msg_hl7.startswith("MSH|"):
            msg_ack = Analyzer.generate_ack_response(None, "AE", "Invalid HL7 format")
            self.log.error(Logs.fileline() + " : ERROR - Invalid HL7 message format")
            return compose_ret(msg_ack, Constants.cst_content_type_hl7, 400)

        # stock in DB the message received
        id_msg = Analyzer.insertLabTransactions(ans_ser=analyzer['ans_ser'], id_samp=0, stat=Constants.cst_stat_init, recv=msg_hl7.replace("\r", "\n"), sent='', tot='LAB-27')

        if not id_msg:
            self.log.error(Logs.fileline() + ' ERROR insertLabTransactions LAB-29 for id_analyzer=' + str("id_analyzer"))
            msg_ack = Analyzer.generate_ack_response(None, "AE", "Database insert failed")
            return compose_ret(msg_ack, Constants.cst_content_type_hl7, 500)

        self.log.info(Logs.fileline() + ' : TRACE AnalyzerLab27 msg_hl7 (after correction) : ' + str(msg_hl7))

        try:
            # Parse HL7 message
            hl7_msg = parse_message(msg_hl7, find_groups=False, validation_level=2)

            # Log message type
            self.log.info(Logs.fileline() + f' : DEBUG hl7_msg type = {type(hl7_msg)}')

            if not isinstance(hl7_msg, Message):
                self.log.error(Logs.fileline() + f' : ERROR - HL7 parsing failed, returned type: {type(hl7_msg)}')
                self.log.error(Logs.fileline() + f' : ERROR - HL7 parsing returned: {hl7_msg}')
                msg_ack = Analyzer.generate_ack_response(None, "AE", "HL7 parsing failed")
                Analyzer.updateLab27(id_task=id_msg, stat="AE", msg=msg_ack)
                return compose_ret(msg_ack, Constants.cst_content_type_hl7, 400)

            # Extract MSH-9 safely
            try:
                message_type = hl7_msg.MSH.msh_9.value
            except AttributeError:
                self.log.error(Logs.fileline() + ' : ERROR - MSH-9 missing or incorrect format')
                msg_ack = Analyzer.generate_ack_response(hl7_msg, "AE", "MSH-9 missing or incorrect format")
                Analyzer.updateLab27(id_task=id_msg, stat="AE", msg=msg_ack)
                return compose_ret(msg_ack, Constants.cst_content_type_hl7, 400)

            self.log.info(Logs.fileline() + ' : DEBUG message_type = ' + str(message_type))

            if not message_type.startswith("OUL^R22"):
                msg_ack = Analyzer.generate_ack_response(hl7_msg, "AE", f"Unexpected message type ({message_type})")
                self.log.error(Logs.fileline() + f' : ERROR AnalyzerLab27 Unexpected message type, msg_ack : {msg_ack}')
                Analyzer.updateLab27(id_task=id_msg, stat="AE", msg=msg_ack)
                return compose_ret(msg_ack, Constants.cst_content_type_hl7, 400)

            # Extract patient, specimen, and test details
            patient_id = hl7_msg.PID.pid_3.value if hasattr(hl7_msg, 'PID') else "UNKNOWN"
            self.log.info(Logs.fileline() + ' : DEBUG patient_id  = ' + str(patient_id))

            specimen_id = hl7_msg.SPM.spm_2.value.split('&')[0] if hasattr(hl7_msg, 'SPM') and hasattr(hl7_msg.SPM, 'spm_2') else "UNKNOWN"
            self.log.info(Logs.fileline() + ' : DEBUG specimen_id  = ' + str(specimen_id))

            test_id = hl7_msg.OBR.obr_4.value if hasattr(hl7_msg, 'OBR') else "UNKNOWN"
            self.log.info(Logs.fileline() + ' : DEBUG test_id  = ' + str(test_id))

            order_status = hl7_msg.ORC.orc_1.value if hasattr(hl7_msg, 'ORC') else "UNKNOWN"
            self.log.info(Logs.fileline() + ' : DEBUG order_status  = ' + str(order_status))

            self.log.info(Logs.fileline() + ' : TRACE AnalyzerLab27 - Message processed successfully')

            # Generate an ACK^R22 HL7 response
            msg_ack = Analyzer.generate_ack_response(hl7_msg, "AA", "Message processed successfully")

            self.log.info(Logs.fileline() + f' : TRACE AnalyzerLab27 msg_ack : {msg_ack}')

            ack_status = "AA" if "AA" in msg_ack else "AE" if "AE" in msg_ack else "AR"

            # update transaction in DB
            ret = Analyzer.updateLab27(id_task=id_msg, stat=ack_status, msg=msg_ack)

            # Return HL7 ACK^R22 as a response
            return compose_ret(msg_ack, Constants.cst_content_type_hl7)

        except Exception as e:
            self.log.error(Logs.fileline() + f' : ERROR - HL7 parsing exception: {str(e)}')
            msg_ack = Analyzer.generate_ack_response(None, "AE", "HL7 parsing failed")
            Analyzer.updateLab27(id_task=id_msg, stat="AE", msg=msg_ack)
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
                self.log.error(Logs.fileline() + ' : ERROR - MSH-9 missing or incorrect format')
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

            specimen_id = hl7_msg.SPM.spm_2.value.split('&')[0] if hasattr(hl7_msg, 'SPM') and hasattr(hl7_msg.SPM, 'spm_2') else "UNKNOWN"
            self.log.info(Logs.fileline() + ' : DEBUG specimen_id  = ' + str(specimen_id))

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

            # TODO save result matching with specimen_id

            # Return HL7 ACK^R22 as a response
            return compose_ret(msg_ack, Constants.cst_content_type_hl7)

        except Exception as e:
            self.log.error(Logs.fileline() + f' : ERROR - HL7 parsing exception: {str(e)}')
            msg_ack = Analyzer.generate_ack_response(None, "AE", "HL7 parsing failed")
            Analyzer.updateLab29_ACK(id_task=id_msg, id_samp=0, stat="AE", msg=msg_ack)
            return compose_ret(msg_ack, Constants.cst_content_type_hl7, 400)


class AnalyzerMsgList(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        l_msg = Analyzer.getAnalyzerMsgList(args)

        if not l_msg:
            self.log.error(Logs.fileline() + ' : TRACE AnalyzerMsgList not found')
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
        return compose_ret({"data": l_msg}, Constants.cst_content_type_json)


class AnalyzerMsgDet(Resource):
    log = logging.getLogger('log_services')

    def delete(self, id_msg):
        ret = Analyzer.deleteMsgAnalyzer(id_msg)

        if not ret:
            self.log.error(Logs.fileline() + ' : TRACE AnalyzerMsgDet delete ERROR')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE AnalyzerMsgDet delete id_msg=' + str(id_msg))
        return compose_ret('', Constants.cst_content_type_json)
