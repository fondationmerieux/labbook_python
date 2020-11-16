#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@project_name : Labbook Front End

@author: Alexandre CHARLES <ac@aegle.fr>
@creation_date: 20/11/2019
"""

# ###########################################
#   Imports
# ###########################################

import os
import logging
import requests
import json

from logging.handlers import WatchedFileHandler
from datetime import datetime, date

from flask import Flask, render_template, request, session, redirect, send_file, url_for
from flask_babel import Babel

from app.models.Logs import Logs
from app.models.Constants import Constants

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

prep_log('log_front', r'../logs/log_front.log')

log = logging.getLogger('log_front')

app = Flask(__name__)
app.config.from_object('default_settings')

config_envvar = 'LOCAL_SETTINGS'

if config_envvar in os.environ:
    print("Loading local configuration from {}={}".format(config_envvar, os.environ[config_envvar]))
    app.config.from_envvar(config_envvar)
else:
    print("No local configuration available: {} is undefined in the environment".format(config_envvar))

babel = Babel(app)


@app.context_processor
def locale():
    lang = app.config.get('BABEL_DEFAULT_LOCALE')
    if session and 'lang' in session:
        lang = session['lang']
        log.info(Logs.fileline() + ' : lang = ' + lang)

        if lang == 'en_GB':
            session['lang_select'] = 'UK'
            session['date_format'] = Constants.cst_date_eu
            session.modified = True
        elif lang == 'en_US':
            session['lang_select'] = 'US'
            session['date_format'] = Constants.cst_date_us
            session.modified = True
        else:
            session['lang_select'] = 'FR'
            session['date_format'] = Constants.cst_date_eu
            session.modified = True
    return dict(locale=lang)


# Selection de langues avec Babel
@babel.localeselector
def get_locale():
    lang = request.accept_languages.best_match(LANGUAGES.keys())
    if not session or 'lang' not in session:
        session['lang'] = lang
        session.modified = True
    elif session and 'lang' in session:
        lang = session['lang']
    return lang


def get_init_var():

    # init external server
    root = request.url_root
    log.info(Logs.fileline() + ' : URL : %s', root)
    session['server_ext'] = root
    session.modified = True

    # init internal server
    if not session or 'server_int' not in session or session['server_int'] != ('http://' + app.config.get('SERVER_INT')):
        session['server_int'] = 'http://' + app.config.get('SERVER_INT')
        session.modified = True

    # init internal url server
    if not session or 'redirect_name' not in session or session['redirect_name'] != app.config.get('REDIRECT_NAME'):
        session['redirect_name'] = app.config.get('REDIRECT_NAME')
        session.modified = True

    # init number version
    if not session or 'version' not in session or session['version'] != app.config.get('APP_VERSION'):
        session['version'] = app.config.get('APP_VERSION')
        session.modified = True

    # Get locale
    """
    if request.cookies and 'PHP_locale' in request.cookies:
        log.info(Logs.fileline() + ' : cookies PHP_locale = ' + request.cookies.get('PHP_locale'))
        session['lang'] = request.cookies.get('PHP_locale')
        session.modified = True
    else:
        log.info(Logs.fileline() + ' : cookies PHP_locale missing')"""

    # Get user_name
    """
    if request.cookies and 'PHP_user_name' in request.cookies:
        log.info(Logs.fileline() + ' : cookies PHP_user_name = ' + request.cookies.get('PHP_user_name'))
        session['user_name'] = request.cookies.get('PHP_user_name')
        session.modified = True
    else:
        log.info(Logs.fileline() + ' : cookies PHP_user_name missing')"""

    # Load auto_logout
    try:
        url = session['server_int'] + '/services/default/val/auto_logout'
        req = requests.get(url)

        if req.status_code == 200:
            ret_json = req.json()
            session['auto_logout'] = ret_json['value']
            session.modified = True

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests auto_logout failed, err=%s , url=%s', err, url)


def get_user_data(login):
    if not login:
        log.error(Logs.fileline() + ' : get_user_data ERROR no login')
        return False

    try:
        url = session['server_int'] + '/services/user/login/' + login
        req = requests.get(url)

        if req.status_code == 200:
            json = req.json()

            session['user_id']        = json['id_data']  # not used for now
            session['user_id_role']   = json['id_role']
            session['user_id_group']  = json['id_group']
            session['user_name']      = json['username']
            session['user_firstname'] = json['firstname']
            session['user_lastname']  = json['lastname']
            session.modified = True

            if session['user_id_role'] == 1:
                session['user_role'] = 'A'  # Administrator
                session.modified = True
            elif session['user_id_role'] == 2:
                session['user_role'] = 'B'  # Biologist
                session.modified = True
            elif session['user_id_role'] == 3:
                session['user_role'] = 'T'  # Technician
                session.modified = True
            elif session['user_id_role'] == 4:
                session['user_role'] = 'S'  # Secretary
                session.modified = True
            else:
                log.error(Logs.fileline() + ' : TRACE unknow role')
                session['user_role'] = 'X'  # Unknown
                session.modified = True

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests user login failed, err=%s , url=%s', err, url)
        return False

    return True


def get_software_settings():
    try:
        url = session['server_int'] + '/services/record/type/number'
        req = requests.get(url)

        if req.status_code == 200:
            json = req.json()

            session['record_period'] = json['periode']
            session['record_format'] = json['format']
            session.modified = True

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests software settings failed, err=%s , url=%s', err, url)
        return False

    return True


@app.template_filter('date_format')
def date_format(date_iso):
    date_tmp = datetime.strptime(date_iso, Constants.cst_isodate)
    return datetime.strftime(date_tmp, session['date_format'])


@app.template_filter('date_now')
def date_now(date_now):
    return datetime.strftime(date.today(), "%Y-%m-%d")


# ######################################
# Routes Flask pages
# ######################################


@app.route("/")
def index():
    if not session or 'current_page' not in session:
        log.info(Logs.fileline() + ' : TRACE Labbook FRONT END Login')
        get_init_var()
        return render_template('login.html')
    else:
        log.info(Logs.fileline() + ' : TRACE Labbook FRONT END Current')
        return redirect(url_for(session['current_page']))


@app.route("/disconnect/")
def disconnect():
    log.info(Logs.fileline() + ' : TRACE Labbook FRONT END disconnect')
    url = session['server_ext'] + session['redirect_name']
    session.clear()
    return redirect(url)


# Page : homepage
@app.route('/homepage/<string:login>')
def homepage(login=''):
    log.info(Logs.fileline() + ' : TRACE Homepage login=' + str(login))

    dt_start_req = datetime.now()

    get_user_data(login)

    # get_init_var()
    # get_software_settings()
    dt_stop_req = datetime.now()
    dt_time_req = dt_stop_req - dt_start_req

    log.info(Logs.fileline() + ' : DEBUG homepage processing time = ' + str(dt_time_req))

    return render_template('homepage.html')


# Change la langue
@app.route("/lang/<string:lang>/")
def lang(lang='fr'):
    # TODO change for Python process
    url_php_lang = session['server_ext'] + '/sigl/lang/index/change-lang/lang/'

    if lang == 'en_GB':
        lang_php = 'en_GB'
        session['lang_select'] = 'UK'
        session['date_format'] = Constants.cst_date_eu
        session.modified = True
    elif lang == 'en_US':
        lang_php = 'en_US'
        session['lang_select'] = 'US'
        session['date_format'] = Constants.cst_date_us
        session.modified = True
    else:
        lang_php = 'fr_FR'
        session['lang_select'] = 'FR'
        session['date_format'] = Constants.cst_date_eu
        session.modified = True

    session['lang']  = lang
    session.modified = True

    return redirect(url_php_lang + lang_php)


# Page : list of results to enter
@app.route('/list-results/')
def list_results():
    log.info(Logs.fileline())

    get_init_var()
    get_user_data(session['user_name'])
    get_software_settings()

    json_ihm  = {}
    json_data = {}

    dt_start_req = datetime.now()
    # Load analysis type
    try:
        url = session['server_int'] + '/services/dico/list/famille_analyse'
        req = requests.get(url)

        if req.status_code == 200:
            json_ihm['type_ana'] = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests analysis type failed, err=%s , url=%s', err, url)

    # Load list results
    try:
        date_beg = datetime.strftime(date.today(), Constants.cst_isodate)
        date_end = date_beg

        payload = {'date_beg': date_beg, 'date_end': date_end, 'type_ana': 0, 'emer_ana': 0, 'valid_res': 0}

        url = session['server_int'] + '/services/result/list'
        req = requests.post(url, json=payload)

        if req.status_code == 200:
            json_data['list_res'] = json.dumps(req.json())

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests results list failed, err=%s , url=%s', err, url)

    # Load list of technician
    try:
        url = session['server_int'] + '/services/user/role/3'
        req = requests.get(url)

        if req.status_code == 200:
            json_ihm['tech_list'] = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests user role failed, err=%s , url=%s', err, url)

    dt_stop_req = datetime.now()
    dt_time_req = dt_stop_req - dt_start_req

    log.info(Logs.fileline() + ' : DEBUG list-results processing time = ' + str(dt_time_req))

    return render_template('list-results.html', ihm=json_ihm, args=json_data)


# Page : enter result
@app.route('/enter-result/<int:id_rec>')
def enter_result(id_rec=0):
    log.info(Logs.fileline() + ' : id_rec = ' + str(id_rec))

    json_ihm  = {}
    json_data = {}

    id_pat = 0

    dt_start_req = datetime.now()
    # Load list results
    try:
        url = session['server_int'] + '/services/result/record/' + str(id_rec)
        req = requests.get(url)

        if req.status_code == 200:
            json_data['list_res'] = req.json()

            # Get result answer
            if json_data['list_res']:
                for res in json_data['list_res']:
                    # load result types
                    type_res = ''

                    if res['type_resultat']:
                        try:
                            url = session['server_int'] + '/services/dico/id/' + str(res['type_resultat'])
                            req = requests.get(url)

                            if req.status_code == 200:
                                type_res = req.json()

                                # get short_label (without prefix "dico_") in type_res
                                if type_res and type_res['short_label'].startswith("dico_"):
                                    type_res = type_res['short_label'][5:]
                                else:
                                    type_res = ''

                        except requests.exceptions.RequestException as err:
                            log.error(Logs.fileline() + ' : requests result type failed, err=%s , url=%s', err, url)

                    # get unit label
                    try:
                        url = session['server_int'] + '/services/dico/id/' + str(res['unite'])
                        req = requests.get(url)

                        res['unit'] = ''

                        if req.status_code == 200:
                            unit = req.json()

                            if unit and unit['label']:
                                res['unit'] = unit['label']

                    except requests.exceptions.RequestException as err:
                        log.error(Logs.fileline() + ' : requests result type failed, err=%s , url=%s', err, url)

                    # init list of answer
                    res['res_answer'] = []
                    # get anwser
                    try:
                        if type_res:
                            url = session['server_int'] + '/services/dico/list/' + str(type_res)
                            req = requests.get(url)

                            if req.status_code == 200:
                                res['res_answer'] = req.json()

                    except requests.exceptions.RequestException as err:
                        log.error(Logs.fileline() + ' : requests results list failed, err=%s , url=%s', err, url)

            # Load data patient
            if res and res['id_pat']:
                id_pat = res['id_pat']

        # If no ResultRecord found we're looking for record information
        else:
            try:
                url = session['server_int'] + '/services/record/det/' + str(id_rec)
                req = requests.get(url)

                if req.status_code == 200:
                    json_data['record'] = req.json()

                    # Load data patient
                    if json_data['record']:
                        id_pat = json_data['record']['id_patient']

            except requests.exceptions.RequestException as err:
                log.error(Logs.fileline() + ' : requests results list failed, err=%s , url=%s', err, url)

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests results record failed, err=%s , url=%s', err, url)

    json_data['patient'] = {}
    if id_pat > 0:
        try:
            url = session['server_int'] + '/services/patient/det/' + str(id_pat)
            req = requests.get(url)

            if req.status_code == 200:
                json_data['patient'] = req.json()

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests patient det failed, err=%s , url=%s', err, url)

    # Load list of technician
    try:
        url = session['server_int'] + '/services/user/role/3'
        req = requests.get(url)

        if req.status_code == 200:
            json_ihm['tech_list'] = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests user role failed, err=%s , url=%s', err, url)

    dt_stop_req = datetime.now()
    dt_time_req = dt_stop_req - dt_start_req

    log.info(Logs.fileline() + ' : DEBUG enter-result processing time = ' + str(dt_time_req))

    return render_template('enter-result.html', ihm=json_ihm, args=json_data)


# Page : List of records
@app.route('/list-records/')
def list_records():
    log.info(Logs.fileline())

    get_init_var()
    get_user_data(session['user_name'])
    get_software_settings()

    json_data = {}

    dt_start_req = datetime.now()
    # Load list records
    try:
        url = session['server_int'] + '/services/record/list/' + str(session['user_id_group'])
        req = requests.post(url)

        if req.status_code == 200:
            json_data = json.dumps(req.json())

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests records list failed, err=%s , url=%s', err, url)

    dt_stop_req = datetime.now()
    dt_time_req = dt_stop_req - dt_start_req

    log.info(Logs.fileline() + ' : DEBUG list-records processing time = ' + str(dt_time_req))

    return render_template('list-records.html', args=json_data)


# Page : new external request
@app.route('/new-req-ext/')
def new_req_ext():
    log.info(Logs.fileline())

    dt_start_req = datetime.now()
    get_init_var()
    get_user_data(session['user_name'])
    get_software_settings()
    dt_stop_req = datetime.now()
    dt_time_req = dt_stop_req - dt_start_req

    log.info(Logs.fileline() + ' : DEBUG new-req-ext processing time = ' + str(dt_time_req))

    return render_template('new-req-ext.html')


# Page : new internal request
@app.route('/new-req-int/')
def new_req_int():
    log.info(Logs.fileline())

    get_init_var()
    get_user_data(session['user_name'])
    get_software_settings()

    return render_template('new-req-int.html')


# Page : patient details
@app.route('/det-patient/<int:id_pat>')
def det_patient(id_pat=0):
    log.info(Logs.fileline() + ' : id_pat = ' + str(id_pat))

    json_data = {}

    dt_start_req = datetime.now()
    # Load data patient
    if id_pat > 0:
        try:
            url = session['server_int'] + '/services/patient/det/' + str(id_pat)
            req = requests.get(url)

            if req.status_code == 200:
                json_data = req.json()
                json_data['id_pat'] = id_pat

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests patient det failed, err=%s , url=%s', err, url)
    else:
        # generate a code
        try:
            url = session['server_int'] + '/services/patient/generate/code'
            req = requests.get(url)

            if req.status_code == 200:
                json_data['code'] = req.json()
                json_data['id_pat'] = 0

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests patient generate code failed, err=%s , url=%s', err, url)

    dt_stop_req = datetime.now()
    dt_time_req = dt_stop_req - dt_start_req

    log.info(Logs.fileline() + ' : DEBUG det-patient processing time = ' + str(dt_time_req))

    return render_template('det-patient.html', args=json_data)


# Page : external request details
@app.route('/det-req-ext/<string:entry>/<int:ref>')
def det_req_ext(entry='Y', ref=0):
    log.info(Logs.fileline() + ' : ref = ' + str(ref))

    json_ihm  = {}
    json_data = {}

    dt_start_req = datetime.now()
    if entry == "Y":
        # ref = id_pat
        # Load data patient
        if ref > 0:
            try:
                url = session['server_int'] + '/services/patient/det/' + str(ref)
                req = requests.get(url)

                if req.status_code == 200:
                    json_data['patient'] = req.json()

            except requests.exceptions.RequestException as err:
                log.error(Logs.fileline() + ' : requests patient det failed, err=%s , url=%s', err, url)

        # Load yes or no
        try:
            url = session['server_int'] + '/services/dico/list/yorn'
            req = requests.get(url)

            if req.status_code == 200:
                json_ihm['yorn'] = req.json()

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests yorn list failed, err=%s , url=%s', err, url)

        # Load discount billing
        try:
            url = session['server_int'] + '/services/dico/list/remise_facturation'
            req = requests.get(url)

            if req.status_code == 200:
                json_ihm['discount_bill'] = req.json()

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests discount bill list failed, err=%s , url=%s', err, url)

        # Load products statut
        try:
            url = session['server_int'] + '/services/dico/list/prel_statut'
            req = requests.get(url)

            if req.status_code == 200:
                json_ihm['products_statut'] = req.json()

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests products statut list failed, err=%s , url=%s', err, url)

        # Load products
        try:
            url = session['server_int'] + '/services/dico/list/type_prel'
            req = requests.get(url)

            if req.status_code == 200:
                json_ihm['products'] = req.json()

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests products list failed, err=%s , url=%s', err, url)

        # Load prix_acte
        try:
            url = session['server_int'] + '/services/default/val/prix_acte'
            req = requests.get(url)

            if req.status_code == 200:
                json_ihm['act_price'] = req.json()

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests prix_acte failed, err=%s , url=%s', err, url)

        # Load facturation_pat_hosp
        try:
            url = session['server_int'] + '/services/default/val/facturation_pat_hosp'
            req = requests.get(url)

            if req.status_code == 200:
                json_data['billing_hosp'] = req.json()

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests billing_pat failed, err=%s , url=%s', err, url)

        # add empty structure for post data_save after save_request
        json_data['data_analysis'] = []
        json_data['data_samples']  = []
        json_data['data_products'] = []
        json_data['record']        = []

    else:
        # ref = id_rec
        # Load save record
        try:
            url = session['server_int'] + '/services/record/det/' + str(ref)
            req = requests.get(url)

            if req.status_code == 200:
                json_data['record'] = req.json()

                # Load data patient with id_patient
                if json_data['record']['id_patient'] and json_data['record']['id_patient'] > 0:
                    try:
                        url = session['server_int'] + '/services/patient/det/' + str(json_data['record']['id_patient'])
                        req = requests.get(url)

                        if req.status_code == 200:
                            json_data['patient'] = req.json()

                    except requests.exceptions.RequestException as err:
                        log.error(Logs.fileline() + ' : requests patient det failed, err=%s , url=%s', err, url)

                # Load data patient with id_patient
                if json_data['record']['med_prescripteur'] and json_data['record']['med_prescripteur'] > 0:
                    try:
                        url = session['server_int'] + '/services/doctor/det/' + str(json_data['record']['med_prescripteur'])
                        req = requests.get(url)

                        if req.status_code == 200:
                            json_data['doctor'] = req.json()

                    except requests.exceptions.RequestException as err:
                        log.error(Logs.fileline() + ' : requests doctor det failed, err=%s , url=%s', err, url)

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests record det failed, err=%s , url=%s', err, url)

        # Load list analysis requested
        try:
            url = session['server_int'] + '/services/analysis/list/req/' + str(ref) + '/type/O'
            req = requests.get(url)

            if req.status_code == 200:
                json_data['data_analysis'] = req.json()

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests list ana failed, err=%s , url=%s', err, url)

        # Load list samples requested
        try:
            url = session['server_int'] + '/services/analysis/list/req/' + str(ref) + '/type/N'
            req = requests.get(url)

            if req.status_code == 200:
                json_data['data_samples'] = req.json()

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests list ana failed, err=%s , url=%s', err, url)

        # Load list products requested
        try:
            url = session['server_int'] + '/services/product/list/req/' + str(ref)
            req = requests.get(url)

            if req.status_code == 200:
                json_data['data_products'] = req.json()

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests list prod failed, err=%s , url=%s', err, url)

        # Load prix_acte
        try:
            url = session['server_int'] + '/services/default/val/prix_acte'
            req = requests.get(url)

            if req.status_code == 200:
                json_ihm['act_price'] = req.json()

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests prix_acte failed, err=%s , url=%s', err, url)

        # Load yes or no
        try:
            url = session['server_int'] + '/services/dico/list/yorn'
            req = requests.get(url)

            if req.status_code == 200:
                json_ihm['yorn'] = req.json()

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests yorn list failed, err=%s , url=%s', err, url)

    dt_stop_req = datetime.now()
    dt_time_req = dt_stop_req - dt_start_req

    log.info(Logs.fileline() + ' : DEBUG det-req-ext processing time = ' + str(dt_time_req))

    return render_template('det-req-ext.html', entry=entry, ihm=json_ihm, args=json_data)


# Page : internal request details
@app.route('/det-req-int/<string:entry>/<int:ref>')
def det_req_int(entry='Y', ref=0):
    log.info(Logs.fileline() + ' : ref = ' + str(ref))

    json_ihm  = {}
    json_data = {}

    if entry == "Y":
        # here : ref = id_pat
        # Load data patient
        if ref > 0:
            try:
                url = session['server_int'] + '/services/patient/det/' + str(ref)
                req = requests.get(url)

                if req.status_code == 200:
                    json_data['patient'] = req.json()

            except requests.exceptions.RequestException as err:
                log.error(Logs.fileline() + ' : requests patient det failed, err=%s , url=%s', err, url)

        # Load yes or no
        try:
            url = session['server_int'] + '/services/dico/list/yorn'
            req = requests.get(url)

            if req.status_code == 200:
                json_ihm['yorn'] = req.json()

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests yorn list failed, err=%s , url=%s', err, url)

        # Load discount billing
        try:
            url = session['server_int'] + '/services/dico/list/remise_facturation'
            req = requests.get(url)

            if req.status_code == 200:
                json_ihm['discount_bill'] = req.json()

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests discount bill list failed, err=%s , url=%s', err, url)

        # Load products statut
        try:
            url = session['server_int'] + '/services/dico/list/prel_statut'
            req = requests.get(url)

            if req.status_code == 200:
                json_ihm['products_statut'] = req.json()

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests products statut list failed, err=%s , url=%s', err, url)

        # Load products
        try:
            url = session['server_int'] + '/services/dico/list/type_prel'
            req = requests.get(url)

            if req.status_code == 200:
                json_ihm['products'] = req.json()

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests products list failed, err=%s , url=%s', err, url)

        # Load prix_acte
        try:
            url = session['server_int'] + '/services/default/val/prix_acte'
            req = requests.get(url)

            if req.status_code == 200:
                json_ihm['act_price'] = req.json()

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests prix_acte failed, err=%s , url=%s', err, url)

        # Load facturation_pat_hosp
        try:
            url = session['server_int'] + '/services/default/val/facturation_pat_hosp'
            req = requests.get(url)

            if req.status_code == 200:
                json_data['billing_hosp'] = req.json()

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests billing_pat failed, err=%s , url=%s', err, url)

        # add empty structure
        json_data['data_analysis'] = []
        json_data['data_samples']  = []
        json_data['data_products'] = []
        json_data['record']        = []

    else:
        # here : ref = id_rec
        # Load save record
        try:
            url = session['server_int'] + '/services/record/det/' + str(ref)
            req = requests.get(url)

            if req.status_code == 200:
                json_data['record'] = req.json()

                # Load data patient with id_patient
                if json_data['record']['id_patient'] and json_data['record']['id_patient'] > 0:
                    try:
                        url = session['server_int'] + '/services/patient/det/' + str(json_data['record']['id_patient'])
                        req = requests.get(url)

                        if req.status_code == 200:
                            json_data['patient'] = req.json()

                    except requests.exceptions.RequestException as err:
                        log.error(Logs.fileline() + ' : requests patient det failed, err=%s , url=%s', err, url)

                # Load data patient with id_patient
                if json_data['record']['med_prescripteur'] and json_data['record']['med_prescripteur'] > 0:
                    try:
                        url = session['server_int'] + '/services/doctor/det/' + str(json_data['record']['med_prescripteur'])
                        req = requests.get(url)

                        if req.status_code == 200:
                            json_data['doctor'] = req.json()

                    except requests.exceptions.RequestException as err:
                        log.error(Logs.fileline() + ' : requests doctor det failed, err=%s , url=%s', err, url)

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests record det failed, err=%s , url=%s', err, url)

        # Load list analysis requested
        try:
            url = session['server_int'] + '/services/analysis/list/req/' + str(ref) + '/type/O'
            req = requests.get(url)

            if req.status_code == 200:
                json_data['data_analysis'] = req.json()

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests list ana failed, err=%s , url=%s', err, url)

        # Load list samples requested
        try:
            url = session['server_int'] + '/services/analysis/list/req/' + str(ref) + '/type/N'
            req = requests.get(url)

            if req.status_code == 200:
                json_data['data_samples'] = req.json()

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests list ana failed, err=%s , url=%s', err, url)

        # Load list products requested
        try:
            url = session['server_int'] + '/services/product/list/req/' + str(ref)
            req = requests.get(url)

            if req.status_code == 200:
                json_data['data_products'] = req.json()

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests list prod failed, err=%s , url=%s', err, url)

        # Load prix_acte
        try:
            url = session['server_int'] + '/services/default/val/prix_acte'
            req = requests.get(url)

            if req.status_code == 200:
                json_ihm['act_price'] = req.json()

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests prix_acte failed, err=%s , url=%s', err, url)

        # Load yes or no
        try:
            url = session['server_int'] + '/services/dico/list/yorn'
            req = requests.get(url)

            if req.status_code == 200:
                json_ihm['yorn'] = req.json()

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests yorn list failed, err=%s , url=%s', err, url)

    return render_template('det-req-int.html', entry=entry, ihm=json_ihm, args=json_data)


# Page : administrative record
@app.route('/administrative-record/<string:type_req>/<int:id_rec>')
def administrative_record(type_req='E', id_rec=0):
    log.info(Logs.fileline() + ' : id_rec = ' + str(id_rec))

    json_data = {}
    json_data['data_analysis'] = []
    json_data['data_samples']  = []
    json_data['data_reports']  = []
    json_data['data_files']    = []
    json_data['record']        = []

    dt_start_req = datetime.now()
    # Load save record
    try:
        url = session['server_int'] + '/services/record/det/' + str(id_rec)
        req = requests.get(url)

        if req.status_code == 200:
            json_data['record'] = req.json()

            # Load data patient with id_patient
            if json_data['record']['id_patient'] and json_data['record']['id_patient'] > 0:
                try:
                    url = session['server_int'] + '/services/patient/det/' + str(json_data['record']['id_patient'])
                    req = requests.get(url)

                    if req.status_code == 200:
                        json_data['patient'] = req.json()

                except requests.exceptions.RequestException as err:
                    log.error(Logs.fileline() + ' : requests patient det failed, err=%s , url=%s', err, url)

            # Load data doctor with id_doctor
            if json_data['record']['med_prescripteur'] and json_data['record']['med_prescripteur'] > 0:
                try:
                    url = session['server_int'] + '/services/doctor/det/' + str(json_data['record']['med_prescripteur'])
                    req = requests.get(url)

                    if req.status_code == 200:
                        json_data['doctor'] = req.json()

                except requests.exceptions.RequestException as err:
                    log.error(Logs.fileline() + ' : requests doctor det failed, err=%s , url=%s', err, url)

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests record det failed, err=%s , url=%s', err, url)

    # Load list analysis requested
    try:
        url = session['server_int'] + '/services/analysis/list/req/' + str(id_rec) + '/type/O'
        req = requests.get(url)

        if req.status_code == 200:
            json_data['data_analysis'] = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests list ana failed, err=%s , url=%s', err, url)

    # Load list samples requested
    try:
        url = session['server_int'] + '/services/analysis/list/req/' + str(id_rec) + '/type/N'
        req = requests.get(url)

        if req.status_code == 200:
            json_data['data_samples'] = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests list ana failed, err=%s , url=%s', err, url)

    # Load report attached to this record
    try:
        url = session['server_int'] + '/services/file/report/record/' + str(id_rec)
        req = requests.get(url)

        if req.status_code == 200:
            json_data['data_reports'] = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests report file failed, err=%s , url=%s', err, url)

    # Load files attached to this record
    try:
        url = session['server_int'] + '/services/record/list/file/' + str(id_rec)
        req = requests.get(url)

        if req.status_code == 200:
            json_data['data_files'] = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests record list files failed, err=%s , url=%s', err, url)

    dt_stop_req = datetime.now()
    dt_time_req = dt_stop_req - dt_start_req

    log.info(Logs.fileline() + ' : DEBUG administrative-record processing time = ' + str(dt_time_req))

    return render_template('administrative-record.html', type_req=type_req, args=json_data)


# Page : technical validation
@app.route('/technical-validation/<int:id_rec>')
def technical_validation(id_rec=0):
    log.info(Logs.fileline() + ' : id_rec = ' + str(id_rec))

    json_ihm  = {}
    json_data = {}

    id_pat = 0

    dt_start_req = datetime.now()
    # Load list results
    try:
        url = session['server_int'] + '/services/result/record/' + str(id_rec)
        req = requests.get(url)

        if req.status_code == 200:
            json_data['list_res'] = req.json()

            # Get result answer
            if json_data['list_res']:
                for res in json_data['list_res']:
                    # load result types
                    type_res = ''

                    if res['type_resultat']:
                        try:
                            url = session['server_int'] + '/services/dico/id/' + str(res['type_resultat'])
                            req = requests.get(url)

                            if req.status_code == 200:
                                type_res = req.json()

                                # get short_label (without prefix "dico_") in type_res
                                if type_res and type_res['short_label'].startswith("dico_"):
                                    type_res = type_res['short_label'][5:]
                                else:
                                    type_res = ''

                        except requests.exceptions.RequestException as err:
                            log.error(Logs.fileline() + ' : requests result type failed, err=%s , url=%s', err, url)

                    # get result label if a value has been entered
                    if type_res and res['valeur']:
                        try:
                            url = session['server_int'] + '/services/dico/id/' + str(res['valeur'])
                            req = requests.get(url)

                            res['res_label'] = ''

                            if req.status_code == 200:
                                dico_tmp = req.json()
                                res['res_label'] = dico_tmp['label']

                        except requests.exceptions.RequestException as err:
                            log.error(Logs.fileline() + ' : requests result label failed, err=%s , url=%s', err, url)
                    else:
                        res['res_label'] = res['valeur']

                    # get unit label
                    try:
                        url = session['server_int'] + '/services/dico/id/' + str(res['unite'])
                        req = requests.get(url)

                        res['unit'] = ''

                        if req.status_code == 200:
                            unit = req.json()

                            # get short_label (without prefix "dico_") in type_res
                            if unit and unit['label']:
                                res['unit'] = unit['label']

                    except requests.exceptions.RequestException as err:
                        log.error(Logs.fileline() + ' : requests result type failed, err=%s , url=%s', err, url)

            # Load data patient
            if res and res['id_pat']:
                id_pat = res['id_pat']

        # If no ResultRecord found we're looking for record information
        else:
            try:
                url = session['server_int'] + '/services/record/det/' + str(id_rec)
                req = requests.get(url)

                if req.status_code == 200:
                    json_data['record'] = req.json()

                    # Load data patient
                    if json_data['record']:
                        id_pat = json_data['record']['id_patient']

            except requests.exceptions.RequestException as err:
                log.error(Logs.fileline() + ' : requests results list failed, err=%s , url=%s', err, url)

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests results record failed, err=%s , url=%s', err, url)

    json_data['patient'] = {}
    if id_pat > 0:
        try:
            url = session['server_int'] + '/services/patient/det/' + str(id_pat)
            req = requests.get(url)

            if req.status_code == 200:
                json_data['patient'] = req.json()

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests patient det failed, err=%s , url=%s', err, url)

    # Load list of technician
    try:
        url = session['server_int'] + '/services/user/role/3'
        req = requests.get(url)

        if req.status_code == 200:
            json_ihm['tech_list'] = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests user role failed, err=%s , url=%s', err, url)

    dt_stop_req = datetime.now()
    dt_time_req = dt_stop_req - dt_start_req

    log.info(Logs.fileline() + ' : DEBUG technical-validation processing time = ' + str(dt_time_req))

    return render_template('technical-validation.html', ihm=json_ihm, args=json_data)


# Page : biological validation
@app.route('/biological-validation/<int:id_rec>')
def biological_validation(id_rec=0):
    log.info(Logs.fileline() + ' : id_rec = ' + str(id_rec))

    json_ihm  = {}
    json_data = {}

    json_data['data_reports'] = []

    id_pat = 0

    dt_start_req = datetime.now()
    # Load record
    try:
        url = session['server_int'] + '/services/record/det/' + str(id_rec)
        req = requests.get(url)

        if req.status_code == 200:
            json_data['record'] = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests record failed, err=%s , url=%s', err, url)

    # Load list results
    try:
        url = session['server_int'] + '/services/result/record/' + str(id_rec)
        req = requests.get(url)

        if req.status_code == 200:
            json_data['list_res'] = req.json()

            # Get result answer
            if json_data['list_res']:
                for res in json_data['list_res']:
                    # load result types
                    type_res = ''

                    if res['type_resultat']:
                        try:
                            url = session['server_int'] + '/services/dico/id/' + str(res['type_resultat'])
                            req = requests.get(url)

                            if req.status_code == 200:
                                type_res = req.json()

                                # get short_label (without prefix "dico_") in type_res
                                if type_res and type_res['short_label'].startswith("dico_"):
                                    type_res = type_res['short_label'][5:]
                                else:
                                    type_res = ''

                        except requests.exceptions.RequestException as err:
                            log.error(Logs.fileline() + ' : requests result type failed, err=%s , url=%s', err, url)

                    # get result label if a value has been entered
                    if type_res and res['valeur']:
                        try:
                            url = session['server_int'] + '/services/dico/id/' + str(res['valeur'])
                            req = requests.get(url)

                            res['res_label'] = ''

                            if req.status_code == 200:
                                dico_tmp = req.json()
                                res['res_label'] = dico_tmp['label']

                        except requests.exceptions.RequestException as err:
                            log.error(Logs.fileline() + ' : requests result label failed, err=%s , url=%s', err, url)
                    else:
                        res['res_label'] = res['valeur']

                    # get unit label
                    try:
                        url = session['server_int'] + '/services/dico/id/' + str(res['unite'])
                        req = requests.get(url)

                        res['unit'] = ''

                        if req.status_code == 200:
                            unit = req.json()

                            # get short_label (without prefix "dico_") in type_res
                            if unit and unit['label']:
                                res['unit'] = unit['label']

                    except requests.exceptions.RequestException as err:
                        log.error(Logs.fileline() + ' : requests result type failed, err=%s , url=%s', err, url)

            # Load data patient
            if res and res['id_pat']:
                id_pat = res['id_pat']

        # If no ResultRecord found we're looking for record information
        else:
            try:
                url = session['server_int'] + '/services/record/det/' + str(id_rec)
                req = requests.get(url)

                if req.status_code == 200:
                    json_data['record'] = req.json()

                    # Load data patient
                    if json_data['record']:
                        id_pat = json_data['record']['id_patient']

            except requests.exceptions.RequestException as err:
                log.error(Logs.fileline() + ' : requests results list failed, err=%s , url=%s', err, url)

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests results record failed, err=%s , url=%s', err, url)

    json_data['patient'] = {}
    if id_pat > 0:
        try:
            url = session['server_int'] + '/services/patient/det/' + str(id_pat)
            req = requests.get(url)

            if req.status_code == 200:
                json_data['patient'] = req.json()

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests patient det failed, err=%s , url=%s', err, url)

    # Load list of biologist
    try:
        url = session['server_int'] + '/services/user/role/2'
        req = requests.get(url)

        if req.status_code == 200:
            json_ihm['bio_list'] = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests user role failed, err=%s , url=%s', err, url)

    # Load report attached to this record
    try:
        url = session['server_int'] + '/services/file/report/record/' + str(id_rec)
        req = requests.get(url)

        if req.status_code == 200:
            json_data['data_reports'] = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests report file failed, err=%s , url=%s', err, url)

    # Load reasons to cancel a result
    try:
        url = session['server_int'] + '/services/dico/list/motif_annulation'
        req = requests.get(url)

        if req.status_code == 200:
            json_ihm['cancel_reason'] = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests cancel reason failed, err=%s , url=%s', err, url)

    dt_stop_req = datetime.now()
    dt_time_req = dt_stop_req - dt_start_req

    log.info(Logs.fileline() + ' : DEBUG biological-validation processing time = ' + str(dt_time_req))

    return render_template('biological-validation.html', ihm=json_ihm, args=json_data)


# Page : contributors
@app.route('/contributors/')
def contributors():
    log.info(Logs.fileline())

    get_init_var()

    return render_template('contributors.html')


# Page : WHONET export
@app.route('/whonet-export/')
def whonet_export():
    log.info(Logs.fileline())

    get_init_var()
    get_user_data(session['user_name'])
    get_software_settings()

    return render_template('whonet-export.html')


# Route : download a file
@app.route('/download-file/type/<string:type>/name/<string:filename>/ref/<string:ref>')
def download_file(type='', filename='', ref=''):
    log.info(Logs.fileline())

    # TYPE
    # PY => Python : BarCode, Bill, Whonet
    # JF => Join File
    # RP => Report

    if type == 'PY':
        filepath = '/home/apps/labbook_BE/labbook_BE/tmp/'
        generated_name = filename
    elif type == 'JF':
        # ref = id_file
        try:
            url = session['server_int'] + '/services/file/document/' + ref
            req = requests.get(url)

            if req.status_code == 200:
                file_info = req.json()

                if file_info:
                    filepath = os.path.join(file_info['storage'] + '/sigl', file_info['path'])
                    generated_name = file_info['generated_name']
                else:
                    return False

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests file document failed, err=%s , url=%s', err, url)
    elif type == 'RP':
        filepath = '/space/www/apps/labbook/labbook_2.05/files/'
        generated_name = filename

        filename = 'cr_' + ref + '.pdf'
    else:
        return False

    ret_file = send_file(os.path.join(filepath, generated_name), as_attachment=True, attachment_filename=filename)
    ret_file.headers["x-suggested-filename"] = filename

    return ret_file


# Route : upload a file
@app.route('/upload-file/<int:id_rec>', methods=['POST'])
def upload_file(id_rec=0):
    log.info(Logs.fileline() + ' : id_rec = ' + str(id_rec))
    if request.method == 'POST':
        try:
            f = request.files['file']

            original_name = f.filename

            # random name kind like VOOZANOO
            # PHP version : md5( mt_rand() . mt_rand() .microtime() )
            import pathlib
            import time
            import hashlib
            generated_name = hashlib.md5((original_name + str(int(round(time.time() * 1000)))).encode('utf-8')).hexdigest()
            hash_name      = hashlib.md5((original_name).encode('utf-8')).hexdigest()

            log.info(Logs.fileline() + ' : DEBUG generated_name=' + str(generated_name))

            # Create end of storage path
            end_path = generated_name[:2] + "/" + generated_name[2:4] + "/"
        except Exception as err:
            log.error(Logs.fileline() + ' : upload-file failed to hash name, err=%s', err)
            return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}

        try:
            # Get last storage path
            url = session['server_int'] + '/services/file/storage/' + str(session['user_id_group'])
            req = requests.get(url)

            if req.status_code == 200:
                storage = req.json()

                if not storage:
                    log.error(Logs.fileline() + ' : upload-file storage failed')
                    return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}
        except Exception as err:
            log.error(Logs.fileline() + ' : upload-file failed requests storage, err=%s', err)
            return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}

        filepath = storage['path'] + '/sigl/'

        try:
            pathlib.Path(filepath + end_path[:2]).mkdir(mode=0o777, parents=False, exist_ok=True)
            pathlib.Path(filepath + end_path).mkdir(mode=0o777, parents=False, exist_ok=True)
        except Exception as err:
            log.error(Logs.fileline() + ' : upload-file failed to filepath, err=%s', err)
            return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}

        try:
            f.save(os.path.join(filepath + end_path, generated_name))
        except Exception as err:
            log.error(Logs.fileline() + ' : upload-file failed to save file, err=%s', err)
            return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}

        try:
            # Get info on file
            file_ext  = pathlib.Path(original_name).suffix
            file_size = pathlib.Path(os.path.join(filepath + end_path, generated_name)).stat().st_size
            mime_type = f.mimetype

            # remove first dot
            if file_ext.startswith('.'):
                file_ext = file_ext[1:]

            # insert upload information in DB
            payload = {'id_owner': session['user_id_group'],
                       'original_name': original_name,
                       'generated_name': generated_name,
                       'size': file_size,
                       'hash': hash_name,
                       'ext': file_ext,
                       'content_type': mime_type,
                       'id_storage': storage['id_data'],
                       'end_path': end_path}

            url = session['server_int'] + '/services/file/document/' + str(id_rec)
            req = requests.post(url, json=payload)

            if req.status_code != 200:
                log.error(Logs.fileline() + ' : upload-file insert failed')
                return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}

        except Exception as err:
            log.error(Logs.fileline() + ' : upload-file failed information file, err=%s', err)
            return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}

        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

    return json.dumps({'success': False}), 405, {'ContentType': 'application/json'}


if __name__ == "__main__":
    app.run()
