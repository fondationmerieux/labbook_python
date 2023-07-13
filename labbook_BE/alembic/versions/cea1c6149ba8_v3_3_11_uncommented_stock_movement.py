"""v3_3_12_uncommented_stock_movement

Revision ID: cea1c6149ba8
Revises: 716a07e9a30a
Create Date: 2023-07-07 10:28:30.778786

"""
from alembic import op
import sqlalchemy import text

from datetime import datetime


# revision identifiers, used by Alembic.
revision = 'cea1c6149ba8'
down_revision = '716a07e9a30a'
branch_labels = None
depends_on = None


def upgrade():
    print("--- " + str(datetime.today()) + "---")
    print("START of migration v3_3_12_lab_profil_and_stock_movement revision=cea1c6149ba8")

    # Get the current
    conn = op.get_bind()

    # Create table for local of stock
    try:
        conn.execute(text("create table product_local("
                          "prl_ser int not NULL AUTO_INCREMENT,"
                          "prl_date DATETIME,"
                          "prl_rank INT default 0,"
                          "prl_name varchar(100) unique not null,"
                          "PRIMARY KEY (prl_ser),"
                          "INDEX (prl_rank), INDEX (prl_name)) "
                          "character set=utf8"))
    except Exception as err:
        print("ERROR create table product_local,\n\terr=" + str(err))

    # ADD previous local fields from product_supply
    try:
        conn.execute(text("insert into product_local (prl_name, prl_date, prl_rank) "
                          "(select prs_rack, now(), 0 from product_supply where prs_rack != '' "
                          "group by prs_rack order by prs_rack)"))
    except Exception as err:
        print("ERROR insert into product_local (previous local from product_supply),\n\terr=" + str(err))

    # ADD COLUMN for serial of local product in product supply table
    try:
        conn.execute(text("alter table product_supply add column prs_prl int not null default 0"))
    except Exception as err:
        print("ERROR add column prs_prl to product_supply,\n\terr=" + str(err))

    # COPY info serial local to new column in product_supply
    try:
        conn.execute(text("update product_supply inner join product_local on prl_name=prs_rack "
                          "set prs_prl=prl_ser "))
    except Exception as err:
        print("ERROR update product_supply inner join product_local on prl_name=prs_rack set prs_prl=prl_ser,\n\terr=" + str(err))

    # DROP COLUMN prs_rack
    try:
        conn.execute(text("alter table product_supply drop column prs_rack"))
    except Exception as err:
        print("ERROR drop column prs_rack to product_supply,\n\terr=" + str(err))

    # ADD COLUMN for remove empty product supply
    try:
        conn.execute(text("alter table product_supply add column prs_remove varchar(1) not null default 'N'"))
    except Exception as err:
        print("ERROR add column prs_remove to product_supply,\n\terr=" + str(err))

    # ADD COLUMN for user who remove empty product supply
    try:
        conn.execute(text("alter table product_supply add column prs_user_remove int default 0"))
    except Exception as err:
        print("ERROR add column prs_user_remove to product_supply,\n\terr=" + str(err))

    print(str(datetime.today()) + " : END of migration v3_3_12_lab_profil_and_stock_movement revision=cea1c6149ba8")


def downgrade():
    pass
