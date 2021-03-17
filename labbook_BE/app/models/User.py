# -*- coding:utf-8 -*-
import logging
import mysql.connector

from app.models.Constants import *
from app.models.DB import DB
from app.models.Logs import Logs
from app.models.Various import Various


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

        # save in sigl_evtlog_data this connection
        req = 'select id_data '\
              'from sigl_user_data '\
              'where status != 31 and username=%s and password=%s'  # 31 = deleted user

        cursor.execute(req, (login, pwd,))

        res = cursor.fetchone()

        Various.insertEvent(id_user=res['id_data'],
                            type='17',
                            name='EVT_LOGIN',
                            message='')

        return True

    @staticmethod
    def getUserByLogin(login):
        cursor = DB.cursor()

        req = 'select g.id_group, g.name, g.id_axis, l.id_role, u.side_account, '\
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

        req = 'select g.id_group, g.name, g.id_axis, u.side_account, '\
              'u.id_data, u.username, u.firstname, u.lastname, u.password, u.expire_date, '\
              'u.cps_id, u.status, u.email, u.oauth_provider_id_user, u.locale, u.rpps, u.otp_phone_number '\
              'from sigl_pj_group as g '\
              'inner join sigl_user_data AS u ON g.id_group = u.id_group '\
              'where u.status != 31 and g.id_group=%s'  # 31 correspond à l'utilisateur "supprimé"

        cursor.execute(req, (id_group,))

        return cursor.fetchone()

    @staticmethod
    def getUserDetails(id_user):
        cursor = DB.cursor()

        req = 'select u.username, u.cps_id as cps, u.rpps, u.status as stat, u.firstname, u.lastname, '\
              'u.locale as lang, u.email, u.titre as title, u.initiale as initial, u.adresse as address, '\
              'u.ddn as birth, u.tel as phone, u.darrive as arrived, u.position, u.cv, u.diplome as diploma, '\
              'u.formation as training, u.section, u.deval as last_eval, u.commentaire as comment, '\
              'l.id_role as id_role, u.side_account, '\
              'TRIM(CONCAT((COALESCE(pres.nom, ""))," ",TRIM(COALESCE(pres.prenom, "")))) as prescriber '\
              'from sigl_user_data as u '\
              'inner join sigl_pj_group as g on g.name = u.username '\
              'inner join sigl_pj_group_link as l on l.id_group = g.id_group '\
              'left join sigl_08_data as pres on pres.id_data=u.side_account '\
              'where u.id_data=%s'

        cursor.execute(req, (id_user,))

        return cursor.fetchone()

    @staticmethod
    def insertUser(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into sigl_user_data '
                           '(creation_date, id_owner, id_group, username, password, cps_id, rpps, status, firstname, '
                           'lastname, locale, email, titre, initiale, ddn, adresse, tel, darrive, position, cv, diplome, '
                           'formation, section, deval, side_account, commentaire) '
                           'values (NOW(), %(id_owner)s, %(id_group)s, %(username)s, %(password)s, %(cps_id)s, %(rpps)s, '
                           '%(status)s, %(firstname)s, %(lastname)s, %(locale)s, %(email)s, %(titre)s, %(initiale)s, '
                           '%(ddn)s, %(adresse)s, %(tel)s, %(darrive)s, %(position)s, %(cv)s, %(diplome)s, %(formation)s, '
                           '%(section)s, %(deval)s, %(side_account)s, %(commentaire)s)', params)

            User.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            User.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def updateUser(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('update sigl_user_data '
                           'set username=%(username)s, cps_id=%(cps_id)s, rpps=%(rpps)s, status=%(status)s, '
                           'firstname=%(firstname)s, lastname=%(lastname)s, locale=%(locale)s, email=%(email)s, '
                           'titre=%(titre)s, initiale=%(initiale)s, ddn=%(ddn)s, adresse=%(adresse)s, tel=%(tel)s, '
                           'darrive=%(darrive)s, position=%(position)s, cv=%(cv)s, diplome=%(diplome)s, '
                           'formation=%(formation)s, section=%(section)s, deval=%(deval)s, '
                           'side_account=%(side_account)s, commentaire=%(commentaire)s '
                           'where id_data=%(id_data)s', params)

            User.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            User.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def insertUserName(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into sigl_pj_group '
                           '(name) '
                           'values (%(name)s)', params)

            User.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            User.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def updateUserName(old_name, new_name):
        try:
            cursor = DB.cursor()

            cursor.execute('update sigl_pj_group '
                           'set name=%s '
                           'where name=%s', (new_name, old_name))

            User.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            User.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def insertUserRole(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into sigl_pj_group_link '
                           '(id_group, id_group_parent, id_role) '
                           'values (%(id_group)s, %(id_group_parent)s, %(id_role)s)', params)

            User.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            User.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def updateUserRole(id_group, id_role):
        try:
            cursor = DB.cursor()

            cursor.execute('update sigl_pj_group_link '
                           'set id_role=%s '
                           'where id_group=%s', (id_role, id_group))

            User.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            User.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getUserGroupParent(id_group):
        cursor = DB.cursor()

        req = 'select id_group_parent '\
              'from sigl_pj_group_link '\
              'where id_group = %s'

        cursor.execute(req, (id_group,))

        return cursor.fetchone()  # TODO AlC : a confirmer que c'est unique

    @staticmethod
    def getUserIdGroup(username):
        cursor = DB.cursor()

        req = 'select id_group '\
              'from sigl_pj_group '\
              'where name = %s'

        cursor.execute(req, (username,))

        return cursor.fetchone()

    @staticmethod
    def getUsersByRole(id_role):
        # From sigl_pj_role
        # Admin      = 1
        # Biologist  = 2
        # Technician = 3
        # Secretary  = 4
        # Advanced technician = 5
        # quality technician  = 6
        # Advanced secretary  = 7
        # Qualitician         = 8
        # Prescriber          = 9

        cursor = DB.cursor()

        req = 'select g.id_group, g.name, g.id_axis, u.side_account, '\
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

            filter_cond += ' and u.status=29 '  # remove deleted users by default
        else:
            limit = 'LIMIT 500'
            # filter conditions
            if args['login']:
                filter_cond += ' and u.username LIKE "%' + args['login'] + '%" '

            if 'group' in args and args['group'] > 0:
                filter_cond += ' and group=' + str(args['group']) + ' '

            if args['firstname']:
                filter_cond += ' and u.firstname LIKE "%' + args['firstname'] + '%" '

            if args['lastname']:
                filter_cond += ' and u.lastname LIKE "%' + args['lastname'] + '%" '

            if 'status' in args and args['status'] > 0:
                stat = 'u.status=' + str(args['status'])

                # Keep compatibility with old delete user where status = 31
                if args['status'] == 30:
                    stat = "(u.status=30 or u.status=31)"

                filter_cond += ' and ' + stat + ' '
            else:
                filter_cond += ' and u.status=29 '  # keep only activated users by default

            if 'role' in args and args['role'] > 0:
                filter_cond += ' and r.id_role=' + str(args['role']) + ' '

        # struct : stat, urgent, num_dos, id_data, date_dos, code, nom, prenom, id_pat
        req = ('select u.id_data, u.id_owner, u.username, u.firstname, u.lastname, u.status as stat, '
               'u.initiale as initial, u.ddn as birth, u.adresse as address, u.tel as phone, u.email, '
               'u.darrive as arrived, u.position as position, dict.label as section, u.deval as last_eval, '
               'date_format(u.creation_date, %s) as date_create, r.label as role, u.oauth_provider_id_user as id_origin, '
               'COALESCE(u2.username, "") as origin '
               'from sigl_pj_group_link as gl '
               'inner join sigl_user_data as u on u.id_group=gl.id_group '
               'inner join sigl_pj_role as r on gl.id_role=r.id_role '
               'left join sigl_user_data as u2 on u2.id_data=u.oauth_provider_id_user '
               'left join sigl_dico_data as dict on dict.id_data=u.section '
               'where gl.id_group_parent=%s ' + filter_cond +
               'group by u.id_data order by u.creation_date asc ' + limit)

        cursor.execute(req, (Constants.cst_isodate, id_lab,))

        return cursor.fetchall()

    @staticmethod
    def getUserSearch(text):
        cursor = DB.cursor()

        l_words = text.split(' ')

        cond = 'status=29 '

        for word in l_words:
            cond = (cond +
                    ' and (lastname like "' + word + '%" or '
                    'firstname like "' + word + '%" or '
                    'username like "' + word + '%") ')

        limit = ' limit 1000'

        # struct : stat, urgent, num_dos, id_data, date_dos, code, nom, prenom, id_pat
        req = ('select id_data, TRIM(CONCAT(lastname," ",firstname," - ",username)) AS field_value '
               'from sigl_user_data '
               'where ' + cond + limit)

        cursor.execute(req)

        return cursor.fetchall()

    @staticmethod
    def getRightsByRole(role):
        # TODO database structure for that

        ret = {}

        return ret

    @staticmethod
    def getUserConnections(date_beg, date_end):
        cursor = DB.cursor()

        limit = ' limit 50000'

        req = ('select e.id_owner as id_user, COALESCE(u.username, "") as username, e.evt_datetime as date, '
               'e.evt_name as event, e.message '
               'from sigl_evtlog_data as e '
               'left join sigl_user_data as u on u.id_data=e.id_owner '
               'where (e.evt_datetime between %s and %s) and e.evt_type=17 '
               'order by e.evt_datetime ' + limit)

        cursor.execute(req, (date_beg, date_end,))

        return cursor.fetchall()

    @staticmethod
    def getPasswordDB(pwd, salt=''):
        # password hash (TODO by Bcrypt)
        import hashlib
        import os

        if not salt:
            salt = hashlib.sha1(os.urandom(32)).hexdigest()

        len_pwd   = len(pwd)
        len_start = len_pwd - 1
        len_end   = 40 - len_pwd + len_start

        pwd = pwd + salt[len_start:len_end]

        pwd_md5  = hashlib.md5(pwd.encode()).hexdigest()

        pwd_sha1 = hashlib.sha1(pwd_md5.encode())
        pwd_sha1 = pwd_sha1.hexdigest()

        pwd_db   = pwd_sha1 + ':' + salt

        return pwd_db

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

    @staticmethod
    def getUserNbUsers():
        cursor = DB.cursor()

        # Number of records
        req = 'select count(*) as nb_users '\
              'from sigl_user_data '\
              'where status=29'

        cursor.execute(req)

        return cursor.fetchone()
