# app/security/oauth_routes.py
import logging
import time
import os

from urllib.parse import urlparse
from flask import Blueprint, request, jsonify, session, current_app

# Authlib
from authlib.integrations.flask_oauth2 import AuthorizationServer
from authlib.oauth2.rfc6749 import grants
from authlib.oauth2.rfc7636 import CodeChallenge
from authlib.oauth2.rfc6750 import BearerTokenValidator
from authlib.integrations.flask_oauth2 import ResourceProtector

from app.models.DB import DB
from app.models.Logs import Logs
from app.models.User import User


log = logging.getLogger('log_services')

# OAuth routes and helpers for the BE side.
bp_oauth = Blueprint('oauth', __name__)


# ===== DB Helpers =====

def _load_client(client_id: str):
    """
    Fetch an active OAuth client row by client_id.
    Returns a dict-like row or None when not found/inactive.
    """
    cur = DB.cursor()
    cur.execute(
        "SELECT * FROM oauth2_client WHERE oacl_client_id=%s AND oacl_is_active='Y'",
        (client_id,)
    )
    return cur.fetchone()


def _validate_redirect_uri(client_row: dict, redirect_uri: str) -> bool:
    """
    Check that redirect_uri's path matches one of the client's allowed paths.
    Honors SCRIPT_NAME so deployments under a URL prefix still work.
    """

    raw = (client_row.get('oacl_redirect_uris') or '').replace('\r', '\n').replace(' ', '\n')
    allowed_paths = [p.strip() for p in raw.split('\n') if p.strip()]
    if not allowed_paths:
        return False

    # Extract path part from the candidate redirect_uri.
    u = urlparse(redirect_uri or '')
    req_path = u.path or '/'

    # Remove SCRIPT_NAME prefix when the app is mounted under a subpath.
    prefix = request.environ.get('SCRIPT_NAME', '')
    norm = req_path[len(prefix):] if prefix and req_path.startswith(prefix) else req_path

    # Accept either the normalized path or the raw path.
    ok = (norm in allowed_paths) or (req_path in allowed_paths)
    log.debug(Logs.fileline() + f" : OAUTH redirect-check path='{req_path}' norm='{norm}' ok={ok}")

    return ok


# ===== Authlib Glue (Client Adapter & Token Storage) =====

def query_client(client_id):
    """
    Load an OAuth client from DB and adapt it to Authlib's expected interface.
    Validates redirect URIs by path, honors configured grant/response types,
    and enforces the client's token auth method. Returns a lightweight
    object with the checks Authlib calls during authorization and token steps.
    """
    row = _load_client(client_id)
    if not row:
        return None

    # Debug only: count configured redirect URIs (avoid logging secrets/values).
    debug_uris = [p.strip() for p in (row.get('oacl_redirect_uris') or '').replace('\r', '\n').split('\n') if p.strip()]
    log.debug(Logs.fileline() + f" : OAUTH load-client id={client_id!r} allowed_uris_count={len(debug_uris)}")

    # Prefer environment-provided secret (shared with FE) over DB value
    env_secret = (os.environ.get('LABBOOK_OAUTH_FE_SECRET') or '').strip()

    class Client:
        # Static attributes read by Authlib
        client_id = row['oacl_client_id']
        client_name = row['oacl_client_name']
        token_endpoint_auth_method = row['oacl_token_endpoint_auth_method']
        grant_types = (row['oacl_grant_types'] or '').split()
        response_types = (row.get('oacl_response_types') or 'code').split()
        scope = row.get('oacl_scope') or ''
        redirect_uris = [p.strip() for p in (row['oacl_redirect_uris'] or '').replace('\r', '\n').split('\n') if p.strip()]
        # client_secret = row['oacl_client_secret'] or None
        # Priority: env secret > DB secret; never log this value.
        client_secret = None if row['oacl_token_endpoint_auth_method'] == 'none' else (env_secret or (row.get('oacl_client_secret') or None))

        def check_redirect_uri(self, redirect_uri):
            """Accept if the URI path matches one of the configured paths."""
            return _validate_redirect_uri(row, redirect_uri)

        def check_response_type(self, response_type):
            """Authorize only configured response types."""
            return response_type in self.response_types

        def check_grant_type(self, grant_type):
            """Authorize only configured grant types."""
            return grant_type in self.grant_types

        def check_client_secret(self, client_secret):
            """Simple equality; secret comes from env override or DB. Do not log."""
            return self.client_secret == client_secret

        def get_default_redirect_uri(self):
            """First configured URI acts as default."""
            return self.redirect_uris[0] if self.redirect_uris else None

        def check_token_endpoint_auth_method(self, method):
            """Exact match, defaulting to 'none' for public clients."""
            return method == (self.token_endpoint_auth_method or 'none')

        def check_endpoint_auth_method(self, method, endpoint):
            """Be explicit on /token, relaxed elsewhere to avoid surprises."""
            if endpoint != 'token':
                return True
            expected = (self.token_endpoint_auth_method or 'none')
            return method == expected

        def get_default_scope(self):
            """Scopes applied when request omits 'scope'."""
            return self.scope or ''

        def get_allowed_scope(self, scope):
            """Filter requested scopes against what's allowed in DB."""
            allowed = (self.scope or '').split()
            if not allowed:
                # If no restriction in DB, accept whatever was requested
                return scope or ''
            requested = (scope or '').split()
            effective = [s for s in requested if s in allowed]
            return ' '.join(effective)

    return Client()


def save_token(token, req):
    """
    Persist an issued OAuth token pair to DB.
    Stores access/refresh, scope, issued_at (epoch), and expires_in (seconds).
    Marks token as not revoked ('N') on insert.
    Note: do not log token values; treat as secrets.
    """
    cur = DB.cursor(ecr=True)
    cur.execute("""
        INSERT INTO oauth2_token
        (oato_client_id, oato_token_type, oato_access_token, oato_refresh_token,
         oato_scope, oato_revoked, oato_issued_at, oato_expires_in)
        VALUES (%s,%s,%s,%s,%s,'N',%s,%s)
    """, (
        req.client.client_id,
        token.get('token_type', 'Bearer'),
        token['access_token'],
        token.get('refresh_token'),
        token.get('scope', ''),
        int(time.time()),
        int(token.get('expires_in') or 3600)
    ))


# ===== Grant: Authorization Code (PKCE) =====

class AuthorizationCodeGrantPKCE(grants.AuthorizationCodeGrant):
    """
    Authorization Code grant with PKCE support.
    Accepts public clients ('none') and standard confidential methods.
    Mirrors Authlib's expectations while sourcing data from DB rows.
    """
    # Allow public PKCE client and the usual confidential methods
    TOKEN_ENDPOINT_AUTH_METHODS = ['none', 'client_secret_post', 'client_secret_basic']

    def get_expires_in(self, token, client):
        return int(current_app.config.get('OAUTH2_TOKEN_EXPIRES_IN', {}).get('authorization_code', 3600))

    class _CodeObj:
        """
        Lightweight wrapper around an authorization_code DB row.
        Provides the minimal interface Authlib calls during the token exchange.
        """
        def __init__(self, row):
            self.row = row or {}

        def get_redirect_uri(self):
            """Return the redirect URI saved with the code."""
            return self.row.get('oaco_redirect_uri') or ''

        def get_scope(self):
            """Space-delimited scopes associated with the code."""
            return self.row.get('oaco_scope') or ''

        def is_expired(self):
            """True when current time is past the stored expiry."""
            return int(time.time()) >= int(self.row.get('oaco_expires_at') or 0)

        @property
        def oaco_code(self):
            """Raw authorization code value."""
            return self.row.get('oaco_code')

        @property
        def oaco_code_challenge(self):
            """PKCE code_challenge as stored."""
            return self.row.get('oaco_code_challenge') or ''

        @property
        def oaco_code_challenge_method(self):
            """Stored PKCE method ('plain' or 'S256')."""
            return self.row.get('oaco_code_challenge_method') or ''

        @property
        def code_challenge(self):
            """Alias expected by Authlib."""
            return self.row.get('oaco_code_challenge') or ''

        @property
        def code_challenge_method(self):
            """Alias expected by Authlib."""
            return self.row.get('oaco_code_challenge_method') or ''

    def save_authorization_code(self, code, req):
        """
        Persist an authorization code with its redirect URI, scope, PKCE, and expiry.
        Scope priority: requested → client's default. Sets 10-minute lifetime.
        Returns the raw code value (Authlib expectation).
        """
        # Single source of truth for scope:
        # 1) use requested scope if provided
        # 2) else fallback to client's configured scope
        requested = (req.scope or '').strip()
        client_default = getattr(req.client, 'scope', '') or ''
        scope_to_save = requested if requested else client_default

        cur = DB.cursor(ecr=True)
        cur.execute("""
            INSERT INTO oauth2_code
            (oaco_code, oaco_client_id, oaco_redirect_uri, oaco_scope, oaco_auth_time,
             oaco_nonce, oaco_code_challenge, oaco_code_challenge_method, oaco_expires_at)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            code,
            req.client.client_id,
            req.payload.redirect_uri or '',
            scope_to_save,
            int(time.time()),
            req.payload.data.get('nonce', ''),
            req.payload.data.get('code_challenge', ''),
            req.payload.data.get('code_challenge_method', ''),
            int(time.time()) + 600
        ))
        return code

    def query_authorization_code(self, code, client):
        """
        Load a stored authorization code for the given client.
        Wrap the row into a _CodeObj compatible with Authlib calls.
        """
        cur = DB.cursor()
        cur.execute("""
            SELECT * FROM oauth2_code
            WHERE oaco_code=%s AND oaco_client_id=%s
            LIMIT 1
        """, (code, client.client_id))
        row = cur.fetchone()
        return self._CodeObj(row) if row else None

    def delete_authorization_code(self, code_obj):
        """
        One-time use: remove the consumed/invalid code from storage.
        No effect if code_obj is None.
        """
        if not code_obj:
            return
        cur = DB.cursor(ecr=True)
        cur.execute("DELETE FROM oauth2_code WHERE oaco_code=%s", (code_obj.oaco_code,))

    def authenticate_user(self, code_obj):
        """
        Provide the user principal for the token exchange.
        Here we map the session user_id into a minimal object with .id.
        """
        class U:
            pass
        u = U()
        u.id = session.get('user_id', 0)
        return u

    def validate_code_challenge(self, code_verifier, code_obj):
        """
        PKCE verification: recompute from verifier and compare to stored challenge.
        Supports 'plain' and 'S256' via CodeChallenge helper.
        """
        method = code_obj.oaco_code_challenge_method
        challenge = code_obj.oaco_code_challenge
        return CodeChallenge(method).verify(code_verifier, challenge)


def _auth_none(query_client, request):
    """
    Public-client auth: accept only clients explicitly configured with 'none'
    and without a stored secret. Returns the client object or None.
    """
    cid = (request.form.get('client_id') or '').strip()
    client = query_client(cid) if cid else None
    if not client:
        return None
    expected = getattr(client, 'token_endpoint_auth_method', None) or 'none'
    # Accept only truly public clients (no secret stored in DB)
    if expected == 'none' and not getattr(client, 'client_secret', None):
        return client
    return None


# ===== Grant: Client Credentials (M2M) with POST auth =====
class ClientCredentialsGrantPOST(grants.ClientCredentialsGrant):
    """
    Extend default client-credentials grant to accept both client_secret_basic and client_secret_post
    at the token endpoint.
    """
    TOKEN_ENDPOINT_AUTH_METHODS = ['client_secret_basic', 'client_secret_post']

    # Force token lifetime from Flask config (fallback 3600s)
    def get_expires_in(self, token, client):
        return int(current_app.config.get('OAUTH2_TOKEN_EXPIRES_IN', 3600))


# ===== Authorization Server Wiring =====

authorization = AuthorizationServer(
    query_client=query_client,
    save_token=save_token
)
# Enable Authorization Code with PKCE; PKCE is required.
authorization.register_grant(AuthorizationCodeGrantPKCE, [CodeChallenge(required=True)])
# Register the "no client secret" auth for public clients.
authorization.register_client_auth_method('none', _auth_none)
authorization.register_grant(ClientCredentialsGrantPOST)


# ===== Resource Protection =====

require_oauth = ResourceProtector()


# ===== Bearer Token Validator =====

class MyBearerTokenValidator(BearerTokenValidator):
    """
    DB-backed Bearer validator for ResourceProtector.
    Wraps DB rows so Authlib can query expiry, revocation, and scope.
    """

    # tiny wrapper so Authlib can call token.is_expired()
    class _Tok:
        """
        Minimal token view used by Authlib during validation.
        Delegates to row fields without exposing raw storage details.
        """
        def __init__(self, row):
            self._row = row or {}

        def get(self, key, default=None):
            """Dict-like access for optional fields."""
            return self._row.get(key, default)

        def is_expired(self):
            """True if now exceeds issued_at + expires_in."""
            now = int(time.time())
            issued = int(self._row.get('oato_issued_at') or 0)
            ttl = int(self._row.get('oato_expires_in') or 0)
            return now > (issued + ttl)

        def is_revoked(self):
            """True if token was explicitly revoked."""
            return (self._row.get('oato_revoked') == 'Y')

        def get_scope(self):
            """Space-delimited scopes of the token."""
            return self._row.get('oato_scope') or ''

    # Check if the token exists and is not expired
    def authenticate_token(self, token_string):
        """
        Look up a non-revoked access token and reject if expired.
        Returns a lightweight wrapper or None when invalid.
        Also populates request.oauth_user from BE session for audit trail.
        """
        cur = DB.cursor()
        cur.execute("""
            SELECT * FROM oauth2_token
            WHERE oato_access_token=%s AND oato_revoked='N'
            LIMIT 1
        """, (token_string,))
        tok = cur.fetchone()
        if not tok:
            return None

        now = int(time.time())
        if now > (tok['oato_issued_at'] + tok['oato_expires_in']):
            return None

        # Build audit user from BE session when available
        try:
            login = session.get('user_login') or ''
            display = session.get('user_display') or login
            role = session.get('user_role')
            user_id = session.get('user_id')

            request.oauth_user = {
                "usr_login": login,
                "usr_display": display,
                "usr_role": role,
                "usr_id": user_id,
            }
        except Exception:
            log.exception(Logs.fileline() + ' : MyBearerTokenValidator ERROR building oauth_user from session')
            request.oauth_user = {
                "usr_login": '',
                "usr_display": '',
                "usr_role": None,
                "usr_id": None,
            }

        return self._Tok(tok)

    def request_invalid(self, request):
        """
        Validate the HTTP request shape for OAuth checks.
        Return True to flag a malformed request; False otherwise.
        """
        return False

    def token_revoked(self, token):
        """
        True when the token was explicitly revoked in DB.
        """
        return token.is_revoked()

    def scope_insufficient(self, token_scope, required_scopes):
        """
        Enforce scope: return True if any required scope is missing.
        Accepts string or list for required_scopes.
        """
        if not required_scopes:
            return False

        # Normalize required scopes to a list of strings
        if isinstance(required_scopes, str):
            needed = [s for s in required_scopes.split() if s]
        else:
            needed = list(required_scopes)

        # Token scope string -> list
        token_scopes = [s for s in (token_scope or '').split() if s]

        # Return True if any required scope is missing
        missing = [s for s in needed if s not in token_scopes]
        return bool(missing)


# Register the validator with the resource protector.
require_oauth.register_token_validator(MyBearerTokenValidator())


# ========= ROUTES =========

@bp_oauth.route('/services/oauth/authorize', methods=['GET', 'POST'])
def oauth_authorize():
    """
    Authorization endpoint. Requires a BE user session.
    Delegates validation and response building to Authlib.
    If no session, stash current URL and return 401 so the FE can bounce.
    """
    if 'user_id' not in session:
        session['next'] = request.url
        session.modified = True
        return jsonify({'error': 'login_required', 'detail': 'User session required'}), 401

    client_id = request.args.get('client_id', '')
    state     = request.args.get('state', '')

    # Minimal entry logging for troubleshooting
    q = request.args
    cid = (q.get('client_id') or '').strip()
    ccm = (q.get('code_challenge_method') or '')
    has_user = 'user_id' in session
    log.debug(Logs.fileline() + f" : OAUTH /authorize enter session={has_user} client_id={cid!r} ccm={ccm!r}")

    # Minimal debug logging
    try:
        log.debug(Logs.fileline() + f" : OAUTH authorize args client_id={client_id!r} state_set={bool(state)}")
        row = _load_client(client_id) if client_id else None
        if row:
            log.debug(Logs.fileline() + " : OAUTH client has registered redirect URIs")
    except Exception:
        pass

    # Authlib handles response building (validations, state, etc.)
    return authorization.create_authorization_response(grant_user=type('U', (), {'id': session['user_id']}))


@bp_oauth.route('/services/oauth/token', methods=['POST'])
def oauth_token():
    """
    Token endpoint. Authlib performs the code → token exchange and PKCE checks.
    Logs a few booleans for diagnostics without leaking secrets.
    """
    # DEBUG logs
    auth_hdr = request.headers.get('Authorization', '')
    has_client_secret = 'client_secret' in request.form
    has_code = 'code' in request.form
    has_verifier = 'code_verifier' in request.form
    log.debug("OAUTH /token "
              f"auth_header={bool(auth_hdr)} client_id={request.form.get('client_id','')!r} "
              f"secret_present={has_client_secret} code_present={has_code} verifier_present={has_verifier}")

    resp = authorization.create_token_response()

    # remove browser basic auth popup
    resp.headers.pop('WWW-Authenticate', None)

    # Status-only log to keep noise low
    try:
        status = resp.status_code
        log.debug(f"OAUTH /token response_status={status}")
    except Exception:
        pass

    return resp


@bp_oauth.route('/services/confirm-access', methods=['POST'])
def confirm_access():
    """
    Bind the BE session to a user id so /authorize can grant.
    Also store minimal user identity in session for later audit use.
    Returns any paused /authorize URL from session for the FE to resume.
    """
    args = request.get_json() or {}
    id_user = args.get('id_user', None)
    if id_user is None:
        return jsonify({'error': 'id_user missing'}), 400

    try:
        id_user_int = int(id_user)
    except (TypeError, ValueError):
        return jsonify({'error': 'id_user invalid'}), 400

    # Store user id in session (used by /services/oauth/authorize)
    session['user_id'] = id_user_int

    # Store minimal user identity for audit
    try:
        user = User.getUserDetails(id_user_int)
    except Exception:
        log.exception(Logs.fileline() + ' : confirm_access ERROR getUserDetails')
        user = None

    if user:
        firstname = (user.get('firstname') or '').strip()
        lastname = (user.get('lastname') or '').strip()
        display = (firstname + ' ' + lastname).strip() or (user.get('username') or '')
        session['user_login'] = user.get('username') or ''
        session['user_display'] = display
        session['user_role'] = user.get('role_type')
    else:
        session['user_login'] = ''
        session['user_display'] = ''
        session['user_role'] = None

    session.modified = True

    # Only return the paused OAuth authorize URL if present
    redirect_url = session.pop('next', None)
    return jsonify({'redirect_url': redirect_url})
