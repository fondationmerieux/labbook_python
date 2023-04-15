"""v3_3_7_default_indicator

Revision ID: c341c66fe1f0
Revises: 6fee80b9f8b8
Create Date: 2023-04-07 16:01:53.242302

"""
from alembic import op
import sqlalchemy import text

from datetime import datetime

# revision identifiers, used by Alembic.
revision = 'c341c66fe1f0'
down_revision = '6fee80b9f8b8'
branch_labels = None
depends_on = None


def upgrade():
    print("--- " + str(datetime.today()) + "---")
    print("START of migration v3_3_7_default_indicator revision=c341c66fe1f0")

    # Get the current
    conn = op.get_bind()

    # NEW DIRECTORY IN STORAGE
    try:
        import pathlib

        pathlib.Path("/storage/resource/indicator").mkdir(mode=0o777, parents=False, exist_ok=True)
    except Exception as err:
        print("ERROR mkdir -p /storage/resource/indicator,\n\terr=" + str(err))

    # COPY alembic resource indicator
    try:
        from distutils.dir_util import copy_tree

        fromDirectory = "alembic/resource/indicator"
        toDirectory = "/storage/resource/indicator"

        copy_tree(fromDirectory, toDirectory)
    except Exception as err:
        print("ERROR copy alembic resource indicator,\n\terr=" + str(err))

    # COPY alembic resource dhis2
    try:
        from distutils.dir_util import copy_tree

        fromDirectory = "alembic/resource/dhis2"
        toDirectory = "/storage/resource/dhis2"

        copy_tree(fromDirectory, toDirectory)
    except Exception as err:
        print("ERROR copy alembic resource dhis2,\n\terr=" + str(err))

    print(str(datetime.today()) + " : END of migration v3_3_7_default_indicator revision=c341c66fe1f0")


def downgrade():
    pass
