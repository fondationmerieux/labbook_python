"""v3_0_4_modify_dict_for_stock

Revision ID: 3fec2eab4253
Revises: 1c2971eb5ac6
Create Date: 2021-04-21 10:01:55.510209

"""
from alembic import op
import sqlalchemy as sa

from datetime import datetime

# revision identifiers, used by Alembic.
revision = '3fec2eab4253'
down_revision = '1c2971eb5ac6'
branch_labels = None
depends_on = None


def upgrade():
    print("--- " + str(datetime.today()) + "---")
    print("START of migration v3_0_4_modify_dict_for_stock revision=3fec2eab4253")

    # Get the current
    conn = op.get_bind()

    # DELETE B171 ANALYSIS Diagnostic sérologique des bactéries responsables des méningites (test rapide)
    try:
        conn.execute("delete from sigl_05_data "
                     "where code='B171' and famille=302")
    except:
        print("ERROR delete from sigl_05_data where code='B171' and famille=302")

    # ADD NEW VAR FOR B213 ANALYSIS Diagnostic du VIH (Western Blot) (test de confirmation)
    try:
        # --- VARIABLE ---
        conn.execute("insert into sigl_07_data (id_owner, libelle, description, type_resultat) "
                     "values (1000, 'test de confirmation Western Blot', 'Confirmation VIH', 625)")
    except:
        print("ERROR insert new variable for B213 analysis")
    else:
        try:
            # Insert links for B213
            conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) "
                         "select 1000, id_data, (select id_data from sigl_07_data where libelle='test de confirmation Western Blot' "
                         "and type_resultat=625 limit 1), 1, 4 from sigl_05_data where code='B213'")
        except:
            print("ERROR insert new link variable for B213 analysis")

    # update links for B650 to B658 and B670 to B678
    try:
        conn.execute("update sigl_05_07_data set obligatoire=5 "
                     "where id_refanalyse in (select id_data from sigl_05_data where code in ('B650','B651','B652','B653',"
                     "'B654','B655','B656','B657','B658','B670','B671','B672','B673','B674','B675','B676','B677','B678'))")
    except:
        print("ERROR update obligatoire for antibiogramme analyzes link vars")

    # REMOVE PRODUCT TYPE IN DICT TABLE
    try:
        conn.execute("delete from sigl_dico_data "
                     "where dico_name='product_type' and label='Microbiologie'")
    except:
        print("ERROR delete from sigl_dico_data where dico_name='product_type' and label='Microbiologie'")

    # ADD PRODUCT TYPE IN DICT TABLE
    try:
        conn.execute("insert into sigl_dico_data "
                     "(id_owner, dico_name, label, short_label, position, code) "
                     "values (100, 'product_type', 'Bactériologie', 'bacterio', 80, 'bacterio')")
    except:
        print("ERROR insert into sigl_dico_data a product_type (bacterio)")

    try:
        conn.execute("insert into sigl_dico_data "
                     "(id_owner, dico_name, label, short_label, position, code) "
                     "values (100, 'product_type', 'Parasitologie', 'parasitologie', 90, 'parasito')")
    except:
        print("ERROR insert into sigl_dico_data a product_type (parasitologie)")

    try:
        conn.execute("insert into sigl_dico_data "
                     "(id_owner, dico_name, label, short_label, position, code) "
                     "values (100, 'product_type', 'Virologie', 'virologie', 100, 'virologie')")
    except:
        print("ERROR insert into sigl_dico_data a product_type (virologie)")

    # NEW DIRECTORY IN STORAGE
    try:
        import pathlib

        pathlib.Path("/storage/resource/dhis2").mkdir(mode=0o777, parents=False, exist_ok=True)
    except:
        print("ERROR mkdir -p /storage/resource/dhis2")

    print("END of migration v3_0_4_modify_dict_for_stock revision=3fec2eab4253")


def downgrade():
    pass
