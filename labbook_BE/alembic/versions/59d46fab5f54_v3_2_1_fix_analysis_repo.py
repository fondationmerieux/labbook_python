# -*- coding:utf-8 -*-
"""v3_2_1_fix_analysis_repo

Revision ID: 59d46fab5f54
Revises: 5a4e9dbb96dc
Create Date: 2021-12-20 10:52:22.584847

"""
from alembic import op

from datetime import datetime

# revision identifiers, used by Alembic.
revision = '59d46fab5f54'
down_revision = '5a4e9dbb96dc'
branch_labels = None
depends_on = None


def upgrade():
    print("--- " + str(datetime.today()) + "---")
    print("START of migration v3_2_1_fix_analysis_repo revision=59d46fab5f54")

    # Get the current
    conn = op.get_bind()

    # UPDATE wrong minimal value for B008
    try:
        conn.execute("update sigl_07_data set normal_min='2.15' "
                     "where normal_min='2. 15' ")
    except Exception as err:
        print("ERROR update normal_min for B008,\n\terr=" + str(err))

    # NEW TABLE for load list of zip code city and region
    try:
        conn.execute("create table zip_city ("
                     "zic_ser int not NULL AUTO_INCREMENT,"
                     "zic_date datetime,"
                     "zic_zip varchar(10),"
                     "zic_city varchar(255),"
                     "PRIMARY KEY (zic_ser),"
                     "INDEX (zic_zip), INDEX (zic_city)) character set=utf8")
    except Exception as err:
        print("ERROR create table zip_city,\n\terr=" + str(err))

   # NEW TABLE for quality control
    try:
        conn.execute("create table control_quality ("
                     "ctq_ser int not NULL AUTO_INCREMENT,"
                     "ctq_date datetime,"
                     "ctq_type_ctrl varchar(10),"
                     "ctq_type_val varchar(10),"
                     "ctq_name varchar(255),"
                     "ctq_eqp int,"
                     "PRIMARY KEY (ctq_ser),"
                     "INDEX (ctq_type_ctrl), INDEX (ctq_name), INDEX (ctq_eqp), INDEX (ctq_type_val)) character set=utf8")
    except Exception as err:
        print("ERROR create table quality_control,\n\terr=" + str(err))

    # NEW TABLE for value of internal control
    try:
        conn.execute("create table control_internal ("
                     "cti_ser int not NULL AUTO_INCREMENT,"
                     "cti_ctq int not NULL,"
                     "cti_date datetime,"
                     "cti_type varchar(10),"
                     "cti_target varchar(255),"
                     "cti_conform varchar(10),"
                     "cti_comment varchar(255),"
                     "PRIMARY KEY (cti_ser),"
                     "INDEX (cti_type), INDEX (cti_ctq)) character set=utf8")
    except Exception as err:
        print("ERROR create table control_internal,\n\terr=" + str(err))

    # NEW TABLE for value of external control
    try:
        conn.execute("create table control_external ("
                     "cte_ser int not NULL AUTO_INCREMENT,"
                     "cte_ctq int not NULL,"
                     "cte_date datetime,"
                     "cte_type varchar(10),"
                     "cte_organizer varchar(255),"
                     "cte_contact varchar(255),"
                     "cte_result varchar(255),"
                     "cte_comment varchar(255),"
                     "PRIMARY KEY (cte_ser),"
                     "INDEX (cte_type), INDEX (cte_ctq)) character set=utf8")
    except Exception as err:
        print("ERROR create table control_external,\n\terr=" + str(err))

    # DROP OLD TABLE
    try:
        conn.execute("drop table sigl_controle_externe_ctrl_resultat__file_data, sigl_controle_externe_data, "
                     "sigl_controle_externe_ctrl_resultat__file_deleted, sigl_controle_externe_deleted, "
                     "sigl_controle_externe_ctrl_resultat_cr__file_deleted, sigl_controle_interne_data, "
                     "sigl_controle_interne_deleted")
    except Exception as err:
        print("ERROR drop table like sigl_control_...\n\terr=" + str(err))

    # DROP COLUMN TO Analysis TABLE
    try:
        conn.execute("alter table sigl_05_data drop column paillasse")
    except Exception as err:
        print("ERROR drop column paillasse to sigl_05_data,\n\terr=" + str(err))

    # DROP COLUMN TO Patient TABLE
    try:
        conn.execute("alter table sigl_03_data drop column ethnie")
    except Exception as err:
        print("ERROR drop column ethnie to sigl_03_data,\n\terr=" + str(err))

    # DROP COLUMN TO Patient TABLE
    try:
        conn.execute("alter table sigl_03_data drop column annee_naiss")
    except Exception as err:
        print("ERROR drop column annee_naiss to sigl_03_data,\n\terr=" + str(err))

    # DROP COLUMN TO Patient TABLE
    try:
        conn.execute("alter table sigl_03_data drop column mois_naiss")
    except Exception as err:
        print("ERROR drop column mois_naiss to sigl_03_data,\n\terr=" + str(err))

    # DROP COLUMN TO Patient TABLE
    try:
        conn.execute("alter table sigl_03_data drop column semaine_naiss")
    except Exception as err:
        print("ERROR drop column semaine_naiss to sigl_03_data,\n\terr=" + str(err))

    print(str(datetime.today()) + " : END of migration v3_2_1_fix_analysis_repo revision=59d46fab5f54")

def downgrade():
    pass
