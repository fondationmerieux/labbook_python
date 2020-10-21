# -*- coding:utf-8 -*-
"""v2.9.1_add_antibiogramme_analysis

Revision ID: 75a90d6bfa9f
Revises: 73570c0407b1
Create Date: 2020-10-13 16:13:02.229354

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = '75a90d6bfa9f'
down_revision = '73570c0407b1'
branch_labels = None
depends_on = None


def upgrade():
    # Get the current
    conn = op.get_bind()

    try:
        # --- VARIABLES ---
        # insert new antibio var (others exist already in DB)
        conn.execute("insert into sigl_07_data (id_owner, libelle, type_resultat) values (1000, 'B-lactamase', 600)")

        # Insert inhibition diameter var
        conn.execute("insert into sigl_07_data (id_owner, libelle, unite, type_resultat) \
                      values (1000, 'Diam. inhibition Acide fusidique', 240, 227)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, unite, type_resultat) \
                      values (1000, 'Diam. inhibition Acide nalidixique', 240, 227)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, unite, type_resultat) \
                      values (1000, 'Diam. inhibition Amikacine', 240, 227)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, unite, type_resultat) \
                      values (1000, 'Diam. inhibition Amoxicilline', 240, 227)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, unite, type_resultat) \
                      values (1000, 'Diam. inhibition Amoxicilline/ac. Clavulanique', 240, 227)")

        conn.execute("insert into sigl_07_data (id_owner, libelle, unite, type_resultat) \
                      values (1000, 'Diam. inhibition Ampicilline', 240, 227)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, unite, type_resultat) \
                      values (1000, 'Diam. inhibition Aztréonam', 240, 227)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, unite, type_resultat) \
                      values (1000, 'Diam. inhibition B-lactamase', 240, 227)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, unite, type_resultat) \
                      values (1000, 'Diam. inhibition Céfalotine', 240, 227)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, unite, type_resultat) \
                      values (1000, 'Diam. inhibition Céfépime', 240, 227)")

        conn.execute("insert into sigl_07_data (id_owner, libelle, unite, type_resultat) \
                      values (1000, 'Diam. inhibition Céfotaxime', 240, 227)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, unite, type_resultat) \
                      values (1000, 'Diam. inhibition Céfoxitine', 240, 227)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, unite, type_resultat) \
                      values (1000, 'Diam. inhibition Cefsulodine', 240, 227)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, unite, type_resultat) \
                      values (1000, 'Diam. inhibition Ceftazidime', 240, 227)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, unite, type_resultat) \
                      values (1000, 'Diam. inhibition Céftriaxone', 240, 227)")

        conn.execute("insert into sigl_07_data (id_owner, libelle, unite, type_resultat) \
                      values (1000, 'Diam. inhibition Chloramphénicol', 240, 227)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, unite, type_resultat) \
                      values (1000, 'Diam. inhibition Ciprofloxacine', 240, 227)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, unite, type_resultat) \
                      values (1000, 'Diam. inhibition Colistine', 240, 227)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, unite, type_resultat) \
                      values (1000, 'Diam. inhibition Cotrimoxazole', 240, 227)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, unite, type_resultat) \
                      values (1000, 'Diam. inhibition Doxycycline', 240, 227)")

        conn.execute("insert into sigl_07_data (id_owner, libelle, unite, type_resultat) \
                      values (1000, 'Diam. inhibition Erythromycine', 240, 227)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, unite, type_resultat) \
                      values (1000, 'Diam. inhibition Fosfomycine', 240, 227)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, unite, type_resultat) \
                      values (1000, 'Diam. inhibition Gentamicine', 240, 227)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, unite, type_resultat) \
                      values (1000, 'Diam. inhibition Imipénème', 240, 227)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, unite, type_resultat) \
                      values (1000, 'Diam. inhibition Kanamycine', 240, 227)")

        conn.execute("insert into sigl_07_data (id_owner, libelle, unite, type_resultat) \
                      values (1000, 'Diam. inhibition Lincomycine', 240, 227)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, unite, type_resultat) \
                      values (1000, 'Diam. inhibition Oxacilline', 240, 227)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, unite, type_resultat) \
                      values (1000, 'Diam. inhibition Nétilmicine', 240, 227)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, unite, type_resultat) \
                      values (1000, 'Diam. inhibition Norfloxacine', 240, 227)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, unite, type_resultat) \
                      values (1000, 'Diam. inhibition Péfloxacine', 240, 227)")

        conn.execute("insert into sigl_07_data (id_owner, libelle, unite, type_resultat) \
                      values (1000, 'Diam. inhibition Pénicilline', 240, 227)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, unite, type_resultat) \
                      values (1000, 'Diam. inhibition Pipéracilline', 240, 227)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, unite, type_resultat) \
                      values (1000, 'Diam. inhibition Pipéracilline/tazobactam', 240, 227)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, unite, type_resultat) \
                      values (1000, 'Diam. inhibition Pristinamycine', 240, 227)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, unite, type_resultat) \
                      values (1000, 'Diam. inhibition Rifamycine', 240, 227)")

        conn.execute("insert into sigl_07_data (id_owner, libelle, unite, type_resultat) \
                      values (1000, 'Diam. inhibition Tétracycline', 240, 227)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, unite, type_resultat) \
                      values (1000, 'Diam. inhibition Ticarcilline', 240, 227)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, unite, type_resultat) \
                      values (1000, 'Diam. inhibition Ticarcilline/ac. Clavulanique', 240, 227)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, unite, type_resultat) \
                      values (1000, 'Diam. inhibition Tobramycine', 240, 227)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, unite, type_resultat) \
                      values (1000, 'Diam. inhibition Vancomycine', 240, 227)")

        # Insert CMI var
        conn.execute("insert into sigl_07_data (id_owner, libelle, type_resultat) \
                      values (1000, 'CMI Acide fusidique', 228)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, type_resultat) \
                      values (1000, 'CMI Acide nalidixique', 228)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, type_resultat) \
                      values (1000, 'CMI Amikacine', 228)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, type_resultat) \
                      values (1000, 'CMI Amoxicilline', 228)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, type_resultat) \
                      values (1000, 'CMI Amoxicilline/ac. Clavulanique', 228)")

        conn.execute("insert into sigl_07_data (id_owner, libelle, type_resultat) \
                      values (1000, 'CMI Ampicilline', 228)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, type_resultat) \
                      values (1000, 'CMI Aztréonam', 228)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, type_resultat) \
                      values (1000, 'CMI B-lactamase', 228)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, type_resultat) \
                      values (1000, 'CMI Céfalotine', 228)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, type_resultat) \
                      values (1000, 'CMI Céfépime', 228)")

        conn.execute("insert into sigl_07_data (id_owner, libelle, type_resultat) \
                      values (1000, 'CMI Céfotaxime', 228)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, type_resultat) \
                      values (1000, 'CMI Céfoxitine', 228)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, type_resultat) \
                      values (1000, 'CMI Cefsulodine', 228)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, type_resultat) \
                      values (1000, 'CMI Ceftazidime', 228)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, type_resultat) \
                      values (1000, 'CMI Céftriaxone', 228)")

        conn.execute("insert into sigl_07_data (id_owner, libelle, type_resultat) \
                      values (1000, 'CMI Chloramphénicol', 228)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, type_resultat) \
                      values (1000, 'CMI Ciprofloxacine', 228)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, type_resultat) \
                      values (1000, 'CMI Colistine', 228)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, type_resultat) \
                      values (1000, 'CMI Cotrimoxazole', 228)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, type_resultat) \
                      values (1000, 'CMI Doxycycline', 228)")

        conn.execute("insert into sigl_07_data (id_owner, libelle, type_resultat) \
                      values (1000, 'CMI Erythromycine', 228)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, type_resultat) \
                      values (1000, 'CMI Fosfomycine', 228)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, type_resultat) \
                      values (1000, 'CMI Gentamicine', 228)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, type_resultat) \
                      values (1000, 'CMI Imipénème', 228)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, type_resultat) \
                      values (1000, 'CMI Kanamycine', 228)")

        conn.execute("insert into sigl_07_data (id_owner, libelle, type_resultat) \
                      values (1000, 'CMI Lincomycine', 228)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, type_resultat) \
                      values (1000, 'CMI Oxacilline', 228)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, type_resultat) \
                      values (1000, 'CMI Nétilmicine', 228)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, type_resultat) \
                      values (1000, 'CMI Norfloxacine', 228)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, type_resultat) \
                      values (1000, 'CMI Péfloxacine', 228)")

        conn.execute("insert into sigl_07_data (id_owner, libelle, type_resultat) \
                      values (1000, 'CMI Pénicilline', 228)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, type_resultat) \
                      values (1000, 'CMI Pipéracilline', 228)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, type_resultat) \
                      values (1000, 'CMI Pipéracilline/tazobactam', 228)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, type_resultat) \
                      values (1000, 'CMI Pristinamycine', 228)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, type_resultat) \
                      values (1000, 'CMI Rifamycine', 228)")

        conn.execute("insert into sigl_07_data (id_owner, libelle, type_resultat) \
                      values (1000, 'CMI Tétracycline', 228)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, type_resultat) \
                      values (1000, 'CMI Ticarcilline', 228)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, type_resultat) \
                      values (1000, 'CMI Ticarcilline/ac. Clavulanique', 228)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, type_resultat) \
                      values (1000, 'CMI Tobramycine', 228)")
        conn.execute("insert into sigl_07_data (id_owner, libelle, type_resultat) \
                      values (1000, 'CMI Vancomycine', 228)")
    except:
        print("ERROR insert new variables for analyzes")
    else:
        try:
            conn.execute("insert into sigl_05_data (id_owner, code, nom, abbr, famille, cote_unite, commentaire, actif) \
                          values (1000, 'B650', 'Antibiogramme Méningocoques [DISK]', 'ABG Méningocoques', 18, 'B', '[WHONET]', 4)")
        except:
            print("ERROR insert B650 analysis")
        else:
            try:
                # Insert links for B650
                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 571, 1, 4 from sigl_05_data where code='B650'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B650') as id_refanalyse, id_data, 2, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Pénicilline' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 565, 3, 4 from sigl_05_data where code='B650'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B650') as id_refanalyse, id_data, 4, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Oxacilline' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 440, 5, 4 from sigl_05_data where code='B650'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B650') as id_refanalyse, id_data, 6, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Amoxicilline' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 474, 7, 4 from sigl_05_data where code='B650'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B650') as id_refanalyse, id_data, 8, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Céfotaxime' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 496, 9, 4 from sigl_05_data where code='B650'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B650') as id_refanalyse, id_data,10, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Céftriaxone' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 502, 11, 4 from sigl_05_data where code='B650'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B650') as id_refanalyse, id_data,12, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Chloramphénicol' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 504, 13, 4 from sigl_05_data where code='B650'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B650') as id_refanalyse, id_data,14, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Ciprofloxacine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 581, 15, 4 from sigl_05_data where code='B650'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B650') as id_refanalyse, id_data,16, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Rifamycine' order by id_data desc limit 1")
            except:
                print("ERROR insert links for B650 analysis")

        try:
            conn.execute("insert into sigl_05_data (id_owner, code, nom, abbr, famille, cote_unite, commentaire, actif) \
                          values (1000, 'B651', 'Antibiogramme Staphylococcus aureus [DISK]', 'ABG Staphylo. aureus', 18, 'B', '[WHONET]', 4)")
        except:
            print("ERROR insert B651 analysis")
        else:
            try:
                # Insert links for B671
                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 571, 1, 4 from sigl_05_data where code='B651'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B651') as id_refanalyse, id_data, 2, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Pénicilline' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 565, 3, 4 from sigl_05_data where code='B651'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B651') as id_refanalyse, id_data, 4, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Oxacilline' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 482, 5, 4 from sigl_05_data where code='B651'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B651') as id_refanalyse, id_data, 6, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Céfoxitine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 528, 7, 4 from sigl_05_data where code='B651'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B651') as id_refanalyse, id_data, 8, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Gentamicine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 534, 9, 4 from sigl_05_data where code='B651'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B651') as id_refanalyse, id_data,10, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Kanamycine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 603, 11, 4 from sigl_05_data where code='B651'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B651') as id_refanalyse, id_data,12, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Tobramycine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 522, 13, 4 from sigl_05_data where code='B651'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B651') as id_refanalyse, id_data,14, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Erythromycine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 539, 15, 4 from sigl_05_data where code='B651'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B651') as id_refanalyse, id_data,16, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Lincomycine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 577, 17, 4 from sigl_05_data where code='B651'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B651') as id_refanalyse, id_data,18, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Pristinamycine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 595, 19, 4 from sigl_05_data where code='B651'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B651') as id_refanalyse, id_data,20, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Tétracycline' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 569, 21, 4 from sigl_05_data where code='B651'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B651') as id_refanalyse, id_data,22, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Péfloxacine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 504, 23, 4 from sigl_05_data where code='B651'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B651') as id_refanalyse, id_data,24, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Ciprofloxacine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 609, 25, 4 from sigl_05_data where code='B651'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B651') as id_refanalyse, id_data,26, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Vancomycine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 502, 27, 4 from sigl_05_data where code='B651'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B651') as id_refanalyse, id_data,28, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Chloramphénicol' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 428, 29, 4 from sigl_05_data where code='B651'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B651') as id_refanalyse, id_data,30, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Acide fusidique' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 526, 31, 4 from sigl_05_data where code='B651'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B651') as id_refanalyse, id_data,32, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Fosfomycine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 510, 33, 4 from sigl_05_data where code='B651'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B651') as id_refanalyse, id_data,34, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Cotrimoxazole' order by id_data desc limit 1")
            except:
                print("ERROR insert links for B651 analysis")

        try:
            conn.execute("insert into sigl_05_data (id_owner, code, nom, abbr, famille, cote_unite, commentaire, actif) \
                          values (1000, 'B652', 'Antibiogramme Pneumocoques [DISK]', 'ABG Pneumocoques', 18, 'B', '[WHONET]', 4)")
        except:
            print("ERROR insert B652 analysis")
        else:
            try:
                # Insert links for B652
                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 571, 1, 4 from sigl_05_data where code='B652'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B652') as id_refanalyse, id_data, 2, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Pénicilline' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 565, 3, 4 from sigl_05_data where code='B652'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B652') as id_refanalyse, id_data, 4, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Oxacilline' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 440, 5, 4 from sigl_05_data where code='B652'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B652') as id_refanalyse, id_data, 6, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Amoxicilline' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 474, 7, 4 from sigl_05_data where code='B652'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B652') as id_refanalyse, id_data, 8, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Céfotaxime' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 528, 9, 4 from sigl_05_data where code='B652'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B652') as id_refanalyse, id_data,10, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Gentamicine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 534, 11, 4 from sigl_05_data where code='B652'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B652') as id_refanalyse, id_data,12, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Kanamycine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 595, 13, 4 from sigl_05_data where code='B652'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B652') as id_refanalyse, id_data,14, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Tétracycline' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 522, 15, 4 from sigl_05_data where code='B652'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B652') as id_refanalyse, id_data,16, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Erythromycine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 539, 17, 4 from sigl_05_data where code='B652'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B652') as id_refanalyse, id_data,18, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Lincomycine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 577, 19, 4 from sigl_05_data where code='B652'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B652') as id_refanalyse, id_data,20, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Pristinamycine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 560, 21, 4 from sigl_05_data where code='B652'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B652') as id_refanalyse, id_data,22, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Norfloxacine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 502, 23, 4 from sigl_05_data where code='B652'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B652') as id_refanalyse, id_data,24, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Chloramphénicol' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 609, 25, 4 from sigl_05_data where code='B652'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B652') as id_refanalyse, id_data,26, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Vancomycine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 526, 27, 4 from sigl_05_data where code='B652'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B652') as id_refanalyse, id_data,28, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Fosfomycine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 510, 29, 4 from sigl_05_data where code='B652'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B652') as id_refanalyse, id_data,30, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Cotrimoxazole' order by id_data desc limit 1")
            except:
                print("ERROR insert links for B652 analysis")

        try:
            conn.execute("insert into sigl_05_data (id_owner, code, nom, abbr, famille, cote_unite, commentaire, actif) \
                          values (1000, 'B653', 'Antibiogramme Haemophilus influenzae [DISK]', 'ABG H. influenzae', 18, 'B', '[WHONET]', 4)")
        except:
            print("ERROR insert B653 analysis")
        else:
            try:
                # Insert links for B653
                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 445, 1, 4 from sigl_05_data where code='B653'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B653') as id_refanalyse, id_data, 2, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Ampicilline' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 443, 3, 4 from sigl_05_data where code='B653'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B653') as id_refanalyse, id_data, 4, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Amoxicilline/ac. Clavulanique' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 460, 5, 4 from sigl_05_data where code='B653'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B653') as id_refanalyse, id_data, 6, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Céfalotine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 496, 7, 4 from sigl_05_data where code='B653'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B653') as id_refanalyse, id_data, 8, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Céftriaxone' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 595, 9, 4 from sigl_05_data where code='B653'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B653') as id_refanalyse, id_data,10, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Tétracycline' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 502, 11, 4 from sigl_05_data where code='B653'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B653') as id_refanalyse, id_data,12, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Chloramphénicol' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 504, 13, 4 from sigl_05_data where code='B653'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B653') as id_refanalyse, id_data,14, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Ciprofloxacine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 528, 15, 4 from sigl_05_data where code='B653'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B653') as id_refanalyse, id_data,16, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Gentamicine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 534, 17, 4 from sigl_05_data where code='B653'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B653') as id_refanalyse, id_data,18, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Kanamycine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, (select id_data from sigl_07_data where libelle='B-lactamase' limit 1) as id_refanalyse, 19, 4 \
                              from sigl_05_data where code='B653'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B653') as id_refanalyse, id_data,20, 4 \
                              from sigl_07_data where libelle='Diam. inhibition B-lactamase' order by id_data desc limit 1")
            except:
                print("ERROR insert links for B653 analysis")

        try:
            conn.execute("insert into sigl_05_data (id_owner, code, nom, abbr, famille, cote_unite, commentaire, actif) \
                          values (1000, 'B654', 'Antibiogramme Pseudomonas [DISK]', 'ABG Pseudomonas', 18, 'B', '[WHONET]', 4)")
        except:
            print("ERROR insert B654 analysis")
        else:
            try:
                # Insert links for B654
                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 597, 1, 4 from sigl_05_data where code='B654'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B654') as id_refanalyse, id_data, 2, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Ticarcilline' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 599, 3, 4 from sigl_05_data where code='B654'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B654') as id_refanalyse, id_data, 4, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Ticarcilline/ac. Clavulanique' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 573, 5, 4 from sigl_05_data where code='B654'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B654') as id_refanalyse, id_data, 6, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Pipéracilline' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 450, 7, 4 from sigl_05_data where code='B654'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B654') as id_refanalyse, id_data, 8, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Aztréonam' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 490, 9, 4 from sigl_05_data where code='B654'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B654') as id_refanalyse, id_data,10, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Cefsulodine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 492, 11, 4 from sigl_05_data where code='B654'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B654') as id_refanalyse, id_data,12, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Ceftazidime' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 530, 13, 4 from sigl_05_data where code='B654'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B654') as id_refanalyse, id_data,14, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Imipénème' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 528, 15, 4 from sigl_05_data where code='B654'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B654') as id_refanalyse, id_data,16, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Gentamicine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 534, 17, 4 from sigl_05_data where code='B654'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B654') as id_refanalyse, id_data,18, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Kanamycine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 603, 19, 4 from sigl_05_data where code='B654'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B654') as id_refanalyse, id_data,20, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Tobramycine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 438, 21, 4 from sigl_05_data where code='B654'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B654') as id_refanalyse, id_data,22, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Amikacine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 556, 23, 4 from sigl_05_data where code='B654'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B654') as id_refanalyse, id_data,24, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Nétilmicine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 508, 25, 4 from sigl_05_data where code='B654'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B654') as id_refanalyse, id_data,26, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Colistine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 502, 27, 4 from sigl_05_data where code='B654'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B654') as id_refanalyse, id_data,28, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Chloramphénicol' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 569, 29, 4 from sigl_05_data where code='B654'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B654') as id_refanalyse, id_data,30, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Péfloxacine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 504, 31, 4 from sigl_05_data where code='B654'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B654') as id_refanalyse, id_data,32, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Ciprofloxacine' order by id_data desc limit 1")
            except:
                print("ERROR insert links for B654 analysis")

        try:
            conn.execute("insert into sigl_05_data (id_owner, code, nom, abbr, famille, cote_unite, commentaire, actif) \
                          values (1000, 'B655', 'Antibiogramme Acinetobacter [DISK]', 'ABG Acinetobacter', 18, 'B', '[WHONET]', 4)")
        except:
            print("ERROR insert B655 analysis")
        else:
            try:
                # Insert links for B655
                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 597, 1, 4 from sigl_05_data where code='B655'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B655') as id_refanalyse, id_data, 2, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Ticarcilline' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 599, 3, 4 from sigl_05_data where code='B655'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B655') as id_refanalyse, id_data, 4, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Ticarcilline/ac. Clavulanique' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 573, 5, 4 from sigl_05_data where code='B655'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B655') as id_refanalyse, id_data, 6, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Pipéracilline' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 575, 7, 4 from sigl_05_data where code='B655'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B655') as id_refanalyse, id_data, 8, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Pipéracilline/tazobactam' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 492, 9, 4 from sigl_05_data where code='B655'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B655') as id_refanalyse, id_data,10, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Ceftazidime' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 468, 11, 4 from sigl_05_data where code='B655'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B655') as id_refanalyse, id_data,12, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Céfépime' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 530, 13, 4 from sigl_05_data where code='B655'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B655') as id_refanalyse, id_data,14, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Imipénème' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 528, 15, 4 from sigl_05_data where code='B655'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B655') as id_refanalyse, id_data,16, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Gentamicine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 534, 17, 4 from sigl_05_data where code='B655'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B655') as id_refanalyse, id_data,18, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Kanamycine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 556, 19, 4 from sigl_05_data where code='B655'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B655') as id_refanalyse, id_data,20, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Nétilmicine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 438, 21, 4 from sigl_05_data where code='B655'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B655') as id_refanalyse, id_data,22, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Amikacine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 502, 23, 4 from sigl_05_data where code='B655'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B655') as id_refanalyse, id_data,24, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Chloramphénicol' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 595, 25, 4 from sigl_05_data where code='B655'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B655') as id_refanalyse, id_data,26, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Tétracycline' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 508, 27, 4 from sigl_05_data where code='B655'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B655') as id_refanalyse, id_data,28, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Colistine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 510, 29, 4 from sigl_05_data where code='B655'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B655') as id_refanalyse, id_data,30, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Cotrimoxazole' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 504, 31, 4 from sigl_05_data where code='B655'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B655') as id_refanalyse, id_data,32, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Ciprofloxacine' order by id_data desc limit 1")
            except:
                print("ERROR insert links for B655 analysis")

        try:
            conn.execute("insert into sigl_05_data (id_owner, code, nom, abbr, famille, cote_unite, commentaire, actif) \
                          values (1000, 'B656', 'Antibiogramme Escherichia coli [DISK]', 'ABG Escherichia coli', 18, 'B', '[WHONET]', 4)")
        except:
            print("ERROR insert B656 analysis")
        else:
            try:
                # Insert links for B656
                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 440, 1, 4 from sigl_05_data where code='B656'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B656') as id_refanalyse, id_data, 2, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Amoxicilline' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 443, 3, 4 from sigl_05_data where code='B656'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B656') as id_refanalyse, id_data, 4, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Amoxicilline/ac. Clavulanique' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 597, 5, 4 from sigl_05_data where code='B656'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B656') as id_refanalyse, id_data, 6, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Ticarcilline' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 573, 7, 4 from sigl_05_data where code='B656'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B656') as id_refanalyse, id_data, 8, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Pipéracilline' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 450, 9, 4 from sigl_05_data where code='B656'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B656') as id_refanalyse, id_data,10, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Aztréonam' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 530, 11, 4 from sigl_05_data where code='B656'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B656') as id_refanalyse, id_data,12, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Imipénème' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 460, 13, 4 from sigl_05_data where code='B656'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B656') as id_refanalyse, id_data,14, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Céfalotine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 482, 15, 4 from sigl_05_data where code='B656'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B656') as id_refanalyse, id_data,16, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Céfoxitine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 496, 17, 4 from sigl_05_data where code='B656'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B656') as id_refanalyse, id_data,18, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Céftriaxone' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 492, 19, 4 from sigl_05_data where code='B656'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B656') as id_refanalyse, id_data,20, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Ceftazidime' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 534, 21, 4 from sigl_05_data where code='B656'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B656') as id_refanalyse, id_data,22, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Kanamycine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 603, 23, 4 from sigl_05_data where code='B656'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B656') as id_refanalyse, id_data,24, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Tobramycine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 528, 25, 4 from sigl_05_data where code='B656'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B656') as id_refanalyse, id_data,26, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Gentamicine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 502, 27, 4 from sigl_05_data where code='B656'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B656') as id_refanalyse, id_data,28, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Chloramphénicol' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 508, 29, 4 from sigl_05_data where code='B656'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B656') as id_refanalyse, id_data,30, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Colistine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 430, 31, 4 from sigl_05_data where code='B656'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B656') as id_refanalyse, id_data,32, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Acide nalidixique' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 560, 33, 4 from sigl_05_data where code='B656'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B656') as id_refanalyse, id_data,34, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Norfloxacine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 504, 35, 4 from sigl_05_data where code='B656'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B656') as id_refanalyse, id_data,36, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Ciprofloxacine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 595, 37, 4 from sigl_05_data where code='B656'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B656') as id_refanalyse, id_data,38, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Tétracycline' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 516, 39, 4 from sigl_05_data where code='B656'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B656') as id_refanalyse, id_data,40, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Doxycycline' order by id_data desc limit 1")
            except:
                print("ERROR insert links for B656 analysis")

        try:
            conn.execute("insert into sigl_05_data (id_owner, code, nom, abbr, famille, cote_unite, commentaire, actif) \
                          values (1000, 'B657', 'Antibiogramme Salmonella spp [DISK]', 'ABG Salmonella spp', 18, 'B', '[WHONET]', 4)")
        except:
            print("ERROR insert B657 analysis")
        else:
            try:
                # Insert links for B657
                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 440, 1, 4 from sigl_05_data where code='B657'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B657') as id_refanalyse, id_data, 2, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Amoxicilline' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 443, 3, 4 from sigl_05_data where code='B657'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B657') as id_refanalyse, id_data, 4, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Amoxicilline/ac. Clavulanique' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 597, 5, 4 from sigl_05_data where code='B657'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B657') as id_refanalyse, id_data, 6, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Ticarcilline' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 573, 7, 4 from sigl_05_data where code='B657'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B657') as id_refanalyse, id_data, 8, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Pipéracilline' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 450, 9, 4 from sigl_05_data where code='B657'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B657') as id_refanalyse, id_data,10, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Aztréonam' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 530, 11, 4 from sigl_05_data where code='B657'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B657') as id_refanalyse, id_data,12, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Imipénème' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 460, 13, 4 from sigl_05_data where code='B657'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B657') as id_refanalyse, id_data,14, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Céfalotine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 482, 15, 4 from sigl_05_data where code='B657'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B657') as id_refanalyse, id_data,16, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Céfoxitine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 496, 17, 4 from sigl_05_data where code='B657'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B657') as id_refanalyse, id_data,18, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Céftriaxone' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 492, 19, 4 from sigl_05_data where code='B657'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B657') as id_refanalyse, id_data,20, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Ceftazidime' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 534, 21, 4 from sigl_05_data where code='B657'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B657') as id_refanalyse, id_data,22, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Kanamycine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 603, 23, 4 from sigl_05_data where code='B657'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B657') as id_refanalyse, id_data,24, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Tobramycine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 528, 25, 4 from sigl_05_data where code='B657'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B657') as id_refanalyse, id_data,26, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Gentamicine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 502, 27, 4 from sigl_05_data where code='B657'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B657') as id_refanalyse, id_data,28, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Chloramphénicol' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 508, 29, 4 from sigl_05_data where code='B657'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B657') as id_refanalyse, id_data,30, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Colistine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 430, 31, 4 from sigl_05_data where code='B657'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B657') as id_refanalyse, id_data,32, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Acide nalidixique' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 560, 33, 4 from sigl_05_data where code='B657'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B657') as id_refanalyse, id_data,34, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Norfloxacine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 504, 35, 4 from sigl_05_data where code='B657'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B657') as id_refanalyse, id_data,36, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Ciprofloxacine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 595, 37, 4 from sigl_05_data where code='B657'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B657') as id_refanalyse, id_data,38, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Tétracycline' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 516, 39, 4 from sigl_05_data where code='B657'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B657') as id_refanalyse, id_data,40, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Doxycycline' order by id_data desc limit 1")
            except:
                print("ERROR insert links for B657 analysis")

        try:
            conn.execute("insert into sigl_05_data (id_owner, code, nom, abbr, famille, cote_unite, commentaire, actif) \
                          values (1000, 'B658', 'Antibiogramme Shigella spp [DISK]', 'ABG Shigella spp', 18, 'B', '[WHONET]', 4)")
        except:
            print("ERROR insert B658 analysis")
        else:
            try:
                # Insert links for B658
                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 440, 1, 4 from sigl_05_data where code='B658'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B658') as id_refanalyse, id_data, 2, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Amoxicilline' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 443, 3, 4 from sigl_05_data where code='B658'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B658') as id_refanalyse, id_data, 4, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Amoxicilline/ac. Clavulanique' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 597, 5, 4 from sigl_05_data where code='B658'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B658') as id_refanalyse, id_data, 6, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Ticarcilline' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 573, 7, 4 from sigl_05_data where code='B658'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B658') as id_refanalyse, id_data, 8, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Pipéracilline' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 450, 9, 4 from sigl_05_data where code='B658'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B658') as id_refanalyse, id_data,10, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Aztréonam' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 530, 11, 4 from sigl_05_data where code='B658'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B658') as id_refanalyse, id_data,12, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Imipénème' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 460, 13, 4 from sigl_05_data where code='B658'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B658') as id_refanalyse, id_data,14, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Céfalotine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 482, 15, 4 from sigl_05_data where code='B658'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B658') as id_refanalyse, id_data,16, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Céfoxitine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 496, 17, 4 from sigl_05_data where code='B658'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B658') as id_refanalyse, id_data,18, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Céftriaxone' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 492, 19, 4 from sigl_05_data where code='B658'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B658') as id_refanalyse, id_data,20, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Ceftazidime' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 534, 21, 4 from sigl_05_data where code='B658'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B658') as id_refanalyse, id_data,22, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Kanamycine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 603, 23, 4 from sigl_05_data where code='B658'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B658') as id_refanalyse, id_data,24, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Tobramycine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 528, 25, 4 from sigl_05_data where code='B658'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B658') as id_refanalyse, id_data,26, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Gentamicine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 502, 27, 4 from sigl_05_data where code='B658'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B658') as id_refanalyse, id_data,28, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Chloramphénicol' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 508, 29, 4 from sigl_05_data where code='B658'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B658') as id_refanalyse, id_data,30, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Colistine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 430, 31, 4 from sigl_05_data where code='B658'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B658') as id_refanalyse, id_data,32, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Acide nalidixique' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 560, 33, 4 from sigl_05_data where code='B658'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B658') as id_refanalyse, id_data,34, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Norfloxacine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 504, 35, 4 from sigl_05_data where code='B658'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B658') as id_refanalyse, id_data,36, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Ciprofloxacine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 595, 37, 4 from sigl_05_data where code='B658'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B658') as id_refanalyse, id_data,38, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Tétracycline' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 516, 39, 4 from sigl_05_data where code='B658'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B658') as id_refanalyse, id_data,40, 4 \
                              from sigl_07_data where libelle='Diam. inhibition Doxycycline' order by id_data desc limit 1")
            except:
                print("ERROR insert links for B658 analysis")

        # Insert Antibiogramme [CMI]
        try:
            conn.execute("insert into sigl_05_data (id_owner, code, nom, abbr, famille, cote_unite, commentaire, actif) \
                          values (1000, 'B670', 'Antibiogramme Méningocoques [CMI]', 'ABG Méningocoques', 18, 'B', '[WHONET]', 4)")
        except:
            print("ERROR insert B670 analysis")
        else:
            try:
                # Insert links for B670
                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 571, 1, 4 from sigl_05_data where code='B670'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B670') as id_refanalyse, id_data, 2, 4 \
                              from sigl_07_data where libelle='CMI Pénicilline' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 565, 3, 4 from sigl_05_data where code='B670'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B670') as id_refanalyse, id_data, 4, 4 \
                              from sigl_07_data where libelle='CMI Oxacilline' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 440, 5, 4 from sigl_05_data where code='B670'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B670') as id_refanalyse, id_data, 6, 4 \
                              from sigl_07_data where libelle='CMI Amoxicilline' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 474, 7, 4 from sigl_05_data where code='B670'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B670') as id_refanalyse, id_data, 8, 4 \
                              from sigl_07_data where libelle='CMI Céfotaxime' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 496, 9, 4 from sigl_05_data where code='B670'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B670') as id_refanalyse, id_data,10, 4 \
                              from sigl_07_data where libelle='CMI Céftriaxone' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 502, 11, 4 from sigl_05_data where code='B670'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B670') as id_refanalyse, id_data,12, 4 \
                              from sigl_07_data where libelle='CMI Chloramphénicol' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 504, 13, 4 from sigl_05_data where code='B670'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B670') as id_refanalyse, id_data,14, 4 \
                              from sigl_07_data where libelle='CMI Ciprofloxacine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 581, 15, 4 from sigl_05_data where code='B670'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B670') as id_refanalyse, id_data,16, 4 \
                              from sigl_07_data where libelle='CMI Rifamycine' order by id_data desc limit 1")
            except:
                print("ERROR insert links for B670 analysis")

        try:
            conn.execute("insert into sigl_05_data (id_owner, code, nom, abbr, famille, cote_unite, commentaire, actif) \
                          values (1000, 'B671', 'Antibiogramme Staphylococcus aureus [CMI]', 'ABG Staphylo. aureus', 18, 'B', '[WHONET]', 4)")
        except:
            print("ERROR insert B671 analysis")
        else:
            try:
                # Insert links for B671
                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 571, 1, 4 from sigl_05_data where code='B671'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B671') as id_refanalyse, id_data, 2, 4 \
                              from sigl_07_data where libelle='CMI Pénicilline' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 565, 3, 4 from sigl_05_data where code='B671'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B671') as id_refanalyse, id_data, 4, 4 \
                              from sigl_07_data where libelle='CMI Oxacilline' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 482, 5, 4 from sigl_05_data where code='B671'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B671') as id_refanalyse, id_data, 6, 4 \
                              from sigl_07_data where libelle='CMI Céfoxitine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 528, 7, 4 from sigl_05_data where code='B671'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B671') as id_refanalyse, id_data, 8, 4 \
                              from sigl_07_data where libelle='CMI Gentamicine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 534, 9, 4 from sigl_05_data where code='B671'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B671') as id_refanalyse, id_data,10, 4 \
                              from sigl_07_data where libelle='CMI Kanamycine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 603, 11, 4 from sigl_05_data where code='B671'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B671') as id_refanalyse, id_data,12, 4 \
                              from sigl_07_data where libelle='CMI Tobramycine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 522, 13, 4 from sigl_05_data where code='B671'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B671') as id_refanalyse, id_data,14, 4 \
                              from sigl_07_data where libelle='CMI Erythromycine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 539, 15, 4 from sigl_05_data where code='B671'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B671') as id_refanalyse, id_data,16, 4 \
                              from sigl_07_data where libelle='CMI Lincomycine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 577, 17, 4 from sigl_05_data where code='B671'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B671') as id_refanalyse, id_data,18, 4 \
                              from sigl_07_data where libelle='CMI Pristinamycine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 595, 19, 4 from sigl_05_data where code='B671'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B671') as id_refanalyse, id_data,20, 4 \
                              from sigl_07_data where libelle='CMI Tétracycline' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 569, 21, 4 from sigl_05_data where code='B671'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B671') as id_refanalyse, id_data,22, 4 \
                              from sigl_07_data where libelle='CMI Péfloxacine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 504, 23, 4 from sigl_05_data where code='B671'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B671') as id_refanalyse, id_data,24, 4 \
                              from sigl_07_data where libelle='CMI Ciprofloxacine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 609, 25, 4 from sigl_05_data where code='B671'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B671') as id_refanalyse, id_data,26, 4 \
                              from sigl_07_data where libelle='CMI Vancomycine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 502, 27, 4 from sigl_05_data where code='B671'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B671') as id_refanalyse, id_data,28, 4 \
                              from sigl_07_data where libelle='CMI Chloramphénicol' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 428, 29, 4 from sigl_05_data where code='B671'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B671') as id_refanalyse, id_data,30, 4 \
                              from sigl_07_data where libelle='CMI Acide fusidique' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 526, 31, 4 from sigl_05_data where code='B671'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B671') as id_refanalyse, id_data,32, 4 \
                              from sigl_07_data where libelle='CMI Fosfomycine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 510, 33, 4 from sigl_05_data where code='B671'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B671') as id_refanalyse, id_data,34, 4 \
                              from sigl_07_data where libelle='CMI Cotrimoxazole' order by id_data desc limit 1")
            except:
                print("ERROR insert links for B671 analysis")

        try:
            conn.execute("insert into sigl_05_data (id_owner, code, nom, abbr, famille, cote_unite, commentaire, actif) \
                          values (1000, 'B672', 'Antibiogramme Pneumocoques [CMI]', 'ABG Pneumocoques', 18, 'B', '[WHONET]', 4)")
        except:
            print("ERROR insert B672 analysis")
        else:
            try:
                # Insert links for B672
                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 571, 1, 4 from sigl_05_data where code='B672'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B672') as id_refanalyse, id_data, 2, 4 \
                              from sigl_07_data where libelle='CMI Pénicilline' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 565, 3, 4 from sigl_05_data where code='B672'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B672') as id_refanalyse, id_data, 4, 4 \
                              from sigl_07_data where libelle='CMI Oxacilline' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 440, 5, 4 from sigl_05_data where code='B672'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B672') as id_refanalyse, id_data, 6, 4 \
                              from sigl_07_data where libelle='CMI Amoxicilline' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 474, 7, 4 from sigl_05_data where code='B672'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B672') as id_refanalyse, id_data, 8, 4 \
                              from sigl_07_data where libelle='CMI Céfotaxime' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 528, 9, 4 from sigl_05_data where code='B672'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B672') as id_refanalyse, id_data,10, 4 \
                              from sigl_07_data where libelle='CMI Gentamicine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 534, 11, 4 from sigl_05_data where code='B672'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B672') as id_refanalyse, id_data,12, 4 \
                              from sigl_07_data where libelle='CMI Kanamycine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 595, 13, 4 from sigl_05_data where code='B672'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B672') as id_refanalyse, id_data,14, 4 \
                              from sigl_07_data where libelle='CMI Tétracycline' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 522, 15, 4 from sigl_05_data where code='B672'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B672') as id_refanalyse, id_data,16, 4 \
                              from sigl_07_data where libelle='CMI Erythromycine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 539, 17, 4 from sigl_05_data where code='B672'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B672') as id_refanalyse, id_data,18, 4 \
                              from sigl_07_data where libelle='CMI Lincomycine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 577, 19, 4 from sigl_05_data where code='B672'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B672') as id_refanalyse, id_data,20, 4 \
                              from sigl_07_data where libelle='CMI Pristinamycine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 560, 21, 4 from sigl_05_data where code='B672'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B672') as id_refanalyse, id_data,22, 4 \
                              from sigl_07_data where libelle='CMI Norfloxacine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 502, 23, 4 from sigl_05_data where code='B672'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B672') as id_refanalyse, id_data,24, 4 \
                              from sigl_07_data where libelle='CMI Chloramphénicol' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 609, 25, 4 from sigl_05_data where code='B672'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B672') as id_refanalyse, id_data,26, 4 \
                              from sigl_07_data where libelle='CMI Vancomycine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 526, 27, 4 from sigl_05_data where code='B672'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B672') as id_refanalyse, id_data,28, 4 \
                              from sigl_07_data where libelle='CMI Fosfomycine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 510, 29, 4 from sigl_05_data where code='B672'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B672') as id_refanalyse, id_data,30, 4 \
                              from sigl_07_data where libelle='CMI Cotrimoxazole' order by id_data desc limit 1")
            except:
                print("ERROR insert links for B672 analysis")

        try:
            conn.execute("insert into sigl_05_data (id_owner, code, nom, abbr, famille, cote_unite, commentaire, actif) \
                          values (1000, 'B673', 'Antibiogramme Haemophilus influenzae [CMI]', 'ABG H. influenzae', 18, 'B', '[WHONET]', 4)")
        except:
            print("ERROR insert B673 analysis")
        else:
            try:
                # Insert links for B673
                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 445, 1, 4 from sigl_05_data where code='B673'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B673') as id_refanalyse, id_data, 2, 4 \
                              from sigl_07_data where libelle='CMI Ampicilline' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 443, 3, 4 from sigl_05_data where code='B673'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B673') as id_refanalyse, id_data, 4, 4 \
                              from sigl_07_data where libelle='CMI Amoxicilline/ac. Clavulanique' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 460, 5, 4 from sigl_05_data where code='B673'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B673') as id_refanalyse, id_data, 6, 4 \
                              from sigl_07_data where libelle='CMI Céfalotine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 496, 7, 4 from sigl_05_data where code='B673'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B673') as id_refanalyse, id_data, 8, 4 \
                              from sigl_07_data where libelle='CMI Céftriaxone' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 595, 9, 4 from sigl_05_data where code='B673'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B673') as id_refanalyse, id_data,10, 4 \
                              from sigl_07_data where libelle='CMI Tétracycline' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 502, 11, 4 from sigl_05_data where code='B673'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B673') as id_refanalyse, id_data,12, 4 \
                              from sigl_07_data where libelle='CMI Chloramphénicol' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 504, 13, 4 from sigl_05_data where code='B673'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B673') as id_refanalyse, id_data,14, 4 \
                              from sigl_07_data where libelle='CMI Ciprofloxacine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 528, 15, 4 from sigl_05_data where code='B673'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B673') as id_refanalyse, id_data,16, 4 \
                              from sigl_07_data where libelle='CMI Gentamicine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 534, 17, 4 from sigl_05_data where code='B673'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B673') as id_refanalyse, id_data,18, 4 \
                              from sigl_07_data where libelle='CMI Kanamycine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, (select id_data from sigl_07_data where libelle='B-lactamase' limit 1) as id_refanalyse, 19, 4 \
                              from sigl_05_data where code='B673'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B673') as id_refanalyse, id_data,20, 4 \
                              from sigl_07_data where libelle='CMI B-lactamase' order by id_data desc limit 1")
            except:
                print("ERROR insert links for B673 analysis")

        try:
            conn.execute("insert into sigl_05_data (id_owner, code, nom, abbr, famille, cote_unite, commentaire, actif) \
                          values (1000, 'B674', 'Antibiogramme Pseudomonas [CMI]', 'ABG Pseudomonas', 18, 'B', '[WHONET]', 4)")
        except:
            print("ERROR insert B674 analysis")
        else:
            try:
                # Insert links for B674
                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 597, 1, 4 from sigl_05_data where code='B674'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B674') as id_refanalyse, id_data, 2, 4 \
                              from sigl_07_data where libelle='CMI Ticarcilline' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 599, 3, 4 from sigl_05_data where code='B674'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B674') as id_refanalyse, id_data, 4, 4 \
                              from sigl_07_data where libelle='CMI Ticarcilline/ac. Clavulanique' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 573, 5, 4 from sigl_05_data where code='B674'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B674') as id_refanalyse, id_data, 6, 4 \
                              from sigl_07_data where libelle='CMI Pipéracilline' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 450, 7, 4 from sigl_05_data where code='B674'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B674') as id_refanalyse, id_data, 8, 4 \
                              from sigl_07_data where libelle='CMI Aztréonam' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 490, 9, 4 from sigl_05_data where code='B674'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B674') as id_refanalyse, id_data,10, 4 \
                              from sigl_07_data where libelle='CMI Cefsulodine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 492, 11, 4 from sigl_05_data where code='B674'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B674') as id_refanalyse, id_data,12, 4 \
                              from sigl_07_data where libelle='CMI Ceftazidime' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 530, 13, 4 from sigl_05_data where code='B674'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B674') as id_refanalyse, id_data,14, 4 \
                              from sigl_07_data where libelle='CMI Imipénème' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 528, 15, 4 from sigl_05_data where code='B674'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B674') as id_refanalyse, id_data,16, 4 \
                              from sigl_07_data where libelle='CMI Gentamicine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 534, 17, 4 from sigl_05_data where code='B674'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B674') as id_refanalyse, id_data,18, 4 \
                              from sigl_07_data where libelle='CMI Kanamycine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 603, 19, 4 from sigl_05_data where code='B674'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B674') as id_refanalyse, id_data,20, 4 \
                              from sigl_07_data where libelle='CMI Tobramycine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 438, 21, 4 from sigl_05_data where code='B674'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B674') as id_refanalyse, id_data,22, 4 \
                              from sigl_07_data where libelle='CMI Amikacine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 556, 23, 4 from sigl_05_data where code='B674'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B674') as id_refanalyse, id_data,24, 4 \
                              from sigl_07_data where libelle='CMI Nétilmicine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 508, 25, 4 from sigl_05_data where code='B674'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B674') as id_refanalyse, id_data,26, 4 \
                              from sigl_07_data where libelle='CMI Colistine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 502, 27, 4 from sigl_05_data where code='B674'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B674') as id_refanalyse, id_data,28, 4 \
                              from sigl_07_data where libelle='CMI Chloramphénicol' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 569, 29, 4 from sigl_05_data where code='B674'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B674') as id_refanalyse, id_data,30, 4 \
                              from sigl_07_data where libelle='CMI Péfloxacine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 504, 31, 4 from sigl_05_data where code='B674'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B674') as id_refanalyse, id_data,32, 4 \
                              from sigl_07_data where libelle='CMI Ciprofloxacine' order by id_data desc limit 1")
            except:
                print("ERROR insert links for B674 analysis")

        try:
            conn.execute("insert into sigl_05_data (id_owner, code, nom, abbr, famille, cote_unite, commentaire, actif) \
                          values (1000, 'B675', 'Antibiogramme Acinetobacter [CMI]', 'ABG Acinetobacter', 18, 'B', '[WHONET]', 4)")
        except:
            print("ERROR insert B675 analysis")
        else:
            try:
                # Insert links for B675
                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 597, 1, 4 from sigl_05_data where code='B675'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B675') as id_refanalyse, id_data, 2, 4 \
                              from sigl_07_data where libelle='CMI Ticarcilline' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 599, 3, 4 from sigl_05_data where code='B675'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B675') as id_refanalyse, id_data, 4, 4 \
                              from sigl_07_data where libelle='CMI Ticarcilline/ac. Clavulanique' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 573, 5, 4 from sigl_05_data where code='B675'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B675') as id_refanalyse, id_data, 6, 4 \
                              from sigl_07_data where libelle='CMI Pipéracilline' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 575, 7, 4 from sigl_05_data where code='B675'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B675') as id_refanalyse, id_data, 8, 4 \
                              from sigl_07_data where libelle='CMI Pipéracilline/tazobactam' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 492, 9, 4 from sigl_05_data where code='B675'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B675') as id_refanalyse, id_data,10, 4 \
                              from sigl_07_data where libelle='CMI Ceftazidime' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 468, 11, 4 from sigl_05_data where code='B675'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B675') as id_refanalyse, id_data,12, 4 \
                              from sigl_07_data where libelle='CMI Céfépime' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 530, 13, 4 from sigl_05_data where code='B675'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B675') as id_refanalyse, id_data,14, 4 \
                              from sigl_07_data where libelle='CMI Imipénème' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 528, 15, 4 from sigl_05_data where code='B675'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B675') as id_refanalyse, id_data,16, 4 \
                              from sigl_07_data where libelle='CMI Gentamicine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 534, 17, 4 from sigl_05_data where code='B675'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B675') as id_refanalyse, id_data,18, 4 \
                              from sigl_07_data where libelle='CMI Kanamycine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 556, 19, 4 from sigl_05_data where code='B675'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B675') as id_refanalyse, id_data,20, 4 \
                              from sigl_07_data where libelle='CMI Nétilmicine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 438, 21, 4 from sigl_05_data where code='B675'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B675') as id_refanalyse, id_data,22, 4 \
                              from sigl_07_data where libelle='CMI Amikacine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 502, 23, 4 from sigl_05_data where code='B675'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B675') as id_refanalyse, id_data,24, 4 \
                              from sigl_07_data where libelle='CMI Chloramphénicol' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 595, 25, 4 from sigl_05_data where code='B675'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B675') as id_refanalyse, id_data,26, 4 \
                              from sigl_07_data where libelle='CMI Tétracycline' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 508, 27, 4 from sigl_05_data where code='B675'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B675') as id_refanalyse, id_data,28, 4 \
                              from sigl_07_data where libelle='CMI Colistine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 510, 29, 4 from sigl_05_data where code='B675'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B675') as id_refanalyse, id_data,30, 4 \
                              from sigl_07_data where libelle='CMI Cotrimoxazole' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 504, 31, 4 from sigl_05_data where code='B675'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B675') as id_refanalyse, id_data,32, 4 \
                              from sigl_07_data where libelle='CMI Ciprofloxacine' order by id_data desc limit 1")
            except:
                print("ERROR insert links for B675 analysis")

        try:
            conn.execute("insert into sigl_05_data (id_owner, code, nom, abbr, famille, cote_unite, commentaire, actif) \
                          values (1000, 'B676', 'Antibiogramme Escherichia coli [CMI]', 'ABG Escherichia coli', 18, 'B', '[WHONET]', 4)")
        except:
            print("ERROR insert B676 analysis")
        else:
            try:
                # Insert links for B676
                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 440, 1, 4 from sigl_05_data where code='B676'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B676') as id_refanalyse, id_data, 2, 4 \
                              from sigl_07_data where libelle='CMI Amoxicilline' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 443, 3, 4 from sigl_05_data where code='B676'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B676') as id_refanalyse, id_data, 4, 4 \
                              from sigl_07_data where libelle='CMI Amoxicilline/ac. Clavulanique' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 597, 5, 4 from sigl_05_data where code='B676'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B676') as id_refanalyse, id_data, 6, 4 \
                              from sigl_07_data where libelle='CMI Ticarcilline' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 573, 7, 4 from sigl_05_data where code='B676'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B676') as id_refanalyse, id_data, 8, 4 \
                              from sigl_07_data where libelle='CMI Pipéracilline' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 450, 9, 4 from sigl_05_data where code='B676'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B676') as id_refanalyse, id_data,10, 4 \
                              from sigl_07_data where libelle='CMI Aztréonam' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 530, 11, 4 from sigl_05_data where code='B676'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B676') as id_refanalyse, id_data,12, 4 \
                              from sigl_07_data where libelle='CMI Imipénème' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 460, 13, 4 from sigl_05_data where code='B676'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B676') as id_refanalyse, id_data,14, 4 \
                              from sigl_07_data where libelle='CMI Céfalotine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 482, 15, 4 from sigl_05_data where code='B676'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B676') as id_refanalyse, id_data,16, 4 \
                              from sigl_07_data where libelle='CMI Céfoxitine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 496, 17, 4 from sigl_05_data where code='B676'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B676') as id_refanalyse, id_data,18, 4 \
                              from sigl_07_data where libelle='CMI Céftriaxone' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 492, 19, 4 from sigl_05_data where code='B676'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B676') as id_refanalyse, id_data,20, 4 \
                              from sigl_07_data where libelle='CMI Ceftazidime' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 534, 21, 4 from sigl_05_data where code='B676'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B676') as id_refanalyse, id_data,22, 4 \
                              from sigl_07_data where libelle='CMI Kanamycine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 603, 23, 4 from sigl_05_data where code='B676'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B676') as id_refanalyse, id_data,24, 4 \
                              from sigl_07_data where libelle='CMI Tobramycine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 528, 25, 4 from sigl_05_data where code='B676'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B676') as id_refanalyse, id_data,26, 4 \
                              from sigl_07_data where libelle='CMI Gentamicine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 502, 27, 4 from sigl_05_data where code='B676'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B676') as id_refanalyse, id_data,28, 4 \
                              from sigl_07_data where libelle='CMI Chloramphénicol' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 508, 29, 4 from sigl_05_data where code='B676'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B676') as id_refanalyse, id_data,30, 4 \
                              from sigl_07_data where libelle='CMI Colistine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 430, 31, 4 from sigl_05_data where code='B676'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B676') as id_refanalyse, id_data,32, 4 \
                              from sigl_07_data where libelle='CMI Acide nalidixique' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 560, 33, 4 from sigl_05_data where code='B676'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B676') as id_refanalyse, id_data,34, 4 \
                              from sigl_07_data where libelle='CMI Norfloxacine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 504, 35, 4 from sigl_05_data where code='B676'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B676') as id_refanalyse, id_data,36, 4 \
                              from sigl_07_data where libelle='CMI Ciprofloxacine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 595, 37, 4 from sigl_05_data where code='B676'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B676') as id_refanalyse, id_data,38, 4 \
                              from sigl_07_data where libelle='CMI Tétracycline' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 516, 39, 4 from sigl_05_data where code='B676'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B676') as id_refanalyse, id_data,40, 4 \
                              from sigl_07_data where libelle='CMI Doxycycline' order by id_data desc limit 1")
            except:
                print("ERROR insert links for B676 analysis")

        try:
            conn.execute("insert into sigl_05_data (id_owner, code, nom, abbr, famille, cote_unite, commentaire, actif) \
                          values (1000, 'B677', 'Antibiogramme Salmonella spp [CMI]', 'ABG Salmonella spp', 18, 'B', '[WHONET]', 4)")
        except:
            print("ERROR insert B677 analysis")
        else:
            try:
                # Insert links for B677
                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 440, 1, 4 from sigl_05_data where code='B677'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B677') as id_refanalyse, id_data, 2, 4 \
                              from sigl_07_data where libelle='CMI Amoxicilline' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 443, 3, 4 from sigl_05_data where code='B677'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B677') as id_refanalyse, id_data, 4, 4 \
                              from sigl_07_data where libelle='CMI Amoxicilline/ac. Clavulanique' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 597, 5, 4 from sigl_05_data where code='B677'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B677') as id_refanalyse, id_data, 6, 4 \
                              from sigl_07_data where libelle='CMI Ticarcilline' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 573, 7, 4 from sigl_05_data where code='B677'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B677') as id_refanalyse, id_data, 8, 4 \
                              from sigl_07_data where libelle='CMI Pipéracilline' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 450, 9, 4 from sigl_05_data where code='B677'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B677') as id_refanalyse, id_data,10, 4 \
                              from sigl_07_data where libelle='CMI Aztréonam' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 530, 11, 4 from sigl_05_data where code='B677'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B677') as id_refanalyse, id_data,12, 4 \
                              from sigl_07_data where libelle='CMI Imipénème' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 460, 13, 4 from sigl_05_data where code='B677'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B677') as id_refanalyse, id_data,14, 4 \
                              from sigl_07_data where libelle='CMI Céfalotine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 482, 15, 4 from sigl_05_data where code='B677'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B677') as id_refanalyse, id_data,16, 4 \
                              from sigl_07_data where libelle='CMI Céfoxitine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 496, 17, 4 from sigl_05_data where code='B677'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B677') as id_refanalyse, id_data,18, 4 \
                              from sigl_07_data where libelle='CMI Céftriaxone' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 492, 19, 4 from sigl_05_data where code='B677'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B677') as id_refanalyse, id_data,20, 4 \
                              from sigl_07_data where libelle='CMI Ceftazidime' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 534, 21, 4 from sigl_05_data where code='B677'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B677') as id_refanalyse, id_data,22, 4 \
                              from sigl_07_data where libelle='CMI Kanamycine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 603, 23, 4 from sigl_05_data where code='B677'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B677') as id_refanalyse, id_data,24, 4 \
                              from sigl_07_data where libelle='CMI Tobramycine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 528, 25, 4 from sigl_05_data where code='B677'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B677') as id_refanalyse, id_data,26, 4 \
                              from sigl_07_data where libelle='CMI Gentamicine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 502, 27, 4 from sigl_05_data where code='B677'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B677') as id_refanalyse, id_data,28, 4 \
                              from sigl_07_data where libelle='CMI Chloramphénicol' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 508, 29, 4 from sigl_05_data where code='B677'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B677') as id_refanalyse, id_data,30, 4 \
                              from sigl_07_data where libelle='CMI Colistine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 430, 31, 4 from sigl_05_data where code='B677'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B677') as id_refanalyse, id_data,32, 4 \
                              from sigl_07_data where libelle='CMI Acide nalidixique' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 560, 33, 4 from sigl_05_data where code='B677'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B677') as id_refanalyse, id_data,34, 4 \
                              from sigl_07_data where libelle='CMI Norfloxacine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 504, 35, 4 from sigl_05_data where code='B677'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B677') as id_refanalyse, id_data,36, 4 \
                              from sigl_07_data where libelle='CMI Ciprofloxacine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 595, 37, 4 from sigl_05_data where code='B677'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B677') as id_refanalyse, id_data,38, 4 \
                              from sigl_07_data where libelle='CMI Tétracycline' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 516, 39, 4 from sigl_05_data where code='B677'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B677') as id_refanalyse, id_data,40, 4 \
                              from sigl_07_data where libelle='CMI Doxycycline' order by id_data desc limit 1")
            except:
                print("ERROR insert links for B677 analysis")

        try:
            conn.execute("insert into sigl_05_data (id_owner, code, nom, abbr, famille, cote_unite, commentaire, actif) \
                          values (1000, 'B678', 'Antibiogramme Shigella spp [CMI]', 'ABG Shigella spp', 18, 'B', '[WHONET]', 4)")
        except:
            print("ERROR insert B678 analysis")
        else:
            try:
                # Insert links for B678
                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 440, 1, 4 from sigl_05_data where code='B678'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B678') as id_refanalyse, id_data, 2, 4 \
                              from sigl_07_data where libelle='CMI Amoxicilline' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 443, 3, 4 from sigl_05_data where code='B678'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B678') as id_refanalyse, id_data, 4, 4 \
                              from sigl_07_data where libelle='CMI Amoxicilline/ac. Clavulanique' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 597, 5, 4 from sigl_05_data where code='B678'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B678') as id_refanalyse, id_data, 6, 4 \
                              from sigl_07_data where libelle='CMI Ticarcilline' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 573, 7, 4 from sigl_05_data where code='B678'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B678') as id_refanalyse, id_data, 8, 4 \
                              from sigl_07_data where libelle='CMI Pipéracilline' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 450, 9, 4 from sigl_05_data where code='B678'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B678') as id_refanalyse, id_data,10, 4 \
                              from sigl_07_data where libelle='CMI Aztréonam' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 530, 11, 4 from sigl_05_data where code='B678'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B678') as id_refanalyse, id_data,12, 4 \
                              from sigl_07_data where libelle='CMI Imipénème' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 460, 13, 4 from sigl_05_data where code='B678'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B678') as id_refanalyse, id_data,14, 4 \
                              from sigl_07_data where libelle='CMI Céfalotine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 482, 15, 4 from sigl_05_data where code='B678'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B678') as id_refanalyse, id_data,16, 4 \
                              from sigl_07_data where libelle='CMI Céfoxitine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 496, 17, 4 from sigl_05_data where code='B678'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B678') as id_refanalyse, id_data,18, 4 \
                              from sigl_07_data where libelle='CMI Céftriaxone' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 492, 19, 4 from sigl_05_data where code='B678'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B678') as id_refanalyse, id_data,20, 4 \
                              from sigl_07_data where libelle='CMI Ceftazidime' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 534, 21, 4 from sigl_05_data where code='B678'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B678') as id_refanalyse, id_data,22, 4 \
                              from sigl_07_data where libelle='CMI Kanamycine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 603, 23, 4 from sigl_05_data where code='B678'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B678') as id_refanalyse, id_data,24, 4 \
                              from sigl_07_data where libelle='CMI Tobramycine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 528, 25, 4 from sigl_05_data where code='B678'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B678') as id_refanalyse, id_data,26, 4 \
                              from sigl_07_data where libelle='CMI Gentamicine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 502, 27, 4 from sigl_05_data where code='B678'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B678') as id_refanalyse, id_data,28, 4 \
                              from sigl_07_data where libelle='CMI Chloramphénicol' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 508, 29, 4 from sigl_05_data where code='B678'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B678') as id_refanalyse, id_data,30, 4 \
                              from sigl_07_data where libelle='CMI Colistine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 430, 31, 4 from sigl_05_data where code='B678'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B678') as id_refanalyse, id_data,32, 4 \
                              from sigl_07_data where libelle='CMI Acide nalidixique' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 560, 33, 4 from sigl_05_data where code='B678'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B678') as id_refanalyse, id_data,34, 4 \
                              from sigl_07_data where libelle='CMI Norfloxacine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 504, 35, 4 from sigl_05_data where code='B678'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B678') as id_refanalyse, id_data,36, 4 \
                              from sigl_07_data where libelle='CMI Ciprofloxacine' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 595, 37, 4 from sigl_05_data where code='B678'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B678') as id_refanalyse, id_data,38, 4 \
                              from sigl_07_data where libelle='CMI Tétracycline' order by id_data desc limit 1")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, id_data, 516, 39, 4 from sigl_05_data where code='B678'")

                conn.execute("insert into sigl_05_07_data (id_owner, id_refanalyse, id_refvariable, position, obligatoire) \
                              select 1000, (select id_data from sigl_05_data where code='B678') as id_refanalyse, id_data,40, 4 \
                              from sigl_07_data where libelle='CMI Doxycycline' order by id_data desc limit 1")
            except:
                print("ERROR insert links for B678 analysis")


def downgrade():
    pass
