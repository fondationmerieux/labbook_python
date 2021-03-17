"""v3_0_2_stock_and_add_new_manual

Revision ID: 5b3058a99439
Revises: e23db03512eb
Create Date: 2021-03-16 16:07:15.000345

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5b3058a99439'
down_revision = 'e23db03512eb'
branch_labels = None
depends_on = None


def upgrade():
    # Get the current
    conn = op.get_bind()

    # ADD COLUMN TO PRODUCT DETAILS TABLE
    try:
        op.add_column('product_details', sa.Column('prd_safe_limit', sa.Integer, 0))
    except:
        print("ERROR add column prd_safe_limit to product_details")
    else:
        # UPDATE NEW COLUMN prd_safe_limit IN product_details
        try:
            conn = op.get_bind()

            conn.execute('update product_details set prd_safe_limit=0')
        except:
            print("ERROR update product_details set prd_safe_limit=0")

    # DROP COLUMN TO PRODUCT SUPPLY TABLE
    try:
        op.drop_column('product_supply', sa.Column('prs_status'))
    except:
        print("ERROR drop column prs_status to product_supply")

    # DROP COLUMN TO PRODUCT SUPPLY TABLE
    try:
        op.drop_column('product_supply', sa.Column('prs_sell_price'))
    except:
        print("ERROR drop column prs_sell_price to product_supply")

    # ADD COLUMN TO PRODUCT SUPPLY TABLE
    try:
        op.add_column('product_supply', sa.Column('prs_empty', sa.String(1), 'N'))
    except:
        print("ERROR add column prs_empty to product_supply")
    else:
        # UPDATE NEW COLUMN prs_empty IN product_supply
        try:
            conn = op.get_bind()

            conn.execute('update product_supply set prs_empty="N"')
        except:
            print("ERROR update product_supply set prs_empty='N'")

    # DELETE ALL IN sigl_storage_data
    try:
        conn.execute("delete from sigl_storage_data")
    except:
        print("ERROR delete from sigl_storage_data")

    # ADD default storage path
    try:
        conn.execute("insert into sigl_storage_data "
                     "(id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, path) "
                     "values (100, NOW(), NOW(), 100, '/storage' )")
    except:
        print("ERROR insert into sigl_storage_data a default storage path")


def downgrade():
    pass
