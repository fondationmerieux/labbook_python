# -*- coding:utf-8 -*-
import logging

# from datetime import datetime
from flask import request
from flask_restful import Resource

from app.models.General import compose_ret
from app.models.Constants import *
from app.models.User import *
from app.models.Logs import Logs


class UserAccess(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        if 'login' not in args or 'pwd' not in args:
            self.log.error(Logs.fileline() + ' : UserAccess ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        login = args['login']
        pwd   = args['pwd']

        user = User.getUserByLogin(login)

        if not user:
            self.log.error(Logs.fileline() + ' : UserAccess login not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        pwd = args['pwd']

        # password hash (TODO by Bcrypt)
        import hashlib

        salt_start = user['password'].find(":")
        salt = user['password'][salt_start + 1:]

        len_pwd   = len(pwd)
        len_start = len_pwd - 1
        len_end   = 40 - len_pwd + len_start

        pwd = pwd + salt[len_start:len_end]

        pwd_md5  = hashlib.md5(pwd.encode()).hexdigest()

        pwd_sha1 = hashlib.sha1(pwd_md5.encode())
        pwd_sha1 = pwd_sha1.hexdigest()

        pwd_db   = pwd_sha1 + ':' + salt

        ret = User.checkUserAccess(login, pwd_db)

        if ret is True:
            self.log.info(Logs.fileline() + ' : TRACE UserAccess authorized role=' + str(user['id_role']) + ' | login=' + str(login))
            return compose_ret(user['id_role'], Constants.cst_content_type_json)
        elif ret is False:
            self.log.info(Logs.fileline() + ' : TRACE UserAccess not authorized ' + str(login))
            return compose_ret('', Constants.cst_content_type_json, 401)
        else:
            self.log.error(Logs.fileline() + ' : UserAccess ERROR checkUserAccess')
            return compose_ret('', Constants.cst_content_type_json, 500)


class UserDet(Resource):
    log = logging.getLogger('log_services')

    def get(self, login):
        user = User.getUserByLogin(login)

        if not user:
            self.log.error(Logs.fileline() + ' : TRACE UserDet')
            return compose_ret('', Constants.cst_content_type_json, 500)

        # Replace None by empty string
        for key, value in user.items():
            if user[key] is None:
                user[key] = ''

        self.log.info(Logs.fileline() + ' : TRACE UserDet')
        return compose_ret(user, Constants.cst_content_type_json)


class UserByRole(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_role):
        l_users = User.getUsersByRole(id_role)

        if not l_users:
            self.log.error(Logs.fileline() + ' : TRACE UserByRole')
            return compose_ret('', Constants.cst_content_type_json, 404)

        for user in l_users:
            # Replace None by empty string
            for key, value in user.items():
                if user[key] is None:
                    user[key] = ''

        self.log.info(Logs.fileline() + ' : TRACE UserByRole')
        return compose_ret(l_users, Constants.cst_content_type_json)


class UserRights(Resource):
    log = logging.getLogger('log_services')

    def get(self, role):
        rights = User.getRightsByRole(role)

        if not rights:
            self.log.error(Logs.fileline() + ' : TRACE UserRights')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE UserRights')
        return compose_ret(rights, Constants.cst_content_type_json)
