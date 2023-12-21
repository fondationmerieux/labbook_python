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

from app.models.Logs import Logs
from app.models.Various import *
from app.services.GeneralRest import *
from app.services.UserRest import *
from app.services.AnalysisRest import *
from app.services.DbRest import *
from app.services.DeviceRest import *
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
    'es': 'Spanish',
    'ar': 'Arabic',
    'km': 'Khmer',
    'lo': 'Laotian',
    'mg': 'Malagasy',
    'pt': 'Portuguese',
}

# ######################################
# Initializing stuff
# ######################################


def prep_log(logger_name, log_file, level=logging.INFO):
    logger = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(asctime)s : %(message)s')
    fileHandler = WatchedFileHandler(log_file)
    fileHandler.setFormatter(formatter)

    logger.setLevel(level)
    logger.addHandler(fileHandler)


prep_log('log_services', '/home/apps/logs/log_services.log')
prep_log('log_db', '/home/apps/logs/log_db.log')

log = logging.getLogger('log_services')

app = Flask(__name__)
app.config.from_object('default_settings')

config_envvar = 'LOCAL_SETTINGS'

if config_envvar in os.environ:
    print(("Loading local configuration from {}={}".format(config_envvar, os.environ[config_envvar])))
    app.config.from_envvar(config_envvar)

    os.environ['LABBOOK_KEY_DIR']    = Constants.cst_key
    os.environ['LABBOOK_STATUS_DIR'] = Constants.cst_io
    os.environ['LABBOOK_LOG_DIR']    = Constants.cst_log

    log.info(Logs.fileline() + ' : LABBOOK_KEY_DIR=' + str(os.environ['LABBOOK_KEY_DIR']))
    log.info(Logs.fileline() + ' : LABBOOK_STATUS_DIR=' + str(os.environ['LABBOOK_STATUS_DIR']))
    log.info(Logs.fileline() + ' : LABBOOK_LOG_DIR=' + str(os.environ['LABBOOK_LOG_DIR']))

    if app.config['APP_VERSION']:
        log.info(Logs.fileline() + ' : LABBOOK VERSION : ' + str(app.config['APP_VERSION']))

    # check if LABBOOK_USER already exist in os.environ if not use one from Constants
    if 'LABBOOK_USER' in os.environ and os.environ['LABBOOK_USER']:
        log.info(Logs.fileline() + ' : LABBOOK_USER from environ : ' + str(os.environ['LABBOOK_USER']))
    else:
        os.environ['LABBOOK_USER'] = Constants.cst_script_user

    # check if LABBOOK_DB_USER already exist in os.environ if not use one from default_settings
    if 'LABBOOK_DB_USER' in os.environ and os.environ['LABBOOK_DB_USER']:
        app.config['DB_USER'] = os.environ['LABBOOK_DB_USER']
        log.info(Logs.fileline() + ' : LABBOOK_DB_USER from environ')
    else:
        os.environ['LABBOOK_DB_USER'] = app.config['DB_USER']

    # check if LABBOOK_DB_PWD already exist in os.environ if not use one from default_settings
    if 'LABBOOK_DB_PWD' in os.environ and os.environ['LABBOOK_DB_PWD']:
        app.config['DB_PWD'] = os.environ['LABBOOK_DB_PWD']
        log.info(Logs.fileline() + ' : LABBOOK_DB_PWD from environ')
    else:
        os.environ['LABBOOK_DB_PWD'] = app.config['DB_PWD']

    # check if LABBOOK_DB_NAME already exist in os.environ if not use one from default_settings
    if 'LABBOOK_DB_NAME' in os.environ and os.environ['LABBOOK_DB_NAME']:
        app.config['DB_NAME'] = os.environ['LABBOOK_DB_NAME']
        log.info(Logs.fileline() + ' : LABBOOK_DB_NAME from environ')
    else:
        os.environ['LABBOOK_DB_NAME'] = app.config['DB_NAME']

    # check if LABBOOK_DB_HOST already exist in os.environ if not use one from default_settings
    if 'LABBOOK_DB_HOST' in os.environ and os.environ['LABBOOK_DB_HOST']:
        app.config['DB_HOST'] = os.environ['LABBOOK_DB_HOST']
        log.info(Logs.fileline() + ' : LABBOOK_DB_HOST from environ')
    else:
        os.environ['LABBOOK_DB_HOST'] = app.config['DB_HOST']

    log.info(Logs.fileline() + ' : LABBOOK_DB_USER=' + str(os.environ['LABBOOK_DB_USER']))
    log.info(Logs.fileline() + ' : LABBOOK_DB_HOST=' + str(os.environ['LABBOOK_DB_HOST']))
    log.info(Logs.fileline() + ' : LABBOOK_DB_NAME=' + str(os.environ['LABBOOK_DB_NAME']))

    if 'LABBOOK_TEST_OK' in os.environ and os.environ['LABBOOK_TEST_OK']:
        log.info(Logs.fileline() + ' : LABBOOK_TEST_OK=' + str(os.environ['LABBOOK_TEST_OK']))
    if 'LABBOOK_TEST_KO' in os.environ and os.environ['LABBOOK_TEST_KO']:
        log.info(Logs.fileline() + ' : LABBOOK_TEST_KO=' + str(os.environ['LABBOOK_TEST_KO']))
else:
    print(("No local configuration available: {} is undefined in the environment".format(config_envvar)))

# app.config["CACHE_TYPE"] = "null"  # NOTE : Use if flask keep translation in cache


# ######################################
# REST initialization
# ######################################
api = Api(app)


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
api.add_resource(AnalysisExport,      '/services/analysis/export')
api.add_resource(AnalysisImport,      '/services/analysis/import')
api.add_resource(AnalysisList,        '/services/analysis/list')
api.add_resource(AnalysisHistoList,   '/services/analysis/historic/list')
api.add_resource(AnalysisHistoExport, '/services/analysis/historic/export')
api.add_resource(AnalysisHistoDet,    '/services/analysis/historic/details')
api.add_resource(AnalysisReq,         '/services/analysis/list/req/<int:id_rec>/type/<string:type_ana>', '/services/analysis/list/req', '/services/analysis/delete/req/<int:id_req>')
api.add_resource(AnalysisSearch,      '/services/analysis/search/<string:type>')
api.add_resource(AnalysisStatus,      '/services/analysis/status')
api.add_resource(AnalysisVarSearch,   '/services/analysis/variable/search')
api.add_resource(AnalysisTypeProd,    '/services/analysis/type/product/<int:id_type_prod>')
api.add_resource(AnalysisVarAll,      '/services/analysis/variable/all')
api.add_resource(AnalysisVarList,     '/services/analysis/variable/list/<int:id_ana>')
api.add_resource(AnalysisVarDet,      '/services/analysis/variable/det/<int:id_var>')
api.add_resource(AnalyzerDet,         '/services/device/analyzer/det/<int:id_analyzer>')
api.add_resource(AnalyzerFile,        '/services/device/analyzer/file')
api.add_resource(AnalyzerLab29,       '/services/device/analyzer/lab29')
api.add_resource(AnalyzerList,        '/services/device/analyzer/list')
api.add_resource(ConformityList,      '/services/quality/nonconformity/list')
api.add_resource(ConformityDet,       '/services/quality/nonconformity/det/<int:id_item>')
api.add_resource(ConformityExport,    '/services/quality/nonconformity/export')
api.add_resource(ControlList,         '/services/quality/control/list/<string:type_ctrl>')
api.add_resource(ControlDet,          '/services/quality/control/det/<int:id_item>')
api.add_resource(ControlIntExport,    '/services/quality/control/int/export')
api.add_resource(ControlIntResList,   '/services/quality/control/int/res/list/<int:id_ctrl>')
api.add_resource(ControlIntRes,       '/services/quality/control/int/res/<int:id_item>')
api.add_resource(ControlIntResExport, '/services/quality/control/int/res/export/<int:id_ctrl>')
api.add_resource(ControlExtExport,    '/services/quality/control/ext/export')
api.add_resource(ControlExtResList,   '/services/quality/control/ext/res/list/<int:id_ctrl>')
api.add_resource(ControlExtRes,       '/services/quality/control/ext/res/<int:id_item>')
api.add_resource(ControlExtResExport, '/services/quality/control/ext/res/export/<int:id_ctrl>')
api.add_resource(DatasetByName,       '/services/dataset/name/<string:name>')
api.add_resource(DbLastStat,          '/services/db/stat/last/<string:type>')
api.add_resource(DefaultValue,        '/services/default/val/<string:name>', '/services/default/name/<string:name>/val/<string:value>')
api.add_resource(DicoById,            '/services/dico/id/<int:id_data>')
api.add_resource(DictDescr,           '/services/dict/descr/<string:dict_name>')
api.add_resource(DictDet,             '/services/dict/det/<string:dict_name>')
api.add_resource(DictExport,          '/services/dict/export')
api.add_resource(DictImport,          '/services/dict/import/<string:filename>/<int:id_user>')
api.add_resource(DictList,            '/services/dict/list')
api.add_resource(DoctorList,          '/services/doctor/list')
api.add_resource(DoctorDet,           '/services/doctor/det/<int:id_doctor>')
api.add_resource(DoctorExport,        '/services/doctor/export')
api.add_resource(DoctorSearch,        '/services/doctor/search')
api.add_resource(EquipmentList,       '/services/quality/equipment/list')
api.add_resource(EquipmentDet,        '/services/quality/equipment/det/<int:id_item>')
api.add_resource(EquipmentExport,     '/services/quality/equipment/export')
api.add_resource(EquipmentSearch,     '/services/quality/equipment/search')
api.add_resource(ExportCSV,           '/services/export/csv')
api.add_resource(ExportDHIS2,         '/services/export/dhis2')
api.add_resource(ExportWhonet,        '/services/export/whonet')
api.add_resource(FileDocList,         '/services/file/document/list/<string:type_ref>/<int:ref>')
api.add_resource(FileDoc,             '/services/file/document/<string:type_ref>/<int:ref>')
api.add_resource(FileNbManual,        '/services/file/count/manual')
api.add_resource(FileReport,          '/services/file/report/record/<int:id_rec>')
api.add_resource(FileReportCopy,      '/services/file/report/<string:filename>/copy/<string:copy_name>')
api.add_resource(FileReportNbDL,      '/services/file/report/nb_download/<string:filename>')
api.add_resource(FileStorage,         '/services/file/storage')
api.add_resource(InitVersion,         '/services/init/version')
api.add_resource(ListComment,         '/services/quality/list/comment/<int:id_item>')
api.add_resource(ManualList,          '/services/quality/manual/list')
api.add_resource(ManualDet,           '/services/quality/manual/det/<int:id_item>')
api.add_resource(ManualExport,        '/services/quality/manual/export')
api.add_resource(ManualSearch,        '/services/quality/manual/search')
api.add_resource(MeetingList,         '/services/quality/meeting/list')
api.add_resource(MeetingDet,          '/services/quality/meeting/det/<int:id_item>')
api.add_resource(MeetingExport,       '/services/quality/meeting/export')
api.add_resource(NationalityList,     '/services/nationality/list')
api.add_resource(PatientCode,         '/services/patient/generate/code')
api.add_resource(PatientCombine,      '/services/patient/combine/<int:id_pat1>/<int:id_pat2>')
api.add_resource(PatientList,         '/services/patient/list')
api.add_resource(PatientListExport,   '/services/patient/list/export')
api.add_resource(PatientDet,          '/services/patient/det/<int:id_pat>')
api.add_resource(PatientHistoric,     '/services/patient/historic/<int:id_pat>')
api.add_resource(PatientSearch,       '/services/patient/search')
api.add_resource(PdfBill,             '/services/pdf/bill/<int:id_rec>')
api.add_resource(PdfBillList,         '/services/pdf/bill/list')
api.add_resource(PdfReport,           '/services/pdf/report/<int:id_rec>/<string:filename>/<string:template>/<string:reedit>/<int:id_user>')
api.add_resource(PdfReportGeneric,    '/services/pdf/report/generic')
api.add_resource(PdfReportGrouped,    '/services/pdf/report/grouped')
api.add_resource(PdfReportGlobal,     '/services/pdf/report/global')
api.add_resource(PdfSticker,          '/services/pdf/sticker/<string:template>')
api.add_resource(PdfTemplate,         '/services/pdf/template/test/<int:id_item>')
api.add_resource(PdfOutsourced,       '/services/pdf/outsourced/<int:id_rec>/<string:template>/<string:filename>')
api.add_resource(ProcedureList,       '/services/quality/procedure/list')
api.add_resource(ProcedureDet,        '/services/quality/procedure/det/<int:id_item>')
api.add_resource(ProcedureExport,     '/services/quality/procedure/export')
api.add_resource(ProcedureSearch,     '/services/quality/procedure/search')
api.add_resource(ProductDet,          '/services/product/det/<int:id_prod>')
api.add_resource(ProductList,         '/services/product/list')
api.add_resource(ProductReq,          '/services/product/list/req/<int:id_rec>', '/services/product/list/req')
api.add_resource(QualityLastMeeting,  '/services/quality/last/meeting')
api.add_resource(QualityNbNonCompl,   '/services/quality/count/noncompliance/<string:period>')
api.add_resource(RecordComm,          '/services/record/comm/<int:id_rec>')
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
api.add_resource(ReportIndicator,     '/services/report/indicator')
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
api.add_resource(SettingFormDet,      '/services/setting/form/det')
api.add_resource(SettingFormList,     '/services/setting/form/list')
api.add_resource(SettingFuncUnitDet,  '/services/setting/functionnal/unit/det/<int:id_unit>')
api.add_resource(SettingFuncUnit,     '/services/setting/functionnal/unit')
api.add_resource(SettingLinkUnit,     '/services/setting/link/unit/<string:type>/<int:id_unit>')
api.add_resource(SettingLinkByUser,   '/services/setting/link/user/<int:id_user>')
api.add_resource(SettingManual,       '/services/setting/manual')
api.add_resource(SettingManualCat,    '/services/setting/manual/category')
api.add_resource(SettingPref,         '/services/setting/pref/list', '/services/setting/pref/list/<int:id_owner>')
api.add_resource(SettingRecNum,       '/services/setting/record/number')
api.add_resource(SettingReqServices,  '/services/setting/requesting/services')
api.add_resource(SettingReport,       '/services/setting/report')
api.add_resource(SettingStock,        '/services/setting/stock')
api.add_resource(ScriptBackup,        '/services/setting/script/backup/<string:media>')
api.add_resource(ScriptGenkey,        '/services/setting/script/genkey')
api.add_resource(ScriptInitMedia,     '/services/setting/script/initmedia/<string:media>')
api.add_resource(ScriptKeyexist,      '/services/setting/script/keyexist')
api.add_resource(ScriptListarchive,   '/services/setting/script/listarchive/<string:media>')
api.add_resource(ScriptListmedia,     '/services/setting/script/listmedia/<string:type>')
api.add_resource(ScriptProgbackup,    '/services/setting/script/progbackup')
api.add_resource(ScriptRestart,       '/services/setting/script/restart')
api.add_resource(ScriptRestore,       '/services/setting/script/restore')
api.add_resource(ScriptStatus,        '/services/setting/script/status/<string:mode>')
api.add_resource(StaffExport,         '/services/quality/staff/export')
api.add_resource(StockCancelIO,       '/services/quality/stock/cancel/io')
api.add_resource(StockLocalList,      '/services/quality/stock/local/list')
api.add_resource(StockProductDet,     '/services/quality/stock/product/det/<int:id_item>')
api.add_resource(StockProductHist,    '/services/quality/stock/product/history/<int:id_item>/<int:id_local>')
api.add_resource(StockProductList,    '/services/quality/stock/product/list')
api.add_resource(StockProductSearch,  '/services/quality/stock/product/search')
api.add_resource(StockSupplyList,     '/services/quality/stock/supply/list')
api.add_resource(StockSupplyDet,      '/services/quality/stock/supply/det/<int:id_item>')
api.add_resource(StockSupplyMove,     '/services/quality/stock/supply/move')
api.add_resource(StockSupplyRemove,   '/services/quality/stock/supply/remove/<int:id_item>/<int:id_local>')
api.add_resource(StockExport,         '/services/quality/stock/export')
api.add_resource(StockProductsExport, '/services/quality/stock/export/products')
api.add_resource(StockSuppliesExport, '/services/quality/stock/export/supplies')
api.add_resource(StockUsesExport,     '/services/quality/stock/export/uses')
api.add_resource(StockList,           '/services/quality/stock/list')
api.add_resource(StockListDet,        '/services/quality/stock/list/det/<int:id_item>/<int:id_local>')
api.add_resource(StockUse,            '/services/quality/stock/use/<int:prs_ser>', '/services/quality/stock/use')
api.add_resource(SupplierDet,         '/services/quality/supplier/det/<int:id_item>')
api.add_resource(SupplierExport,      '/services/quality/supplier/export')
api.add_resource(SupplierList,        '/services/quality/supplier/list')
api.add_resource(SupplierSearch,      '/services/quality/supplier/search')
api.add_resource(TemplateDet,         '/services/setting/template/det/<int:id_item>')
api.add_resource(TemplateList,        '/services/setting/template/list', '/services/setting/template/list/<string:type>')
api.add_resource(TraceDownload,       '/services/quality/trace/download')
api.add_resource(TraceList,           '/services/quality/trace/list/<string:type_trace>')
api.add_resource(UserAccess,          '/services/user/access')
api.add_resource(UserByLogin,         '/services/user/login/<string:login>')
api.add_resource(UserConnExport,      '/services/user/connection/export')
api.add_resource(UserCount,           '/services/user/count')
api.add_resource(UserDet,             '/services/user/det/<int:id_user>')
api.add_resource(UserExport,          '/services/user/export')
api.add_resource(UserIdentList,       '/services/user/ident/list')
api.add_resource(UserImport,          '/services/user/import/<string:filename>/<int:id_user>')
api.add_resource(UserList,            '/services/user/list')
api.add_resource(UserStaffDet,        '/services/user/staff/det/<int:id_user>')
api.add_resource(UserRights,          '/services/user/rights/<string:role>')
api.add_resource(UserRoleList,        '/services/user/role/list', '/services/user/role/list/<string:type>')
api.add_resource(UserStatus,          '/services/user/status')
api.add_resource(UserSearch,          '/services/user/search')
api.add_resource(UserPassword,        '/services/user/password')
api.add_resource(ZipCityAdd,          '/services/setting/zipcity/add/<string:filename>')
api.add_resource(ZipCityDelAll,       '/services/setting/zipcity/delete/all')
api.add_resource(ZipCityDet,          '/services/setting/zipcity/det/<int:id_item>')
api.add_resource(ZipCityList,         '/services/setting/zipcity/list')
api.add_resource(ZipCitySearch,       '/services/setting/zipcity/search')

log.info(Logs.fileline() + ' : LABBOOK_BE is ready')

# if __name__ == "__main__":
#    app.run()
