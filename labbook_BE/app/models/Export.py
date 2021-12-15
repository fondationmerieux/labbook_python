# -*- coding:utf-8 -*-
import logging

from app.models.DB import DB
from app.models.Logs import Logs
from app.models.Various import Various


class Export:
    log = logging.getLogger('log_db')

    @staticmethod
    def getDataWhonet(date_beg, date_end):
        cursor = DB.cursor()

        l_res = []
        l_tmp = []

        # Records list between two date
        req = ('select rec.id_data as id_rec, date_hosp, service_interne, num_lit, dico.label as rec_type, id_patient, '
               'ifnull(dict_med.label, "") as med_spe, num_dos_an '
               'from sigl_02_data as rec '
               'inner join sigl_dico_data as dico on rec.type=dico.id_data and dico.dico_name = "type_dossier" '
               'left join sigl_08_data as med on med.id_data=rec.med_prescripteur '
               'left join sigl_dico_data as dict_med on dict_med.id_data=med.specialite '
               'where statut=256 and date_dos >= %s and date_dos <= %s '
               'order by rec.id_data asc')

        cursor.execute(req, (date_beg, date_end,))

        l_rec = cursor.fetchall()

        # Export.log.info(Logs.fileline() + ' : l_rec=' + str(l_rec))

        for rec in l_rec:
            # check this list for whonet analyzes
            req = ('select ana.id_data as id_ana, req.id_data as id_req, code as ana_code, nom as ana_name '
                   'from sigl_04_data as req '
                   'left join sigl_05_data as ana on req.ref_analyse=ana.id_data '
                   'where ana.famille=18 and ana.ana_whonet=4 and req.id_dos=%s')

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
                    # add method result on the same line
                    elif res_var['libelle'].startswith('Diam. inhibition ') or res_var['libelle'].startswith('CMI '):
                        res['method_value'] = res_var['valeur']
                        l_res.append(res)
                    # in case of something else than antiobic and method result
                    else:
                        res = ana.copy()
                        res.update(res_var)
                        l_res.append(res)

        # Export.log.info(Logs.fileline() + ' : l_res=' + str(l_res))

        # get products details with list of analyzes
        id_rec_p = 0

        for res in l_res:
            if id_rec_p != res['id_rec']:
                req = ('select id_dos, date_prel, dico.label as type_prod, commentaire as comment, prod.code '
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
                        res['spec_date'] = prod['date_prel']
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
