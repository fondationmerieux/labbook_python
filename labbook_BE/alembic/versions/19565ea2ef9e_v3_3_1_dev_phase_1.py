"""v3_3_1_dev_phase_1

Revision ID: 19565ea2ef9e
Revises: a868e3dd7d57
Create Date: 2022-12-16 11:05:34.876659

"""
from alembic import op
from sqlalchemy import text

from datetime import datetime

# revision identifiers, used by Alembic.
revision = '19565ea2ef9e'
down_revision = 'a868e3dd7d57'
branch_labels = None
depends_on = None


def upgrade():
    print("--- " + str(datetime.today()) + "---")
    print("START of migration v3_3_1_dev_phase_1 revision=19565ea2ef9e")

    # Get the current
    conn = op.get_bind()

    # NEW DIRECTORY IN STORAGE
    try:
        import pathlib

        pathlib.Path("/storage/resource/indicator").mkdir(mode=0o777, parents=False, exist_ok=True)
    except Exception as err:
        print("ERROR mkdir -p /storage/resource/indicator,\n\terr=" + str(err))

    # COPY alembic resource indicator
    try:
        from distutils.dir_util import copy_tree

        fromDirectory = "alembic/resource/indicator"
        toDirectory = "/storage/resource/indicator"

        copy_tree(fromDirectory, toDirectory)
    except Exception as err:
        print("ERROR copy alembic resource indicator,\n\terr=" + str(err))

    # UPDATE default sample quotation
    try:
        conn.execute(text("update sigl_05_data set cote_valeur=0.00 "
                          "where cote_unite like 'PB%' or code like 'PB%'"))
    except Exception as err:
        print("ERROR update cote_valeur in sigl_05_data,\n\terr=" + str(err))

    # ADD COLUMN for type in database status
    try:
        conn.execute(text("alter table database_status add column dbs_type varchar(3) not null default 'ANA'"))
    except Exception as err:
        print("ERROR add column dbs_type to database_status,\n\terr=" + str(err))

    # ADD COLUMN for catalog reference of a product
    try:
        conn.execute(text("alter table product_details add column prd_ref_catalog varchar(50) not null default ''"))
    except Exception as err:
        print("ERROR add column prd_ref_catalog to product_details,\n\terr=" + str(err))

    # ADD COLUMN for lessor name of a supply product
    try:
        conn.execute(text("alter table product_supply add column prs_lessor varchar(100) not null default ''"))
    except Exception as err:
        print("ERROR add column prs_lessor to product_supply,\n\terr=" + str(err))

    # ADD NEW USER ROLE
    try:
        conn.execute(text("insert into sigl_pj_role (name, label, type) "
                          "values ('gestionnaire stock', 'Gestionnaire de stock', 'K')"))
    except Exception as err:
        print("ERROR insert into sigl_pj_role (gestionnaire stock),\n\terr=" + str(err))

    # Create table for requesting services
    try:
        conn.execute(text("create table requesting_services("
                          "rqs_ser int not NULL AUTO_INCREMENT,"
                          "rqs_date DATETIME,"
                          "rqs_rank INT default 0,"
                          "rqs_name varchar(255) NOT NULL,"
                          "PRIMARY KEY (rqs_ser),"
                          "INDEX (rqs_rank)) "
                          "character set=utf8"))
    except Exception as err:
        print("ERROR create table requesting_services,\n\terr=" + str(err))

    # Create table for operating units
    try:
        conn.execute(text("create table functionnal_unit("
                          "fun_ser int not NULL AUTO_INCREMENT,"
                          "fun_date DATETIME,"
                          "fun_rank INT default 0,"
                          "fun_name varchar(255) NOT NULL,"
                          "PRIMARY KEY (fun_ser),"
                          "INDEX (fun_rank)) "
                          "character set=utf8"))
    except Exception as err:
        print("ERROR create table functionnal_unit,\n\terr=" + str(err))

    # Create table for functionnal_unit_link
    try:
        conn.execute(text("create table functionnal_unit_link("
                          "ful_ser int not NULL AUTO_INCREMENT,"
                          "ful_date DATETIME,"
                          "ful_fun INT NOT NULL,"
                          "ful_ref INT NOT NULL,"  # serial of user or analysis family
                          "ful_type varchar(1) NOT NULL,"  # 'U'ser or analysis 'F'amily
                          "PRIMARY KEY (ful_ser),"
                          "INDEX (ful_fun), INDEX (ful_ref), INDEX (ful_type)) "
                          "character set=utf8"))
    except Exception as err:
        print("ERROR create table functionnal_unit_link,\n\terr=" + str(err))

    # Create table for stock setting
    try:
        conn.execute(text("create table stock_setting("
                          "sos_ser int not NULL AUTO_INCREMENT,"
                          "sos_date DATETIME,"
                          "sos_expir_oblig varchar(1) NOT NULL default 'Y',"
                          "sos_expir_warning INT NOT NULL default 14,"
                          "sos_expir_alert INT NOT NULL default 0,"
                          "PRIMARY KEY (sos_ser))"
                          "character set=utf8"))
    except Exception as err:
        print("ERROR create table stock_setting,\n\terr=" + str(err))

    # ADD default stock setting
    try:
        conn.execute(text("insert into stock_setting "
                          "(sos_date, sos_expir_oblig, sos_expir_warning, sos_expir_alert) "
                          "values (NOW(), 'Y', 14, 0)"))
    except Exception as err:
        print("ERROR insert default stock_setting,\n\terr=" + str(err))

    # Create table for list of comment
    try:
        conn.execute(text("create table list_comment("
                          "lic_ser int not NULL AUTO_INCREMENT,"
                          "lic_date DATETIME,"
                          "lic_ref INT NOT NULL,"  # serial of item, like id_data from sigl_equipement_data
                          "lic_type varchar(1) NOT NULL,"  # 'E'quipment
                          "lic_sub_type varchar(1) NOT NULL,"  # 'B'reakdown, 'M'aintenance
                          "lic_user INT NOT NULL,"
                          "lic_comm text NOT NULL,"
                          "PRIMARY KEY (lic_ser), "
                          "INDEX (lic_ref), INDEX (lic_type), INDEX (lic_sub_type), INDEX (lic_user))"
                          "character set=utf8"))
    except Exception as err:
        print("ERROR create table list_comment,\n\terr=" + str(err))

    # ADD old entry in pannes fields
    try:
        conn.execute(text("insert into list_comment (lic_date, lic_type, lic_sub_type, lic_ref, lic_user, lic_comm) "
                          "select NOW(), 'E', 'B', id_data, id_owner, pannes from sigl_equipement_data "
                          "where pannes is not null and pannes != ''"))
    except Exception as err:
        print("ERROR insert old entry from sigl_equipement_data.pannes in list_comment,\n\terr=" + str(err))

    # ADD old entry in maintenance_preventive fields
    try:
        conn.execute(text("insert into list_comment (lic_date, lic_type, lic_sub_type, lic_ref, lic_user, lic_comm) "
                          "select NOW(), 'E', 'M', id_data, id_owner, maintenance_preventive from sigl_equipement_data "
                          "where maintenance_preventive is not null and maintenance_preventive != ''"))
    except Exception as err:
        print("ERROR insert old entry from sigl_equipement_data.maintenance_preventive in list_comment,\n\terr=" + str(err))

    # DROP COLUMN TO sigl_dico_data TABLE
    try:
        conn.execute(text("alter table sigl_dico_data drop column dico_id"))
    except Exception as err:
        print("ERROR drop column dico_id to sigl_dico_data,\n\terr=" + str(err))

    # DROP COLUMN TO sigl_dico_data TABLE
    try:
        conn.execute(text("alter table sigl_dico_data drop column dico_value_id"))
    except Exception as err:
        print("ERROR drop column dico_value_id to sigl_dico_data,\n\terr=" + str(err))

    # DROP COLUMN TO sigl_dico_data TABLE
    try:
        conn.execute(text("alter table sigl_dico_data drop column archived"))
    except Exception as err:
        print("ERROR drop column archived to sigl_dico_data,\n\terr=" + str(err))

    # DELETE duplicates type_resultat TO sigl_dico_data TABLE
    try:
        conn.execute(text("delete from sigl_dico_data where id_data in (1126,1141,1132,602,1125,1136,1139,1140) and "
                          "dico_name='type_resultat'"))
    except Exception as err:
        print("ERROR delete id_data in (1126,1141,1132,602,1125,1136,1139,1140) to sigl_dico_data,\n\terr=" + str(err))

    # UPDATE type_resultat in sigl_07_data to remove duplicates of type_resultat
    # 1127 => 585
    try:
        conn.execute(text("update sigl_07_data set type_resultat=585 where type_resultat=1127"))

        conn.execute(text("delete from sigl_dico_data where id_data=1127"))
    except Exception as err:
        print("ERROR update type_resultat 1127 to 585 in sigl_07_data then delete in sigl_dico_data,\n\terr=" + str(err))

    # 1128 => 586
    try:
        conn.execute(text("update sigl_07_data set type_resultat=586 where type_resultat=1128"))

        conn.execute(text("delete from sigl_dico_data where id_data=1128"))
    except Exception as err:
        print("ERROR update type_resultat 1128 to 586 in sigl_07_data then delete in sigl_dico_data,\n\terr=" + str(err))

    # 1129 => 588
    try:
        conn.execute(text("update sigl_07_data set type_resultat=588 where type_resultat=1129"))

        conn.execute(text("delete from sigl_dico_data where id_data=1129"))
    except Exception as err:
        print("ERROR update type_resultat 1129 to 588 in sigl_07_data then delete in sigl_dico_data,\n\terr=" + str(err))

    # 1130 => 589
    try:
        conn.execute(text("update sigl_07_data set type_resultat=589 where type_resultat=1130"))

        conn.execute(text("delete from sigl_dico_data where id_data=1130"))
    except Exception as err:
        print("ERROR update type_resultat 1130 to 589 in sigl_07_data then delete in sigl_dico_data,\n\terr=" + str(err))

    # 1137 => 617
    try:
        conn.execute(text("update sigl_07_data set type_resultat=617 where type_resultat=1137"))

        conn.execute(text("delete from sigl_dico_data where id_data=1137"))
    except Exception as err:
        print("ERROR update type_resultat 1137 to 617 in sigl_07_data then delete in sigl_dico_data,\n\terr=" + str(err))

    # 1131 => 591
    try:
        conn.execute(text("update sigl_07_data set type_resultat=591 where type_resultat=1131"))

        conn.execute(text("delete from sigl_dico_data where id_data=1131"))
    except Exception as err:
        print("ERROR update type_resultat 1131 to 591 in sigl_07_data then delete in sigl_dico_data,\n\terr=" + str(err))

    # 1133 => 599
    try:
        conn.execute(text("update sigl_07_data set type_resultat=599 where type_resultat=1133"))

        conn.execute(text("delete from sigl_dico_data where id_data=1133"))
    except Exception as err:
        print("ERROR update type_resultat 1133 to 599 in sigl_07_data then delete in sigl_dico_data,\n\terr=" + str(err))

    # 1134 => 600
    try:
        conn.execute(text("update sigl_07_data set type_resultat=600 where type_resultat=1134"))

        conn.execute(text("delete from sigl_dico_data where id_data=1134"))
    except Exception as err:
        print("ERROR update type_resultat 1134 to 600 in sigl_07_data then delete in sigl_dico_data,\n\terr=" + str(err))

    print(str(datetime.today()) + " : END of migration v3_3_1_dev_phase_1 revision=19565ea2ef9e")


def downgrade():
    pass
