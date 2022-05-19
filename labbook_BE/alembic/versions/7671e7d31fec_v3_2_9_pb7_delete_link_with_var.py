# -*- coding:utf-8 -*-
"""v3_2_9_PB7_delete_link_with_var

Revision ID: 7671e7d31fec
Revises: 588cfbb88538
Create Date: 2022-05-19 10:48:57.275938

"""
from alembic import op

from datetime import datetime

# revision identifiers, used by Alembic.
revision = '7671e7d31fec'
down_revision = '588cfbb88538'
branch_labels = None
depends_on = None


def upgrade():
    print("--- " + str(datetime.today()) + "---")
    print("START of migration v3_2_9_PB7_delete_link_with_var revision=7671e7d31fec")

    # Get the current
    conn = op.get_bind()

    # MODIFY PB7 remove link with Détection et titrage des IgG et de IgM (Toxoplasmose) variable
    try:
        conn.execute("delete from sigl_05_07_data "
                     "where id_refanalyse=7 and id_refvariable in (select id_data from sigl_07_data "
                     "where libelle='Détection et titrage des IgG et de IgM (Toxoplasmose)')")
    except Exception as err:
        print("ERROR remove link with variable for PB7,\n\terr=" + str(err))

    print(str(datetime.today()) + " : END of migration v3_2_9_PB7_delete_link_with_var revision=7671e7d31fec")


def downgrade():
    pass
