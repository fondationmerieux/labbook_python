# -*- coding:utf-8 -*-
"""v3_0_3_add_covid_analyzes

Revision ID: 1c2971eb5ac6
Revises: 5b3058a99439
Create Date: 2021-04-12 09:45:58.149424

"""
from alembic import op
from sqlalchemy import text

from datetime import datetime

# revision identifiers, used by Alembic.
revision = '1c2971eb5ac6'
down_revision = '5b3058a99439'
branch_labels = None
depends_on = None


def upgrade():
    print("--- " + str(datetime.today()) + "---")
    print("START of migration v3_0_3_add_covid_analizes revision=1c2971eb5ac6")

    # Get the current
    conn = op.get_bind()

    # RENAME COLUMN TO ANALYSIS VARIABLE TABLE BECAUSE RESERVED WORDS
    try:
        conn.execute(text("alter table sigl_07_data change `precision` accuracy int(1) unsigned"))
    except Exception as err:
        print("ERROR alter table sigl_07_data change `precision` accuracy int(1) unsigned,\n\terr=" + str(err))

    # MODIFY COLUMN TO ANALYSIS TABLE
    try:
        conn.execute(text("alter table sigl_05_data modify column code varchar(7)"))
    except Exception as err:
        print("ERROR alter table sigl_05_data modify column code varchar(7),\n\terr=" + str(err))

    # ADD UNIT TYPE IN DICT TABLE
    try:
        conn.execute(text("insert into sigl_dico_data "
                     "(id_owner, dico_name, label, short_label, position, code) "
                     "values (100, 'unite_valeur', 'Ct', 'Ct', 400, 'Ct')"))
    except Exception as err:
        print("ERROR insert into sigl_dico_data a unite_valeur (Ct),\n\terr=" + str(err))

    # ADD COLUMN TO PRODUCT ANALYSIS TABLE
    try:
        conn.execute(text("alter table sigl_05_data add column ana_whonet int(1) default 5"))
    except Exception as err:
        print("ERROR add column ana_whonet to sigl_05_data,\n\terr=" + str(err))
    else:
        # UPDATE NEW COLUMN ana_whonet IN sigl_05_data
        try:
            conn = op.get_bind()

            conn.execute(text('update sigl_05_data set ana_whonet=5'))
        except Exception as err:
            print("ERROR update sigl_05_data set ana_whonet=5,\n\terr=" + str(err))

        # UPDATE WHONET ANALYZES
        try:
            conn = op.get_bind()

            conn.execute(text('update sigl_05_data set ana_whonet=4 '
                         'where code in ("B650","B651","B652","B653","B654","B655","B656","B657","B658", '
                         '"B670","B671","B672","B673","B674","B675","B676","B677","B678")'))
        except Exception as err:
            print("ERROR update sigl_05_data set ana_whonet=4 where code in ('B650',...),\n\terr=" + str(err))

    # ADD COVID 19 ANALYZES
    try:
        # --- VARIABLES FOR COVID 19 ANALYZES ---
        conn.execute(text('insert into sigl_07_data (id_owner, libelle, type_resultat) '
                     'values (1000, "Recherche de l\'ARN du virus SARS-CoV-2 (COVID 19) par RT-PCR", 246)'))
        conn.execute(text('insert into sigl_07_data (id_owner, libelle, type_resultat) '
                     'values (1000, "Recherche de l\'ARN du virus SARS-CoV-2 (COVID 19) par RT-LAMP", 246)'))
        conn.execute(text('insert into sigl_07_data (id_owner, libelle, type_resultat, normal_min, normal_max, accuracy, unite) '
                     'values (1000, "Cycle d\'amplification", 228, "0", "45", 1, (select id_data from sigl_dico_data '
                     'where dico_name="unite_valeur" and label="Ct" limit 1))'))
        conn.execute(text('insert into sigl_07_data (id_owner, libelle, type_resultat) '
                     'values (1000, "Recherche de l\'antigène pour le SARS-CoV-2 (COVID 19)", 246)'))
        conn.execute(text('insert into sigl_07_data (id_owner, libelle, type_resultat) '
                     'values (1000, "Recherche des Ac Anti SARS-CoV-2 (COVID 19)", 246)'))
        conn.execute(text('insert into sigl_07_data (id_owner, libelle, type_resultat, accuracy) '
                     'values (1000, "Titrage des Ac Anti SARS-CoV-2 (COVID 19)", 228, 2)'))

    except Exception as err:
        print("ERROR insert new variables for COVID 19 analyzes,\n\terr=" + str(err))
    else:
        # RT-PCR SARS-CoV-2
        try:
            conn.execute(text('insert into sigl_05_data (id_owner, code, nom, abbr, famille, cote_unite, cote_valeur, '
                         'produit_biologique, type_prel, type_analyse, commentaire, actif) '
                         'values (1000, "B5271a", "Recherche de l\'ARN de virus SARS-CoV-2 (COVID 19) par RT-PCR", '
                         '"RT-PCR SARS-CoV-2", 23, "B", 160, 13, 163, 170, "Recherche du génome du SARS COV 2 par RT-PCR, '
                         'les amorces utilisés pour ce test ciblent les gènes ... et ... du génome du SARS COV2", 4)'))
        except Exception as err:
            print("ERROR insert B5271a analysis,\n\terr=" + str(err))
        else:
            try:
                # Insert links for B5271a
                conn.execute(text('insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) '
                             'select 1000, id_data, (select id_data from sigl_07_data '
                             'where libelle="Recherche de l\'ARN du virus SARS-CoV-2 (COVID 19) par RT-PCR"), 1, 4 '
                             'from sigl_05_data where code="B5271a"'))

                conn.execute(text('insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) '
                             'select 1000, id_data, (select id_data from sigl_07_data '
                             'where libelle="Cycle d\'amplification"), 2, 4 from sigl_05_data where code="B5271a"'))

            except Exception as err:
                print("ERROR insert links for B5271a analysis,\n\terr=" + str(err))

        # RT-LAMP SARS-CoV-2
        try:
            conn.execute(text('insert into sigl_05_data (id_owner, code, nom, abbr, famille, cote_unite, cote_valeur, '
                         'produit_biologique, type_prel, type_analyse, commentaire, actif) '
                         'values (1000, "B5271b", "Recherche de l\'ARN de virus SARS-CoV-2 (COVID 19) par RT-LAMP", '
                         '"RT-LAMP SARS-CoV-2", 23, "B", 160, 13, 163, 170, "Recherche du génome du SARS-CoV-2 '
                         'par RT-LAMP, les amorces utilisés pour ce test ciblent les gènes ... et ... du génome '
                         'du SARS COV2", 4)'))
        except Exception as err:
            print("ERROR insert B5271b analysis,\n\terr=" + str(err))
        else:
            try:
                # Insert links for B5271b
                conn.execute(text('insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) '
                             'select 1000, id_data, (select id_data from sigl_07_data '
                             'where libelle="Recherche de l\'ARN du virus SARS-CoV-2 (COVID 19) par RT-LAMP"), 1, 4 '
                             'from sigl_05_data where code="B5271b"'))

                conn.execute(text('insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) '
                             'select 1000, id_data, (select id_data from sigl_07_data '
                             'where libelle="Cycle d\'amplification"), 2, 4 from sigl_05_data where code="B5271b"'))

            except Exception as err:
                print("ERROR insert links for B5271b analysis,\n\terr=" + str(err))

        # ANTIGEN TEST SARS-CoV-2
        try:
            conn.execute(text('insert into sigl_05_data (id_owner, code, nom, abbr, famille, cote_unite, cote_valeur, '
                         'produit_biologique, type_prel, type_analyse, commentaire, actif) '
                         'values (1000, "B4274", "Recherche de l\'antigène pour le SARS-CoV-2 (COVID 19)", "",302, "B", '
                         '36, 1, 163, 170, "Recherche d\'un antigène du SARS-CoV-2, recherche par tests non automatisable '
                         'de type immunochromatographique ciblant l\'antigène ... du SARS-CoV-2 (dépend du kit utilisé)", 4)'))
        except Exception as err:
            print("ERROR insert B4274 analysis,\n\terr=" + str(err))
        else:
            try:
                # Insert links for B4274
                conn.execute(text('insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) '
                             'select 1000, id_data, (select id_data from sigl_07_data '
                             'where libelle="Recherche de l\'antigène pour le SARS-CoV-2 (COVID 19)"), 1, 4 '
                             'from sigl_05_data where code="B4274"'))

            except Exception as err:
                print("ERROR insert links for B4274 analysis,\n\terr=" + str(err))

        # SEROLOGICAL TEST SARS-CoV-2
        try:
            conn.execute(text('insert into sigl_05_data (id_owner, code, nom, abbr, famille, cote_unite, cote_valeur, '
                         'produit_biologique, type_prel, type_analyse, commentaire, actif) '
                         'values (1000, "B4719", "Recherche des Ac Anti SARS-CoV-2 (COVID 19)", "", 302, "B", 45, 1, 138, '
                         '170, "Recherche et titrage éventuels des anticorps dirigés contre le SARS-CoV-2, '
                         'recherche par tests automatisables de type ELISA/ELFA", 4)'))
        except Exception as err:
            print("ERROR insert B4719 analysis,\n\terr=" + str(err))
        else:
            try:
                # Insert links for B4719
                conn.execute(text('insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) '
                             'select 1000, id_data, (select id_data from sigl_07_data '
                             'where libelle="Recherche des Ac Anti SARS-CoV-2 (COVID 19)"), 1, 4 '
                             'from sigl_05_data where code="B4719"'))

                conn.execute(text('insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) '
                             'select 1000, id_data, (select id_data from sigl_07_data '
                             'where libelle="Titrage des Ac Anti SARS-CoV-2 (COVID 19)"), 2, 4 '
                             'from sigl_05_data where code="B4719"'))

            except Exception as err:
                print("ERROR insert links for B4719 analysis,\n\terr=" + str(err))

        # QUICK SEROLOGICAL TEST SARS-CoV-2
        try:
            conn.execute(text('insert into sigl_05_data (id_owner, code, nom, abbr, famille, cote_unite, cote_valeur, '
                         'produit_biologique, type_prel, type_analyse, commentaire, actif) '
                         'values (1000, "B4721", "Recherche rapide des Ac Anti SARS-CoV-2 (COVID 19)", "", 302, "B", '
                         '35, 1, 138, 170, "Recherche des anticorps dirigés contre le SARS-CoV-2, recherche par '
                         'tests immunochromatographiques", 4)'))
        except Exception as err:
            print("ERROR insert B4721 analysis,\n\terr=" + str(err))
        else:
            try:
                # Insert links for B4721
                conn.execute(text('insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) '
                             'select 1000, id_data, (select id_data from sigl_07_data '
                             'where libelle="Recherche des Ac Anti SARS-CoV-2 (COVID 19)"), 1, 4 '
                             'from sigl_05_data where code="B4721"'))

                conn.execute(text('insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) '
                             'select 1000, id_data, (select id_data from sigl_07_data '
                             'where libelle="Titrage des Ac Anti SARS-CoV-2 (COVID 19)"), 2, 4 '
                             'from sigl_05_data where code="B4721"'))

            except Exception as err:
                print("ERROR insert links for B4721 analysis,\n\terr=" + str(err))

    # UPDATE formula in SIGL_07_DATA for VIH analysis
    try:
        conn = op.get_bind()

        conn.execute(text('update sigl_07_data set formule="$1 / $3 * 100" where id_data=182 and formule="($1 + $2) * 100 / $3"'))
    except Exception as err:
        print("ERROR update sigl_07_data set formule='$1 / $3 * 100' where id_data=182 ...,\n\terr=" + str(err))

    # UPDATE SIGL_15_DATA for VIH epidemio
    try:
        conn = op.get_bind()

        conn.execute(text('update sigl_15_data set formule="$_284" where id_data=68 and formule="$_182 > 1000"'))
    except Exception as err:
        print("ERROR update sigl_15_data set formule='$_284' where id_data=68 ...,\n\terr=" + str(err))

    # UPDATE SIGL_15_DATA for Paludisme epidemio
    try:
        conn = op.get_bind()

        conn.execute(text('update sigl_15_data set formule="$_316 != [posnegind.Positif]" where id_data=44 and '
                     'formule="$_316 != [posnegind.Positif] AND $_616 != [posnegind.Positif] AND $_617 != [posnegind.Positif]"'))
    except Exception as err:
        print("ERROR update sigl_15_data set formule='$_316 != [posnegind.Positif]' where id_data=44 ...,\n\terr=" + str(err))

    try:
        conn = op.get_bind()

        conn.execute(text('update sigl_15_data set formule="$_316 = [posnegind.Positif]" where id_data=45 and '
                     'formule="$_316 = [posnegind.Positif] OR $_616 = [posnegind.Positif] OR $_617 = [posnegind.Positif]"'))
    except Exception as err:
        print("ERROR update sigl_15_data set formule='$_316 = [posnegind.Positif]' where id_data=45 ...,\n\terr=" + str(err))

    print(str(datetime.today()) + " : END of migration v3_0_3_add_covid_analizes revision=1c2971eb5ac6")


def downgrade():
    pass
