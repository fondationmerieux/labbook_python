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

        req = ('select id_data, id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, '
               'date, organisateur_id as id_promoter, type_reu as type, cr as report '
               'from sigl_reunion_data '
               'order by date desc limit 1')

        cursor.execute(req)

        return cursor.fetchone()

    @staticmethod
    def getNbNonCompliance(period):
        cursor = DB.cursor()

        cond = ''

        if period == 'open':
            cond = ' cloture_date is NULL or cloture_date ="0000-00-00" '
        elif period == 'month':
            cond = ' date > adddate(NOW(), INTERVAL -1 MONTH) '

        # NOTE count with sigl_non_conformite_data too ?
        # Number of non-compliance
        req = ('select count(*) as nb_noncompliance '
               'from sigl_non_conformite_data '
               'where ' + cond)

        cursor.execute(req)

        return cursor.fetchone()

    @staticmethod
    def getConformityList(date_beg, date_end):
        cursor = DB.cursor()

        req = ('select id_data, id_owner, nom as name, date as date_create, impact_patient, '
               'impacts_perso_visit as impact_user, traitement_quand as date_correction, '
               'traitement_action_corrective as correction, cloture_date as close_date '
               'from sigl_non_conformite_data '
               'where (date between %s and %s) order by date')

        cursor.execute(req, (date_beg, date_end,))

        return cursor.fetchall()

    @staticmethod
    def getNonConformity(id_item):
        cursor = DB.cursor()

        req = ('select sigl_non_conformite_data.id_data, sigl_non_conformite_data.nom as name, user_id as reporter_id, '
               'date as date_create, pre_analytique as cat_preana, '
               'analytique as cat_analy, post_analytique as cat_postana, transmission_resultats as cat_res, rh as cat_hr, '
               'equipements as cat_eqp, reactifs_consommables as cat_consu, locaux_environnement as cat_local, '
               'systemes_informatiques as cat_si, sous_traitance as cat_contract, pre_analytique_prescription as sub_preana_cat1, '
               'pre_analytique_oubli_examen_error as sub_preana_cat2, pre_analytique_dossier_pat as sub_preana_cat3, '
               'pre_analytique_prel as sub_preana_cat4, pre_analytique_heure_prel as sub1_sub_preana_cat4, '
               'pre_analytique_vol_prel as sub2_sub_preana_cat4, pre_analytique_ident_prel as sub3_sub_preana_cat4, '
               'pre_analytique_renseignement_clin as sub_preana_cat5, pre_analytique_transport_echant as sub_preana_cat6, '
               'pre_analytique_respect_proc as sub_preana_cat7, pre_analytique_urgence as sub_preana_cat8, '
               'pre_analytique_tracabilite as sub_preana_cat9, pre_analytique_autre_content as sub_preana_cat10, '
               'analytique_conservation as sub_analy_cat1, analytique_urgence as sub_analy_cat2, '
               'analytique_centrifugation as sub_analy_cat3, analytique_aliquotage as sub_analy_cat4, '
               'analytique_ctrl_qualite_int as sub_analy_cat5, analytique_ctrl_qualite_ext as sub_analy_cat6, '
               'analytique_tracabilite as sub_analy_cat7, analytique_procedures as sub_analy_cat8, '
               'analytique_absence_resultat as sub_analy_cat9, analytique_critere_de_repasse as sub_analy_cat10, '
               'analytique_autre_content as sub_analy_cat11, post_analytique_dos_non_valide as sub_postana_cat1, '
               'post_analytique_validation_partiel as sub_postana_cat2, post_analytique_res_errone as sub_postana_cat3, '
               'post_analytique_absence_resultat as sub_postana_cat4, post_analytique_erreur_saisie as sub_postana_cat5, '
               'post_analytique_interpretation as sub_postana_cat6, post_analytique_presta_conseil as sub_postana_cat7, '
               'post_analytique_conservation as sub_postana_cat8, post_analytique_procedures as sub_postana_cat9, '
               'post_analytique_autre_content as sub_postana_cat10, transmission_resultats_non_transmis_patient as sub_res_cat1, '
               'transmission_resultats_non_transmis_presc as sub_res_cat2, transmission_resultats_acces_result as sub_res_cat3, '
               'transmission_resultats_date_rendu as sub_res_cat4, transmission_resultats_delai_non_resp as sub_res_cat5, '
               'transmission_resultats_procedure as sub_res_cat6, transmission_resultats_autre_content as sub_res_cat7, '
               'rh_procedures as sub_hr_cat1, rh_absence as sub_hr_cat2, rh_habilitation as sub_hr_cat3, '
               'rh_aes_hygiene_secu as sub_hr_cat4, rh_autre_contenu as sub_hr_cat5, equipements_etalonnage as sub_eqp_cat1, '
               'equipements_calibration as sub_eqp_cat2, equipements_alarme as sub_eqp_cat3, equipements_panne as sub_eqp_cat4, '
               'equipements_procedures as sub_eqp_cat5, equipements_autre_content as sub_eqp_cat6, equipements_autre as equipment_id, '
               'reactifs_consommables_reception as sub_consu_cat1, reactifs_consommables_delais as sub_consu_cat2, '
               'reactifs_consommables_reactifs as sub_consu_cat3, reactifs_consommables_rupture as sub_consu_cat4, '
               'reactifs_consommables_destockage as sub_consu_cat5, reactifs_consommables_autre_content as sub_consu_cat6, '
               'reactifs_consommables_autre as supplier_id, locaux_environnement_nettoyage as sub_local_cat1, '
               'locaux_environnement_entretien as sub_local_cat2, locaux_environnement_coupure_elec as sub_local_cat3, '
               'locaux_environnement_coupure_eau as sub_local_cat4, locaux_environnement_dechets as sub_local_cat5, '
               'locaux_environnement_autre_content as sub_local_cat6, systemes_informatiques_absence as sub_si_cat1, '
               'systemes_informatiques_erreur as sub_si_cat2, systemes_informatiques_panne_reseau as sub_si_cat3, '
               'systemes_informatiques_panne_systeme as sub_si_cat4, systemes_informatiques_panne_materiel as sub_si_cat5, '
               'systemes_informatiques_autre_content as sub_si_cat6, sous_traitance_delai as sub_contract_cat1, '
               'sous_traitance_erreur as sub_contract_cat2, sous_traitance_conservation as sub_contract_cat3, '
               'sous_traitance_facturation as sub_contract_cat4, sous_traitance_autre_content as sub_contract_cat5, '
               'autre_contenu as cat_other, reclamations_clients_contenu as cat_client, relation_dos_client as about_pat_rec, '
               'no_dos as pat_rec_num, description, impact_patient as impact_pat, impacts_perso_visit as impact_user, '
               'traitement_qui_id as followed_id, traitement_quoi as flwd_what, traitement_quand as flwd_when, '
               'traitement_action_corrective as impl_action, traitement_action_description as flwd_descr_action, '
               'traitement_date_real as flwd_action_date, traitement_correctif_responsable_id as incharge_id, '
               'cloture_commentaire as close_comment, cloture_validateur_id as validate_id, cloture_date as close_date, '
               'TRIM(CONCAT(u1.lastname," ",u1.firstname," - ",u1.username)) as reporter, '
               'TRIM(CONCAT(u2.lastname," ",u2.firstname," - ",u2.username)) as followed, '
               'TRIM(CONCAT(u3.lastname," ",u3.firstname," - ",u3.username)) as incharge, '
               'TRIM(CONCAT(u4.lastname," ",u4.firstname," - ",u4.username)) as validate, '
               'eqp.nom as equipment, sup.fournisseur_nom as supplier '
               'from sigl_non_conformite_data '
               'left join sigl_user_data as u1 on u1.id_data=user_id '
               'left join sigl_user_data as u2 on u2.id_data=traitement_qui_id '
               'left join sigl_user_data as u3 on u3.id_data=traitement_correctif_responsable_id '
               'left join sigl_user_data as u4 on u4.id_data=cloture_validateur_id '
               'left join sigl_equipement_data as eqp on eqp.id_data=equipements_autre '
               'left join sigl_fournisseurs_data as sup on sup.id_data=reactifs_consommables_autre '
               'where sigl_non_conformite_data.id_data=%s')

        cursor.execute(req, (id_item,))

        return cursor.fetchone()

    @staticmethod
    def insertNonConformity(**params):
        try:
            cursor = DB.cursor()

            # useless :
            # pre_analytique_autre, analytique_autre, post_analytique_autre, transmission_resultats_autre, rh_autre
            # reactifs_consommables_tracabilite, locaux_environnement_autre, systemes_informatiques_autre
            # sous_traitance_autre, autre

            # reactifs_consommables_autre == supplier
            # equipements_autre == equipment

            cursor.execute('insert into sigl_non_conformite_data '
                           '(id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, nom, user_id, date, '
                            'pre_analytique, analytique, post_analytique, transmission_resultats, rh, equipements, reactifs_consommables, '
                            'locaux_environnement, systemes_informatiques, sous_traitance, '
                            'pre_analytique_prescription, pre_analytique_oubli_examen_error, pre_analytique_dossier_pat, '
                            'pre_analytique_prel, pre_analytique_heure_prel, pre_analytique_vol_prel, pre_analytique_ident_prel, '
                            'pre_analytique_renseignement_clin, pre_analytique_transport_echant, pre_analytique_respect_proc, '
                            'pre_analytique_urgence, pre_analytique_tracabilite, pre_analytique_autre_content, analytique_conservation, '
                            'analytique_urgence, analytique_centrifugation, analytique_aliquotage, analytique_ctrl_qualite_int, '
                            'analytique_ctrl_qualite_ext, analytique_tracabilite, analytique_procedures, analytique_absence_resultat, '
                            'analytique_critere_de_repasse, analytique_autre_content, post_analytique_dos_non_valide, '
                            'post_analytique_validation_partiel, post_analytique_res_errone, post_analytique_absence_resultat, '
                            'post_analytique_erreur_saisie, post_analytique_interpretation, post_analytique_presta_conseil, '
                            'post_analytique_conservation, post_analytique_procedures, post_analytique_autre_content, '
                            'transmission_resultats_non_transmis_patient, transmission_resultats_non_transmis_presc, '
                            'transmission_resultats_acces_result, transmission_resultats_date_rendu, transmission_resultats_delai_non_resp, '
                            'transmission_resultats_procedure, transmission_resultats_autre_content, rh_procedures, rh_absence, '
                            'rh_habilitation, rh_aes_hygiene_secu, rh_autre_contenu, equipements_etalonnage, equipements_calibration, '
                            'equipements_alarme, equipements_panne, equipements_procedures, equipements_autre_content, equipements_autre, '
                            'reactifs_consommables_reception, reactifs_consommables_delais, reactifs_consommables_reactifs, '
                            'reactifs_consommables_rupture, reactifs_consommables_destockage, reactifs_consommables_autre_content, '
                            'reactifs_consommables_autre, locaux_environnement_nettoyage, locaux_environnement_entretien, '
                            'locaux_environnement_coupure_elec, locaux_environnement_coupure_eau, '
                            'locaux_environnement_dechets, locaux_environnement_autre_content, systemes_informatiques_absence, '
                            'systemes_informatiques_erreur, systemes_informatiques_panne_reseau, systemes_informatiques_panne_systeme, '
                            'systemes_informatiques_panne_materiel, systemes_informatiques_autre_content, sous_traitance_delai, '
                            'sous_traitance_erreur, sous_traitance_conservation, sous_traitance_facturation, sous_traitance_autre_content, '
                            'autre_contenu, reclamations_clients_contenu, relation_dos_client, no_dos, description, impact_patient, '
                            'impacts_perso_visit, traitement_qui_id, traitement_quoi, traitement_quand, traitement_action_corrective, '
                            'traitement_action_description, traitement_date_real, traitement_correctif_responsable_id, cloture_commentaire, '
                            'cloture_validateur_id, cloture_date) '
                            'values '
                            '(%(id_owner)s, NOW(), NOW(), %(id_owner)s, %(name)s, %(reporter)s, %(report_date)s, '
                            '%(cat_preana)s, %(cat_analy)s, %(cat_postana)s, %(cat_res)s, %(cat_hr)s, %(cat_eqp)s, '
                            '%(cat_consu)s, %(cat_local)s, %(cat_si)s, %(cat_contract)s, '
                            '%(sub_preana_cat1)s, %(sub_preana_cat2)s, %(sub_preana_cat3)s, %(sub_preana_cat4)s, %(sub1_sub_preana_cat4)s, '
                            '%(sub2_sub_preana_cat4)s, %(sub3_sub_preana_cat4)s, %(sub_preana_cat5)s, %(sub_preana_cat6)s, '
                            '%(sub_preana_cat7)s, %(sub_preana_cat8)s, %(sub_preana_cat9)s, %(sub_preana_cat10)s, %(sub_analy_cat1)s,'
                            '%(sub_analy_cat2)s, %(sub_analy_cat3)s, %(sub_analy_cat4)s, %(sub_analy_cat5)s, %(sub_analy_cat6)s, '
                            '%(sub_analy_cat7)s, %(sub_analy_cat8)s, %(sub_analy_cat9)s, %(sub_analy_cat10)s, %(sub_analy_cat11)s, '
                            '%(sub_postana_cat1)s, %(sub_postana_cat2)s, %(sub_postana_cat3)s, %(sub_postana_cat4)s, %(sub_postana_cat5)s, '
                            '%(sub_postana_cat6)s, %(sub_postana_cat7)s, %(sub_postana_cat8)s, %(sub_postana_cat9)s, %(sub_postana_cat10)s, '
                            '%(sub_res_cat1)s, %(sub_res_cat2)s, %(sub_res_cat3)s, %(sub_res_cat4)s, %(sub_res_cat5)s, '
                            '%(sub_res_cat6)s, %(sub_res_cat7)s, %(sub_hr_cat1)s, %(sub_hr_cat2)s, %(sub_hr_cat3)s, '
                            '%(sub_hr_cat4)s, %(sub_hr_cat5)s, %(sub_eqp_cat1)s, %(sub_eqp_cat2)s, %(sub_eqp_cat3)s, '
                            '%(sub_eqp_cat4)s, %(sub_eqp_cat5)s, %(sub_eqp_cat6)s, %(equipment)s, %(sub_consu_cat1)s, %(sub_consu_cat2)s, '
                            '%(sub_consu_cat3)s, %(sub_consu_cat4)s, %(sub_consu_cat5)s, %(sub_consu_cat6)s, %(supplier)s, %(sub_local_cat1)s, '
                            '%(sub_local_cat2)s, %(sub_local_cat3)s, %(sub_local_cat4)s, %(sub_local_cat5)s, %(sub_local_cat6)s, '
                            '%(sub_si_cat1)s, %(sub_si_cat2)s, %(sub_si_cat3)s, %(sub_si_cat4)s, %(sub_si_cat5)s,  %(sub_si_cat6)s, '
                            '%(sub_contract_cat1)s, %(sub_contract_cat2)s, %(sub_contract_cat3)s, %(sub_contract_cat4)s, %(sub_contract_cat5)s, '
                            '%(cat_other)s, %(cat_client)s, %(about_pat_rec)s, %(pat_rec_num)s, %(description)s, %(impact_pat)s, %(impact_user)s, %(followed)s, '
                            '%(flwd_what)s, %(flwd_when)s, %(impl_action)s, %(flwd_descr_action)s, %(flwd_action_date)s, '
                            '%(incharge)s, %(close_comment)s, %(validate)s, %(close_date)s)', params)

            Quality.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def updateNonConformity(**params):
        try:
            cursor = DB.cursor()

            req = ('update sigl_non_conformite_data set id_owner=%(id_owner)s,'
                   'nom=%(name)s, user_id=%(reporter)s, date=%(report_date)s, pre_analytique=%(cat_preana)s, '
                   'analytique=%(cat_analy)s, post_analytique=%(cat_postana)s, transmission_resultats=%(cat_res)s, '
                   'rh=%(cat_hr)s, equipements=%(cat_eqp)s, reactifs_consommables=%(cat_consu)s, '
                   'locaux_environnement=%(cat_local)s, systemes_informatiques=%(cat_si)s, '
                   'sous_traitance=%(cat_contract)s, pre_analytique_prescription=%(sub_preana_cat1)s, '
                   'pre_analytique_oubli_examen_error=%(sub_preana_cat2)s, pre_analytique_dossier_pat=%(sub_preana_cat3)s, '
                   'pre_analytique_prel=%(sub_preana_cat4)s, pre_analytique_heure_prel=%(sub1_sub_preana_cat4)s, '
                   'pre_analytique_vol_prel=%(sub2_sub_preana_cat4)s, pre_analytique_ident_prel=%(sub3_sub_preana_cat4)s, '
                   'pre_analytique_renseignement_clin=%(sub_preana_cat5)s, '
                   'pre_analytique_transport_echant=%(sub_preana_cat6)s, pre_analytique_respect_proc=%(sub_preana_cat7)s, '
                   'pre_analytique_urgence=%(sub_preana_cat8)s, pre_analytique_tracabilite=%(sub_preana_cat9)s, '
                   'pre_analytique_autre_content=%(sub_preana_cat10)s, analytique_conservation=%(sub_analy_cat1)s, '
                   'analytique_urgence=%(sub_analy_cat2)s, analytique_centrifugation=%(sub_analy_cat3)s, '
                   'analytique_aliquotage=%(sub_analy_cat4)s, analytique_ctrl_qualite_int=%(sub_analy_cat5)s, '
                   'analytique_ctrl_qualite_ext=%(sub_analy_cat6)s, analytique_tracabilite=%(sub_analy_cat7)s, '
                   'analytique_procedures=%(sub_analy_cat8)s, analytique_absence_resultat=%(sub_analy_cat9)s, '
                   'analytique_critere_de_repasse=%(sub_analy_cat10)s, analytique_autre_content=%(sub_analy_cat11)s, '
                   'post_analytique_dos_non_valide=%(sub_postana_cat1)s, '
                   'post_analytique_validation_partiel=%(sub_postana_cat2)s, '
                   'post_analytique_res_errone=%(sub_postana_cat3)s, '
                   'post_analytique_absence_resultat=%(sub_postana_cat4)s, '
                   'post_analytique_erreur_saisie=%(sub_postana_cat5)s, '
                   'post_analytique_interpretation=%(sub_postana_cat6)s, '
                   'post_analytique_presta_conseil=%(sub_postana_cat7)s, '
                   'post_analytique_conservation=%(sub_postana_cat8)s, '
                   'post_analytique_procedures=%(sub_postana_cat9)s, '
                   'post_analytique_autre_content=%(sub_postana_cat10)s, '
                   'transmission_resultats_non_transmis_patient=%(sub_res_cat1)s, '
                   'transmission_resultats_non_transmis_presc=%(sub_res_cat2)s, '
                   'transmission_resultats_acces_result=%(sub_res_cat3)s, '
                   'transmission_resultats_date_rendu=%(sub_res_cat4)s, '
                   'transmission_resultats_delai_non_resp=%(sub_res_cat5)s, '
                   'transmission_resultats_procedure=%(sub_res_cat6)s, '
                   'transmission_resultats_autre_content=%(sub_res_cat7)s, rh_procedures=%(sub_hr_cat1)s, '
                   'rh_absence=%(sub_hr_cat2)s, rh_habilitation=%(sub_hr_cat3)s, rh_aes_hygiene_secu=%(sub_hr_cat4)s, '
                   'rh_autre_contenu=%(sub_hr_cat5)s, equipements_etalonnage=%(sub_eqp_cat1)s, '
                   'equipements_calibration=%(sub_eqp_cat2)s, equipements_alarme=%(sub_eqp_cat3)s, '
                   'equipements_panne=%(sub_eqp_cat4)s, equipements_procedures=%(sub_eqp_cat5)s, '
                   'equipements_autre_content=%(sub_eqp_cat6)s, equipements_autre=%(equipment)s, '
                   'reactifs_consommables_reception=%(sub_consu_cat1)s, reactifs_consommables_delais=%(sub_consu_cat2)s, '
                   'reactifs_consommables_reactifs=%(sub_consu_cat3)s, reactifs_consommables_rupture=%(sub_consu_cat4)s, '
                   'reactifs_consommables_destockage=%(sub_consu_cat5)s, '
                   'reactifs_consommables_autre_content=%(sub_consu_cat6)s, reactifs_consommables_autre=%(supplier)s, '
                   'locaux_environnement_nettoyage=%(sub_local_cat1)s, locaux_environnement_entretien=%(sub_local_cat2)s, '
                   'locaux_environnement_coupure_elec=%(sub_local_cat3)s, '
                   'locaux_environnement_coupure_eau=%(sub_local_cat4)s, locaux_environnement_dechets=%(sub_local_cat5)s, '
                   'locaux_environnement_autre_content=%(sub_local_cat6)s, '
                   'systemes_informatiques_absence=%(sub_si_cat1)s, systemes_informatiques_erreur=%(sub_si_cat2)s, '
                   'systemes_informatiques_panne_reseau=%(sub_si_cat3)s, '
                   'systemes_informatiques_panne_systeme=%(sub_si_cat4)s, '
                   'systemes_informatiques_panne_materiel=%(sub_si_cat5)s, '
                   'systemes_informatiques_autre_content=%(sub_si_cat6)s, '
                   'sous_traitance_delai=%(sub_contract_cat1)s, sous_traitance_erreur=%(sub_contract_cat2)s, '
                   'sous_traitance_conservation=%(sub_contract_cat3)s, sous_traitance_facturation=%(sub_contract_cat4)s, '
                   'sous_traitance_autre_content=%(sub_contract_cat5)s, autre_contenu=%(cat_other)s, '
                   'reclamations_clients_contenu=%(cat_client)s, relation_dos_client=%(about_pat_rec)s, '
                   'no_dos=%(pat_rec_num)s, description=%(description)s, impact_patient=%(impact_pat)s, '
                   'impacts_perso_visit=%(impact_user)s, traitement_qui_id=%(followed)s, traitement_quoi=%(flwd_what)s, '
                   'traitement_quand=%(flwd_when)s, traitement_action_corrective=%(impl_action)s, '
                   'traitement_action_description=%(flwd_descr_action)s, traitement_date_real=%(flwd_action_date)s, '
                   'traitement_correctif_responsable_id=%(incharge)s, cloture_commentaire=%(close_comment)s, '
                   'cloture_validateur_id=%(validate)s, cloture_date=%(close_date)s '
                   'where id_data=%(id_data)s')

            cursor.execute(req, params)

            Quality.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def deleteNonConformity(id_item):
        try:
            cursor = DB.cursor()

            cursor.execute('delete from sigl_non_conformite_data '
                           'where id_data=%s', (id_item,))

            Quality.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getControlList(type_ctrl):
        cursor = DB.cursor()

        req = ('select ctq_ser as id_item, ctq_name, ctq_type_ctrl, ctq_type_val, ctq_eqp, eqp.nom as eqp_name '
               'from control_quality '
               'inner join sigl_equipement_data as eqp on eqp.id_data=ctq_eqp '
               'where ctq_type_ctrl=%s order by ctq_name')

        cursor.execute(req, (type_ctrl,))

        return cursor.fetchall()

    @staticmethod
    def getControlDet(id_ctrl):
        cursor = DB.cursor()

        req = ('select ctq_ser as id_item, ctq_name, ctq_type_val, ctq_eqp, eqp.nom as eqp_name '
               'from control_quality '
               'inner join sigl_equipement_data as eqp on eqp.id_data=ctq_eqp '
               'where ctq_ser=%s')

        cursor.execute(req, (id_ctrl,))

        return cursor.fetchone()

    @staticmethod
    def insertControlDet(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into control_quality '
                           '(ctq_date, ctq_type_ctrl, ctq_type_val, ctq_name, ctq_eqp) '
                            'values (NOW(), %(ctq_type_ctrl)s, %(ctq_type_val)s, %(ctq_name)s, %(ctq_eqp)s)', params)

            Quality.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def updateControlDet(**params):
        try:
            cursor = DB.cursor()

            req = ('update control_quality set ctq_type_ctrl=%(ctq_type_ctrl)s,'
                   'ctq_type_val=%(ctq_type_val)s, ctq_name=%(ctq_name)s, ctq_eqp=%(ctq_eqp)s '
                   'where ctq_ser=%(ctq_ser)s')

            cursor.execute(req, params)

            Quality.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getControlIntResList(id_ctrl):
        cursor = DB.cursor()

        req = ('select cti_ser as id_item, cti_ctq, cti_date, cti_type, cti_target, cti_result, cti_comment '
               'from control_internal '
               'where cti_ctq=%s order by cti_date desc')

        cursor.execute(req, (id_ctrl,))

        return cursor.fetchall()

    @staticmethod
    def getControlIntRes(cti_ser):
        cursor = DB.cursor()

        req = ('select cti_ser as id_item, cti_ctq, cti_date, cti_type, cti_target, cti_result, cti_comment '
               'from control_internal '
               'where cti_ser=%s')

        cursor.execute(req, (cti_ser,))

        return cursor.fetchone()

    @staticmethod
    def insertControlIntRes(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into control_internal '
                           '(cti_date, cti_ctq, cti_type, cti_target, cti_result, cti_comment) '
                            'values (%(cti_date)s, %(cti_ctq)s, %(cti_type)s, %(cti_target)s, %(cti_result)s, %(cti_comment)s)', params)

            Quality.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def updateControlIntRes(**params):
        try:
            cursor = DB.cursor()

            req = ('update control_internal set cti_date=%(cti_date)s, cti_ctq=%(cti_ctq)s, cti_type=%(cti_type)s, '
                   'cti_target=%(cti_target)s, cti_result=%(cti_result)s, cti_comment=%(cti_comment)s '
                   'where cti_ser=%(cti_ser)s')

            cursor.execute(req, params)

            Quality.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getControlExtResList(id_ctrl):
        cursor = DB.cursor()

        req = ('select cte_ser as id_item, cte_ctq, cte_date, cte_type, cte_organizer, cte_contact, '
               'cte_conform, cte_comment '
               'from control_external '
               'where cte_ctq=%s order by cte_date desc')

        cursor.execute(req, (id_ctrl,))

        return cursor.fetchall()

    @staticmethod
    def getControlExtRes(cte_ser):
        cursor = DB.cursor()

        req = ('select cte_ser as id_item, cte_ctq, cte_date, cte_type, cte_organizer, cte_contact, '
               'cte_conform, cte_comment '
               'from control_external '
               'where cte_ser=%s')

        cursor.execute(req, (cte_ser,))

        return cursor.fetchone()

    @staticmethod
    def insertControlExtRes(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into control_external '
                           '(cte_date, cte_ctq, cte_type, cte_organizer, cte_contact, cte_conform, cte_comment) '
                            'values (%(cte_date)s, %(cte_ctq)s, %(cte_type)s, %(cte_organizer)s, '
                            '%(cte_contact)s, %(cte_conform)s, %(cte_comment)s)', params)

            Quality.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def updateControlExtRes(**params):
        try:
            cursor = DB.cursor()

            req = ('update control_external set cte_date=%(cte_date)s, cte_ctq=%(cte_ctq)s, cte_type=%(cte_type)s, '
                   'cte_organizer=%(cte_organizer)s, cte_contact=%(cte_contact)s, cte_conform=%(cte_conform)s, '
                   'cte_comment=%(cte_comment)s '
                   'where cte_ser=%(cte_ser)s')

            cursor.execute(req, params)

            Quality.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

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
    def getEquipmentListExport():
        cursor = DB.cursor()

        req = ('select eqp.id_data, date_format(eqp.sys_creation_date, %s) as creation_date, eqp.nom as name, '
               'eqp.nom_fabriquant as maker, eqp.modele as model, eqp.fonction as funct, eqp.localisation as location, '
               'dict.label as section, supp.fournisseur_nom as supplier, eqp.no_serie as serial_number, '
               'eqp.no_inventaire as inventory_number, date_format(eqp.date_achat, %s) as purchase_date, '
               'TRIM(CONCAT(u1.lastname," ",u1.firstname," - ",u1.username)) as incharge, '
               'date_format(eqp.date_reception, %s) as receipt_date, '
               'date_format(eqp.date_mise_en_service, %s) as commissioning_date, '
               'date_format(eqp.date_de_retrait, %s) as withdrawal_date, eqp.eqp_critical, eqp.commentaires as comments '
               'from sigl_equipement_data as eqp '
               'left join sigl_dico_data as dict on dict.id_data=eqp.section '
               'left join sigl_fournisseurs_data as supp on supp.id_data=eqp.fournisseur_id '
               'left join sigl_user_data as u1 on u1.id_data=eqp.responsable_id '
               'order by name asc')

        cursor.execute(req, (Constants.cst_isodate, Constants.cst_isodate, Constants.cst_isodate, Constants.cst_isodate, Constants.cst_isodate))

        return cursor.fetchall()

    @staticmethod
    def getEquipmentSearch(text):
        cursor = DB.cursor()

        l_words = text.split(' ')

        cond = 'nom is not NULL '

        for word in l_words:
            cond = (cond + ' and (nom like "%' + word + '%") ')

        req = ('select nom as field_value, id_data '
               'from sigl_equipement_data '
               'where ' + cond + ' order by field_value asc limit 1000')

        cursor.execute(req)

        return cursor.fetchall()

    @staticmethod
    def getEquipment(id_item):
        cursor = DB.cursor()

        req = ('select eqp.id_data, eqp.nom as name, eqp.nom_fabriquant as maker, eqp.modele as model, '
               'eqp.fonction as funct, eqp.localisation as location, eqp.section, eqp.fournisseur_id as supplier_id, '
               'eqp.no_serie as serial, eqp.no_inventaire as inventory, eqp.responsable_id as incharge_id, '
               'eqp.date_reception as date_receipt, eqp.date_achat as date_buy, eqp_critical, '
               'eqp.date_mise_en_service as date_onduty, eqp.date_de_retrait as date_revoc, eqp.commentaires as comment, '
               'u1.fournisseur_nom as supplier, '
               'TRIM(CONCAT(u2.lastname," ",u2.firstname," - ",u2.username)) as incharge '
               'from sigl_equipement_data as eqp '
               'left join sigl_fournisseurs_data as u1 on u1.id_data=eqp.fournisseur_id '
               'left join sigl_user_data as u2 on u2.id_data=eqp.responsable_id '
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
                           'responsable_id, date_reception, date_achat, '
                           'date_mise_en_service, date_de_retrait, eqp_critical, commentaires) '
                           'values '
                           '(%(id_owner)s, NOW(), NOW(), %(id_owner)s, %(name)s, %(maker)s, %(model)s, '
                           '%(funct)s, %(location)s, %(section)s, %(supplier)s, %(serial)s, %(inventory)s, '
                           '%(incharge)s, %(date_receipt)s, %(date_buy)s, '
                           '%(date_onduty)s, %(date_revoc)s, %(critical)s, %(comment)s)', params)

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
                           'responsable_id=%(incharge)s, date_reception=%(date_receipt)s, '
                           'date_achat=%(date_buy)s, date_mise_en_service=%(date_onduty)s, '
                           'date_de_retrait=%(date_revoc)s, eqp_critical=%(critical)s, commentaires=%(comment)s  '
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

            cursor.execute('delete from eqp_document '
                           'where eqd_eqp=%s', (id_item,))

            cursor.execute('delete from sigl_equipement_data '
                           'where id_data=%s', (id_item,))

            Quality.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getEquipmentComm(type_comm, id_eqp):
        cursor = DB.cursor()

        cond_select = ''

        if type_comm == 'DOC':
            cond_select = 'eqp_comm_doc '
        else:
            Quality.log.error(Logs.alert() + 'type_comm unknown : ' + str(type_comm))

        req = ('select ' + cond_select +
               'from sigl_equipement_data '
               'where id_data=%s ')

        cursor.execute(req, (id_eqp,))

        return cursor.fetchone()

    @staticmethod
    def updateEquipmentComm(type_comm, id_eqp, comm):
        try:
            cursor = DB.cursor()

            cond_set = ''

            if type_comm == 'DOC':
                cond_set = 'eqp_comm_doc=%s '
            elif type_comm == 'MAIN':
                cond_set = 'eqp_comm_maintenance=%s '

            cursor.execute('update sigl_equipement_data '
                           'set ' + cond_set +
                           'where id_data=%s', (comm, id_eqp))

            Quality.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getEquipmentDoc(type_doc, id_eqp):
        cursor = DB.cursor()

        cond = ''

        if type_doc == 'MANU':
            cond = ('inner join sigl_manuels_data as doc on doc.id_data=eqd_ref '
                    'inner join manual_file as link on link.id_ext=doc.id_data ')
        elif type_doc == 'PROC':
            cond = ('inner join sigl_procedures_data as doc on doc.id_data=eqd_ref '
                    'inner join procedure_file as link on link.id_ext=doc.id_data ')
        else:
            Quality.log.error(Logs.alert() + 'type_doc unknown : ' + str(type_doc))

        req = ('select eqd_ser, doc.titre as title, file.id_data as id_file, file.original_name as name '
               'from eqp_document ' + cond +
               'inner join sigl_file_data as file on file.id_data=link.id_file '
               'where eqd_eqp=%s and eqd_type=%s ')

        cursor.execute(req, (id_eqp, type_doc))

        return cursor.fetchall()

    @staticmethod
    def insertEquipmentDoc(id_user, id_eqp, type, ref):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into eqp_document '
                           '(eqd_date, eqd_user, eqd_eqp, eqd_type, eqd_ref) '
                           'values '
                           '(NOW(), %s, %s, %s, %s)', (id_user, id_eqp, type, ref))

            Quality.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def deleteEquipmentDoc(id_eqd):
        try:
            cursor = DB.cursor()

            cursor.execute('delete from eqp_document '
                           'where eqd_ser=%s', (id_eqd,))

            Quality.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getEqpFailureList(id_eqp):
        cursor = DB.cursor()

        req = ('select eqf_ser, eqf_date, eqf_user, eqf_eqp, eqf_type, eqf_incharge, eqf_supplier, eqf_comm, '
               'sup.fournisseur_nom as supplier, '
               'TRIM(CONCAT(u1.lastname," ",u1.firstname," - ",u1.username)) as incharge '
               'from eqp_failure '
               'left join sigl_user_data as u1 on u1.id_data=eqf_incharge '
               'left join sigl_fournisseurs_data as sup on sup.id_data=eqf_supplier '
               'where eqf_eqp=%s '
               'order by eqf_date desc')

        cursor.execute(req, (id_eqp,))

        return cursor.fetchall()

    @staticmethod
    def insertEqpFailure(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into eqp_failure '
                           '(eqf_date, eqf_user, eqf_eqp, eqf_type, eqf_incharge, eqf_supplier, eqf_comm) '
                           'values '
                           '(%(date)s, %(id_user)s, %(id_eqp)s, %(type)s, %(incharge)s, '
                           '%(supplier)s, %(comm)s)', params)

            Quality.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def deleteEqpFailure(id_item, with_id_eqp=False):
        try:
            cursor = DB.cursor()

            cond  = id_item
            cond2 = 'eqf_ser = %s'

            if with_id_eqp:
                cond  = '(select eqf_ser from eqp_failure where eqf_eqp=%s)'
                cond2 = 'eqf_eqp = %s'

            cursor.execute('delete from sigl_file_data '
                           'where id_data in (select id_file from eqp_failure_file where id_ext in ' + cond + ')', (id_item,))

            cursor.execute('delete from eqp_failure_file '
                           'where id_ext in ' + cond, (id_item,))

            cursor.execute('delete from eqp_failure '
                           'where ' + cond2, (id_item,))

            Quality.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getEqpMetrologyList(id_eqp):
        cursor = DB.cursor()

        req = ('select eqm_ser, eqm_date, eqm_user, eqm_eqp, eqm_supplier, eqm_comm, '
               'sup.fournisseur_nom as supplier '
               'from eqp_metrology '
               'left join sigl_fournisseurs_data as sup on sup.id_data=eqm_supplier '
               'where eqm_eqp=%s '
               'order by eqm_date desc')

        cursor.execute(req, (id_eqp,))

        return cursor.fetchall()

    @staticmethod
    def insertEqpMetrology(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into eqp_metrology '
                           '(eqm_date, eqm_user, eqm_eqp, eqm_supplier, eqm_comm) '
                           'values '
                           '(%(date)s, %(id_user)s, %(id_eqp)s, %(supplier)s, %(comm)s)', params)

            Quality.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def deleteEqpMetrology(id_item, with_id_eqp=False):
        try:
            cursor = DB.cursor()

            cond  = id_item
            cond2 = 'eqm_ser = %s'

            if with_id_eqp:
                cond  = '(select eqm_ser from eqp_metrology where eqm_eqp=%s)'
                cond2 = 'eqm_eqp = %s'

            cursor.execute('delete from sigl_file_data '
                           'where id_data in (select id_file from eqp_calibration_file where id_ext in ' + cond + ')', (id_item,))

            cursor.execute('delete from eqp_calibration_file '
                           'where id_ext in ' + cond, (id_item,))

            cursor.execute('delete from eqp_metrology '
                           'where ' + cond2, (id_item,))

            Quality.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getEquipmentPreventiveList(id_eqp):
        cursor = DB.cursor()

        req = ('select eqs_ser, eqs_date, eqs_user, eqs_eqp, eqs_operator, eqs_comm, '
               'TRIM(CONCAT(u1.lastname," ",u1.firstname," - ",u1.username)) as operator '
               'from eqp_preventive_maintenance '
               'left join sigl_user_data as u1 on u1.id_data=eqs_operator '
               'where eqs_eqp=%s '
               'order by eqs_date desc')

        cursor.execute(req, (id_eqp,))

        return cursor.fetchall()

    @staticmethod
    def insertEqpPreventive(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into eqp_preventive_maintenance '
                           '(eqs_date, eqs_user, eqs_eqp, eqs_operator, eqs_comm) '
                           'values '
                           '(%(date)s, %(id_user)s, %(id_eqp)s, %(operator)s, %(comm)s)', params)

            Quality.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def deleteEqpPreventive(id_item, with_id_eqp=False):
        try:
            cursor = DB.cursor()

            cond  = id_item
            cond2 = 'eqs_ser = %s'

            if with_id_eqp:
                cond  = '(select eqs_ser from eqp_preventive_maintenance where eqs_eqp=%s)'
                cond2 = 'eqs_eqp = %s'

            cursor.execute('delete from sigl_file_data '
                           'where id_data in (select id_file from eqp_preventive_maintenance_file '
                           'where id_ext in ' + cond + ')', (id_item,))

            cursor.execute('delete from eqp_preventive_maintenance_file '
                           'where id_ext in ' + cond, (id_item,))

            cursor.execute('delete from eqp_preventive_maintenance '
                           'where ' + cond2, (id_item,))

            Quality.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getEquipmentContractList(id_eqp):
        cursor = DB.cursor()

        req = ('select eqc_ser, eqc_date, eqc_user, eqc_eqp, eqc_supplier, eqc_date_upd, eqc_comm, '
               'sup.fournisseur_nom as supplier '
               'from eqp_maintenance_contract '
               'left join sigl_fournisseurs_data as sup on sup.id_data=eqc_supplier '
               'where eqc_eqp=%s '
               'order by eqc_date desc')

        cursor.execute(req, (id_eqp,))

        return cursor.fetchall()

    @staticmethod
    def insertEqpContract(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into eqp_maintenance_contract '
                           '(eqc_date, eqc_user, eqc_eqp, eqc_supplier, eqc_date_upd, eqc_comm) '
                           'values '
                           '(%(date)s, %(id_user)s, %(id_eqp)s, %(supplier)s, %(date_upd)s, %(comm)s)', params)

            Quality.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def deleteEqpContract(id_item, with_id_eqp=False):
        try:
            cursor = DB.cursor()

            cond  = id_item
            cond2 = 'eqc_ser = %s'

            if with_id_eqp:
                cond  = '(select eqc_ser from eqp_maintenance_contract where eqc_eqp=%s)'
                cond2 = 'eqc_eqp = %s'

            cursor.execute('delete from sigl_file_data '
                           'where id_data in (select id_file from eqp_maintenance_file where id_ext in ' + cond + ')', (id_item,))

            cursor.execute('delete from eqp_maintenance_file '
                           'where id_ext in ' + cond, (id_item,))

            cursor.execute('delete from eqp_maintenance_contract '
                           'where ' + cond2, (id_item,))

            Quality.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def cancelStockIO(**params):
        try:
            cursor = DB.cursor()

            if params['type_move'] == 'I':
                table_name = 'product_supply '
                set_var    = 'prs_cancel="Y", prs_user_cancel=%(id_user)s '
                stock_ser  = 'prs_ser=%(id_stock)s'
            elif params['type_move'] == 'O':
                table_name = 'product_use '
                set_var    = 'pru_cancel="Y", pru_user_cancel=%(id_user)s '
                stock_ser  = 'pru_ser=%(id_stock)s'

                # update prs_empty to N (even if its already to N)
                cursor.execute('update product_supply set prs_empty="N" where prs_ser= '
                               '(select pru_prs from product_use where pru_ser=%(id_stock)s)', params)
            else:
                Quality.log.error(Logs.fileline() + ' : ERROR wrong type_move = ' + str(params['type_move']))
                return False

            cursor.execute('update ' + table_name +
                           'set ' + set_var +
                           'where ' + stock_ser, params)

            Quality.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getStockList(args):
        cursor = DB.cursor()

        filter_cond = ' prs_ser > 0 and prs_cancel="N" and prs_remove="N" '

        if not args:
            limit = 'LIMIT 1000'
        else:
            if 'limit' in args and args['limit'] > 0:
                limit = 'LIMIT ' + str(args['limit'])
            else:
                limit = 'LIMIT 500'

            # filter conditions
            if 'prod_name' in args and args['prod_name']:
                filter_cond += ' and prd_name LIKE "%' + str(args['prod_name']) + '%" '

            if 'prod_type' in args and args['prod_type'] > 0:
                filter_cond += ' and prd_type = ' + str(args['prod_type'])

            if 'prod_conserv' in args and args['prod_conserv'] > 0:
                filter_cond += ' and prd_conserv = ' + str(args['prod_conserv'])

            if 'prod_lessor' in args and args['prod_lessor']:
                filter_cond += ' and prs_lessor LIKE "%' + str(args['prod_lessor']) + '%" '

            if 'prod_local' in args and args['prod_local'] > 0:
                filter_cond += ' and prs_prl = ' + str(args['prod_local'])

        req = ('select prs_ser, prs_prd, prd_name, prd_nb_by_pack, prs_nb_pack, '
               'sum(pru_nb_pack) as pru_nb_pack, prd_safe_limit, prd_expir_oblig, prs_prl, prl_name, '
               'dict1.label as type,  dict2.label as conserv, '
               'sup.fournisseur_nom as supplier, Min(if(prs_empty="Y", NULL, prs_expir_date)) as expir_date '
               'from product_supply '
               'inner join product_details on prd_ser=prs_prd '
               'left join product_local on prl_ser=prs_prl '
               'left join product_use on pru_prs=prs_ser and pru_cancel="N" '
               'left join sigl_fournisseurs_data as sup on sup.id_data=prd_supplier '
               'left join sigl_dico_data as dict1 on dict1.id_data=prd_type '
               'left join sigl_dico_data as dict2 on dict2.id_data=prd_conserv '
               'where ' + filter_cond + ' ' +
               'group by prd_name, prl_name '
               'order by prd_name asc, prl_name asc ' + limit)

        cursor.execute(req)

        return cursor.fetchall()

    @staticmethod
    def getStockExportProducts():
        cursor = DB.cursor()

        req = ('select prd_ser, prd_date, prd_name, prd_type, dict1.label as type, prd_nb_by_pack, '
               'sup.fournisseur_nom as supplier, prd_ref_supplier, dict2.label as conserv, prd_safe_limit '
               'from product_details '
               'left join sigl_fournisseurs_data as sup on sup.id_data=prd_supplier '
               'left join sigl_dico_data as dict1 on dict1.id_data=prd_type '
               'left join sigl_dico_data as dict2 on dict2.id_data=prd_conserv '
               'order by prd_ser asc ')

        cursor.execute(req)

        return cursor.fetchall()

    @staticmethod
    def getStockExportSupplies():
        cursor = DB.cursor()

        req = ('select prs_ser, prs_date, prd_name as product, prs_nb_pack, prs_receipt_date, prs_expir_date, prl_name, '
               'prs_batch_num, prs_buy_price, u1.username as user, prs_empty, prs_cancel, u2.username as user_cancel, '
               'prs_lessor, prs_remove, u3.username as user_remove '
               'from product_supply '
               'left join product_details on prd_ser=prs_prd '
               'left join product_local on prl_ser=prs_prl '
               'left join sigl_user_data as u1 on u1.id_data=prs_user '
               'left join sigl_user_data as u2 on u2.id_data=prs_user_cancel '
               'left join sigl_user_data as u3 on u3.id_data=prs_user_remove '
               'order by prs_ser asc')

        cursor.execute(req)

        return cursor.fetchall()

    @staticmethod
    def getStockExportUses():
        cursor = DB.cursor()

        req = ('select pru_ser, pru_date, prd_name as product, pru_nb_pack, u1.username as user, pru_cancel, '
               'u2.username as user_cancel '
               'from product_use '
               'left join product_supply on prs_ser=pru_prs '
               'left join product_details on prd_ser=prs_prd '
               'left join sigl_user_data as u1 on u1.id_data=pru_user '
               'left join sigl_user_data as u2 on u2.id_data=pru_user_cancel '
               'order by pru_ser asc')

        cursor.execute(req)

        return cursor.fetchall()

    @staticmethod
    def getSumStockSupply(id_item, id_local):
        cursor = DB.cursor()

        req = ('select sum(prs_nb_pack) as total '
               'from product_supply '
               'where prs_prd=%s and prs_cancel="N" and prs_remove="N" and prs_prl=%s '
               'group by prs_prd')

        cursor.execute(req, (id_item, id_local))

        return cursor.fetchone()

    @staticmethod
    def getStockListDet(id_item, id_local=0):
        cursor = DB.cursor()

        req = ('select prs_ser, prd_name, prs_nb_pack, prs_receipt_date, prs_expir_date, prl_name, prs_prl, '
               'prs_batch_num, prs_buy_price, sum(pru_nb_pack) as pru_nb_pack, prs_lessor, prd_expir_oblig '
               'from product_supply '
               'inner join product_details on prd_ser=prs_prd '
               'left join product_use on pru_prs=prs_ser and pru_cancel="N" '
               'left join product_local on prl_ser=prs_prl '
               'where (prs_empty="N" and prs_cancel="N" and prs_remove="N") and prd_ser=%s and prs_prl=%s '
               'group by prs_ser '
               'order by prs_expir_date asc ')

        cursor.execute(req, (id_item, id_local))

        return cursor.fetchall()

    @staticmethod
    def getStockSearch(text):
        cursor = DB.cursor()

        l_words = text.split(' ')

        cond = 'fournisseur_nom is not NULL '

        for word in l_words:
            cond = (cond + ' and (fournisseur_nom like "%' + word + '%") ')

        req = ('select fournisseur_nom as field_value, id_data '
               'from sigl_fournisseurs_data '
               'where ' + cond + ' order by field_value asc limit 1000')

        cursor.execute(req)

        return cursor.fetchall()

    @staticmethod
    def getStockProductSearch(text):
        cursor = DB.cursor()

        l_words = text.split(' ')

        cond = 'prd_ser > 0 '

        for word in l_words:
            cond = (cond + ' and (prd_name like "%' + word + '%") ')

        req = ('select prd_name as field_value, prd_ser as id_item '
               'from product_details '
               'where ' + cond + ' order by field_value asc limit 1000')

        cursor.execute(req)

        return cursor.fetchall()

    @staticmethod
    def getStockProduct(id_item):
        cursor = DB.cursor()

        req = ('select prd_ser, prd_name, prd_type, prd_nb_by_pack, prd_supplier, prd_ref_supplier, '
               'prd_conserv, sup.fournisseur_nom as supplier_name, prd_safe_limit, prd_expir_oblig '
               'from product_details '
               'left join sigl_fournisseurs_data as sup on sup.id_data=prd_supplier '
               'where prd_ser=%s')

        cursor.execute(req, (id_item,))

        return cursor.fetchone()

    @staticmethod
    def getStockProductHist(id_item, date_beg, date_end, id_local=0):
        cursor = DB.cursor()

        # Take all supply  for this product
        req = ('select prs_ser, prs_nb_pack, prs_receipt_date, prs_expir_date, prl_name, prs_prl, '
               'prs_batch_num, prs_buy_price, prs_date as date_create, username, prs_lessor '
               'from product_supply '
               'left join product_local on prl_ser=prs_prl '
               'left join sigl_user_data on id_data=prs_user '
               'where prs_prd=%s and prs_prl=%s and (prs_date between %s and %s) and prs_cancel="N"')

        cursor.execute(req, (id_item, id_local, date_beg, date_end))

        ret = cursor.fetchall()

        # Take all use for this product
        req = ('select pru_ser, pru_nb_pack, username, pru_date as date_create '
               'from product_use '
               'inner join product_supply on prs_ser=pru_prs '
               'left join sigl_user_data on id_data=pru_user '
               'where prs_prd=%s and prs_prl=%s and (pru_date between %s and %s) and pru_cancel="N"')

        cursor.execute(req, (id_item, id_local, date_beg, date_end,))

        ret = ret + cursor.fetchall()

        return ret

    @staticmethod
    def getStockProductList():
        cursor = DB.cursor()

        req = ('select prd_ser, prd_name, prd_type, prd_nb_by_pack, prd_supplier, prd_ref_supplier, '
               'prd_conserv, sup.fournisseur_nom as supplier_name, prd_safe_limit, d1.label as type, d2.label as conserv '
               'from product_details '
               'left join sigl_dico_data as d1 on d1.id_data=prd_type '
               'left join sigl_dico_data as d2 on d2.id_data=prd_conserv '
               'left join sigl_fournisseurs_data as sup on sup.id_data=prd_supplier '
               'order by prd_name asc, supplier_name asc')

        cursor.execute(req)

        return cursor.fetchall()

    @staticmethod
    def insertStockProduct(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into product_details '
                           '(prd_date, prd_name, prd_type, prd_nb_by_pack, prd_supplier, prd_ref_supplier, '
                           'prd_conserv, prd_safe_limit, prd_expir_oblig) '
                           'values '
                           '(NOW(), %(prd_name)s, %(prd_type)s, %(prd_nb_by_pack)s, %(prd_supplier)s, '
                           '%(prd_ref_supplier)s, %(prd_conserv)s, %(prd_safe_limit)s, '
                           '%(prd_expir_oblig)s)', params)

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
                           'prd_conserv=%(prd_conserv)s, '
                           'prd_safe_limit=%(prd_safe_limit)s, prd_expir_oblig=%(prd_expir_oblig)s '
                           'where prd_ser=%(prd_ser)s', params)

            Quality.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getStockSupplyList(args):
        cursor = DB.cursor()

        filter_cond = ' '

        if args:
            # filter conditions
            if 'prod_name' in args and args['prod_name']:
                filter_cond += ' and prd_name LIKE "%' + str(args['prod_name']) + '%" '

            if 'prod_local' in args and args['prod_local'] > 0:
                filter_cond += ' and prs_prl = ' + str(args['prod_local'])

        req = ('select prs_ser, prd_name, prs_date, prs_nb_pack, prs_prl, prl_name '
               'from product_supply '
               'inner join product_details on prd_ser=prs_prd '
               'left join product_local on prl_ser=prs_prl '
               'where prs_empty="N" and prs_cancel="N" and prs_remove="N" ' + filter_cond + ' ' +
               'order by prd_name asc, prl_name asc')

        cursor.execute(req)

        return cursor.fetchall()

    @staticmethod
    def getStockSupply(prs_ser):
        cursor = DB.cursor()

        req = ('select prs_ser, prs_date, prs_prd, prs_nb_pack, prs_receipt_date, prs_expir_date, prs_batch_num, '
               'prs_buy_price, prs_user, prs_empty, prs_cancel, prs_user_cancel, prs_lessor, prs_prl '
               'from product_supply '
               'where prs_ser=%s')

        cursor.execute(req, (prs_ser,))

        return cursor.fetchone()

    @staticmethod
    def updateStockSupplyLocal(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('update product_supply '
                           'set prs_prl=%(prs_prl)s '
                           # DESACT 24/06/2024 supposed to be a bug , prs_nb_pack=%(prs_nb_pack)s
                           'where prs_ser=%(prs_ser)s', params)

            Quality.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def insertStockSupplySplit(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into product_supply '
                           '(prs_date, prs_prd, prs_nb_pack, prs_receipt_date, prs_expir_date, prs_batch_num, '
                           'prs_buy_price, prs_user, prs_empty, prs_cancel, prs_user_cancel, prs_lessor, prs_prl) '
                           'select NOW(), prs_prd, %(prs_nb_pack)s, prs_receipt_date, prs_expir_date, prs_batch_num, '
                           'prs_buy_price, %(prs_user)s, prs_empty, prs_cancel, prs_user_cancel, prs_lessor, %(prs_prl)s '
                           'from product_supply '
                           'where prs_ser=%(prs_ser)s', params)

            Quality.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def removeStockSupply(id_item, id_local, id_user):
        try:
            cursor = DB.cursor()

            cursor.execute('update product_supply '
                           'set prs_remove="Y", prs_user_remove=%s '
                           'where prs_prd=%s and prs_prl=%s', (id_user, id_item, id_local))

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
               'where prs_ser=%s and prs_cancel="N" and prs_remove="N"')

        cursor.execute(req, (id_item,))

        return cursor.fetchone()

    @staticmethod
    def getNbStockUse(id_item):
        cursor = DB.cursor()

        req = ('select sum(pru_nb_pack) as nb_pack '
               'from product_use '
               'where pru_prs=%s and pru_cancel="N" '
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
                           '(prs_date, prs_user, prs_prd, prs_nb_pack, prs_receipt_date, prs_expir_date, '
                           'prs_prl, prs_batch_num, prs_buy_price, prs_lessor) '
                           'values '
                           '(NOW(), %(prs_user)s, %(prs_prd)s, %(prs_nb_pack)s, %(prs_receipt_date)s, '
                           '%(prs_expir_date)s, %(prs_prl)s, %(prs_batch_num)s, %(prs_buy_price)s, %(prs_lessor)s)', params)

            Quality.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def updateStockSupply(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('update product_supply '
                           'set prs_user=%(prs_user)s, prs_prd=%(prs_prd)s, prs_nb_pack=%(prs_nb_pack)s, '
                           'prs_receipt_date=%(prs_receipt_date)s, prs_expir_date=%(prs_expir_date)s, '
                           'prs_prl=%(prs_prl)s, prs_batch_num=%(prs_batch_num)s, prs_buy_price=%(prs_buy_price)s, '
                           'prs_lessor=%(prs_lessor)s '
                           'where prs_ser=%(prs_ser)s', params)

            Quality.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def emptyStockSupply(prs_ser):
        try:
            cursor = DB.cursor()

            cursor.execute('update product_supply '
                           'set prs_empty="Y" '
                           'where prs_ser=%s', (prs_ser,))

            Quality.log.info(Logs.fileline() + ' : prs_ser = ' + str(prs_ser))

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
    def getStockLocalList():
        cursor = DB.cursor()

        req = ('select prl_ser, prl_name, prl_rank '
               'from product_local '
               'order by prl_rank asc, prl_name asc')

        cursor.execute(req)

        return cursor.fetchall()

    @staticmethod
    def countStockLocalUsed(id_local):
        cursor = DB.cursor()

        req = ('select count(*) as nb_used '
               'from product_supply '
               'where prs_prl=%s and prs_cancel="N" and prs_remove="N"')

        cursor.execute(req, (id_local,))

        return cursor.fetchone()

    @staticmethod
    def getStorageList(args):
        cursor = DB.cursor()

        in_stock = args.get('in_stock', 'Y') if args else 'Y'

        req = ('SELECT sal_ser, sbo_ser, sbo_label, sco_ser, sco_label, sch_ser, sch_label, sro_ser, sro_label, '
               'sbo_coordinates, sal_coordinates, sal_pathogen, sal_in_stock, sal_date, '
               'IFNULL(pat.code, "") AS pat_code, IFNULL(pat.code_patient, "") AS pat_code_lab, '
               'IFNULL(pat.nom, "") AS pat_name, IFNULL(pat.prenom, "") AS pat_firstname, '
               'IFNULL(samp.type_prel, sal_type) AS type, IFNULL(samp.id_dos, 0) AS id_rec, '
               'IF(param_num_rec.periode=1070, rec.num_dos_mois, rec.num_dos_an) AS rec_num_long, rec.type AS rec_type, '
               'rec.rec_num_int, rec.date_prescription AS rec_date_prescr, IFNULL(samp_id_ana, 0) AS id_ana, '
               'ana.code AS ana_code, ana.ana_loinc, ana.nom AS ana_name, '

               # Add column only if in_stock = 'N'
               'CASE WHEN %s = "N" THEN sad_reason ELSE NULL END AS sad_reason, '
               'CASE WHEN %s = "N" THEN sad_external ELSE NULL END AS sad_external, '
               'CASE WHEN %s = "N" THEN sad_location ELSE NULL END AS sad_location, '
               'CASE WHEN %s = "N" THEN sad_destock_date ELSE NULL END AS sad_destock_date '

               'FROM storage_aliquot '
               'INNER JOIN storage_box sbo ON sal_box = sbo_ser '
               'INNER JOIN storage_compartment ON sbo_compartment = sco_ser '
               'INNER JOIN storage_chamber ON sco_chamber = sch_ser '
               'INNER JOIN storage_room ON sch_room = sro_ser '
               'INNER JOIN sigl_03_data pat ON sal_patient = pat.id_data '
               'LEFT JOIN sigl_01_data samp ON sal_sample = samp.id_data '
               'LEFT JOIN sigl_02_data rec ON samp.id_dos = rec.id_data '
               'LEFT JOIN sigl_05_data ana ON samp.samp_id_ana = ana.id_data '
               'LEFT JOIN sigl_param_num_dos_data AS param_num_rec ON param_num_rec.id_data=1 '

               'LEFT JOIN sample_destock ON sad_aliquot = sal_ser AND %s = "N" '

               'WHERE sal_in_stock=%s order by sal_date desc')

        # Exécution de la requête
        cursor.execute(req, (in_stock, in_stock, in_stock, in_stock, in_stock, in_stock))

        return cursor.fetchall()

    @staticmethod
    def getStorageRoomList():
        cursor = DB.cursor()

        req = ('select sro_ser as id, sro_name as name, sro_abbrev as abbrev, '
               'sro_label AS label, count(sch_ser) as nb_chamber '
               'from storage_room '
               'left join storage_chamber on sro_ser = sch_room '
               'group by sro_ser, sro_name, sro_abbrev, sro_label '
               'order by sro_name asc')

        cursor.execute(req)

        return cursor.fetchall()

    @staticmethod
    def getStorageRoom(id_item):
        cursor = DB.cursor()

        req = ('select sro_ser, sro_user, sro_name, sro_abbrev, sro_label '
               'from storage_room '
               'where sro_ser=%s')

        cursor.execute(req, (id_item,))

        return cursor.fetchone()

    @staticmethod
    def insertStorageRoom(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into storage_room '
                           '(sro_date, sro_user, sro_name, sro_abbrev, sro_label) '
                           'values '
                           '(NOW(), %(user)s, %(name)s, %(abbrev)s, %(label)s)', params)

            Quality.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def updateStorageRoom(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('update storage_room '
                           'set sro_user=%(user)s, sro_name=%(name)s, sro_abbrev=%(abbrev)s, sro_label=%(label)s '
                           'where sro_ser=%(id_item)s', params)

            Quality.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def deleteStorageRoom(id_item):
        try:
            cursor = DB.cursor()

            cursor.execute('delete from storage_room '
                           'where sro_ser=%s', (id_item,))

            Quality.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getStorageChamberList():
        cursor = DB.cursor()

        req = ('select sch_ser as id, sch_name as name, sch_abbrev as abbrev, '
               'sch_label as label, count(sco_ser) as nb_compartment, sro_abbrev as room_abbrev, sro_label as room_label '
               'from storage_chamber '
               'inner join storage_room on sro_ser = sch_room '
               'left join storage_compartment on sco_chamber = sch_ser '
               'group by sch_ser, sch_name, sch_abbrev, sch_label, sro_abbrev, sro_label '
               'order by sch_name asc')

        cursor.execute(req)

        return cursor.fetchall()

    @staticmethod
    def getStorageChamber(id_item):
        cursor = DB.cursor()

        req = ('select sch_ser, sch_user, sch_room, sch_name, sch_abbrev, sch_label '
               'from storage_chamber '
               'where sch_ser=%s')

        cursor.execute(req, (id_item,))

        return cursor.fetchone()

    @staticmethod
    def insertStorageChamber(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into storage_chamber '
                           '(sch_date, sch_user, sch_name, sch_abbrev, sch_label, sch_room) '
                           'values '
                           '(NOW(), %(user)s, %(name)s, %(abbrev)s, %(label)s, %(room)s)', params)

            Quality.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def updateStorageChamber(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('update storage_chamber '
                           'set sch_user=%(user)s, sch_name=%(name)s, sch_abbrev=%(abbrev)s, sch_label=%(label)s, '
                           'sch_room=%(room)s '
                           'where sch_ser=%(id_item)s', params)

            Quality.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def deleteStorageChamber(id_item):
        try:
            cursor = DB.cursor()

            cursor.execute('delete from storage_chamber '
                           'where sch_ser=%s', (id_item,))

            Quality.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getStorageCompList():
        cursor = DB.cursor()

        req = ('select sco_ser as id, sco_name as name, sco_abbrev as abbrev, sco_dim_x as dim_x, sco_dim_y as dim_y, '
               'sco_dim_z as dim_z, sco_label as label, count(sbo_ser) as nb_box, sch_abbrev as chamber_abbrev, '
               'sch_label as chamber_label '
               'from storage_compartment '
               'inner join storage_chamber on sch_ser = sco_chamber '
               'left join storage_box on sbo_compartment = sco_ser '
               'group by sco_ser, sco_name, sco_abbrev, sco_label, sch_abbrev, sch_label '
               'order by sco_name asc')

        cursor.execute(req)

        return cursor.fetchall()

    @staticmethod
    def getStorageComp(id_item):
        cursor = DB.cursor()

        req = ('select sco_ser, sco_user, sco_chamber, sco_name, sco_abbrev, sco_label, sco_dim_x, sco_dim_y, sco_dim_z '
               'from storage_compartment '
               'where sco_ser=%s')

        cursor.execute(req, (id_item,))

        return cursor.fetchone()

    @staticmethod
    def insertStorageComp(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into storage_compartment '
                           '(sco_date, sco_user, sco_name, sco_abbrev, sco_label, sco_chamber, '
                           'sco_dim_x, sco_dim_y, sco_dim_z) '
                           'values '
                           '(NOW(), %(user)s, %(name)s, %(abbrev)s, %(label)s, %(chamber)s, '
                           '%(dim_x)s, %(dim_y)s, %(dim_z)s)', params)

            Quality.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def updateStorageComp(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('update storage_compartment '
                           'set sco_user=%(user)s, sco_name=%(name)s, sco_abbrev=%(abbrev)s, sco_label=%(label)s, '
                           'sco_chamber=%(chamber)s, sco_dim_x=%(dim_x)s, sco_dim_y=%(dim_y)s, sco_dim_z=%(dim_z)s '
                           'where sco_ser=%(id_item)s', params)

            Quality.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def deleteStorageComp(id_item):
        try:
            cursor = DB.cursor()

            cursor.execute('delete from storage_compartment '
                           'where sco_ser=%s', (id_item,))

            Quality.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getStorageBoxList():
        cursor = DB.cursor()

        req = ('select sbo_ser as id, sbo_name as name, sbo_coordinates as coord, sbo_dim_x as dim_x, sbo_dim_y as dim_y, '
               'sbo_label as label, count(sal_ser) as nb_box, sco_abbrev as compartment_abbrev, '
               'sco_label as compartment_label, sbo_full as full '
               'from storage_box '
               'inner join storage_compartment on sco_ser = sbo_compartment '
               'left join storage_aliquot on sal_box = sbo_ser '
               'group by sbo_ser, sbo_name, sbo_coordinates, sbo_label, sbo_label '
               'order by sbo_name asc')

        cursor.execute(req)

        return cursor.fetchall()

    @staticmethod
    def getStorageBox(id_item):
        cursor = DB.cursor()

        req = ('select sbo_ser, sbo_user, sbo_compartment, sbo_name, sbo_coordinates, sbo_label, sbo_dim_x, sbo_dim_y, '
               'sbo_full '
               'from storage_box '
               'where sbo_ser=%s')

        cursor.execute(req, (id_item,))

        return cursor.fetchone()

    @staticmethod
    def insertStorageBox(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into storage_box '
                           '(sbo_date, sbo_user, sbo_name, sbo_label, sbo_compartment, '
                           'sbo_dim_x, sbo_dim_y, sbo_coordinates, sbo_full) '
                           'values '
                           '(NOW(), %(user)s, %(name)s, %(label)s, %(compartment)s, '
                           '%(dim_x)s, %(dim_y)s, %(coordinates)s, %(full)s)', params)

            Quality.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def updateStorageBox(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('update storage_box '
                           'set sbo_user=%(user)s, sbo_name=%(name)s, sbo_label=%(label)s, sbo_dim_x=%(dim_x)s, '
                           'sbo_dim_y=%(dim_y)s, sbo_compartment=%(compartment)s, sbo_coordinates=%(coordinates)s, '
                           'sbo_full=%(full)s '
                           'where sbo_ser=%(id_item)s', params)

            Quality.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def deleteStorageBox(id_item):
        try:
            cursor = DB.cursor()

            cursor.execute('delete from storage_box '
                           'where sbo_ser=%s', (id_item,))

            Quality.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getStorageBoxCoord(id_item):
        cursor = DB.cursor()

        req = ('select sro_label, sch_label, sco_label, sbo_coordinates, sbo_label, sbo_full '
               'from storage_box '
               'inner join storage_compartment on sco_ser=sbo_compartment '
               'inner join storage_chamber on sch_ser=sco_chamber '
               'inner join storage_room on sro_ser=sch_room '
               'where sbo_ser=%s')

        cursor.execute(req, (id_item,))

        return cursor.fetchone()

    @staticmethod
    def getStorageAliquot(id_item):
        cursor = DB.cursor()

        req = ('select sal_ser, sal_user, sal_sample, sal_patient, sal_pathogen, sal_box, sal_coordinates, sal_in_stock, '
               'ifnull(pat.code, "") as pat_code, ifnull(pat.code_patient, "") as pat_code_lab, '
               'ifnull(pat.nom, "") as pat_name, ifnull(pat.prenom, "") as pat_firstname, '
               'ifnull(samp.type_prel, sal_type) as type, ifnull(samp.id_dos, 0) as id_rec '
               'from storage_aliquot '
               'LEFT JOIN sigl_03_data pat ON sal_patient = pat.id_data '
               'LEFT JOIN sigl_01_data samp ON sal_sample = samp.id_data '
               'where sal_ser=%s')

        cursor.execute(req, (id_item,))

        return cursor.fetchone()

    @staticmethod
    def insertStorageAliquot(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into storage_aliquot '
                           '(sal_date, sal_user, sal_sample, sal_patient, sal_type, sal_pathogen, sal_box, '
                           'sal_coordinates, sal_in_stock) '
                           'values '
                           '(NOW(), %(user)s, %(sample)s, %(patient)s, %(type)s, '
                           '%(pathogen)s, %(box)s, %(coordinates)s, %(in_stock)s)', params)

            Quality.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def updateStorageAliquot(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('update storage_aliquot '
                           'set sal_user=%(user)s, sal_sample=%(sample)s, sal_patient=%(patient)s, '
                           'sal_pathogen=%(pathogen)s, sal_box=%(box)s, sal_coordinates=%(coordinates)s, '
                           'sal_in_stock=%(in_stock)s, sal_type=%(type)s '
                           'where sal_ser=%(id_item)s', params)

            Quality.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def deleteStorageAliquot(id_item):
        try:
            cursor = DB.cursor()

            cursor.execute('delete from storage_aliquot '
                           'where sal_ser=%s', (id_item,))

            Quality.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getSupplierList():
        cursor = DB.cursor()

        req = ('select id_data, id_owner, fournisseur_nom as supplier, contact_nom as lastname, '
               'contact_prenom as firstname, contact_fonction as funct, fournisseur_adresse as address, '
               'contact_tel as phone, contact_mobile as mobile, contact_fax as fax, contact_email as email, '
               'commentaire as comment, date_format(sys_creation_date, %s) as date_create, '
               'date_format(sys_last_mod_date, %s) as date_update, sys_last_mod_user as id_user_upd, supp_critical '
               'from sigl_fournisseurs_data '
               'order by supplier asc, lastname asc, firstname asc')

        cursor.execute(req, (Constants.cst_dt_HMS_SQL, Constants.cst_dt_HMS_SQL,))

        return cursor.fetchall()

    @staticmethod
    def destockStorageAliquot(id_item, id_user, reason, external, location, destock_date):
        try:
            cursor = DB.cursor()

            cursor.execute("""
                INSERT INTO sample_destock (sad_date, sad_user, sad_aliquot, sad_reason, sad_external, sad_location, sad_destock_date)
                VALUES (now(), %s, %s, %s, %s, %s, %s)
            """, (id_user, id_item, reason, external, location, destock_date))

            cursor.execute("UPDATE storage_aliquot SET sal_in_stock = 'N' WHERE sal_ser = %s", (id_item,))

            Quality.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def restockStorageAliquot(id_item, id_user):
        try:
            cursor = DB.cursor()

            cursor.execute("UPDATE storage_aliquot SET sal_in_stock = 'Y' WHERE sal_ser = %s", (id_item,))

            cursor.execute("""
                UPDATE sample_destock
                SET sad_restock_date = now(), sad_restock_user = %s
                WHERE sad_aliquot = %s
                ORDER BY sad_ser DESC
                LIMIT 1
            """, (id_user, id_item))

            Quality.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getSupplierSearch(text):
        cursor = DB.cursor()

        l_words = text.split(' ')

        cond = 'fournisseur_nom is not NULL '

        for word in l_words:
            cond = (cond + ' and (fournisseur_nom like "%' + word + '%") ')

        req = ('select fournisseur_nom as field_value, id_data '
               'from sigl_fournisseurs_data '
               'where ' + cond + ' order by field_value asc limit 1000')

        cursor.execute(req)

        return cursor.fetchall()

    @staticmethod
    def getSupplier(id_item):
        cursor = DB.cursor()

        req = ('select id_data ,id_owner, fournisseur_nom as supplier, contact_nom as lastname, '
               'contact_prenom as firstname, contact_fonction as funct, contact_tel as phone, '
               'contact_email as email, fournisseur_adresse as address, supp_critical, '
               'contact_mobile as mobile, contact_fax as fax, commentaire as comment '
               'from sigl_fournisseurs_data '
               'where id_data=%s')

        cursor.execute(req, (id_item,))

        return cursor.fetchone()

    @staticmethod
    def insertSupplier(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into sigl_fournisseurs_data '
                           '(id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, fournisseur_nom, '
                           'contact_nom, contact_prenom, contact_fonction, fournisseur_adresse, contact_tel, '
                           'contact_email, contact_mobile, contact_fax, commentaire, supp_critical) '
                           'values '
                           '(%(id_owner)s, NOW(), NOW(), %(id_owner)s, %(supplier)s, %(lastname)s, %(firstname)s, '
                           '%(funct)s, %(address)s, %(phone)s, %(email)s, %(mobile)s, %(fax)s, %(comment)s, %(critical)s)', params)

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
                           'set fournisseur_nom=%(supplier)s, contact_nom=%(lastname)s, contact_prenom=%(firstname)s, '
                           'contact_fonction=%(funct)s, fournisseur_adresse=%(address)s, contact_tel=%(phone)s, '
                           'contact_email=%(email)s, contact_mobile=%(mobile)s, contact_fax=%(fax)s, '
                           'commentaire=%(comment)s, supp_critical=%(critical)s '
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
    def getManualList(args):
        cursor = DB.cursor()

        filter_cond = ' manu.titre != "" '

        if args:
            # filter conditions
            if 'title' in args and args['title']:
                filter_cond += ' and manu.titre LIKE "%' + str(args['title']) + '%" '

            if 'man_mas' in args and args['man_mas'] > 0:
                filter_cond += ' and manu.man_mas = ' + str(args['man_mas'])

        req = ('select manu.id_data, manu.titre as title, mas_name, manu.reference, '
               'u1.initiale as writer, u2.initiale as auditor, u3.initiale as approver, '
               'date_insert, date_apply, date_update, dict.label as section '
               'from sigl_manuels_data as manu '
               'left join manual_setting on mas_ser=manu.man_mas '
               'left join sigl_user_data as u1 on u1.id_data=manu.redacteur_id '
               'left join sigl_user_data as u2 on u2.id_data=manu.verificateur_id '
               'left join sigl_user_data as u3 on u3.id_data=manu.approbateur_id '
               'left join sigl_dico_data as dict on dict.id_data=manu.section '
               'where ' + filter_cond + ' ' +
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

        req = ('select CONCAT(titre, IF(reference is not NULL and reference != "", CONCAT(" / ref: ",reference), "")) '
               'as field_value, id_data '
               'from sigl_manuels_data '
               'where ' + cond + ' order by field_value asc limit 1000')

        cursor.execute(req)

        return cursor.fetchall()

    @staticmethod
    def getManual(id_item):
        cursor = DB.cursor()

        req = ('select manu.id_data ,manu.id_owner, manu.titre as title, manu.reference, mas_name, '
               'TRIM(CONCAT(u1.lastname," ",u1.firstname," - ",u1.username)) as writer, '
               'TRIM(CONCAT(u2.lastname," ",u2.firstname," - ",u2.username)) as auditor, '
               'TRIM(CONCAT(u3.lastname," ",u3.firstname," - ",u3.username)) as approver, '
               'manu.redacteur_id as writer_id, manu.verificateur_id as auditor_id, '
               'manu.approbateur_id as approver_id, manu.date_insert, manu.date_apply, '
               'manu.date_update, manu.section '
               'from sigl_manuels_data as manu '
               'left join manual_setting on mas_ser=manu.man_mas '
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
                           '(id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, titre , man_mas, reference, '
                           'redacteur_id, verificateur_id, approbateur_id, date_insert, date_apply, date_update, section) '
                           'values '
                           '(%(id_owner)s, NOW(), NOW(), %(id_owner)s, %(title)s, %(man_mas)s, %(reference)s, %(writer)s, %(auditor)s, '
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
                           'set titre=%(title)s, man_mas=%(man_mas)s, reference=%(reference)s, redacteur_id=%(writer)s, '
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

        req = ('select meet.id_data, meet.date as date_meeting, meet.type_reu as type_id, '
               'u1.initiale as promoter, meet.cr as report, d1.label as type '
               'from sigl_reunion_data as meet '
               'left join sigl_user_data as u1 on u1.id_data=meet.organisateur_id '
               'left join sigl_dico_data as d1 on d1.id_data=meet.type_reu '
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

        req = ('select CONCAT(titre, IF(reference is not NULL and reference != "", CONCAT(" / ref: ",reference), "")) '
               'as field_value, id_data '
               'from sigl_procedures_data '
               'where ' + cond + ' order by field_value asc limit 1000')

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
               'where usr.status="' + Constants.cst_user_active + '" '
               'order by usr.lastname asc, usr.firstname asc')

        cursor.execute(req, (Constants.cst_dt_HMS_SQL, Constants.cst_dt_HMS_SQL, Constants.cst_dt_HMS_SQL,))

        return cursor.fetchall()

    @staticmethod
    def getListComment(id_item, type, sub_type):
        cursor = DB.cursor()

        req = ('select lic_ser, date_format(lic_date, "%Y-%m-%d %H:%i") as lic_date, username, lic_comm '
               'from list_comment '
               'left join sigl_user_data on id_data=lic_user '
               'where lic_ref=%s and lic_type=%s and lic_sub_type=%s '
               'order by lic_date asc')

        cursor.execute(req, (id_item, type, sub_type))

        return cursor.fetchall()

    @staticmethod
    def insertListComment(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into list_comment '
                           '(lic_date, lic_ref, lic_type, lic_sub_type, lic_user, lic_comm) '
                           'values '
                           '(NOW(), %(lic_ref)s, %(lic_type)s, %(lic_sub_type)s, %(lic_user)s, %(lic_comm)s)', params)

            Quality.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def deleteListComment(id_item):
        try:
            cursor = DB.cursor()

            cursor.execute('delete from list_comment '
                           'where lic_ser=%s', (id_item,))

            Quality.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getTraceList(type_trace):
        cursor = DB.cursor()

        info_doc  = ''
        table_doc = ''

        if type_trace == 'PROC':
            info_doc  = 'proc.titre as doc_name, proc_file.sys_creation_date as doc_date '
            table_doc = ('inner join procedure_file as proc_file on proc_file.id_file=trd_ref '
                         'inner join sigl_procedures_data as proc on proc.id_data=proc_file.id_ext ')
        else:
            Quality.log.info(Logs.fileline() + ': WRONG type_trace : ' + str(type_trace))
            return []

        req = ('select trd_ser, trd_date, trd_last_access, trd_type, trd_ref, trd_user, '
               'TRIM(CONCAT(u1.lastname," ",u1.firstname," - ",u1.username)) as user_name, ' + info_doc +
               'from trace_download ' + table_doc +
               'inner join sigl_user_data as u1 on u1.id_data=trd_user '
               'where trd_type=%s order by trd_last_access desc')

        cursor.execute(req, (type_trace,))

        return cursor.fetchall()

    @staticmethod
    def getTraceListSearch(type_trace, args):
        cursor = DB.cursor()

        info_doc  = ''
        table_doc = ''
        cond      = ''

        if args['user_id']:
            cond += ' and u1.id_data=' + str(args['user_id']) + ' '

        if type_trace == 'PROC':
            info_doc  = 'proc.titre as doc_name, proc_file.sys_creation_date as doc_date '
            table_doc = ('inner join procedure_file as proc_file on proc_file.id_file=trd_ref '
                         'inner join sigl_procedures_data as proc on proc.id_data=proc_file.id_ext ')

            if args['doc_name']:
                cond += ' and proc.titre like "%' + args['doc_name'] + '%" '
        else:
            Quality.log.info(Logs.fileline() + ': WRONG type_trace : ' + str(type_trace))
            return []

        req = ('select trd_ser, trd_date, trd_last_access, trd_type, trd_ref, trd_user, '
               'TRIM(CONCAT(u1.lastname," ",u1.firstname," - ",u1.username)) as user_name, ' + info_doc +
               'from trace_download ' + table_doc +
               'inner join sigl_user_data as u1 on u1.id_data=trd_user '
               'where trd_type=%s ' + cond + 'order by trd_last_access desc')

        cursor.execute(req, (type_trace,))

        return cursor.fetchall()

    @staticmethod
    def getTraceDownload(id_user, type, ref):
        cursor = DB.cursor()

        req = ('select trd_ser, trd_date, trd_last_access, trd_type, trd_ref, trd_user '
               'from trace_download '
               'where trd_user=%s and trd_type=%s and trd_ref=%s')

        cursor.execute(req, (id_user, type, ref))

        return cursor.fetchone()

    @staticmethod
    def insertTraceDownload(id_user, type, ref):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into trace_download '
                           '(trd_date, trd_last_access, trd_user, trd_type, trd_ref) '
                            'values (NOW(), NOW(), %s, %s, %s)', (id_user, type, ref))

            Quality.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def updateTraceDownload(id_user, type, ref):
        try:
            cursor = DB.cursor()

            req = ('update trace_download set trd_last_access=NOW() '
                   'where trd_user=%s and trd_type=%s and trd_ref=%s')

            cursor.execute(req, (id_user, type, ref))

            Quality.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def getMessageList(id_user):
        cursor = DB.cursor()

        req = ('select ime_ser, ime_date, ime_sender, ime_receiver, ime_subject, ime_body, ime_is_read, '
               'TRIM(CONCAT(u1.lastname," ",u1.firstname," - ",u1.username)) as sender, '
               'TRIM(CONCAT(u2.lastname," ",u2.firstname," - ",u2.username)) as receiver '
               'from internal_messaging '
               'left join sigl_user_data as u1 on u1.id_data=ime_sender '
               'left join sigl_user_data as u2 on u2.id_data=ime_receiver '
               'where (ime_sender = %s and ime_sender_del = "N") or '
               '(ime_receiver = %s and ime_receiver_del = "N") '
               'order by ime_date desc ')

        cursor.execute(req, (id_user, id_user))

        return cursor.fetchall()

    @staticmethod
    def getMessage(id_item):
        cursor = DB.cursor()

        req = ('select ime_ser, ime_date, ime_sender, ime_subject, ime_body, ime_is_read, '
               'TRIM(CONCAT(u1.lastname," ",u1.firstname," - ",u1.username)) as sender, '
               'TRIM(CONCAT(u2.lastname," ",u2.firstname," - ",u2.username)) as receiver '
               'from internal_messaging '
               'left join sigl_user_data as u1 on u1.id_data=ime_sender '
               'left join sigl_user_data as u2 on u2.id_data=ime_receiver '
               'where ime_ser=%s')

        cursor.execute(req, (id_item,))

        return cursor.fetchone()

    @staticmethod
    def insertMessage(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into internal_messaging '
                           '(ime_date, ime_sender, ime_receiver, ime_subject, ime_body) '
                           'values '
                           '(NOW(), %(id_user)s, %(receiver)s, %(title)s, %(message)s)', params)

            Quality.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def deleteMessage(id_item, id_user):
        try:
            cursor = DB.cursor()

            cursor.execute('update internal_messaging set '
                           'ime_sender_del = CASE '
                           'when ime_sender = %s then "Y" else ime_sender_del END, '
                           'ime_receiver_del = CASE '
                           'when ime_receiver = %s then "Y" else ime_receiver_del END '
                           'where ime_ser=%s', (id_user, id_user, id_item))

            Quality.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def messageRead(id_item):
        try:
            cursor = DB.cursor()

            cursor.execute('update internal_messaging set ime_is_read="Y" '
                           'where ime_ser=%s', (id_item,))

            Quality.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def countMessageUnread(id_user):
        cursor = DB.cursor()

        req = ('select count(*) as nb_msg '
               'from internal_messaging '
               'where ime_is_read="N" and ime_receiver_del="N" and ime_receiver=%s')

        cursor.execute(req, (id_user,))

        return cursor.fetchone()

    @staticmethod
    def getPrinterList():
        cursor = DB.cursor()

        req = ('select prt_ser, prt_name, prt_script, prt_default, prt_rank '
               'from printer_setting '
               'order by prt_rank asc, prt_date desc')

        cursor.execute(req)

        return cursor.fetchall()

    @staticmethod
    def getPrinter(id_item):
        cursor = DB.cursor()

        req = ('select prt_ser, prt_name, prt_script, prt_default, prt_rank '
               'from printer_setting '
               'where prt_ser=%s')

        cursor.execute(req, (id_item,))

        return cursor.fetchone()

    @staticmethod
    def insertPrinter(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('insert into printer_setting '
                           '(prt_date, prt_name, prt_script, prt_default, prt_rank) '
                           'values '
                           '(NOW(), %(name)s, %(script)s, %(default)s, %(rank)s)', params)

            Quality.log.info(Logs.fileline())

            return cursor.lastrowid
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return 0

    @staticmethod
    def updatePrinter(**params):
        try:
            cursor = DB.cursor()

            cursor.execute('update printer_setting '
                           'set prt_name=%(name)s , prt_script=%(script)s, prt_default=%(default)s, prt_rank=%(rank)s '
                           'where prt_ser=%(id_item)s', params)

            Quality.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False

    @staticmethod
    def deletePrinter(id_item):
        try:
            cursor = DB.cursor()

            cursor.execute('delete from printer_setting '
                           'where prt_ser=%s', (id_item,))

            Quality.log.info(Logs.fileline())

            return True
        except mysql.connector.Error as e:
            Quality.log.error(Logs.fileline() + ' : ERROR SQL = ' + str(e))
            return False
