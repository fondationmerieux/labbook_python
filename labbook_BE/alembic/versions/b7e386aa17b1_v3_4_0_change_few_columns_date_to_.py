"""v3_4_0_change_few_columns_date_to_datetime

Revision ID: b7e386aa17b1
Revises: d4b6851a4a5c
Create Date: 2023-12-26 16:06:56.917313

"""
from alembic import op
from sqlalchemy import text

from datetime import datetime

# revision identifiers, used by Alembic.
revision = 'b7e386aa17b1'
down_revision = 'd4b6851a4a5c'
branch_labels = None
depends_on = None


def upgrade():
    print("--- " + str(datetime.today()) + "---")
    print("START of migration change_few_columns_date_to_datetime revision=b7e386aa17b1")

    # Get the current
    conn = op.get_bind()

    # ADD COLUMN for supplier
    try:
        conn.execute(text("alter table sigl_fournisseurs_data add column supp_critical varchar(1) not null default 'N'"))
    except Exception as err:
        print("ERROR add column supp_critical to sigl_fournisseurs_data,\n\terr=" + str(err))

    # CHANGE COLUMN date_reception_colis to rec_parcel_date
    try:
        conn.execute(text("alter table sigl_02_data change column date_reception_colis rec_parcel_date datetime"))
    except Exception as err:
        print("ERROR change column date_reception_colis to sigl_02_data,\n\terr=" + str(err))

    # CHANGE COLUMN date_reception to samp_receipt_date
    try:
        conn.execute(text("alter table sigl_01_data change column date_reception samp_receipt_date datetime"))
    except Exception as err:
        print("ERROR change column date_reception to sigl_01_data,\n\terr=" + str(err))

    # CHANGE COLUMN date_prel to samp_date
    try:
        conn.execute(text("alter table sigl_01_data change column date_prel samp_date datetime"))
    except Exception as err:
        print("ERROR change column date_prel to sigl_01_data,\n\terr=" + str(err))

    # DROP COLUMN heure_reception
    try:
        conn.execute(text("alter table sigl_01_data drop column heure_reception"))
    except Exception as err:
        print("ERROR drop column heure_reception to sigl_01_data,\n\terr=" + str(err))

    # --- UPDATE TABLE sigl_02_deleted ---
    # CHANGE COLUMN date_reception_colis to rec_parcel_date
    try:
        conn.execute(text("alter table sigl_02_deleted change column date_reception_colis rec_parcel_date datetime"))
    except Exception as err:
        print("ERROR change column date_reception_colis to sigl_02_deleted,\n\terr=" + str(err))

    try:
        conn.execute(text("alter table sigl_02_deleted add column date_hosp date"))
    except Exception as err:
        print("ERROR add column date_hosp to sigl_02_deleted,\n\terr=" + str(err))

    try:
        conn.execute(text("alter table sigl_02_deleted add column rec_custody varchar(1) not null default 'N'"))
    except Exception as err:
        print("ERROR add column rec_custody to sigl_02_deleted,\n\terr=" + str(err))

    try:
        conn.execute(text("alter table sigl_02_deleted add column rec_num_int varchar(30) not null default ''"))
    except Exception as err:
        print("ERROR add column rec_num_int to sigl_02_deleted,\n\terr=" + str(err))

    try:
        conn.execute(text("alter table sigl_02_deleted add column rec_date_vld datetime"))
    except Exception as err:
        print("ERROR add column rec_date_vld to sigl_02_deleted,\n\terr=" + str(err))

    try:
        conn.execute(text("alter table sigl_02_deleted add column rec_modified varchar(1) not null default 'N'"))
    except Exception as err:
        print("ERROR add column rec_modified to sigl_02_deleted,\n\terr=" + str(err))

    try:
        conn.execute(text("alter table sigl_02_deleted add column rec_hosp_num varchar(30) not null default ''"))
    except Exception as err:
        print("ERROR add column rec_hosp_num to sigl_02_deleted,\n\terr=" + str(err))

    # --- UPDATE TABLE sigl_01_deleted ---
    # CHANGE COLUMN date_reception to samp_receipt_date
    try:
        conn.execute(text("alter table sigl_01_deleted change column date_reception samp_receipt_date datetime"))
    except Exception as err:
        print("ERROR change column date_reception to sigl_01_deleted,\n\terr=" + str(err))

    try:
        conn.execute(text("alter table sigl_01_deleted change column date_prel samp_date datetime"))
    except Exception as err:
        print("ERROR change column date_prel to sigl_01_deleted,\n\terr=" + str(err))

    try:
        conn.execute(text("alter table sigl_01_deleted drop column heure_reception"))
    except Exception as err:
        print("ERROR drop column heure_reception to sigl_01_deleted,\n\terr=" + str(err))
    
    print(str(datetime.today()) + " : END of migration change_few_columns_date_to_datetime revision=b7e386aa17b1")


def downgrade():
    pass
