# -*- coding:utf-8 -*-
import logging
import json

# from datetime import datetime, timedelta
from flask import request
from flask_restful import Resource

from app.models.General import compose_ret
from app.models.Constants import Constants
from app.models.Automation import Automation
from app.models.Logs import Logs
from app.models.Audit import Audit
from app.security.oauth_routes import require_oauth


# Names exported when this module is imported with "*" (see app/__init__.py).
# Without __all__, "import *" also brings in this module's own imports
# (Constants, datetime, logging...) and they leak into the caller.
__all__ = [
    'AutoJobList',
    'AutoJobDet',
    'AutoJobCreate',
    'AutoJobUpdate',
    'AutoJobDelete',
    'AutoRunList',
    'AutoJobRunNow',
]


class AutoJobList(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self):
        """
        List automation jobs with optional filters and pagination.
        Body (all optional):
        {
          "type": "dhis2|activity|billing",
          "active": "Y|N",
          "limit": 100,
          "offset": 0,
          "order_by": "ajb_next_run_at|ajb_created_at|ajb_updated_at|ajb_label|ajb_type",
          "order_dir": "asc|desc"
        }
        """
        audit_user = request.oauth_user
        body = request.get_json(silent=True) or {}
        job_type = body.get('type')
        is_active = body.get('active')
        try:
            limit = max(1, min(int(body.get('limit', 100)), 500))
            offset = max(0, int(body.get('offset', 0)))
        except Exception:
            try:
                details = {"result": "ERROR", "reason": "INVALID_PAGINATION", "payload": body}
                Audit.insertAudit(audit_user, "AutoJobList", "AUTOMATION", None, "ERROR", details, "R")
            except Exception as err:
                self.log.error(Logs.fileline() + ' : AutoJobList ERROR audit invalid pagination err=' + str(err))
            return compose_ret('', Constants.cst_content_type_json, 400)
        order_by = body.get('order_by', 'ajb_next_run_at')
        order_dir = body.get('order_dir', 'asc')

        try:
            jobs = Automation.getAutomationJobs(
                job_type=job_type,
                is_active=is_active,
                limit=limit,
                offset=offset,
                order_by=order_by,
                order_dir=order_dir
            )

            if jobs:
                jobs = [j for j in jobs if (j.get('ajb_type') or '').lower() != 'system']

            try:
                details = {"result": "SUCCESS", "type": job_type, "active": is_active, "limit": limit, "offset": offset,
                           "order_by": order_by, "order_dir": order_dir, "count": len(jobs) if jobs else 0}
                Audit.insertAudit(audit_user, "AutoJobList", "AUTOMATION", None, "SUCCESS", details, "R")
            except Exception as err:
                self.log.error(Logs.fileline() + ' : AutoJobList ERROR audit success err=' + str(err))
            return compose_ret(json.dumps(jobs, default=str), Constants.cst_content_type_json)
        except Exception as err:
            self.log.error(Logs.fileline() + ' : AutoJobList failed, err=%s', err)
            try:
                details = {"result": "ERROR", "reason": "EXCEPTION", "error": str(err), "payload": body}
                Audit.insertAudit(audit_user, "AutoJobList", "AUTOMATION", None, "ERROR", details, "R")
            except Exception as err2:
                self.log.error(Logs.fileline() + ' : AutoJobList ERROR audit exception err=' + str(err2))
            return compose_ret('', Constants.cst_content_type_json, 500)


class AutoJobDet(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self, ajb_ser: int):
        """Get a single automation job by id."""
        audit_user = request.oauth_user
        try:
            job = Automation.getAutomationJob(ajb_ser=ajb_ser)
            if not job:
                try:
                    details = {"result": "NOT_FOUND", "ajb_ser": ajb_ser}
                    Audit.insertAudit(audit_user, "AutoJobDet", "AUTOMATION", ajb_ser, "ERROR", details, "R")
                except Exception as err:
                    self.log.error(Logs.fileline() + ' : AutoJobDet ERROR audit not found err=' + str(err))
                return compose_ret('', Constants.cst_content_type_json, 404)

            try:
                details = {"result": "SUCCESS", "ajb_ser": ajb_ser}
                Audit.insertAudit(audit_user, "AutoJobDet", "AUTOMATION", ajb_ser, "SUCCESS", details, "R")
            except Exception as err:
                self.log.error(Logs.fileline() + ' : AutoJobDet ERROR audit success err=' + str(err))
            return compose_ret(json.dumps(job, default=str), Constants.cst_content_type_json)
        except Exception as err:
            self.log.error(Logs.fileline() + ' : AutoJobDet failed, err=%s', err)
            try:
                details = {"result": "ERROR", "reason": "EXCEPTION", "ajb_ser": ajb_ser, "error": str(err)}
                Audit.insertAudit(audit_user, "AutoJobDet", "AUTOMATION", ajb_ser, "ERROR", details, "R")
            except Exception as err2:
                self.log.error(Logs.fileline() + ' : AutoJobDet ERROR audit exception err=' + str(err2))
            return compose_ret('', Constants.cst_content_type_json, 500)


class AutoJobCreate(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self):
        """
        Create an automation job.
        Required minimal fields in body:
          type, label, schedule.kind
        Returns the new job id as a raw scalar in the response body (200).
        """
        audit_user = request.oauth_user
        body = request.get_json(silent=False) or {}
        try:
            new_id = Automation.createAutomationJob(payload=body)

            try:
                details = {"result": "SUCCESS", "ajb_ser": new_id}
                Audit.insertAudit(audit_user, "AutoJobCreate", "AUTOMATION", new_id, "SUCCESS", details, "C")
            except Exception as err:
                self.log.error(Logs.fileline() + ' : AutoJobCreate ERROR audit success err=' + str(err))
            return compose_ret(str(new_id), Constants.cst_content_type_json)
        except ValueError as verr:
            self.log.warning(Logs.fileline() + ' : AutoJobCreate validation=%s', verr)
            try:
                details = {"result": "ERROR", "reason": "VALIDATION", "error": str(verr)}
                Audit.insertAudit(audit_user, "AutoJobCreate", "AUTOMATION", None, "ERROR", details, "C")
            except Exception as err:
                self.log.error(Logs.fileline() + ' : AutoJobCreate ERROR audit validation err=' + str(err))
            return compose_ret('', Constants.cst_content_type_json, 400)
        except Exception as err:
            self.log.error(Logs.fileline() + ' : AutoJobCreate failed, err=%s', err)
            try:
                details = {"result": "ERROR", "reason": "EXCEPTION", "error": str(err)}
                Audit.insertAudit(audit_user, "AutoJobCreate", "AUTOMATION", None, "ERROR", details, "C")
            except Exception as err2:
                self.log.error(Logs.fileline() + ' : AutoJobCreate ERROR audit exception err=' + str(err2))
            return compose_ret('', Constants.cst_content_type_json, 500)


class AutoJobUpdate(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def put(self, ajb_ser: int):
        """
        Update an automation job. Only provided fields are applied.
        Body shape is identical to create(), all fields optional.
        """
        audit_user = request.oauth_user
        body = request.get_json(silent=False) or {}
        try:
            updated = Automation.updateAutomationJob(ajb_ser=ajb_ser, payload=body)
            if not updated:
                try:
                    details = {"result": "ERROR", "reason": "UPDATE_FAILED", "ajb_ser": ajb_ser}
                    Audit.insertAudit(audit_user, "AutoJobUpdate", "AUTOMATION", ajb_ser, "ERROR", details, "U")
                except Exception as err:
                    self.log.error(Logs.fileline() + ' : AutoJobUpdate ERROR audit update failed err=' + str(err))
                return compose_ret('', Constants.cst_content_type_json, 500)

            try:
                details = {"result": "SUCCESS", "ajb_ser": ajb_ser}
                Audit.insertAudit(audit_user, "AutoJobUpdate", "AUTOMATION", ajb_ser, "SUCCESS", details, "U")
            except Exception as err:
                self.log.error(Logs.fileline() + ' : AutoJobUpdate ERROR audit success err=' + str(err))
            return compose_ret('', Constants.cst_content_type_json)
        except ValueError as verr:
            self.log.warning(Logs.fileline() + ' : AutoJobUpdate validation=%s', verr)
            try:
                details = {"result": "ERROR", "reason": "VALIDATION", "ajb_ser": ajb_ser, "error": str(verr)}
                Audit.insertAudit(audit_user, "AutoJobUpdate", "AUTOMATION", ajb_ser, "ERROR", details, "U")
            except Exception as err:
                self.log.error(Logs.fileline() + ' : AutoJobUpdate ERROR audit validation err=' + str(err))
            return compose_ret('', Constants.cst_content_type_json, 400)
        except Exception as err:
            self.log.error(Logs.fileline() + ' : AutoJobUpdate failed, err=%s', err)
            try:
                details = {"result": "ERROR", "reason": "EXCEPTION", "ajb_ser": ajb_ser, "error": str(err)}
                Audit.insertAudit(audit_user, "AutoJobUpdate", "AUTOMATION", ajb_ser, "ERROR", details, "U")
            except Exception as err2:
                self.log.error(Logs.fileline() + ' : AutoJobUpdate ERROR audit exception err=' + str(err2))
            return compose_ret('', Constants.cst_content_type_json, 500)


class AutoJobDelete(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def delete(self, ajb_ser: int):
        """Delete an automation job by id."""
        audit_user = request.oauth_user

        job = Automation.getAutomationJob(ajb_ser=ajb_ser)
        if job:
            params = job.get('ajb_params') or {}
            if (job.get('ajb_type') or '').lower() == 'system' and (params.get('type') or '').lower() == 'ssh':
                return compose_ret('', Constants.cst_content_type_json, 403)

        try:
            deleted = Automation.deleteAutomationJob(ajb_ser=ajb_ser)
            if not deleted:
                try:
                    details = {"result": "NOT_FOUND", "ajb_ser": ajb_ser}
                    Audit.insertAudit(audit_user, "AutoJobDelete", "AUTOMATION", ajb_ser, "ERROR", details, "D")
                except Exception as err:
                    self.log.error(Logs.fileline() + ' : AutoJobDelete ERROR audit not found err=' + str(err))
                return compose_ret('', Constants.cst_content_type_json, 404)

            try:
                details = {"result": "SUCCESS", "ajb_ser": ajb_ser}
                Audit.insertAudit(audit_user, "AutoJobDelete", "AUTOMATION", ajb_ser, "SUCCESS", details, "D")
            except Exception as err:
                self.log.error(Logs.fileline() + ' : AutoJobDelete ERROR audit success err=' + str(err))
            return compose_ret('', Constants.cst_content_type_json)
        except Exception as err:
            self.log.error(Logs.fileline() + ' : AutoJobDelete failed, err=%s', err)
            try:
                details = {"result": "ERROR", "reason": "EXCEPTION", "ajb_ser": ajb_ser, "error": str(err)}
                Audit.insertAudit(audit_user, "AutoJobDelete", "AUTOMATION", ajb_ser, "ERROR", details, "D")
            except Exception as err2:
                self.log.error(Logs.fileline() + ' : AutoJobDelete ERROR audit exception err=' + str(err2))
            return compose_ret('', Constants.cst_content_type_json, 500)


class AutoRunList(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self):
        """
        List execution history (automation_run).
        Body (all optional):
        {
          "job_id": 123,
          "status": "running|success|error|timeout",
          "from": "YYYY-MM-DD",
          "to": "YYYY-MM-DD",
          "limit": 100,
          "offset": 0
        }
        """
        audit_user = request.oauth_user
        body = request.get_json(silent=True) or {}
        job_id = body.get('job_id')
        status = body.get('status')
        date_from = body.get('from')
        date_to = body.get('to')
        try:
            limit = max(1, min(int(body.get('limit', 100)), 500))
            offset = max(0, int(body.get('offset', 0)))
        except Exception:
            try:
                details = {"result": "ERROR", "reason": "INVALID_PAGINATION", "payload": body}
                Audit.insertAudit(audit_user, "AutoRunList", "AUTOMATION_RUN", None, "ERROR", details, "R")
            except Exception as err:
                self.log.error(Logs.fileline() + ' : AutoRunList ERROR audit invalid pagination err=' + str(err))
            return compose_ret('', Constants.cst_content_type_json, 400)

        try:
            runs = Automation.getAutomationRuns(
                job_id=job_id,
                status=status,
                date_from=date_from,
                date_to=date_to,
                limit=limit,
                offset=offset
            )

            try:
                details = {"result": "SUCCESS", "job_id": job_id, "status": status, "from": date_from, "to": date_to,
                           "limit": limit, "offset": offset, "count": len(runs) if runs else 0}
                Audit.insertAudit(audit_user, "AutoRunList", "AUTOMATION_RUN", None, "SUCCESS", details, "R")
            except Exception as err:
                self.log.error(Logs.fileline() + ' : AutoRunList ERROR audit success err=' + str(err))

            return compose_ret(json.dumps(runs, default=str), Constants.cst_content_type_json)
        except Exception as err:
            self.log.error(Logs.fileline() + ' : AutoRunList failed, err=%s', err)
            try:
                details = {"result": "ERROR", "reason": "EXCEPTION", "error": str(err), "payload": body}
                Audit.insertAudit(audit_user, "AutoRunList", "AUTOMATION_RUN", None, "ERROR", details, "R")
            except Exception as err2:
                self.log.error(Logs.fileline() + ' : AutoRunList ERROR audit exception err=' + str(err2))
            return compose_ret('', Constants.cst_content_type_json, 500)


class AutoJobRunNow(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self, ajb_ser: int):
        """
        Force immediate execution by setting next_run_at to NOW().
        Optional body:
        {
          "message": "triggered from UI"
        }
        """
        audit_user = request.oauth_user
        body = request.get_json(silent=True) or {}
        trigger_message = body.get('message', '')

        try:
            forced = Automation.forceAutomationRunNow(ajb_ser=ajb_ser, message=trigger_message)
            if not forced:
                try:
                    details = {"result": "NOT_FOUND", "ajb_ser": ajb_ser, "message": trigger_message}
                    Audit.insertAudit(audit_user, "AutoJobRunNow", "AUTOMATION", ajb_ser, "ERROR", details, "U")
                except Exception as err:
                    self.log.error(Logs.fileline() + ' : AutoJobRunNow ERROR audit not found err=' + str(err))
                return compose_ret('', Constants.cst_content_type_json, 404)

            try:
                details = {"result": "SUCCESS", "ajb_ser": ajb_ser, "message": trigger_message}
                Audit.insertAudit(audit_user, "AutoJobRunNow", "AUTOMATION", ajb_ser, "SUCCESS", details, "U")
            except Exception as err:
                self.log.error(Logs.fileline() + ' : AutoJobRunNow ERROR audit success err=' + str(err))
            return compose_ret('', Constants.cst_content_type_json)
        except Exception as err:
            self.log.error(Logs.fileline() + ' : AutoJobRunNow failed, err=%s', err)
            try:
                details = {"result": "ERROR", "reason": "EXCEPTION", "ajb_ser": ajb_ser, "error": str(err),
                           "message": trigger_message}
                Audit.insertAudit(audit_user, "AutoJobRunNow", "AUTOMATION", ajb_ser, "ERROR", details, "U")
            except Exception as err2:
                self.log.error(Logs.fileline() + ' : AutoJobRunNow ERROR audit exception err=' + str(err2))
            return compose_ret('', Constants.cst_content_type_json, 500)
