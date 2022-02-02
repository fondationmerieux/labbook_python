# -*- coding:utf-8 -*-
"""v3_2_1_fix_analysis_repo

Revision ID: 59d46fab5f54
Revises: 5a4e9dbb96dc
Create Date: 2021-12-20 10:52:22.584847

"""
from alembic import op

from datetime import datetime

# revision identifiers, used by Alembic.
revision = '59d46fab5f54'
down_revision = '5a4e9dbb96dc'
branch_labels = None
depends_on = None


def upgrade():
    print("--- " + str(datetime.today()) + "---")
    print("START of migration v3_2_1_fix_analysis_repo revision=59d46fab5f54")

    # Get the current
    conn = op.get_bind()

    # UPDATE wrong minimal value for B008
    try:
        conn.execute("update sigl_07_data set normal_min='2.15' "
                     "where normal_min='2. 15' ")
    except Exception as err:
        print("ERROR update normal_min for B008,\n\terr=" + str(err))

    # NEW TABLE for load list of zip code city and region
    try:
        conn.execute("create table zip_city ("
                     "zic_ser int not NULL AUTO_INCREMENT,"
                     "zic_date datetime,"
                     "zic_zip varchar(10),"
                     "zic_city varchar(255),"
                     "PRIMARY KEY (zic_ser),"
                     "INDEX (zic_zip), INDEX (zic_city)) character set=utf8")
    except Exception as err:
        print("ERROR create table zip_city,\n\terr=" + str(err))

    # NEW TABLE for quality control
    try:
        conn.execute("create table control_quality ("
                     "ctq_ser int not NULL AUTO_INCREMENT,"
                     "ctq_date datetime,"
                     "ctq_type_ctrl varchar(10),"
                     "ctq_type_val varchar(10),"
                     "ctq_name varchar(255),"
                     "ctq_eqp int,"
                     "PRIMARY KEY (ctq_ser),"
                     "INDEX (ctq_type_ctrl), INDEX (ctq_name), INDEX (ctq_eqp), INDEX (ctq_type_val)) character set=utf8")
    except Exception as err:
        print("ERROR create table quality_control,\n\terr=" + str(err))

    # NEW TABLE for value of internal control
    try:
        conn.execute("create table control_internal ("
                     "cti_ser int not NULL AUTO_INCREMENT,"
                     "cti_ctq int not NULL,"
                     "cti_date datetime,"
                     "cti_type varchar(10),"
                     "cti_target varchar(255),"
                     "cti_conform varchar(10),"
                     "cti_comment varchar(255),"
                     "PRIMARY KEY (cti_ser),"
                     "INDEX (cti_type), INDEX (cti_ctq)) character set=utf8")
    except Exception as err:
        print("ERROR create table control_internal,\n\terr=" + str(err))

    # NEW TABLE for value of external control
    try:
        conn.execute("create table control_external ("
                     "cte_ser int not NULL AUTO_INCREMENT,"
                     "cte_ctq int not NULL,"
                     "cte_date datetime,"
                     "cte_type varchar(10),"
                     "cte_organizer varchar(255),"
                     "cte_contact varchar(255),"
                     "cte_result varchar(255),"
                     "cte_comment varchar(255),"
                     "PRIMARY KEY (cte_ser),"
                     "INDEX (cte_type), INDEX (cte_ctq)) character set=utf8")
    except Exception as err:
        print("ERROR create table control_external,\n\terr=" + str(err))

    # DROP OLD TABLE
    try:
        conn.execute("drop table sigl_controle_externe_ctrl_resultat__file_data, sigl_controle_externe_data, "
                     "sigl_controle_externe_ctrl_resultat__file_deleted, sigl_controle_externe_deleted, "
                     "sigl_controle_externe_ctrl_resultat_cr__file_deleted, sigl_controle_interne_data, "
                     "sigl_controle_interne_deleted")
    except Exception as err:
        print("ERROR drop table like sigl_control_...\n\terr=" + str(err))

    # DROP COLUMN TO Analysis TABLE
    try:
        conn.execute("alter table sigl_05_data drop column paillasse")
    except Exception as err:
        print("ERROR drop column paillasse to sigl_05_data,\n\terr=" + str(err))

    # DROP COLUMN TO Patient TABLE
    try:
        conn.execute("alter table sigl_03_data drop column ethnie")
    except Exception as err:
        print("ERROR drop column ethnie to sigl_03_data,\n\terr=" + str(err))

    # DROP COLUMN TO Patient TABLE
    try:
        conn.execute("alter table sigl_03_data drop column annee_naiss")
    except Exception as err:
        print("ERROR drop column annee_naiss to sigl_03_data,\n\terr=" + str(err))

    # DROP COLUMN TO Patient TABLE
    try:
        conn.execute("alter table sigl_03_data drop column mois_naiss")
    except Exception as err:
        print("ERROR drop column mois_naiss to sigl_03_data,\n\terr=" + str(err))

    # DROP COLUMN TO Patient TABLE
    try:
        conn.execute("alter table sigl_03_data drop column semaine_naiss")
    except Exception as err:
        print("ERROR drop column semaine_naiss to sigl_03_data,\n\terr=" + str(err))

    # REPLACE old system of id_group by id_user in id_owner and role_type instrad of id_role
    # New user type
    try:
        conn.execute("alter table sigl_pj_role add column type varchar(10)")
    except Exception as err:
        print("ERROR add column type to sigl_pj_role,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_pj_role set type='A' where name='admin'")
    except Exception as err:
        print("ERROR update sigl_pj_role set type='A' where name='admin',\n\terr=" + str(err))

    try:
        conn.execute("update sigl_pj_role set type='B' where name='biologiste'")
    except Exception as err:
        print("ERROR update sigl_pj_role set type='B' where name='biologiste',\n\terr=" + str(err))

    try:
        conn.execute("update sigl_pj_role set type='T' where name='technicien'")
    except Exception as err:
        print("ERROR update sigl_pj_role set type='T' where name='technicien',\n\terr=" + str(err))

    try:
        conn.execute("update sigl_pj_role set type='S' where name='secretaire'")
    except Exception as err:
        print("ERROR update sigl_pj_role set type='S' where name='secretaire',\n\terr=" + str(err))

    try:
        conn.execute("update sigl_pj_role set type='TA' where name='technicien avance'")
    except Exception as err:
        print("ERROR update sigl_pj_role set type='TA' where name='technicien avance',\n\terr=" + str(err))

    try:
        conn.execute("update sigl_pj_role set type='TQ' where name='technicien qualiticien'")
    except Exception as err:
        print("ERROR update sigl_pj_role set type='TQ' where name='technicien qualiticien',\n\terr=" + str(err))

    try:
        conn.execute("update sigl_pj_role set type='SA' where name='secretaire avancee'")
    except Exception as err:
        print("ERROR update sigl_pj_role set type='SA' where name='secretaire avancee',\n\terr=" + str(err))

    try:
        conn.execute("update sigl_pj_role set type='Q' where name='qualiticien'")
    except Exception as err:
        print("ERROR update sigl_pj_role set type='Q' where name='qualiticien',\n\terr=" + str(err))

    try:
        conn.execute("update sigl_pj_role set type='P' where name='prescripteur'")
    except Exception as err:
        print("ERROR update sigl_pj_role set type='P' where name='prescripteur',\n\terr=" + str(err))

    try:
        conn.execute("alter table sigl_user_data add column role_type varchar(10)")
    except Exception as err:
        print("ERROR add column role_type to sigl_user_data,\n\terr=" + str(err))

    # Replace id_role by role_type for users
    try:
        conn.execute("update sigl_user_data set role_type='A' where role_type is NULL and id_group in "
                     "(select id_group from sigl_pj_group_link where id_role=1)")
    except Exception as err:
        print("ERROR update id_role=1 by role_type='A' in sigl_user_data,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_user_data set role_type='B' where role_type is NULL and id_group in "
                     "(select id_group from sigl_pj_group_link where id_role=2)")
    except Exception as err:
        print("ERROR update id_role=2 by role_type='B' in sigl_user_data,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_user_data set role_type='T' where role_type is NULL and id_group in "
                     "(select id_group from sigl_pj_group_link where id_role=3)")
    except Exception as err:
        print("ERROR update id_role=3 by role_type='T' in sigl_user_data,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_user_data set role_type='S' where role_type is NULL and id_group in "
                     "(select id_group from sigl_pj_group_link where id_role=4)")
    except Exception as err:
        print("ERROR update id_role=4 by role_type='S' in sigl_user_data,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_user_data set role_type='TA' where role_type is NULL and id_group in "
                     "(select id_group from sigl_pj_group_link where id_role=5)")
    except Exception as err:
        print("ERROR update id_role=5 by role_type='TA' in sigl_user_data,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_user_data set role_type='TQ' where role_type is NULL and id_group in "
                     "(select id_group from sigl_pj_group_link where id_role=6)")
    except Exception as err:
        print("ERROR update id_role=6 by role_type='TQ' in sigl_user_data,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_user_data set role_type='SA' where role_type is NULL and id_group in "
                     "(select id_group from sigl_pj_group_link where id_role=7)")
    except Exception as err:
        print("ERROR update id_role=7 by role_type='SA' in sigl_user_data,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_user_data set role_type='Q' where role_type is NULL and id_group in "
                     "(select id_group from sigl_pj_group_link where id_role=8)")
    except Exception as err:
        print("ERROR update id_role=8 by role_type='Q' in sigl_user_data,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_user_data set role_type='P' where role_type is NULL and id_group in "
                     "(select id_group from sigl_pj_group_link where id_role=9)")
    except Exception as err:
        print("ERROR update id_role=9 by role_type='P' in sigl_user_data,\n\terr=" + str(err))

    # Replace id_group by id_user in all id_owner column
    try:
        conn.execute("update sigl_01_data as ref inner join sigl_user_data as user on "
                     "(ref.id_owner=user.id_group) set ref.id_owner=user.id_data")
    except Exception as err:
        print("ERROR replace id_owner by id_user in sigl_01_data,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_01_deleted as ref inner join sigl_user_data as user on "
                     "(ref.id_owner=user.id_group) set ref.id_owner=user.id_data")
    except Exception as err:
        print("ERROR replace id_owner by id_user in sigl_01_deleted,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_01_dico_analyse_data as ref inner join sigl_user_data as user on "
                     "(ref.id_owner=user.id_group) set ref.id_owner=user.id_data")
    except Exception as err:
        print("ERROR replace id_owner by id_user in sigl_01_dico_analyse_data,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_01_dico_analyse_deleted as ref inner join sigl_user_data as user on "
                     "(ref.id_owner=user.id_group) set ref.id_owner=user.id_data")
    except Exception as err:
        print("ERROR replace id_owner by id_user in sigl_01_dico_analyse_deleted,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_02_data as ref inner join sigl_user_data as user on "
                     "(ref.id_owner=user.id_group) set ref.id_owner=user.id_data")
    except Exception as err:
        print("ERROR replace id_owner by id_user in sigl_02_data,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_02_deleted as ref inner join sigl_user_data as user on "
                     "(ref.id_owner=user.id_group) set ref.id_owner=user.id_data")
    except Exception as err:
        print("ERROR replace id_owner by id_user in sigl_02_deleted,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_03_data as ref inner join sigl_user_data as user on "
                     "(ref.id_owner=user.id_group) set ref.id_owner=user.id_data")
    except Exception as err:
        print("ERROR replace id_owner by id_user in sigl_03_data,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_04_data as ref inner join sigl_user_data as user on "
                     "(ref.id_owner=user.id_group) set ref.id_owner=user.id_data")
    except Exception as err:
        print("ERROR replace id_owner by id_user in sigl_04_data,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_04_deleted as ref inner join sigl_user_data as user on "
                     "(ref.id_owner=user.id_group) set ref.id_owner=user.id_data")
    except Exception as err:
        print("ERROR replace id_owner by id_user in sigl_04_deleted,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_05_data as ref inner join sigl_user_data as user on "
                     "(ref.id_owner=user.id_group) set ref.id_owner=user.id_data")
    except Exception as err:
        print("ERROR replace id_owner by id_user in sigl_05_data,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_05_07_data as ref inner join sigl_user_data as user on "
                     "(ref.id_owner=user.id_group) set ref.id_owner=user.id_data")
    except Exception as err:
        print("ERROR replace id_owner by id_user in sigl_05_07_data,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_06_data as ref inner join sigl_user_data as user on "
                     "(ref.id_owner=user.id_group) set ref.id_owner=user.id_data")
    except Exception as err:
        print("ERROR replace id_owner by id_user in sigl_06_data,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_07_data as ref inner join sigl_user_data as user on "
                     "(ref.id_owner=user.id_group) set ref.id_owner=user.id_data")
    except Exception as err:
        print("ERROR replace id_owner by id_user in sigl_07_data,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_08_data as ref inner join sigl_user_data as user on "
                     "(ref.id_owner=user.id_group) set ref.id_owner=user.id_data")
    except Exception as err:
        print("ERROR replace id_owner by id_user in sigl_08_data,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_09_data as ref inner join sigl_user_data as user on "
                     "(ref.id_owner=user.id_group) set ref.id_owner=user.id_data")
    except Exception as err:
        print("ERROR replace id_owner by id_user in sigl_09_data,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_09_deleted as ref inner join sigl_user_data as user on "
                     "(ref.id_owner=user.id_group) set ref.id_owner=user.id_data")
    except Exception as err:
        print("ERROR replace id_owner by id_user in sigl_09_deleted,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_10_data as ref inner join sigl_user_data as user on "
                     "(ref.id_owner=user.id_group) set ref.id_owner=user.id_data")
    except Exception as err:
        print("ERROR replace id_owner by id_user in sigl_10_data,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_10_deleted as ref inner join sigl_user_data as user on "
                     "(ref.id_owner=user.id_group) set ref.id_owner=user.id_data")
    except Exception as err:
        print("ERROR replace id_owner by id_user in sigl_10_deleted,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_11_data as ref inner join sigl_user_data as user on "
                     "(ref.id_owner=user.id_group) set ref.id_owner=user.id_data")
    except Exception as err:
        print("ERROR replace id_owner by id_user in sigl_11_data,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_11_deleted as ref inner join sigl_user_data as user on "
                     "(ref.id_owner=user.id_group) set ref.id_owner=user.id_data")
    except Exception as err:
        print("ERROR replace id_owner by id_user in sigl_11_deleted,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_12_data as ref inner join sigl_user_data as user on "
                     "(ref.id_owner=user.id_group) set ref.id_owner=user.id_data")
    except Exception as err:
        print("ERROR replace id_owner by id_user in sigl_12_data,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_12_deleted as ref inner join sigl_user_data as user on "
                     "(ref.id_owner=user.id_group) set ref.id_owner=user.id_data")
    except Exception as err:
        print("ERROR replace id_owner by id_user in sigl_12_deleted,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_14_data as ref inner join sigl_user_data as user on "
                     "(ref.id_owner=user.id_group) set ref.id_owner=user.id_data")
    except Exception as err:
        print("ERROR replace id_owner by id_user in sigl_14_data,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_15_data as ref inner join sigl_user_data as user on "
                     "(ref.id_owner=user.id_group) set ref.id_owner=user.id_data")
    except Exception as err:
        print("ERROR replace id_owner by id_user in sigl_15_data,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_dico_data as ref inner join sigl_user_data as user on "
                     "(ref.id_owner=user.id_group) set ref.id_owner=user.id_data")
    except Exception as err:
        print("ERROR replace id_owner by id_user in sigl_dico_data,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_controle_externe_ctrl_resultat_cr__file_data as ref inner join sigl_user_data as user on "
                     "(ref.id_owner=user.id_group) set ref.id_owner=user.id_data")
    except Exception as err:
        print("ERROR replace id_owner by id_user in sigl_controle_externe_ctrl_resultat_cr__file_data,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_dos_valisedoc__file_data as ref inner join sigl_user_data as user on "
                     "(ref.id_owner=user.id_group) set ref.id_owner=user.id_data")
    except Exception as err:
        print("ERROR replace id_owner by id_user in sigl_dos_valisedoc__file_data,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_dos_valisedoc__file_deleted as ref inner join sigl_user_data as user on "
                     "(ref.id_owner=user.id_group) set ref.id_owner=user.id_data")
    except Exception as err:
        print("ERROR replace id_owner by id_user in sigl_dos_valisedoc__file_deleted,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_equipement_certif_etalonnage__file_data as ref inner join sigl_user_data as user on "
                     "(ref.id_owner=user.id_group) set ref.id_owner=user.id_data")
    except Exception as err:
        print("ERROR replace id_owner by id_user in sigl_equipement_certif_etalonnage__file_data,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_equipement_contrat_maintenance__file_data as ref inner join sigl_user_data as user on "
                     "(ref.id_owner=user.id_group) set ref.id_owner=user.id_data")
    except Exception as err:
        print("ERROR replace id_owner by id_user in sigl_equipement_contrat_maintenance__file_data,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_equipement_data as ref inner join sigl_user_data as user on "
                     "(ref.id_owner=user.id_group) set ref.id_owner=user.id_data")
    except Exception as err:
        print("ERROR replace id_owner by id_user in sigl_equipement_data,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_equipement_facture__file_data as ref inner join sigl_user_data as user on "
                     "(ref.id_owner=user.id_group) set ref.id_owner=user.id_data")
    except Exception as err:
        print("ERROR replace id_owner by id_user in sigl_equipement_facture__file_data,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_equipement_maintenance_preventive__file_data as ref inner join sigl_user_data as user on "
                     "(ref.id_owner=user.id_group) set ref.id_owner=user.id_data")
    except Exception as err:
        print("ERROR replace id_owner by id_user in sigl_equipement_maintenance_preventive__file_data,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_equipement_pannes__file_data as ref inner join sigl_user_data as user on "
                     "(ref.id_owner=user.id_group) set ref.id_owner=user.id_data")
    except Exception as err:
        print("ERROR replace id_owner by id_user in sigl_equipement_pannes__file_data,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_equipement_photo__file_data as ref inner join sigl_user_data as user on "
                     "(ref.id_owner=user.id_group) set ref.id_owner=user.id_data")
    except Exception as err:
        print("ERROR replace id_owner by id_user in sigl_equipement_photo__file_data,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_evtlog_data as ref inner join sigl_user_data as user on "
                     "(ref.id_owner=user.id_group) set ref.id_owner=user.id_data")
    except Exception as err:
        print("ERROR replace id_owner by id_user in sigl_evtlog_data,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_file_data as ref inner join sigl_user_data as user on "
                     "(ref.id_owner=user.id_group) set ref.id_owner=user.id_data")
    except Exception as err:
        print("ERROR replace id_owner by id_user in sigl_file_data,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_fournisseurs_data as ref inner join sigl_user_data as user on "
                     "(ref.id_owner=user.id_group) set ref.id_owner=user.id_data")
    except Exception as err:
        print("ERROR replace id_owner by id_user in sigl_fournisseurs_data,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_laboratoire_organigramme__file_data as ref inner join sigl_user_data as user on "
                     "(ref.id_owner=user.id_group) set ref.id_owner=user.id_data")
    except Exception as err:
        print("ERROR replace id_owner by id_user in sigl_laboratoire_organigramme__file_data,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_manuels_data as ref inner join sigl_user_data as user on "
                     "(ref.id_owner=user.id_group) set ref.id_owner=user.id_data")
    except Exception as err:
        print("ERROR replace id_owner by id_user in sigl_manuels_data,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_manuels_document__file_data as ref inner join sigl_user_data as user on "
                     "(ref.id_owner=user.id_group) set ref.id_owner=user.id_data")
    except Exception as err:
        print("ERROR replace id_owner by id_user in sigl_manuels_document__file_data,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_non_conformite_data as ref inner join sigl_user_data as user on "
                     "(ref.id_owner=user.id_group) set ref.id_owner=user.id_data")
    except Exception as err:
        print("ERROR replace id_owner by id_user in sigl_non_conformite_data,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_param_cr_data as ref inner join sigl_user_data as user on "
                     "(ref.id_owner=user.id_group) set ref.id_owner=user.id_data")
    except Exception as err:
        print("ERROR replace id_owner by id_user in sigl_param_cr_data,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_param_num_dos_data as ref inner join sigl_user_data as user on "
                     "(ref.id_owner=user.id_group) set ref.id_owner=user.id_data")
    except Exception as err:
        print("ERROR replace id_owner by id_user in sigl_param_num_dos_data,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_procedures_data as ref inner join sigl_user_data as user on "
                     "(ref.id_owner=user.id_group) set ref.id_owner=user.id_data")
    except Exception as err:
        print("ERROR replace id_owner by id_user in sigl_procedures_data,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_procedures_document__file_data as ref inner join sigl_user_data as user on "
                     "(ref.id_owner=user.id_group) set ref.id_owner=user.id_data")
    except Exception as err:
        print("ERROR replace id_owner by id_user in sigl_procedures_document__file_data,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_reunion_data as ref inner join sigl_user_data as user on "
                     "(ref.id_owner=user.id_group) set ref.id_owner=user.id_data")
    except Exception as err:
        print("ERROR replace id_owner by id_user in sigl_reunion_data,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_reunion_pj__file_data as ref inner join sigl_user_data as user on "
                     "(ref.id_owner=user.id_group) set ref.id_owner=user.id_data")
    except Exception as err:
        print("ERROR replace id_owner by id_user in sigl_reunion_pj__file_data,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_storage_data as ref inner join sigl_user_data as user on "
                     "(ref.id_owner=user.id_group) set ref.id_owner=user.id_data")
    except Exception as err:
        print("ERROR replace id_owner by id_user in sigl_storage_data,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_user_cv__file_data as ref inner join sigl_user_data as user on "
                     "(ref.id_owner=user.id_group) set ref.id_owner=user.id_data")
    except Exception as err:
        print("ERROR replace id_owner by id_user in sigl_user_cv__file_data,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_user_data as ref inner join sigl_user_data as user on "
                     "(ref.id_owner=user.id_group) set ref.id_owner=user.id_data")
    except Exception as err:
        print("ERROR replace id_owner by id_user in sigl_user_data,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_user_diplomes__file_data as ref inner join sigl_user_data as user on "
                     "(ref.id_owner=user.id_group) set ref.id_owner=user.id_data")
    except Exception as err:
        print("ERROR replace id_owner by id_user in sigl_user_diplomes__file_data,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_user_evaluation__file_data as ref inner join sigl_user_data as user on "
                     "(ref.id_owner=user.id_group) set ref.id_owner=user.id_data")
    except Exception as err:
        print("ERROR replace id_owner by id_user in sigl_user_evaluation__file_data,\n\terr=" + str(err))

    try:
        conn.execute("update sigl_user_formations__file_data as ref inner join sigl_user_data as user on "
                     "(ref.id_owner=user.id_group) set ref.id_owner=user.id_data")
    except Exception as err:
        print("ERROR replace id_owner by id_user in sigl_user_formations__file_data,\n\terr=" + str(err))

    # Drop column and table useless
    try:
        conn.execute("alter table sigl_03_data drop column id_group")
    except Exception as err:
        print("ERROR alter table sigl_03_data drop column id_group,\n\terr=" + str(err))

    try:
        conn.execute("drop table sigl_pj_group_link, sigl_pj_group")
    except Exception as err:
        print("ERROR drop table sigl_pj_group_link, sigl_pj_group,\n\terr=" + str(err))

    # update syntax of one role label
    try:
        conn.execute("update sigl_pj_role set label='Secrétaire avancée' where type='SA'")
    except Exception as err:
        print("ERROR update sigl_pj_role set label='Secrétaire avancée' where type='SA',\n\terr=" + str(err))

    print(str(datetime.today()) + " : END of migration v3_2_1_fix_analysis_repo revision=59d46fab5f54")


def downgrade():
    pass
