# -*- coding:utf-8 -*-
import logging
import mysql.connector
import os
import toml
import hl7apy

from datetime import datetime
from hl7apy.core import Message, Segment
from hl7apy.parser import parse_message

from app.models.Constants import *
from app.models.DB import DB
from app.models.Logs import Logs
from app.models.Patient import Patient
from app.models.Product import Product
from app.models.Record import Record
from app.models.Result import Result


class Analyzer:
    log = logging.getLogger('log_db')

    @staticmethod
    def getAnalyzerList():
        cursor = DB.cursor()

        req = ('select ans_ser, ans_rank, ans_name, ans_id '
               'from analyzer_setting '
               'order by ans_rank')

        cursor.execute(req,)

        return cursor.fetchall()

    @staticmethod
    def getAnalyzerDet(id_analyzer):
        cursor = DB.cursor()

        req = ('select ans_ser, ans_user, ans_name, ans_id, ans_lab28, ans_mapping, ans_filename '
               'from analyzer_setting '
               'where ans_ser=%s')

        cursor.execute(req, (id_analyzer,))

        return cursor.fetchone()

    @staticmethod
    def insertAnalyzerDet(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into analyzer_setting '
                           '(ans_date, ans_user, ans_rank, ans_name, ans_id, ans_lab28, ans_mapping, ans_filename) '
                            'values (NOW(), %(id_user)s, %(rank)s, %(name)s, %(id)s, %(lab28)s, %(mapping)s, '
                            '%(filename)s)', params)

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
                   'ans_id=%(id)s, ans_lab28=%(lab28)s, ans_mapping=%(mapping)s, ans_filename=%(filename)s '
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

        l_files = [f for f in os.listdir(path) if f.endswith(".toml") and os.path.isfile(os.path.join(path, f))]

        Analyzer.log.info(Logs.fileline() + ' DEBUG l_files= ' + str(l_files))

        # parse files
        for filename in l_files:
            filepath = os.path.join(path, filename)

            config = toml.load(filepath)

            analyzer = {}

            analyzer['filename'] = filename
            analyzer['version']  = config['version']
            analyzer['brand']    = config['analyzer']['brand']
            analyzer['name']     = config['analyzer']['name']
            analyzer['id']       = config['analyzer']['id']
            analyzer['lab28']    = config['analyzer']['lab28']
            analyzer['mapping']  = config['analyzer']['mapping']
            analyzer['display']  = str(analyzer['brand']) + ' - ' + str(analyzer['name']) + ' | Id : ' + str(analyzer['id'])

            ret.append(analyzer)

        Analyzer.log.info(Logs.fileline() + ' DEBUG ret= ' + str(ret))

        return ret

    @staticmethod
    def listTaskLab28(stat):
        cursor = DB.cursor()

        cond = ' anl_stat = "' + stat + '"'

        if not stat:
            cond = ' anl_stat != NULL'

        req = ('select anl_ser, anl_date, anl_date_upd, anl_id_samp, anl_stat, anl_OML_O33, anl_ORL_O34, anl_ans '
               'from analyzer_lab28 '
               'where ' + cond + ' order by anl_date')

        cursor.execute(req)

        return cursor.fetchall()

    @staticmethod
    def buildLab28(id_samp):
        date_now = datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")

        # get specimen details
        samp = Product.getProductDet(id_samp)

        if not samp:
            Analyzer.log.error(Logs.fileline() + ' ERROR buildLab28 getProductDet for id_samp=' + str(id_samp))

        id_rec = samp['id_rec']

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

        if pat['ddn']:
            pat_birth = datetime.strftime(pat['ddn'], "%Y%m%d%H%M%S")
        else:
            pat_birth = ''

        if pat['sexe'] == 1:
            pat_sex = 'M'
        elif pat['sexe'] == 2:
            pat_sex = 'F'

        l_analyzer = Analyzer.getAnalyzerList()

        for analyzer in l_analyzer:
            # Save OML33 task for one analyzer
            ret = Analyzer.insertLab28(ans_ser=analyzer['ans_ser'], id_samp=id_samp, stat=Constants.cst_stat_init, OML_O33='', )

            if not ret:
                Analyzer.log.error(Logs.fileline() + ' ERROR insertLab28 for id_analyzer=' + str(analyzer['ans_ser']) + 'and id_samp=' + str(id_samp))

            else:
                id_task = ret

                # Build OML_O33
                msg = Message("OML_O33", version="2.5.1")

                # Message segment
                msg.msh.msh_1  = "|"
                msg.msh.msh_2  = "^~\\&"
                msg.msh.msh_3  = "LabBook"
                msg.msh.msh_5  = "LabBook Connect"
                msg.msh.msh_7  = date_now
                msg.msh.msh_9  = "OML^O33^OML_O33"  # Message type, cf line page 44 from IHE_PaLM_TF_Vol2b.pdf
                msg.msh.msh_10 = str(id_task)       # Message control ID, sending back by receiving system
                msg.msh.msh_11 = "P"                # Processing ID, "D"ebugging, "P"roduction, "T"raining.
                msg.msh.msh_12 = "2.5.1"            # HL7 version
                msg.msh.msh_18 = "UTF-8"            # Character set
                msg.msh.msh_21 = "LAB-28^IHE"       # Message profile identifier

                try:
                    msg.msh.validate()
                    Analyzer.log.error(Logs.fileline() + ' DEBUG MSH Validated')
                except Exception as e:
                    Analyzer.log.error(Logs.fileline() + ' ERROR e : ' + str(e))

                # Patient group
                msg.add_group('OML_O33_PATIENT')

                # Patient segment
                msg.oml_o33_patient.add_segment('PID')
                msg.oml_o33_patient.pid.pid_1  = "1"                  # ID of this transaction
                msg.oml_o33_patient.pid.pid_2  = pat['code']          # Patient ID
                msg.oml_o33_patient.pid.pid_3  = pat['code_patient']  # Laboratory code for patient
                msg.oml_o33_patient.pid.pid_4  = str(pat['id_data'])  # Alternative ID, serial from database
                msg.oml_o33_patient.pid.pid_5  = pat['nom'] + '^' + pat['prenom'] + '^L'  # Family name^Given name^Type. "L"egal name
                msg.oml_o33_patient.pid.pid_6  = pat['nom_jf']        # Maiden name
                msg.oml_o33_patient.pid.pid_7  = pat_birth            # Datetime of birth.
                msg.oml_o33_patient.pid.pid_8  = pat_sex              # Sex : "F"emale, "M"ale, "O"ther, "U"nknown, "A"mbigous, "N"ot app
                msg.oml_o33_patient.pid.pid_11 = "Street^Other^City^Zip"  # Address
                msg.oml_o33_patient.pid.pid_13 = ""                   # Home phone number and email
                msg.oml_o33_patient.pid.pid_13 = ""                   # Record number
                msg.oml_o33_patient.pid.pid_28 = ""                   # Nationality

                """
                # Patient visit group
                msg.oml_o33_patient.pid.add_group('OML_O33_PATIENT_VISIT')

                # Patient visit segment
                msg.oml_o33_patient.oml_o33_patient_visit.add_segment('PV1')
                msg.oml_o33_patient.oml_o33_patient_visit.pv1.pv1_1 = "1"
                msg.oml_o33_patient.oml_o33_patient_visit.pv1.pv1_2 = "U"  # patient class unknown
                """

                try:
                    msg.oml_o33_patient.pid.validate()
                    Analyzer.log.error(Logs.fileline() + ' DEBUG PID Validated')
                except Exception as e:
                    Analyzer.log.error(Logs.fileline() + ' ERROR e : ' + str(e))

                # Specimen group
                msg.add_group('OML_O33_SPECIMEN')

                # Specimen segment
                msg.oml_o33_specimen.add_segment('spm')
                msg.oml_o33_specimen.spm.spm_1  = "1"
                msg.oml_o33_specimen.spm.spm_2  = str(id_samp)  # specimen ID
                msg.oml_o33_specimen.spm.spm_4  = str(id_samp) + "^type^coding_system"   # type specimen
                msg.oml_o33_specimen.spm.spm_11 = "L"  # Specimen role, "Q" QC AWOS, "P" patient AWOS, "L" pooled AWOS, "U" negative query resp

                try:
                    msg.oml_o33_specimen.spm.validate()
                    Analyzer.log.error(Logs.fileline() + ' DEBUG SPM Validated')
                except Exception as e:
                    Analyzer.log.error(Logs.fileline() + ' ERROR e : ' + str(e))

                # Order group
                msg.oml_o33_specimen.add_group('OML_O33_ORDER')

                # Order segment
                msg.oml_o33_specimen.oml_o33_order.add_segment('ORC')
                msg.oml_o33_specimen.oml_o33_order.orc.orc_1 = "NW"          # order control code : NW (new order), CA (cancel)
                msg.oml_o33_specimen.oml_o33_order.orc.orc_2 = str(id_task)  # Placer order number. One order by OML^O33 so same number of msh_10

                try:
                    msg.oml_o33_specimen.oml_o33_order.orc.validate()
                    Analyzer.log.error(Logs.fileline() + ' DEBUG ORC Validated')
                except Exception as e:
                    Analyzer.log.error(Logs.fileline() + ' ERROR e : ' + str(e))

                # Timing group
                msg.oml_o33_specimen.oml_o33_order.add_group('OML_O33_TIMING')

                # Timing quantity segment
                msg.oml_o33_specimen.oml_o33_order.oml_o33_timing.add_segment('TQ1')
                msg.oml_o33_specimen.oml_o33_order.oml_o33_timing.tq1.tq1_1 = "1"
                msg.oml_o33_specimen.oml_o33_order.oml_o33_timing.tq1.tq1_9 = "R"  # priority : "R"outine, "S"tat with highest priority

                try:
                    msg.oml_o33_specimen.oml_o33_order.oml_o33_timing.tq1.validate()
                    Analyzer.log.error(Logs.fileline() + ' DEBUG TQ1 Validated')
                except Exception as e:
                    Analyzer.log.error(Logs.fileline() + ' ERROR e : ' + str(e))

                # observation request group
                msg.oml_o33_specimen.oml_o33_order.add_group('OML_O33_OBSERVATION_REQUEST')

                # Observation request segment
                msg.oml_o33_specimen.oml_o33_order.add_segment('OBR')
                msg.oml_o33_specimen.oml_o33_order.obr.obr_1  = "1"                # ID OBR
                msg.oml_o33_specimen.oml_o33_order.obr.obr_2  = str(id_task) + "_1"   # Place order number. Same ad orc_2
                msg.oml_o33_specimen.oml_o33_order.obr.obr_4  = "CODE_TEST^Blood Group Analysis"  # Name of observation aka name of test

                try:
                    msg.oml_o33_specimen.oml_o33_order.obr.validate()
                    Analyzer.log.error(Logs.fileline() + ' DEBUG OBR Validated')
                except Exception as e:
                    Analyzer.log.error(Logs.fileline() + ' ERROR e : ' + str(e))

                # Convertir le message en une chaîne
                hl7_string = msg.to_er7()

                Analyzer.log.info(Logs.fileline() + ' DEBUG buildLab28 hl7_string=' + str(hl7_string))

                # update task lab28 with hl7 message
                ret = Analyzer.updateLab28_OML_O33(id_task=id_task, stat=Constants.cst_stat_pending, OML_O33=str(hl7_string))

                if not ret:
                    Analyzer.log.error(Logs.fileline() + ' ERROR updateLab28 for id_task=' + str(id_task))
                    return False

        return True

    @staticmethod
    def insertLab28(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into analyzer_lab28 '
                           '(anl_date, anl_id_samp, anl_stat, anl_OML_O33, anl_ans) '
                            'values (NOW(), %(id_samp)s, %(stat)s, %(OML_O33)s, %(ans_ser)s)', params)

            Analyzer.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Analyzer.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def updateLab28_OML_O33(**params):
        try:
            cursor = DB.cursor()

            Analyzer.log.error(Logs.fileline() + 'DEBUG params=' + str(params))

            req = ('update analyzer_lab28 set anl_date_upd=NOW(), anl_stat=%(stat)s, anl_OML_O33=%(OML_O33)s '
                   'where anl_ser=%(id_task)s')

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

            req = ('update analyzer_lab28 set anl_date_upd=NOW(), anl_stat=%(stat)s, anl_ORL_O34=%(ORL_O34)s '
                   'where anl_ser=%(id_task)s')

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

        Result.updateResultDemo()

        return True
