# -*- coding:utf-8 -*-
"""v3_5_5_fix_pathogen_dictionnary

Revision ID: 2aff1c082bb7
Revises: 14d207abf78f
Create Date: 2025-03-07 09:08:00.338202

"""
from alembic import op
from sqlalchemy import text

from datetime import datetime


# revision identifiers, used by Alembic.
revision = '2aff1c082bb7'
down_revision = '14d207abf78f'
branch_labels = None
depends_on = None


def upgrade():
    print("--- " + str(datetime.today()) + "---")
    print("START of migration V3_5_5_fix_pathogen_dictionnary revision=2aff1c082bb7")

    # Get the current
    conn = op.get_bind()

    # delete some entries of pathogen dictionnary
    try:
        conn.execute(text("""
                          DELETE FROM sigl_dico_data
                          WHERE code IN (
                              'bact_45',
                              'virus_11',
                              'virus_163',
                              'virus_164',
                              'virus_165',
                              'virus_176',
                              'virus_177',
                              'virus_178',
                              'virus_179',
                              'virus_180'
                          )
                          """))
    except Exception as err:
        print("ERROR deleting records from sigl_dico_data,\n\terr=" + str(err))

    # update pathogen dictionnary
    try:
        conn.execute(text('''
                          UPDATE sigl_dico_data
                          SET label = CASE
                              WHEN code = 'bact_44' THEN 'Chlamydia psittaci'
                              WHEN code = 'bact_67' THEN 'Escherichia coli'
                              WHEN code = 'bact_68' THEN 'Escherichia coli hautement pathogènes'
                              WHEN code = 'bact_93' THEN 'Leptospira interrogans'
                              WHEN code = 'virus_10' THEN 'Lymphocytic choriomeningitis mammarenavirus'
                              WHEN code = 'virus_19' THEN 'Andes orthohantavirus'
                              WHEN code = 'virus_24' THEN 'Dobrava-Belgrade orthohantavirus'
                              WHEN code = 'virus_26' THEN 'Hantaan orthohantavirus'
                              WHEN code = 'virus_29' THEN 'Puumala orthohantavirus'
                              WHEN code = 'virus_30' THEN 'Seoul orthohantavirus'
                              WHEN code = 'virus_31' THEN 'Sin Nombre orthohantavirus'
                              WHEN code = 'virus_32' THEN 'Orthohantavirus'
                              WHEN code = 'virus_39' THEN 'Orthonairovirus'
                              WHEN code = 'virus_45' THEN 'Orthobunyavirus'
                              WHEN code = 'virus_49' THEN 'Dabie bandavirus'
                              WHEN code = 'virus_55' THEN 'Phlebovirus'
                              WHEN code = 'virus_112' THEN 'Severe acute respiratory syndrome-related coronavirus [virus SARS-CoV]'
                              WHEN code = 'virus_113' THEN 'Severe acute respiratory syndrome-related coronavirus-2 [virus SARS-CoV-2]'
                              WHEN code = 'virus_114' THEN 'Middle East respiratory syndrome-related coronavirus [virus MERS-CoV]'
                              WHEN code = 'virus_115' THEN 'Coronaviridae'
                              WHEN code = 'virus_119' THEN 'Caliciviridae'
                              WHEN code = 'virus_129' THEN 'Enterovirus D'
                              WHEN code = 'virus_140' THEN 'Picornaviridae'
                              WHEN code = 'virus_146' THEN 'Hepelivirales'
                              WHEN code = 'virus_150' THEN 'Amarillovirales'
                              WHEN code = 'virus_162' THEN 'Tick-borne encephalitis virus'
                              WHEN code = 'virus_170' THEN 'Flavivirus'
                              WHEN code = 'virus_186' THEN 'Dhori thogotovirus'
                              WHEN code = 'virus_187' THEN 'Thogoto thogotovirus'
                              WHEN code = 'virus_203' THEN 'Vaccinia virus'
                              WHEN code = 'virus_242' THEN 'Alphavirus'
                              ELSE label
                          END
                          '''))
    except Exception as err:
        print("ERROR updating sigl_dico_data,\n\terr=" + str(err))

    print(str(datetime.today()) + " : END of migration V3_5_5_fix_pathogen_dictionnary revision=2aff1c082bb7")


def downgrade():
    pass
