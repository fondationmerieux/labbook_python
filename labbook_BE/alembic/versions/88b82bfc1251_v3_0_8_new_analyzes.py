# -*- coding:utf-8 -*-
"""v3_0_8_new_analyzes

Revision ID: 88b82bfc1251
Revises: 2660636fdaf9
Create Date: 2021-06-08 12:28:51.255080

"""
from alembic import op
from sqlalchemy import text

from datetime import datetime

# revision identifiers, used by Alembic.
revision = '88b82bfc1251'
down_revision = '2660636fdaf9'
branch_labels = None
depends_on = None


def upgrade():
    print("--- " + str(datetime.today()) + "---")
    print("START of migration v3.0.8_new_analyzes revision=88b82bfc1251")

    # Get the current
    conn = op.get_bind()

    # ADD variable for B796 Anthrax
    try:
        conn.execute(text('insert into sigl_07_data (id_owner, libelle, type_resultat, commentaire) '
                          'values (1000, "Recherche du bacille de l\'anthrax par PCR", (select id_data from sigl_dico_data '
                          'where code="D_POS_NEG" limit 1), "Recherche de l\'ADN du bacillus anthracis par PCR")'))

        conn.execute(text('update sigl_07_data set code_var=id_data where libelle="Recherche du bacille de l\'anthrax par PCR" limit 1'))
    except Exception as err:
        print("ERROR insert new variable Recherche du bacille de l\'anthrax par PCR,\n\terr=" + str(err))
    else:
        # Insert analysis B796
        try:
            conn.execute(text('insert into sigl_05_data (id_owner, code, nom, abbr, famille, '
                              'cote_unite, commentaire, actif, ana_whonet, produit_biologique, type_prel, type_analyse) '
                              'values (1000, "B796", "Diagnostic moléculaire du bacille de l\'anthrax par PCR", "Anthrax", 19, '
                              '"", "", 4, 5, 23, 163, 170)'))
        except Exception as err:
            print("ERROR insert B796 analysis,\n\terr=" + str(err))
        else:
            try:
                # Insert links for B796
                conn.execute(text('insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, '
                                  'obligatoire, var_whonet) '
                                  'select 1000, id_data, (select id_data from sigl_07_data where '
                                  'libelle="Recherche du bacille de l\'anthrax par PCR" limit 1), 1, 4, 5 '
                                  'from sigl_05_data where code="B796"'))
            except Exception as err:
                print("ERROR insert link for B796 analysis,\n\terr=" + str(err))

    # ADD variable for B797 Dengue PCR
    try:
        conn.execute(text('insert into sigl_07_data (id_owner, libelle, type_resultat, commentaire) '
                          'values (1000, "Détection de l\'ARN du virus de la Dengue par RT-PCR", '
                          '(select id_data from sigl_dico_data where code="D_POS_NEG" limit 1), "")'))

        conn.execute(text('update sigl_07_data set code_var=id_data where libelle="Détection de l\'ARN du virus de la Dengue '
                          'par RT-PCR" limit 1'))
    except Exception as err:
        print("ERROR insert new variable Dengue for B797,\n\terr=" + str(err))
    else:
        # Insert analysis B797
        try:
            conn.execute(text('insert into sigl_05_data (id_owner, code, nom, abbr, famille, '
                              'cote_unite, commentaire, actif, ana_whonet, produit_biologique, type_prel, type_analyse) '
                              'values (1000, "B797", "Détection de l\'ARN du virus de la Dengue par RT-PCR sur prélèvement '
                              'sanguin", "Dengue RT-PCR", 23, "", "", 4, 5, 1, 138, 170)'))
        except Exception as err:
            print("ERROR insert B797 analysis,\n\terr=" + str(err))
        else:
            try:
                # Insert links for B797
                conn.execute(text('insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, '
                                  'obligatoire, var_whonet) '
                                  'select 1000, id_data, (select id_data from sigl_07_data where '
                                  'libelle="Détection de l\'ARN du virus de la Dengue par RT-PCR" limit 1), 1, 4, 5 '
                                  'from sigl_05_data where code="B797"'))
            except Exception as err:
                print("ERROR insert link for B797 analysis,\n\terr=" + str(err))

    # ADD variable for B798 Dengue EIA ou ICT
    try:
        conn.execute(text('insert into sigl_07_data (id_owner, libelle, type_resultat, commentaire) '
                          'values (1000, "Détection de l\'antigène NS1 de la Dengue", '
                          '(select id_data from sigl_dico_data where code="D_POS_NEG" limit 1), "")'))

        conn.execute(text('update sigl_07_data set code_var=id_data where libelle="Détection de l\'antigène NS1 de la Dengue" limit 1'))
    except Exception as err:
        print("ERROR insert new variable Dengue for B798,\n\terr=" + str(err))
    else:
        # Insert analysis B798
        try:
            conn.execute(text('insert into sigl_05_data (id_owner, code, nom, abbr, famille, '
                              'cote_unite, commentaire, actif, ana_whonet, produit_biologique, type_prel, type_analyse) '
                              'values (1000, "B798", "Détection de l\'antigène NS1 de la Dengue par EIA ou ICT", "Ag Dengue", 302, "", "", 4, 5, 1, 138, 170)'))
        except Exception as err:
            print("ERROR insert B798 analysis,\n\terr=" + str(err))
        else:
            try:
                # Insert links for B798
                conn.execute(text('insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, '
                                  'obligatoire, var_whonet) '
                                  'select 1000, id_data, (select id_data from sigl_07_data where '
                                  'libelle="Détection de l\'antigène NS1 de la Dengue" limit 1), 1, 4, 5 '
                                  'from sigl_05_data where code="B798"'))
            except Exception as err:
                print("ERROR insert link for B798 analysis,\n\terr=" + str(err))

    # ADD variable for B799 Dengue IgG IgM par EIA
    try:
        conn.execute(text('insert into sigl_07_data (id_owner, libelle, type_resultat, commentaire) '
                          'values (1000, "Recherche des Ac contre la Dengue", '
                          '(select id_data from sigl_dico_data where code="D_POS_NEG" limit 1), "")'))

        conn.execute(text('update sigl_07_data set code_var=id_data where libelle="Recherche des Ac contre la Dengue" limit 1'))
    except Exception as err:
        print("ERROR insert new variable Dengue for B799,\n\terr=" + str(err))
    else:
        # Insert analysis B799
        try:
            conn.execute(text('insert into sigl_05_data (id_owner, code, nom, abbr, famille, '
                              'cote_unite, commentaire, actif, ana_whonet, produit_biologique, type_prel, type_analyse) '
                              'values (1000, "B799", "Recherche des IgG et des IgM contre la Dengue par EIA", "Ac anti Dengue", 302, "", "", 4, 5, 1, 138, 170)'))
        except Exception as err:
            print("ERROR insert B799 analysis,\n\terr=" + str(err))
        else:
            try:
                # Insert links for B799
                conn.execute(text('insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, '
                                  'obligatoire, var_whonet) '
                                  'select 1000, id_data, (select id_data from sigl_07_data where '
                                  'libelle="Recherche des Ac contre la Dengue" limit 1), 1, 4, 5 '
                                  'from sigl_05_data where code="B799"'))
            except Exception as err:
                print("ERROR insert link for B799 analysis,\n\terr=" + str(err))

    # ADD variable for B800 Rage
    try:
        conn.execute(text('insert into sigl_07_data (id_owner, libelle, type_resultat, commentaire) '
                          'values (1000, "Recherche des Ac IgG et IgM anti rage", '
                          '(select id_data from sigl_dico_data where code="D_POS_NEG" limit 1), "")'))

        conn.execute(text('update sigl_07_data set code_var=id_data where libelle="Recherche des Ac IgG et IgM anti rage" limit 1'))
    except Exception as err:
        print("ERROR insert new variable Rage for B800,\n\terr=" + str(err))
    else:
        # Insert analysis B800
        try:
            conn.execute(text('insert into sigl_05_data (id_owner, code, nom, abbr, famille, '
                              'cote_unite, commentaire, actif, ana_whonet, produit_biologique, type_prel, type_analyse) '
                              'values (1000, "B800", "Diagnostic d\'une infection récente de la rage", "Ac anti rabbique", 302, "", "", 4, 5, 1, 138, 170)'))
        except Exception as err:
            print("ERROR insert B800 analysis,\n\terr=" + str(err))
        else:
            try:
                # Insert links for B800
                conn.execute(text('insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, '
                                  'obligatoire, var_whonet) '
                                  'select 1000, id_data, (select id_data from sigl_07_data where '
                                  'libelle="Recherche des Ac IgG et IgM anti rage" limit 1), 1, 4, 5 '
                                  'from sigl_05_data where code="B800"'))
            except Exception as err:
                print("ERROR insert link for B800 analysis,\n\terr=" + str(err))

    # ADD variable for B801 Rage
    try:
        conn.execute(text('insert into sigl_07_data (id_owner, libelle, type_resultat, commentaire) '
                          'values (1000, "Recherche génome du virus de la rage", '
                          '(select id_data from sigl_dico_data where code="D_POS_NEG" limit 1), "")'))

        conn.execute(text('update sigl_07_data set code_var=id_data where libelle="Recherche génome du virus de la rage" limit 1'))
    except Exception as err:
        print("ERROR insert new variable Rage for B801,\n\terr=" + str(err))
    else:
        # Insert analysis B801
        try:
            conn.execute(text('insert into sigl_05_data (id_owner, code, nom, abbr, famille, '
                              'cote_unite, commentaire, actif, ana_whonet, produit_biologique, type_prel, type_analyse) '
                              'values (1000, "B801", "Recherche directe virus de la rage par IF ou EIA", "Rage direct", 302, "", "", 4, 5, 1, 138, 170)'))
        except Exception as err:
            print("ERROR insert B801 analysis,\n\terr=" + str(err))
        else:
            try:
                # Insert links for B801
                conn.execute(text('insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, '
                                  'obligatoire, var_whonet) '
                                  'select 1000, id_data, (select id_data from sigl_07_data where '
                                  'libelle="Recherche génome du virus de la rage" limit 1), 1, 4, 5 '
                                  'from sigl_05_data where code="B801"'))
            except Exception as err:
                print("ERROR insert link for B801 analysis,\n\terr=" + str(err))

    # ADD variable for B802 Influenza A et B de la grippe
    try:
        conn.execute(text('insert into sigl_07_data (id_owner, libelle, type_resultat, commentaire) '
                          'values (1000, "Détection du génome des virus Influenza A et B de la grippe", '
                          '(select id_data from sigl_dico_data where code="D_POS_NEG" limit 1), "")'))

        conn.execute(text('update sigl_07_data set code_var=id_data where libelle="Détection du génome des virus Influenza A et B de la grippe" limit 1'))
    except Exception as err:
        print("ERROR insert new variable for B802,\n\terr=" + str(err))
    else:
        # Insert analysis B802
        try:
            conn.execute(text('insert into sigl_05_data (id_owner, code, nom, abbr, famille, '
                              'cote_unite, commentaire, actif, ana_whonet, produit_biologique, type_prel, type_analyse) '
                              'values (1000, "B802", "Recherche directe virus de la rage par IF ou EIA", "Influenza RT-PCR", 302, "", "", 4, 5, 13, 163, 170)'))
        except Exception as err:
            print("ERROR insert B802 analysis,\n\terr=" + str(err))
        else:
            try:
                # Insert links for B802
                conn.execute(text('insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, '
                                  'obligatoire, var_whonet) '
                                  'select 1000, id_data, (select id_data from sigl_07_data where '
                                  'libelle="Détection du génome des virus Influenza A et B de la grippe" limit 1), 1, 4, 5 '
                                  'from sigl_05_data where code="B802"'))
            except Exception as err:
                print("ERROR insert link for B802 analysis,\n\terr=" + str(err))

    # ADD variable for E06 Ebola
    try:
        conn.execute(text('insert into sigl_07_data (id_owner, libelle, type_resultat, commentaire) '
                          'values (1000, "Détection virus Ebola par test rapide Oraquick", '
                          '(select id_data from sigl_dico_data where code="D_POS_NEG" limit 1), "")'))

        conn.execute(text('update sigl_07_data set code_var=id_data where libelle="Détection virus Ebola par test rapide Oraquick" limit 1'))
    except Exception as err:
        print("ERROR insert new variable for E06,\n\terr=" + str(err))
    else:
        # Insert analysis E06
        try:
            conn.execute(text('insert into sigl_05_data (id_owner, code, nom, abbr, famille, '
                              'cote_unite, commentaire, actif, ana_whonet, produit_biologique, type_prel, type_analyse) '
                              'values (1000, "E06", "Test de diagnostic rapide de la maladie à virus Ebola par Oraquick", "TDR MVE test rapide", 17, "", "", 4, 5, 15, 50, 170)'))
        except Exception as err:
            print("ERROR insert E06 analysis,\n\terr=" + str(err))
        else:
            try:
                # Insert links for E06
                conn.execute(text('insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, '
                                  'obligatoire, var_whonet) '
                                  'select 1000, id_data, (select id_data from sigl_07_data where '
                                  'libelle="Détection virus Ebola par test rapide Oraquick" limit 1), 1, 4, 5 '
                                  'from sigl_05_data where code="E06"'))
            except Exception as err:
                print("ERROR insert link for E06 analysis,\n\terr=" + str(err))

    print(str(datetime.today()) + " : END of migration v3.0.8_new_analyzes revision=88b82bfc1251")


def downgrade():
    pass
