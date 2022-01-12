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
            cond = ' cloture_date is NULL '

        elif period == 'month':
            cond = ' date > adddate(NOW(), INTERVAL -1 MONTH) '

        # NOTE count with sigl_non_conformite_data too ?
        # Number of non-compliance
        req = 'select count(*) as nb_noncompliance '\
              'from sigl_non_conformite_data '\
              'where ' + cond

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

        filter_cond = ' prs_ser > 0 and prs_cancel="N" '

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

        req = ('select prs_ser, prs_prd, prd_name, prd_nb_by_pack, prs_nb_pack, '
               'sum(pru_nb_pack) as pru_nb_pack, prd_safe_limit, '
               'dict1.label as type,  dict2.label as conserv, '
               'sup.fournisseur_nom as supplier, Min(if(prs_empty="Y", NULL, prs_expir_date)) as expir_date '
               'from product_supply '
               'inner join product_details on prd_ser=prs_prd '
               'left join product_use on pru_prs=prs_ser and pru_cancel="N" '
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
               'where prs_prd=%s and prs_cancel="N" group by prs_prd')

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
               'where (prs_empty="N" or prs_cancel="N") and prd_ser=%s '
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
               'where prs_prd=%s and (prs_date between %s and %s) and prs_cancel="N"')

        cursor.execute(req, (id_item, date_beg, date_end,))

        ret = cursor.fetchall()

        # Take all use for this product
        req = ('select pru_ser, pru_nb_pack, username, pru_date as date_create '
               'from product_use '
               'inner join product_supply on prs_ser=pru_prs '
               'left join sigl_user_data on id_data=pru_user '
               'where prs_prd=%s and (pru_date between %s and %s) and pru_cancel="N"')

        cursor.execute(req, (id_item, date_beg, date_end,))

        ret = ret + cursor.fetchall()

        return ret

    @staticmethod
    def getStockProductList():
        cursor = DB.cursor()

        req = ('select prd_ser, prd_name, prd_type, prd_nb_by_pack, prd_supplier, prd_ref_supplier, prd_conserv, '
               'sup.fournisseur_nom as supplier_name, prd_safe_limit, d1.label as type, d2.label as conserv '
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
               'where prs_ser=%s and prs_cancel="N"')

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
                           '(prs_date, prs_user, prs_prd, prs_nb_pack, prs_receipt_date, prs_expir_date, '
                           'prs_rack, prs_batch_num, prs_buy_price) '
                           'values '
                           '(NOW(), %(prs_user)s, %(prs_prd)s, %(prs_nb_pack)s, %(prs_receipt_date)s, '
                           '%(prs_expir_date)s, %(prs_rack)s, %(prs_batch_num)s, %(prs_buy_price)s)', params)

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
                           'prs_rack=%(prs_rack)s, prs_batch_num=%(prs_batch_num)s, prs_buy_price=%(prs_buy_price)s '
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

        req = ('select id_data, id_owner, fournisseur_nom as supplier, contact_nom as lastname, '
               'contact_prenom as firstname, contact_fonction as funct, fournisseur_adresse as address, '
               'contact_tel as phone, contact_mobile as mobile, contact_fax as fax, contact_email as email, '
               'commentaire as comment, date_format(sys_creation_date, %s) as date_create, '
               'date_format(sys_last_mod_date, %s) as date_update, sys_last_mod_user as id_user_upd '
               'from sigl_fournisseurs_data '
               'order by supplier asc, lastname asc, firstname asc')

        cursor.execute(req, (Constants.cst_isodatetime, Constants.cst_isodatetime,))

        return cursor.fetchall()

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
               'contact_email as email, fournisseur_adresse as address, '
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
                           'set fournisseur_nom=%(supplier)s, contact_nom=%(lastname)s, contact_prenom=%(firstname)s, '
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
