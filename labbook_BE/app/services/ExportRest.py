# -*- coding:utf-8 -*-
import logging
import csv
import re

from datetime import datetime, timedelta
from flask import request
from flask_restful import Resource
from pathlib import Path
from io import StringIO

from app.models.General import compose_ret
from app.models.Constants import Constants
from app.models.Audit import Audit
from app.models.Various import Various
from app.models.Export import Export
from app.models.Report import Report
from app.models.Logs import Logs
from app.models.User import User
from app.models.Setting import Setting
from app.security.oauth_routes import require_oauth


def get_dhis2_orgunit_storedby(l_cols, l_rows, id_user):
    """
    Resolve the DHIS2 'orgunit' and 'storedby' values from the epidemio spreadsheet.
    Both fall back on a default when the sheet leaves them empty: the lab header for
    orgunit, the requesting user for storedby. Shared by the file and API exports.
    """
    # Determine orgunit
    orgunit = ''

    idx_orgunit = l_cols.index("orgunit")

    if idx_orgunit:
        orgunit = l_rows[1][idx_orgunit]

    if not orgunit:
        lab = Various.getDefaultValue('entete_1')

        if lab:
            orgunit = lab['value']

    # Determine storedby
    storedby = ''

    idx_storedby = l_cols.index("storedby")

    if idx_storedby:
        storedby = l_rows[1][idx_storedby]

    if not storedby:
        user = User.getUserDetails(id_user)

        if user:
            storedby = user['firstname'] + user['lastname']

    # remove space
    storedby = storedby.replace(' ', '')

    return orgunit, storedby


def build_dhis2_list_data(filename, l_period, rec_type, lite_filter, caller):
    """
    Build the exported rows for the four LIST_* reports, header row included.
    Returns (l_data, initial_len), or (None, 0) when filename is not one of them:
    the caller then falls back on the spreadsheet-driven export.
    'caller' only names the calling resource in the log lines.
    """
    log = logging.getLogger('log_services')

    if filename == "LIST_OUTSOURCING":
        log.error(Logs.fileline() + ' : TRACE ' + caller + ' LIST_OUTSOURCING')

        # Data headers
        l_data = [["period", "code patient", "record number", "record date", "analysis outsourced", "LabBook Lite"]]

        for period in l_period:
            l_rows = Export.getListOutsourcing(period[1], period[2], rec_type, lite_filter)

            for row in (l_rows or []):
                data = []

                code = str(row['code'])

                if row['code_patient']:
                    code += ' / ' + str(row['code_patient'])

                num_rec = str(row['num_dos_an'])

                date_rec = str(row['date_rec'])

                ana_outsourced = str(row['ana_code']) + ' ' + str(row['ana_name'])

                lite_flag = 'Y' if (row.get('rec_lite') or 0) > 0 else 'N'

                data.append(period[0])
                data.append(code)
                data.append(num_rec)
                data.append(date_rec)
                data.append(ana_outsourced)
                data.append(lite_flag)

                l_data.append(data)

    elif filename == "LIST_EEQ":
        log.error(Logs.fileline() + ' : TRACE ' + caller + ' LIST_EEQ')

        # Data headers
        l_data = [["period", "control name", "control date",  "supplier", "result date", "result", "comment"]]

        for period in l_period:
            l_rows = Export.getListEEQ(period[1], period[2])

            for row in (l_rows or []):
                result_map = {'Y': 'Conforme', 'N': 'Non conforme', 'U': 'Autres'}
                result = result_map.get(row.get('cte_conform'), '')

                data = []

                data.append(period[0])
                data.append(row.get('ctq_name'))
                data.append(row.get('ctq_date'))
                data.append(row.get('cte_date'))
                data.append(row.get('cte_organizer'))
                data.append(result)
                data.append(row.get('cte_comment'))

                l_data.append(data)

    elif filename == "LIST_EQUIPMENT_FAILURE":
        log.error(Logs.fileline() + ' : TRACE ' + caller + ' LIST_EQUIPMENT_FAILURE')

        l_data = [["period", "Equipment name", "Manufacturer name", "Supplier name", "Inventory number", "Date of failure", "Comment"]]

        for period in l_period:
            l_rows = Export.getListEqpFailure(period[1], period[2])

            for row in (l_rows or []):
                data = []

                data.append(period[0])
                data.append(row.get('eqp_name'))
                data.append(row.get('eqp_manufacturer'))
                data.append(row.get('supplier_name'))
                data.append(row.get('eqp_invent_num'))
                data.append(row.get('eqf_date'))
                data.append(row.get('eqf_comm'))

                l_data.append(data)

    elif filename == "LIST_STOCK_STATUS":
        log.error(Logs.fileline() + ' : TRACE ' + caller + ' LIST_STOCK')

        l_data = [["period", "product name", "Expiration status", "Quantity status"]]

        for period in l_period:
            l_rows = Export.getListStockStatus(period[1], period[2])

            for row in (l_rows or []):
                l_data.append([
                    period[0],
                    str(row.get('prd_name') or ''),
                    str(row.get('exp_status') or ''),
                    str(row.get('qty_status') or '')
                ])

    else:
        return None, 0

    # The header row is the only content when no data row was appended
    return l_data, 1


def fill_dhis2_rows(l_data, l_rows, l_period, version, orgunit, storedby, rec_type, lite_filter, caller):
    """
    Append one exported row per (period, spreadsheet row) pair to l_data.
    The exported value comes either from a parsed formula or from a statistic query,
    depending on the filter column of the row.
    l_rows is consumed: its header line is removed.
    'caller' only names the calling resource in the log lines.
    """
    log = logging.getLogger('log_services')

    date_now = datetime.now()

    if not l_rows:
        return l_data

    # remove headers line
    l_rows.pop(0)

    for period in l_period:
        for row in l_rows:

            # in case of an empty line
            if not row or all(str(c).strip() == '' for c in row):
                continue

            if row:
                data = []

                if version == 'v3':
                    data.append(row[0])
                    data.append(period[0])
                    data.append(orgunit)
                    data.append(row[4])
                    data.append(row[5])
                else:
                    data.append(row[0])
                    data.append(period[0])
                    data.append(orgunit)
                    data.append(row[5])
                    data.append(row[6])

                period_beg_db = period[1]
                period_end_db = period[2]

                if version == 'v3':
                    filter_row = row[2].strip()
                else:
                    filter_row = row[3].strip()

                # --- check if formula or others statistic object  ---
                # formula case
                # if filter_row.startswith("$") or filter_row.startswith("{") or filter_row.startswith("( "):
                if filter_row.startswith("$") or filter_row.startswith("{") or filter_row.lstrip().startswith("("):
                    # Parse formula for result request
                    formula   = filter_row

                    if version == 'v3':
                        type_samp = row[3]
                    else:
                        type_samp = row[4]

                    log.error(Logs.fileline() + ' : TRACE ' + caller + ' --- before ParseFormula ---')
                    log.error(Logs.fileline() + ' : TRACE ' + caller + ' formula=%s', formula)
                    log.error(Logs.fileline() + ' : TRACE ' + caller + ' type_samp=%s', type_samp)

                    req_part = ''

                    req_part = Report.ParseFormula(formula, type_samp)

                    log.error(Logs.fileline() + ' : DEBUG ' + caller + ' req_part=%s', req_part)

                    result = Report.getResultEpidemio(req_part=req_part,
                                                      date_beg=period_beg_db,
                                                      date_end=period_end_db,
                                                      rec_type=rec_type,
                                                      lite_filter=lite_filter)

                    # result normalization
                    value_to_write = ''
                    if isinstance(result, dict):
                        value_to_write = result.get('value', '')
                    elif isinstance(result, (list, tuple)) and len(result) > 0:
                        value_to_write = result[0]
                    elif result is not None:
                        value_to_write = result
                    data.append(str(value_to_write) if value_to_write != '' else '')

                # statistic case
                else:
                    result = Export.getStatDHIS2(period_beg_db, period_end_db, filter_row, rec_type, lite_filter)

                    if result:
                        data.append(str(result['value']))
                    else:
                        data.append('')

                data.append(storedby)
                data.append(date_now.strftime("%Y-%m-%dT%H:%M:%S"))
                data.append('')
                data.append('FALSE')
                data.append('')

                l_data.append(data)

    return l_data


def build_dhis2_periods(args, audit_user, caller):
    """
    Validate the requested date range and build the list of periods to export.
    Returns the pair (l_period, error): error is None when all went well, otherwise
    it is the response the caller must return at once.
    caller names the calling resource in the logs and the audit trail.
    """
    log = logging.getLogger('log_services')

    period   = args['period']
    l_period = []

    try:
        date_beg = datetime.strptime(args['date_beg'], '%Y-%m-%d')
        date_end = datetime.strptime(args['date_end'], '%Y-%m-%d')
    except Exception as e:
        log.error(Logs.fileline() + ' : TRACE ' + caller + f' ERROR bad dates: {e}')
        try:
            details = {"result": "ERROR", "reason": "BAD_DATES", "date_beg": args.get('date_beg'),
                       "date_end": args.get('date_end'), "error": str(e)}
            Audit.insertAudit(audit_user, caller, "EXPORT", None, "ERROR", details, "R")
        except Exception as err:
            log.error(Logs.fileline() + ' : ' + caller + ' ERROR audit bad dates err=' + str(err))
        return compose_ret('', Constants.cst_content_type_json, 409)

    # build list of period
    if period == 'W':
        # Weekly: iterate Monday..Sunday blocks
        cur = date_beg
        while cur <= date_end:
            iso_year, iso_week, _ = cur.isocalendar()
            tmp_period = f"{iso_year}W{iso_week:02d}"
            cur_end = cur + timedelta(days=6)
            if cur_end > date_end:
                cur_end = date_end
            l_period.append([tmp_period, cur, cur_end])
            cur = cur + timedelta(days=7)

    elif period == 'M':
        # Monthly: 1st..last day of each month
        import calendar
        y, m = date_beg.year, date_beg.month
        while (y, m) <= (date_end.year, date_end.month):
            last_dom = calendar.monthrange(y, m)[1]
            cur_start = datetime(y, m, 1)
            cur_end   = datetime(y, m, last_dom)
            tmp_period = f"{y}{m:02d}"
            l_period.append([tmp_period, cur_start, cur_end])
            if m == 12:
                y, m = y + 1, 1
            else:
                m = m + 1

    elif period in ('B', 'T', 'Q', 'S', 'A'):
        # Grouped periods; front already aligned range to group start
        import calendar
        span_map = {'B': 2, 'T': 3, 'Q': 4, 'S': 6, 'A': 12}
        span = span_map[period]

        y, m = date_beg.year, date_beg.month  # group start month
        while (y, m) <= (date_end.year, date_end.month):
            # Compute end of the group (inclusive)
            end_month_index = (m - 1) + (span - 1)
            y_end = y + (end_month_index // 12)
            m_end = (end_month_index % 12) + 1
            last_dom = calendar.monthrange(y_end, m_end)[1]
            cur_start = datetime(y, m, 1)
            cur_end   = datetime(y_end, m_end, last_dom)

            # Build period label with new formats
            if period == 'A':
                # Annual: YYYY
                tmp_period = f"{y}"
            elif period == 'S':
                # Semester: YYYYSn (n=1..2)
                idx = 1 if m <= 6 else 2
                tmp_period = f"{y}S{idx}"
            elif period == 'T':
                # Quarter: YYYYQn (n=1..4)
                idx = ((m - 1) // 3) + 1
                tmp_period = f"{y}Q{idx}"
            elif period == 'B':
                # Bi-monthly: YYYYiiB (ii=01..06)
                idx = ((m - 1) // 2) + 1
                tmp_period = f"{y}{idx:02d}B"
            else:  # period == 'Q'
                # Quadrimestrial: YYYYQnC (n=1..3)
                idx = ((m - 1) // 4) + 1
                tmp_period = f"{y}Q{idx}C"

            l_period.append([tmp_period, cur_start, cur_end])

            # Advance to next group start by 'span' months
            next_index = (m - 1) + span
            y, m = y + (next_index // 12), (next_index % 12) + 1

    else:
        log.error(Logs.fileline() + ' : TRACE ' + caller + ' ERROR wrong period : ' + Logs.clean(period))
        try:
            details = {"result": "ERROR", "reason": "WRONG_PERIOD", "period": str(period)}
            Audit.insertAudit(audit_user, caller, "EXPORT", None, "ERROR", details, "R")
        except Exception as err:
            log.error(Logs.fileline() + ' : ' + caller + ' ERROR audit wrong period err=' + str(err))
        return compose_ret('', Constants.cst_content_type_json, 409)

    return l_period, None


class ExportCSV(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        if 'filename' not in args or 'csv_str' not in args:
            self.log.error(Logs.fileline() + ' : TRACE ExportCSV ERROR args missing')
            try:
                details = {"result": "ERROR", "reason": "ARGS_MISSING", "missing": ["filename", "csv_str"]}
                Audit.insertAudit(audit_user, "ExportCSV", "EXPORT", None, "ERROR", details, "R")
            except Exception as err:
                self.log.error(Logs.fileline() + ' : ExportCSV ERROR audit args missing err=' + str(err))
            return compose_ret('', Constants.cst_content_type_json, 400)

        # write csv file
        try:
            # Ensure tmp directory exists
            tmp_dir = Path("tmp")
            tmp_dir.mkdir(parents=True, exist_ok=True)

            # Sanitize user-provided filename to prevent path traversal and invalid characters
            raw_name = str(args['filename'])
            safe_name = re.sub(r'[^A-Za-z0-9._-]+', '_', raw_name).strip('_') or 'export.csv'

            # Always build the path inside the controlled directory
            file_path = tmp_dir / safe_name

            # Write CSV content safely
            with file_path.open("w", encoding="utf-8", newline="") as f:
                f.write(args['csv_str'])

        except Exception as err:
            # Log error and return failure
            self.log.error(Logs.fileline() + ' : ERROR post ExportCSV failed, err=%s', err)
            try:
                details = {"result": "ERROR", "reason": "WRITE_FAILED", "filename": args.get('filename'), "error": str(err)}
                Audit.insertAudit(audit_user, "ExportCSV", "EXPORT", None, "ERROR", details, "R")
            except Exception as err2:
                self.log.error(Logs.fileline() + ' : ExportCSV ERROR audit write failed err=' + str(err2))
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE ExportCSV')
        try:
            details = {"result": "SUCCESS", "filename": args.get('filename')}
            Audit.insertAudit(audit_user, "ExportCSV", "EXPORT", None, "SUCCESS", details, "R")
        except Exception as err:
            self.log.error(Logs.fileline() + ' : ExportCSV ERROR audit success err=' + str(err))
        return compose_ret('', Constants.cst_content_type_json)


class ExportDHIS2(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        if 'date_beg' not in args or 'date_end' not in args or 'filename' not in args or 'id_user' not in args or \
           'period' not in args or 'rec_type' not in args or 'lite_filter' not in args:
            self.log.error(Logs.fileline() + ' : TRACE ExportDHIS2 ERROR args missing')
            try:
                details = {"result": "ERROR", "reason": "ARGS_MISSING",
                           "missing": ["date_beg", "date_end", "filename", "id_user", "period", "rec_type", "lite_filter"]}
                Audit.insertAudit(audit_user, "ExportDHIS2", "EXPORT", None, "ERROR", details, "R")
            except Exception as err:
                self.log.error(Logs.fileline() + ' : ExportDHIS2 ERROR audit args missing err=' + str(err))
            return compose_ret('', Constants.cst_content_type_json, 400)

        filename  = args['filename'][:-4]
        rec_type  = args['rec_type']
        lite_filter = args['lite_filter']

        l_period, err = build_dhis2_periods(args, audit_user, 'ExportDHIS2')
        if err:
            return err

        # dates already validated above, reused to build a safe file name
        date_beg = datetime.strptime(args['date_beg'], '%Y-%m-%d')
        date_end = datetime.strptime(args['date_end'], '%Y-%m-%d')

        # --- BUILD DATA ---

        # Pre-defined export
        l_data, initial_len = build_dhis2_list_data(filename, l_period, rec_type, lite_filter, 'ExportDHIS2')

        if l_data is None:
            # Data headers
            l_data = [["dataelement", "period", "orgunit", "categoryoptioncombo", "attributeoptioncombo", "value",
                       "storedby", "lastupdated", "comment", "followup", "deleted"]]
            initial_len = len(l_data)

            # Read CSV spreadsheet
            base_dir = Path(Constants.cst_dhis2).resolve()
            base_dir.mkdir(parents=True, exist_ok=True)

            safe_name = re.sub(Constants.cst_safe_pattern, '_', str(args['filename']))[:80]
            if not safe_name.lower().endswith('.csv'):
                safe_name += '.csv'

            csv_path = (base_dir / safe_name).resolve()

            if base_dir not in csv_path.parents:
                self.log.error(Logs.fileline() + ' : TRACE ExportDHIS2 ERROR invalid input path')
                try:
                    details = {"result": "ERROR", "reason": "INVALID_INPUT_PATH", "filename": args.get('filename')}
                    Audit.insertAudit(audit_user, "ExportDHIS2", "EXPORT", None, "ERROR", details, "R")
                except Exception as err:
                    self.log.error(Logs.fileline() + ' : ExportDHIS2 ERROR audit invalid input path err=' + str(err))
                return compose_ret('', Constants.cst_content_type_json, 400)

            with csv_path.open('r', encoding='utf-8', newline='') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=';')
                l_rows = list(csv_reader)

            if not l_rows or len(l_rows) < 2:
                self.log.error(Logs.fileline() + ' : TRACE ExportDHIS2 ERROR spreadsheet empty')
                try:
                    details = {"result": "ERROR", "reason": "SPREADSHEET_EMPTY", "filename": args.get('filename')}
                    Audit.insertAudit(audit_user, "ExportDHIS2", "EXPORT", None, "ERROR", details, "R")
                except Exception as err:
                    self.log.error(Logs.fileline() + ' : ExportDHIS2 ERROR audit spreadsheet empty err=' + str(err))
                return compose_ret('', Constants.cst_content_type_json, 500)

            l_cols = l_rows[0]  # keep first row to read l_cols of csv

            if "version" in l_cols:
                idx_version = l_cols.index("version")
                version = l_rows[1][idx_version]
                if version not in ("v1", "v2", "v3"):
                    self.log.error(Logs.fileline() + ' : TRACE ExportDHIS2 ERROR spreadsheet wrong version :' + str(version))
                    try:
                        details = {"result": "ERROR", "reason": "WRONG_VERSION", "version": str(version), "filename": args.get('filename')}
                        Audit.insertAudit(audit_user, "ExportDHIS2", "EXPORT", None, "ERROR", details, "R")
                    except Exception as err:
                        self.log.error(Logs.fileline() + ' : ExportDHIS2 ERROR audit wrong version err=' + str(err))
                    return compose_ret('', Constants.cst_content_type_json, 409)
            else:
                self.log.error(Logs.fileline() + ' : TRACE ExportDHIS2 ERROR spreadsheet not found version')
                try:
                    details = {"result": "ERROR", "reason": "VERSION_NOT_FOUND"}
                    Audit.insertAudit(audit_user, "ExportDHIS2", "EXPORT", None, "ERROR", details, "R")
                except Exception as err:
                    self.log.error(Logs.fileline() + ' : ExportDHIS2 ERROR audit version not found err=' + str(err))
                return compose_ret('', Constants.cst_content_type_json, 409)

            orgunit, storedby = get_dhis2_orgunit_storedby(l_cols, l_rows, args['id_user'])

            fill_dhis2_rows(l_data, l_rows, l_period, version, orgunit, storedby, rec_type, lite_filter, 'ExportDHIS2')

        # --- WRITE FILE ---
        # if no result to export
        if len(l_data) == initial_len:
            try:
                details = {"result": "ERROR", "reason": "NO_DATA",
                           "date_beg": args.get('date_beg'), "date_end": args.get('date_end'),
                           "filename": args.get('filename'), "period": args.get('period'),
                           "rec_type": args.get('rec_type'), "lite_filter": args.get('lite_filter')}
                Audit.insertAudit(audit_user, "ExportDHIS2", "EXPORT", None, "ERROR", details, "R")
            except Exception as err:
                self.log.error(Logs.fileline() + ' : ExportDHIS2 ERROR audit no data err=' + str(err))
            return compose_ret('', Constants.cst_content_type_json, 404)

        try:
            rec_suffix = '_rec-external' if rec_type == 'E' else (
                         '_rec-internal' if rec_type == 'I' else '_rec-all')

            # Lite suffix: A => '', N => '_without-Lite', Y => '_only-Lite'
            lf = (args.get('lite_filter', 'A') or 'A').upper()
            lite_suffix = '_without-Lite' if lf == 'N' else ('_only-Lite' if lf == 'Y' else '')

            # --- Build a SAFE filename; never trust raw user input ---
            # Use parsed dates (not raw args) to avoid injection
            beg_str = date_beg.strftime('%Y-%m-%d')
            end_str = date_end.strftime('%Y-%m-%d')

            # Keep only safe chars for {filename}; fallback to 'export' if empty
            safe_token = re.sub(Constants.cst_safe_pattern, '_', str(filename))[:64] or 'export'

            outname = f"dhis2_{safe_token}_{beg_str}-{end_str}{rec_suffix}{lite_suffix}.csv"

            # Fixed base directory + path traversal guard
            base_dir = Path('tmp').resolve()
            base_dir.mkdir(parents=True, exist_ok=True)  # ensure it exists

            outpath = (base_dir / outname).resolve()

            # Final guard: forbid escaping the base directory
            if base_dir not in outpath.parents:
                self.log.error(Logs.fileline() + ' : TRACE ExportDHIS2 ERROR invalid output path')
                try:
                    details = {"result": "ERROR", "reason": "INVALID_OUTPUT_PATH", "outname": outname}
                    Audit.insertAudit(audit_user, "ExportDHIS2", "EXPORT", None, "ERROR", details, "R")
                except Exception as err:
                    self.log.error(Logs.fileline() + ' : ExportDHIS2 ERROR audit invalid output path err=' + str(err))
                return compose_ret('', Constants.cst_content_type_json, 400)

            # Write CSV
            with outpath.open(mode='w', encoding='utf-8', newline='') as file:  # newline='' for csv module
                writer = csv.writer(file, delimiter=',')
                writer.writerows(l_data)

        except Exception as err:
            self.log.error(Logs.fileline() + ' : post ExportDHIS2 failed, err=%s', err)
            try:
                details = {"result": "ERROR", "reason": "WRITE_FAILED", "error": str(err)}
                Audit.insertAudit(audit_user, "ExportDHIS2", "EXPORT", None, "ERROR", details, "R")
            except Exception as err2:
                self.log.error(Logs.fileline() + ' : ExportDHIS2 ERROR audit write failed err=' + str(err2))
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE ExportDHIS2')
        try:
            details = {"result": "SUCCESS",
                       "date_beg": args.get('date_beg'), "date_end": args.get('date_end'),
                       "filename": args.get('filename'), "period": args.get('period'),
                       "rec_type": args.get('rec_type'), "lite_filter": args.get('lite_filter')}
            Audit.insertAudit(audit_user, "ExportDHIS2", "EXPORT", None, "SUCCESS", details, "R")
        except Exception as err:
            self.log.error(Logs.fileline() + ' : ExportDHIS2 ERROR audit success err=' + str(err))
        return compose_ret('', Constants.cst_content_type_json)


class ExportDHIS2Api(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        if 'date_beg' not in args or 'date_end' not in args or 'filename' not in args or 'id_user' not in args or \
           'period' not in args or 'rec_type' not in args or 'dhs_ser' not in args or 'dry_run' not in args or \
           'lite_filter' not in args:
            self.log.error(Logs.fileline() + ' : TRACE ExportDHIS2Api ERROR args missing')
            try:
                missing = []
                for k in ["date_beg", "date_end", "filename", "id_user", "period", "rec_type", "dhs_ser", "dry_run", "lite_filter"]:
                    if k not in args:
                        missing.append(k)
                details = {"result": "ERROR", "reason": "ARGS_MISSING", "missing": missing}
                Audit.insertAudit(audit_user, "ExportDHIS2Api", "EXPORT", None, "ERROR", details, "R")
            except Exception as err:
                self.log.error(Logs.fileline() + ' : ExportDHIS2Api ERROR audit args missing err=' + str(err))
            return compose_ret('', Constants.cst_content_type_json, 400)

        filename = args['filename'][:-4]
        rec_type = args['rec_type']
        lite_filter = args['lite_filter']

        l_period, err = build_dhis2_periods(args, audit_user, 'ExportDHIS2Api')
        if err:
            return err

        # --- BUILD DATA ---

        # Pre-defined export
        l_data, initial_len = build_dhis2_list_data(filename, l_period, rec_type, lite_filter, 'ExportDHIS2Api')

        if l_data is None:
            # Data headers
            l_data = [["dataelement", "period", "orgunit", "categoryoptioncombo", "attributeoptioncombo", "value",
                       "storedby", "lastupdated", "comment", "followup", "deleted"]]
            initial_len = len(l_data)

            # Read CSV spreadsheet
            base_dir = Path(Constants.cst_dhis2).resolve()
            base_dir.mkdir(parents=True, exist_ok=True)

            safe_name = re.sub(Constants.cst_safe_pattern, '_', str(args['filename']))[:80]
            if not safe_name.lower().endswith('.csv'):
                safe_name += '.csv'

            csv_path = (base_dir / safe_name).resolve()

            if base_dir not in csv_path.parents:
                self.log.error(Logs.fileline() + ' : TRACE ExportDHIS2 ERROR invalid input path')
                try:
                    details = {"result": "ERROR", "reason": "INVALID_INPUT_PATH"}
                    Audit.insertAudit(audit_user, "ExportDHIS2Api", "EXPORT", None, "ERROR", details, "R")
                except Exception as err:
                    self.log.error(Logs.fileline() + ' : ExportDHIS2Api ERROR audit invalid path err=' + str(err))
                return compose_ret('', Constants.cst_content_type_json, 400)

            with csv_path.open('r', encoding='utf-8', newline='') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=';')
                l_rows = list(csv_reader)

            if not l_rows or len(l_rows) < 2:
                self.log.error(Logs.fileline() + ' : TRACE ExportDHIS2Api ERROR spreadsheet empty')
                try:
                    details = {"result": "ERROR", "reason": "SPREADSHEET_EMPTY"}
                    Audit.insertAudit(audit_user, "ExportDHIS2Api", "EXPORT", None, "ERROR", details, "R")
                except Exception as err:
                    self.log.error(Logs.fileline() + ' : ExportDHIS2Api ERROR audit spreadsheet empty err=' + str(err))
                return compose_ret('', Constants.cst_content_type_json, 500)

            l_cols = l_rows[0]  # keep first row to read l_cols of csv

            if "version" in l_cols:
                idx_version = l_cols.index("version")
                version = l_rows[1][idx_version]
                if version not in ("v1", "v2", "v3"):
                    self.log.error(Logs.fileline() + ' : TRACE ExportDHIS2Api ERROR spreadsheet wrong version :' + str(version))
                    try:
                        details = {"result": "ERROR", "reason": "WRONG_VERSION", "version": str(version)}
                        Audit.insertAudit(audit_user, "ExportDHIS2Api", "EXPORT", None, "ERROR", details, "R")
                    except Exception as err:
                        self.log.error(Logs.fileline() + ' : ExportDHIS2Api ERROR audit wrong version err=' + str(err))
                    return compose_ret('', Constants.cst_content_type_json, 409)
            else:
                self.log.error(Logs.fileline() + ' : TRACE ExportDHIS2Api ERROR spreadsheet not found version')
                try:
                    details = {"result": "ERROR", "reason": "VERSION_NOT_FOUND"}
                    Audit.insertAudit(audit_user, "ExportDHIS2Api", "EXPORT", None, "ERROR", details, "R")
                except Exception as err:
                    self.log.error(Logs.fileline() + ' : ExportDHIS2Api ERROR audit version not found err=' + str(err))
                return compose_ret('', Constants.cst_content_type_json, 409)

            orgunit, storedby = get_dhis2_orgunit_storedby(l_cols, l_rows, args['id_user'])

            fill_dhis2_rows(l_data, l_rows, l_period, version, orgunit, storedby, rec_type, lite_filter, 'ExportDHIS2Api')

        # Send data to api DHIS2 (3 steps)
        if len(l_data) == initial_len:
            try:
                details = {"result": "ERROR", "reason": "NO_DATA"}
                Audit.insertAudit(audit_user, "ExportDHIS2Api", "EXPORT", None, "ERROR", details, "R")
            except Exception as err:
                self.log.error(Logs.fileline() + ' : ExportDHIS2Api ERROR audit no data err=' + str(err))
            return compose_ret('', Constants.cst_content_type_json, 404)

        # 1 - Get api settings
        api = Setting.getDHIS2Det(args['dhs_ser'])

        if not api:
            self.log.error(Logs.fileline() + ' : TRACE ExportDHIS2Api ERROR api setting not found version')
            try:
                details = {"result": "ERROR", "reason": "API_SETTING_NOT_FOUND", "dhs_ser": args.get('dhs_ser')}
                Audit.insertAudit(audit_user, "ExportDHIS2Api", "EXPORT", None, "ERROR", details, "R")
            except Exception as err:
                self.log.error(Logs.fileline() + ' : ExportDHIS2Api ERROR audit api setting not found err=' + str(err))
            return compose_ret('', Constants.cst_content_type_json, 405)

        dry_run = ''

        if args['dry_run'] == 'Y':
            dry_run = '?dryRun=true'

        # 2 - send data
        url   = api['dhs_url'] + str("/dataValueSets") + dry_run
        login = api['dhs_login']
        pwd   = api['dhs_pwd']

        # convert l_data to CSV string
        csv_data = StringIO()
        csv_writer = csv.writer(csv_data)
        csv_writer.writerows(l_data)

        headers = {"Content-Type": "application/csv"}

        auth = (login, pwd)

        try:
            import requests

            resp = requests.post(url, data=csv_data.getvalue(), headers=headers, auth=auth)

            # 3 - analyze the return
            if resp.status_code == 200:
                self.log.info(Logs.fileline() + ' : post ExportDHIS2Api requests OK resp = ' + str(resp.text))
            else:
                self.log.error(Logs.fileline() + ' : post ExportDHIS2Api requests KO code:' + str(resp.status_code) + 'resp = ' + str(resp.text))
                try:
                    details = {"result": "ERROR", "reason": "DHIS2_API_ERROR", "status_code": resp.status_code}
                    Audit.insertAudit(audit_user, "ExportDHIS2Api", "EXPORT", None, "ERROR", details, "R")
                except Exception as err2:
                    self.log.error(Logs.fileline() + ' : ExportDHIS2Api ERROR audit dhis2 api error err=' + str(err2))
                return compose_ret(resp.text, Constants.cst_content_type_json, resp.status_code)
        except Exception as err:
            self.log.error(Logs.fileline() + ' : post ExportDHIS2Api requests post failed, err=%s', err)
            try:
                details = {"result": "ERROR", "reason": "WRITE_FAILED"}
                Audit.insertAudit(audit_user, "ExportDHIS2Api", "EXPORT", None, "ERROR", details, "R")
            except Exception as err2:
                self.log.error(Logs.fileline() + ' : ExportDHIS2Api ERROR audit write failed err=' + str(err2))
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE ExportDHIS2Api')
        try:
            details = {"result": "SUCCESS"}
            Audit.insertAudit(audit_user, "ExportDHIS2Api", "EXPORT", None, "SUCCESS", details, "R")
        except Exception as err:
            self.log.error(Logs.fileline() + ' : ExportDHIS2Api ERROR audit success err=' + str(err))
        return compose_ret(resp.text, Constants.cst_content_type_json, resp.status_code)


class ExportWhonet(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        if 'date_beg' not in args or 'date_end' not in args:
            self.log.error(Logs.fileline() + ' : TRACE ExportWhonet ERROR args missing')
            try:
                details = {"result": "ERROR", "reason": "ARGS_MISSING", "missing": ["date_beg", "date_end"]}
                Audit.insertAudit(audit_user, "ExportWhonet", "EXPORT", None, "ERROR", details, "R")
            except Exception as err:
                self.log.error(Logs.fileline() + ' : ExportWhonet ERROR audit args missing err=' + str(err))
            return compose_ret('', Constants.cst_content_type_json, 400)

        # Data
        l_data = [["Laboratoire", "Lab adresse", "Lab ville", "Téléphone laboratoire", "Email laboratoire",
                   "Specialité du prescripteur", "Numéro d'identification", "Nom de famille",
                   "Prénom", "Nom et prénom ", "Sexe", "Date de naissance", "Age", "Catégorie d'âge", "Adresse (patient)",
                   "Ville (patient)", "Code postal (patient)", "Téléphone (patient)", "Profession (patient)",
                   "Date d'admission", "Service demandeur", "Numéro de lit", "Identification hôpital", "Type patient",
                   "Isolate number", "Numéro de prélèvement", "Date de prélèvement", "Type de prélèvement",
                   "Commentaire de prélèvement", "Micro-organisme", "Nom de l'antibiotique", "Methode de détermination",
                   "Method value", "Resultat d'antibiotique"]]
        dict_data = Export.getDataWhonet(args['date_beg'], args['date_end'])

        Various.useLangDB()

        if dict_data:
            for d in dict_data:
                data = []

                # LAB PART
                if d['lab_name']:
                    data.append(d['lab_name'])
                else:
                    data.append('')

                if d['lab_addr']:
                    data.append(d['lab_addr'])
                else:
                    data.append('')

                if d['lab_city']:
                    data.append(d['lab_city'])
                else:
                    data.append('')

                if d['lab_phone']:
                    data.append(d['lab_phone'])
                else:
                    data.append('')

                if d['lab_email']:
                    data.append(d['lab_email'])
                else:
                    data.append('')

                if d['med_spe']:
                    spe = d['med_spe']
                    data.append(_(spe.strip()))
                else:
                    data.append('')

                # PATIENT PART
                if d['pat_code']:
                    data.append(d['pat_code'])
                else:
                    data.append('')

                if d['pat_name']:
                    data.append(d['pat_name'])
                else:
                    data.append('')

                if d['pat_fname']:
                    data.append(d['pat_fname'])
                else:
                    data.append('')

                if d['pat_name'] and d['pat_fname']:
                    data.append(d['pat_name'] + ' ' + d['pat_fname'])
                else:
                    data.append('')

                if d['sex']:
                    data.append(d['sex'])
                else:
                    data.append('Inconnu')

                if d['ddn']:
                    if isinstance(d['ddn'], datetime):
                        d['ddn'] = datetime.strftime(d['ddn'], Constants.cst_isodate)
                    data.append(d['ddn'])
                else:
                    data.append('')

                if d['age']:
                    data.append(d['age'])
                else:
                    data.append('')

                if d['cat_age']:
                    if int(d['cat_age']) == 1037:
                        data.append(_('Années'))
                    elif int(d['cat_age']) == 1036:
                        data.append(_('Mois'))
                    elif int(d['cat_age']) == 1035:
                        data.append(_('Semaines'))
                    elif int(d['cat_age']) == 1034:
                        data.append(_('Jours'))
                    else:
                        data.append('')
                else:
                    data.append('')

                if d['pat_addr']:
                    data.append(d['pat_addr'])
                else:
                    data.append('')

                if d['pat_city']:
                    data.append(d['pat_city'])
                else:
                    data.append('')

                if d['pat_zip']:
                    data.append(d['pat_zip'])
                else:
                    data.append('')

                if d['pat_phone']:
                    data.append(d['pat_phone'])
                else:
                    data.append('')

                if d['pat_class']:
                    data.append(d['pat_class'])
                else:
                    data.append('')

                if d['date_hosp']:
                    d['date_hosp'] = datetime.strftime(d['date_hosp'], Constants.cst_isodate)
                    data.append(d['date_hosp'])
                else:
                    data.append('')

                if d['service_interne']:
                    service = d['service_interne']
                    data.append(_(service.strip()))
                else:
                    data.append('')

                if d['num_lit']:
                    data.append(d['num_lit'])
                else:
                    data.append('')

                if d['rec_hosp_num']:
                    data.append(d['rec_hosp_num'])
                else:
                    data.append('')

                if d['rec_type']:
                    rec_type = d['rec_type']
                    data.append(_(rec_type.strip()))
                else:
                    data.append('')

                if d['ana_code']:
                    data.append(d['ana_code'])
                else:
                    data.append('')

                # SPECIMEN PART
                if d['spec_code']:
                    data.append(d['spec_code'])
                elif d['num_dos_an'] and d['code_patient']:
                    num_samp = str(d['num_dos_an']) + str(d['code_patient'])
                    data.append(num_samp)
                else:
                    data.append('')

                if d['spec_date']:
                    if isinstance(d['spec_date'], datetime):
                        d['spec_date'] = datetime.strftime(d['spec_date'], Constants.cst_isodate)
                    data.append(d['spec_date'])
                else:
                    data.append('')

                if d['spec_type']:
                    spec_type = d['spec_type']
                    data.append(_(spec_type.strip()))
                else:
                    data.append('')

                if d['spec_comment']:
                    data.append(d['spec_comment'])
                else:
                    data.append('')

                # ANALYSIS PART
                if d['ana_name']:
                    ana_name = d['ana_name']
                    ana_name = ana_name[14:]  # delete "Antibiogramme"

                    start_meth = ana_name.find('[')  # search where method starts
                    end_meth   = ana_name.find(']')  # search where method ends

                    method_name = ana_name[start_meth + 1:end_meth]

                    ana_name = ana_name[0:start_meth - 1]

                    data.append(_(ana_name.strip()))
                    libel = d['libelle']
                    data.append(_(libel.strip()))
                    data.append(method_name)
                    data.append(d['method_value'])
                    data.append(d['valeur'])

                l_data.append(data)  # list(d.values()))

        self.log.error(Logs.fileline() + ' : l_data=' + str(l_data))

        # if no result to export
        if len(l_data) < 2:
            try:
                details = {"result": "ERROR", "reason": "NO_DATA", "date_beg": args.get('date_beg'), "date_end": args.get('date_end')}
                Audit.insertAudit(audit_user, "ExportWhonet", "EXPORT", None, "ERROR", details, "R")
            except Exception as err:
                self.log.error(Logs.fileline() + ' : ExportWhonet ERROR audit no data err=' + str(err))
            return compose_ret('', Constants.cst_content_type_json, 404)

        # write csv file
        try:
            # Build a deterministic filename from request dates
            raw_filename = f"whonet_{args['date_beg'][:-6]}_{args['date_end'][:-6]}.txt"

            # Sanitize to avoid path traversal or illegal characters
            safe_filename = re.sub(Constants.cst_safe_pattern, '_', raw_filename).strip('_') or 'whonet.txt'

            # Ensure tmp directory exists and build path safely
            tmp_dir = Path("tmp")
            tmp_dir.mkdir(parents=True, exist_ok=True)
            file_path = tmp_dir / safe_filename

            # Write TSV content safely
            with file_path.open(mode='w', encoding='utf-8', newline='') as file:
                writer = csv.writer(file, delimiter='\t')
                writer.writerows(l_data)

        except Exception as err:
            self.log.error(Logs.fileline() + ' : post ExportWhonet failed, err=%s', err)
            try:
                details = {"result": "ERROR", "reason": "WRITE_FAILED", "error": str(err),
                           "date_beg": args.get('date_beg'), "date_end": args.get('date_end'), "filename": safe_filename}
                Audit.insertAudit(audit_user, "ExportWhonet", "EXPORT", None, "ERROR", details, "R")
            except Exception as err2:
                self.log.error(Logs.fileline() + ' : ExportWhonet ERROR audit write failed err=' + str(err2))
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE ExportWhonet')
        try:
            details = {"result": "SUCCESS", "filename": safe_filename, "date_beg": args.get('date_beg'), "date_end": args.get('date_end')}
            Audit.insertAudit(audit_user, "ExportWhonet", "EXPORT", None, "SUCCESS", details, "R")
        except Exception as err:
            self.log.error(Logs.fileline() + ' : ExportWhonet ERROR audit success err=' + str(err))
        return compose_ret('', Constants.cst_content_type_json)
