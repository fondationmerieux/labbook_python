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

    # ADD COLUMN for users
    try:
        conn.execute("alter table sigl_user_data add column tmp_status varchar(10) not null")
    except Exception as err:
        print("ERROR add column tmp_status to sigl_user_data,\n\terr=" + str(err))

    # UPDATE users tmp_status
    try:
        conn.execute("update sigl_user_data set tmp_status='A' where status=29")
        conn.execute("update sigl_user_data set tmp_status='D' where status=30")
        conn.execute("update sigl_user_data set tmp_status='X' where status=31")
    except Exception as err:
        print("ERROR update status to sigl_user_data,\n\terr=" + str(err))

    # Drop column users status
    try:
        conn.execute("alter table sigl_user_data drop column status")
    except Exception as err:
        print("ERROR drop column status in sigl_user_data,\n\terr=" + str(err))

    # RENAME COLUMN tmp_status to status
    try:
        conn.execute("alter table sigl_user_data change `tmp_status` status varchar(10) not null")
    except Exception as err:
        print("ERROR alter table sigl_user_data change `tmp_status` status varchar(10),\n\terr=" + str(err))

    # ADD second phone number for patient
    try:
        conn.execute("alter table sigl_03_data add column pat_phone2 varchar(20)")
    except Exception as err:
        print("ERROR add column pat_phone2 to sigl_03_data,\n\terr=" + str(err))

    # ADD INDEX
    try:
        conn.execute("create index idx_status on sigl_user_data (status)")
        conn.execute("create index idx_role_type on sigl_user_data (role_type)")
        conn.execute("create index idx_code on sigl_01_data (code)")
        conn.execute("create index idx_status on sigl_02_data (statut)")
        conn.execute("create index idx_phone1 on sigl_03_data (tel)")
        conn.execute("create index idx_phone2 on sigl_03_data (pat_phone2)")
        conn.execute("create index idx_oblig on sigl_05_07_data (obligatoire)")
        conn.execute("create index idx_whonet on sigl_05_07_data (var_whonet)")
        conn.execute("create index idx_pos on sigl_05_07_data (position)")
        conn.execute("create index idx_num_var on sigl_05_07_data (num_var)")
    except Exception as err:
        print("ERROR create index,\n\terr=" + str(err))

    print(str(datetime.today()) + " : END of migration v3_2_3_second_phone_number revision=ca44f5d0984c")


def downgrade():
    pass
