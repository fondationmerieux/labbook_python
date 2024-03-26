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

        req = ('select count(*) as nb_user '
               'from sigl_user_data '
               'where status = "' + Constants.cst_user_active + '" and username=%s and password=%s')

        cursor.execute(req, (login, pwd,))

        res = cursor.fetchone()

        if not res or res['nb_user'] != 1:
            return False

        # save in sigl_evtlog_data this connection
        req = ('select id_data '
               'from sigl_user_data '
               'where status = "' + Constants.cst_user_active + '" and username=%s and password=%s')

        cursor.execute(req, (login, pwd,))

        res = cursor.fetchone()

        Various.insertEvent(id_user=res['id_data'],
                            type='17',
                            name='EVT_LOGIN',
                            message='')
        return True

    @staticmethod
    def exist(firstname, lastname, username):
        cursor = DB.cursor()

        req = ('select count(*) as nb_user '
               'from sigl_user_data '
               'where firstname=%s and lastname=%s and username=%s')

        cursor.execute(req, (firstname, lastname, username,))

        res = cursor.fetchone()

        if not res or res['nb_user'] != 1:
            return False

        return True

    @staticmethod
    def getUserByLogin(login):
        cursor = DB.cursor()

        req = ('select user.id_data, user.username, user.side_account, user.password, user.role_type, '
               'user.firstname, user.lastname, user.expire_date, user.cps_id, user.status, '
               'user.email, user.oauth_provider_id_user, user.locale, user.rpps, user.tel as phone '
               'from sigl_user_data as user '
               'inner join sigl_pj_role as role on role.type = user.role_type '
               'where user.status="' + Constants.cst_user_active + '" and user.username=%s')

        cursor.execute(req, (login,))

        return cursor.fetchone()

    @staticmethod
    def getUserDetails(id_user):
        cursor = DB.cursor()

        req = ('select u.username, u.cps_id as cps, u.rpps, u.status as stat, u.firstname, u.lastname, '
               'u.locale as lang, u.email, u.titre as title, u.initiale as initial, u.adresse as address, '
               'u.ddn as birth, u.tel as phone, u.darrive as arrived, u.position, u.cv, u.diplome as diploma, '
               'u.formation as training, u.section, u.deval as last_eval, u.commentaire as comment, '
               'u.side_account, u.role_type, d_title.label as title, '
               'TRIM(CONCAT((COALESCE(pres.nom, ""))," ",TRIM(COALESCE(pres.prenom, "")))) as prescriber '
               'from sigl_user_data as u '
               'left join sigl_08_data as pres on pres.id_data=u.side_account '
               'left join sigl_dico_data as d_title on d_title.id_data=u.titre '
               'where u.id_data=%s')

        cursor.execute(req, (id_user,))

        return cursor.fetchone()

    @staticmethod
    def insertUser(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into sigl_user_data '
                           '(creation_date, id_owner, role_type, username, password, cps_id, rpps, status, firstname, '
                           'lastname, locale, email, titre, initiale, ddn, adresse, tel, darrive, position, cv, diplome, '
                           'formation, section, deval, side_account, commentaire, oauth_provider_id_user) '
                           'values (NOW(), %(id_owner)s, %(role_type)s, %(username)s, %(password)s, %(cps_id)s, %(rpps)s, '
                           '%(status)s, %(firstname)s, %(lastname)s, %(locale)s, %(email)s, %(titre)s, %(initiale)s, '
                           '%(ddn)s, %(adresse)s, %(tel)s, %(darrive)s, %(position)s, %(cv)s, %(diplome)s, %(formation)s, '
                           '%(section)s, %(deval)s, %(side_account)s, %(commentaire)s, %(origin)s)', params)

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
                           'set username=%(username)s, role_type=%(role_type)s, cps_id=%(cps_id)s, rpps=%(rpps)s, status=%(status)s, '
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
    def updateUserByImport(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('update sigl_user_data '
                           'set cps_id=%(cps_id)s, rpps=%(rpps)s, status=%(status)s, locale=%(locale)s, email=%(email)s, '
                           'titre=%(titre)s, initiale=%(initiale)s, ddn=%(ddn)s, adresse=%(adresse)s, tel=%(phone)s, '
                           'darrive=%(darrive)s, position=%(position)s, cv=%(cv)s, diplome=%(diplome)s, '
                           'formation=%(formation)s, section=%(section)s, deval=%(deval)s, commentaire=%(commentaire)s '
                           'where username=%(username)s and firstname=%(firstname)s and lastname=%(lastname)s', params)

            User.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            User.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getUserRoleList(type=''):
        cursor = DB.cursor()

        cond = ' order by label '

        if type:
            cond = ' where type="' + str(type) + '"' + cond

        req = ('select id_role, name, label, type from sigl_pj_role' + cond)

        cursor.execute(req)

        return cursor.fetchall()

    @staticmethod
    def getUserIdentList():
        cursor = DB.cursor()

        req = ('select id_data as id_user, TRIM(CONCAT(lastname," ",firstname," - ",username)) as user_ident '
               'from sigl_user_data '
               'where status="A" order by lastname asc, firstname asc')

        cursor.execute(req)

        return cursor.fetchall()

    @staticmethod
    def getUserExport():
        cursor = DB.cursor()

        req = ('select u.firstname, u.lastname, u.username, u.password, u.titre, u.email, u.status, u.locale, '
               'u.cps_id, u.rpps, u.tel, u.initiale, date_format(u.ddn, %s) as ddn, u.adresse, u.position, '
               'u.cv, u.diplome, u.formation, date_format(u.darrive, %s) as darrive, date_format(u.deval, %s) as deval, '
               'u.section, u.commentaire, u.side_account, u.role_type '
               'from sigl_user_data as u '
               'where u.username != "root" '
               'group by u.id_data order by u.role_type asc')

        cursor.execute(req, (Constants.cst_isodate, Constants.cst_isodate, Constants.cst_isodate))

        return cursor.fetchall()

    @staticmethod
    def getUserList(args):
        cursor = DB.cursor()

        filter_cond = 'u.role_type != "X" '

        if not args:
            limit = 'LIMIT 500'

            filter_cond += ' and u.status="' + Constants.cst_user_active + '" '  # keep active users by default
        else:
            limit = 'LIMIT 500'
            # filter conditions
            if args['login']:
                filter_cond += ' and u.username LIKE "%' + args['login'] + '%" '

            if args['firstname']:
                filter_cond += ' and u.firstname LIKE "%' + args['firstname'] + '%" '

            if args['lastname']:
                filter_cond += ' and u.lastname LIKE "%' + args['lastname'] + '%" '

            if 'status' in args and args['status']:
                stat = 'u.status="' + str(args['status']) + '" '

                # Keep compatibility with old delete user
                if args['status'] == Constants.cst_user_inactive:
                    stat = '(u.status="' + Constants.cst_user_inactive + '" or u.status="' + Constants.cst_user_deleted + '")'

                filter_cond += ' and ' + stat + ' '
            else:
                filter_cond += ' and u.status="' + Constants.cst_user_active + '" '  # keep active users by default

            if 'role' in args and args['role']:
                filter_cond += ' and u.role_type="' + str(args['role']) + '" '

        req = ('select u.id_data, u.id_owner, u.username, u.firstname, u.lastname, u.status as stat, '
               'u.initiale as initial, u.ddn as birth, u.adresse as address, u.tel as phone, u.email, '
               'u.darrive as arrived, u.position as position, dict.label as section, u.deval as last_eval, '
               'date_format(u.creation_date, "' + Constants.cst_isodate + '") as date_create, r.label as role, '
               'u.oauth_provider_id_user as id_origin, COALESCE(u2.username, "") as origin, u.role_type '
               'from sigl_user_data as u '
               'inner join sigl_pj_role as r on r.type=u.role_type '
               'left join sigl_user_data as u2 on u2.id_data=u.oauth_provider_id_user '
               'left join sigl_dico_data as dict on dict.id_data=u.section '
               'where ' + filter_cond +
               'group by u.id_data order by u.creation_date asc ' + limit)

        cursor.execute(req)

        return cursor.fetchall()

    @staticmethod
    def getUserSearch(text):
        cursor = DB.cursor()

        l_words = text.split(' ')

        cond = 'status="' + Constants.cst_user_active + '" '

        for word in l_words:
            cond = (cond +
                    ' and (lastname like "' + word + '%" or '
                    'firstname like "' + word + '%" or '
                    'username like "' + word + '%") ')

        limit = ' limit 1000'

        req = ('select id_data, TRIM(CONCAT(lastname," ",firstname," - ",username)) AS field_value '
               'from sigl_user_data '
               'where ' + cond + limit)

        cursor.execute(req)

        return cursor.fetchall()

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
        req = ('select count(*) as nb_users '
               'from sigl_user_data '
               'where status="' + Constants.cst_user_active + '"')

        cursor.execute(req)

        return cursor.fetchone()
