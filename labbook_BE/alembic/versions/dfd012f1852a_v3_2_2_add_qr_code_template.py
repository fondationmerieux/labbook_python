# -*- coding:utf-8 -*-
"""v3_2_2_add_qr_code_template

Revision ID: dfd012f1852a
Revises: 59d46fab5f54
Create Date: 2022-02-22 10:14:35.982029

"""
from alembic import op

from datetime import datetime

# revision identifiers, used by Alembic.
revision = 'dfd012f1852a'
down_revision = '59d46fab5f54'
branch_labels = None
depends_on = None


def upgrade():
    print("--- " + str(datetime.today()) + "---")
    print("START of migration v3_2_2_add_qr_code_template revision=dfd012f1852a")

    # Get the current
    conn = op.get_bind()

    # ADD template QR code
    try:
        conn.execute("insert into template_setting "
                     "(tpl_date, tpl_name, tpl_file, tpl_default, tpl_type) "
                     "values (NOW(), 'Modèle code QR', 'template_qrcode.toml', 'Y', 'QRC')")
    except Exception as err:
        print("ERROR insert default QR code template for template_setting,\n\terr=" + str(err))

    # ADD flag for generate a QR code image
    try:
        conn.execute("alter table sigl_05_07_data add column var_qrcode varchar(10) default 'N'")
    except Exception as err:
        print("ERROR add column var_qrcode to sigl_05_07_data,\n\terr=" + str(err))
    else:
        # change for antibiogramme variables
        try:
            conn.execute("update sigl_05_07_data set var_qrcode='Y' "
                         "where id_refanalyse in (select id_data from sigl_05_data where position=1 and code in "
                         "('B4274','B4719','B4721','B5271a','B5271b'))")
        except Exception as err:
            print("ERROR update var_qrcode,\n\terr=" + str(err))
    
    print(str(datetime.today()) + " : END of migration v3_2_2_add_qr_code_template revision=dfd012f1852a")


def downgrade():
    pass
