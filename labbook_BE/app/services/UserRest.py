# -*- coding:utf-8 -*-
import logging

from datetime import datetime
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

        user = User.getUserByLogin(login)

        if not user:
            self.log.error(Logs.fileline() + ' : UserAccess login not found')
            return compose_ret('', Constants.cst_content_type_json, 404)

        salt_start = user['password'].find(":")
        salt = user['password'][salt_start + 1:]

        pwd_db = User.getPasswordDB(args['pwd'], salt)

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


class UserByLogin(Resource):
    log = logging.getLogger('log_services')

    def get(self, login):
        user = User.getUserByLogin(login)

        if not user:
            self.log.error(Logs.fileline() + ' : TRACE UserByLogin')
            return compose_ret('', Constants.cst_content_type_json, 500)

        # Replace None by empty string
        for key, value in user.items():
            if user[key] is None:
                user[key] = ''

        self.log.info(Logs.fileline() + ' : TRACE UserByLogin')
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


class UserDet(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_user):
        user = User.getUserDetails(id_user)

        if not user:
            self.log.error(Logs.fileline() + ' : TRACE UserDet no user')
            return compose_ret('', Constants.cst_content_type_json, 500)

        if user['birth']:
            user['birth'] = datetime.strftime(user['birth'], '%Y-%m-%d')

        if user['arrived']:
            user['arrived'] = datetime.strftime(user['arrived'], '%Y-%m-%d')

        if user['last_eval']:
            user['last_eval'] = datetime.strftime(user['last_eval'], '%Y-%m-%d')

        # Replace None by empty string
        for key, value in user.items():
            if user[key] is None:
                user[key] = ''

        self.log.info(Logs.fileline() + ' : TRACE UserDet')
        return compose_ret(user, Constants.cst_content_type_json)

    def post(self, id_user):
        args = request.get_json()

        if 'id_user' not in args or 'login' not in args or 'cps' not in args or 'rpps' not in args or \
           'firstname' not in args or 'lastname' not in args or 'lang' not in args or 'email' not in args or \
           'title' not in args or 'initial' not in args or 'birth' not in args or 'phone' not in args or \
           'arrived' not in args or 'position' not in args or 'section' not in args or 'last_eval' not in args or \
           'address' not in args or 'cv' not in args or 'diploma' not in args or 'training' not in args or \
           'comment' not in args or 'id_role' not in args or 'id_pres' not in args:
            self.log.error(Logs.fileline() + ' : UserDet ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # update user
        if id_user > 0:
            if 'stat' not in args:
                self.log.error(Logs.fileline() + ' : UserDet ERROR args missing')
                return compose_ret('', Constants.cst_content_type_json, 400)

            # get login by id_user
            user = User.getUserDetails(id_user)

            if not user:
                self.log.error(Logs.fileline() + ' : TRACE UserDet no user')
                return compose_ret('', Constants.cst_content_type_json, 500)

            # get id_group in sigl_pj_group with login
            res = User.getUserIdGroup(user['username'])

            if not res:
                self.log.error(Logs.fileline() + ' : TRACE UserDet no id_group')
                return compose_ret('', Constants.cst_content_type_json, 500)

            id_group = res['id_group']

            # update sigl_user_data
            ret = User.updateUser(id_data=id_user,
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

            if ret is False:
                self.log.info(Logs.fileline() + ' : TRACE UserDet ERROR update user')
                return compose_ret('', Constants.cst_content_type_json, 500)

            if user['username'] != args['login']:
                # update sigl_pj_group
                ret = User.updateUserName(user['username'], args['login'])

                if ret is False:
                    self.log.info(Logs.fileline() + ' : TRACE UserDet ERROR update user Name')
                    return compose_ret('', Constants.cst_content_type_json, 500)

            # update sigl_pj_group_link
            ret = User.updateUserRole(id_group, args['id_role'])

            if ret is False:
                self.log.info(Logs.fileline() + ' : TRACE UserDet ERROR update user Role')
                return compose_ret('', Constants.cst_content_type_json, 500)

        # insert new user
        else:
            if 'id_owner' not in args or 'password' not in args:
                self.log.error(Logs.fileline() + ' : UserDet ERROR args missing')
                return compose_ret('', Constants.cst_content_type_json, 400)

            pwd_db = User.getPasswordDB(args['password'])

            # insert into sigl_pj_group
            ret = User.insertUserName(name=args['login'])

            if ret <= 0:
                self.log.error(Logs.alert() + ' : UserDet ERROR insert user Name')
                return compose_ret('', Constants.cst_content_type_json, 500)

            res = {}
            res['id_group'] = ret

            # insert into sigl_pj_group_link
            ret = User.insertUserRole(id_group=res['id_group'],
                                      id_group_parent=1000,  # I cant explain 1000
                                      id_role=args['id_role'])

            if ret <= 0:
                self.log.error(Logs.alert() + ' : UserDet ERROR insert user Role')
                return compose_ret('', Constants.cst_content_type_json, 500)

            res['id_group_link'] = ret

            # insert in sigl_user_data
            ret = User.insertUser(id_owner=args['id_owner'],
                                  id_group=res['id_group'],
                                  username=args['login'],
                                  password=pwd_db,
                                  cps_id=args['cps'],
                                  rpps=args['rpps'],
                                  status=29,
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

            if ret <= 0:
                self.log.error(Logs.alert() + ' : UserDet ERROR insert user')
                return compose_ret('', Constants.cst_content_type_json, 500)

            res['id_user'] = ret

        self.log.info(Logs.fileline() + ' : TRACE UserDet id_user=' + str(id_user))
        return compose_ret('', Constants.cst_content_type_json)


class UserStaffDet(Resource):
    log = logging.getLogger('log_services')

    def post(self, id_user):
        args = request.get_json()

        if 'id_user' not in args or 'firstname' not in args or 'lastname' not in args or 'email' not in args or \
           'title' not in args or 'initial' not in args or 'birth' not in args or 'phone' not in args or \
           'arrived' not in args or 'position' not in args or 'section' not in args or 'last_eval' not in args or \
           'address' not in args or 'cv' not in args or 'diploma' not in args or 'training' not in args or \
           'comment' not in args:
            self.log.error(Logs.fileline() + ' : UserStaffDet ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # update user
        if id_user > 0:
            # get login by id_user
            user = User.getUserDetails(id_user)

            if not user:
                self.log.error(Logs.fileline() + ' : TRACE UserStaffDet no user')
                return compose_ret('', Constants.cst_content_type_json, 500)

            # update sigl_user_data
            ret = User.updateUser(id_data=id_user,
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
                                  commentaire=args['comment'])

            if ret is False:
                self.log.info(Logs.fileline() + ' : TRACE UserStaffDet ERROR update user')
                return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE UserStaffDet id_user=' + str(id_user))
        return compose_ret('', Constants.cst_content_type_json)


class UserList(Resource):
    log = logging.getLogger('log_services')

    def post(self, id_group):
        args = request.get_json()

        id_lab = User.getUserGroupParent(id_group)

        self.log.error(Logs.fileline() + ' : TRACE UserList id_lab=' + str(id_lab))

        if not args:
            args = {}

        l_users = User.getUserList(args, id_lab['id_group_parent'])

        if not l_users:
            self.log.error(Logs.fileline() + ' : TRACE UserList not found')

        for user in l_users:
            # Replace None by empty string
            for key, value in user.items():
                if user[key] is None:
                    user[key] = ''

            if user['birth']:
                user['birth'] = datetime.strftime(user['birth'], '%Y-%m-%d')

            if user['arrived']:
                user['arrived'] = datetime.strftime(user['arrived'], '%Y-%m-%d')

            if user['last_eval']:
                user['last_eval'] = datetime.strftime(user['last_eval'], '%Y-%m-%d')

        self.log.info(Logs.fileline() + ' : TRACE UserList')
        return compose_ret(l_users, Constants.cst_content_type_json)


class UserSearch(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        l_users = User.getUserSearch(args['term'])

        if not l_users:
            self.log.error(Logs.fileline() + ' : TRACE UserSearch not found')

        for user in l_users:
            # Replace None by empty string
            for key, value in user.items():
                if user[key] is None:
                    user[key] = ''

        self.log.info(Logs.fileline() + ' : TRACE UserSearch')
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


class UserPassword(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

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

    def post(self):
        args = request.get_json()

        if 'id_user' not in args or 'status' not in args:
            self.log.error(Logs.fileline() + ' : UserStatus ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        ret = User.updateStatus(args['id_user'], args['status'])

        if ret is False:
            self.log.info(Logs.fileline() + ' : TRACE UserStatus ERROR update password')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE UserStatus')
        return compose_ret('', Constants.cst_content_type_json)


class UserCount(Resource):
    log = logging.getLogger('log_services')

    def get(self):

        res = User.getUserNbUsers()

        if not res:
            self.log.error(Logs.fileline() + ' : TRACE UserNbUsers not found')
            nb_users = 0
        else:
            nb_users = res['nb_users']

        self.log.info(Logs.fileline() + ' : TRACE UserNbUsers')
        return compose_ret(nb_users, Constants.cst_content_type_json)
