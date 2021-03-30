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
    def getEquipmentSearch(text):
        cursor = DB.cursor()

        l_words = text.split(' ')

        cond = 'nom is not NULL '

        for word in l_words:
            cond = (cond + ' and (nom like "%' + word + '%") ')

        req = 'select nom as field_value, id_data '\
              'from sigl_equipement_data '\
              'where ' + cond + ' order by field_value asc limit 1000'

        cursor.execute(req)

        return cursor.fetchall()

    @staticmethod
    def getEquipment(id_item):
        cursor = DB.cursor()

        req = ('select eqp.id_data, eqp.nom as name, eqp.nom_fabriquant as maker, eqp.modele as model, eqp.fonction as funct, '
               'eqp.localisation as location, eqp.section, eqp.fournisseur_id as supplier_id, eqp.no_serie as serial, '
               'eqp.no_inventaire as inventory, eqp.responsable_id as incharge_id, eqp.manuel_id as manual_id, '
               'eqp.procedures_id as procedur_id, eqp.pannes as breakdown, eqp.maintenance_preventive as maintenance, '
               'eqp.certif_etalonnage as calibration, eqp.contrat_maintenance as contract, eqp.date_fin_contrat as date_endcontract, '
               'eqp.date_reception as date_receipt, eqp.date_achat as date_buy, eqp.date_acquisition as date_procur, '
               'eqp.date_mise_en_service as date_onduty, eqp.date_de_retrait as date_revoc, eqp.commentaires as comment, '
               'u1.fournisseur_nom as supplier, u3.titre as manual, u4.titre as procedur, '
               'TRIM(CONCAT(u2.lastname," ",u2.firstname," - ",u2.username)) as incharge '
               'from sigl_equipement_data as eqp '
               'left join sigl_fournisseurs_data as u1 on u1.id_data=eqp.fournisseur_id '
               'left join sigl_user_data as u2 on u2.id_data=eqp.responsable_id '
               'left join sigl_manuels_data as u3 on u3.id_data=eqp.manuel_id '
               'left join sigl_procedures_data as u4 on u4.id_data=eqp.procedures_id '
               'where eqp.id_data=%s')

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
                           '%(incharge)s, %(manual)s, %(procedur)s, %(breakdown)s, %(maintenance)s, '
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
                           'responsable_id=%(incharge)s, manuel_id=%(manual)s, procedures_id=%(procedur)s, '
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
    def getStockList(args):
        cursor = DB.cursor()

        filter_cond = ' prs_ser > 0 '

        if not args:
            limit = 'LIMIT 1000'
        else:
            if 'limit' in args and args['limit'] > 0:
                limit = 'LIMIT ' + str(args['limit'])
            else:
                limit = 'LIMIT 500'

            # filter conditions
            if args['prod_name']:
                filter_cond += ' and prd_name LIKE "%' + args['prod_name'] + '%" '

            if 'prod_type' in args and args['prod_type'] > 0:
                filter_cond += ' and prd_type = ' + str(args['prod_type'])

            if 'prod_conserv' in args and args['prod_conserv'] > 0:
                filter_cond += ' and prd_conserv = ' + str(args['prod_conserv'])

        req = ('select prs_ser, prs_prd, prd_name, prd_nb_by_pack, '
               'sum(pru_nb_pack) as pru_nb_pack, prd_safe_limit, '
               'dict1.label as type,  dict2.label as conserv, '
               'sup.fournisseur_nom as supplier, Min(prs_expir_date) as expir_date '
               'from product_supply '
               'inner join product_details on prd_ser=prs_prd '
               'left join product_use on pru_prs=prs_ser '
               'left join sigl_fournisseurs_data as sup on sup.id_data=prd_supplier '
               'left join sigl_dico_data as dict1 on dict1.id_data=prd_type '
               'left join sigl_dico_data as dict2 on dict2.id_data=prd_conserv '
               'where ' + filter_cond + ' ' +
               'group by prd_name '
               'order by prd_name asc ' + limit)

        cursor.execute(req)

        return cursor.fetchall()

    @staticmethod
    def getSumStockSupply(id_item):
        cursor = DB.cursor()

        req = ('select sum(prs_nb_pack) as total '
               'from product_supply '
               'where prs_prd=%s group by prs_prd')

        cursor.execute(req, (id_item,))

        return cursor.fetchone()

    @staticmethod
    def getStockListDet(id_item):
        cursor = DB.cursor()

        req = ('select prs_ser, prd_name, prs_nb_pack, prs_receipt_date, prs_expir_date, prs_rack, prs_batch_num, '
               'prs_buy_price, sum(pru_nb_pack) as pru_nb_pack '
               'from product_supply '
               'inner join product_details on prd_ser=prs_prd '
               'left join product_use on pru_prs=prs_ser '
               'where prs_empty="N" and prd_ser=%s '
               'group by prs_ser '
               'order by prs_expir_date asc ')

        cursor.execute(req, (id_item,))

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
    def getStockProductSearch(text):
        cursor = DB.cursor()

        l_words = text.split(' ')

        cond = 'prd_ser > 0 '

        for word in l_words:
            cond = (cond + ' and (prd_name like "%' + word + '%") ')

        req = 'select prd_name as field_value, prd_ser as id_item '\
              'from product_details '\
              'where ' + cond + ' order by field_value asc limit 1000'

        cursor.execute(req)

        return cursor.fetchall()

    @staticmethod
    def getStockProduct(id_item):
        cursor = DB.cursor()

        req = ('select prd_ser, prd_name, prd_type, prd_nb_by_pack, prd_supplier, prd_ref_supplier, prd_conserv, '
               'sup.fournisseur_nom as supplier_name, prd_safe_limit '
               'from product_details '
               'left join sigl_fournisseurs_data as sup on sup.id_data=prd_supplier '
               'where prd_ser=%s')

        cursor.execute(req, (id_item,))

        return cursor.fetchone()

    @staticmethod
    def getStockProductHist(id_item, date_beg, date_end):
        cursor = DB.cursor()

        # Take all supply  for this product
        req = ('select prs_ser, prs_nb_pack, prs_receipt_date, prs_expir_date, prs_rack, '
               'prs_batch_num, prs_buy_price, prs_date as date_create, username '
               'from product_supply '
               'left join sigl_user_data on id_data=prs_user '
               'where prs_prd=%s and (prs_date between %s and %s)')

        cursor.execute(req, (id_item, date_beg, date_end,))

        ret = cursor.fetchall()

        # Take all use for this product
        req = ('select pru_ser, pru_nb_pack, username, pru_date as date_create '
               'from product_use '
               'inner join product_supply on prs_ser=pru_prs '
               'left join sigl_user_data on id_data=pru_user '
               'where prs_prd=%s and (pru_date between %s and %s)')

        cursor.execute(req, (id_item, date_beg, date_end,))

        ret = ret + cursor.fetchall()

        return ret

    @staticmethod
    def insertStockProduct(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into product_details '
                           '(prd_date, prd_name, prd_type, prd_nb_by_pack, prd_supplier, prd_ref_supplier, prd_conserv, prd_safe_limit) '
                           'values '
                           '(NOW(), %(prd_name)s, %(prd_type)s, %(prd_nb_by_pack)s, %(prd_supplier)s, '
                           '%(prd_ref_supplier)s, %(prd_conserv)s, %(prd_safe_limit)s)', params)

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
                           'prd_supplier=%(prd_supplier)s, prd_ref_supplier=%(prd_ref_supplier)s, '
                           'prd_conserv=%(prd_conserv)s, prd_safe_limit=%(prd_safe_limit)s '
                           'where prd_ser=%(prd_ser)s', params)

            Quality.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getNbStockSupply(id_item):
        cursor = DB.cursor()

        req = ('select prs_nb_pack as nb_pack '
               'from product_supply '
               'where prs_ser=%s')

        cursor.execute(req, (id_item,))

        return cursor.fetchone()

    @staticmethod
    def getNbStockUse(id_item):
        cursor = DB.cursor()

        req = ('select sum(pru_nb_pack) as nb_pack '
               'from product_use '
               'where pru_prs=%s '
               'group by pru_prs')

        cursor.execute(req, (id_item,))

        return cursor.fetchone()

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
    def insertStockSupply(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into product_supply '
                           '(prs_date, prs_prd, prs_nb_pack, prs_receipt_date, prs_expir_date, '
                           'prs_rack, prs_batch_num, prs_buy_price) '
                           'values '
                           '(NOW(), %(prs_prd)s, %(prs_nb_pack)s, %(prs_receipt_date)s, '
                           '%(prs_expir_date)s, %(prs_rack)s, %(prs_batch_num)s, %(prs_buy_price)s)', params)

            Quality.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def emptyStockSupply(prs_ser):
        try:
            cursor = DB.cursor()

            cursor.execute('update product_supply '
                           'set prs_empty="Y" '
                           'where prs_ser=%s', (prs_ser,))

            Quality.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def insertStockUse(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into product_use '
                           '(pru_date, pru_user, pru_prs, pru_nb_pack) '
                           'values '
                           '(NOW(), %(pru_user)s, %(pru_prs)s, %(pru_nb_pack)s)', params)

            Quality.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

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
    def getManualSearch(text):
        cursor = DB.cursor()

        l_words = text.split(' ')

        cond = '(titre is not NULL or reference is not NULL) '

        for word in l_words:
            cond = (cond + ' and (titre like "%' + word + '%" or reference like "%' + word + '%") ')

        req = 'select CONCAT(titre," / ref: ",reference) as field_value, id_data '\
              'from sigl_manuels_data '\
              'where ' + cond + ' order by field_value asc limit 1000'

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
               'manu.approbateur_id as approver_id, manu.date_insert, manu.date_apply, '
               'manu.date_update, manu.section '
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
    def getProcedureSearch(text):
        cursor = DB.cursor()

        l_words = text.split(' ')

        cond = '(titre is not NULL or reference is not NULL) '

        for word in l_words:
            cond = (cond + ' and (titre like "%' + word + '%" or reference like "%' + word + '%") ')

        req = 'select CONCAT(titre," / ref: ",reference) as field_value, id_data '\
              'from sigl_procedures_data '\
              'where ' + cond + ' order by field_value asc limit 1000'

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
