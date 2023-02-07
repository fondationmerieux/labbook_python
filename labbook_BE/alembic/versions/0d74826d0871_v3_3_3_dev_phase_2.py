"""v3_3_3_dev_phase_2

Revision ID: 0d74826d0871
Revises: 19565ea2ef9e
Create Date: 2023-01-17 09:54:25.029933

"""
from alembic import op
from sqlalchemy import text

from datetime import datetime

# revision identifiers, used by Alembic.
revision = '0d74826d0871'
down_revision = '19565ea2ef9e'
branch_labels = None
depends_on = None


def upgrade():
    print("--- " + str(datetime.today()) + "---")
    print("START of migration v3_3_3_dev_phase_2 revision=0d74826d0871")

    # Get the current
    conn = op.get_bind()

    # COPY alembic resource
    try:
        from distutils.dir_util import copy_tree

        fromDirectory = "alembic/resource"
        toDirectory = "/storage/resource"

        copy_tree(fromDirectory, toDirectory)
    except Exception as err:
        print("ERROR copy alembic resource,\n\terr=" + str(err))

    # ADD template outsourced
    try:
        conn.execute(text("insert into template_setting "
                          "(tpl_date, tpl_name, tpl_file, tpl_default, tpl_type) "
                          "values (NOW(), 'Modèle bon de transfert', 'tpl_outsourced.odt', 'Y', 'OUT')"))
    except Exception as err:
        print("ERROR insert outsourced template for template_setting,\n\terr=" + str(err))

    # UPDATE defautl position from sigl_dico_data
    try:
        conn.execute(text("update sigl_dico_data set position=0 where position is NULL"))
    except Exception as err:
        print("ERROR update sigl_dico_data set position=0 where position is NULL,\n\terr=" + str(err))

    # DROP COLUMN TO catalog reference of a product
    try:
        conn.execute(text("alter table product_details drop column prd_ref_catalog"))
    except Exception as err:
        print("ERROR drop column prd_ref_catalog to product_details,\n\terr=" + str(err))

    # ADD COLUMN for outsourced of an analysis
    try:
        conn.execute(text("alter table sigl_04_data add column req_outsourced varchar(1) not null default 'N'"))
    except Exception as err:
        print("ERROR add column req_outsourced to sigl_04_data,\n\terr=" + str(err))

    # ADD COLUMN for formatting of a dict value
    try:
        conn.execute(text("alter table sigl_dico_data add column dict_formatting varchar(1) not null default 'N'"))
    except Exception as err:
        print("ERROR add column dict_formatting to sigl_dico_data,\n\terr=" + str(err))

    # DROP COLUMN TO stock_setting TABLE
    try:
        conn.execute(text("alter table stock_setting drop column sos_expir_oblig"))
    except Exception as err:
        print("ERROR drop column sos_expir_oblig to stock_setting,\n\terr=" + str(err))

    # ADD COLUMN for expir oblig of a product
    try:
        conn.execute(text("alter table product_details add column prd_expir_oblig varchar(1) not null default 'Y'"))
    except Exception as err:
        print("ERROR add column prd_expir_oblig to product_details,\n\terr=" + str(err))

    # Create table for enable/disable fields of forms
    try:
        conn.execute(text("create table form_setting("
                          "fos_ser int not NULL AUTO_INCREMENT,"
                          "fos_date DATETIME,"
                          "fos_rank INT default 0,"
                          "fos_name varchar(255) NOT NULL,"  # name of fields
                          "fos_type varchar(5) NOT NULL,"  # 'PAT'ient form, 'PROD'uct form, 'SUPP'LY form
                          "fos_ref varchar(50) NOT NULL,"  # name of html ref
                          "fos_stat varchar(1) NOT NULL default 'Y',"
                          "PRIMARY KEY (fos_ser),"
                          "INDEX (fos_type), INDEX (fos_ref), INDEX (fos_stat), INDEX (fos_rank)) "
                          "character set=utf8"))
    except Exception as err:
        print("ERROR create table form_setting,\n\terr=" + str(err))

    # ADD fields in form setting
    try:
        conn.execute(text('insert into form_setting '
                          '(fos_date, fos_rank, fos_name, fos_type, fos_ref, fos_stat) '
                          'values '
                          '(NOW(), 5, "Nationalité", "PAT", "pat_nationality", "Y"), '
                          '(NOW(), 10, "Résident", "PAT", "pat_resident", "Y"), '
                          '(NOW(), 15, "Groupe sanguin", "PAT", "pat_blood_group", "Y"), '
                          '(NOW(), 20, "Rhésus", "PAT", "pat_blood_rhesus", "Y"), '
                          '(NOW(), 25, "Profession", "PAT", "pat_profession", "Y"), '
                          '(NOW(), 30, "Boite postale", "PAT", "pat_pbox", "Y"), '
                          '(NOW(), 35, "Quartier / Secteur", "PAT", "pat_district", "Y"), '
                          '(NOW(), 50, "Réference fournisseur", "PROD", "prod_ref_supplier", "Y"), '
                          '(NOW(), 60, "Localisation", "SUPP", "supp_rack", "Y"), '
                          '(NOW(), 65, "Numéro de lot", "SUPP", "supp_batch_num", "Y"), '
                          '(NOW(), 70, "Prix d\'achat", "SUPP", "supp_buy_price", "Y"), '
                          '(NOW(), 75, "Nom bailleur", "SUPP", "supp_lessor", "Y")'))
    except Exception as err:
        print('ERROR insert default form_setting,\n\terr=' + str(err))

    print(str(datetime.today()) + " : END of migration v3_3_3_dev_phase_2 revision=0d74826d0871")


def downgrade():
    pass
