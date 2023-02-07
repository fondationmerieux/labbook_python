# -*- coding:utf-8 -*-
"""v3_2_5_update_nonconformities_column

Revision ID: 588cfbb88538
Revises: 8cf6c432fcfb
Create Date: 2022-04-07 16:17:14.655009

"""
from alembic import op
from sqlalchemy import text

from datetime import datetime

# revision identifiers, used by Alembic.
revision = '588cfbb88538'
down_revision = '8cf6c432fcfb'
branch_labels = None
depends_on = None


def upgrade():
    print("--- " + str(datetime.today()) + "---")
    print("START of migration v3_2_5_update_nonconformities_column revision=588cfbb88538")

    # Get the current
    conn = op.get_bind()

    # convert value of impact_patient and impacts_perso_visit from sigl_non_conformite_data
    try:
        conn.execute(text("update sigl_non_conformite_data set impact_patient=1053 where impact_patient=4"))
    except Exception as err:
        print("ERROR convert value of impact_patient 4 to 1053,\n\terr=" + str(err))

    try:
        conn.execute(text("update sigl_non_conformite_data set impact_patient=1055 where impact_patient=5"))
    except Exception as err:
        print("ERROR convert value of impact_patient 5 to 1055,\n\terr=" + str(err))

    try:
        conn.execute(text("update sigl_non_conformite_data set impact_patient=1057 where impact_patient=6"))
    except Exception as err:
        print("ERROR convert value of impact_patient 6 to 1057,\n\terr=" + str(err))

    try:
        conn.execute(text("update sigl_non_conformite_data set impact_patient=0 where impact_patient=7"))
    except Exception as err:
        print("ERROR convert value of impact_patient 7 to 0,\n\terr=" + str(err))

    try:
        conn.execute(text("update sigl_non_conformite_data set impacts_perso_visit=1053 where impacts_perso_visit=4"))
    except Exception as err:
        print("ERROR convert value of impacts_perso_visit 4 to 1053,\n\terr=" + str(err))

    try:
        conn.execute(text("update sigl_non_conformite_data set impacts_perso_visit=1055 where impacts_perso_visit=5"))
    except Exception as err:
        print("ERROR convert value of impacts_perso_visit 5 to 1055,\n\terr=" + str(err))

    try:
        conn.execute(text("update sigl_non_conformite_data set impacts_perso_visit=1057 where impacts_perso_visit=6"))
    except Exception as err:
        print("ERROR convert value of impacts_perso_visit 6 to 1057,\n\terr=" + str(err))

    try:
        conn.execute(text("update sigl_non_conformite_data set impacts_perso_visit=0 where impacts_perso_visit=7"))
    except Exception as err:
        print("ERROR convert value of impacts_perso_visit 7 to 0,\n\terr=" + str(err))

    print(str(datetime.today()) + " : END of migration v3_2_5_update_nonconformities_column revision=588cfbb88538")


def downgrade():
    pass
