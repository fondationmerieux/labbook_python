"""v3_3_8_testing_import_analysis_repository

Revision ID: d44f950a2b07
Revises: c341c66fe1f0
Create Date: 2023-04-18 16:29:45.511100

"""
from alembic import op
from sqlalchemy import text

from datetime import datetime

# revision identifiers, used by Alembic.
revision = 'd44f950a2b07'
down_revision = 'c341c66fe1f0'
branch_labels = None
depends_on = None


def upgrade():
    print("--- " + str(datetime.today()) + "---")
    print("START of migration v3_3_8_testing_import_analysis_repository revision=d44f950a2b07")

    # Get the current
    conn = op.get_bind()

    # COPY alembic resource indicator
    try:
        from distutils.dir_util import copy_tree

        fromDirectory = "alembic/resource/template"
        toDirectory = "/storage/resource/template"

        copy_tree(fromDirectory, toDirectory)
    except Exception as err:
        print("ERROR copy alembic resource template,\n\terr=" + str(err))

    # ADD COLUMN for notify if almost one result of this record was canceled or re-initialized
    try:
        conn.execute(text("alter table sigl_02_data add column rec_modified varchar(1) not null default 'N'"))
    except Exception as err:
        print("ERROR add column rec_modified to sigl_02_data,\n\terr=" + str(err))

    # Create 3 tables for testing import analysis repository
    try:
        conn.execute(text("create table sigl_05_data_test like sigl_05_data"))
    except Exception as err:
        print("ERROR create table sigl_05_data_test,\n\terr=" + str(err))

    try:
        conn.execute(text("create table sigl_07_data_test like sigl_07_data"))
    except Exception as err:
        print("ERROR create table sigl_07_data_test,\n\terr=" + str(err))

    try:
        conn.execute(text("create table sigl_05_07_data_test like sigl_05_07_data"))
    except Exception as err:
        print("ERROR create table sigl_05_07_data_test,\n\terr=" + str(err))

    # ADD NEW USER ROLE
    try:
        conn.execute(text("insert into sigl_pj_role (name, label, type) "
                          "values ('personnel', 'Personnel', 'Z')"))
    except Exception as err:
        print("ERROR insert into sigl_pj_role (personnel),\n\terr=" + str(err))

    # TRACE DOWNLOAD TABLE
    try:
        # Create table for trace donwload
        conn.execute(text("create table trace_download("
                          "trd_ser int not NULL AUTO_INCREMENT, "
                          "trd_date datetime, "
                          "trd_last_access datetime, "
                          "trd_type varchar(5) not NULL, "
                          "trd_ref int not NULL, "
                          "trd_user int not NULL, "
                          "PRIMARY KEY (trd_ser), INDEX (trd_type), INDEX (trd_ref), INDEX (trd_user))"))
    except Exception as err:
        print("ERROR create table trace_download,\n\terr=" + str(err))

    print(str(datetime.today()) + " : END of migration v3_3_8_testing_import_analysis_repository revision=d44f950a2b07")


def downgrade():
    pass
