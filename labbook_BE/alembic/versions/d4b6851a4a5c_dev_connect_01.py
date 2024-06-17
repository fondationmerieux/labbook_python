# -*- coding:utf-8 -*-
"""dev_connect_01

Revision ID: d4b6851a4a5c
Revises: 3d67b66dcc23
Create Date: 2023-11-08 15:24:25.516919

"""
from alembic import op
from sqlalchemy import text

from datetime import datetime

# revision identifiers, used by Alembic.
revision = 'd4b6851a4a5c'
down_revision = '3d67b66dcc23'
branch_labels = None
depends_on = None


def upgrade():
    print("--- " + str(datetime.today()) + "---")
    print("START of migration dev_connect_01 revision=d4b6851a4a5c")

    # Get the current
    conn = op.get_bind()

    # NEW DIRECTORY IN STORAGE
    try:
        import pathlib

        pathlib.Path("/storage/resource/connect").mkdir(mode=0o777, parents=False, exist_ok=True)
    except Exception as err:
        print("ERROR mkdir -p /storage/resource/connect,\n\terr=" + str(err))

    # NEW DIRECTORY IN STORAGE
    try:
        import pathlib

        pathlib.Path("/storage/resource/connect/analyzer").mkdir(mode=0o777, parents=False, exist_ok=True)
    except Exception as err:
        print("ERROR mkdir -p /storage/resource/connect/analyzer,\n\terr=" + str(err))

    # NEW DIRECTORY IN STORAGE
    try:
        import pathlib

        pathlib.Path("/storage/resource/connect/analyzer/setting").mkdir(mode=0o777, parents=False, exist_ok=True)
    except Exception as err:
        print("ERROR mkdir -p /storage/resource/connect/analyzer/setting,\n\terr=" + str(err))

    # NEW DIRECTORY IN STORAGE
    try:
        import pathlib

        pathlib.Path("/storage/resource/connect/analyzer/plugin").mkdir(mode=0o777, parents=False, exist_ok=True)
    except Exception as err:
        print("ERROR mkdir -p /storage/resource/connect/analyzer/plugin,\n\terr=" + str(err))

    # ADD COLUMN to link a sample to an analysis
    try:
        conn.execute(text("alter table sigl_01_data add column samp_id_ana int not null default 0"))
    except Exception as err:
        print("ERROR add column samp_id_ana to sigl_01_data,\n\terr=" + str(err))

    # DROP COLUMN quantite
    try:
        conn.execute(text("alter table sigl_01_data drop column quantite"))
    except Exception as err:
        print("ERROR drop column quantite to sigl_01_data,\n\terr=" + str(err))

    # ADD COLUMN to link a sample to an analysis
    try:
        conn.execute(text("alter table sigl_01_deleted add column samp_id_ana int not null default 0"))
    except Exception as err:
        print("ERROR add column samp_id_ana to sigl_01_deleted,\n\terr=" + str(err))

    # DROP COLUMN quantite
    try:
        conn.execute(text("alter table sigl_01_deleted drop column quantite"))
    except Exception as err:
        print("ERROR drop column quantite to sigl_01_deleted,\n\terr=" + str(err))

    # ADD COLUMN for type of result recovery 'M'anual or 'A'uto
    try:
        conn.execute(text("alter table sigl_09_data add column res_recovery varchar(1) not null default 'M'"))
    except Exception as err:
        print("ERROR add column res_recovery to sigl_09_data,\n\terr=" + str(err))

    # Create table for analyzers setting
    try:
        conn.execute(text("create table analyzer_setting("
                          "ans_ser int not NULL AUTO_INCREMENT,"
                          "ans_date DATETIME,"
                          "ans_user INT not null default 0,"
                          "ans_rank INT not null default 0,"
                          "ans_name varchar(100) not null,"
                          "ans_id varchar(80) unique not null,"
                          "ans_lab28 varchar(255) not null,"
                          "ans_mapping varchar(255) not null,"
                          "ans_filename varchar(255) not null,"
                          "PRIMARY KEY (ans_ser),"
                          "INDEX (ans_rank), INDEX (ans_name), INDEX (ans_id)) "
                          "character set=utf8"))
    except Exception as err:
        print("ERROR create table analyzer_setting,\n\terr=" + str(err))

    # Create table for analyzers requests LAB28
    try:
        conn.execute(text("create table analyzer_lab28("
                          "anl_ser int not NULL AUTO_INCREMENT,"
                          "anl_date DATETIME,"
                          "anl_date_upd DATETIME,"
                          "anl_ans INT not null,"
                          "anl_id_samp INT not null,"
                          "anl_stat varchar(2) not null,"
                          "anl_OML_O33 text not null,"
                          "anl_ORL_O34 text not null,"
                          "PRIMARY KEY (anl_ser),"
                          "INDEX (anl_stat), INDEX (anl_id_samp)) "
                          "character set=utf8"))
    except Exception as err:
        print("ERROR create table analyzer_lab28,\n\terr=" + str(err))

    print(str(datetime.today()) + " : END of migration dev_connect_01 revision=d4b6851a4a5c")


def downgrade():
    pass
