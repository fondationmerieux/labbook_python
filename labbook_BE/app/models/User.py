# -*- coding:utf-8 -*-
import hashlib
import logging
import os

import mysql.connector

from app.models.Constants import Constants
from app.models.DB import DB
from app.models.Logs import Logs
from app.models.Various import Various


class User:
    log = logging.getLogger('log_db')

    @staticmethod
    def checkUserAccess(login, pwd):
        """
        Tell whether an active user has this login and this password hash.

        Returns:
            bool: True when they match, False otherwise or on SQL error.
        """
        cursor = DB.cursor()

        req = ('select count(*) as nb_user '
               'from sigl_user_data '
               'where status = "' + Constants.cst_user_active + '" and username=%s and password=%s')

        cursor.execute(req, (login, pwd,))

        res = cursor.fetchone()

        if not res or res['nb_user'] != 1:
            return False

        # save in event_log this connection
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
        """
        Tell whether a user has this first name, last name and login, used by the import.
        """
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
        """
        Read the active user of a login with its profile, password hash included.
        """
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
    def hasRight(oauth_user, *prr_tags):
        """
        True when the calling user is granted one of these rights.
        """
        id_user = (oauth_user or {}).get('usr_id')
        if not id_user:
            return False

        l_rights = User.getUserListOfRights(id_user) or []

        return any(right['prr_tag'] in prr_tags and right['prp_granted'] == 'Y' for right in l_rights)

    @staticmethod
    def getCallerPrescriber(oauth_user):
        """
        Prescriber id of a caller with the prescriber role, None for any other role, 0 when none is linked.
        """
        if not oauth_user or oauth_user.get('usr_role') != 'P':
            return None

        user = User.getUserDetails(oauth_user.get('usr_id') or 0)

        return int(user['side_account'] or 0) if user else 0

    @staticmethod
    def getUserDetails(id_user):
        """
        Read one user with its title label and linked prescriber name, password left out.
        """
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
        """
        Insert a user in sigl_user_data, password already hashed.

        Returns:
            int: new id, 0 on SQL error.
        """
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
        """
        Update a user of sigl_user_data, password left unchanged.

        Returns:
            bool: True on success, False on SQL error.
        """
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
        """
        Update the user with this login, first name and last name from an import line, password left unchanged.

        Returns:
            bool: True on success, False on SQL error.
        """
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

        """
        Read the rights of a user: the ones of its profile, overridden by its own permissions.
        """
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

        """
        Read every right with its value for a user, or for a profile when id_user is 0, for the rights screen.
        """
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
    def getUserRoleList(type='', l_exclude=None, genuine='N'):
        """
        Read the profiles, of one role type, without the types of l_exclude, built-in ones only when
        genuine is 'Y', ordered by label.
        """
        cursor = DB.cursor()

        l_cond = []
        params = []

        if type:
            l_cond.append('type=%s')
            params.append(str(type))

        if l_exclude:
            l_cond.append('type not in (' + ','.join(['%s'] * len(l_exclude)) + ')')
            params.extend([str(exclude) for exclude in l_exclude])

        if genuine == 'Y':
            l_cond.append('pro_genuine="Y"')

        cond = ''
        if l_cond:
            cond = ' where ' + ' and '.join(l_cond)

        req = ('select pro_ser, pro_role as id_role, name, pro_label as label, type, pro_genuine, pro_color_1, '
               'pro_color_2, pro_text_color '
               'from profile_role '
               'inner join sigl_pj_role on id_role=pro_role ' + cond + ' order by label ')

        cursor.execute(req, tuple(params))

        return cursor.fetchall()

    @staticmethod
    def getUserRole(role_type):
        """
        Read the role (sigl_pj_role) of a role type.
        """
        cursor = DB.cursor()

        req = ('select id_role, name, label, type '
               'from sigl_pj_role '
               'where type=%s')

        cursor.execute(req, (role_type,))

        return cursor.fetchone()

    @staticmethod
    def getRoleDetails(pro_ser):
        """
        Read one profile with its role.
        """
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
        """
        Delete a profile with its permissions and the user permissions based on it.

        Returns:
            bool: True on success, False on SQL error.
        """
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
        """
        Insert a profile in profile_role.

        Returns:
            int: new id, 0 on SQL error.
        """
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
        """
        Read the profile of a user.
        """
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
        """
        Update the label and colours of a profile.

        Returns:
            bool: True on success, False on SQL error.
        """
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
        """
        Insert a permission of a profile for one right.

        Returns:
            int: new id, 0 on SQL error.
        """
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
        """
        Set the value of one permission of a profile.

        Returns:
            bool: True on success, False on SQL error.
        """
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
        """
        Tell whether a profile permission has this value, to know if a user permission still differs from it.
        """
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
        """
        Insert a permission of a user that differs from its profile.

        Returns:
            int: new id, 0 on SQL error.
        """
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
        """
        Set the value of one permission of a user.

        Returns:
            bool: True on success, False on SQL error.
        """
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
        """
        Remove one permission of a user, its profile value applies again.

        Returns:
            bool: True on success, False on SQL error.
        """
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
        """
        Read the identity of every active user ('lastname firstname - login'), for select fields.
        """
        cursor = DB.cursor()

        req = ('select id_data as id_user, TRIM(CONCAT(lastname," ",firstname," - ",username)) as user_ident '
               'from sigl_user_data '
               'where status="A" order by lastname asc, firstname asc')

        cursor.execute(req)

        return cursor.fetchall()

    @staticmethod
    def getUserExport():
        """
        Read every user with a login, password hashes included, for the CSV export.
        """
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
        """
        Read the users with their profile, oldest first.
        args: firstname, lastname, login, role_pro, status.
        """
        cursor = DB.cursor()

        filter_cond = 'u.role_type != "X" '
        params = [Constants.cst_isodate]

        if not args:
            limit = 'LIMIT 500'

            filter_cond += ' and u.status="' + Constants.cst_user_active + '" '  # keep active users by default
        else:
            limit = 'LIMIT 500'
            # filter conditions
            if 'login' in args and args['login']:
                filter_cond += ' and u.username LIKE %s '
                params.append('%' + args['login'] + '%')

            if 'firstname' in args and args['firstname']:
                filter_cond += ' and u.firstname LIKE %s '
                params.append('%' + args['firstname'] + '%')

            if 'lastname' in args and args['lastname']:
                filter_cond += ' and u.lastname LIKE %s '
                params.append('%' + args['lastname'] + '%')

            if 'status' in args and args['status']:
                # Keep compatibility with old delete user
                if args['status'] == Constants.cst_user_inactive:
                    stat = '(u.status="' + Constants.cst_user_inactive + '" or u.status="' + Constants.cst_user_deleted + '")'
                else:
                    stat = 'u.status=%s '
                    params.append(str(args['status']))

                filter_cond += ' and ' + stat + ' '
            else:
                filter_cond += ' and u.status="' + Constants.cst_user_active + '" '  # keep active users by default

            if 'role_pro' in args and args['role_pro']:
                filter_cond += ' and u.role_pro=%s '
                params.append(args['role_pro'])

        req = ('select u.id_data, u.id_owner, u.username, u.firstname, u.lastname, u.status as stat, '
               'u.initiale as initial, u.ddn as birth, u.adresse as address, u.tel as phone, u.email, '
               'u.darrive as arrived, u.position as position, dict.label as section, u.deval as last_eval, '
               'date_format(u.creation_date, %s) as date_create, r.label as role, '
               'u.oauth_provider_id_user as id_origin, COALESCE(u2.username, "") as origin, u.role_type, u.role_pro, '
               'pro.pro_label as pro_label '
               'from sigl_user_data as u '
               'inner join profile_role as pro on pro.pro_ser=u.role_pro '
               'inner join sigl_pj_role as r on r.id_role=pro.pro_role '
               'left join sigl_user_data as u2 on u2.id_data=u.oauth_provider_id_user '
               'left join sigl_dico_data as dict on dict.id_data=u.section '
               'where ' + filter_cond +
               'group by u.id_data order by u.creation_date asc ' + limit)

        cursor.execute(req, tuple(params))

        return cursor.fetchall()

    @staticmethod
    def getUserLiteList():
        """
        Read the active users with an 'A' or 'AGT' role, who can be given access to LabBook Lite.
        """
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
        """
        Search users for a select field.
        """
        cursor = DB.cursor()

        l_words = text.split(' ')

        cond = 'status="' + Constants.cst_user_active + '" '

        params = []

        for word in l_words:
            cond = (cond +
                    ' and (lastname like %s or '
                    'firstname like %s or '
                    'username like %s) ')
            params.extend([word + '%'] * 3)

        limit = ' limit 1000'

        req = ('select id_data, TRIM(CONCAT(lastname," ",firstname," - ",username)) AS field_value '
               'from sigl_user_data '
               'where ' + cond + limit)

        cursor.execute(req, tuple(params))

        return cursor.fetchall()

    @staticmethod
    def getUserConnections(date_beg, date_end):
        """
        Read the logins and logouts of a period from event_log (type 17), oldest first.
        """
        cursor = DB.cursor()

        limit = ' limit 50000'

        req = ('select e.evl_user as id_user, COALESCE(u.username, "") as username, e.evl_date as date, '
               'e.evl_name as event, e.evl_message as message '
               'from event_log as e '
               'left join sigl_user_data as u on u.id_data=e.evl_user '
               'where (e.evl_date between %s and %s) and e.evl_type=17 '
               'order by e.evl_date ' + limit)

        cursor.execute(req, (date_beg, date_end,))

        return cursor.fetchall()

    @staticmethod
    def checkPassword(id_user, pwd):
        """
        True when pwd is the current password of this user, hashed as at login with the stored salt.
        """
        cursor = DB.cursor()

        cursor.execute('select password from sigl_user_data where id_data=%s', (id_user,))

        res = cursor.fetchone()

        if not res or not res['password'] or ':' not in res['password'] or not pwd:
            return False

        salt = res['password'].split(':', 1)[1]

        return User.getPasswordDB(pwd, salt) == res['password']

    @staticmethod
    def getPasswordDB(pwd, salt=''):
        # password hash (TODO by Bcrypt)

        """
        Hash a password as stored in sigl_user_data: SHA1 of the MD5 of the password completed with part
        of the salt, then ':' and the salt. A new random salt is drawn when none is given.
        MD5 and SHA1 are fast hashes, the code notes a move to bcrypt still to do.

        Returns:
            str: 'hash:salt'.
        """
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
        """
        Store a new password hash for a user.

        Returns:
            bool: True on success, False on SQL error.
        """
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
        """
        Set the status of a user ('A' active, 'D' disabled).

        Returns:
            bool: True on success, False on SQL error.
        """
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
        """
        Count the active users.
        """
        cursor = DB.cursor()

        # Number of records
        req = ('select count(*) as nb_users '
               'from sigl_user_data '
               'where status="' + Constants.cst_user_active + '"')

        cursor.execute(req)

        return cursor.fetchone()

    @staticmethod
    def countProfileByRole(pro_ser):
        """
        Count the active users of a profile.
        """
        cursor = DB.cursor()

        # Number of profiles
        req = ('select count(*) as nb_profile '
               'from sigl_user_data '
               'where status="' + Constants.cst_user_active + '" and role_pro=%s')

        cursor.execute(req, (pro_ser,))

        return cursor.fetchone()

    @staticmethod
    def role_exist(role_label):
        """
        Tell whether a profile name is used.

        Returns:
            bool or int: True if used, False otherwise, -1 on SQL error.
        """
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
