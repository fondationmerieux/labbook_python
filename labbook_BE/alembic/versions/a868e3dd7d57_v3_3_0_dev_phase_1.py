# -*- coding:utf-8 -*-
"""v3_3_0_dev_phase_1

Revision ID: a868e3dd7d57
Revises: 7671e7d31fec
Create Date: 2022-11-29 16:37:04.365632

"""
from alembic import op
from sqlalchemy import text

from datetime import datetime

# revision identifiers, used by Alembic.
revision = 'a868e3dd7d57'
down_revision = '7671e7d31fec'
branch_labels = None
depends_on = None


def upgrade():
    print("--- " + str(datetime.today()) + "---")
    print("START of migration v3_3_0_dev_phase_1 revision=a868e3dd7d57")

    # Get the current
    conn = op.get_bind()

    # ADD COLUMN for custody status
    try:
        conn.execute(text("alter table sigl_02_data add column rec_custody varchar(1) not null default 'N'"))
    except Exception as err:
        print("ERROR add column rec_custody to sigl_02_data,\n\terr=" + str(err))

    # ADD COLUMN for internal record number
    try:
        conn.execute(text("alter table sigl_02_data add column rec_num_int varchar(30) not null default ''"))
    except Exception as err:
        print("ERROR add column rec_num_int to sigl_02_data,\n\terr=" + str(err))

    # ADD COLUMN for validation date for a record
    try:
        conn.execute(text("alter table sigl_02_data add column rec_date_vld datetime"))
    except Exception as err:
        print("ERROR add column rec_date_vld to sigl_02_data,\n\terr=" + str(err))

    # ADD COLUMN for highlight result value
    try:
        conn.execute(text("alter table sigl_07_data add column var_highlight varchar(1) not null default 'N'"))
    except Exception as err:
        print("ERROR add column var_highlight to sigl_07_data,\n\terr=" + str(err))

    print(str(datetime.today()) + " : END of migration v3_3_0_dev_phase_1 revision=a868e3dd7d57")


def downgrade():
    pass
