"""v3_4_5_new_form_pat

Revision ID: 352eb3c5188f
Revises: e404bf2dacd0
Create Date: 2024-04-10 16:36:29.511631

"""
from alembic import op
from sqlalchemy import text

from datetime import datetime

# revision identifiers, used by Alembic.
revision = '352eb3c5188f'
down_revision = 'e404bf2dacd0'
branch_labels = None
depends_on = None


def upgrade():
    print("--- " + str(datetime.today()) + "---")
    print("START of migration v3_4_5_new_form_pat revision=352eb3c5188f")

    # Get the current
    conn = op.get_bind()

    # MODIFY COLUMN date_validation
    try:
        conn.execute(text("alter table sigl_10_data modify date_validation datetime"))
    except Exception as err:
        print("ERROR modify date_validation of sigl_10_data to datetime,\n\terr=" + str(err))

    # NEW DIRECTORY IN STORAGE
    try:
        import pathlib

        pathlib.Path("/storage/resource/form/patient").mkdir(mode=0o777, parents=True, exist_ok=True)
    except Exception as err:
        print("ERROR mkdir -p /storage/resource/form/patient,\n\terr=" + str(err))

    # COPY resource form patient
    try:
        from distutils.dir_util import copy_tree

        fromDirectory = "alembic/resource/form/patient"
        toDirectory = "/storage/resource/form/patient"

        copy_tree(fromDirectory, toDirectory)
    except Exception as err:
        print("ERROR copy alembic resource form patient,\n\terr=" + str(err))

    print(str(datetime.today()) + " : END of migration v3_4_5_new_form_pat revision=352eb3c5188f")


def downgrade():
    pass
