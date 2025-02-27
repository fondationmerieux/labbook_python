# -*- coding:utf-8 -*-
"""v3_5_0_internal_messaging_and_personalized_profile

Revision ID: 114c3d84e3cb
Revises: e997e3d843ef
Create Date: 2024-12-09 14:39:54.958383

"""
from alembic import op
from sqlalchemy import text

from datetime import datetime

# revision identifiers, used by Alembic.
revision = '114c3d84e3cb'
down_revision = 'e997e3d843ef'
branch_labels = None
depends_on = None


def upgrade():
    print("--- " + str(datetime.today()) + "---")
    print("START of migration v3_5_0_internal_messaging_and_personalized_profile revision=114c3d84e3cb")

    # Get the current
    conn = op.get_bind()

    # Create table for internal messaging
    try:
        conn.execute(text("create table internal_messaging("
                          "ime_ser int not NULL AUTO_INCREMENT,"
                          "ime_date DATETIME,"
                          "ime_sender INT default 0,"
                          "ime_receiver INT default 0,"
                          "ime_subject varchar(255) NOT NULL,"
                          "ime_body text NOT NULL,"
                          "ime_is_read varchar(1) NOT NULL default 'N',"
                          "ime_sender_del varchar(1) NOT NULL default 'N',"
                          "ime_receiver_del varchar(1) NOT NULL default 'N',"
                          "PRIMARY KEY (ime_ser), INDEX (ime_sender), INDEX (ime_receiver)) "
                          "character set=utf8"))
    except Exception as err:
        print("ERROR create table internal_messaging,\n\terr=" + str(err))

    # Create table for internal_messaging_file
    try:
        conn.execute(text("create table internal_messaging_file("
                          "id_data INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY, "
                          "id_owner INT UNSIGNED DEFAULT NULL, "
                          "sys_creation_date DATETIME DEFAULT NULL, "
                          "sys_last_mod_date DATETIME DEFAULT NULL, "
                          "sys_last_mod_user INT UNSIGNED DEFAULT NULL, "
                          "id_ext INT UNSIGNED DEFAULT NULL, "
                          "id_file INT UNSIGNED DEFAULT NULL )"
                          "character set=utf8"))
    except Exception as err:
        print("ERROR create table internal_messaging_file,\n\terr=" + str(err))

    print(str(datetime.today()) + " : END of migration v3_5_0_internal_messaging_and_personalized_profile revision=114c3d84e3cb")


def downgrade():
    pass
