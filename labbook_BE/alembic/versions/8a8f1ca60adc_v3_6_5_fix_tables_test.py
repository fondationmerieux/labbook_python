"""v3_6_5_fix_tables_test

Revision ID: 8a8f1ca60adc
Revises: 76ef200b0496
Create Date: 2025-11-06 11:33:48.495653

"""
import os
from pathlib import Path
from alembic import op
from sqlalchemy import text

from datetime import datetime


# revision identifiers, used by Alembic.
revision = '8a8f1ca60adc'
down_revision = '76ef200b0496'
branch_labels = None
depends_on = None


def upgrade():
    print("--- " + str(datetime.today()) + "---")
    print("START of migration v3_6_5_fix_tables_test revision=8a8f1ca60adc")

    # Create report directories directly
    for path in [
        "/storage/upload/dhis2",
        "/storage/upload/activity",
        "/storage/upload/billing"
    ]:
        try:
            Path(path).mkdir(parents=True, exist_ok=True)
            os.chmod(path, 0o775)
            Path(path, ".keep").touch()
        except Exception as err:
            print(f"ERROR creating directory {path},\n\terr={err}")

    # Get the current
    conn = op.get_bind()

    # COPY alembic resource, erase file only if more recent
    try:
        from distutils.dir_util import copy_tree

        fromDirectory = "alembic/resource"
        toDirectory = "/storage/resource"

        copy_tree(fromDirectory, toDirectory, update=1)
    except Exception as err:
        print("ERROR copy alembic resource,\n\terr=" + str(err))

    # ADD template activity report
    try:
        conn.execute(text('''
            insert into template_setting
            (tpl_date, tpl_name, tpl_file, tpl_default, tpl_type)
            values (NOW(), "Modèle rapport d'activité", "tpl_activity_report.odt", "Y", "ACT")
            '''))
    except Exception as err:
        print("ERROR insert activity report template for template_setting,\n\terr=" + str(err))

    # ADD COLUMN for ana_lite in sigl_05_data_test
    try:
        conn.execute(text("alter table sigl_05_data_test add column ana_lite varchar(1) not null default 'N'"))
    except Exception as err:
        print("ERROR add column ana_lite to sigl_05_data_test,\n\terr=" + str(err))

    # ADD COLUMN for var_in_report in sigl_07_data
    try:
        conn.execute(text("ALTER TABLE sigl_07_data_test ADD COLUMN var_in_report varchar(1) not null default 'Y'"))
    except Exception as err:
        print("ERROR add column var_in_report to sigl_07_data_test,\n\terr=" + str(err))

    # ENLARGED COLUMN path IN sigl_file_data
    try:
        conn.execute(text("ALTER TABLE sigl_file_data MODIFY COLUMN path VARCHAR(64) NOT NULL"))
    except Exception as err:
        print("ERROR alter column path in sigl_file_data,\n\terr=" + str(err))

    # CREATE TABLE patient_hist_form_item
    try:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS patient_hist_form_item (
                phfi_ser   INT         NOT NULL AUTO_INCREMENT,
                phfi_evt   VARCHAR(36) NOT NULL,
                phfi_date  DATETIME    NOT NULL,
                phfi_user  INT         NOT NULL DEFAULT 0,
                phfi_pat   INT         NOT NULL,
                phfi_act   VARCHAR(1)  NOT NULL DEFAULT 'Y',
                phfi_type  VARCHAR(20) NOT NULL,
                phfi_key   VARCHAR(80) NOT NULL,
                phfi_value MEDIUMTEXT  NOT NULL,
                PRIMARY KEY (phfi_ser),
                KEY idx_phfi_pat  (phfi_pat),
                KEY idx_phfi_type (phfi_type),
                KEY idx_phfi_evt  (phfi_evt),
                KEY idx_phfi_date (phfi_date)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """))
    except Exception as err:
        print("ERROR create table patient_hist_form_item,\n\terr=" + str(err))

    print(str(datetime.today()) + " : END of migration v3_6_5_fix_tables_test revision=8a8f1ca60adc")


def downgrade():
    """
    No-op by design.

    This migration is intentionally irreversible per the organization's
    forward-only policy. It includes destructive operations and/or renames
    that cannot be safely undone. To roll back, restore a verified backup
    taken before revision 8a8f1ca60adc.
    """
    print("downgrade skipped: irreversible migration 8a8f1ca60adc (forward-only policy)")
