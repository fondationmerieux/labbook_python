# -*- coding:utf-8 -*-
"""v3_5_7_update_some_manual

Revision ID: 558a7ba02d35
Revises: 745df49ffe70
Create Date: 2025-03-15 16:29:14.853701

"""
from alembic import op
from sqlalchemy import text

from datetime import datetime

# revision identifiers, used by Alembic.
revision = '558a7ba02d35'
down_revision = '745df49ffe70'
branch_labels = None
depends_on = None


def upgrade():
    print("--- " + str(datetime.today()) + "---")
    print("START of migration v3_5_7_update_some_manual revision=558a7ba02d35")

    # Get the current
    conn = op.get_bind()

    import shutil
    import os

    # Source and destination directories
    fromDirectory = "alembic/upload"
    toDirectory = "/storage/upload"

    # Try block to catch any potential errors
    try:
        # Walk through the source directory
        for dirpath, dirnames, filenames in os.walk(fromDirectory):
            # Create corresponding directory in the destination if it doesn't exist
            for dirname in dirnames:
                dest_dir = os.path.join(toDirectory, os.path.relpath(os.path.join(dirpath, dirname), fromDirectory))
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)

            # Copy files and overwrite existing ones
            for filename in filenames:
                source_file = os.path.join(dirpath, filename)
                dest_file = os.path.join(toDirectory, os.path.relpath(source_file, fromDirectory))

                # Overwrite the file if it already exists
                shutil.copy2(source_file, dest_file)  # copy2 preserves metadata

    except Exception as err:
        # Catch and print any errors that occur during the process
        print("ERROR copy alembic upload,\n\terr=" + str(err))

    """
    # Laboratory biosecurity guidance
    try:
        conn.execute(text('''
                          insert into sigl_manuels_data
                          (id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, titre , reference,
                          redacteur_id, verificateur_id, approbateur_id, date_insert, date_apply, date_update, section)
                          values (100, now(), now(), 100, 'Laboratory biosecurity guidance 2024', '', 0, 0, 0, now(), now(), now(), 0)
                          '''
                          ))
    except Exception as err:
        print("ERROR insert into sigl_manuels_data Laboratory biosecurity guidance 2024,\n\terr=" + str(err))

    try:
        conn.execute(text("insert into sigl_file_data "
                          "(id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, status, date_creation, "
                          "original_name, generated_name, size, hash, ext, content_type, id_storage, path) "
                          "values (100, now(), now(), 100, 1, now(), 'laboratory_biosecurity_guidance_2024.pdf', "
                          "'f814b85ac49438ab84af785bf6ec3594', 1165974, '31fb8e59c9bb43c4b73dfce31dc64984', "
                          "'pdf', 'application/pdf', 1, 'f8/14/')"))
    except Exception as err:
        print("ERROR insert into sigl_file_data laboratory_biosecurity_guidance_2024.pdf,\n\terr=" + str(err))

    try:
        conn.execute(text("insert into manual_file "
                          "(id_owner, sys_creation_date, sys_last_mod_date, sys_last_mod_user, id_ext, id_file) "
                          "values (100, now(), now(), 100, (select id_data from sigl_manuels_data order by id_data desc limit 1), "
                          "(select id_data from sigl_file_data order by id_data desc limit 1))"))
    except Exception as err:
        print("ERROR insert into manual_file,\n\terr=" + str(err))
    """

    # --- UPDATE SOME MANUALS ---
    try:
        conn.execute(text("""
            UPDATE `sigl_manuels_data`
            SET
                `titre` = CASE
                    WHEN `titre` = "Guide pratique sur l'application du Reglement relatif au transport des matieres infectieuses 2019-2020"
                    THEN "Guidance on regulations for the transport of infectious substances 2023-2024"
                    WHEN `titre` = "CASFM Recommandations 2020 Oct v1.2"
                    THEN "CASFM Recommandations 2024 v1.0"
                    WHEN `titre` = "EUCAST Breakpoint tables for interpretation of MICs and zone diameters v11.0 2021"
                    THEN "EUCAST Breakpoint tables for interpretation of MICs and zone diameters v15.0 2025"
                    WHEN `titre` = "EUCAST Dosages v11.0 2021"
                    THEN "EUCAST Dosages v15.0 2025"
                    ELSE `titre`
                END,
                `date_update` = CASE
                    WHEN `titre` = "Guidance on regulations for the transport of infectious substances 2023-2024"
                         OR `titre` = "CASFM Recommandations 2024 v1.0"
                         OR `titre` = "EUCAST Breakpoint tables for interpretation of MICs and zone diameters v15.0 2025"
                         OR `titre` = "EUCAST Dosages v15.0 2025"
                    THEN NOW()
                    ELSE `date_update`
                END
        """))
    except Exception as err:
        print("ERROR update titre and date_update in sigl_manuels_data,\n\terr=" + str(err))

    # update original_name and sys_last_mod_date
    try:
        conn.execute(text("""
                          UPDATE sigl_file_data
                          SET
                          original_name = CASE
                          WHEN original_name = 'WHO Guidance on regulations for transport of infectious substances 2019-FR.pdf'
                          THEN 'Guidance on regulations for the transport of infectious substances 2023-2024.pdf'
                          WHEN original_name = 'CASFM_Recommandations_2020_Oct_v1.2.pdf'
                          THEN 'CASFM_Recommandations_2024_v1.0.pdf'
                          WHEN original_name = 'EUCAST_Breakpoint_tables_v11.0_2021.pdf'
                          THEN 'EUCAST_Breakpoint_tables_v15.0_2025.pdf'
                          WHEN original_name = 'EUCAST_Dosages_v11.0_2021.pdf'
                          THEN 'EUCAST_Dosages_v15.0_2025.pdf'
                          ELSE original_name
                          END,
                          sys_last_mod_date = NOW(),
                          size = CASE
                          WHEN original_name = 'Guidance on regulations for the transport of infectious substances 2023-2024.pdf' THEN 1165974
                          WHEN original_name = 'CASFM_Recommandations_2024_v1.0.pdf' THEN 8045852
                          WHEN original_name = 'EUCAST_Breakpoint_tables_v15.0_2025.pdf' THEN 3853956
                          WHEN original_name = 'EUCAST_Dosages_v15.0_2025.pdf' THEN 3709284
                          ELSE size
                          END
                          """))
    except Exception as err:
        print("ERROR update original_name and sys_last_mod_date in sigl_file_data,\n\terr=" + str(err))

    # Insert default permissions for technician qualitician (pro_ser = 13)
    try:
        conn.execute(text('''
                          insert into profile_permissions (prp_date, prp_by_user, prp_pro, prp_prr, prp_granted)
                          values
                          (NOW(), 0, 13, 1,"N"),
                          (NOW(), 0, 13, 2,"N"),
                          (NOW(), 0, 13, 3,"Y"),
                          (NOW(), 0, 13, 4,"N"),
                          (NOW(), 0, 13, 5,"N"),
                          (NOW(), 0, 13, 6,"N"),
                          (NOW(), 0, 13, 7,"N"),
                          (NOW(), 0, 13, 8,"Y"),
                          (NOW(), 0, 13, 9,"Y"),
                          (NOW(), 0, 13, 10,"Y"),
                          (NOW(), 0, 13, 11,"Y"),
                          (NOW(), 0, 13, 12,"Y"),
                          (NOW(), 0, 13, 13,"Y"),
                          (NOW(), 0, 13, 14,"Y"),
                          (NOW(), 0, 13, 15,"Y"),
                          (NOW(), 0, 13, 16,"Y"),
                          (NOW(), 0, 13, 17,"Y"),
                          (NOW(), 0, 13, 18,"Y"),
                          (NOW(), 0, 13, 19,"Y"),
                          (NOW(), 0, 13, 20,"Y"),
                          (NOW(), 0, 13, 21,"Y"),
                          (NOW(), 0, 13, 22,"Y"),
                          (NOW(), 0, 13, 23,"N"),
                          (NOW(), 0, 13, 24,"Y"),
                          (NOW(), 0, 13, 25,"Y"),
                          (NOW(), 0, 13, 26,"Y"),
                          (NOW(), 0, 13, 27,"Y"),
                          (NOW(), 0, 13, 28,"Y"),
                          (NOW(), 0, 13, 29,"Y"),
                          (NOW(), 0, 13, 30,"Y"),
                          (NOW(), 0, 13, 31,"Y"),
                          (NOW(), 0, 13, 32,"Y"),
                          (NOW(), 0, 13, 33,"Y"),
                          (NOW(), 0, 13, 34,"Y"),
                          (NOW(), 0, 13, 35,"Y"),
                          (NOW(), 0, 13, 36,"Y"),
                          (NOW(), 0, 13, 37,"Y"),
                          (NOW(), 0, 13, 38,"Y"),
                          (NOW(), 0, 13, 39,"Y"),
                          (NOW(), 0, 13, 40,"N"),
                          (NOW(), 0, 13, 41,"N"),
                          (NOW(), 0, 13, 42,"N"),
                          (NOW(), 0, 13, 43,"N"),
                          (NOW(), 0, 13, 44,"N"),
                          (NOW(), 0, 13, 45,"N"),
                          (NOW(), 0, 13, 46,"N"),
                          (NOW(), 0, 13, 47,"N"),
                          (NOW(), 0, 13, 48,"N"),
                          (NOW(), 0, 13, 49,"N"),
                          (NOW(), 0, 13, 50,"N"),
                          (NOW(), 0, 13, 51,"N"),
                          (NOW(), 0, 13, 52,"N"),
                          (NOW(), 0, 13, 53,"N"),
                          (NOW(), 0, 13, 54,"N"),
                          (NOW(), 0, 13, 55,"N"),
                          (NOW(), 0, 13, 56,"N"),
                          (NOW(), 0, 13, 57,"N"),
                          (NOW(), 0, 13, 58,"N"),
                          (NOW(), 0, 13, 59,"N"),
                          (NOW(), 0, 13, 60,"N"),
                          (NOW(), 0, 13, 61,"N"),
                          (NOW(), 0, 13, 62,"N"),
                          (NOW(), 0, 13, 63,"N"),
                          (NOW(), 0, 13, 64,"N"),
                          (NOW(), 0, 13, 65,"N"),
                          (NOW(), 0, 13, 66,"N"),
                          (NOW(), 0, 13, 67,"N"),
                          (NOW(), 0, 13, 68,"N"),
                          (NOW(), 0, 13, 69,"N"),
                          (NOW(), 0, 13, 70,"Y"),
                          (NOW(), 0, 13, 71,"N"),
                          (NOW(), 0, 13, 72,"N"),
                          (NOW(), 0, 13, 73,"N"),
                          (NOW(), 0, 13, 74,"N"),
                          (NOW(), 0, 13, 75,"N"),
                          (NOW(), 0, 13, 76,"N"),
                          (NOW(), 0, 13, 77,"Y"),
                          (NOW(), 0, 13, 78,"Y"),
                          (NOW(), 0, 13, 79,"Y"),
                          (NOW(), 0, 13, 80,"Y"),
                          (NOW(), 0, 13, 81,"Y"),
                          (NOW(), 0, 13, 82,"Y"),
                          (NOW(), 0, 13, 83,"Y"),
                          (NOW(), 0, 13, 84,"Y"),
                          (NOW(), 0, 13, 85,"Y"),
                          (NOW(), 0, 13, 86,"Y"),
                          (NOW(), 0, 13, 87,"Y"),
                          (NOW(), 0, 13, 88,"Y"),
                          (NOW(), 0, 13, 89,"Y"),
                          (NOW(), 0, 13, 90,"Y"),
                          (NOW(), 0, 13, 91,"Y"),
                          (NOW(), 0, 13, 92,"Y"),
                          (NOW(), 0, 13, 93,"Y"),
                          (NOW(), 0, 13, 94,"Y"),
                          (NOW(), 0, 13, 95,"Y"),
                          (NOW(), 0, 13, 96,"Y"),
                          (NOW(), 0, 13, 97,"Y"),
                          (NOW(), 0, 13, 98,"Y"),
                          (NOW(), 0, 13, 99,"Y"),
                          (NOW(), 0, 13, 100,"Y"),
                          (NOW(), 0, 13, 101,"Y"),
                          (NOW(), 0, 13, 102,"Y"),
                          (NOW(), 0, 13, 103,"Y"),
                          (NOW(), 0, 13, 104,"Y"),
                          (NOW(), 0, 13, 105,"Y"),
                          (NOW(), 0, 13, 106,"Y"),
                          (NOW(), 0, 13, 107,"Y"),
                          (NOW(), 0, 13, 108,"Y"),
                          (NOW(), 0, 13, 109,"Y"),
                          (NOW(), 0, 13, 110,"Y"),
                          (NOW(), 0, 13, 111,"Y"),
                          (NOW(), 0, 13, 112,"Y"),
                          (NOW(), 0, 13, 113,"Y"),
                          (NOW(), 0, 13, 114,"Y"),
                          (NOW(), 0, 13, 115,"Y"),
                          (NOW(), 0, 13, 116,"Y"),
                          (NOW(), 0, 13, 117,"Y"),
                          (NOW(), 0, 13, 118,"Y"),
                          (NOW(), 0, 13, 119,"Y"),
                          (NOW(), 0, 13, 120,"Y"),
                          (NOW(), 0, 13, 121,"Y"),
                          (NOW(), 0, 13, 122,"Y"),
                          (NOW(), 0, 13, 123,"Y"),
                          (NOW(), 0, 13, 124,"Y"),
                          (NOW(), 0, 13, 125,"Y"),
                          (NOW(), 0, 13, 126,"Y"),
                          (NOW(), 0, 13, 127,"N"),
                          (NOW(), 0, 13, 128,"Y"),
                          (NOW(), 0, 13, 129,"Y"),
                          (NOW(), 0, 13, 130,"Y"),
                          (NOW(), 0, 13, 131,"Y"),
                          (NOW(), 0, 13, 132,"Y"),
                          (NOW(), 0, 13, 133,"Y"),
                          (NOW(), 0, 13, 134,"N"),
                          (NOW(), 0, 13, 135,"N"),
                          (NOW(), 0, 13, 136,"N"),
                          (NOW(), 0, 13, 137,"N"),
                          (NOW(), 0, 13, 138,"N"),
                          (NOW(), 0, 13, 139,"Y"),
                          (NOW(), 0, 13, 140,"N"),
                          (NOW(), 0, 13, 141,"N"),
                          (NOW(), 0, 13, 142,"N"),
                          (NOW(), 0, 13, 143,"Y"),
                          (NOW(), 0, 13, 144,"Y"),
                          (NOW(), 0, 13, 145,"Y"),
                          (NOW(), 0, 13, 146,"Y"),
                          (NOW(), 0, 13, 147,"Y"),
                          (NOW(), 0, 13, 148,"N"),
                          (NOW(), 0, 13, 149,"N"),
                          (NOW(), 0, 13, 150,"N"),
                          (NOW(), 0, 13, 151,"Y"),
                          (NOW(), 0, 13, 152,"Y"),
                          (NOW(), 0, 13, 153,"Y"),
                          (NOW(), 0, 13, 154,"Y"),
                          (NOW(), 0, 13, 155,"Y"),
                          (NOW(), 0, 13, 156,"Y"),
                          (NOW(), 0, 13, 157,"Y"),
                          (NOW(), 0, 13, 158,"Y"),
                          (NOW(), 0, 13, 159,"Y"),
                          (NOW(), 0, 13, 160,"Y"),
                          (NOW(), 0, 13, 161,"Y"),
                          (NOW(), 0, 13, 162,"Y"),
                          (NOW(), 0, 13, 163,"Y"),
                          (NOW(), 0, 13, 164,"Y"),
                          (NOW(), 0, 13, 165,"Y"),
                          (NOW(), 0, 13, 166,"Y"),
                          (NOW(), 0, 13, 167,"Y"),
                          (NOW(), 0, 13, 168,"Y"),
                          (NOW(), 0, 13, 169,"Y"),
                          (NOW(), 0, 13, 170,"Y"),
                          (NOW(), 0, 13, 171,"Y"),
                          (NOW(), 0, 13, 172,"Y"),
                          (NOW(), 0, 13, 173,"Y")
                          '''
                          ))
    except Exception as err:
        print("ERROR insert default profile_role technician qualitician,\n\terr=" + str(err))

    # UPDATE switch Y to N some biologist permissions
    try:
        conn.execute(text('''
                          UPDATE profile_permissions pp
                          JOIN profile_role pr ON pp.prp_pro = pr.pro_ser
                          JOIN sigl_pj_role r ON pr.pro_role = r.id_role
                          JOIN profile_rights prr ON pp.prp_prr = prr.prr_ser
                          SET pp.prp_granted = 'N'
                          WHERE r.type = 'B'
                          AND pp.prp_granted = 'Y'
                          AND prr.prr_tag IN ('API_2')
                          '''))
    except Exception as err:
        print("ERROR update biologist Y to N profile_permissions set prp_granted,\n\terr=" + str(err))

    # UPDATE switch N to Y some tech advanced permissions
    try:
        conn.execute(text('''
                          UPDATE profile_permissions pp
                          JOIN profile_role pr ON pp.prp_pro = pr.pro_ser
                          JOIN sigl_pj_role r ON pr.pro_role = r.id_role
                          JOIN profile_rights prr ON pp.prp_prr = prr.prr_ser
                          SET pp.prp_granted = 'Y'
                          WHERE r.type = 'TA'
                          AND pp.prp_granted = 'N'
                          AND prr.prr_tag IN ('RECORD_6', 'RECORD_7', 'SETTING_42', 'SETTING_43', 'SETTING_48',
                          'SETTING_49', 'SETTING_50', 'SETTING_52', 'SETTING_53', 'SETTING_56', 'SETTING_57', 'SETTING_58',
                          'SETTING_75', 'SETTING_76')
                          '''))
    except Exception as err:
        print("ERROR update tech advanced N to Y profile_permissions set prp_granted,\n\terr=" + str(err))

    # UPDATE switch Y to N some tech advanced permissions
    try:
        conn.execute(text('''
                          UPDATE profile_permissions pp
                          JOIN profile_role pr ON pp.prp_pro = pr.pro_ser
                          JOIN sigl_pj_role r ON pr.pro_role = r.id_role
                          JOIN profile_rights prr ON pp.prp_prr = prr.prr_ser
                          SET pp.prp_granted = 'N'
                          WHERE r.type = 'TA'
                          AND pp.prp_granted = 'Y'
                          AND prr.prr_tag IN ('SETTING_60', 'SETTING_61', 'SETTING_62', 'SETTING_63', 'LAB_79', 'LAB_80',
                          'LAB_81', 'STAFF_83', 'STAFF_84', 'STAFF_85', 'SUPPLIER_92', 'SUPPLIER_93', 'SUPPLIER_94',
                          'SUPPLIER_95', 'EQP_97', 'EQP_98', 'EQP_99', 'EQP_100', 'EQP_101', 'EQP_102', 'EQP_103',
                          'EQP_104', 'EQP_105', 'EQP_106', 'EQP_107', 'EQP_108', 'EQP_109', 'EQP_110', 'EQP_111',
                          'EQP_112', 'EQP_113', 'EQP_114', 'EQP_115', 'EQP_116', 'EQP_117', 'EQP_118', 'EQP_119',
                          'PROCEDURE_127', 'PROCEDURE_128', 'PROCEDURE_129', 'PROCEDURE_130', 'PROCEDURE_131',
                          'PROCEDURE_132', 'STOCK_139', 'CTRLINT_152', 'CTRLINT_153', 'CTRLINT_154', 'CTRLINT_155',
                          'CTRLINT_156', 'CTRLEXT_158', 'CTRLEXT_159', 'CTRLEXT_160', 'CTRLEXT_161', 'CTRLEXT_162',
                          'MEETING_164', 'MEETING_165', 'MEETING_166', 'MEETING_167', 'MEETING_168')
                          '''))
    except Exception as err:
        print("ERROR update tech advanced Y to N profile_permissions set prp_granted,\n\terr=" + str(err))

    # UPDATE switch Y to N some tech permissions
    try:
        conn.execute(text('''
                          UPDATE profile_permissions pp
                          JOIN profile_role pr ON pp.prp_pro = pr.pro_ser
                          JOIN sigl_pj_role r ON pr.pro_role = r.id_role
                          JOIN profile_rights prr ON pp.prp_prr = prr.prr_ser
                          SET pp.prp_granted = 'N'
                          WHERE r.type = 'T'
                          AND pp.prp_granted = 'Y'
                          AND prr.prr_tag IN ('RECORD_6', 'RECORD_7', 'SETTING_38', 'SETTING_39', 'SETTING_42',
                          'SETTING_43', 'SETTING_48', 'SETTING_49', 'SETTING_50', 'SETTING_52', 'SETTING_53', 'SETTING_56',
                          'SETTING_57', 'SETTING_58', 'SETTING_70', 'SETTING_71', 'SETTING_75', 'SETTING_76')
                          '''))
    except Exception as err:
        print("ERROR update tech Y to N profile_permissions set prp_granted,\n\terr=" + str(err))

    # UPDATE switch Y to N some secr advanced permissions
    try:
        conn.execute(text('''
                          UPDATE profile_permissions pp
                          JOIN profile_role pr ON pp.prp_pro = pr.pro_ser
                          JOIN sigl_pj_role r ON pr.pro_role = r.id_role
                          JOIN profile_rights prr ON pp.prp_prr = prr.prr_ser
                          SET pp.prp_granted = 'N'
                          WHERE r.type = 'SA'
                          AND pp.prp_granted = 'Y'
                          AND prr.prr_tag IN ('RECORD_8', 'RECORD_9', 'RECORD_13', 'NONCONF_145', 'NONCONF_146')
                          '''))
    except Exception as err:
        print("ERROR update secr advanced Y to N profile_permissions set prp_granted,\n\terr=" + str(err))

    # UPDATE switch N to Y some secr advanced permissions
    try:
        conn.execute(text('''
                          UPDATE profile_permissions pp
                          JOIN profile_role pr ON pp.prp_pro = pr.pro_ser
                          JOIN sigl_pj_role r ON pr.pro_role = r.id_role
                          JOIN profile_rights prr ON pp.prp_prr = prr.prr_ser
                          SET pp.prp_granted = 'N'
                          WHERE r.type = 'SA'
                          AND pp.prp_granted = 'Y'
                          AND prr.prr_tag IN ('SETTING_38', 'SETTING_39', 'SETTING_70')
                          '''))
    except Exception as err:
        print("ERROR update secr advanced N to Y profile_permissions set prp_granted,\n\terr=" + str(err))

    # UPDATE switch Y to N some secr permissions
    try:
        conn.execute(text('''
                          UPDATE profile_permissions pp
                          JOIN profile_role pr ON pp.prp_pro = pr.pro_ser
                          JOIN sigl_pj_role r ON pr.pro_role = r.id_role
                          JOIN profile_rights prr ON pp.prp_prr = prr.prr_ser
                          SET pp.prp_granted = 'N'
                          WHERE r.type = 'S'
                          AND pp.prp_granted = 'Y'
                          AND prr.prr_tag IN ('RECORD_14', 'RECORD_15', 'RECORD_16', 'RECORD_17', 'RECORD_24', 'RECORD_25',
                          'SETTING_38', 'SETTING_39', 'SETTING_70', 'GEN_77', 'STOCK_133')
                          '''))
    except Exception as err:
        print("ERROR update secr Y to N profile_permissions set prp_granted,\n\terr=" + str(err))

    # UPDATE switch Y to N some qualitician permissions
    try:
        conn.execute(text('''
                          UPDATE profile_permissions pp
                          JOIN profile_role pr ON pp.prp_pro = pr.pro_ser
                          JOIN sigl_pj_role r ON pr.pro_role = r.id_role
                          JOIN profile_rights prr ON pp.prp_prr = prr.prr_ser
                          SET pp.prp_granted = 'N'
                          WHERE r.type = 'Q'
                          AND pp.prp_granted = 'Y'
                          AND prr.prr_tag IN ('REPORT_26', 'REPORT_27', 'REPORT_28', 'REPORT_29', 'REPORT_30', 'REPORT_31',
                          'REPORT_32', 'REPORT_33', 'REPORT_34', 'REPORT_35', 'REPORT_36', 'REPORT_37', 'RECORD_3',
                          'RECORD_10', 'RECORD_11', 'RECORD_12', 'RECORD_18', 'RECORD_19', 'RECORD_20', 'RECORD_21',
                          'RECORD_22')
                          '''))
    except Exception as err:
        print("ERROR update qualitician Y to N profile_permissions set prp_granted,\n\terr=" + str(err))

    # UPDATE switch N to Y some qualitician permissions
    try:
        conn.execute(text('''
                          UPDATE profile_permissions pp
                          JOIN profile_role pr ON pp.prp_pro = pr.pro_ser
                          JOIN sigl_pj_role r ON pr.pro_role = r.id_role
                          JOIN profile_rights prr ON pp.prp_prr = prr.prr_ser
                          SET pp.prp_granted = 'Y'
                          WHERE r.type = 'Q'
                          AND pp.prp_granted = 'N'
                          AND prr.prr_tag IN ('GEN_77', 'SUPPLIER_91', 'SUPPLIER_92', 'SUPPLIER_93', 'SUPPLIER_94',
                          'SUPPLIER_95', 'EQP_96', 'EQP_97', 'EQP_98', 'EQP_99', 'EQP_100', 'EQP_101', 'EQP_102',
                          'EQP_103', 'EQP_104', 'EQP_105', 'EQP_106', 'EQP_107', 'EQP_108', 'EQP_109', 'EQP_110',
                          'EQP_111', 'EQP_112', 'EQP_113', 'EQP_114', 'EQP_115', 'EQP_116', 'EQP_117', 'EQP_118',
                          'EQP_119', 'MANUAL_121', 'MANUAL_122', 'MANUAL_123', 'MANUAL_124', 'MANUAL_125',
                          'PROCEDURE_127', 'PROCEDURE_128', 'PROCEDURE_129', 'PROCEDURE_130', 'PROCEDURE_131',
                          'PROCEDURE_132', 'STOCK_133', 'NONCONF_145', 'NONCONF_146', 'NONCONF_148', 'NONCONF_149',
                          'NONCONF_150', 'CTRLINT_152', 'CTRLINT_153', 'CTRLINT_154', 'CTRLINT_155', 'CTRLINT_156',
                          'CTRLEXT_158', 'CTRLEXT_159', 'CTRLEXT_160', 'CTRLEXT_161', 'CTRLEXT_162', 'MEETING_164',
                          'MEETING_165', 'MEETING_166', 'MEETING_167', 'MEETING_168', 'STAFF_83', 'STAFF_84', 'STAFF_85')
                          '''))
    except Exception as err:
        print("ERROR update qualitician N to Y profile_permissions set prp_granted,\n\terr=" + str(err))

    # UPDATE switch N to Y some prescriber permissions
    try:
        conn.execute(text('''
                          UPDATE profile_permissions pp
                          JOIN profile_role pr ON pp.prp_pro = pr.pro_ser
                          JOIN sigl_pj_role r ON pr.pro_role = r.id_role
                          JOIN profile_rights prr ON pp.prp_prr = prr.prr_ser
                          SET pp.prp_granted = 'Y'
                          WHERE r.type = 'P'
                          AND pp.prp_granted = 'N'
                          AND prr.prr_tag IN ('RECORD_3', 'RECORD_14', 'RECORD_18')
                          '''))
    except Exception as err:
        print("ERROR update prescriber N to Y profile_permissions set prp_granted,\n\terr=" + str(err))

    # UPDATE switch Y to N some prescriber permissions
    try:
        conn.execute(text('''
                          UPDATE profile_permissions pp
                          JOIN profile_role pr ON pp.prp_pro = pr.pro_ser
                          JOIN sigl_pj_role r ON pr.pro_role = r.id_role
                          JOIN profile_rights prr ON pp.prp_prr = prr.prr_ser
                          SET pp.prp_granted = 'N'
                          WHERE r.type = 'P'
                          AND pp.prp_granted = 'Y'
                          AND prr.prr_tag IN ('SETTING_60', 'SETTING_61', 'SETTING_62', 'SETTING_63', 'GEN_77', 'LAB_78',
                          'LAB_79', 'LAB_80', 'LAB_81', 'STAFF_82', 'STAFF_83', 'STAFF_84', 'STAFF_85', 'DOCTOR_86',
                          'DOCTOR_87', 'DOCTOR_88', 'DOCTOR_89', 'DOCTOR_90', 'SUPPLIER_91', 'SUPPLIER_92', 'SUPPLIER_93',
                          'SUPPLIER_94', 'SUPPLIER_95', 'EQP_96', 'EQP_97', 'EQP_98', 'EQP_99', 'EQP_100', 'EQP_101',
                          'EQP_102', 'EQP_103', 'EQP_104', 'EQP_105', 'EQP_106', 'EQP_107', 'EQP_108', 'EQP_109',
                          'EQP_110', 'EQP_111', 'EQP_112', 'EQP_113', 'EQP_114', 'EQP_115', 'EQP_116', 'EQP_117',
                          'EQP_118', 'EQP_119', 'MANUAL_120', 'MANUAL_121', 'MANUAL_122', 'MANUAL_123', 'MANUAL_124',
                          'MANUAL_125', 'PROCEDURE_126', 'PROCEDURE_127', 'PROCEDURE_128', 'PROCEDURE_129',
                          'PROCEDURE_130', 'PROCEDURE_131', 'PROCEDURE_132', 'STOCK_133', 'STOCK_134', 'STOCK_135',
                          'STOCK_136', 'STOCK_137', 'STOCK_138', 'STOCK_139', 'STOCK_140', 'STOCK_141', 'STOCK_142',
                          'NONCONF_147', 'NONCONF_148', 'NONCONF_149', 'NONCONF_150', 'CTRLINT_151', 'CTRLINT_152',
                          'CTRLINT_153', 'CTRLINT_154', 'CTRLINT_155', 'CTRLINT_156', 'CTRLEXT_157', 'CTRLEXT_158',
                          'CTRLEXT_159', 'CTRLEXT_160', 'CTRLEXT_161', 'CTRLEXT_162', 'MEETING_163', 'MEETING_164',
                          'MEETING_165', 'MEETING_166', 'MEETING_167', 'MEETING_168')
                          '''))
    except Exception as err:
        print("ERROR update prescriber Y to N profile_permissions set prp_granted,\n\terr=" + str(err))

    # Create table for connect_setting
    try:
        conn.execute(text('''
                          create table connect_setting(
                          cos_ser int not NULL AUTO_INCREMENT,
                          cos_date DATETIME,
                          cos_by_user int default 0,
                          cos_url varchar(255) NOT NULL,
                          PRIMARY KEY (cos_ser))
                          character set=utf8
                          '''))
    except Exception as err:
        print("ERROR create table connect_setting,\n\terr=" + str(err))

    # Insert default connect_setting
    try:
        conn.execute(text('''
                          insert into connect_setting (cos_date, cos_by_user, cos_url)
                          values (NOW(), 0, "http://localhost:8080")
                          '''))
    except Exception as err:
        print("ERROR insert default connect_setting,\n\terr=" + str(err))

    try:
        conn.execute(text('''
                          ALTER TABLE analyzer_setting
                          DROP COLUMN ans_connect,
                          DROP COLUMN ans_mapping
                          '''))
    except Exception as err:
        print("ERROR delete ans_connect and ans_cmapping in analyzer_setting,\n\terr=" + str(err))

    try:
        conn.execute(text('''
                          ALTER TABLE analyzer_setting
                          ADD COLUMN ans_batch VARCHAR(1) NOT NULL DEFAULT 'Y'
                          '''))
    except Exception as err:
        print("ERROR while adding column ans_batch:\n\terr=" + str(err))

    print(str(datetime.today()) + " : END of migration v3_5_7_update_some_manual revision=558a7ba02d35")


def downgrade():
    pass
