"""v3_3_15_retry_to_create_manual_setting

Revision ID: f7f46cfe7e02
Revises: cea1c6149ba8
Create Date: 2023-10-06 09:11:04.870990

"""
from alembic import op
from sqlalchemy import text

from datetime import datetime

# revision identifiers, used by Alembic.
revision = 'f7f46cfe7e02'
down_revision = 'cea1c6149ba8'
branch_labels = None
depends_on = None


def upgrade():
    print("--- " + str(datetime.today()) + "---")
    print("START of migration v3_3_15_retry_to_create_manual_setting revision=f7f46cfe7e02")

    # Get the current
    conn = op.get_bind()

    # Create table for manual category
    try:
        conn.execute(text("create table if not exists manual_setting("
                          "mas_ser int not NULL AUTO_INCREMENT,"
                          "mas_date DATETIME,"
                          "mas_rank INT default 0,"
                          "mas_name varchar(100) unique not null,"
                          "PRIMARY KEY (mas_ser),"
                          "INDEX (mas_rank), INDEX (mas_name)) "
                          "character set=utf8"))
    except Exception as err:
        print("ERROR create table manual_setting,\n\terr=" + str(err))
    
    print(str(datetime.today()) + " : END of migration v3_3_15_retry_to_create_manual_setting revision=f7f46cfe7e02")


def downgrade():
    pass
