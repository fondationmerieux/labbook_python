# -*- coding:utf-8 -*-
import logging
import gettext
import random
import string

from datetime import datetime
from flask import request
from flask_restful import Resource

from app.models.General import compose_ret
from app.models.Constants import Constants
from app.models.User import User
from app.models.Logs import Logs
from app.models.Various import Various


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
            self.log.info(Logs.fileline() + ' : UserAccess authorized role=' + str(user['role_type']) + ' | login=' + str(login))
            return compose_ret(user['role_type'], Constants.cst_content_type_json)
        elif ret is False:
            self.log.info(Logs.fileline() + ' : UserAccess not authorized ' + str(login))
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
        for key, value in list(user.items()):
            if user[key] is None:
                user[key] = ''

        self.log.info(Logs.fileline() + ' : TRACE UserByLogin')
        return compose_ret(user, Constants.cst_content_type_json)


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
        for key, value in list(user.items()):
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
           'comment' not in args or 'id_pres' not in args or 'role_type' not in args or 'role_pro' not in args:
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

            if ret is False:
                self.log.info(Logs.fileline() + ' : TRACE UserDet ERROR update user')
                return compose_ret('', Constants.cst_content_type_json, 500)

        # insert new user
        else:
            if 'id_owner' not in args or 'password' not in args:
                self.log.error(Logs.fileline() + ' : UserDet ERROR args missing')
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

            if ret <= 0:
                self.log.error(Logs.alert() + ' : UserDet ERROR insert user')
                return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE UserDet id_user=' + str(id_user))
        return compose_ret(ret, Constants.cst_content_type_json)


class UserStaffDet(Resource):
    log = logging.getLogger('log_services')

    def post(self, id_user):
        args = request.get_json()

        if 'id_user' not in args or 'firstname' not in args or 'lastname' not in args or 'email' not in args or \
           'title' not in args or 'initial' not in args or 'birth' not in args or 'phone' not in args or \
           'arrived' not in args or 'position' not in args or 'section' not in args or 'last_eval' not in args or \
           'address' not in args or 'cv' not in args or 'diploma' not in args or 'training' not in args or \
           'comment' not in args or 'role_type' not in args or 'role_pro' not in args:
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
                return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE UserStaffDet id_user=' + str(id_user))
        return compose_ret('', Constants.cst_content_type_json)


class UserList(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

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
        return compose_ret(l_users, Constants.cst_content_type_json)


class UserRoleList(Resource):
    log = logging.getLogger('log_services')

    def post(self, type=''):
        args = request.get_json()

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
        return compose_ret(l_roles, Constants.cst_content_type_json)


class UserRoleDet(Resource):
    log = logging.getLogger('log_services')

    def get(self, pro_ser):
        role = User.getRoleDetails(pro_ser)

        if not role:
            self.log.error(Logs.fileline() + ' : TRACE UserRoleDet no role')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE UserRoleDet')
        return compose_ret(role, Constants.cst_content_type_json)

    def post(self, pro_ser):
        args = request.get_json()

        if 'by_user' not in args or 'id_user' not in args or 'role_type' not in args or 'role_label' not in args or \
           'role_color_1' not in args or 'role_color_2' not in args or 'role_text_color' not in args or \
           'l_rights' not in args:
            self.log.error(Logs.fileline() + ' : UserRoleDet ERROR args missing')
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
                    return compose_ret('', Constants.cst_content_type_json, 500)

        # insert new user
        else:
            role = User.getUserRole(args['role_type'])

            if not role:
                self.log.error(Logs.fileline() + ' : UserRoleDet ERROR role not found')
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
                return compose_ret('', Constants.cst_content_type_json, 500)

            # insert profile_permissions
            for right in args['l_rights']:
                ret_perm = User.insertProfilePermission(by_user=args['by_user'],
                                                        pro=ret,
                                                        prp=right['prp_ser'],
                                                        granted=right['prp_granted'])

                if ret_perm <= 0:
                    self.log.error(Logs.alert() + ' : UserRoleDet ERROR insert profilePermissions')
                    return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE UserRoleDet pro_ser=' + str(pro_ser))
        return compose_ret(ret, Constants.cst_content_type_json)

    def delete(self, pro_ser):
        args = request.get_json()

        if 'id_user' not in args:
            self.log.error(Logs.fileline() + ' : UserRoleDet ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        ret = User.deleteRoleDet(pro_ser, args['id_user'])

        if not ret:
            self.log.error(Logs.fileline() + ' : TRACE UserRoleDet delete ERROR')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE UserRoleDet delete pro_ser=' + str(pro_ser))
        return compose_ret('', Constants.cst_content_type_json)


class UserRoleByUser(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_user):
        role = User.getRoleDetByUser(id_user)

        if not role:
            self.log.error(Logs.fileline() + ' : TRACE UserRoleByUser no role')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE UserRoleByUser')
        return compose_ret(role, Constants.cst_content_type_json)


class UserIdentList(Resource):
    log = logging.getLogger('log_services')

    def get(self):
        l_ident = User.getUserIdentList()

        if not l_ident:
            self.log.error(Logs.fileline() + ' : TRACE UserIdentList not found')

        for ident in l_ident:
            # Replace None by empty string
            for key, value in list(ident.items()):
                if ident[key] is None:
                    ident[key] = ''

        self.log.info(Logs.fileline() + ' : TRACE UserIdentList')
        return compose_ret(l_ident, Constants.cst_content_type_json)


class UserSearch(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        l_users = User.getUserSearch(args['term'])

        if not l_users:
            self.log.error(Logs.fileline() + ' : TRACE UserSearch not found')

        for user in l_users:
            # Replace None by empty string
            for key, value in list(user.items()):
                if user[key] is None:
                    user[key] = ''

        self.log.info(Logs.fileline() + ' : TRACE UserSearch')
        return compose_ret(l_users, Constants.cst_content_type_json)


class UserRightsList(Resource):
    log = logging.getLogger('log_services')

    def get(self, id_user):
        l_rights = User.getUserListOfRights(id_user)

        if not l_rights:
            self.log.error(Logs.fileline() + ' : TRACE UserRightsList getUserListOfRights not found')
            return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE UserRightsList')
        return compose_ret(l_rights, Constants.cst_content_type_json)

    def post(self):
        args = request.get_json()

        l_rights = User.getUserRightsList(args['id_user'], args['role_type'], args['role_id'])

        # self.log.info(Logs.fileline() + ' : DEBUG UserRightsList l_rights=' + str(l_rights))

        if not l_rights:
            self.log.error(Logs.fileline() + ' : TRACE UserRightsList not found')
            return compose_ret('', Constants.cst_content_type_json, 500)

        Various.useLangDB()

        for right in l_rights:
            # Replace None by empty string
            for key, value in list(right.items()):
                if right[key] is None:
                    right[key] = ''
                elif key == 'prr_label' and right[key]:
                    right[key] = _(right[key].strip())

        self.log.info(Logs.fileline() + ' : TRACE UserRightsList')
        return compose_ret(l_rights, Constants.cst_content_type_json)


class UserRights(Resource):
    log = logging.getLogger('log_services')

    def post(self, id_user):
        args = request.get_json()

        if 'by_user' not in args or 'id_user' not in args or 'l_rights' not in args:
            self.log.error(Logs.fileline() + ' : UserRights ERROR args missing')
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
                            return compose_ret('', Constants.cst_content_type_json, 500)

                    # same granted with same right of role, we remove user permission
                    elif same_granted is True:
                        # remove user permission
                        ret_perm = User.deleteUserPermission(user=args['id_user'],
                                                             prp=right['prp_ser'])

                        if ret_perm is False:
                            self.log.info(Logs.fileline() + ' : UserRights ERROR update userPermissions')
                            return compose_ret('', Constants.cst_content_type_json, 500)
                    else:
                        self.log.info(Logs.fileline() + ' : UserRights ERROR sameRight userPermissions')
                        return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE UserRights')
        return compose_ret('', Constants.cst_content_type_json)


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


class UserConnExport(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        l_data = [['id_user', 'username', 'date', 'event', ]]

        if 'date_beg' not in args or 'date_end' not in args:
            self.log.error(Logs.fileline() + ' : UserConnExport ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        dict_data = User.getUserConnections(args['date_beg'] + ' 00:00', args['date_end'] + ' 23:59')

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
            return compose_ret('', Constants.cst_content_type_json, 404)

        # write csv file
        try:
            import csv

            filename = 'user-conn_' + args['date_beg'] + '_' + args['date_end'] + '.csv'

            with open('tmp/' + filename, mode='w', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=';')
                for line in l_data:
                    writer.writerow(line)

        except Exception as err:
            self.log.error(Logs.fileline() + ' : post UserConnExport failed, err=%s', err)
            return False

        self.log.info(Logs.fileline() + ' : TRACE UserConnExport')
        return compose_ret('', Constants.cst_content_type_json)


class UserExport(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        l_data = [['version', 'firstname', 'lastname', 'username', 'password', 'title', 'email', 'status', 'locale',
                   'cps_id', 'rpps', 'phone', 'initial', 'birth', 'address', 'position', 'cv', 'diploma',
                   'formation', 'darrived', 'deval', 'section', 'comment', 'side_account', 'role']]

        if 'id_user' not in args:
            self.log.error(Logs.fileline() + ' : UserExport ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        dict_data = User.getUserExport()

        if dict_data:
            for d in dict_data:
                data = []

                data.append('v2')

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

                l_data.append(data)

        # if no result to export
        if len(l_data) < 2:
            return compose_ret('', Constants.cst_content_type_json, 404)

        # write csv file
        try:
            import csv

            today = datetime.now().strftime("%Y%m%d")

            filename = 'users_' + str(today) + '.csv'

            with open('tmp/' + filename, mode='w', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=';')
                for line in l_data:
                    writer.writerow(line)

        except Exception as err:
            self.log.error(Logs.fileline() + ' : post UserExport failed, err=%s', err)
            return False

        self.log.info(Logs.fileline() + ' : TRACE UserExport')
        return compose_ret('', Constants.cst_content_type_json)


class UserImport(Resource):
    log = logging.getLogger('log_services')

    def get(self, filename, id_user):

        if not filename or id_user <= 0:
            self.log.error(Logs.fileline() + ' : UserImport ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        # Read CSV user
        import os

        from csv import reader

        path = Constants.cst_path_tmp

        with open(os.path.join(path, filename), 'r', encoding='utf-8') as csv_file:
            csv_reader = reader(csv_file, delimiter=';')
            l_rows = list(csv_reader)

        if not l_rows or len(l_rows) < 2:
            self.log.error(Logs.fileline() + ' : TRACE UserImport ERROR file empty')
            return compose_ret('', Constants.cst_content_type_json, 500)

        # remove headers line
        l_rows.pop(0)

        # check version
        if l_rows[0][0] != 'v2':
            self.log.error(Logs.fileline() + ' : TRACE UserImport ERROR wrong version')
            return compose_ret('', Constants.cst_content_type_json, 409)

        # check number of column (dont forget version columns)
        if len(l_rows[0]) != 25:
            self.log.error(Logs.fileline() + ' : TRACE UserImport ERROR wrong number of column')
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
                    ret = User.UpdateUserByImport(firstname=firstname,
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
                        return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE UserImport')
        return compose_ret('', Constants.cst_content_type_json, 200)
