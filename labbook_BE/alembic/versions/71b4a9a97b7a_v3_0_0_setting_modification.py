# -*- coding:utf-8 -*-
"""v3.0.0_setting_modification

Revision ID: 71b4a9a97b7a
Revises: 75a90d6bfa9f
Create Date: 2021-02-03 10:46:43.668497

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '71b4a9a97b7a'
down_revision = '75a90d6bfa9f'
branch_labels = None
depends_on = None


def upgrade():
    # Get the current
    conn = op.get_bind()

    # AGE INTERVAL TABLE
    try:
        # Create table for age interval setting
        conn.execute("create table age_interval_setting("
                     "ais_ser int not NULL AUTO_INCREMENT,"
                     "ais_rank int not NULL,"
                     "ais_lower_bound INT,"
                     "ais_upper_bound INT,"
                     "PRIMARY KEY (ais_ser))")
    except:
        print("ERROR create table age_interval_setting")
    else:
        try:
            # insert 4 age interval by default
            conn.execute("insert into age_interval_setting (ais_rank, ais_upper_bound) values (0, 5)")
            conn.execute("insert into age_interval_setting (ais_rank, ais_lower_bound, ais_upper_bound) values (1, 5, 20)")
            conn.execute("insert into age_interval_setting (ais_rank, ais_lower_bound, ais_upper_bound) values (2, 20, 40)")
            conn.execute("insert into age_interval_setting (ais_rank, ais_lower_bound) values (3, 40)")
        except:
            print("ERROR insert default value for age_interval_setting")

    # STICKER TABLE
    try:
        # Create table for sticker_setting
        conn.execute("create table sticker_setting("
                     "sts_ser int not NULL AUTO_INCREMENT,"
                     "sts_margin_top int not NULL,"
                     "sts_margin_bottom int not NULL,"
                     "sts_margin_left int not NULL,"
                     "sts_margin_right int not NULL,"
                     "sts_height int not NULL,"
                     "sts_width int not NULL,"
                     "PRIMARY KEY (sts_ser))")
    except:
        print("ERROR create table sticker_setting")
    else:
        try:
            # insert a default format for stickers_setting
            conn.execute("insert into sticker_setting "
                         "(sts_margin_top, sts_margin_bottom, sts_margin_left, sts_margin_right, sts_height, sts_width) "
                         "values (10, 10, 10, 10, 15, 60)")
        except:
            print("ERROR insert default value for sticker_setting")

    # BACKUP TABLE
    try:
        # Create table for backup setting
        conn.execute("create table backup_setting("
                     "bks_ser int not NULL AUTO_INCREMENT,"
                     "bks_pwd varchar(50) NOT NULL,"
                     "bks_start_time TIME NOT NULL,"
                     "PRIMARY KEY (bks_ser))")
    except:
        print("ERROR create table backup_setting")
    else:
        try:
            # insert backup setting by default
            conn.execute("insert into backup_setting (bks_pwd, bks_start_time) values ('', '12:00:00')")
        except:
            print("ERROR insert default value for backup_setting")

    # UPDATE MANUAL
    try:
        # update id_storage for sigl_file_data
        conn.execute("update sigl_file_data set id_storage=1 where id_storage is null")
    except:
        print("ERROR update sigl_file_data set id_storage=1 where id_storage is null")

    # wrong character in manual table
    try:
        # update id_storage for sigl_manuels_data
        conn.execute("update sigl_manuels_data"
                     "set titre='Guide pratique sur l\'application du Règlement relatif au transport des matières infectieuses 2013-2014'"
                     "where titre like 'Guide pratique sur l\'application du R%'")
    except:
        print("ERROR update sigl_manuels_data for wrong character in one title")

    # PRODUCT STORAGE
    try:
        # Create table for product_details
        conn.execute("create table product_details("
                     "prd_ser int not NULL AUTO_INCREMENT,"
                     "prd_date datetime,"
                     "prd_name varchar(100) NOT NULL,"
                     "prd_type int default 0,"
                     "prd_nb_by_pack int default 0,"
                     "prd_supplier int default 0,"
                     "prd_ref_supplier varchar(50),"
                     "prd_conserv int default 0,"
                     "PRIMARY KEY (prd_ser),"
                     "INDEX (prd_name), INDEX (prd_type), INDEX (prd_supplier))")
    except:
        print("ERROR create table product_storage")

    try:
        # Create table for product_supply
        conn.execute("create table product_supply("
                     "prs_ser int not NULL AUTO_INCREMENT,"
                     "prs_date datetime,"
                     "prs_prd int NOT NULL,"
                     "prs_nb_pack int default 0,"
                     "prs_status int default 0,"
                     "prs_receipt_date datetime,"
                     "prs_expir_date datetime,"
                     "prs_rack varchar(100),"
                     "prs_batch_num varchar(50),"
                     "prs_buy_price int default 0,"
                     "prs_sell_price int default 0,"
                     "PRIMARY KEY (prs_ser),"
                     "INDEX (prs_prd))")
    except:
        print("ERROR create table product_supply")

    try:
        # Create table for product_use
        conn.execute("create table product_use("
                     "pru_ser int not NULL AUTO_INCREMENT,"
                     "pru_date datetime,"
                     "pru_user int NOT NULL,"
                     "pru_prs int NOT NULL,"
                     "pru_nb_pack int NOT NULL,"
                     "PRIMARY KEY (pru_ser),"
                     "INDEX (pru_prs))")
    except:
        print("ERROR create table product_use")

    # ADD PRODUCT TYPE IN DICT TABLE
    try:
        conn.execute("insert into sigl_dico_data "
                     "(id_owner, dico_name, label, short_label, position, code) "
                     "values (100, 'product_type', 'Consommables', 'consommables', 10, 'consommables')")
    except:
        print("ERROR insert into sigl_dico_data a product_type (consommables)")

    try:
        conn.execute("insert into sigl_dico_data "
                     "(id_owner, dico_name, label, short_label, position, code) "
                     "values (100, 'product_type', 'Réactifs microbio', 'reactif_microbio', 20, 'reactif_microbio')")
    except:
        print("ERROR insert into sigl_dico_data a product_type (reactif_microbio)")

    try:
        conn.execute("insert into sigl_dico_data "
                     "(id_owner, dico_name, label, short_label, position, code) "
                     "values (100, 'product_type', 'Hygiène sécurité', 'hygiene', 30, 'hygiene')")
    except:
        print("ERROR insert into sigl_dico_data a product_type (hygiene)")

    try:
        conn.execute("insert into sigl_dico_data "
                     "(id_owner, dico_name, label, short_label, position, code) "
                     "values (100, 'product_type', 'Matériel de prélèvement', 'materiel_prel', 40, 'materiel_prel')")
    except:
        print("ERROR insert into sigl_dico_data a product_type (materiel_prel)")

    try:
        conn.execute("insert into sigl_dico_data "
                     "(id_owner, dico_name, label, short_label, position, code) "
                     "values (100, 'product_type', 'Matériel microscopie', 'materiel_micro', 50, 'materiel_micro' )")
    except:
        print("ERROR insert into sigl_dico_data a product_type (materiel_micro)")

    # ADD STATUS PRODUCT IN DICT TABLE
    try:
        conn.execute("insert into sigl_dico_data "
                     "(id_owner, dico_name, label, short_label, position, code) "
                     "values (100, 'product_status', 'Bon', 'bon', 10, 'bon' )")
    except:
        print("ERROR insert into sigl_dico_data a product_status (bon)")

    try:
        conn.execute("insert into sigl_dico_data "
                     "(id_owner, dico_name, label, short_label, position, code) "
                     "values (100, 'product_status', 'Cassé', 'casse', 20, 'casse' )")
    except:
        print("ERROR insert into sigl_dico_data a product_status (cassé)")

    try:
        conn.execute("insert into sigl_dico_data "
                     "(id_owner, dico_name, label, short_label, position, code) "
                     "values (100, 'product_status', 'Périmé', 'perime', 30, 'perime' )")
    except:
        print("ERROR insert into sigl_dico_data a product_status (périmé)")

    # ADD CONSERVATION TYPE IN DICT TABLE
    try:
        conn.execute("insert into sigl_dico_data "
                     "(id_owner, dico_name, label, short_label, position, code) "
                     "values (100, 'product_conserv', 'Ambiante', 'ambiante', 10, 'ambiante' )")
    except:
        print("ERROR insert into sigl_dico_data a product_conserv (ambiante)")

    try:
        conn.execute("insert into sigl_dico_data "
                     "(id_owner, dico_name, label, short_label, position, code) "
                     "values (100, 'product_conserv', '2 - 8°C', 'frigo', 20, 'frigo' )")
    except:
        print("ERROR insert into sigl_dico_data a product_conserv (frigo)")

    try:
        conn.execute("insert into sigl_dico_data "
                     "(id_owner, dico_name, label, short_label, position, code) "
                     "values (100, 'product_conserv', '-18°C', 'congel', 30, 'congel' )")
    except:
        print("ERROR insert into sigl_dico_data a product_conserv (congel)")

    # ADD default storage path
    try:
        conn.execute("insert into sigl_storage_data "
                     "(id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, path) "
                     "values (100, NOW(), NOW(), 100, '/space/applisdata/labbook/storage' )")
    except:
        print("ERROR insert into sigl_storage_data a default storage path")

    # ADD NEW USER ROLE
    try:
        conn.execute("insert into sigl_pj_role "
                     "(name, label) "
                     "values ('technicien avance', 'Technicien avancé')")
    except:
        print("ERROR insert into sigl_pj_role (technicien avance)")

    try:
        conn.execute("insert into sigl_dico_data "
                     "(id_owner, dico_name, label, short_label, position, code) "
                     "values (100, 'profil', 'Technicien avancé', 'tech_avance', 22, 'tech_avance' )")
    except:
        print("ERROR insert into sigl_dico_data new profil (Technicien avancé)")

    try:
        conn.execute("insert into sigl_pj_role "
                     "(name, label) "
                     "values ('technicien qualiticien', 'Technicien qualiticien')")
    except:
        print("ERROR insert into sigl_pj_role (technicien qualiticien)")

    try:
        conn.execute("insert into sigl_dico_data "
                     "(id_owner, dico_name, label, short_label, position, code) "
                     "values (100, 'profil', 'Technicien qualiticien', 'tech_qualiticien', 24, 'tech_qualiticien' )")
    except:
        print("ERROR insert into sigl_dico_data new profil (Technicien qualiticien)")

    try:
        conn.execute("insert into sigl_pj_role "
                     "(name, label) "
                     "values ('secretaire avancee', 'secrétaire avancée')")
    except:
        print("ERROR insert into sigl_pj_role (secretaire avancee)")

    try:
        conn.execute("insert into sigl_dico_data "
                     "(id_owner, dico_name, label, short_label, position, code) "
                     "values (100, 'profil', 'Secretaire avancée', 'secr_avance', 12, 'secr_avance' )")
    except:
        print("ERROR insert into sigl_dico_data new profil (Secretaire avancée)")

    try:
        conn.execute("insert into sigl_pj_role "
                     "(name, label) "
                     "values ('qualiticien', 'Qualiticien')")
    except:
        print("ERROR insert into sigl_pj_role (qualiticien)")

    try:
        conn.execute("insert into sigl_dico_data "
                     "(id_owner, dico_name, label, short_label, position, code) "
                     "values (100, 'profil', 'Qualiticien', 'qualiticien', 14, 'qualiticien' )")
    except:
        print("ERROR insert into sigl_dico_data new profil (Qualiticien)")

    try:
        conn.execute("insert into sigl_pj_role "
                     "(name, label) "
                     "values ('prescripteur', 'Prescripteur')")
    except:
        print("ERROR insert into sigl_pj_role (prescripteur)")

    try:
        conn.execute("insert into sigl_dico_data "
                     "(id_owner, dico_name, label, short_label, position, code) "
                     "values (100, 'profil', 'Prescripteur', 'prescripteur', 16, 'prescripteur' )")
    except:
        print("ERROR insert into sigl_dico_data new profil (Prescripteur)")


def downgrade():
    pass