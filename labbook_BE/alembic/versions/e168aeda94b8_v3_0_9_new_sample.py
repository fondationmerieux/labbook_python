# -*- coding:utf-8 -*-
"""v3_0_9_new_sample

Revision ID: e168aeda94b8
Revises: 88b82bfc1251
Create Date: 2021-06-21 09:58:52.549906

"""
from alembic import op
from sqlalchemy import text

from datetime import datetime

# revision identifiers, used by Alembic.
revision = 'e168aeda94b8'
down_revision = '88b82bfc1251'
branch_labels = None
depends_on = None


def upgrade():
    print("--- " + str(datetime.today()) + "---")
    print("START of migration v3.0.9_new_sample revision=e168aeda94b8")

    # Get the current
    conn = op.get_bind()

    # Insert new sample analysis PB25
    try:
        conn.execute(text('insert into sigl_05_data (id_owner, code, nom, abbr, famille, '
                          'cote_unite, commentaire, actif, ana_whonet, produit_biologique, type_prel) '
                          'values (1000, "PB25", "Prélèvement pus", "Pus", 0, "PB", "", 4, 5, 0, 0)'))
    except Exception as err:
        print("ERROR insert PB25 sample analysis,\n\terr=" + str(err))

    print(str(datetime.today()) + " : END of migration v3.0.9_new_sample revision=e168aeda94b8")


def downgrade():
    pass
