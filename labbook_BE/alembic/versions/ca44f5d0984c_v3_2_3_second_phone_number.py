# -*- coding:utf-8 -*-
"""v3_2_3_second_phone_number

Revision ID: ca44f5d0984c
Revises: dfd012f1852a
Create Date: 2022-03-07 10:42:36.442408

"""
from alembic import op

from datetime import datetime

# revision identifiers, used by Alembic.
revision = 'ca44f5d0984c'
down_revision = 'dfd012f1852a'
branch_labels = None
depends_on = None


def upgrade():
    print("--- " + str(datetime.today()) + "---")
    print("START of migration v3_2_3_second_phone_number revision=ca44f5d0984c")

    # Get the current
    conn = op.get_bind()

    # COPY alembic resource
    try:
        from distutils.dir_util import copy_tree

        fromDirectory = "alembic/resource"
        toDirectory = "/storage/resource"

        copy_tree(fromDirectory, toDirectory)
    except Exception as err:
        print("ERROR copy alembic resource,\n\terr=" + str(err))

    # ADD second phone number for patient
    try:
        conn.execute("alter table sigl_03_data add column pat_phone2 varchar(20)")
    except Exception as err:
        print("ERROR add column pat_phone2 to sigl_03_data,\n\terr=" + str(err))

    # ADD INDEX
    try:
        conn.execute("create index idx_phone1 on sigl_03_data (tel)")
        conn.execute("create index idx_phone2 on sigl_03_data (pat_phone2)")
    except Exception as err:
        print("ERROR create index,\n\terr=" + str(err))

    print(str(datetime.today()) + " : END of migration v3_2_3_second_phone_number revision=ca44f5d0984c")


def downgrade():
    pass
