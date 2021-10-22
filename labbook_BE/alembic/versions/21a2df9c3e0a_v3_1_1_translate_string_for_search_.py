# -*- coding:utf-8 -*-
"""v3_1_1_translate_string_for_search_fields

Revision ID: 21a2df9c3e0a
Revises: 027a982a0313
Create Date: 2021-09-20 16:02:44.465936

"""
from alembic import op

from datetime import datetime
# from app.models.Various import Various

# revision identifiers, used by Alembic.
revision = '21a2df9c3e0a'
down_revision = '027a982a0313'
branch_labels = None
depends_on = None


def upgrade():
    print("--- " + str(datetime.today()) + "---")
    print("START of migration v3_1_1_translate_string_for_search_fields revision=21a2df9c3e0a")

    # Get the current
    conn = op.get_bind()

    # convert table to character set utf8
    try:
        conn.execute("alter table age_interval_setting convert to character set utf8")
    except Exception as err:
        print("ERROR alter table character age_interval_setting set utf8,\n\terr=" + str(err))

    try:
        conn.execute("alter table backup_setting convert to character set utf8")
    except Exception as err:
        print("ERROR alter table character backup_setting set utf8,\n\terr=" + str(err))

    try:
        conn.execute("alter table database_status convert to character set utf8")
    except Exception as err:
        print("ERROR alter table character database_status set utf8,\n\terr=" + str(err))

    try:
        conn.execute("alter table product_details convert to character set utf8")
    except Exception as err:
        print("ERROR alter table character product_details set utf8,\n\terr=" + str(err))

    try:
        conn.execute("alter table product_supply convert to character set utf8")
    except Exception as err:
        print("ERROR alter table character product_supply set utf8,\n\terr=" + str(err))

    try:
        conn.execute("alter table product_use convert to character set utf8")
    except Exception as err:
        print("ERROR alter table character product_use set utf8,\n\terr=" + str(err))

    try:
        conn.execute("alter table sticker_setting convert to character set utf8")
    except Exception as err:
        print("ERROR alter table character sticker_setting set utf8,\n\terr=" + str(err))

    # TRANSLATION TABLE
    try:
        # Create table for translations used by fields search
        conn.execute("create table translations("
                     "tra_ser int not NULL AUTO_INCREMENT,"
                     "tra_date DATETIME,"
                     "tra_lang varchar(6) NOT NULL,"
                     "tra_ref INT default 0,"
                     "tra_type varchar(10) NOT NULL,"
                     "tra_text text,"
                     "PRIMARY KEY (tra_ser),"
                     "INDEX (tra_lang), INDEX (tra_type), INDEX (tra_ref)) "
                     "character set=utf8")
    except Exception as err:
        print("ERROR create table translations,\n\terr=" + str(err))

    # INIT TABLE
    try:
        # Create table for launch some process (not possible with alembic) after start a new version
        conn.execute("create table init_version("
                     "ini_ser int not NULL AUTO_INCREMENT,"
                     "ini_date DATETIME,"
                     "ini_stat varchar(1) NOT NULL,"
                     "PRIMARY KEY (ini_ser),"
                     "INDEX (ini_date)) "
                     "character set=utf8")
    except Exception as err:
        print("ERROR create table init_version,\n\terr=" + str(err))
    else:
        try:
            # insert a line in init_version
            conn.execute("insert into init_version (ini_date, ini_stat) values (NOW(), 'Y')")
        except Exception as err:
            print("ERROR insert init_version,\n\terr=" + str(err))

    # ADD INDEX
    try:
        conn.execute("create index idx_date_samp on sigl_01_data (date_prel)")

        conn.execute("create index idx_date_rec on sigl_02_data (date_dos)")
        conn.execute("create index idx_date_prescr on sigl_02_data (date_prescription)")
        conn.execute("create index idx_date_hosp on sigl_02_data (date_hosp)")

        conn.execute("create index idx_name on sigl_03_data (nom)")
        conn.execute("create index idx_fname on sigl_03_data (prenom)")

        conn.execute("create index idx_name on sigl_05_data (nom)")

        conn.execute("create index idx_label on sigl_07_data (libelle)")

        conn.execute("create index idx_name on sigl_08_data (nom)")
        conn.execute("create index idx_fname on sigl_08_data (prenom)")
        conn.execute("create index idx_code on sigl_08_data (code)")

        conn.execute("create index idx_date_vld on sigl_10_data (date_validation)")

        conn.execute("create index idx_file on sigl_11_data (file)")

        conn.execute("create index idx_label on sigl_dico_data (label)")

        conn.execute("create index idx_oname on sigl_file_data (original_name)")
        conn.execute("create index idx_gname on sigl_file_data (generated_name)")

        conn.execute("create index idx_username on sigl_user_data (username)")
        conn.execute("create index idx_name on sigl_user_data (lastname)")
        conn.execute("create index idx_account on sigl_user_data (side_account)")

        conn.execute("create index idx_date on product_details (prd_date)")

        conn.execute("create index idx_date on product_supply (prs_date)")
        conn.execute("create index idx_user on product_supply (prs_user)")

        conn.execute("create index idx_date on product_use (pru_date)")
        conn.execute("create index idx_user on product_use (pru_user)")
    except Exception as err:
        print("ERROR create index,\n\terr=" + str(err))

    print(str(datetime.today()) + " : END of migration v3_1_1_translate_string_for_search_fields revision=21a2df9c3e0a")


def downgrade():
    pass
