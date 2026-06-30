# -*- coding:utf-8 -*-
import json
import logging
import calendar
import re
import csv
import os
import shutil
import hashlib

from pathlib import Path
from datetime import datetime, date, time, timedelta, timezone
from io import StringIO

from app.models.Constants import Constants
from app.models.DB import DB
from app.models.Audit import Audit
from app.models.Export import Export
from app.models.Setting import Setting
from app.models.Pdf import Pdf
from app.models.User import User
from app.models.Report import Report
from app.models.Logs import Logs
from app.models.Various import Various

# map schedule kind to month span
SPAN_BY_KIND = {'M': 1, 'B': 2, 'T': 3, 'Q': 4, 'S': 6, 'A': 12}
SAFE = Constants.cst_safe_pattern


class Automation:
    log = logging.getLogger('log_services')

    # ---------------------------
    # Automation JOBS
    # ---------------------------
    @staticmethod
    def getAutomationJobs(job_type=None, is_active=None, limit=100, offset=0, order_by='ajb_next_run_at', order_dir='asc'):
        cursor = DB.cursor()

        valid_order_by = {
            'ajb_next_run_at',
            'ajb_created_at',
            'ajb_updated_at',
            'ajb_label',
            'ajb_type'
        }
        valid_order_dir = {'asc', 'desc'}

        order_by_sql = order_by if order_by in valid_order_by else 'ajb_next_run_at'
        order_dir_sql = order_dir.lower() if order_dir and order_dir.lower() in valid_order_dir else 'asc'

        req = (
            'select '
            '  ajb_ser, ajb_type, ajb_label, ajb_is_active, '
            '  ajb_schedule_kind, ajb_schedule_time, ajb_schedule_dow, '
            '  ajb_schedule_dom, ajb_schedule_last_dom, ajb_schedule_anchor_jan, '
            '  ajb_fire_on, ajb_schedule_start_on, ajb_next_run_at, ajb_last_run_at, '
            '  ajb_last_status, ajb_params, ajb_created_at, ajb_updated_at '
            'from automation_job '
            'where 1=1 '
        )
        params = []

        if job_type:
            req += ' and ajb_type = %s'
            params.append(job_type)

        if is_active in ('Y', 'N'):
            req += ' and ajb_is_active = %s'
            params.append(is_active)

        req += f' order by {order_by_sql} {order_dir_sql} limit %s offset %s'
        params.extend([int(limit), int(offset)])

        cursor.execute(req, tuple(params))
        rows = cursor.fetchall() or []

        for row in rows:
            if 'ajb_params' in row and isinstance(row['ajb_params'], str):
                try:
                    row['ajb_params'] = json.loads(row['ajb_params'])
                except Exception:
                    Automation.log.exception(Logs.fileline() + " : getAutomationJobs json decode failed ajb_ser=" + str(row.get('ajb_ser')))

        return rows

    @staticmethod
    def getAutomationJob(ajb_ser: int):
        cursor = DB.cursor()

        req = (
            'select '
            '  ajb_ser, ajb_type, ajb_label, ajb_is_active, '
            '  ajb_schedule_kind, ajb_schedule_time, ajb_schedule_dow, '
            '  ajb_schedule_dom, ajb_schedule_last_dom, ajb_schedule_anchor_jan, '
            '  ajb_fire_on, ajb_schedule_start_on, ajb_next_run_at, ajb_last_run_at, '
            '  ajb_last_status, ajb_params, ajb_created_at, ajb_updated_at '
            'from automation_job '
            'where ajb_ser = %s'
        )

        cursor.execute(req, (ajb_ser,))
        row = cursor.fetchone()
        if not row:
            return None

        if 'ajb_params' in row and isinstance(row['ajb_params'], str):
            try:
                row['ajb_params'] = json.loads(row['ajb_params'])
            except Exception:
                Automation.log.exception(Logs.fileline() + " : getAutomationJob json decode failed ajb_ser=" + str(row.get('ajb_ser')))

        params = row.get('ajb_params') or {}

        recipient_keys = [
            'dhis2_internal_recipient',
            'activity_internal_recipient',
            'billing_internal_recipient',
            'system_internal_recipient',
        ]

        id_list = []
        key_to_id = {}
        for key in recipient_keys:
            raw_val = params.get(key)
            if raw_val is None or raw_val == '':
                continue
            try:
                recipient_id = int(raw_val)
                if recipient_id > 0:
                    key_to_id[key] = recipient_id
                    id_list.append(recipient_id)
            except (TypeError, ValueError):
                continue

        if id_list:
            placeholders = ','.join(['%s'] * len(id_list))
            try:
                req = (
                    "select id_data, firstname, lastname, username "
                    f"from sigl_user_data where id_data in ({placeholders})"
                )
                cursor.execute(req, tuple(id_list))
                users = cursor.fetchall() or []
            except Exception:
                users = []

            user_label = {}
            for user in users:
                first = (user.get('firstname') or '').strip()
                last = (user.get('lastname') or '').strip()
                label = (first + ' ' + last).strip()
                if not label:
                    label = (user.get('username') or '').strip()
                user_label[user.get('id_data')] = label

            for key, recipient_id in key_to_id.items():
                params[f"{key}_label"] = user_label.get(recipient_id, str(recipient_id))

            row['ajb_params'] = params

        return row

    @staticmethod
    def createAutomationJob(payload: dict) -> int:
        """
        Insert new automation_job row.
        Required:
          payload.type in ('dhis2','activity','billing','system')
          payload.label non-empty
          payload.schedule.kind in ('H', 'D','W','M','B','T','Q','S','A')
        """
        job_type = (payload.get('type') or '').strip()
        label = (payload.get('label') or '').strip()
        schedule = payload.get('schedule') or {}
        params_obj = payload.get('params') or {}
        is_active = (payload.get('active') or 'Y').upper()

        if job_type not in ('dhis2', 'activity', 'billing', 'system'):
            raise ValueError('invalid job type')
        if not label:
            raise ValueError('missing label')

        schedule_kind = (schedule.get('kind') or '').upper()
        if schedule_kind not in ('H', 'D', 'W', 'M', 'B', 'T', 'Q', 'S', 'A'):
            raise ValueError('invalid schedule kind')

        # DHIS2 does not support daily schedule
        if job_type == 'dhis2' and schedule_kind == 'D':
            raise ValueError('daily not allowed for dhis2')

        schedule_time = schedule.get('time') or '02:00:00'
        if len(schedule_time) == 5:
            schedule_time += ':00'

        schedule_dow = schedule.get('dow')            # int or None
        schedule_dom = schedule.get('dom')            # int or None
        schedule_last_dom = (schedule.get('last_dom') or 'N').upper()
        schedule_anchor_jan = (schedule.get('anchor_jan') or 'Y').upper()

        if schedule_kind == 'H':
            schedule_dow = None
            schedule_dom = None
            schedule_last_dom = 'N'
            schedule_anchor_jan = 'Y'

        fire_on = (schedule.get('fire_on') or 'period_end')
        if fire_on not in ('period_start', 'period_end'):
            fire_on = 'period_end'

        schedule_start_on = schedule.get('start_on')  # 'YYYY-MM-DD' or None

        next_run_dt = compute_next_run_at(
            kind=schedule_kind,
            time_str=schedule_time,
            schedule_dow=schedule_dow,
            schedule_dom=schedule_dom,
            schedule_last_dom=schedule_last_dom,
            anchor_jan=schedule_anchor_jan,
            start_on=schedule_start_on
        )

        cursor = DB.cursor()

        req = (
            'insert into automation_job ('
            '  ajb_type, ajb_label, ajb_is_active, '
            '  ajb_schedule_kind, ajb_schedule_time, ajb_schedule_dow, '
            '  ajb_schedule_dom, ajb_schedule_last_dom, ajb_schedule_anchor_jan, '
            '  ajb_fire_on, ajb_schedule_start_on, ajb_next_run_at, '
            '  ajb_last_run_at, ajb_last_status, ajb_params'
            ') values ('
            '  %s, %s, %s, '
            '  %s, %s, %s, '
            '  %s, %s, %s, '
            '  %s, %s, %s, '
            '  NULL, %s, %s'
            ')'
        )

        params = [
            job_type,
            label,
            ('Y' if is_active == 'Y' else 'N'),
            schedule_kind,
            schedule_time,
            schedule_dow,
            schedule_dom,
            schedule_last_dom,
            schedule_anchor_jan,
            fire_on,
            schedule_start_on,
            next_run_dt.strftime('%Y-%m-%d %H:%M:%S'),
            'never',
            json.dumps(params_obj, ensure_ascii=False)
        ]

        try:
            cursor.execute(req, tuple(params))
            new_id = cursor.lastrowid
        except Exception:
            Automation.log.exception(Logs.fileline() + ' : createAutomationJob SQL')
            return 0

        return new_id or 0

    @staticmethod
    def updateAutomationJob(ajb_ser: int, payload: dict) -> bool:
        """
        Update only fields present in payload.
        Recompute ajb_next_run_at if any schedule field changes.
        """
        if not ajb_ser:
            return False

        current = Automation.getAutomationJob(ajb_ser)
        if not current:
            return False

        set_clauses = []
        values = []

        if 'type' in payload:
            job_type = (payload.get('type') or '').strip()
            if job_type not in ('dhis2', 'activity', 'billing', 'system'):
                raise ValueError('invalid job type')
            set_clauses.append('ajb_type = %s')
            values.append(job_type)

        if 'label' in payload:
            set_clauses.append('ajb_label = %s')
            values.append((payload.get('label') or '').strip())

        if 'active' in payload:
            active_flag = 'Y' if (payload.get('active') or '').upper() == 'Y' else 'N'
            set_clauses.append('ajb_is_active = %s')
            values.append(active_flag)

        schedule = payload.get('schedule')
        schedule_changed = False

        effective_kind = current['ajb_schedule_kind']
        effective_time = current['ajb_schedule_time']
        effective_dow = current['ajb_schedule_dow']
        effective_dom = current['ajb_schedule_dom']
        effective_last_dom = current['ajb_schedule_last_dom']
        effective_anchor_jan = current['ajb_schedule_anchor_jan']
        effective_start_on = current['ajb_schedule_start_on'].strftime('%Y-%m-%d') if current['ajb_schedule_start_on'] else None

        if schedule is not None:
            if 'kind' in schedule:
                new_kind = (schedule.get('kind') or '').upper()
                if new_kind not in ('H', 'D', 'W', 'M', 'B', 'T', 'Q', 'S', 'A'):
                    raise ValueError('invalid schedule kind')
                set_clauses.append('ajb_schedule_kind = %s')
                values.append(new_kind)
                effective_kind = new_kind
                schedule_changed = True

                if new_kind == 'H':
                    set_clauses.append('ajb_schedule_dow = %s')
                    values.append(None)
                    effective_dow = None

                    set_clauses.append('ajb_schedule_dom = %s')
                    values.append(None)
                    effective_dom = None

                    set_clauses.append('ajb_schedule_last_dom = %s')
                    values.append('N')
                    effective_last_dom = 'N'

                    set_clauses.append('ajb_schedule_anchor_jan = %s')
                    values.append('Y')
                    effective_anchor_jan = 'Y'

            if 'time' in schedule:
                new_time = schedule.get('time') or '02:00:00'
                if len(new_time) == 5:
                    new_time += ':00'
                set_clauses.append('ajb_schedule_time = %s')
                values.append(new_time)
                effective_time = new_time
                schedule_changed = True

            if 'dow' in schedule:
                set_clauses.append('ajb_schedule_dow = %s')
                values.append(schedule.get('dow'))
                effective_dow = schedule.get('dow')
                schedule_changed = True

            if 'dom' in schedule:
                set_clauses.append('ajb_schedule_dom = %s')
                values.append(schedule.get('dom'))
                effective_dom = schedule.get('dom')
                schedule_changed = True

            if 'last_dom' in schedule:
                new_last_dom = (schedule.get('last_dom') or 'N').upper()
                set_clauses.append('ajb_schedule_last_dom = %s')
                values.append(new_last_dom)
                effective_last_dom = new_last_dom
                schedule_changed = True

            if 'anchor_jan' in schedule:
                new_anchor = (schedule.get('anchor_jan') or 'Y').upper()
                set_clauses.append('ajb_schedule_anchor_jan = %s')
                values.append(new_anchor)
                effective_anchor_jan = new_anchor
                schedule_changed = True

            if 'start_on' in schedule:
                set_clauses.append('ajb_schedule_start_on = %s')
                values.append(schedule.get('start_on'))
                effective_start_on = schedule.get('start_on')
                schedule_changed = True

            if 'fire_on' in schedule:
                new_fire = schedule.get('fire_on')
                if new_fire not in ('period_start', 'period_end'):
                    new_fire = 'period_end'
                set_clauses.append('ajb_fire_on = %s')
                values.append(new_fire)

        if schedule_changed:
            next_run_dt = compute_next_run_at(
                kind=effective_kind,
                time_str=effective_time,
                schedule_dow=effective_dow,
                schedule_dom=effective_dom,
                schedule_last_dom=effective_last_dom,
                anchor_jan=effective_anchor_jan,
                start_on=effective_start_on
            )
            set_clauses.append('ajb_next_run_at = %s')
            values.append(next_run_dt.strftime('%Y-%m-%d %H:%M:%S'))

        # Handle params (JSON) if provided
        if 'params' in payload:
            params_obj = payload.get('params') or {}

            # Determine effective job type (payload override or current)
            effective_type = (payload.get('type') or current.get('ajb_type') or '').strip()

            # Safety rule for DHIS2 send mode: no internal messaging
            if effective_type == 'dhis2':
                mode = (params_obj.get('dhis2_mode') or '').lower()
                if mode == 'send':
                    # Force internal messaging off in send mode
                    params_obj['dhis2_internal_msg'] = 'N'
                    params_obj['dhis2_internal_recipient'] = None

            set_clauses.append('ajb_params = %s')
            values.append(json.dumps(params_obj, ensure_ascii=False))

        if not set_clauses:
            return True

        set_sql = ', '.join(set_clauses)
        req = f'update automation_job set {set_sql} where ajb_ser = %s'
        values.append(ajb_ser)

        cursor = DB.cursor()
        try:
            cursor.execute(req, tuple(values))
            return True
        except Exception:
            Automation.log.exception(Logs.fileline() + ' : updateAutomationJob SQL')
            return False

    @staticmethod
    def deleteAutomationJob(ajb_ser: int) -> bool:
        cursor = DB.cursor()
        try:
            req = 'delete from automation_job where ajb_ser = %s'
            cursor.execute(req, (ajb_ser,))
            return cursor.rowcount > 0
        except Exception:
            Automation.log.exception(Logs.fileline() + ' : deleteAutomationJob SQL')
            return False

    # ---------------------------
    # Automation RUNS (history)
    # ---------------------------
    @staticmethod
    def getAutomationRuns(job_id=None,
                          status=None,
                          date_from=None,
                          date_to=None,
                          limit=100,
                          offset=0):
        cursor = DB.cursor()

        req = (
            'select '
            '  r.arn_ser, r.arn_job_id, r.arn_started_at, r.arn_finished_at, r.arn_status, '
            '  r.arn_output_uri, r.arn_rows_count, r.arn_message, r.arn_error_trace, '
            '  j.ajb_label, j.ajb_type, j.ajb_schedule_kind, j.ajb_schedule_time, '
            '  j.ajb_schedule_dow, j.ajb_schedule_dom, j.ajb_schedule_last_dom, '
            '  j.ajb_schedule_anchor_jan, j.ajb_fire_on, j.ajb_params '
            'from automation_run r '
            'join automation_job j on j.ajb_ser = r.arn_job_id '
            'where 1=1 '
        )
        params = []

        if job_id:
            req += ' and r.arn_job_id = %s'
            params.append(int(job_id))

        if status in ('running', 'success', 'error', 'timeout'):
            req += ' and r.arn_status = %s'
            params.append(status)

        if date_from:
            req += ' and r.arn_started_at >= %s'
            params.append(date_from)

        if date_to:
            req += ' and r.arn_started_at <= %s'
            params.append(date_to)

        req += ' order by r.arn_started_at desc limit %s offset %s'
        params.extend([int(limit), int(offset)])

        try:
            cursor.execute(req, tuple(params))
            rows = cursor.fetchall() or []
        except Exception:
            Automation.log.exception(Logs.fileline() + ' : getAutomationRuns SQL')
            return []

        # Decode ajb_params and collect all potential internal recipients
        all_user_ids = set()
        typed_recipient_key = {
            'dhis2': 'dhis2_internal_recipient',
            'activity': 'activity_internal_recipient',
            'billing': 'billing_internal_recipient',
            'system': 'system_internal_recipient',
        }

        for row in rows:
            params_blob = row.get('ajb_params')
            if isinstance(params_blob, str):
                try:
                    params_obj = json.loads(params_blob)
                except Exception:
                    Automation.log.exception(Logs.fileline() + " : getAutomationRuns json decode failed arn_ser=" + str(row.get('arn_ser')))
                    params_obj = {}
            else:
                params_obj = params_blob or {}

            row['ajb_params'] = params_obj

            job_type = (row.get('ajb_type') or '').lower()
            rec_key = typed_recipient_key.get(job_type)
            if not rec_key:
                continue

            raw_val = params_obj.get(rec_key)
            if raw_val is None or raw_val == '':
                continue

            try:
                uid = int(raw_val)
                if uid > 0:
                    all_user_ids.add(uid)
            except (TypeError, ValueError):
                continue

        # Resolve user labels in one query
        user_labels = {}
        if all_user_ids:
            placeholders = ','.join(['%s'] * len(all_user_ids))
            try:
                req_users = (
                    "select id_data, firstname, lastname, username "
                    f"from sigl_user_data where id_data in ({placeholders})"
                )
                cursor.execute(req_users, tuple(all_user_ids))
                users = cursor.fetchall() or []
            except Exception:
                users = []

            for user in users:
                first = (user.get('firstname') or '').strip()
                last = (user.get('lastname') or '').strip()
                label = (first + ' ' + last).strip()
                if not label:
                    label = (user.get('username') or '').strip()
                if label:
                    user_labels[user.get('id_data')] = label

        # Inject *_internal_recipient_label into ajb_params
        for row in rows:
            params_obj = row.get('ajb_params') or {}
            job_type = (row.get('ajb_type') or '').lower()
            rec_key = typed_recipient_key.get(job_type)
            if not rec_key:
                continue

            raw_val = params_obj.get(rec_key)
            if raw_val is None or raw_val == '':
                continue

            try:
                uid = int(raw_val)
            except (TypeError, ValueError):
                continue

            if uid > 0:
                label = user_labels.get(uid, str(uid))
                label_key = rec_key + '_label'
                params_obj[label_key] = label
                row['ajb_params'] = params_obj

        # Collect all generated_name tokens from arn_output_uri (basename of path)
        hash_tokens = set()
        for row in rows:
            uri = row.get('arn_output_uri')
            if not uri:
                continue
            token = os.path.basename(str(uri)).strip()
            if token:
                hash_tokens.add(token)

        file_by_hash = {}
        if hash_tokens:
            placeholders = ','.join(['%s'] * len(hash_tokens))
            try:
                req_files = (
                    "select id_data, original_name, generated_name "
                    "from sigl_file_data "
                    f"where generated_name in ({placeholders})"
                )
                cursor.execute(req_files, tuple(hash_tokens))
                frows = cursor.fetchall() or []
            except Exception:
                Automation.log.exception(Logs.fileline() + " : getAutomationRuns file lookup SQL")
                frows = []

            for f in frows:
                gen = f.get('generated_name')
                if gen:
                    file_by_hash[gen] = f

        # Enrich rows with file_id / file_name if matching entry found
        for row in rows:
            uri = row.get('arn_output_uri')
            if not uri:
                continue
            token = os.path.basename(str(uri)).strip()
            if not token:
                continue

            f = file_by_hash.get(token)
            if not f:
                continue

            row['file_id'] = f.get('id_data')
            row['file_name'] = (f.get('original_name') or '').strip() or token

        return rows

    # ---------------------------
    # Trigger "run now"
    # ---------------------------
    @staticmethod
    def forceAutomationRunNow(ajb_ser: int, message: str = '') -> bool:
        """
        Force next_run_at = now() so scheduler will execute ASAP.
        We do NOT pre-create a run row here, UI will see it once real run starts.
        """
        cursor = DB.cursor()
        try:
            req = (
                'update automation_job '
                'set ajb_next_run_at = now() '
                'where ajb_ser = %s'
            )
            cursor.execute(req, (ajb_ser,))
            if cursor.rowcount <= 0:
                return False
        except Exception:
            Automation.log.exception(Logs.fileline() + ' : forceAutomationRunNow SQL')
            return False
        return True

    # ---------------------------
    # Lightweight scheduler (DB only)
    # ---------------------------
    @staticmethod
    def scheduler_process_due(max_jobs: int = 5) -> int:
        """
        Pick up to max_jobs due jobs (active, next_run_at <= now), run them sequentially.
        This method only handles DB state (start/finish runs, compute next_run_at).
        The actual job execution (HTTP, files, etc.) must be done by the runner/REST.
        """
        cursor = DB.cursor()

        req = (
            'select '
            '  ajb_ser, ajb_type, ajb_label, ajb_is_active, '
            '  ajb_schedule_kind, ajb_schedule_time, ajb_schedule_dow, '
            '  ajb_schedule_dom, ajb_schedule_last_dom, ajb_schedule_anchor_jan, '
            '  ajb_fire_on, ajb_schedule_start_on, ajb_next_run_at, ajb_last_run_at, '
            '  ajb_last_status, ajb_params '
            'from automation_job '
            'where ajb_is_active = "Y" '
            'and ajb_next_run_at is not null '
            'and ajb_next_run_at <= now() '
            'and (ajb_last_status is null or ajb_last_status <> "running") '
            'order by ajb_next_run_at asc '
            'limit %s'
        )

        cursor.execute(req, (int(max_jobs),))
        jobs = cursor.fetchall() or []
        if not jobs:
            return 0

        processed = 0
        for job in jobs:
            job_id = int(job['ajb_ser'])

            run_id = _start_run(job_id)
            if not run_id:
                try:
                    cursor_fail = DB.cursor()
                    cursor_fail.execute(
                        'update automation_job set ajb_last_status = %s where ajb_ser = %s',
                        ('error', job_id)
                    )
                except Exception:
                    Automation.log.exception(Logs.fileline() + " : scheduler _start_run failed ajb_ser=" + str(job_id))
                continue

            cursor2 = DB.cursor()
            try:
                req2 = (
                    'update automation_job '
                    'set ajb_last_status = %s, ajb_last_run_at = now() '
                    'where ajb_ser = %s'
                )
                cursor2.execute(req2, ('running', job_id))
            except Exception:
                Automation.log.exception(Logs.fileline() + ' : scheduler mark running SQL')

            try:
                result = _execute_job(job)  # placeholder: computes window only
                status = result.get('status') or 'error'
                rows_count = result.get('rows_count')
                output_uri = result.get('output_uri')
                message = result.get('message')
                error_trace = result.get('error_trace')
            except Exception as ex:
                status = 'error'
                rows_count = None
                output_uri = None
                message = 'unhandled exception'
                error_trace = str(ex)

            _finish_run(run_id, status, rows_count, output_uri, message, error_trace)

            try:
                next_dt = _recompute_next_from_row(job)
                cursor3 = DB.cursor()
                req3 = (
                    'update automation_job '
                    'set ajb_next_run_at = %s, ajb_last_status = %s '
                    'where ajb_ser = %s'
                )
                cursor3.execute(req3, (next_dt.strftime('%Y-%m-%d %H:%M:%S'), status, job_id))
            except Exception:
                Automation.log.exception(Logs.fileline() + ' : scheduler persist next_run_at SQL')

            processed += 1

        return processed

    # --- aliases / helpers expected by FE ---
    @staticmethod
    def listActiveJobs():
        """Return all active jobs (Y)."""
        cursor = DB.cursor()
        req = (
            "SELECT ajb_ser, ajb_type, ajb_label, ajb_is_active, "
            "ajb_schedule_kind, ajb_schedule_time, ajb_schedule_dow, "
            "ajb_schedule_dom, ajb_schedule_last_dom, ajb_schedule_anchor_jan, "
            "ajb_fire_on, ajb_schedule_start_on, ajb_next_run_at, ajb_last_run_at, "
            "ajb_last_status, ajb_params, ajb_created_at, ajb_updated_at "
            "FROM automation_job WHERE ajb_is_active = 'Y'"
        )
        cursor.execute(req)
        rows = cursor.fetchall() or []
        for row in rows:
            param_blob = row.get('ajb_params')
            if isinstance(param_blob, str):
                try:
                    row['ajb_params'] = json.loads(param_blob)
                except Exception:
                    Automation.log.exception(Logs.fileline() + " : listActiveJobs json decode failed ajb_ser=" + str(row.get('ajb_ser')))
        return rows

    @staticmethod
    def get_due_jobs(now_str):
        """Return active jobs whose next_run_at <= now_str."""
        cursor = DB.cursor()
        req = (
            "SELECT ajb_ser, ajb_type, ajb_label, ajb_is_active, "
            "ajb_schedule_kind, ajb_schedule_time, ajb_schedule_dow, "
            "ajb_schedule_dom, ajb_schedule_last_dom, ajb_schedule_anchor_jan, "
            "ajb_fire_on, ajb_schedule_start_on, ajb_next_run_at, ajb_last_run_at, "
            "ajb_last_status, ajb_params, ajb_created_at, ajb_updated_at "
            "FROM automation_job "
            "WHERE ajb_is_active = 'Y' "
            "AND ajb_next_run_at IS NOT NULL "
            "AND ajb_next_run_at <= %s"
        )
        cursor.execute(req, (now_str,))
        rows = cursor.fetchall()
        for row in rows:
            param_blob = row.get('ajb_params')
            if isinstance(param_blob, str):
                try:
                    row['ajb_params'] = json.loads(param_blob)
                except Exception:
                    Automation.log.exception(Logs.fileline() + " : get_due_jobs json decode failed ajb_ser=" + str(row.get('ajb_ser')))
        return rows

    @staticmethod
    def update_next_run_at(ajb_ser, next_run_at_str):
        """Set next_run_at (on ne touche pas à last_status ici)."""
        cursor = DB.cursor()
        req = (
            "UPDATE automation_job "
            "SET ajb_next_run_at = %s, ajb_last_status = ajb_last_status "
            "WHERE ajb_ser = %s"
        )
        cursor.execute(req, (next_run_at_str, ajb_ser))

    @staticmethod
    def execute_job(job_row: dict) -> dict:
        """
        Public, sans HTTP : calcule seulement la fenêtre et retourne un message.
        L’exécution réelle (DHIS2/activity/billing) doit se faire côté REST/runner.
        """
        return _execute_job(job_row)


# ---------------------------
# Helpers (dates & runs)
# ---------------------------
def _parse_time(hhmmss: str) -> time:
    """Return a time object from 'HH:MM[:SS]' (default seconds=00)."""
    if not hhmmss:
        hhmmss = '02:00:00'
    if len(hhmmss) == 5:
        hhmmss += ':00'
    hour, minute, second = hhmmss.split(':')
    return time(int(hour), int(minute), int(second))


def _end_of_month(year: int, month: int) -> date:
    """Return last day of (year, month)."""
    last_dom = calendar.monthrange(year, month)[1]
    return date(year, month, last_dom)


def _add_months(year: int, month: int, delta: int) -> (int, int):
    """Add delta months to (year, month). Return (year, month)."""
    index = (year * 12 + (month - 1)) + delta
    whole_years, month_index = divmod(index, 12)
    return whole_years, (month_index + 1)


def _next_weekly_occurrence(base_day: date, now_dt: datetime, dow: int, run_at: time) -> datetime:
    """Compute next weekly run (1=Mon..7=Sun)."""
    target_wd = (dow - 1) % 7
    delta_days = (target_wd - base_day.weekday()) % 7
    candidate_day = base_day + timedelta(days=delta_days)
    candidate_dt = datetime.combine(candidate_day, run_at)
    if delta_days == 0 and candidate_dt <= now_dt:
        candidate_dt += timedelta(days=7)
    return candidate_dt


def _period_end_anchored_jan(base_day: date, span: int) -> date:
    """End date of the period containing base_day, anchored to January."""
    group_index = (base_day.month - 1) // span
    start_month = group_index * span + 1
    start_year = base_day.year
    end_year, end_month = _add_months(start_year, start_month, span - 1)
    return _end_of_month(end_year, end_month)


def _period_end_rolling(base_day: date, span: int) -> date:
    """End date of the rolling period starting at base_day's month."""
    start_year, start_month = base_day.year, base_day.month
    end_year, end_month = _add_months(start_year, start_month, span - 1)
    return _end_of_month(end_year, end_month)


def _apply_day_choice(month_end: date, schedule_dom: int | None, last_dom_flag: str) -> date:
    """Choose execution day within the end month: last_dom or specific dom (bounded)."""
    if (last_dom_flag or 'N').upper() == 'Y' or not schedule_dom:
        return month_end
    safe_dom = min(schedule_dom, month_end.day)
    return date(month_end.year, month_end.month, safe_dom)


def compute_next_run_at(kind: str,
                        time_str: str,
                        schedule_dow: int | None,
                        schedule_dom: int | None,
                        schedule_last_dom: str | None,
                        anchor_jan: str | None,
                        start_on: str | None,
                        now_dt: datetime | None = None) -> datetime:
    """Compute the first next_run_at strictly > now()."""
    time_str = str(time_str or '02:00:00')
    run_at = _parse_time(time_str)
    now_dt = now_dt or datetime.now()
    today = now_dt.date()

    start_day = None
    if start_on:
        try:
            start_day = datetime.strptime(start_on, '%Y-%m-%d').date()
        except Exception:
            Automation.log.exception(Logs.fileline() + " : compute_next_run_at invalid start_on=" + str(start_on))
            start_day = None

    # -----------------
    # Hourly / Daily / Weekly
    # -----------------
    if kind == 'H':
        candidate_dt = datetime(now_dt.year, now_dt.month, now_dt.day, now_dt.hour, run_at.minute, run_at.second)
        if candidate_dt <= now_dt:
            candidate_dt = candidate_dt + timedelta(hours=1)

        if start_day and candidate_dt.date() < start_day:
            candidate_dt = datetime.combine(start_day, time(0, run_at.minute, run_at.second))

        return candidate_dt

    if kind == 'D':
        base_day = today
        if start_day and start_day > base_day:
            base_day = start_day

        candidate_dt = datetime.combine(base_day, run_at)
        if candidate_dt <= now_dt:
            candidate_dt = datetime.combine(base_day + timedelta(days=1), run_at)
        return candidate_dt

    if kind == 'W':
        base_day = today
        if start_day and start_day > base_day:
            base_day = start_day

        desired_dow = int(schedule_dow or 1)
        return _next_weekly_occurrence(base_day, now_dt, desired_dow, run_at)

    # -----------------
    # Monthly-like (M/B/T/Q/S/A)
    # -----------------
    span = SPAN_BY_KIND.get(kind, 1)
    use_anchor_jan = (str(anchor_jan or 'Y').upper() == 'Y')
    last_dom_flag = str(schedule_last_dom or 'N').upper()

    def _exec_dt_for_period_start(start_y: int, start_m: int) -> datetime:
        end_y, end_m = _add_months(start_y, start_m, span - 1)
        month_end = _end_of_month(end_y, end_m)
        exec_day = _apply_day_choice(month_end, schedule_dom, last_dom_flag)
        return datetime.combine(exec_day, run_at)

    if use_anchor_jan:
        # Periods are aligned to January (e.g. quarters: Jan-Apr-Jul-Oct start months)
        base_day = today
        if start_day and start_day > base_day:
            base_day = start_day

        # Find the period containing base_day
        group_idx = (base_day.month - 1) // span
        start_m = group_idx * span + 1
        start_y = base_day.year

        candidate_dt = _exec_dt_for_period_start(start_y, start_m)

        # If we missed it, jump by span months until > now
        while candidate_dt <= now_dt:
            start_y, start_m = _add_months(start_y, start_m, span)
            candidate_dt = _exec_dt_for_period_start(start_y, start_m)

        # Respect start_on as a minimal date (date-only)
        if start_day and candidate_dt.date() < start_day:
            # recompute from the period containing start_day
            group_idx = (start_day.month - 1) // span
            start_m = group_idx * span + 1
            start_y = start_day.year
            candidate_dt = _exec_dt_for_period_start(start_y, start_m)
            while candidate_dt <= now_dt or candidate_dt.date() < start_day:
                start_y, start_m = _add_months(start_y, start_m, span)
                candidate_dt = _exec_dt_for_period_start(start_y, start_m)

        return candidate_dt

    # Rolling periods anchored to start_on (if provided) otherwise anchored to today month
    anchor_day = start_day or today
    anchor_index = anchor_day.year * 12 + (anchor_day.month - 1)
    now_index = today.year * 12 + (today.month - 1)

    diff = now_index - anchor_index
    if diff < 0:
        period_idx = 0
    else:
        period_idx = diff // span

    start_index = anchor_index + (period_idx * span)
    start_y, start_m = divmod(start_index, 12)
    start_m += 1

    candidate_dt = _exec_dt_for_period_start(start_y, start_m)
    while candidate_dt <= now_dt:
        period_idx += 1
        start_index = anchor_index + (period_idx * span)
        start_y, start_m = divmod(start_index, 12)
        start_m += 1
        candidate_dt = _exec_dt_for_period_start(start_y, start_m)

    return candidate_dt


def _start_run(job_id: int, message: str = '') -> int:
    """Create a new automation_run row with status=running."""
    cursor = DB.cursor()
    try:
        req = (
            'insert into automation_run (arn_job_id, arn_started_at, arn_status, arn_message) '
            'values (%s, now(), %s, %s)'
        )
        cursor.execute(req, (job_id, 'running', message or ''))
        return cursor.lastrowid or 0
    except Exception:
        Automation.log.exception(Logs.fileline() + ' : _start_run SQL')
        return 0


def _finish_run(run_id: int,
                status: str,
                rows_count: int | None = None,
                output_uri: str | None = None,
                message: str | None = None,
                error_trace: str | None = None) -> None:
    """Finalize automation_run row."""
    cursor = DB.cursor()
    try:
        req = (
            'update automation_run '
            'set arn_finished_at = now(), arn_status = %s, '
            '    arn_rows_count = %s, arn_output_uri = %s, '
            '    arn_message = %s, arn_error_trace = %s '
            'where arn_ser = %s'
        )
        cursor.execute(req, (status, rows_count, output_uri, message, error_trace, run_id))
    except Exception:
        Automation.log.exception(Logs.fileline() + " : _finish_run failed arn_ser=" + str(run_id))
        try:
            cursor2 = DB.cursor()
            cursor2.execute(
                'update automation_run set arn_status = %s where arn_ser = %s',
                ('error', run_id)
            )
        except Exception:
            Automation.log.exception(Logs.fileline() + " : _finish_run fallback update failed arn_ser=" + str(run_id))


def _recompute_next_from_row(job_row: dict) -> datetime:
    """Recompute next_run_at using current row fields."""
    return compute_next_run_at(
        kind=job_row['ajb_schedule_kind'],
        time_str=str(job_row['ajb_schedule_time']),
        schedule_dow=job_row['ajb_schedule_dow'],
        schedule_dom=job_row['ajb_schedule_dom'],
        schedule_last_dom=job_row['ajb_schedule_last_dom'],
        anchor_jan=job_row['ajb_schedule_anchor_jan'],
        start_on=job_row['ajb_schedule_start_on'].strftime('%Y-%m-%d') if job_row['ajb_schedule_start_on'] else None
    )


def _compute_period_window(job_row: dict, now_dt: datetime | None = None) -> tuple[datetime, datetime]:
    """
    Compute [date_beg, date_end] for the job being fired now.
    Inclusive bounds, in local server time.
    Honors:
      - ajb_schedule_kind: 'H', 'D','W','M','B','T','Q','S','A'
      - ajb_schedule_dow (weekly)
      - ajb_schedule_dom / ajb_schedule_last_dom / ajb_schedule_anchor_jan (monthly-like)
      - ajb_fire_on: 'period_end' | 'period_start'
    """
    now_dt = now_dt or datetime.now()
    today = now_dt.date()

    kind = job_row['ajb_schedule_kind']
    schedule_dow = job_row['ajb_schedule_dow']          # 1..7 or None
    # schedule_last_dom = (job_row['ajb_schedule_last_dom'] or 'N').upper()
    schedule_anchor_jan = (job_row['ajb_schedule_anchor_jan'] or 'Y').upper()
    fire_on = job_row['ajb_fire_on'] or 'period_end'
    job_type = (job_row.get('ajb_type') or '').lower()

    def day_bounds(d: date) -> tuple[datetime, datetime]:
        beg = datetime(d.year, d.month, d.day, 0, 0, 0)
        end = datetime(d.year, d.month, d.day, 23, 59, 59)
        return beg, end

    if kind == 'H':
        # Hourly window: previous full hour (period_end) or current hour (period_start).
        if fire_on == 'period_end':
            ref_dt = now_dt - timedelta(hours=1)
        else:
            ref_dt = now_dt

        hour_start = datetime(ref_dt.year, ref_dt.month, ref_dt.day, ref_dt.hour, 0, 0)
        hour_end = datetime(ref_dt.year, ref_dt.month, ref_dt.day, ref_dt.hour, 59, 59)
        return hour_start, hour_end

    if kind == 'D':
        if fire_on == 'period_end':
            reference_day = today - timedelta(days=1)
            return day_bounds(reference_day)
        else:
            return day_bounds(today)

    if kind == 'W':
        # DHIS2 weekly = full previous week Monday→Sunday
        if job_type == 'dhis2' and fire_on == 'period_end':
            ref = today - timedelta(days=7)
            week_start = ref - timedelta(days=ref.weekday())   # Monday
            week_end = week_start + timedelta(days=6)          # Sunday
            return (
                datetime(week_start.year, week_start.month, week_start.day, 0, 0, 0),
                datetime(week_end.year, week_end.month, week_end.day, 23, 59, 59)
            )

        # generic behavior for non-DHIS2 or fire_on = period_start
        target = ((schedule_dow or 1) - 1) % 7
        today_wd = today.weekday()

        if fire_on == 'period_end':
            end_day = today - timedelta(days=(today_wd - target) % 7)
            start_day = end_day - timedelta(days=6)
        else:
            start_day = today + timedelta(days=(target - today_wd) % 7)
            end_day = start_day + timedelta(days=6)

        return (
            datetime(start_day.year, start_day.month, start_day.day, 0, 0, 0),
            datetime(end_day.year, end_day.month, end_day.day, 23, 59, 59)
        )

    span = SPAN_BY_KIND.get(kind, 1)
    use_anchor = (schedule_anchor_jan == 'Y')

    def period_end_for(d: date) -> date:
        if use_anchor:
            group_idx = (d.month - 1) // span
            start_month = group_idx * span + 1
            end_year, end_month = _add_months(d.year, start_month, span - 1)
            return _end_of_month(end_year, end_month)
        else:
            end_year, end_month = _add_months(d.year, d.month, span - 1)
            return _end_of_month(end_year, end_month)

    def period_start_from_end(end_d: date) -> date:
        start_year, start_month = _add_months(end_d.year, end_d.month, -(span - 1))
        return date(start_year, start_month, 1)

    # Current span (containing today)
    this_end = period_end_for(today)
    this_start = period_start_from_end(this_end)

    if fire_on == 'period_end':
        # Previous complete span
        prev_start_year, prev_start_month = _add_months(this_start.year, this_start.month, -span)
        prev_start = date(prev_start_year, prev_start_month, 1)
        prev_end = period_end_for(prev_start)
        begin_dt = datetime(prev_start.year, prev_start.month, prev_start.day, 0, 0, 0)
        end_dt = datetime(prev_end.year, prev_end.month, prev_end.day, 23, 59, 59)
        return begin_dt, end_dt
    else:
        # Next span (fire_on = period_start)
        next_start_year, next_start_month = _add_months(this_start.year, this_start.month, span)
        next_start = date(next_start_year, next_start_month, 1)
        next_end = period_end_for(next_start)
        begin_dt = datetime(next_start.year, next_start.month, next_start.day, 0, 0, 0)
        end_dt = datetime(next_end.year, next_end.month, next_end.day, 23, 59, 59)
        return begin_dt, end_dt


def _build_periods(period_kind: str, date_beg: datetime, date_end: datetime) -> list[list]:
    """Build l_period as in /services/export/dhis2 (inclusive bounds)."""
    l_period = []

    if period_kind == 'W':
        # ISO weeks: always start on Monday
        cur_day = date_beg.date()
        cur_day = cur_day - timedelta(days=cur_day.weekday())  # Monday of that week

        while datetime.combine(cur_day, time(0, 0, 0)) <= date_end:
            iso_year, iso_week, _ = cur_day.isocalendar()
            tmp_period = f"{iso_year}W{iso_week:02d}"

            week_start = datetime.combine(cur_day, time(0, 0, 0))
            week_end = datetime.combine(cur_day + timedelta(days=6), time(23, 59, 59))

            beg = max(week_start, date_beg)
            end = min(week_end, date_end)

            if beg <= end:
                l_period.append([tmp_period, beg, end])

            cur_day = cur_day + timedelta(days=7)

    elif period_kind == 'M':
        # Calendar months (clamped to [date_beg, date_end])
        y, m = date_beg.year, date_beg.month
        while datetime(y, m, 1, 0, 0, 0) <= date_end:
            last_dom = calendar.monthrange(y, m)[1]
            cur_start = datetime(y, m, 1, 0, 0, 0)
            cur_end = datetime(y, m, last_dom, 23, 59, 59)
            tmp_period = f"{y}M{m:02d}"

            beg = max(cur_start, date_beg)
            end = min(cur_end, date_end)

            if beg <= end:
                l_period.append([tmp_period, beg, end])

            if m == 12:
                y, m = y + 1, 1
            else:
                m = m + 1

    elif period_kind in ('B', 'T', 'Q', 'S', 'A'):
        # Multi-month groups (B=2, T=3, Q=4, S=6, A=12), clamped to [date_beg, date_end]
        span_map = {'B': 2, 'T': 3, 'Q': 4, 'S': 6, 'A': 12}
        span = span_map[period_kind]
        y, m = date_beg.year, date_beg.month

        while datetime(y, m, 1, 0, 0, 0) <= date_end:
            cur_start = datetime(y, m, 1, 0, 0, 0)

            ym_next = (m - 1) + (span - 1)
            y_end, m_end = y + (ym_next // 12), (ym_next % 12) + 1
            last_dom = calendar.monthrange(y_end, m_end)[1]
            cur_end = datetime(y_end, m_end, last_dom, 23, 59, 59)

            # label formats aligned with REST endpoint
            if period_kind == 'A':
                tmp_period = f"{y}"
            elif period_kind == 'S':
                idx = 1 if m <= 6 else 2
                tmp_period = f"{y}S{idx}"
            elif period_kind == 'T':
                idx = ((m - 1) // 3) + 1
                tmp_period = f"{y}Q{idx}"
            elif period_kind == 'B':
                idx = ((m - 1) // 2) + 1
                tmp_period = f"{y}{idx:02d}B"
            else:  # Quadrimestrial 'Q' (custom …QnC)
                idx = ((m - 1) // 4) + 1
                tmp_period = f"{y}Q{idx}C"

            beg = max(cur_start, date_beg)
            end = min(cur_end, date_end)

            if beg <= end:
                l_period.append([tmp_period, beg, end])

            next_index = (m - 1) + span
            y, m = y + (next_index // 12), (next_index % 12) + 1

    else:
        raise ValueError(f"wrong period kind: {period_kind}")

    return l_period


def _write_file_safe(src_path: str, dst_folder: str) -> tuple[str, str, int]:
    """
    Generic MD5 hashing + move/rename.
    Used by all automation jobs (dhis2, billing, activity...).
    Returns (final_path, generated_name, size).
    """
    if not os.path.isfile(src_path):
        raise RuntimeError("source file not found: " + src_path)

    # Ensure destination exists
    Path(dst_folder).mkdir(parents=True, exist_ok=True)

    # Compute MD5 hash on existing file
    md5 = hashlib.md5()
    with open(src_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            md5.update(chunk)

    generated_name = md5.hexdigest()
    final_path = os.path.join(dst_folder, generated_name)

    # Move + rename
    shutil.move(src_path, final_path)

    size = os.path.getsize(final_path)
    return final_path, generated_name, size


def _execute_job_dhis2_send(job_row: dict) -> dict:
    """Execute DHIS2 send mode (API push, same logic as ExportDHIS2Api but without HTTP response)."""
    params = job_row.get('ajb_params') or {}
    if isinstance(params, str):
        try:
            params = json.loads(params)
        except Exception:
            params = {}

    sheet = str(params.get('dhis2_sheet') or '').strip()
    if not sheet:
        return {'status': 'error', 'rows_count': 0, 'output_uri': None, 'message': 'missing dhis2_sheet for send mode', 'error_trace': None}

    rec_type = (params.get('dhis2_folder_scope') or 'A').upper()
    if rec_type not in ('A', 'E', 'I'):
        rec_type = 'A'

    lite_filter = (params.get('dhis2_lblite_mode') or 'A').upper()
    if lite_filter not in ('A', 'N', 'Y'):
        lite_filter = 'A'

    try:
        dhs_ser = int(params.get('dhis2_api_config') or 0)
    except Exception:
        Automation.log.exception(Logs.fileline() + " : DHIS2 send invalid dhis2_api_config=" + str(params.get('dhis2_api_config')))
        dhs_ser = 0

    if dhs_ser <= 0:
        return {'status': 'error', 'rows_count': 0, 'output_uri': None, 'message': 'missing or invalid dhis2_api_config', 'error_trace': None}

    try:
        id_user = int(params.get('dhis2_user_id') or 0)
    except Exception:
        Automation.log.exception(Logs.fileline() + " : DHIS2 send invalid dhis2_user_id=" + str(params.get('dhis2_user_id')))
        id_user = 1

    dry_run_flag = (params.get('dhis2_dry_run') or 'N').upper()
    if dry_run_flag not in ('Y', 'N'):
        dry_run_flag = 'N'

    # Compute time window from scheduler (same as create)
    date_beg, date_end = _compute_period_window(job_row)
    period_kind = job_row['ajb_schedule_kind']

    l_period = _build_periods(period_kind, date_beg, date_end)

    # --- Build data (same logic as ExportDHIS2Api) ---
    filename_token = sheet[:-4] if sheet.lower().endswith('.csv') else sheet
    l_data = []

    if filename_token == "LIST_OUTSOURCING":
        Automation.log.info(Logs.fileline() + ' : DHIS2 send LIST_OUTSOURCING')
        l_data = [["period", "code patient", "record number", "record date", "analysis outsourced", "LabBook Lite"]]
        for period_item in l_period:
            rows = Export.getListOutsourcing(period_item[1], period_item[2], rec_type, lite_filter)
            for row in (rows or []):
                code = str(row['code'])
                if row['code_patient']:
                    code += ' / ' + str(row['code_patient'])
                num_rec = str(row['num_dos_an'])
                date_rec = str(row['date_rec'])
                ana_outsourced = str(row['ana_code']) + ' ' + str(row['ana_name'])
                lite_flag = 'Y' if (row.get('rec_lite') or 0) > 0 else 'N'
                l_data.append([period_item[0], code, num_rec, date_rec, ana_outsourced, lite_flag])

    elif filename_token == "LIST_EEQ":
        Automation.log.info(Logs.fileline() + ' : DHIS2 send LIST_EEQ')
        l_data = [["period", "control name", "control date", "supplier", "result date", "result", "comment"]]
        for period_item in l_period:
            rows = Export.getListEEQ(period_item[1], period_item[2])
            for row in (rows or []):
                result_map = {'Y': 'Conforme', 'N': 'Non conforme', 'U': 'Autres'}
                result = result_map.get(row.get('cte_conform'), '')
                l_data.append([
                    period_item[0],
                    row.get('ctq_name'),
                    row.get('ctq_date'),
                    row.get('cte_organizer'),
                    row.get('cte_date'),
                    result,
                    row.get('cte_comment'),
                ])

    elif filename_token == "LIST_EQUIPMENT_FAILURE":
        Automation.log.info(Logs.fileline() + ' : DHIS2 send LIST_EQUIPMENT_FAILURE')
        l_data = [["period", "Equipment name", "Manufacturer name", "Supplier name", "Inventory number", "Date of failure", "Comment"]]
        for period_item in l_period:
            rows = Export.getListEqpFailure(period_item[1], period_item[2])
            for row in (rows or []):
                l_data.append([
                    period_item[0],
                    row.get('eqp_name'),
                    row.get('eqp_manufacturer'),
                    row.get('supplier_name'),
                    row.get('eqp_invent_num'),
                    row.get('eqf_date'),
                    row.get('eqf_comm'),
                ])

    elif filename_token == "LIST_STOCK_STATUS":
        Automation.log.info(Logs.fileline() + ' : DHIS2 send LIST_STOCK_STATUS')
        l_data = [["period", "product name", "Expiration status", "Quantity status"]]
        for period_item in l_period:
            rows = Export.getListStockStatus(period_item[1], period_item[2])
            for row in (rows or []):
                l_data.append([
                    period_item[0],
                    str(row.get('prd_name') or ''),
                    str(row.get('exp_status') or ''),
                    str(row.get('qty_status') or ''),
                ])

    else:
        # Spreadsheet mode
        base_dir = Path(Constants.cst_dhis2).resolve()
        base_dir.mkdir(parents=True, exist_ok=True)

        safe_name = re.sub(Constants.cst_safe_pattern, '_', str(sheet))[:80]
        if not safe_name.lower().endswith('.csv'):
            safe_name += '.csv'

        csv_path = (base_dir / safe_name).resolve()
        if base_dir not in csv_path.parents:
            Automation.log.error(Logs.fileline() + ' : DHIS2 send ERROR invalid input path')
            return {'status': 'error', 'rows_count': 0, 'output_uri': None, 'message': 'invalid spreadsheet path', 'error_trace': None}

        try:
            with csv_path.open('r', encoding='utf-8', newline='') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=';')
                l_rows = list(csv_reader)
        except Exception as err:
            Automation.log.error(Logs.fileline() + ' : DHIS2 send ERROR reading spreadsheet ' + str(err))
            return {'status': 'error', 'rows_count': 0, 'output_uri': None, 'message': 'spreadsheet read error', 'error_trace': str(err)}

        if not l_rows or len(l_rows) < 2:
            Automation.log.error(Logs.fileline() + ' : DHIS2 send ERROR spreadsheet empty')
            return {'status': 'error', 'rows_count': 0, 'output_uri': None, 'message': 'spreadsheet empty', 'error_trace': None}

        l_cols = l_rows[0]
        if "version" not in l_cols:
            Automation.log.error(Logs.fileline() + ' : DHIS2 send ERROR spreadsheet missing version column')
            return {'status': 'error', 'rows_count': 0, 'output_uri': None, 'message': 'spreadsheet missing version column', 'error_trace': None}

        idx_version = l_cols.index("version")
        version = l_rows[1][idx_version]
        if version not in ("v1", "v2", "v3"):
            Automation.log.error(Logs.fileline() + ' : DHIS2 send ERROR spreadsheet wrong version ' + str(version))
            return {'status': 'error', 'rows_count': 0, 'output_uri': None, 'message': 'spreadsheet wrong version', 'error_trace': None}

        # Determine orgunit
        orgunit = ''
        if "orgunit" in l_cols:
            idx_orgunit = l_cols.index("orgunit")
            orgunit = l_rows[1][idx_orgunit]
        if not orgunit:
            lab = Various.getDefaultValue('entete_1')
            if lab:
                orgunit = lab['value']

        # Determine storedby
        storedby = ''
        if "storedby" in l_cols:
            idx_storedby = l_cols.index("storedby")
            storedby = l_rows[1][idx_storedby]
        if not storedby:
            user = User.getUserDetails(id_user)
            if user:
                storedby = (user.get('firstname') or '') + (user.get('lastname') or '')
        storedby = storedby.replace(' ', '')

        now_dt = datetime.now()

        # Remove header line
        l_rows.pop(0)

        l_data = [["dataelement", "period", "orgunit", "categoryoptioncombo", "attributeoptioncombo", "value", "storedby", "lastupdated", "comment", "followup", "deleted"]]

        for period_item in l_period:
            period_beg_db = period_item[1]
            period_end_db = period_item[2]
            for row in l_rows:
                if not row or all(str(c).strip() == '' for c in row):
                    continue

                if version == 'v3':
                    filter_row = row[2].strip()
                else:
                    filter_row = row[3].strip()

                data = []
                if version == 'v3':
                    data.append(row[0])
                    data.append(period_item[0])
                    data.append(orgunit)
                    data.append(row[4])
                    data.append(row[5])
                else:
                    data.append(row[0])
                    data.append(period_item[0])
                    data.append(orgunit)
                    data.append(row[5])
                    data.append(row[6])

                # Formula/statistics handling
                if filter_row.startswith("$") or filter_row.startswith("{") or filter_row.lstrip().startswith("("):
                    if version == 'v3':
                        type_samp = row[3]
                    else:
                        type_samp = row[4]

                    Automation.log.info(Logs.fileline() + ' : DHIS2 send formula filter_row=' + str(filter_row) + ' type_samp=' + str(type_samp))

                    req_part = Report.ParseFormula(filter_row, type_samp)
                    result = Report.getResultEpidemio(req_part=req_part, date_beg=period_beg_db, date_end=period_end_db, rec_type=rec_type, lite_filter=lite_filter)

                    value_to_write = ''
                    if isinstance(result, dict):
                        value_to_write = result.get('value', '')
                    elif isinstance(result, (list, tuple)) and len(result) > 0:
                        value_to_write = result[0]
                    elif result is not None:
                        value_to_write = result
                    data.append(str(value_to_write) if value_to_write != '' else '')

                else:
                    result = Export.getStatDHIS2(period_beg_db, period_end_db, filter_row, rec_type, lite_filter)
                    if result and isinstance(result, dict) and 'value' in result:
                        data.append(str(result['value']))
                    else:
                        data.append('')

                data.append(storedby)
                data.append(now_dt.strftime("%Y-%m-%dT%H:%M:%S"))
                data.append('')
                data.append('FALSE')
                data.append('')
                l_data.append(data)

    # If no data rows, we still log but return success with 0
    if not l_data or len(l_data) < 2:
        Automation.log.info(Logs.fileline() + ' : DHIS2 send no data rows for period_kind=' + str(period_kind))
        return {'status': 'success', 'rows_count': 0, 'output_uri': None, 'message': 'no data for period', 'error_trace': None}

    # --- Send data to DHIS2 (same as ExportDHIS2Api, but internal) ---
    api = Setting.getDHIS2Det(dhs_ser)
    if not api:
        Automation.log.error(Logs.fileline() + ' : DHIS2 send ERROR api setting not found for dhs_ser=' + str(dhs_ser))
        return {'status': 'error', 'rows_count': len(l_data) - 1, 'output_uri': None, 'message': 'DHIS2 api setting not found', 'error_trace': None}

    dry_run_suffix = '?dryRun=true' if dry_run_flag == 'Y' else ''
    url = api['dhs_url'] + str("/dataValueSets") + dry_run_suffix
    login = api['dhs_login']
    pwd = api['dhs_pwd']

    csv_buf = StringIO()
    csv_writer = csv.writer(csv_buf)
    csv_writer.writerows(l_data)

    headers = {"Content-Type": "application/csv"}
    auth = (login, pwd)

    resp_text = ''
    try:
        import requests
        resp = requests.post(url, data=csv_buf.getvalue(), headers=headers, auth=auth)
        resp_text = str(resp.text)

        if resp.status_code == 200:
            Automation.log.info(Logs.fileline() + ' : DHIS2 send requests OK code=' + str(resp.status_code))
            return {'status': 'success', 'rows_count': len(l_data) - 1, 'output_uri': None, 'message': resp_text, 'error_trace': None}
        else:
            Automation.log.error(Logs.fileline() + ' : DHIS2 send requests KO code=' + str(resp.status_code) + ' resp=' + resp_text)
            return {'status': 'error', 'rows_count': len(l_data) - 1, 'output_uri': None, 'message': resp_text, 'error_trace': resp_text}
    except Exception as err:
        Automation.log.error(Logs.fileline() + ' : DHIS2 send requests post failed err=' + str(err))
        return {'status': 'error', 'rows_count': len(l_data) - 1, 'output_uri': None, 'message': 'requests post failed', 'error_trace': str(err)}


def _execute_job_dhis2_create(job_row: dict) -> dict:
    """
    Create a DHIS2 CSV file (LIST_* modes implemented).
    ajb_params:
      - dhis2_sheet: "LIST_STOCK_STATUS.csv", "LIST_EEQ.csv", etc. (or spreadsheet .csv)
      - dhis2_folder_scope: 'A'|'E'|'I'  (mapped to rec_type)
      - dhis2_lblite_mode:  'A'|'N'|'Y'  (lite_filter)
    """
    params = job_row.get('ajb_params') or {}
    if isinstance(params, str):
        try:
            params = json.loads(params)
        except Exception:
            Automation.log.exception(Logs.fileline() + " : DHIS2 create ajb_params json decode failed")
            params = {}
    sheet = str(params.get('dhis2_sheet') or '').strip()
    if not sheet:
        return {'status': 'error', 'rows_count': 0, 'output_uri': None, 'message': 'missing dhis2_sheet', 'error_trace': None}

    rec_type   = (params.get('dhis2_folder_scope') or 'A').upper()
    lite_mode  = (params.get('dhis2_lblite_mode') or 'A').upper()
    send_msg = (params.get('dhis2_internal_msg') or 'N').upper() == 'Y'
    recipient_raw = params.get('dhis2_internal_recipient')
    sender_id = int(params.get('dhis2_internal_sender') or 0)
    receiver_id = None
    if recipient_raw is not None and recipient_raw != '':
        try:
            receiver_id = int(recipient_raw)
        except Exception:
            receiver_id = None

    # Build time window from scheduler settings (same as FE/REST)
    date_beg, date_end = _compute_period_window(job_row)  # inclusive
    period_kind = job_row['ajb_schedule_kind']            # 'W','M','B','T','Q','S','A'
    l_period = _build_periods(period_kind, date_beg, date_end)

    # Token used to identify LIST_* vs spreadsheet
    filename_token = sheet[:-4] if sheet.lower().endswith('.csv') else sheet
    l_data = []

    # LIST_* implementations (aligned with Export.* sources)
    if filename_token == 'LIST_OUTSOURCING':
        l_data = [["period", "code patient", "record number", "record date", "analysis outsourced", "LabBook Lite"]]
        for p in l_period:
            for row in (Export.getListOutsourcing(p[1], p[2], rec_type, lite_mode) or []):
                code = str(row['code'])
                if row.get('code_patient'):
                    code += ' / ' + str(row['code_patient'])
                lite_flag = 'Y' if (row.get('rec_lite') or 0) > 0 else 'N'
                l_data.append([p[0], code, str(row.get('num_dos_an', '')), str(row.get('date_rec', '')),
                               f"{row.get('ana_code', '')} {row.get('ana_name', '')}", lite_flag])

    elif filename_token == 'LIST_EEQ':
        l_data = [["period", "control name", "control date", "supplier", "result date", "result", "comment"]]
        for p in l_period:
            for row in (Export.getListEEQ(p[1], p[2]) or []):
                result = {'Y': 'Conforme', 'N': 'Non conforme', 'U': 'Autres'}.get(row.get('cte_conform'), '')
                l_data.append([p[0], row.get('ctq_name'), row.get('ctq_date'), row.get('cte_organizer'),
                               row.get('cte_date'), result, row.get('cte_comment')])

    elif filename_token == 'LIST_EQUIPMENT_FAILURE':
        l_data = [["period", "Equipment name", "Manufacturer name", "Supplier name", "Inventory number", "Date of failure", "Comment"]]
        for p in l_period:
            for row in (Export.getListEqpFailure(p[1], p[2]) or []):
                l_data.append([p[0], row.get('eqp_name'), row.get('eqp_manufacturer'), row.get('supplier_name'),
                               row.get('eqp_invent_num'), row.get('eqf_date'), row.get('eqf_comm')])

    elif filename_token == 'LIST_STOCK_STATUS':
        l_data = [["period", "product name", "Expiration status", "Quantity status"]]
        for p in l_period:
            for row in (Export.getListStockStatus(p[1], p[2]) or []):
                l_data.append([p[0], str(row.get('prd_name', '')), str(row.get('exp_status', '')), str(row.get('qty_status', ''))])

    else:
        # Spreadsheet mode: load source CSV into l_data and reuse generic logic below
        base_dir = Path(Constants.cst_dhis2).resolve()
        base_dir.mkdir(parents=True, exist_ok=True)

        safe_name = re.sub(SAFE, '_', str(sheet))[:80]
        if not safe_name.lower().endswith('.csv'):
            safe_name += '.csv'

        csv_path = (base_dir / safe_name).resolve()

        if base_dir not in csv_path.parents:
            Automation.log.error(Logs.fileline() + " : DHIS2 spreadsheet ERROR invalid input path")
            return {
                'status': 'error',
                'rows_count': 0,
                'output_uri': None,
                'message': 'invalid spreadsheet path',
                'error_trace': None,
            }

        if not csv_path.exists():
            Automation.log.error(Logs.fileline() + " : DHIS2 spreadsheet ERROR missing file " + str(csv_path))
            return {
                'status': 'error',
                'rows_count': 0,
                'output_uri': None,
                'message': 'spreadsheet file not found: ' + safe_name,
                'error_trace': None,
            }

        l_data = []
        try:
            with csv_path.open('r', encoding='utf-8', newline='') as f:
                reader = csv.reader(f, delimiter=';')
                for row in reader:
                    l_data.append(row)
        except Exception as err:
            Automation.log.error(Logs.fileline() + " : DHIS2 spreadsheet read error = " + str(err))
            return {
                'status': 'error',
                'rows_count': 0,
                'output_uri': None,
                'message': 'spreadsheet read error',
                'error_trace': str(err),
            }

    beg_str = date_beg.strftime('%Y-%m-%d')
    end_str = date_end.strftime('%Y-%m-%d')

    # No data : still return success with 0 rows so scheduler records the run
    if len(l_data) < 2:
        Automation.log.info(Logs.fileline() + " : DHIS2 create - no data for period " + beg_str + " -> " + end_str + " sheet=" + sheet)
        if send_msg and receiver_id:
            Various.useLangPDF()

            title = _("Export DHIS2")
            msg   = _("Export DHIS2 pour la période %(beg)s → %(end)s : aucun résultat.")
            body  = msg % {"beg": beg_str, "end": end_str}
            _send_internal_message(sender_id, receiver_id, title, body)
        return {'status': 'success', 'rows_count': 0, 'output_uri': None, 'message': 'no rows for period', 'error_trace': None}

    # Filename consistent with REST endpoint
    rec_suffix  = '_rec-external' if rec_type == 'E' else ('_rec-internal' if rec_type == 'I' else '_rec-all')
    lite_suffix = '_without-Lite' if lite_mode == 'N' else ('_only-Lite' if lite_mode == 'Y' else '')
    safe_token = re.sub(SAFE, '_', filename_token)[:64] or 'export'
    outname = f"dhis2_{safe_token}_{beg_str}-{end_str}{rec_suffix}{lite_suffix}.csv"

    # Write CSV to tmp, then move+hash to dhis2 upload
    tmp_csv = os.path.join(Constants.cst_path_tmp, outname)

    try:
        with open(tmp_csv, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerows(l_data)
    except Exception as err:
        Automation.log.error(Logs.fileline() + " : DHIS2 create CSV write error = " + str(err))
        return {
            'status': 'error',
            'rows_count': 0,
            'output_uri': None,
            'message': 'csv write error',
            'error_trace': str(err),
        }

    try:
        final_path, md5_name, file_size = _write_file_safe(tmp_csv, Constants.cst_dhis2_upload)
    except Exception as err:
        Automation.log.error(Logs.fileline() + " : DHIS2 create _write_file_safe error = " + str(err))
        return {'status': 'error', 'rows_count': len(l_data) - 1, 'output_uri': None, 'message': 'file move/hash error', 'error_trace': str(err)}

    Automation.log.info(Logs.fileline() + " : DHIS2 create - building file " + outname + " for period " + beg_str + " -> " + end_str)

    # Ensure sigl_file_data entry even without internal message
    owner_id = job_row.get("ajb_created_by") or sender_id or 0
    file_id = _ensure_file_record(
        generated_name=md5_name,
        original_name=outname,
        file_size=file_size,
        owner_id=owner_id,
        path="dhis2/",
        ext="csv",
        content_type=Constants.cst_content_type_csv,
    )

    if send_msg and receiver_id:
        try:
            Various.useLangPDF()

            title = _("Export DHIS2")
            msg   = _("Fichier %(name)s généré pour la période %(beg)s → %(end)s.")
            body  = msg % {"name": outname, "beg": beg_str, "end": end_str}

            msg_id = _send_internal_message(owner_id, receiver_id, title, body)

            if msg_id > 0 and file_id:
                _attach_file_to_message(
                    msg_id,
                    generated_name=md5_name,
                    original_name=outname,
                    file_size=file_size,
                    sender_id=owner_id,
                    ext="csv",
                    content_type=Constants.cst_content_type_csv,
                    path="dhis2/",
                )
        except Exception:
            Automation.log.exception(Logs.fileline() + " : DHIS2 internal messaging failed")

    return {
        'status': 'success',
        'rows_count': len(l_data) - 1,
        'output_uri': final_path,
        'message': 'file created',
        'error_trace': None,
    }


def _execute_job_billing(job_row: dict) -> dict:
    params = job_row.get('ajb_params') or {}
    if isinstance(params, str):
        try:
            params = json.loads(params)
        except Exception:
            params = {}

    tpl_file = params.get('billing_template')
    if not tpl_file:
        return {
            'status': 'error',
            'rows_count': 0,
            'output_uri': None,
            'message': 'missing billing_template',
            'error_trace': None,
        }

    base_name = params.get('billing_filename') or 'billing_status'

    # Compute scheduler window
    date_beg_dt, date_end_dt = _compute_period_window(job_row)
    date_beg = date_beg_dt.strftime('%Y-%m-%d %H:%M:%S')
    date_end = date_end_dt.strftime('%Y-%m-%d %H:%M:%S')

    # Load billing data
    try:
        l_datas = Report.getBillingStatus(date_beg, date_end, 0) or []
    except Exception as err:
        Automation.log.error(Logs.fileline() + " : billing Report.getBillingStatus failed " + str(err))
        return {
            'status': 'error',
            'rows_count': 0,
            'output_uri': None,
            'message': 'Report.getBillingStatus failed',
            'error_trace': str(err),
        }

    if not l_datas:
        # Internal messaging even if no data
        send_msg = (params.get('billing_internal_msg') or "N").upper()
        receiver = int(params.get('billing_internal_recipient') or 0)

        if send_msg == "Y" and receiver > 0:
            try:
                Various.useLangPDF()

                title = _("État de la facturation")
                body = _("Aucune donnée de facturation pour la période %(beg)s → %(end)s.") % {
                    "beg": date_beg_dt.strftime('%Y-%m-%d'),
                    "end": date_end_dt.strftime('%Y-%m-%d')
                }

                sender = job_row.get("ajb_created_by") or 0
                _send_internal_message(sender, receiver, title, body)

            except Exception:
                Automation.log.exception(Logs.fileline() + " : billing internal msg failed")

        # Return success (same behaviour as DHIS2 create)
        msg = "no billing data for selected period"
        Automation.log.info(Logs.fileline() + " : " + msg)
        return {
            'status': 'success',
            'rows_count': 0,
            'output_uri': None,
            'message': msg,
            'error_trace': None,
        }

    for d in l_datas:
        for k, v in list(d.items()):
            if v is None:
                d[k] = ''

    # Build filename
    beg_short = date_beg_dt.strftime('%Y-%m-%d')
    end_short = date_end_dt.strftime('%Y-%m-%d')
    safe_name = f"{base_name}_{beg_short}_{end_short}"
    safe_name = re.sub(SAFE, "_", safe_name).strip("_")[:80]

    # Generate PDF in tmp
    try:
        ok = Pdf.getPdfBillList(l_datas, date_beg, date_end, tpl_file, safe_name)
        if not ok:
            msg = "Pdf.getPdfBillList failed"
            Automation.log.error(Logs.fileline() + " : " + msg)
            return {
                'status': 'error',
                'rows_count': len(l_datas),
                'output_uri': None,
                'message': msg,
                'error_trace': None,
            }
    except Exception as err:
        Automation.log.error(Logs.fileline() + " : billing PDF exception " + str(err))
        return {
            'status': 'error',
            'rows_count': 0,
            'output_uri': None,
            'message': 'exception in Pdf.getPdfBillList',
            'error_trace': str(err),
        }

    tmp_file = os.path.join(Constants.cst_path_tmp, safe_name + ".pdf")

    # Move to upload/billing/ with MD5 hashed name
    final_path, md5_name, file_size = _write_file_safe(
        tmp_file,
        Constants.cst_billing_upload
    )

    # Ensure sigl_file_data entry even without internal message
    owner_id = job_row.get("ajb_created_by") or 0
    _ensure_file_record(
        generated_name=md5_name,
        original_name=safe_name + ".pdf",
        file_size=file_size,
        owner_id=owner_id,
        path="billing/",
        ext="pdf",
        content_type=Constants.cst_content_type_pdf,
    )

    # Internal messaging (translated text)
    send_msg = (params.get('billing_internal_msg') or "N").upper()
    receiver = int(params.get('billing_internal_recipient') or 0)

    if send_msg == "Y" and receiver > 0:
        try:
            Various.useLangPDF()

            title = _("État de la facturation")
            body = _("Le rapport de facturation a été généré pour la période %(beg)s → %(end)s.") % {
                "beg": beg_short,
                "end": end_short
            }

            sender = job_row.get("ajb_created_by") or 0
            msg_id = _send_internal_message(sender, receiver, title, body)

            if msg_id > 0:
                _attach_file_to_message(
                    msg_id,
                    md5_name,                    # hashed file
                    safe_name + ".pdf",          # original name
                    file_size,
                    sender,
                    ext="pdf",
                    content_type=Constants.cst_content_type_pdf,
                    path="billing/"
                )

        except Exception:
            Automation.log.exception(Logs.fileline() + " : billing internal msg failed")

    return {
        'status': 'success',
        'rows_count': len(l_datas),
        'output_uri': final_path,       # hashed file path
        'message': 'billing pdf generated',
        'error_trace': None,
    }


def _execute_job_activity(job_row: dict) -> dict:
    """Execute activity report job (PDF + optional internal message)."""
    params = job_row.get('ajb_params') or {}
    if isinstance(params, str):
        try:
            params = json.loads(params)
        except Exception:
            params = {}

    tpl_file = params.get('activity_template')
    if not tpl_file:
        return {
            'status': 'error',
            'rows_count': 0,
            'output_uri': None,
            'message': 'missing activity_template',
            'error_trace': None,
        }

    output_mode = (params.get('activity_output') or 'pdf').lower()

    # Supported outputs: pdf, csv_type, csv_age
    if output_mode not in ('pdf', 'csv_type', 'csv_age'):
        return {
            'status': 'error',
            'rows_count': 0,
            'output_uri': None,
            'message': 'unknown activity_output=' + output_mode,
            'error_trace': None,
        }

    try:
        type_ana = int(params.get('activity_family') or 0)
    except Exception:
        type_ana = 0

    date_beg_dt, date_end_dt = _compute_period_window(job_row)
    date_beg = date_beg_dt.strftime('%Y-%m-%d %H:%M:%S')
    date_end = date_end_dt.strftime('%Y-%m-%d %H:%M:%S')

    send_msg = (params.get('activity_internal_msg') or "N").upper()
    receiver = int(params.get('activity_internal_recipient') or 0)
    sender   = job_row.get("ajb_created_by") or 0

    # Load stats by type
    try:
        stat_type = Report.getActivityType(date_beg, date_end, type_ana)
    except Exception as err:
        Automation.log.error(Logs.fileline() + " : activity Report.getActivityType failed err=" + str(err))
        return {
            'status': 'error',
            'rows_count': 0,
            'output_uri': None,
            'message': 'Report.getActivityType failed',
            'error_trace': str(err),
        }

    if not stat_type:
        Automation.log.error(Logs.fileline() + " : activity stat_type empty")
        stat_type = []

    # Load stats by age
    try:
        stat_age = Report.getActivityAge(date_beg, date_end, type_ana)
    except Exception as err:
        Automation.log.error(Logs.fileline() + " : activity Report.getActivityAge failed err=" + str(err))
        return {
            'status': 'error',
            'rows_count': len(stat_type),
            'output_uri': None,
            'message': 'Report.getActivityAge failed',
            'error_trace': str(err),
        }

    if not stat_age:
        Automation.log.error(Logs.fileline() + " : activity stat_age empty")
        stat_age = []

    # Family label (same logic as PdfActivityReport)
    Various.useLangDB()
    try:
        type_ana_int = int(type_ana)
    except Exception:
        type_ana_int = 0

    family_label = ''
    if type_ana_int > 0:
        try:
            dico_row = Various.getDicoById(type_ana_int)
        except Exception:
            Automation.log.exception(Logs.fileline() + " : activity getDicoById failed")
            dico_row = None
        if dico_row and 'label' in dico_row:
            family_label = dico_row['label']

    # Translate analysis label for type stats
    Various.useLangDB()
    for row in stat_type:
        ana = row.get('analysis') or ''
        row['analysis'] = _(ana.strip())

    # Translate and normalize age for age stats
    Various.useLangDB()
    for row in stat_age:
        ana = row.get('analysis') or ''
        row['analysis'] = _(ana.strip())

        unit = row.get('unite')
        age = row.get('age')
        if age is not None:
            try:
                if unit == 1034:
                    row['age'] = int(age // 365)
                elif unit == 1035:
                    row['age'] = int(age // 52)
                elif unit == 1036:
                    row['age'] = int(age // 12)
            except Exception:
                # Silent failure, keep original age
                Automation.log.exception(Logs.fileline() + " : activity age normalize failed unit=" + str(unit) + " age=" + str(age))

    # Replace None by empty string (same as PdfActivityReport)
    for row in stat_type:
        for k, v in list(row.items()):
            if v is None:
                row[k] = ''

    for row in stat_age:
        for k, v in list(row.items()):
            if v is None:
                row[k] = ''

    # If no data at all => no PDF, optional internal message
    if len(stat_type) == 0 and len(stat_age) == 0:
        Automation.log.info(Logs.fileline() + " : no activity data -> skip PDF generation")

        send_msg = (params.get('activity_internal_msg') or "N").upper()
        receiver = int(params.get('activity_internal_recipient') or 0)

        if send_msg == "Y" and receiver > 0:
            try:
                Various.useLangPDF()

                title = _("Rapport d'activité")
                body = _("Aucune donnée d'activité pour la période sélectionnée.")

                sender = job_row.get("ajb_created_by") or 0
                msg_id = _send_internal_message(sender, receiver, title, body)

            except Exception:
                Automation.log.exception(Logs.fileline() + " : activity no-data internal msg failed")

        return {
            'status': 'success',
            'rows_count': 0,
            'output_uri': None,
            'message': 'no activity data for this period',
            'error_trace': None,
        }

    # Prevent Relatorio crashes if one list is empty
    if len(stat_type) == 0:
        stat_type = [{'analysis': '', 'M': 0, 'F': 0, 'U': 0, 'total': 0}]

    if len(stat_age) == 0:
        stat_age = [{'analysis': '', 'age': '', 'M': 0, 'F': 0, 'U': 0, 'total': 0}]

    beg_short = date_beg_dt.strftime('%Y-%m-%d')
    end_short = date_end_dt.strftime('%Y-%m-%d')

    # CSV by TYPE
    if output_mode == 'csv_type':
        tmp_path = os.path.join(Constants.cst_path_tmp, f"activity_type_{beg_short}_{end_short}.csv")

        # Aggregation: key = (code, name)
        # values: ext_M/F/U, inp_M/F/U, onc_M/F/U, tot_M/F/U
        agg = {}

        for row in stat_type:
            code = str(row.get('code') or '').strip()
            name = str(row.get('analysis') or '').strip()
            if not code and not name:
                continue

            key = (code, name)
            if key not in agg:
                agg[key] = {
                    'ext_M': 0, 'ext_F': 0, 'ext_U': 0,
                    'inp_M': 0, 'inp_F': 0, 'inp_U': 0,
                    'onc_M': 0, 'onc_F': 0, 'onc_U': 0,
                    'tot_M': 0, 'tot_F': 0, 'tot_U': 0,
                }

            # --- sex: 1 = M, 2 = F, 3 = U ---
            sex_raw = row.get('sex')
            try:
                sex_code = int(sex_raw)
            except (TypeError, ValueError):
                # fallback si jamais on reçoit déjà 'M'/'F'/'U'
                sex_txt = str(sex_raw or '').upper()
                if sex_txt in ('M', 'F', 'U'):
                    sex = sex_txt
                else:
                    continue
            else:
                if sex_code == 1:
                    sex = 'M'
                elif sex_code == 2:
                    sex = 'F'
                elif sex_code == 3:
                    sex = 'U'
                else:
                    continue

            # --- rec_type: 184 = externe, 183 = interne ---
            rec_type_raw = row.get('rec_type')
            try:
                rec_type_code = int(rec_type_raw)
            except (TypeError, ValueError):
                rec_type_code = 0

            is_external = (rec_type_code == 184)
            is_internal = (rec_type_code == 183)

            # --- on-call: rec_custody == 'Y' ---
            custody = str(row.get('rec_custody') or '').upper()
            is_oncall = (custody == 'Y')

            try:
                nb = int(row.get('nb_ana') or 0)
            except (TypeError, ValueError):
                nb = 0
            if nb <= 0:
                continue

            # Fill buckets
            if is_external:
                agg[key]['ext_' + sex] += nb
            if is_internal:
                agg[key]['inp_' + sex] += nb
            if is_oncall:
                agg[key]['onc_' + sex] += nb

            agg[key]['tot_' + sex] += nb

        # Écriture CSV
        try:
            with open(tmp_path, "w", encoding="utf-8") as f:
                f.write("code;nom;ext_M;ext_F;ext_U;inp_M;inp_F;inp_U;onc_M;onc_F;onc_U;tot_M;tot_F;tot_U\n")
                for (code, name), vals in sorted(agg.items(), key=lambda x: x[0][1]):
                    f.write(
                        f"{code};{name};"
                        f"{vals['ext_M']};{vals['ext_F']};{vals['ext_U']};"
                        f"{vals['inp_M']};{vals['inp_F']};{vals['inp_U']};"
                        f"{vals['onc_M']};{vals['onc_F']};{vals['onc_U']};"
                        f"{vals['tot_M']};{vals['tot_F']};{vals['tot_U']}\n"
                    )
        except Exception as err:
            Automation.log.error(Logs.fileline() + " : csv_type writing failed err=" + str(err))
            return {
                'status': 'error',
                'rows_count': len(stat_type),
                'output_uri': None,
                'message': 'csv_type write failed',
                'error_trace': str(err),
            }

        # Move + register file
        try:
            final_path, md5_name, file_size = _write_file_safe(
                tmp_path,
                Constants.cst_activity_upload
            )
        except Exception as err:
            Automation.log.error(Logs.fileline() + " : csv_type _write_file_safe err=" + str(err))
            return {
                'status': 'error',
                'rows_count': len(stat_type),
                'output_uri': None,
                'message': '_write_file_safe failed for csv_type',
                'error_trace': str(err),
            }

        owner_id = job_row.get("ajb_created_by") or 0
        file_id = _ensure_file_record(
            generated_name=md5_name,
            original_name=f"activity_type_{beg_short}_{end_short}.csv",
            file_size=file_size,
            owner_id=owner_id,
            path="activity/",
            ext="csv",
            content_type=Constants.cst_content_type_csv,
        )

        # Optional internal message
        if send_msg == "Y" and receiver > 0:
            title = _("Rapport d'activité - CSV par type")
            body = _("Le fichier CSV (analyses par type) a été généré pour la période %(beg)s → %(end)s.") % {
                "beg": beg_short, "end": end_short
            }
            msg_id = _send_internal_message(sender, receiver, title, body)
            if msg_id > 0 and file_id:
                _attach_file_to_message(
                    msg_id, md5_name,
                    f"activity_type_{beg_short}_{end_short}.csv",
                    file_size,
                    sender,
                    ext="csv",
                    content_type=Constants.cst_content_type_csv,
                    path="activity/",
                )

        return {
            'status': 'success',
            'rows_count': len(stat_type),
            'output_uri': final_path,
            'message': 'csv_type generated',
            'error_trace': None,
        }

    # CSV by AGE
    if output_mode == 'csv_age':
        tmp_path = os.path.join(Constants.cst_path_tmp, f"activity_age_{beg_short}_{end_short}.csv")

        # agg_age[(code, name)] = dict with col1_M/F/U ... tot_M/F/U
        agg_age = {}

        def _age_band(age_val):
            """Return 1..4 selon la tranche (à adapter si besoin)."""
            try:
                a = int(age_val)
            except (TypeError, ValueError):
                return None
            # Exemple de découpage (à adapter à ton HTML si différent)
            if a < 5:
                return 1
            elif a < 15:
                return 2
            elif a < 45:
                return 3
            else:
                return 4

        for row in stat_age:
            code = str(row.get('code') or '').strip()
            name = str(row.get('analysis') or '').strip()
            if not code and not name:
                continue

            key = (code, name)
            if key not in agg_age:
                agg_age[key] = {
                    'col1_M': 0, 'col1_F': 0, 'col1_U': 0,
                    'col2_M': 0, 'col2_F': 0, 'col2_U': 0,
                    'col3_M': 0, 'col3_F': 0, 'col3_U': 0,
                    'col4_M': 0, 'col4_F': 0, 'col4_U': 0,
                    'tot_M': 0,  'tot_F': 0,  'tot_U': 0,
                }

            # age en jours/semaines/mois selon unite, tu avais déjà normalisé plus haut
            band = _age_band(row.get('age'))
            if band not in (1, 2, 3, 4):
                continue

            # sex: 1/2/3 -> M/F/U (même logique que csv_type)
            sex_raw = row.get('sex')
            try:
                sex_code = int(sex_raw)
            except (TypeError, ValueError):
                sex_txt = str(sex_raw or '').upper()
                if sex_txt in ('M', 'F', 'U'):
                    sex = sex_txt
                else:
                    continue
            else:
                if sex_code == 1:
                    sex = 'M'
                elif sex_code == 2:
                    sex = 'F'
                elif sex_code == 3:
                    sex = 'U'
                else:
                    continue

            try:
                nb = int(row.get('nb_ana') or 0)
            except (TypeError, ValueError):
                nb = 0
            if nb <= 0:
                continue

            agg_age[key][f'col{band}_{sex}'] += nb
            agg_age[key][f'tot_{sex}'] += nb

        try:
            with open(tmp_path, "w", encoding="utf-8") as f:
                f.write("code;nom;col1_M;col1_F;col1_U;col2_M;col2_F;col2_U;col3_M;col3_F;col3_U;col4_M;col4_F;col4_U;tot_M;tot_F;tot_U\n")

                for (code, name), vals in sorted(agg_age.items(), key=lambda x: x[0][1]):
                    f.write(
                        f"{code};{name};"
                        f"{vals['col1_M']};{vals['col1_F']};{vals['col1_U']};"
                        f"{vals['col2_M']};{vals['col2_F']};{vals['col2_U']};"
                        f"{vals['col3_M']};{vals['col3_F']};{vals['col3_U']};"
                        f"{vals['col4_M']};{vals['col4_F']};{vals['col4_U']};"
                        f"{vals['tot_M']};{vals['tot_F']};{vals['tot_U']}\n"
                    )
        except Exception as err:
            Automation.log.error(Logs.fileline() + " : csv_age writing failed err=" + str(err))
            return {
                'status': 'error',
                'rows_count': len(stat_age),
                'output_uri': None,
                'message': 'csv_age write failed',
                'error_trace': str(err),
            }

        # Move + register file
        try:
            final_path, md5_name, file_size = _write_file_safe(
                tmp_path,
                Constants.cst_activity_upload
            )
        except Exception as err:
            Automation.log.error(Logs.fileline() + " : csv_age _write_file_safe err=" + str(err))
            return {
                'status': 'error',
                'rows_count': len(stat_age),
                'output_uri': None,
                'message': '_write_file_safe failed for csv_age',
                'error_trace': str(err),
            }

        owner_id = job_row.get("ajb_created_by") or 0
        file_id = _ensure_file_record(
            generated_name=md5_name,
            original_name=f"activity_age_{beg_short}_{end_short}.csv",
            file_size=file_size,
            owner_id=owner_id,
            path="activity/",
            ext="csv",
            content_type=Constants.cst_content_type_csv,
        )

        # Internal message
        if send_msg == "Y" and receiver > 0:
            title = _("Rapport d'activité - CSV par âge")
            body = _("Le fichier CSV (analyses par âge) a été généré pour la période %(beg)s → %(end)s.") % {
                "beg": beg_short, "end": end_short
            }
            msg_id = _send_internal_message(sender, receiver, title, body)
            if msg_id > 0 and file_id:
                _attach_file_to_message(
                    msg_id, md5_name,
                    f"activity_age_{beg_short}_{end_short}.csv",
                    file_size,
                    sender,
                    ext="csv",
                    content_type=Constants.cst_content_type_csv,
                    path="activity/",
                )

        return {
            'status': 'success',
            'rows_count': len(stat_age),
            'output_uri': final_path,
            'message': 'csv_age generated',
            'error_trace': None,
        }

    # Build safe filename
    base_name = params.get('activity_filename') or 'activity_report'
    safe_name = f"{base_name}_{beg_short}_{end_short}"
    safe_name = re.sub(SAFE, "_", safe_name).strip("_")[:80]

    # Generate PDF in tmp
    try:
        ok = Pdf.getPdfActivityReport(stat_type, stat_age, date_beg, date_end, tpl_file, safe_name, family_label)
        if not ok:
            msg = "Pdf.getPdfActivityReport failed"
            Automation.log.error(Logs.fileline() + " : " + msg)
            return {
                'status': 'error',
                'rows_count': len(stat_type) + len(stat_age),
                'output_uri': None,
                'message': msg,
                'error_trace': None,
            }
    except Exception as err:
        Automation.log.error(Logs.fileline() + " : activity PDF exception " + str(err))
        return {
            'status': 'error',
            'rows_count': 0,
            'output_uri': None,
            'message': 'exception in Pdf.getPdfActivityReport',
            'error_trace': str(err),
        }

    tmp_file = os.path.join(Constants.cst_path_tmp, safe_name + ".pdf")

    # Move to upload/activity/ with MD5 hashed name
    try:
        final_path, md5_name, file_size = _write_file_safe(
            tmp_file,
            Constants.cst_activity_upload
        )
    except Exception as err:
        Automation.log.error(Logs.fileline() + " : activity _write_file_safe error = " + str(err))
        return {
            'status': 'error',
            'rows_count': len(stat_type) + len(stat_age),
            'output_uri': None,
            'message': 'file move/hash error',
            'error_trace': str(err),
        }

    # Ensure sigl_file_data entry
    owner_id = job_row.get("ajb_created_by") or 0
    file_id = _ensure_file_record(
        generated_name=md5_name,
        original_name=safe_name + ".pdf",
        file_size=file_size,
        owner_id=owner_id,
        path="activity/",
        ext="pdf",
        content_type=Constants.cst_content_type_pdf,
    )

    # Optional internal messaging
    send_msg = (params.get('activity_internal_msg') or "N").upper()
    receiver = int(params.get('activity_internal_recipient') or 0)

    if send_msg == "Y" and receiver > 0:
        try:
            Various.useLangPDF()

            title = _("Rapport d'activité")
            body = _("Le rapport d'activité a été généré pour la période %(beg)s → %(end)s.") % {
                "beg": beg_short,
                "end": end_short
            }

            sender = job_row.get("ajb_created_by") or 0
            msg_id = _send_internal_message(sender, receiver, title, body)

            if msg_id > 0 and file_id:
                _attach_file_to_message(
                    msg_id,
                    md5_name,
                    safe_name + ".pdf",
                    file_size,
                    sender,
                    ext="pdf",
                    content_type=Constants.cst_content_type_pdf,
                    path="activity/",
                )
        except Exception:
            Automation.log.exception(Logs.fileline() + " : activity internal msg failed")

    return {
        'status': 'success',
        'rows_count': len(stat_type) + len(stat_age),
        'output_uri': final_path,
        'message': 'activity pdf generated',
        'error_trace': None,
    }


def _send_internal_message(sender_id: int, receiver_id: int, title: str, body: str) -> int:
    """Send message in internal_messaging table via Quality model."""
    try:
        from app.models.Quality import Quality  # lazy import to avoid cycles
        msg_id = Quality.insertMessage(id_user=sender_id, receiver=receiver_id, title=title, message=body)
        if msg_id > 0:
            Automation.log.info(Logs.fileline() + " : internal message sent to user_id=" + str(receiver_id) + " msg_id=" + str(msg_id))
        else:
            Automation.log.error(Logs.fileline() + " : internal messaging insertMessage error")
        return msg_id
    except Exception:
        Automation.log.exception(Logs.fileline() + " : internal messaging failed")
        return 0


def _ensure_file_record(generated_name: str,
                        original_name: str,
                        file_size: int,
                        owner_id: int,
                        path: str,
                        ext: str,
                        content_type: str) -> int:
    """Ensure there is a row in sigl_file_data for this generated_name."""
    if not generated_name:
        return 0

    cursor = DB.cursor()
    try:
        cursor.execute(
            "select id_data from sigl_file_data where generated_name = %s",
            (generated_name,)
        )
        row = cursor.fetchone()
        if row and row.get('id_data'):
            return int(row['id_data'])
    except Exception:
        Automation.log.exception(Logs.fileline() + " : _ensure_file_record select")

    try:
        from app.models.File import File

        storage_row = File.getFileStorage(1)
        if not storage_row or not storage_row.get('id_data') or not storage_row.get('path'):
            Automation.log.error(Logs.fileline() + " : _ensure_file_record no storage row")
            return 0

        file_params = {
            'id_owner': owner_id,
            'original_name': original_name,
            'generated_name': generated_name,
            'size': file_size,
            'hash': generated_name,
            'ext': ext,
            'content_type': content_type,
            'id_storage': storage_row['id_data'],
            'path': path,
        }

        file_id = File.insertFileData(**file_params)
        if not file_id:
            Automation.log.error(Logs.fileline() + " : _ensure_file_record insertFileData failed")
            return 0

        return int(file_id)
    except Exception:
        Automation.log.exception(Logs.fileline() + " : _ensure_file_record failed")
        return 0


def _attach_file_to_message(message_id: int,
                            generated_name: str,
                            original_name: str,
                            file_size: int,
                            sender_id: int,
                            ext: str,
                            content_type: str,
                            path: str) -> None:
    """Attach existing (or ensured) file to an internal message."""
    try:
        file_id = _ensure_file_record(
            generated_name=generated_name,
            original_name=original_name,
            file_size=file_size,
            owner_id=sender_id,
            path=path,
            ext=ext,
            content_type=content_type,
        )
        if not file_id:
            Automation.log.error(Logs.fileline() + " : _attach_file_to_message no file_id")
            return

        from app.models.File import File

        link_params = {
            'id_owner': sender_id,
            'id_ext': message_id,
            'id_file': file_id,
            'type_ref': 'MSG',
        }
        File.insertFileDoc(**link_params)
    except Exception:
        Automation.log.exception(Logs.fileline() + " : _attach_file_to_message failed")


def _execute_job_ssh(job_row: dict) -> dict:
    params = job_row.get('ajb_params') or {}
    if isinstance(params, str):
        try:
            params = json.loads(params)
        except Exception:
            params = {}

    cmd = params.get('command')
    if not cmd:
        return {'status': 'error', 'rows_count': 0, 'output_uri': None,
                'message': 'missing ssh command', 'error_trace': None}

    try:
        rc = os.system(cmd + " > /storage/io/ntp_status.out 2>&1")
        with open("/storage/io/ntp_status.out", "r") as f:
            content = f.read().strip()
        synced = 1 if rc == 0 else 0

        audit_flag = (params.get('audit') or 'N').upper() == 'Y'
        if audit_flag:
            try:
                # No request context in scheduler => do NOT rely on client_ip, Audit.py does.
                # We still call it and log if it fails.
                Audit.insertAudit(
                    None,
                    "NTP_STATUS",
                    "SYSTEM",
                    str(job_row.get('ajb_ser') or ''),
                    "SUCCESS" if synced else "ERROR",
                    {"synced": synced, "output": content},
                    "E"
                )
            except Exception:
                Automation.log.exception(Logs.fileline() + ' : _execute_job_ssh Audit.insertAudit failed')

        return {
            'status': 'success' if synced else 'error',
            'rows_count': 0,
            'output_uri': None,
            'message': content,
            'error_trace': None
        }

    except Exception as err:
        return {
            'status': 'error',
            'rows_count': 0,
            'output_uri': None,
            'message': 'ssh execution failed',
            'error_trace': str(err)
        }


def _first_day_utc(dt: datetime) -> datetime:
    """Return the first day of the month at 00:00:00 UTC."""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)
    return dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)


def _add_months_dt(dt: datetime, months: int) -> datetime:
    """
    Add/subtract months without external dependencies
    Example: months=-12 means "12 months earlier".
    """
    year = dt.year + (dt.month - 1 + months) // 12
    month = (dt.month - 1 + months) % 12 + 1
    day = min(dt.day, calendar.monthrange(year, month)[1])
    return dt.replace(year=year, month=month, day=day)


def _execute_job_audit_purge(job_row: dict) -> dict:
    """
    Automatic monthly archive + purge for the audit_trail table.

    Retention rule:
    - Setting: sigl_06_data.identifiant = 'audit_purge_months'
    - If months=12: keep the last 12 months in DB.
    - Data strictly older than the cutoff is archived to files then deleted.

    Files are written into: /storage/resource/audit/
    One file per archived month (JSONL format).
    """

    # 1) Read retention months from settings table
    row = Various.getDefaultValue('audit_purge_months')
    raw = (row.get('value') if row else None)

    try:
        months = int(raw) if raw is not None and str(raw).strip() != '' else 0
    except Exception:
        months = 0

    if months <= 0:
        # Disabled
        return {"status": "success", "rows_count": 0, "output_uri": None, "message": "disabled (months<=0)", "error_trace": None}

    Automation.log.info(Logs.fileline() + " : Audit auto archive/purge start months=" + str(months))

    # 2) Compute cutoff date (UTC)
    # month0 = first day of current month at 00:00:00
    now_utc = datetime.now(timezone.utc)
    month0 = _first_day_utc(now_utc)

    # cutoff = first day of current month minus N months
    # Example (month0=2026-01-01, months=12) => cutoff=2025-01-01
    cutoff = _add_months_dt(month0, -months)

    # 3) Ensure output directory exists
    base_path = Constants.cst_audit
    os.makedirs(base_path, exist_ok=True)

    # 4) Find if there is anything older than cutoff
    cursor = DB.cursor()
    cursor.execute(
        "SELECT MIN(aud_date_utc) AS min_dt FROM audit_trail WHERE aud_date_utc < %s",
        [cutoff.strftime('%Y-%m-%d %H:%M:%S')]
    )
    r = cursor.fetchone() or {}
    cursor.close()

    min_dt = r.get('min_dt')
    if not min_dt:
        Automation.log.info(Logs.fileline() + " : Audit auto archive/purge nothing to do cutoff=" + cutoff.strftime('%Y-%m-%d %H:%M:%S'))
        return {"status": "success", "rows_count": 0, "output_uri": None, "message": "nothing to purge", "error_trace": None}

    # 5) Start archiving month by month, from the month of the oldest record
    if not isinstance(min_dt, datetime):
        min_dt = datetime.strptime(str(min_dt), '%Y-%m-%d %H:%M:%S')

    iter_start = _first_day_utc(min_dt)

    total_archived = 0
    total_purged = 0
    last_file = None
    audit_date_beg = None
    audit_date_end = None

    while iter_start < cutoff:
        next_month = _add_months_dt(iter_start, 1)
        period_end = next_month if next_month < cutoff else cutoff

        date_beg_utc = iter_start.strftime('%Y-%m-%d 00:00:00')
        date_end_utc = (period_end - timedelta(seconds=1)).strftime('%Y-%m-%d %H:%M:%S')

        filename = (
            "audit-archive_" +
            iter_start.strftime("%Y%m%d") + "_" +
            (period_end - timedelta(seconds=1)).strftime("%Y%m%d") +
            "_purge.jsonl"
        )
        fullpath = os.path.join(base_path, filename)

        archived_count = 0
        c = DB.cursor()
        c.execute(
            """
            SELECT aud_ser, aud_date_utc, aud_user_login, aud_user_display, aud_user_role,
                   aud_resource_type, aud_resource_id, aud_action, aud_client_ip,
                   aud_status, aud_details, aud_event_type
            FROM audit_trail
            WHERE aud_date_utc BETWEEN %s AND %s
            ORDER BY aud_date_utc, aud_ser
            """,
            [date_beg_utc, date_end_utc]
        )

        with open(fullpath, "w", encoding="utf-8") as f:
            while True:
                batch = c.fetchmany(1000)
                if not batch:
                    break
                for row in batch:
                    rr = dict(row)
                    if rr.get("aud_date_utc"):
                        rr["aud_date_utc"] = rr["aud_date_utc"].strftime("%Y-%m-%d %H:%M:%S")
                    f.write(json.dumps(rr, ensure_ascii=False, default=str) + "\n")
                    archived_count += 1

        c.close()

        if archived_count <= 0:
            try:
                os.remove(fullpath)
            except Exception:
                Automation.log.exception(Logs.fileline() + " : Audit auto archive/purge remove file failed path=" + str(fullpath))
            iter_start = next_month
            continue

        purged = Audit.purgeAuditByPeriod(date_beg_utc, date_end_utc)
        purged = int(purged or 0)

        Automation.log.info(Logs.fileline() + " : Audit auto archive/purge month done rows=" + str(archived_count) + " purged=" + str(purged))

        total_archived += archived_count
        total_purged += purged
        last_file = fullpath

        if audit_date_beg is None:
            audit_date_beg = date_beg_utc
        audit_date_end = date_end_utc

        iter_start = next_month

    if total_archived > 0:
        details = {
            "context": "AUDIT_AUTO_ARCHIVE_PURGE",
            "date_beg": audit_date_beg,
            "date_end": audit_date_end,
            "archived_rows": total_archived,
            "purged_rows": total_purged,
            "cutoff": cutoff.strftime('%Y-%m-%d %H:%M:%S'),
        }
        try:
            Audit.insertAudit(None, "AuditAutoArchivePurge", "AUDIT", None, "SUCCESS", details, "E")
        except Exception:
            Automation.log.exception(Logs.fileline() + " : Audit auto archive/purge audit insert failed")

    return {
        "status": "success",
        "rows_count": total_archived,
        "output_uri": last_file,
        "message": f"archived={total_archived} purged={total_purged}",
        "error_trace": None
    }


def _execute_job(job_row: dict) -> dict:
    """Dispatch execution by job type."""
    ajb_type = (job_row.get('ajb_type') or '').lower()
    params = job_row.get('ajb_params') or {}

    if isinstance(params, str):
        try:
            params = json.loads(params)
        except Exception:
            params = {}

    if ajb_type == 'dhis2':
        mode = (params.get('dhis2_mode') or 'create').lower()
        if mode == 'create':
            return _execute_job_dhis2_create(job_row)
        if mode == 'send':
            return _execute_job_dhis2_send(job_row)
        return {
            'status': 'error',
            'rows_count': 0,
            'output_uri': None,
            'message': 'unknown dhis2_mode=' + mode,
            'error_trace': None,
        }

    if ajb_type == 'billing':
        return _execute_job_billing(job_row)

    if ajb_type == 'activity':
        return _execute_job_activity(job_row)

    if ajb_type == 'system':
        job_kind = (params.get('type') or '').lower()
        if job_kind == 'ssh':
            return _execute_job_ssh(job_row)

        if job_kind == 'audit_purge':
            return _execute_job_audit_purge(job_row)

        return {
            'status': 'error',
            'rows_count': 0,
            'output_uri': None,
            'message': 'unknown system job type=' + job_kind,
            'error_trace': None,
        }

    return {
        'status': 'error',
        'rows_count': 0,
        'output_uri': None,
        'message': 'unsupported ajb_type=' + str(job_row.get('ajb_type')),
        'error_trace': None,
    }
