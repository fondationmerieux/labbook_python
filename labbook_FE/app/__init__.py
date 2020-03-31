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

from logging.handlers import WatchedFileHandler
from datetime import datetime, date

from flask import Flask, render_template, request, session, redirect
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

app = Flask(__name__)  # ,static_url_path='/TEST/static')
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

    # init internal server
    if not session or 'server_int' not in session or session['server_int'] != ('http://' + app.config.get('SERVER_INT')):
        session['server_int'] = 'http://' + app.config.get('SERVER_INT')
        session.modified = True

    # init external server
    if request.cookies and 'PHP_url_host' in request.cookies:
        if not session or 'server_ext' not in session or session['server_ext'] != 'http://' + request.cookies.get('PHP_url_host'):
            log.info(Logs.fileline() + ' : cookies PHP_url_host = ' + request.cookies.get('PHP_url_host'))
            session['server_ext'] = 'http://' + request.cookies.get('PHP_url_host')
            session.modified = True
    else:
        log.info(Logs.fileline() + ' : cookies PHP_url_host missing')

    # init internal url server
    if not session or 'redirect_name' not in session or session['redirect_name'] != app.config.get('REDIRECT_NAME'):
        session['redirect_name'] = app.config.get('REDIRECT_NAME')
        session.modified = True

    # init number version
    if not session or 'version' not in session or session['version'] != app.config.get('APP_VERSION'):
        session['version'] = app.config.get('APP_VERSION')
        session.modified = True

    # Get locale
    if request.cookies and 'PHP_locale' in request.cookies:
        log.info(Logs.fileline() + ' : cookies PHP_locale = ' + request.cookies.get('PHP_locale'))
        session['lang'] = request.cookies.get('PHP_locale')
        session.modified = True
    else:
        log.info(Logs.fileline() + ' : cookies PHP_locale missing')

    # Get user_role
    if request.cookies and 'PHP_user_role' in request.cookies:
        log.info(Logs.fileline() + ' : cookies PHP_user_role = ' + request.cookies.get('PHP_user_role'))
        session['user_role'] = request.cookies.get('PHP_user_role')
        session.modified = True
    else:
        log.info(Logs.fileline() + ' : cookies PHP_user_role missing')

    # Get user_name
    if request.cookies and 'PHP_user_name' in request.cookies:
        log.info(Logs.fileline() + ' : cookies PHP_user_name = ' + request.cookies.get('PHP_user_name'))
        session['user_name'] = request.cookies.get('PHP_user_name')
        session.modified = True
    else:
        log.info(Logs.fileline() + ' : cookies PHP_user_name missing')


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
            session['user_id_group']  = json['id_group']
            session['user_firstname'] = json['firstname']
            session['user_lastname']  = json['lastname']
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
            log.error(Logs.fileline() + ' : DEBUG period et format=' + str(json))

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
    log.info(Logs.fileline() + ' : TRACE Labbook FRONT END')
    return "Hello World ! Coucou le Monde ! Labbook FRONT END"


# Change la langue
@app.route("/lang/<string:lang>/")
def lang(lang='fr'):
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

        payload = {'date_beg': date_beg, 'date_end': date_end, 'type_ana': 0, 'emer_ana': 0, 'valid_res': 0 }
        # payload = {'date_beg': '2019-01-01', 'date_end': '2020-03-25', 'emer_ana': 0}  # TEST

        url = session['server_int'] + '/services/result/list'
        req = requests.post(url, json=payload)

        if req.status_code == 200:
            json_data['list_res'] = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests results list failed, err=%s , url=%s', err, url)

    return render_template('list-results.html', ihm=json_ihm, args=json_data)


# Page : enter result
@app.route('/enter-result/<int:id_rec>')
def enter_result(id_rec=0):
    log.info(Logs.fileline() + ' : id_rec = ' + str(id_rec))

    json_ihm  = {}
    json_data = {}

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

                            # get short_label (without prefix "dico_") in type_res
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

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests results list failed, err=%s , url=%s', err, url)

    # Load data patient
    id_pat = res['id_pat']

    json_data['patient'] = {}
    if id_pat > 0:
        try:
            url = session['server_int'] + '/services/patient/det/' + str(id_pat)
            req = requests.get(url)

            if req.status_code == 200:
                json_data['patient'] = req.json()

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests patient det failed, err=%s , url=%s', err, url)

    return render_template('enter-result.html', ihm=json_ihm, args=json_data)


# Page : List of records
@app.route('/list-records/')
def list_records():
    log.info(Logs.fileline())

    get_init_var()
    get_user_data(session['user_name'])
    get_software_settings()

    json_data = {}

    # Load list records
    try:
        url = session['server_int'] + '/services/record/list/' + str(session['user_id_group'])
        req = requests.post(url)

        if req.status_code == 200:
            json_data = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests records list failed, err=%s , url=%s', err, url)

    return render_template('list-records.html', args=json_data)


# Page : new external request
@app.route('/new-req-ext/')
def new_req_ext():
    log.info(Logs.fileline())

    get_init_var()
    get_user_data(session['user_name'])
    get_software_settings()

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

    # Load data patient
    if id_pat > 0:
        try:
            url = session['server_int'] + '/services/patient/det/' + str(id_pat)
            req = requests.get(url)

            if req.status_code == 200:
                json_data = req.json()

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests patient det failed, err=%s , url=%s', err, url)
    else:
        # generate a code
        try:
            url = session['server_int'] + '/services/patient/generate/code'
            req = requests.get(url)

            if req.status_code == 200:
                json_data['code'] = req.json()

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests patient generate code failed, err=%s , url=%s', err, url)

    return render_template('det-patient.html', args=json_data)


# Page : external request details
@app.route('/det-req-ext/<string:entry>/<int:ref>')
def det_req_ext(entry='Y', ref=0):
    log.info(Logs.fileline() + ' : ref = ' + str(ref))

    json_ihm  = {}
    json_data = {}

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
                json_data['billing_pat'] = req.json()

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
                json_data['billing_pat'] = req.json()

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
@app.route('/administrative-record/<string:entry>/<int:id_rec>')
def administrative_record( entry='Y', id_rec=0):
    log.info(Logs.fileline() + ' : id_rec = ' + str(id_rec))

    json_data = {}
    json_data['data_analysis'] = []
    json_data['data_samples']  = []
    json_data['data_products'] = []
    json_data['record']        = []

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

    if entry == "N":
        log.error(Logs.fileline() + ' : DEBUG TODO administrative-record entry=N')

    return render_template('administrative-record.html', entry=entry, args=json_data)


# Page : contributors
@app.route('/contributors/')
def contributors():
    log.info(Logs.fileline())

    get_init_var()

    return render_template('contributors.html')

if __name__ == "__main__":
    app.run()
