# -*- coding:utf-8 -*-
import logging
import mysql.connector
import os
import tomli

from datetime import datetime
from hl7apy.core import Message

from app.models.Constants import Constants
from app.models.DB import DB
from app.models.Logs import Logs
from app.models.Analysis import Analysis
from app.models.Patient import Patient
from app.models.Product import Product
from app.models.Record import Record
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
        code_samp = samp['code']

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
                pid_segment.pid_3  = pat['pat_code_lab'] or ''  # Laboratory code for patient
                pid_segment.pid_4  = str(pat['id_data'])  # Alternative ID, serial from database
                pid_segment.pid_5  = f"{pat['pat_name']}^{pat['pat_firstname']}^L"  # Family name^Given name^Type."L"egal name
                pid_segment.pid_6  = pat['pat_maiden'] or ''  # Maiden name
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
                spm_segment.spm_2 = str(code_samp) if code_samp not in (None, '', 'None') else str(id_samp)
                spm_segment.spm_4 = f"{id_samp}^{type_samp}^LBK"
                spm_segment.spm_11 = "P"

                try:
                    spm_segment.validate()
                    Analyzer.log.info(Logs.fileline() + ' DEBUG SPM Validated')
                except Exception as e:
                    Analyzer.log.error(Logs.fileline() + ' ERROR e : ' + str(e))

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

                # Timing quantity segment
                tq1_segment = order_group.add_segment('TQ1')
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
    def generate_rsp_k11_response(original_message):
        """
        Generates a RSP^K11 HL7 response to a QBP^Q11 query as per IHE LAB-27.

        :param original_message: HL7 QBP^Q11 message
        :return: HL7 ER7 string or None
        """
        if not original_message:
            Analyzer.log.error(Logs.fileline() + " : ERROR - original_message is None")
            return None

        try:
            now = datetime.now().strftime("%Y%m%d%H%M%S")
            msg_control_id = original_message.msh.msh_10.value or f"RSP{now}"
            query_tag = original_message.qpd.qpd_2.value or "GENEXPERT"

            raw_qpd3 = original_message.qpd.qpd_3[0].value if original_message.qpd.qpd_3 else ""
            patient_id = ""
            specimen_id = ""

            if raw_qpd3:
                parts = raw_qpd3.split("^")
                patient_id = parts[0] if len(parts) > 0 else ""
                specimen_id = parts[1] if len(parts) > 1 else parts[0]

            # Initialize RSP_K11
            rsp = Message("RSP_K11", version="2.5.1")

            # === MSH segment ===
            rsp.msh.msh_3 = "LabBook"
            rsp.msh.msh_4 = "LIS"
            rsp.msh.msh_5 = original_message.msh.msh_3.value or "GeneXpert"
            rsp.msh.msh_6 = original_message.msh.msh_4.value or "Analyzer"
            rsp.msh.msh_7 = now
            rsp.msh.msh_9 = "RSP^K11^RSP_K11"
            rsp.msh.msh_10 = msg_control_id
            rsp.msh.msh_11 = "P"
            rsp.msh.msh_12 = "2.5.1"
            rsp.msh.msh_18 = "UNICODE UTF-8"
            rsp.msh.msh_21 = "LAB-27^IHE"

            # === MSA segment ===
            rsp.msa.msa_1 = "AA"
            rsp.msa.msa_2 = msg_control_id
            rsp.msa.msa_3 = ""

            # === QAK segment ===
            rsp.qak.qak_1 = query_tag
            rsp.qak.qak_2 = "OK"

            # === QPD segment ===
            qpd = rsp.add_segment("QPD")
            qpd.qpd_1 = original_message.qpd.qpd_1.value or "LAB-27^IHE"
            qpd.qpd_2 = original_message.qpd.qpd_2.value or "GENEXPERT"
            if original_message.qpd.qpd_3 and len(original_message.qpd.qpd_3) > 0:
                qpd.qpd_3[0] = original_message.qpd.qpd_3[0].value

            # === Fetch matching orders ===
            raw_orders = []

            date_now = datetime.now().strftime("%Y%m%d%H%M%S")

            Analyzer.log.error(Logs.fileline() + f" : specimen_id received = '{specimen_id}'")

            if specimen_id.upper() == "ALL":
                # Retrieve all samples for batch transmission
                raw_orders = Product.getOrdersForLab27()
            else:
                resolved_id = Product.resolveProductId(specimen_id)
                if resolved_id:
                    Analyzer.log.info(Logs.fileline() + f' : INFO specimen_id resolved to id_data = {resolved_id}')
                    single_order = Product.getOrderDetForLab27(specimen_id)
                    raw_orders = [single_order] if single_order else []
                else:
                    Analyzer.log.warning(Logs.fileline() + f' : WARNING specimen_id not found as id_data or code: {specimen_id}')
                    raw_orders = []

            for order in raw_orders:
                try:
                    patient_id = order['pat_code']
                    last_name = order['pat_name']
                    first_name = order['pat_firstname']
                    dob = order['pat_birth'].strftime("%Y%m%d") if order['pat_birth'] else ""
                    sex = 'M' if order['pat_sex'] == 1 else 'F' if order['pat_sex'] == 2 else 'U'
                    specimen = order['code']
                    test_code = order['ana_loinc'] if order['ana_loinc'] else order['ana_code']
                    test_name = order['ana_name']
                    status = "NW"

                    pid = rsp.add_segment("PID")
                    pid.pid_3 = patient_id
                    pid.pid_5 = f"{last_name}^{first_name}"
                    pid.pid_7 = dob
                    pid.pid_8 = sex

                    pv1 = rsp.add_segment("PV1")
                    pv1.pv1_2 = "O"  # Outpatient by default

                    spm = rsp.add_segment("SPM")
                    spm.spm_1 = "1"
                    spm.spm_2 = specimen

                    orc = rsp.add_segment("ORC")
                    orc.orc_1 = status
                    orc.orc_2 = specimen

                    obr = rsp.add_segment("OBR")
                    obr.obr_1 = "1"
                    obr.obr_2 = specimen
                    obr.obr_4 = f"{test_code}^{test_name}"

                except Exception as e:
                    Analyzer.log.error(Logs.fileline() + f" : ERROR processing sample: {str(e)}")

            hl7_str = rsp.to_er7()
            Analyzer.log.info(Logs.fileline() + " : DEBUG Generated RSP^K11:\n" + hl7_str.replace("\r", "\n"))
            return hl7_str

        except Exception as e:
            Analyzer.log.error(Logs.fileline() + f" : ERROR Failed to generate RSP^K11: {str(e)}")
            return None

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
        msa_segment.msa_3 = str(error_message) if error_message else ""

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

    @staticmethod
    def insertAnalyzerResult(ans_ser, code, samp, value, unit, lb_code=None):
        try:
            cursor = DB.cursor()

            cursor.execute('''
                           INSERT INTO analyzer_result (anr_date, anr_ans, anr_code, anr_lb_code, anr_samp, anr_value, anr_unit)
                           VALUES (NOW(), %s, %s, %s, %s, %s, %s)
                           ''', (ans_ser, code, lb_code, samp, value, unit))
            Analyzer.log.info(Logs.fileline() + f" : INSERT analyzer_result OK ({code}={value} {unit})")
            return True
        except mysql.connector.Error as e:
            Analyzer.log.error(Logs.fileline() + " : ERROR insertAnalyzerResult = " + str(e))
            return False

    @staticmethod
    def getAnalyzerResultsBySample(id_samp):
        try:
            cursor = DB.cursor()

            cursor.execute('''
                           SELECT anr_ser, anr_date, anr_ans, anr_code, anr_lb_code, anr_samp, anr_value, anr_unit
                           FROM analyzer_result
                           WHERE anr_samp = %s
                           ORDER BY anr_date DESC
                           ''', (id_samp,))

            results = cursor.fetchall()
            Analyzer.log.info(Logs.fileline() + f" : getAnalyzerResultsBySample({id_samp}) => {len(results)} result(s) found")
            return results

        except mysql.connector.Error as e:
            Analyzer.log.error(Logs.fileline() + f" : ERROR getAnalyzerResultsBySample({id_samp}) => {str(e)}")
            return []
