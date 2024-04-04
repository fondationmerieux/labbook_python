"""v3_4_4_send_dhis2_to_api

Revision ID: e404bf2dacd0
Revises: e038e2ab0b42
Create Date: 2024-03-28 09:09:59.584697

"""
from alembic import op
from sqlalchemy import text

from datetime import datetime

# revision identifiers, used by Alembic.
revision = 'e404bf2dacd0'
down_revision = 'e038e2ab0b42'
branch_labels = None
depends_on = None


def upgrade():
    print("--- " + str(datetime.today()) + "---")
    print("START of migration send_dhis2_to_api revision=e404bf2dacd0")

    # Get the current
    conn = op.get_bind()

    # Create table dhis2_setting
    try:
        conn.execute(text("create table if not exists dhis2_setting("
                          "dhs_ser int not NULL AUTO_INCREMENT,"
                          "dhs_date DATETIME,"
                          "dhs_user INT default 0,"
                          "dhs_name varchar(100) NOT NULL,"
                          "dhs_login varchar(50) NOT NULL,"
                          "dhs_pwd varchar(50) NOT NULL,"
                          "dhs_url varchar(255) NOT NULL,"
                          "dhs_default varchar(1) NOT NULL default 'N',"
                          "PRIMARY KEY (dhs_ser),"
                          "INDEX (dhs_login)) "
                          "character set=utf8"))
    except Exception as err:
        print("ERROR create table dhis2_setting,\n\terr=" + str(err))

    print(str(datetime.today()) + " : END of migration send_dhis2_to_api revision=e404bf2dacd0")


def downgrade():
    pass
