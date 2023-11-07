"""v3_3_16_rename_tables

Revision ID: 3d67b66dcc23
Revises: f7f46cfe7e02
Create Date: 2023-10-29 17:36:25.535559

"""
from alembic import op
from sqlalchemy import text

from datetime import datetime

# revision identifiers, used by Alembic.
revision = '3d67b66dcc23'
down_revision = 'f7f46cfe7e02'
branch_labels = None
depends_on = None


def upgrade():
    print("--- " + str(datetime.today()) + "---")
    print("START of migration v3_3_16_rename_tables revision=3d67b66dcc23")

    # Get the current
    conn = op.get_bind()

    # rename sigl_controle_externe_ctrl_resultat_cr__file_data to ctrl_ext_res_report_file
    try:
        conn.execute(text("rename table sigl_controle_externe_ctrl_resultat_cr__file_data to ctrl_ext_res_report_file"))
    except Exception as err:
        print("ERROR rename table sigl_controle_externe_ctrl_resultat_cr__file_data,\n\terr=" + str(err))

    # rename sigl_equipement_certif_etalonnage__file_data to eqp_calibration_file
    try:
        conn.execute(text("rename table sigl_equipement_certif_etalonnage__file_data to eqp_calibration_file"))
    except Exception as err:
        print("ERROR rename table sigl_equipement_certif_etalonnage__file_data,\n\terr=" + str(err))

    # rename sigl_equipement_contrat_maintenance__file_data to eqp_calibration_file
    try:
        conn.execute(text("rename table sigl_equipement_contrat_maintenance__file_data to eqp_maintenance_file"))
    except Exception as err:
        print("ERROR rename table sigl_equipement_contrat_maintenance__file_data,\n\terr=" + str(err))

    # rename sigl_equipement_facture__file_data to eqp_invoice_file
    try:
        conn.execute(text("rename table sigl_equipement_facture__file_data to eqp_invoice_file"))
    except Exception as err:
        print("ERROR rename table sigl_equipement_facture__file_data,\n\terr=" + str(err))

    # rename sigl_equipement_maintenance_preventive__file_data to eqp_preventive_maintenance_file
    try:
        conn.execute(text("rename table sigl_equipement_maintenance_preventive__file_data to eqp_preventive_maintenance_file"))
    except Exception as err:
        print("ERROR rename table sigl_equipement_maintenance_preventive__file_data,\n\terr=" + str(err))

    # rename sigl_equipement_pannes__file_data to eqp_failure_file
    try:
        conn.execute(text("rename table sigl_equipement_pannes__file_data to eqp_failure_file"))
    except Exception as err:
        print("ERROR rename table sigl_equipement_pannes__file_data,\n\terr=" + str(err))

    # rename sigl_equipement_photo__file_data to eqp_failure_file
    try:
        conn.execute(text("rename table sigl_equipement_photo__file_data to eqp_photo_file"))
    except Exception as err:
        print("ERROR rename table sigl_equipement_photo__file_data,\n\terr=" + str(err))

    # rename sigl_laboratoire_organigramme__file_data to lab_chart_file
    try:
        conn.execute(text("rename table sigl_laboratoire_organigramme__file_data to lab_chart_file"))
    except Exception as err:
        print("ERROR rename table sigl_laboratoire_organigramme__file_data,\n\terr=" + str(err))

    # rename sigl_procedures_document__file_data to procedure_file
    try:
        conn.execute(text("rename table sigl_procedures_document__file_data to procedure_file"))
    except Exception as err:
        print("ERROR rename table sigl_procedures_document__file_data,\n\terr=" + str(err))

    # rename sigl_dos_valisedoc__file_data to record_file
    try:
        conn.execute(text("rename table sigl_dos_valisedoc__file_data to record_file"))
    except Exception as err:
        print("ERROR rename table sigl_dos_valisedoc__file_data,\n\terr=" + str(err))

    # rename sigl_dos_valisedoc__file_deleted to record_file_deleted
    try:
        conn.execute(text("rename table sigl_dos_valisedoc__file_deleted to record_file_deleted"))
    except Exception as err:
        print("ERROR rename table sigl_dos_valisedoc__file_deleted,\n\terr=" + str(err))

    # rename sigl_reunion_pj__file_data to meeting_file
    try:
        conn.execute(text("rename table sigl_reunion_pj__file_data to meeting_file"))
    except Exception as err:
        print("ERROR rename table sigl_reunion_pj__file_data,\n\terr=" + str(err))

    # rename sigl_manuels_document__file_data to manual_file
    try:
        conn.execute(text("rename table sigl_manuels_document__file_data to manual_file"))
    except Exception as err:
        print("ERROR rename table sigl_manuels_document__file_data,\n\terr=" + str(err))

    # rename sigl_user_diplomes__file_data to user_diploma_file 
    try:
        conn.execute(text("rename table sigl_user_diplomes__file_data to user_diploma_file"))
    except Exception as err:
        print("ERROR rename table sigl_user_diplomes__file_data,\n\terr=" + str(err))

    # rename sigl_user_evaluation__file_data to user_evaluation_file 
    try:
        conn.execute(text("rename table sigl_user_evaluation__file_data to user_evaluation_file"))
    except Exception as err:
        print("ERROR rename table sigl_user_evaluation__file_data,\n\terr=" + str(err))

    # rename sigl_user_cv__file_data to user_cv_file 
    try:
        conn.execute(text("rename table sigl_user_cv__file_data to user_cv_file"))
    except Exception as err:
        print("ERROR rename table sigl_user_cv__file_data,\n\terr=" + str(err))

    # rename sigl_user_formations__file_data to user_training_file
    try:
        conn.execute(text("rename table sigl_user_formations__file_data to user_training_file"))
    except Exception as err:
        print("ERROR rename table sigl_user_formations__file_data,\n\terr=" + str(err))

    # DROP OLD TABLE
    try:
        conn.execute(text("drop table sigl_01_dico_analyse_data, sigl_01_dico_analyse_deleted, "
                          "sigl_12_data, sigl_12_deleted, sigl_03_deleted, sigl_05_05_data, sigl_05_deleted, "
                          "sigl_07_deleted, sigl_08_deleted, sigl_13_data, sigl_16_data, sigl_dico_deleted, "
                          "sigl_equipement_deleted, sigl_fournisseurs_deleted, sigl_laboratoire_data"))
    except Exception as err:
        print("ERROR drop table unused\n\terr=" + str(err))

    print(str(datetime.today()) + " : END of migration v3_3_16_rename_tables revision=3d67b66dcc23")


def downgrade():
    pass
