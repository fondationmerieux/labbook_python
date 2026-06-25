# -*- coding:utf-8 -*-
import logging

from datetime import datetime
from app.models.DB import DB
from app.models.Logs import Logs
from app.models.Various import Various

# --- SQL fragments (avoid magic strings) ---
LITE_EXCLUDE_CLAUSE = ' and rec.rec_lite = 0'   # exclude LabBook Lite
LITE_ONLY_CLAUSE    = ' and rec.rec_lite > 0'   # only LabBook Lite


class Export:
    log = logging.getLogger('log_db')

    @staticmethod
    def getDataWhonet(date_beg, date_end):
        cursor = DB.cursor()

        l_res = []
        l_tmp = []

        # Records list between two date
        req = ('select rec.id_data as id_rec, rec.date_hosp, rec.service_interne, rec.num_lit, rec.rec_hosp_num, '
               'dico.label as rec_type, rec.id_patient, ifnull(dict_med.label, "") as med_spe, num_dos_an '
               'from sigl_02_data as rec '
               'inner join sigl_dico_data as dico on rec.type=dico.id_data and dico.dico_name = "type_dossier" '
               'left join sigl_08_data as med on med.id_data=rec.med_prescripteur '
               'left join sigl_dico_data as dict_med on dict_med.id_data=med.specialite '
               'where statut=256 and rec_date_receipt >= %s and rec_date_receipt <= %s '
               'order by rec.id_data asc')

        cursor.execute(req, (date_beg, date_end,))

        l_rec = cursor.fetchall()

        # Export.log.info(Logs.fileline() + ' : l_rec=' + str(l_rec))

        for rec in l_rec:
            # check this list for whonet analyzes
            req = ('select ana.id_data as id_ana, req.id_data as id_req, code as ana_code, nom as ana_name '
                   'from sigl_04_data as req '
                   'left join sigl_05_data as ana on req.ref_analyse=ana.id_data '
                   'where ana.famille=18 and ana.ana_whonet=4 and ana.actif=4 and req.id_dos=%s')

            cursor.execute(req, (rec['id_rec'],))

            l_ana = cursor.fetchall()

            # Export.log.info(Logs.fileline() + ' : l_ana=' + str(l_ana))

            if l_ana:

                for ana in l_ana:
                    res = rec.copy()
                    res.update(ana)
                    l_tmp.append(res)

        # get results
        for ana in l_tmp:
            req = ('select res.id_data as id_res, res.valeur, var.libelle, var.type_resultat as type_res '
                   'from sigl_09_data as res '
                   'inner join sigl_07_data as var on var.id_data = res.ref_variable '
                   'inner join sigl_05_07_data as pos on var.id_data = pos.id_refvariable and pos.id_refanalyse=%s '
                   'inner join sigl_10_data as vld on vld.id_resultat = res.id_data '
                   'where res.id_analyse=%s and vld.type_validation=252 and vld.motif_annulation is NULL '
                   'and res.valeur is not NULL and res.valeur != "" and res.valeur != 1013 and pos.var_whonet=4 '
                   'order by pos.position asc')

            cursor.execute(req, (ana['id_ana'], ana['id_req'],))

            l_var = cursor.fetchall()

            if l_var:
                res = {}

                for res_var in l_var:
                    # find label for res value
                    if res_var['type_res'] == 600 or res_var['type_res'] == 1134:
                        res_label = Various.getDicoById(res_var['valeur'])
                        res_var['valeur'] = res_label['label']

                        res = ana.copy()
                        res.update(res_var)

                        res['method_value'] = ''
                    # add method result on the same line
                    elif res_var['libelle'].startswith('Diam. inhibition ') or res_var['libelle'].startswith('CMI ') or \
                         res_var['libelle'].endswith('inhibition diam.') or res_var['libelle'].endswith(' CMI'):
                        res['method_value'] = res_var['valeur']
                        if 'id_rec' not in res:
                            Export.log.warning(Logs.fileline() + ' : WHONET invalid ana=' + str(ana) + ' res_var=' + str(res_var))
                        l_res.append(res)

                    # in case of something else than antiobic and method result
                    else:
                        res = ana.copy()
                        res.update(res_var)

                        res['method_value'] = ''

                        if 'id_rec' not in res:
                            Export.log.warning(Logs.fileline() + ' : WHONET invalid ana=' + str(ana) + ' res_var=' + str(res_var))

                        l_res.append(res)

        # Export.log.info(Logs.fileline() + ' : l_res=' + str(l_res))

        # get products details with list of analyzes
        id_rec_p = 0
        l_products = []

        for res in l_res:
            if 'id_rec' not in res:
                Export.log.error(Logs.fileline() + ' : getDataWhonet missing id_rec in result=' + str(res))
                continue

            if id_rec_p != res['id_rec']:
                req = ('select id_dos, samp_date, dico.label as type_prod, commentaire as comment, prod.code '
                       'from sigl_01_data as prod '
                       'inner join sigl_dico_data as dico on prod.type_prel=dico.id_data and dico.dico_name="type_prel" '
                       'where prod.statut=8 and prod.id_dos=%s')

                cursor.execute(req, (res['id_rec'],))

                l_products = cursor.fetchall()
                id_rec_p = res['id_rec']

            if l_products:
                Export.log.info(Logs.fileline() + ' : l_products=' + str(l_products))
                for prod in l_products:
                    if res['id_rec'] == prod['id_dos']:
                        res['spec_code'] = prod['code']
                        res['spec_date'] = prod['samp_date']
                        res['spec_type'] = prod['type_prod']
                        res['spec_comment'] = prod['comment']
            else:
                res['spec_code'] = ''
                res['spec_date'] = ''
                res['spec_type'] = ''
                res['spec_comment'] = ''

        # Laboratory name
        lab_info = {}

        req = ('select value '
               'from sigl_06_data '
               'where identifiant="entete_1"')

        cursor.execute(req,)

        ret_info = cursor.fetchone()

        lab_info['lab_name'] = ret_info['value']

        # Laboratory address
        req = ('select value '
               'from sigl_06_data '
               'where identifiant="entete_adr"')

        cursor.execute(req,)

        ret_info = cursor.fetchone()

        lab_info['lab_addr'] = ret_info['value']

        # Laboratory city
        req = ('select value '
               'from sigl_06_data '
               'where identifiant="entete_ville"')

        cursor.execute(req,)

        ret_info = cursor.fetchone()

        lab_info['lab_city'] = ret_info['value']

        # Laboratory phone
        req = ('select value '
               'from sigl_06_data '
               'where identifiant="entete_tel"')

        cursor.execute(req,)

        ret_info = cursor.fetchone()

        lab_info['lab_phone'] = ret_info['value']

        # Laboratory email
        req = ('select value '
               'from sigl_06_data '
               'where identifiant="entete_email"')

        cursor.execute(req,)

        ret_info = cursor.fetchone()

        lab_info['lab_email'] = ret_info['value']

        # patient details and add lab info
        for res in l_res:
            req = ('select pat.code as pat_code, pat.nom as pat_name, pat.prenom as pat_fname, ddn, age, '
                   'dico.label as sex, pat.adresse as pat_addr, pat.ville as pat_city, pat.cp as pat_zip, '
                   'pat.tel as pat_phone, pat.profession as pat_class, pat.unite as cat_age, pat.code_patient '
                   'from sigl_03_data as pat '
                   'inner join sigl_dico_data as dico on pat.sexe=dico.id_data and dico.dico_name="sexe" '
                   'where pat.id_data=%s')

            cursor.execute(req, (res['id_patient'],))

            res.update(cursor.fetchone())

            if lab_info and lab_info['lab_name'] and lab_info['lab_addr'] and lab_info['lab_city'] and \
               lab_info['lab_phone'] and lab_info['lab_email']:
                res['lab_name']  = lab_info['lab_name']
                res['lab_addr']  = lab_info['lab_addr']
                res['lab_city']  = lab_info['lab_city']
                res['lab_phone'] = lab_info['lab_phone']
                res['lab_email'] = lab_info['lab_email']
            else:
                res['lab_name']  = ''
                res['lab_addr']  = ''
                res['lab_city']  = ''
                res['lab_phone'] = ''
                res['lab_email'] = ''

        return l_res

    @staticmethod
    def getStatDHIS2(date_beg, date_end, key, rec_type='A', lite_filter='A'):
        res = ''

        cursor = DB.cursor()

        # Number of records saved on a period
        if key == 'NB_REC_SAVED':
            req = ('select count(*) as value '
                   'from sigl_02_data '
                   'where (rec_date_receipt between %s and %s) and statut > 181')
            params = [date_beg, date_end]

            # Optional rec_type filter
            type_map = {'E': 183, 'I': 184}
            tval = type_map.get(rec_type)
            if tval is not None:
                req += ' and type = %s'
                params.append(tval)

            # LabBook Lite 3-state filter:
            #  - 'A' (All): no filter
            #  - 'N' (Exclude Lite): rec.rec_lite = 0
            #  - 'Y' (Only Lite):    rec.rec_lite > 0
            lf = (lite_filter or 'A').upper()
            if lf == 'N':
                req += LITE_EXCLUDE_CLAUSE
            elif lf == 'Y':
                req += LITE_ONLY_CLAUSE

            cursor.execute(req, tuple(params))
            res = cursor.fetchone()

        # Number of analyses saved on a period (without sample request)
        elif key == 'NB_ANA_SAVED':
            req = ('select count(*) as value '
                   'from sigl_04_data as req '
                   'inner join sigl_02_data as rec on rec.id_data=req.id_dos '
                   'inner join sigl_05_data as ref on ref.id_data = req.ref_analyse and ref.cote_unite != "PB" '
                   'where (rec.rec_date_receipt between %s and %s) and rec.statut > 181 and ref.actif=4')
            params = [date_beg, date_end]

            # Optional rec_type filter
            type_map = {'E': 183, 'I': 184}
            tval = type_map.get(rec_type)
            if tval is not None:
                req += ' and rec.type = %s'
                params.append(tval)

            # LabBook Lite 3-state filter:
            #  - 'A' (All): no filter
            #  - 'N' (Exclude Lite): rec.rec_lite = 0
            #  - 'Y' (Only Lite):    rec.rec_lite > 0
            lf = (lite_filter or 'A').upper()
            if lf == 'N':
                req += LITE_EXCLUDE_CLAUSE
            elif lf == 'Y':
                req += LITE_ONLY_CLAUSE

            cursor.execute(req, tuple(params))
            res = cursor.fetchone()

        # Number of sample outsourced on a period
        elif key == 'NB_SAMP_OUTSOURCED':
            req = ('select count(*) as value '
                   'from sigl_04_data as req '
                   'inner join sigl_02_data as rec on rec.id_data=req.id_dos '
                   'inner join sigl_05_data as ref on ref.id_data = req.ref_analyse and ref.cote_unite != "PB" '
                   'where (rec.rec_date_receipt between %s and %s) and rec.statut > 181 and ref.actif=4 '
                   'and req.req_outsourced = "Y"')
            params = [date_beg, date_end]

            # Optional rec_type filter
            type_map = {'E': 183, 'I': 184}
            tval = type_map.get(rec_type)
            if tval is not None:
                req += ' and rec.type = %s'
                params.append(tval)

            # LabBook Lite 3-state filter:
            #  - 'A' (All): no filter
            #  - 'N' (Exclude Lite): rec.rec_lite = 0
            #  - 'Y' (Only Lite):    rec.rec_lite > 0
            lf = (lite_filter or 'A').upper()
            if lf == 'N':
                req += LITE_EXCLUDE_CLAUSE
            elif lf == 'Y':
                req += LITE_ONLY_CLAUSE

            cursor.execute(req, tuple(params))
            res = cursor.fetchone()

        # Number of staff
        elif key == 'NB_STAFF':
            req = ('select count(*) as value '
                   'from sigl_user_data '
                   'where status="A"')

            cursor.execute(req)

            res = cursor.fetchone()

        # Number of secretary type
        elif key == 'NB_SECRETARY_TYPE':
            req = ('select count(*) as value '
                   'from sigl_user_data '
                   'where status="A" and role_type in ("S", "SA")')

            cursor.execute(req)

            res = cursor.fetchone()

        # Number of technician type
        elif key == 'NB_TECHNICIAN_TYPE':
            req = ('select count(*) as value '
                   'from sigl_user_data '
                   'where status="A" and role_type in ("T", "TA", "TQ")')

            cursor.execute(req)

            res = cursor.fetchone()

        # Number of qualitician type
        elif key == 'NB_QUALITICIAN_TYPE':
            req = ('select count(*) as value '
                   'from sigl_user_data '
                   'where status="A" and role_type in ("Q", "TQ")')

            cursor.execute(req)

            res = cursor.fetchone()

        # Number of biologist type
        elif key == 'NB_BIOLOGIST_TYPE':
            req = ('select count(*) as value '
                   'from sigl_user_data '
                   'where status="A" and role_type in ("B")')

            cursor.execute(req)

            res = cursor.fetchone()

        # Number of equipment
        elif key == 'NB_EQUIPMENT':
            req = ('select count(*) as value '
                   'from sigl_equipement_data')

            cursor.execute(req)

            res = cursor.fetchone()

        # Number of breakdown equipement on a period
        elif key == 'NB_EQP_BREAKDOWN':
            req = ('select count(*) as value '
                   'from eqp_failure as fail '
                   'inner join sigl_equipement_data as eqp on eqp.id_data=fail.eqf_eqp '
                   'where (fail.eqf_date between %s and %s) and fail.eqf_type="FAIL"')

            cursor.execute(req, (date_beg, date_end))

            res = cursor.fetchone()

        # Number of procedure
        elif key == 'NB_PROCEDURE':
            req = ('select count(*) as value '
                   'from sigl_procedures_data')

            cursor.execute(req)

            res = cursor.fetchone()

        # Number of product with expiry warning
        elif key == 'NB_PRODUCT_WITH_EXPIRY_WARNING':
            # get expiry warning setting
            req = ('select sos_expir_warning '
                   'from stock_setting')

            cursor.execute(req)

            setting = cursor.fetchone()

            req = ('select prs_prd '
                   'from product_supply '
                   'inner join product_details on prd_ser=prs_prd and prd_expir_oblig="Y" '
                   'where TIMESTAMPDIFF(SECOND, NOW(), prs_expir_date)/86400 > 0 and '
                   'TIMESTAMPDIFF(SECOND, NOW(), prs_expir_date)/86400 < %s and prs_empty="N" and prs_cancel="N" '
                   'group by prs_prd')

            cursor.execute(req, (setting['sos_expir_warning'],))

            row = cursor.fetchall()

            res = {}
            res['value'] = 0

            if row:
                res['value'] = len(row)

        # Number of product with expiry alert
        elif key == 'NB_PRODUCT_WITH_EXPIRY_ALERT':
            req = ('select prs_prd '
                   'from product_supply '
                   'inner join product_details on prd_ser=prs_prd and prd_expir_oblig="Y" '
                   'where TIMESTAMPDIFF(SECOND, NOW(), prs_expir_date)/86400 <= 0 and prs_empty="N" and prs_cancel="N" '
                   'group by prs_prd')

            cursor.execute(req)

            row = cursor.fetchall()

            res = {}
            res['value'] = 0

            if row:
                res['value'] = len(row)

        # Number of product close to be out of stock
        elif key == 'NB_PRODUCT_UNDER_SAFE_LIMIT':
            res = {}
            res['value'] = 0

            # count supply not canceled
            req = ('select prd_name, prd_safe_limit, sum(prs_nb_pack * prd_nb_by_pack) as nb_sup '
                   'from product_supply '
                   'inner join product_details on prd_ser=prs_prd '
                   'where prs_cancel="N" '
                   'group by prd_name order by prd_name')

            cursor.execute(req)

            l_sup = cursor.fetchall()

            # count use not canceled
            req = ('select prd_name, sum(pru_nb_pack * prd_nb_by_pack) as nb_use '
                   'from product_use '
                   'inner join product_supply on pru_prs=prs_ser '
                   'inner join product_details on prd_ser=prs_prd '
                   'where prs_cancel="N" and pru_cancel="N" '
                   'group by prd_name order by prd_name')

            cursor.execute(req)

            l_use = cursor.fetchall()

            for sup in l_sup:
                for use in l_use:
                    if sup['prd_name'] == use['prd_name']:
                        nb_stock = sup['nb_sup'] - use['nb_use']

                        if nb_stock > 0 and nb_stock <= sup['prd_safe_limit']:
                            res['value'] += 1

        # Number of product at 0 in stock
        elif key == 'NB_PRODUCT_OUT_OF_STOCK':
            res = {}
            res['value'] = 0

            # count supply not canceled
            req = ('select prd_name, prd_safe_limit, sum(prs_nb_pack * prd_nb_by_pack) as nb_sup '
                   'from product_supply '
                   'inner join product_details on prd_ser=prs_prd '
                   'where prs_cancel="N" '
                   'group by prd_name order by prd_name')

            cursor.execute(req)

            l_sup = cursor.fetchall()

            # count use not canceled
            req = ('select prd_name, sum(pru_nb_pack * prd_nb_by_pack) as nb_use '
                   'from product_use '
                   'inner join product_supply on pru_prs=prs_ser '
                   'inner join product_details on prd_ser=prs_prd '
                   'where prs_cancel="N" and pru_cancel="N" '
                   'group by prd_name order by prd_name')

            cursor.execute(req)

            l_use = cursor.fetchall()

            for sup in l_sup:
                for use in l_use:
                    if sup['prd_name'] == use['prd_name']:
                        nb_stock = sup['nb_sup'] - use['nb_use']

                        if nb_stock <= 0:
                            res['value'] += 1

        # Number of opened non-conformity
        elif key == 'NB_OPEN_NON_CONFORMITY':
            req = ('select count(*) as value '
                   'from sigl_non_conformite_data '
                   'where cloture_date = "0000-00-00"')

            cursor.execute(req)

            res = cursor.fetchone()

        # Number of non-conformity on a period
        elif key == 'NB_NON_CONFORMITY':
            req = ('select count(*) as value '
                   'from sigl_non_conformite_data '
                   'where (sys_creation_date between %s and %s)')

            cursor.execute(req, (date_beg, date_end))

            res = cursor.fetchone()

        # Number of internal quality control
        elif key == 'NB_INTERNAL_QUALITY_CONTROL':
            req = ('select count(*) as value '
                   'from control_quality '
                   'where ctq_type_ctrl = "INT"')

            cursor.execute(req)

            res = cursor.fetchone()

        # Number of internal quality control on a period
        elif key == 'NB_INTERNAL_QUALITY_RESULT':
            req = ('select count(*) as value '
                   'from control_internal '
                   'where (cti_date between %s and %s)')

            cursor.execute(req, (date_beg, date_end))

            res = cursor.fetchone()

        # Number of external quality control
        elif key == 'NB_EXTERNAL_QUALITY_CONTROL':
            req = ('select count(*) as value '
                   'from control_quality '
                   'where ctq_type_ctrl = "EXT"')

            cursor.execute(req)

            res = cursor.fetchone()

        # Number of meeting on a period
        elif key == 'NB_MEETING':
            req = ('select count(*) as value '
                   'from sigl_reunion_data '
                   'where (sys_creation_date between %s and %s)')

            cursor.execute(req, (date_beg, date_end))

            res = cursor.fetchone()

        else:
            Export.log.info(Logs.fileline() + ' : getStatDHIS2 ERROR wrong filter_row = ' + str(key))
            res = 'WRONG FILTER'

        return res

    @staticmethod
    def getListOutsourcing(date_beg, date_end, rec_type='A', lite_filter='A'):
        cursor = DB.cursor()

        sql = (
            'select pat.code, pat.code_patient, rec.num_dos_an, rec.rec_date_receipt as date_rec, '
            'ref.code as ana_code, ref.nom as ana_name, rec.rec_lite '
            'from sigl_02_data as rec '
            'inner join sigl_03_data as pat on pat.id_data=rec.id_patient '
            'inner join sigl_04_data as req on req.id_dos=rec.id_data '
            'inner join sigl_05_data as ref on ref.id_data=req.ref_analyse '
            'where (rec.rec_date_receipt between %s and %s) '
            'and rec.statut > 181 and req.req_outsourced="Y"'
        )
        params = [date_beg, date_end]

        # Optional filter by record type
        if rec_type and rec_type.upper() != 'A':
            type_map = {'E': 183, 'I': 184}
            tval = type_map.get(rec_type)
            if tval is not None:
                sql += ' and rec.type = %s'
                params.append(tval)

        # LabBook Lite 3-state filter:
        #  - 'A' (All): no filter
        #  - 'N' (Exclude Lite): rec.rec_lite = 0
        #  - 'Y' (Only Lite):    rec.rec_lite > 0
        lf = (lite_filter or 'A').upper()
        if lf == 'N':
            sql += LITE_EXCLUDE_CLAUSE
        elif lf == 'Y':
            sql += LITE_ONLY_CLAUSE

        cursor.execute(sql, tuple(params))
        return cursor.fetchall()

    @staticmethod
    def getListEEQ(date_beg, date_end):
        cursor = DB.cursor()

        sql = (
            'select '
            '  ctq.ctq_name, '
            '  ctq.ctq_date, '
            '  cte.cte_organizer, '
            '  cte.cte_date, '
            '  cte.cte_conform, '
            '  cte.cte_comment '
            'from control_quality as ctq '
            'inner join control_external as cte on cte.cte_ctq = ctq.ctq_ser '
            'where ctq.ctq_type_ctrl = "EXT" '
            '  and (cte.cte_date between %s and %s) '
            'order by cte.cte_date, ctq.ctq_name'
        )
        params = [date_beg, date_end]

        cursor.execute(sql, tuple(params))
        return cursor.fetchall()

    @staticmethod
    def getListEqpFailure(date_beg, date_end):
        cursor = DB.cursor()

        sql = (
            'select '
            '  eqp.nom as eqp_name, '
            '  eqp.nom_fabriquant as eqp_manufacturer, '
            '  coalesce(fsup_evt.fournisseur_nom, fsup_eqp.fournisseur_nom) as supplier_name, '
            '  eqp.no_inventaire as eqp_invent_num, '
            '  eqf.eqf_date, '
            '  eqf.eqf_comm '
            'from eqp_failure as eqf '
            'inner join sigl_equipement_data as eqp on eqp.id_data = eqf.eqf_eqp '
            'left join sigl_fournisseurs_data as fsup_eqp on fsup_eqp.id_data = eqp.fournisseur_id '
            'left join sigl_fournisseurs_data as fsup_evt on fsup_evt.id_data = eqf.eqf_supplier '
            'where (eqf.eqf_date between %s and %s) '
            'order by eqf.eqf_date, eqp.nom'
        )
        params = [date_beg, date_end]

        cursor.execute(sql, tuple(params))
        return cursor.fetchall()

    @staticmethod
    def getListStockStatus(date_beg, date_end):
        cursor = DB.cursor()

        # Load setting (warning in days)
        cursor.execute('select sos_expir_warning from stock_setting order by sos_ser desc limit 1')
        st = cursor.fetchone() or {}
        warn_days = int(st.get('sos_expir_warning', 14))

        # per product: total supplied, total used, earliest non-empty expiry date
        sql = (
            'select '
            '  p.prd_ser, '
            '  p.prd_name, '
            '  p.prd_expir_oblig, '
            '  p.prd_safe_limit, '
            '  s.nb_sup, '
            '  coalesce(u.nb_use, 0) as nb_use, '
            '  me.min_expir_date '
            'from ( '
            '   select ps.prs_prd as prd_ser, sum(ps.prs_nb_pack * pd.prd_nb_by_pack) as nb_sup '
            '   from product_supply ps '
            '   join product_details pd on pd.prd_ser = ps.prs_prd '
            '   where ps.prs_cancel = "N" '
            '   group by ps.prs_prd '
            ') s '
            'join product_details p on p.prd_ser = s.prd_ser '
            'left join ( '
            '   select ps.prs_prd as prd_ser, sum(u.pru_nb_pack * pd2.prd_nb_by_pack) as nb_use '
            '   from product_use u '
            '   join product_supply ps on ps.prs_ser = u.pru_prs '
            '   join product_details pd2 on pd2.prd_ser = ps.prs_prd '
            '   where ps.prs_cancel = "N" and u.pru_cancel = "N" '
            '   group by ps.prs_prd '
            ') u on u.prd_ser = p.prd_ser '
            'left join ( '
            '   select prs_prd as prd_ser, min(prs_expir_date) as min_expir_date '
            '   from product_supply '
            '   where prs_cancel = "N" and prs_empty = "N" and prs_expir_date is not null '
            '   group by prs_prd '
            ') me on me.prd_ser = p.prd_ser '
            'order by p.prd_name'
        )
        cursor.execute(sql)
        rows = cursor.fetchall()

        # Build one row per product with combined statuses
        now = datetime.now()

        out = []
        for r in rows or []:
            prd_name   = r['prd_name']
            expir_obl  = (r['prd_expir_oblig'] or 'Y') == 'Y'
            safe_limit = int(r['prd_safe_limit'] or 0)
            nb_sup     = int(r['nb_sup'] or 0)
            nb_use     = int(r['nb_use'] or 0)
            qty_stock  = nb_sup - nb_use
            next_exp   = r['min_expir_date']

            # Quantity status
            if qty_stock <= 0:
                qty_status = 'Out of stock'
            elif qty_stock <= safe_limit:
                qty_status = f'Warning {qty_stock}'
            else:
                qty_status = ''

            # Expiration status
            if expir_obl and next_exp:
                days_to_exp = (next_exp - now).days
                date_label = next_exp.strftime("%Y-%m-%d")
                if days_to_exp <= 0:
                    exp_status = f'expired {date_label}'
                elif days_to_exp <= warn_days:
                    exp_status = f'warning {date_label}'
                else:
                    exp_status = ''
            else:
                exp_status = ''

            # Only include products that are in at least one of the 4 states
            if exp_status or qty_status:
                out.append({
                    'prd_name': prd_name,
                    'exp_status': exp_status,
                    'qty_status': qty_status,
                })

        return out
