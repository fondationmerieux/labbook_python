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
        List automation jobs with optional filters and pagination, system jobs left out.

        Body (all optional):
            type (str): 'dhis2', 'activity' or 'billing'.
            active (str): 'Y' or 'N'.
            limit (int): 100 by default, 500 at most.
            offset (int): 0 by default.
            order_by (str): ajb_next_run_at (default), ajb_created_at, ajb_updated_at, ajb_label or ajb_type.
            order_dir (str): 'asc' (default) or 'desc'.

        Returns:
            200: list of jobs.
            400: limit or offset is not a number.
            500: database read failed.
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
        """
        Get a single automation job by id.

        Args:
            ajb_ser (int): job id.

        Returns:
            200: job fields.
            404: job not found.
            500: database read failed.
        """
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

        Body:
            type (str): 'dhis2', 'activity', 'billing' or 'system'.
            label (str): job name.
            schedule (dict): kind among H, D, W, M, B, T, Q, S, A (D refused for dhis2),
                             time 02:00:00 by default.
            params (dict, optional): job settings.
            active (str, optional): 'Y' (default) or 'N'.

        Returns:
            200: new job id as a raw scalar.
            400: type, label or schedule kind invalid.
            403: type 'system', those jobs come from Alembic only.
            500: insertion failed.
        """
        audit_user = request.oauth_user
        body = request.get_json(silent=False) or {}

        # system jobs (NTP, audit purge) come from Alembic only: one of them runs a shell command
        if (body.get('type') or '').strip().lower() == 'system':
            self.log.error(Logs.fileline() + ' : AutoJobCreate ERROR system job refused')
            try:
                details = {"result": "ERROR", "reason": "SYSTEM_JOB_FORBIDDEN"}
                Audit.insertAudit(audit_user, "AutoJobCreate", "AUTOMATION", None, "ERROR", details, "C")
            except Exception as err:
                self.log.error(Logs.fileline() + ' : AutoJobCreate ERROR audit system job err=' + str(err))
            return compose_ret('', Constants.cst_content_type_json, 403)

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
        Update an automation job, only the fields provided are applied.

        Args:
            ajb_ser (int): job id.

        Body:
            Same fields as AutoJobCreate, all optional. The next run is recomputed when the schedule changes.

        Returns:
            200: empty body.
            400: type or schedule kind invalid.
            403: system job, or type 'system' asked, those jobs come from Alembic only.
            500: job not found or update failed.
        """
        audit_user = request.oauth_user
        body = request.get_json(silent=False) or {}

        # system jobs (NTP, audit purge) come from Alembic only: one of them runs a shell command
        job = Automation.getAutomationJob(ajb_ser=ajb_ser)
        if (body.get('type') or '').strip().lower() == 'system' or \
           (job and (job.get('ajb_type') or '').lower() == 'system'):
            self.log.error(Logs.fileline() + ' : AutoJobUpdate ERROR system job refused ajb_ser=' + str(ajb_ser))
            try:
                details = {"result": "ERROR", "reason": "SYSTEM_JOB_FORBIDDEN", "ajb_ser": ajb_ser}
                Audit.insertAudit(audit_user, "AutoJobUpdate", "AUTOMATION", ajb_ser, "ERROR", details, "U")
            except Exception as err:
                self.log.error(Logs.fileline() + ' : AutoJobUpdate ERROR audit system job err=' + str(err))
            return compose_ret('', Constants.cst_content_type_json, 403)

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
        """
        Delete an automation job by id, system SSH jobs cannot be deleted.

        Args:
            ajb_ser (int): job id.

        Returns:
            200: empty body.
            403: system SSH job.
            404: job not found.
            500: deletion failed.
        """
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
            job_id (int): job id.
            status (str): 'running', 'success', 'error' or 'timeout'.
            from (str): first day, YYYY-MM-DD.
            to (str): last day, YYYY-MM-DD.
            limit (int): 100 by default, 500 at most.
            offset (int): 0 by default.

        Returns:
            200: list of runs.
            400: limit or offset is not a number.
            500: database read failed.
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

        Args:
            ajb_ser (int): job id.

        Body (optional):
            message (str): reason kept in the audit trail only, 'triggered from UI' for instance.

        Returns:
            200: empty body.
            404: job not found.
            500: update failed.
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
