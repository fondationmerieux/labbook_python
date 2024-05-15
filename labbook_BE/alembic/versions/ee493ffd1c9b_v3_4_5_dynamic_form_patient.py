"""v3_4_5_dynamic_form_patient

Revision ID: ee493ffd1c9b
Revises: 352eb3c5188f
Create Date: 2024-05-06 15:05:49.159422

"""
from alembic import op
from sqlalchemy import text

from datetime import datetime


# revision identifiers, used by Alembic.
revision = 'ee493ffd1c9b'
down_revision = '352eb3c5188f'
branch_labels = None
depends_on = None


def upgrade():
    print("--- " + str(datetime.today()) + "---")
    print("START of migration v3_4_5_dynamic_form_patient revision=ee493ffd1c9b")

    # Get the current
    conn = op.get_bind()

    # Create table patient_form_item
    try:
        conn.execute(text("create table if not exists patient_form_item("
                          "pfi_ser int not NULL AUTO_INCREMENT,"
                          "pfi_date DATETIME,"
                          "pfi_user INT default 0,"
                          "pfi_pat INT not NULL,"
                          "pfi_act varchar(1) NOT NULL default 'Y',"
                          "pfi_key varchar(80) NOT NULL,"
                          "pfi_value varchar(65535) NOT NULL,"
                          "PRIMARY KEY (pfi_ser),"
                          "INDEX (pfi_key), INDEX (pfi_act), INDEX (pfi_pat)) "
                          "character set=utf8"))
    except Exception as err:
        print("ERROR create table patient_form_item,\n\terr=" + str(err))

    # ADD COLUMN var_show_minmax in table test
    try:
        conn.execute(text("alter table sigl_07_data_test add column var_show_minmax varchar(1) not null default 'N'"))
    except Exception as err:
        print("ERROR add column var_show_minmax to sigl_07_data_test,\n\terr=" + str(err))

    print(str(datetime.today()) + " : END of migration v3_4_5_dynamic_form_patient revision=ee493ffd1c9b")


def downgrade():
    pass
