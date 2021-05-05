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
                    d['date'] = datetime.strftime(d['date'], '%Y-%m-%d')
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

        l_data = [['firstname', 'lastname', 'username', 'password', 'titre', 'email', 'status', 'cps_id', 'locale',
                   'rpps', 'otp_phone_number', 'initiale', 'ddn', 'position', 'adresse', 'tel', 'darrive', 'cv',
                   'diplome', 'formation', 'deval', 'section', 'commentaire', 'side_account', 'id_role', 'version']]

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

                if d['status']:
                    data.append(d['status'])
                else:
                    data.append('')

                if d['cps_id']:
                    data.append(d['cps_id'])
                else:
                    data.append('')

                if d['locale']:
                    data.append(d['locale'])
                else:
                    data.append('')

                if d['rpps']:
                    data.append(d['rpps'])
                else:
                    data.append('')

                if d['otp_phone_number']:
                    data.append(d['otp_phone_number'])
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

                if d['position']:
                    data.append(d['position'])
                else:
                    data.append('')

                if d['adresse']:
                    data.append(d['adresse'])
                else:
                    data.append('')

                if d['tel']:
                    data.append(d['tel'])
                else:
                    data.append('')

                if d['darrive']:
                    data.append(d['darrive'])
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

                if d['id_role']:
                    data.append(d['id_role'])
                else:
                    data.append('')

                data.append('v1')

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
        if l_rows[0][25] != 'v1':
            self.log.error(Logs.fileline() + ' : TRACE UserImport ERROR wrong version')
            return compose_ret('', Constants.cst_content_type_json, 409)

        # check number of column (dont forget version columns)
        if len(l_rows[0]) != 26:
            self.log.error(Logs.fileline() + ' : TRACE UserImport ERROR wrong number of column')
            return compose_ret('', Constants.cst_content_type_json, 409)

        for l in l_rows:
            if l:
                firstname    = l[0]
                lastname     = l[1]
                username     = l[2]
                password     = l[3]
                titre        = l[4]
                email        = l[5]
                status       = l[6]
                cps_id       = l[7]
                locale       = l[8]
                rpps         = l[9]
                phone        = l[10]
                initiale     = l[11]
                ddn          = l[12]
                position     = l[13]
                adresse      = l[14]
                tel          = l[15]
                darrive      = l[16]
                cv           = l[17]
                diplome      = l[18]
                formation    = l[19]
                deval        = l[20]
                section      = l[21]
                commentaire  = l[22]
                side_account = l[23]
                id_role      = l[24]

                # Check if user exist (same username, lastname and firstname)
                # if EXIST => UPDATE (all except password)
                if User.exist(firstname, lastname, username):
                    ret = User.UpdateUserByImport(firstname=firstname,
                                                  lastname=lastname,
                                                  username=username,
                                                  titre=titre,
                                                  email=email,
                                                  status=status,
                                                  cps_id=cps_id,
                                                  locale=locale,
                                                  rpps=rpps,
                                                  phone=phone,
                                                  initiale=initiale,
                                                  ddn=ddn,
                                                  position=position,
                                                  adresse=adresse,
                                                  tel=tel,
                                                  darrive=darrive,
                                                  cv=cv,
                                                  diplome=diplome,
                                                  formation=formation,
                                                  deval=deval,
                                                  section=section,
                                                  commentaire=commentaire)

                    if not ret:
                        self.log.error(Logs.alert() + ' : UserImport ERROR update user username=' + str(username))
                        return compose_ret('', Constants.cst_content_type_json, 500)

                # if not EXIST => INSERT
                else:
                    # insert into sigl_pj_group
                    ret = User.insertUserName(name=username)

                    if ret <= 0:
                        self.log.error(Logs.alert() + ' : UserImport ERROR insert user Name')
                        return compose_ret('', Constants.cst_content_type_json, 500)

                    res = {}
                    res['id_group'] = ret

                    # insert into sigl_pj_group_link
                    ret = User.insertUserRole(id_group=res['id_group'],
                                              id_group_parent=1000,  # I cant explain 1000
                                              id_role=id_role)

                    if ret <= 0:
                        self.log.error(Logs.alert() + ' : UserImport ERROR insert user Role')
                        return compose_ret('', Constants.cst_content_type_json, 500)

                    res['id_group_link'] = ret

                    # insert in sigl_user_data
                    ret = User.insertUser(id_owner=id_user,
                                          id_group=res['id_group'],
                                          username=username,
                                          password=password,
                                          cps_id=cps_id,
                                          rpps=rpps,
                                          status=status,
                                          firstname=firstname,
                                          lastname=lastname,
                                          locale=locale,
                                          email=email,
                                          titre=titre,
                                          initiale=initiale,
                                          ddn=ddn,
                                          adresse=adresse,
                                          tel=phone,
                                          darrive=darrive,
                                          position=position,
                                          cv=cv,
                                          diplome=diplome,
                                          formation=formation,
                                          section=section,
                                          deval=deval,
                                          side_account=side_account,
                                          commentaire=commentaire)

                    if ret <= 0:
                        self.log.error(Logs.alert() + ' : UserDet ERROR insert user')
                        return compose_ret('', Constants.cst_content_type_json, 500)

        self.log.info(Logs.fileline() + ' : TRACE UserImport')
        return compose_ret('', Constants.cst_content_type_json, 200)
