# -*- coding:utf-8 -*-
"""v2.9.1-beta.1 01

Revision ID: 73570c0407b1
Revises:
Create Date: 2020-09-24 16:02:11.552434

"""
from alembic import op
# import sqlalchemy as sa
from sqlalchemy import text

from datetime import datetime

# revision identifiers, used by Alembic.
revision = '73570c0407b1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    print("--- " + str(datetime.today()) + "---")
    print("START of migration v2.9.1-beta.1 01 revision=73570c0407b1")

    # op.add_column('sigl_02_data', sa.Column('date_hosp', sa.Date))
    # Get the current
    conn = op.get_bind()

    # ADD COLUMN TO PRODUCT DETAILS TABLE
    try:
        conn.execute(text("alter table sigl_02_data add column date_hosp date"))
    except Exception as err:
        print("ERROR add column date_hosp to sigl_02_data,\n\terr=" + str(err))

    print(str(datetime.today()) + " : END of migration v2.9.1-beta.1 01 revision=73570c0407b1")


def downgrade():
    pass
