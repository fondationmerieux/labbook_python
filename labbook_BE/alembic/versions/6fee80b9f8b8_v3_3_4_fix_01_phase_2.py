# -*- coding:utf-8 -*-
"""v3_3_4_fix_01_phase_2

Revision ID: 6fee80b9f8b8
Revises: 0d74826d0871
Create Date: 2023-02-19 18:09:35.519778

"""
from alembic import op
from sqlalchemy import text

from datetime import datetime

# revision identifiers, used by Alembic.
revision = '6fee80b9f8b8'
down_revision = '0d74826d0871'
branch_labels = None
depends_on = None


def upgrade():
    print("--- " + str(datetime.today()) + "---")
    print("START of migration v3_3_4_fix_01_phase_2 revision=6fee80b9f8b8")

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

    # ADD fields in form setting
    try:
        conn.execute(text('insert into form_setting '
                          '(fos_date, fos_rank, fos_name, fos_type, fos_ref, fos_stat) '
                          'values '
                          '(NOW(), 3, "Deuxième nom", "PAT", "pat_midname", "Y"), '
                          '(NOW(), 4, "Nom de jeune fille", "PAT", "nom_jf", "Y")'))
    except Exception as err:
        print('ERROR insert default form_setting,\n\terr=' + str(err))

    # UPDATE type_resultat in sigl_07_data to remove duplicates of type_resultat
    # 1138 => 635
    try:
        conn.execute(text("update sigl_07_data set type_resultat=635 where type_resultat=1138"))

        conn.execute(text("delete from sigl_dico_data where id_data=1138"))
    except Exception as err:
        print("ERROR update type_resultat 1138 to 635 in sigl_07_data then delete in sigl_dico_data,\n\terr=" + str(err))

    print(str(datetime.today()) + " : END of migration v3_3_4_fix_01_phase_2 revision=6fee80b9f8b8")


def downgrade():
    pass
