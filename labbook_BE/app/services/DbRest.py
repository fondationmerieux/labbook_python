# -*- coding:utf-8 -*-
import logging

from datetime import datetime
# from flask import request
from flask_restful import Resource

from app.models.General import compose_ret
from app.models.Constants import *
from app.models.DB import *
from app.models.Logs import Logs


class DbLastStat(Resource):
    log = logging.getLogger('log_services')

    def get(self):
        ret = ''

        stat = DB.getLastStatus()

        if stat and stat['dbs_date']:
            ret = datetime.strftime(stat['dbs_date'], '%Y-%m-%d %H:%M:%S')
            ret = ret + ';' + stat['dbs_stat']

        self.log.info(Logs.fileline() + ' : TRACE DbLastStat')
        return compose_ret(ret, Constants.cst_content_type_json)
