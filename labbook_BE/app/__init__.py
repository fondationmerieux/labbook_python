#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@project_name : Labbook Back End

@author: Alexandre CHARLES <ac@aegle.fr>
@creation_date: 20/11/2019
"""

# ###########################################
#   Imports
# ###########################################

import os
import logging

from logging.handlers import WatchedFileHandler

from flask import Flask
from flask_restful import Api
from flask_restful_swagger import swagger

from app.models.Logs import Logs
from app.services.GeneralRest import *
from app.services.UserRest import *
from app.services.AnalysisRest import *
from app.services.ExportRest import *
from app.services.ProductRest import *
from app.services.DoctorRest import *
from app.services.DictRest import *
from app.services.FileRest import *
from app.services.PatientRest import *
from app.services.PdfRest import *
from app.services.QualityRest import *
from app.services.RecordRest import *
from app.services.ReportRest import *
from app.services.ResultRest import *
from app.services.SettingRest import *

LANGUAGES = {
    'fr_FR': 'French',
    'en_GB': 'English',
    'en_US': 'English',
}

# ######################################
# Initializing stuff
# ######################################


def prep_log(logger_nom, log_fich, niveau=logging.INFO):
    l = logging.getLogger(logger_nom)
    formatter = logging.Formatter('%(asctime)s : %(message)s')
    fileHandler = WatchedFileHandler(log_fich)
    fileHandler.setFormatter(formatter)

    l.setLevel(niveau)
    l.addHandler(fileHandler)

prep_log('log_services', r'../logs/log_services.log')
prep_log('log_db', r'../logs/log_db.log')

log = logging.getLogger('log_services')

app = Flask(__name__)
app.config.from_object('default_settings')

config_envvar = 'LOCAL_SETTINGS'

if config_envvar in os.environ:
    print("Loading local configuration from {}={}".format(config_envvar, os.environ[config_envvar]))
    app.config.from_envvar(config_envvar)

    os.environ['LABBOOK_KEY_DIR']    = Constants.cst_key
    os.environ['LABBOOK_STATUS_DIR'] = Constants.cst_io
    os.environ['LABBOOK_LOG_DIR']    = Constants.cst_log
    os.environ['LABBOOK_USER']       = Constants.cst_script_user

    log.info(Logs.fileline() + ' : LABBOOK_KEY_DIR=' + str(os.environ['LABBOOK_KEY_DIR']))
    log.info(Logs.fileline() + ' : LABBOOK_STATUS_DIR=' + str(os.environ['LABBOOK_STATUS_DIR']))
    log.info(Logs.fileline() + ' : LABBOOK_LOG_DIR=' + str(os.environ['LABBOOK_LOG_DIR']))
    log.info(Logs.fileline() + ' : LABBOOK_USER=' + str(os.environ['LABBOOK_USER']))

    # Put in os.environ DB variables
    os.environ['LABBOOK_DB_USER'] = app.config['DB_USER']
    os.environ['LABBOOK_DB_PWD']  = app.config['DB_PWD']
    os.environ['LABBOOK_DB_HOST'] = app.config['DB_HOST']
    os.environ['LABBOOK_DB_NAME'] = app.config['DB_NAME']

    log.info(Logs.fileline() + ' : LABBOOK_DB_USER=' + str(os.environ['LABBOOK_DB_USER']))
    log.info(Logs.fileline() + ' : LABBOOK_DB_HOST=' + str(os.environ['LABBOOK_DB_HOST']))
    log.info(Logs.fileline() + ' : LABBOOK_DB_NAME=' + str(os.environ['LABBOOK_DB_NAME']))
else:
    print("No local configuration available: {} is undefined in the environment".format(config_envvar))

# ######################################
# REST initialization
# ######################################
api = swagger.docs(Api(app), apiVersion='0.1')


@app.route("/")
def index():
    log.info(Logs.fileline() + ' : TRACE Labbook BACK END')
    return "Hello World! Labbook BACK END"

# ######################################
# REST pages
# ######################################

api.add_resource(Test,                '/services/test')
api.add_resource(AnalysisCode,        '/services/analysis/code/check/<string:code>')
api.add_resource(AnalysisDet,         '/services/analysis/det/<int:id_ana>')
api.add_resource(AnalysisList,        '/services/analysis/list')
api.add_resource(AnalysisHistoList,   '/services/analysis/historic/list')
api.add_resource(AnalysisHistoExport, '/services/analysis/historic/export')
api.add_resource(AnalysisHistoDet,    '/services/analysis/historic/details')
api.add_resource(AnalysisReq,         '/services/analysis/list/req/<int:id_rec>/type/<string:type_ana>', '/services/analysis/list/req')
api.add_resource(AnalysisSearch,      '/services/analysis/search/<string:type>')
api.add_resource(AnalysisVarSearch,   '/services/analysis/variable/search')
api.add_resource(AnalysisTypeProd,    '/services/analysis/type/product/<int:id_type_prod>')
api.add_resource(AnalysisVarList,     '/services/analysis/variable/list/<int:id_ana>')
api.add_resource(AnalysisVarDet,      '/services/analysis/variable/det/<int:id_var>')
api.add_resource(ConformityList,      '/services/quality/nonconformity/list')
api.add_resource(ConformityDet,       '/services/quality/nonconformity/det/<int:id_item>')
api.add_resource(ConformityExport,    '/services/quality/nonconformity/export')
api.add_resource(DefaultValue,        '/services/default/val/<string:name>', '/services/default/name/<string:name>/val/<string:value>')
api.add_resource(DicoById,            '/services/dico/id/<int:id_data>')
api.add_resource(DictDet,             '/services/dict/det/<string:dict_name>')
api.add_resource(DictList,            '/services/dict/list')
api.add_resource(DoctorList,          '/services/doctor/list')
api.add_resource(DoctorDet,           '/services/doctor/det/<int:id_doctor>')
api.add_resource(DoctorExport,        '/services/doctor/export')
api.add_resource(DoctorSearch,        '/services/doctor/search/<int:id_group>')
api.add_resource(EquipmentList,       '/services/quality/equipment/list')
api.add_resource(EquipmentDet,        '/services/quality/equipment/det/<int:id_item>')
api.add_resource(EquipmentExport,     '/services/quality/equipment/export')
api.add_resource(EquipmentSearch,     '/services/quality/equipment/search')
api.add_resource(ExportCSV,           '/services/export/csv')
api.add_resource(ExportWhonet,        '/services/export/whonet')
api.add_resource(FileDocList,         '/services/file/document/list/<string:type_ref>/<int:ref>')
api.add_resource(FileDoc,             '/services/file/document/<string:type_ref>/<int:ref>')
api.add_resource(FileNbManual,        '/services/file/count/manual')
api.add_resource(FileReport,          '/services/file/report/record/<int:id_rec>')
api.add_resource(FileStorage,         '/services/file/storage/<int:id_group>')
api.add_resource(ManualList,          '/services/quality/manual/list')
api.add_resource(ManualDet,           '/services/quality/manual/det/<int:id_item>')
api.add_resource(ManualExport,        '/services/quality/manual/export')
api.add_resource(ManualSearch,        '/services/quality/manual/search')
api.add_resource(MeetingList,         '/services/quality/meeting/list')
api.add_resource(MeetingDet,          '/services/quality/meeting/det/<int:id_item>')
api.add_resource(MeetingExport,       '/services/quality/meeting/export')
api.add_resource(PatientCode,         '/services/patient/generate/code')
api.add_resource(PatientCombine,      '/services/patient/combine/<int:id_pat1>/<int:id_pat2>')
api.add_resource(PatientList,         '/services/patient/list')
api.add_resource(PatientListExport,   '/services/patient/list/export')
api.add_resource(PatientDet,          '/services/patient/det/<int:id_pat>')
api.add_resource(PatientHistoric,     '/services/patient/historic/<int:id_pat>')
api.add_resource(PatientSearch,       '/services/patient/search')
api.add_resource(PdfBarcode,          '/services/pdf/barcode/num/<string:num>')
api.add_resource(PdfBill,             '/services/pdf/bill/<int:id_rec>')
api.add_resource(PdfBillList,         '/services/pdf/bill/list')
api.add_resource(PdfReport,           '/services/pdf/report/<int:id_rec>/<string:filename>')
api.add_resource(PdfReportGeneric,    '/services/pdf/report/generic')
api.add_resource(ProcedureList,       '/services/quality/procedure/list')
api.add_resource(ProcedureDet,        '/services/quality/procedure/det/<int:id_item>')
api.add_resource(ProcedureExport,     '/services/quality/procedure/export')
api.add_resource(ProcedureSearch,     '/services/quality/procedure/search')
api.add_resource(ProductDet,          '/services/product/det/<int:id_prod>')
api.add_resource(ProductList,         '/services/product/list')
api.add_resource(ProductReq,          '/services/product/list/req/<int:id_rec>', '/services/product/list/req')
api.add_resource(QualityLastMeeting,  '/services/quality/last/meeting')
api.add_resource(QualityNbNonCompl,   '/services/quality/count/noncompliance/<string:period>')
api.add_resource(RecordDet,           '/services/record/det/<int:id_rec>')
api.add_resource(RecordLast,          '/services/record/last')
api.add_resource(RecordList,          '/services/record/list/<int:id_pres>')
api.add_resource(RecordListAna,       '/services/record/list/analysis/<int:id_rec>')
api.add_resource(RecordNext,          '/services/record/next/<int:id_rec>')
api.add_resource(RecordNbEmer,        '/services/record/count/emergency')
api.add_resource(RecordStat,          '/services/record/stat/<int:id_rec>')
api.add_resource(RecordNbRecTech,     '/services/record/count/technician')
api.add_resource(RecordNbRecBio,      '/services/record/count/biologist')
api.add_resource(RecordNbRec,         '/services/record/count')
api.add_resource(RecordNbRecToday,    '/services/record/count/today')
api.add_resource(ReportActivity,      '/services/report/activity')
api.add_resource(ReportBilling,       '/services/report/billing')
api.add_resource(ReportEpidemio,      '/services/report/epidemio')
api.add_resource(ReportStat,          '/services/report/stat')
api.add_resource(ReportToday,         '/services/report/today')
api.add_resource(ReportTodayExport,   '/services/report/today/export')
api.add_resource(ResultCancel,        '/services/result/cancel/<int:id_rec>')
api.add_resource(ResultCreate,        '/services/result/create/<int:id_rec>')
api.add_resource(ResultHisto,         '/services/result/history/<int:id_res>')
api.add_resource(ResultList,          '/services/result/list')
api.add_resource(ResultRecord,        '/services/result/record/<int:id_rec>')
api.add_resource(ResultReset,         '/services/result/reset/<int:id_rec>')
api.add_resource(ResultValid,         '/services/result/valid/<string:type_valid>/<int:id_rec>')
api.add_resource(ResultValue,         '/services/result/list/value')
api.add_resource(SettingAgeInterval,  '/services/setting/age/interval')
api.add_resource(SettingBackup,       '/services/setting/backup')
api.add_resource(SettingPref,         '/services/setting/pref/list', '/services/setting/pref/list/<int:id_owner>')
api.add_resource(SettingRecNum,       '/services/setting/record/number')
api.add_resource(SettingReport,       '/services/setting/report')
api.add_resource(SettingSticker,      '/services/setting/sticker', '/services/setting/sticker/<int:sts_ser>')
api.add_resource(ScriptBackup,        '/services/setting/script/backup/<string:media>')
api.add_resource(ScriptGenkey,        '/services/setting/script/genkey')
api.add_resource(ScriptInitmedia,     '/services/setting/script/initmedia/<string:media>')
api.add_resource(ScriptKeyexist,      '/services/setting/script/keyexist')
api.add_resource(ScriptListarchive,   '/services/setting/script/listarchive/<string:media>')
api.add_resource(ScriptListmedia,     '/services/setting/script/listmedia/<string:type>')
api.add_resource(ScriptProgbackup,    '/services/setting/script/progbackup')
api.add_resource(ScriptRestart,       '/services/setting/script/restart')
api.add_resource(ScriptRestore,       '/services/setting/script/restore')
api.add_resource(StaffExport,         '/services/quality/staff/export')
api.add_resource(StockProductDet,     '/services/quality/stock/product/det/<int:id_item>')
api.add_resource(StockProductHist,    '/services/quality/stock/product/history/<int:id_item>')
api.add_resource(StockProductSearch,  '/services/quality/stock/product/search')
api.add_resource(StockSupplyDet,      '/services/quality/stock/supply/det/<int:id_item>')
api.add_resource(StockExport,         '/services/quality/stock/export')
api.add_resource(StockList,           '/services/quality/stock/list')
api.add_resource(StockListDet,        '/services/quality/stock/list/det/<int:id_item>')
api.add_resource(StockUse,            '/services/quality/stock/use')
api.add_resource(SupplierDet,         '/services/quality/supplier/det/<int:id_item>')
api.add_resource(SupplierExport,      '/services/quality/supplier/export')
api.add_resource(SupplierList,        '/services/quality/supplier/list')
api.add_resource(SupplierSearch,      '/services/quality/supplier/search')
api.add_resource(UserAccess,          '/services/user/access')
api.add_resource(UserByLogin,         '/services/user/login/<string:login>')
api.add_resource(UserByRole,          '/services/user/role/<int:id_role>')
api.add_resource(UserConnExport,      '/services/user/connection/export')
api.add_resource(UserCount,           '/services/user/count')
api.add_resource(UserDet,             '/services/user/det/<int:id_user>')
api.add_resource(UserList,            '/services/user/list/<int:id_group>')
api.add_resource(UserStaffDet,        '/services/user/staff/det/<int:id_user>')
api.add_resource(UserRights,          '/services/user/rights/<string:role>')
api.add_resource(UserStatus,          '/services/user/status')
api.add_resource(UserSearch,          '/services/user/search')
api.add_resource(UserPassword,        '/services/user/password')

# if __name__ == "__main__":
#    app.run()
