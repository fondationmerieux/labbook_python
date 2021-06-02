# -*- coding:utf-8 -*-
"""v3.0.0_setting_modification

Revision ID: 71b4a9a97b7a
Revises: 75a90d6bfa9f
Create Date: 2021-02-03 10:46:43.668497

"""
from alembic import op

from datetime import datetime

# revision identifiers, used by Alembic.
revision = '71b4a9a97b7a'
down_revision = '75a90d6bfa9f'
branch_labels = None
depends_on = None


def upgrade():
    print("--- " + str(datetime.today()) + "---")
    print("START of migration v3.0.0_setting_modification revision=71b4a9a97b7a")

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
    except Exception as err:
        print("ERROR create table age_interval_setting,\n\terr=" + str(err))
    else:
        try:
            # insert 4 age interval by default
            conn.execute("insert into age_interval_setting (ais_rank, ais_upper_bound) values (0, 5)")
            conn.execute("insert into age_interval_setting (ais_rank, ais_lower_bound, ais_upper_bound) values (1, 5, 20)")
            conn.execute("insert into age_interval_setting (ais_rank, ais_lower_bound, ais_upper_bound) values (2, 20, 40)")
            conn.execute("insert into age_interval_setting (ais_rank, ais_lower_bound) values (3, 40)")
        except Exception as err:
            print("ERROR insert default value for age_interval_setting,\n\terr=" + str(err))

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
    except Exception as err:
        print("ERROR create table sticker_setting,\n\terr=" + str(err))
    else:
        try:
            # insert a default format for stickers_setting
            conn.execute("insert into sticker_setting "
                         "(sts_margin_top, sts_margin_bottom, sts_margin_left, sts_margin_right, sts_height, sts_width) "
                         "values (10, 10, 10, 10, 15, 60)")
        except Exception as err:
            print("ERROR insert default value for sticker_setting,\n\terr=" + str(err))

    # BACKUP TABLE
    try:
        # Create table for backup setting
        conn.execute("create table backup_setting("
                     "bks_ser int not NULL AUTO_INCREMENT,"
                     "bks_start_time TIME NOT NULL,"
                     "PRIMARY KEY (bks_ser))")
    except Exception as err:
        print("ERROR create table backup_setting,\n\terr=" + str(err))
    else:
        try:
            # insert backup setting by default
            conn.execute("insert into backup_setting (bks_start_time) values ('12:00:00')")
        except Exception as err:
            print("ERROR insert default value for backup_setting,\n\terr=" + str(err))

    # UPDATE MANUAL
    try:
        # update id_storage for sigl_file_data
        conn.execute("update sigl_file_data set id_storage=1 where id_storage is null")
    except Exception as err:
        print("ERROR update sigl_file_data set id_storage=1 where id_storage is null,\n\terr=" + str(err))

    # wrong character in manual table
    """ Not working everytime and its deprecated because this manual it delete in v3.0.2
    try:
        # update id_storage for sigl_manuels_data
        conn.execute("update sigl_manuels_data"
                     "set titre='Guide pratique sur l\'application du Règlement relatif au transport des matières infectieuses 2013-2014'"
                     "where titre like 'Guide pratique sur l\'application du R%'")
    except Exception as err:
        print("ERROR update sigl_manuels_data for wrong character in one title,\n\terr=" + str(err))"""

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
    except Exception as err:
        print("ERROR create table product_storage,\n\terr=" + str(err))

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
    except Exception as err:
        print("ERROR create table product_supply,\n\terr=" + str(err))

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
    except Exception as err:
        print("ERROR create table product_use,\n\terr=" + str(err))

    # ADD PRODUCT TYPE IN DICT TABLE
    try:
        conn.execute("insert into sigl_dico_data "
                     "(id_owner, dico_name, label, short_label, position, code) "
                     "values (100, 'product_type', 'Consommables', 'consommables', 10, 'consommables')")
    except Exception as err:
        print("ERROR insert into sigl_dico_data a product_type (consommables),\n\terr=" + str(err))

    try:
        conn.execute("insert into sigl_dico_data "
                     "(id_owner, dico_name, label, short_label, position, code) "
                     "values (100, 'product_type', 'Réactifs microbio', 'reactif_microbio', 20, 'reactif_microbio')")
    except Exception as err:
        print("ERROR insert into sigl_dico_data a product_type (reactif_microbio),\n\terr=" + str(err))

    try:
        conn.execute("insert into sigl_dico_data "
                     "(id_owner, dico_name, label, short_label, position, code) "
                     "values (100, 'product_type', 'Hygiène sécurité', 'hygiene', 30, 'hygiene')")
    except Exception as err:
        print("ERROR insert into sigl_dico_data a product_type (hygiene),\n\terr=" + str(err))

    try:
        conn.execute("insert into sigl_dico_data "
                     "(id_owner, dico_name, label, short_label, position, code) "
                     "values (100, 'product_type', 'Matériel de prélèvement', 'materiel_prel', 40, 'materiel_prel')")
    except Exception as err:
        print("ERROR insert into sigl_dico_data a product_type (materiel_prel),\n\terr=" + str(err))

    try:
        conn.execute("insert into sigl_dico_data "
                     "(id_owner, dico_name, label, short_label, position, code) "
                     "values (100, 'product_type', 'Matériel microscopie', 'materiel_micro', 50, 'materiel_micro' )")
    except Exception as err:
        print("ERROR insert into sigl_dico_data a product_type (materiel_micro),\n\terr=" + str(err))

    # ADD STATUS PRODUCT IN DICT TABLE
    try:
        conn.execute("insert into sigl_dico_data "
                     "(id_owner, dico_name, label, short_label, position, code) "
                     "values (100, 'product_status', 'Bon', 'bon', 10, 'bon' )")
    except Exception as err:
        print("ERROR insert into sigl_dico_data a product_status (bon),\n\terr=" + str(err))

    try:
        conn.execute("insert into sigl_dico_data "
                     "(id_owner, dico_name, label, short_label, position, code) "
                     "values (100, 'product_status', 'Cassé', 'casse', 20, 'casse' )")
    except Exception as err:
        print("ERROR insert into sigl_dico_data a product_status (cassé),\n\terr=" + str(err))

    try:
        conn.execute("insert into sigl_dico_data "
                     "(id_owner, dico_name, label, short_label, position, code) "
                     "values (100, 'product_status', 'Périmé', 'perime', 30, 'perime' )")
    except Exception as err:
        print("ERROR insert into sigl_dico_data a product_status (périmé),\n\terr=" + str(err))

    # ADD CONSERVATION TYPE IN DICT TABLE
    try:
        conn.execute("insert into sigl_dico_data "
                     "(id_owner, dico_name, label, short_label, position, code) "
                     "values (100, 'product_conserv', 'Ambiante', 'ambiante', 10, 'ambiante' )")
    except Exception as err:
        print("ERROR insert into sigl_dico_data a product_conserv (ambiante),\n\terr=" + str(err))

    try:
        conn.execute("insert into sigl_dico_data "
                     "(id_owner, dico_name, label, short_label, position, code) "
                     "values (100, 'product_conserv', '2 - 8°C', 'frigo', 20, 'frigo' )")
    except Exception as err:
        print("ERROR insert into sigl_dico_data a product_conserv (frigo),\n\terr=" + str(err))

    try:
        conn.execute("insert into sigl_dico_data "
                     "(id_owner, dico_name, label, short_label, position, code) "
                     "values (100, 'product_conserv', '-18°C', 'congel', 30, 'congel' )")
    except Exception as err:
        print("ERROR insert into sigl_dico_data a product_conserv (congel),\n\terr=" + str(err))

    # ADD NEW USER ROLE
    try:
        conn.execute("insert into sigl_pj_role "
                     "(name, label) "
                     "values ('technicien avance', 'Technicien avancé')")
    except Exception as err:
        print("ERROR insert into sigl_pj_role (technicien avance),\n\terr=" + str(err))

    try:
        conn.execute("insert into sigl_dico_data "
                     "(id_owner, dico_name, label, short_label, position, code) "
                     "values (100, 'profil', 'Technicien avancé', 'tech_avance', 22, 'tech_avance' )")
    except Exception as err:
        print("ERROR insert into sigl_dico_data new profil (Technicien avancé),\n\terr=" + str(err))

    try:
        conn.execute("insert into sigl_pj_role "
                     "(name, label) "
                     "values ('technicien qualiticien', 'Technicien qualiticien')")
    except Exception as err:
        print("ERROR insert into sigl_pj_role (technicien qualiticien),\n\terr=" + str(err))

    try:
        conn.execute("insert into sigl_dico_data "
                     "(id_owner, dico_name, label, short_label, position, code) "
                     "values (100, 'profil', 'Technicien qualiticien', 'tech_qualiticien', 24, 'tech_qualiticien' )")
    except Exception as err:
        print("ERROR insert into sigl_dico_data new profil (Technicien qualiticien),\n\terr=" + str(err))

    try:
        conn.execute("insert into sigl_pj_role "
                     "(name, label) "
                     "values ('secretaire avancee', 'secrétaire avancée')")
    except Exception as err:
        print("ERROR insert into sigl_pj_role (secretaire avancee),\n\terr=" + str(err))

    try:
        conn.execute("insert into sigl_dico_data "
                     "(id_owner, dico_name, label, short_label, position, code) "
                     "values (100, 'profil', 'Secretaire avancée', 'secr_avance', 12, 'secr_avance' )")
    except Exception as err:
        print("ERROR insert into sigl_dico_data new profil (Secretaire avancée),\n\terr=" + str(err))

    try:
        conn.execute("insert into sigl_pj_role "
                     "(name, label) "
                     "values ('qualiticien', 'Qualiticien')")
    except Exception as err:
        print("ERROR insert into sigl_pj_role (qualiticien),\n\terr=" + str(err))

    try:
        conn.execute("insert into sigl_dico_data "
                     "(id_owner, dico_name, label, short_label, position, code) "
                     "values (100, 'profil', 'Qualiticien', 'qualiticien', 14, 'qualiticien' )")
    except Exception as err:
        print("ERROR insert into sigl_dico_data new profil (Qualiticien),\n\terr=" + str(err))

    try:
        conn.execute("insert into sigl_pj_role "
                     "(name, label) "
                     "values ('prescripteur', 'Prescripteur')")
    except Exception as err:
        print("ERROR insert into sigl_pj_role (prescripteur),\n\terr=" + str(err))

    try:
        conn.execute("insert into sigl_dico_data "
                     "(id_owner, dico_name, label, short_label, position, code) "
                     "values (100, 'profil', 'Prescripteur', 'prescripteur', 16, 'prescripteur' )")
    except Exception as err:
        print("ERROR insert into sigl_dico_data new profil (Prescripteur),\n\terr=" + str(err))

    print(str(datetime.today()) + " : END of migration v3.0.0_setting_modification revision=71b4a9a97b7a")


def downgrade():
    pass
