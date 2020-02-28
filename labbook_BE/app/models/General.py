# import informixdb
import logging
import mysql.connector

from app.models.Constants import *
from app.models.BDD import BDD
from app.models.Logs import Logs


'''
def set_locale(lang, utf8=False):
    from flask import current_app
    current_app.config['BABEL_DEFAULT_LOCALE'] = lang

    import locale
    if lang == 'fr':
        if utf8:
            locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
        else:
            locale.setlocale(locale.LC_TIME, 'fr_FR')
    else:
        locale.setlocale(locale.LC_TIME, 'en_US')

    from flask.ext.babel import refresh
    refresh()
'''


def compose_ret(ret, type=Constants.cst_content_type_plain, http_code=200, ensure_ascii=True):
    import json
    from flask import make_response

    if type == Constants.cst_content_type_json:
        if not ensure_ascii:
            resp = make_response(json.dumps(ret, ensure_ascii=False), http_code)
        else:
            resp = make_response(json.dumps(ret), http_code)
    else:
        resp = make_response(ret, http_code)

    if type == Constants.cst_content_type_json:
        resp.headers['Content-type'] = 'application/json; charset=utf-8'
    else:
        resp.headers['Content-type'] = 'text/plain; charset=utf-8'

    resp.headers['Access-Control-Allow-Origin'] = '*'

    return resp


def compose_ret_ascii(ret, http_code=200):
    import json
    from flask import make_response

    resp = make_response(json.dumps(ret, ensure_ascii=False), http_code)

    resp.headers['Content-type'] = 'application/json; charset=utf-8'

    return resp
