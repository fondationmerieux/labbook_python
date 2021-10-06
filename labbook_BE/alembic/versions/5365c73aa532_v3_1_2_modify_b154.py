# -*- coding:utf-8 -*-
"""v3_1_2_modify_B154

Revision ID: 5365c73aa532
Revises: 21a2df9c3e0a
Create Date: 2021-10-06 14:14:45.013818

"""
from alembic import op

from datetime import datetime

# revision identifiers, used by Alembic.
revision = '5365c73aa532'
down_revision = '21a2df9c3e0a'
branch_labels = None
depends_on = None


def upgrade():
    print("--- " + str(datetime.today()) + "---")
    print("START of migration v3_1_2_modify_B154 revision=5365c73aa532")

    # Get the current
    conn = op.get_bind()

    # Update name of variable
    try:
        conn.execute("update sigl_07_data set libelle='TCA ou TCK (témoin : 28s)' "
                     "where code_var=199")
    except Exception as err:
        print("ERROR update sigl_07_data libelle='TCA ou TCK (témoin : 28s),\n\terr=" + str(err))

    # delete link (code_var=200)
    try:
        conn.execute("delete from sigl_05_07_data "
                     "where id_refvariable = 200")
    except Exception as err:
        print("ERROR remove link with code_var=200,\n\terr=" + str(err))

    # delete variable (code_var=200)
    try:
        conn.execute("delete from sigl_07_data "
                     "where code_var = 200")
    except Exception as err:
        print("ERROR remove var with code_var=200,\n\terr=" + str(err))

    # ask for update translation in DB
    try:
        # insert a line in init_version
        conn.execute("insert into init_version (ini_date, ini_stat) values (NOW(), 'Y')")
    except Exception as err:
        print("ERROR insert init_version,\n\terr=" + str(err))

    print(str(datetime.today()) + " : END of migration v3_1_2_modify_B154 revision=5365c73aa532")


def downgrade():
    pass
