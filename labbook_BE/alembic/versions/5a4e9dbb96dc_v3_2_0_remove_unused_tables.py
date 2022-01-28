# -*- coding:utf-8 -*-
"""v3_2_0_remove_unused_tables

Revision ID: 5a4e9dbb96dc
Revises: d48ad0fcd1b8
Create Date: 2021-11-08 14:26:42.330399

"""
from alembic import op

from datetime import datetime

# revision identifiers, used by Alembic.
revision = '5a4e9dbb96dc'
down_revision = 'd48ad0fcd1b8'
branch_labels = None
depends_on = None


def upgrade():
    print("--- " + str(datetime.today()) + "---")
    print("START of migration v3_2_0_remove_unused_tables revision=5a4e9dbb96dc")

    # Get the current
    conn = op.get_bind()

    # NEW DIRECTORY IN STORAGE
    try:
        import pathlib

        pathlib.Path("/storage/resource/template").mkdir(mode=0o777, parents=False, exist_ok=True)
    except Exception as err:
        print("ERROR mkdir -p /storage/resource/template,\n\terr=" + str(err))

    # COPY alembic resource
    try:
        from distutils.dir_util import copy_tree

        fromDirectory = "alembic/resource"
        toDirectory = "/storage/resource"

        copy_tree(fromDirectory, toDirectory)
    except Exception as err:
        print("ERROR copy alembic resource,\n\terr=" + str(err))

    # TEMPLATE TABLE
    try:
        # Create table for template_setting
        conn.execute("create table template_setting("
                     "tpl_ser int not NULL AUTO_INCREMENT, "
                     "tpl_date datetime, "
                     "tpl_name varchar(100) not NULL, "
                     "tpl_file varchar(40) not NULL, "
                     "tpl_default varchar(1) not NULL, "
                     "tpl_type varchar(4) not NULL, "
                     "PRIMARY KEY (tpl_ser), INDEX (tpl_name), INDEX (tpl_type), INDEX (tpl_default))")
    except Exception as err:
        print("ERROR create table template_setting,\n\terr=" + str(err))
    else:
        try:
            # insert a default template for result report
            conn.execute("insert into template_setting "
                         "(tpl_date, tpl_name, tpl_file, tpl_default, tpl_type) "
                         "values (NOW(), 'Modèle résultat', 'template_result.odt', 'Y', 'RES')")
        except Exception as err:
            print("ERROR insert default result template for template_setting,\n\terr=" + str(err))

        try:
            # insert a arabic default template for result report
            conn.execute("insert into template_setting "
                         "(tpl_date, tpl_name, tpl_file, tpl_default, tpl_type) "
                         "values (NOW(), 'Modèle résultat écriture de droite à gauche', 'template_result-RtL.odt', 'N', 'RES')")
        except Exception as err:
            print("ERROR insert default result RtL template for template_setting,\n\terr=" + str(err))

        try:
            # insert a default template for stickers
            conn.execute("insert into template_setting "
                         "(tpl_date, tpl_name, tpl_file, tpl_default, tpl_type) "
                         "values (NOW(), 'Modèle étiquette', 'template_sticker.odt', 'Y', 'STI')")
        except Exception as err:
            print("ERROR insert default sticker template for template_setting,\n\terr=" + str(err))

    # ADD COLUMN for description in dictionnary table
    try:
        conn.execute("alter table sigl_dico_data add column dico_descr text")
    except Exception as err:
        print("ERROR add column dico_descr to sigl_dico_data,\n\terr=" + str(err))

    # ADD COLUMN for code sample request
    try:
        conn.execute("alter table sigl_01_data add column code varchar(20)")
    except Exception as err:
        print("ERROR add column code to sigl_01_data,\n\terr=" + str(err))
    else:
        try:
            # update code sample by id_data
            conn.execute("update sigl_01_data set code=id_data")
        except Exception as err:
            print("ERROR update default code for sigl_01_data,\n\terr=" + str(err))

    try:
        conn.execute("alter table sigl_01_deleted add column code varchar(20)")
    except Exception as err:
        print("ERROR add column code to sigl_01_deleted,\n\terr=" + str(err))
    else:
        try:
            # update code sample by id_data
            conn.execute("update sigl_01_deleted set code=id_data")
        except Exception as err:
            print("ERROR update default code for sigl_01_deleted,\n\terr=" + str(err))

    # ADD COLUMN for cancel stock and trace cancellation
    try:
        conn.execute("alter table product_supply add column prs_cancel varchar(1) not null default 'N'")
    except Exception as err:
        print("ERROR add column prs_cancel to product_supply,\n\terr=" + str(err))

    try:
        conn.execute("alter table product_supply add column prs_user_cancel int default 0")
    except Exception as err:
        print("ERROR add column prs_user_cancel to product_supply,\n\terr=" + str(err))

    try:
        conn.execute("alter table product_use add column pru_cancel varchar(1) not null default 'N'")
    except Exception as err:
        print("ERROR add column pru_cancel to product_use,\n\terr=" + str(err))

    try:
        conn.execute("alter table product_use add column pru_user_cancel int default 0")
    except Exception as err:
        print("ERROR add column pru_user_cancel to product_use,\n\terr=" + str(err))

    # MODIFY COLUMN cote_valeur analysis
    try:
        conn.execute("alter table sigl_05_data modify column cote_valeur decimal(10,2)")
    except Exception as err:
        print("ERROR alter table sigl_05_data modify column cote_valeur decimal(10,2),\n\terr=" + str(err))

    # MODIFY COLUMN code patient
    try:
        conn.execute("alter table sigl_03_data modify column code_patient varchar(20)")
    except Exception as err:
        print("ERROR alter table sigl_03_data modify column code_patient varchar(20),\n\terr=" + str(err))

    # ADD COLUMN for patient
    try:
        conn.execute("alter table sigl_03_data add column pat_midname varchar(40)")
    except Exception as err:
        print("ERROR add column pat_midname to sigl_03_data,\n\terr=" + str(err))

    try:
        conn.execute("alter table sigl_03_data add column pat_nation int(3) default 0")
    except Exception as err:
        print("ERROR add column pat_nation to sigl_03_data,\n\terr=" + str(err))

    try:
        conn.execute("alter table sigl_03_data add column pat_resident varchar(1) not null default 'Y'")
    except Exception as err:
        print("ERROR add column pat_resident to sigl_03_data,\n\terr=" + str(err))

    try:
        conn.execute("alter table sigl_03_data add column pat_blood_group int default 0")
    except Exception as err:
        print("ERROR add column pat_blood_group to sigl_03_data,\n\terr=" + str(err))

    try:
        conn.execute("alter table sigl_03_data add column pat_blood_rhesus int default 0")
    except Exception as err:
        print("ERROR add column pat_blood_rhesus to sigl_03_data,\n\terr=" + str(err))

    # NEW TABLE nationality
    try:
        # Create table for age interval setting
        conn.execute("create table nationality("
                     "nat_ser int not NULL AUTO_INCREMENT, "
                     "nat_name varchar(30) not null, "
                     "nat_code varchar(3) not null, "
                     "PRIMARY KEY (nat_ser), "
                     "INDEX (nat_name), INDEX (nat_code)) character set=utf8")
    except Exception as err:
        print("ERROR create table nationality,\n\terr=" + str(err))
    else:
        try:
            conn.execute("insert into nationality "
                         "(nat_name, nat_code) "
                         "values ('Algérienne','dz'), "
                         "('Allemande', 'de'), "
                         "('Américaine', 'us'), "
                         "('Angolaise', 'ao'), "
                         "('Argentine', 'arg'), "
                         "('Arménienne', 'am'), "
                         "('Australienne', 'au'), "
                         "('Autrichienne', 'at'), "
                         "('Bahamienne', 'bs'), "
                         "('Bangladaise', 'bd'), "
                         "('Barbadienne', 'bb'), "
                         "('Belge', 'be'), "
                         "('Beninoise', 'bj'), "
                         "('Bermudienne', 'bm'), "
                         "('Bolivienne', 'bo'), "
                         "('Bosnienne', 'ba'), "
                         "('Britannique', 'en'), "
                         "('Brésilienne', 'br'), "
                         "('Bulgare', 'bg'), "
                         "('Burkinabe', 'bf'), "
                         "('Cambodgienne', 'kh'), "
                         "('Camerounaise', 'cm'), "
                         "('Canadienne', 'ca'), "
                         "('Chilienne', 'cl'), "
                         "('Chinoise', 'zh'), "
                         "('Chypriote', 'cy'), "
                         "('Colombienne', 'co'), "
                         "('Congolaise', 'cd'), "
                         "('Costaricaine', 'cr'), "
                         "('Croate', 'hr'), "
                         "('Cubaine', 'cu'), "
                         "('Danoise', 'da'), "
                         "('Djiboutienne', 'dj'), "
                         "('Dominiquaise', 'do'), "
                         "('Egyptienne', 'eg'), "
                         "('Equatorienne', 'ec'), "
                         "('Espagnole', 'es'), "
                         "('Estonienne', 'et'), "
                         "('Ethiopienne', 'eth'), "
                         "('Fidjienne', 'fj'), "
                         "('Finlandaise', 'fi'), "
                         "('Française', 'fr'), "
                         "('Gambienne', 'gm'), "
                         "('Gambonaise', 'ga'), "
                         "('Ghanéenne', 'gh'), "
                         "('Grecque', 'el'), "
                         "('Grenadienne', 'gd'), "
                         "('Guatémaltèque', 'gt'), "
                         "('Guinéenne', 'gn'), "
                         "('Guyanaise', 'gy'), "
                         "('Haïtienne', 'ht'), "
                         "('Hondurienne', 'hn'), "
                         "('Hongroise', 'hu'), "
                         "('Indienne', 'in'), "
                         "('Indonésienne', 'id'), "
                         "('Irakienne', 'iq'), "
                         "('Iranienne', 'ir'), "
                         "('Irlandaise', 'ie'), "
                         "('Islandaise', 'is'), "
                         "('Israélienne', 'il'), "
                         "('Italienne', 'it'), "
                         "('Ivoirienne', 'ci'), "
                         "('Jamaicaine', 'jm'), "
                         "('Japonaise', 'ja'), "
                         "('Kenyane', 'ke'), "
                         "('Lettone', 'lv'), "
                         "('Libanaise', 'lb'), "
                         "('Libyenne', 'ly'), "
                         "('Libérienne', 'lr'), "
                         "('Lituanne', 'lt'), "
                         "('Luxembourgeoise', 'lu'), "
                         "('Macédoinienne', 'mk'), "
                         "('Malaisienne', 'my'), "
                         "('Malawite', 'mw'), "
                         "('Malgache', 'mg'), "
                         "('Malienne', 'ml'), "
                         "('Marocaine', 'ma'), "
                         "('Mauricienne', 'mu'), "
                         "('Mauritanienne', 'mr'), "
                         "('Mexicaine', 'mx'), "
                         "('Mongole', 'mn'), "
                         "('Mozambicaine', 'mz'), "
                         "('Namibienne', 'na'), "
                         "('Nicaraguayenne', 'ni'), "
                         "('Nigérienne', 'ng'), "
                         "('Norvégienne', 'no'), "
                         "('Néerlandaise', 'nl'), "
                         "('Néo-Zélandaise', 'nz'), "
                         "('Ougandaise', 'ug'), "
                         "('Pakistanaise', 'pk'), "
                         "('Panaméenne', 'pa'), "
                         "('Papouasienne', 'pg'), "
                         "('Paraguayenne', 'py'), "
                         "('Philippine', 'ph'), "
                         "('Polonaise', 'pl'), "
                         "('Portugaise', 'pt'), "
                         "('Péruvienne', 'pe'), "
                         "('Roumaine', 'ro'), "
                         "('Russe', 'ru'), "
                         "('Rwandaise', 'rw'), "
                         "('Salvadorienne', 'svl'), "
                         "('Saoudienne', 'sa'), "
                         "('Serbe', 'rs'), "
                         "('Sierra-Léonaise', 'sl'), "
                         "('Singapourienne', 'sg'), "
                         "('Slovaque','sk'), "
                         "('Slovène', 'si'), "
                         "('Somalienne', 'so'), "
                         "('Soudanaise', 'sd'), "
                         "('Sud-Africaine', 'za'), "
                         "('Sud-Coréenne ', 'kr'), "
                         "('Suisse', 'ch'), "
                         "('Suédoise', 'sv'), "
                         "('Swazie', 'sz'), "
                         "('Syrienne', 'sy'), "
                         "('Sénégalaise', 'sn'), "
                         "('Taiwanaise', 'tw'), "
                         "('Tanzanienne', 'tz'), "
                         "('Tchadienne', 'td'), "
                         "('Tchèque', 'cz'), "
                         "('Thaïlandaise', 'th'), "
                         "('Togolaise', 'tg'), "
                         "('Tunisienne', 'tn'), "
                         "('Turque', 'tr'), "
                         "('Ukrainienne', 'ua'), "
                         "('Uruguayenne', 'uy'), "
                         "('Vietnamienne', 'vn'), "
                         "('Vénézuelienne', 've'), "
                         "('Zambienne', 'zm'), "
                         "('Zimbabwéenne', 'zw')")
        except Exception as err:
            print("ERROR insert into nationality,\n\terr=" + str(err))

    # DROP OLD TABLE
    try:
        conn.execute("drop table ecversion, premieretransition, session, sys_context, sys_editor, sys_editor_publication")
    except Exception as err:
        print("ERROR drop table ecversion, premieretransition, session, sys_context, sys_editor ,sys_editor_publication\n\terr=" + str(err))

    # DROP OLD TABLE
    try:
        conn.execute("drop table sys_dico_data, sys_module, sys_module_acl, sys_project, sys_project_user, "
                     "sys_script, sys_script_error, sys_user, sticker_setting")
    except Exception as err:
        print("ERROR drop table sys_dico_data, sys_module, sys_module_acl, sys_project, sys_project_user, sys_script, sys_script_error, sys_user\n\terr=" + str(err))

    # DROP OLD TABLE
    try:
        conn.execute("drop table sigl_varset_n16s_data, sigl_varset_n16s_data_group, sigl_varset_n16s_data_group_mode, "
                     "sigl_varset_n16s_deleted, sigl_varsetmonitor_data, sigl_varsetmonitor_data_group, "
                     "sigl_varsetmonitor_data_group_mode, sigl_varsetmonitor_deleted")
    except Exception as err:
        print("ERROR drop table like sigl_varset*\n\terr=" + str(err))

    # DROP OLD TABLE
    try:
        conn.execute("drop table sigl_01_data_group, sigl_01_data_group_mode, sigl_02_data_group, "
                     "sigl_02_data_group_mode, sigl_03_data_group, sigl_03_data_group_mode, "
                     "sigl_04_data_group, sigl_04_data_group_mode, sigl_05_05_data_group, sigl_05_05_data_group_mode, "
                     "sigl_05_07_data_group, sigl_05_07_data_group_mode, sigl_05_data_group, sigl_05_data_group_mode, "
                     "sigl_06_data_group, sigl_06_data_group_mode, sigl_07_data_group, sigl_07_data_group_mode, "
                     "sigl_08_data_group, sigl_08_data_group_mode, sigl_09_data_group, sigl_09_data_group_mode, "
                     "sigl_10_data_group, sigl_10_data_group_mode, sigl_11_data_group, sigl_11_data_group_mode, "
                     "sigl_12_data_group, sigl_12_data_group_mode, sigl_13_data_group, sigl_13_data_group_mode, "
                     "sigl_14_data_group, sigl_14_data_group_mode, sigl_15_data_group, sigl_15_data_group_mode, "
                     "sigl_16_data_group, sigl_16_data_group_mode")
    except Exception as err:
        print("ERROR drop table like sigl_XX_data_group and group_mode\n\terr=" + str(err))

    # DROP OLD TABLE
    try:
        conn.execute("drop table sigl_controle_externe_ctrl_resultat__file_data_group, "
                     "sigl_controle_externe_ctrl_resultat__file_data_group_mode, "
                     "sigl_controle_externe_ctrl_resultat_cr__file_data_group, "
                     "sigl_controle_externe_ctrl_resultat_cr__file_data_group_mode, "
                     "sigl_controle_externe_data_group, sigl_controle_externe_data_group_mode, "
                     "sigl_controle_interne_data_group, sigl_controle_interne_data_group_mode, sigl_dico_data_group, "
                     "sigl_dico_data_group_mode, sigl_dicostatus_data_group, sigl_dicostatus_data_group_mode, "
                     "sigl_dos_valisedoc__file_data_group, sigl_dos_valisedoc__file_data_group_mode, "
                     "sigl_equipement_certif_etalonnage__file_data_group, "
                     "sigl_equipement_certif_etalonnage__file_data_group_mode, "
                     "sigl_equipement_contrat_maintenance__file_data_group, "
                     "sigl_equipement_contrat_maintenance__file_data_group_mode, sigl_equipement_data_group, "
                     "sigl_equipement_data_group_mode, sigl_equipement_facture__file_data_group, "
                     "sigl_equipement_facture__file_data_group_mode, "
                     "sigl_equipement_maintenance_preventive__file_data_group, "
                     "sigl_equipement_maintenance_preventive__file_data_group_mode, "
                     "sigl_equipement_pannes__file_data_group, sigl_equipement_pannes__file_data_group_mode, "
                     "sigl_equipement_photo__file_data_group, sigl_equipement_photo__file_data_group_mode, "
                     "sigl_evtlog_data_group, sigl_evtlog_data_group_mode, sigl_file_data_group, "
                     "sigl_file_data_group_mode, sigl_fournisseurs_data_group, sigl_fournisseurs_data_group_mode, "
                     "sigl_laboratoire_data_group, sigl_laboratoire_data_group_mode, "
                     "sigl_laboratoire_organigramme__file_data_group, "
                     "sigl_laboratoire_organigramme__file_data_group_mode, sigl_manuels_data_group, "
                     "sigl_manuels_data_group_mode, sigl_manuels_document__file_data_group, "
                     "sigl_manuels_document__file_data_group_mode, sigl_mgt_qlt_data_group, sigl_mgt_qlt_data_group_mode, "
                     "sigl_non_conf_data_group, sigl_non_conf_data_group_mode, sigl_non_conformite_data_group, "
                     "sigl_non_conformite_data_group_mode, sigl_param_cr_data_group, sigl_param_cr_data_group_mode, "
                     "sigl_param_num_dos_data_group, sigl_param_num_dos_data_group_mode, sigl_pj_auth_flooding, "
                     "sigl_pj_auth_lock, sigl_pj_axis, sigl_pj_group_mode, "
                     "sigl_pj_group_role, sigl_pj_module, sigl_pj_module_acl, sigl_pj_monitoring, "
                     "sigl_pj_monitoring_detail, sigl_pj_old_passwords, sigl_pj_query, sigl_pj_query_var, sigl_pj_random, "
                     "sigl_pj_resource, sigl_pj_resource_settings, sigl_pj_role_acl, "
                     "sigl_pj_token, sigl_pj_varset, sigl_planning_ctrl_ext_data_group, "
                     "sigl_planning_ctrl_ext_data_group_mode, sigl_planning_ctrl_int_data_group, "
                     "sigl_planning_ctrl_int_data_group_mode, sigl_procedures_data_group, "
                     "sigl_procedures_data_group_mode, sigl_procedures_document__file_data_group, "
                     "sigl_procedures_document__file_data_group_mode, sigl_qualite_general_data_group, "
                     "sigl_qualite_general_data_group_mode, sigl_query_data_group, sigl_query_data_group_mode, "
                     "sigl_queryvar_data_group, sigl_queryvar_data_group_mode, sigl_resource_data_group, "
                     "sigl_resource_data_group_mode, sigl_reunion_data_group, sigl_reunion_data_group_mode, "
                     "sigl_reunion_pj__file_data_group, sigl_reunion_pj__file_data_group_mode, sigl_revue_data_group, "
                     "sigl_revue_data_group_mode, sigl_revue_pj__file_data_group, sigl_revue_pj__file_data_group_mode, "
                     "sigl_storage_data_group, sigl_storage_data_group_mode, sigl_user_cv__file_data_group, "
                     "sigl_user_cv__file_data_group_mode, sigl_user_data_group, sigl_user_data_group_mode, "
                     "sigl_user_diplomes__file_data_group, sigl_user_diplomes__file_data_group_mode, "
                     "sigl_user_evaluation__file_data_group, sigl_user_evaluation__file_data_group_mode, "
                     "sigl_user_formations__file_data_group, sigl_user_formations__file_data_group_mode")
    except Exception as err:
        print("ERROR drop table like sigl_[abc]_data_group and group_mode\n\terr=" + str(err))

    # DROP OLD TABLE
    try:
        conn.execute("drop table sigl_non_conf_data, sigl_non_conf_deleted, sigl_non_conf_dico_anal_abs_result_data, "
                     "sigl_non_conf_dico_anal_abs_result_deleted, sigl_non_conf_dico_anal_aliquo_data, "
                     "sigl_non_conf_dico_anal_aliquo_deleted, sigl_non_conf_dico_anal_autre_data, "
                     "sigl_non_conf_dico_anal_autre_deleted, sigl_non_conf_dico_anal_centrif_data, "
                     "sigl_non_conf_dico_anal_centrif_deleted, sigl_non_conf_dico_anal_conserv_data, "
                     "sigl_non_conf_dico_anal_conserv_deleted, sigl_non_conf_dico_anal_crit_de_rep_data, "
                     "sigl_non_conf_dico_anal_crit_de_rep_deleted, sigl_non_conf_dico_anal_ctrl_qualite_ext_data, "
                     "sigl_non_conf_dico_anal_ctrl_qualite_ext_deleted, sigl_non_conf_dico_anal_ctrl_qualite_int_data, "
                     "sigl_non_conf_dico_anal_ctrl_qualite_int_deleted, sigl_non_conf_dico_anal_data, "
                     "sigl_non_conf_dico_anal_deleted, sigl_non_conf_dico_anal_proce_data, "
                     "sigl_non_conf_dico_anal_proce_deleted, sigl_non_conf_dico_anal_trac_data, "
                     "sigl_non_conf_dico_anal_trac_deleted, sigl_non_conf_dico_anal_urg_data, "
                     "sigl_non_conf_dico_anal_urg_deleted, sigl_non_conf_dico_autre_data, "
                     "sigl_non_conf_dico_autre_deleted, sigl_non_conf_dico_eqpm_alarme_data, "
                     "sigl_non_conf_dico_eqpm_alarme_deleted, sigl_non_conf_dico_eqpm_autre_data, "
                     "sigl_non_conf_dico_eqpm_autre_deleted, sigl_non_conf_dico_eqpm_calibr_data, "
                     "sigl_non_conf_dico_eqpm_calibr_deleted, sigl_non_conf_dico_eqpm_data, "
                     "sigl_non_conf_dico_eqpm_deleted, sigl_non_conf_dico_eqpm_etal_data, "
                     "sigl_non_conf_dico_eqpm_etal_deleted, sigl_non_conf_dico_eqpm_panne_data, "
                     "sigl_non_conf_dico_eqpm_panne_deleted, sigl_non_conf_dico_eqpm_proc_data, "
                     "sigl_non_conf_dico_eqpm_proc_deleted, sigl_non_conf_dico_loc_env_autre_data, "
                     "sigl_non_conf_dico_loc_env_autre_deleted, sigl_non_conf_dico_loc_env_coup_eau_data, "
                     "sigl_non_conf_dico_loc_env_coup_eau_deleted, sigl_non_conf_dico_loc_env_coup_elec_data, "
                     "sigl_non_conf_dico_loc_env_coup_elec_deleted, sigl_non_conf_dico_loc_env_data, "
                     "sigl_non_conf_dico_loc_env_dechets_data, sigl_non_conf_dico_loc_env_dechets_deleted, "
                     "sigl_non_conf_dico_loc_env_deleted, sigl_non_conf_dico_loc_env_entretien_data, "
                     "sigl_non_conf_dico_loc_env_entretien_deleted, sigl_non_conf_dico_loc_env_nettoy_labo_data, "
                     "sigl_non_conf_dico_loc_env_nettoy_labo_deleted, sigl_non_conf_dico_post_anal_abs_result_data, "
                     "sigl_non_conf_dico_post_anal_abs_result_deleted, sigl_non_conf_dico_post_anal_autre_data, "
                     "sigl_non_conf_dico_post_anal_autre_deleted, sigl_non_conf_dico_post_anal_conserv_data, "
                     "sigl_non_conf_dico_post_anal_conserv_deleted, sigl_non_conf_dico_post_anal_data, "
                     "sigl_non_conf_dico_post_anal_deleted, sigl_non_conf_dico_post_anal_dos_non_valide_data, "
                     "sigl_non_conf_dico_post_anal_dos_non_valide_deleted, sigl_non_conf_dico_post_anal_err_saisie_data, "
                     "sigl_non_conf_dico_post_anal_err_saisie_deleted, sigl_non_conf_dico_post_anal_interp_data, "
                     "sigl_non_conf_dico_post_anal_interp_deleted, sigl_non_conf_dico_post_anal_presta_conseil_data, "
                     "sigl_non_conf_dico_post_anal_presta_conseil_deleted, sigl_non_conf_dico_post_anal_proc_data, "
                     "sigl_non_conf_dico_post_anal_proc_deleted, sigl_non_conf_dico_post_anal_res_errone_data, "
                     "sigl_non_conf_dico_post_anal_res_errone_deleted, sigl_non_conf_dico_post_anal_valid_part_data, "
                     "sigl_non_conf_dico_post_anal_valid_part_deleted, sigl_non_conf_dico_pre_anal_autre_data, "
                     "sigl_non_conf_dico_pre_anal_autre_deleted, sigl_non_conf_dico_pre_anal_data, "
                     "sigl_non_conf_dico_pre_anal_deleted, sigl_non_conf_dico_pre_anal_dos_pat_data, "
                     "sigl_non_conf_dico_pre_anal_dos_pat_deleted, sigl_non_conf_dico_pre_anal_heure_prel_data, "
                     "sigl_non_conf_dico_pre_anal_heure_prel_deleted, sigl_non_conf_dico_pre_anal_ident_prel_data, "
                     "sigl_non_conf_dico_pre_anal_ident_prel_deleted, sigl_non_conf_dico_pre_anal_oubli_data, "
                     "sigl_non_conf_dico_pre_anal_oubli_deleted, sigl_non_conf_dico_pre_anal_prel_data, "
                     "sigl_non_conf_dico_pre_anal_prel_deleted, sigl_non_conf_dico_pre_anal_respect_proc_data, "
                     "sigl_non_conf_dico_pre_anal_respect_proc_deleted, sigl_non_conf_dico_pre_anal_rsgnmt_clin_data, "
                     "sigl_non_conf_dico_pre_anal_rsgnmt_clin_deleted, sigl_non_conf_dico_pre_anal_tracab_data, "
                     "sigl_non_conf_dico_pre_anal_tracab_deleted, sigl_non_conf_dico_pre_anal_urg_data, "
                     "sigl_non_conf_dico_pre_anal_transp_echant_data, sigl_non_conf_dico_pre_anal_transp_echant_deleted, "
                     "sigl_non_conf_dico_pre_anal_urg_deleted, sigl_non_conf_dico_pre_anal_vol_prel_data, "
                     "sigl_non_conf_dico_pre_anal_vol_prel_deleted, sigl_non_conf_dico_pre_analytique_prescription_data, "
                     "sigl_non_conf_dico_pre_analytique_prescription_deleted, sigl_non_conf_dico_reac_conso_autre_data, "
                     "sigl_non_conf_dico_reac_conso_autre_deleted, sigl_non_conf_dico_reac_conso_data, "
                     "sigl_non_conf_dico_reac_conso_delais_data, sigl_non_conf_dico_reac_conso_delais_deleted, "
                     "sigl_non_conf_dico_reac_conso_deleted, sigl_non_conf_dico_reac_conso_destock_data, "
                     "sigl_non_conf_dico_reac_conso_destock_deleted, sigl_non_conf_dico_reac_conso_reactifs_data, "
                     "sigl_non_conf_dico_reac_conso_reactifs_deleted, sigl_non_conf_dico_reac_conso_recep_data, "
                     "sigl_non_conf_dico_reac_conso_recep_deleted, sigl_non_conf_dico_reac_conso_rupture_data, "
                     "sigl_non_conf_dico_reac_conso_rupture_deleted, sigl_non_conf_dico_reac_conso_tracab_data, "
                     "sigl_non_conf_dico_reac_conso_tracab_deleted, sigl_non_conf_dico_recl_clients_data, "
                     "sigl_non_conf_dico_recl_clients_deleted, sigl_non_conf_dico_rh_abs_data, "
                     "sigl_non_conf_dico_rh_abs_deleted, sigl_non_conf_dico_rh_aes_hyg_secu_data, "
                     "sigl_non_conf_dico_rh_aes_hyg_secu_deleted, sigl_non_conf_dico_rh_autre_data, "
                     "sigl_non_conf_dico_rh_autre_deleted, sigl_non_conf_dico_rh_data, sigl_non_conf_dico_rh_deleted, "
                     "sigl_non_conf_dico_rh_habilit_data, sigl_non_conf_dico_rh_habilit_deleted, "
                     "sigl_non_conf_dico_rh_proc_data, sigl_non_conf_dico_rh_proc_deleted, "
                     "sigl_non_conf_dico_si_autre_data, sigl_non_conf_dico_si_autre_deleted, sigl_non_conf_dico_si_data, "
                     "sigl_non_conf_dico_si_deleted, sigl_non_conf_dico_si_erreur_data, "
                     "sigl_non_conf_dico_si_erreur_deleted, sigl_non_conf_dico_si_no_co_data, "
                     "sigl_non_conf_dico_si_no_co_deleted, sigl_non_conf_dico_si_panne_materiel_data, "
                     "sigl_non_conf_dico_si_panne_materiel_deleted, sigl_non_conf_dico_si_panne_reseau_data, "
                     "sigl_non_conf_dico_si_panne_reseau_deleted, sigl_non_conf_dico_si_panne_systeme_data, "
                     "sigl_non_conf_dico_si_panne_systeme_deleted, sigl_non_conf_dico_ss_trait_autre_data, "
                     "sigl_non_conf_dico_ss_trait_autre_deleted, sigl_non_conf_dico_ss_trait_conservation_data, "
                     "sigl_non_conf_dico_ss_trait_conservation_deleted, sigl_non_conf_dico_ss_trait_data, "
                     "sigl_non_conf_dico_ss_trait_delai_data, sigl_non_conf_dico_ss_trait_delai_deleted, "
                     "sigl_non_conf_dico_ss_trait_deleted, sigl_non_conf_dico_ss_trait_erreur_data, "
                     "sigl_non_conf_dico_ss_trait_erreur_deleted, sigl_non_conf_dico_ss_trait_fact_data, "
                     "sigl_non_conf_dico_ss_trait_fact_deleted, sigl_non_conf_dico_trans_result_acces_result_data, "
                     "sigl_non_conf_dico_trans_result_acces_result_deleted, sigl_non_conf_dico_trans_result_autre_data, "
                     "sigl_non_conf_dico_trans_result_autre_deleted, sigl_non_conf_dico_trans_result_data, "
                     "sigl_non_conf_dico_trans_result_date_rendu_data, "
                     "sigl_non_conf_dico_trans_result_date_rendu_deleted, "
                     "sigl_non_conf_dico_trans_result_delai_non_resp_data, "
                     "sigl_non_conf_dico_trans_result_delai_non_resp_deleted, sigl_non_conf_dico_trans_result_deleted, "
                     "sigl_non_conf_dico_trans_result_non_trans_pat_data, "
                     "sigl_non_conf_dico_trans_result_non_trans_pat_deleted, "
                     "sigl_non_conf_dico_trans_result_non_trans_presc_data, "
                     "sigl_non_conf_dico_trans_result_non_trans_presc_deleted, sigl_non_conf_dico_trans_result_proc_data, "
                     "sigl_non_conf_dico_trans_result_proc_deleted")
    except Exception as err:
        print("ERROR drop table like sigl_non_conf_dico_[abc]_data and deleted\n\terr=" + str(err))

    # DROP OLD TABLE
    try:
        conn.execute("drop table sigl_query_data, sigl_query_deleted, sigl_query_dico_runlevel_data, "
                     "sigl_queryvar_data, sigl_queryvar_deleted, sigl_resource_data, sigl_resource_deleted, "
                     "sigl_storage_deleted, sigl_mgt_qlt_deleted, sigl_evtlog_deleted, sigl_dicostatus_deleted, "
                     "sigl_dicostatus_data, sigl_mgt_qlt_data, sigl_param_cr_deleted, sigl_param_num_dos_deleted, "
                     "sigl_qualite_general_data, sigl_qualite_general_deleted, sigl_revue_data, sigl_revue_deleted, "
                     "sigl_revue_pj__file_data, sigl_revue_pj__file_deleted, sigl_user_cv__file_deleted, "
                     "sigl_user_dico_profil_bis_data, sigl_user_dico_profil_bis_deleted, sigl_user_dico_profil_data, "
                     "sigl_user_dico_profil_deleted, sigl_user_diplomes__file_deleted, "
                     "sigl_user_evaluation__file_deleted, sigl_user_formations__file_deleted")
    except Exception as err:
        print("ERROR drop table like various sigl_...\n\terr=" + str(err))

    print(str(datetime.today()) + " : END of migration v3_2_0_remove_unused_tables revision=5a4e9dbb96dc")


def downgrade():
    pass
