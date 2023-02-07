# -*- coding:utf-8 -*-
"""v3_0_5_add_Ebola_analyzes

Revision ID: 3c7d8a35d79a
Revises: 3fec2eab4253
Create Date: 2021-05-04 17:36:43.920214

"""
from alembic import op
from sqlalchemy import text

from datetime import datetime

# revision identifiers, used by Alembic.
revision = '3c7d8a35d79a'
down_revision = '3fec2eab4253'
branch_labels = None
depends_on = None


def upgrade():
    print("--- " + str(datetime.today()) + "---")
    print("START of migration v3_0_5_add_Ebola_analyzes revision=3c7d8a35d79a")

    # Get the current
    conn = op.get_bind()

    # ADD UNIT TYPE IN DICT TABLE
    try:
        conn.execute(text("insert into sigl_dico_data "
                     "(id_owner, dico_name, label, short_label, position, code) "
                     "values (100, 'unite_valeur', 'cp/ml', 'cp/ml', 420, 'cpml')"))
    except Exception as err:
        print("ERROR insert into sigl_dico_data a unite_valeur (cp/ml),\n\terr=" + str(err))

    # ADD EBOLA ANALYZES
    try:
        # --- VARIABLES FOR EBOLA ANALYZES ---
        conn.execute(text('insert into sigl_07_data (id_owner, libelle, type_resultat) '
                     'values (1000, "RT-PCR", 230)'))
        conn.execute(text('insert into sigl_07_data (id_owner, libelle, type_resultat, normal_min, normal_max, accuracy, unite) '
                     'values (1000, "Titrage", 228, "0", "1000000", 1, (select id_data from sigl_dico_data '
                     'where dico_name="unite_valeur" and label="cp/ml" limit 1))'))

    except Exception as err:
        print("ERROR insert new variables for EBOLA analyzes,\n\terr=" + str(err))
    else:
        # MVE RT-PCR Sang
        try:
            conn.execute(text('insert into sigl_05_data (id_owner, code, nom, abbr, famille, cote_unite, cote_valeur, '
                         'produit_biologique, type_prel, type_analyse, commentaire, actif) '
                         'values (1000, "E01", "Recherche dans le sang de l\'ADN viral de la maladie à virus Ebola par RT-PCR", '
                         '"MVE RT-PCR Sang", 17, "", 0, 1, 138, 170, "", 4)'))
        except Exception as err:
            print("ERROR insert E01 analysis,\n\terr=" + str(err))
        else:
            try:
                # Insert links for E01
                conn.execute(text('insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) '
                             'select 1000, id_data, (select id_data from sigl_07_data '
                             'where libelle="RT-PCR" order by id_data desc limit 1), 1, 4 '
                             'from sigl_05_data where code="E01"'))

                conn.execute(text('insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) '
                             'select 1000, id_data, (select id_data from sigl_07_data '
                             'where libelle="Titrage" order by id_data desc limit 1), 2, 5 '
                             'from sigl_05_data where code="E01"'))
            except Exception as err:
                print("ERROR insert links for E01 analysis,\n\terr=" + str(err))

        # MVE RT-PCR Buccal
        try:
            conn.execute(text('insert into sigl_05_data (id_owner, code, nom, abbr, famille, cote_unite, cote_valeur, '
                         'produit_biologique, type_prel, type_analyse, commentaire, actif) '
                         'values (1000, "E02", "Recherche dans la bouche de l\'ADN viral de la maladie à virus Ebola par RT-PCR", '
                         '"MVE RT-PCR Buccal", 17, "", 0, 15, 50, 170, "", 4)'))
        except Exception as err:
            print("ERROR insert E02 analysis,\n\terr=" + str(err))
        else:
            try:
                # Insert links for E02
                conn.execute(text('insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) '
                             'select 1000, id_data, (select id_data from sigl_07_data '
                             'where libelle="RT-PCR" order by id_data desc limit 1), 1, 4 '
                             'from sigl_05_data where code="E02"'))

                conn.execute(text('insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) '
                             'select 1000, id_data, (select id_data from sigl_07_data '
                             'where libelle="Titrage" order by id_data desc limit 1), 2, 5 '
                             'from sigl_05_data where code="E02"'))
            except Exception as err:
                print("ERROR insert links for E02 analysis,\n\terr=" + str(err))

        # MVE RT-PCR Urine
        try:
            conn.execute(text('insert into sigl_05_data (id_owner, code, nom, abbr, famille, cote_unite, cote_valeur, '
                         'produit_biologique, type_prel, type_analyse, commentaire, actif) '
                         'values (1000, "E03", "Recherche dans les urines de l\'ADN viral de la maladie à virus Ebola par RT-PCR", '
                         '"MVE RT-PCR Urine", 17, "", 0, 3, 153, 170, "", 4)'))
        except Exception as err:
            print("ERROR insert E03 analysis,\n\terr=" + str(err))
        else:
            try:
                # Insert links for E03
                conn.execute(text('insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) '
                             'select 1000, id_data, (select id_data from sigl_07_data '
                             'where libelle="RT-PCR" order by id_data desc limit 1), 1, 4 '
                             'from sigl_05_data where code="E03"'))

                conn.execute(text('insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) '
                             'select 1000, id_data, (select id_data from sigl_07_data '
                             'where libelle="Titrage" order by id_data desc limit 1), 2, 5 '
                             'from sigl_05_data where code="E03"'))
            except Exception as err:
                print("ERROR insert links for E03 analysis,\n\terr=" + str(err))

        # MVE RT-PCR Sperme
        try:
            conn.execute(text('insert into sigl_05_data (id_owner, code, nom, abbr, famille, cote_unite, cote_valeur, '
                         'produit_biologique, type_prel, type_analyse, commentaire, actif) '
                         'values (1000, "E04", "Recherche dans le sperme de l\'ADN viral de la maladie à virus Ebola par RT-PCR", '
                         '"MVE RT-PCR Sperme", 17, "", 0, 22, 152, 170, "", 4)'))
        except Exception as err:
            print("ERROR insert E04 analysis,\n\terr=" + str(err))
        else:
            try:
                # Insert links for E04
                conn.execute(text('insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) '
                             'select 1000, id_data, (select id_data from sigl_07_data '
                             'where libelle="RT-PCR" order by id_data desc limit 1), 1, 4 '
                             'from sigl_05_data where code="E04"'))

                conn.execute(text('insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) '
                             'select 1000, id_data, (select id_data from sigl_07_data '
                             'where libelle="Titrage" order by id_data desc limit 1), 2, 5 '
                             'from sigl_05_data where code="E04"'))
            except Exception as err:
                print("ERROR insert links for E04 analysis,\n\terr=" + str(err))

        # MVE RT-PCR Selles
        try:
            conn.execute(text('insert into sigl_05_data (id_owner, code, nom, abbr, famille, cote_unite, cote_valeur, '
                         'produit_biologique, type_prel, type_analyse, commentaire, actif) '
                         'values (1000, "E05", "Recherche dans les selles de l\'ADN viral de la maladie à virus Ebola par RT-PCR", '
                         '"MVE RT-PCR Selles", 17, "", 0, 4, 141, 170, "", 4)'))
        except Exception as err:
            print("ERROR insert E05 analysis,\n\terr=" + str(err))
        else:
            try:
                # Insert links for E05
                conn.execute(text('insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) '
                             'select 1000, id_data, (select id_data from sigl_07_data '
                             'where libelle="RT-PCR" order by id_data desc limit 1), 1, 4 '
                             'from sigl_05_data where code="E05"'))

                conn.execute(text('insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) '
                             'select 1000, id_data, (select id_data from sigl_07_data '
                             'where libelle="Titrage" order by id_data desc limit 1), 2, 5 '
                             'from sigl_05_data where code="E05"'))
            except Exception as err:
                print("ERROR insert links for E05 analysis,\n\terr=" + str(err))

    print(str(datetime.today()) + " : END of migration v3_0_5_add_Ebola_analyzes revision=3c7d8a35d79a")


def downgrade():
    pass
