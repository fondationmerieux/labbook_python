# -*- coding:utf-8 -*-
import json

from app.models.Constants import *
from datetime import datetime
from flask import make_response


def compose_ret(ret, type=Constants.cst_content_type_plain, http_code=200, ensure_ascii=True):
    if type == Constants.cst_content_type_json:
        resp = make_response(json.dumps(ret, ensure_ascii=ensure_ascii, default=safe_json_default), http_code)
    else:
        resp = make_response(ret, http_code)

    # Correct definition of the Content-Type according to the requested type
    if type == Constants.cst_content_type_json:
        resp.headers['Content-type'] = 'application/json; charset=utf-8'
    elif type == Constants.cst_content_type_hl7:
        resp.headers['Content-type'] = 'application/hl7-v2'
    else:
        resp.headers['Content-type'] = 'text/plain; charset=utf-8'

    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


def compose_ret_ascii(ret, http_code=200):
    resp = make_response(json.dumps(ret, ensure_ascii=False, default=safe_json_default), http_code)

    resp.headers['Content-type'] = 'application/json; charset=utf-8'

    return resp


def safe_json_default(obj):
    from decimal import Decimal
    from datetime import date, datetime
    import base64

    if isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, (datetime, date)):
        return obj.isoformat()
    elif isinstance(obj, bytes):
        try:
            return obj.decode("utf-8")
        except UnicodeDecodeError:
            return base64.b64encode(obj).decode("ascii")
    return str(obj)


def parse_date_safe(date_str):
    formats = [
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d"
    ]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"Unsupported date format: {date_str}")
