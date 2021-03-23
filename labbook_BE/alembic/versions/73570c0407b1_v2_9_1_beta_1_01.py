# -*- coding:utf-8 -*-
"""v2.9.1-beta.1 01

Revision ID: 73570c0407b1
Revises:
Create Date: 2020-09-24 16:02:11.552434

"""
from alembic import op
import sqlalchemy as sa

from datetime import datetime

# revision identifiers, used by Alembic.
revision = '73570c0407b1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    print("--- " + str(datetime.today()) + "---")
    print("START of migration v2.9.1-beta.1 01 revision=73570c0407b1")

    op.add_column('sigl_02_data', sa.Column('date_hosp', sa.Date))

    print("END of migration v2.9.1-beta.1 01 revision=73570c0407b1")


def downgrade():
    pass
