"""v3_3_9_lab_profil_and_stock_movement

Revision ID: 716a07e9a30a
Revises: d44f950a2b07
Create Date: 2023-06-20 11:04:31.141341

"""
from alembic import op
from sqlalchemy import text

from datetime import datetime


# revision identifiers, used by Alembic.
revision = '716a07e9a30a'
down_revision = 'd44f950a2b07'
branch_labels = None
depends_on = None


def upgrade():
    print("--- " + str(datetime.today()) + "---")
    print("START of migration v3_3_9_lab_profil_and_stock_movement revision=716a07e9a30a")

    # Get the current
    conn = op.get_bind()

    # ADD COLUMN for record
    try:
        conn.execute(text("alter table sigl_02_data add column rec_hosp_num varchar(30) not null default ''"))
    except Exception as err:
        print("ERROR add column rec_hosp_num to sigl_02_data,\n\terr=" + str(err))

    # ADD NEW USER ROLE
    try:
        conn.execute(text("insert into sigl_pj_role (name, label, type) "
                          "values ('laboratoire', 'Laboratoire', 'L')"))
    except Exception as err:
        print("ERROR insert into sigl_pj_role (laboratoire),\n\terr=" + str(err))

    # UPDATE label of secrétaire avancée
    try:
        conn.execute(text("update sigl_pj_role set label='Secrétaire avancé' where type='SA'"))
    except Exception as err:
        print("ERROR update label to sigl_pj_role,\n\terr=" + str(err))

    # Create table for manual category
    try:
        conn.execute(text("create table manual_setting("
                          "mas_ser int not NULL AUTO_INCREMENT,"
                          "mas_date DATETIME,"
                          "mas_rank INT default 0,"
                          "mas_name varchar(100) unique not null,"
                          "PRIMARY KEY (mas_ser),"
                          "INDEX (mas_rank), INDEX (mas_name)) "
                          "character set=utf8"))
    except Exception as err:
        print("ERROR create table manual_setting,\n\terr=" + str(err))

    # ADD COLUMN for serial of manual category in sigl_manuels_data table
    try:
        conn.execute(text("alter table sigl_manuels_data add column man_mas int not null default 0"))
    except Exception as err:
        print("ERROR add column man_mas to sigl_manuels_data,\n\terr=" + str(err))

    print(str(datetime.today()) + " : END of migration v3_3_9_lab_profil_and_stock_movement revision=716a07e9a30a")


def downgrade():
    pass
