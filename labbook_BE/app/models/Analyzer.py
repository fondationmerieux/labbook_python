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
from app.models.Patient import Patient
from app.models.Product import Product
from app.models.Record import Record
from app.models.Result import Result
from app.models.Various import Various


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

        req = ('select ans_ser, ans_user, ans_name, ans_id, ans_connect, ans_mapping, ans_filename '
               'from analyzer_setting '
               'where ans_ser=%s')

        cursor.execute(req, (id_analyzer,))

        return cursor.fetchone()

    @staticmethod
    def insertAnalyzerDet(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into analyzer_setting '
                           '(ans_date, ans_user, ans_rank, ans_name, ans_id, ans_connect, ans_mapping, ans_filename) '
                            'values (NOW(), %(id_user)s, %(rank)s, %(name)s, %(id)s, %(connect)s, %(mapping)s, '
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
                   'ans_id=%(id)s, ans_connect=%(connect)s, ans_mapping=%(mapping)s, ans_filename=%(filename)s '
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
                msg.msh.msh_4  = str(lab_name)
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

                Analyzer.log.info(Logs.fileline() + f" DEBUG : Groupe ajouté -> OML_O33_SPECIMEN ({len(msg.children)} enfants dans msg)")

                # Specimen segment
                spm_segment = specimen_group.add_segment('SPM')
                Analyzer.log.info(Logs.fileline() + f" DEBUG : Segment ajouté -> SPM ({len(specimen_group.children)} enfants dans SPECIMEN)")
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
                Analyzer.log.info(Logs.fileline() + f" DEBUG : Groupe ajouté -> OML_O33_ORDER ({len(specimen_group.children)} enfants dans SPECIMEN)")

                # Order segment
                orc_segment = order_group.add_segment('ORC')
                Analyzer.log.info(Logs.fileline() + f" DEBUG : Segment ajouté -> ORC ({len(order_group.children)} enfants dans ORDER)")
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
                Analyzer.log.info(Logs.fileline() + f" DEBUG : Groupe ajouté -> OML_O33_TIMING ({len(order_group.children)} enfants dans ORDER)")
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
                Analyzer.log.info(Logs.fileline() + f" DEBUG : Groupe ajouté -> OML_O33_OBSERVATION_REQUEST ({len(order_group.children)} enfants dans ORDER)")

                # Observation request segment
                obr_segment = observation_request_group.add_segment('OBR')
                obr_segment.obr_1  = "1"             # ID OBR
                obr_segment.obr_2  = f"{id_task}_1"  # Place order number. Same ad orc_2
                obr_segment.obr_4  = "B157^Blood Group Analysis"  # Code and Name of observation aka name of test.
                # TODO code^ana_name

                try:
                    obr_segment.validate()
                    Analyzer.log.info(Logs.fileline() + ' DEBUG OBR Validated')
                except Exception as e:
                    Analyzer.log.error(Logs.fileline() + ' ERROR e : ' + str(e))

                Analyzer.log.info(Logs.fileline() + " INFO : Vérification détaillée des groupes et segments dans le message HL7 :")
                Analyzer.log_hl7_structure(msg)
                Analyzer.log.info(Logs.fileline() + f" DEBUG : Nombre de segments dans msg.children = {len(msg.children)}")

                # Convertir le message en une chaîne
                hl7_string = msg.to_er7()

                str_hl7_string = hl7_string

                Analyzer.log.info(Logs.fileline() + ' DEBUG buildLab28 hl7_string=\n' + str_hl7_string.replace('\r', '\n'))

                # update task lab28 with hl7 message
                ret = Analyzer.updateLab28_OML_O33(id_task=id_task, stat=Constants.cst_stat_pending, OML_O33=str(hl7_string))

                if not ret:
                    Analyzer.log.error(Logs.fileline() + ' ERROR updateLab28 for id_task=' + str(id_task))
                    return False

        return True

    @staticmethod
    def log_hl7_structure(msg, level=0):
        """
        Fonction récursive pour afficher la structure du message HL7 avec indentation.
        :param msg: Objet Message HL7apy
        :param level: Niveau d'indentation (0 = racine)
        """
        indent = "  " * level  # Définir l'indentation selon le niveau
        for child in msg.children:
            Analyzer.log.info(Logs.fileline() + f"{indent}INFO : Groupe/Segment détecté -> {child.name}")
            if hasattr(child, "to_er7"):  # Vérifier si le segment peut être affiché
                Analyzer.log.info(Logs.fileline() + f"{indent}  └── Valeur ER7 : {child.to_er7()}")

            # Vérifier s'il a des enfants et les afficher avec un niveau supplémentaire
            if hasattr(child, "children"):
                Analyzer.log_hl7_structure(child, level + 1)  # Appel récursif pour les sous-niveaux

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

            Analyzer.log.info(Logs.fileline() + ' : DEBUG params=' + str(params))

            params["OML_O33"] = params["OML_O33"].replace("\r", "\\r")

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
