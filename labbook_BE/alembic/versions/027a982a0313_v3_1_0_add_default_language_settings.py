# -*- coding:utf-8 -*-
"""v3_1_0_add_default_language_settings

Revision ID: 027a982a0313
Revises: a45b98972abb
Create Date: 2021-08-31 16:22:10.739567

"""
from alembic import op

from datetime import datetime

# revision identifiers, used by Alembic.
revision = '027a982a0313'
down_revision = 'a45b98972abb'
branch_labels = None
depends_on = None


def upgrade():
    print("--- " + str(datetime.today()) + "---")
    print("START of migration v3_1_0_add_default_language_settings revision=027a982a0313")

    # Get the current
    conn = op.get_bind()

    # Insert default language settings
    try:
        conn.execute('insert into sigl_06_data (id_owner, identifiant, label, value) '
                     'values (1000, "default_language", "Langue par défaut (rapport aussi)", "fr_FR")')
    except Exception as err:
        print("ERROR insert default language settings,\n\terr=" + str(err))

    # Insert default language settings
    try:
        conn.execute('insert into sigl_06_data (id_owner, identifiant, label, value) '
                     'values (1000, "db_language", "Langue du référentiel", "fr_FR")')
    except Exception as err:
        print("ERROR insert default language settings,\n\terr=" + str(err))

    print(str(datetime.today()) + " : END of migration v3_1_0_add_default_language_settings revision=027a982a0313")


def downgrade():
    pass
