#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@project_name : Labbook Front End

@author: Alexandre CHARLES <ac@aegle.fr>
@creation_date: 20/11/2019
"""

# =============================================================================
# LabBook Front-End application entry point
# -----------------------------------------------------------------------------
# Creates the Flask application instance.
#
# Responsibilities of this module:
# - Load configuration (default_settings + optional LOCAL_SETTINGS)
# - Configure file-based logging
# - Initialize session lifetime and cookie parameters
# - Initialize Flask-Babel for language handling
# - Provide helpers for authenticated calls to the Back-End (BE)
# - Store user and system data in session
#
# The FE communicates with the BE through HTTP requests.
# OAuth access tokens are stored in session under 'be_access_token'.
#
# This file centralizes:
# - Application bootstrap
# - Session management
# - BE communication helpers
# - Jinja context injection and filters
# =============================================================================

# ###########################################
#   Imports
# ###########################################

import os
import logging
import requests
import json
import uuid
import secrets
import base64
import re
import tomllib

from logging.handlers import WatchedFileHandler
from datetime import datetime, date, timedelta
from urllib.parse import quote, urlencode
from werkzeug.utils import secure_filename

from flask import Flask, render_template, render_template_string, request, session, redirect, send_file, Response, url_for, jsonify, current_app
from flask_babel import Babel

from app.models.Logs import Logs
from app.models.Constants import Constants
from app.models.Form import Form

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


# -----------------------------------------------------------------------------
# Logging setup
# -----------------------------------------------------------------------------
# Configures a dedicated logger named "log_front".
# Logs are written to a file using WatchedFileHandler.
# The handler supports external log rotation.
# No console logging is used.
# -----------------------------------------------------------------------------
def prep_log(logger_name, log_file, level=logging.INFO):
    logger = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(asctime)s : %(message)s')
    fileHandler = WatchedFileHandler(log_file)
    fileHandler.setFormatter(formatter)

    logger.setLevel(level)
    logger.addHandler(fileHandler)


prep_log('log_front', '/home/apps/logs/log_front.log')

log = logging.getLogger('log_front')

app = Flask(__name__)
app.config.from_object('default_settings')
app.permanent_session_lifetime = timedelta(hours=2)

# -----------------------------------------------------------------------------
# Configuration loading
# -----------------------------------------------------------------------------
# 1) Load base configuration from default_settings.
# 2) If environment variable LOCAL_SETTINGS exists:
#       - Load additional configuration from that file.
# 3) Optionally override REDIRECT_NAME using LABBOOK_URL_PREFIX.
#
# Configuration values are read at startup and stored in app.config.
# -----------------------------------------------------------------------------
config_envvar = 'LOCAL_SETTINGS'

if config_envvar in os.environ:
    log.info(Logs.fileline() + f' : Loaded config from {config_envvar}={os.environ[config_envvar]}')
    app.config.from_envvar(config_envvar)

    if app.config['APP_VERSION']:
        log.info(Logs.fileline() + ' : LABBOOK VERSION : ' + str(app.config['APP_VERSION']))

    # check if LABBOOK_URL_PREFIX already exist in os.environ if not use one from default_settings
    if 'LABBOOK_URL_PREFIX' in os.environ and os.environ['LABBOOK_URL_PREFIX']:
        app.config['REDIRECT_NAME'] = os.environ['LABBOOK_URL_PREFIX'].strip().strip('/')
        log.info(Logs.fileline() + ' : LABBOOK_URL_PREFIX from environ : ' + str(os.environ['LABBOOK_URL_PREFIX']))
    else:
        os.environ['LABBOOK_URL_PREFIX'] = app.config.get('REDIRECT_NAME')
else:
    print(("No local configuration available: {} is undefined in the environment".format(config_envvar)))

# --- Session cookie configuration ---
# These settings ensure the session persists across OAuth redirects,
# works under both HTTP and HTTPS, and covers all subpaths like /sigl/.
app.config['SESSION_COOKIE_NAME'] = 'labbook_fe_sess'   # explicit cookie name
app.config['SESSION_COOKIE_PATH'] = '/'                 # cookie valid everywhere
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'           # required for OAuth redirect (Strict, None needs HTTPS)
app.config['SESSION_COOKIE_SECURE'] = False             # must stay False because some sites still use HTTP

app.config.setdefault('OAUTH_CLIENT_ID', 'labbook-FE')

# Prefer LOCAL_SETTINGS; fallback to env LABBOOK_OAUTH_FE_SECRET; never log the value.
app.config['OAUTH_CLIENT_SECRET'] = (
    app.config.get('OAUTH_CLIENT_SECRET') or os.getenv('LABBOOK_OAUTH_FE_SECRET', '')
)

# app.config["CACHE_TYPE"] = "null"  # NOTE : Use if flask keep translation in cache

babel = Babel(app)


# -----------------------------------------------------------------------------
# Per-request session management
# -----------------------------------------------------------------------------
# Executed before each request.
#
# - Checks inactivity timeout (2 hours).
# - Redirects to 'disconnect' if expired.
# - Generates a per-request nonce.
# - Stores user agent in session.
# - Updates last activity timestamp.
# -----------------------------------------------------------------------------
@app.before_request
def before_request_func():
    last = session.get('last_activity')
    now  = datetime.now()
    if last:
        try:
            last_dt = datetime.fromisoformat(last)
            if (now - last_dt) > timedelta(hours=2):
                if request.endpoint != 'disconnect':
                    return redirect(url_for('disconnect'))
        except Exception:
            pass

    nonce = uuid.uuid1()

    session['nonce'] = str(nonce)

    user_agent = request.headers.get('User-Agent')
    session['user_agent'] = user_agent
    session['last_activity'] = now.isoformat(timespec='seconds')
    session.permanent = True
    session.modified = True


LANG_SELECT = {
    'fr_FR': 'FR', 'en_GB': 'UK', 'en_US': 'US', 'es': 'ES',
    'ar': 'AR', 'km': 'KM', 'lo': 'LO', 'mg': 'MG', 'pt': 'PT'
}

EU_FORMAT_LANGS = {'fr_FR', 'en_GB', 'es', 'ar', 'km', 'lo', 'mg', 'pt'}


@app.context_processor
def locale():
    lang = app.config.get('BABEL_DEFAULT_LOCALE')
    if session and 'lang' in session:
        lang = session['lang']
        log.info(Logs.fileline() + ' : lang = ' + lang)

        session['lang_select'] = LANG_SELECT.get(lang, 'FR')
        if lang in EU_FORMAT_LANGS:
            session['date_format'] = Constants.cst_date_eu
            session['dt_format']   = Constants.cst_dt_eu_HM
        else:
            session['date_format'] = Constants.cst_date_us
            session['dt_format']   = Constants.cst_dt_us_HM

        session.modified = True

    return dict(locale=lang)


@app.context_processor
def inject_app_version():
    # value is global FE version from config, not per-session
    return {"app_version": app.config.get("APP_VERSION", "")}


# -----------------------------------------------------------------------------
# Back-End (BE) communication helpers
# -----------------------------------------------------------------------------
# These functions handle:
#
# - Building the Authorization header from session token
# - Redirecting to OAuth if token is missing
# - Handling HTTP 401 responses from the BE
#
# All BE calls must use the session key 'be_access_token'.
# Token validation logic is centralized in these helpers.
# -----------------------------------------------------------------------------
def be_auth_headers():
    """
    Build Authorization header from the session access token.
    Returns {} if no token (caller should already have ensured OAuth).
    """
    token = session.get('be_access_token')
    if token:
        return {'Authorization': f'Bearer {token}'}
    return {}


def ensure_be_token():
    """
    Guard before calling the BE: if the session has NO access token,
    remember the current URL and redirect to the OAuth entry point.
    Return None when the token already exists.
    NOTE: use the SAME session key everywhere: 'be_access_token'.
    """
    tok = session.get('be_access_token')  # exact same key used by templates/headers
    if not tok:                           # handles None and ""
        session['next'] = request.url     # remember where to come back
        session.modified = True
        return redirect(url_for('oauth_bounce'))
    return None


def be_check_or_bounce(resp):
    """
    Handle BE responses that indicate an expired/invalid token.
    On 401: drop the token, remember the current URL, and restart OAuth.
    Otherwise: return None so the caller can proceed.
    """
    # If BE returns 401, drop token and restart OAuth
    if resp.status_code == 401:
        session.pop('be_access_token', None)
        session['next'] = request.url
        session.modified = True
        return redirect(url_for('oauth_bounce'))
    return None


def be_get(path, what):
    """
    GET `path` on the BE and return the pair (data, redirect).

    data     : decoded JSON on a 200 answer, None otherwise, so the caller can
               leave its own default untouched when the call fails.
    redirect : response the caller must return at once when the token expired,
               None the rest of the time.
    what     : names the call in the log line, nothing else.
    """
    url = session['server_int'] + '/' + session['redirect_name'] + path

    try:
        req = requests.get(url, timeout=10, headers=be_auth_headers())

        redir = be_check_or_bounce(req)
        if redir:
            return None, redir

        if req.status_code == 200:
            return req.json(), None

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests ' + what + ' failed, url=%s', url)

    return None, None


def get_locale():
    """
    Selects the active language for the current request.

    - Uses browser Accept-Language as default.
    - Overrides with session['lang'] if defined.
    - Stores the selected language in session.
    """
    log.info(Logs.fileline() + ' : LANG = ' + str(os.environ['LANG']))
    lang = request.accept_languages.best_match(list(LANGUAGES.keys()), default='fr_FR')
    if not session or 'lang' not in session:
        session['lang'] = lang
        session.modified = True
        log.info(Logs.fileline() + ' :default lang=' + str(lang))
    elif session and 'lang' in session:
        lang = session['lang']
        log.info(Logs.fileline() + ' :session lang=' + str(lang))
    return lang


# 2023-05-02: Flask-Babel upgrade, locale is now provided via locale_selector (no decorator).
babel.init_app(app, locale_selector=get_locale)


def check_init_version():
    """
    Check Back-End availability by calling the version endpoint.

    Sets session['labbook_BE_OK'] to True if BE responds with 200 or 401,
    otherwise sets it to False.
    """
    log.info(Logs.fileline() + ' : LABBOOK_FE check_init_version begins')

    ensure_base_urls_in_session()

    try:
        url = session['server_int'] + '/' + session['redirect_name'] + '/services/init/version'
        req = requests.get(url, timeout=10)

        if req.status_code in (200, 401):
            session['labbook_BE_OK'] = True
        else:
            session['labbook_BE_OK'] = False

        session.modified = True
        return None

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests check init version failed, url=%s', url)
        session['labbook_BE_OK'] = False
        session.modified = True
        return None


def ensure_base_urls_in_session():
    """
    Ensure base URLs are present in session.

    - server_ext: external URL used for browser redirects.
    - server_int: internal BE base URL used for FE → BE calls.
    - redirect_name: optional URL prefix if application is mounted under a subpath.
    """
    # External base for browser redirects
    root = request.url_root.rstrip('/')
    if request.headers.get('X-Forwarded-Proto') == 'https' and root.startswith('http://'):
        root = 'https://' + root[len('http://'):]
    session.setdefault('server_ext', root)

    # Internal base for FE->BE back-channel (from config)
    server_int = str(current_app.config.get('SERVER_INT') or '').strip()
    if server_int and not server_int.startswith(('http://', 'https://')):
        server_int = 'http://' + server_int
    session.setdefault('server_int', server_int.rstrip('/'))

    # Optional path prefix if the app is mounted under a subpath
    rn = (current_app.config.get('REDIRECT_NAME') or request.environ.get('SCRIPT_NAME', '')).strip('/')
    session.setdefault('redirect_name', rn)

    session.modified = True


def get_init_var():
    """
    Load runtime configuration values from the Back-End into session.

    Retrieves:
    - application version
    - auto logout delay
    - default and database languages
    - stock settings
    - form settings
    - report settings
    """
    log.info(Logs.fileline() + ' : LABBOOK_FE get_init_var begins')

    ensure_base_urls_in_session()

    call_headers = be_auth_headers()

    # init number version
    if not session or 'version' not in session or session['version'] != app.config.get('APP_VERSION'):
        session['version'] = app.config.get('APP_VERSION')
        session.modified = True

    # Load auto_logout
    try:
        log.info(Logs.fileline() + ' : LABBOOK_FE first request to LABBOOK_BE')
        url = session['server_int'] + '/' + session['redirect_name'] + '/services/default/val/auto_logout'
        req = requests.get(url, timeout=10, headers=call_headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            ret_json = req.json()
            session['auto_logout'] = ret_json['value']
            session['labbook_BE_OK'] = True
            session.modified = True
        else:
            session['labbook_BE_OK'] = False
            session.modified = True

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests auto_logout failed, url=%s', url)

    # Load default language
    try:
        url = session['server_int'] + '/' + session['redirect_name'] + '/services/default/val/default_language'
        req = requests.get(url, timeout=10, headers=call_headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            ret_json = req.json()
            session['lang_pdf'] = ret_json['value']
            session.modified = True

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests default_language failed, url=%s', url)

    # Load db language
    try:
        url = session['server_int'] + '/' + session['redirect_name'] + '/services/default/val/db_language'
        req = requests.get(url, timeout=10, headers=call_headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            ret_json = req.json()
            session['lang_db'] = ret_json['value']
            session.modified = True

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests db_language failed, url=%s', url)

    # Load stock setting
    try:
        url = session['server_int'] + '/' + session['redirect_name'] + '/services/setting/stock'
        req = requests.get(url, timeout=10, headers=call_headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            ret_json = req.json()
            session['stock_expir_warning'] = ret_json['sos_expir_warning']
            session['stock_expir_alert']   = ret_json['sos_expir_alert']
            session.modified = True

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests default_language failed, url=%s', url)

    # Load form setting
    try:
        url = session['server_int'] + '/' + session['redirect_name'] + '/services/setting/form/list'
        req = requests.get(url, timeout=10, headers=call_headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            l_fos = req.json()

            for fos in l_fos:
                session[fos['fos_ref']] = fos['fos_stat']
                session.modified = True

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests form setting failed, url=%s', url)

    # Load setting report
    try:
        url = session['server_int'] + '/' + session['redirect_name'] + '/services/setting/report'
        req = requests.get(url, timeout=10, headers=call_headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            json_data = req.json()

            session['report_pwd'] = (json_data.get('report_pwd') or 'N').strip().upper()
            session.modified = True

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests setting report failed, url=%s', url)

    try:
        path = os.path.join(Constants.cst_io, 'amicare.toml')

        if os.path.exists(path):
            with open(path, 'rb') as f:
                cfg = tomllib.load(f)

            session['amicare'] = cfg.get('amicare', {})
        else:
            session['amicare'] = {}

        session.modified = True

    except Exception:
        log.exception(Logs.fileline() + ' : load amicare.toml failed')
        session['amicare'] = {}

    log.info(Logs.fileline() + ' : LABBOOK_FE get_init_var ends')


def get_user_data(login, be_headers=None):
    """
    Load authenticated user profile and permissions from the Back-End.

    Stores in session:
    - user identity and role
    - UI colors
    - granted rights
    - linked analyze families (if applicable)
    """
    if not login:
        log.error(Logs.fileline() + ' : get_user_data ERROR no login')
        return disconnect()  # redirect(session['server_ext'] + '/disconnect')

    call_headers = be_auth_headers()

    try:
        if 'server_int' not in session or not session['server_int']:
            index()

        url = session['server_int'] + '/' + session['redirect_name'] + '/services/user/login/' + login
        req = requests.get(url, timeout=10, headers=call_headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            json = req.json()

            session['user_id']        = json['id_data']
            session['user_role']      = json['role_type']
            session['user_id_role']   = json['role_pro']
            session['user_name']      = json['username']
            session['user_firstname'] = json['firstname']
            session['user_lastname']  = json['lastname']
            session['user_locale']    = json['locale']
            session['user_side_account'] = json['side_account']
            session['color_1']        = json['pro_color_1']
            session['color_2']        = json['pro_color_2']
            session['text_color']     = json['pro_text_color']
            session.modified = True

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests user login failed, url=%s', url)
        return None

    # get all rights for this user
    try:
        url = session['server_int'] + '/' + session['redirect_name'] + '/services/user/rights/list/' + str(session['user_id'])
        req = requests.get(url, timeout=10, headers=call_headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            session['l_user_rights'] = req.json()
            session.modified = True
        else:
            session['l_user_rights'] = []
            session.modified = True

        # log.info(Logs.fileline() + ' : DEBUG l_user_rights = ' + str(session['l_user_rights']))

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests list of user rights failed, url=%s', url)
        return None

    # Get analyzes families linked functionnal unit for this user only for all secretary, technician and biologist
    if session['user_role'] not in ('API', 'Z'):
        try:
            url = session['server_int'] + '/' + session['redirect_name'] + '/services/setting/link/user/' + str(session['user_id'])
            req = requests.get(url, timeout=10, headers=call_headers)

            redir = be_check_or_bounce(req)
            if redir:
                return redir

            if req.status_code == 200:
                json = req.json()

                session['user_link_fam'] = []

                for data in json:
                    session['user_link_fam'].append(data['id_fam'])

                session.modified = True
            else:
                session['user_link_fam'] = []
                session.modified = True
        except requests.exceptions.RequestException:
            log.exception(Logs.fileline() + ' : requests setting link user failed, url=%s', url)
            return None
    else:
        session['user_link_fam'] = []
        session.modified = True

    return None


def get_software_settings(be_headers=None):
    call_headers = be_auth_headers()

    try:
        url = session['server_int'] + '/' + session['redirect_name'] + '/services/setting/record/number'
        req = requests.get(url, timeout=10, headers=call_headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            json = req.json()

            session['record_period'] = json['rstg_period']
            session['record_format'] = json['rstg_format']
            session['samp_mask'] = json['rstg_samp_mask']
            session['samp_regex'] = json['rstg_samp_regex']
            session.modified = True

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests software settings failed, url=%s', url)

    return None


def test_session():
    if 'login_ok' not in session or 'user_role' not in session or session['user_role'] not in ('A', 'B', 'T', 'TA', 'TQ', 'S', 'SA', 'P', 'Q', 'K', 'L', 'API', 'SP'):
        log.info(Logs.fileline() + ' : TRACE test_session KO, perhaps user_role not allowed')
        return False
    else:
        log.info(Logs.fileline() + ' : TRACE test_session OK')
        return True


@app.template_filter('date_format')
def date_format(date_iso):
    if date_iso:
        date_tmp = datetime.strptime(date_iso, Constants.cst_isodate)
        return datetime.strftime(date_tmp, session['date_format'])
    else:
        return


@app.template_filter('dt_format')
def dt_format(dt_iso):
    if dt_iso:
        date_tmp = datetime.strptime(dt_iso, Constants.cst_dt_HM)
        return datetime.strftime(date_tmp, session['dt_format'])
    else:
        return


@app.template_filter('date_now')
def date_now(date_now):
    return datetime.strftime(date.today(), "%Y-%m-%d")


@app.template_filter('datetime_now')
def datetime_now(datetime_now):
    return datetime.strftime(datetime.now(), "%Y-%m-%dT%H:%M")


def custom_style():
    background_color = session.get('color_1', '#333333')  # Default background color
    text_color = session.get('text_color', '#FFFFFF')     # Default text color
    hover_color = session.get('color_2', '#111111')       # Default hover background color

    background_color = background_color.strip('#')  # Remove leading #
    text_color = text_color.strip('#')
    hover_color = hover_color.strip('#')

    styles = f'''
    <style>
         /* style introduced by jinja2 with database role colors */
         .page-title-color
         {{
             background-color : #{background_color} !important;
             color            : #{text_color} !important;
         }}

        .menu-act-drop
        {{
             background-color : #{background_color} !important;
             color            : #{text_color} !important;
        }}

        .menu-act-item:hover
        {{
             background-color : #{hover_color} !important;
             color            : #{text_color} !important;
        }}

        .nav-style a
        {{
             background-color : #{background_color} !important;
             color            : #{text_color} !important;
             border           : 0;
        }}

        .nav-style a:hover
        {{
             background-color : #{hover_color} !important;
             color            : #{text_color} !important;
        }}
    </style>
    '''

    return styles


app.jinja_env.globals.update(custom_style=custom_style)


def has_permission(prr_tag):
    """
    Checks if a user has a specific permission.

    Args:
        prr_tag (str): The tag identifier of the permission (prr_type_prr_ser).
        prp_granted (str): The expected state of the permission ('Y' for granted, 'N' for not granted).

    Returns:
        bool: True if the user has the specified permission with the expected state, otherwise False.
    """
    l_user_rights = session.get('l_user_rights', [])
    return any(right['prr_tag'] == prr_tag and right['prp_granted'] == 'Y' for right in l_user_rights)


def has_permission_by_ser(prr_sers):
    """
    Checks if the user has a specific permission by prr_ser.

    Args:
        prr_sers (int or list): A single prr_ser or a list of prr_ser to check.
        prp_granted (str): The expected permission state ('Y' for granted, 'N' for not granted).

    Returns:
        bool: True if the user has any matching permission with the expected state, otherwise False.
    """
    l_user_rights = session.get('l_user_rights', [])

    # Ensure prr_sers is iterable (convert single int to list)
    if isinstance(prr_sers, int):
        prr_sers = [prr_sers]

    # Check if any permission matches
    return any(right['prr_ser'] in prr_sers and right['prp_granted'] == 'Y' for right in l_user_rights)


app.jinja_env.globals.update(has_permission=has_permission)
app.jinja_env.globals.update(has_permission_by_ser=has_permission_by_ser)


def safe_build_download_path(base_dir: str, user_name: str) -> str | None:
    """
    Build a safe absolute path inside base_dir.

    - Sanitizes filename.
    - Prevents directory traversal.
    - Returns None if validation fails.
    """
    try:
        base_dir_abs = os.path.abspath(base_dir or '')
        safe_name = secure_filename(user_name or '')
        if not base_dir_abs or not safe_name:
            return None

        target_path = os.path.abspath(os.path.join(base_dir_abs, safe_name))

        # Ensure the target path stays inside the allowed directory
        if not target_path.startswith(base_dir_abs + os.sep):
            return None

        return target_path
    except Exception:
        return None


# ######################################
# Routes Flask pages
# ######################################

# --- STARTS OAUTH ROUTES ---

@app.route('/confirm-access', methods=['POST'])
def confirm_access():
    """
    Finalize pre-login: store minimal user identity in the server session
    and return the next URL to navigate to. If a deferred redirect ('next')
    exists in session (e.g., started an OAuth flow), use it; otherwise fall
    back to the homepage with the provided login for display.
    """
    args = request.get_json()
    login = args.get('login', '')
    id_user = args.get('id_user', None)

    if id_user is None:
        return jsonify({'error': 'id_user missing'}), 400

    session.clear()

    session.permanent = True
    session['login_ok'] = login
    session['user_id'] = int(id_user)
    session.modified = True

    redirect_url = session.pop('next', None)
    if not redirect_url:
        redirect_url = url_for('homepage', login=str(session['login_ok']), _external=True)

    return jsonify({'redirect_url': redirect_url})


@app.route('/oauth/bounce')
def oauth_bounce():
    """
    Start the OAuth Authorization Code + PKCE dance.
    Optionally push the BE to bind user_id (confirm-access).
    Generate PKCE verifier and CSRF state, persist in session.
    Build /authorize URL from server_ext + redirect_name, then redirect.
    """

    ensure_base_urls_in_session()

    server_int = session.get('server_int')
    redirect_name = (session.get('redirect_name') or '').strip('/')

    # Optionally inform BE of the UI user
    user_id = session.get('user_id')
    if user_id:
        try:
            url_confirm = f"{server_int}/{redirect_name}/services/confirm-access" if redirect_name else f"{server_int}/services/confirm-access"
            requests.post(url_confirm, json={'id_user': int(user_id)}, timeout=5)
        except requests.RequestException:
            pass

    # Generate PKCE + state and persist in session
    verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).rstrip(b'=').decode('ascii')
    state = base64.urlsafe_b64encode(secrets.token_bytes(16)).rstrip(b'=').decode('ascii')
    session['oauth_pkce_verifier'] = verifier
    session['oauth_state'] = state
    session.modified = True

    # Redirect user to BE /authorize
    rn   = (session.get('redirect_name') or '').strip('/')
    base = (session.get('server_ext') or '').rstrip('/')

    if rn and base.endswith('/' + rn):
        auth_base = base
    elif rn:
        auth_base = f"{base}/{rn}"
    else:
        auth_base = base

    redirect_uri = f"/{rn}/oauth/callback" if rn else "/oauth/callback"
    params = {
        'client_id': 'labbook-FE',
        'response_type': 'code',
        'redirect_uri': redirect_uri,
        'code_challenge': verifier,
        'code_challenge_method': 'plain',
        'state': state,
    }
    auth_url = f"{auth_base}/services/oauth/authorize?{urlencode(params)}"

    log.info("OAUTH authorize redirect_uri=%s", redirect_uri)
    log.info("OAUTH authorize url=%s", auth_url)
    return redirect(auth_url)


@app.route('/oauth/callback')
def oauth_callback():
    """
    Complete the OAuth flow: verify state, exchange code for a token
    using the stored PKCE verifier, store access_token in session,
    clean PKCE/state, then send the user back to the original page
    (or a safe homepage fallback).
    """
    has_session_cookie = app.config['SESSION_COOKIE_NAME'] in request.cookies
    log.info("CALLBACK session_cookie_present=%s", has_session_cookie)

    ensure_base_urls_in_session()

    redirect_name = (session.get('redirect_name') or '').strip('/')
    redirect_uri = f"/{redirect_name}/oauth/callback" if redirect_name else "/oauth/callback"

    server_int = session.get('server_int')
    token_url = f"{server_int}/{redirect_name}/services/oauth/token" if redirect_name else f"{server_int}/services/oauth/token"
    # Basic state check
    if request.args.get('state') != session.get('oauth_state'):
        return redirect(url_for('disconnect'))

    # Exchange code for token
    data = {
        'grant_type': 'authorization_code',
        'code': request.args.get('code', ''),
        'redirect_uri': redirect_uri,
        'client_id': 'labbook-FE',
        'client_secret': app.config.get('OAUTH_CLIENT_SECRET'),
        'code_verifier': session.get('oauth_pkce_verifier'),
    }

    log.debug(Logs.fileline() + " : DEBUG OAUTH_CB token_url=" + str(token_url))
    log.debug(Logs.fileline() + " : DEBUG OAUTH_CB redirect_uri=" + str(redirect_uri))

    try:
        req = requests.post(token_url, data=data, timeout=5)
        log.info(Logs.fileline() + " : DEBUG OAUTH_CB token_post_done status=" + str(req.status_code))
    except requests.RequestException:
        log.exception(Logs.fileline() + " : OAUTH token POST raised exception")
        req = type('R', (), {'status_code': 500, 'json': lambda: {}})()

    if req.status_code != 200:
        # Reset PKCE/state on failure and disconnect
        session.pop('oauth_pkce_verifier', None)
        session.pop('oauth_state', None)
        log.debug(Logs.fileline() + " : DEBUG OAUTH_CB state_mismatch")
        return redirect(url_for('disconnect'))

    # Persist access token for BE calls
    tok = req.json()
    session.permanent = True
    session['be_access_token'] = tok.get('access_token')
    session.modified = True
    session.pop('oauth_pkce_verifier', None)
    session.pop('oauth_state', None)

    # Return user to originally requested page
    next_url = session.pop('next', None)
    return redirect(next_url or f"{session.get('server_ext','').rstrip('/')}/{session.get('current_page','homepage')}")

# --- ENDS OAUTH ROUTES ---


@app.route("/")
def index():
    if 'login_ok' not in session:
        check_init_version()
        return render_template('login.html', rand=secrets.randbelow(1000))
    elif 'current_page' not in session:
        log.info(Logs.fileline() + ' : TRACE Labbook_FE get_init_var()')

        resp = get_init_var()
        if isinstance(resp, Response):
            return resp

        check_init_version()
        if session and 'labbook_BE_OK' in session and session['labbook_BE_OK']:
            session['lang_chosen'] = False
            session.modified = True
            log.info(Logs.fileline() + ' : TRACE Labbook_FE no current_page => Login')
            return render_template('login.html', rand=secrets.randbelow(1000))
        else:
            log.info(Logs.fileline() + ' : TRACE Labbook_FE no current_page AND labbook_BE not OK or problem with session')
            return render_template('initialization.html', rand=secrets.randbelow(1000))
    else:
        log.info(Logs.fileline() + ' : TRACE Labbook FRONT END current_page=' + str(session['current_page']))
        if 'redirect_name' not in session or not session['redirect_name']:
            session['lang_chosen'] = False
            session.modified = True
            get_init_var()

        return redirect(session['server_ext'] + '/' + session['current_page'])


# Page : labbook_BE not ready
@app.route('/initialization')
def initialization():
    log.info(Logs.fileline() + ' : TRACE initialization')

    return render_template('initialization.html', rand=secrets.randbelow(1000))


# Page :
@app.route('/api')
def api():
    log.info(Logs.fileline() + ' : TRACE api')
    get_init_var()

    if 'LABBOOK_DEBUG' in os.environ and os.environ['LABBOOK_DEBUG'] == '1':
        debug = 1
    else:
        debug = 0

    log.info(Logs.fileline() + ' : TRACE api LABBOOK_DEBUG=' + str(debug))
    return render_template('api.html', debug=debug, rand=secrets.randbelow(1000))


# switch language
@app.route('/lang/<string:lang>')
def lang(lang='fr_FR'):
    session['lang'] = lang
    session['lang_select'] = LANG_SELECT.get(lang, 'FR')

    if lang in EU_FORMAT_LANGS:
        session['date_format'] = Constants.cst_date_eu
        session['dt_format'] = Constants.cst_dt_eu_HM
    else:
        session['date_format'] = Constants.cst_date_us
        session['dt_format'] = Constants.cst_dt_us_HM

    session['lang_chosen'] = True
    session.modified = True

    return redirect(session['server_ext'] + '/' + session.get('current_page', 'homepage'))


@app.route('/disconnect')
def disconnect():
    log.info(Logs.fileline() + ' : TRACE Labbook FRONT END disconnect')
    session.clear()
    ensure_base_urls_in_session()
    return index()


# Page : homepage
@app.route('/homepage')
@app.route('/homepage/<string:login>')
def homepage(login=''):
    log.info(Logs.fileline() + ' : TRACE Homepage login=' + str(login))

    session['current_page'] = 'homepage'
    session.modified = True

    dt_start_req = datetime.now()

    # Ensure token before any BE call in this route
    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    json_data = {}
    json_data['nb_emer'] = 0

    if login:
        session['login'] = login
        session.modified = True
    elif 'login' in session and session['login']:
        login = session['login']

    # if 'server_ext' not in session or not session['server_ext']:
    resp = get_init_var()
    if isinstance(resp, Response):
        return resp

    resp = get_user_data(login, headers)
    if isinstance(resp, Response):
        return resp

    resp = get_software_settings(headers)
    if isinstance(resp, Response):
        return resp

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook homepage => disconnect')
        session.clear()
        return index()

    if 'user_locale' in session and ('lang_chosen' not in session or not session['lang_chosen']):
        if session['user_locale'] == 34:
            session['lang']  = 'en_GB'
            session.modified = True
        elif session['user_locale'] == 35:
            session['lang']  = 'fr_FR'
            session.modified = True
        elif session['user_locale'] == 75:
            session['lang']  = 'en_US'
            session.modified = True
        elif session['user_locale'] == 724:
            session['lang']  = 'es'
        elif session['user_locale'] == 118:
            session['lang']  = 'ar'
            session.modified = True
        elif session['user_locale'] == 1113:
            session['lang']  = 'km'
            session.modified = True
        elif session['user_locale'] == 1215:
            session['lang']  = 'lo'
            session.modified = True
        elif session['user_locale'] == 137:
            session['lang']  = 'mg'
            session.modified = True
        elif session['user_locale'] == 1620:
            session['lang']  = 'pt'
            session.modified = True
        else:
            session['lang']  = 'fr_FR'
            session.modified = True

    # read backup
    try:
        ret = ''

        path = os.path.join(Constants.cst_io, 'backup')

        if os.path.exists(path) and os.stat(path).st_size > 0:
            with open(path, 'r') as f:
                for line in f:
                    pass

            ret = line[:-1]

            if ret:
                ret = ret.split(';')
                json_data['stat_backup'] = ret[0]
                json_data['date_backup'] = ret[1]
    except Exception:
        log.exception(Logs.fileline() + ' : cant read ' + path)

    # difference between now and last_backup_ok
    try:
        import pathlib

        f = pathlib.Path(Constants.cst_io + 'last_backup_ok')

        if f.exists():
            last_mod_time = datetime.fromtimestamp(f.stat().st_mtime)
            current_time = datetime.now()
            time_difference = current_time - last_mod_time

            json_data['last_backup_ok'] = {
                'date_backup_ok': last_mod_time.strftime('%Y-%m-%d %H:%M:%S'),
                'is_older_than_24h': time_difference > timedelta(hours=24)
            }
        else:
            json_data['last_backup_ok'] = {
                'date_backup_ok': 'undefined',
                'is_older_than_24h': False
            }
    except Exception:
        log.exception(Logs.fileline() + ' : cant read ' + Constants.cst_io + 'last_backup_ok ')

    # Load pref_quality
    try:
        url = session['server_int'] + '/' + session['redirect_name'] + '/services/default/val/qualite'
        req = requests.get(url, timeout=10, headers=headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            ret = req.json()
            if ret and 'value' in ret:
                session['pref_quality'] = int(ret['value'])
                session.modified = True
            else:
                session['pref_quality'] = 0
                session.modified = True

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests pref_quality failed, url=%s', url)

    # Load pref_bill
    try:
        url = session['server_int'] + '/' + session['redirect_name'] + '/services/default/val/facturation'
        req = requests.get(url, timeout=10, headers=headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            ret = req.json()
            if ret and 'value' in ret:
                session['pref_bill'] = ret['value']
                session.modified = True
            else:
                session['pref_bill'] = 0
                session.modified = True

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests pref_bill failed, url=%s', url)

    if 'user_role' not in session:
        log.info(Logs.fileline() + ' : TRACE Labbook_FE homepage no user_role in session => Login')
        return render_template('login.html', rand=secrets.randbelow(1000))
    # API access
    elif session['user_role'] == 'API':
        session['current_page'] = 'api'
        session.modified = True

        return redirect(session['server_ext'] + '/' + session['current_page'])
    # Prescriber homepage
    elif session['user_role'] == 'P':
        session['current_page'] = 'list-records'
        session.modified = True

        return redirect(session['server_ext'] + '/' + session['current_page'])
    # Qualitican or Laboratory homepage
    elif session['user_role'] in ('Q', 'L'):
        session['current_page'] = 'quality-general'
        session.modified = True

        return redirect(session['server_ext'] + '/' + session['current_page'])
    # Sampler homepage
    elif session['user_role'] == 'SP':
        session['current_page'] = 'list-samples'
        session.modified = True

        return redirect(session['server_ext'] + '/' + session['current_page'])

    # Stock manager homepage
    elif session['user_role'] == 'K':
        session['current_page'] = 'list-stock'
        session.modified = True

        return redirect(session['server_ext'] + '/' + session['current_page'])
    else:
        # Load nb_emer
        try:
            payload = {'link_fam': session['user_link_fam']}

            url = session['server_int'] + '/' + session['redirect_name'] + '/services/record/count/emergency'
            req = requests.post(url, timeout=10, json=payload, headers=headers)

            redir = be_check_or_bounce(req)
            if redir:
                return redir

            if req.status_code == 200:
                json_data['nb_emer'] = req.json()

        except requests.exceptions.RequestException:
            log.exception(Logs.fileline() + ' : requests count ermergency failed, url=%s', url)

        # Load nb_rec_tech
        data, redir = be_get('/services/record/count/technician', 'count technician records')
        if redir:
            return redir
        if data is not None:
            json_data['nb_rec_tech'] = data

        # Load nb_rec_bio
        data, redir = be_get('/services/record/count/biologist', 'count biologist records')
        if redir:
            return redir
        if data is not None:
            json_data['nb_rec_bio'] = data

        # Load nb_rec
        try:
            url = session['server_int'] + '/' + session['redirect_name'] + '/services/record/count'
            req = requests.get(url, timeout=10, headers=headers)

            redir = be_check_or_bounce(req)
            if redir:
                return redir

            if req.status_code == 200:
                json_data['nb_rec'] = req.json()
            else:
                log.warning(Logs.fileline() + f' : unexpected status {req.status_code} for URL {url}')

        except requests.exceptions.RequestException:
            log.exception(Logs.fileline() + ' : requests count records failed, url=%s', url)

        # Load nb_rec_today
        data, redir = be_get('/services/record/count/today', 'count today validated records')
        if redir:
            return redir
        if data is not None:
            json_data['nb_rec_today'] = data

        # Load last_record
        data, redir = be_get('/services/record/last', 'last records')
        if redir:
            return redir
        if data is not None:
            json_data['record'] = data

        # Load list of stock for display alert
        try:
            url = session['server_int'] + '/' + session['redirect_name'] + '/services/quality/stock/list'
            req = requests.post(url, timeout=10, json={}, headers=headers)

            redir = be_check_or_bounce(req)
            if redir:
                return redir

            if req.status_code == 200:
                json_data['stock'] = req.json()

        except requests.exceptions.RequestException:
            log.exception(Logs.fileline() + ' : requests stock list failed, url=%s', url)

        dt_stop_req = datetime.now()
        dt_time_req = dt_stop_req - dt_start_req

        log.info(Logs.fileline() + ' : TRACE homepage processing time = ' + str(dt_time_req))

        return render_template('homepage.html', args=json_data, rand=secrets.randbelow(1000))


# --------------------
# --- Setting page ---
# --------------------

# Page : users list
@app.route('/setting-roles-and-rights')
def setting_roles_and_rights():
    log.info(Logs.fileline() + ' : TRACE setting roles-and-rights')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook setting roles-and-rights => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'setting-roles-and-rights'
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    json_ihm  = {}
    json_data = {}

    # Load list roles
    try:
        url = session['server_int'] + '/' + session['redirect_name'] + '/services/user/role/list'
        req = requests.post(url, timeout=10, json={}, headers=headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            json_data = req.json()

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests role list failed, url=%s', url)

    log.info(Logs.fileline() + ' : TRACE Labbook setting roles-and-rights json_data = ' + str(json_data))

    return render_template('setting-roles-and-rights.html', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# Page : role details
@app.route('/setting-det-role/<int:role_id>')
def setting_det_role(role_id=0):
    log.info(Logs.fileline() + ' : TRACE setting det role=' + str(role_id))

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook setting det role => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'setting-det-role/' + str(role_id)
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    json_ihm  = {}
    json_data = {}

    # Load list of user role
    try:
        payload = {'exclude': ["API", "TA", "TQ", "SA", "Z"], 'genuine': 'Y'}

        url = session['server_int'] + '/' + session['redirect_name'] + '/services/user/role/list'
        req = requests.post(url, timeout=10, json=payload, headers=headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            json_ihm['user_role'] = req.json()

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests user role list failed, url=%s', url)

    if role_id > 0:
        # Load user details
        try:
            url = session['server_int'] + '/' + session['redirect_name'] + '/services/user/role/det/' + str(role_id)
            req = requests.get(url, timeout=10, headers=headers)

            if req.status_code == 200:
                json_data = req.json()

        except requests.exceptions.RequestException:
            log.exception(Logs.fileline() + ' : requests user role det failed, url=%s', url)

    json_data['by_user'] = session['user_id']
    json_data['user_id'] = 0
    json_data['role_id'] = role_id

    return render_template('setting-det-role.html', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# table of rights
@app.route('/setting-det-role/table-rights')
def role_table_rights():
    log.info(Logs.fileline() + ' : TRACE /setting-det-role/table-rights')
    role_type = request.args.get('role_type', default='', type=str)
    role_id   = request.args.get('role_id', default=0, type=int)

    l_rights = {}

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    payload = {'id_user': 0,
               'role_type': role_type,
               'role_id': role_id}

    # log.info(Logs.fileline() + ' : DEBUG payload = ' + str(payload))

    try:
        url = session['server_int'] + '/' + session['redirect_name'] + '/services/user/rights/list'
        req = requests.post(url, timeout=10, json=payload, headers=headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            l_rights = req.json()

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests user list rights failed, url=%s', url)

    # log.info(Logs.fileline() + ' : DEBUG l_rights = ' + str(l_rights))

    return render_template('table-rights.html', l_rights=l_rights)


# Page : user rights
@app.route('/setting-user-rights/<int:id_user>')
def setting_user_rights(id_user=0):
    log.info(Logs.fileline() + ' : TRACE setting user rights user=' + str(id_user))

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook setting user rights => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'setting-user-rights/' + str(id_user)
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    json_ihm  = {}
    json_data = {}

    # Load list of user role
    try:
        payload = {'exclude': ["API", "Z"], 'genuine': 'N'}

        url = session['server_int'] + '/' + session['redirect_name'] + '/services/user/role/list'
        req = requests.post(url, timeout=10, json=payload, headers=headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            json_ihm['user_role'] = req.json()

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests user role list failed, url=%s', url)

    if id_user > 0:
        # Load role for this user
        try:
            url = session['server_int'] + '/' + session['redirect_name'] + '/services/user/role/user/' + str(id_user)
            req = requests.get(url, timeout=10, headers=headers)

            if req.status_code == 200:
                json_data = req.json()

        except requests.exceptions.RequestException:
            log.exception(Logs.fileline() + ' : requests user role det failed, url=%s', url)

    json_data['by_user'] = session['user_id']
    json_data['id_user'] = id_user

    return render_template('setting-user-rights.html', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# table of rights
@app.route('/setting-user-rights/table-rights')
def user_table_rights():
    log.info(Logs.fileline() + ' : TRACE /setting-user-rights/table-rights')
    id_user  = request.args.get('id_user', default=0, type=int)

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    l_rights = {}

    payload = {'id_user': id_user,
               'role_type': '',
               'role_id': 0}

    # log.info(Logs.fileline() + ' : DEBUG payload = ' + str(payload))

    try:
        url = session['server_int'] + '/' + session['redirect_name'] + '/services/user/rights/list'
        req = requests.post(url, timeout=10, json=payload, headers=headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            l_rights = req.json()

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests user list rights failed, url=%s', url)

    # log.info(Logs.fileline() + ' : DEBUG l_rights = ' + str(l_rights))

    return render_template('table-rights.html', l_rights=l_rights)


# Page : users list
@app.route('/setting-users')
def setting_users():
    log.info(Logs.fileline() + ' : TRACE setting users')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook setting users => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'setting-users'
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    json_ihm  = {}
    json_data = {}

    # Load list of user role
    try:
        url = session['server_int'] + '/' + session['redirect_name'] + '/services/user/role/list'
        req = requests.post(url, timeout=10, json={}, headers=headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            json_ihm['user_role'] = req.json()

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests user role list failed, url=%s', url)

    # Load list users
    try:
        url = session['server_int'] + '/' + session['redirect_name'] + '/services/user/list'
        req = requests.post(url, timeout=10, json={}, headers=headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            json_data = req.json()

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests user list failed, url=%s', url)

    return render_template('setting-users.html', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# Page : details user
@app.route('/setting-det-user/<int:user_id>')
@app.route('/setting-det-user/<string:ctx>/<int:user_id>')
@app.route('/setting-det-user/<string:ctx>/<int:user_id>/<string:role_type>')
def setting_det_user(user_id=0, ctx='', role_type=''):
    log.info(Logs.fileline() + ' : TRACE setting det user=' + str(user_id))

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook setting det user => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'setting-det-user/' + str(user_id)
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    json_ihm  = {}
    json_data = {}

    # the return page after saving
    if ctx:
        json_ihm['return_page'] = ctx

    # specific role_type, only for add staff
    if role_type:
        # Load list of one user role type
        try:
            url = session['server_int'] + '/' + session['redirect_name'] + '/services/user/role/list/Z'
            req = requests.post(url, timeout=10, json={}, headers=headers)

            redir = be_check_or_bounce(req)
            if redir:
                return redir

            if req.status_code == 200:
                json_ihm['user_role']  = req.json()
                json_data['role_type'] = 'Z'

        except requests.exceptions.RequestException:
            log.exception(Logs.fileline() + ' : requests user role list failed, url=%s', url)
    else:
        # Load list of user role
        try:
            payload = {'exclude': ["Z"]}

            url = session['server_int'] + '/' + session['redirect_name'] + '/services/user/role/list'
            req = requests.post(url, timeout=10, json=payload, headers=headers)

            redir = be_check_or_bounce(req)
            if redir:
                return redir

            if req.status_code == 200:
                json_ihm['user_role'] = req.json()

        except requests.exceptions.RequestException:
            log.exception(Logs.fileline() + ' : requests user role list failed, url=%s', url)

    # Load civility
    data, redir = be_get('/services/dict/det/titre_civilite', 'civility list')
    if redir:
        return redir
    if data is not None:
        json_ihm['civility'] = data

    # Load sections
    data, redir = be_get('/services/dict/det/sections', 'sections')
    if redir:
        return redir
    if data is not None:
        json_ihm['sections'] = data

    if user_id > 0:
        # Load user details
        data, redir = be_get('/services/user/det/' + str(user_id), 'user det')
        if redir:
            return redir
        if data is not None:
            json_data = data

    json_data['user_id'] = user_id

    return render_template('setting-det-user.html', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# Page : users connection export
@app.route('/user-conn-export')
def user_conn_export():
    log.info(Logs.fileline() + ' : TRACE user-conn-export')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook user-conn-export => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'user-conn-export'
    session.modified = True

    return render_template('user-conn-export.html', rand=secrets.randbelow(1000))


# Page : users import
@app.route('/user-import')
def user_import():
    log.info(Logs.fileline() + ' : TRACE user-import')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook user-import => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'user-import'
    session.modified = True

    return render_template('user-import.html', rand=secrets.randbelow(1000))


# Page : setting new password for a user
@app.route('/setting-pwd-user/<int:user_id>')
@app.route('/setting-pwd-user/<string:ctx>/<int:user_id>')
def setting_pwd_user(user_id=0, ctx=''):
    log.info(Logs.fileline() + ' : TRACE setting pwd user')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook pwd user => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'setting-pwd-user/' + str(user_id)
    session.modified = True

    json_ihm  = {}
    json_data = {}

    # the return page after saving
    if ctx:
        json_ihm['return_page'] = ctx

    json_data['user_id'] = user_id

    return render_template('setting-pwd-user.html', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# Page : import dict
@app.route('/dict-import')
def dict_import():
    log.info(Logs.fileline() + ' : TRACE dict import')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook dict import => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'dict-import'
    session.modified = True

    json_ihm  = {}
    json_data = {}

    return render_template('dict-import.html', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# Page : dict list
@app.route('/setting-dicts')
def setting_dicts():
    log.info(Logs.fileline() + ' : TRACE setting dict')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook setting dict => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'setting-dicts'
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    json_data = {}

    # Load list dict
    try:
        url = session['server_int'] + '/' + session['redirect_name'] + '/services/dict/list'
        req = requests.post(url, timeout=10, json={}, headers=headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            json_data = req.json()

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests dicts list failed, url=%s', url)

    return render_template('setting-dicts.html', args=json_data, rand=secrets.randbelow(1000))


# Page : details dictionnary
@app.route('/setting-det-dict')
@app.route('/setting-det-dict/<string:dict_name>')
@app.route('/setting-det-dict/<int:id_dict>')
def setting_det_dict(dict_name='', id_dict=0):
    log.info(Logs.fileline() + ' : TRACE setting det dict=' + str(dict_name) + ', id_dict=' + str(id_dict))

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook det dict => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'setting-det-dict/' + str(dict_name)

    if not dict_name and id_dict > 0:
        session['current_page'] = 'setting-det-dict/' + str(id_dict)

    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    json_ihm  = {}
    json_data = {}

    if dict_name:
        # Load dict details
        try:
            url = session['server_int'] + '/' + session['redirect_name'] + '/services/dict/det/' + str(dict_name)
            req = requests.get(url, timeout=10, headers=headers)

            redir = be_check_or_bounce(req)
            if redir:
                return redir

            if req.status_code == 200:
                json_data['data_values'] = req.json()

                i = 0
                for val in json_data['data_values']:
                    val['id_ihm'] = i
                    i += 1

                json_data['data_last_id'] = i

        except requests.exceptions.RequestException:
            log.exception(Logs.fileline() + ' : requests dict det failed, url=%s', url)
    elif id_dict > 0:
        # Load dict details
        try:
            url = session['server_int'] + '/' + session['redirect_name'] + '/services/dict/det/id/' + str(id_dict)
            req = requests.get(url, timeout=10, headers=headers)

            redir = be_check_or_bounce(req)
            if redir:
                return redir

            if req.status_code == 200:
                json_data['data_values'] = req.json()

                i = 0
                for val in json_data['data_values']:
                    dict_name = val['dico_name']
                    val['id_ihm'] = i
                    i += 1

                json_data['data_last_id'] = i

                json_ihm['readonly'] = 'Y'

        except requests.exceptions.RequestException:
            log.exception(Logs.fileline() + ' : requests dict det by id failed, url=%s', url)
    else:
        json_data['data_values'] = []

    json_data['dict_name'] = str(dict_name)

    return render_template('setting-det-dict.html', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# Page : analyzes list
@app.route('/setting-analyzes')
def setting_analyzes():
    log.info(Logs.fileline() + ' : TRACE setting analyzes')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook setting analyzes => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'setting-analyzes'
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    json_ihm  = {}
    json_data = {}

    # Load analysis type
    data, redir = be_get('/services/dict/det/famille_analyse', 'analysis type')
    if redir:
        return redir
    if data is not None:
        json_ihm['type_ana'] = data

    # Load products
    data, redir = be_get('/services/dict/det/type_prel', 'products list')
    if redir:
        return redir
    if data is not None:
        json_ihm['products'] = data

    # Load list analyzes
    try:
        url = session['server_int'] + '/' + session['redirect_name'] + '/services/analysis/list'
        req = requests.post(url, timeout=10, json={}, headers=headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            json_data = req.json()

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests analyzes list failed, url=%s', url)

    return render_template('setting-analyzes.html', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# Page : analyzers list
@app.route('/list-analyzers')
def list_analyzers():
    log.info(Logs.fileline() + ' : TRACE setting analyzers')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook setting analyzers => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'setting-analyzers'
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp

    json_ihm  = {}
    json_data = {}

    data, redir = be_get('/services/device/analyzer/list', 'analyzers list')
    if redir:
        return redir
    if data is not None:
        json_data = data

    return render_template('list-analyzers.html', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# Page : details analyzer
@app.route('/det-analyzer/<int:id_analyzer>')
def det_analyzer(id_analyzer=0):
    log.info(Logs.fileline() + ' : TRACE setting det analyzer=' + str(id_analyzer))

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook det analyzer => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'det-analyzer/' + str(id_analyzer)
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp

    json_ihm  = {}
    json_data = {}

    json_data['analyzer'] = []

    # Load Connect setting
    data, redir = be_get('/services/connect/setting', 'get connect setting')
    if redir:
        return redir
    if data is not None:
        json_data['connect'] = data

    # Load list of analyzers
    data, redir = be_get('/services/device/analyzer/file', 'list of analyzers files')
    if redir:
        return redir
    if data is not None:
        json_ihm['analyzers'] = data

    if id_analyzer > 0:
        # Load analyzer details
        data, redir = be_get('/services/device/analyzer/det/' + str(id_analyzer), 'analyzer det')
        if redir:
            return redir
        if data is not None:
            json_data['analyzer'] = data

    json_data['id_analyzer'] = id_analyzer

    return render_template('det-analyzer.html', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# Page : list msg analyzer
@app.route('/list-msg-analyzer')
def list_msg_analyzer():
    log.info(Logs.fileline() + ' : TRACE list msg analyzer')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook list msg analyzer => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'list-msg-analyzer'
    session.modified = True

    json_ihm  = {}
    json_data = {}

    return render_template('list-msg-analyzer.html', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# Page : Connect management
@app.route('/connect-management')
def connect_management():
    log.info(Logs.fileline() + ' : TRACE connect management')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook connect-management => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'connect-management'
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    json_ihm  = {}
    json_data = {}

    # Load Connect setting
    try:
        url = session['server_int'] + '/' + session['redirect_name'] + '/services/connect/setting'
        req = requests.get(url, timeout=10, headers=headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            json_data = req.json()
        else:
            log.warning(Logs.fileline() + ' : connect setting HTTP error %s', req.status_code)

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests get connect setting failed, url=%s', url)

    cos_url = json_data.get('cos_url')

    # Load Connect version
    if cos_url:
        try:
            url = json_data['cos_url'] + '/connect/test'
            req = requests.get(url, timeout=5)
            json_data['version'] = req.text

        except requests.exceptions.RequestException:
            log.exception(Logs.fileline() + ' : requests get version connect failed, url=%s', url)
    else:
        json_data['version'] = ''

    # Load Connect analyzers loaded
    if cos_url:
        try:
            url = json_data['cos_url'] + '/connect/list_analyzers_loaded'
            req = requests.get(url, timeout=5)
            json_data['analyzers_loaded'] = req.text.replace("\n", ",").rstrip(",")

        except requests.exceptions.RequestException:
            log.exception(Logs.fileline() + ' : requests get analyzers loaded in Connect failed, url=%s', url)
    else:
        json_data['analyzers_loaded'] = ''

    return render_template('connect-management.html', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# Page : variables list
@app.route('/list-vars')
def list_vars():
    log.info(Logs.fileline() + ' : TRACE list vars')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook list vars => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'list-vars'
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp

    json_data = {}

    # Load list vars
    data, redir = be_get('/services/analysis/variable/all', 'vars all')
    if redir:
        return redir
    if data is not None:
        json_data = data

    return render_template('list-vars.html', args=json_data, rand=secrets.randbelow(1000))


# Page : import analyzes list
@app.route('/analysis-import')
def analysis_import():
    log.info(Logs.fileline() + ' : TRACE import analysis')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook import analysis => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'analysis-import'
    session.modified = True

    json_ihm  = {}
    json_data = {}

    return render_template('analysis-import.html', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# Page : details analysis
@app.route('/setting-det-analysis/<int:analysis_id>')
def setting_det_analysis(analysis_id=0):
    log.info(Logs.fileline() + ' : TRACE setting det analysis=' + str(analysis_id))

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook det analysis => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'setting-det-analysis/' + str(analysis_id)
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp

    json_ihm  = {}
    json_data = {}

    json_data['details'] = []
    json_data['var'] = []

    # Load analysis type
    data, redir = be_get('/services/dict/det/famille_analyse', 'analysis type')
    if redir:
        return redir
    if data is not None:
        json_ihm['type_ana'] = data

    # Load products
    data, redir = be_get('/services/dict/det/type_prel', 'products list')
    if redir:
        return redir
    if data is not None:
        json_ihm['products'] = data

    # Load type result
    data, redir = be_get('/services/dict/det/type_resultat', 'type result list')
    if redir:
        return redir
    if data is not None:
        json_ihm['type_res'] = data

    # Load unit
    data, redir = be_get('/services/dict/det/unite_valeur', 'unit list')
    if redir:
        return redir
    if data is not None:
        json_ihm['unit'] = data

    if analysis_id > 0:
        # Load analysis details
        data, redir = be_get('/services/analysis/det/' + str(analysis_id), 'analysis det')
        if redir:
            return redir
        if data is not None:
            json_data['details'] = data

        # Load analysis variables list
        data, redir = be_get('/services/analysis/variable/list/' + str(analysis_id), 'analysis var list')
        if redir:
            return redir
        if data is not None:
            json_data['var'] = data

    json_data['analysis_id'] = analysis_id

    return render_template('setting-det-analysis.html', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# Page : manage patient records
@app.route('/manage-pat-records')
def manage_pat_records():
    log.info(Logs.fileline() + ' : TRACE manage patient records')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook patient records => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'manage-pat-records'
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    json_ihm  = {}
    json_data = {}

    # Load nationality
    data, redir = be_get('/services/nationality/list', 'nationality list')
    if redir:
        return redir
    if data is not None:
        json_ihm['pat_nationality'] = data

    # Load unit age
    try:
        url = session['server_int'] + '/' + session['redirect_name'] + '/services/dict/det/periode_unite'
        req = requests.get(url, timeout=10, headers=headers)

        if req.status_code == 200:
            json_ihm['pat_age_unit'] = req.json()

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests unit age failed, url=%s', url)

    # Load blood group
    try:
        url = session['server_int'] + '/' + session['redirect_name'] + '/services/dict/det/groupesang'
        req = requests.get(url, timeout=10, headers=headers)

        if req.status_code == 200:
            json_ihm['pat_blood_group'] = req.json()

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests blood group failed, url=%s', url)

    # Load blood rhesus
    try:
        url = session['server_int'] + '/' + session['redirect_name'] + '/services/dict/det/posneg'
        req = requests.get(url, timeout=10, headers=headers)

        if req.status_code == 200:
            json_ihm['pat_blood_rhesus'] = req.json()

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests blood rhesus failed, url=%s', url)

    # --- Form from file (same as det-patient) ---
    form_filename = 'form_patient_fr.toml'

    if session.get('lang_select') and session['lang_select'] != 'FR':
        form_filename = 'form_patient_' + session['lang_select'].lower() + '.toml'
        dirpath = Constants.cst_form_pat
        path = os.path.join(dirpath, form_filename)
        if not (os.path.isfile(path) and path.endswith('.toml')):
            form_filename = 'form_patient_fr.toml'

    ret_build_form = Form.build_form('PAT', form_filename)

    # Raw outputs from builder
    json_data['form_html'] = ret_build_form['form_html']
    json_data['json_save'] = ret_build_form['json_save']

    # Render embedded Jinja (includes, translations, etc.)
    json_data['form_html'] = render_template_string(
        json_data['form_html'],
        ihm=json_ihm,
        args=json_data
    )

    json_data['json_save'] = render_template_string(json_data['json_save'])

    return render_template('manage-pat-records.html', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# Page : preferences list
@app.route('/setting-pref')
def setting_preferences():
    log.info(Logs.fileline() + ' : TRACE setting preferences')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook setting preferences => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'setting-pref'
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp

    json_data = {}

    data, redir = be_get('/services/setting/pref/list', 'preferences list')
    if redir:
        return redir
    if data is not None:
        json_data['pref_list'] = data

    return render_template('setting-pref.html', args=json_data, rand=secrets.randbelow(1000))


# Page : setting backup and restore
@app.route('/setting-backup')
def setting_backup():
    log.info(Logs.fileline() + ' : TRACE setting backup')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook setting backup => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'setting-backup'
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp

    json_data = {}
    json_data['stat_backup'] = ''
    json_data['date_backup'] = ''
    json_data['last_backup'] = ''
    json_data['bks_data']    = []

    # read backup
    try:
        ret = ''

        path = os.path.join(Constants.cst_io, 'backup')

        if os.path.exists(path) and os.stat(path).st_size > 0:
            f = open(path, 'r')
            for line in f:
                pass

            ret = line[:-1]

            if ret:
                ret = ret.split(';')
                json_data['stat_backup'] = ret[0]
                json_data['date_backup'] = ret[1]
    except Exception:
        log.exception(Logs.fileline() + ' : cant read ' + path)

    # get modification time from last_backup_ok
    try:
        import pathlib

        f = pathlib.Path(Constants.cst_io + 'last_backup_ok')

        if f.exists():
            json_data['last_backup_ok'] = str(datetime.fromtimestamp(f.stat().st_mtime))
            json_data['last_backup_ok'] = json_data['last_backup_ok'][:19]
    except Exception:
        log.exception(Logs.fileline() + ' : cant read ' + Constants.cst_io + 'last_backup_ok ')

    # load start_time
    data, redir = be_get('/services/setting/backup', 'preferences list')
    if redir:
        return redir
    if data is not None:
        json_data['bks_data'] = data

    return render_template('setting-backup.html', args=json_data, rand=secrets.randbelow(1000))


# Page : zip code and city list
@app.route('/setting-zipcity')
def setting_zipcity():
    log.info(Logs.fileline() + ' : TRACE setting zipcity')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook setting zipcity => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'setting-zipcity'
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    json_data = {}

    try:
        payload = {}

        url = session['server_int'] + '/' + session['redirect_name'] + '/services/setting/zipcity/list'
        req = requests.post(url, timeout=10, json=payload, headers=headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            json_data = req.json()

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests zipcity list failed, url=%s', url)

    return render_template('setting-zipcity.html', args=json_data, rand=secrets.randbelow(1000))


# Page : setting stock
@app.route('/setting-stock')
def setting_stock():
    log.info(Logs.fileline() + ' : TRACE setting stock')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook setting stock => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'setting-stock'
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    json_data = {}

    # Load stock setting
    data, redir = be_get('/services/setting/stock', 'stock setting')
    if redir:
        return redir
    if data is not None:
        json_data = data

    # Load local list
    try:
        url = session['server_int'] + '/' + session['redirect_name'] + '/services/quality/stock/local/list'
        req = requests.get(url, timeout=10, headers=headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            json_data['data_values'] = req.json()

            i = 0
            for val in json_data['data_values']:
                val['id_ihm'] = i
                i += 1

            json_data['data_last_id'] = i

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests stock local list failed, url=%s', url)

    return render_template('setting-stock.html', args=json_data, rand=secrets.randbelow(1000))


# Page : setting form
@app.route('/setting-form')
def setting_form():
    log.info(Logs.fileline() + ' : TRACE setting form')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook setting form => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'setting-form'
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp

    json_data = {}

    json_data['data_form_pat'] = []
    json_data['data_form_pat_hist'] = []

    # Load form patient files
    try:
        path = Constants.cst_form_pat

        filenames = sorted(os.listdir(path))

        for filename in filenames:
            full_path = os.path.join(path, filename)

            # skip directories
            if os.path.isdir(full_path):
                continue

            # only TOML files
            if not filename.endswith('.toml'):
                continue

            # history forms
            if filename.startswith('form_patient_hist_'):
                json_data['data_form_pat_hist'].append(filename)
            # main patient forms (avoid mixing with history)
            elif filename.startswith('form_patient_'):
                json_data['data_form_pat'].append(filename)

    except Exception:
        log.exception(Logs.fileline() + ' : load patient form files failed')

    # Load form setting
    data, redir = be_get('/services/setting/form/list', 'form setting')
    if redir:
        return redir
    if data is not None:
        json_data['l_fos'] = data

    return render_template('setting-form.html', args=json_data, rand=secrets.randbelow(1000))


# Page : form preview
@app.route('/preview-form/<string:type_form>/<string:filename>')
def preview_form(type_form='', filename=''):
    log.info(Logs.fileline() + ' : TRACE preview_form')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook preview form => disconnect')
        session.clear()
        return index()

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    json_ihm  = {}
    json_data = {}

    # ------------------------------------------------------------------
    # case: patient history form (PAT-HIST)
    # ------------------------------------------------------------------
    if type_form == 'PAT-HIST':
        try:
            import tomli

            # Validate and sanitize filename
            safe_name = secure_filename(filename or '')
            if not safe_name:
                log.error(Logs.fileline() + ' : preview-form PAT-HIST invalid filename (empty after sanitize)')
                form_toml = {}
            else:
                base_dir = os.path.abspath(Constants.cst_form_pat)
                path = os.path.abspath(os.path.join(base_dir, safe_name))

                # Prevent path traversal: path must stay under base_dir
                if not path.startswith(base_dir + os.sep):
                    log.error(Logs.fileline() + ' : preview-form PAT-HIST invalid filename (path traversal)')
                    form_toml = {}
                elif os.path.isfile(path):
                    with open(path, "rb") as f:
                        form_toml = tomli.load(f)
                else:
                    form_toml = {}

            for elem in form_toml.get('description', {}).get('form_element', []):
                # only input elements with an id
                if elem and 'id' in elem and 'input_type' in elem:
                    json_data[elem['id']] = ''
        except Exception:
            log.exception(Logs.fileline() + ' : preview-form PAT-HIST init from toml failed')

        ret_build_form = Form.build_form(type_form, filename)
        json_data['form_html'] = ret_build_form['form_html']

        page_content = ('<!DOCTYPE html>'
                        '<html lang="{{ locale }}" {% if locale == "ar" %}dir="rtl"{% else %}dir="ltr"{% endif %}>'
                        '<head>'
                            '<meta charset="UTF-8">'
                            '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
                            '<title>Preview form</title>'
                            '<link href="{{ url_for("static", filename="vendor/bootstrap/bootstrap-icons/bootstrap-icons.css") }}" rel="stylesheet">'
                            '<link href="{{ url_for("static", filename="vendor/bootstrap/css/bootstrap.min.css") }}" media="screen, print" rel="stylesheet" type="text/css">'
                            '<link href="{{ url_for("labbook_css") }}?{{ rand }}" media="screen" rel="stylesheet" type="text/css">'
                            '<script src="{{ url_for("static", filename="vendor/js/jquery-3.6.1.min.js") }}"></script>'
                            '<link href="{{ url_for("static", filename="vendor/bootstrap/css/bootstrap-datepicker3.min.css") }}" rel="stylesheet" />'
                            '<link href="{{ url_for("static", filename="vendor/css/select2.min.css") }}" rel="stylesheet" />'
                            '<script type="text/javascript" src="{{ url_for("static", filename="vendor/js/select2.min.js") }}" nonce="{{ session["nonce"] }}"></script>'
                        '</head>'
                        '<body>'
                            '<div id="page" class="container-fluid">'
                                '{{ args["form_html"] | safe }}'
                            '</div>'
                        '</body>'
                        '</html>')

        # pre-render the page
        page_content = render_template_string(page_content, ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))

        return render_template_string(page_content, ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))

    # ------------------------------------------------------------------
    # Default case: patient main form (PAT)
    # ------------------------------------------------------------------

    # Load unit age
    data, redir = be_get('/services/dict/det/periode_unite', 'unit age')
    if redir:
        return redir
    if data is not None:
        json_ihm['pat_age_unit'] = data

    # Load blood group
    try:
        url = session['server_int'] + '/' + session['redirect_name'] + '/services/dict/det/groupesang'
        req = requests.get(url, timeout=10, headers=headers)

        if req.status_code == 200:
            json_ihm['pat_blood_group'] = req.json()

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests blood group failed, url=%s', url)

    # Load blood rhesus
    try:
        url = session['server_int'] + '/' + session['redirect_name'] + '/services/dict/det/posneg'
        req = requests.get(url, timeout=10, headers=headers)

        if req.status_code == 200:
            json_ihm['pat_blood_rhesus'] = req.json()

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests blood rhesus failed, url=%s', url)

    # Load nationality
    try:
        url = session['server_int'] + '/' + session['redirect_name'] + '/services/nationality/list'
        req = requests.get(url, timeout=10, headers=headers)

        if req.status_code == 200:
            json_ihm['pat_nationality'] = req.json()

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests nationality list failed, url=%s', url)

    # Load unit age by default
    try:
        url = session['server_int'] + '/' + session['redirect_name'] + '/services/default/val/unite_age_defaut'
        req = requests.get(url, timeout=10, headers=headers)

        if req.status_code == 200:
            unit_age_def = req.json()
            json_ihm['unit_age_def'] = 0

            val_age_def = unit_age_def['value'].lower()

            # unit_age['code'] without accent so we need to remove it from val_age_def to compare
            if val_age_def == 'années':
                val_age_def = 'annees'

            for unit_age in json_ihm['pat_age_unit']:
                if unit_age['code'] == val_age_def:
                    json_data['def_age_unit'] = unit_age['id_data']

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests unite_age_defaut failed, url=%s', url)

    # generate a code
    try:
        url = session['server_int'] + '/' + session['redirect_name'] + '/services/patient/generate/code'
        req = requests.get(url, timeout=10, headers=headers)

        if req.status_code == 200:
            json_data['pat_code'] = req.json()
            json_data['id_pat'] = 0

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests patient generate code failed, url=%s', url)

    ret_build_form = Form.build_form(type_form, filename)
    json_data['form_html'] = ret_build_form['form_html']

    page_content = ('<!DOCTYPE html>'
                    '<html lang="{{ locale }}" {% if locale == "ar" %}dir="rtl"{% else %}dir="ltr"{% endif %}>'
                    '<head>'
                        '<meta charset="UTF-8">'
                        '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
                        '<title>Preview form</title>'
                        '<link href="{{ url_for("static", filename="vendor/bootstrap/bootstrap-icons/bootstrap-icons.css") }}" rel="stylesheet">'
                        '<link href="{{ url_for("static", filename="vendor/bootstrap/css/bootstrap.min.css") }}" media="screen, print" rel="stylesheet" type="text/css">'
                        '<link href="{{ url_for("labbook_css") }}?{{ rand }}" media="screen" rel="stylesheet" type="text/css">'
                        '<script src="{{ url_for("static", filename="vendor/js/jquery-3.6.1.min.js") }}"></script>'
                        '<link href="{{ url_for("static", filename="vendor/bootstrap/css/bootstrap-datepicker3.min.css") }}" rel="stylesheet" />'
                        '<link href="{{ url_for("static", filename="vendor/css/select2.min.css") }}" rel="stylesheet" />'
                        '<script type="text/javascript" src="{{ url_for("static", filename="vendor/js/select2.min.js") }}" nonce="{{ session["nonce"] }}"></script>'
                    '</head>'
                    '<body>'
                        '<div id="page" class="container-fluid">'
                            '{{ args["form_html"] | safe }}'
                        '</div>'
                    '</body>'
                    '</html>')

    # pre-render the page
    page_content = render_template_string(page_content, ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))

    return render_template_string(page_content, ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# Page : list template
@app.route('/list-template')
def list_template():
    log.info(Logs.fileline() + ' : TRACE list template')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook list template => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'list-template'
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp

    json_data = {}

    data, redir = be_get('/services/setting/template/list', 'template list')
    if redir:
        return redir
    if data is not None:
        json_data = data

    return render_template('list-template.html', args=json_data, rand=secrets.randbelow(1000))


# Page : template details
@app.route('/det-template/<int:id_tpl>')
def det_template(id_tpl=0):
    log.info(Logs.fileline() + ' : TRACE setting template det=' + str(id_tpl))

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook template det => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'det-template/' + str(id_tpl)
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp

    json_data = {}

    json_data['template'] = []

    if id_tpl > 0:
        # Load template details
        data, redir = be_get('/services/setting/template/det/' + str(id_tpl), 'template det')
        if redir:
            return redir
        if data is not None:
            json_data['template'] = data

    json_data['id_tpl'] = id_tpl

    return render_template('det-template.html', args=json_data, rand=secrets.randbelow(1000))


# Page : setting report
@app.route('/setting-report')
def setting_report():
    log.info(Logs.fileline() + ' : TRACE setting report')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook setting report => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'setting-report'
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp

    json_data = {}

    # Load setting report
    data, redir = be_get('/services/setting/report', 'setting report')
    if redir:
        return redir
    if data is not None:
        json_data = data

    return render_template('setting-report.html', args=json_data, rand=secrets.randbelow(1000))


# Page : setting sending method
@app.route('/setting-sending-method')
def setting_sending_method():
    log.info(Logs.fileline() + ' : TRACE setting sending method')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook setting sending method => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'setting-sending-method'
    session.modified = True

    json_data = {}

    return render_template('setting-sending-method.html', args=json_data, rand=secrets.randbelow(1000))


# Page : details sending method
@app.route('/det-sending-method/<string:type>/<int:id_item>')
def det_sending_method(type='', id_item=0):
    log.info(Logs.fileline() + ' : TRACE details sending method ' + str(id_item))

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook details sending method => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'det-sending-method/' + str(type) + '/' + str(id_item)
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    json_data = {}

    if id_item > 0:
        # Load sending method details
        try:
            allowed_types = {'S': 'S', 'M': 'M', 'W': 'W'}
            validated_type = allowed_types.get(type)

            if not validated_type:
                return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

            url = session['server_int'] + '/' + session['redirect_name'] + '/services/setting/sending/method/det/' + validated_type + '/' + str(id_item)
            req = requests.get(url, timeout=10, headers=headers)

            redir = be_check_or_bounce(req)
            if redir:
                return redir

            if req.status_code == 200:
                json_data['item'] = req.json()

        except requests.exceptions.RequestException:
            log.exception(Logs.fileline() + ' : requests sending method det failed, url=%s', url)
    else:
        json_data['item'] = {}

    json_data['id_item'] = id_item
    json_data['type_item'] = type

    return render_template('det-sending-method.html', args=json_data, rand=secrets.randbelow(1000))


# Page : details sending model
@app.route('/det-sending-model/<string:type>/<int:id_item>')
def det_sending_model(type='', id_item=0):
    log.info(Logs.fileline() + ' : TRACE details sending model ' + str(id_item))

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook details sending model => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'det-sending-model/' + str(type) + '/' + str(id_item)
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    json_data = {}

    if id_item > 0:
        # Load sending model details
        try:
            allowed_types = {'S': 'S', 'M': 'M', 'W': 'W'}
            validated_type = allowed_types.get(type)

            if not validated_type:
                return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

            url = session['server_int'] + '/' + session['redirect_name'] + '/services/setting/sending/model/det/' + validated_type + '/' + str(id_item)
            req = requests.get(url, timeout=10, headers=headers)

            redir = be_check_or_bounce(req)
            if redir:
                return redir

            if req.status_code == 200:
                json_data['item'] = req.json()

        except requests.exceptions.RequestException:
            log.exception(Logs.fileline() + ' : requests sending model det failed, url=%s', url)
    else:
        json_data['item'] = {}

    json_data['id_item'] = id_item
    json_data['type_item'] = type

    return render_template('det-sending-model.html', args=json_data, rand=secrets.randbelow(1000))


# Page : setting record number
@app.route('/setting-rec-num')
def setting_rec_num():
    log.info(Logs.fileline() + ' : TRACE setting record number')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook setting rec num => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'setting-rec-num'
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp

    json_data = {}

    # Load record number setting
    data, redir = be_get('/services/setting/record/number', 'record number setting')
    if redir:
        return redir
    if data is not None:
        json_data = data

    return render_template('setting-rec-num.html', args=json_data, rand=secrets.randbelow(1000))


# Page : logo
@app.route('/setting-logo')
def setting_logo():
    log.info(Logs.fileline() + ' : TRACE setting logo')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook setting logo => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'setting-logo'
    session.modified = True

    return render_template('setting-logo.html', rand=secrets.randbelow(1000))


# Page : age interval setting
@app.route('/setting-age-interval')
def setting_age_interval():
    log.info(Logs.fileline() + ' : TRACE setting age interval')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook setting age interval => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'setting-age-interval'
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    json_data = {}

    # Load interval details
    try:
        url = session['server_int'] + '/' + session['redirect_name'] + '/services/setting/age/interval'
        req = requests.get(url, timeout=10, headers=headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            json_data['data_values'] = req.json()

            i = 0
            for val in json_data['data_values']:
                val['id_ihm'] = i
                i += 1

            json_data['data_last_id'] = i

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests dict det failed, url=%s', url)

    return render_template('setting-age-interval.html', args=json_data, rand=secrets.randbelow(1000))


# Page : requesting services setting
@app.route('/setting-requesting-services')
def setting_requesting_services():
    log.info(Logs.fileline() + ' : TRACE setting requesting services')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook setting requesting services => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'setting-requesting-services'
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    json_data = {}

    # Load requesting services list
    try:
        url = session['server_int'] + '/' + session['redirect_name'] + '/services/setting/requesting/services'
        req = requests.get(url, timeout=10, headers=headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            json_data['data_values'] = req.json()

            i = 0
            for val in json_data['data_values']:
                val['id_ihm'] = i
                i += 1

            json_data['data_last_id'] = i

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests requesting services list failed, url=%s', url)

    return render_template('setting-requesting-services.html', args=json_data, rand=secrets.randbelow(1000))


# Page : functionnal units setting
@app.route('/setting-functionnal-units')
def setting_functionnal_units():
    log.info(Logs.fileline() + ' : TRACE setting functionnal units')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook setting functionnal units => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'setting-functionnal-units'
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    json_data = {}

    # Load functionnal units list
    try:
        url = session['server_int'] + '/' + session['redirect_name'] + '/services/setting/functionnal/unit'
        req = requests.get(url, timeout=10, headers=headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            json_data['data_values'] = req.json()

            # Data never empty because of counts of user and fam
            if not json_data['data_values'][0]['fun_name']:
                json_data['data_values'] = []

            i = 0
            for val in json_data['data_values']:
                val['id_ihm'] = i
                i += 1

            json_data['data_last_id'] = i

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests functionnal units list failed, url=%s', url)

    return render_template('setting-functionnal-units.html', args=json_data, rand=secrets.randbelow(1000))


# Page : manual setting
@app.route('/setting-manual')
def setting_manual():
    log.info(Logs.fileline() + ' : TRACE setting manual')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook setting manual => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'setting-manual'
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    json_data = {}

    # Load requesting services list
    try:
        url = session['server_int'] + '/' + session['redirect_name'] + '/services/setting/manual'
        req = requests.get(url, timeout=10, headers=headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            json_data['data_values'] = req.json()

            i = 0
            for val in json_data['data_values']:
                val['id_ihm'] = i
                i += 1

            json_data['data_last_id'] = i

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests setting manual list failed, url=%s', url)

    return render_template('setting-manual.html', args=json_data, rand=secrets.randbelow(1000))


# Page : setting link unit user
@app.route('/setting-link-unit-user/<int:id_unit>')
def setting_link_unit_user(id_unit):
    log.info(Logs.fileline() + ' : TRACE setting link unit user')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook setting link user => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'setting-link-unit-user'
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    json_data = {}

    json_data['id_func_unit'] = id_unit

    # Load details of functionnal unit
    data, redir = be_get('/services/setting/functionnal/unit/det/' + str(id_unit), 'functionnal unit details')
    if redir:
        return redir
    if data is not None:
        json_data['func_unit'] = data

    # Load list of user with or without link with this unit
    try:
        url = session['server_int'] + '/' + session['redirect_name'] + '/services/setting/link/unit/U/' + str(id_unit)
        req = requests.get(url, timeout=10, headers=headers)

        if req.status_code == 200:
            json_data['data_values'] = req.json()

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests link unit users failed, url=%s', url)

    return render_template('setting-link-unit-user.html', args=json_data, rand=secrets.randbelow(1000))


# Page : setting link unit analysis family
@app.route('/setting-link-unit-fam/<int:id_unit>')
def setting_link_unit_fam(id_unit):
    log.info(Logs.fileline() + ' : TRACE setting link unit fam')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook setting link unit => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'setting-link-unit-fam'
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    json_data = {}

    json_data['id_func_unit'] = id_unit

    # Load details of functionnal unit
    data, redir = be_get('/services/setting/functionnal/unit/det/' + str(id_unit), 'functionnal unit details')
    if redir:
        return redir
    if data is not None:
        json_data['func_unit'] = data

    # Load list of analysis family with or without link with this unit
    try:
        url = session['server_int'] + '/' + session['redirect_name'] + '/services/setting/link/unit/F/' + str(id_unit)
        req = requests.get(url, timeout=10, headers=headers)

        if req.status_code == 200:
            json_data['data_values'] = req.json()

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests link unit family failed, url=%s', url)

    return render_template('setting-link-unit-fam.html', args=json_data, rand=secrets.randbelow(1000))


# Page : setting dhis2
@app.route('/setting-dhis2')
def setting_dhis2():
    log.info(Logs.fileline() + ' : TRACE setting dhis2')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook setting dhis2 => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'setting-dhis2'
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp

    json_data = {}

    json_data['data_dhis2'] = []

    # Load list of dhis2 api
    data, redir = be_get('/services/setting/dhis2/api/list', 'list of dhis2 api')
    if redir:
        return redir
    if data is not None:
        json_data['dhs'] = data

    # Load dhis2 files in dhis2 directory
    try:
        path = Constants.cst_dhis2

        for filename in os.listdir(path):
            if not os.path.isdir(os.path.join(path, filename)) and filename.endswith('.csv'):
                json_data['data_dhis2'].append(filename)

    except Exception:
        log.exception(Logs.fileline() + ' : load dhis2 files in dhis2 directory failed')

    return render_template('setting-dhis2.html', args=json_data, rand=secrets.randbelow(1000))


# Page : dhis2 api details
@app.route('/det-dhis2-api/<int:id_item>')
def det_dhis2_api(id_item=0):
    log.info(Logs.fileline() + ' : TRACE dhis2 api =' + str(id_item))

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook dhis2 api => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'det-dhis2-api/' + str(id_item)
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    json_ihm  = {}
    json_data = {}

    json_data['dhs'] = {}

    # Load dhis2 api details
    try:
        url = session['server_int'] + '/' + session['redirect_name'] + '/services/setting/dhis2/api/det/' + str(id_item)
        req = requests.get(url, timeout=10, headers=headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            json_data['dhs'] = req.json()

            log.error(Logs.fileline() + ' : json_data = ' + str(json_data))

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests dhis2 api det failed, url=%s', url)

    json_data['id_item'] = id_item

    return render_template('det-dhis2-api.html', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# Page : setting epidemio
@app.route('/setting-epidemio')
def setting_epidemio():
    log.info(Logs.fileline() + ' : TRACE setting epidemio')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook setting epidemio => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'setting-epidemio'
    session.modified = True

    json_data = {}

    json_data['data_epidemio'] = []

    # Load epidemio files in epidemio directory
    try:
        path = Constants.cst_epidemio

        for filename in os.listdir(path):
            if not os.path.isdir(os.path.join(path, filename)) and filename == 'epidemio.ini':
                json_data['data_epidemio'].append(filename)

    except Exception:
        log.exception(Logs.fileline() + ' : load epidemio files in epidemio directory failed')

    return render_template('setting-epidemio.html', args=json_data, rand=secrets.randbelow(1000))


# Page : setting indicator
@app.route('/setting-indicator')
def setting_indicator():
    log.info(Logs.fileline() + ' : TRACE setting indicator')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook setting indicator => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'setting-indicator'
    session.modified = True

    json_data = {}

    json_data['data_indicator'] = []

    # Load indicator files in indicator directory
    try:
        path = Constants.cst_indicator

        for filename in os.listdir(path):
            if not os.path.isdir(os.path.join(path, filename)) and filename == 'indicator.ini':
                json_data['data_indicator'].append(filename)

    except Exception:
        log.exception(Logs.fileline() + ' : load indicator files in indicator directory failed')

    return render_template('setting-indicator.html', args=json_data, rand=secrets.randbelow(1000))


# Page : setting-lite
@app.route('/setting-lite')
def setting_lite():
    log.info(Logs.fileline() + ' : TRACE setting-lite')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook setting-lite => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'setting-lite'
    session.modified = True

    json_data = {}

    return render_template('setting-lite.html', args=json_data, rand=secrets.randbelow(1000))


# Page : details setting Lite
@app.route('/det-lite/<int:id_item>')
def det_lite(id_item=0):
    log.info(Logs.fileline() + ' : TRACE setting det lite=' + str(id_item))

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook det lite => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'det-lite/' + str(id_item)
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    json_ihm  = {}
    json_data = {}

    json_ihm['l_users'] = []
    json_data['item'] = []

    # Load list users
    try:
        url = session['server_int'] + '/' + session['redirect_name'] + '/services/user/lite/list'
        req = requests.get(url, json={}, timeout=10, headers=headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            json_ihm['l_users'] = req.json()

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests user list failed, url=%s', url)

    if id_item > 0:
        # Load printer details
        data, redir = be_get('/services/lite/setup/det/' + str(id_item), 'lite setup det')
        if redir:
            return redir
        if data is not None:
            json_data['item'] = data

    json_data['id_item'] = id_item

    return render_template('det-lite.html', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# Page : setting-oauth-list
@app.route('/setting-oauth-list')
def setting_oauth_list():
    log.info(Logs.fileline() + ' : TRACE setting-oauth-list')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook setting-oauth-list => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'setting-oauth-list'
    session.modified = True

    json_data = {}

    return render_template('setting-oauth-list.html', args=json_data, rand=secrets.randbelow(1000))


# Page : details setting OAuth client
@app.route('/det-oauth-client/<int:id_item>')
def det_oauth_client(id_item=0):
    log.info(Logs.fileline() + ' : TRACE setting det oauth client=' + str(id_item))

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook det oauth client => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'det-oauth-client/' + str(id_item)
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp

    json_ihm  = {}
    json_data = {}

    json_data['item'] = []

    if id_item > 0:
        # Load printer details
        data, redir = be_get('/services/setting/oauth/det/' + str(id_item), 'oauth det')
        if redir:
            return redir
        if data is not None:
            json_data['item'] = data
    else:
        # Defaults for creation
        json_data['item'] = {
            'oacl_client_name': '',
            'oacl_client_id': '',
            'oacl_client_secret': '',
            'oacl_redirect_uris': '',
            'oacl_scope': 'external/...',
            'oacl_grant_types': 'client_credentials',
            'oacl_response_types': 'code',
            'oacl_token_endpoint_auth_method': 'client_secret_post',
            'oacl_is_active': 'Y'
        }

    json_data['id_item'] = id_item

    return render_template('det-oauth-client.html', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# ---------------------------
# --- Administrative page ---
# ---------------------------

# Page : list of results to enter
@app.route('/list-results')
def list_results():
    log.info(Logs.fileline() + ' : TRACE list-results')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook list results => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'list-results'
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    json_ihm  = {}
    json_data = {}

    dt_start_req = datetime.now()

    # List pathogen
    data, redir = be_get('/services/dict/det/pathogène', 'list pathogen')
    if redir:
        return redir
    if data is not None:
        json_ihm['l_pathogen'] = data

    # List storage box
    data, redir = be_get('/services/quality/storage/box/list', 'list storage box')
    if redir:
        return redir
    if data is not None:
        json_ihm['l_box'] = data

    # Load analysis type
    data, redir = be_get('/services/dict/det/famille_analyse', 'analysis type')
    if redir:
        return redir
    if data is not None:
        json_ihm['type_ana'] = data

    # Load list results
    try:
        date_beg = datetime.strftime(datetime.now().replace(hour=0, minute=0), Constants.cst_iso_dt_HM)
        date_end = datetime.strftime(datetime.now().replace(hour=23, minute=59), Constants.cst_iso_dt_HM)

        payload = {'date_beg': date_beg,
                   'date_end': date_end,
                   'type_ana': 0,
                   'id_ana': 0,
                   'emer_ana': 0,
                   'code_pat': '',
                   'valid_res': 0,
                   'link_fam': session['user_link_fam']}

        url = session['server_int'] + '/' + session['redirect_name'] + '/services/result/list'
        req = requests.post(url, timeout=10, json=payload, headers=headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            json_data['list_res'] = json.dumps(req.json())

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests results list failed, url=%s', url)

    dt_stop_req = datetime.now()
    dt_time_req = dt_stop_req - dt_start_req

    log.info(Logs.fileline() + ' : TRACE list-results processing time = ' + str(dt_time_req))

    return render_template('list-results.html', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# Page : enter result
@app.route('/enter-result/<int:id_rec>')
@app.route('/enter-result/<int:id_rec>/<string:anchor>')
def enter_result(id_rec=0, anchor=''):
    log.info(Logs.fileline() + ' : id_rec = ' + str(id_rec))

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook enter result => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'enter-result/' + str(id_rec)
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    json_ihm  = {}
    json_data = {}

    id_pat = 0

    # If there is no prescriber in the record
    json_data['doctor'] = {}
    json_data['doctor']['id_data'] = 0

    json_ihm['anchor'] = ''

    if anchor:
        json_ihm['anchor'] = '#' + anchor

    dt_start_req = datetime.now()

    # Load products
    data, redir = be_get('/services/dict/det/type_prel', 'products list')
    if redir:
        return redir
    if data is not None:
        json_ihm['products'] = data

    # List pathogen
    data, redir = be_get('/services/dict/det/pathogène', 'list pathogen')
    if redir:
        return redir
    if data is not None:
        json_ihm['l_pathogen'] = data

    # List storage box
    data, redir = be_get('/services/quality/storage/box/list', 'list storage box')
    if redir:
        return redir
    if data is not None:
        json_ihm['l_box'] = data

    # Load list results
    try:
        payload = {'link_fam': session['user_link_fam']}

        url = session['server_int'] + '/' + session['redirect_name'] + '/services/result/record/' + str(id_rec)
        req = requests.post(url, timeout=10, json=payload, headers=headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            json_data['list_res'] = req.json()

            # Get result answer
            if json_data['list_res']:
                for res in json_data['list_res']:
                    # load result types
                    type_res = ''

                    if res['type_resultat']:
                        try:
                            url = session['server_int'] + '/' + session['redirect_name'] + '/services/dico/id/' + str(res['type_resultat'])
                            req = requests.get(url, timeout=10, headers=headers)

                            redir = be_check_or_bounce(req)
                            if redir:
                                return redir

                            if req.status_code == 200:
                                type_res = req.json()

                                # get short_label (without prefix "dico_") in type_res
                                if type_res and type_res['short_label'].startswith("dico_"):
                                    type_res = type_res['short_label'][5:]
                                else:
                                    type_res = ''

                        except requests.exceptions.RequestException:
                            log.exception(Logs.fileline() + ' : requests result type failed, url=%s', url)

                    # get unit label
                    try:
                        url = session['server_int'] + '/' + session['redirect_name'] + '/services/dico/id/' + str(res['unite'])
                        req = requests.get(url, timeout=10, headers=headers)

                        redir = be_check_or_bounce(req)
                        if redir:
                            return redir

                        res['unit'] = ''

                        if req.status_code == 200:
                            unit = req.json()

                            if unit and unit['label']:
                                res['unit'] = unit['label']

                    except requests.exceptions.RequestException:
                        log.exception(Logs.fileline() + ' : requests result unit failed, url=%s', url)

                    # get unit2 label
                    try:
                        url = session['server_int'] + '/' + session['redirect_name'] + '/services/dico/id/' + str(res['unite2'])
                        req = requests.get(url, timeout=10, headers=headers)

                        redir = be_check_or_bounce(req)
                        if redir:
                            return redir

                        res['unit2'] = ''

                        if req.status_code == 200:
                            unit2 = req.json()

                            if unit2 and unit2['label']:
                                res['unit2'] = unit2['label']

                    except requests.exceptions.RequestException:
                        log.exception(Logs.fileline() + ' : requests result unit2 failed, url=%s', url)

                    # init list of answer
                    res['res_answer'] = []
                    # get anwser
                    try:
                        if type_res:
                            url = session['server_int'] + '/' + session['redirect_name'] + '/services/dict/det/' + str(type_res)
                            req = requests.get(url, timeout=10, headers=headers)

                            redir = be_check_or_bounce(req)
                            if redir:
                                return redir

                            if req.status_code == 200:
                                res['res_answer'] = req.json()

                    except requests.exceptions.RequestException:
                        log.exception(Logs.fileline() + ' : requests results list failed, url=%s', url)

            # Load data patient
            if res and res['id_pat']:
                id_pat = res['id_pat']

            # Load data doctor
            if res and res['id_med']:
                id_med = res['id_med']

                data, redir = be_get('/services/doctor/det/' + str(id_med), 'doctor det')
                if redir:
                    return redir
                if data is not None:
                    json_data['doctor'] = data

        # If no ResultRecord found we're looking for record information
        else:
            try:
                url = session['server_int'] + '/' + session['redirect_name'] + '/services/record/det/' + str(id_rec)
                req = requests.get(url, timeout=10, headers=headers)

                redir = be_check_or_bounce(req)
                if redir:
                    return redir

                if req.status_code == 200:
                    json_data['record'] = req.json()

                    # Load data patient
                    if json_data['record']:
                        id_pat = json_data['record']['id_patient']

            except requests.exceptions.RequestException:
                log.exception(Logs.fileline() + ' : requests results list failed, url=%s', url)

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests results record failed, url=%s', url)

    json_data['patient'] = {}
    if id_pat > 0:
        data, redir = be_get('/services/patient/det/' + str(id_pat), 'patient det')
        if redir:
            return redir
        if data is not None:
            json_data['patient'] = data

    dt_stop_req = datetime.now()
    dt_time_req = dt_stop_req - dt_start_req

    log.info(Logs.fileline() + ' : TRACE enter-result processing time = ' + str(dt_time_req))

    return render_template('enter-result.html', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# Page : List of records
@app.route('/list-records')
def list_records():
    log.info(Logs.fileline() + ' : TRACE list-records')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook list records => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'list-records'
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    id_pres = 0

    if session['user_role'] == 'P':
        id_pres = session['user_side_account']

    json_ihm  = {}
    json_data = {}

    dt_start_req = datetime.now()
    # Load analysis type
    data, redir = be_get('/services/dict/det/famille_analyse', 'analysis type')
    if redir:
        return redir
    if data is not None:
        json_ihm['type_ana'] = data

    # Load list records
    try:
        payload = {'link_fam': session['user_link_fam']}

        url = session['server_int'] + '/' + session['redirect_name'] + '/services/record/list/' + str(id_pres)
        req = requests.post(url, timeout=10, json=payload, headers=headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            json_data = json.dumps(req.json())

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests records list failed, url=%s', url)

    json_ihm['id_pres'] = id_pres

    dt_stop_req = datetime.now()
    dt_time_req = dt_stop_req - dt_start_req

    log.info(Logs.fileline() + ' : TRACE list-records processing time = ' + str(dt_time_req))
    return render_template('list-records.html', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


@app.route('/list-works/<string:user_role>')
@app.route('/list-works/<string:user_role>/<string:emer>')
def list_works(user_role='', emer=''):
    log.info(Logs.fileline() + " : TRACE list-works role_known=%s", user_role in ('B', 'T'))

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook list works => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'list-works/' + str(user_role)
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    json_ihm  = {}
    json_data = {}

    if emer:
        emer = 4

    dt_start_req = datetime.now()
    # Load analysis type
    data, redir = be_get('/services/dict/det/famille_analyse', 'analysis type')
    if redir:
        return redir
    if data is not None:
        json_ihm['type_ana'] = data

    # Load list records with status filter
    try:
        payload = {'num_rec': '',
                   'stat_rec': 0,
                   'patient': '',
                   'date_beg': '',
                   'date_end': '',
                   'code_pat': '',
                   'emer': emer,
                   'link_fam': session['user_link_fam']}

        if user_role == 'B' or has_permission('RECORD_5'):
            # We looking for emergency record in more record status
            if emer == 4:
                payload['stat_work'] = '(181,182,253,254,255)'
            else:
                payload['stat_work'] = '(254,255)'
        elif user_role == 'T' or has_permission('RECORD_8'):
            payload['stat_work'] = '(181,182,253)'

        json_ihm['stat_work'] = payload['stat_work']

        url = session['server_int'] + '/' + session['redirect_name'] + '/services/record/list/0'
        req = requests.post(url, timeout=10, json=payload, headers=headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            json_data = json.dumps(req.json())
            if emer:
                json_ihm['emer'] = 'E'

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests works list failed, url=%s', url)

    dt_stop_req = datetime.now()
    dt_time_req = dt_stop_req - dt_start_req

    log.info(Logs.fileline() + ' : TRACE list-works processing time = ' + str(dt_time_req))
    return render_template('list-works.html', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# Page : global report
@app.route('/global-report')
def global_report():
    log.info(Logs.fileline() + ' : TRACE global-report')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook global report => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'global-report'
    session.modified = True

    json_data = {}

    return render_template('global-report.html', args=json_data, rand=secrets.randbelow(1000))


# Page : List of samples to do or modify
@app.route('/list-samples')
def list_samples():
    log.info(Logs.fileline() + ' : TRACE list-samples')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook list samples => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'list-samples'
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    json_data = {}

    dt_start_req = datetime.now()
    # Load list samples
    try:
        payload = {'link_fam': session['user_link_fam']}

        url = session['server_int'] + '/' + session['redirect_name'] + '/services/product/list'
        req = requests.post(url, timeout=10, json=payload, headers=headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            json_data = json.dumps(req.json())

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests samples list failed, url=%s', url)

    dt_stop_req = datetime.now()
    dt_time_req = dt_stop_req - dt_start_req

    log.info(Logs.fileline() + ' : TRACE list-samples processing time = ' + str(dt_time_req))
    return render_template('list-samples.html', args=json_data, rand=secrets.randbelow(1000))


# Page : details of a sample
@app.route('/det-sample/<int:id_prod>')
def det_sample(id_prod=0):
    log.info(Logs.fileline() + ' : TRACE det sample=' + str(id_prod))

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook det sample => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'det-sample/' + str(id_prod)
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    json_ihm  = {}
    json_data = {}

    # Load samples statut
    data, redir = be_get('/services/dict/det/prel_statut', 'samples statut list')
    if redir:
        return redir
    if data is not None:
        json_ihm['products_statut'] = data

    # Load samples type
    data, redir = be_get('/services/dict/det/type_prel', 'samples type list')
    if redir:
        return redir
    if data is not None:
        json_ihm['products'] = data

    # Load samples location choice
    data, redir = be_get('/services/dict/det/lieu_prel', 'samples location list')
    if redir:
        return redir
    if data is not None:
        json_ihm['products_location'] = data

    if id_prod > 0:
        # Load sample details
        data, redir = be_get('/services/product/det/' + str(id_prod), 'sample det')
        if redir:
            return redir
        if data is not None:
            json_data['product'] = data

        # Load record details
        try:
            url = session['server_int'] + '/' + session['redirect_name'] + '/services/record/det/' + str(json_data['product']['id_rec'])
            req = requests.get(url, timeout=10, headers=headers)

            redir = be_check_or_bounce(req)
            if redir:
                return redir

            if req.status_code == 200:
                json_data['record'] = req.json()

                # Load data patient with id_patient
                if json_data['record']['id_patient'] and json_data['record']['id_patient'] > 0:
                    data, redir = be_get('/services/patient/det/' + str(json_data['record']['id_patient']), 'patient det')
                    if redir:
                        return redir
                    if data is not None:
                        json_data['patient'] = data

        except requests.exceptions.RequestException:
            log.exception(Logs.fileline() + ' : requests record det failed, url=%s', url)

    json_data['id_prod'] = id_prod

    return render_template('det-sample.html', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# Page : doctors list (prescribers exactly)
@app.route('/list-doctors')
def list_doctors():
    log.info(Logs.fileline() + ' : TRACE list doctors')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook list doctors => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'list-doctors'
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    json_data = {}

    # Load list doctors
    try:
        url = session['server_int'] + '/' + session['redirect_name'] + '/services/doctor/list'
        req = requests.post(url, timeout=10, json={}, headers=headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            json_data = req.json()

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests doctors list failed, url=%s', url)

    return render_template('list-doctors.html', args=json_data, rand=secrets.randbelow(1000))


# Page : details doctor (prescribers exactly
@app.route('/det-doctor/<int:id_doctor>')
def det_doctor(id_doctor=0):
    log.info(Logs.fileline() + ' : TRACE setting det doctor=' + str(id_doctor))

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook det doctor => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'det-doctor/' + str(id_doctor)
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp

    json_ihm  = {}
    json_data = {}

    # Load speciality
    data, redir = be_get('/services/dict/det/specialite', 'speciality list')
    if redir:
        return redir
    if data is not None:
        json_ihm['spe_list'] = data

    # Load civility
    data, redir = be_get('/services/dict/det/titre_civilite', 'civility list')
    if redir:
        return redir
    if data is not None:
        json_ihm['civility'] = data

    if id_doctor > 0:
        # Load doctor details
        data, redir = be_get('/services/doctor/det/' + str(id_doctor), 'doctor det')
        if redir:
            return redir
        if data is not None:
            json_data = data

    json_data['id_doctor'] = id_doctor

    return render_template('det-doctor.html', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


def new_req(req_type):
    """
    Shared handler to start a new analysis request, for an inpatient ('I')
    or an outpatient ('E').
    """
    page = 'new-req-int' if req_type == 'I' else 'new-req-ext'

    log.info(Logs.fileline() + ' : TRACE ' + page)

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook ' + page + ' => disconnect')
        session.clear()
        return index()

    session['current_page'] = page
    session.modified = True

    return render_template('new-req.html', req_type=req_type, rand=secrets.randbelow(1000))


# Page : new external request
@app.route('/new-req-ext')
def new_req_ext():
    return new_req('E')


# Page : new internal request
@app.route('/new-req-int')
def new_req_int():
    return new_req('I')


# Page : patient details
@app.route('/det-patient/<string:type_req>/<int:id_pat>')
def det_patient(type_req='E', id_pat=0):
    log.info(Logs.fileline() + ' : TRACE det-patient id_pat = ' + str(id_pat))

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook det patient => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'det-patient/' + type_req + '/' + str(id_pat)
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    json_ihm  = {}
    json_data = {}

    has_pat_hist_form = False

    dt_start_req = datetime.now()

    try:
        path = Constants.cst_form_pat
        for filename in os.listdir(path):
            if filename.startswith('form_patient_hist_') and filename.endswith('.toml'):
                has_pat_hist_form = True
                break
    except Exception:
        log.exception(Logs.fileline() + ' : failed to detect patient history form')

    # Load unit age
    data, redir = be_get('/services/dict/det/periode_unite', 'unit age')
    if redir:
        return redir
    if data is not None:
        json_ihm['pat_age_unit'] = data

    # Load blood group
    data, redir = be_get('/services/dict/det/groupesang', 'blood group')
    if redir:
        return redir
    if data is not None:
        json_ihm['pat_blood_group'] = data

    # Load blood rhesus
    data, redir = be_get('/services/dict/det/posneg', 'blood rhesus')
    if redir:
        return redir
    if data is not None:
        json_ihm['pat_blood_rhesus'] = data

    # Load nationality
    data, redir = be_get('/services/nationality/list', 'nationality list')
    if redir:
        return redir
    if data is not None:
        json_ihm['pat_nationality'] = data

    # Load data patient
    if id_pat > 0:
        try:
            url = session['server_int'] + '/' + session['redirect_name'] + '/services/patient/det/' + str(id_pat)
            req = requests.get(url, timeout=10, headers=headers)

            redir = be_check_or_bounce(req)
            if redir:
                return redir

            if req.status_code == 200:
                data_pat = req.json()
                json_data.update(data_pat)
                json_data['id_pat'] = id_pat

        except requests.exceptions.RequestException:
            log.exception(Logs.fileline() + ' : requests patient det failed, url=%s', url)

        # add form items to json_data
        data, redir = be_get('/services/patient/form/item/' + str(id_pat), 'patient det')
        if redir:
            return redir
        if data is not None:
            json_data.update(data)
    else:
        # Load unit age by default
        try:
            url = session['server_int'] + '/' + session['redirect_name'] + '/services/default/val/unite_age_defaut'
            req = requests.get(url, timeout=10, headers=headers)

            redir = be_check_or_bounce(req)
            if redir:
                return redir

            if req.status_code == 200:
                unit_age_def = req.json()
                json_ihm['unit_age_def'] = 0

                val_age_def = unit_age_def['value'].lower()

                # unit_age['code'] without accent so we need to remove it from val_age_def to compare
                if val_age_def == 'années':
                    val_age_def = 'annees'

                for unit_age in json_ihm['pat_age_unit']:
                    if unit_age['code'] == val_age_def:
                        json_data['def_age_unit'] = unit_age['id_data']

        except requests.exceptions.RequestException:
            log.exception(Logs.fileline() + ' : requests unite_age_defaut failed, url=%s', url)

        # generate a code
        try:
            url = session['server_int'] + '/' + session['redirect_name'] + '/services/patient/generate/code'
            req = requests.get(url, timeout=10, headers=headers)

            redir = be_check_or_bounce(req)
            if redir:
                return redir

            if req.status_code == 200:
                json_data['pat_code'] = req.json()
                json_data['id_pat'] = 0

        except requests.exceptions.RequestException:
            log.exception(Logs.fileline() + ' : requests patient generate code failed, url=%s', url)

    # --- Form from file ---
    # build filename with lang check if exist otherwise take file with lang by default
    form_filename = 'form_patient_fr.toml'

    if session['lang_select'] and session['lang_select'] != 'FR':
        form_filename = 'form_patient_' + session['lang_select'].lower() + '.toml'

        dirpath = Constants.cst_form_pat

        path = os.path.join(dirpath, form_filename)

        # test if not exist
        if not (os.path.isfile(path) and path.endswith('.toml')):
            form_filename = 'form_patient_fr.toml'

    ret_build_form = Form.build_form('PAT', form_filename)
    json_data['form_html'] = ret_build_form['form_html']
    json_data['json_save'] = ret_build_form['json_save']
    json_data['has_pat_hist_form'] = has_pat_hist_form

    tpl_html = render_template('det-patient.html', type_req=type_req, ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))

    dt_stop_req = datetime.now()
    dt_time_req = dt_stop_req - dt_start_req

    log.info(Logs.fileline() + ' : TRACE det-patient processing time = ' + str(dt_time_req))

    return render_template_string(tpl_html, type_req=type_req, ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# Page : patient history (form-based)
@app.route('/det-pat-hist/<int:id_pat>')
def det_pat_hist(id_pat=0):
    log.info(Logs.fileline() + ' : TRACE det-pat-hist id_pat = ' + str(id_pat))

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook det-pat-hist => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'det-pat-hist/' + str(id_pat)
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp

    json_data = {}
    json_data['id_pat'] = id_pat

    # --- Form PAT-HIST depuis fichier TOML ---
    form_filename = 'form_patient_hist_fr.toml'

    if session.get('lang_select') and session['lang_select'] != 'FR':
        form_filename = 'form_patient_hist_' + session['lang_select'].lower() + '.toml'

        dirpath = Constants.cst_form_pat
        path = os.path.join(dirpath, form_filename)

        # si fichier inexistant, on revient au FR
        if not (os.path.isfile(path) and path.endswith('.toml')):
            form_filename = 'form_patient_hist_fr.toml'

    ret_build_form = Form.build_form('PAT-HIST', form_filename)
    json_data['form_html'] = ret_build_form['form_html']
    json_data['history_js'] = ret_build_form.get('history_js', '')

    tpl_html = render_template(
        'det-pat-hist.html',
        id_pat=id_pat,
        args=json_data,
        rand=secrets.randbelow(1000)
    )

    return render_template_string(
        tpl_html,
        id_pat=id_pat,
        args=json_data,
        rand=secrets.randbelow(1000)
    )


# Page : wrapper request details
def det_req(req_type, entry='Y', ref=0):
    log.info(Logs.fileline() + ' : TRACE det-req-' + req_type + ' ref = ' + str(ref))

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook det-req-ext => disconnect')
        session.clear()
        return index()

    session['current_page'] = f'det-req-{"int" if req_type == "I" else "ext"}/{entry}/{ref}'
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    get_software_settings(headers)

    json_ihm  = {}
    json_data = {}

    dt_start_req = datetime.now()
    # Detect if a patient history form TOML exists
    has_pat_hist_form = False
    try:
        path = Constants.cst_form_pat
        for filename in os.listdir(path):
            if filename.startswith('form_patient_hist_') and filename.endswith('.toml'):
                has_pat_hist_form = True
                break
    except Exception:
        log.exception(Logs.fileline() + ' : failed to detect patient history form')

    if entry == "Y":
        # ref = id_pat
        # Load data patient
        if ref > 0:
            data, redir = be_get('/services/patient/det/' + str(ref), 'patient det')
            if redir:
                return redir
            if data is not None:
                json_data['patient'] = data

        # Load yes or no
        data, redir = be_get('/services/dict/det/yorn', 'yorn list')
        if redir:
            return redir
        if data is not None:
            json_ihm['yorn'] = data

        # Load discount billing
        data, redir = be_get('/services/dict/det/remise_facturation', 'discount bill list')
        if redir:
            return redir
        if data is not None:
            json_ihm['discount_bill'] = data

        # Load samples statut
        data, redir = be_get('/services/dict/det/prel_statut', 'samples statut list')
        if redir:
            return redir
        if data is not None:
            json_ihm['products_statut'] = data

        # Load samples
        data, redir = be_get('/services/dict/det/type_prel', 'samples list')
        if redir:
            return redir
        if data is not None:
            json_ihm['products'] = data

        # Load prix_acte
        data, redir = be_get('/services/default/val/prix_acte', 'prix_acte')
        if redir:
            return redir
        if data is not None:
            json_ihm['act_price'] = data

        # Load facturation_pat_hosp
        data, redir = be_get('/services/default/val/facturation_pat_hosp', 'billing_pat')
        if redir:
            return redir
        if data is not None:
            json_data['billing_hosp'] = data

        # load requesting services setting
        if req_type == "I":
            data, redir = be_get('/services/setting/requesting/services', 'requesting services setting')
            if redir:
                return redir
            if data is not None:
                json_ihm['req_services'] = data

        # add empty structure for post data_save after save_request
        json_data['data_analysis'] = []
        json_data['data_samples']  = []
        json_data['data_products'] = []
        json_data['record']        = []
        json_data['has_pat_hist_form'] = has_pat_hist_form

    dt_stop_req = datetime.now()
    dt_time_req = dt_stop_req - dt_start_req

    log.info(Logs.fileline() + ' : TRACE det-req processing time = ' + str(dt_time_req))

    return render_template('det-req.html', req_type=req_type, entry=entry, ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# Page : external request details
@app.route('/det-req-ext/<string:entry>/<int:ref>')
def det_req_ext(entry='Y', ref=0):
    return det_req("E", entry, ref)


# Page : internal request details
@app.route('/det-req-int/<string:entry>/<int:ref>')
def det_req_int(entry='Y', ref=0):
    return det_req("I", entry, ref)


# Page : administrative record
@app.route('/administrative-record/<string:type_req>/<int:id_rec>')
def administrative_record(type_req='E', id_rec=0):
    log.info(Logs.fileline() + ' : TRACE administrative-record id_rec = ' + str(id_rec))

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook administrative record => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'administrative-record/' + str(type_req) + '/' + str(id_rec)
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    json_ihm  = {}

    json_data = {}
    json_data['data_analysis'] = []
    json_data['data_samples']  = []
    json_data['data_reports']  = []
    json_data['data_files']    = []
    json_data['record']        = []

    # If there is no prescriber in the record
    json_data['doctor'] = {}
    json_data['doctor']['id_data'] = 0

    dt_start_req = datetime.now()
    # Detect if a patient history form TOML exists
    has_pat_hist_form = False
    try:
        path = Constants.cst_form_pat
        for filename in os.listdir(path):
            if filename.startswith('form_patient_hist_') and filename.endswith('.toml'):
                has_pat_hist_form = True
                break
    except Exception:
        log.exception(Logs.fileline() + ' : failed to detect patient history form')

    # Load save record
    try:
        url = session['server_int'] + '/' + session['redirect_name'] + '/services/record/det/' + str(id_rec)
        req = requests.get(url, timeout=10, headers=headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            json_data['record'] = req.json()

            # Load data patient with id_patient
            if json_data['record']['id_patient'] and json_data['record']['id_patient'] > 0:
                data, redir = be_get('/services/patient/det/' + str(json_data['record']['id_patient']), 'patient det')
                if redir:
                    return redir
                if data is not None:
                    json_data['patient'] = data

            # Load data doctor with id_doctor
            if json_data['record']['med_prescripteur'] and json_data['record']['med_prescripteur'] > 0:
                data, redir = be_get('/services/doctor/det/' + str(json_data['record']['med_prescripteur']), 'doctor det')
                if redir:
                    return redir
                if data is not None:
                    json_data['doctor'] = data

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests record det failed, url=%s', url)

    # Load list analysis requested
    data, redir = be_get('/services/analysis/list/req/' + str(id_rec) + '/type/Y', 'list ana')
    if redir:
        return redir
    if data is not None:
        json_data['data_analysis'] = data

    # Load list samples requested
    data, redir = be_get('/services/analysis/list/req/' + str(id_rec) + '/type/N', 'list ana')
    if redir:
        return redir
    if data is not None:
        json_data['data_samples'] = data

    # Load report attached to this record
    data, redir = be_get('/services/file/report/record/' + str(id_rec), 'report file')
    if redir:
        return redir
    if data is not None:
        json_data['data_reports'] = data

    # Load files attached to this record
    data, redir = be_get('/services/file/document/list/REC/' + str(id_rec), 'record list files')
    if redir:
        return redir
    if data is not None:
        json_data['data_files'] = data

    # Load list template RES
    data, redir = be_get('/services/setting/template/list/RES', 'list template RES')
    if redir:
        return redir
    if data is not None:
        json_ihm['tpl_result'] = data

    # Load list template OUT
    data, redir = be_get('/services/setting/template/list/OUT', 'list template')
    if redir:
        return redir
    if data is not None:
        json_ihm['tpl_outsourced'] = data

    # Load list template STI
    data, redir = be_get('/services/setting/template/list/STI', 'list template STI')
    if redir:
        return redir
    if data is not None:
        json_ihm['tpl_sticker'] = data

    # Load list template INV
    data, redir = be_get('/services/setting/template/list/INV', 'list template INV')
    if redir:
        return redir
    if data is not None:
        json_ihm['tpl_invoice'] = data

    # Load list of sending method
    data, redir = be_get('/services/setting/sending/method/list', 'sending method list')
    if redir:
        return redir
    if data is not None:
        json_ihm['send_method_list'] = data

    # Load list of sending model
    data, redir = be_get('/services/setting/sending/model/list', 'sending method list')
    if redir:
        return redir
    if data is not None:
        json_ihm['send_model_list'] = data

    json_data['has_pat_hist_form'] = has_pat_hist_form

    dt_stop_req = datetime.now()
    dt_time_req = dt_stop_req - dt_start_req

    log.info(Logs.fileline() + ' : TRACE administrative-record processing time = ' + str(dt_time_req))

    return render_template('administrative-record.html', type_req=type_req, ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# Page : technical validation
@app.route('/technical-validation/<int:id_rec>')
@app.route('/technical-validation/<int:id_rec>/<string:anchor>')
def technical_validation(id_rec=0, anchor=''):
    log.info(Logs.fileline() + ' : TRACE technical-validation id_rec = ' + str(id_rec))

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook technical validation => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'technical-validation/' + str(id_rec)
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    json_ihm  = {}
    json_data = {}

    id_pat = 0

    # If there is no prescriber in the record
    json_data['doctor'] = {}
    json_data['doctor']['id_data'] = 0

    json_ihm['anchor'] = ''

    if anchor:
        json_ihm['anchor'] = '#' + anchor

    dt_start_req = datetime.now()
    # Load list results
    try:
        payload = {'link_fam': session['user_link_fam']}

        url = session['server_int'] + '/' + session['redirect_name'] + '/services/result/record/' + str(id_rec)
        req = requests.post(url, timeout=10, json=payload, headers=headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            json_data['list_res'] = req.json()

            # Get result answer
            if json_data['list_res']:
                for res in json_data['list_res']:
                    # load result types
                    type_res = ''

                    if res['type_resultat']:
                        try:
                            url = session['server_int'] + '/' + session['redirect_name'] + '/services/dico/id/' + str(res['type_resultat'])
                            req = requests.get(url, timeout=10, headers=headers)

                            redir = be_check_or_bounce(req)
                            if redir:
                                return redir

                            if req.status_code == 200:
                                type_res = req.json()

                                # get short_label (without prefix "dico_") in type_res
                                if type_res and type_res['short_label'].startswith("dico_"):
                                    type_res = type_res['short_label'][5:]
                                else:
                                    type_res = ''

                        except requests.exceptions.RequestException:
                            log.exception(Logs.fileline() + ' : requests result type failed, url=%s', url)

                    # get result label if a value has been entered
                    if type_res and res['valeur']:
                        try:
                            url = session['server_int'] + '/' + session['redirect_name'] + '/services/dico/id/' + str(res['valeur'])
                            req = requests.get(url, timeout=10, headers=headers)

                            redir = be_check_or_bounce(req)
                            if redir:
                                return redir

                            res['res_label'] = ''

                            if req.status_code == 200:
                                dico_tmp = req.json()
                                if 'label' in dico_tmp:
                                    res['res_label'] = dico_tmp['label']
                                else:
                                    res['res_label'] = ''

                        except requests.exceptions.RequestException:
                            log.exception(Logs.fileline() + ' : requests result label failed, url=%s', url)
                    else:
                        res['res_label'] = res['valeur']

                    # get unit label
                    try:
                        url = session['server_int'] + '/' + session['redirect_name'] + '/services/dico/id/' + str(res['unite'])
                        req = requests.get(url, timeout=10, headers=headers)

                        redir = be_check_or_bounce(req)
                        if redir:
                            return redir

                        res['unit'] = ''

                        if req.status_code == 200:
                            unit = req.json()

                            # get short_label (without prefix "dico_") in type_res
                            if unit and unit['label']:
                                res['unit'] = unit['label']

                    except requests.exceptions.RequestException:
                        log.exception(Logs.fileline() + ' : requests result unit failed, url=%s', url)

                    # get unit2 label
                    try:
                        url = session['server_int'] + '/' + session['redirect_name'] + '/services/dico/id/' + str(res['unite2'])
                        req = requests.get(url, timeout=10, headers=headers)

                        redir = be_check_or_bounce(req)
                        if redir:
                            return redir

                        res['unit2'] = ''

                        if req.status_code == 200:
                            unit2 = req.json()

                            if unit2 and unit2['label']:
                                res['unit2'] = unit2['label']

                    except requests.exceptions.RequestException:
                        log.exception(Logs.fileline() + ' : requests result unit2 failed, url=%s', url)

                    # get previous result
                    try:
                        res['prev_val']  = ''
                        res['prev_date'] = ''
                        date_res = ''

                        if res['validation'] and 'date_res' in res['validation']:
                            date_res = res['validation']['date_res']

                        payload = {'id_pat': res['id_pat'], 'ref_ana': res['ref_ana'], 'ref_var': res['id_data'],
                                   'id_res': res['id_res'], 'res_type': res['type_resultat'], 'date_res': date_res}

                        url = session['server_int'] + '/' + session['redirect_name'] + '/services/result/previous'
                        req = requests.post(url, timeout=10, json=payload, headers=headers)

                        redir = be_check_or_bounce(req)
                        if redir:
                            return redir

                        if req.status_code == 200:
                            prev = req.json()

                            if prev:
                                res['prev_val']  = prev['valeur']
                                res['prev_date'] = prev['date_valid']

                    except requests.exceptions.RequestException:
                        log.exception(Logs.fileline() + ' : requests previous result failed, url=%s', url)

            # Load data patient
            if res and res['id_pat']:
                id_pat = res['id_pat']

            # Load data doctor
            if res and res['id_med']:
                id_med = res['id_med']

                data, redir = be_get('/services/doctor/det/' + str(id_med), 'doctor det')
                if redir:
                    return redir
                if data is not None:
                    json_data['doctor'] = data

            # Load record
            data, redir = be_get('/services/record/det/' + str(id_rec), 'record')
            if redir:
                return redir
            if data is not None:
                json_data['record'] = data

        # If no ResultRecord found we're looking for record information
        else:
            try:
                url = session['server_int'] + '/' + session['redirect_name'] + '/services/record/det/' + str(id_rec)
                req = requests.get(url, timeout=10, headers=headers)

                redir = be_check_or_bounce(req)
                if redir:
                    return redir

                if req.status_code == 200:
                    json_data['record'] = req.json()

                    # Load data patient
                    if json_data['record']:
                        id_pat = json_data['record']['id_patient']

            except requests.exceptions.RequestException:
                log.exception(Logs.fileline() + ' : requests results list failed, url=%s', url)

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests results record failed, url=%s', url)

    json_data['patient'] = {}
    if id_pat > 0:
        data, redir = be_get('/services/patient/det/' + str(id_pat), 'patient det')
        if redir:
            return redir
        if data is not None:
            json_data['patient'] = data

    # Load reasons to cancel a result
    data, redir = be_get('/services/dict/det/motif_annulation', 'cancel reason')
    if redir:
        return redir
    if data is not None:
        json_ihm['cancel_reason'] = data

    dt_stop_req = datetime.now()
    dt_time_req = dt_stop_req - dt_start_req

    log.info(Logs.fileline() + ' : TRACE technical-validation processing time = ' + str(dt_time_req))

    return render_template('technical-validation.html', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# Page : biological validation
@app.route('/biological-validation/<string:mode>/<int:id_rec>')
def biological_validation(mode='', id_rec=0):
    log.info(Logs.fileline() + ' : TRACE biological-validation id_rec = ' + str(id_rec))

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook biological validation => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'biological-validation/' + str(id_rec)
    session.modified = True

    if mode:
        session['current_page'] = 'biological-validation/' + mode + '/' + str(id_rec)
        session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    json_ihm  = {}
    json_data = {}

    json_data['data_reports'] = []

    id_pat = 0

    # If there is no prescriber in the record
    json_data['doctor'] = {}
    json_data['doctor']['id_data'] = 0

    # Single or Group mode of validation
    if mode and mode == 'G':
        json_ihm['mode'] = mode
        # find next record to validate
        try:
            url = session['server_int'] + '/' + session['redirect_name'] + '/services/record/next/' + str(id_rec)
            req = requests.get(url, timeout=10, headers=headers)

            redir = be_check_or_bounce(req)
            if redir:
                return redir

            if req.status_code == 200:
                id_rec_next = req.json()
                if id_rec_next and id_rec_next > 0:
                    json_ihm['id_rec_next'] = id_rec_next
                else:
                    json_ihm['id_rec_next'] = ''

        except requests.exceptions.RequestException:
            log.exception(Logs.fileline() + ' : requests record next failed, url=%s', url)
    else:
        json_ihm['mode'] = 'S'

    dt_start_req = datetime.now()

    # Load list template
    data, redir = be_get('/services/setting/template/list/RES', 'list template')
    if redir:
        return redir
    if data is not None:
        json_ihm['tpl_result'] = data

    # Load record
    try:
        url = session['server_int'] + '/' + session['redirect_name'] + '/services/record/det/' + str(id_rec)
        req = requests.get(url, timeout=10, headers=headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            json_data['record'] = req.json()

            # Get last record_validation
            url = session['server_int'] + '/' + session['redirect_name'] + '/services/record/valid/' + str(id_rec)

            redir = be_check_or_bounce(req)
            if redir:
                return redir

            req = requests.get(url, timeout=10, headers=headers)

            if req.status_code == 200:
                json_data['record']['valid'] = req.json()

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests det record and validation failed, url=%s', url)

    # Load list results
    try:
        payload = {'link_fam': session['user_link_fam']}

        url = f"{session['server_int']}/{session['redirect_name']}/services/result/record/{id_rec}"
        req = requests.post(url, timeout=10, json=payload, headers=headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            json_data['list_res'] = req.json()

            log.error(Logs.fileline() + ' : list_res = ' + str(json_data['list_res']))

            # Get result answer
            if json_data['list_res']:
                for res in json_data['list_res']:
                    # load result types
                    type_res = ''

                    if res['type_resultat']:
                        try:
                            url = session['server_int'] + '/' + session['redirect_name'] + '/services/dico/id/' + str(res['type_resultat'])
                            req = requests.get(url, timeout=10, headers=headers)

                            redir = be_check_or_bounce(req)
                            if redir:
                                return redir

                            if req.status_code == 200:
                                type_res = req.json()

                                # get short_label (without prefix "dico_") in type_res
                                if type_res and type_res['short_label'].startswith("dico_"):
                                    type_res = type_res['short_label'][5:]
                                else:
                                    type_res = ''

                        except requests.exceptions.RequestException:
                            log.exception(Logs.fileline() + ' : requests result type failed, url=%s', url)

                    # get result label if a value has been entered
                    if type_res and res['valeur']:
                        try:
                            url = session['server_int'] + '/' + session['redirect_name'] + '/services/dico/id/' + str(res['valeur'])
                            req = requests.get(url, timeout=10, headers=headers)

                            redir = be_check_or_bounce(req)
                            if redir:
                                return redir

                            res['res_label'] = ''

                            dico_tmp = req.json()
                            if req.status_code == 200 and 'label' in dico_tmp:
                                res['res_label'] = dico_tmp['label']
                            else:
                                res['res_label'] = ''

                        except requests.exceptions.RequestException:
                            log.exception(Logs.fileline() + ' : requests result label failed, url=%s', url)
                    else:
                        res['res_label'] = res['valeur']

                    # get unit label
                    try:
                        url = session['server_int'] + '/' + session['redirect_name'] + '/services/dico/id/' + str(res['unite'])
                        req = requests.get(url, timeout=10, headers=headers)

                        redir = be_check_or_bounce(req)
                        if redir:
                            return redir

                        res['unit'] = ''

                        if req.status_code == 200:
                            unit = req.json()

                            # get short_label (without prefix "dico_") in type_res
                            if unit and unit['label']:
                                res['unit'] = unit['label']

                    except requests.exceptions.RequestException:
                        log.exception(Logs.fileline() + ' : requests result unit failed, url=%s', url)

                    # get unit2 label
                    try:
                        url = session['server_int'] + '/' + session['redirect_name'] + '/services/dico/id/' + str(res['unite2'])
                        req = requests.get(url, timeout=10, headers=headers)

                        redir = be_check_or_bounce(req)
                        if redir:
                            return redir

                        res['unit2'] = ''

                        if req.status_code == 200:
                            unit2 = req.json()

                            if unit2 and unit2['label']:
                                res['unit2'] = unit2['label']

                    except requests.exceptions.RequestException:
                        log.exception(Logs.fileline() + ' : requests result unit2 failed, url=%s', url)

                    # get previous result
                    try:
                        res['prev_val']  = ''
                        res['prev_date'] = ''
                        date_res = ''

                        if res['validation'] and 'date_res' in res['validation']:
                            date_res = res['validation']['date_res']

                        payload = {'id_pat': res['id_pat'], 'ref_ana': res['ref_ana'], 'ref_var': res['id_data'],
                                   'id_res': res['id_res'], 'res_type': res['type_resultat'], 'date_res': date_res}

                        url = session['server_int'] + '/' + session['redirect_name'] + '/services/result/previous'
                        req = requests.post(url, timeout=10, json=payload, headers=headers)

                        redir = be_check_or_bounce(req)
                        if redir:
                            return redir

                        if req.status_code == 200:
                            prev = req.json()

                            if prev:
                                res['prev_val'] = prev['valeur'] if prev['valeur'] is not None else ''
                                res['prev_date'] = prev['date_valid'] if prev['date_valid'] is not None else ''

                    except requests.exceptions.RequestException:
                        log.exception(Logs.fileline() + ' : requests previous result failed, url=%s', url)

            # Load data patient
            if res and res['id_pat']:
                id_pat = res['id_pat']

            # Load data doctor
            if res and res['id_med']:
                id_med = res['id_med']

                data, redir = be_get('/services/doctor/det/' + str(id_med), 'doctor det')
                if redir:
                    return redir
                if data is not None:
                    json_data['doctor'] = data

        # If no ResultRecord found we're looking for record information
        else:
            try:
                url = session['server_int'] + '/' + session['redirect_name'] + '/services/record/det/' + str(id_rec)
                req = requests.get(url, timeout=10, headers=headers)

                redir = be_check_or_bounce(req)
                if redir:
                    return redir

                if req.status_code == 200:
                    json_data['record'] = req.json()

                    # Load data patient
                    if json_data['record']:
                        id_pat = json_data['record']['id_patient']

            except requests.exceptions.RequestException:
                log.exception(Logs.fileline() + ' : requests results list failed, url=%s', url)

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests results record failed, url=%s', url)

    json_data['patient'] = {}
    if id_pat > 0:
        data, redir = be_get('/services/patient/det/' + str(id_pat), 'patient det')
        if redir:
            return redir
        if data is not None:
            json_data['patient'] = data

    # Load report attached to this record
    data, redir = be_get('/services/file/report/record/' + str(id_rec), 'report file')
    if redir:
        return redir
    if data is not None:
        json_data['data_reports'] = data

    # Load reasons to cancel a result
    data, redir = be_get('/services/dict/det/motif_annulation', 'cancel reason')
    if redir:
        return redir
    if data is not None:
        json_ihm['cancel_reason'] = data

    # Load list of sending method
    data, redir = be_get('/services/setting/sending/method/list', 'sending method list')
    if redir:
        return redir
    if data is not None:
        json_ihm['send_method_list'] = data

    # Load list of sending model
    data, redir = be_get('/services/setting/sending/model/list', 'sending method list')
    if redir:
        return redir
    if data is not None:
        json_ihm['send_model_list'] = data

    dt_stop_req = datetime.now()
    dt_time_req = dt_stop_req - dt_start_req

    log.info(Logs.fileline() + ' : TRACE biological-validation processing time = ' + str(dt_time_req))

    log.info(Logs.fileline() + ' : TRACE DEBUG json_data = ' + str(json_data))

    return render_template('biological-validation.html', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# --------------------
# --- Report page ---
# --------------------

# Page : report activity
@app.route('/report-activity')
def report_activity():
    log.info(Logs.fileline() + ' : TRACE report activity')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook report activity => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'report-activity'
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    json_ihm  = {}
    json_data = {}

    json_ihm['lite_users'] = []
    try:
        url = session['server_int'] + '/' + session['redirect_name'] + '/services/user/lite/list'
        req = requests.get(url, timeout=10, headers=headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            json_ihm['lite_users'] = req.json()
    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : load lite users failed, url=%s', url)

    # Load list template ACT
    data, redir = be_get('/services/setting/template/list/ACT', 'list template ACT')
    if redir:
        return redir
    if data is not None:
        json_ihm['tpl_activity_report'] = data

    # Load analysis type
    data, redir = be_get('/services/dict/det/famille_analyse', 'analysis type')
    if redir:
        return redir
    if data is not None:
        json_ihm['type_ana'] = data

    # load age interval setting
    data, redir = be_get('/services/setting/age/interval', 'age interval setting')
    if redir:
        return redir
    if data is not None:
        json_ihm['age_interval'] = data

    # load data for activity
    try:
        date_beg = date.today()
        date_beg = date_beg - timedelta(days=31)
        date_beg = datetime.strftime(date_beg.replace(day=1), Constants.cst_isodate)

        date_end = date.today()
        date_end = datetime.strftime(date_end, Constants.cst_isodate)

        json_data['date_beg'] = date_beg
        json_data['date_end'] = date_end

        payload = {'date_beg': date_beg + " 00:00",
                   'date_end': date_end + " 23:59",
                   'type_ana': 0}

        url = session['server_int'] + '/' + session['redirect_name'] + '/services/report/activity'
        req = requests.post(url, timeout=10, json=payload, headers=headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            json_data['stat'] = json.dumps(req.json())

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests report activity failed, url=%s', url)

    return render_template('report-activity.html', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# Page : report epidemiological
@app.route('/report-epidemio')
@app.route('/report-epidemio/<string:date_beg>/<string:date_end>')
@app.route('/report-epidemio/<string:date_beg>/<string:date_end>/<string:lite_filter>/<int:lite_user_id>')
def report_epidemio(date_beg='', date_end='', lite_filter='A', lite_user_id=0):
    log.info(Logs.fileline() + ' : TRACE report epidemio')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook report epidemio => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'report-epidemio'
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    json_ihm  = {}
    json_data = {}

    # Load lite users list
    json_ihm['lite_users'] = []
    try:
        url = session['server_int'] + '/' + session['redirect_name'] + '/services/user/lite/list'
        req = requests.get(url, timeout=10, headers=headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            users = req.json()
            json_ihm['lite_users'] = [u for u in users if u.get('role_type') != 'A']
    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : load lite users failed, url=%s', url)

    # Normalize lite filter
    if lite_filter not in ('A', 'N', 'Y'):
        lite_filter = 'A'
    if lite_filter != 'Y':
        lite_user_id = 0

    json_data['lite_filter'] = lite_filter
    json_data['lite_user_id'] = lite_user_id

    # load data for epiodemio
    try:
        if not date_beg:
            date_beg = date.today()
            date_beg = date_beg - timedelta(days=31)
            date_beg = datetime.strftime(date_beg.replace(day=1), Constants.cst_isodate)

        if not date_end:
            date_end = date.today()
            date_end = datetime.strftime(date_end, Constants.cst_isodate)

        json_data['date_beg'] = date_beg
        json_data['date_end'] = date_end

        payload = {'date_beg': date_beg + " 00:00",
                   'date_end': date_end + " 23:59",
                   'lite_filter': lite_filter,
                   'lite_user_id': lite_user_id}

        url = session['server_int'] + '/' + session['redirect_name'] + '/services/report/epidemio'
        req = requests.post(url, timeout=10, json=payload, headers=headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            json_data['epidemio'] = req.json()

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests report epidemio failed, url=%s', url)

    return render_template('report-epid-indi.html', report_type='epidemio', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# Page : report with indicator
@app.route('/report-indicator')
@app.route('/report-indicator/<string:date_beg>/<string:date_end>')
@app.route('/report-indicator/<string:date_beg>/<string:date_end>/<string:lite_filter>/<int:lite_user_id>')
def report_indicator(date_beg='', date_end='', lite_filter='A', lite_user_id=0):
    log.info(Logs.fileline() + ' : TRACE report indicator')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook report indicator => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'report-indicator'
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    json_ihm  = {}
    json_data = {}

    json_ihm['lite_users'] = []
    try:
        url = session['server_int'] + '/' + session['redirect_name'] + '/services/user/lite/list'
        req = requests.get(url, timeout=10, headers=headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            json_ihm['lite_users'] = req.json()
    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : load lite users failed, url=%s', url)

    # load data for indicator
    try:
        if not date_beg:
            date_beg = date.today()
            date_beg = date_beg - timedelta(days=31)
            date_beg = datetime.strftime(date_beg.replace(day=1), Constants.cst_isodate)

        if not date_end:
            date_end = date.today()
            date_end = datetime.strftime(date_end, Constants.cst_isodate)

        json_data['date_beg'] = date_beg
        json_data['date_end'] = date_end
        json_data['lite_filter'] = lite_filter
        json_data['lite_user_id'] = lite_user_id

        payload = {'date_beg': date_beg + " 00:00",
                   'date_end': date_end + " 23:59",
                   'lite_filter': lite_filter,
                   'lite_user_id': lite_user_id}

        url = session['server_int'] + '/' + session['redirect_name'] + '/services/report/indicator'
        req = requests.post(url, timeout=10, json=payload, headers=headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            json_data['indicator'] = req.json()

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests report indicator failed, url=%s', url)

    return render_template('report-epid-indi.html', report_type='indicator', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# Page : pivot table
@app.route('/pivot-table')
def pivot_table():
    log.info(Logs.fileline() + ' : TRACE pivot table')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook pivot table => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'pivot-table'
    session.modified = True

    json_ihm  = {}
    json_data = {}

    date_beg = date.today()
    date_beg = datetime.strftime(date_beg.replace(day=1), Constants.cst_isodate)

    date_end = date.today()
    date_end = datetime.strftime(date_end, Constants.cst_isodate)

    json_data['date_beg'] = date_beg
    json_data['date_end'] = date_end

    return render_template('pivot-table.html', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# Page : report statistic
@app.route('/report-statistic')
@app.route('/report-statistic/<string:lite_filter>/<int:lite_user_id>')
def report_statistic(lite_filter='A', lite_user_id=0):
    log.info(Logs.fileline() + ' : TRACE report statistic')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook report statistic => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'report-statistic'
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    json_ihm  = {}
    json_data = {}

    # load lite users
    try:
        url = session['server_int'] + '/' + session['redirect_name'] + '/services/user/lite/list'
        req = requests.get(url, timeout=10, headers=headers)
        redir = be_check_or_bounce(req)
        if redir:
            return redir
        if req.status_code == 200:
            json_ihm['lite_users'] = req.json()
    except Exception:
        log.exception(Logs.fileline() + ' : requests lite users list failed, url=%s', url)
        json_ihm['lite_users'] = []

    # load age interval setting
    data, redir = be_get('/services/setting/age/interval', 'age interval setting')
    if redir:
        return redir
    if data is not None:
        json_ihm['age_interval'] = data

    # load requesting services setting
    data, redir = be_get('/services/setting/requesting/services', 'requesting services setting')
    if redir:
        return redir
    if data is not None:
        json_ihm['req_services'] = data

    # load data for statistic
    try:
        date_beg = date.today()
        date_beg = date_beg - timedelta(days=31)
        date_beg = datetime.strftime(date_beg.replace(day=1), Constants.cst_isodate)

        date_end = date.today()
        date_end = datetime.strftime(date_end, Constants.cst_isodate)

        json_data['date_beg'] = date_beg
        json_data['date_end'] = date_end
        json_data['lite_filter'] = lite_filter
        json_data['lite_user_id'] = lite_user_id

        payload = {'date_beg': date_beg + " 00:00",
                   'date_end': date_end + " 23:59",
                   'service_int': '',
                   'lite_filter': lite_filter,
                   'lite_user_id': lite_user_id}

        url = session['server_int'] + '/' + session['redirect_name'] + '/services/report/stat'
        req = requests.post(url, timeout=10, json=payload, headers=headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            json_data['stat'] = json.dumps(req.json())

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests report stat failed, url=%s', url)

    return render_template('report-statistic.html', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# Page : report tat
@app.route('/report-tat')
def report_tat():
    log.info(Logs.fileline() + ' : TRACE report tat')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook report tat => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'report-tat'
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    json_ihm  = {}
    json_data = {}

    # Load analysis type
    data, redir = be_get('/services/dict/det/famille_analyse', 'analysis type')
    if redir:
        return redir
    if data is not None:
        json_ihm['type_ana'] = data

    # Load LabBook Lite users
    json_ihm['lite_users'] = []
    try:
        url = session['server_int'] + '/' + session['redirect_name'] + '/services/user/lite/list'
        req = requests.get(url, timeout=10, headers=headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            json_ihm['lite_users'] = req.json()
    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : load lite users failed, url=%s', url)

    return render_template('report-tat.html', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# Page : report dhis2
@app.route('/report-dhis2')
def report_dhis2():
    log.info(Logs.fileline() + ' : TRACE report dhis2')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook report dhis2 => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'report-dhis2'
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp

    json_ihm  = {}
    json_data = {}

    json_data['data_dhis2'] = []

    # Load dhis2 files in dhis2 directory
    try:
        path = Constants.cst_dhis2

        for filename in os.listdir(path):
            if not os.path.isdir(os.path.join(path, filename)) and filename.endswith('.csv'):
                json_data['data_dhis2'].append(filename)

    except Exception:
        log.exception(Logs.fileline() + ' : load dhis2 files in dhis2 directory failed')

    # Load list dhis2 setting
    data, redir = be_get('/services/setting/dhis2/api/list', 'list dhis2 setting')
    if redir:
        return redir
    if data is not None:
        json_ihm['dhs'] = data

    return render_template('report-dhis2.html', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# Page : WHONET export
@app.route('/whonet-export')
def whonet_export():
    log.info(Logs.fileline() + ' : TRACE whonet-export')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook whonet export => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'whonet-export'
    session.modified = True

    return render_template('whonet-export.html', rand=secrets.randbelow(1000))


# Page : historic patients
@app.route('/hist-patients')
def hist_patients():
    log.info(Logs.fileline() + ' : TRACE hist patients')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook hist patients => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'hist-patients'
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    json_ihm  = {}
    json_data = {}

    # Load sex
    data, redir = be_get('/services/dict/det/sexe', 'dict sex')
    if redir:
        return redir
    if data is not None:
        json_ihm['dict_sex'] = data

    # Load list patients
    try:
        url = session['server_int'] + '/' + session['redirect_name'] + '/services/patient/list'
        req = requests.post(url, timeout=10, json={}, headers=headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            json_data = req.json()

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests patients list failed, url=%s', url)

    return render_template('hist-patients.html', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# Page : details historic patient
@app.route('/det-hist-patient/<int:id_pat>')
def det_hist_patient(id_pat=0):
    log.info(Logs.fileline() + ' : TRACE det hist patient')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook det hist patient => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'det-hist-patient/' + str(id_pat)
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp

    json_data = {}

    # Load details hitoric patient
    data, redir = be_get('/services/patient/historic/' + str(id_pat), 'details hitoric patient')
    if redir:
        return redir
    if data is not None:
        json_data = data

    return render_template('det-hist-patient.html', args=json_data, rand=secrets.randbelow(1000))


# Page : historic analyzes
@app.route('/hist-analyzes')
def hist_analyzes():
    log.info(Logs.fileline() + ' : TRACE hist analyzes')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook hist analyzes => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'hist-analyzes'
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    json_ihm  = {}
    json_data = {}

    # Load analysis type
    data, redir = be_get('/services/dict/det/famille_analyse', 'analysis type')
    if redir:
        return redir
    if data is not None:
        json_ihm['type_ana'] = data

    # Load list analyzes
    try:
        date_end = date.today()
        date_beg = date_end - timedelta(days=7)

        date_beg = datetime.strftime(date_beg, Constants.cst_isodate)
        date_end = datetime.strftime(date_end, Constants.cst_isodate)

        json_data['date_beg'] = date_beg
        json_data['date_end'] = date_end

        payload = {'date_beg': date_beg, 'date_end': date_end}

        url = session['server_int'] + '/' + session['redirect_name'] + '/services/analysis/historic/list'
        req = requests.post(url, timeout=10, json=payload, headers=headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            json_data['analyzes'] = req.json()

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests analyzes list failed, url=%s', url)

    return render_template('hist-analyzes.html', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# Page : details historic patient
@app.route('/det-hist-analysis/<int:id_ana>/<string:date_beg>/<string:date_end>')
def det_hist_analysis(id_ana=0, date_beg='', date_end=''):
    log.info(Logs.fileline() + ' : TRACE det hist analysis')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook det hist analysis => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'det-hist-analysis/' + str(id_ana) + '/' + date_beg + '/' + date_end
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    json_data = {}

    # Load details hitoric analysis
    try:
        json_data['date_beg'] = date_beg
        json_data['date_end'] = date_end

        payload = {'date_beg': date_beg, 'date_end': date_end, 'id_ana': id_ana}

        url = session['server_int'] + '/' + session['redirect_name'] + '/services/analysis/historic/details'
        req = requests.post(url, timeout=10, json=payload, headers=headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            json_data['details'] = req.json()

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests details hitoric analysis failed, url=%s', url)

    return render_template('det-hist-analysis.html', args=json_data, rand=secrets.randbelow(1000))


# Page : report today
@app.route('/report-today')
def report_today():
    log.info(Logs.fileline() + ' : TRACE report today')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook report today => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'report-today'
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    json_ihm  = {}
    json_data = {}

    # load requesting services setting
    data, redir = be_get('/services/setting/requesting/services', 'requesting services setting')
    if redir:
        return redir
    if data is not None:
        json_ihm['req_services'] = data

    try:
        date_end = date.today()
        date_beg = date_end - timedelta(days=1)

        date_beg = datetime.strftime(date_beg, Constants.cst_isodate)
        date_end = datetime.strftime(date_end, Constants.cst_isodate)

        json_data['date_beg'] = date_beg
        json_data['date_end'] = date_end

        payload = {'date_beg': date_beg + " 00:00", 'date_end': date_end + " 23:59", 'service_int': ""}

        url = session['server_int'] + '/' + session['redirect_name'] + '/services/report/today'
        req = requests.post(url, timeout=10, json=payload, headers=headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            json_data['today_list'] = req.json()

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests today list failed, url=%s', url)

    return render_template('report-today.html', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# Page : report billing
@app.route('/report-billing')
def report_billing():
    log.info(Logs.fileline() + ' : TRACE report billing')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook report billing => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'report-billing'
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    json_ihm  = {}
    json_data = {}

    # Load list template BIL
    data, redir = be_get('/services/setting/template/list/BIL', 'list template BIL')
    if redir:
        return redir
    if data is not None:
        json_ihm['tpl_billing_status'] = data

    try:
        date_end = date.today()
        date_beg = date_end - timedelta(days=7)

        date_beg = datetime.strftime(date_beg, Constants.cst_isodate)
        date_end = datetime.strftime(date_end, Constants.cst_isodate)

        json_data['date_beg'] = date_beg
        json_data['date_end'] = date_end

        payload = {'date_beg': date_beg, 'date_end': date_end, 'id_user': 0}

        url = session['server_int'] + '/' + session['redirect_name'] + '/services/report/billing'
        req = requests.post(url, timeout=10, json=payload, headers=headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            json_data['bills'] = req.json()

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests billing list failed, url=%s', url)

    return render_template('report-billing.html', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# --------------------
# --- Quality page ---
# --------------------

# Page : Quality General
@app.route('/quality-general')
def quality_general():
    log.info(Logs.fileline() + ' : TRACE quality-general')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook quality general => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'quality-general'
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp

    json_data = {}

    # Load nb_users
    data, redir = be_get('/services/user/count', 'count users')
    if redir:
        return redir
    if data is not None:
        json_data['nb_users'] = data

    # Load nb_manuals
    data, redir = be_get('/services/file/count/manual', 'count manuals')
    if redir:
        return redir
    if data is not None:
        json_data['nb_manuals'] = data

    # Load last_meeting
    data, redir = be_get('/services/quality/last/meeting', 'last meeting')
    if redir:
        return redir
    if data is not None:
        json_data['meeting'] = data

    # Load nb_noncompliances_open
    data, redir = be_get('/services/quality/count/noncompliance/open', 'count noncompliances open')
    if redir:
        return redir
    if data is not None:
        json_data['nb_noncompliances_open'] = data

    # Load nb_noncompliances_month
    data, redir = be_get('/services/quality/count/noncompliance/month', 'count noncompliances month')
    if redir:
        return redir
    if data is not None:
        json_data['nb_noncompliances_month'] = data

    return render_template('quality-general.html', args=json_data, rand=secrets.randbelow(1000))


# Page : list laboratory
@app.route('/list-laboratory')
def list_laboratory():
    log.info(Logs.fileline() + ' : TRACE list laboratory')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook list laboratory => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'list-laboratory'
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    json_data = {}

    # Load laboratory files
    data, redir = be_get('/services/file/document/list/LABO/1', 'laboratory files')
    if redir:
        return redir
    if data is not None:
        json_data['data_files'] = data

    # Load dict details
    try:
        url = session['server_int'] + '/' + session['redirect_name'] + '/services/dict/det/sections'
        req = requests.get(url, timeout=10, headers=headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            json_data['data_values'] = req.json()

            i = 0
            for val in json_data['data_values']:
                val['id_ihm'] = i
                i += 1

            json_data['data_last_id'] = i

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests dict det failed, url=%s', url)

    json_data['dict_name'] = 'sections'

    return render_template('list-laboratory.html', args=json_data, rand=secrets.randbelow(1000))


# Page : list staff
@app.route('/list-staff')
def list_staff():
    log.info(Logs.fileline() + ' : TRACE list staff')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook list staff => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'list-staff'
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    json_data = {}

    try:
        url = session['server_int'] + '/' + session['redirect_name'] + '/services/user/list'
        req = requests.post(url, timeout=10, json={}, headers=headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            json_data = req.json()

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests user list failed, url=%s', url)

    return render_template('list-staff.html', args=json_data, rand=secrets.randbelow(1000))


# Page : details staff
@app.route('/det-staff/<int:user_id>')
@app.route('/det-staff/<string:ctx>/<int:user_id>')
def det_staff(user_id=0, ctx=''):
    log.info(Logs.fileline() + ' : TRACE det staff=' + str(user_id))

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook det staff => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'det-staff/' + str(user_id)
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    json_ihm  = {}
    json_data = {}

    # the return page after saving
    if ctx:
        json_ihm['return_page'] = ctx

    # Load civility
    data, redir = be_get('/services/dict/det/titre_civilite', 'civility list')
    if redir:
        return redir
    if data is not None:
        json_ihm['civility'] = data

    # Load sections
    data, redir = be_get('/services/dict/det/sections', 'sections')
    if redir:
        return redir
    if data is not None:
        json_ihm['sections'] = data

    # Load User CV files
    data, redir = be_get('/services/file/document/list/USCV/' + str(user_id), 'User CV files')
    if redir:
        return redir
    if data is not None:
        json_data['data_USCV'] = data

    # Load User Diploma files
    data, redir = be_get('/services/file/document/list/USDI/' + str(user_id), 'User Diploma files')
    if redir:
        return redir
    if data is not None:
        json_data['data_USDI'] = data

    # Load User Training files
    data, redir = be_get('/services/file/document/list/USTR/' + str(user_id), 'User Training files')
    if redir:
        return redir
    if data is not None:
        json_data['data_USTR'] = data

    # Load User Evaluation files
    data, redir = be_get('/services/file/document/list/USEV/' + str(user_id), 'User Evaluation files')
    if redir:
        return redir
    if data is not None:
        json_data['data_USEV'] = data

    # Load User signature files
    data, redir = be_get('/services/file/document/list/SIGN/' + str(user_id), 'User signature files')
    if redir:
        return redir
    if data is not None:
        json_data['data_SIGN'] = data

    if user_id > 0:
        # Load user details
        try:
            url = session['server_int'] + '/' + session['redirect_name'] + '/services/user/det/' + str(user_id)
            req = requests.get(url, timeout=10, headers=headers)

            redir = be_check_or_bounce(req)
            if redir:
                return redir

            if req.status_code == 200:
                json_data['user_det'] = req.json()
            else:
                json_data['user_det'] = []

        except requests.exceptions.RequestException:
            log.exception(Logs.fileline() + ' : requests user det failed, url=%s', url)

    json_data['user_id'] = user_id

    return render_template('det-staff.html', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# Page : list equipment
@app.route('/list-equipment')
def list_equipment():
    log.info(Logs.fileline() + ' : TRACE list equipment')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook list equipment => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'list-equipment'
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp

    json_data = {}

    data, redir = be_get('/services/quality/equipment/list', 'equipment list')
    if redir:
        return redir
    if data is not None:
        json_data = data

    return render_template('list-equipment.html', args=json_data, rand=secrets.randbelow(1000))


# Page : details equipment
@app.route('/det-equipment/<int:id_eqp>')
def det_equipment(id_eqp=0):
    log.info(Logs.fileline() + ' : TRACE det equipment=' + str(id_eqp))

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook det equipment => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'det-equipment/' + str(id_eqp)
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp

    json_ihm  = {}
    json_data = {}

    json_data['det_eqp'] = {}

    # Load sections
    data, redir = be_get('/services/dict/det/sections', 'sections')
    if redir:
        return redir
    if data is not None:
        json_ihm['sections'] = data

    # Load equipment status
    data, redir = be_get('/services/dict/det/etat_equipement', 'equipment status')
    if redir:
        return redir
    if data is not None:
        json_ihm['statuses'] = data

    if id_eqp > 0:
        # Load Equipment Photo files
        data, redir = be_get('/services/file/document/list/EQPH/' + str(id_eqp), 'Equipment Photo files')
        if redir:
            return redir
        if data is not None:
            json_data['data_EQPH'] = data

        # Load Equipment Bill files
        data, redir = be_get('/services/file/document/list/EQBI/' + str(id_eqp), 'Equipment Bill files')
        if redir:
            return redir
        if data is not None:
            json_data['data_EQBI'] = data

        # Load equipment details
        data, redir = be_get('/services/quality/equipment/det/' + str(id_eqp), 'equipment det')
        if redir:
            return redir
        if data is not None:
            json_data['det_eqp'] = data

    json_data['id_eqp'] = id_eqp

    return render_template('det-equipment.html', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# Page : documents equipment
@app.route('/eqp-document/<int:id_eqp>')
def eqp_document(id_eqp=0):
    log.info(Logs.fileline() + ' : TRACE eqp document=' + str(id_eqp))

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook eqp document => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'eqp-document/' + str(id_eqp)
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp

    json_ihm  = {}
    json_data = {}

    # Load Equipment document Manuels
    data, redir = be_get('/services/quality/equipment/doc/MANU/' + str(id_eqp), 'Equipment document MANU')
    if redir:
        return redir
    if data is not None:
        json_data['data_MANU'] = data

    # Load Equipment document Procedures
    data, redir = be_get('/services/quality/equipment/doc/PROC/' + str(id_eqp), 'Equipment document PROC')
    if redir:
        return redir
    if data is not None:
        json_data['data_PROC'] = data

    # Load equipment document comment
    data, redir = be_get('/services/quality/equipment/comm/DOC/' + str(id_eqp), 'equipment comm DOC')
    if redir:
        return redir
    if data is not None:
        json_data['comm'] = data

    json_data['id_eqp'] = id_eqp

    return render_template('eqp-document.html', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# Page : list failure of equipment
@app.route('/list-eqp-failure/<int:id_eqp>')
def list_eqp_failure(id_eqp=0):
    log.info(Logs.fileline() + ' : TRACE list eqp failure' + str(id_eqp))

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook list eqp failure => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'list-eqp-failure/' + str(id_eqp)
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp

    json_data = {}

    data, redir = be_get('/services/quality/equipment/failure/list/' + str(id_eqp), 'equipment failure list')
    if redir:
        return redir
    if data is not None:
        json_data['eqf'] = data

    # Load equipment details to get name
    data, redir = be_get('/services/quality/equipment/det/' + str(id_eqp), 'equipment det')
    if redir:
        return redir
    if data is not None:
        json_data['det_eqp'] = data

    json_data['id_eqp'] = id_eqp

    return render_template('list-eqp-failure.html', args=json_data, rand=secrets.randbelow(1000))


# Page : failures equipment
@app.route('/eqp-failure/<int:id_eqp>')
def eqp_failure(id_eqp=0):
    return eqp_operation(id_eqp, 'FAILURE')


# Page : list metrology of equipment
@app.route('/list-eqp-metrology/<int:id_eqp>')
def list_eqp_metrology(id_eqp=0):
    log.info(Logs.fileline() + ' : TRACE list eqp metrology' + str(id_eqp))

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook list eqp metrology => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'list-eqp-metrology/' + str(id_eqp)
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp

    json_data = {}

    data, redir = be_get('/services/quality/equipment/metrology/list/' + str(id_eqp), 'equipment metrology list')
    if redir:
        return redir
    if data is not None:
        json_data['eqm'] = data

    # Load equipment details to get name
    data, redir = be_get('/services/quality/equipment/det/' + str(id_eqp), 'equipment det')
    if redir:
        return redir
    if data is not None:
        json_data['det_eqp'] = data

    json_data['id_eqp'] = id_eqp

    return render_template('list-eqp-metrology.html', args=json_data, rand=secrets.randbelow(1000))


def eqp_operation(id_eqp, type_doc):
    """
    Shared handler for the four dated equipment operations: metrology/calibration
    (METROLOGY), maintenance contract (CONTRACT), preventive maintenance (PREVENTIVE)
    and failure report (FAILURE).
    """
    pages = {'METROLOGY': 'eqp-metrology',
             'CONTRACT': 'eqp-maintenance-contract',
             'PREVENTIVE': 'eqp-maintenance-preventive',
             'FAILURE': 'eqp-failure'}

    labels = {'METROLOGY': 'eqp metrology',
              'CONTRACT': 'eqp maintenance contract',
              'PREVENTIVE': 'eqp preventive maintenance',
              'FAILURE': 'eqp failure'}

    page  = pages[type_doc]
    label = labels[type_doc]

    log.info(Logs.fileline() + ' : TRACE ' + label + '=' + str(id_eqp))

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook ' + label + ' => disconnect')
        session.clear()
        return index()

    session['current_page'] = page + '/' + str(id_eqp)
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp

    json_ihm  = {}
    json_data = {}

    # Load equipment details to get name
    data, redir = be_get('/services/quality/equipment/det/' + str(id_eqp), 'equipment det')
    if redir:
        return redir
    if data is not None:
        json_data['det_eqp'] = data

    json_data['id_eqp'] = id_eqp

    return render_template('eqp-operation.html', type_doc=type_doc, ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# Page : metrology equipment
@app.route('/eqp-metrology/<int:id_eqp>')
def eqp_metrology(id_eqp=0):
    return eqp_operation(id_eqp, 'METROLOGY')


# Page : list maintenance of equipment
@app.route('/list-eqp-maintenance/<int:id_eqp>')
def list_eqp_maintenance(id_eqp=0):
    log.info(Logs.fileline() + ' : TRACE list eqp maintenance' + str(id_eqp))

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook list eqp maintenance => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'list-eqp-maintenance/' + str(id_eqp)
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp

    json_data = {}

    # List of preventive maintenance
    data, redir = be_get('/services/quality/equipment/preventive/list/' + str(id_eqp), 'equipment preventive maintenance list')
    if redir:
        return redir
    if data is not None:
        json_data['eqpm'] = data

    # List of maintenance contract
    data, redir = be_get('/services/quality/equipment/contract/list/' + str(id_eqp), 'equipment maintenance contract list')
    if redir:
        return redir
    if data is not None:
        json_data['eqmc'] = data

    # Load equipment details to get name
    data, redir = be_get('/services/quality/equipment/det/' + str(id_eqp), 'equipment det')
    if redir:
        return redir
    if data is not None:
        json_data['det_eqp'] = data

    json_data['id_eqp'] = id_eqp

    return render_template('list-eqp-maintenance.html', args=json_data, rand=secrets.randbelow(1000))


# Page : preventive maintenance equipment
@app.route('/eqp-maintenance-preventive/<int:id_eqp>')
def eqp_maintenance_preventive(id_eqp=0):
    return eqp_operation(id_eqp, 'PREVENTIVE')


# Page : maintenance contract equipment
@app.route('/eqp-maintenance-contract/<int:id_eqp>')
def eqp_maintenance_contract(id_eqp=0):
    return eqp_operation(id_eqp, 'CONTRACT')


# Page : suppliers list
@app.route('/list-suppliers')
def list_suppliers():
    log.info(Logs.fileline() + ' : TRACE list suppliers')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook list suppliers => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'list-suppliers'
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp

    json_data = {}

    # Load list suppliers
    data, redir = be_get('/services/quality/supplier/list', 'suppliers list')
    if redir:
        return redir
    if data is not None:
        json_data = data

    return render_template('list-suppliers.html', args=json_data, rand=secrets.randbelow(1000))


# Page : details supplier
@app.route('/det-supplier/<int:id_supplier>')
def det_supplier(id_supplier=0):
    log.info(Logs.fileline() + ' : TRACE setting det supplier=' + str(id_supplier))

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook setting det supplier => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'det-supplier/' + str(id_supplier)
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp

    json_data = {}

    if id_supplier > 0:
        # Load supplier details
        data, redir = be_get('/services/quality/supplier/det/' + str(id_supplier), 'supplier det')
        if redir:
            return redir
        if data is not None:
            json_data = data

    json_data['id_supplier'] = id_supplier

    return render_template('det-supplier.html', args=json_data, rand=secrets.randbelow(1000))


# Page : list manuals
@app.route('/list-manuals')
def list_manuals():
    log.info(Logs.fileline() + ' : TRACE list manuals')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook list manuals => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'list-manuals'
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    json_ihm  = {}
    json_data = {}

    # Load list of manual category
    data, redir = be_get('/services/setting/manual/category', 'product local list')
    if redir:
        return redir
    if data is not None:
        json_ihm['l_manualCat'] = data

    try:
        url = session['server_int'] + '/' + session['redirect_name'] + '/services/quality/manual/list'
        req = requests.post(url, timeout=10, json={}, headers=headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            json_data = req.json()

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests manual list failed, url=%s', url)

    return render_template('list-manuals.html', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# Page : details manual
@app.route('/det-manual/<int:id_manual>')
def det_manual(id_manual=0):
    log.info(Logs.fileline() + ' : TRACE setting det manual=' + str(id_manual))

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook det manual => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'det-manual/' + str(id_manual)
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp

    json_ihm  = {}
    json_data = {}

    json_data['manual_det'] = []

    # Load list of manual category
    data, redir = be_get('/services/setting/manual/category', 'product local list')
    if redir:
        return redir
    if data is not None:
        json_ihm['l_manualCat'] = data

    # Load sections
    data, redir = be_get('/services/dict/det/sections', 'sections')
    if redir:
        return redir
    if data is not None:
        json_ihm['sections'] = data

    if id_manual > 0:
        # Load Manual files
        data, redir = be_get('/services/file/document/list/MANU/' + str(id_manual), 'Manual files')
        if redir:
            return redir
        if data is not None:
            json_data['data_MANU'] = data

        # Load manual details
        data, redir = be_get('/services/quality/manual/det/' + str(id_manual), 'manual det')
        if redir:
            return redir
        if data is not None:
            json_data['manual_det'] = data

    json_data['id_manual'] = id_manual

    return render_template('det-manual.html', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# Page : list procedure
@app.route('/list-procedure')
def list_procedure():
    log.info(Logs.fileline() + ' : TRACE list procedure')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook list procedure => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'list-procedure'
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp

    json_data = {}

    data, redir = be_get('/services/quality/procedure/list', 'procedure list')
    if redir:
        return redir
    if data is not None:
        json_data = data

    return render_template('list-procedure.html', args=json_data, rand=secrets.randbelow(1000))


# Page : details procedure
@app.route('/det-procedure/<int:id_procedure>')
def det_procedure(id_procedure=0):
    log.info(Logs.fileline() + ' : TRACE setting det procedure=' + str(id_procedure))

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook det procedure => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'det-procedure/' + str(id_procedure)
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp

    json_ihm  = {}
    json_data = {}

    json_data['procedure'] = []

    # Load sections
    data, redir = be_get('/services/dict/det/sections', 'sections')
    if redir:
        return redir
    if data is not None:
        json_ihm['sections'] = data

    if id_procedure > 0:
        # Load procedure files
        data, redir = be_get('/services/file/document/list/PROC/' + str(id_procedure), 'Procedure files')
        if redir:
            return redir
        if data is not None:
            json_data['data_PROC'] = data

        # Load procedure details
        data, redir = be_get('/services/quality/procedure/det/' + str(id_procedure), 'procedure det')
        if redir:
            return redir
        if data is not None:
            json_data['procedure'] = data

    json_data['id_procedure'] = id_procedure

    return render_template('det-procedure.html', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# Page : list trace download
@app.route('/list-trace-download/<string:type_trace>')
def list_trace_download(type_trace=''):
    log.info(Logs.fileline() + ' : TRACE list trace download')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook list trace download => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'list-trace-download/' + str(type_trace)
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    json_ihm  = {}
    json_data = {}

    json_ihm['type_trace'] = type_trace

    # Load list of user ident
    data, redir = be_get('/services/user/ident/list', 'user ident list')
    if redir:
        return redir
    if data is not None:
        json_ihm['user_ident'] = data

    try:
        allowed_types = {'PROC': 'PROC'}
        validated_type = allowed_types.get(type_trace)

        if not validated_type:
            return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

        url = session['server_int'] + '/' + session['redirect_name'] + '/services/quality/trace/list/' + validated_type
        req = requests.get(url, timeout=10, headers=headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            json_data = req.json()

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests trace download list failed, url=%s', url)

    return render_template('list-trace-download.html', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# Page : internal control list
@app.route('/list-ctrl-int')
def list_ctrl_int():
    log.info(Logs.fileline() + ' : TRACE internal control list')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook internal control list => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'list-ctrl-int'
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp

    json_data = {}

    data, redir = be_get('/services/quality/control/list/INT', 'internal control list')
    if redir:
        return redir
    if data is not None:
        json_data = data

    return render_template('list-ctrl-int.html', args=json_data, rand=secrets.randbelow(1000))


def det_control(id_ctrl, type_ctrl):
    """
    Shared handler for the internal (INT) and external (EXT) control detail pages.
    Both differ only by the back-end sub-path and the template flavour.
    """
    type_url = 'ext' if type_ctrl == 'EXT' else 'int'
    label    = 'external' if type_ctrl == 'EXT' else 'internal'

    log.info(Logs.fileline() + ' : TRACE ' + label + ' control det=' + str(id_ctrl))

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook ' + label + ' control det => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'det-control-' + type_url + '/' + str(id_ctrl)
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp

    json_data = {}

    json_data['control'] = []
    json_data['result']  = []

    if id_ctrl > 0:
        # Load control details
        data, redir = be_get('/services/quality/control/det/' + str(id_ctrl), '\' + label + \' control det')
        if redir:
            return redir
        if data is not None:
            json_data['control'] = data

        # Load list of result
        data, redir = be_get('/services/quality/control/' + type_url + '/res/list/' + str(id_ctrl), '\' + label + \' control res list')
        if redir:
            return redir
        if data is not None:
            json_data['result'] = data

    json_data['id_ctrl'] = id_ctrl

    return render_template('det-control.html', type_ctrl=type_ctrl, args=json_data, rand=secrets.randbelow(1000))


# Page : internal control details
@app.route('/det-control-int/<int:id_ctrl>')
def det_control_int(id_ctrl=0):
    return det_control(id_ctrl, 'INT')


# Page : internal control results
@app.route('/res-control-int/<int:ctq_ser>/<string:type_val>/<int:cti_ser>')
def res_control_int(ctq_ser, type_val='', cti_ser=0):
    log.info(Logs.fileline() + ' : TRACE internal control res=' + str(cti_ser))

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook internal control res => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'res-control-int/' + str(ctq_ser) + '/' + type_val + '/' + str(cti_ser)
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp

    json_data = {}

    json_data['result'] = []

    if cti_ser > 0:
        # Load internal control details
        data, redir = be_get('/services/quality/control/int/res/' + str(cti_ser), 'internal control res')
        if redir:
            return redir
        if data is not None:
            json_data['result'] = data

    json_data['ctq_ser']  = ctq_ser
    json_data['type_val'] = type_val
    json_data['cti_ser']  = cti_ser

    return render_template('res-control-int.html', args=json_data, rand=secrets.randbelow(1000))


# Page : external control list
@app.route('/list-ctrl-ext')
def list_ctrl_ext():
    log.info(Logs.fileline() + ' : TRACE external control list')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook external control list => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'list-ctrl-ext'
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp

    json_data = {}

    data, redir = be_get('/services/quality/control/list/EXT', 'external control list')
    if redir:
        return redir
    if data is not None:
        json_data = data

    return render_template('list-ctrl-ext.html', args=json_data, rand=secrets.randbelow(1000))


# Page : external control details
@app.route('/det-control-ext/<int:id_ctrl>')
def det_control_ext(id_ctrl=0):
    return det_control(id_ctrl, 'EXT')


# Page : external control results
@app.route('/res-control-ext/<int:ctq_ser>/<string:type_val>/<int:cte_ser>')
def res_control_ext(ctq_ser, type_val='', cte_ser=0):
    log.info(Logs.fileline() + ' : TRACE external control res=' + str(cte_ser))

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook external control res => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'res-control-ext/' + str(ctq_ser) + '/' + type_val + '/' + str(cte_ser)
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp

    json_data = {}

    json_data['result'] = []

    if cte_ser > 0:
        # Load Report control external files
        data, redir = be_get('/services/file/document/list/CTRL/' + str(cte_ser), 'Control files')
        if redir:
            return redir
        if data is not None:
            json_data['data_CTRL'] = data

        # Load external control details
        data, redir = be_get('/services/quality/control/ext/res/' + str(cte_ser), 'external control res')
        if redir:
            return redir
        if data is not None:
            json_data['result'] = data

    json_data['ctq_ser']  = ctq_ser
    json_data['type_val'] = type_val
    json_data['cte_ser']  = cte_ser

    return render_template('res-control-ext.html', args=json_data, rand=secrets.randbelow(1000))


# Page : list stock
@app.route('/list-stock')
def list_stock():
    log.info(Logs.fileline() + ' : TRACE list stock')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook list stock => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'list-stock'
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    json_ihm  = {}
    json_data = {}

    # Load product_type
    data, redir = be_get('/services/dict/det/product_type', 'product type')
    if redir:
        return redir
    if data is not None:
        json_ihm['product_type'] = data

    # Load product_conserv
    data, redir = be_get('/services/dict/det/product_conserv', 'product status')
    if redir:
        return redir
    if data is not None:
        json_ihm['product_conserv'] = data

    # Load list of local
    data, redir = be_get('/services/quality/stock/local/list', 'product local list')
    if redir:
        return redir
    if data is not None:
        json_ihm['product_local'] = data

    # Load list of stock
    try:
        url = session['server_int'] + '/' + session['redirect_name'] + '/services/quality/stock/list'
        req = requests.post(url, timeout=10, json={}, headers=headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            json_data = req.json()

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests stock list failed, url=%s', url)

    return render_template('list-stock.html', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# Page : move stock product
@app.route('/move-stock-product')
def move_stock_product():
    log.info(Logs.fileline() + ' : TRACE setting move stock product')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook setting move stock => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'move-stock-product'
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    json_ihm  = {}
    json_data = {}

    # Load list of local
    data, redir = be_get('/services/quality/stock/local/list', 'product local list')
    if redir:
        return redir
    if data is not None:
        json_ihm['product_local'] = data

    # Load stock product by local
    try:
        url = session['server_int'] + '/' + session['redirect_name'] + '/services/quality/stock/supply/list'
        req = requests.post(url, timeout=10, json={}, headers=headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            json_data = req.json()

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests list supply product failed, url=%s', url)

    return render_template('move-stock-product.html', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# Page : products list
@app.route('/list-products')
def list_products():
    log.info(Logs.fileline() + ' : TRACE list products')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook list products => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'list-products'
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp

    json_data = {}

    # Load list products
    data, redir = be_get('/services/quality/stock/product/list', 'products list')
    if redir:
        return redir
    if data is not None:
        json_data = data

    return render_template('list-products.html', args=json_data, rand=secrets.randbelow(1000))


# Page : details list stock
@app.route('/det-list-stock/<int:prd_ser>/<int:prl_ser>')
def det_list_stock(prd_ser=0, prl_ser=0):
    log.info(Logs.fileline() + ' : TRACE setting det list stock=' + str(prd_ser) + ' local=' + str(prl_ser))

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook det list stock => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'det-list-stock/' + str(prd_ser) + '/' + str(prl_ser)
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp

    json_ihm  = {}
    json_data = {}

    json_data['det_list_stock'] = []

    if prd_ser > 0:
        # Load stock product details
        data, redir = be_get('/services/quality/stock/list/det/' + str(prd_ser) + '/' + str(prl_ser), 'stock product det')
        if redir:
            return redir
        if data is not None:
            json_data['det_list_stock'] = data

    json_data['prd_ser'] = prd_ser
    json_data['prl_ser'] = prl_ser

    return render_template('det-list-stock.html', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# Page : history of supply and use of a product
@app.route('/hist-stock-product/<int:prd_ser>/<int:prl_ser>')
def hist_stock_product(prd_ser=0, prl_ser=0):
    log.info(Logs.fileline() + ' : TRACE setting hist stock product=' + str(prd_ser) + ' local=' + str(prl_ser))

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook hist stock product => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'hist-stock-product/' + str(prd_ser) + '/' + str(prl_ser)
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    json_ihm  = {}
    json_data = {}

    json_data['hist_stock_product'] = []

    if prd_ser > 0:
        # Load history stock product
        try:
            date_end = datetime.today()
            date_beg = (date_end - timedelta(days=1)).replace(month=1, day=1, hour=0, minute=0)
            date_end = date_end + timedelta(days=1)

            date_beg = datetime.strftime(date_beg, Constants.cst_isodate)
            date_end = datetime.strftime(date_end, Constants.cst_isodate)

            json_data['date_beg'] = date_beg
            json_data['date_end'] = date_end

            payload = {'date_beg': date_beg + ' 00:00', 'date_end': date_end + ' 23:59'}

            url = session['server_int'] + '/' + session['redirect_name'] + '/services/quality/stock/product/history/' + str(prd_ser) + '/' + str(prl_ser)
            req = requests.post(url, timeout=10, json=payload, headers=headers)

            redir = be_check_or_bounce(req)
            if redir:
                return redir

            if req.status_code == 200:
                json_data['hist_stock_product'] = req.json()

        except requests.exceptions.RequestException:
            log.exception(Logs.fileline() + ' : requests history stock product failed, url=%s', url)

    json_data['prd_ser'] = prd_ser
    json_data['prl_ser'] = prl_ser

    return render_template('hist-stock-product.html', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# Page : details of a product
@app.route('/det-new-product/<int:prd_ser>')
def det_new_product(prd_ser=0):
    log.info(Logs.fileline() + ' : TRACE setting det new product=' + str(prd_ser))

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook det new product => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'det-new-product/' + str(prd_ser)
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp

    json_ihm  = {}
    json_data = {}

    json_data['stock_product'] = []

    # Load product_type
    data, redir = be_get('/services/dict/det/product_type', 'product type')
    if redir:
        return redir
    if data is not None:
        json_ihm['product_type'] = data

    # Load product_conserv
    data, redir = be_get('/services/dict/det/product_conserv', 'product conserv')
    if redir:
        return redir
    if data is not None:
        json_ihm['product_conserv'] = data

    if prd_ser > 0:
        # Load stock product details
        data, redir = be_get('/services/quality/stock/product/det/' + str(prd_ser), 'stock product det')
        if redir:
            return redir
        if data is not None:
            json_data['stock_product'] = data

    json_data['prd_ser'] = prd_ser

    return render_template('det-new-product.html', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# Page : details a stock product
@app.route('/det-stock-product/<int:prs_ser>')
def det_stock_product(prs_ser=0):
    log.info(Logs.fileline() + ' : TRACE setting det stock product=' + str(prs_ser))

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook det stock product => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'det-stock-product/' + str(prs_ser)
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp

    json_ihm  = {}
    json_data = {}

    json_data['stock_product'] = []

    # Load list of local
    data, redir = be_get('/services/quality/stock/local/list', 'product local list')
    if redir:
        return redir
    if data is not None:
        json_ihm['product_local'] = data

    if prs_ser > 0:
        # Load stock product details
        data, redir = be_get('/services/quality/stock/product/det/' + str(prs_ser), 'stock product det')
        if redir:
            return redir
        if data is not None:
            json_data['stock_product'] = data

    json_data['prs_ser'] = prs_ser

    return render_template('det-stock-product.html', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# Page : list-printer
@app.route('/list-printer')
def list_printer():
    log.info(Logs.fileline() + ' : TRACE setting list-printer')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook list-printer => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'list-printer'
    session.modified = True

    json_data = {}

    return render_template('list-printer.html', args=json_data, rand=secrets.randbelow(1000))


# Page : details printer
@app.route('/det-printer/<int:id_printer>')
def det_printer(id_printer=0):
    log.info(Logs.fileline() + ' : TRACE setting det printer=' + str(id_printer))

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook det printer => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'det-printer/' + str(id_printer)
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp

    json_ihm  = {}
    json_data = {}

    json_data['printer'] = []

    if id_printer > 0:
        # Load printer details
        data, redir = be_get('/services/quality/printer/det/' + str(id_printer), 'printer det')
        if redir:
            return redir
        if data is not None:
            json_data['printer'] = data

    json_data['id_printer'] = id_printer

    return render_template('det-printer.html', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# Page : list-aliquot
@app.route('/list-aliquot')
def list_aliquot():
    log.info(Logs.fileline() + ' : TRACE setting list-aliquot')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook list-aliquot => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'list-aliquot'
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    json_ihm  = {}
    json_data = {}

    # List printer
    try:
        url = session['server_int'] + '/' + session['redirect_name'] + '/services/quality/printer/list'
        req = requests.post(url, timeout=10, headers=headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            json_ihm['l_printer'] = req.json()

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests list printer failed, url=%s', url)

    return render_template('list-aliquot.html', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# Page : list storage room
@app.route('/list-storage-room')
def list_storage_room():
    log.info(Logs.fileline() + ' : TRACE setting list-storage-room')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook setting list-storage-room => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'list-storage-room'
    session.modified = True

    json_data = {}

    return render_template('list-storage-room.html', args=json_data, rand=secrets.randbelow(1000))


# Page : add storage room
@app.route('/det-storage-room/<int:id_item>')
def det_storage_room(id_item=0):
    log.info(Logs.fileline() + ' : TRACE setting det-storage-room ' + str(id_item))

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook setting det-storage-room => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'det-storage-room/' + str(id_item)
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp

    json_data = {}

    if id_item > 0:
        # Load storage room details
        data, redir = be_get('/services/quality/storage/room/det/' + str(id_item), 'storage room det')
        if redir:
            return redir
        if data is not None:
            json_data['room'] = data
    else:
        json_data['room'] = {}

    json_data['id_item'] = id_item

    return render_template('det-storage-room.html', args=json_data, rand=secrets.randbelow(1000))


# Page : list storage
@app.route('/list-storage-chamber')
def list_storage_chamber():
    log.info(Logs.fileline() + ' : TRACE setting list-storage-chamber')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook setting list-storage-chamber => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'list-storage-chamber'
    session.modified = True

    json_data = {}

    return render_template('list-storage-chamber.html', args=json_data, rand=secrets.randbelow(1000))


# Page : add storage chamber
@app.route('/det-storage-chamber/<int:id_item>')
def det_storage_chamber(id_item=0):
    log.info(Logs.fileline() + ' : TRACE setting det-storage-chamber ' + str(id_item))

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook setting det-storage-chamber => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'det-storage-chamber/' + str(id_item)
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp

    json_ihm  = {}
    json_data = {}

    # List storage room
    data, redir = be_get('/services/quality/storage/room/list', 'list storage room')
    if redir:
        return redir
    if data is not None:
        json_ihm['l_rooms'] = data

    if id_item > 0:
        # Load storage chamber details
        data, redir = be_get('/services/quality/storage/chamber/det/' + str(id_item), 'storage chamber det')
        if redir:
            return redir
        if data is not None:
            json_data['chamber'] = data
    else:
        json_data['chamber'] = {}

    json_data['id_item'] = id_item

    return render_template('det-storage-chamber.html', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# Page : list storage compartment
@app.route('/list-storage-compartment')
def list_storage_compartment():
    log.info(Logs.fileline() + ' : TRACE setting list-storage-compartment')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook setting list-storage-compartment => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'list-storage-compartment'
    session.modified = True

    json_data = {}

    return render_template('list-storage-compartment.html', args=json_data, rand=secrets.randbelow(1000))


# Page : add storage compartment
@app.route('/det-storage-compartment/<int:id_item>')
def det_storage_compartment(id_item=0):
    log.info(Logs.fileline() + ' : TRACE setting det-storage-compartment' + str(id_item))

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook setting det-storage-compartment => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'det-storage-compartment/' + str(id_item)
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp

    json_ihm  = {}
    json_data = {}

    # List storage chamber
    data, redir = be_get('/services/quality/storage/chamber/list', 'list storage chamber')
    if redir:
        return redir
    if data is not None:
        json_ihm['l_chambers'] = data

    if id_item > 0:
        # Load storage compartment details
        data, redir = be_get('/services/quality/storage/compartment/det/' + str(id_item), 'storage compartment det')
        if redir:
            return redir
        if data is not None:
            json_data['compartment'] = data
    else:
        json_data['compartment'] = {}

    json_data['id_item'] = id_item

    return render_template('det-storage-compartment.html', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# Page : list storage box
@app.route('/list-storage-box')
def list_storage_box():
    log.info(Logs.fileline() + ' : TRACE setting list-storage-box')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook setting list-storage-box => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'list-storage-box'
    session.modified = True

    json_data = {}

    return render_template('list-storage-box.html', args=json_data, rand=secrets.randbelow(1000))


# Page : add storage box
@app.route('/det-storage-box/<int:id_item>')
def det_storage_box(id_item=0):
    log.info(Logs.fileline() + ' : TRACE setting det-storage-box' + str(id_item))

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook setting det-storage-box => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'det-storage-box/' + str(id_item)
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp

    json_ihm  = {}
    json_data = {}

    # List storage compartment
    data, redir = be_get('/services/quality/storage/compartment/list', 'list storage compartment')
    if redir:
        return redir
    if data is not None:
        json_ihm['l_compartments'] = data

    if id_item > 0:
        # Load storage box details
        data, redir = be_get('/services/quality/storage/box/det/' + str(id_item), 'storage box det')
        if redir:
            return redir
        if data is not None:
            json_data['box'] = data
    else:
        json_data['box'] = {}

    json_data['id_item'] = id_item

    return render_template('det-storage-box.html', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# Page : aliquot details
@app.route('/det-aliquot/<int:id_item>')
def det_aliquot(id_item=0):
    log.info(Logs.fileline() + ' : TRACE setting det-aliquot' + str(id_item))

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook setting det-aliquot => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'det-aliquot/' + str(id_item)
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    json_ihm  = {}
    json_data = {}

    json_data['id_pat']  = 0
    json_data['id_samp'] = 0

    # Load products
    data, redir = be_get('/services/dict/det/type_prel', 'products list')
    if redir:
        return redir
    if data is not None:
        json_ihm['products'] = data

    # List pathogen
    data, redir = be_get('/services/dict/det/pathogène', 'list pathogen')
    if redir:
        return redir
    if data is not None:
        json_ihm['l_pathogen'] = data

    # List storage box
    data, redir = be_get('/services/quality/storage/box/list', 'list storage box')
    if redir:
        return redir
    if data is not None:
        json_ihm['l_box'] = data

    if id_item > 0:
        # Load aliquot details
        try:
            url = session['server_int'] + '/' + session['redirect_name'] + '/services/quality/storage/aliquot/det/' + str(id_item)
            req = requests.get(url, timeout=10, headers=headers)

            redir = be_check_or_bounce(req)
            if redir:
                return redir

            if req.status_code == 200:
                json_data['aliquot'] = req.json()
                json_data['id_pat']  = json_data['aliquot']['sal_patient']
                json_data['id_samp'] = json_data['aliquot']['sal_sample']

        except requests.exceptions.RequestException:
            log.exception(Logs.fileline() + ' : requests aliquot det failed, url=%s', url)
    else:
        json_data['aliquot'] = {}

    json_data['id_item'] = id_item

    return render_template('det-aliquot.html', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# Page : list-sending
@app.route('/list-sending')
def list_sending():
    log.info(Logs.fileline() + ' : TRACE setting list-sending')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook list-sending => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'list-sending'
    session.modified = True

    json_ihm  = {}
    json_data = {}

    return render_template('list-sending.html', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# Page : list-jobs
@app.route('/list-jobs')
def list_jobs():
    log.info(Logs.fileline() + ' : TRACE setting list-jobs')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook list-jobs => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'list-jobs'
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    # headers = be_auth_headers()

    json_ihm  = {}
    json_data = {}

    return render_template('list-jobs.html', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# Page : histo-jobs
@app.route('/histo-jobs')
def histo_jobs():
    log.info(Logs.fileline() + ' : TRACE setting histo-jobs')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook histo-jobs => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'histo-jobs'
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    # headers = be_auth_headers()

    json_ihm  = {}
    json_data = {}

    return render_template('histo-jobs.html', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# Page : details sending method
@app.route('/det-job/<int:id_item>')
def det_job(id_item=0):
    log.info(Logs.fileline() + ' : TRACE details job ' + str(id_item))

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook details job => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'det-job/' + str(id_item)
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    json_ihm  = {"dhs": [], "tpl_activity": [], "tpl_billing": []}
    json_data = {"data_dhis2": [], "item": {}}

    # Load DHIS2 CSV filenames
    try:
        path = Constants.cst_dhis2
        for filename in os.listdir(path):
            if not os.path.isdir(os.path.join(path, filename)) and filename.endswith('.csv'):
                json_data['data_dhis2'].append(filename)
    except Exception:
        log.exception(Logs.fileline() + ' : load dhis2 files failed')

    # Load DHIS2 API configs
    try:
        url = f"{session['server_int']}/{session['redirect_name']}/services/setting/dhis2/api/list"
        req = requests.get(url, timeout=10, headers=headers)
        redir = be_check_or_bounce(req)
        if redir:
            return redir
        if req.status_code == 200:
            json_ihm['dhs'] = req.json()
    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests list dhis2 setting failed, url=%s', url)

    # Load analysis type
    data, redir = be_get('/services/dict/det/famille_analyse', 'analysis type')
    if redir:
        return redir
    if data is not None:
        json_ihm['type_ana'] = data

    # Load templates ACT
    try:
        url = f"{session['server_int']}/{session['redirect_name']}/services/setting/template/list/ACT"
        req = requests.get(url, timeout=10, headers=headers)
        redir = be_check_or_bounce(req)
        if redir:
            return redir
        if req.status_code == 200:
            json_ihm['tpl_activity'] = req.json()
    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests list template ACT failed, url=%s', url)

    # Load templates BIL
    try:
        url = f"{session['server_int']}/{session['redirect_name']}/services/setting/template/list/BIL"
        req = requests.get(url, timeout=10, headers=headers)
        redir = be_check_or_bounce(req)
        if redir:
            return redir
        if req.status_code == 200:
            json_ihm['tpl_billing'] = req.json()
    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests list template DBS failed, url=%s', url)

    # Load job details when editing
    if id_item > 0:
        try:
            url = f"{session['server_int']}/{session['redirect_name']}/services/automation/job/det/{id_item}"
            req = requests.get(url, timeout=10, headers=headers)
            redir = be_check_or_bounce(req)
            if redir:
                return redir

            item_raw = None
            if req.status_code == 200:
                # BE may return dict, list, or a JSON-encoded string; normalize to dict
                try:
                    item_raw = req.json()
                except Exception:
                    item_raw = req.text

                import json as pyjson
                if isinstance(item_raw, dict):
                    item = item_raw
                elif isinstance(item_raw, list):
                    item = item_raw[0] if item_raw else {}
                elif isinstance(item_raw, str):
                    try:
                        item = pyjson.loads(item_raw) if item_raw.strip() else {}
                    except Exception:
                        item = {}
                else:
                    item = {}

                # Normalize a few fields for the form
                # - time must be HH:MM or HH:MM:SS; pad single-digit hour
                t = item.get('ajb_schedule_time_utc')
                if isinstance(t, str) and len(t) >= 7 and t[1] == ':':
                    item['ajb_schedule_time_utc'] = '0' + t  # e.g. "9:00:00" -> "09:00:00"

                # - ensure DOW integer if present
                if 'ajb_schedule_dow' in item and item['ajb_schedule_dow'] is not None:
                    try:
                        item['ajb_schedule_dow'] = int(item['ajb_schedule_dow'])
                    except Exception:
                        pass

                json_data['item'] = item

        except requests.exceptions.RequestException:
            log.exception(Logs.fileline() + ' : requests job det failed, url=%s', url)
    else:
        json_data['item'] = {}

    json_data['id_item'] = id_item

    # Derive type for the template:
    # - when editing, take it from the item (ajb_type)
    # - when creating, accept ?type= in querystring (optional)
    try:
        from flask import request
        json_data['type_item'] = (json_data['item'].get('ajb_type')
                                  if isinstance(json_data['item'], dict) else None) \
                                 or request.args.get('type', '') \
                                 or ''
    except Exception:
        json_data['type_item'] = (json_data['item'].get('ajb_type')
                                  if isinstance(json_data['item'], dict) else '')

    return render_template('det-job.html', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# Page : list nonconformities
@app.route('/list-nonconformities')
def list_nonconformities():
    log.info(Logs.fileline() + ' : TRACE list nonconformities')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook list nonconformities => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'list-nonconformities'
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    json_data = {}

    try:
        date_end = date.today()
        date_beg = date_end - timedelta(days=30)

        date_beg = datetime.strftime(date_beg, Constants.cst_isodate)
        date_end = datetime.strftime(date_end, Constants.cst_isodate)

        json_data['date_beg'] = date_beg
        json_data['date_end'] = date_end

        payload = {'date_beg': date_beg, 'date_end': date_end}

        url = session['server_int'] + '/' + session['redirect_name'] + '/services/quality/nonconformity/list'
        req = requests.post(url, timeout=10, json=payload, headers=headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            json_data['item_list'] = req.json()

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests conformity list failed, url=%s', url)

    return render_template('list-nonconformities.html', args=json_data, rand=secrets.randbelow(1000))


# Page : apply a non-conformity
@app.route('/non-conformity/<int:id_det>')
def non_conformity(id_det=0):
    log.info(Logs.fileline() + ' : TRACE non-conformity')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook non-conformity => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'non-conformity/' + str(id_det)
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    json_data = {}

    json_data['details'] = []

    try:
        url = session['server_int'] + '/' + session['redirect_name'] + '/services/quality/nonconformity/det/' + str(id_det)
        req = requests.get(url, timeout=10, headers=headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            json_data['details'] = req.json()
            log.error(Logs.fileline() + ' : details=' + str(json_data['details']))

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests non-conformity details failed, url=%s', url)

    json_data['id_det'] = id_det

    return render_template('non-conformity.html', args=json_data, rand=secrets.randbelow(1000))


# Page : list meeting
@app.route('/list-meeting')
def list_meeting():
    log.info(Logs.fileline() + ' : TRACE list meeting')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook list meeting => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'list-meeting'
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp

    json_data = {}

    data, redir = be_get('/services/quality/meeting/list', 'meeting list')
    if redir:
        return redir
    if data is not None:
        json_data = data

    return render_template('list-meeting.html', args=json_data, rand=secrets.randbelow(1000))


# Page : details meeting
@app.route('/det-meeting/<int:id_meeting>')
def det_meeting(id_meeting=0):
    log.info(Logs.fileline() + ' : TRACE setting det meeting=' + str(id_meeting))

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook det meeting => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'det-meeting/' + str(id_meeting)
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    json_data = {}

    json_data['meeting'] = []

    if id_meeting > 0:
        # Load meeting files
        data, redir = be_get('/services/file/document/list/MEET/' + str(id_meeting), 'Meeting files')
        if redir:
            return redir
        if data is not None:
            json_data['data_MEET'] = data

        # Load meeting details
        try:
            url = session['server_int'] + '/' + session['redirect_name'] + '/services/quality/meeting/det/' + str(id_meeting)
            req = requests.get(url, timeout=10, headers=headers)

            redir = be_check_or_bounce(req)
            if redir:
                return redir

            redir = be_check_or_bounce(req)
            if redir:
                return redir

            if req.status_code == 200:
                json_data['meeting'] = req.json()

        except requests.exceptions.RequestException:
            log.exception(Logs.fileline() + ' : requests meeting det failed, url=%s', url)

    json_data['id_meeting'] = id_meeting

    return render_template('det-meeting.html', args=json_data, rand=secrets.randbelow(1000))


# Page : list messages
@app.route('/list-messages')
def list_messages():
    log.info(Logs.fileline() + ' : TRACE list messages')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook list messages => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'list-messages'
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp

    json_data = {}

    data, redir = be_get('/services/quality/message/list/' + str(session['user_id']), 'messages list')
    if redir:
        return redir
    if data is not None:
        json_data = data

    return render_template('list-messages.html', args=json_data, rand=secrets.randbelow(1000))


# Page : details message
@app.route('/det-message/<int:id_message>')
def det_message(id_message=0):
    log.info(Logs.fileline() + ' : TRACE setting det message=' + str(id_message))

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook det message => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'det-message/' + str(id_message)
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    json_ihm  = {}
    json_data = {}

    json_data['message'] = []

    if id_message > 0:
        # update to read status
        try:
            url = session['server_int'] + '/' + session['redirect_name'] + '/services/quality/message/read/' + str(id_message)
            req = requests.post(url, timeout=10, headers=headers)

            redir = be_check_or_bounce(req)
            if redir:
                return redir

            if req.status_code != 200:
                log.error(Logs.fileline() + ' : requests Message read failed status_code=%s', str(req.status_code))

        except requests.exceptions.RequestException:
            log.exception(Logs.fileline() + ' : requests Message read failed, url=%s', url)

        # Load message files
        data, redir = be_get('/services/file/document/list/MSG/' + str(id_message), 'Message files')
        if redir:
            return redir
        if data is not None:
            json_data['data_MSG'] = data

        # Load message details
        data, redir = be_get('/services/quality/message/det/' + str(id_message), 'message det')
        if redir:
            return redir
        if data is not None:
            json_data['message'] = data

    json_data['id_message'] = id_message

    return render_template('det-message.html', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# Page : list-audits
@app.route('/list-audits')
def list_audits():
    log.info(Logs.fileline() + ' : TRACE setting list-audits')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook list-audits => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'list-audits'
    session.modified = True

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    json_ihm  = {}
    json_data = {}

    # Read NTP status from local IO file
    ntp_status = {
        'synced': None,
        'timestamp_utc': None,
        'timestamp_utc_fmt': None,
        'raw_content': None
    }

    try:
        ntp_file_path = os.path.join(Constants.cst_io, 'ntp_status.out')

        if os.path.isfile(ntp_file_path):
            with open(ntp_file_path, 'r', encoding='utf-8', errors='replace') as ntp_file:
                file_content = (ntp_file.read() or '').strip()

            ntp_status['raw_content'] = file_content

            timestamp_match = re.search(r'\bts_utc=([0-9T:\-]+Z)\b', file_content)
            if timestamp_match:
                ntp_status['timestamp_utc'] = timestamp_match.group(1)

                try:
                    parsed_datetime = datetime.strptime(
                        ntp_status['timestamp_utc'],
                        '%Y-%m-%dT%H:%M:%SZ'
                    )
                    ntp_status['timestamp_utc_fmt'] = parsed_datetime.strftime(
                        '%Y-%m-%d %H:%M:%S UTC'
                    )
                except Exception:
                    ntp_status['timestamp_utc_fmt'] = ntp_status['timestamp_utc']

            synced_match = re.search(r'\bsynced=(\d)\b', file_content)
            if synced_match:
                ntp_status['synced'] = 1 if synced_match.group(1) == '1' else 0

        else:
            ntp_status['raw_content'] = 'file_not_found'

    except Exception:
        log.exception(Logs.fileline() + ' : read ntp_status.out failed')
        ntp_status['raw_content'] = 'read_error'

    json_ihm['ntp_status'] = ntp_status

    # Load list of user role
    try:
        url = session['server_int'] + '/' + session['redirect_name'] + '/services/user/role/list'
        req = requests.post(url, timeout=10, json={}, headers=headers)

        redir = be_check_or_bounce(req)
        if redir:
            return redir

        if req.status_code == 200:
            json_ihm['user_role'] = req.json()

    except requests.exceptions.RequestException:
        log.exception(Logs.fileline() + ' : requests user role list failed, url=%s', url)

    return render_template('list-audits.html', ihm=json_ihm, args=json_data, rand=secrets.randbelow(1000))


# page : det-audit
@app.route('/det-audit/<int:aud_ser>')
def det_audit(aud_ser):
    return render_template('det-audit.html', aud_ser=aud_ser)


# Page : list audit archives
@app.route('/list-audit-archives')
def list_audit_archives():
    log.info(Logs.fileline() + ' : TRACE list audit archives')

    if not test_session():
        log.info(Logs.fileline() + ' : TRACE Labbook list audit archives => disconnect')
        session.clear()
        return index()

    session['current_page'] = 'list-audit-archives'
    session.modified = True

    json_data = {}

    json_data['data_audit_archives'] = []

    # Load audit archives files in audit directory
    try:
        path = Constants.cst_audit

        for filename in os.listdir(path):
            if not os.path.isdir(os.path.join(path, filename)):
                json_data['data_audit_archives'].append(filename)

    except Exception:
        log.exception(Logs.fileline() + ' : load audit archives files in audit directory failed')

    return render_template('list-audit-archives.html', args=json_data, rand=secrets.randbelow(1000))


# --------------------
# --- Various page ---
# --------------------

# Page : contributors
@app.route('/contributors')
def contributors():
    log.info(Logs.fileline() + ' : TRACE contributors')

    return render_template('contributors.html', rand=secrets.randbelow(1000))


# Route : download a file
@app.route('/download-file/type/<string:type>/name/<string:filename>/ref/<string:type_ref>/<string:ref>')
def download_file(type='', filename='', type_ref='', ref=''):
    log.info(Logs.fileline())

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    # TYPE
    # PY   => Python : BarCode, Bill, Whonet
    # JF   => Join File
    # PH   => Photo
    # RP   => Report
    # RLT  => Report from LabBook Lite
    # RPC  => Report Copy
    # DH   => DHIS2 spreadsheet
    # DHU  => DHIS2 from job
    # BILU => Billing report from job
    # ACTU => Activity report from job
    # EP   => EPIDEMIO spreadsheet
    # FP   => Form Patient
    # FPH  => Form Patient History
    # IN   => INDICATOR spreadsheet
    # TP   => template odt
    # AA   => audit archive

    allowed_types = {'PY': 'PY', 'JF': 'JF', 'PH': 'PH', 'RP': 'RP', 'RLT': 'RLT', 'RPC': 'RPC', 'DH': 'DH', 'DHU': 'DHU',
                     'BILU': 'BILU', 'ACTU': 'ACTU', 'EP': 'EP', 'FP': 'FP', 'FPH': 'FPH', 'IN': 'IN', 'TP': 'TP', 'AA': 'AA'}

    allowed_types_ref = {
        'GEN', 'MEET', 'PROC', 'MSG', 'CTRL', 'REC', 'FORM', 'MANU', 'LABO', 'TPL',
        'EQBD', 'EQCC', 'DHIS2', 'EPIDEMIO', 'INDICATOR', 'AUDIT', 'ACTU', 'BILU',
        'DHU', 'STAFF'
    }

    validated_type = allowed_types.get(type)

    if not validated_type:
        return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

    if validated_type == 'PY':
        filepath = Constants.cst_path_tmp
        generated_name = filename
    elif validated_type == 'JF':
        # ref = id_file
        url = ''
        try:
            validated_type_ref = str(type_ref or '')
            if validated_type_ref not in allowed_types_ref:
                return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

            validated_ref = str(ref or '')
            if not validated_ref.isdigit():
                return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

            redirect_name = str(session.get('redirect_name') or '')
            if not re.fullmatch(r'[A-Za-z0-9_-]+', redirect_name):
                return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

            url = (
                str(session.get('server_int') or '') + '/' + redirect_name +
                '/services/file/document/' + quote(validated_type_ref, safe='') +
                '/' + quote(validated_ref, safe='')
            )
            req = requests.get(url, timeout=10, headers=headers)

            redir = be_check_or_bounce(req)
            if redir:
                return redir

            if req.status_code == 200:
                file_info = req.json()

                if file_info:
                    filepath = os.path.join(file_info['storage'] + '/upload', file_info['path'])
                    generated_name = file_info['generated_name']
                else:
                    return False

        except requests.exceptions.RequestException:
            log.exception(Logs.fileline() + ' : requests file document failed, url=%s', url)
    elif validated_type == 'PH':
        # ref = id_file
        url = ''
        try:
            validated_type_ref = str(type_ref or '')
            if validated_type_ref not in allowed_types_ref:
                return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

            validated_ref = str(ref or '')
            if not validated_ref.isdigit():
                return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

            redirect_name = str(session.get('redirect_name') or '')
            if not re.fullmatch(r'[A-Za-z0-9_-]+', redirect_name):
                return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

            url = (
                str(session.get('server_int') or '') + '/' + redirect_name +
                '/services/file/document/' + quote(validated_type_ref, safe='') +
                '/' + quote(validated_ref, safe='')
            )
            req = requests.get(url, timeout=10, headers=headers)

            redir = be_check_or_bounce(req)
            if redir:
                return redir

            if req.status_code == 200:
                file_info = req.json()

                if file_info:
                    filepath = os.path.join(file_info['storage'] + '/resource/photo', file_info['path'])
                    generated_name = file_info['generated_name']
                else:
                    return False

        except requests.exceptions.RequestException:
            log.exception(Logs.fileline() + " : requests file photo failed")
    elif validated_type in ('RP', 'RLT'):
        filepath = Constants.cst_report
        generated_name = filename  # UUID
        filename = f"cr_{ref}.pdf"

        path = safe_build_download_path(filepath, generated_name)
        if not path:
            log.error(Logs.fileline() + " : ERROR download-file invalid path")
            return redirect(session['server_ext'] + '/' + session['current_page'])

        if os.path.exists(path) and os.stat(path).st_size > 0:
            url = ''
            try:
                redirect_name = str(session.get('redirect_name') or '')
                if not re.fullmatch(r'[A-Za-z0-9_-]+', redirect_name):
                    return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

                validated_generated_name = str(generated_name or '')
                if not re.fullmatch(r'[A-Fa-f0-9-]{36}', validated_generated_name):
                    return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

                url = (
                    str(session.get('server_int') or '') + '/' + redirect_name +
                    '/services/file/report/nb_download/' + quote(validated_generated_name, safe='')
                )
                req = requests.post(url, timeout=10, json={}, headers=headers)

                redir = be_check_or_bounce(req)
                if redir:
                    return redir

                if req.status_code != 200:
                    return False

            except requests.exceptions.RequestException:
                log.exception(Logs.fileline() + " : requests file increase nb download failed")
    elif validated_type == 'RPC':
        filepath = Constants.cst_report
        generated_name = filename
        copy_name = 'copy_cr_' + ref + '.pdf'

        path = safe_build_download_path(filepath, generated_name)
        if not path:
            log.error(Logs.fileline() + " : ERROR download-file invalid path")
            return redirect(session['server_ext'] + '/' + session['current_page'])

        if os.path.exists(path) and os.stat(path).st_size > 0:
            url = ''
            try:
                redirect_name = str(session.get('redirect_name') or '')
                if not re.fullmatch(r'[A-Za-z0-9_-]+', redirect_name):
                    return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

                validated_generated_name = str(generated_name or '')
                if not re.fullmatch(r'[A-Fa-f0-9-]{36}', validated_generated_name):
                    return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

                validated_copy_name = str(copy_name or '')
                if not re.fullmatch(r'copy_cr_[A-Za-z0-9_-]+\.pdf', validated_copy_name):
                    return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

                # increase number of download
                url = (
                    str(session.get('server_int') or '') + '/' + redirect_name +
                    '/services/file/report/nb_download/' +
                    quote(validated_generated_name, safe='')
                )
                req = requests.post(url, timeout=10, json={}, headers=headers)

                redir = be_check_or_bounce(req)
                if redir:
                    return redir

                if req.status_code != 200:
                    return False

            except requests.exceptions.RequestException:
                log.exception(Logs.fileline() + ' : requests file increase nb download failed, url=%s', url)

            # Generate copy with watermark
            url = ''
            try:
                url = (
                    str(session.get('server_int') or '') + '/' + redirect_name +
                    '/services/file/report/' + quote(validated_generated_name, safe='') +
                    '/copy/' + quote(validated_copy_name, safe='')
                )
                req = requests.post(url, json={}, headers=headers)

                redir = be_check_or_bounce(req)
                if redir:
                    return redir

                if req.status_code != 200:
                    return False
                else:
                    filepath = Constants.cst_path_tmp
                    generated_name = validated_copy_name
                    filename = validated_copy_name

            except requests.exceptions.RequestException:
                log.exception(Logs.fileline() + ' : requests copy file failed, url=%s', url)
    elif validated_type == 'DH':
        filepath = Constants.cst_dhis2
        generated_name = filename
    elif validated_type == 'DHU':
        filepath = Constants.cst_dhis2_upload
        generated_name = ref or filename  # ref = hash name
    elif validated_type == 'BILU':
        filepath = Constants.cst_billing_upload
        generated_name = ref or filename
    elif validated_type == 'ACTU':
        filepath = Constants.cst_activity_upload
        generated_name = ref or filename
    elif validated_type == 'EP':
        filepath = Constants.cst_epidemio
        generated_name = filename
    elif validated_type in ('FP', 'FPH'):
        filepath = Constants.cst_form_pat
        generated_name = filename
    elif validated_type == 'IN':
        filepath = Constants.cst_indicator
        generated_name = filename
    elif validated_type == 'TP':
        filepath = Constants.cst_template
        generated_name = filename
    elif validated_type == 'AA':
        filepath = Constants.cst_audit
        generated_name = filename
    else:
        return False

    path = safe_build_download_path(filepath, generated_name)
    if not path:
        log.error(Logs.fileline() + " : ERROR download-file invalid path")
        return redirect(session['server_ext'] + '/' + session['current_page'])

    # check if file exist and size > 0
    if not os.path.exists(path) or os.stat(path).st_size == 0:
        log.error(Logs.fileline() + " : ERROR download-file file missing or empty")
        return redirect(session['server_ext'] + '/' + session['current_page'])

    encoded_filename = quote(filename)

    ret_file = send_file(path, as_attachment=True, download_name=encoded_filename)
    ret_file.headers["x-suggested-filename"] = encoded_filename
    ret_file.headers["Cache-Control"] = 'no-store, must-revalidate'
    ret_file.headers["Expires"] = '0'
    ret_file.headers["Content-Disposition"] = f'attachment; filename="{encoded_filename}"'
    ret_file.headers["Content-Length"] = str(os.stat(path).st_size)

    return ret_file


# Route : upload a file to permanent storage
@app.route('/upload-file/<string:type_ref>/<int:id_ref>', methods=['POST'])
def upload_file(type_ref='', id_ref=0):
    log.info(Logs.fileline() + " : upload-file called")

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    allowed_types_ref = {
        'GEN', 'MEET', 'PROC', 'MSG', 'CTRL', 'REC', 'FORM', 'MANU', 'LABO', 'TPL',
        'EQBD', 'EQBI', 'EQPH', 'EQCC', 'EQMC', 'EQPM',
        'USCV', 'USDI', 'USTR', 'USEV', 'SIGN',
        'DHIS2', 'EPIDEMIO', 'INDICATOR', 'AUDIT', 'ACTU', 'BILU', 'DHU', 'STAFF'
    }

    validated_type_ref = str(type_ref or '')
    if validated_type_ref not in allowed_types_ref:
        return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

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

            # Create end of storage path
            end_path = generated_name[:2] + "/" + generated_name[2:4] + "/"
        except Exception:
            log.exception(Logs.fileline() + ' : upload-file failed to hash name')
            return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}

        try:
            # Get last storage path
            url = session['server_int'] + '/' + session['redirect_name'] + '/services/file/storage'
            req = requests.get(url, timeout=10, headers=headers)

            redir = be_check_or_bounce(req)
            if redir:
                return redir

            if req.status_code == 200:
                storage = req.json()

                if not storage:
                    log.error(Logs.fileline() + ' : upload-file storage failed')
                    return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}
        except Exception:
            log.exception(Logs.fileline() + ' : upload-file failed requests storage')
            return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}

        filepath = Constants.cst_upload

        try:
            pathlib.Path(filepath + end_path[:2]).mkdir(mode=0o777, parents=False, exist_ok=True)
            pathlib.Path(filepath + end_path).mkdir(mode=0o777, parents=False, exist_ok=True)
        except Exception:
            log.exception(Logs.fileline() + ' : upload-file failed to filepath')
            return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}

        try:
            f.save(os.path.join(filepath + end_path, generated_name))
        except Exception:
            log.exception(Logs.fileline() + ' : upload-file failed to save file')
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
            payload = {'id_owner': session['user_id'],
                       'original_name': original_name,
                       'generated_name': generated_name,
                       'size': file_size,
                       'hash': hash_name,
                       'ext': file_ext,
                       'content_type': mime_type,
                       'id_storage': storage['id_data'],
                       'end_path': end_path}

            redirect_name = str(session.get('redirect_name') or '')
            if not re.fullmatch(r'[A-Za-z0-9_-]+', redirect_name):
                return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

            validated_type_ref = str(type_ref or '')
            if validated_type_ref not in allowed_types_ref:
                return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

            url = (
                str(session.get('server_int') or '') + '/' + redirect_name +
                '/services/file/document/' + quote(validated_type_ref, safe='') +
                '/' + str(int(id_ref))
            )
            req = requests.post(url, timeout=10, json=payload, headers=headers)

            redir = be_check_or_bounce(req)
            if redir:
                return redir

            if req.status_code != 200:
                log.error(Logs.fileline() + ' : upload-file insert failed')
                return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}

        except Exception:
            log.exception(Logs.fileline() + ' : upload-file failed information file')
            return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}

        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

    return json.dumps({'success': False}), 405, {'ContentType': 'application/json'}


# Route : upload a photo to permanent storage
@app.route('/upload-photo/<string:type_ref>/<int:id_ref>', methods=['POST'])
def upload_photo(type_ref='', id_ref=0):
    log.info(Logs.fileline() + " : upload-photo called")

    resp = ensure_be_token()
    if resp:
        return resp
    headers = be_auth_headers()

    allowed_types_ref = {'EQPH'}

    validated_type_ref = str(type_ref or '')
    if validated_type_ref not in allowed_types_ref:
        return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

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

            # Create end of storage path
            end_path = generated_name[:2] + "/" + generated_name[2:4] + "/"
        except Exception:
            log.exception(Logs.fileline() + ' : upload-photo failed to hash name')
            return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}

        try:
            # Get last storage path
            url = session['server_int'] + '/' + session['redirect_name'] + '/services/file/storage'
            req = requests.get(url, timeout=10, headers=headers)

            redir = be_check_or_bounce(req)
            if redir:
                return redir

            if req.status_code == 200:
                storage = req.json()

                if not storage:
                    log.error(Logs.fileline() + ' : upload-photo storage failed')
                    return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}
        except Exception:
            log.exception(Logs.fileline() + ' : upload-photo failed requests storage')
            return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}

        filepath = Constants.cst_photo

        try:
            full_path = os.path.join(filepath, end_path)
            pathlib.Path(full_path).mkdir(mode=0o777, parents=True, exist_ok=True)
        except Exception:
            log.exception(Logs.fileline() + ' : upload-photo failed to filepath')
            return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}

        try:
            file_path = os.path.join(filepath, end_path, generated_name)
            f.save(file_path)
        except Exception:
            log.exception(Logs.fileline() + ' : upload-photo failed to save file')
            return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}

        try:
            # Get info on file
            file_ext = pathlib.Path(original_name).suffix
            file_size = pathlib.Path(os.path.join(filepath + end_path, generated_name)).stat().st_size
            mime_type = f.mimetype

            # remove first dot
            if file_ext.startswith('.'):
                file_ext = file_ext[1:]

            # insert upload information in DB
            payload = {'id_owner': session['user_id'],
                       'original_name': original_name,
                       'generated_name': generated_name,
                       'size': file_size,
                       'hash': hash_name,
                       'ext': file_ext,
                       'content_type': mime_type,
                       'id_storage': storage['id_data'],
                       'end_path': end_path}

            redirect_name = str(session.get('redirect_name') or '')
            if not re.fullmatch(r'[A-Za-z0-9_-]+', redirect_name):
                return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

            validated_type_ref = str(type_ref or '')
            if validated_type_ref not in allowed_types_ref:
                return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

            url = (
                str(session.get('server_int') or '') + '/' + redirect_name +
                '/services/file/document/' + quote(validated_type_ref, safe='') +
                '/' + str(int(id_ref))
            )
            req = requests.post(url, timeout=10, json=payload, headers=headers)

            redir = be_check_or_bounce(req)
            if redir:
                return redir

            if req.status_code != 200:
                log.error(Logs.fileline() + ' : upload-photo insert failed')
                return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}

        except Exception:
            log.exception(Logs.fileline() + ' : upload-photo failed information file')
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
        except Exception:
            log.exception(Logs.fileline() + ' : upload-logo failed to get file from request')
            return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}

        filepath  = Constants.cst_resource
        logo_name = 'logo.png'

        log.info(Logs.fileline())

        try:
            f.save(os.path.join(filepath, logo_name))
        except Exception:
            log.exception(Logs.fileline() + ' : upload-logo failed to save file')
            return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}

        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

    return json.dumps({'success': False}), 405, {'ContentType': 'application/json'}


# Route : upload a spreadsheet for DHIS2
@app.route('/upload-dhis2', methods=['POST'])
def upload_dhis2():
    log.info(Logs.fileline())
    if request.method != 'POST':
        return json.dumps({'success': False}), 405, {'ContentType': 'application/json'}

    try:
        f = request.files['file']

        filename = f.filename
    except Exception:
        log.exception(Logs.fileline() + ' : upload-dhis2 failed to get file from request')
        return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}

    filepath = os.path.abspath(Constants.cst_dhis2)

    safe_name = secure_filename(filename)
    if not safe_name:
        return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

    if not safe_name.lower().endswith('.csv'):
        return json.dumps({'success': False}), 415, {'ContentType': 'application/json'}

    path = os.path.abspath(os.path.join(filepath, safe_name))
    if not path.startswith(filepath + os.sep):
        log.error(Logs.fileline() + ' : upload-dhis2 invalid path, filepath=%s, name=%s', filepath, safe_name)
        return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

    try:
        f.save(path)
    except Exception:
        log.exception(Logs.fileline() + ' : upload-dhis2 failed to save file')
        return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


# Route : upload a spreadsheet for EPIDEMIO
@app.route('/upload-epidemio', methods=['POST'])
def upload_epidemio():
    log.info(Logs.fileline())

    if request.method != 'POST':
        return json.dumps({'success': False}), 405, {'ContentType': 'application/json'}

    try:
        f = request.files['file']
        filename = f.filename or ''
    except Exception:
        log.exception(Logs.fileline() + ' : upload-epidemio failed to get file from request')
        return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}

    # Accept only this exact file name
    if secure_filename(filename) != 'epidemio.ini':
        return json.dumps({'success': False}), 415, {'ContentType': 'application/json'}

    filepath = os.path.abspath(Constants.cst_epidemio)
    path = os.path.join(filepath, 'epidemio.ini')  # fixed name, no user input

    try:
        f.save(path)
    except Exception:
        log.exception(Logs.fileline() + ' : upload-epidemio failed to save file')
        return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


# Route : upload a toml form
@app.route('/upload-form/<string:type_form>', methods=['POST'])
def upload_form(type_form):
    log.info(Logs.fileline())

    if request.method != 'POST':
        return json.dumps({'success': False}), 405, {'ContentType': 'application/json'}

    try:
        f = request.files['file']
        filename = f.filename or ''
    except Exception:
        log.exception(Logs.fileline() + ' : upload-form failed to get file from request')
        return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}

    if type_form == 'PAT':
        file_start_with = 'form_patient_'
        filepath = Constants.cst_form_pat
    elif type_form == 'PAT-HIST':
        file_start_with = 'form_patient_hist_'
        filepath = Constants.cst_form_pat
    else:
        return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

    safe_name = secure_filename(filename)
    if not safe_name:
        return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

    if not (safe_name.startswith(file_start_with) and safe_name.lower().endswith('.toml')):
        return json.dumps({'success': False}), 415, {'ContentType': 'application/json'}

    filepath = os.path.abspath(filepath)
    path = os.path.abspath(os.path.join(filepath, safe_name))
    if not path.startswith(filepath + os.sep):
        log.error(Logs.fileline() + ' : upload-form invalid path, filepath=%s, name=%s', filepath, safe_name)
        return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

    log.info(Logs.fileline() + ' upload-form Before save file')

    try:
        f.save(path)
    except Exception:
        log.exception(Logs.fileline() + ' : upload-form failed to save file')
        return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}

    log.info(Logs.fileline() + ' upload-form After save file')

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


# Route : upload a spreadsheet for INDICATOR
@app.route('/upload-indicator', methods=['POST'])
def upload_indicator():
    log.info(Logs.fileline())

    if request.method != 'POST':
        return json.dumps({'success': False}), 405, {'ContentType': 'application/json'}

    try:
        f = request.files['file']
        filename = f.filename or ''
    except Exception:
        log.exception(Logs.fileline() + ' : upload-indicator failed to get file from request')
        return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}

    # accept only the expected filename
    if secure_filename(filename) != 'indicator.ini':
        return json.dumps({'success': False}), 415, {'ContentType': 'application/json'}

    filepath = os.path.abspath(Constants.cst_indicator)
    path = os.path.join(filepath, 'indicator.ini')  # fixed name, no user input

    try:
        f.save(path)
    except Exception:
        log.exception(Logs.fileline() + ' : upload-indicator failed to save file')
        return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


# Route : upload a template for document
@app.route('/upload-tpl', methods=['POST'])
def upload_tpl():
    log.info(Logs.fileline())

    if request.method != 'POST':
        return json.dumps({'success': False}), 405, {'ContentType': 'application/json'}

    try:
        f = request.files['file']
        filename = f.filename or ''
    except Exception:
        log.exception(Logs.fileline() + ' : upload-tpl failed to get file from request')
        return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}

    filepath = os.path.abspath(Constants.cst_template)

    safe_name = secure_filename(filename)
    if not safe_name:
        return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

    # check extension after sanitizing
    if not (safe_name.lower().endswith('.odt') or safe_name.lower().endswith('.toml')):
        return json.dumps({'success': False}), 415, {'ContentType': 'application/json'}

    path = os.path.abspath(os.path.join(filepath, safe_name))
    if not path.startswith(filepath + os.sep):
        log.error(Logs.fileline() + ' : upload-tpl invalid path, filepath=%s, name=%s', filepath, safe_name)
        return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

    log.info(Logs.fileline() + ' upload-tpl Before save file')

    try:
        f.save(path)
    except Exception:
        log.exception(Logs.fileline() + ' : upload-tpl failed to save file')
        return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}

    log.info(Logs.fileline() + ' upload-tpl After save file')

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


# Route : upload temp file for import
@app.route('/upload-import', methods=['POST'])
def upload_import():
    log.info(Logs.fileline())

    if request.method != 'POST':
        return json.dumps({'success': False}), 405, {'ContentType': 'application/json'}

    try:
        f = request.files['file']
        filename = f.filename or ''
    except Exception:
        log.exception(Logs.fileline() + ' : upload-import failed to get file from request')
        return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}

    filepath = os.path.abspath(Constants.cst_path_tmp)

    safe_name = secure_filename(filename)
    if not safe_name:
        return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

    if not safe_name.lower().endswith('.csv'):
        return json.dumps({'success': False}), 415, {'ContentType': 'application/json'}

    path = os.path.abspath(os.path.join(filepath, safe_name))
    if not path.startswith(filepath + os.sep):
        log.error(Logs.fileline() + ' : upload-import invalid path, filepath=%s, name=%s', filepath, safe_name)
        return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

    try:
        f.save(path)
    except Exception:
        log.exception(Logs.fileline() + ' : upload-import failed to save file')
        return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


# Route : upload temp file for zipcity
@app.route('/upload-zipcity', methods=['POST'])
def upload_zipcity():
    log.info(Logs.fileline())

    if request.method != 'POST':
        return json.dumps({'success': False}), 405, {'ContentType': 'application/json'}

    try:
        f = request.files['file']
        filename = f.filename or ''
    except Exception:
        log.exception(Logs.fileline() + ' : upload-zipcity failed to get file from request')
        return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}

    filepath = os.path.abspath(Constants.cst_path_tmp)

    safe_name = secure_filename(filename)
    if not safe_name:
        return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

    if not safe_name.lower().endswith('.csv'):
        return json.dumps({'success': False}), 415, {'ContentType': 'application/json'}

    path = os.path.abspath(os.path.join(filepath, safe_name))
    if not path.startswith(filepath + os.sep):
        log.error(Logs.fileline() + ' : upload-zipcity invalid path, filepath=%s, name=%s', filepath, safe_name)
        return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

    try:
        f.save(path)
    except Exception:
        log.exception(Logs.fileline() + ' : upload-zipcity failed to save file')
        return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


# Route : upload a file for Connect
@app.route('/upload-connect/<string:type>', methods=['POST'])
def upload_connect(type=''):
    log.info(Logs.fileline() + " : upload-connect called")

    if request.method != 'POST':
        return json.dumps({'success': False}), 405, {'ContentType': 'application/json'}

    try:
        f = request.files['file']
        filename = f.filename or ''
    except Exception:
        log.exception(Logs.fileline() + ' : upload-connect failed to get file from request')
        return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}

    if type == 'plugin':
        filepath = Constants.cst_connect_plugin
        if not filename.lower().endswith('.jar'):
            return json.dumps({'success': False}), 415, {'ContentType': 'application/json'}
    elif type == 'setting':
        filepath = Constants.cst_connect_setting
    elif type == 'mapping':
        filepath = Constants.cst_connect_mapping
    else:
        return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

    filepath = os.path.abspath(filepath)

    safe_name = secure_filename(filename)
    if not safe_name:
        return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

    path = os.path.abspath(os.path.join(filepath, safe_name))
    if not path.startswith(filepath + os.sep):
        log.error(Logs.fileline() + ' : upload-connect invalid path, filepath=%s, name=%s', filepath, safe_name)
        return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

    log.info(Logs.fileline() + ' upload-connect Before save file')

    try:
        f.save(path)
    except Exception:
        log.exception(Logs.fileline() + ' : upload-connect failed to save file')
        return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}

    log.info(Logs.fileline() + ' upload-connect After save file')

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


# Route : upload file for printer
@app.route('/upload-printer', methods=['POST'])
def upload_printer():
    log.info(Logs.fileline())
    if request.method != 'POST':
        return json.dumps({'success': False}), 405, {'ContentType': 'application/json'}

    try:
        f = request.files['file']

        filename = f.filename or ''
    except Exception:
        log.exception(Logs.fileline() + ' : upload-printer failed to get file from request')
        return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}

    base_dir = Constants.cst_printer
    log.info(Logs.fileline())

    # Sanitize filename
    safe_name = secure_filename(filename)
    if not safe_name:
        log.error(Logs.fileline() + ' : upload-printer invalid filename (empty after sanitize)')
        return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

    # Only allow .sh scripts
    if not safe_name.lower().endswith('.sh'):
        return json.dumps({'success': False}), 415, {'ContentType': 'application/json'}

    try:
        base_dir_abs = os.path.abspath(base_dir)
        target_path = os.path.abspath(os.path.join(base_dir_abs, safe_name))

        # Prevent path traversal
        if not target_path.startswith(base_dir_abs + os.sep):
            log.error(Logs.fileline() + ' : upload-printer path traversal attempt: %s', target_path)
            return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

        f.save(target_path)
    except Exception:
        log.exception(Logs.fileline() + ' : upload-printer failed to save file')
        return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


# Route : delete a file
@app.route('/delete-file/<string:type>/<string:filename>')
def delete_file(type='', filename=''):
    log.info(Logs.fileline())

    # DH  => DHIS2 spreadsheet
    # FP  => Form Patient
    # FPH => Form Patient Hist
    # TP  => template odt

    if type == 'DH':
        base_dir = Constants.cst_dhis2
    elif type in ('FP', 'FPH'):
        base_dir = Constants.cst_form_pat
    elif type == 'TP':
        base_dir = Constants.cst_template
    else:
        # type inconnu → on ne fait rien
        log.error(Logs.fileline() + ' : delete-file invalid file type')
        return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

    try:
        # Sanitize filename
        safe_name = secure_filename(filename or '')
        if not safe_name:
            log.error(Logs.fileline() + ' : delete-file invalid filename (empty after sanitize)')
            return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

        # Build absolute path and prevent path traversal
        base_dir_abs = os.path.abspath(base_dir)
        target_path = os.path.abspath(os.path.join(base_dir_abs, safe_name))

        # Ensure the target path stays inside the allowed directory
        if not target_path.startswith(base_dir_abs + os.sep):
            log.error(Logs.fileline() + ' : delete-file path traversal attempt')
            return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

        if os.path.exists(target_path):
            os.remove(target_path)

    except Exception:
        log.exception(Logs.fileline() + ' : delete-file failed to delete file')
        return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/app-labbook.css')
def labbook_css():
    return Response(render_template('app-labbook.css'), mimetype='text/css')


@app.route('/app-swagger-api.yaml')
def swagger_api():
    return Response(render_template('app-swagger-api.yaml'), mimetype='text/yaml')
