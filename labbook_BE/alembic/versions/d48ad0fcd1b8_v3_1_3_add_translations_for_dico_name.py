# -*- coding:utf-8 -*-
"""v3_1_3_add_translations_for_dico_name

Revision ID: d48ad0fcd1b8
Revises: 5365c73aa532
Create Date: 2021-10-21 11:31:59.211523

"""
from alembic import op

from datetime import datetime

# revision identifiers, used by Alembic.
revision = 'd48ad0fcd1b8'
down_revision = '5365c73aa532'
branch_labels = None
depends_on = None


def upgrade():
    print("--- " + str(datetime.today()) + "---")
    print("START of migration v3_1_3_add_translations_for_dico_name revision=d48ad0fcd1b8")

    # Get the current
    conn = op.get_bind()

    # ask for update translation in DB
    try:
        # insert a line in init_version
        conn.execute("insert into init_version (ini_date, ini_stat) values (NOW(), 'Y')")
    except Exception as err:
        print("ERROR insert init_version,\n\terr=" + str(err))

    print(str(datetime.today()) + " : END of migration v3_1_3_add_translations_for_dico_name revision=d48ad0fcd1b8")


def downgrade():
    pass
