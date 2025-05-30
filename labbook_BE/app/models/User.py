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
               'user.email, user.oauth_provider_id_user, user.locale, user.rpps, user.tel as phone, '
               'user.role_pro, pro.pro_label, pro.pro_color_1, pro.pro_color_2, pro.pro_text_color '
               'from sigl_user_data as user '
               'inner join profile_role as pro on pro.pro_ser = user.role_pro '
               'inner join sigl_pj_role as role on role.id_role = pro.pro_role '
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
               'u.side_account, u.role_type, u.role_pro, d_title.label as title_label, '
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
                           'formation, section, deval, side_account, commentaire, oauth_provider_id_user, role_pro) '
                           'values (NOW(), %(id_owner)s, %(role_type)s, %(username)s, %(password)s, %(cps_id)s, %(rpps)s, '
                           '%(status)s, %(firstname)s, %(lastname)s, %(locale)s, %(email)s, %(titre)s, %(initiale)s, '
                           '%(ddn)s, %(adresse)s, %(tel)s, %(darrive)s, %(position)s, %(cv)s, %(diplome)s, %(formation)s, '
                           '%(section)s, %(deval)s, %(side_account)s, %(commentaire)s, %(origin)s, %(role_pro)s)', params)

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
                           'side_account=%(side_account)s, commentaire=%(commentaire)s, role_pro=%(role_pro)s '
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
                           'titre=%(titre)s, initiale=%(initiale)s, ddn=%(ddn)s, adresse=%(adresse)s, tel=%(tel)s, '
                           'darrive=%(darrive)s, position=%(position)s, cv=%(cv)s, diplome=%(diplome)s, '
                           'formation=%(formation)s, section=%(section)s, deval=%(deval)s, commentaire=%(commentaire)s, '
                           'role_type=%(role_type)s, role_pro=%(role_pro)s '
                           'where username=%(username)s and firstname=%(firstname)s and lastname=%(lastname)s', params)

            User.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            User.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getUserListOfRights(id_user):

        cursor = DB.cursor()

        req = ('select prr_ser, coalesce(usp_granted, prp_granted) as prp_granted, prr_tag '
               'from profile_permissions '
               'inner join profile_rights on prr_ser = prp_prr '
               'left join user_permissions on usp_prp = prp_ser and usp_user = %s '
               'where prp_pro = (select role_pro from sigl_user_data where id_data=%s) '
               'order by prr_ser asc')

        cursor.execute(req, (id_user, id_user))

        return cursor.fetchall()

    @staticmethod
    def getUserRightsList(id_user=0, role_type='', role_id=0):

        cursor = DB.cursor()

        req = ''

        if id_user > 0:
            # specific profile_permissions for a user replace by user_permissions if exist
            req = ('select case when usp_prp is not null then "usp" else "prp" end as src, '
                   'coalesce(usp_prp, prp_ser) as prp_ser, prr_label, prr_type, '
                   'coalesce(usp_granted, prp_granted) as prp_granted '
                   'from profile_permissions '
                   'inner join profile_rights on prr_ser = prp_prr '
                   'left join user_permissions on usp_prp = prp_ser and usp_user = %s '
                   'where prp_pro = (select role_pro from sigl_user_data where id_data=%s) '
                   'order by prr_rank asc')

            cursor.execute(req, (id_user, id_user))
        else:
            if role_id > 0:
                # specific profile_role
                req = ('select prp_ser, prr_label, prr_type, prp_granted, "prp" as src '
                       'from profile_permissions '
                       'inner join profile_rights on prr_ser = prp_prr '
                       'inner join profile_role on pro_ser = prp_pro '
                       'where prp_pro=%s '
                       'order by prr_rank asc')

                cursor.execute(req, (role_id,))
            else:
                # first role with this role_type
                req = ('select prp_ser, prr_label, prr_type, prp_granted, "prp" as src '
                       'from profile_permissions '
                       'inner join profile_rights on prr_ser = prp_prr '
                       'inner join profile_role on pro_ser = prp_pro '
                       'inner join sigl_pj_role on id_role = pro_role '
                       'where pro_genuine="Y" and type=%s '
                       'order by prr_rank asc')

                cursor.execute(req, (role_type,))

        return cursor.fetchall()

    @staticmethod
    def getUserRoleList(type='', l_exclude=[], genuine='N'):
        cursor = DB.cursor()

        cond = ' order by label '

        if type:
            cond = ' where type="' + str(type) + '"' + cond

        if l_exclude:
            if not type:
                cond = ' where type not in ('
            else:
                cond = cond + ' and type not in ('

            for exclude in l_exclude:
                cond += '"' + str(exclude) + '",'

            # inversed string then replace last , by ) then re-inversed string
            cond = cond[::-1].replace(',', ')', 1)[::-1]

        if genuine == 'Y':
            cond = cond + ' and pro_genuine="Y" '

        req = ('select pro_ser, pro_role as id_role, name, pro_label as label, type, pro_genuine, pro_color_1, '
               'pro_color_2, pro_text_color '
               'from profile_role '
               'inner join sigl_pj_role on id_role=pro_role ' + cond)

        cursor.execute(req)

        return cursor.fetchall()

    @staticmethod
    def getUserRole(role_type):
        cursor = DB.cursor()

        req = ('select id_role, name, label, type '
               'from sigl_pj_role '
               'where type=%s')

        cursor.execute(req, (role_type,))

        return cursor.fetchone()

    @staticmethod
    def getRoleDetails(pro_ser):
        cursor = DB.cursor()

        req = ('select pro_ser, pro_by_user, pro_role, pro_label, type as role_type, pro_genuine, pro_color_1, '
               'pro_color_2, pro_text_color '
               'from profile_role '
               'inner join sigl_pj_role on id_role = pro_role '
               'where pro_ser=%s')

        cursor.execute(req, (pro_ser,))

        return cursor.fetchone()

    @staticmethod
    def deleteRoleDet(pro_ser, id_user):
        try:
            cursor = DB.cursor()

            req = ('delete from profile_permissions where prp_pro=%s')

            cursor.execute(req, (pro_ser,))

            req = ('delete from profile_role where pro_ser=%s')

            cursor.execute(req, (pro_ser,))

            req = ('delete from user_permissions where usp_user=%s')

            cursor.execute(req, (id_user,))

            return True
        except mysql.connector.Error as e:
            User.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def insertProfileRole(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into profile_role '
                           '(pro_date, pro_by_user, pro_role, pro_label, pro_color_1, pro_color_2, pro_text_color) '
                           'values (NOW(), %(by_user)s, %(role)s, %(label)s, %(color_1)s, %(color_2)s, %(text_color)s)', params)

            User.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            User.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def getRoleDetByUser(id_user):
        cursor = DB.cursor()

        req = ('select pro_ser, pro_by_user, pro_role, pro_label, type as role_type, pro_genuine, pro_color_1, '
               'pro_color_2, pro_text_color '
               'from profile_role '
               'inner join sigl_pj_role on id_role = pro_role '
               'inner join sigl_user_data as user on user.role_pro = pro_ser '
               'where user.id_data=%s')

        cursor.execute(req, (id_user,))

        return cursor.fetchone()

    @staticmethod
    def updateProfileRole(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('update profile_role '
                           'set pro_by_user=%(by_user)s, pro_label=%(label)s, pro_color_1=%(color_1)s, '
                           'pro_color_2=%(color_2)s, pro_text_color=%(text_color)s '
                           'where pro_ser=%(pro)s', params)

            User.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            User.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def insertProfilePermission(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into profile_permissions '
                           '(prp_date, prp_by_user, prp_pro, prp_prr, prp_granted) '
                           'select NOW(), %(by_user)s, %(pro)s, derived_table.prp_prr, %(granted)s '
                           'from (select prp_prr from profile_permissions where prp_ser = %(prp)s) '
                           'as derived_table', params)

            User.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            User.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def updateProfilePermission(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('update profile_permissions '
                           'set prp_by_user=%(by_user)s, prp_granted=%(granted)s '
                           'where prp_pro=%(pro)s and prp_ser=%(prp)s', params)

            User.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            User.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def sameGranted(prp, granted):
        cursor = DB.cursor()

        req = ('select 1 '
               'from profile_permissions '
               'where prp_ser=%s and prp_granted=%s')

        cursor.execute(req, (prp, granted))

        res = cursor.fetchone()

        if not res:
            return False

        return True

    @staticmethod
    def insertUserPermission(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into user_permissions '
                           '(usp_date, usp_by_user, usp_user, usp_prp, usp_granted) '
                           'values (NOW(), %(by_user)s, %(user)s, %(prp)s, %(granted)s)', params)

            User.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            User.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def updateUserPermission(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('update user_permissions '
                           'set usp_by_user=%(by_user)s, usp_granted=%(granted)s '
                           'where usp_user=%(user)s and usp_prp=%(prp)s', params)

            User.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            User.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def deleteUserPermission(user, prp):
        try:
            cursor = DB.cursor()

            req = ('delete from user_permissions where usp_user=%s and usp_prp=%s')

            cursor.execute(req, (user, prp))

            return True
        except mysql.connector.Error as e:
            User.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

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
               'u.section, u.commentaire, u.side_account, u.role_type, u.role_pro '
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

            if 'role_pro' in args and args['role_pro']:
                filter_cond += ' and u.role_pro=' + str(args['role_pro']) + ' '

        req = ('select u.id_data, u.id_owner, u.username, u.firstname, u.lastname, u.status as stat, '
               'u.initiale as initial, u.ddn as birth, u.adresse as address, u.tel as phone, u.email, '
               'u.darrive as arrived, u.position as position, dict.label as section, u.deval as last_eval, '
               'date_format(u.creation_date, "' + Constants.cst_isodate + '") as date_create, r.label as role, '
               'u.oauth_provider_id_user as id_origin, COALESCE(u2.username, "") as origin, u.role_type, u.role_pro, '
               'pro.pro_label as pro_label '
               'from sigl_user_data as u '
               'inner join profile_role as pro on pro.pro_ser=u.role_pro '
               'inner join sigl_pj_role as r on r.id_role=pro.pro_role '
               'left join sigl_user_data as u2 on u2.id_data=u.oauth_provider_id_user '
               'left join sigl_dico_data as dict on dict.id_data=u.section '
               'where ' + filter_cond +
               'group by u.id_data order by u.creation_date asc ' + limit)

        cursor.execute(req)

        return cursor.fetchall()

    @staticmethod
    def getUserLiteList():
        cursor = DB.cursor()

        req = ('select u.id_data, u.username, u.firstname, u.lastname, u.role_type, pro.pro_label as pro_label '
               'from sigl_user_data as u '
               'inner join profile_role as pro on pro.pro_ser=u.role_pro '
               'inner join sigl_pj_role as r on r.id_role=pro.pro_role '
               'where u.status="' + Constants.cst_user_active + '" and u.role_type in ("A","AGT") '
               'order by u.role_type asc, u.lastname asc, u.firstname asc, u.username asc ')

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

    @staticmethod
    def countProfileByRole(pro_ser):
        cursor = DB.cursor()

        # Number of profiles
        req = ('select count(*) as nb_profile '
               'from sigl_user_data '
               'where status="' + Constants.cst_user_active + '" and role_pro=%s')

        cursor.execute(req, (pro_ser,))

        return cursor.fetchone()

    @staticmethod
    def role_exist(role_label):
        try:
            cursor = DB.cursor()

            cursor.execute('select count(*) as nb_role '
                           'from profile_role '
                           'where pro_label=%s', (role_label,))

            ret = cursor.fetchone()

            if ret and ret['nb_role'] == 0:
                return False
            else:
                return True
        except mysql.connector.Error as e:
            User.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return -1
