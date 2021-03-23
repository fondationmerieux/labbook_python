"""v3_0_1_stock_and_prescribers_change

Revision ID: e23db03512eb
Revises: 71b4a9a97b7a
Create Date: 2021-03-12 09:59:44.663714

"""
from alembic import op
import sqlalchemy as sa

from datetime import datetime

# revision identifiers, used by Alembic.
revision = 'e23db03512eb'
down_revision = '71b4a9a97b7a'
branch_labels = None
depends_on = None


def upgrade():
    print("--- " + str(datetime.today()) + "---")
    print("START of migration v3_0_1_stock_and_prescribers_change revision=e23db03512eb")

    # Get the current
    conn = op.get_bind()

    # REMOVE PREVIOUS ALL PRODUCT STATUS ADDED IN V3.0.0 AND NOT REPLACED
    try:
        conn.execute("delete from sigl_dico_data "
                     "where dico_name='product_status'")
    except:
        print("ERROR delete from sigl_dico_data where dico_name='product_status'")

    # REMOVE PREVIOUS ALL PRODUCT TYPE ADDED IN V3.0.0
    try:
        conn.execute("delete from sigl_dico_data "
                     "where dico_name='product_type'")
    except:
        print("ERROR delete from sigl_dico_data where dico_name='product_type'")

    # ADD PRODUCT TYPE IN DICT TABLE
    try:
        conn.execute("insert into sigl_dico_data "
                     "(id_owner, dico_name, label, short_label, position, code) "
                     "values (100, 'product_type', 'Consommables', 'consommables', 10, 'consommables')")
    except:
        print("ERROR insert into sigl_dico_data a product_type (consommables)")

    try:
        conn.execute("insert into sigl_dico_data "
                     "(id_owner, dico_name, label, short_label, position, code) "
                     "values (100, 'product_type', 'Réactifs généraux', 'reactif_gen', 20, 'reactif_gen')")
    except:
        print("ERROR insert into sigl_dico_data a product_type (reactif_gen)")

    try:
        conn.execute("insert into sigl_dico_data "
                     "(id_owner, dico_name, label, short_label, position, code) "
                     "values (100, 'product_type', 'Produits chimiques', 'chimiques', 30, 'chimiques')")
    except:
        print("ERROR insert into sigl_dico_data a product_type (chimiques)")

    try:
        conn.execute("insert into sigl_dico_data "
                     "(id_owner, dico_name, label, short_label, position, code) "
                     "values (100, 'product_type', 'Hygiène et sécurité', 'hygiene', 40, 'hygiene')")
    except:
        print("ERROR insert into sigl_dico_data a product_type (hygiene)")

    try:
        conn.execute("insert into sigl_dico_data "
                     "(id_owner, dico_name, label, short_label, position, code) "
                     "values (100, 'product_type', 'Biochimie', 'biochimie', 50, 'biochimie')")
    except:
        print("ERROR insert into sigl_dico_data a product_type (biochimie)")

    try:
        conn.execute("insert into sigl_dico_data "
                     "(id_owner, dico_name, label, short_label, position, code) "
                     "values (100, 'product_type', 'Hématologie', 'hematologie', 60, 'hematologie' )")
    except:
        print("ERROR insert into sigl_dico_data a product_type (hematologie)")

    try:
        conn.execute("insert into sigl_dico_data "
                     "(id_owner, dico_name, label, short_label, position, code) "
                     "values (100, 'product_type', 'Sérologie', 'serologie', 70, 'serologie')")
    except:
        print("ERROR insert into sigl_dico_data a product_type (serologie)")

    try:
        conn.execute("insert into sigl_dico_data "
                     "(id_owner, dico_name, label, short_label, position, code) "
                     "values (100, 'product_type', 'Microbiologie', 'microbio', 80, 'microbio')")
    except:
        print("ERROR insert into sigl_dico_data a product_type (microbio)")

    # REMOVE PREVIOUS ALL PRODUCT CONSERV ADDED IN V3.0.0
    try:
        conn.execute("delete from sigl_dico_data "
                     "where dico_name='product_conserv'")
    except:
        print("ERROR delete from sigl_dico_data where dico_name='product_conserv'")

    # ADD CONSERVATION TYPE IN DICT TABLE
    try:
        conn.execute("insert into sigl_dico_data "
                     "(id_owner, dico_name, label, short_label, position, code) "
                     "values (100, 'product_conserv', '2 - 4°C', 'frigo_2_4', 10, 'frigo_2_4' )")
    except:
        print("ERROR insert into sigl_dico_data a product_conserv (frigo_2_4)")

    try:
        conn.execute("insert into sigl_dico_data "
                     "(id_owner, dico_name, label, short_label, position, code) "
                     "values (100, 'product_conserv', '2 - 8°C', 'frigo_2_8', 20, 'frigo_2_8' )")
    except:
        print("ERROR insert into sigl_dico_data a product_conserv (frigo_2_8)")

    try:
        conn.execute("insert into sigl_dico_data "
                     "(id_owner, dico_name, label, short_label, position, code) "
                     "values (100, 'product_conserv', '4 - 12°C', 'frigo_4_12', 30, 'frigo_4_12' )")
    except:
        print("ERROR insert into sigl_dico_data a product_conserv (frigo_4_12)")

    try:
        conn.execute("insert into sigl_dico_data "
                     "(id_owner, dico_name, label, short_label, position, code) "
                     "values (100, 'product_conserv', '-20°C', 'congel_20', 40, 'congel_20' )")
    except:
        print("ERROR insert into sigl_dico_data a product_conserv (congel_20)")

    try:
        conn.execute("insert into sigl_dico_data "
                     "(id_owner, dico_name, label, short_label, position, code) "
                     "values (100, 'product_conserv', '-80°C', 'congel_80', 50, 'congel_80' )")
    except:
        print("ERROR insert into sigl_dico_data a product_conserv (congel_80)")

    try:
        conn.execute("insert into sigl_dico_data "
                     "(id_owner, dico_name, label, short_label, position, code) "
                     "values (100, 'product_conserv', 'T ambiante', 'ambiante', 60, 'ambiante' )")
    except:
        print("ERROR insert into sigl_dico_data a product_conserv (ambiante)")

    # ADD COLUMN TO USER TABLE FOR ASSOCIATE A SIDE ACCOUNT
    try:
        op.add_column('sigl_user_data', sa.Column('side_account', sa.Integer))
    except:
        print("ERROR add column side_account to sigl_user_data")
    else:
        # UPDATE NEW COLUMN side_account IN sigl_user_data
        try:
            conn = op.get_bind()

            conn.execute('update sigl_user_data set side_account=0')
        except:
            print("ERROR update sigl_user_data set side_account=0")

    # ADD and REPLACE MANUALS
    ## TODO

    print("END of migration v3_0_1_stock_and_prescribers_change revision=e23db03512eb")


def downgrade():
    pass
