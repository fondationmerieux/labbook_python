# -*- coding:utf-8 -*-
import logging
import mysql.connector

from app.models.Constants import *
from app.models.DB import DB
from app.models.Logs import Logs


class User:
    log = logging.getLogger('log_db')

    @staticmethod
    def checkUserAccess(login, pwd):
        cursor = DB.cursor()

        req = 'select count(*) as nb_user '\
              'from sigl_user_data '\
              'where status != 31 and username=%s and password=%s'  # 31 = deleted user

        cursor.execute(req, (login, pwd,))

        res = cursor.fetchone()

        if not res or res['nb_user'] != 1:
            return False

        return True

    @staticmethod
    def getUserByLogin(login):
        cursor = DB.cursor()

        req = 'select g.id_group, g.name, g.id_axis, l.id_role, '\
              'u.id_data, u.username, u.firstname, u.lastname, u.password, u.expire_date, '\
              'u.cps_id, u.status, u.email, u.oauth_provider_id_user, u.locale, u.rpps, u.otp_phone_number '\
              'from sigl_pj_group as g '\
              'inner join sigl_user_data AS u ON g.id_group = u.id_group '\
              'inner join sigl_pj_group_link AS l ON g.id_group = l.id_group '\
              'where u.status != 31 and g.name=%s'  # 31 correspond à l'utilisateur "supprimé", 29 désactivé

        cursor.execute(req, (login,))

        return cursor.fetchone()

    @staticmethod
    def getUserByIdGroup(id_group):
        cursor = DB.cursor()

        req = 'select g.id_group, g.name, g.id_axis, '\
              'u.id_data, u.username, u.firstname, u.lastname, u.password, u.expire_date, '\
              'u.cps_id, u.status, u.email, u.oauth_provider_id_user, u.locale, u.rpps, u.otp_phone_number '\
              'from sigl_pj_group as g '\
              'inner join sigl_user_data AS u ON g.id_group = u.id_group '\
              'where u.status != 31 and g.id_group=%s'  # 31 correspond à l'utilisateur "supprimé"

        cursor.execute(req, (id_group,))

        return cursor.fetchone()

    @staticmethod
    def getUserByIdUser(id_user):
        cursor = DB.cursor()

        req = 'select g.id_group, g.name, g.id_axis, l.id_role, '\
              'u.id_data, u.username, u.firstname, u.lastname, u.password, u.expire_date, '\
              'u.cps_id, u.status, u.email, u.oauth_provider_id_user, u.locale, u.rpps, u.otp_phone_number '\
              'from sigl_pj_group as g '\
              'inner join sigl_user_data AS u ON g.id_group = u.id_group '\
              'inner join sigl_pj_group_link AS l ON g.id_group = l.id_group '\
              'where u.id_data=%s'

        cursor.execute(req, (login,))

        return cursor.fetchone()

    @staticmethod
    def getUserGroupParent(id_group):
        cursor = DB.cursor()

        req = 'select id_group_parent '\
              'from sigl_pj_group_link '\
              'where id_group = %s'

        cursor.execute(req, (id_group,))

        return cursor.fetchone()  # TODO AlC : a confirmer que c'est unique

    @staticmethod
    def getUsersByRole(id_role):
        # From sigl_pj_role
        # Admin      = 1
        # Biologist  = 2
        # Technician = 3
        # Secretary  = 4
        cursor = DB.cursor()

        req = 'select g.id_group, g.name, g.id_axis, '\
              'u.id_data, u.username, u.firstname, u.lastname, u.password, u.expire_date, '\
              'u.cps_id, u.status, u.email, u.oauth_provider_id_user, u.locale, u.rpps, u.otp_phone_number '\
              'from sigl_pj_group as g '\
              'inner join sigl_user_data AS u ON g.id_group = u.id_group '\
              'inner join sigl_pj_group_link AS l ON g.id_group = l.id_group '\
              'where u.status != "31" and l.id_role=%s'  # 31 correspond à l'utilisateur "supprimé"

        cursor.execute(req, (id_role,))

        return cursor.fetchall()

    @staticmethod
    def getUserList(args, id_lab):
        cursor = DB.cursor()

        filter_cond = ''

        if not args:
            limit = 'LIMIT 500'

            filter_cond += ' and status!=31 '  # remove deleted users by default
        else:
            limit = 'LIMIT 500'
            # filter conditions
            if args['login']:
                filter_cond += ' and username LIKE "%' + args['login'] + '%" '

            if args['group'] and args['group'] > 0:
                filter_cond += ' and group=' + args['group'] + ' '

            if args['firstname']:
                filter_cond += ' and firstname LIKE "%' + args['firstname'] + '%" '

            if args['lastname']:
                filter_cond += ' and lastname LIKE "%' + args['lastname'] + '%" '

            if args['status'] and args['status'] > 0:
                filter_cond += ' and status=' + args['status'] + ' '
            else:
                filter_cond += ' and status!=31 '  # remove deleted users by default

            if args['role'] and args['role'] > 0:
                filter_cond += ' and role=' + args['role'] + ' '

        # struct : stat, urgent, num_dos, id_data, date_dos, code, nom, prenom, id_pat
        req = 'select u.id_data, u.id_owner, u.username, u.firstname, u.lastname, u.status as stat, '\
              'date_format(u.creation_date, %s) as date_create, r.label as role, u.oauth_provider_id_user as id_origin '\
              'from sigl_pj_group_link as gl '\
              'inner join sigl_user_data as u on u.id_group=gl.id_group '\
              'inner join sigl_pj_role as r on gl.id_role=r.id_role '\
              'where gl.id_group_parent=%s ' + filter_cond +\
              'group by u.id_data order by u.creation_date asc ' + limit

        cursor.execute(req, (Constants.cst_isodate, id_lab,))

        return cursor.fetchall()

    @staticmethod
    def getRightsByRole(role):
        # TODO database structure for that

        ret = {}

        return ret

    @staticmethod
    def updatePassword(id_user, password):
        try:
            cursor = DB.cursor()

            cursor.execute('update sigl_user_data '
                           'set password=%s '
                           'where id_data=%s', (password, id_user))

            User.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            User.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def updateStatus(id_user, status):
        try:
            cursor = DB.cursor()

            cursor.execute('update sigl_user_data '
                           'set status=%s '
                           'where id_data=%s', (status, id_user))

            User.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            User.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False
