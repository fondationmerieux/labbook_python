import logging
import os

from logging.handlers import WatchedFileHandler
from app import app


def prep_log(logger_nom, log_fich, niveau=logging.INFO):
    logger = logging.getLogger(logger_nom)
    formatter = logging.Formatter('%(asctime)s : %(message)s')
    fileHandler = WatchedFileHandler(log_fich)
    fileHandler.setFormatter(formatter)

    logger.setLevel(niveau)
    logger.addHandler(fileHandler)


prep_log('log_wsgi', '/home/apps/logs/log_wsgi.log')

log = logging.getLogger('log_wsgi')


# src = http://flask.pocoo.org/snippets/35/
class ReverseProxied(object):
    '''Wrap the application in this middleware and configure the
    front-end server to add these headers, to let you quietly bind
    this to a URL other than / and to an HTTP scheme that is
    different than what is used locally.

    In nginx:
    location /myprefix {
        proxy_pass http://192.168.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Scheme $scheme;
        proxy_set_header X-Script-Name /myprefix;
        }

    :param app: the WSGI application
    '''
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        if os.environ.get('LABBOOK_DEBUG'):
            log.info("LABBOOK_DEBUG __call__ environ=" + str(environ))
        script_name = environ.get('HTTP_X_SCRIPT_NAME', '')
        if script_name:
            environ['SCRIPT_NAME'] = script_name
            path_info = environ['PATH_INFO']
            if path_info.startswith(script_name):
                environ['PATH_INFO'] = path_info[len(script_name):]

        scheme = environ.get('HTTP_X_SCHEME', '')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)


app.wsgi_app = ReverseProxied(app.wsgi_app)
