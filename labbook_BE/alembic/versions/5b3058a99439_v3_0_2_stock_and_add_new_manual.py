"""v3_0_2_stock_and_add_new_manual

Revision ID: 5b3058a99439
Revises: e23db03512eb
Create Date: 2021-03-16 16:07:15.000345

"""
from alembic import op
import sqlalchemy as sa

from datetime import datetime

# revision identifiers, used by Alembic.
revision = '5b3058a99439'
down_revision = 'e23db03512eb'
branch_labels = None
depends_on = None


def upgrade():
    print("--- " + str(datetime.today()) + "---")
    print("START of migration v3_0_2_stock_and_add_new_manual revision=5b3058a99439")

    # Get the current
    conn = op.get_bind()

    # DELETE B603 ANALYSIS Recherche de Plasmodium
    try:
        conn.execute("delete from sigl_05_data "
                     "where code='B603' and famille=15")
    except:
        print("ERROR delete from sigl_05_data where code='B603' and famille=15")

    # DROP COLUMN TO PRODUCT SUPPLY TABLE
    try:
        # DOESNT WORK op.drop_column('backup_setting', sa.Column('bks_pwd'))
        conn.execute("alter table backup_setting drop column bks_pwd")
    except:
        print("ERROR drop column bks_pwd to backup_setting")

    # ADD COLUMN TO PRODUCT DETAILS TABLE
    try:
        # DOESNT WORK op.add_column('product_details', sa.Column('prd_safe_limit', sa.Integer, 0))
        conn.execute("alter table product_details add column prd_safe_limit int default 0")
    except:
        print("ERROR add column prd_safe_limit to product_details")
    else:
        # UPDATE NEW COLUMN prd_safe_limit IN product_details
        try:
            conn = op.get_bind()

            conn.execute('update product_details set prd_safe_limit=0')
        except:
            print("ERROR update product_details set prd_safe_limit=0")

    # ADD COLUMN TO PRODUCT SUPPLY TABLE
    try:
        # DOESNT WORK op.add_column('product_supply', sa.Column('prs_user', sa.Integer, 0))
        conn.execute("alter table product_supply add column prs_user int default 0")
    except:
        print("ERROR add column prd_user to product_supply")
    else:
        # UPDATE NEW COLUMN prd_user IN product_supply
        try:
            conn = op.get_bind()

            conn.execute('update product_supply set prs_user=0')
        except:
            print("ERROR update product_supply set prs_user=0")

    # DROP COLUMN TO PRODUCT SUPPLY TABLE
    try:
        # DOESNT WORK op.drop_column('product_supply', sa.Column('prs_status'))
        conn.execute("alter table product_supply drop column prs_status")
    except:
        print("ERROR drop column prs_status to product_supply")

    # DROP COLUMN TO PRODUCT SUPPLY TABLE
    try:
        # DOESNT WORK op.drop_column('product_supply', sa.Column('prs_sell_price'))
        conn.execute("alter table product_supply drop column prs_sell_price")
    except:
        print("ERROR drop column prs_sell_price to product_supply")

    # ADD COLUMN TO PRODUCT SUPPLY TABLE
    try:
        # DOESNT WORK op.add_column('product_supply', sa.Column('prs_empty', sa.String(1), 'N'))
        conn.execute("alter table product_supply add column prs_empty varchar(1) not null default 'N'")
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
                     "(id_data, id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, path) "
                     "values (1, 100, NOW(), NOW(), 100, '/storage' )")
    except:
        print("ERROR insert into sigl_storage_data a default storage path")

    # DELETE OLD MANUALS
    try:
        conn.execute("delete from sigl_manuels_data where id_data in (5,6,10,11)")
    except:
        print("ERROR delete from sigl_manuels_data where id_data in (5,6,10,11)")

    try:
        conn.execute("delete from sigl_manuels_document__file_data where id_ext in (5,6,10,11)")
    except:
        print("ERROR delete from sigl_manuels_document__file_data where id_ext in (5,6,10,11)")

    try:
        conn.execute("delete from sigl_file_data where id_data in (5,7,12,13)")
    except:
        print("ERROR delete from sigl_file_data where id_data in (5,7,12,13)")

    # --- ADD NEW MANUALS ---

    # Laboratory biosafety manual 4th ed.
    try:
        conn.execute("insert into sigl_manuels_data "
                     "(id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, titre , reference, "
                     "redacteur_id, verificateur_id, approbateur_id, date_insert, date_apply, date_update, section) "
                     "values (100, now(), now(), 100, 'Laboratory biosafety manual 4th ed.', '', 0, 0, 0, now(), now(), now(), 0)")
    except:
        print("ERROR insert into sigl_manuels_data Laboratory biosafety manual 4th ed.")

    try:
        conn.execute("insert into sigl_file_data "
                     "(id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, status, date_creation, "
                     "original_name, generated_name, size, hash, ext, content_type, id_storage, path) "
                     "values (100, now(), now(), 100, 1, now(), 'LBM4.pdf', "
                     "'7631273b506e08bedb54bb635949299a', 3142655, '20f75956e0a807e954d3a4faad14e0f8', "
                     "'pdf', 'application/pdf', 1, '76/31/')")
    except:
        print("ERROR insert into sigl_file_data LBM4.pdf")

    try:
        conn.execute("insert into sigl_manuels_document__file_data "
                     "(id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, id_ext, id_file) "
                     "values (100, now(), now(), 100, (select id_data from sigl_manuels_data order by id_data desc limit 1), "
                     "(select id_data from sigl_file_data order by id_data desc limit 1))")
    except:
        print("ERROR insert into sigl_manuels_document__file_data")

    # Laboratory biosafety manual 4th ed. Risk Assessment
    try:
        conn.execute("insert into sigl_manuels_data "
                     "(id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, titre , reference, "
                     "redacteur_id, verificateur_id, approbateur_id, date_insert, date_apply, date_update, section) "
                     "values (100, now(), now(), 100, 'Laboratory biosafety manual 4th ed. Risk Assessment', '', 0, 0, 0, now(), now(), now(), 0)")
    except:
        print("ERROR insert into sigl_manuels_data Laboratory biosafety manual 4th ed. Risk Assessment")

    try:
        conn.execute("insert into sigl_file_data "
                     "(id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, status, date_creation, "
                     "original_name, generated_name, size, hash, ext, content_type, id_storage, path) "
                     "values (100, now(), now(), 100, 1, now(), 'LBM4_Risk_Assessment.pdf', "
                     "'d43b5882e7c909ee1bdc5cc74334b0ba', 2909550, '4e259c8d7cc50adfcef79ccb1f749682', "
                     "'pdf', 'application/pdf', 1, 'd4/3b/')")
    except:
        print("ERROR insert into sigl_file_data LBM4_Risk_Assessment.pdf")

    try:
        conn.execute("insert into sigl_manuels_document__file_data "
                     "(id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, id_ext, id_file) "
                     "values (100, now(), now(), 100, (select id_data from sigl_manuels_data order by id_data desc limit 1), "
                     "(select id_data from sigl_file_data order by id_data desc limit 1))")
    except:
        print("ERROR insert into sigl_manuels_document__file_data")

    # Laboratory biosafety manual 4th ed. Laboratory design and maintenance
    try:
        conn.execute("insert into sigl_manuels_data "
                     "(id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, titre , reference, "
                     "redacteur_id, verificateur_id, approbateur_id, date_insert, date_apply, date_update, section) "
                     "values (100, now(), now(), 100, 'Laboratory biosafety manual 4th ed. Laboratory design and maintenance', '', 0, 0, 0, now(), now(), now(), 0)")
    except:
        print("ERROR insert into sigl_manuels_data Laboratory biosafety manual 4th ed. Laboratory design and maintenance")

    try:
        conn.execute("insert into sigl_file_data "
                     "(id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, status, date_creation, "
                     "original_name, generated_name, size, hash, ext, content_type, id_storage, path) "
                     "values (100, now(), now(), 100, 1, now(), 'LBM4_Laboratory_design_and_maintenance.pdf', "
                     "'637172a076c1d0803f50a6675a60a624', 725013, '2fcf2f896eb6c2606da1e8fac91194b9', "
                     "'pdf', 'application/pdf', 1, '63/71/')")
    except:
        print("ERROR insert into sigl_file_data LBM4_Laboratory_design_and_maintenance.pdf")

    try:
        conn.execute("insert into sigl_manuels_document__file_data "
                     "(id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, id_ext, id_file) "
                     "values (100, now(), now(), 100, (select id_data from sigl_manuels_data order by id_data desc limit 1), "
                     "(select id_data from sigl_file_data order by id_data desc limit 1))")
    except:
        print("ERROR insert into sigl_manuels_document__file_data")

    # Laboratory biosafety manual 4th ed. Biological safety cabinets
    try:
        conn.execute("insert into sigl_manuels_data "
                     "(id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, titre , reference, "
                     "redacteur_id, verificateur_id, approbateur_id, date_insert, date_apply, date_update, section) "
                     "values (100, now(), now(), 100, 'Laboratory biosafety manual 4th ed. Biological safety cabinets', '', 0, 0, 0, now(), now(), now(), 0)")
    except:
        print("ERROR insert into sigl_manuels_data Laboratory biosafety manual 4th ed. Biological safety cabinets")

    try:
        conn.execute("insert into sigl_file_data "
                     "(id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, status, date_creation, "
                     "original_name, generated_name, size, hash, ext, content_type, id_storage, path) "
                     "values (100, now(), now(), 100, 1, now(), 'LBM4_Biological_safety_cabinets.pdf', "
                     "'88e1f09a873093346b110f653ad048c5', 970693, '157a5d381ece843ba01bdfd41a90dcb2', "
                     "'pdf', 'application/pdf', 1, '88/e1/')")
    except:
        print("ERROR insert into sigl_file_data LBM4_Biological_safety_cabinets.pdf")

    try:
        conn.execute("insert into sigl_manuels_document__file_data "
                     "(id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, id_ext, id_file) "
                     "values (100, now(), now(), 100, (select id_data from sigl_manuels_data order by id_data desc limit 1), "
                     "(select id_data from sigl_file_data order by id_data desc limit 1))")
    except:
        print("ERROR insert into sigl_manuels_document__file_data")

    # Laboratory biosafety manual 4th ed. Personal protective equipment
    try:
        conn.execute("insert into sigl_manuels_data "
                     "(id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, titre , reference, "
                     "redacteur_id, verificateur_id, approbateur_id, date_insert, date_apply, date_update, section) "
                     "values (100, now(), now(), 100, 'Laboratory biosafety manual 4th ed. Personal protective equipment', '', 0, 0, 0, now(), now(), now(), 0)")
    except:
        print("ERROR insert into sigl_manuels_data Laboratory biosafety manual 4th ed. Personal protective equipment")

    try:
        conn.execute("insert into sigl_file_data "
                     "(id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, status, date_creation, "
                     "original_name, generated_name, size, hash, ext, content_type, id_storage, path) "
                     "values (100, now(), now(), 100, 1, now(), 'LBM4_Personal_protective_equipment.pdf', "
                     "'c723bddda72c8633e79da3aa01ebacc3', 3476881, '206fce518ae53429f33623250b782348', "
                     "'pdf', 'application/pdf', 1, 'c7/23/')")
    except:
        print("ERROR insert into sigl_file_data LBM4_Personal_protective_equipment.pdf")

    try:
        conn.execute("insert into sigl_manuels_document__file_data "
                     "(id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, id_ext, id_file) "
                     "values (100, now(), now(), 100, (select id_data from sigl_manuels_data order by id_data desc limit 1), "
                     "(select id_data from sigl_file_data order by id_data desc limit 1))")
    except:
        print("ERROR insert into sigl_manuels_document__file_data")

    # Laboratory biosafety manual 4th ed. Decontamination and waste management
    try:
        conn.execute("insert into sigl_manuels_data "
                     "(id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, titre , reference, "
                     "redacteur_id, verificateur_id, approbateur_id, date_insert, date_apply, date_update, section) "
                     "values (100, now(), now(), 100, 'Laboratory biosafety manual 4th ed. Decontamination and waste management', '', 0, 0, 0, now(), now(), now(), 0)")
    except:
        print("ERROR insert into sigl_manuels_data Laboratory biosafety manual 4th ed. Decontamination and waste management")

    try:
        conn.execute("insert into sigl_file_data "
                     "(id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, status, date_creation, "
                     "original_name, generated_name, size, hash, ext, content_type, id_storage, path) "
                     "values (100, now(), now(), 100, 1, now(), 'LBM4_Decontamination_and_waste_management.pdf', "
                     "'f82c0fb67ea9b2e9c309cfe5fe2de5c4', 715596, '0f8bb8d9f9cc22336c951252ef8762cb', "
                     "'pdf', 'application/pdf', 1, 'f8/2c/')")
    except:
        print("ERROR insert into sigl_file_data LBM4_Decontamination_and_waste_management.pdf")

    try:
        conn.execute("insert into sigl_manuels_document__file_data "
                     "(id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, id_ext, id_file) "
                     "values (100, now(), now(), 100, (select id_data from sigl_manuels_data order by id_data desc limit 1), "
                     "(select id_data from sigl_file_data order by id_data desc limit 1))")
    except:
        print("ERROR insert into sigl_manuels_document__file_data")

    # Laboratory biosafety manual 4th ed. Biosafety programme management
    try:
        conn.execute("insert into sigl_manuels_data "
                     "(id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, titre , reference, "
                     "redacteur_id, verificateur_id, approbateur_id, date_insert, date_apply, date_update, section) "
                     "values (100, now(), now(), 100, 'Laboratory biosafety manual 4th ed. Biosafety programme management', '', 0, 0, 0, now(), now(), now(), 0)")
    except:
        print("ERROR insert into sigl_manuels_data Laboratory biosafety manual 4th ed. Biosafety programme management")

    try:
        conn.execute("insert into sigl_file_data "
                     "(id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, status, date_creation, "
                     "original_name, generated_name, size, hash, ext, content_type, id_storage, path) "
                     "values (100, now(), now(), 100, 1, now(), 'LBM4_Biosafety_programme_management.pdf', "
                     "'c36e578c2125b7aa8c5da4d1bfd38944', 837739, '7dad41cae2ac4467f76d6a0764cb3af1', "
                     "'pdf', 'application/pdf', 1, 'c3/6e/')")
    except:
        print("ERROR insert into sigl_file_data LBM4_Biosafety_programme_management.pdf")

    try:
        conn.execute("insert into sigl_manuels_document__file_data "
                     "(id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, id_ext, id_file) "
                     "values (100, now(), now(), 100, (select id_data from sigl_manuels_data order by id_data desc limit 1), "
                     "(select id_data from sigl_file_data order by id_data desc limit 1))")
    except:
        print("ERROR insert into sigl_manuels_document__file_data")

    # Laboratory biosafety manual 4th ed. Outbreak preparedness and resilience
    try:
        conn.execute("insert into sigl_manuels_data "
                     "(id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, titre , reference, "
                     "redacteur_id, verificateur_id, approbateur_id, date_insert, date_apply, date_update, section) "
                     "values (100, now(), now(), 100, 'Laboratory biosafety manual 4th ed. Outbreak preparedness and resilience', '', 0, 0, 0, now(), now(), now(), 0)")
    except:
        print("ERROR insert into sigl_manuels_data Laboratory biosafety manual 4th ed. Outbreak preparedness and resilience")

    try:
        conn.execute("insert into sigl_file_data "
                     "(id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, status, date_creation, "
                     "original_name, generated_name, size, hash, ext, content_type, id_storage, path) "
                     "values (100, now(), now(), 100, 1, now(), 'LBM4_Outbreak_preparedness_and_resilience.pdf', "
                     "'53b11253ac64bdde755a94c9f2564b24', 1156566, 'fbf3875adea9bcd9c4ef297e65b4b216', "
                     "'pdf', 'application/pdf', 1, '53/b1/')")
    except:
        print("ERROR insert into sigl_file_data LBM4_Outbreak_preparedness_and_resilience.pdf")

    try:
        conn.execute("insert into sigl_manuels_document__file_data "
                     "(id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, id_ext, id_file) "
                     "values (100, now(), now(), 100, (select id_data from sigl_manuels_data order by id_data desc limit 1), "
                     "(select id_data from sigl_file_data order by id_data desc limit 1))")
    except:
        print("ERROR insert into sigl_manuels_document__file_data")

    # CASFM Recommandations 2020 Oct v1.2
    try:
        conn.execute("insert into sigl_manuels_data "
                     "(id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, titre , reference, "
                     "redacteur_id, verificateur_id, approbateur_id, date_insert, date_apply, date_update, section) "
                     "values (100, now(), now(), 100, 'CASFM Recommandations 2020 Oct v1.2', '', 0, 0, 0, now(), now(), now(), 0)")
    except:
        print("ERROR insert into sigl_manuels_data ")

    try:
        conn.execute("insert into sigl_file_data "
                     "(id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, status, date_creation, "
                     "original_name, generated_name, size, hash, ext, content_type, id_storage, path) "
                     "values (100, now(), now(), 100, 1, now(), 'CASFM_Recommandations_2020_Oct_v1.2.pdf', "
                     "'65d69cdaf3ca25e83840c93bf571e6ea', 2478569, '44d69b97c9655a79de184ef0805d6ec3', "
                     "'pdf', 'application/pdf', 1, '65/d6/')")
    except:
        print("ERROR insert into sigl_file_data CASFM_Recommandations_2020_Oct_v1.2.pdf")

    try:
        conn.execute("insert into sigl_manuels_document__file_data "
                     "(id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, id_ext, id_file) "
                     "values (100, now(), now(), 100, (select id_data from sigl_manuels_data order by id_data desc limit 1), "
                     "(select id_data from sigl_file_data order by id_data desc limit 1))")
    except:
        print("ERROR insert into sigl_manuels_document__file_data")

    # EUCAST Breakpoint tables for interpretation of MICs and zone diameters v11.0 2021
    try:
        conn.execute("insert into sigl_manuels_data "
                     "(id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, titre , reference, "
                     "redacteur_id, verificateur_id, approbateur_id, date_insert, date_apply, date_update, section) "
                     "values (100, now(), now(), 100, 'EUCAST Breakpoint tables for interpretation of MICs and zone diameters v11.0 2021', '', "
                     "0, 0, 0, now(), now(), now(), 0)")
    except:
        print("ERROR insert into sigl_manuels_data ")

    try:
        conn.execute("insert into sigl_file_data "
                     "(id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, status, date_creation, "
                     "original_name, generated_name, size, hash, ext, content_type, id_storage, path) "
                     "values (100, now(), now(), 100, 1, now(), 'EUCAST_Breakpoint_tables_v11.0_2021.pdf', "
                     "'8c42586eb5e771edd6f94ce1be236c05', 3803959, '5abc924f62ab32fb746c8d09e43257f0', "
                     "'pdf', 'application/pdf', 1, '8c/42/')")
    except:
        print("ERROR insert into sigl_file_data EUCAST_Breakpoint_tables_v11.0_2021.pdf")

    try:
        conn.execute("insert into sigl_manuels_document__file_data "
                     "(id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, id_ext, id_file) "
                     "values (100, now(), now(), 100, (select id_data from sigl_manuels_data order by id_data desc limit 1), "
                     "(select id_data from sigl_file_data order by id_data desc limit 1))")
    except:
        print("ERROR insert into sigl_manuels_document__file_data")

    # EUCAST Dosages v11.0 2021
    try:
        conn.execute("insert into sigl_manuels_data "
                     "(id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, titre , reference, "
                     "redacteur_id, verificateur_id, approbateur_id, date_insert, date_apply, date_update, section) "
                     "values (100, now(), now(), 100, 'EUCAST Dosages v11.0 2021', '', 0, 0, 0, now(), now(), now(), 0)")
    except:
        print("ERROR insert into sigl_manuels_data ")

    try:
        conn.execute("insert into sigl_file_data "
                     "(id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, status, date_creation, "
                     "original_name, generated_name, size, hash, ext, content_type, id_storage, path) "
                     "values (100, now(), now(), 100, 1, now(), 'EUCAST_Dosages_v11.0_2021.pdf', "
                     "'a3f92e0209158407a5d059e7325657a8', 217508, 'f6cce322e79234fa6cade7a5699a56f8', "
                     "'pdf', 'application/pdf', 1, 'a3/f9/')")
    except:
        print("ERROR insert into sigl_file_data EUCAST_Dosages_v11.0_2021.pdf")

    try:
        conn.execute("insert into sigl_manuels_document__file_data "
                     "(id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, id_ext, id_file) "
                     "values (100, now(), now(), 100, (select id_data from sigl_manuels_data order by id_data desc limit 1), "
                     "(select id_data from sigl_file_data order by id_data desc limit 1))")
    except:
        print("ERROR insert into sigl_manuels_document__file_data")

    print("END of migration v3_0_2_stock_and_add_new_manual revision=5b3058a99439")


def downgrade():
    pass
