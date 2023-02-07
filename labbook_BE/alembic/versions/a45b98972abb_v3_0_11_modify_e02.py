# -*- coding:utf-8 -*-
"""v3_0_11_modify_E02

Revision ID: a45b98972abb
Revises: 69fede710356
Create Date: 2021-07-09 09:44:24.628280

"""
from alembic import op
from sqlalchemy import text

from datetime import datetime

# revision identifiers, used by Alembic.
revision = 'a45b98972abb'
down_revision = '69fede710356'
branch_labels = None
depends_on = None


def upgrade():
    print("--- " + str(datetime.today()) + "---")
    print("START of migration v3.0.11_modify_E02 revision=a45b98972abb")

    # Get the current
    conn = op.get_bind()

    # MODIFY E02 Ebola analysis update name
    try:
        conn.execute(text('update sigl_05_data set nom="Recherche par prélèvement buccal de l\'ADN viral de la maladie '
                          'à virus Ebola par RT-PCR" where code="E02"'))
    except Exception as err:
        print("ERROR rename E02 analysis,\n\terr=" + str(err))

    print(str(datetime.today()) + " : END of migration v3.0.11_modify_E02 revision=a45b98972abb")


def downgrade():
    pass
