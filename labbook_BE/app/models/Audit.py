# -*- coding:utf-8 -*-
import logging
import json

from flask import request as flask_request

from app.models.DB import DB
from app.models.Various import Various
from app.models.Logs import Logs


class Audit:
    log = logging.getLogger('log_services')
    audit_trail_enabled = True

    @staticmethod
    def list_audit(offset=0, limit=25, order_col_index=1, order_dir="desc", search_value=None, filters=None):
        cursor = DB.cursor()
        try:
            order_col = Audit._get_order_column(order_col_index)
            order_dir = "ASC" if str(order_dir).lower() == "asc" else "DESC"

            filters = filters or {}

            sql = '''
                select aud_ser, aud_date_utc, aud_user_login, aud_user_display, aud_user_role, aud_resource_type,
                aud_resource_id, aud_action, aud_client_ip, aud_status, aud_details
                from audit_trail where 1=1
            '''
            params = []

            sql, params = Audit._apply_filters(sql, params, filters)

            # System calls filter (default: exclude system)
            include_system = str(filters.get("include_system") or "N").upper()
            if include_system != "Y":
                sql += " AND COALESCE(aud_client_ip, '') <> '127.0.0.1'"

            sql, params = Audit._apply_global_search(sql, params, search_value)

            sql += " ORDER BY " + order_col + " " + order_dir + ", aud_ser DESC LIMIT %s, %s"
            params.extend([offset, limit])

            cursor.execute(sql, params)
            rows = cursor.fetchall()

            result = []
            for r in rows:
                result.append(Audit._build_audit_item(r))

            return result
        except Exception as err:
            Audit.log.error(Logs.fileline() + " : ERROR type=" + err.__class__.__name__ + " args=" + repr(getattr(err, "args", None)))
            raise
        finally:
            try:
                cursor.close()
            except Exception:
                # closing the cursor must not hide the error that led here
                pass

    # --- begin of methods for list-audit ---

    @staticmethod
    def _get_order_column(order_col_index):
        return {
            1: "aud_date_utc",
            2: "aud_user_display",
            3: "aud_user_role",
            4: "aud_details",
            5: "aud_resource_type",
            6: "aud_action",
            7: "aud_client_ip",
            8: "aud_status",
            9: "aud_ser"
        }.get(order_col_index, "aud_date_utc")

    @staticmethod
    def _apply_filters(sql, params, filters):
        # Date filters
        if filters.get("date_start"):
            sql += " AND aud_date_utc >= %s"
            params.append((filters["date_start"] or "").replace("T", " "))

        if filters.get("date_end"):
            sql += " AND aud_date_utc <= %s"
            params.append((filters["date_end"] or "").replace("T", " "))

        # User filter (login or display)
        if filters.get("user"):
            like_user = "%" + filters["user"] + "%"
            sql += " AND (aud_user_login LIKE %s OR aud_user_display LIKE %s)"
            params.extend([like_user, like_user])

        # Role filter
        if filters.get("role"):
            role_raw = filters["role"]
            role_prefix = role_raw.split("_", 1)[0] if role_raw else ""
            if role_prefix:
                sql += " AND LEFT(aud_user_role, 1) = %s"
                params.append(role_prefix)

        # Context filter
        if filters.get("context"):
            sql += " AND aud_details LIKE %s"
            params.append("%" + filters["context"] + "%")

        # Action filter
        if filters.get("action"):
            sql += " AND aud_action LIKE %s"
            params.append("%" + filters["action"] + "%")

        # Status filter
        if filters.get("status"):
            sql += " AND aud_status = %s"
            params.append(filters["status"])

        # IP filter
        if filters.get("ip"):
            sql += " AND aud_client_ip LIKE %s"
            params.append("%" + filters["ip"] + "%")

        # Resource filter
        if filters.get("resource"):
            sql += (
                " AND CONCAT(COALESCE(aud_resource_type, ''), ' ', "
                "COALESCE(aud_resource_id, '')) LIKE %s"
            )
            params.append("%" + filters["resource"] + "%")

        # System calls filter
        include_system = str(filters.get("include_system") or "N").upper()
        if include_system != "Y":
            sql += " AND COALESCE(aud_client_ip, '') <> '127.0.0.1'"

        return sql, params

    @staticmethod
    def _apply_global_search(sql, params, search_value):
        if search_value:
            like = "%" + search_value + "%"
            sql += """
                AND (
                    aud_user_login LIKE %s OR
                    aud_user_display LIKE %s OR
                    aud_user_role LIKE %s OR
                    aud_resource_type LIKE %s OR
                    aud_resource_id LIKE %s OR
                    aud_action LIKE %s OR
                    aud_client_ip LIKE %s OR
                    aud_status LIKE %s OR
                    aud_details LIKE %s
                )
            """
            params.extend([like, like, like, like, like, like, like, like, like])

        return sql, params

    @staticmethod
    def _build_audit_item(r):
        item = {}

        item["aud_ser"] = r["aud_ser"]
        item["event_time_utc"] = r["aud_date_utc"].strftime("%Y-%m-%d %H:%M:%S") if r["aud_date_utc"] else ""
        item["aud_user_login"] = r["aud_user_login"] or ""
        item["user_display"] = r["aud_user_display"] or item["aud_user_login"]
        item["role_name"] = r["aud_user_role"]

        # Extract context label from aud_details (JSON) for the "Contexte" column
        context_label = ""
        details_raw = r.get("aud_details")
        if details_raw:
            try:
                details_obj = details_raw if isinstance(details_raw, dict) else json.loads(details_raw)
                if isinstance(details_obj, dict):
                    context_label = str(details_obj.get("context") or "")
            except Exception:
                context_label = ""

        item["context_label"] = context_label

        if r["aud_resource_type"] and r["aud_resource_id"]:
            resource_label = str(r["aud_resource_type"]) + " " + str(r["aud_resource_id"])
        elif r["aud_resource_type"]:
            resource_label = r["aud_resource_type"]
        else:
            resource_label = r["aud_resource_id"]

        action_label = r.get("aud_action") or ""
        if action_label:
            resource_label = str(resource_label) + " - " + str(action_label)

        item["resource_label"] = resource_label

        # Keep action for the "Action" column (menu stays separate)
        item["details_summary"] = r["aud_action"]

        item["ip_addr"] = r["aud_client_ip"]
        item["status_label"] = r["aud_status"]

        return item

    # --- end of methods for list-audit ---

    @staticmethod
    def countAuditTotal():
        cursor = DB.cursor()
        try:
            cursor.execute("SELECT COUNT(*) AS nb FROM audit_trail")
            row = cursor.fetchone()
            return row["nb"] if row else 0
        finally:
            try:
                cursor.close()
            except Exception:
                # closing the cursor must not hide the error that led here
                pass

    @staticmethod
    def countAuditFiltered(search_value=None, filters=None):
        filters = filters or {}

        # Detect if at least one filter is set
        has_filter = False
        for key in ("date_start", "date_end", "user", "role", "action", "status", "ip", "context", "resource", "include_system"):
            if filters.get(key):
                has_filter = True
                break

        # No global search, no filters => same as total
        if not search_value and not has_filter:
            return Audit.countAuditTotal()

        cursor = DB.cursor()
        try:
            sql = "SELECT COUNT(*) AS nb FROM audit_trail WHERE 1=1"
            params = []

            sql, params = Audit._apply_filters(sql, params, filters)
            sql, params = Audit._apply_global_search(sql, params, search_value)

            cursor.execute(sql, params)
            row = cursor.fetchone()
            return row["nb"] if row else 0

        finally:
            try:
                cursor.close()
            except Exception:
                # closing the cursor must not hide the error that led here
                pass

    @staticmethod
    def list_audit_by_period(date_beg_utc, date_end_utc):
        cursor = DB.cursor()
        try:
            sql = ('''
                SELECT aud_ser, aud_date_utc, aud_user_login, aud_user_display, aud_user_role, aud_resource_type,
                       aud_resource_id, aud_action, aud_client_ip, aud_status, aud_details, aud_event_type
                FROM audit_trail
                WHERE aud_date_utc BETWEEN %s AND %s
                ORDER BY aud_date_utc, aud_ser
            ''')
            cursor.execute(sql, [date_beg_utc, date_end_utc])
            rows = cursor.fetchall()
            return rows
        except Exception as err:
            Audit.log.error(Logs.fileline() + " : ERROR type=" + err.__class__.__name__ + " args=" + repr(getattr(err, "args", None)))
            raise
        finally:
            try:
                cursor.close()
            except Exception:
                # closing the cursor must not hide the error that led here
                pass

    @staticmethod
    def getAuditById(aud_ser):
        cursor = DB.cursor()
        try:
            sql = ('''
                SELECT aud_ser, aud_date_utc, aud_user_login, aud_user_display, aud_user_role, aud_resource_type,
                       aud_resource_id, aud_action, aud_client_ip, aud_status, aud_details
                FROM audit_trail
                WHERE aud_ser = %s
            ''')
            cursor.execute(sql, [aud_ser])
            row = cursor.fetchone()
            if not row:
                return None

            item = {}
            item["aud_ser"] = row["aud_ser"]
            item["event_time_utc"] = row["aud_date_utc"].strftime("%Y-%m-%d %H:%M:%S") if row["aud_date_utc"] else ""
            item["aud_user_login"] = row["aud_user_login"] or ""
            item["user_display"] = row["aud_user_display"] or item["aud_user_login"]
            item["role_name"] = row["aud_user_role"]
            item["resource_type"] = row["aud_resource_type"]
            item["resource_id"] = row["aud_resource_id"]
            item["action"] = row["aud_action"]
            item["ip_addr"] = row["aud_client_ip"]
            item["status_label"] = row["aud_status"]
            item["details"] = row["aud_details"]
            return item
        except Exception as err:
            Audit.log.error(Logs.fileline() + " : ERROR type=" + err.__class__.__name__ + " args=" + repr(getattr(err, "args", None)))
            raise
        finally:
            try:
                cursor.close()
            except Exception:
                # closing the cursor must not hide the error that led here
                pass

    @staticmethod
    def insertAudit(user, action, resource_type=None, resource_id=None, status=None, details_json=None, event_type="E"):
        """Insert a new audit event into audit_trail."""

        # Skip audit if disabled
        if not Audit.audit_trail_enabled:
            return None

        cursor = DB.cursor()
        try:
            user_login = user.get('usr_login') if user else None
            user_display = user.get('usr_display') if user else None
            user_role = user.get('usr_role') if user else None
            try:
                client_ip = Various.get_client_ip()
            except Exception:
                client_ip = '127.0.0.1'

            # Inject UI context from FE headers (if provided)
            try:
                ctx_label = flask_request.headers.get("X-LabBook-Audit-Context", "") or ""
            except Exception:
                ctx_label = ""

            if isinstance(details_json, dict) and ctx_label:
                if "context" not in details_json:
                    details_json["context"] = ctx_label

            if details_json is not None and not isinstance(details_json, str):
                details_json = json.dumps(details_json, default=str)

            sql = """
                INSERT INTO audit_trail (aud_date_utc, aud_user_login, aud_user_display, aud_user_role, aud_resource_type,
                    aud_resource_id, aud_action, aud_client_ip, aud_status, aud_details, aud_event_type)
                VALUES (UTC_TIMESTAMP(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = [user_login, user_display, user_role, resource_type, resource_id, action, client_ip, status, details_json, event_type]
            cursor.execute(sql, params)

            aud_ser = getattr(cursor, "lastrowid", None)
            Audit.log.info(Logs.fileline() + " : OK user_login=" + str(user_login) + " action=" + str(action) + " aud_ser=" + str(aud_ser))
            return aud_ser

        except Exception as err:
            Audit.log.error(Logs.fileline() + " : ERROR user_login=" + str(user_login) + " action=" + str(action) + " err=" + str(err))
            raise
        finally:
            try:
                cursor.close()
            except Exception:
                # closing the cursor must not hide the error that led here
                pass

    @staticmethod
    def purgeAuditByPeriod(date_beg_utc, date_end_utc):
        cursor = DB.cursor()
        try:
            sql = "DELETE FROM audit_trail WHERE aud_date_utc BETWEEN %s AND %s"
            cursor.execute(sql, [date_beg_utc, date_end_utc])
            return int(getattr(cursor, "rowcount", 0) or 0)
        except Exception as err:
            Audit.log.error(Logs.fileline() + " : ERROR err=" + str(err))
            raise
        finally:
            try:
                cursor.close()
            except Exception:
                # closing the cursor must not hide the error that led here
                pass
