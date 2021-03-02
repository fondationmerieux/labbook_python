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
import random

from logging.handlers import WatchedFileHandler
from datetime import datetime, date, timedelta

from flask import Flask, render_template, request, session, redirect, send_file
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

    if root.endswith('/'):
        root = root[:-1]

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
        url = session['server_int'] + '/services/setting/record/number'
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
        return render_template('login.html', rand=random.randint(0, 999))
    else:
        log.info(Logs.fileline() + ' : TRACE Labbook FRONT END Current')
        return redirect('/' + session['redirect_name'] + '/' + session['current_page'])


# Change la langue
@app.route("/lang/<string:lang>")
def lang(lang='fr_FR'):
    if lang == 'en_GB':
        session['lang_select'] = 'en_GB'
        session['date_format'] = Constants.cst_date_eu
        session.modified = True
    elif lang == 'en_US':
        session['lang_select'] = 'en_US'
        session['date_format'] = Constants.cst_date_us
        session.modified = True
    else:
        session['lang_select'] = 'fr_FR'
        session['date_format'] = Constants.cst_date_eu
        session.modified = True

    session['lang']  = lang
    session.modified = True

    return redirect('/' + session['redirect_name'] + '/' + session['current_page'])


@app.route("/disconnect")
def disconnect():
    log.info(Logs.fileline() + ' : TRACE Labbook FRONT END disconnect')
    url = session['server_ext'] + '/' + session['redirect_name']
    session.clear()
    return redirect(url)


# Page : homepage
@app.route('/homepage')
@app.route('/homepage/<string:login>')
def homepage(login=''):
    log.info(Logs.fileline() + ' : TRACE Homepage login=' + str(login))

    session['current_page'] = 'homepage'
    session.modified = True

    dt_start_req = datetime.now()

    json_data = {}

    if login:
        session['login'] = login
        session.modified = True
    elif 'login' in session and session['login']:
        login = session['login']

    get_user_data(login)
    get_software_settings()

    # Load pref_quality
    try:
        url = session['server_int'] + '/services/default/val/qualite'
        req = requests.get(url)

        if req.status_code == 200:
            ret = req.json()
            if ret and 'value' in ret:
                json_data['pref_quality'] = ret['value']
            else:
                json_data['pref_quality'] = 0

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests pref_quality failed, err=%s , url=%s', err, url)

    # Load pref_bill
    try:
        url = session['server_int'] + '/services/default/val/facturation'
        req = requests.get(url)

        if req.status_code == 200:
            ret = req.json()
            if ret and 'value' in ret:
                json_data['pref_bill'] = ret['value']
            else:
                json_data['pref_bill'] = 0

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests pref_bill failed, err=%s , url=%s', err, url)

    # Load nb_emer
    try:
        url = session['server_int'] + '/services/record/count/emergency'
        req = requests.get(url)

        if req.status_code == 200:
            json_data['nb_emer'] = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests count ermergency failed, err=%s , url=%s', err, url)

    # Load nb_rec_tech
    try:
        url = session['server_int'] + '/services/record/count/technician'
        req = requests.get(url)

        if req.status_code == 200:
            json_data['nb_rec_tech'] = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests count technician records failed, err=%s , url=%s', err, url)

    # Load nb_rec_bio
    try:
        url = session['server_int'] + '/services/record/count/biologist'
        req = requests.get(url)

        if req.status_code == 200:
            json_data['nb_rec_bio'] = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests count biologist records failed, err=%s , url=%s', err, url)

    # Load nb_rec
    try:
        url = session['server_int'] + '/services/record/count'
        req = requests.get(url)

        if req.status_code == 200:
            json_data['nb_rec'] = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests count records failed, err=%s , url=%s', err, url)

    # Load nb_rec_today
    try:
        url = session['server_int'] + '/services/record/count/today'
        req = requests.get(url)

        if req.status_code == 200:
            json_data['nb_rec_today'] = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests count today validated records failed, err=%s , url=%s', err, url)

    # Load last_record
    try:
        url = session['server_int'] + '/services/record/last'
        req = requests.get(url)

        if req.status_code == 200:
            json_data['record'] = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests last records failed, err=%s , url=%s', err, url)

    dt_stop_req = datetime.now()
    dt_time_req = dt_stop_req - dt_start_req

    log.info(Logs.fileline() + ' : DEBUG homepage processing time = ' + str(dt_time_req))

    return render_template('homepage.html', args=json_data, rand=random.randint(0, 999))


# --------------------
# --- Setting page ---
# --------------------

# Page : users list
@app.route('/setting-users')
def setting_users():
    log.info(Logs.fileline() + ' : TRACE setting users')

    session['current_page'] = 'setting-users'
    session.modified = True

    json_data = {}

    # Load list users
    try:
        url = session['server_int'] + '/services/user/list/' + str(session['user_id_group'])
        req = requests.post(url)

        if req.status_code == 200:
            json_data = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests user list failed, err=%s , url=%s', err, url)

    return render_template('setting-users.html', args=json_data, rand=random.randint(0, 999))


# Page : details user
@app.route('/setting-det-user/<int:user_id>')
def setting_det_user(user_id=0):
    log.info(Logs.fileline() + ' : TRACE setting det user=' + str(user_id))

    session['current_page'] = 'setting-det-user/' + str(user_id)
    session.modified = True

    json_ihm  = {}
    json_data = {}

    # Load sections
    try:
        url = session['server_int'] + '/services/dict/det/sections'
        req = requests.get(url)

        if req.status_code == 200:
            json_ihm['sections'] = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests sections failed, err=%s , url=%s', err, url) 

    if user_id > 0:
        # Load user details
        try:
            url = session['server_int'] + '/services/user/det/' + str(user_id)
            req = requests.get(url)

            if req.status_code == 200:
                json_data = req.json()

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests user det failed, err=%s , url=%s', err, url)

    json_data['user_id'] = user_id

    return render_template('setting-det-user.html', ihm=json_ihm, args=json_data, rand=random.randint(0, 999))


# Page : setting new password for a user
@app.route('/setting-pwd-user/<int:user_id>')
def setting_pwd_user(user_id=0):
    log.info(Logs.fileline() + ' : TRACE setting pwd user')

    session['current_page'] = 'setting-pwd-user/' + str(user_id)
    session.modified = True

    json_data = {}

    json_data['user_id'] = user_id

    return render_template('setting-pwd-user.html', args=json_data, rand=random.randint(0, 999))


# Page : dict list
@app.route('/setting-dicts')
def setting_dicts():
    log.info(Logs.fileline() + ' : TRACE setting dict')

    session['current_page'] = 'setting-dicts'
    session.modified = True

    json_data = {}

    # Load list dict
    try:
        url = session['server_int'] + '/services/dict/list'
        req = requests.post(url)

        if req.status_code == 200:
            json_data = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests dicts list failed, err=%s , url=%s', err, url)

    return render_template('setting-dicts.html', args=json_data, rand=random.randint(0, 999))


# Page : details dictionnary
@app.route('/setting-det-dict')
@app.route('/setting-det-dict/<string:dict_name>')
def setting_det_dict(dict_name=''):
    log.info(Logs.fileline() + ' : TRACE setting det dict=' + str(dict_name))

    session['current_page'] = 'setting-det-dict/' + str(dict_name)
    session.modified = True

    json_data = {}

    if dict_name:
        # Load dict details
        try:
            url = session['server_int'] + '/services/dict/det/' + str(dict_name)
            req = requests.get(url)

            if req.status_code == 200:
                json_data['data_values'] = req.json()

                i = 0
                for val in json_data['data_values']:
                    val['id_ihm'] = i
                    i += 1

                json_data['data_last_id'] = i

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests dict det failed, err=%s , url=%s', err, url)
    else:
        json_data['data_values'] = []

    json_data['dict_name'] = str(dict_name)

    return render_template('setting-det-dict.html', args=json_data, rand=random.randint(0, 999))


# Page : analyzes list
@app.route('/setting-analyzes')
def setting_analyzes():
    log.info(Logs.fileline() + ' : TRACE setting analyzes')

    session['current_page'] = 'setting-analyzes'
    session.modified = True

    json_ihm  = {}
    json_data = {}

    # Load analysis type
    try:
        url = session['server_int'] + '/services/dict/det/famille_analyse'
        req = requests.get(url)

        if req.status_code == 200:
            json_ihm['type_ana'] = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests analysis type failed, err=%s , url=%s', err, url)

    # Load products
    try:
        url = session['server_int'] + '/services/dict/det/type_prel'
        req = requests.get(url)

        if req.status_code == 200:
            json_ihm['products'] = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests products list failed, err=%s , url=%s', err, url)

    # Load list analyzes
    try:
        url = session['server_int'] + '/services/analysis/list'
        req = requests.post(url)

        if req.status_code == 200:
            json_data = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests analyzes list failed, err=%s , url=%s', err, url)

    return render_template('setting-analyzes.html', ihm=json_ihm, args=json_data, rand=random.randint(0, 999))


# Page : import analyzes list
@app.route('/import-analyzes')
def import_analyzes():
    log.info(Logs.fileline() + ' : TRACE import analyzes')

    session['current_page'] = 'import-analyzes'
    session.modified = True

    json_ihm  = {}
    json_data = {}

    return render_template('import-analyzes.html', ihm=json_ihm, args=json_data, rand=random.randint(0, 999))


# Page : details analysis
@app.route('/setting-det-analysis/<int:analysis_id>')
def setting_det_analysis(analysis_id=0):
    log.info(Logs.fileline() + ' : TRACE setting det analysis=' + str(analysis_id))

    session['current_page'] = 'setting-det-analysis/' + str(analysis_id)
    session.modified = True

    json_ihm  = {}
    json_data = {}

    # Load analysis type
    try:
        url = session['server_int'] + '/services/dict/det/famille_analyse'
        req = requests.get(url)

        if req.status_code == 200:
            json_ihm['type_ana'] = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests analysis type failed, err=%s , url=%s', err, url)

    # Load products
    try:
        url = session['server_int'] + '/services/dict/det/type_prel'
        req = requests.get(url)

        if req.status_code == 200:
            json_ihm['products'] = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests products list failed, err=%s , url=%s', err, url)

    if analysis_id > 0:
        # Load analysis details
        try:
            url = session['server_int'] + '/services/analysis/det/' + str(analysis_id)
            req = requests.get(url)

            if req.status_code == 200:
                json_data = req.json()

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests analysis det failed, err=%s , url=%s', err, url)

    json_data['analysis_id'] = analysis_id

    return render_template('setting-det-analysis.html', ihm=json_ihm, args=json_data, rand=random.randint(0, 999))


# Page : manage patient records
@app.route('/manage-pat-records')
def manage_pat_records():
    log.info(Logs.fileline() + ' : TRACE manage patient records')

    session['current_page'] = 'manage-pat-records'
    session.modified = True

    json_data = {}

    return render_template('manage-pat-records.html', args=json_data, rand=random.randint(0, 999))


# Page : setting stickers
@app.route('/setting-stickers')
def setting_stickers():
    log.info(Logs.fileline() + ' : TRACE setting stickers')

    session['current_page'] = 'setting-stickers'
    session.modified = True

    json_data = {}

    try:
        url = session['server_int'] + '/services/setting/sticker'
        req = requests.get(url)

        if req.status_code == 200:
            json_data = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests setting stickers failed, err=%s , url=%s', err, url)

    return render_template('setting-stickers.html', args=json_data, rand=random.randint(0, 999))


# Page : preferences list
@app.route('/setting-pref')
def setting_preferences():
    log.info(Logs.fileline() + ' : TRACE setting preferences')

    session['current_page'] = 'setting-pref'
    session.modified = True

    json_data = {}

    try:
        url = session['server_int'] + '/services/setting/pref/list'
        req = requests.get(url)

        if req.status_code == 200:
            json_data['pref_list'] = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests preferences list failed, err=%s , url=%s', err, url)

    return render_template('setting-pref.html', args=json_data, rand=random.randint(0, 999))


# Page : setting backup and restore
@app.route('/setting-backup')
def setting_backup():
    log.info(Logs.fileline() + ' : TRACE setting backup')

    session['current_page'] = 'setting-backup'
    session.modified = True

    json_data = {}

    try:
        url = session['server_int'] + '/services/setting/backup'
        req = requests.get(url)

        if req.status_code == 200:
            json_data = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests preferences list failed, err=%s , url=%s', err, url)

    return render_template('setting-backup.html', args=json_data, rand=random.randint(0, 999))


# Page : setting report
@app.route('/setting-report')
def setting_report():
    log.info(Logs.fileline() + ' : TRACE setting report')

    session['current_page'] = 'setting-report'
    session.modified = True

    json_data = {}

    # Load setting report
    try:
        url = session['server_int'] + '/services/setting/report'
        req = requests.get(url)

        if req.status_code == 200:
            json_data = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests setting report failed, err=%s , url=%s', err, url)

    return render_template('setting-report.html', args=json_data, rand=random.randint(0, 999))


# Page : setting record number
@app.route('/setting-rec-num')
def setting_rec_num():
    log.info(Logs.fileline() + ' : TRACE setting record number')

    session['current_page'] = 'setting-rec-num'
    session.modified = True

    json_data = {}

    # Load record number setting
    try:
        url = session['server_int'] + '/services/setting/record/number'
        req = requests.get(url)

        if req.status_code == 200:
            json_data = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests record number setting failed, err=%s , url=%s', err, url)

    return render_template('setting-rec-num.html', args=json_data, rand=random.randint(0, 999))


# Page : logo
@app.route('/setting-logo')
def setting_logo():
    log.info(Logs.fileline() + ' : TRACE setting logo')

    session['current_page'] = 'setting-logo'
    session.modified = True

    return render_template('setting-logo.html', rand=random.randint(0, 999))


# Page : age interval setting
@app.route('/setting-age-interval')
def setting_age_interval():
    log.info(Logs.fileline() + ' : TRACE setting age interval')

    session['current_page'] = 'setting-age-interval'
    session.modified = True

    json_data = {}

    # Load interval details
    try:
        url = session['server_int'] + '/services/setting/age/interval'
        req = requests.get(url)

        if req.status_code == 200:
            json_data['data_values'] = req.json()

            i = 0
            for val in json_data['data_values']:
                val['id_ihm'] = i
                i += 1

            json_data['data_last_id'] = i

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests dict det failed, err=%s , url=%s', err, url)

    return render_template('setting-age-interval.html', args=json_data, rand=random.randint(0, 999))


# ---------------------------
# --- Administrative page ---
# ---------------------------

# Page : list of results to enter
@app.route('/list-results')
def list_results():
    log.info(Logs.fileline() + ' : TRACE list-results')

    session['current_page'] = 'list-results'
    session.modified = True

    json_ihm  = {}
    json_data = {}

    dt_start_req = datetime.now()
    # Load analysis type
    try:
        url = session['server_int'] + '/services/dict/det/famille_analyse'
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

    return render_template('list-results.html', ihm=json_ihm, args=json_data, rand=random.randint(0, 999))


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
                            url = session['server_int'] + '/services/dict/det/' + str(type_res)
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

    return render_template('enter-result.html', ihm=json_ihm, args=json_data, rand=random.randint(0, 999))


# Page : List of records
@app.route('/list-records')
def list_records():
    log.info(Logs.fileline() + ' : TRACE list-records')

    session['current_page'] = 'list-records'
    session.modified = True

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
    return render_template('list-records.html', args=json_data, rand=random.randint(0, 999))


@app.route('/list-works/<string:user_role>')
@app.route('/list-works/<string:user_role>/<string:emer>')
def list_works(user_role='', emer=''):
    log.info(Logs.fileline() + ' : TRACE list-works user_role=' + str(user_role))

    session['current_page'] = 'list-works/' + str(user_role)
    session.modified = True

    json_ihm  = {}
    json_data = {}

    if emer:
        emer = 4

    dt_start_req = datetime.now()
    # Load list records with status filter
    try:
        payload = {'num_rec': '',
                   'stat_rec': 0,
                   'patient': '',
                   'date_beg': '',
                   'date_end': '',
                   'emer': emer}

        if user_role == 'B':
            # We lloking for emergency record in more record status
            if emer == 4:
                payload['stat_work'] = '(182,253,254,255)'
            else:
                payload['stat_work'] = '(254,255)'
        elif user_role == 'T':
            payload['stat_work'] = '(182,253)'

        json_ihm['stat_work'] = payload['stat_work']

        url = session['server_int'] + '/services/record/list/' + str(session['user_id_group'])
        req = requests.post(url, json=payload)

        if req.status_code == 200:
            json_data = json.dumps(req.json())
            if emer:
                json_ihm['emer'] = 'E'

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests works list failed, err=%s , url=%s', err, url)

    dt_stop_req = datetime.now()
    dt_time_req = dt_stop_req - dt_start_req

    log.info(Logs.fileline() + ' : DEBUG list-works processing time = ' + str(dt_time_req))
    return render_template('list-works.html', ihm=json_ihm, args=json_data, rand=random.randint(0, 999))


# Page : List of products to do or modify
@app.route('/list-products')
def list_products():
    log.info(Logs.fileline() + ' : TRACE list-products')

    session['current_page'] = 'list-products'
    session.modified = True

    json_data = {}

    dt_start_req = datetime.now()
    # Load list records
    try:
        url = session['server_int'] + '/services/product/list'
        req = requests.post(url)

        if req.status_code == 200:
            json_data = json.dumps(req.json())

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests products list failed, err=%s , url=%s', err, url)

    dt_stop_req = datetime.now()
    dt_time_req = dt_stop_req - dt_start_req

    log.info(Logs.fileline() + ' : DEBUG list-products processing time = ' + str(dt_time_req))
    return render_template('list-products.html', args=json_data, rand=random.randint(0, 999))


# Page : details of a product
@app.route('/det-product/<int:id_prod>')
def det_product(id_prod=0):
    log.info(Logs.fileline() + ' : TRACE det product=' + str(id_prod))

    session['current_page'] = 'det-product/' + str(id_prod)
    session.modified = True

    json_ihm  = {}
    json_data = {}

    # Load products statut
    try:
        url = session['server_int'] + '/services/dict/det/prel_statut'
        req = requests.get(url)

        if req.status_code == 200:
            json_ihm['products_statut'] = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests products statut list failed, err=%s , url=%s', err, url)

    # Load products type
    try:
        url = session['server_int'] + '/services/dict/det/type_prel'
        req = requests.get(url)

        if req.status_code == 200:
            json_ihm['products'] = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests products type list failed, err=%s , url=%s', err, url)

    # Load products location choice
    try:
        url = session['server_int'] + '/services/dict/det/lieu_prel'
        req = requests.get(url)

        if req.status_code == 200:
            json_ihm['products_location'] = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests products location list failed, err=%s , url=%s', err, url)

    if id_prod > 0:
        # Load product details
        try:
            url = session['server_int'] + '/services/product/det/' + str(id_prod)
            req = requests.get(url)

            if req.status_code == 200:
                json_data['product'] = req.json()

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests product det failed, err=%s , url=%s', err, url)

        # Load record details
        try:
            url = session['server_int'] + '/services/record/det/' + str(json_data['product']['id_rec'])
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

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests record det failed, err=%s , url=%s', err, url)

    json_data['id_prod'] = id_prod

    return render_template('det-product.html', ihm=json_ihm, args=json_data, rand=random.randint(0, 999))


# Page : doctors list (prescribers exactly)
@app.route('/list-doctors')
def list_doctors():
    log.info(Logs.fileline() + ' : TRACE list doctors')

    session['current_page'] = 'list-doctors'
    session.modified = True

    json_data = {}

    # Load list doctors
    try:
        url = session['server_int'] + '/services/doctor/list'
        req = requests.post(url)

        if req.status_code == 200:
            json_data = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests doctors list failed, err=%s , url=%s', err, url)

    return render_template('list-doctors.html', args=json_data, rand=random.randint(0, 999))


# Page : details doctor (prescribers exactly
@app.route('/det-doctor/<int:id_doctor>')
def det_doctor(id_doctor=0):
    log.info(Logs.fileline() + ' : TRACE setting det doctor=' + str(id_doctor))

    session['current_page'] = 'det-doctor/' + str(id_doctor)
    session.modified = True

    json_ihm  = {}
    json_data = {}

    # Load speciality
    try:
        url = session['server_int'] + '/services/dict/det/specialite'
        req = requests.get(url)

        if req.status_code == 200:
            json_ihm['spe_list'] = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests speciality list failed, err=%s , url=%s', err, url)

    if id_doctor > 0:
        # Load doctor details
        try:
            url = session['server_int'] + '/services/doctor/det/' + str(id_doctor)
            req = requests.get(url)

            if req.status_code == 200:
                json_data = req.json()

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests doctor det failed, err=%s , url=%s', err, url)

    json_data['id_doctor'] = id_doctor

    return render_template('det-doctor.html', ihm=json_ihm, args=json_data, rand=random.randint(0, 999))


# Page : new external request
@app.route('/new-req-ext')
def new_req_ext():
    log.info(Logs.fileline() + ' : TRACE new-req-ext')

    session['current_page'] = 'new-req-ext'
    session.modified = True

    return render_template('new-req-ext.html', rand=random.randint(0, 999))


# Page : new internal request
@app.route('/new-req-int')
def new_req_int():
    log.info(Logs.fileline() + ' : TRACE new-req-int')

    session['current_page'] = 'new-req-int'
    session.modified = True

    return render_template('new-req-int.html', rand=random.randint(0, 999))


# Page : patient details
@app.route('/det-patient/<int:id_pat>')
def det_patient(id_pat=0):
    log.info(Logs.fileline() + ' : TRACE det-patient id_pat = ' + str(id_pat))

    session['current_page'] = 'det-patient/' + str(id_pat)
    session.modified = True

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

    return render_template('det-patient.html', args=json_data, rand=random.randint(0, 999))


# Page : external request details
@app.route('/det-req-ext/<string:entry>/<int:ref>')
def det_req_ext(entry='Y', ref=0):
    log.info(Logs.fileline() + ' : TRACE det-req-ext ref = ' + str(ref))

    session['current_page'] = 'det-req-ext/' + str(entry) + '/' + str(ref)
    session.modified = True

    get_software_settings()

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
            url = session['server_int'] + '/services/dict/det/yorn'
            req = requests.get(url)

            if req.status_code == 200:
                json_ihm['yorn'] = req.json()

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests yorn list failed, err=%s , url=%s', err, url)

        # Load discount billing
        try:
            url = session['server_int'] + '/services/dict/det/remise_facturation'
            req = requests.get(url)

            if req.status_code == 200:
                json_ihm['discount_bill'] = req.json()

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests discount bill list failed, err=%s , url=%s', err, url)

        # Load products statut
        try:
            url = session['server_int'] + '/services/dict/det/prel_statut'
            req = requests.get(url)

            if req.status_code == 200:
                json_ihm['products_statut'] = req.json()

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests products statut list failed, err=%s , url=%s', err, url)

        # Load products
        try:
            url = session['server_int'] + '/services/dict/det/type_prel'
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
            url = session['server_int'] + '/services/dict/det/yorn'
            req = requests.get(url)

            if req.status_code == 200:
                json_ihm['yorn'] = req.json()

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests yorn list failed, err=%s , url=%s', err, url)

    dt_stop_req = datetime.now()
    dt_time_req = dt_stop_req - dt_start_req

    log.info(Logs.fileline() + ' : DEBUG det-req-ext processing time = ' + str(dt_time_req))

    return render_template('det-req-ext.html', entry=entry, ihm=json_ihm, args=json_data, rand=random.randint(0, 999))


# Page : internal request details
@app.route('/det-req-int/<string:entry>/<int:ref>')
def det_req_int(entry='Y', ref=0):
    log.info(Logs.fileline() + ' : TRACE det-req-int ref = ' + str(ref))

    session['current_page'] = 'det-req-int/' + str(entry) + '/' + str(ref)
    session.modified = True

    get_software_settings()

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
            url = session['server_int'] + '/services/dict/det/yorn'
            req = requests.get(url)

            if req.status_code == 200:
                json_ihm['yorn'] = req.json()

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests yorn list failed, err=%s , url=%s', err, url)

        # Load discount billing
        try:
            url = session['server_int'] + '/services/dict/det/remise_facturation'
            req = requests.get(url)

            if req.status_code == 200:
                json_ihm['discount_bill'] = req.json()

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests discount bill list failed, err=%s , url=%s', err, url)

        # Load products statut
        try:
            url = session['server_int'] + '/services/dict/det/prel_statut'
            req = requests.get(url)

            if req.status_code == 200:
                json_ihm['products_statut'] = req.json()

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests products statut list failed, err=%s , url=%s', err, url)

        # Load products
        try:
            url = session['server_int'] + '/services/dict/det/type_prel'
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
            url = session['server_int'] + '/services/dict/det/yorn'
            req = requests.get(url)

            if req.status_code == 200:
                json_ihm['yorn'] = req.json()

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests yorn list failed, err=%s , url=%s', err, url)

    return render_template('det-req-int.html', entry=entry, ihm=json_ihm, args=json_data, rand=random.randint(0, 999))


# Page : administrative record
@app.route('/administrative-record/<string:type_req>/<int:id_rec>')
def administrative_record(type_req='E', id_rec=0):
    log.info(Logs.fileline() + ' : TRACE administrative-record id_rec = ' + str(id_rec))

    session['current_page'] = 'administrative-record/' + str(type_req) + '/' + str(id_rec)
    session.modified = True

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
        url = session['server_int'] + '/services/file/document/list/REC/' + str(id_rec)
        req = requests.get(url)

        if req.status_code == 200:
            json_data['data_files'] = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests record list files failed, err=%s , url=%s', err, url)

    dt_stop_req = datetime.now()
    dt_time_req = dt_stop_req - dt_start_req

    log.info(Logs.fileline() + ' : DEBUG administrative-record processing time = ' + str(dt_time_req))

    return render_template('administrative-record.html', type_req=type_req, args=json_data, rand=random.randint(0, 999))


# Page : technical validation
@app.route('/technical-validation/<int:id_rec>')
def technical_validation(id_rec=0):
    log.info(Logs.fileline() + ' : TRACE technical-validation id_rec = ' + str(id_rec))

    session['current_page'] = 'technical-validation/' + str(id_rec)
    session.modified = True

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

    return render_template('technical-validation.html', ihm=json_ihm, args=json_data, rand=random.randint(0, 999))


# Page : biological validation
@app.route('/biological-validation/<string:mode>/<int:id_rec>')
def biological_validation(mode='', id_rec=0):
    log.info(Logs.fileline() + ' : TRACE biological-validation id_rec = ' + str(id_rec))

    session['current_page'] = 'biological-validation/' + str(id_rec)
    session.modified = True

    json_ihm  = {}
    json_data = {}

    json_data['data_reports'] = []

    id_pat = 0

    # Single or Group mode of validation
    if mode and mode == 'G':
        json_ihm['mode'] = mode
        # find next record to validate
        try:
            url = session['server_int'] + '/services/record/next/' + str(id_rec)
            req = requests.get(url)

            if req.status_code == 200:
                id_rec_next = req.json()
                if id_rec_next and id_rec_next > 0:
                    json_ihm['id_rec_next'] = id_rec_next
                else:
                    json_ihm['id_rec_next'] = ''

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests record next failed, err=%s , url=%s', err, url)
    else:
        json_ihm['mode'] = 'S'

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
        url = session['server_int'] + '/services/dict/det/motif_annulation'
        req = requests.get(url)

        if req.status_code == 200:
            json_ihm['cancel_reason'] = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests cancel reason failed, err=%s , url=%s', err, url)

    dt_stop_req = datetime.now()
    dt_time_req = dt_stop_req - dt_start_req

    log.info(Logs.fileline() + ' : DEBUG biological-validation processing time = ' + str(dt_time_req))

    return render_template('biological-validation.html', ihm=json_ihm, args=json_data, rand=random.randint(0, 999))


# --------------------
# --- Report page ---
# --------------------

# Page : report epidemiological
@app.route('/report-epidemio')
@app.route('/report-epidemio/<string:date_beg>/<string:date_end>')
def report_epidemio(date_beg='', date_end=''):
    log.info(Logs.fileline() + ' : TRACE report epidemio')

    session['current_page'] = 'report-epidemio'
    session.modified = True

    json_ihm  = {}
    json_data = {}

    # load data for statistic
    try:
        if not date_beg:
            date_beg = date.today()
            date_beg = date_beg - timedelta(days=31)
            date_beg = datetime.strftime(date_beg.replace(day=1), Constants.cst_isodate)
            # date_beg = "2019-01-01"  # TEST

        if not date_end:
            date_end = date.today()
            date_end = datetime.strftime(date_end, Constants.cst_isodate)

        json_data['date_beg'] = date_beg
        json_data['date_end'] = date_end

        payload = {'date_beg': date_beg,
                   'date_end': date_end}

        url = session['server_int'] + '/services/report/epidemio'
        req = requests.post(url, json=payload)

        if req.status_code == 200:
            json_data['epidemio'] = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests report epidemio failed, err=%s , url=%s', err, url)

    return render_template('report-epidemio.html', ihm=json_ihm, args=json_data, rand=random.randint(0, 999))


# Page : report statistic
@app.route('/report-statistic')
def report_statistic():
    log.info(Logs.fileline() + ' : TRACE report statistic')

    session['current_page'] = 'report-statistic'
    session.modified = True

    json_ihm  = {}
    json_data = {}

    # load age interval setting
    try:
        url = session['server_int'] + '/services/setting/age/interval'
        req = requests.get(url)

        if req.status_code == 200:
            json_ihm['age_interval'] = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests age interval setting failed, err=%s , url=%s', err, url)

    # load data for statistic
    try:
        date_beg = date.today()
        date_beg = date_beg - timedelta(days=31)
        date_beg = datetime.strftime(date_beg.replace(day=1), Constants.cst_isodate)

        date_end = date.today()
        date_end = datetime.strftime(date_end, Constants.cst_isodate)

        json_data['date_beg'] = date_beg
        json_data['date_end'] = date_end

        payload = {'date_beg': date_beg,
                   'date_end': date_end}

        url = session['server_int'] + '/services/report/stat'
        req = requests.post(url, json=payload)

        if req.status_code == 200:
            json_data['stat'] = json.dumps(req.json())

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests report stat failed, err=%s , url=%s', err, url)

    return render_template('report-statistic.html', ihm=json_ihm, args=json_data, rand=random.randint(0, 999))


# Page : report dhis2
@app.route('/report-dhis2')
def report_dhis2():
    log.info(Logs.fileline() + ' : TRACE report dhis2')

    session['current_page'] = 'report-dhis2'
    session.modified = True

    json_data = {}

    return render_template('report-dhis2.html', args=json_data, rand=random.randint(0, 999))


# Page : WHONET export
@app.route('/whonet-export')
def whonet_export():
    log.info(Logs.fileline() + ' : TRACE whonet-export')

    session['current_page'] = 'whonet-export'
    session.modified = True

    return render_template('whonet-export.html', rand=random.randint(0, 999))


# Page : historic patients
@app.route('/hist-patients')
def hist_patients():
    log.info(Logs.fileline() + ' : TRACE hist patients')

    session['current_page'] = 'hist-patients'
    session.modified = True

    json_data = {}

    # Load list patients
    try:
        url = session['server_int'] + '/services/patient/list'
        req = requests.post(url)

        if req.status_code == 200:
            json_data = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests patients list failed, err=%s , url=%s', err, url)

    return render_template('hist-patients.html', args=json_data, rand=random.randint(0, 999))


# Page : details historic patient
@app.route('/det-hist-patient/<int:id_pat>')
def det_hist_patient(id_pat=0):
    log.info(Logs.fileline() + ' : TRACE det hist patient')

    session['current_page'] = 'det-hist-patient/' + str(id_pat)
    session.modified = True

    json_data = {}

    # Load details hitoric patient
    try:
        url = session['server_int'] + '/services/patient/historic/' + str(id_pat)
        req = requests.get(url)

        if req.status_code == 200:
            json_data = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests details hitoric patient failed, err=%s , url=%s', err, url)

    return render_template('det-hist-patient.html', args=json_data, rand=random.randint(0, 999))


# Page : historic analyzes
@app.route('/hist-analyzes')
def hist_analyzes():
    log.info(Logs.fileline() + ' : TRACE hist analyzes')

    session['current_page'] = 'hist-analyzes'
    session.modified = True

    json_ihm  = {}
    json_data = {}

    # Load analysis type
    try:
        url = session['server_int'] + '/services/dict/det/famille_analyse'
        req = requests.get(url)

        if req.status_code == 200:
            json_ihm['type_ana'] = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests analysis type failed, err=%s , url=%s', err, url)

    # Load list analyzes
    try:
        date_end = date.today()
        date_beg = date_end - timedelta(days=7)

        date_beg = datetime.strftime(date_beg, Constants.cst_isodate)
        date_end = datetime.strftime(date_end, Constants.cst_isodate)

        json_data['date_beg'] = date_beg
        json_data['date_end'] = date_end

        payload = {'date_beg': date_beg, 'date_end': date_end}

        url = session['server_int'] + '/services/analysis/historic/list'
        req = requests.post(url, json=payload)

        if req.status_code == 200:
            json_data['analyzes'] = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests analyzes list failed, err=%s , url=%s', err, url)

    return render_template('hist-analyzes.html', ihm=json_ihm, args=json_data, rand=random.randint(0, 999))


# Page : details historic patient
@app.route('/det-hist-analysis/<int:id_ana>/<string:date_beg>/<string:date_end>')
def det_hist_analysis(id_ana=0, date_beg='', date_end=''):
    log.info(Logs.fileline() + ' : TRACE det hist analysis')

    session['current_page'] = 'det-hist-analysis/' + str(id_ana) + '/' + date_beg + '/' + date_end
    session.modified = True

    json_data = {}

    # Load details hitoric analysis
    try:
        json_data['date_beg'] = date_beg
        json_data['date_end'] = date_end

        payload = {'date_beg': date_beg, 'date_end': date_end, 'id_ana': id_ana}

        url = session['server_int'] + '/services/analysis/historic/details'
        req = requests.post(url, json=payload)

        if req.status_code == 200:
            json_data['details'] = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests details hitoric analysis failed, err=%s , url=%s', err, url)

    return render_template('det-hist-analysis.html', args=json_data, rand=random.randint(0, 999))


# Page : report today
@app.route('/report-today')
def report_today():
    log.info(Logs.fileline() + ' : TRACE report today')

    session['current_page'] = 'report-today'
    session.modified = True

    json_data = {}

    try:
        date_end = date.today()
        date_beg = date_end - timedelta(days=1)

        date_beg = datetime.strftime(date_beg, Constants.cst_isodate)
        date_end = datetime.strftime(date_end, Constants.cst_isodate)

        json_data['date_beg'] = date_beg
        json_data['date_end'] = date_end

        payload = {'date_beg': date_beg, 'date_end': date_end}

        url = session['server_int'] + '/services/report/today'
        req = requests.post(url, json=payload)

        if req.status_code == 200:
            json_data['today_list'] = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests today list failed, err=%s , url=%s', err, url)

    return render_template('report-today.html', args=json_data, rand=random.randint(0, 999))


# Page : report billing
@app.route('/report-billing')
def report_billing():
    log.info(Logs.fileline() + ' : TRACE report billing')

    session['current_page'] = 'report-billing'
    session.modified = True

    json_ihm  = {}
    json_data = {}

    try:
        date_end = date.today()
        date_beg = date_end - timedelta(days=365)

        date_beg = datetime.strftime(date_beg, Constants.cst_isodate)
        date_end = datetime.strftime(date_end, Constants.cst_isodate)

        json_data['date_beg'] = date_beg
        json_data['date_end'] = date_end

        payload = {'date_beg': date_beg, 'date_end': date_end, 'id_user': 0}

        url = session['server_int'] + '/services/report/billing'
        req = requests.post(url, json=payload)

        if req.status_code == 200:
            json_data['bills'] = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests billing list failed, err=%s , url=%s', err, url)

    return render_template('report-billing.html', ihm=json_ihm, args=json_data, rand=random.randint(0, 999))


# --------------------
# --- Quality page ---
# --------------------

# Page : Quality General
@app.route('/quality-general')
def quality_general():
    log.info(Logs.fileline() + ' : TRACE quality-general')

    session['current_page'] = 'quality-general'
    session.modified = True

    json_data = {}

    # Load nb_users
    try:
        url = session['server_int'] + '/services/user/count'
        req = requests.get(url)

        if req.status_code == 200:
            json_data['nb_users'] = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests count users failed, err=%s , url=%s', err, url)

    # Load nb_manuals
    try:
        url = session['server_int'] + '/services/file/count/manual'
        req = requests.get(url)

        if req.status_code == 200:
            json_data['nb_manuals'] = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests count manuals failed, err=%s , url=%s', err, url)

    # Load last_meeting
    try:
        url = session['server_int'] + '/services/quality/last/meeting'
        req = requests.get(url)

        if req.status_code == 200:
            json_data['meeting'] = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests last meeting failed, err=%s , url=%s', err, url)

    # Load nb_noncompliances_open
    try:
        url = session['server_int'] + '/services/quality/count/noncompliance/open'
        req = requests.get(url)

        if req.status_code == 200:
            json_data['nb_noncompliances_open'] = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests count noncompliances open failed, err=%s , url=%s', err, url)

    # Load nb_noncompliances_month
    try:
        url = session['server_int'] + '/services/quality/count/noncompliance/month'
        req = requests.get(url)

        if req.status_code == 200:
            json_data['nb_noncompliances_month'] = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests count noncompliances month failed, err=%s , url=%s', err, url)

    return render_template('quality-general.html', args=json_data, rand=random.randint(0, 999))


# Page : list laboratory
@app.route('/list-laboratory')
def list_laboratory():
    log.info(Logs.fileline() + ' : TRACE list laboratory')

    session['current_page'] = 'list-laboratory'
    session.modified = True

    json_data = {}

    # Load laboratory files
    try:
        url = session['server_int'] + '/services/file/document/list/LABO/1'
        req = requests.get(url)

        if req.status_code == 200:
            json_data['data_files'] = req.json()
            log.error(Logs.fileline() + ' : DEBUG json data file=' + str(json_data['data_files']))

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests laboratory files failed, err=%s , url=%s', err, url)

    # Load dict details
    try:
        url = session['server_int'] + '/services/dict/det/sections'
        req = requests.get(url)

        if req.status_code == 200:
            json_data['data_values'] = req.json()

            i = 0
            for val in json_data['data_values']:
                val['id_ihm'] = i
                i += 1

            json_data['data_last_id'] = i

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests dict det failed, err=%s , url=%s', err, url)

    json_data['dict_name'] = 'sections'

    return render_template('list-laboratory.html', args=json_data, rand=random.randint(0, 999))


# Page : list staff
@app.route('/list-staff')
def list_staff():
    log.info(Logs.fileline() + ' : TRACE list staff')

    session['current_page'] = 'list-staff'
    session.modified = True

    json_data = {}

    try:
        url = session['server_int'] + '/services/user/list/' + str(session['user_id_group'])
        req = requests.post(url)

        if req.status_code == 200:
            json_data = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests user list failed, err=%s , url=%s', err, url)

    return render_template('list-staff.html', args=json_data, rand=random.randint(0, 999))


# Page : details staff
@app.route('/det-staff/<int:user_id>')
def det_staff(user_id=0):
    log.info(Logs.fileline() + ' : TRACE det staff=' + str(user_id))

    session['current_page'] = 'det-staff/' + str(user_id)
    session.modified = True

    json_ihm  = {}
    json_data = {}

    # Load sections
    try:
        url = session['server_int'] + '/services/dict/det/sections'
        req = requests.get(url)

        if req.status_code == 200:
            json_ihm['sections'] = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests sections failed, err=%s , url=%s', err, url)

    # Load User CV files
    try:
        url = session['server_int'] + '/services/file/document/list/USCV/' + str(user_id)
        req = requests.get(url)

        if req.status_code == 200:
            json_data['data_USCV'] = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests User CV files failed, err=%s , url=%s', err, url)

    # Load User Diploma files
    try:
        url = session['server_int'] + '/services/file/document/list/USDI/' + str(user_id)
        req = requests.get(url)

        if req.status_code == 200:
            json_data['data_USDI'] = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests User Diploma files failed, err=%s , url=%s', err, url)

    # Load User Training files
    try:
        url = session['server_int'] + '/services/file/document/list/USTR/' + str(user_id)
        req = requests.get(url)

        if req.status_code == 200:
            json_data['data_USTR'] = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests User Training files failed, err=%s , url=%s', err, url)

    # Load User Evaluation files
    try:
        url = session['server_int'] + '/services/file/document/list/USEV/' + str(user_id)
        req = requests.get(url)

        if req.status_code == 200:
            json_data['data_USEV'] = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests User Evaluation files failed, err=%s , url=%s', err, url)

    if user_id > 0:
        # Load user details
        try:
            url = session['server_int'] + '/services/user/det/' + str(user_id)
            req = requests.get(url)

            if req.status_code == 200:
                json_data['user_det'] = req.json()
            else:
                json_data['user_det'] = []

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests user det failed, err=%s , url=%s', err, url)

    json_data['user_id'] = user_id

    return render_template('det-staff.html', ihm=json_ihm, args=json_data, rand=random.randint(0, 999))


# Page : list equipment
@app.route('/list-equipment')
def list_equipment():
    log.info(Logs.fileline() + ' : TRACE list equipment')

    session['current_page'] = 'list-equipment'
    session.modified = True

    json_data = {}

    try:
        url = session['server_int'] + '/services/quality/equipment/list'
        req = requests.get(url)

        if req.status_code == 200:
            json_data = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests equipment list failed, err=%s , url=%s', err, url)

    return render_template('list-equipment.html', args=json_data, rand=random.randint(0, 999))


# Page : details equipment
@app.route('/det-equipment/<int:id_eqp>')
def det_equipment(id_eqp=0):
    log.info(Logs.fileline() + ' : TRACE det equipment=' + str(id_eqp))

    session['current_page'] = 'det-equipment/' + str(id_eqp)
    session.modified = True

    json_ihm  = {}
    json_data = {}

    # Load sections
    try:
        url = session['server_int'] + '/services/dict/det/sections'
        req = requests.get(url)

        if req.status_code == 200:
            json_ihm['sections'] = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests sections failed, err=%s , url=%s', err, url)

    if id_eqp > 0:
        # Load Equipment Photo files
        try:
            url = session['server_int'] + '/services/file/document/list/EQPH/' + str(id_eqp)
            req = requests.get(url)

            if req.status_code == 200:
                json_data['data_EQPH'] = req.json()

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests Equipment Photo files failed, err=%s , url=%s', err, url)

        # Load Equipment Breakdown files
        try:
            url = session['server_int'] + '/services/file/document/list/EQBD/' + str(id_eqp)
            req = requests.get(url)

            if req.status_code == 200:
                json_data['data_EQBD'] = req.json()

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests Equipment Breakdown files failed, err=%s , url=%s', err, url)

        # Load Equipment Preventive Maintenance files
        try:
            url = session['server_int'] + '/services/file/document/list/EQPM/' + str(id_eqp)
            req = requests.get(url)

            if req.status_code == 200:
                json_data['data_EQPM'] = req.json()

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests Equipment Preventive Maintenance files failed, err=%s , url=%s', err, url)

        # Load Equipment Calibration Certificat files
        try:
            url = session['server_int'] + '/services/file/document/list/EQCC/' + str(id_eqp)
            req = requests.get(url)

            if req.status_code == 200:
                json_data['data_EQCC'] = req.json()

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests Equipment Calibration Certificat files failed, err=%s , url=%s', err, url)

        # Load Equipment Maintenance Contract files
        try:
            url = session['server_int'] + '/services/file/document/list/EQMC/' + str(id_eqp)
            req = requests.get(url)

            if req.status_code == 200:
                json_data['data_EQMC'] = req.json()

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests Equipment Maintenance Contract files failed, err=%s , url=%s', err, url)

        # Load Equipment Bill files
        try:
            url = session['server_int'] + '/services/file/document/list/EQBI/' + str(id_eqp)
            req = requests.get(url)

            if req.status_code == 200:
                json_data['data_USEV'] = req.json()

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests Equipment Bill files failed, err=%s , url=%s', err, url)

        # Load equipment details
        try:
            url = session['server_int'] + '/services/quality/equipment/det/' + str(id_eqp)
            req = requests.get(url)

            if req.status_code == 200:
                json_data['det_eqp'] = req.json()

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests equipment det failed, err=%s , url=%s', err, url)

    json_data['id_eqp'] = id_eqp

    return render_template('det-equipment.html', ihm=json_ihm, args=json_data, rand=random.randint(0, 999))


# Page : suppliers list
@app.route('/list-suppliers')
def list_suppliers():
    log.info(Logs.fileline() + ' : TRACE list suppliers')

    session['current_page'] = 'list-suppliers'
    session.modified = True

    json_data = {}

    # Load list suppliers
    try:
        url = session['server_int'] + '/services/quality/supplier/list'
        req = requests.get(url)

        if req.status_code == 200:
            json_data = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests suppliers list failed, err=%s , url=%s', err, url)

    return render_template('list-suppliers.html', args=json_data, rand=random.randint(0, 999))


# Page : details supplier
@app.route('/det-supplier/<int:id_supplier>')
def det_supplier(id_supplier=0):
    log.info(Logs.fileline() + ' : TRACE setting det supplier=' + str(id_supplier))

    session['current_page'] = 'det-supplier/' + str(id_supplier)
    session.modified = True

    json_data = {}

    if id_supplier > 0:
        # Load supplier details
        try:
            url = session['server_int'] + '/services/quality/supplier/det/' + str(id_supplier)
            req = requests.get(url)

            if req.status_code == 200:
                json_data = req.json()

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests supplier det failed, err=%s , url=%s', err, url)

    json_data['id_supplier'] = id_supplier

    return render_template('det-supplier.html', args=json_data, rand=random.randint(0, 999))


# Page : list manuals
@app.route('/list-manuals')
def list_manuals():
    log.info(Logs.fileline() + ' : TRACE list manuals')

    session['current_page'] = 'list-manuals'
    session.modified = True

    json_data = {}

    try:
        url = session['server_int'] + '/services/quality/manual/list'
        req = requests.get(url)

        if req.status_code == 200:
            json_data = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests manual list failed, err=%s , url=%s', err, url)

    return render_template('list-manuals.html', args=json_data, rand=random.randint(0, 999))


# Page : details manual
@app.route('/det-manual/<int:id_manual>')
def det_manual(id_manual=0):
    log.info(Logs.fileline() + ' : TRACE setting det manual=' + str(id_manual))

    session['current_page'] = 'det-manual/' + str(id_manual)
    session.modified = True

    json_ihm  = {}
    json_data = {}

    json_data['manual_det'] = []

    # Load sections
    try:
        url = session['server_int'] + '/services/dict/det/sections'
        req = requests.get(url)

        if req.status_code == 200:
            json_ihm['sections'] = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests sections failed, err=%s , url=%s', err, url)

    if id_manual > 0:
        # Load Manual files
        try:
            url = session['server_int'] + '/services/file/document/list/MANU/' + str(id_manual)
            req = requests.get(url)

            if req.status_code == 200:
                json_data['data_MANU'] = req.json()

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests Manual files failed, err=%s , url=%s', err, url)

        # Load manual details
        try:
            url = session['server_int'] + '/services/quality/manual/det/' + str(id_manual)
            req = requests.get(url)

            if req.status_code == 200:
                json_data['manual_det'] = req.json()

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests manual det failed, err=%s , url=%s', err, url)

    json_data['id_manual'] = id_manual

    return render_template('det-manual.html', ihm=json_ihm, args=json_data, rand=random.randint(0, 999))


# Page : list procedure
@app.route('/list-procedure')
def list_procedure():
    log.info(Logs.fileline() + ' : TRACE list procedure')

    session['current_page'] = 'list-procedure'
    session.modified = True

    json_data = {}

    try:
        url = session['server_int'] + '/services/quality/procedure/list'
        req = requests.get(url)

        if req.status_code == 200:
            json_data = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests procedure list failed, err=%s , url=%s', err, url)

    return render_template('list-procedure.html', args=json_data, rand=random.randint(0, 999))


# Page : details procedure
@app.route('/det-procedure/<int:id_procedure>')
def det_procedure(id_procedure=0):
    log.info(Logs.fileline() + ' : TRACE setting det procedure=' + str(id_procedure))

    session['current_page'] = 'det-procedure/' + str(id_procedure)
    session.modified = True

    json_ihm  = {}
    json_data = {}

    json_data['procedure'] = []

    # Load sections
    try:
        url = session['server_int'] + '/services/dict/det/sections'
        req = requests.get(url)

        if req.status_code == 200:
            json_ihm['sections'] = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests sections failed, err=%s , url=%s', err, url)

    if id_procedure > 0:
        # Load procdeure files
        try:
            url = session['server_int'] + '/services/file/document/list/PROC/' + str(id_procedure)
            req = requests.get(url)

            if req.status_code == 200:
                json_data['data_PROC'] = req.json()

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests Procedure files failed, err=%s , url=%s', err, url)

        # Load procedure details
        try:
            url = session['server_int'] + '/services/quality/procedure/det/' + str(id_procedure)
            req = requests.get(url)

            if req.status_code == 200:
                json_data['procedure'] = req.json()

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests procedure det failed, err=%s , url=%s', err, url)

    json_data['id_procedure'] = id_procedure

    return render_template('det-procedure.html', ihm=json_ihm, args=json_data, rand=random.randint(0, 999))


# Page : list stock
@app.route('/list-stock')
def list_stock():
    log.info(Logs.fileline() + ' : TRACE list stock')

    session['current_page'] = 'list-stock'
    session.modified = True

    json_ihm  = {}
    json_data = {}

    # Load product_type
    try:
        url = session['server_int'] + '/services/dict/det/product_type'
        req = requests.get(url)

        if req.status_code == 200:
            json_ihm['product_type'] = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests product type failed, err=%s , url=%s', err, url)

    # Load product_status
    try:
        url = session['server_int'] + '/services/dict/det/product_status'
        req = requests.get(url)

        if req.status_code == 200:
            json_ihm['product_status'] = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests product status failed, err=%s , url=%s', err, url)

    try:
        url = session['server_int'] + '/services/quality/stock/list'
        req = requests.post(url)

        if req.status_code == 200:
            json_data = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests stock list failed, err=%s , url=%s', err, url)

    return render_template('list-stock.html', ihm=json_ihm, args=json_data, rand=random.randint(0, 999))


# Page : details of a product
@app.route('/det-new-product/<int:prd_ser>')
def det_new_product(prd_ser=0):
    log.info(Logs.fileline() + ' : TRACE setting det new product=' + str(prd_ser))

    session['current_page'] = 'det-new-product/' + str(prd_ser)
    session.modified = True

    json_ihm  = {}
    json_data = {}

    json_data['stock_product'] = []

    # Load product_type
    try:
        url = session['server_int'] + '/services/dict/det/product_type'
        req = requests.get(url)

        if req.status_code == 200:
            json_ihm['product_type'] = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests product type failed, err=%s , url=%s', err, url)

    # Load product_conserv
    try:
        url = session['server_int'] + '/services/dict/det/product_conserv'
        req = requests.get(url)

        if req.status_code == 200:
            json_ihm['product_conserv'] = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests product conserv failed, err=%s , url=%s', err, url)

    if prd_ser > 0:
        # Load stock product details
        try:
            url = session['server_int'] + '/services/quality/stock/product/det/' + str(prd_ser)
            req = requests.get(url)

            if req.status_code == 200:
                json_data['stock_product'] = req.json()

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests stock product det failed, err=%s , url=%s', err, url)

    json_data['prd_ser'] = prd_ser

    return render_template('det-new-product.html', ihm=json_ihm, args=json_data, rand=random.randint(0, 999))


# Page : details a stock product
@app.route('/det-stock-product/<int:prs_ser>')
def det_stock_product(prs_ser=0):
    log.info(Logs.fileline() + ' : TRACE setting det stock product=' + str(prs_ser))

    session['current_page'] = 'det-stock-product/' + str(prs_ser)
    session.modified = True

    json_ihm  = {}
    json_data = {}

    json_data['stock_product'] = []

    # Load product_status
    try:
        url = session['server_int'] + '/services/dict/det/product_status'
        req = requests.get(url)

        if req.status_code == 200:
            json_ihm['product_status'] = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests product status failed, err=%s , url=%s', err, url)

    if prs_ser > 0:
        # Load stock product details
        try:
            url = session['server_int'] + '/services/quality/stock/product/det/' + str(prs_ser)
            req = requests.get(url)

            if req.status_code == 200:
                json_data['stock_product'] = req.json()

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests stock product det failed, err=%s , url=%s', err, url)

    json_data['prs_ser'] = prs_ser

    return render_template('det-stock-product.html', ihm=json_ihm, args=json_data, rand=random.randint(0, 999))


# Page : list nonconformities
@app.route('/list-nonconformities')
def list_nonconformities():
    log.info(Logs.fileline() + ' : TRACE list nonconformities')

    session['current_page'] = 'list-nonconformities'
    session.modified = True

    json_data = {}

    try:
        date_end = date.today()
        date_beg = date_end - timedelta(days=30)

        date_beg = datetime.strftime(date_beg, Constants.cst_isodate)
        date_end = datetime.strftime(date_end, Constants.cst_isodate)

        json_data['date_beg'] = date_beg
        json_data['date_end'] = date_end

        payload = {'date_beg': date_beg, 'date_end': date_end}

        url = session['server_int'] + '/services/quality/conformity/list'
        req = requests.post(url, json=payload)

        if req.status_code == 200:
            json_data['item_list'] = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests conformity list failed, err=%s , url=%s', err, url)

    return render_template('list-nonconformities.html', args=json_data, rand=random.randint(0, 999))


# Page : apply a non-conformity
@app.route('/non-conformity/<int:id_det>')
def non_conformity(id_det=0):
    log.info(Logs.fileline() + ' : TRACE non-conformity')

    session['current_page'] = 'non-conformity/' + str(id_det)
    session.modified = True

    json_data = {}

    json_data['details'] = []

    try:
        url = session['server_int'] + '/services/quality/nonconformity/det/' + str(id_det)
        req = requests.get(url)

        if req.status_code == 200:
            json_data['details'] = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests non-conformity details failed, err=%s , url=%s', err, url)

    json_data['id_det'] = id_det

    return render_template('non-conformity.html', args=json_data, rand=random.randint(0, 999))


# Page : list meeting
@app.route('/list-meeting')
def list_meeting():
    log.info(Logs.fileline() + ' : TRACE list meeting')

    session['current_page'] = 'list-meeting'
    session.modified = True

    json_data = {}

    try:
        url = session['server_int'] + '/services/quality/meeting/list'
        req = requests.get(url)

        if req.status_code == 200:
            json_data = req.json()

    except requests.exceptions.RequestException as err:
        log.error(Logs.fileline() + ' : requests meeting list failed, err=%s , url=%s', err, url)

    return render_template('list-meeting.html', args=json_data, rand=random.randint(0, 999))


# Page : details meeting
@app.route('/det-meeting/<int:id_meeting>')
def det_meeting(id_meeting=0):
    log.info(Logs.fileline() + ' : TRACE setting det meeting=' + str(id_meeting))

    session['current_page'] = 'det-meeting/' + str(id_meeting)
    session.modified = True

    json_data = {}

    json_data['meeting'] = []

    if id_meeting > 0:
        # Load meeting files
        try:
            url = session['server_int'] + '/services/file/document/list/MEET/' + str(id_meeting)
            req = requests.get(url)

            if req.status_code == 200:
                json_data['data_MEET'] = req.json()

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests Meeting files failed, err=%s , url=%s', err, url)

        # Load meeting details
        try:
            url = session['server_int'] + '/services/quality/meeting/det/' + str(id_meeting)
            req = requests.get(url)

            if req.status_code == 200:
                json_data['meeting'] = req.json()

        except requests.exceptions.RequestException as err:
            log.error(Logs.fileline() + ' : requests meeting det failed, err=%s , url=%s', err, url)

    json_data['id_meeting'] = id_meeting

    return render_template('det-meeting.html', args=json_data, rand=random.randint(0, 999))


# --------------------
# --- Various page ---
# --------------------

# Page : contributors
@app.route('/contributors')
def contributors():
    log.info(Logs.fileline() + ' : TRACE contributors')

    return render_template('contributors.html', rand=random.randint(0, 999))


# Route : download a file
@app.route('/download-file/type/<string:type>/name/<string:filename>/ref/<string:type_ref>/<string:ref>')
def download_file(type='', filename='', type_ref='', ref=''):
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
            url = session['server_int'] + '/services/file/document/' + str(type_ref) + '/' + str(ref)
            req = requests.get(url)

            if req.status_code == 200:
                file_info = req.json()

                if file_info:
                    filepath = os.path.join(file_info['storage'] + '/' + session['redirect_name'], file_info['path'])
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
    ret_file.headers["Cache-Control"] = 'no-store, must-revalidate'
    ret_file.headers["Expires"] = '0'

    return ret_file


# Route : upload a file form permanent storage
@app.route('/upload-file/<string:type_ref>/<int:id_ref>', methods=['POST'])
def upload_file(type_ref='', id_ref=0):
    log.info(Logs.fileline() + ' : type_ref = ' + str(type_ref) + ' | id_ref = ' + str(id_ref))
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
            log.error(Logs.fileline() + ' : upload-file-rec failed to hash name, err=%s', err)
            return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}

        try:
            # Get last storage path
            url = session['server_int'] + '/services/file/storage/' + str(session['user_id_group'])
            req = requests.get(url)

            if req.status_code == 200:
                storage = req.json()

                if not storage:
                    log.error(Logs.fileline() + ' : upload-file-rec storage failed')
                    return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}
        except Exception as err:
            log.error(Logs.fileline() + ' : upload-file failed requests storage, err=%s', err)
            return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}

        filepath = storage['path'] + '/sigl/'

        try:
            pathlib.Path(filepath + end_path[:2]).mkdir(mode=0o777, parents=False, exist_ok=True)
            pathlib.Path(filepath + end_path).mkdir(mode=0o777, parents=False, exist_ok=True)
        except Exception as err:
            log.error(Logs.fileline() + ' : upload-file-rec failed to filepath, err=%s', err)
            return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}

        try:
            f.save(os.path.join(filepath + end_path, generated_name))
        except Exception as err:
            log.error(Logs.fileline() + ' : upload-file-rec failed to save file, err=%s', err)
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

            url = session['server_int'] + '/services/file/document/' + str(type_ref) + '/' + str(id_ref)
            req = requests.post(url, json=payload)

            if req.status_code != 200:
                log.error(Logs.fileline() + ' : upload-file-rec insert failed')
                return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}

        except Exception as err:
            log.error(Logs.fileline() + ' : upload-file-rec failed information file, err=%s', err)
            return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}

        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

    return json.dumps({'success': False}), 405, {'ContentType': 'application/json'}


# Route : upload a logo for document
@app.route('/upload-logo', methods=['POST'])
def upload_logo():
    log.info(Logs.fileline())
    if request.method == 'POST':
        try:
            f = request.files['file']
        except Exception as err:
            log.error(Logs.fileline() + ' : upload-logo failed to get file from request, err=%s', err)
            return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}

        filepath  = '/space/www/apps/labbook/current/resources/images/'
        logo_name = 'logo.png'

        try:
            f.save(os.path.join(filepath, logo_name))
        except Exception as err:
            log.error(Logs.fileline() + ' : upload-logo failed to save file, err=%s', err)
            return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}

        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

    return json.dumps({'success': False}), 405, {'ContentType': 'application/json'}


# if __name__ == "__main__":
#    app.run()
