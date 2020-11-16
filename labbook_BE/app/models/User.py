# -*- coding:utf-8 -*-
import logging

# from app.models.Constants import *
from app.models.DB import DB
# from app.models.Logs import Logs


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
              'where u.status != 31 and g.name=%s'  # 31 correspond à l'utilisateur "supprimé"

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
    def getRightsByRole(role):
        # TODO database structure for that

        ret = {}

        return ret
