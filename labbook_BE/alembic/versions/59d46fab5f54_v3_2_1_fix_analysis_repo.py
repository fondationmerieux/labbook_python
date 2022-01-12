# -*- coding:utf-8 -*-
"""v3_2_1_fix_analysis_repo

Revision ID: 59d46fab5f54
Revises: 5a4e9dbb96dc
Create Date: 2021-12-20 10:52:22.584847

"""
from alembic import op

from datetime import datetime

# revision identifiers, used by Alembic.
revision = '59d46fab5f54'
down_revision = '5a4e9dbb96dc'
branch_labels = None
depends_on = None


def upgrade():
    print("--- " + str(datetime.today()) + "---")
    print("START of migration v3_2_1_fix_analysis_repo revision=59d46fab5f54")

    # Get the current
    conn = op.get_bind()

    # UPDATE wrong minimal value for B008
    try:
        conn.execute("update sigl_07_data set normal_min='2.15' "
                     "where normal_min='2. 15' ")
    except Exception as err:
        print("ERROR update normal_min for B008,\n\terr=" + str(err))

    # NEW TABLE for load list of zip code city and region
    try:
        conn.execute("create table zip_city ("
                     "zic_ser int not NULL AUTO_INCREMENT, "
                     "zic_date datetime, "
                     "zic_zip varchar(10), "
                     "zic_city varchar(40), "
                     "PRIMARY KEY (zic_ser), "
                     "INDEX (zic_zip), INDEX (zic_city)) character set=utf8")
    except Exception as err:
        print("ERROR create table zip_city,\n\terr=" + str(err))

    print(str(datetime.today()) + " : END of migration v3_2_1_fix_analysis_repo revision=59d46fab5f54")

def downgrade():
    pass
