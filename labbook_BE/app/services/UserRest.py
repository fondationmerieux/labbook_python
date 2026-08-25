# -*- coding:utf-8 -*-
import logging
import random
import string
import csv
import os

from datetime import datetime
from flask import request
from flask_restful import Resource

from app.models.Audit import Audit
from app.models.General import compose_ret
from app.models.Constants import Constants
from app.models.User import User
from app.models.Logs import Logs
from app.models.Various import Various
from app.security.oauth_routes import require_oauth


class UserAccess(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json() or {}

        # Check required fields
        if 'login' not in args or 'pwd' not in args:
            self.log.error(Logs.fileline() + ' : UserAccess ERROR args missing')
            try:
                details = {"result": "ERROR", "reason": "ARGS_MISSING"}
                Audit.insertAudit(None, "UserAccess", "USER", None, "ERROR", details, "E")
            except Exception:
                self.log.exception(Logs.fileline() + ' : UserAccess ERROR audit args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        login = args['login']
        user = User.getUserByLogin(login)

        # User not found
        if not user:
            self.log.error(Logs.fileline() + ' : UserAccess login not found')
            try:
                details = {"login": login, "result": "ERROR", "reason": "LOGIN_NOT_FOUND"}
                Audit.insertAudit({"usr_login": login, "usr_display": login, "usr_role": None}, "UserAccess", "USER", None, "ERROR", details, "E")
            except Exception:
                self.log.exception(Logs.fileline() + ' : UserAccess ERROR audit UserLogin')
            return compose_ret('', Constants.cst_content_type_json, 404)

        # Extract salt
        salt_start = user['password'].find(":")
        salt = user['password'][salt_start + 1:]
        pwd_db = User.getPasswordDB(args['pwd'], salt)

        # Validate password
        ret = User.checkUserAccess(login, pwd_db)

        # Successful login
        if ret is True:
            payload = {"id_user": int(user["id_data"]), "role_type": user["role_type"], "login": login}
            self.log.info(Logs.fileline() + ' : UserAccess authorized role=' + str(user['role_type']) + ' | login=' + str(login))
            try:
                details = {"user_id": int(user["id_data"]), "login": login, "result": "SUCCESS"}
                Audit.insertAudit({"usr_login": user["username"], "usr_display": user["username"], "usr_role": user["role_type"]},
                                  "UserAccess", "USER", int(user["id_data"]), "SUCCESS", details, "E")
            except Exception:
                self.log.exception(Logs.fileline() + ' : UserAccess ERROR audit UserLogin SUCCESS')
            return compose_ret(payload, Constants.cst_content_type_json)

        # Wrong password
        if ret is False:
            self.log.info(Logs.fileline() + ' : UserAccess not authorized ' + str(login))
            try:
                details = {"login": login, "result": "ERROR", "reason": "BAD_PASSWORD"}
                Audit.insertAudit({"usr_login": user["username"], "usr_display": user["username"], "usr_role": user["role_type"]},
                                  "UserAccess", "USER", int(user["id_data"]), "ERROR", details, "E")
            except Exception:
                self.log.exception(Logs.fileline() + ' : UserAccess ERROR audit UserLogin BAD_PASSWORD')
            return compose_ret('', Constants.cst_content_type_json, 401)

        # Unexpected error
        self.log.error(Logs.fileline() + ' : UserAccess ERROR checkUserAccess')
        try:
            details = {"login": login, "result": "ERROR", "reason": "CHECK_ERROR"}
            Audit.insertAudit({"usr_login": user["username"], "usr_display": user["username"], "usr_role": user["role_type"]},
                              "UserAccess", "USER", int(user["id_data"]), "ERROR", details, "E")
        except Exception:
            self.log.exception(Logs.fileline() + ' : UserAccess ERROR audit UserLogin CHECK_ERROR')
        return compose_ret('', Constants.cst_content_type_json, 500)


class UserByLogin(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self, login):
        audit_user = request.oauth_user
        user = User.getUserByLogin(login)

        if not user:
            self.log.error(Logs.fileline() + ' : TRACE UserByLogin')
            try:
                details = {"result": "ERROR", "reason": "NOT_FOUND", "login": str(login)}
                Audit.insertAudit(audit_user, "UserByLogin", "USER", None, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : UserByLogin ERROR audit not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        # Replace None by empty string
        for key, value in list(user.items()):
            if user[key] is None:
                user[key] = ''

        self.log.info(Logs.fileline() + ' : TRACE UserByLogin')
        try:
            details = {"result": "SUCCESS", "action": "VIEW", "login": login}
            Audit.insertAudit(audit_user, "UserByLogin", "USER", int(user["id_data"]), "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : UserByLogin ERROR audit success')
        return compose_ret(user, Constants.cst_content_type_json)


class UserDet(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self, id_user):
        audit_user = request.oauth_user
        user = User.getUserDetails(id_user)

        if not user:
            self.log.error(Logs.fileline() + ' : TRACE UserDet no user')
            try:
                details = {"result": "ERROR", "reason": "NOT_FOUND", "user_id": int(id_user)}
                Audit.insertAudit(audit_user, "UserDet", "USER", int(id_user), "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : UserDet ERROR audit not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        if user['birth']:
            user['birth'] = datetime.strftime(user['birth'], '%Y-%m-%d')

        if user['arrived']:
            user['arrived'] = datetime.strftime(user['arrived'], '%Y-%m-%d')

        if user['last_eval']:
            user['last_eval'] = datetime.strftime(user['last_eval'], '%Y-%m-%d')

        # Replace None by empty string
        for key, value in list(user.items()):
            if user[key] is None:
                user[key] = ''

        self.log.info(Logs.fileline() + ' : TRACE UserDet')
        try:
            details = {"result": "SUCCESS", "action": "VIEW", "user_id": int(id_user)}
            Audit.insertAudit(audit_user, "UserDet", "USER", int(id_user), "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : UserDet ERROR audit success')
        return compose_ret(user, Constants.cst_content_type_json)

    @require_oauth()
    def post(self, id_user):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        if 'id_user' not in args or 'login' not in args or 'cps' not in args or 'rpps' not in args or \
           'firstname' not in args or 'lastname' not in args or 'lang' not in args or 'email' not in args or \
           'title' not in args or 'initial' not in args or 'birth' not in args or 'phone' not in args or \
           'arrived' not in args or 'position' not in args or 'section' not in args or 'last_eval' not in args or \
           'address' not in args or 'cv' not in args or 'diploma' not in args or 'training' not in args or \
           'comment' not in args or 'id_pres' not in args or 'role_type' not in args or 'role_pro' not in args:
            self.log.error(Logs.fileline() + ' : UserDet ERROR args missing')
            try:
                details = {"result": "ERROR", "reason": "ARGS_MISSING", "user_id": int(id_user)}
                Audit.insertAudit(audit_user, "UserDet", "USER", int(id_user), "ERROR", details, "U" if id_user > 0 else "C")
            except Exception:
                self.log.exception(Logs.fileline() + ' : UserDet ERROR audit args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # update user
        if id_user > 0:
            if 'stat' not in args:
                self.log.error(Logs.fileline() + ' : UserDet ERROR args missing')
                try:
                    details = {"result": "ERROR", "reason": "ARGS_MISSING", "user_id": int(id_user), "missing": ["stat"]}
                    Audit.insertAudit(audit_user, "UserDet", "USER", int(id_user), "ERROR", details, "U")
                except Exception:
                    self.log.exception(Logs.fileline() + ' : UserDet ERROR audit args missing')
                return compose_ret('', Constants.cst_content_type_json, 400)

            # get login by id_user
            user = User.getUserDetails(id_user)

            if not user:
                self.log.error(Logs.fileline() + ' : TRACE UserDet no user')
                try:
                    details = {"result": "ERROR", "reason": "NOT_FOUND", "user_id": int(id_user)}
                    Audit.insertAudit(audit_user, "UserDet", "USER", int(id_user), "ERROR", details, "U")
                except Exception:
                    self.log.exception(Logs.fileline() + ' : UserDet ERROR audit not found')
                return compose_ret('', Constants.cst_content_type_json, 404)

            # update sigl_user_data
            ret = User.updateUser(id_data=id_user,
                                  role_type=args['role_type'],
                                  role_pro=args['role_pro'],
                                  username=args['login'],
                                  cps_id=args['cps'],
                                  rpps=args['rpps'],
                                  status=args['stat'],
                                  firstname=args['firstname'],
                                  lastname=args['lastname'],
                                  locale=args['lang'],
                                  email=args['email'],
                                  titre=args['title'],
                                  initiale=args['initial'],
                                  ddn=args['birth'],
                                  adresse=args['address'],
                                  tel=args['phone'],
                                  darrive=args['arrived'],
                                  position=args['position'],
                                  cv=args['cv'],
                                  diplome=args['diploma'],
                                  formation=args['training'],
                                  section=args['section'],
                                  deval=args['last_eval'],
                                  side_account=args['id_pres'],
                                  commentaire=args['comment'])

            success = ret is not False
            status = "SUCCESS" if success else "ERROR"

            if not success:
                self.log.info(Logs.fileline() + ' : TRACE UserDet ERROR update user')
                try:
                    details = {"user_id": id_user, "login": user['username'], "result": status,
                               "reason": "UPDATE_FAILED" if not success else None}
                    if details.get("reason") is None:
                        details.pop("reason", None)
                    Audit.insertAudit(audit_user, "UserDet", "USER", id_user, status, details, "U")
                except Exception:
                    self.log.exception(Logs.fileline() + ' : UserDet ERROR audit UserDet')
                return compose_ret('', Constants.cst_content_type_json, 500)

        # insert new user
        else:
            if 'id_owner' not in args or 'password' not in args:
                self.log.error(Logs.fileline() + ' : UserDet ERROR args missing')
                try:
                    details = {"result": "ERROR", "reason": "ARGS_MISSING", "user_id": int(id_user),
                               "missing": ["id_owner", "password"]}
                    Audit.insertAudit(audit_user, "UserDet", "USER", None, "ERROR", details, "C")
                except Exception:
                    self.log.exception(Logs.fileline() + ' : UserDet ERROR audit args missing')
                return compose_ret('', Constants.cst_content_type_json, 400)

            if args['role_type'] == 'Z':
                # replace login by empty string
                args['login'] = ''

                # generate a long fake password for unused type of account
                args['password'] = ''.join(random.choices(string.ascii_letters + string.digits, k=24))

            pwd_db = User.getPasswordDB(args['password'])

            # insert in sigl_user_data
            ret = User.insertUser(id_owner=args['id_owner'],
                                  role_type=args['role_type'],
                                  username=args['login'],
                                  password=pwd_db,
                                  cps_id=args['cps'],
                                  rpps=args['rpps'],
                                  status=Constants.cst_user_active,
                                  firstname=args['firstname'],
                                  lastname=args['lastname'],
                                  locale=args['lang'],
                                  email=args['email'],
                                  titre=args['title'],
                                  initiale=args['initial'],
                                  ddn=args['birth'],
                                  adresse=args['address'],
                                  tel=args['phone'],
                                  darrive=args['arrived'],
                                  position=args['position'],
                                  cv=args['cv'],
                                  diplome=args['diploma'],
                                  formation=args['training'],
                                  section=args['section'],
                                  deval=args['last_eval'],
                                  side_account=args['id_pres'],
                                  commentaire=args['comment'],
                                  origin=args['id_owner'],
                                  role_pro=args['role_pro'])

            success = ret > 0
            status = "SUCCESS" if success else "ERROR"

            if not success:
                self.log.error(Logs.alert() + ' : UserDet ERROR insert user')
                try:
                    details = {"user_id": ret, "login": args['login'], "result": status,
                               "reason": "INSERT_FAILED" if not success else None}
                    if details.get("reason") is None:
                        details.pop("reason", None)
                    Audit.insertAudit(audit_user, "UserDet", "USER", ret, status, details, "C")
                except Exception:
                    self.log.exception(Logs.fileline() + ' : UserDet ERROR audit UserDet')
                return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE UserDet id_user=' + str(id_user))
        try:
            event_type = "U" if id_user > 0 else "C"
            details = {"result": "SUCCESS", "user_id": int(ret) if id_user <= 0 else int(id_user)}
            if id_user > 0 and 'login' in args:
                details["login"] = str(args.get('login'))
            Audit.insertAudit(audit_user, "UserDet", "USER", int(ret) if id_user <= 0 else int(id_user), "SUCCESS",
                              details, event_type)
        except Exception:
            self.log.exception(Logs.fileline() + ' : UserDet ERROR audit success')
        return compose_ret(ret, Constants.cst_content_type_json)


class UserStaffDet(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self, id_user):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        if 'id_user' not in args or 'firstname' not in args or 'lastname' not in args or 'email' not in args or \
           'title' not in args or 'initial' not in args or 'birth' not in args or 'phone' not in args or \
           'arrived' not in args or 'position' not in args or 'section' not in args or 'last_eval' not in args or \
           'address' not in args or 'cv' not in args or 'diploma' not in args or 'training' not in args or \
           'comment' not in args or 'role_type' not in args or 'role_pro' not in args:
            self.log.error(Logs.fileline() + ' : UserStaffDet ERROR args missing')
            try:
                details = {"result": "ERROR", "reason": "ARGS_MISSING", "user_id": int(id_user)}
                Audit.insertAudit(audit_user, "UserStaffDet", "USER", int(id_user), "ERROR", details, "U")
            except Exception:
                self.log.exception(Logs.fileline() + ' : UserStaffDet ERROR audit args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # update user
        if id_user > 0:
            # get login by id_user
            user = User.getUserDetails(id_user)

            if not user:
                self.log.error(Logs.fileline() + ' : TRACE UserStaffDet no user')
                try:
                    details = {"result": "ERROR", "reason": "NOT_FOUND", "user_id": int(id_user)}
                    Audit.insertAudit(audit_user, "UserStaffDet", "USER", int(id_user), "ERROR", details, "U")
                except Exception:
                    self.log.exception(Logs.fileline() + ' : UserStaffDet ERROR audit not found')
                return compose_ret('', Constants.cst_content_type_json, 500)

            # update sigl_user_data
            ret = User.updateUser(id_data=id_user,
                                  role_type=user['role_type'],
                                  username=user['username'],
                                  cps_id=user['cps'],
                                  rpps=user['rpps'],
                                  status=user['stat'],
                                  firstname=args['firstname'],
                                  lastname=args['lastname'],
                                  locale=user['lang'],
                                  email=args['email'],
                                  titre=args['title'],
                                  initiale=args['initial'],
                                  ddn=args['birth'],
                                  adresse=args['address'],
                                  tel=args['phone'],
                                  darrive=args['arrived'],
                                  position=args['position'],
                                  cv=args['cv'],
                                  diplome=args['diploma'],
                                  formation=args['training'],
                                  section=args['section'],
                                  deval=args['last_eval'],
                                  side_account=user['side_account'],
                                  commentaire=args['comment'],
                                  role_pro=user['role_pro'])

            if ret is False:
                self.log.info(Logs.fileline() + ' : TRACE UserStaffDet ERROR update user')
                try:
                    details = {"user_id": id_user, "login": user['username'], "result": "ERROR", "source": "UserStaffDet"}
                    Audit.insertAudit(audit_user, "UserStaffUpdate", "USER", id_user, "ERROR", details, "U")
                except Exception:
                    self.log.exception(Logs.fileline() + ' : UserStaffDet ERROR audit UserStaffUpdate')
                return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE UserStaffDet id_user=' + str(id_user))
        try:
            details = {"user_id": id_user, "login": user['username'], "result": "SUCCESS", "source": "UserStaffDet"}
            Audit.insertAudit(audit_user, "UserStaffUpdate", "USER", id_user, "SUCCESS", details, "U")
        except Exception:
            self.log.exception(Logs.fileline() + ' : UserStaffDet ERROR audit UserStaffUpdate')
        return compose_ret('', Constants.cst_content_type_json)


class UserList(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        if not args:
            args = {}

        l_users = User.getUserList(args)

        if not l_users:
            self.log.error(Logs.fileline() + ' : TRACE UserList not found')

        Various.useLangDB()

        for user in l_users:
            # Replace None by empty string
            for key, value in list(user.items()):
                if user[key] is None:
                    user[key] = ''
                elif key == 'section' and user[key]:
                    user[key] = _(user[key].strip())
                elif key == 'role' and user[key]:
                    user[key] = _(user[key].strip())

            if user['birth']:
                user['birth'] = datetime.strftime(user['birth'], '%Y-%m-%d')

            if user['arrived']:
                user['arrived'] = datetime.strftime(user['arrived'], '%Y-%m-%d')

            if user['last_eval']:
                user['last_eval'] = datetime.strftime(user['last_eval'], '%Y-%m-%d')

        self.log.info(Logs.fileline() + ' : TRACE UserList')
        try:
            details = {"result": "SUCCESS", "action": "QUERY", "count": len(l_users)}
            Audit.insertAudit(audit_user, "UserList", "USER", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : UserList ERROR audit success')
        return compose_ret(l_users, Constants.cst_content_type_json)


class UserListFromExt(Resource):
    log = logging.getLogger('log_services')

    @require_oauth('external/user')
    def post(self):
        self.log.info(Logs.fileline() + ' : UserListFromExt API access authorized')
        audit_user = request.oauth_user
        args = request.get_json() or {}

        if not args:
            args = {}

        l_users = User.getUserList(args)

        if not l_users:
            self.log.error(Logs.fileline() + ' : TRACE UserListFromExt not found')

        Various.useLangDB()

        for user in l_users:
            # Replace None by empty string
            for key, value in list(user.items()):
                if user[key] is None:
                    user[key] = ''
                elif key == 'section' and user[key]:
                    user[key] = _(user[key].strip())
                elif key == 'role' and user[key]:
                    user[key] = _(user[key].strip())

            if user['birth']:
                user['birth'] = datetime.strftime(user['birth'], '%Y-%m-%d')

            if user['arrived']:
                user['arrived'] = datetime.strftime(user['arrived'], '%Y-%m-%d')

            if user['last_eval']:
                user['last_eval'] = datetime.strftime(user['last_eval'], '%Y-%m-%d')

        self.log.info(Logs.fileline() + ' : TRACE UserListFromExt')
        try:
            details = {"result": "SUCCESS", "action": "QUERY", "count": len(l_users)}
            Audit.insertAudit(audit_user, "UserListFromExt", "USER", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : UserListFromExt ERROR audit success')
        return compose_ret(l_users, Constants.cst_content_type_json, 200)


class UserLiteList(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self):
        audit_user = request.oauth_user
        l_users = User.getUserLiteList()

        if not l_users:
            self.log.error(Logs.fileline() + ' : TRACE UserLiteList not found')

        for user in l_users:
            # Replace None by empty string
            for key, value in list(user.items()):
                if user[key] is None:
                    user[key] = ''

        self.log.info(Logs.fileline() + ' : TRACE UserLiteList')
        try:
            details = {"result": "SUCCESS", "action": "QUERY", "count": len(l_users)}
            Audit.insertAudit(audit_user, "UserLiteList", "USER", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : UserLiteList ERROR audit success')
        return compose_ret(l_users, Constants.cst_content_type_json)


class UserRoleList(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self, type=''):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        l_exclude = []
        genuine   = "N"

        if 'exclude' in args:
            l_exclude = args['exclude']

        if 'genuine' in args:
            genuine = args['genuine']

        l_roles = User.getUserRoleList(type, l_exclude, genuine)

        if not l_roles:
            self.log.error(Logs.fileline() + ' : TRACE UserRoleList not found')

        Various.useLangDB()

        for role in l_roles:
            # count number of profiles associated of this role
            role['nb_profile'] = 0

            ret_nb = User.countProfileByRole(role['pro_ser'])

            if ret_nb:
                role['nb_profile'] = ret_nb['nb_profile']

            # Replace None by empty string
            for key, value in list(role.items()):
                if role[key] is None:
                    role[key] = ''
                elif key == 'label' and role[key]:
                    role[key] = _(role[key].strip())
                elif key == 'name' and role[key]:
                    role['role_based'] = _(role[key].strip())

        self.log.info(Logs.fileline() + ' : TRACE UserRoleList')
        try:
            details = {"result": "SUCCESS", "action": "QUERY", "count": len(l_roles)}
            Audit.insertAudit(audit_user, "UserRoleList", "ROLE", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : UserRoleList ERROR audit success')
        return compose_ret(l_roles, Constants.cst_content_type_json)


class UserRoleDet(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self, pro_ser):
        audit_user = request.oauth_user
        role = User.getRoleDetails(pro_ser)

        if not role:
            self.log.error(Logs.fileline() + ' : TRACE UserRoleDet no role')
            try:
                details = {"result": "ERROR", "reason": "NOT_FOUND", "pro_ser": int(pro_ser)}
                Audit.insertAudit(audit_user, "UserRoleDet", "ROLE", int(pro_ser), "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : UserRoleDet ERROR audit not found')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE UserRoleDet')
        try:
            details = {"result": "SUCCESS", "action": "VIEW", "role_id": int(pro_ser)}
            Audit.insertAudit(audit_user, "UserRoleDet", "ROLE", int(pro_ser), "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : UserRoleDet ERROR audit success')
        return compose_ret(role, Constants.cst_content_type_json)

    @require_oauth()
    def post(self, pro_ser):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        if 'by_user' not in args or 'id_user' not in args or 'role_type' not in args or 'role_label' not in args or \
           'role_color_1' not in args or 'role_color_2' not in args or 'role_text_color' not in args or \
           'l_rights' not in args:
            self.log.error(Logs.fileline() + ' : UserRoleDet ERROR args missing')
            try:
                details = {"result": "ERROR", "reason": "ARGS_MISSING", "pro_ser": int(pro_ser)}
                Audit.insertAudit(audit_user, "UserRoleDet", "ROLE", int(pro_ser), "ERROR", details, "U" if pro_ser > 0 else "C")
            except Exception:
                self.log.exception(Logs.fileline() + ' : UserRoleDet ERROR audit args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # update user
        if pro_ser > 0:
            # update profile_role
            ret = User.updateProfileRole(by_user=args['by_user'],
                                         pro=pro_ser,
                                         label=args['role_label'],
                                         color_1=args['role_color_1'],
                                         color_2=args['role_color_2'],
                                         text_color=args['role_text_color'])

            # update profile_permissions
            for right in args['l_rights']:
                ret_perm = User.updateProfilePermission(by_user=args['by_user'],
                                                        pro=pro_ser,
                                                        prp=right['prp_ser'],
                                                        granted=right['prp_granted'])

                if ret_perm is False:
                    self.log.info(Logs.fileline() + ' : UserRoleDet ERROR update profilePermissions')
                    try:
                        details = {"result": "ERROR", "reason": "UPDATE_FAILED", "pro_ser": int(pro_ser),
                                   "prp_ser": right.get('prp_ser')}
                        Audit.insertAudit(audit_user, "UserRoleDet", "ROLE", int(pro_ser), "ERROR", details, "U")
                    except Exception:
                        self.log.exception(Logs.fileline() + ' : UserRoleDet ERROR audit update perm')
                    return compose_ret('', Constants.cst_content_type_json, 500)

            try:
                details = {"pro_ser": pro_ser, "by_user": args['by_user'], "result": "SUCCESS", "role_label": args['role_label']}
                Audit.insertAudit(audit_user, "UserRoleDet", "ROLE", pro_ser, "SUCCESS", details, "U")
            except Exception:
                self.log.exception(Logs.fileline() + ' : UserRoleDet ERROR audit UserRoleUpdate')

        # insert new user
        else:
            role = User.getUserRole(args['role_type'])

            if not role:
                self.log.error(Logs.fileline() + ' : UserRoleDet ERROR role not found')
                try:
                    details = {"result": "ERROR", "reason": "NOT_FOUND", "role_type": args.get('role_type')}
                    Audit.insertAudit(audit_user, "UserRoleDet", "ROLE", None, "ERROR", details, "C")
                except Exception:
                    self.log.exception(Logs.fileline() + ' : UserRoleDet ERROR audit role not found')
                return compose_ret('', Constants.cst_content_type_json, 500)

            # insert profile_role
            ret = User.insertProfileRole(by_user=args['by_user'],
                                         role=role['id_role'],
                                         label=args['role_label'],
                                         color_1=args['role_color_1'],
                                         color_2=args['role_color_2'],
                                         text_color=args['role_text_color'])

            if ret <= 0:
                self.log.error(Logs.alert() + ' : UserRoleDet ERROR insert user')
                try:
                    details = {"result": "ERROR", "reason": "INSERT_FAILED", "role_type": args.get('role_type')}
                    Audit.insertAudit(audit_user, "UserRoleDet", "ROLE", None, "ERROR", details, "C")
                except Exception:
                    self.log.exception(Logs.fileline() + ' : UserRoleDet ERROR audit insert role')
                return compose_ret('', Constants.cst_content_type_json, 500)

            # insert profile_permissions
            for right in args['l_rights']:
                ret_perm = User.insertProfilePermission(by_user=args['by_user'],
                                                        pro=ret,
                                                        prp=right['prp_ser'],
                                                        granted=right['prp_granted'])

                if ret_perm <= 0:
                    self.log.error(Logs.alert() + ' : UserRoleDet ERROR insert profilePermissions')
                    try:
                        details = {"result": "ERROR", "reason": "INSERT_FAILED", "pro_ser": int(ret),
                                   "prp_ser": right.get('prp_ser')}
                        Audit.insertAudit(audit_user, "UserRoleDet", "ROLE", int(ret), "ERROR", details, "C")
                    except Exception:
                        self.log.exception(Logs.fileline() + ' : UserRoleDet ERROR audit insert perm')
                    return compose_ret('', Constants.cst_content_type_json, 500)

            try:
                details = {"pro_ser": ret, "by_user": args['by_user'], "result": "SUCCESS", "role_label": args['role_label'], "role_type": args['role_type']}
                Audit.insertAudit(audit_user, "UserRoleDet", "ROLE", ret, "SUCCESS", details, "C")
            except Exception:
                self.log.exception(Logs.fileline() + ' : UserRoleDet ERROR audit UserRoleCreate')

        self.log.info(Logs.fileline() + ' : TRACE UserRoleDet pro_ser=' + str(pro_ser))
        return compose_ret(ret, Constants.cst_content_type_json)

    @require_oauth()
    def delete(self, pro_ser):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        if 'id_user' not in args:
            self.log.error(Logs.fileline() + ' : UserRoleDet ERROR args missing')
            try:
                details = {"result": "ERROR", "reason": "ARGS_MISSING", "pro_ser": int(pro_ser), "missing": ["id_user"]}
                Audit.insertAudit(audit_user, "UserRoleDet", "ROLE", int(pro_ser), "ERROR", details, "D")
            except Exception:
                self.log.exception(Logs.fileline() + ' : UserRoleDet ERROR audit args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        ret = User.deleteRoleDet(pro_ser, args['id_user'])

        if not ret:
            self.log.error(Logs.fileline() + ' : TRACE UserRoleDet delete ERROR')
            try:
                details = {"result": "ERROR", "reason": "DELETE_FAILED", "pro_ser": int(pro_ser)}
                Audit.insertAudit(audit_user, "UserRoleDet", "ROLE", int(pro_ser), "ERROR", details, "D")
            except Exception:
                self.log.exception(Logs.fileline() + ' : UserRoleDet ERROR audit delete failed')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE UserRoleDet delete pro_ser=' + str(pro_ser))
        try:
            details = {"pro_ser": pro_ser, "by_user": args['id_user'], "result": "SUCCESS"}
            Audit.insertAudit(audit_user, "UserRoleDet", "ROLE", pro_ser, "SUCCESS", details, "D")
        except Exception:
            self.log.exception(Logs.fileline() + ' : UserRoleDet ERROR audit UserRoleDelete')
        return compose_ret('', Constants.cst_content_type_json)


class UserRoleByUser(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self, id_user):
        audit_user = request.oauth_user
        role = User.getRoleDetByUser(id_user)

        if not role:
            self.log.error(Logs.fileline() + ' : TRACE UserRoleByUser no role')
            try:
                details = {"result": "ERROR", "reason": "NOT_FOUND", "user_id": int(id_user)}
                Audit.insertAudit(audit_user, "UserRoleByUser", "ROLE", int(id_user), "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : UserRoleByUser ERROR audit not found')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE UserRoleByUser')
        try:
            details = {"result": "SUCCESS", "action": "QUERY", "user_id": int(id_user)}
            Audit.insertAudit(audit_user, "UserRoleByUser", "ROLE", int(id_user), "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : UserRoleByUser ERROR audit success')
        return compose_ret(role, Constants.cst_content_type_json)


class UserIdentList(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self):
        audit_user = request.oauth_user
        l_ident = User.getUserIdentList()

        if not l_ident:
            self.log.error(Logs.fileline() + ' : TRACE UserIdentList not found')

        for ident in l_ident:
            # Replace None by empty string
            for key, value in list(ident.items()):
                if ident[key] is None:
                    ident[key] = ''

        self.log.info(Logs.fileline() + ' : TRACE UserIdentList')
        try:
            details = {"result": "SUCCESS", "action": "QUERY", "count": len(l_ident)}
            Audit.insertAudit(audit_user, "UserIdentList", "USER", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : UserIdentList ERROR audit success')
        return compose_ret(l_ident, Constants.cst_content_type_json)


class UserSearch(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        l_users = User.getUserSearch(args['term'])

        if not l_users:
            self.log.error(Logs.fileline() + ' : TRACE UserSearch not found')

        for user in l_users:
            # Replace None by empty string
            for key, value in list(user.items()):
                if user[key] is None:
                    user[key] = ''

        self.log.info(Logs.fileline() + ' : TRACE UserSearch')
        try:
            details = {"result": "SUCCESS", "action": "QUERY", "count": len(l_users)}
            Audit.insertAudit(audit_user, "UserSearch", "USER", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : UserSearch ERROR audit success')
        return compose_ret(l_users, Constants.cst_content_type_json)


class UserRightsList(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self, id_user):
        audit_user = request.oauth_user
        l_rights = User.getUserListOfRights(id_user)

        if not l_rights:
            self.log.error(Logs.fileline() + ' : TRACE UserRightsList getUserListOfRights not found')
            try:
                details = {"result": "ERROR", "reason": "NOT_FOUND", "user_id": int(id_user)}
                Audit.insertAudit(audit_user, "UserRightsList", "RIGHT", int(id_user), "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : UserRightsList ERROR audit not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        self.log.info(Logs.fileline() + ' : TRACE UserRightsList')
        try:
            details = {"result": "SUCCESS", "action": "QUERY", "count": len(l_rights)}
            Audit.insertAudit(audit_user, "UserRightsList", "RIGHT", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : UserRightsList ERROR audit success')
        return compose_ret(l_rights, Constants.cst_content_type_json)

    @require_oauth()
    def post(self):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        l_rights = User.getUserRightsList(args['id_user'], args['role_type'], args['role_id'])

        # self.log.info(Logs.fileline() + ' : DEBUG UserRightsList l_rights=' + str(l_rights))

        if not l_rights:
            self.log.error(Logs.fileline() + ' : TRACE UserRightsList not found')
            try:
                details = {"result": "ERROR", "reason": "NOT_FOUND", "user_id": args.get('id_user'),
                           "role_type": args.get('role_type'), "role_id": args.get('role_id')}
                Audit.insertAudit(audit_user, "UserRightsList", "RIGHT", None, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : UserRightsList ERROR audit not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        Various.useLangDB()

        for right in l_rights:
            # Replace None by empty string
            for key, value in list(right.items()):
                if right[key] is None:
                    right[key] = ''
                elif key == 'prr_label' and right[key]:
                    right[key] = _(right[key].strip())

        self.log.info(Logs.fileline() + ' : TRACE UserRightsList')
        try:
            details = {"result": "SUCCESS", "action": "QUERY", "count": len(l_rights)}
            Audit.insertAudit(audit_user, "UserRightsList", "RIGHT", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : UserRightsList ERROR audit success')
        return compose_ret(l_rights, Constants.cst_content_type_json)


class UserRights(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self, id_user):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        if 'by_user' not in args or 'id_user' not in args or 'l_rights' not in args:
            self.log.error(Logs.fileline() + ' : UserRights ERROR args missing')
            try:
                missing = []
                if 'by_user' not in args:
                    missing.append("by_user")
                if 'id_user' not in args:
                    missing.append("id_user")
                if 'l_rights' not in args:
                    missing.append("l_rights")
                details = {"result": "ERROR", "reason": "ARGS_MISSING", "user_id": int(id_user), "missing": missing}
                Audit.insertAudit(audit_user, "UserRightsUpdate", "USER", int(id_user), "ERROR", details, "U")
            except Exception:
                self.log.exception(Logs.fileline() + ' : UserRights ERROR audit args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # update user
        if id_user > 0:
            # user permissions
            for right in args['l_rights']:
                same_granted = User.sameGranted(right['prp_ser'], right['prp_granted'])

                if right['src'] == 'prp' and same_granted is False:
                    # insert user permission
                    ret_perm = User.insertUserPermission(by_user=args['by_user'],
                                                         user=args['id_user'],
                                                         prp=right['prp_ser'],
                                                         granted=right['prp_granted'])

                    if ret_perm <= 0:
                        self.log.info(Logs.fileline() + ' : UserRights ERROR insert userPermissions')
                        try:
                            details = {"user_id": args['id_user'], "by_user": args['by_user'], "prp": right['prp_ser'],
                                       "result": "ERROR", "action": "INSERT"}
                            Audit.insertAudit(audit_user, "UserRightsUpdate", "USER", args['id_user'], "ERROR", details, "U")
                        except Exception:
                            self.log.exception(Logs.fileline() + ' : UserRights ERROR audit UserRightsUpdate')
                        return compose_ret('', Constants.cst_content_type_json, 500)

                # already user permission
                if right['src'] == 'usp':
                    # different from same right of role
                    if same_granted is False:
                        # update user permission
                        ret_perm = User.updateUserPermission(by_user=args['by_user'],
                                                             user=args['id_user'],
                                                             prp=right['prp_ser'],
                                                             granted=right['prp_granted'])

                        if ret_perm is False:
                            self.log.info(Logs.fileline() + ' : UserRights ERROR update userPermissions')
                            try:
                                details = {"user_id": args['id_user'], "by_user": args['by_user'], "prp": right['prp_ser'],
                                           "result": "ERROR", "action": "UPDATE"}
                                Audit.insertAudit(audit_user, "UserRightsUpdate", "USER", args['id_user'], "ERROR", details, "U")
                            except Exception:
                                self.log.exception(Logs.fileline() + ' : UserRights ERROR audit UserRightsUpdate')
                            return compose_ret('', Constants.cst_content_type_json, 500)

                    # same granted with same right of role, we remove user permission
                    elif same_granted is True:
                        # remove user permission
                        ret_perm = User.deleteUserPermission(user=args['id_user'],
                                                             prp=right['prp_ser'])

                        if ret_perm is False:
                            self.log.info(Logs.fileline() + ' : UserRights ERROR update userPermissions')
                            try:
                                details = {"user_id": args['id_user'], "by_user": args['by_user'], "prp": right['prp_ser'],
                                           "result": "ERROR", "action": "DELETE"}
                                Audit.insertAudit(audit_user, "UserRightsUpdate", "USER", args['id_user'], "ERROR", details, "D")
                            except Exception:
                                self.log.exception(Logs.fileline() + ' : UserRights ERROR audit UserRightsUpdate')
                            return compose_ret('', Constants.cst_content_type_json, 500)
                    else:
                        self.log.info(Logs.fileline() + ' : UserRights ERROR sameRight userPermissions')
                        try:
                            details = {"user_id": args.get('id_user'), "by_user": args.get('by_user'), "result": "ERROR",
                                       "reason": "SAME_RIGHT"}
                            Audit.insertAudit(audit_user, "UserRightsUpdate", "USER", args.get('id_user'), "ERROR",
                                              details, "D")
                        except Exception:
                            self.log.exception(Logs.fileline() + ' : UserRights ERROR audit UserRightsUpdate SAME_RIGHT')
                        return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE UserRights')
        try:
            details = {"user_id": args.get('id_user'), "by_user": args.get('by_user'), "result": "SUCCESS"}
            Audit.insertAudit(audit_user, "UserRightsUpdate", "USER", args.get('id_user'), "SUCCESS", details, "U")
        except Exception:
            self.log.exception(Logs.fileline() + ' : UserRights ERROR audit UserRightsUpdate SUCCESS')
        return compose_ret('', Constants.cst_content_type_json)


class UserPassword(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self):
        args = request.get_json() or {}

        if 'id_user' not in args or 'password' not in args:
            self.log.error(Logs.fileline() + ' : UserPassword ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        pwd_db = User.getPasswordDB(args['password'])

        ret = User.updatePassword(args['id_user'], pwd_db)

        if ret is False:
            self.log.info(Logs.fileline() + ' : TRACE UserPassword ERROR update password')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE UserPassword')
        return compose_ret('', Constants.cst_content_type_json)


class UserStatus(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        if 'id_user' not in args or 'status' not in args:
            self.log.error(Logs.fileline() + ' : UserStatus ERROR args missing')
            try:
                details = {"result": "ERROR", "reason": "ARGS_MISSING"}
                Audit.insertAudit(audit_user, "UserStatusUpdate", "USER", None, "ERROR", details, "U")
            except Exception:
                self.log.exception(Logs.fileline() + ' : UserStatus ERROR audit args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        status = args['status']
        status_label = "Active" if status == "A" else "Disabled" if status == "D" else status

        ret = User.updateStatus(args['id_user'], status)

        if ret is False:
            self.log.info(Logs.fileline() + ' : TRACE UserStatus ERROR update password')
            try:
                details = {"user_id": args['id_user'], "status": args['status'], "status_label": status_label, "result": "ERROR"}
                Audit.insertAudit(audit_user, "UserStatusUpdate", "USER", args['id_user'], "ERROR", details, "U")
            except Exception:
                self.log.exception(Logs.fileline() + ' : UserStatus ERROR audit UserStatusUpdate')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE UserStatus')
        try:
            details = {"user_id": args['id_user'], "status": args['status'], "status_label": status_label, "result": "SUCCESS"}
            Audit.insertAudit(audit_user, "UserStatusUpdate", "USER", args['id_user'], "SUCCESS", details, "U")
        except Exception:
            self.log.exception(Logs.fileline() + ' : UserStatus ERROR audit UserStatusUpdate')
        return compose_ret('', Constants.cst_content_type_json)


class UserCount(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self):
        audit_user = request.oauth_user
        res = User.getUserNbUsers()

        if not res:
            self.log.error(Logs.fileline() + ' : TRACE UserNbUsers not found')
            nb_users = 0
        else:
            nb_users = res['nb_users']

        self.log.info(Logs.fileline() + ' : TRACE UserNbUsers')
        try:
            details = {"result": "SUCCESS", "action": "QUERY", "count": int(nb_users)}
            Audit.insertAudit(audit_user, "UserCount", "USER", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : UserCount ERROR audit success')
        return compose_ret(nb_users, Constants.cst_content_type_json)


class UserConnExport(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        l_data = [['id_user', 'username', 'date', 'event', ]]

        if 'date_beg' not in args or 'date_end' not in args:
            self.log.error(Logs.fileline() + ' : UserConnExport ERROR args missing')
            try:
                details = {"result": "ERROR", "reason": "ARGS_MISSING"}
                Audit.insertAudit(audit_user, "UserConnExport", "USER", None, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : UserConnExport ERROR audit args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        try:
            date_beg = datetime.strptime(args['date_beg'], Constants.cst_isodate).date()
            date_end = datetime.strptime(args['date_end'], Constants.cst_isodate).date()
        except (ValueError, TypeError):
            self.log.exception(Logs.fileline() + ' : UserConnExport ERROR invalid date format')
            try:
                details = {"result": "ERROR", "reason": "BAD_DATE_FORMAT", "date_beg": args.get('date_beg'),
                           "date_end": args.get('date_end')}
                Audit.insertAudit(audit_user, "UserConnExport", "USER", None, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : UserConnExport ERROR audit bad date')
            return compose_ret('', Constants.cst_content_type_json, 400)

        dict_data = User.getUserConnections(str(date_beg) + ' 00:00', str(date_end) + ' 23:59')

        if dict_data:
            for d in dict_data:
                data = []

                data.append(d['id_user'])
                data.append(d['username'])

                if d['date']:
                    d['date'] = datetime.strftime(d['date'], '%Y-%m-%d %H:%M:%S')
                else:
                    d['date'] = ''

                data.append(d['date'])
                data.append(d['event'])

                l_data.append(data)

        # if no result to export
        if len(l_data) < 2:
            try:
                details = {"result": "ERROR", "reason": "NOT_FOUND", "date_beg": str(date_beg), "date_end": str(date_end)}
                Audit.insertAudit(audit_user, "UserConnExport", "USER", None, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : UserConnExport ERROR audit not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        # write csv file
        try:
            base_path = Constants.cst_path_tmp
            os.makedirs(base_path, exist_ok=True)

            filename = 'user-conn_' + str(date_beg) + '_' + str(date_end) + '.csv'
            fullpath = os.path.join(base_path, filename)

            with open(fullpath, mode='w', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=';')
                for line in l_data:
                    writer.writerow(line)

        except Exception:
            self.log.exception(Logs.fileline() + ' : post UserConnExport failed')
            try:
                details = {"result": "ERROR", "reason": "FILE_WRITE_FAILED", "date_beg": str(date_beg), "date_end": str(date_end)}
                Audit.insertAudit(audit_user, "UserConnExport", "USER", None, "ERROR", details, "R")
            except Exception as e:
                self.log.exception(Logs.fileline() + ' : UserConnExport ERROR audit write file err=' + str(e))
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE UserConnExport')
        try:
            details = {"date_beg": str(date_beg), "date_end": str(date_end), "result": "SUCCESS"}
            Audit.insertAudit(audit_user, "UserConnExport", "USER", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : UserConnExport ERROR audit UserConnExport')
        return compose_ret('', Constants.cst_content_type_json)


class UserExport(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def post(self):
        audit_user = request.oauth_user
        args = request.get_json() or {}

        l_data = [['version', 'firstname', 'lastname', 'username', 'password', 'title', 'email', 'status', 'locale',
                   'cps_id', 'rpps', 'phone', 'initial', 'birth', 'address', 'position', 'cv', 'diploma',
                   'formation', 'darrived', 'deval', 'section', 'comment', 'side_account', 'role_type', 'role_pro']]

        if 'id_user' not in args:
            self.log.error(Logs.fileline() + ' : UserExport ERROR args missing')
            try:
                details = {"result": "ERROR", "reason": "ARGS_MISSING"}
                Audit.insertAudit(audit_user, "UserExport", "USER", None, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : UserExport ERROR audit args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        dict_data = User.getUserExport()

        if dict_data:
            for d in dict_data:
                data = []

                data.append('v3')

                if d['firstname']:
                    data.append(d['firstname'])
                else:
                    data.append('')

                if d['lastname']:
                    data.append(d['lastname'])
                else:
                    data.append('')

                if d['username']:
                    data.append(d['username'])
                else:
                    data.append('')

                if d['password']:
                    data.append(d['password'])
                else:
                    data.append('')

                if d['titre']:
                    data.append(d['titre'])
                else:
                    data.append('')

                if d['email']:
                    data.append(d['email'])
                else:
                    data.append('')

                if d['status'] and d['status'] == Constants.cst_user_active:
                    data.append('A')
                else:
                    data.append('D')

                if d['locale']:
                    if d['locale'] == 35:
                        d['locale'] = 'FR'
                    elif d['locale'] == 34:
                        d['locale'] = 'EN'
                    elif d['locale'] == 75:
                        d['locale'] = 'US'
                    elif d['locale'] == 724:
                        d['locale'] = 'ES'
                    elif d['locale'] == 118:
                        d['locale'] = 'AR'
                    elif d['locale'] == 1113:
                        d['locale'] = 'KM'
                    elif d['locale'] == 1215:
                        d['locale'] = 'LO'
                    elif d['locale'] == 137:
                        d['locale'] = 'MG'
                    elif d['locale'] == 1620:
                        d['locale'] = 'PT'

                    data.append(d['locale'])
                else:
                    data.append('')

                if d['cps_id']:
                    data.append(d['cps_id'])
                else:
                    data.append('')

                if d['rpps']:
                    data.append(d['rpps'])
                else:
                    data.append('')

                if d['tel']:
                    data.append(d['tel'])
                else:
                    data.append('')

                if d['initiale']:
                    data.append(d['initiale'])
                else:
                    data.append('')

                if d['ddn']:
                    data.append(d['ddn'])
                else:
                    data.append('')

                if d['adresse']:
                    data.append(d['adresse'])
                else:
                    data.append('')

                if d['position']:
                    data.append(d['position'])
                else:
                    data.append('')

                if d['cv']:
                    data.append(d['cv'])
                else:
                    data.append('')

                if d['diplome']:
                    data.append(d['diplome'])
                else:
                    data.append('')

                if d['formation']:
                    data.append(d['formation'])
                else:
                    data.append('')

                if d['darrive']:
                    data.append(d['darrive'])
                else:
                    data.append('')

                if d['deval']:
                    data.append(d['deval'])
                else:
                    data.append('')

                if d['section']:
                    data.append(d['section'])
                else:
                    data.append('')

                if d['commentaire']:
                    data.append(d['commentaire'])
                else:
                    data.append('')

                if d['side_account']:
                    data.append(d['side_account'])
                else:
                    data.append('')

                if d['role_type']:
                    data.append(d['role_type'])
                else:
                    data.append('')

                if d['role_pro']:
                    data.append(d['role_pro'])
                else:
                    data.append('')

                l_data.append(data)

        # if no result to export
        if len(l_data) < 2:
            try:
                details = {"result": "ERROR", "reason": "NOT_FOUND"}
                Audit.insertAudit(audit_user, "UserExport", "USER", None, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : UserExport ERROR audit not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        # write csv file
        try:
            today = datetime.now().strftime("%Y%m%d")

            filename = 'users_' + str(today) + '.csv'

            with open('tmp/' + filename, mode='w', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=';')
                for line in l_data:
                    writer.writerow(line)

        except Exception:
            self.log.exception(Logs.fileline() + ' : post UserExport failed')
            return False

        self.log.info(Logs.fileline() + ' : TRACE UserExport')
        try:
            details = {"user_id": args['id_user'], "result": "SUCCESS"}
            Audit.insertAudit(audit_user, "UserExport", "USER", None, "SUCCESS", details, "R")
        except Exception:
            self.log.exception(Logs.fileline() + ' : UserExport ERROR audit UserExport')
        return compose_ret('', Constants.cst_content_type_json)


class UserImport(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self, filename, id_user):
        audit_user = request.oauth_user

        if not filename or id_user <= 0:
            self.log.error(Logs.fileline() + ' : UserImport ERROR args missing')
            try:
                details = {"result": "ERROR", "reason": "ARGS_MISSING", "filename": str(filename), "user_id": int(id_user)}
                Audit.insertAudit(audit_user, "UserImport", "USER", int(id_user), "ERROR", details, "U")
            except Exception:
                self.log.exception(Logs.fileline() + ' : UserImport ERROR audit args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # Read CSV user
        path = Constants.cst_path_tmp

        with open(os.path.join(path, filename), 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';', quotechar='"')
            l_rows = list(csv_reader)

        # clean double quotes
        l_rows = [[col.strip('"') if col else col for col in row] for row in l_rows]

        if not l_rows or len(l_rows) < 2:
            self.log.error(Logs.fileline() + ' : TRACE UserImport ERROR file empty')
            try:
                details = {"result": "ERROR", "reason": "FILE_EMPTY", "filename": str(filename), "user_id": int(id_user)}
                Audit.insertAudit(audit_user, "UserImport", "USER", int(id_user), "ERROR", details, "U")
            except Exception:
                self.log.exception(Logs.fileline() + ' : UserImport ERROR audit file empty')
            return compose_ret('', Constants.cst_content_type_json, 500)

        # remove headers line
        l_rows.pop(0)

        # check version
        if l_rows[0][0] != 'v3':
            self.log.error(Logs.fileline() + ' : TRACE UserImport ERROR wrong version')
            try:
                details = {"result": "ERROR", "reason": "WRONG_VERSION", "filename": str(filename), "version": str(l_rows[0][0])}
                Audit.insertAudit(audit_user, "UserImport", "USER", int(id_user), "ERROR", details, "U")
            except Exception:
                self.log.exception(Logs.fileline() + ' : UserImport ERROR audit wrong version')
            return compose_ret('', Constants.cst_content_type_json, 409)

        # check number of column (dont forget version columns)
        if len(l_rows[0]) != 26:
            self.log.error(Logs.fileline() + ' : TRACE UserImport ERROR wrong number of column')
            try:
                details = {"result": "ERROR", "reason": "WRONG_COLUMN_OR_ORDER", "filename": str(filename),
                           "col_count": len(l_rows[0]), "expected": 26}
                Audit.insertAudit(audit_user, "UserImport", "USER", int(id_user), "ERROR", details, "U")
            except Exception:
                self.log.exception(Logs.fileline() + ' : UserImport ERROR audit wrong column')
            return compose_ret('', Constants.cst_content_type_json, 409)

        for row in l_rows:
            if row:
                firstname    = row[1]
                lastname     = row[2]
                username     = row[3]
                password     = row[4]
                title        = row[5]
                email        = row[6]
                status       = row[7]
                locale       = row[8]
                cps_id       = row[9]
                rpps         = row[10]
                phone        = row[11]
                initial      = row[12]
                birth        = row[13]
                address      = row[14]
                position     = row[15]
                cv           = row[16]
                diploma      = row[17]
                formation    = row[18]
                darrived     = row[19]
                deval        = row[20]
                section      = row[21]
                comment      = row[22]
                side_account = row[23]
                role_type    = row[24]
                role_pro     = row[25]

                # status convert
                if status and status == 'A':
                    status = Constants.cst_user_active
                else:
                    status = Constants.cst_user_inactive

                # locale convert
                if locale:
                    if locale == 'FR':
                        locale = 35
                    elif locale == 'UK':
                        locale = 34
                    elif locale == 'US':
                        locale = 75
                    elif locale == 'ES':
                        locale = 724
                    elif locale == 'AR':
                        locale = 118
                    elif locale == 'KM':
                        locale = 1113
                    elif locale == 'LO':
                        locale = 1215
                    elif locale == 'MG':
                        locale = 137
                    elif locale == 'PT':
                        locale = 1620
                else:
                    locale = 35

                # Check if user exist (same username, lastname and firstname)
                # if EXIST => UPDATE (all except password)
                if User.exist(firstname, lastname, username):
                    ret = User.updateUserByImport(firstname=firstname,
                                                  lastname=lastname,
                                                  username=username,
                                                  titre=title,
                                                  email=email,
                                                  status=status,
                                                  locale=locale,
                                                  cps_id=cps_id,
                                                  rpps=rpps,
                                                  tel=phone,
                                                  initiale=initial,
                                                  ddn=birth,
                                                  adresse=address,
                                                  position=position,
                                                  cv=cv,
                                                  diplome=diploma,
                                                  formation=formation,
                                                  darrive=darrived,
                                                  deval=deval,
                                                  section=section,
                                                  commentaire=comment,
                                                  side_account=side_account,
                                                  role_type=role_type,
                                                  role_pro=role_pro)

                    if not ret:
                        self.log.error(Logs.alert() + ' : UserImport ERROR update user username=' + str(username))
                        try:
                            details = {"username": username, "action": "UPDATE", "result": "ERROR"}
                            Audit.insertAudit(audit_user, "UserImport", "USER", None, "ERROR", details, "U")
                        except Exception:
                            self.log.exception(Logs.fileline() + ' : UserImport ERROR audit UserImport')
                        return compose_ret('', Constants.cst_content_type_json, 500)

                # if not EXIST => INSERT
                else:
                    # insert in sigl_user_data
                    ret = User.insertUser(id_owner=id_user,
                                          role_type=role_type,
                                          firstname=firstname,
                                          lastname=lastname,
                                          username=username,
                                          password=password,
                                          titre=title,
                                          email=email,
                                          status=status,
                                          locale=locale,
                                          cps_id=cps_id,
                                          rpps=rpps,
                                          tel=phone,
                                          initiale=initial,
                                          ddn=birth,
                                          adresse=address,
                                          position=position,
                                          cv=cv,
                                          diplome=diploma,
                                          formation=formation,
                                          darrive=darrived,
                                          deval=deval,
                                          section=section,
                                          side_account=side_account,
                                          commentaire=comment,
                                          origin=id_user,
                                          role_pro=role_pro)

                    if ret <= 0:
                        self.log.error(Logs.alert() + ' : UserImport ERROR insert user')
                        try:
                            details = {"username": username, "action": "INSERT", "result": "ERROR"}
                            Audit.insertAudit(audit_user, "UserImport", "USER", None, "ERROR", details, "U")
                        except Exception:
                            self.log.exception(Logs.fileline() + ' : UserImport ERROR audit UserImport')
                        return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE UserImport')
        try:
            details = {"filename": filename, "user_id": id_user, "result": "SUCCESS"}
            Audit.insertAudit(audit_user, "UserImport", "USER", int(id_user), "SUCCESS", details, "U")
        except Exception:
            self.log.exception(Logs.fileline() + ' : UserImport ERROR audit UserImport')
        return compose_ret('', Constants.cst_content_type_json, 200)


class UserRoleExist(Resource):
    log = logging.getLogger('log_services')

    @require_oauth()
    def get(self, role_label):
        audit_user = request.oauth_user
        ret = User.role_exist(role_label)

        if ret and ret == -1:
            self.log.error(Logs.fileline() + ' : ' + 'UserRoleExist ERROR sql')
            try:
                details = {"result": "ERROR", "reason": "SQL_ERROR", "role_label": str(role_label)}
                Audit.insertAudit(audit_user, "UserRoleExist", "ROLE", None, "ERROR", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : UserRoleExist ERROR audit sql')
            return compose_ret(-1, Constants.cst_content_type_json, 500)

        if ret:
            self.log.error(Logs.fileline() + ' : ' + 'UserRoleExist WARNING role already exist')
            try:
                details = {"result": "SUCCESS", "action": "QUERY", "role_label": role_label}
                Audit.insertAudit(audit_user, "UserRoleExist", "ROLE", None, "SUCCESS", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : UserRoleExist ERROR audit success')
            return compose_ret(1, Constants.cst_content_type_json, 200)
        else:
            self.log.info(Logs.fileline() + ' : UserRoleExist code ok :' + str(role_label))
            try:
                details = {"result": "SUCCESS", "action": "QUERY", "role_label": role_label}
                Audit.insertAudit(audit_user, "UserRoleExist", "ROLE", None, "SUCCESS", details, "R")
            except Exception:
                self.log.exception(Logs.fileline() + ' : UserRoleExist ERROR audit success')
            return compose_ret(0, Constants.cst_content_type_json, 200)
