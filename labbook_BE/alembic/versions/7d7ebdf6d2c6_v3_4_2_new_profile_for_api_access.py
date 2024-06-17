# -*- coding:utf-8 -*-
"""v3_4_2_new_profile_for_api_access

Revision ID: 7d7ebdf6d2c6
Revises: 6cda5712fcbe
Create Date: 2024-02-15 15:56:13.598425

"""
from alembic import op
from sqlalchemy import text

from datetime import datetime

# revision identifiers, used by Alembic.
revision = '7d7ebdf6d2c6'
down_revision = '6cda5712fcbe'
branch_labels = None
depends_on = None


def upgrade():
    print("--- " + str(datetime.today()) + "---")
    print("START of migration v3_4_2_new_profile_for_api_access revision=7d7ebdf6d2c6")

    # Get the current
    conn = op.get_bind()

    # ADD NEW USER ROLE
    try:
        conn.execute(text("insert into sigl_pj_role (name, label, type) "
                          "values ('api', 'API', 'API')"))
    except Exception as err:
        print("ERROR insert into sigl_pj_role (api),\n\terr=" + str(err))

    print(str(datetime.today()) + " : END of migration v3_4_2_new_profile_for_api_access revision=7d7ebdf6d2c6")


def downgrade():
    pass
