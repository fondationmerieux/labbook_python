# -*- coding:utf-8 -*-
"""v3_0_7_changes_for_dhis2_monthly

Revision ID: 2660636fdaf9
Revises: 3c7d8a35d79a
Create Date: 2021-05-18 10:06:01.906600

"""
from alembic import op
from sqlalchemy import text

from datetime import datetime

# revision identifiers, used by Alembic.
revision = '2660636fdaf9'
down_revision = '3c7d8a35d79a'
branch_labels = None
depends_on = None


def upgrade():
    print("--- " + str(datetime.today()) + "---")
    print("START of migration v3.0.7_changes_for_dhis2_monthly revision=2660636fdaf9")

    # Get the current
    conn = op.get_bind()

    # DELETE Indetermine for dico_posneg
    try:
        conn.execute(text("delete from sigl_dico_data where dico_name='posneg' and short_label='EQUI'"))
    except Exception as err:
        print("ERROR delete Indeterminé for dico_posneg in sigl_dico_data,\n\terr=" + str(err))

    # ADD an unmutable unique id for analysis variable
    try:
        conn.execute(text("alter table sigl_07_data add column code_var varchar(10) unique"))
    except Exception as err:
        print("ERROR add column code_var to sigl_07_data,\n\terr=" + str(err))
    else:
        # init code_var for old variable
        try:
            conn.execute(text("update sigl_07_data set code_var=id_data"))
        except Exception as err:
            print("ERROR init code_var for all variables,\n\terr=" + str(err))

    # ADD flag for exclude variable to export WHONET
    try:
        conn.execute(text("alter table sigl_05_07_data add column var_whonet int(1) default 5"))
    except Exception as err:
        print("ERROR add column var_whonet to sigl_05_07_data,\n\terr=" + str(err))
    else:
        # change for antibiogramme variables
        try:
            conn.execute(text("update sigl_05_07_data set var_whonet=4 "
                         "where id_refanalyse in (select id_data from sigl_05_data where code in ('B650','B651','B652',"
                         "'B653','B654','B655','B656','B657','B658','B670','B671','B672','B673','B674','B675','B676',"
                         "'B677','B678'))"))
        except Exception as err:
            print("ERROR update var_whonet for new existing ABG anayzes,\n\terr=" + str(err))

    # Change type_resultat for variable with id_data=236
    try:
        conn.execute(text("update sigl_07_data set type_resultat=246 "
                     "where code_var='236' and libelle='Recherche directe de chlamydiae par technique immunologique'"))
    except Exception as err:
        print("ERROR update type_resultat for a variable without type_resultat,\n\terr=" + str(err))

    # Change formule for Chlamydia trachomatis direct (Prélèvement Urétral)
    try:
        conn.execute(text("update sigl_15_data set formule='$_236 = [absent.present]' "
                     "where id_data=132 and label_exp_dhis2='Chlamydia trachomatis direct (Prelevement Uretral)'"))
    except Exception as err:
        print("ERROR update type_resultat for a variable without type_resultat,\n\terr=" + str(err))

    # Change label_exp_dhis2 for Candida albicans (Prélèvement Urétral)
    try:
        conn.execute(text("update sigl_15_data set label_exp_dhis2='Candida albicans (Prélèvement Urétral)' "
                     "where id_data=83 and label_exp_dhis2='Chlamydia trachomatis direct (Prelevement Uretral)'"))
    except Exception as err:
        print("ERROR update type_resultat for a variable without type_resultat,\n\terr=" + str(err))

    # MODIFY EBOLA ANALYZES Titrage to Ct
    try:
        conn.execute(text('update sigl_07_data set libelle="Cycle d\'amplification", '
                     'unite=(select id_data from sigl_dico_data where label="Ct" limit 1) '
                     'where libelle="Titrage" and id_data in '
                     '(select id_refvariable from sigl_05_07_data where id_refanalyse in '
                     '(select id_data from sigl_05_data where code in ("E01","E02","E03","E04","E05")))'))
    except Exception as err:
        print("ERROR update titrage variable for Ebola analyzes,\n\terr=" + str(err))

    # MODIFY SARS-CoV-2 ANALYZES Absent/present to Positif/Négatif
    try:
        conn.execute(text("update sigl_07_data set type_resultat=(select id_data from sigl_dico_data "
                     "where code='D_POS_NEG' limit 1) "
                     "where type_resultat=(select id_data from sigl_dico_data where code='D_ABS' limit 1) and "
                     "id_data in (select id_refvariable from sigl_05_07_data where id_refanalyse in "
                     "(select id_data from sigl_05_data where code in ('B4274','B4719','B4721','B5271a','B5271b')))"))
    except Exception as err:
        print("ERROR update type_resultat Absent/Présent to Positif/Négatif/Indéterminé for SARS-CoV-2 analyzes,\n\terr=" + str(err))

    # MODIFY SARS-CoV-2 B4721 remove link with Titrage variable
    try:
        conn.execute(text("delete from sigl_05_07_data "
                     "where position=2 and id_refanalyse in (select id_data from sigl_05_data where code='B4721')"))
    except Exception as err:
        print("ERROR remove link with Titrage variable for SARS-CoV-2 B4721,\n\terr=" + str(err))

    # MODIFY SARS-CoV-2 B4721 update name
    try:
        conn.execute(text("update sigl_05_data set nom='Test de Détection Rapide (TDR) de recherche de protéines du "
                     "virus SARS-CoV-2' where code='B4721'"))
    except Exception as err:
        print("ERROR rename B4721 analysis,\n\terr=" + str(err))

    # MODIFY SARS-CoV-2 B4274 update name
    try:
        conn.execute(text("update sigl_05_data set nom='Test sérologique unitaire qualitatif de recherche des anticorps "
                     "dirigés contre des antigènes du virus SARS-CoV-2' where code='B4274'"))
    except Exception as err:
        print("ERROR rename B4274 analysis,\n\terr=" + str(err))

    # MODIFY SARS-CoV-2 B4719 update name
    try:
        conn.execute(text("update sigl_05_data set nom='Test sérologique quantitatif automatisable de recherche des "
                     "anticorps dirigés contre des antigènes du virus SARS-CoV-2' where code='B4719'"))
    except Exception as err:
        print("ERROR rename B4719 analysis,\n\terr=" + str(err))

    # MODIFY SARS-CoV-2 B5271a update name
    try:
        conn.execute(text("update sigl_05_data set nom='Recherche quantitative du génome du virus SARS-CoV-2 par RT-PCR "
                     "(Reverse Transcriptase Polymerase Chain Reaction)' where code='B5271a'"))
    except Exception as err:
        print("ERROR rename B5271a analysis,\n\terr=" + str(err))

    # MODIFY SARS-CoV-2 B5271a remove link with Cycle amplification variable
    try:
        conn.execute(text("delete from sigl_05_07_data "
                     "where position=2 and id_refanalyse in (select id_data from sigl_05_data where code='B5271a')"))
    except Exception as err:
        print("ERROR remove link with Cycle amplification variable for SARS-CoV-2 B5271a,\n\terr=" + str(err))

    # MODIFY SARS-CoV-2 B5271b update name
    try:
        conn.execute(text("update sigl_05_data set nom='Recherche qualitative du génome du virus SARS-CoV-2 par "
                     "Reverse Transcriptase Loop-mediated isothermal AMPlification' where code='B5271b'"))
    except Exception as err:
        print("ERROR rename B5271b analysis,\n\terr=" + str(err))

    # MODIFY SARS-CoV-2 B5271b remove link with Cycle amplification variable
    try:
        conn.execute(text("delete from sigl_05_07_data "
                     "where position=2 and id_refanalyse in (select id_data from sigl_05_data where code='B5271b')"))
    except Exception as err:
        print("ERROR remove link with Cycle amplification variable for SARS-CoV-2 B5271b,\n\terr=" + str(err))

    # ADD Phenotype dictionnary x6
    try:
        conn.execute(text("insert into sigl_dico_data (id_owner, dico_name, label, short_label, position, code) "
                     "values (100, 'pheno', 'Ph. sauvage', 'Ph. sauvage', 10, 'pheno_01')"))
    except Exception as err:
        print("ERROR insert new dict Phenotype 01,\n\terr=" + str(err))

    try:
        conn.execute(text("insert into sigl_dico_data (id_owner, dico_name, label, short_label, position, code) "
                     "values (100, 'pheno', 'Ph. Pénicillinase à bas niveau', 'Ph. Pénicillinase b.', 20, 'pheno_02')"))
    except Exception as err:
        print("ERROR insert new dict Phenotype 02,\n\terr=" + str(err))

    try:
        conn.execute(text("insert into sigl_dico_data (id_owner, dico_name, label, short_label, position, code) "
                     "values (100, 'pheno', 'Ph. Pénicillinase à haut niveau', 'Ph. Pénicillinase h.', 30, 'pheno_03')"))
    except Exception as err:
        print("ERROR insert new dict Phenotype 03,\n\terr=" + str(err))

    try:
        conn.execute(text("insert into sigl_dico_data (id_owner, dico_name, label, short_label, position, code) "
                     "values (100, 'pheno', 'Phénotype TRI', 'Ph. TRI', 40, 'pheno_04')"))
    except Exception as err:
        print("ERROR insert new dict Phenotype 04,\n\terr=" + str(err))

    try:
        conn.execute(text("insert into sigl_dico_data (id_owner, dico_name, label, short_label, position, code) "
                     "values (100, 'pheno', 'Phénotype céphalosporinase', 'Ph. céphalosporinase', 50, 'pheno_05')"))
    except Exception as err:
        print("ERROR insert new dict Phenotype 05,\n\terr=" + str(err))

    try:
        conn.execute(text("insert into sigl_dico_data (id_owner, dico_name, label, short_label, position, code) "
                     "values (100, 'pheno', 'Phénotype BLSE', 'Ph. BLSE', 60, 'pheno_06')"))
    except Exception as err:
        print("ERROR insert new dict Phenotype 06,\n\terr=" + str(err))

    # ADD Phenotype type of result
    try:
        conn.execute(text("insert into sigl_dico_data (id_owner, dico_name, label, short_label, position, code) "
                     "values (100, 'type_resultat', 'Phénotypes', 'dico_pheno', 370, 'dico_pheno')"))
    except Exception as err:
        print("ERROR insert new type of result Phenotypes,\n\terr=" + str(err))

    # ADD Phenotype variable
    try:
        conn.execute(text("insert into sigl_07_data (id_owner, libelle, type_resultat) "
                     "values (1000, 'Phénotype', (select id_data from sigl_dico_data where dico_name='type_resultat' "
                     "and short_label='dico_pheno'))"))

        conn.execute(text("update sigl_07_data set code_var=id_data where libelle='Phénotype' limit 1"))
    except Exception as err:
        print("ERROR insert new variable Phenotype,\n\terr=" + str(err))
    else:
        # Link Phenotype variable to B656, B657, B658, B676, B677, B678
        try:
            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "values (1000, (select id_data from sigl_05_data where code='B656'), "
                         "(select id_data from sigl_07_data where libelle='Phénotype' order by id_data desc limit 1), 41, 5, 5)"))
        except Exception as err:
            print("ERROR insert new link with Phenotype to B656,\n\terr=" + str(err))

        try:
            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "values (1000, (select id_data from sigl_05_data where code='B657'), "
                         "(select id_data from sigl_07_data where libelle='Phénotype' order by id_data desc limit 1), 41, 5, 5)"))
        except Exception as err:
            print("ERROR insert new link with Phenotype to B657,\n\terr=" + str(err))

        try:
            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "values (1000, (select id_data from sigl_05_data where code='B658'), "
                         "(select id_data from sigl_07_data where libelle='Phénotype' order by id_data desc limit 1), 41, 5, 5)"))
        except Exception as err:
            print("ERROR insert new link with Phenotype to B658,\n\terr=" + str(err))

        try:
            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "values (1000, (select id_data from sigl_05_data where code='B676'), "
                         "(select id_data from sigl_07_data where libelle='Phénotype' order by id_data desc limit 1), 41, 5, 5)"))
        except Exception as err:
            print("ERROR insert new link with Phenotype to B676,\n\terr=" + str(err))

        try:
            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "values (1000, (select id_data from sigl_05_data where code='B677'), "
                         "(select id_data from sigl_07_data where libelle='Phénotype' order by id_data desc limit 1), 41, 5, 5)"))
        except Exception as err:
            print("ERROR insert new link with Phenotype to B677,\n\terr=" + str(err))

        try:
            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "values (1000, (select id_data from sigl_05_data where code='B678'), "
                         "(select id_data from sigl_07_data where libelle='Phénotype' order by id_data desc limit 1), 41, 5, 5)"))
        except Exception as err:
            print("ERROR insert new link with Phenotype to B678,\n\terr=" + str(err))

    # ADD new ABG analyzes B659
    try:
        conn.execute(text("insert into sigl_05_data (id_owner, code, nom, abbr, famille, cote_unite, commentaire, actif, ana_whonet) "
                     "values (1000, 'B659', 'Antibiogramme Klebsiella spp. [DISK]', 'ABG Klebsiella', 18, 'B', '', 4, 4)"))
    except Exception as err:
        print("ERROR insert B659 analysis,\n\terr=" + str(err))
    else:
        try:
            # Insert links for B659
            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 440, 1, 5, 4 from sigl_05_data where code='B659'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B659') as id_refanalyse, id_data, 2, 5, 4 "
                         "from sigl_07_data where libelle='Diam. inhibition Amoxicilline' order by id_data desc limit 1"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 443, 3, 5, 4 from sigl_05_data where code='B659'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B659') as id_refanalyse, id_data, 4, 5, 4 "
                         "from sigl_07_data where libelle='Diam. inhibition Amoxicilline/ac. Clavulanique' order by id_data desc limit 1"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 597, 5, 5, 4 from sigl_05_data where code='B659'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B659') as id_refanalyse, id_data, 6, 5, 4 "
                         "from sigl_07_data where libelle='Diam. inhibition Ticarcilline' order by id_data desc limit 1"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 573, 7, 5, 4 from sigl_05_data where code='B659'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B659') as id_refanalyse, id_data, 8, 5, 4 "
                         "from sigl_07_data where libelle='Diam. inhibition Pipéracilline' order by id_data desc limit 1"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 450, 9, 5, 4 from sigl_05_data where code='B659'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B659') as id_refanalyse, id_data, 10, 5, 4 "
                         "from sigl_07_data where libelle='Diam. inhibition Aztréonam' order by id_data desc limit 1"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 530, 11, 5, 4 from sigl_05_data where code='B659'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B659') as id_refanalyse, id_data, 12, 5, 4 "
                         "from sigl_07_data where libelle='Diam. inhibition Imipénème' order by id_data desc limit 1"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 460, 13, 5, 4 from sigl_05_data where code='B659'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B659') as id_refanalyse, id_data, 14, 5, 4 "
                         "from sigl_07_data where libelle='Diam. inhibition Céfalotine' order by id_data desc limit 1"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 482, 15, 5, 4 from sigl_05_data where code='B659'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B659') as id_refanalyse, id_data, 16, 5, 4 "
                         "from sigl_07_data where libelle='Diam. inhibition Céfoxitine' order by id_data desc limit 1"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 496, 17, 5, 4 from sigl_05_data where code='B659'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B659') as id_refanalyse, id_data, 18, 5, 4 "
                         "from sigl_07_data where libelle='Diam. inhibition Céftriaxone' order by id_data desc limit 1"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 492, 19, 5, 4 from sigl_05_data where code='B659'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B659') as id_refanalyse, id_data, 20, 5, 4 "
                         "from sigl_07_data where libelle='Diam. inhibition Ceftazidime' order by id_data desc limit 1"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 534, 21, 5, 4 from sigl_05_data where code='B659'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B659') as id_refanalyse, id_data, 22, 5, 4 "
                         "from sigl_07_data where libelle='Diam. inhibition Kanamycine' order by id_data desc limit 1"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 603, 23, 5, 4 from sigl_05_data where code='B659'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B659') as id_refanalyse, id_data, 24, 5, 4 "
                         "from sigl_07_data where libelle='Diam. inhibition Tobramycine' order by id_data desc limit 1"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 528, 25, 5, 4 from sigl_05_data where code='B659'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B659') as id_refanalyse, id_data, 26, 5, 4 "
                         "from sigl_07_data where libelle='Diam. inhibition Gentamicine' order by id_data desc limit 1"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 502, 27, 5, 4 from sigl_05_data where code='B659'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B659') as id_refanalyse, id_data, 28, 5, 4 "
                         "from sigl_07_data where libelle='Diam. inhibition Chloramphénicol' order by id_data desc limit 1"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 508, 29, 5, 4 from sigl_05_data where code='B659'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B659') as id_refanalyse, id_data, 30, 5, 4 "
                         "from sigl_07_data where libelle='Diam. inhibition Colistine' order by id_data desc limit 1"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 430, 31, 5, 4 from sigl_05_data where code='B659'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B659') as id_refanalyse, id_data, 32, 5, 4 "
                         "from sigl_07_data where libelle='Diam. inhibition Acide nalidixique' order by id_data desc limit 1"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 560, 33, 5, 4 from sigl_05_data where code='B659'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B659') as id_refanalyse, id_data, 34, 5, 4 "
                         "from sigl_07_data where libelle='Diam. inhibition Norfloxacine' order by id_data desc limit 1"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 504, 35, 5, 4 from sigl_05_data where code='B659'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B659') as id_refanalyse, id_data, 36, 5, 4 "
                         "from sigl_07_data where libelle='Diam. inhibition Ciprofloxacine' order by id_data desc limit 1"))

            # Link phenotype
            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "values (1000, (select id_data from sigl_05_data where code='B659'), "
                         "(select id_data from sigl_07_data where libelle='Phénotype' order by id_data desc limit 1), 37, 5, 5)"))

        except Exception as err:
            print("ERROR insert links for B659 analysis,\n\terr=" + str(err))

    # ADD new ABG analyzes B660
    try:
        conn.execute(text("insert into sigl_05_data (id_owner, code, nom, abbr, famille, cote_unite, commentaire, actif, ana_whonet) "
                     "values (1000, 'B660', 'Antibiogramme Enterobacter spp. [DISK]', 'ABG Enterobacter', 18, 'B', '', 4, 4)"))
    except Exception as err:
        print("ERROR insert B660 analysis,\n\terr=" + str(err))
    else:
        try:
            # Insert links for B660
            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 440, 1, 5, 4 from sigl_05_data where code='B660'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B660') as id_refanalyse, id_data, 2, 5, 4 "
                         "from sigl_07_data where libelle='Diam. inhibition Amoxicilline' order by id_data desc limit 1"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 443, 3, 5, 4 from sigl_05_data where code='B660'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B660') as id_refanalyse, id_data, 4, 5, 4 "
                         "from sigl_07_data where libelle='Diam. inhibition Amoxicilline/ac. Clavulanique' order by id_data desc limit 1"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 597, 5, 5, 4 from sigl_05_data where code='B660'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B660') as id_refanalyse, id_data, 6, 5, 4 "
                         "from sigl_07_data where libelle='Diam. inhibition Ticarcilline' order by id_data desc limit 1"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 573, 7, 5, 4 from sigl_05_data where code='B660'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B660') as id_refanalyse, id_data, 8, 5, 4 "
                         "from sigl_07_data where libelle='Diam. inhibition Pipéracilline' order by id_data desc limit 1"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 450, 9, 5, 4 from sigl_05_data where code='B660'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B660') as id_refanalyse, id_data, 10, 5, 4 "
                         "from sigl_07_data where libelle='Diam. inhibition Aztréonam' order by id_data desc limit 1"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 530, 11, 5, 4 from sigl_05_data where code='B660'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B660') as id_refanalyse, id_data, 12, 5, 4 "
                         "from sigl_07_data where libelle='Diam. inhibition Imipénème' order by id_data desc limit 1"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 460, 13, 5, 4 from sigl_05_data where code='B660'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B660') as id_refanalyse, id_data, 14, 5, 4 "
                         "from sigl_07_data where libelle='Diam. inhibition Céfalotine' order by id_data desc limit 1")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 482, 15, 5, 4 from sigl_05_data where code='B660'")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B660') as id_refanalyse, id_data, 16, 5, 4 "
                         "from sigl_07_data where libelle='Diam. inhibition Céfoxitine' order by id_data desc limit 1")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 496, 17, 5, 4 from sigl_05_data where code='B660'")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B660') as id_refanalyse, id_data, 18, 5, 4 "
                         "from sigl_07_data where libelle='Diam. inhibition Céftriaxone' order by id_data desc limit 1")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 492, 19, 5, 4 from sigl_05_data where code='B660'")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B660') as id_refanalyse, id_data, 20, 5, 4 "
                         "from sigl_07_data where libelle='Diam. inhibition Ceftazidime' order by id_data desc limit 1")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 534, 21, 5, 4 from sigl_05_data where code='B660'")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B660') as id_refanalyse, id_data, 22, 5, 4 "
                         "from sigl_07_data where libelle='Diam. inhibition Kanamycine' order by id_data desc limit 1"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 603, 23, 5, 4 from sigl_05_data where code='B660'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B660') as id_refanalyse, id_data, 24, 5, 4 "
                         "from sigl_07_data where libelle='Diam. inhibition Tobramycine' order by id_data desc limit 1"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 528, 25, 5, 4 from sigl_05_data where code='B660'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B660') as id_refanalyse, id_data, 26, 5, 4 "
                         "from sigl_07_data where libelle='Diam. inhibition Gentamicine' order by id_data desc limit 1"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 502, 27, 5, 4 from sigl_05_data where code='B660'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B660') as id_refanalyse, id_data, 28, 5, 4 "
                         "from sigl_07_data where libelle='Diam. inhibition Chloramphénicol' order by id_data desc limit 1"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 508, 29, 5, 4 from sigl_05_data where code='B660'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B660') as id_refanalyse, id_data, 30, 5, 4 "
                         "from sigl_07_data where libelle='Diam. inhibition Colistine' order by id_data desc limit 1"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 430, 31, 5, 4 from sigl_05_data where code='B660'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B660') as id_refanalyse, id_data, 32, 5, 4 "
                         "from sigl_07_data where libelle='Diam. inhibition Acide nalidixique' order by id_data desc limit 1"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 560, 33, 5, 4 from sigl_05_data where code='B660'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B660') as id_refanalyse, id_data, 34, 5, 4 "
                         "from sigl_07_data where libelle='Diam. inhibition Norfloxacine' order by id_data desc limit 1"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 504, 35, 5, 4 from sigl_05_data where code='B660'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B660') as id_refanalyse, id_data, 36, 5, 4 "
                         "from sigl_07_data where libelle='Diam. inhibition Ciprofloxacine' order by id_data desc limit 1"))

            # Link phenotype
            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "values (1000, (select id_data from sigl_05_data where code='B660'), "
                         "(select id_data from sigl_07_data where libelle='Phénotype' order by id_data desc limit 1), 37, 5, 5)"))

        except Exception as err:
            print("ERROR insert links for B660 analysis,\n\terr=" + str(err))

    # ADD new ABG analyzes B661
    try:
        conn.execute(text("insert into sigl_05_data (id_owner, code, nom, abbr, famille, cote_unite, commentaire, actif, ana_whonet) "
                     "values (1000, 'B661', 'Antibiogramme Vibrio cholerae spp. [DISK]', 'ABG Vibrio cholerae', 18, 'B', '', 4, 4)"))
    except Exception as err:
        print("ERROR insert B661 analysis,\n\terr=" + str(err))
    else:
        try:
            # Insert links for B661
            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 440, 1, 5, 4 from sigl_05_data where code='B661'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B661') as id_refanalyse, id_data, 2, 5, 4 "
                         "from sigl_07_data where libelle='Diam. inhibition Amoxicilline' order by id_data desc limit 1"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 443, 3, 5, 4 from sigl_05_data where code='B661'")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B661') as id_refanalyse, id_data, 4, 5, 4 "
                         "from sigl_07_data where libelle='Diam. inhibition Amoxicilline/ac. Clavulanique' order by id_data desc limit 1")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 597, 5, 5, 4 from sigl_05_data where code='B661'")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B661') as id_refanalyse, id_data, 6, 5, 4 "
                         "from sigl_07_data where libelle='Diam. inhibition Ticarcilline' order by id_data desc limit 1")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 573, 7, 5, 4 from sigl_05_data where code='B661'")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B661') as id_refanalyse, id_data, 8, 5, 4 "
                         "from sigl_07_data where libelle='Diam. inhibition Pipéracilline' order by id_data desc limit 1")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 450, 9, 5, 4 from sigl_05_data where code='B661'")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B661') as id_refanalyse, id_data, 10, 5, 4 "
                         "from sigl_07_data where libelle='Diam. inhibition Aztréonam' order by id_data desc limit 1")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 530, 11, 5, 4 from sigl_05_data where code='B661'")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B661') as id_refanalyse, id_data, 12, 5, 4 "
                         "from sigl_07_data where libelle='Diam. inhibition Imipénème' order by id_data desc limit 1")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 460, 13, 5, 4 from sigl_05_data where code='B661'")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B661') as id_refanalyse, id_data, 14, 5, 4 "
                         "from sigl_07_data where libelle='Diam. inhibition Céfalotine' order by id_data desc limit 1")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 482, 15, 5, 4 from sigl_05_data where code='B661'")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B661') as id_refanalyse, id_data, 16, 5, 4 "
                         "from sigl_07_data where libelle='Diam. inhibition Céfoxitine' order by id_data desc limit 1")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 496, 17, 5, 4 from sigl_05_data where code='B661'")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B661') as id_refanalyse, id_data, 18, 5, 4 "
                         "from sigl_07_data where libelle='Diam. inhibition Céftriaxone' order by id_data desc limit 1")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 492, 19, 5, 4 from sigl_05_data where code='B661'")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B661') as id_refanalyse, id_data, 20, 5, 4 "
                         "from sigl_07_data where libelle='Diam. inhibition Ceftazidime' order by id_data desc limit 1")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 534, 21, 5, 4 from sigl_05_data where code='B661'")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B661') as id_refanalyse, id_data, 22, 5, 4 "
                         "from sigl_07_data where libelle='Diam. inhibition Kanamycine' order by id_data desc limit 1")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 603, 23, 5, 4 from sigl_05_data where code='B661'")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B661') as id_refanalyse, id_data, 24, 5, 4 "
                         "from sigl_07_data where libelle='Diam. inhibition Tobramycine' order by id_data desc limit 1")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 528, 25, 5, 4 from sigl_05_data where code='B661'")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B661') as id_refanalyse, id_data, 26, 5, 4 "
                         "from sigl_07_data where libelle='Diam. inhibition Gentamicine' order by id_data desc limit 1")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 502, 27, 5, 4 from sigl_05_data where code='B661'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B661') as id_refanalyse, id_data, 28, 5, 4 "
                         "from sigl_07_data where libelle='Diam. inhibition Chloramphénicol' order by id_data desc limit 1"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 508, 29, 5, 4 from sigl_05_data where code='B661'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B661') as id_refanalyse, id_data, 30, 5, 4 "
                         "from sigl_07_data where libelle='Diam. inhibition Colistine' order by id_data desc limit 1"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 430, 31, 5, 4 from sigl_05_data where code='B661'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B661') as id_refanalyse, id_data, 32, 5, 4 "
                         "from sigl_07_data where libelle='Diam. inhibition Acide nalidixique' order by id_data desc limit 1"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 560, 33, 5, 4 from sigl_05_data where code='B661'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B661') as id_refanalyse, id_data, 34, 5, 4 "
                         "from sigl_07_data where libelle='Diam. inhibition Norfloxacine' order by id_data desc limit 1"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 504, 35, 5, 4 from sigl_05_data where code='B661'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B661') as id_refanalyse, id_data, 36, 5, 4 "
                         "from sigl_07_data where libelle='Diam. inhibition Ciprofloxacine' order by id_data desc limit 1"))

            # Link phenotype
            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "values (1000, (select id_data from sigl_05_data where code='B661'), "
                         "(select id_data from sigl_07_data where libelle='Phénotype' order by id_data desc limit 1), 37, 5, 5)"))

        except Exception as err:
            print("ERROR insert links for B661 analysis,\n\terr=" + str(err))

    # ADD new ABG analyzes B679
    try:
        conn.execute(text("insert into sigl_05_data (id_owner, code, nom, abbr, famille, cote_unite, commentaire, actif, ana_whonet) "
                     "values (1000, 'B679', 'Antibiogramme Klebsiella spp. [CMI]', 'ABG Klebsiella', 18, 'B', '', 4, 4)"))
    except Exception as err:
        print("ERROR insert B679 analysis,\n\terr=" + str(err))
    else:
        try:
            # Insert links for B679
            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 440, 1, 5, 4 from sigl_05_data where code='B679'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B679') as id_refanalyse, id_data, 2, 5, 4 "
                         "from sigl_07_data where libelle='CMI Amoxicilline' order by id_data desc limit 1"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 443, 3, 5, 4 from sigl_05_data where code='B679'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B679') as id_refanalyse, id_data, 4, 5, 4 "
                         "from sigl_07_data where libelle='CMI Amoxicilline/ac. Clavulanique' order by id_data desc limit 1"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 597, 5, 5, 4 from sigl_05_data where code='B679'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B679') as id_refanalyse, id_data, 6, 5, 4 "
                         "from sigl_07_data where libelle='CMI Ticarcilline' order by id_data desc limit 1"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 573, 7, 5, 4 from sigl_05_data where code='B679'")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B679') as id_refanalyse, id_data, 8, 5, 4 "
                         "from sigl_07_data where libelle='CMI Pipéracilline' order by id_data desc limit 1")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 450, 9, 5, 4 from sigl_05_data where code='B679'")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B679') as id_refanalyse, id_data, 10, 5, 4 "
                         "from sigl_07_data where libelle='CMI Aztréonam' order by id_data desc limit 1")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 530, 11, 5, 4 from sigl_05_data where code='B679'")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B679') as id_refanalyse, id_data, 12, 5, 4 "
                         "from sigl_07_data where libelle='CMI Imipénème' order by id_data desc limit 1")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 460, 13, 5, 4 from sigl_05_data where code='B679'")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B679') as id_refanalyse, id_data, 14, 5, 4 "
                         "from sigl_07_data where libelle='CMI Céfalotine' order by id_data desc limit 1")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 482, 15, 5, 4 from sigl_05_data where code='B679'")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B679') as id_refanalyse, id_data, 16, 5, 4 "
                         "from sigl_07_data where libelle='CMI Céfoxitine' order by id_data desc limit 1")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 496, 17, 5, 4 from sigl_05_data where code='B679'")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B679') as id_refanalyse, id_data, 18, 5, 4 "
                         "from sigl_07_data where libelle='CMI Céftriaxone' order by id_data desc limit 1")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 492, 19, 5, 4 from sigl_05_data where code='B679'")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B679') as id_refanalyse, id_data, 20, 5, 4 "
                         "from sigl_07_data where libelle='CMI Ceftazidime' order by id_data desc limit 1")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 534, 21, 5, 4 from sigl_05_data where code='B679'")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B679') as id_refanalyse, id_data, 22, 5, 4 "
                         "from sigl_07_data where libelle='CMI Kanamycine' order by id_data desc limit 1")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 603, 23, 5, 4 from sigl_05_data where code='B679'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B679') as id_refanalyse, id_data, 24, 5, 4 "
                         "from sigl_07_data where libelle='CMI Tobramycine' order by id_data desc limit 1"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 528, 25, 5, 4 from sigl_05_data where code='B679'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B679') as id_refanalyse, id_data, 26, 5, 4 "
                         "from sigl_07_data where libelle='CMI Gentamicine' order by id_data desc limit 1"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 502, 27, 5, 4 from sigl_05_data where code='B679'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B679') as id_refanalyse, id_data, 28, 5, 4 "
                         "from sigl_07_data where libelle='CMI Chloramphénicol' order by id_data desc limit 1"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 508, 29, 5, 4 from sigl_05_data where code='B679'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B679') as id_refanalyse, id_data, 30, 5, 4 "
                         "from sigl_07_data where libelle='CMI Colistine' order by id_data desc limit 1"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 430, 31, 5, 4 from sigl_05_data where code='B679'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B679') as id_refanalyse, id_data, 32, 5, 4 "
                         "from sigl_07_data where libelle='CMI Acide nalidixique' order by id_data desc limit 1"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 560, 33, 5, 4 from sigl_05_data where code='B679'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B679') as id_refanalyse, id_data, 34, 5, 4 "
                         "from sigl_07_data where libelle='CMI Norfloxacine' order by id_data desc limit 1"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 504, 35, 5, 4 from sigl_05_data where code='B679'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B679') as id_refanalyse, id_data, 36, 5, 4 "
                         "from sigl_07_data where libelle='CMI Ciprofloxacine' order by id_data desc limit 1"))

            # Link phenotype
            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "values (1000, (select id_data from sigl_05_data where code='B679'), "
                         "(select id_data from sigl_07_data where libelle='Phénotype' order by id_data desc limit 1), 37, 5, 5)"))

        except Exception as err:
            print("ERROR insert links for B679 analysis,\n\terr=" + str(err))

    # ADD new ABG analyzes B680
    try:
        conn.execute(text("insert into sigl_05_data (id_owner, code, nom, abbr, famille, cote_unite, commentaire, actif, ana_whonet) "
                     "values (1000, 'B680', 'Antibiogramme Enterobacter spp. [CMI]', 'ABG Enterobacter', 18, 'B', '', 4, 4)"))
    except Exception as err:
        print("ERROR insert B680 analysis,\n\terr=" + str(err))
    else:
        try:
            # Insert links for B680
            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 440, 1, 5, 4 from sigl_05_data where code='B680'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B680') as id_refanalyse, id_data, 2, 5, 4 "
                         "from sigl_07_data where libelle='CMI Amoxicilline' order by id_data desc limit 1"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 443, 3, 5, 4 from sigl_05_data where code='B680'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B680') as id_refanalyse, id_data, 4, 5, 4 "
                         "from sigl_07_data where libelle='CMI Amoxicilline/ac. Clavulanique' order by id_data desc limit 1")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 597, 5, 5, 4 from sigl_05_data where code='B680'")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B680') as id_refanalyse, id_data, 6, 5, 4 "
                         "from sigl_07_data where libelle='CMI Ticarcilline' order by id_data desc limit 1")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 573, 7, 5, 4 from sigl_05_data where code='B680'")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B680') as id_refanalyse, id_data, 8, 5, 4 "
                         "from sigl_07_data where libelle='CMI Pipéracilline' order by id_data desc limit 1")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 450, 9, 5, 4 from sigl_05_data where code='B680'")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B680') as id_refanalyse, id_data, 10, 5, 4 "
                         "from sigl_07_data where libelle='CMI Aztréonam' order by id_data desc limit 1")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 530, 11, 5, 4 from sigl_05_data where code='B680'")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B680') as id_refanalyse, id_data, 12, 5, 4 "
                         "from sigl_07_data where libelle='CMI Imipénème' order by id_data desc limit 1")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 460, 13, 5, 4 from sigl_05_data where code='B680'")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B680') as id_refanalyse, id_data, 14, 5, 4 "
                         "from sigl_07_data where libelle='CMI Céfalotine' order by id_data desc limit 1")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 482, 15, 5, 4 from sigl_05_data where code='B680'")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B680') as id_refanalyse, id_data, 16, 5, 4 "
                         "from sigl_07_data where libelle='CMI Céfoxitine' order by id_data desc limit 1")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 496, 17, 5, 4 from sigl_05_data where code='B680'")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B680') as id_refanalyse, id_data, 18, 5, 4 "
                         "from sigl_07_data where libelle='CMI Céftriaxone' order by id_data desc limit 1")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 492, 19, 5, 4 from sigl_05_data where code='B680'")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B680') as id_refanalyse, id_data, 20, 5, 4 "
                         "from sigl_07_data where libelle='CMI Ceftazidime' order by id_data desc limit 1")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 534, 21, 5, 4 from sigl_05_data where code='B680'")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B680') as id_refanalyse, id_data, 22, 5, 4 "
                         "from sigl_07_data where libelle='CMI Kanamycine' order by id_data desc limit 1")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 603, 23, 5, 4 from sigl_05_data where code='B680'")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B680') as id_refanalyse, id_data, 24, 5, 4 "
                         "from sigl_07_data where libelle='CMI Tobramycine' order by id_data desc limit 1")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 528, 25, 5, 4 from sigl_05_data where code='B680'")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B680') as id_refanalyse, id_data, 26, 5, 4 "
                         "from sigl_07_data where libelle='CMI Gentamicine' order by id_data desc limit 1")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 502, 27, 5, 4 from sigl_05_data where code='B680'")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B680') as id_refanalyse, id_data, 28, 5, 4 "
                         "from sigl_07_data where libelle='CMI Chloramphénicol' order by id_data desc limit 1")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 508, 29, 5, 4 from sigl_05_data where code='B680'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B680') as id_refanalyse, id_data, 30, 5, 4 "
                         "from sigl_07_data where libelle='CMI Colistine' order by id_data desc limit 1"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 430, 31, 5, 4 from sigl_05_data where code='B680'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B680') as id_refanalyse, id_data, 32, 5, 4 "
                         "from sigl_07_data where libelle='CMI Acide nalidixique' order by id_data desc limit 1"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 560, 33, 5, 4 from sigl_05_data where code='B680'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B680') as id_refanalyse, id_data, 34, 5, 4 "
                         "from sigl_07_data where libelle='CMI Norfloxacine' order by id_data desc limit 1"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 504, 35, 5, 4 from sigl_05_data where code='B680'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B680') as id_refanalyse, id_data, 36, 5, 4 "
                         "from sigl_07_data where libelle='CMI Ciprofloxacine' order by id_data desc limit 1"))

            # Link phenotype
            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "values (1000, (select id_data from sigl_05_data where code='B680'), "
                         "(select id_data from sigl_07_data where libelle='Phénotype' order by id_data desc limit 1), 37, 5, 5)"))

        except Exception as err:
            print("ERROR insert links for B680 analysis,\n\terr=" + str(err))

    # ADD new ABG analyzes B681
    try:
        conn.execute(text("insert into sigl_05_data (id_owner, code, nom, abbr, famille, cote_unite, commentaire, actif, ana_whonet) "
                     "values (1000, 'B681', 'Antibiogramme Vibrio cholerae spp. [CMI]', 'ABG Vibrio cholerae', 18, 'B', '', 4, 4)"))
    except Exception as err:
        print("ERROR insert B681 analysis,\n\terr=" + str(err))
    else:
        try:
            # Insert links for B681
            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 440, 1, 5, 4 from sigl_05_data where code='B681'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B681') as id_refanalyse, id_data, 2, 5, 4 "
                         "from sigl_07_data where libelle='CMI Amoxicilline' order by id_data desc limit 1"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 443, 3, 5, 4 from sigl_05_data where code='B681'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B681') as id_refanalyse, id_data, 4, 5, 4 "
                         "from sigl_07_data where libelle='CMI Amoxicilline/ac. Clavulanique' order by id_data desc limit 1"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 597, 5, 5, 4 from sigl_05_data where code='B681'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B681') as id_refanalyse, id_data, 6, 5, 4 "
                         "from sigl_07_data where libelle='CMI Ticarcilline' order by id_data desc limit 1"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 573, 7, 5, 4 from sigl_05_data where code='B681'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B681') as id_refanalyse, id_data, 8, 5, 4 "
                         "from sigl_07_data where libelle='CMI Pipéracilline' order by id_data desc limit 1"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 450, 9, 5, 4 from sigl_05_data where code='B681'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B681') as id_refanalyse, id_data, 10, 5, 4 "
                         "from sigl_07_data where libelle='CMI Aztréonam' order by id_data desc limit 1"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 530, 11, 5, 4 from sigl_05_data where code='B681'")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B681') as id_refanalyse, id_data, 12, 5, 4 "
                         "from sigl_07_data where libelle='CMI Imipénème' order by id_data desc limit 1")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 460, 13, 5, 4 from sigl_05_data where code='B681'")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B681') as id_refanalyse, id_data, 14, 5, 4 "
                         "from sigl_07_data where libelle='CMI Céfalotine' order by id_data desc limit 1")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 482, 15, 5, 4 from sigl_05_data where code='B681'")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B681') as id_refanalyse, id_data, 16, 5, 4 "
                         "from sigl_07_data where libelle='CMI Céfoxitine' order by id_data desc limit 1")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 496, 17, 5, 4 from sigl_05_data where code='B681'")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B681') as id_refanalyse, id_data, 18, 5, 4 "
                         "from sigl_07_data where libelle='CMI Céftriaxone' order by id_data desc limit 1")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 492, 19, 5, 4 from sigl_05_data where code='B681'")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B681') as id_refanalyse, id_data, 20, 5, 4 "
                         "from sigl_07_data where libelle='CMI Ceftazidime' order by id_data desc limit 1")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 534, 21, 5, 4 from sigl_05_data where code='B681'")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B681') as id_refanalyse, id_data, 22, 5, 4 "
                         "from sigl_07_data where libelle='CMI Kanamycine' order by id_data desc limit 1")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 603, 23, 5, 4 from sigl_05_data where code='B681'")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B681') as id_refanalyse, id_data, 24, 5, 4 "
                         "from sigl_07_data where libelle='CMI Tobramycine' order by id_data desc limit 1")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 528, 25, 5, 4 from sigl_05_data where code='B681'")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B681') as id_refanalyse, id_data, 26, 5, 4 "
                         "from sigl_07_data where libelle='CMI Gentamicine' order by id_data desc limit 1")

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 502, 27, 5, 4 from sigl_05_data where code='B681'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B681') as id_refanalyse, id_data, 28, 5, 4 "
                         "from sigl_07_data where libelle='CMI Chloramphénicol' order by id_data desc limit 1"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 508, 29, 5, 4 from sigl_05_data where code='B681'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B681') as id_refanalyse, id_data, 30, 5, 4 "
                         "from sigl_07_data where libelle='CMI Colistine' order by id_data desc limit 1"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 430, 31, 5, 4 from sigl_05_data where code='B681'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B681') as id_refanalyse, id_data, 32, 5, 4 "
                         "from sigl_07_data where libelle='CMI Acide nalidixique' order by id_data desc limit 1"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 560, 33, 5, 4 from sigl_05_data where code='B681'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B681') as id_refanalyse, id_data, 34, 5, 4 "
                         "from sigl_07_data where libelle='CMI Norfloxacine' order by id_data desc limit 1"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, id_data, 504, 35, 5, 4 from sigl_05_data where code='B681'"))

            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "select 1000, (select id_data from sigl_05_data where code='B681') as id_refanalyse, id_data, 36, 5, 4 "
                         "from sigl_07_data where libelle='CMI Ciprofloxacine' order by id_data desc limit 1"))

            # Link phenotype
            conn.execute(text("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire, var_whonet) "
                         "values (1000, (select id_data from sigl_05_data where code='B681'), "
                         "(select id_data from sigl_07_data where libelle='Phénotype' order by id_data desc limit 1), 37, 5, 5)"))

        except Exception as err:
            print("ERROR insert links for B681 analysis,\n\terr=" + str(err))

    print(str(datetime.today()) + " : END of migration v3.0.7_changes_for_dhis2_monthly revision=2660636fdaf9")


def downgrade():
    pass
