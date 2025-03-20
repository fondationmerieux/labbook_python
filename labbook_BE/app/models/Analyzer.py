# -*- coding:utf-8 -*-
import logging
import mysql.connector
import os
import tomli
import hl7apy

from datetime import datetime
from hl7apy.core import Message, Segment
from hl7apy.parser import parse_message

from app.models.Constants import *
from app.models.DB import DB
from app.models.Logs import Logs
from app.models.Analysis import Analysis
from app.models.Patient import Patient
from app.models.Product import Product
from app.models.Record import Record
from app.models.Result import Result
from app.models.Various import Various


class Analyzer:
    log = logging.getLogger('log_db')

    @staticmethod
    def getConnectSetting():
        cursor = DB.cursor()

        req = ('select cos_by_user, cos_url '
               'from connect_setting')

        cursor.execute(req)

        return cursor.fetchone()

    @staticmethod
    def updateConnectSetting(**params):
        try:
            cursor = DB.cursor()

            req = ('update connect_setting set cos_by_user=%(id_user)s, cos_url=%(url)s')

            cursor.execute(req, params)

            Analyzer.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Analyzer.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getAnalyzerList():
        cursor = DB.cursor()

        req = ('select ans_ser, ans_rank, ans_name, ans_id, ans_batch '
               'from analyzer_setting '
               'order by ans_rank')

        cursor.execute(req,)

        return cursor.fetchall()

    @staticmethod
    def getAnalyzerDet(id_analyzer):
        cursor = DB.cursor()

        req = ('select ans_ser, ans_user, ans_name, ans_id, ans_filename, ans_batch '
               'from analyzer_setting '
               'where ans_ser=%s')

        cursor.execute(req, (id_analyzer,))

        return cursor.fetchone()

    @staticmethod
    def getAnalyzerDetById(id_analyzer):
        cursor = DB.cursor()

        req = ('select ans_ser, ans_user, ans_name, ans_id, ans_filename, ans_batch '
               'from analyzer_setting '
               'where ans_id=%s')

        cursor.execute(req, (id_analyzer,))

        return cursor.fetchone()

    @staticmethod
    def insertAnalyzerDet(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into analyzer_setting '
                           '(ans_date, ans_user, ans_rank, ans_name, ans_id, ans_filename, ans_batch) '
                            'values (NOW(), %(id_user)s, %(rank)s, %(name)s, %(id)s, %(filename)s, %(batch)s)', params)

            Analyzer.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Analyzer.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def updateAnalyzerDet(**params):
        try:
            cursor = DB.cursor()

            req = ('update analyzer_setting set ans_user=%(id_user)s, ans_rank=%(rank)s, ans_name=%(name)s, '
                   'ans_id=%(id)s, ans_filename=%(filename)s, ans_batch=%(batch)s '
                   'where ans_ser=%(id_analyzer)s')

            cursor.execute(req, params)

            Analyzer.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Analyzer.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def deleteAnalyzer(id_analyzer):
        try:
            cursor = DB.cursor()

            cursor.execute('delete from analyzer_setting '
                           'where ans_ser=%s', (id_analyzer,))

            Analyzer.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Analyzer.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getAnalyzerFiles():
        ret = []

        # get list of file a specific permanent directory
        path = "/storage/resource/connect/analyzer/setting/"

        l_files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

        Analyzer.log.info(Logs.fileline() + ' DEBUG l_files= ' + str(l_files))

        # parse files
        for filename in l_files:
            filepath = os.path.join(path, filename)

            with open(filepath, "rb") as f:
                config = tomli.load(f)

            analyzer = {}

            analyzer['filename'] = filename
            analyzer['version']  = config['version']
            analyzer['brand']    = config['analyzer']['brand']
            analyzer['name']     = config['analyzer']['name']
            analyzer['id']       = config['analyzer']['id']
            # Useless 12/02/2025 : analyzer['connect']  = config['analyzer']['connect']
            analyzer['mapping']  = config['analyzer']['mapping']
            analyzer['display']  = str(analyzer['brand']) + ' - ' + str(analyzer['name']) + ' | Id : ' + str(analyzer['id'])

            ret.append(analyzer)

        Analyzer.log.info(Logs.fileline() + ' DEBUG ret= ' + str(ret))

        return ret

    @staticmethod
    def listTask(stat, tot=''):
        cursor = DB.cursor()

        cond = ' anm_stat = "' + stat + '"'

        if not stat:
            cond = ' anm_stat != NULL'

        if tot:
            cond += ' and anm_tot="' + str(tot) + '"'

        req = ('select anm_ser, anm_date, anm_date_upd, anm_id_samp, anm_stat, anm_msg_sent, anm_msg_recv, anm_ans, anm_tot '
               'from analyzer_msg '
               'where ' + cond + ' order by anm_date')

        cursor.execute(req)

        return cursor.fetchall()

    @staticmethod
    def buildLab28(id_samp):
        date_now = datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")

        # laboritory details
        lab_name = Various.getDefaultValue('entete_1')

        if lab_name:
            lab_name = lab_name['value']
        else:
            lab_name = ""

        # get specimen details
        samp = Product.getProductDet(id_samp)

        if not samp:
            Analyzer.log.error(Logs.fileline() + ' ERROR buildLab28 getProductDet for id_samp=' + str(id_samp))

        id_rec = samp['id_rec']
        type_samp = Various.getDicoById(samp['prod_type'])

        if type_samp:
            Various.useLangDB()
            trans = type_samp['label']
            type_samp = _(trans.strip())
        else:
            type_samp = "UNKNOWN"

        # get analysis details
        ana = Analysis.getAnalysis(samp['samp_id_ana'])

        if not ana:
            Analyzer.log.error(Logs.fileline() + ' ERROR buildLab28 getAnalysis for samp_id_ana=' + str(samp['samp_id_ana']))

        ana_name = ana['nom']
        ana_code = ana['code']

        if ana['ana_loinc']:
            ana_code = ana['ana_loinc']

        # get record details
        rec = Record.getRecord(id_rec)

        if not rec:
            Analyzer.log.error(Logs.fileline() + ' ERROR buildLab28 getRecord for id_rec=' + str(id_rec))

        id_pat = rec['id_patient']

        # get patient details
        pat = Patient.getPatient(id_pat)

        if not pat:
            Analyzer.log.error(Logs.fileline() + ' ERROR buildLab28 getPatient for id_pat=' + str(id_pat))

        pat_sex = 'U'

        if pat['pat_birth']:
            pat_birth = datetime.strftime(pat['pat_birth'], "%Y%m%d%H%M%S")
        else:
            pat_birth = ''

        if pat['pat_sex'] == 1:
            pat_sex = 'M'
        elif pat['pat_sex'] == 2:
            pat_sex = 'F'

        l_analyzer = Analyzer.getAnalyzerList()

        for analyzer in l_analyzer:
            # Check ans_batch before proceeding
            if analyzer['ans_batch'] == 'N':
                Analyzer.log.info(f"INFO: Skipping analyzer {analyzer['ans_ser']} because ans_batch is 'N'")
                continue

            # Save OML33 task for one analyzer
            ret = Analyzer.insertLabTransactions(ans_ser=analyzer['ans_ser'], id_samp=id_samp, stat=Constants.cst_stat_init, sent='', recv='', tot='LAB-28')

            if not ret:
                Analyzer.log.error(Logs.fileline() + ' ERROR insertLabTransactions LAB-28 for id_analyzer=' + str(analyzer['ans_ser']) + 'and id_samp=' + str(id_samp))

            else:
                id_task = ret

                # Build OML_O33
                msg = Message("OML_O33", version="2.5.1")

                # Message segment
                msg.msh.msh_1  = "|"
                msg.msh.msh_2  = "^~\\&"
                msg.msh.msh_3  = "LabBook"
                msg.msh.msh_4  = str(lab_name)
                msg.msh.msh_5  = "LabBook Connect"
                msg.msh.msh_7  = date_now
                msg.msh.msh_9  = "OML^O33^OML_O33"  # Message type, cf line page 44 from IHE_PaLM_TF_Vol2b.pdf
                msg.msh.msh_10 = str(id_task)       # Message control ID, sending back by receiving system
                msg.msh.msh_11 = "P"                # Processing ID, "D"ebugging, "P"roduction, "T"raining.
                msg.msh.msh_12 = "2.5.1"            # HL7 version
                msg.msh.msh_18 = "UNICODE UTF-8"    # Character set
                msg.msh.msh_21 = "LAB-28^IHE"       # Message profile identifier

                try:
                    msg.msh.validate()
                    Analyzer.log.info(Logs.fileline() + ' DEBUG MSH Validated')
                except Exception as e:
                    Analyzer.log.error(Logs.fileline() + ' ERROR e : ' + str(e))

                # Add group
                msg.add_group("OML_O33_PATIENT")

                # Patient segment
                pid_segment = msg.oml_o33_patient.add_segment('PID')
                pid_segment.pid_1  = "1"                  # ID of this transaction
                pid_segment.pid_2  = pat['pat_code']      # Patient ID
                pid_segment.pid_3  = pat['pat_code_lab']  # Laboratory code for patient
                pid_segment.pid_4  = str(pat['id_data'])  # Alternative ID, serial from database
                pid_segment.pid_5  = f"{pat['pat_name']}^{pat['pat_firstname']}^L"  # Family name^Given name^Type."L"egal name
                pid_segment.pid_6  = pat['pat_maiden']    # Maiden name
                pid_segment.pid_7  = pat_birth            # Datetime of birth.
                pid_segment.pid_8  = pat_sex              # Sex : "F"emale, "M"ale, "O"ther, "U"nknown, "A"mbigous, "N"ot app
                pid_segment.pid_11 = "Street^Other^City^Zip"  # Address TODO
                pid_segment.pid_13 = "Phone^Email"            # Home phone number and email
                pid_segment.pid_28 = ""                   # Nationality

                try:
                    pid_segment.validate()
                    Analyzer.log.info(Logs.fileline() + ' DEBUG PID Validated')
                except Exception as e:
                    Analyzer.log.error(Logs.fileline() + ' ERROR e : ' + str(e))

                # Add group
                specimen_group = msg.add_group("OML_O33_SPECIMEN")

                # Specimen segment
                spm_segment = specimen_group.add_segment('SPM')
                spm_segment.spm_1 = "1"
                spm_segment.spm_2 = str(id_samp)
                spm_segment.spm_4 = f"{id_samp}^{type_samp}^LBK"
                spm_segment.spm_11 = "P"

                try:
                    spm_segment.validate()
                    Analyzer.log.info(Logs.fileline() + ' DEBUG SPM Validated')
                except Exception as e:
                    Analyzer.log.error(Logs.fileline() + ' ERROR e : ' + str(e))

                # Add group
                order_group = specimen_group.add_group("OML_O33_ORDER")

                # Order segment
                orc_segment = order_group.add_segment('ORC')
                orc_segment.orc_1 = "NW"          # order control code : NW (new order), CA (cancel)
                orc_segment.orc_2 = str(id_task)  # Placer order number. One order by OML^O33 so same number of msh_10

                try:
                    orc_segment.validate()
                    Analyzer.log.info(Logs.fileline() + ' DEBUG ORC Validated')
                except Exception as e:
                    Analyzer.log.error(Logs.fileline() + ' ERROR e : ' + str(e))

                timing_group = order_group.add_group("OML_O33_TIMING")

                # Timing quantity segment
                tq1_segment = timing_group.add_segment('TQ1')
                tq1_segment.tq1_1 = "1"
                tq1_segment.tq1_9 = "R"  # priority : "R"outine, "S"tat with highest priority.
                # TODO emergency ?

                try:
                    tq1_segment.validate()
                    Analyzer.log.info(Logs.fileline() + ' DEBUG TQ1 Validated')
                except Exception as e:
                    Analyzer.log.error(Logs.fileline() + ' ERROR e : ' + str(e))

                # Add group
                observation_request_group = order_group.add_group("OML_O33_OBSERVATION_REQUEST")

                # Observation request segment
                obr_segment = observation_request_group.add_segment('OBR')
                obr_segment.obr_1  = "1"             # ID OBR
                obr_segment.obr_2  = f"{id_task}_1"  # Place order number. Same ad orc_2
                obr_segment.obr_4  = f"{ana_code}^{ana_name}"  # Code and Name of observation aka name of test.

                try:
                    obr_segment.validate()
                    Analyzer.log.info(Logs.fileline() + ' DEBUG OBR Validated')
                except Exception as e:
                    Analyzer.log.error(Logs.fileline() + ' ERROR e : ' + str(e))

                # Convertir le message en une chaîne
                hl7_string = msg.to_er7()

                str_hl7_string = hl7_string

                Analyzer.log.info(Logs.fileline() + ' DEBUG buildLab28 hl7_string=\n' + str_hl7_string.replace('\r', '\n'))

                # update task lab28 with hl7 message
                ret = Analyzer.updateLab28_OML_O33(id_task=id_task, stat=Constants.cst_stat_pending, msg=str(hl7_string))

                if not ret:
                    Analyzer.log.error(Logs.fileline() + ' ERROR updateLab28 for id_task=' + str(id_task))
                    return False

        return True

    @staticmethod
    def insertLabTransactions(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into analyzer_msg '
                           '(anm_date, anm_id_samp, anm_stat, anm_msg_sent, anm_msg_recv, anm_ans, anm_tot) '
                            'values (NOW(), %(id_samp)s, %(stat)s, %(sent)s, %(recv)s, %(ans_ser)s, %(tot)s)', params)

            Analyzer.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Analyzer.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def updateLab27_ACK(**params):
        try:
            cursor = DB.cursor()

            Analyzer.log.info(Logs.fileline() + ' : DEBUG params=' + str(params))

            params["msg"] = params["msg"].replace("\r", "\\r")

            req = ('update analyzer_msg set anm_date_upd=NOW(), anm_stat=%(stat)s, anm_msg_sent=%(msg)s '
                   'where anm_ser=%(id_task)s')

            cursor.execute(req, params)

            Analyzer.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Analyzer.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def updateLab28_OML_O33(**params):
        try:
            cursor = DB.cursor()

            Analyzer.log.info(Logs.fileline() + ' : DEBUG params=' + str(params))

            params["msg"] = params["msg"].replace("\r", "\\r")

            req = ('update analyzer_msg set anm_date_upd=NOW(), anm_stat=%(stat)s, anm_msg_sent=%(msg)s '
                   'where anm_ser=%(id_task)s')

            cursor.execute(req, params)

            Analyzer.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Analyzer.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def updateLab28_ORL_O34(**params):
        try:
            cursor = DB.cursor()

            req = ('update analyzer_msg set anm_date_upd=NOW(), anm_stat=%(stat)s, anm_msg_recv=%(ORL_O34)s '
                   'where anm_ser=%(id_task)s')

            cursor.execute(req, params)

            Analyzer.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Analyzer.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def updateLab29_ACK(**params):
        try:
            cursor = DB.cursor()

            Analyzer.log.info(Logs.fileline() + ' : DEBUG params=' + str(params))

            params["msg"] = params["msg"].replace("\r", "\\r")

            req = ('update analyzer_msg set anm_date_upd=NOW(), anm_id_samp=%(id_samp)s, anm_stat=%(stat)s, '
                   'anm_msg_sent=%(msg)s '
                   'where anm_ser=%(id_task)s')

            cursor.execute(req, params)

            Analyzer.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Analyzer.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def saveResult(msg):

        hl7_msg = 'TODO'  # parse_message(msg)

        Analyzer.log.info(Logs.fileline() + ' : DEBUG hl7_msg received = ' + str(hl7_msg))

        # Result.updateResultDemo()

        return True

    @staticmethod
    def getAnalyzerMsgList(args):
        cursor = DB.cursor()

        if args:
            # TODO
            Analyzer.log.info(Logs.fileline() + ' : DEBUG TODO args getAnalyzerMsgList')

        req = ('select anm_ser, anm_date, anm_date_upd, anm_id_samp, anm_stat, anm_msg_sent, anm_msg_recv, anm_ans, '
               'ifnull(ans_name, "") as analyzer_name, ifnull(ans_id, "") as analyzer_id, anm_tot '
               'from analyzer_msg '
               'left join analyzer_setting on anm_ans=ans_ser '
               'order by anm_date desc')

        cursor.execute(req,)

        return cursor.fetchall()

    @staticmethod
    def deleteMsgAnalyzer(id_msg):
        try:
            cursor = DB.cursor()

            cursor.execute('delete from analyzer_msg '
                           'where anm_ser=%s', (id_msg,))

            Analyzer.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Analyzer.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def generate_ack_response(original_message, ack_code, error_message=""):
        """
        Generates a correctly formatted HL7 ACK response message according to HL7 2.5.1 specifications.

        :param original_message: The received HL7 message (OUL^R22) or None if parsing failed.
        :param ack_code: "AA" (Accepted), "AE" (Error), "AR" (Rejected).
        :param error_message: Optional error description.
        :return: A correctly formatted HL7 ACK response message.
        """
        if not isinstance(original_message, Message):
            Analyzer.log.error(Logs.fileline() + " : ERROR - original_message is not a valid HL7 object.")
            original_message = None

        message_control_id = original_message.msh.msh_10.value if original_message else str(int(datetime.now().timestamp()))
        receiving_application = original_message.msh.msh_3.value if original_message else "UNKNOWN"
        receiving_facility = original_message.msh.msh_4.value if original_message else "UNKNOWN"

        sending_application = "LabBook"
        sending_facility = "Lab"

        # Extract MSH-9-2 (Trigger Event) from the original message
        trigger_event = original_message.msh.msh_9.value.split("^")[1] if original_message and "^" in original_message.msh.msh_9.value else "R22"

        # Build the ACK message
        ack = Message("ACK", version="2.5.1")

        # Build the MSH segment
        ack.msh.msh_1 = "|"
        ack.msh.msh_2 = "^~\\&"
        ack.msh.msh_3 = sending_application
        ack.msh.msh_4 = sending_facility
        ack.msh.msh_5 = receiving_application
        ack.msh.msh_6 = receiving_facility
        ack.msh.msh_7 = datetime.now().strftime("%Y%m%d%H%M%S")
        ack.msh.msh_9 = f"ACK^{trigger_event}^ACK"  # Compliant with HL7 2.5.1 documentation
        ack.msh.msh_10 = message_control_id
        ack.msh.msh_11 = "P"
        ack.msh.msh_12 = "2.5.1"
        ack.msh.msh_18 = "UNICODE UTF-8"
        ack.msh.msh_21 = "LAB-29^IHE"

        # Add the MSA segment (Message Acknowledgment)
        msa_segment = ack.add_segment("MSA")
        msa_segment.msa_1 = ack_code
        msa_segment.msa_2 = message_control_id
        msa_segment.msa_3 = error_message if error_message else "Message processed successfully"

        # If there is an error, include the ERR segment as per HL7 2.5.1 recommendations
        if ack_code in ["AE", "AR"]:
            err_segment = ack.add_segment("ERR")
            err_segment.err_1 = "0"  # Error location (can be adjusted)
            err_segment.err_2 = "400"  # Application Error Code (example)
            err_segment.err_3 = "E"  # Error severity
            err_segment.err_4 = error_message if error_message else "Unknown error"

        try:
            ack.msh.validate()
            ack.msa.validate()
            Analyzer.log.info(Logs.fileline() + ' DEBUG - ACK Validated.')
        except Exception as e:
            Analyzer.log.error(Logs.fileline() + ' ERROR - Validation failed: ' + str(e))

        # Correctly format the ER7 message with explicit segment separators (`\r`)
        ack_message = f"{ack.msh.to_er7()}\r{ack.msa.to_er7()}\r"

        # Log the generated ACK message
        Analyzer.log.info(f"Generated HL7 ACK: {ack_message.replace(chr(13), '[CR]')}")

        return ack_message
