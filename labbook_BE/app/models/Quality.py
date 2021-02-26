# -*- coding:utf-8 -*-
import logging
import mysql.connector

# from app.models.Constants import *
from app.models.DB import DB
from app.models.Constants import Constants
from app.models.Logs import Logs


class Quality:
    log = logging.getLogger('log_db')

    @staticmethod
    def getLastMeeting():
        cursor = DB.cursor()

        req = 'select id_data, id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, '\
              'date, organisateur_id as id_promoter, type_reu as type, cr as report '\
              'from sigl_reunion_data '\
              'order by date desc limit 1'

        cursor.execute(req)

        return cursor.fetchone()

    @staticmethod
    def getNbNonCompliance(period):
        cursor = DB.cursor()

        cond = ''

        if period == 'open':
            cond = ' cloture_date is NULL '

        elif period == 'month':
            cond = ' date > adddate(NOW(), INTERVAL -1 MONTH) '

        # NOTE count with sigl_non_coformite_data too ?
        # Number of non-compliance
        req = 'select count(*) as nb_noncompliance '\
              'from sigl_non_conf_data '\
              'where ' + cond

        cursor.execute(req)

        return cursor.fetchone()

    @staticmethod
    def getEquipmentList():
        cursor = DB.cursor()

        req = ('select eqp.id_data, eqp.nom as name, eqp.nom_fabriquant as maker, eqp.modele as model, '
               'eqp.fonction as funct, eqp.localisation as location, dict.label as section '
               'from sigl_equipement_data as eqp '
               'left join sigl_dico_data as dict on dict.id_data=eqp.section '
               'order by name asc')

        cursor.execute(req)

        return cursor.fetchall()

    @staticmethod
    def getEquipment(id_item):
        cursor = DB.cursor()

        req = ('select id_data, nom as name, nom_fabriquant as maker, modele as model, fonction as funct, '
               'localisation as location, section, fournisseur_id as supplier, no_serie as serial, '
               'no_inventaire as inventory, responsable_id as incharge, manuel_id as manual, '
               'procedures_id as procedure, pannes as breakdown, maintenance_preventive as maintenance, '
               'certif_etalonnage as calibration, contrat_maintenance as contract, date_fin_contrat as date_endcontract, '
               'date_reception as date_receipt, date_achat as date_buy, date_acquisition as date_procur, '
               'date_mise_en_service as date_onduty, date_de_retrait as date_revoc, commentaires as comment '
               'from sigl_equipement_data '
               'where id_data=%s')

        cursor.execute(req, (id_item,))

        return cursor.fetchone()

    @staticmethod
    def insertEquipment(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into sigl_equipement_data '
                           '(id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, nom, nom_fabriquant, '
                           'modele, fonction, localisation, section, fournisseur_id, no_serie, no_inventaire, '
                           'responsable_id, manuel_id, procedures_id, pannes, maintenance_preventive, '
                           'certif_etalonnage, contrat_maintenance, date_fin_contrat, date_reception, date_achat, '
                           'date_acquisition, date_mise_en_service, date_de_retrait, commentaires) '
                           'values '
                           '(%(id_owner)s, NOW(), NOW(), %(id_owner)s, %(name)s, %(maker)s, %(model)s, '
                           '%(funct)s, %(location)s, %(section)s, %(supplier)s, %(serial)s, %(inventory)s, '
                           '%(incharge)s, %(manual)s, %(procedure)s, %(breakdown)s, %(maintenance)s, '
                           '%(calibration)s, %(contract)s, %(date_endcontract)s, %(date_receipt)s, %(date_buy)s, '
                           '%(date_procur)s, %(date_onduty)s, %(date_revoc)s, %(comment)s)', params)

            Quality.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def updateEquipment(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('update sigl_equipement_data '
                           'set nom=%(name)s, nom_fabriquant=%(maker)s, '
                           'modele=%(model)s, fonction=%(funct)s, localisation=%(location)s, section=%(section)s, '
                           'fournisseur_id=%(supplier)s, no_serie=%(serial)s, no_inventaire=%(inventory)s, '
                           'responsable_id=%(incharge)s, manuel_id=%(manual)s, procedures_id=%(procedure)s, '
                           'pannes=%(breakdown)s, maintenance_preventive=%(maintenance)s, '
                           'certif_etalonnage=%(calibration)s, contrat_maintenance=%(contract)s, '
                           'date_fin_contrat=%(date_endcontract)s, date_reception=%(date_receipt)s, '
                           'date_achat=%(date_buy)s, date_acquisition=%(date_procur)s, '
                           'date_mise_en_service=%(date_onduty)s, date_de_retrait=%(date_revoc)s, commentaires=%(comment)s  '
                           'where id_data=%(id_data)s', params)

            Quality.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def deleteEquipment(id_item):
        try:
            cursor = DB.cursor()

            cursor.execute('delete from sigl_equipement_data '
                           'where id_data=%s', (id_item,))

            Quality.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getStockList():
        cursor = DB.cursor()

        req = 'select id_data, id_owner, fournisseur_nom as supplier, contact_nom as lastname, '\
              'contact_prenom as firstname, contact_fonction as funct, fournisseur_adresse as address, '\
              'contact_tel as phone, contact_mobile as mobile, contact_fax as fax, contact_email as email, '\
              'commentaire as comment, date_format(sys_creation_date, %s) as date_create, '\
              'date_format(sys_last_mod_date, %s) as date_update, sys_last_mod_user as id_user_upd '\
              'from sigl_fournisseurs_data '\
              'order by supplier asc, lastname asc, firstname asc'

        cursor.execute(req, (Constants.cst_isodatetime, Constants.cst_isodatetime,))

        return cursor.fetchall()

    @staticmethod
    def getStockSearch(text):
        cursor = DB.cursor()

        l_words = text.split(' ')

        cond = 'fournisseur_nom is not NULL '

        for word in l_words:
            cond = (cond + ' and (fournisseur_nom like "%' + word + '%") ')

        req = 'select fournisseur_nom as field_value, id_data '\
              'from sigl_fournisseurs_data '\
              'where ' + cond + ' order by field_value asc limit 1000'

        cursor.execute(req)

        return cursor.fetchall()

    @staticmethod
    def getStockProduct(id_item):
        cursor = DB.cursor()

        req = ('select prd_ser, prd_name, prd_type, prd_nb_by_pack, prd_supplier, prd_ref_supplier, prd_conserv '
               'from product_details '
               'where id_data=%s')

        cursor.execute(req, (id_item,))

        return cursor.fetchone()

    @staticmethod
    def insertStockProduct(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into product_details '
                           '(prd_date, prd_name, prd_type, prd_nb_by_pack, prd_supplier, prd_ref_supplier, prd_conserv) '
                           'values '
                           '(NOW(), %(prd_name)s, %(prd_type)s, %(prd_nb_by_pack)s, %(prd_supplier)s, '
                           '%(prd_ref_supplier)s, %(prd_conserv)s)', params)

            Quality.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def updateStockProduct(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('update product_details '
                           'set prd_name=%(prd_name)s, prd_type=%(prd_type)s, prd_nb_by_pack=%(prd_nb_by_pack)s, '
                           'prd_supplier=%(prd_supplier)s, prd_ref_supplier=%(prd_ref_supplier)s, prd_conserv=%(prd_conserv)s, '
                           'where prd_ser=%(prd_ser)s', params)

            Quality.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def deleteStockProduct(id_item):
        try:
            cursor = DB.cursor()

            cursor.execute('delete from product_details '
                           'where prd_ser=%s', (id_item,))

            Quality.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getSupplierList():
        cursor = DB.cursor()

        req = 'select id_data, id_owner, fournisseur_nom as supplier, contact_nom as lastname, '\
              'contact_prenom as firstname, contact_fonction as funct, fournisseur_adresse as address, '\
              'contact_tel as phone, contact_mobile as mobile, contact_fax as fax, contact_email as email, '\
              'commentaire as comment, date_format(sys_creation_date, %s) as date_create, '\
              'date_format(sys_last_mod_date, %s) as date_update, sys_last_mod_user as id_user_upd '\
              'from sigl_fournisseurs_data '\
              'order by supplier asc, lastname asc, firstname asc'

        cursor.execute(req, (Constants.cst_isodatetime, Constants.cst_isodatetime,))

        return cursor.fetchall()

    @staticmethod
    def getSupplierSearch(text):
        cursor = DB.cursor()

        l_words = text.split(' ')

        cond = 'fournisseur_nom is not NULL '

        for word in l_words:
            cond = (cond + ' and (fournisseur_nom like "%' + word + '%") ')

        req = 'select fournisseur_nom as field_value, id_data '\
              'from sigl_fournisseurs_data '\
              'where ' + cond + ' order by field_value asc limit 1000'

        cursor.execute(req)

        return cursor.fetchall()

    @staticmethod
    def getSupplier(id_item):
        cursor = DB.cursor()

        req = 'select id_data ,id_owner, fournisseur_nom as supplier, contact_nom as lastname, '\
              'contact_prenom as firstname, contact_fonction as funct, contact_tel as phone, '\
              'contact_email as email, fournisseur_adresse as address, '\
              'contact_mobile as mobile, contact_fax as fax, commentaire as comment '\
              'from sigl_fournisseurs_data '\
              'where id_data=%s'

        cursor.execute(req, (id_item,))

        return cursor.fetchone()

    @staticmethod
    def insertSupplier(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into sigl_fournisseurs_data '
                           '(id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, fournisseur_nom, '
                           'contact_nom, contact_prenom, contact_fonction, fournisseur_adresse, contact_tel, '
                           'contact_email, contact_mobile, contact_fax, commentaire) '
                           'values '
                           '(%(id_owner)s, NOW(), NOW(), %(id_owner)s, %(supplier)s, %(lastname)s, %(firstname)s, '
                           '%(funct)s, %(address)s, %(phone)s, %(email)s, %(mobile)s, %(fax)s, %(comment)s)', params)

            Quality.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def updateSupplier(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('update sigl_fournisseurs_data '
                           'set fournisseur_nom=%(supplier)s, contact_nom=%(lastname)s, contact_prenom=%(prenom)s, '
                           'contact_fonction=%(funct)s, fournisseur_adresse=%(address)s, contact_tel=%(phone)s, '
                           'contact_email=%(email)s, contact_mobile=%(mobile)s, contact_fax=%(fax)s, commentaire=%(comment)s '
                           'where id_data=%(id_data)s', params)

            Quality.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def deleteSupplier(id_item):
        try:
            cursor = DB.cursor()

            cursor.execute('delete from sigl_fournisseurs_data '
                           'where id_data=%s', (id_item,))

            Quality.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getManualList():
        cursor = DB.cursor()

        req = ('select manu.id_data, manu.titre as title, manu.reference, '
               'u1.initiale as writer, u2.initiale as auditor, u3.initiale as approver, '
               'date_insert, date_apply, date_update, dict.label as section '
               'from sigl_manuels_data as manu '
               'left join sigl_user_data as u1 on u1.id_data=manu.redacteur_id '
               'left join sigl_user_data as u2 on u2.id_data=manu.verificateur_id '
               'left join sigl_user_data as u3 on u3.id_data=manu.approbateur_id '
               'left join sigl_dico_data as dict on dict.id_data=manu.section '
               'order by title asc ')

        cursor.execute(req)

        return cursor.fetchall()

    @staticmethod
    def getManual(id_item):
        cursor = DB.cursor()

        req = ('select manu.id_data ,manu.id_owner, manu.titre as title, manu.reference, '
               'TRIM(CONCAT(u1.lastname," ",u1.firstname," - ",u1.username)) as writer, '
               'TRIM(CONCAT(u2.lastname," ",u2.firstname," - ",u2.username)) as auditor, '
               'TRIM(CONCAT(u3.lastname," ",u3.firstname," - ",u3.username)) as approver, '
               'manu.redacteur_id as writer_id, manu.verificateur_id as auditor_id, '
               'manu.approbateur_id as approver_id, date_insert, date_apply, date_update, section '
               'from sigl_manuels_data as manu '
               'left join sigl_user_data as u1 on u1.id_data=manu.redacteur_id '
               'left join sigl_user_data as u2 on u2.id_data=manu.verificateur_id '
               'left join sigl_user_data as u3 on u3.id_data=manu.approbateur_id '
               'where manu.id_data=%s')

        cursor.execute(req, (id_item,))

        return cursor.fetchone()

    @staticmethod
    def insertManual(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into sigl_manuels_data '
                           '(id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, titre , reference, '
                           'redacteur_id, verificateur_id, approbateur_id, date_insert, date_apply, date_update, section) '
                           'values '
                           '(%(id_owner)s, NOW(), NOW(), %(id_owner)s, %(title)s, %(reference)s, %(writer)s, %(auditor)s, '
                           '%(approver)s, %(date_insert)s, %(date_apply)s, %(date_update)s, %(section)s)', params)

            Quality.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def updateManual(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('update sigl_manuels_data '
                           'set titre=%(title)s , reference=%(reference)s, redacteur_id=%(writer)s, '
                           'verificateur_id=%(auditor)s, approbateur_id=%(approver)s, date_insert=%(date_insert)s, '
                           'date_apply=%(date_apply)s, date_update=%(date_update)s, section=%(section)s '
                           'where id_data=%(id_data)s', params)

            Quality.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def deleteManual(id_item):
        try:
            cursor = DB.cursor()

            cursor.execute('delete from sigl_manuels_data '
                           'where id_data=%s', (id_item,))

            Quality.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getMeetingList():
        cursor = DB.cursor()

        req = ('select meet.id_data, meet.date as date_meeting, meet.type_reu as type, '
               'u1.initiale as promoter, meet.cr as report '
               'from sigl_reunion_data as meet '
               'left join sigl_user_data as u1 on u1.id_data=meet.organisateur_id '
               'order by date_meeting desc ')

        cursor.execute(req)

        return cursor.fetchall()

    @staticmethod
    def getMeeting(id_item):
        cursor = DB.cursor()

        req = ('select meet.id_data ,meet.id_owner, meet.date as date_meeting, meet.type_reu as type, '
               'TRIM(CONCAT(u1.lastname," ",u1.firstname," - ",u1.username)) as promoter, '
               'meet.organisateur_id as promoter_id, cr as report '
               'from sigl_reunion_data as meet '
               'left join sigl_user_data as u1 on u1.id_data=meet.organisateur_id '
               'where meet.id_data=%s')

        cursor.execute(req, (id_item,))

        return cursor.fetchone()

    @staticmethod
    def insertMeeting(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into sigl_reunion_data '
                           '(id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, date, type_reu, '
                           'organisateur_id, cr) '
                           'values '
                           '(%(id_owner)s, NOW(), NOW(), %(id_owner)s, %(date_meeting)s, %(type)s, '
                           '%(promoter)s, %(report)s)', params)

            Quality.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def updateMeeting(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('update sigl_reunion_data '
                           'set date=%(date_meeting)s , type_reu=%(type)s, organisateur_id=%(promoter)s, cr=%(report)s '
                           'where id_data=%(id_data)s', params)

            Quality.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def deleteMeeting(id_item):
        try:
            cursor = DB.cursor()

            cursor.execute('delete from sigl_reunion_data '
                           'where id_data=%s', (id_item,))

            Quality.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getProcedureList():
        cursor = DB.cursor()

        req = ('select proc.id_data, proc.id_owner, proc.titre as title, proc.reference as reference, '
               'u1.initiale as writer, u2.initiale as auditor, u3.initiale as approver, '
               'date_insert, date_apply, date_update, dict.label as section '
               'from sigl_procedures_data as proc '
               'left join sigl_user_data as u1 on u1.id_data=proc.redacteur_id '
               'left join sigl_user_data as u2 on u2.id_data=proc.verificateur_id '
               'left join sigl_user_data as u3 on u3.id_data=proc.approbateur_id '
               'left join sigl_dico_data as dict on dict.id_data=proc.section '
               'order by title asc ')

        cursor.execute(req)

        return cursor.fetchall()

    @staticmethod
    def getProcedure(id_item):
        cursor = DB.cursor()

        req = ('select proc.id_data ,proc.id_owner, proc.titre as title, proc.reference, '
               'TRIM(CONCAT(u1.lastname," ",u1.firstname," - ",u1.username)) as writer, '
               'TRIM(CONCAT(u2.lastname," ",u2.firstname," - ",u2.username)) as auditor, '
               'TRIM(CONCAT(u3.lastname," ",u3.firstname," - ",u3.username)) as approver, '
               'proc.redacteur_id as writer_id, proc.verificateur_id as auditor_id, '
               'proc.approbateur_id as approver_id, date_insert, date_apply, date_update, proc.section '
               'from sigl_procedures_data as proc '
               'left join sigl_user_data as u1 on u1.id_data=proc.redacteur_id '
               'left join sigl_user_data as u2 on u2.id_data=proc.verificateur_id '
               'left join sigl_user_data as u3 on u3.id_data=proc.approbateur_id '
               'where proc.id_data=%s')

        cursor.execute(req, (id_item,))

        return cursor.fetchone()

    @staticmethod
    def insertProcedure(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into sigl_procedures_data '
                           '(id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, titre , reference, '
                           'redacteur_id, verificateur_id, approbateur_id, date_insert, date_apply, date_update, section) '
                           'values '
                           '(%(id_owner)s, NOW(), NOW(), %(id_owner)s, %(title)s, %(reference)s, %(writer)s, %(auditor)s, '
                           '%(approver)s, %(date_insert)s, %(date_apply)s, %(date_update)s, %(section)s)', params)

            Quality.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def updateProcedure(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('update sigl_procedures_data '
                           'set titre=%(title)s , reference=%(reference)s, redacteur_id=%(writer)s, '
                           'verificateur_id=%(auditor)s, approbateur_id=%(approver)s, date_insert=%(date_insert)s, '
                           'date_apply=%(date_apply)s, date_update=%(date_update)s, section=%(section)s '
                           'where id_data=%(id_data)s', params)

            Quality.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def deleteProcedure(id_item):
        try:
            cursor = DB.cursor()

            cursor.execute('delete from sigl_procedures_data '
                           'where id_data=%s', (id_item,))

            Quality.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getStaffList():
        cursor = DB.cursor()

        req = ('select usr.id_data, usr.lastname, usr.firstname, usr.initiale as initial, '
               'date_format(usr.ddn, %s) as birth, usr.adresse as address, usr.tel as phone, usr.email, '
               'date_format(usr.darrive, %s) as arrived, usr.position, dict.label as section, '
               'date_format(usr.deval, %s) as last_eval, usr.username '
               'from sigl_user_data as usr '
               'left join sigl_dico_data as dict on dict.id_data=usr.section '
               'where usr.status=29 '
               'order by usr.lastname asc, usr.firstname asc')

        cursor.execute(req, (Constants.cst_isodatetime, Constants.cst_isodatetime, Constants.cst_isodatetime,))

        return cursor.fetchall()
