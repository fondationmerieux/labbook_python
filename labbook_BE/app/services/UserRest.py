# -*- coding:utf-8 -*-
import logging
import gettext

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
            self.log.info(Logs.fileline() + ' : TRACE UserAccess authorized role=' + str(user['role_type']) + ' | login=' + str(login))
            return compose_ret(user['role_type'], Constants.cst_content_type_json)
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
        for key, value in list(user.items()):
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
            for key, value in list(user.items()):
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
           'comment' not in args or 'id_pres' not in args or 'role_type' not in args:
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
                    return compose_ret(id_user, Constants.cst_content_type_json, 500)

        # insert new user
        else:
            if 'id_owner' not in args or 'password' not in args:
                self.log.error(Logs.fileline() + ' : UserDet ERROR args missing')
                return compose_ret('', Constants.cst_content_type_json, 400)

            pwd_db = User.getPasswordDB(args['password'])

            # insert in sigl_user_data
            ret = User.insertUser(id_owner=args['id_owner'],
                                  role_type=args['role_type'],
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

    def get(self):
        l_roles = User.getUserRoleList()

        if not l_roles:
            self.log.error(Logs.fileline() + ' : TRACE UserRoleList not found')

        Various.useLangDB()

        for role in l_roles:
            # Replace None by empty string
            for key, value in list(role.items()):
                if role[key] is None:
                    role[key] = ''
                elif key == 'label' and role[key]:
                    role[key] = _(role[key].strip())

        self.log.info(Logs.fileline() + ' : TRACE UserRoleList')
        return compose_ret(l_roles, Constants.cst_content_type_json)


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


class UserConnExport(Resource):
    log = logging.getLogger('log_services')

    def post(self):
        args = request.get_json()

        l_data = [['id_user', 'username', 'date', 'event', ]]

        if 'date_beg' not in args or 'date_end' not in args:
            self.log.error(Logs.fileline() + ' : UserConnExport ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        dict_data = User.getUserConnections(args['date_beg'], args['date_end'])

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

        l_data = [['firstname', 'lastname', 'username', 'password', 'title', 'email', 'status', 'locale',
                   'cps_id', 'rpps', 'phone', 'initial', 'birth', 'address', 'position', 'cv', 'diploma',
                   'formation', 'darrived', 'deval', 'section', 'comment', 'side_account', 'role', 'version']]

        if 'id_user' not in args:
            self.log.error(Logs.fileline() + ' : UserExport ERROR args missing')
            return compose_ret('', Constants.cst_content_type_json, 400)

        dict_data = User.getUserExport()

        if dict_data:
            for d in dict_data:
                data = []

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

                if d['status'] and d['status'] == 29:
                    data.append('A')
                else:
                    data.append('D')

                if d['locale']:
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

                data.append('v2')

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
        if l_rows[0][24] != 'v2':
            self.log.error(Logs.fileline() + ' : TRACE UserImport ERROR wrong version')
            return compose_ret('', Constants.cst_content_type_json, 409)

        # check number of column (dont forget version columns)
        if len(l_rows[0]) != 25:
            self.log.error(Logs.fileline() + ' : TRACE UserImport ERROR wrong number of column')
            return compose_ret('', Constants.cst_content_type_json, 409)

        for l in l_rows:
            if l:
                firstname    = l[0]
                lastname     = l[1]
                username     = l[2]
                password     = l[3]
                title        = l[4]
                email        = l[5]
                status       = l[6]
                locale       = l[7]
                cps_id       = l[8]
                rpps         = l[9]
                phone        = l[10]
                initial      = l[11]
                birth        = l[12]
                address      = l[13]
                position     = l[14]
                cv           = l[15]
                diploma      = l[16]
                formation    = l[17]
                darrived     = l[18]
                deval        = l[19]
                section      = l[20]
                comment      = l[21]
                side_account = l[22]
                role_type    = l[23]

                # status convert
                if status and status == 'A':
                    status = 29
                else:
                    status = 30

                # locale convert
                if locale:
                    if locale == 'FR':
                        locale = 35
                    elif locale == 'UK':
                        locale = 34
                    elif locale == 'US':
                        locale = 75
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
                                                  commentaire=comment)

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
                                          commentaire=comment)

                    if ret <= 0:
                        self.log.error(Logs.alert() + ' : UserImport ERROR insert user')
                        return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE UserImport')
        return compose_ret('', Constants.cst_content_type_json, 200)
