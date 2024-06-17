# -*- coding:utf-8 -*-
"""v3_4_6_ast_report

Revision ID: e997e3d843ef
Revises: ee493ffd1c9b
Create Date: 2024-06-10 15:22:48.236027

"""
from alembic import op
from sqlalchemy import text

from datetime import datetime

# revision identifiers, used by Alembic.
revision = 'e997e3d843ef'
down_revision = 'ee493ffd1c9b'
branch_labels = None
depends_on = None


def upgrade():
    print("--- " + str(datetime.today()) + "---")
    print("START of migration v3_4_6_ast_report revision=e997e3d843ef")

    # Get the current
    conn = op.get_bind()

    # ADD COLUMN ana_ast
    try:
        conn.execute(text("alter table sigl_05_data add column ana_ast varchar(1) not null default 'N'"))
    except Exception as err:
        print("ERROR add column ana_ast to sigl_05_data,\n\terr=" + str(err))

    # UPDATE ana_ast for ast analyzes
    try:
        conn = op.get_bind()

        conn.execute(text('update sigl_05_data set ana_ast="Y" '
                          'where code in ("B650","B651","B652","B653","B654","B655","B656","B657","B658","B659","B660", '
                          '"B661","B670","B671","B672","B673","B674","B675","B676","B677","B678","B679","B680","B681")'))
    except Exception as err:
        print("ERROR update sigl_05_data set ana_ast='Y' where code in ('B650' to 'B681'),\n\terr=" + str(err))

    print(str(datetime.today()) + " : END of migration v3_4_6_ast_report revision=e997e3d843ef")


def downgrade():
    pass
