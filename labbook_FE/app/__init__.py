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

import logging
import requests

from logging.handlers import WatchedFileHandler
from datetime import datetime, date

from flask import Flask, render_template, request, session, json, redirect, url_for
from flask_babel import Babel, gettext

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

prep_log('log_front', r'./logs/log_front.log')

log = logging.getLogger('log_front')

app = Flask(__name__)  # , static_url_path='/labbook_FE/app/static')
app.config.from_object('default_settings')

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

    # init internal url server
    if not session or 'server_int' not in session:
        session['server_int'] = app.config.get('URL_SERVER_INT')
        session.modified = True

    # init external url server
    if not session or 'server_ext' not in session:
        session['server_ext'] = app.config.get('URL_SERVER_EXT')
        session.modified = True

    # init number version
    if not session or 'version' not in session:
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

        payload = {'date_beg': date_beg, 'date_end': date_end, 'emer_ana':0} 

        url = session['server_int'] + '/services/result/list'
        req = requests.post(url, json=payload)

        if req.status_code == 200:
            json_data = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests results list failed, err=%s , url=%s', err, url)

    return render_template('list-results.html', ihm=json_ihm, args=json_data)


# Page : enter result
@app.route('/enter-result/')
def enter_result():
    log.info(Logs.fileline())

    # TODO load from id_data

    return render_template('enter-result.html')


# Page : List of records
@app.route('/list-records/')
def list_records():
    log.info(Logs.fileline())

    get_init_var()
    get_user_data(session['user_name'])

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

    return render_template('new-req-ext.html')


# Page : new internal request
@app.route('/new-req-int/')
def new_req_int():
    log.info(Logs.fileline())

    get_init_var()
    get_user_data(session['user_name'])

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

    return render_template('det-patient.html', args=json_data)


# Page : external request details
@app.route('/det-req-ext/<string:entry>/<int:id_pat>')
def det_req_ext(entry='Y', id_pat=0):
    log.info(Logs.fileline() + ' : id_pat = ' + str(id_pat))

    json_ihm  = {}
    json_data = {}

    if entry == "Y":
        # Load data patient
        if id_pat > 0:
            try:
                url = session['server_int'] + '/services/patient/det/' + str(id_pat)
                req = requests.get(url)

                if req.status_code == 200:
                    json_data = req.json()

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

    else:
        json_data = session['data_save']

    return render_template('det-req-ext.html', entry=entry, ihm=json_ihm, args=json_data)


# Page : internal request details
@app.route('/det-req-int/<string:entry>/<int:id_pat>')
def det_req_int(entry='Y', id_pat=0):
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

    return render_template('det-req-int.html', entry=entry, args=json_data)


# Page : administrative record
@app.route('/administrative-record/<string:entry>/<int:id_pat>')
def administrative_record( entry='Y', id_pat=0):
    log.info(Logs.fileline() + ' : id_pat = ' + str(id_pat))

    json_data = {}

    if entry == "Y":
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
        json_data = session['data_save']

    return render_template('administrative-record.html', entry=entry, args=json_data)


# Page : save data for reloading a page with this data
@app.route('/save-data/', methods=['POST'])
def save_data():
    log.info(Logs.fileline())

    session['data_save'] = request.get_json()
    session.modified = True

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


# Page : contributors
@app.route('/contributors/')
def contributors():
    log.info(Logs.fileline())

    get_init_var()

    return render_template('contributors.html')

if __name__ == "__main__":
    app.run()
