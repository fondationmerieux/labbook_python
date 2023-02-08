# -*- coding:utf-8 -*-
"""v3_0_10_new_type_sample

Revision ID: 69fede710356
Revises: e168aeda94b8
Create Date: 2021-06-24 14:33:02.851562

"""
from alembic import op
from sqlalchemy import text

from datetime import datetime

# revision identifiers, used by Alembic.
revision = '69fede710356'
down_revision = 'e168aeda94b8'
branch_labels = None
depends_on = None


def upgrade():
    print("--- " + str(datetime.today()) + "---")
    print("START of migration v3.0.10_new_type_sample revision=69fede710356")

    # Get the current
    conn = op.get_bind()

    # Insert new type of sample
    try:
        conn.execute(text('insert into sigl_dico_data (id_owner, dico_name, label, short_label, position, code) '
                     'values (1000, "type_prel", "Prélèvement pus", "Pus", 1200, "Pus")'))
    except Exception as err:
        print("ERROR insert type of sample Pus,\n\terr=" + str(err))

    # database_status
    try:
        # Create table for database_status
        conn.execute(text("create table database_status("
                          "dbs_ser int not NULL AUTO_INCREMENT,"
                          "dbs_date DATETIME,"
                          "dbs_stat VARCHAR(255),"
                          "PRIMARY KEY (dbs_ser))"))
    except Exception as err:
        print("ERROR create table database_status,\n\terr=" + str(err))

    print(str(datetime.today()) + " : END of migration v3.0.10_new_type_sample revision=69fede710356")


def downgrade():
    pass
