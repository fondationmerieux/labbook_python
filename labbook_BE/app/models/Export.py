# -*- coding:utf-8 -*-
import logging
import mysql.connector

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
        req = 'select rec.id_data as id_rec, date_hosp, service_interne, dico.label as rec_type, id_patient '\
              'from sigl_02_data as rec '\
              'inner join sigl_dico_data as dico on rec.type=dico.id_data and dico.dico_name = "type_dossier" '\
              'where statut=256 and date_dos >= %s and date_dos <= %s '\
              'order by rec.id_data asc'

        cursor.execute(req, (date_beg, date_end,))

        l_rec = cursor.fetchall()

        for rec in l_rec:
            # check this list for whonet analyzes
            req = 'select ana.id_data as id_ana, req.id_data as id_req, code as ana_code, nom as ana_name '\
                  'from sigl_04_data as req '\
                  'left join sigl_05_data as ana on req.ref_analyse=ana.id_data '\
                  'where ana.famille=18 and ana.commentaire like "%[WHONET]%" and req.id_dos=%s' 

            cursor.execute(req, (rec['id_rec'],))

            l_ana = cursor.fetchall()

            if l_ana:

                for ana in l_ana:
                    res = rec.copy()
                    res.update(ana)
                    l_tmp.append(res)

        # get results
        for ana in l_tmp:
            req = 'select res.id_data as id_res, res.valeur, var.libelle, var.type_resultat as type_res '\
                  'from sigl_09_data as res '\
                  'inner join sigl_07_data as var on var.id_data = res.ref_variable '\
                  'inner join sigl_05_07_data as pos on var.id_data = pos.id_refvariable and pos.id_refanalyse=%s '\
                  'inner join sigl_10_data as vld on vld.id_resultat = res.id_data '\
                  'where res.id_analyse=%s and vld.type_validation=252 and vld.motif_annulation is NULL '\
                  'and res.valeur is not NULL and res.valeur != "" and res.valeur != 1013 '\
                  'order by pos.position asc'

            cursor.execute(req, (ana['id_ana'], ana['id_req'],))

            l_var = cursor.fetchall()

            if l_var:
                for res_var in l_var:
                    # find label for res value
                    if res_var['type_res'] == 600 or res_var['type_res'] == 1134:
                        res_label = Various.getDicoById(res_var['valeur'])
                        res_var['valeur'] = res_label['label']

                    res = ana.copy()
                    res.update(res_var)
                    l_res.append(res)

        # patient details
        for res in l_res:
            req = 'select pat.code as pat_code, pat.nom as pat_name, pat.prenom as pat_fname, ddn, age, dico.label as sex '\
                  'from sigl_03_data as pat '\
                  'inner join sigl_dico_data as dico on pat.sexe=dico.id_data and dico.dico_name="sexe" '\
                  'where pat.id_data=%s' 

            cursor.execute(req, (res['id_patient'],))

            res.update(cursor.fetchone())

        return l_res
