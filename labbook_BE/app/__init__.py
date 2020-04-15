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
from app.services.ProductRest import *
from app.services.DoctorRest import *
from app.services.PatientRest import *
from app.services.PdfRest import *
from app.services.RecordRest import *
from app.services.ResultRest import *

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

api.add_resource(Test,               '/services/test')
api.add_resource(DicoList,           '/services/dico/list/<string:dico_name>')
api.add_resource(DicoById,           '/services/dico/id/<int:id_data>')
api.add_resource(DefaultValue,       '/services/default/val/<string:name>')
api.add_resource(UserDet,            '/services/user/login/<string:login>')
api.add_resource(AnalysisSearch,     '/services/analysis/search/<int:id_group>')
api.add_resource(AnalysisDet,        '/services/analysis/det/<int:id_ana>')
api.add_resource(AnalysisTypeProd,   '/services/analysis/type/product/<int:id_type_prod>')
api.add_resource(AnalysisReq,        '/services/analysis/list/req/<int:id_rec>/type/<string:type_ana>', '/services/analysis/list/req')
api.add_resource(ProductReq,         '/services/product/list/req/<int:id_rec>', '/services/product/list/req')
api.add_resource(DoctorSearch,       '/services/doctor/search/<int:id_group>')
api.add_resource(DoctorDet,          '/services/doctor/det/<int:id_doctor>')
api.add_resource(PatientSearch,      '/services/patient/search')
api.add_resource(PatientDet,         '/services/patient/det/<int:id_pat>')
api.add_resource(PatientCode,        '/services/patient/generate/code')
api.add_resource(PdfBarcode,         '/services/pdf/barcode/num/<string:num>')
api.add_resource(RecordList,         '/services/record/list/<int:id_group>')
api.add_resource(RecordDet,          '/services/record/det/<int:id_rec>')
api.add_resource(RecordStat,         '/services/record/stat/<int:id_rec>')
api.add_resource(RecordTypeNumber,   '/services/record/type/number')
api.add_resource(ResultValue,        '/services/result/list/value')
api.add_resource(ResultList,         '/services/result/list')
api.add_resource(ResultRecord,       '/services/result/record/<int:id_rec>')
api.add_resource(ResultCreate,       '/services/result/create/<int:id_rec>')

# if __name__ == "__main__":
#    app.run()
