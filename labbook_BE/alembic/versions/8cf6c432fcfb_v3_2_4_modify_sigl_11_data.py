# -*- coding:utf-8 -*-
"""v3_2_4_modify_sigl_11_data

Revision ID: 8cf6c432fcfb
Revises: ca44f5d0984c
Create Date: 2022-03-23 15:50:57.756373

"""
from alembic import op
from sqlalchemy import text

from datetime import datetime

# revision identifiers, used by Alembic.
revision = '8cf6c432fcfb'
down_revision = 'ca44f5d0984c'
branch_labels = None
depends_on = None


def upgrade():
    print("--- " + str(datetime.today()) + "---")
    print("START of migration v3_2_4_modify_sigl_11_data revision=8cf6c432fcfb")

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

    # ADD COLUMN for id_template with report
    try:
        conn.execute(text("alter table sigl_11_data add column id_tpl int default 0"))
    except Exception as err:
        print("ERROR add column id_tpl to sigl_11_data,\n\terr=" + str(err))

    # ADD COLUMN for nb_donwload with report
    try:
        conn.execute(text("alter table sigl_11_data add column nb_download int default 0"))
    except Exception as err:
        print("ERROR add column nb_donwload to sigl_11_data,\n\terr=" + str(err))

    # ADD INDEX
    try:
        conn.execute(text("create index idx_id_tpl on sigl_11_data (id_tpl)"))
        conn.execute(text("create index idx_tpl_file on template_setting (tpl_file)"))
    except Exception as err:
        print("ERROR create index,\n\terr=" + str(err))

    # DROP OLD TABLE
    try:
        conn.execute(text("drop table sigl_05_05_deleted, sigl_05_07_deleted, sigl_06_deleted, sigl_10_delete, "
                          "sigl_13_deleted, sigl_14_deleted, sigl_15_deleted, sigl_16_deleted, "
                          "sigl_equipement_certif_etalonnage__file_deleted, sigl_equipement_contrat_maintenance__file_deleted, "
                          "sigl_equipement_facture__file_deleted, sigl_equipement_maintenance_preventive__file_deleted, "
                          "sigl_equipement_pannes__file_deleted, sigl_equipement_photo__file_deleted, sigl_file_deleted, "
                          "sigl_laboratoire_deleted, sigl_laboratoire_organigramme__file_deleted, sigl_manuels_deleted, "
                          "sigl_manuels_document__file_deleted, sigl_non_conformite_deleted, sigl_planning_ctrl_ext_data, "
                          "sigl_planning_ctrl_ext_deleted, sigl_planning_ctrl_int_data, sigl_planning_ctrl_int_deleted, "
                          "sigl_procedures_deleted, sigl_procedures_document__file_deleted, sigl_reunion_deleted, "
                          "sigl_reunion_pj__file_deleted, sigl_user_deleted"))
    except Exception as err:
        print("ERROR drop table unused\n\terr=" + str(err))

    print(str(datetime.today()) + " : END of migration v3_2_4_modify_sigl_11_data revision=8cf6c432fcfb")


def downgrade():
    pass
